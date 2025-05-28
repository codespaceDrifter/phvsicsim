package mechanics

import (
	"root/common"
	"math"
)

func ElasticCollisionResponse(a *common.Object, b *common.Object) {

	combinedRestitution := float32(math.Sqrt(float64(a.Restitution * b.Restitution)))

	m1 := a.Mass
	m2 := b.Mass

	// v1 and v2 are the initial velocities
	v1 := a.Velocity
	v2 := b.Velocity


	// v1f = ((m1-m2)/(m1+m2))*v1 + (2*m2/(m1+m2))*v2
	m1pm2 := m1 + m2
	m1tv1pm2tv2 := common.VecAddVec(common.VecMulScalar(v1, m1), common.VecMulScalar(v2, m2))

	v2mv1 := common.VecSubVec(v2, v1)
	v1mv2 := common.VecSubVec(v1, v2)

	A := common.VecMulScalar(v2mv1, (m2*combinedRestitution))
	B := common.VecAddVec(A, m1tv1pm2tv2)
	v1f := common.VecDivScalar(B, m1pm2)

	C := common.VecMulScalar(v1mv2, (m1*combinedRestitution))
	D := common.VecAddVec(C, m1tv1pm2tv2)
	v2f := common.VecDivScalar(D, m1pm2)

	a.Velocity = v1f
	b.Velocity = v2f
}
