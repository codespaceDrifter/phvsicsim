package common

type Mesh struct {
	Vertices []Vector3 // [v1, v2, v3, v4, ...]
	Indices  [][3]int  // [[0,1,2], [0,2,3], [1,4,5], ...]  // each 3 numbers = one triangle
	MinAABB  Vector3
	MaxAABB  Vector3
	Volume   float32
}

func NewMesh(vertices []Vector3, indices [][3]int) *Mesh {
	mesh := &Mesh{
		Vertices: vertices,
		Indices:  indices,
	}
	mesh.ComputeAABB()
	mesh.ComputeVolume()
	return mesh
}

func (m *Mesh) Flatten() ([]float32, []uint32) {
	// Pre-allocate arrays
	vertices := make([]float32, len(m.Vertices)*3)
	indices := make([]uint32, len(m.Indices)*3)

	// Flatten vertices
	for i, v := range m.Vertices {
		vertices[i*3] = v.X
		vertices[i*3+1] = v.Y
		vertices[i*3+2] = v.Z
	}

	// Flatten indices
	for i, tri := range m.Indices {
		indices[i*3] = uint32(tri[0])
		indices[i*3+1] = uint32(tri[1])
		indices[i*3+2] = uint32(tri[2])
	}

	return vertices, indices
}

func (m *Mesh) ComputeAABB() {
	if len(m.Vertices) == 0 {
		return
	}

	min := m.Vertices[0]
	max := m.Vertices[0]

	for _, v := range m.Vertices {
		if v.X < min.X { min.X = v.X }
		if v.Y < min.Y { min.Y = v.Y }
		if v.Z < min.Z { min.Z = v.Z }
		if v.X > max.X { max.X = v.X }
		if v.Y > max.Y { max.Y = v.Y }
		if v.Z > max.Z { max.Z = v.Z }
	}

	m.MinAABB = min
	m.MaxAABB = max
}

func (m *Mesh) ComputeVolume()  {
	var volume float32 = 0.0

	for _, tri := range m.Indices {
		a := m.Vertices[tri[0]]
		b := m.Vertices[tri[1]]
		c := m.Vertices[tri[2]]

		// Volume = (1/6) * dot(a, cross(b, c))
		cross := VecCrossVec(b, c)
		v := VecDotVec(a, cross) / 6.0
		if v < 0 {
			v = -v
		}
		volume += v
	}

	m.Volume = volume
}