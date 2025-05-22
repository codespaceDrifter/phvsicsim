package exampleWorlds

import (
	"root/common"
	"root/world"
)

func RocketLaunch() *world.World {
	world := world.NewWorld("rocketLaunch", 0.01, 1e-3)

	sphere1 := common.NewObject("sphere1", "#301175", common.NewSphere(50, 2), 1e3, common.Vector3{X: 0, Y: 0, Z: 0}, common.Vector3{X: 0, Y: 0, Z: 0})
	sphere2 := common.NewObject("sphere2", "#3fa9c0", common.NewSphere(10, 2), 1e8, common.Vector3{X: 150, Y: 0, Z: 0}, common.Vector3{X: 0, Y: 0, Z: 0})

	world.Objects = append(world.Objects, sphere1)
	world.Objects = append(world.Objects, sphere2)
	world.SaveInitialState()

	return world
}
