package common

type Object struct {
	ID       string
	Color    string
	Mesh     *Mesh
	Position Vector3

	MinAABBWorld Vector3
	MaxAABBWorld Vector3

	Velocity     Vector3
	Acceleration Vector3
	Force        Vector3

	Density  float32
	Mass     float32
	Friction float32

	CenterOfMass Vector3

	MagicForce Vector3
}

func NewObject(id string, color string, mesh *Mesh,density float32, position Vector3, velocity Vector3) *Object {
	result := &Object{
		ID:       id,
		Color:    color,
		Mesh:     mesh,
		Position: position,
		Velocity: velocity,
		Density:  density,
	}
	result.Mass = result.Mesh.Volume * result.Density

	return result
}

// DeepCopy creates a deep copy of the Object
func (o *Object) DeepCopy() *Object {
	newObj := &Object{
		ID:           o.ID,
		Color:        o.Color,
		Position:     o.Position,
		MinAABBWorld: o.MinAABBWorld,
		MaxAABBWorld: o.MaxAABBWorld,
		Velocity:     o.Velocity,
		Density:      o.Density,
		Mass:         o.Mass,
		Friction:     o.Friction,
		CenterOfMass: o.CenterOfMass,
		MagicForce:   o.MagicForce,
	}

	// Deep copy Mesh pointer
	if o.Mesh != nil {
		meshCopy := *o.Mesh
		meshCopy.Vertices = make([]Vector3, len(o.Mesh.Vertices))
		copy(meshCopy.Vertices, o.Mesh.Vertices)
		meshCopy.Indices = make([][3]int, len(o.Mesh.Indices))
		copy(meshCopy.Indices, o.Mesh.Indices)
		newObj.Mesh = &meshCopy
	}

	return newObj
}

func (o *Object) Flatten() (string, []float32, []float32, []uint32, string) {
	v, i := o.Mesh.Flatten()
	return o.ID, []float32{o.Position.X, o.Position.Y, o.Position.Z}, v, i, o.Color
}

func (o *Object) Update(dt float32) {

	// change force here
	o.Force = ClampSmall(o.Force)
	o.Force = VecAddVec(o.Force, o.MagicForce)
	o.Acceleration = VecDivScalar(o.Force, o.Mass)
	o.Velocity = VecAddVec(o.Velocity, VecMulScalar(o.Acceleration, dt))
	o.Position = VecAddVec(o.Position, VecMulScalar(o.Velocity, dt))
	o.Force = Vector3{0, 0, 0}
}

// Returns true if this object's AABB overlaps with another object's AABB
func (a *Object) AABBOverlap(b *Object) bool {
	a.MinAABBWorld = VecAddVec(a.Position, a.Mesh.MinAABB)
	a.MaxAABBWorld = VecAddVec(a.Position, a.Mesh.MaxAABB)
	b.MinAABBWorld = VecAddVec(b.Position, b.Mesh.MinAABB)
	b.MaxAABBWorld = VecAddVec(b.Position, b.Mesh.MaxAABB)

	return (a.MinAABBWorld.X <= b.MaxAABBWorld.X && a.MaxAABBWorld.X >= b.MinAABBWorld.X) &&
		(a.MinAABBWorld.Y <= b.MaxAABBWorld.Y && a.MaxAABBWorld.Y >= b.MinAABBWorld.Y) &&
		(a.MinAABBWorld.Z <= b.MaxAABBWorld.Z && a.MaxAABBWorld.Z >= b.MinAABBWorld.Z)
}

// Returns true if any triangle of a intersects any triangle of b
func (a *Object) TriangleOverlap(b *Object) bool {

	if !a.AABBOverlap(b) {
		return false
	}

	// Build world-space vertex slices once
	wA := make([]Vector3, len(a.Mesh.Vertices))
	for i, v := range a.Mesh.Vertices {
		wA[i] = VecAddVec(v, a.Position)
	}
	wB := make([]Vector3, len(b.Mesh.Vertices))
	for i, v := range b.Mesh.Vertices {
		wB[i] = VecAddVec(v, b.Position)
	}

	// Test each triangle-pair
	for _, triA := range a.Mesh.Indices {
		a0, a1, a2 := wA[triA[0]], wA[triA[1]], wA[triA[2]]
		edgesA := [][2]Vector3{{a0, a1}, {a1, a2}, {a2, a0}}

		for _, triB := range b.Mesh.Indices {
			b0, b1, b2 := wB[triB[0]], wB[triB[1]], wB[triB[2]]
			edgesB := [][2]Vector3{{b0, b1}, {b1, b2}, {b2, b0}}

			// edges of A vs face of B
			for _, e := range edgesA {
				if SegmentIntersectsTriangle(e[0], e[1], b0, b1, b2) {
					return true
				}
			}
			// edges of B vs face of A
			for _, e := range edgesB {
				if SegmentIntersectsTriangle(e[0], e[1], a0, a1, a2) {
					return true
				}
			}
		}
	}

	return false
}

func (o *Object) StepBack(dt float32) {
	negVelocity := NegVec(o.Velocity)

	scaledVelocity := VecMulScalar(negVelocity, 1.1)

	o.Position = VecAddVec(o.Position, VecMulScalar(scaledVelocity, dt))
}
