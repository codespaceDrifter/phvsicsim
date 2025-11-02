import torch

# Disable gradient tracking globally as specified in readme
torch.set_grad_enabled(False)

# Gravitational constant in m^3 kg^-1 s^-2
G = 6.674e-11


class PhysicsSimulation:
    """
    Massively parallel physics simulation using batched tensor operations.
    All objects are represented as tensors with shape (N, ...) where N is the number of objects.
    """

    def __init__(self, n_objects, dt=0.016, device='cpu'):
        """
        Args:
            n_objects: Number of objects in simulation
            dt: Time step in seconds
            device: 'cpu' or 'cuda'
        """
        self.n = n_objects
        self.dt = dt
        self.device = device

        # Object properties - all tensors with batch dimension (N, ...)
        self.positions = torch.zeros((n_objects, 3), dtype=torch.float32, device=device)
        self.velocities = torch.zeros((n_objects, 3), dtype=torch.float32, device=device)
        self.forces = torch.zeros((n_objects, 3), dtype=torch.float32, device=device)
        self.accelerations = torch.zeros((n_objects, 3), dtype=torch.float32, device=device)

        # Scalar properties per object
        self.masses = torch.ones(n_objects, dtype=torch.float32, device=device)
        self.radii = torch.ones(n_objects, dtype=torch.float32, device=device)
        self.restitution = torch.ones(n_objects, dtype=torch.float32, device=device)
        self.density = torch.ones(n_objects, dtype=torch.float32, device=device)

        # Additional forces (user-controlled)
        self.magic_forces = torch.zeros((n_objects, 3), dtype=torch.float32, device=device)

        # Object metadata (not used in computation)
        self.ids = [f"obj_{i}" for i in range(n_objects)]
        self.colors = ["#ffffff"] * n_objects

        self.time = 0.0

    def set_object(self, idx, position=None, velocity=None, mass=None, radius=None,
                   color=None, obj_id=None, restitution=None):
        """Set properties for a specific object"""
        if position is not None:
            self.positions[idx] = torch.tensor(position, dtype=torch.float32, device=self.device)
        if velocity is not None:
            self.velocities[idx] = torch.tensor(velocity, dtype=torch.float32, device=self.device)
        if mass is not None:
            self.masses[idx] = mass
        if radius is not None:
            self.radii[idx] = radius
        if restitution is not None:
            self.restitution[idx] = restitution
        if color is not None:
            self.colors[idx] = color
        if obj_id is not None:
            self.ids[idx] = obj_id

    @torch.compile
    def compute_gravitational_forces(self):
        """
        Compute gravitational forces between all pairs of objects.
        Uses pairwise distance matrix for vectorized computation.
        Result is added to self.forces tensor.
        """
        # Expand positions for broadcasting: (N, 1, 3) and (1, N, 3)
        pos_i = self.positions.unsqueeze(1)  # (N, 1, 3)
        pos_j = self.positions.unsqueeze(0)  # (1, N, 3)

        # Pairwise displacement vectors: delta[i,j] = pos[j] - pos[i]
        delta = pos_j - pos_i  # (N, N, 3)

        # Pairwise distances squared
        dist_sq = torch.sum(delta ** 2, dim=2)  # (N, N)

        # Avoid self-interaction and division by zero
        # Add small epsilon to diagonal
        dist_sq = dist_sq + torch.eye(self.n, device=self.device) * 1e-10

        # Distance
        dist = torch.sqrt(dist_sq)  # (N, N)

        # Pairwise masses: mass[i,j] = mass[i] * mass[j]
        mass_i = self.masses.unsqueeze(1)  # (N, 1)
        mass_j = self.masses.unsqueeze(0)  # (1, N)
        mass_products = mass_i * mass_j  # (N, N)

        # Force magnitudes: F[i,j] = G * m[i] * m[j] / r[i,j]^2
        force_mag = G * mass_products / dist_sq  # (N, N)

        # Unit direction vectors
        directions = delta / dist.unsqueeze(2)  # (N, N, 3)

        # Force vectors: F[i,j] = force_mag[i,j] * direction[i,j]
        force_vectors = force_mag.unsqueeze(2) * directions  # (N, N, 3)

        # Zero out self-interaction
        mask = torch.eye(self.n, device=self.device, dtype=torch.bool)
        force_vectors[mask] = 0

        # Sum forces on each object: forces[i] = sum_j F[i,j]
        gravitational_forces = torch.sum(force_vectors, dim=1)  # (N, 3)

        # Add to total forces
        self.forces = self.forces + gravitational_forces

    @torch.compile
    def detect_collisions(self):
        """
        Detect collisions using sphere-sphere collision detection.
        Returns mask of shape (N, N) where mask[i,j] = True if i and j collide.
        """
        # Pairwise positions
        pos_i = self.positions.unsqueeze(1)  # (N, 1, 3)
        pos_j = self.positions.unsqueeze(0)  # (1, N, 3)

        # Pairwise distances
        delta = pos_j - pos_i
        dist = torch.sqrt(torch.sum(delta ** 2, dim=2))  # (N, N)

        # Sum of radii
        radii_i = self.radii.unsqueeze(1)  # (N, 1)
        radii_j = self.radii.unsqueeze(0)  # (1, N)
        radii_sum = radii_i + radii_j  # (N, N)

        # Collision if distance < sum of radii
        collision_mask = dist < radii_sum

        # Remove self-collisions
        collision_mask = collision_mask & ~torch.eye(self.n, device=self.device, dtype=torch.bool)

        return collision_mask

    @torch.compile
    def resolve_collisions(self):
        """
        Resolve all collisions using elastic collision physics.
        Handles multiple simultaneous collisions.
        """
        collision_mask = self.detect_collisions()

        if not collision_mask.any():
            return

        # Get pairs of colliding objects
        i_indices, j_indices = torch.where(collision_mask)

        # Only process each pair once (i < j)
        pair_mask = i_indices < j_indices
        i_indices = i_indices[pair_mask]
        j_indices = j_indices[pair_mask]

        if len(i_indices) == 0:
            return

        # Get properties for colliding pairs
        pos_i = self.positions[i_indices]  # (M, 3) where M is number of collisions
        pos_j = self.positions[j_indices]
        vel_i = self.velocities[i_indices]
        vel_j = self.velocities[j_indices]
        mass_i = self.masses[i_indices]  # (M,)
        mass_j = self.masses[j_indices]
        rest_i = self.restitution[i_indices]
        rest_j = self.restitution[j_indices]

        # Step back to prevent overlap
        self.positions[i_indices] = pos_i - vel_i * self.dt * 1.3
        self.positions[j_indices] = pos_j - vel_j * self.dt * 1.3

        # Elastic collision formula
        delta_pos = pos_j - pos_i  # (M, 3)
        delta_vel = vel_i - vel_j  # (M, 3)

        dist_sq = torch.sum(delta_pos ** 2, dim=1, keepdim=True)  # (M, 1)
        dist_sq = torch.clamp(dist_sq, min=1e-10)  # Avoid division by zero

        # Dot product
        dot_prod = torch.sum(delta_vel * delta_pos, dim=1, keepdim=True)  # (M, 1)

        # Coefficient of restitution (minimum of the two objects)
        restitution = torch.minimum(rest_i, rest_j).unsqueeze(1)  # (M, 1)

        # Mass factors
        total_mass = mass_i + mass_j
        factor_i = (2 * mass_j / total_mass).unsqueeze(1)  # (M, 1)
        factor_j = (2 * mass_i / total_mass).unsqueeze(1)  # (M, 1)

        # Update velocities
        vel_change_i = factor_i * (dot_prod / dist_sq) * delta_pos * restitution
        vel_change_j = factor_j * (dot_prod / dist_sq) * delta_pos * restitution

        self.velocities[i_indices] = vel_i - vel_change_i
        self.velocities[j_indices] = vel_j + vel_change_j

    @torch.compile
    def update_step(self):
        """Perform one physics update step"""
        # Reset forces
        self.forces.zero_()

        # Compute all forces
        self.compute_gravitational_forces()

        # Add magic forces (user-controlled)
        self.forces = self.forces + self.magic_forces

        # Clamp small forces to zero
        self.forces = torch.where(torch.abs(self.forces) < 1e-6,
                                   torch.zeros_like(self.forces),
                                   self.forces)

        # F = ma => a = F/m
        self.accelerations = self.forces / self.masses.unsqueeze(1)

        # Resolve collisions (modifies velocities)
        self.resolve_collisions()

        # Update velocities: v = v + a*dt
        self.velocities = self.velocities + self.accelerations * self.dt

        # Update positions: x = x + v*dt
        self.positions = self.positions + self.velocities * self.dt

        # Update time
        self.time += self.dt

    def simulate(self, n_steps):
        """Run simulation for n steps"""
        for _ in range(n_steps):
            self.update_step()

    def get_state(self):
        """Get current state for visualization/analysis"""
        return {
            'time': self.time,
            'positions': self.positions.cpu().numpy(),
            'velocities': self.velocities.cpu().numpy(),
            'masses': self.masses.cpu().numpy(),
            'radii': self.radii.cpu().numpy(),
            'ids': self.ids,
            'colors': self.colors
        }

    def reset(self):
        """Reset simulation to initial state"""
        self.positions.zero_()
        self.velocities.zero_()
        self.forces.zero_()
        self.accelerations.zero_()
        self.magic_forces.zero_()
        self.time = 0.0
