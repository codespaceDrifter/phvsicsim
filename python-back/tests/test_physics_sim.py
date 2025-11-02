import pytest
import torch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics_sim import PhysicsSimulation


class TestPhysicsSimulation:
    """Test suite for tensor-based physics simulation"""

    def test_initialization(self):
        """Test that simulation initializes correctly"""
        sim = PhysicsSimulation(n_objects=10, dt=0.01)

        assert sim.n == 10
        assert sim.dt == 0.01
        assert sim.positions.shape == (10, 3)
        assert sim.velocities.shape == (10, 3)
        assert sim.masses.shape == (10,)
        assert sim.time == 0.0

    def test_set_object(self):
        """Test setting individual object properties"""
        sim = PhysicsSimulation(n_objects=5)

        sim.set_object(0, position=[1.0, 2.0, 3.0], velocity=[0.1, 0.2, 0.3],
                      mass=10.0, radius=0.5, color="#ff0000", obj_id="test_obj")

        assert torch.allclose(sim.positions[0], torch.tensor([1.0, 2.0, 3.0]))
        assert torch.allclose(sim.velocities[0], torch.tensor([0.1, 0.2, 0.3]))
        assert sim.masses[0] == 10.0
        assert sim.radii[0] == 0.5
        assert sim.colors[0] == "#ff0000"
        assert sim.ids[0] == "test_obj"

    def test_gravity_two_objects(self):
        """Test gravitational force between two objects"""
        sim = PhysicsSimulation(n_objects=2, dt=0.01)

        # Set up two objects separated by 1 meter
        sim.set_object(0, position=[0.0, 0.0, 0.0], mass=1e10)
        sim.set_object(1, position=[1.0, 0.0, 0.0], mass=1e10)

        # Compute gravitational forces
        sim.compute_gravitational_forces()

        # Forces should be equal and opposite
        force_0 = sim.forces[0]
        force_1 = sim.forces[1]

        # Force should be in x direction
        assert force_0[1] == 0.0
        assert force_0[2] == 0.0
        assert force_1[1] == 0.0
        assert force_1[2] == 0.0

        # Forces should be opposite
        assert torch.allclose(force_0, -force_1, atol=1e-5)

        # Force should pull object 0 towards object 1 (positive x)
        assert force_0[0] > 0

    def test_collision_detection(self):
        """Test collision detection between spheres"""
        sim = PhysicsSimulation(n_objects=3)

        # Set up three objects
        sim.set_object(0, position=[0.0, 0.0, 0.0], radius=1.0)
        sim.set_object(1, position=[1.5, 0.0, 0.0], radius=1.0)  # Overlapping
        sim.set_object(2, position=[5.0, 0.0, 0.0], radius=1.0)  # Not overlapping

        collision_mask = sim.detect_collisions()

        # Objects 0 and 1 should collide
        assert collision_mask[0, 1] == True
        assert collision_mask[1, 0] == True

        # Object 2 should not collide with anyone
        assert collision_mask[2, 0] == False
        assert collision_mask[2, 1] == False

    def test_update_step_no_forces(self):
        """Test that objects move with constant velocity when no forces"""
        sim = PhysicsSimulation(n_objects=1, dt=0.1)

        # Set object with velocity but no forces
        sim.set_object(0, position=[0.0, 0.0, 0.0], velocity=[1.0, 0.0, 0.0], mass=1.0)

        initial_pos = sim.positions[0].clone()

        # Run one step
        sim.update_step()

        # Position should change by velocity * dt
        expected_pos = initial_pos + torch.tensor([1.0, 0.0, 0.0]) * 0.1
        assert torch.allclose(sim.positions[0], expected_pos, atol=1e-5)

    def test_conservation_of_momentum_collision(self):
        """Test that momentum is conserved in elastic collisions"""
        sim = PhysicsSimulation(n_objects=2, dt=0.01)

        # Set up two objects moving towards each other
        sim.set_object(0, position=[0.0, 0.0, 0.0], velocity=[1.0, 0.0, 0.0],
                      mass=2.0, radius=0.5, restitution=1.0)
        sim.set_object(1, position=[0.8, 0.0, 0.0], velocity=[-1.0, 0.0, 0.0],
                      mass=2.0, radius=0.5, restitution=1.0)

        # Calculate initial momentum
        initial_momentum = (sim.masses[0] * sim.velocities[0] +
                          sim.masses[1] * sim.velocities[1])

        # Resolve collision
        sim.resolve_collisions()

        # Calculate final momentum
        final_momentum = (sim.masses[0] * sim.velocities[0] +
                         sim.masses[1] * sim.velocities[1])

        # Momentum should be conserved
        assert torch.allclose(initial_momentum, final_momentum, atol=1e-4)

    def test_simulation_runs(self):
        """Test that simulation can run multiple steps without errors"""
        sim = PhysicsSimulation(n_objects=10, dt=0.01)

        # Set up random initial conditions
        torch.manual_seed(42)
        sim.positions = torch.randn((10, 3)) * 10
        sim.velocities = torch.randn((10, 3)) * 0.1
        sim.masses = torch.rand(10) * 100 + 1
        sim.radii = torch.ones(10) * 0.5

        # Should run without errors
        sim.simulate(n_steps=100)

        # Time should advance
        assert sim.time > 0

    def test_get_state(self):
        """Test that get_state returns correct format"""
        sim = PhysicsSimulation(n_objects=3, dt=0.01)

        state = sim.get_state()

        assert 'time' in state
        assert 'positions' in state
        assert 'velocities' in state
        assert 'masses' in state
        assert 'radii' in state
        assert 'ids' in state
        assert 'colors' in state

        assert state['positions'].shape == (3, 3)
        assert state['velocities'].shape == (3, 3)
        assert len(state['ids']) == 3

    def test_reset(self):
        """Test that reset clears simulation state"""
        sim = PhysicsSimulation(n_objects=5, dt=0.01)

        # Set some state
        sim.positions = torch.randn((5, 3))
        sim.velocities = torch.randn((5, 3))
        sim.time = 10.0

        # Reset
        sim.reset()

        # Everything should be zero
        assert torch.all(sim.positions == 0)
        assert torch.all(sim.velocities == 0)
        assert sim.time == 0.0

    def test_magic_forces(self):
        """Test that magic forces are applied correctly"""
        sim = PhysicsSimulation(n_objects=1, dt=0.1)

        sim.set_object(0, position=[0.0, 0.0, 0.0], velocity=[0.0, 0.0, 0.0], mass=1.0)

        # Apply magic force
        sim.magic_forces[0] = torch.tensor([10.0, 0.0, 0.0])

        # Run one step
        sim.update_step()

        # Velocity should change due to acceleration
        # F = ma => a = F/m = 10/1 = 10
        # v = v0 + a*dt = 0 + 10*0.1 = 1.0
        assert torch.allclose(sim.velocities[0, 0], torch.tensor(1.0), atol=1e-5)

    def test_batch_operations(self):
        """Test that operations work correctly on large batches"""
        # Test with larger batch to ensure vectorization works
        sim = PhysicsSimulation(n_objects=100, dt=0.01)

        torch.manual_seed(42)
        sim.positions = torch.randn((100, 3)) * 100
        sim.masses = torch.rand(100) * 1000 + 1
        sim.radii = torch.ones(100) * 0.5

        # Should compute forces for all pairs without error
        sim.compute_gravitational_forces()

        assert sim.forces.shape == (100, 3)

        # Should run simulation
        sim.simulate(n_steps=10)

        assert sim.time > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
