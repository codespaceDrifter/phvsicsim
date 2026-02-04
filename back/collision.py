"""
Fully parallelized collision detection using pure tensors.
"""
import torch


def check_collision_pair(obj_a, obj_b) -> bool:
    """
    Check if two objects collide using FULLY PARALLELIZED triangle intersection.

    Returns:
        True if any triangles intersect
    """
    # AABB test first
    min_a = obj_a.mesh.min_aabb + obj_a.position
    max_a = obj_a.mesh.max_aabb + obj_a.position
    min_b = obj_b.mesh.min_aabb + obj_b.position
    max_b = obj_b.mesh.max_aabb + obj_b.position

    overlap = ((min_a <= max_b) & (max_a >= min_b)).all()
    if not overlap:
        return False

    # Get world-space vertices
    verts_a = obj_a.mesh.vertices + obj_a.position  # (Na, 3)
    verts_b = obj_b.mesh.vertices + obj_b.position  # (Nb, 3)

    # Get all triangles
    tris_a = verts_a[obj_a.mesh.indices]  # (Ta, 3, 3)
    tris_b = verts_b[obj_b.mesh.indices]  # (Tb, 3, 3)

    # Check ALL edge-triangle combinations IN PARALLEL
    # For each triangle in A, check all 3 edges against all triangles in B

    num_tris_a = tris_a.shape[0]
    num_tris_b = tris_b.shape[0]

    # Edges of A: (Ta, 3, 2, 3) - for each tri, 3 edges, each edge has 2 points
    edges_a = torch.stack([
        torch.stack([tris_a[:, 0], tris_a[:, 1]], dim=1),  # edge 0-1
        torch.stack([tris_a[:, 1], tris_a[:, 2]], dim=1),  # edge 1-2
        torch.stack([tris_a[:, 2], tris_a[:, 0]], dim=1),  # edge 2-0
    ], dim=1)  # (Ta, 3, 2, 3)

    # Flatten edges: (Ta*3, 2, 3)
    edges_a = edges_a.reshape(-1, 2, 3)
    p0_a = edges_a[:, 0]  # (Ta*3, 3)
    p1_a = edges_a[:, 1]  # (Ta*3, 3)

    # Expand triangles B for broadcasting: (1, Tb, 3, 3)
    tris_b_exp = tris_b.unsqueeze(0)  # (1, Tb, 3, 3)

    # Expand edges A: (Ta*3, 1, 1, 3)
    p0_exp = p0_a.unsqueeze(1).unsqueeze(2)  # (Ta*3, 1, 1, 3)
    p1_exp = p1_a.unsqueeze(1).unsqueeze(2)  # (Ta*3, 1, 1, 3)

    # Check all edge-triangle pairs: (Ta*3, Tb)
    intersects_a_b = segment_intersects_triangles(p0_exp, p1_exp, tris_b_exp)
    if intersects_a_b.any():
        return True

    # Same for edges of B vs triangles of A
    edges_b = torch.stack([
        torch.stack([tris_b[:, 0], tris_b[:, 1]], dim=1),
        torch.stack([tris_b[:, 1], tris_b[:, 2]], dim=1),
        torch.stack([tris_b[:, 2], tris_b[:, 0]], dim=1),
    ], dim=1)
    edges_b = edges_b.reshape(-1, 2, 3)
    p0_b = edges_b[:, 0]
    p1_b = edges_b[:, 1]

    tris_a_exp = tris_a.unsqueeze(0)
    p0_exp = p0_b.unsqueeze(1).unsqueeze(2)
    p1_exp = p1_b.unsqueeze(1).unsqueeze(2)

    intersects_b_a = segment_intersects_triangles(p0_exp, p1_exp, tris_a_exp)
    return intersects_b_a.any()


def segment_intersects_triangles(p0, p1, triangles, eps=1e-6):
    """
    Möller-Trumbore ray-triangle intersection (vectorized).

    Args:
        p0: (*, 1, 1, 3) segment start
        p1: (*, 1, 1, 3) segment end
        triangles: (1, T, 3, 3) triangle vertices

    Returns:
        (*, T) boolean tensor
    """
    v0 = triangles[:, :, 0:1]  # (1, T, 1, 3)
    v1 = triangles[:, :, 1:2]
    v2 = triangles[:, :, 2:3]

    e1 = v1 - v0
    e2 = v2 - v0
    d = p1 - p0

    # Cross product
    pvec = torch.cross(d, e2, dim=-1)
    det = (e1 * pvec).sum(dim=-1)  # (*, T, 1)

    parallel = (det > -eps) & (det < eps)
    inv_det = 1.0 / torch.where(parallel, torch.ones_like(det), det)

    tvec = p0 - v0
    u = (tvec * pvec).sum(dim=-1) * inv_det

    qvec = torch.cross(tvec, e1, dim=-1)
    v = (d * qvec).sum(dim=-1) * inv_det

    t = (e2 * qvec).sum(dim=-1) * inv_det

    # Check bounds
    hit = ~parallel & (u >= 0) & (u <= 1) & (v >= 0) & (u + v <= 1) & (t >= 0) & (t <= 1)

    return hit.squeeze(-1)  # (*, T)
