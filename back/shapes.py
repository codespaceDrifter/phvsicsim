"""
Shape generators.
"""
import torch
import numpy as np
from mesh import Mesh
import config


def box(w, h, d):
    """Create box mesh."""
    w2, h2, d2 = w/2, h/2, d/2
    verts = torch.tensor([
        [-w2,-h2,-d2], [w2,-h2,-d2], [w2,h2,-d2], [-w2,h2,-d2],
        [-w2,-h2,d2], [w2,-h2,d2], [w2,h2,d2], [-w2,h2,d2]
    ], device=config.device, dtype=torch.float32)

    indices = torch.tensor([
        [0,1,2],[0,2,3], [4,6,5],[4,7,6], [0,5,1],[0,4,5],
        [1,5,6],[1,6,2], [0,3,7],[0,7,4], [2,6,7],[2,7,3]
    ], device=config.device, dtype=torch.long)

    return Mesh(verts, indices)


def sphere(radius, subdivisions=2):
    """Create sphere mesh via subdivided icosahedron."""
    phi = (1 + np.sqrt(5)) / 2
    verts = np.array([
        [-1,phi,0], [1,phi,0], [-1,-phi,0], [1,-phi,0],
        [0,-1,phi], [0,1,phi], [0,-1,-phi], [0,1,-phi],
        [phi,0,-1], [phi,0,1], [-phi,0,-1], [-phi,0,1]
    ], dtype=np.float32)

    faces = [
        [0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],
        [1,5,9],[5,11,4],[11,10,2],[10,7,6],[7,1,8],
        [3,9,4],[3,4,2],[3,2,6],[3,6,8],[3,8,9],
        [4,9,5],[2,4,11],[6,2,10],[8,6,7],[9,8,1]
    ]

    for _ in range(subdivisions):
        new_faces = []
        for f in faces:
            v1, v2, v3 = verts[f[0]], verts[f[1]], verts[f[2]]
            m1, m2, m3 = (v1+v2)/2, (v2+v3)/2, (v3+v1)/2
            m1_idx, m2_idx, m3_idx = len(verts), len(verts)+1, len(verts)+2
            verts = np.vstack([verts, m1, m2, m3])
            new_faces.extend([
                [f[0],m1_idx,m3_idx], [m1_idx,f[1],m2_idx],
                [m3_idx,m2_idx,f[2]], [m1_idx,m2_idx,m3_idx]
            ])
        faces = new_faces

    # Normalize and scale
    verts = torch.tensor(verts, device=config.device, dtype=torch.float32)
    norms = torch.sqrt((verts**2).sum(dim=1, keepdim=True))
    verts = verts / norms * radius
    indices = torch.tensor(faces, device=config.device, dtype=torch.long)

    return Mesh(verts, indices)


def hollow_rect_frame(width, height, thickness, depth):
    """
    Create a hollow rectangular frame mesh in the XZ plane.
    width: total outer width (X)
    height: total outer height (Z)
    thickness: wall thickness (inward from edge)
    depth: height of the frame (Y)
    """
    w2 = width / 2
    h2 = height / 2
    t = thickness

    all_verts = []
    all_indices = []

    def add_box(cx, cy, cz, sx, sy, sz):
        base = len(all_verts)
        # 8 vertices
        verts = [
            [cx - sx/2, cy - sy/2, cz - sz/2],
            [cx + sx/2, cy - sy/2, cz - sz/2],
            [cx + sx/2, cy + sy/2, cz - sz/2],
            [cx - sx/2, cy + sy/2, cz - sz/2],
            [cx - sx/2, cy - sy/2, cz + sz/2],
            [cx + sx/2, cy - sy/2, cz + sz/2],
            [cx + sx/2, cy + sy/2, cz + sz/2],
            [cx - sx/2, cy + sy/2, cz + sz/2],
        ]
        all_verts.extend(verts)
        # 12 triangles (6 faces)
        indices = [
            [base + 0, base + 1, base + 2], [base + 0, base + 2, base + 3],
            [base + 4, base + 6, base + 5], [base + 4, base + 7, base + 6],
            [base + 0, base + 5, base + 1], [base + 0, base + 4, base + 5],
            [base + 1, base + 5, base + 6], [base + 1, base + 6, base + 2],
            [base + 0, base + 3, base + 7], [base + 0, base + 7, base + 4],
            [base + 2, base + 6, base + 7], [base + 2, base + 7, base + 3],
        ]
        all_indices.extend(indices)

    # Left side
    add_box(-w2 + t/2, 0, 0, t, depth, height)
    # Right side
    add_box(w2 - t/2, 0, 0, t, depth, height)
    # Top side
    add_box(0, 0, -h2 + t/2, width - 2*t, depth, t)
    # Bottom side
    add_box(0, 0, h2 - t/2, width - 2*t, depth, t)

    verts_tensor = torch.tensor(all_verts, device=config.device, dtype=torch.float32)
    indices_tensor = torch.tensor(all_indices, device=config.device, dtype=torch.long)

    return Mesh(verts_tensor, indices_tensor)