import torch
from typing import List
from physics import Vector3, Object
from mechanics import universal_gravitation_response, detect_collisions, resolve_elastic_collision


class World:
    """Physics world that simulates objects over time"""

    def __init__(self, dt=0.016, device='cpu'):
        """
        Args:
            dt: Time step in seconds (default 0.016 = ~60fps)
            device: 'cpu' or 'cuda' for GPU acceleration
        """
        self.objects: List[Object] = []
        self.dt = dt
        self.device = device
        self.time = 0.0
        self.recordings = []  # For storing simulation history

    def add_object(self, obj: Object):
        """Add an object to the world"""
        self.objects.append(obj)

    def remove_object(self, obj_id: str):
        """Remove an object by ID"""
        self.objects = [obj for obj in self.objects if obj.id != obj_id]

    def get_object(self, obj_id: str):
        """Get an object by ID"""
        for obj in self.objects:
            if obj.id == obj_id:
                return obj
        return None

    def step(self):
        """Advance simulation by one time step"""
        # Apply gravitational forces between all pairs
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                universal_gravitation_response(self.objects[i], self.objects[j])

        # Detect and resolve collisions
        collisions = detect_collisions(self.objects)
        for obj_a, obj_b in collisions:
            resolve_elastic_collision(obj_a, obj_b, self.dt)

        # Update all objects
        for obj in self.objects:
            obj.update(self.dt)

        self.time += self.dt

    def simulate(self, duration, record=False):
        """
        Run simulation for a given duration

        Args:
            duration: Simulation duration in seconds
            record: Whether to record object states
        """
        steps = int(duration / self.dt)
        for _ in range(steps):
            if record:
                self.record_state()
            self.step()

    def record_state(self):
        """Record current state of all objects"""
        state = {
            'time': self.time,
            'objects': [obj.deep_copy() for obj in self.objects]
        }
        self.recordings.append(state)

    def get_state(self):
        """Get current state of all objects for rendering"""
        return {
            'time': self.time,
            'objects': [obj.flatten() for obj in self.objects]
        }

    def reset(self):
        """Reset simulation"""
        self.time = 0.0
        self.recordings = []
        # Reset all object states
        for obj in self.objects:
            obj.velocity = Vector3(0, 0, 0, device=self.device)
            obj.force = Vector3(0, 0, 0, device=self.device)

    def __repr__(self):
        return f"World(objects={len(self.objects)}, time={self.time:.3f}s, dt={self.dt}s)"
