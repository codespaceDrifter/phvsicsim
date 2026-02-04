"""
Physics object with full rotational dynamics.
Uses rotation matrices for orientation representation.
"""
import torch
from mesh import Mesh
import config


class Obj:
    def __init__(self, obj_id: str, color: str, mesh: Mesh, density: float,
                 position: torch.Tensor, velocity: torch.Tensor,
                 hinge_point: torch.Tensor | None = None):
        """
        Args:
            position: (3,) tensor - center of mass position
            velocity: (3,) tensor - linear velocity
            hinge_point: (3,) tensor - optional, hinge position in body frame (relative to center of mass)
        """
        self.id = obj_id
        self.color = color
        self.mesh = mesh
        # (3,) hinge position in body frame, None if free body
        self.hinge_point = hinge_point

        # Linear dynamics - all (3,) tensors
        self.position = position
        self.velocity = velocity
        self.acceleration = torch.zeros(3, device=config.device)
        self.force = torch.zeros(3, device=config.device)

        # use: mesh.triangles @ self.rotation.T (row vectors need transpose)
        # ax, ay, az 
        # bx, by, bz 
        # cx, cy, cz
        # @
        # transposed (what you actually matmul with row vectors):
        # xx, xy, xz   ← where body x goes
        # yx, yy, yz   ← where body y goes
        # zx, zy, zz   ← where body z goes

        self.rotation = torch.eye(3, device=config.device)
        # (3,) angular velocity - direction = axis through center of mass, magnitude = speed (rad/s)
        self.angular_velocity = torch.zeros(3, device=config.device)
        # (3,) angular acceleration - same format as angular velocity
        self.angular_acceleration = torch.zeros(3, device=config.device)
        # (3,) torque - same format, τ = r × F
        self.torque = torch.zeros(3, device=config.device)

        # Scalars
        self.density = density
        self.mass = mesh.volume * density
        # bounciness for collision
        self.restitution = 1.0

        # (3, 3) inertia tensor in body frame
        # rotational equivalent of mass: τ = I @ α (like F = m * a)
        # diagonal = resistance to spin around each axis
        # off-diagonal = coupling (torque around X can cause spin in Y/Z for asymmetric shapes)
        #
        #         τx      τy      τz     (torque applied around)
        #      ┌──────┬──────┬──────┐
        #  αx  │ Ixx  │ Ixy  │ Ixz  │
        #  αy  │ Iyx  │ Iyy  │ Iyz  │   (angular acceleration result)
        #  αz  │ Izx  │ Izy  │ Izz  │
        #      └──────┴──────┴──────┘
        self.inertia_body = self._compute_inertia_tensor()
        # inverse used to solve α = I⁻¹ @ τ
        self.inertia_body_inv = torch.inverse(self.inertia_body)

    def _compute_inertia_tensor(self):
        """
        Exact inertia tensor by summing tetrahedra (each triangle + origin).

        For each point mass at (x,y,z) with mass m:
            Ixx = m(y² + z²)     (distance² from X axis)
            Iyy = m(x² + z²)     (distance² from Y axis)
            Izz = m(x² + y²)     (distance² from Z axis)
            Ixy = -mxy, Ixz = -mxz, Iyz = -myz  (coupling terms)

        For tetrahedron with vertex at origin, the /10 factor comes from
        integrating r² over the tetrahedral volume.
        """
        tris = self.mesh.triangles  # (num_tris, 3, 3)
        I = torch.zeros((3, 3), device=config.device)

        for i in range(tris.shape[0]):
            a, b, c = tris[i, 0], tris[i, 1], tris[i, 2]

            # tetrahedron volume (signed) - origin is 4th vertex
            vol = torch.dot(a, torch.cross(b, c)) / 6.0

            # covariance matrix of vertices: sum of outer products
            # (3, 3)
            cov = torch.outer(a, a) + torch.outer(b, b) + torch.outer(c, c)
            cov = cov + torch.outer(a, b) + torch.outer(b, a)
            cov = cov + torch.outer(a, c) + torch.outer(c, a)
            cov = cov + torch.outer(b, c) + torch.outer(c, b)

            # inertia from covariance: I = trace(cov)*identity - cov
            # this gives Ixx = Σ(y² + z²), Ixy = -Σxy, etc.
            trace = cov[0, 0] + cov[1, 1] + cov[2, 2]
            I_tet = torch.eye(3, device=config.device) * trace - cov

            # scale by density * volume / 20 (tetrahedron integration factor)
            I_tet = I_tet * self.density * torch.abs(vol) / 20.0
            I = I + I_tet

        # clamp diagonal to avoid zero inertia
        min_inertia = 1e-6
        I[0, 0] = torch.clamp(I[0, 0], min=min_inertia)
        I[1, 1] = torch.clamp(I[1, 1], min=min_inertia)
        I[2, 2] = torch.clamp(I[2, 2], min=min_inertia)

        return I

    def get_inertia_world(self):
        """Get inertia tensor in world frame: I_world = R * I_body * R^T"""
        # (3, 3)
        return self.rotation @ self.inertia_body @ self.rotation.T

    def get_inertia_world_inv(self):
        """Get inverse inertia tensor in world frame."""
        # (3, 3)
        return self.rotation @ self.inertia_body_inv @ self.rotation.T

    def get_inertia_about_point(self, point: torch.Tensor):
        """
        Get inertia tensor about arbitrary point using parallel axis theorem.

        I_point = I_cm + m * (|d|²·I - d⊗d)

        where d = vector from center of mass to point.

        Args:
            point: (3,) position in body frame

        Returns: (3, 3) inertia tensor about that point
        """
        d = point  # point is relative to center of mass (which is at body origin)
        d_sq = torch.dot(d, d)
        # parallel axis shift: m * (|d|²·I - d⊗d)
        shift = self.mass * (d_sq * torch.eye(3, device=config.device) - torch.outer(d, d))
        return self.inertia_body + shift

    def get_inertia_about_hinge(self):
        """
        Get inertia tensor about hinge point (if set).
        Uses parallel axis theorem.

        Returns: (3, 3) inertia tensor about hinge, or I_body if no hinge
        """
        if self.hinge_point is None:
            return self.inertia_body
        return self.get_inertia_about_point(self.hinge_point)

    def update(self, dt: float):
        """Semi-implicit Euler integration for linear and angular dynamics."""
        # Clamp small forces/torques
        self.force = torch.where(torch.abs(self.force) < 1e-6,
                                 torch.zeros_like(self.force), self.force)
        self.torque = torch.where(torch.abs(self.torque) < 1e-6,
                                  torch.zeros_like(self.torque), self.torque)

        # Linear: F = ma
        # (3,)
        self.acceleration = self.force / self.mass
        # (3,)
        self.velocity = self.velocity + self.acceleration * dt
        # (3,)
        self.position = self.position + self.velocity * dt

        # Angular: tau = I * alpha  =>  alpha = I^-1 * tau
        # (3, 3)
        I_inv = self.get_inertia_world_inv()
        # (3,)
        self.angular_acceleration = I_inv @ self.torque
        # (3,)
        self.angular_velocity = self.angular_velocity + self.angular_acceleration * dt

        # Update rotation matrix using angular velocity
        # R_new = R * exp(omega * dt) ≈ R * (I + [omega]_x * dt) for small dt
        # (3, 3)
        omega_skew = skew_symmetric(self.angular_velocity * dt)
        # (3, 3)
        delta_rot = torch.eye(3, device=config.device) + omega_skew
        # (3, 3)
        self.rotation = self.rotation @ delta_rot

        # Re-orthonormalize rotation matrix to prevent drift
        self.rotation = orthonormalize(self.rotation)

        # Reset forces and torques
        self.force = torch.zeros_like(self.force)
        self.torque = torch.zeros_like(self.torque)

    def step_back(self, dt: float):
        """Move backwards after collision (both linear and angular)."""
        self.position = self.position - self.velocity * 1.3 * dt
        # Reverse rotation
        omega_skew = skew_symmetric(-self.angular_velocity * 1.3 * dt)
        delta_rot = torch.eye(3, device=config.device) + omega_skew
        self.rotation = self.rotation @ delta_rot
        self.rotation = orthonormalize(self.rotation)

    def apply_force_at_point(self, force: torch.Tensor, world_point: torch.Tensor):
        """
        Apply a force at a specific world-space point.
        This generates both linear force and torque.

        Args:
            force: (3,) force vector in world frame
            world_point: (3,) point of application in world frame
        """
        # Linear force
        self.force = self.force + force

        # Torque = r × F where r is vector from center of mass to point
        # (3,)
        r = world_point - self.position
        # (3,)
        torque = torch.cross(r, force)
        self.torque = self.torque + torque

    def get_world_vertices(self):
        """
        Get mesh vertices transformed to world space.
        Returns: (N, 3) tensor of world-space vertices
        """
        # (N, 3) body-space vertices
        verts = self.mesh.vertices
        # Rotate then translate: v_world = R @ v_body + position
        # (N, 3) = (N, 3) @ (3, 3)^T + (3,)
        return verts @ self.rotation.T + self.position

    def get_point_velocity(self, world_point: torch.Tensor):
        """
        Get velocity of a point on the rigid body in world space.
        v_point = v_cm + omega × r

        Args:
            world_point: (3,) point in world frame

        Returns: (3,) velocity at that point
        """
        # (3,)
        r = world_point - self.position
        # (3,)
        return self.velocity + torch.cross(self.angular_velocity, r)


def skew_symmetric(v: torch.Tensor) -> torch.Tensor:
    """
    Create skew-symmetric matrix from vector for cross product.
    [v]_x such that [v]_x @ u = v × u

    Args:
        v: (3,) vector

    Returns: (3, 3) skew-symmetric matrix
    """
    zero = torch.zeros(1, device=v.device, dtype=v.dtype)
    # (3, 3)
    return torch.stack([
        torch.cat([zero, -v[2:3], v[1:2]]),
        torch.cat([v[2:3], zero, -v[0:1]]),
        torch.cat([-v[1:2], v[0:1], zero])
    ])


def orthonormalize(R: torch.Tensor) -> torch.Tensor:
    """
    Re-orthonormalize a rotation matrix using Gram-Schmidt.
    Prevents numerical drift from accumulating.

    Args:
        R: (3, 3) approximately orthonormal matrix

    Returns: (3, 3) proper rotation matrix
    """
    # columns are body axes in world coords
    # (3,)
    x = R[:, 0]
    y = R[:, 1]

    # Gram-Schmidt
    x = x / torch.norm(x)
    y = y - torch.dot(x, y) * x
    y = y / torch.norm(y)
    z = torch.cross(x, y)

    # (3, 3)
    return torch.stack([x, y, z], dim=1)
