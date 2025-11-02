"""
Example simulation demonstrating the physics engine
"""
import torch
from physics_sim import PhysicsSimulation


def three_body_problem():
    """Simulate the classic three-body problem"""
    print("=" * 60)
    print("THREE BODY PROBLEM SIMULATION")
    print("=" * 60)

    sim = PhysicsSimulation(n_objects=3, dt=0.01, device='cpu')

    # Sun-like object at center
    sim.set_object(0,
                   position=[0.0, 0.0, 0.0],
                   velocity=[0.0, 0.0, 0.0],
                   mass=1.989e30,  # Mass of the Sun
                   radius=6.96e8,  # Radius of the Sun
                   color="#FDB813",
                   obj_id="sun")

    # Earth-like object
    sim.set_object(1,
                   position=[1.496e11, 0.0, 0.0],  # 1 AU from Sun
                   velocity=[0.0, 29780.0, 0.0],    # Orbital velocity
                   mass=5.972e24,                   # Mass of Earth
                   radius=6.371e6,                  # Radius of Earth
                   color="#0077be",
                   obj_id="earth")

    # Moon-like object
    sim.set_object(2,
                   position=[1.496e11 + 3.844e8, 0.0, 0.0],  # Earth distance + Moon distance
                   velocity=[0.0, 29780.0 + 1022.0, 0.0],     # Earth velocity + Moon orbital velocity
                   mass=7.342e22,                             # Mass of Moon
                   radius=1.737e6,                            # Radius of Moon
                   color="#888888",
                   obj_id="moon")

    print(f"\nInitial state:")
    print(f"Sun:   pos={sim.positions[0].tolist()}")
    print(f"Earth: pos={sim.positions[1].tolist()}")
    print(f"Moon:  pos={sim.positions[2].tolist()}")

    # Simulate 10 days
    days = 10
    steps_per_day = int(86400 / sim.dt)  # seconds in a day / dt
    total_steps = days * steps_per_day

    print(f"\nSimulating {days} days ({total_steps} steps)...")
    sim.simulate(n_steps=total_steps)

    print(f"\nFinal state after {sim.time:.0f} seconds ({sim.time/86400:.1f} days):")
    print(f"Sun:   pos={sim.positions[0].tolist()}")
    print(f"Earth: pos={sim.positions[1].tolist()}")
    print(f"Moon:  pos={sim.positions[2].tolist()}")

    return sim


def collision_demo():
    """Demonstrate elastic collisions"""
    print("\n" + "=" * 60)
    print("ELASTIC COLLISION DEMONSTRATION")
    print("=" * 60)

    sim = PhysicsSimulation(n_objects=2, dt=0.01, device='cpu')

    # Two objects moving towards each other
    sim.set_object(0,
                   position=[0.0, 0.0, 0.0],
                   velocity=[1.0, 0.0, 0.0],
                   mass=10.0,
                   radius=0.5,
                   restitution=1.0,  # Perfectly elastic
                   color="#ff0000",
                   obj_id="red_ball")

    sim.set_object(1,
                   position=[5.0, 0.0, 0.0],
                   velocity=[-1.0, 0.0, 0.0],
                   mass=10.0,
                   radius=0.5,
                   restitution=1.0,
                   color="#0000ff",
                   obj_id="blue_ball")

    print(f"\nInitial state:")
    print(f"Red ball:  pos={sim.positions[0].tolist()}, vel={sim.velocities[0].tolist()}")
    print(f"Blue ball: pos={sim.positions[1].tolist()}, vel={sim.velocities[1].tolist()}")

    initial_momentum = (sim.masses[0] * sim.velocities[0] +
                       sim.masses[1] * sim.velocities[1])
    print(f"Total momentum: {initial_momentum.tolist()}")

    # Simulate until collision and beyond
    print(f"\nSimulating...")
    sim.simulate(n_steps=500)

    print(f"\nFinal state after {sim.time:.2f} seconds:")
    print(f"Red ball:  pos={sim.positions[0].tolist()}, vel={sim.velocities[0].tolist()}")
    print(f"Blue ball: pos={sim.positions[1].tolist()}, vel={sim.velocities[1].tolist()}")

    final_momentum = (sim.masses[0] * sim.velocities[0] +
                     sim.masses[1] * sim.velocities[1])
    print(f"Total momentum: {final_momentum.tolist()}")
    print(f"Momentum conserved: {torch.allclose(initial_momentum, final_momentum, atol=1e-3)}")

    return sim


def many_objects_demo():
    """Demonstrate performance with many objects"""
    print("\n" + "=" * 60)
    print("MANY OBJECTS PERFORMANCE TEST")
    print("=" * 60)

    n_objects = 100
    print(f"\nSimulating {n_objects} objects...")

    sim = PhysicsSimulation(n_objects=n_objects, dt=0.01, device='cpu')

    # Random initial conditions
    torch.manual_seed(42)
    sim.positions = torch.randn((n_objects, 3)) * 100
    sim.velocities = torch.randn((n_objects, 3)) * 0.1
    sim.masses = torch.rand(n_objects) * 100 + 1
    sim.radii = torch.ones(n_objects) * 0.5

    import time
    start_time = time.time()

    steps = 100
    sim.simulate(n_steps=steps)

    elapsed = time.time() - start_time

    print(f"\nSimulated {steps} steps in {elapsed:.3f} seconds")
    print(f"Performance: {steps/elapsed:.1f} steps/second")
    print(f"Time per step: {elapsed/steps*1000:.2f} ms")

    return sim


if __name__ == "__main__":
    # Run demonstrations
    three_body_problem()
    collision_demo()
    many_objects_demo()

    print("\n" + "=" * 60)
    print("ALL DEMONSTRATIONS COMPLETE!")
    print("=" * 60)
