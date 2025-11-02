import torch
from .vector3 import Vector3
from .mesh import Mesh


class Object:
    """Physics object with position, velocity, and forces"""

    def __init__(self, id, color, mesh, density, position, velocity, device='cpu'):
        self.id = id
        self.color = color
        self.mesh = mesh
        self.position = position if isinstance(position, Vector3) else Vector3(*position, device=device)
        self.velocity = velocity if isinstance(velocity, Vector3) else Vector3(*velocity, device=device)
        self.density = density
        self.device = device

        # Computed properties
        self.mass = mesh.volume * density
        self.restitution = 1.0  # Coefficient of restitution (1.0 = perfectly elastic)
        self.friction = 0.0

        # Dynamic properties
        self.force = Vector3(0, 0, 0, device=device)
        self.acceleration = Vector3(0, 0, 0, device=device)
        self.magic_force = Vector3(0, 0, 0, device=device)  # User-controlled force

        # AABB in world space (computed on demand)
        self.min_aabb_world = Vector3(0, 0, 0, device=device)
        self.max_aabb_world = Vector3(0, 0, 0, device=device)

        # Center of mass (relative to position)
        self.center_of_mass = Vector3(0, 0, 0, device=device)

    def update(self, dt):
        """Update object physics for one timestep"""
        # Clamp small forces
        self.force = self.force.clamp_small()

        # Add magic force (user-controlled)
        self.force = self.force + self.magic_force

        # F = ma => a = F/m
        self.acceleration = self.force / self.mass

        # Update velocity: v = v0 + a*dt
        self.velocity = self.velocity + self.acceleration * dt

        # Update position: x = x0 + v*dt
        self.position = self.position + self.velocity * dt

        # Reset forces for next iteration
        self.force = Vector3(0, 0, 0, device=self.device)

    def apply_force(self, force):
        """Apply a force to the object"""
        self.force = self.force + force

    def deep_copy(self):
        """Create a deep copy of the object"""
        obj = Object(
            self.id,
            self.color,
            self.mesh.deep_copy(),
            self.density,
            Vector3(self.position.x, self.position.y, self.position.z, device=self.device),
            Vector3(self.velocity.x, self.velocity.y, self.velocity.z, device=self.device),
            device=self.device
        )
        obj.restitution = self.restitution
        obj.friction = self.friction
        obj.magic_force = Vector3(self.magic_force.x, self.magic_force.y, self.magic_force.z, device=self.device)
        return obj

    def flatten(self):
        """Return flattened representation for rendering"""
        vertices, indices = self.mesh.flatten()
        return {
            'id': self.id,
            'position': self.position.to_list(),
            'vertices': vertices,
            'indices': indices,
            'color': self.color
        }

    def update_aabb_world(self):
        """Update world-space AABB"""
        self.min_aabb_world = self.position + self.mesh.min_aabb
        self.max_aabb_world = self.position + self.mesh.max_aabb

    def aabb_overlap(self, other):
        """Check if this object's AABB overlaps with another object's AABB"""
        self.update_aabb_world()
        other.update_aabb_world()

        # Check overlap on all three axes
        x_overlap = (self.min_aabb_world.x <= other.max_aabb_world.x and
                     self.max_aabb_world.x >= other.min_aabb_world.x)
        y_overlap = (self.min_aabb_world.y <= other.max_aabb_world.y and
                     self.max_aabb_world.y >= other.min_aabb_world.y)
        z_overlap = (self.min_aabb_world.z <= other.max_aabb_world.z and
                     self.max_aabb_world.z >= other.min_aabb_world.z)

        return x_overlap and y_overlap and z_overlap

    def triangle_overlap(self, other):
        """Check if any triangle of this object intersects with triangles of another object"""
        # First check AABB overlap
        if not self.aabb_overlap(other):
            return False

        # Get world-space vertices
        vertices_a = self.mesh.vertices + self.position.data
        vertices_b = other.mesh.vertices + other.position.data

        # Check triangle-triangle intersection (simplified)
        # TODO: Implement proper triangle-triangle intersection test
        # For now, using AABB as approximation
        return True

    def step_back(self, dt):
        """Step the object backwards (used in collision resolution)"""
        neg_velocity = -self.velocity
        scaled_velocity = neg_velocity * 1.3
        self.position = self.position + scaled_velocity * dt

    def __repr__(self):
        return f"Object(id={self.id}, pos={self.position}, vel={self.velocity}, mass={self.mass:.2f})"
