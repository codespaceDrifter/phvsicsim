"""
Three-body simulation (matches Go version exactly).
"""
import torch
import config

from world import World
from obj import Obj
from shapes import sphere
from recording import Recording


def simulate_three_body():
    print(f"Device: {config.device}")

    # Create world
    world = World('threeBody', time_step=0.01)

    # Alpha Centauri A
    acen_a = Obj(
        'aCenA', '#ffe599',
        sphere(40, 1),
        5e8,
        torch.tensor([0., 0., 0.], device=config.device),
        torch.tensor([0., 0., -5.], device=config.device)
    )
    acen_a.restitution = 0.8

    # Alpha Centauri B
    acen_b = Obj(
        'aCenB', '#ffa64d',
        sphere(25, 1),
        3e8,
        torch.tensor([300., 0., 0.], device=config.device),
        torch.tensor([-3., 0., 0.], device=config.device)
    )
    acen_b.restitution = 0.8

    # Proxima
    proxima = Obj(
        'proxima', '#ff4d4d',
        sphere(30, 1),
        6e8,
        torch.tensor([-300., 0., 0.], device=config.device),
        torch.tensor([0., 0., 2.], device=config.device)
    )
    proxima.restitution = 0.8

    # Trisolaris (planet)
    trisolaris = Obj(
        'trisolaris', '#3fa9c0',
        sphere(5, 1),
        5500,
        torch.tensor([350., 0., 0.], device=config.device),
        torch.tensor([1., 0., 0.], device=config.device)
    )
    trisolaris.restitution = 0.8

    world.add_object(acen_a)
    world.add_object(acen_b)
    world.add_object(proxima)
    world.add_object(trisolaris)

    print(f"World has {len(world.objects)} objects")

    # Create and run recording (matches Go: 0.5 seconds per frame, 3000 seconds total)
    # (batch_size, 3)
    recording = Recording('threeBody', world, seconds_per_frame=0.5, end_seconds=3000)
    recording.simulate()


if __name__ == '__main__':
    simulate_three_body()
