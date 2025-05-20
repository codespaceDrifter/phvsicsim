package common


type Vector3 struct {
	X float32
	Y float32
	Z float32
}

type Mesh struct {
	Vertices []Vector3 // [v1, v2, v3, v4, ...]
	Indices  [][3]int  // [[0,1,2], [0,2,3], [1,4,5], ...]  // each 3 numbers = one triangle
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

type Object struct {
	ID       string
	Mesh     Mesh
	Position Vector3

	Velocity Vector3

	Density  float32
	Mass     float32
	Friction float32

	CenterOfMass Vector3
}

func (o *Object) Flatten() (string, []float32, []float32, []uint32) {
	v, i := o.Mesh.Flatten()
	return o.ID, []float32{o.Position.X, o.Position.Y, o.Position.Z}, v, i

}

// DeepCopy creates a deep copy of the Object
func (o Object) DeepCopy() Object {
	newObj := Object{
		ID:           o.ID,
		Position:     Vector3{X: o.Position.X, Y: o.Position.Y, Z: o.Position.Z},
		Velocity:     Vector3{X: o.Velocity.X, Y: o.Velocity.Y, Z: o.Velocity.Z},
		Density:      o.Density,
		Mass:         o.Mass,
		Friction:     o.Friction,
		CenterOfMass: Vector3{X: o.CenterOfMass.X, Y: o.CenterOfMass.Y, Z: o.CenterOfMass.Z},
	}

	// Deep copy Mesh.Vertices
	newObj.Mesh.Vertices = make([]Vector3, len(o.Mesh.Vertices))
	copy(newObj.Mesh.Vertices, o.Mesh.Vertices)

	// Deep copy Mesh.Indices
	newObj.Mesh.Indices = make([][3]int, len(o.Mesh.Indices))
	copy(newObj.Mesh.Indices, o.Mesh.Indices)

	return newObj
}


func (o *Object) UpdatePosition(dt float32) {
	o.Position.X += o.Velocity.X * dt

	o.Position.Y += o.Velocity.Y * dt
	o.Position.Z += o.Velocity.Z * dt
}
