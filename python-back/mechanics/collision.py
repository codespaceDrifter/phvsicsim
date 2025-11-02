import torch
from physics.vector3 import Vector3


@torch.compile
def resolve_elastic_collision(obj_a, obj_b, dt):
    """
    Resolve elastic collision between two objects.
    Uses conservation of momentum and energy for elastic collisions.

    Args:
        obj_a: First physics object
        obj_b: Second physics object
        dt: Time step (used for stepping back)
    """
    # Step both objects back to prevent overlap
    obj_a.step_back(dt)
    obj_b.step_back(dt)

    # Get masses
    m1 = obj_a.mass
    m2 = obj_b.mass

    # Get velocities
    v1 = obj_a.velocity
    v2 = obj_b.velocity

    # Calculate new velocities using elastic collision formulas
    # For 3D elastic collision along line of centers
    # v1' = v1 - (2*m2/(m1+m2)) * <v1-v2, x1-x2> / |x1-x2|^2 * (x1-x2)

    # Vector from a to b
    delta_pos = obj_b.position - obj_a.position
    delta_vel = v1 - v2

    # Distance squared
    dist_sq = delta_pos.magnitude_squared()

    if dist_sq == 0:
        return  # Objects at same position

    # Dot product of velocity difference and position difference
    dot_prod = delta_vel.dot(delta_pos)

    # Calculate velocity changes
    factor_a = (2 * m2 / (m1 + m2)) * (dot_prod / dist_sq)
    factor_b = (2 * m1 / (m1 + m2)) * (dot_prod / dist_sq)

    # Apply coefficient of restitution
    restitution = min(obj_a.restitution, obj_b.restitution)

    obj_a.velocity = v1 - delta_pos * factor_a * restitution
    obj_b.velocity = v2 + delta_pos * factor_b * restitution


def detect_collisions(objects):
    """
    Detect all collisions between objects in the list.

    Args:
        objects: List of physics objects

    Returns:
        List of tuples (obj_a, obj_b) representing colliding pairs
    """
    collisions = []

    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if objects[i].aabb_overlap(objects[j]):
                # For now, AABB overlap is sufficient
                # TODO: Add triangle-triangle intersection for precision
                collisions.append((objects[i], objects[j]))

    return collisions
