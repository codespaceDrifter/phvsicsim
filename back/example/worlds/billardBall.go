package exampleWorlds

import (
	"fmt"
	"math"
	"root/common"
	"root/world"
)

func BillardBall() *world.World {
	w := world.NewWorld("billardBall", 0.01)

	w.Objects = append(w.Objects, common.NewObject(
		"table", "#654321",
		common.NewHollowRectFrame(2.8, 1.4, 0.05, 0.1),
		1000,
		common.Vector3{X: 0, Y: 0.1 / 2, Z: 0},
		common.Vector3{},
	))

	// Ball parameters
	radius := float32(0.057)
	spacing := float32(0.01)
	startX := float32(0.7)
	triangleRows := 4
	ballColor := "#ffffff"
	ballDensity := float32(170) // 170kg/m^3 (arbitrary, just for mass)

	// Place triangle of balls
	for row := 0; row < triangleRows; row++ {
		for col := 0; col <= row; col++ {
			x := startX + float32(row)*(radius*2+spacing)*float32(math.Sin(math.Pi/3))
			z := (float32(col) - float32(row)/2.0) * ((radius * 2) + spacing)
			w.Objects = append(w.Objects, common.NewObject(
				fmt.Sprintf("ball_%d_%d", row, col), ballColor,
				common.NewSphere(radius, 0),
				ballDensity,
				common.Vector3{X: x, Y: radius, Z: z},
				common.Vector3{},
			))
		}
	}

	cue := common.NewObject(
		"cue", "#ffff00",
		common.NewSphere(radius, 0),
		ballDensity,
		common.Vector3{X: -1.0, Y: radius, Z: 0.0},
		common.Vector3{X: 2.0, Y: 0, Z: 0},
	)
	w.Objects = append(w.Objects, cue)

	return w
}
