package main

import (
	"fmt"
	"net/http"
	"root/api"
	exampleWorlds "root/example/worlds"
	"root/world"
)

func main() {
	/*
	w := exampleWorlds.ThreeBody()
	recording := world.NewRecording("threeBody", w, 0.5, 3000)
	recording.Simulate()
	*/

	w := exampleWorlds.BillardBall()
	recording := world.NewRecording("billardBall", w, 0.01, 100)
	recording.Simulate()

	router := api.NewRouter()

	go func() {
		fmt.Println("Server is running on port 8080")
		http.ListenAndServe(":8080", router)
	}()

	select {}
}
