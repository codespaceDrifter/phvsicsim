package common

import (
	"math"
)

// Create a rectangular prism (box) mesh
func NewBox(width, height, depth float32) *Mesh {
	// Define the 8 vertices of the box
	vertices := []Vector3{
		{X: -width / 2, Y: -height / 2, Z: -depth / 2}, // 0
		{X: width / 2, Y: -height / 2, Z: -depth / 2},  // 1
		{X: width / 2, Y: height / 2, Z: -depth / 2},   // 2
		{X: -width / 2, Y: height / 2, Z: -depth / 2},  // 3
		{X: -width / 2, Y: -height / 2, Z: depth / 2},  // 4
		{X: width / 2, Y: -height / 2, Z: depth / 2},   // 5
		{X: width / 2, Y: height / 2, Z: depth / 2},    // 6
		{X: -width / 2, Y: height / 2, Z: depth / 2},   // 7
	}

	// Define the 12 triangles (6 faces, 2 triangles per face) using indices
	indices := [][3]int{
		// Front face
		{0, 1, 2},
		{0, 2, 3},
		// Back face
		{4, 6, 5},
		{4, 7, 6},
		// Top face
		{0, 5, 1},
		{0, 4, 5},
		// Right face
		{1, 5, 6},
		{1, 6, 2},
		// Left face
		{0, 3, 7},
		{0, 7, 4},
		// Bottom face
		{2, 6, 7},
		{2, 7, 3},
	}

	mesh := NewMesh(vertices, indices)
	return mesh
}

// Create a sphere mesh (approximated with triangles)
func NewSphere(radius float32, subdivisions int) *Mesh {
	if subdivisions < 0 {
		subdivisions = 0
	}
	if subdivisions > 4 {
		subdivisions = 4 // Cap subdivisions to prevent excessive triangle count
	}

	// Start with an icosahedron (20 faces, 12 vertices)
	// Golden ratio for icosahedron
	phi := float32(1.618033988749895) //golden ratio

	// Initial 12 vertices of icosahedron
	vertices := []Vector3{
		{X: -1, Y: phi, Z: 0},  // 0
		{X: 1, Y: phi, Z: 0},   // 1
		{X: -1, Y: -phi, Z: 0}, // 2
		{X: 1, Y: -phi, Z: 0},  // 3
		{X: 0, Y: -1, Z: phi},  // 4
		{X: 0, Y: 1, Z: phi},   // 5
		{X: 0, Y: -1, Z: -phi}, // 6
		{X: 0, Y: 1, Z: -phi},  // 7
		{X: phi, Y: 0, Z: -1},  // 8
		{X: phi, Y: 0, Z: 1},   // 9
		{X: -phi, Y: 0, Z: -1}, // 10
		{X: -phi, Y: 0, Z: 1},  // 11
	}

	// Initial 20 faces of icosahedron
	faces := [][3]int{
		{0, 11, 5}, {0, 5, 1}, {0, 1, 7}, {0, 7, 10}, {0, 10, 11},
		{1, 5, 9}, {5, 11, 4}, {11, 10, 2}, {10, 7, 6}, {7, 1, 8},
		{3, 9, 4}, {3, 4, 2}, {3, 2, 6}, {3, 6, 8}, {3, 8, 9},
		{4, 9, 5}, {2, 4, 11}, {6, 2, 10}, {8, 6, 7}, {9, 8, 1},
	}

	// Subdivide the icosahedron
	for i := 0; i < subdivisions; i++ {
		newFaces := make([][3]int, 0, len(faces)*3)
		for _, face := range faces {
			// Get the three vertices of the face
			v1 := vertices[face[0]]
			v2 := vertices[face[1]]
			v3 := vertices[face[2]]

			// Calculate midpoints
			m1 := Vector3{
				X: (v1.X + v2.X) / 2,
				Y: (v1.Y + v2.Y) / 2,
				Z: (v1.Z + v2.Z) / 2,
			}
			m2 := Vector3{
				X: (v2.X + v3.X) / 2,
				Y: (v2.Y + v3.Y) / 2,
				Z: (v2.Z + v3.Z) / 2,
			}
			m3 := Vector3{
				X: (v3.X + v1.X) / 2,
				Y: (v3.Y + v1.Y) / 2,
				Z: (v3.Z + v1.Z) / 2,
			}

			// Add new vertices
			vertices = append(vertices, m1, m2, m3)
			m1Idx := len(vertices) - 3
			m2Idx := len(vertices) - 2
			m3Idx := len(vertices) - 1

			// Add new faces
			newFaces = append(newFaces,
				[3]int{face[0], m1Idx, m3Idx},
				[3]int{m1Idx, face[1], m2Idx},
				[3]int{m3Idx, m2Idx, face[2]},
				[3]int{m1Idx, m2Idx, m3Idx},
			)
		}
		faces = newFaces
	}

	// Normalize vertices to unit sphere and scale by radius
	for i := range vertices {
		// Calculate length
		length := float32(
			float32(math.Sqrt(float64(vertices[i].X*vertices[i].X +
				vertices[i].Y*vertices[i].Y +
				vertices[i].Z*vertices[i].Z))),
		)
		// Normalize and scale
		vertices[i].X = vertices[i].X / length * radius
		vertices[i].Y = vertices[i].Y / length * radius
		vertices[i].Z = vertices[i].Z / length * radius
	}

	mesh := NewMesh(vertices, faces)
	return mesh
}
