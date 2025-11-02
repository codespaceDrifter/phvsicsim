# Python Physics Backend

Massively parallel physics simulation using PyTorch tensor operations.

## Features

- **Batched tensor operations**: All objects simulated in parallel using tensors with shape (N, 3)
- **GPU acceleration**: Can run on CUDA devices for massive speedups
- **JIT compilation**: Uses `torch.compile` for optimized performance
- **No gradients**: Disabled globally for maximum performance
- **Vectorized physics**:
  - Universal gravitation between all object pairs
  - Elastic collision detection and resolution
  - Customizable forces

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from physics_sim import PhysicsSimulation

# Create simulation with 1000 objects
sim = PhysicsSimulation(n_objects=1000, dt=0.016, device='cuda')

# Set up objects
for i in range(1000):
    sim.set_object(i,
                   position=[random.random()*100, random.random()*100, random.random()*100],
                   velocity=[random.random()-0.5, random.random()-0.5, random.random()-0.5],
                   mass=random.random()*100 + 1,
                   radius=0.5)

# Run simulation
sim.simulate(n_steps=1000)

# Get current state
state = sim.get_state()
print(f"Simulated {state['time']:.2f} seconds")
```

## Running Tests

```bash
pytest python-back/tests/ -v
```

## Architecture

All object properties are stored as batched tensors:

- `positions`: (N, 3) - positions of all objects
- `velocities`: (N, 3) - velocities of all objects
- `forces`: (N, 3) - forces on all objects
- `masses`: (N,) - masses of all objects
- `radii`: (N,) - radii of all objects (for collision detection)

Physics computations are fully vectorized across the batch dimension for maximum parallelization.
