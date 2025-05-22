package exampleWorlds

import (
	"root/common"
	"root/world"
)

func ThreeBody() *world.World {
	world := world.NewWorld("threeBody", 0.01,
		1e-3)

	/*
		aCenA := common.NewObject(
			"aCenA", "#ffe599",                // yellow-white
			common.NewSphere(30, 3),           // radius 30 m
			5.0e10,                             // high density → big mass
			common.Vector3{X: -200, Y: 0, Z: 0},
			common.Vector3{X: 0,   Y: 30, Z: 0},
		)

		aCenB := common.NewObject(
			"aCenB", "#ffa64d",                // orange
			common.NewSphere(30, 3),
			5.0e10,
			common.Vector3{X: 75, Y: 0, Z: 0},
			common.Vector3{X: 0,   Y: -30, Z: 0},
		)

		proxima := common.NewObject(
			"proxima", "#ff4d4d",              // deep red
			common.NewSphere(15, 3),
			6.0e10,
			common.Vector3{X: 0,   Y: 100, Z: 0},
			common.Vector3{X: 20, Y: 0,  Z: 0},
		)

		trisolaris := common.NewObject(
			"trisolaris", "#3fa9c0",           // bluish-green
			common.NewSphere(5, 3),
			5500,
			common.Vector3{X: 0,   Y: 120, Z: 0},
			common.Vector3{X: 60, Y: 0,  Z: 0},
		)

		world.Objects = append(world.Objects, aCenA)
		world.Objects = append(world.Objects, aCenB)
		world.Objects = append(world.Objects, proxima)
		world.Objects = append(world.Objects, trisolaris)
	*/
	acenA := common.NewObject(
		"aCenA", "#ffe599",
		common.NewSphere(40, 1),
		5e8,
		common.Vector3{X: 0, Y: 0, Z: 0},
		common.Vector3{X: 0, Y: 0, Z: 0},
	)

	aCenB := common.NewObject(
		"aCenB", "#ffa64d",
		common.NewSphere(25, 1),
		3e8,
		common.Vector3{X: 300, Y: 0, Z: 0},
		common.Vector3{X: 0, Y: 0, Z: 5},
	)

	proxima := common.NewObject(
		"proxima", "#ff4d4d",
		common.NewSphere(30, 1),
		6e8,
		common.Vector3{X: 0, Y: 0, Z: 300},
		common.Vector3{X: 0, Y: 5, Z: 0},
	)

	trisolaris := common.NewObject(
		"trisolaris", "#3fa9c0",
		common.NewSphere(5, 1),
		5500,
		common.Vector3{X: 0, Y: 0, Z: 350},
		common.Vector3{X: 10, Y: 5, Z: 0},
	)

	world.Objects = append(world.Objects, acenA)
	world.Objects = append(world.Objects, aCenB)
	world.Objects = append(world.Objects, proxima)
	world.Objects = append(world.Objects, trisolaris)

	// Save the initial state after adding all objects
	world.SaveInitialState()

	return world
}
