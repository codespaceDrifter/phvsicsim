"""
Physics mechanics with batched tensor operations.
Includes full rotational collision response.
"""
import torch
import config

G = 6.674e-11


def apply_gravity_batched(objects):
    """
    Apply gravitational forces to all objects IN PARALLEL.
    Gravity acts at center of mass, so no torque is generated.

    Args:
        objects: List of Obj
    """
    if len(objects) <= 1:
        return

    N = len(objects)

    # Stack positions and masses
    # (N, 3)
    positions = torch.stack([obj.position for obj in objects])
    # (N,)
    masses = torch.tensor([obj.mass for obj in objects], device=config.device)

    # Compute all pairwise differences: delta[i,j] = pos[j] - pos[i]
    # (N, N, 3)
    delta = positions.unsqueeze(0) - positions.unsqueeze(1)

    # Distance squared
    # (N, N)
    dist_sq = (delta ** 2).sum(dim=2)

    # Avoid self-interaction
    dist_sq = dist_sq + torch.eye(N, device=config.device) * 1e10

    # Distance
    # (N, N)
    dist = torch.sqrt(dist_sq)

    # Direction
    # (N, N, 3)
    direction = delta / dist.unsqueeze(2)

    # Force magnitude: F[i,j] = G * m[i] * m[j] / r[i,j]^2
    # (N, N)
    mass_products = masses.unsqueeze(0) * masses.unsqueeze(1)
    # (N, N)
    force_mags = G * mass_products / dist_sq

    # Force vectors
    # (N, N, 3)
    force_vectors = direction * force_mags.unsqueeze(2)

    # Sum all forces on each object
    # (N, 3)
    total_forces = force_vectors.sum(dim=1)

    # Apply to objects (gravity at center of mass = no torque)
    for i, obj in enumerate(objects):
        obj.force = obj.force + total_forces[i]


def apply_collision_response_with_rotation(obj_a, obj_b, contact_point=None, contact_normal=None):
    """
    Full rigid body collision response with rotation.
    Uses impulse-based collision resolution.

    Args:
        obj_a, obj_b: Obj
        contact_point: (3,) world-space contact point (if None, uses midpoint)
        contact_normal: (3,) collision normal from A to B (if None, uses position difference)
    """

    # Estimate contact point as midpoint between centers
    if contact_point is None:
        # (3,)
        contact_point = (obj_a.position + obj_b.position) / 2.0

    # Estimate contact normal from A to B
    if contact_normal is None:
        # (3,)
        n = obj_b.position - obj_a.position
        n_norm = torch.norm(n)
        if n_norm < 1e-6:
            n = torch.tensor([1.0, 0.0, 0.0], device=config.device)
        else:
            n = n / n_norm
    else:
        n = contact_normal / torch.norm(contact_normal)

    # Vectors from centers of mass to contact point
    # (3,)
    r_a = contact_point - obj_a.position
    # (3,)
    r_b = contact_point - obj_b.position

    # Velocities at contact point
    # (3,)
    v_a = obj_a.get_point_velocity(contact_point)
    # (3,)
    v_b = obj_b.get_point_velocity(contact_point)

    # Relative velocity at contact point
    # (3,)
    v_rel = v_a - v_b

    # Relative velocity along normal
    # scalar
    v_rel_n = torch.dot(v_rel, n)

    # Only resolve if objects are approaching
    if v_rel_n > 0:
        return

    # Coefficient of restitution
    e = torch.sqrt(torch.tensor(obj_a.restitution * obj_b.restitution, device=config.device))

    # Inverse masses
    m_a_inv = 1.0 / obj_a.mass
    m_b_inv = 1.0 / obj_b.mass

    # Inverse inertia tensors in world frame
    # (3, 3)
    I_a_inv = obj_a.get_inertia_world_inv()
    # (3, 3)
    I_b_inv = obj_b.get_inertia_world_inv()

    # Compute impulse denominator
    # For rigid body collision: j = -(1+e) * v_rel_n / (1/m_a + 1/m_b + (I_a^-1 * (r_a × n)) × r_a · n + ...)
    # (3,)
    r_a_cross_n = torch.cross(r_a, n)
    # (3,)
    r_b_cross_n = torch.cross(r_b, n)

    # (3,)
    term_a = torch.cross(I_a_inv @ r_a_cross_n, r_a)
    # (3,)
    term_b = torch.cross(I_b_inv @ r_b_cross_n, r_b)

    # scalar
    denom = m_a_inv + m_b_inv + torch.dot(term_a + term_b, n)

    # Impulse magnitude
    # scalar
    j = -(1.0 + e) * v_rel_n / denom

    # Impulse vector
    # (3,)
    impulse = j * n

    # Apply linear impulse
    # (3,)
    obj_a.velocity = obj_a.velocity + impulse * m_a_inv
    # (3,)
    obj_b.velocity = obj_b.velocity - impulse * m_b_inv

    # Apply angular impulse: Δω = I^-1 * (r × J)
    # (3,)
    angular_impulse_a = I_a_inv @ torch.cross(r_a, impulse)
    # (3,)
    angular_impulse_b = I_b_inv @ torch.cross(r_b, -impulse)

    # (3,)
    obj_a.angular_velocity = obj_a.angular_velocity + angular_impulse_a
    # (3,)
    obj_b.angular_velocity = obj_b.angular_velocity + angular_impulse_b


def apply_collision_response(obj_a, obj_b):
    """
    Wrapper for backwards compatibility.
    Calls the full rotational collision response.
    """
    apply_collision_response_with_rotation(obj_a, obj_b)
