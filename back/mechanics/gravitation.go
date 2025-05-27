package mechanics

import (
	"math"
	"root/common"
)

const G = 6.674e-11 // gravitational constant in m^3 kg^-1 s^-2

// TO DO: USE CENTER OF MASS NOT POSITION

func UniversalGravitationResponse(a *common.Object, b *common.Object) {
	// Vector from a to b
	delta := common.Vector3{
		X: b.Position.X - a.Position.X,
		Y: b.Position.Y - a.Position.Y,
		Z: b.Position.Z - a.Position.Z,
	}

	distSq := delta.X*delta.X + delta.Y*delta.Y + delta.Z*delta.Z
	if distSq == 0 {
		return // avoid division by zero
	}
	dist := float32(math.Sqrt(float64(distSq)))

	// Unit vector from a to b
	dir := common.Vector3{
		X: delta.X / dist,
		Y: delta.Y / dist,
		Z: delta.Z / dist,
	}

	// Magnitude of force
	forceMag := float32(G) * a.Mass * b.Mass / distSq

	// Force vector
	force := common.Vector3{
		X: dir.X * forceMag,
		Y: dir.Y * forceMag,
		Z: dir.Z * forceMag,
	}

	// Apply to both objects (equal and opposite)
	a.Force = common.VecAddVec(a.Force, force)
	b.Force = common.VecSubVec(b.Force, force)
}
