import torch
from .vector3 import Vector3


class Mesh:
    """Mesh class for 3D objects using PyTorch tensors"""

    def __init__(self, vertices, indices, device='cpu'):
        """
        Args:
            vertices: List of Vector3 or tensor of shape (N, 3)
            indices: List of triangles (each triangle is [i1, i2, i3]) or tensor of shape (M, 3)
        """
        if isinstance(vertices, torch.Tensor):
            self.vertices = vertices
        else:
            vertex_data = [v.data if isinstance(v, Vector3) else torch.tensor(v, dtype=torch.float32)
                          for v in vertices]
            self.vertices = torch.stack(vertex_data).to(device)

        if isinstance(indices, torch.Tensor):
            self.indices = indices
        else:
            self.indices = torch.tensor(indices, dtype=torch.int32, device=device)

        self.device = device
        self._compute_aabb()
        self._compute_volume()

    def _compute_aabb(self):
        """Compute axis-aligned bounding box"""
        self.min_aabb = Vector3(self.vertices.min(dim=0).values)
        self.max_aabb = Vector3(self.vertices.max(dim=0).values)

    def _compute_volume(self):
        """Compute mesh volume (approximation for now)"""
        # Simple bounding box volume for now
        # TODO: Implement proper mesh volume calculation
        size = self.max_aabb.data - self.min_aabb.data
        self.volume = torch.prod(size).item()

    def flatten(self):
        """Return flattened vertex and index arrays"""
        vertices_flat = self.vertices.flatten().tolist()
        indices_flat = self.indices.flatten().tolist()
        return vertices_flat, indices_flat

    def deep_copy(self):
        """Create a deep copy of the mesh"""
        return Mesh(self.vertices.clone(), self.indices.clone(), self.device)

    @staticmethod
    def create_sphere(radius, subdivisions=2, device='cpu'):
        """Create a sphere mesh using icosphere subdivision"""
        # Start with icosahedron
        t = (1.0 + torch.sqrt(torch.tensor(5.0))) / 2.0

        vertices = torch.tensor([
            [-1,  t,  0], [ 1,  t,  0], [-1, -t,  0], [ 1, -t,  0],
            [ 0, -1,  t], [ 0,  1,  t], [ 0, -1, -t], [ 0,  1, -t],
            [ t,  0, -1], [ t,  0,  1], [-t,  0, -1], [-t,  0,  1],
        ], dtype=torch.float32, device=device)

        # Normalize to unit sphere
        vertices = vertices / torch.norm(vertices, dim=1, keepdim=True)
        vertices = vertices * radius

        indices = torch.tensor([
            [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
            [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
            [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
            [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
        ], dtype=torch.int32, device=device)

        return Mesh(vertices, indices, device)

    @staticmethod
    def create_box(width, height, depth, device='cpu'):
        """Create a box mesh"""
        w, h, d = width/2, height/2, depth/2

        vertices = torch.tensor([
            [-w, -h, -d], [ w, -h, -d], [ w,  h, -d], [-w,  h, -d],
            [-w, -h,  d], [ w, -h,  d], [ w,  h,  d], [-w,  h,  d],
        ], dtype=torch.float32, device=device)

        indices = torch.tensor([
            [0, 1, 2], [0, 2, 3],  # front
            [1, 5, 6], [1, 6, 2],  # right
            [5, 4, 7], [5, 7, 6],  # back
            [4, 0, 3], [4, 3, 7],  # left
            [3, 2, 6], [3, 6, 7],  # top
            [4, 5, 1], [4, 1, 0],  # bottom
        ], dtype=torch.int32, device=device)

        return Mesh(vertices, indices, device)
