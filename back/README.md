# PyTorch Physics Backend

Pure tensor-based physics engine with **full GPU parallelization**.

## Features

- ✅ Pure PyTorch tensors (no custom vector classes)
- ✅ Batched gravitational force computation (all N² pairs in parallel)
- ✅ Fully parallelized collision detection (all edges vs all triangles)
- ✅ GPU-accelerated mesh operations
- ✅ API compatible with Go backend

## Files

- `mesh.py` - Triangle mesh (AABB, volume)
- `shapes.py` - Box and sphere generators
- `obj.py` - Object with position/velocity/force tensors
- `collision.py` - **FULLY PARALLEL** triangle intersection detection
- `mechanics.py` - Batched gravity + collision response
- `world.py` - Simulation loop
- `api.py` - Flask API (matches Go backend)
- `example.py` - Demo

## Usage

```python
import torch
from world import World
from obj import Obj
from shapes import sphere

device = 'cuda' if torch.cuda.is_available() else 'cpu'
world = World('sim', time_step=1/60, device=device)

obj = Obj(
    'obj1', '#FF0000',
    sphere(1.0, 2, device),
    1000.0,  # density
    torch.tensor([0., 0., 0.], device=device),  # position
    torch.tensor([1., 0., 0.], device=device)   # velocity
)

world.add_object(obj)

for _ in range(1000):
    world.update()
```

## Run

```bash
python example.py
```

## API

```bash
python api.py
```

Endpoints (same as Go backend):
- `GET /recording/<name>/<chunk>` - Get recording
- `GET /health` - Health check

## Parallelization

### Gravity
All N² force pairs computed simultaneously on GPU:
```python
# (N, N, 3) tensor of all pairwise forces
forces = batched_computation(positions, masses)
```

### Collision
All edge-triangle tests run in parallel:
```python
# (num_edges, num_triangles) boolean tensor
intersects = check_all_pairs_parallel(edges, triangles)
```

## Requirements

```bash
pip install torch flask
```