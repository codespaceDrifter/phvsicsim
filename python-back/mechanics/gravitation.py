import torch
from physics.vector3 import Vector3

# Gravitational constant in m^3 kg^-1 s^-2
G = 6.674e-11


@torch.compile
def universal_gravitation_response(obj_a, obj_b):
    """
    Calculate and apply gravitational force between two objects.
    Uses Newton's law of universal gravitation: F = G * m1 * m2 / r^2

    Args:
        obj_a: First physics object
        obj_b: Second physics object
    """
    # Vector from a to b
    delta = obj_b.position - obj_a.position

    # Distance squared
    dist_sq = delta.magnitude_squared()

    if dist_sq == 0:
        return  # Avoid division by zero

    dist = delta.magnitude()

    # Unit vector from a to b
    direction = delta.normalize()

    # Force magnitude: F = G * m1 * m2 / r^2
    # Use float64 for precision with very small G constant
    force_mag = G * obj_a.mass * obj_b.mass / dist_sq

    # Force vector
    force = direction * force_mag

    # Apply to both objects (equal and opposite)
    obj_a.apply_force(force)
    obj_b.apply_force(-force)
