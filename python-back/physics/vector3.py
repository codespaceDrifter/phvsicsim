import torch

# Disable gradient tracking globally as specified in readme
torch.set_grad_enabled(False)


class Vector3:
    """3D vector using PyTorch tensors for GPU acceleration"""

    def __init__(self, x=0.0, y=0.0, z=0.0, device='cpu'):
        if isinstance(x, torch.Tensor):
            self.data = x
        else:
            self.data = torch.tensor([x, y, z], dtype=torch.float32, device=device)

    @property
    def x(self):
        return self.data[0].item()

    @property
    def y(self):
        return self.data[1].item()

    @property
    def z(self):
        return self.data[2].item()

    def __add__(self, other):
        return Vector3(self.data + other.data)

    def __sub__(self, other):
        return Vector3(self.data - other.data)

    def __mul__(self, scalar):
        return Vector3(self.data * scalar)

    def __truediv__(self, scalar):
        return Vector3(self.data / scalar)

    def __neg__(self):
        return Vector3(-self.data)

    def dot(self, other):
        return torch.dot(self.data, other.data).item()

    def cross(self, other):
        return Vector3(torch.cross(self.data, other.data))

    def magnitude(self):
        return torch.norm(self.data).item()

    def magnitude_squared(self):
        return torch.sum(self.data ** 2).item()

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return self / mag
        return Vector3(0, 0, 0)

    def clamp_small(self, threshold=1e-6):
        """Clamp small values to zero"""
        mask = torch.abs(self.data) < threshold
        clamped = self.data.clone()
        clamped[mask] = 0
        return Vector3(clamped)

    def to_list(self):
        return self.data.tolist()

    def __repr__(self):
        return f"Vector3({self.x:.6f}, {self.y:.6f}, {self.z:.6f})"

    def __eq__(self, other):
        return torch.allclose(self.data, other.data)
