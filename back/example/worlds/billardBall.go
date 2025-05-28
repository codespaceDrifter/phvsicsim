package exampleWorlds

import (
	"fmt"
	"root/common"
	"root/world"
)

func BillardBall() *world.World {
	w := world.NewWorld("billardBall", 0.01)

	w.Objects = append(w.Objects, common.NewObject(
		"table", "#654321",
		common.NewHollowRectFrame(280.0, 140.0, 5.0, 10.0),
		1000,
		common.Vector3{X: 0, Y: 10.0 / 2, Z: 0},
		common.Vector3{},
	))

	radius := float32(5.7)
	spacing := float32(0.0) // balls touching
	ballDensity := float32(170)
	ballsPerRow := 5
	rowCount := 3
	rowSeparation := float32(20.0) // space between rows (Z direction)
	startX := float32(-70.0)       // leftmost ball X position
	startZ := float32(-20.0)
	moveSpeed := float32(200.0)

	for row := 0; row < rowCount; row++ {
		movingBalls := row + 1 // 1, 2, 3
		stationaryBalls := ballsPerRow - movingBalls
		z := startZ + float32(row)*rowSeparation

		// Place stationary balls
		for i := 0; i < stationaryBalls; i++ {
			x := startX + float32(i)*(radius*2+spacing)
			w.Objects = append(w.Objects, common.NewObject(
				fmt.Sprintf("row%d_stat%d", row, i), "#ffffff",
				common.NewSphere(radius, 0),
				ballDensity,
				common.Vector3{X: x, Y: radius, Z: z},
				common.Vector3{}, // no velocity
			))
		}

		// Place moving balls
		for i := 0; i < movingBalls; i++ {
			x := startX + float32(stationaryBalls+i)*(radius*2+spacing)
			w.Objects = append(w.Objects, common.NewObject(
				fmt.Sprintf("row%d_mov%d", row, i), "#ffff00",
				common.NewSphere(radius, 0),
				ballDensity,
				common.Vector3{X: x, Y: radius, Z: z},
				common.Vector3{X: -moveSpeed, Y: 0, Z: 0}, // moving left
			))
		}
	}

	return w
}

func SimulateBillardBall() {
	w := BillardBall()
	recording := world.NewRecording("billardBall", w, 0.01, 10)
	recording.Simulate()
}
