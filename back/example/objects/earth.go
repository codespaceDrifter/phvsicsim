package exampleObjects

import "root/common"

func Earth() *common.Object {
	earthMesh := common.NewSphere(6_000_000, 5)
	earth := common.NewObject(
		"earth",
		"#333333",
		earthMesh,
		5515,
		common.Vector3{X: 0, Y: -6_000_000, Z: 0},
		common.Vector3{X: 0, Y: 0, Z: 0},
	)

	return earth
}
