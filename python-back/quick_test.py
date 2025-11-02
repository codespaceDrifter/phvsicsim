"""Quick sanity test without pytest"""
import sys
import traceback

try:
    import torch
    print("✓ PyTorch imported successfully")
    print(f"  PyTorch version: {torch.__version__}")

    from physics_sim import PhysicsSimulation
    print("✓ PhysicsSimulation imported successfully")

    # Test 1: Basic initialization
    print("\nTest 1: Initialization")
    sim = PhysicsSimulation(n_objects=5, dt=0.01)
    assert sim.n == 5
    assert sim.positions.shape == (5, 3)
    print("✓ Initialization works")

    # Test 2: Set object
    print("\nTest 2: Set object properties")
    sim.set_object(0, position=[1, 2, 3], velocity=[0.1, 0.2, 0.3], mass=10.0)
    assert torch.allclose(sim.positions[0], torch.tensor([1.0, 2.0, 3.0]))
    print("✓ Set object works")

    # Test 3: Gravity computation
    print("\nTest 3: Gravity computation")
    sim2 = PhysicsSimulation(n_objects=2, dt=0.01)
    sim2.set_object(0, position=[0, 0, 0], mass=1e10)
    sim2.set_object(1, position=[1, 0, 0], mass=1e10)
    sim2.compute_gravitational_forces()
    assert torch.abs(sim2.forces[0]).sum() > 0  # Some force exists
    print("✓ Gravity computation works")

    # Test 4: Collision detection
    print("\nTest 4: Collision detection")
    sim3 = PhysicsSimulation(n_objects=2)
    sim3.set_object(0, position=[0, 0, 0], radius=1.0)
    sim3.set_object(1, position=[1.5, 0, 0], radius=1.0)  # Overlapping
    collisions = sim3.detect_collisions()
    assert collisions[0, 1] == True
    print("✓ Collision detection works")

    # Test 5: Update step
    print("\nTest 5: Update step")
    sim4 = PhysicsSimulation(n_objects=1, dt=0.1)
    sim4.set_object(0, position=[0, 0, 0], velocity=[1, 0, 0])
    initial_pos = sim4.positions[0].clone()
    sim4.update_step()
    assert not torch.allclose(sim4.positions[0], initial_pos)
    print("✓ Update step works")

    # Test 6: Simulation
    print("\nTest 6: Run simulation")
    sim5 = PhysicsSimulation(n_objects=10, dt=0.01)
    torch.manual_seed(42)
    sim5.positions = torch.randn((10, 3)) * 10
    sim5.velocities = torch.randn((10, 3)) * 0.1
    sim5.masses = torch.rand(10) * 100 + 1
    sim5.simulate(n_steps=10)
    assert sim5.time > 0
    print("✓ Simulation runs successfully")

    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✓")
    print("="*60)

except Exception as e:
    print(f"\n✗ TEST FAILED")
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)
