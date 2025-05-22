package mechanics

import (
	"root/common"
)

func ElasticCollisionResponse(a *common.Object, b *common.Object) {

	m1 := a.Mass
	m2 := b.Mass

	// v1 and v2 are the initial velocities
	v1 := a.Velocity
	v2 := b.Velocity


	// v1f = ((m1-m2)/(m1+m2))*v1 + (2*m2/(m1+m2))*v2
	m1pm2 := m1 + m2
	m1mm2 := m1 - m2

	v1f := common.Vector3{
		X: (m1mm2*v1.X + 2*m2*v2.X) / m1pm2,
		Y: (m1mm2*v1.Y + 2*m2*v2.Y) / m1pm2,
		Z: (m1mm2*v1.Z + 2*m2*v2.Z) / m1pm2,
	}

	// v2f = v1 + v2 - v1f
	v2f := common.Vector3{
		X: v1.X + v1f.X - v2.X,
		Y: v1.Y + v1f.Y - v2.Y,
		Z: v1.Z + v1f.Z - v2.Z,
	}


	a.Velocity = v1f
	b.Velocity = v2f
}
