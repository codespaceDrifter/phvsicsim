package example

import "root/common"

func ThreeBody() common.World {
	world := common.World{
		ID:        "threeBody",
		TimeStep:  0.01,
		SleepTime: 0.01,
	}
	/*
		earthMesh := common.NewSphere(1, 3)
		earth := common.Object{
			ID:       "earth",
			Mesh:     earthMesh,
			Position: common.Vector3{X: 500, Y: 0, Z: 0},
			Velocity: common.Vector3{X: 0, Y: 0, Z: 0},
		}

		jupiterMesh := common.NewSphere(10, 3)
		jupiter := common.Object{
			ID:       "jupiter",
			Mesh:     jupiterMesh,
			Position: common.Vector3{X: 200, Y: 0, Z: 0},
			Velocity: common.Vector3{X: 0, Y: 0, Z: 0},
		}

		sunMesh := common.NewSphere(100, 3)
		sun := common.Object{
			ID:       "sun",
			Mesh:     sunMesh,
			Position: common.Vector3{X: 0, Y: 0, Z: 0},
			Velocity: common.Vector3{X: 0, Y: 0, Z: 0},
		}

		world.Objects = append(world.Objects, earth)
		world.Objects = append(world.Objects, sun)
		world.Objects = append(world.Objects, jupiter)

	*/

	earthMesh := common.NewSphere(6_000_000, 5)
	earth := common.Object{
		ID:       "earth",
		Mesh:     earthMesh,
		Position: common.Vector3{X: 0, Y: -6_000_000, Z: 0},
		Color:    "#333333",
		Velocity: common.Vector3{X: 0, Y: 0, Z: 0},
	}

	world.Objects = append(world.Objects, earth)

	// Save the initial state after adding all objects
	world.SaveInitialState()

	return world
}
