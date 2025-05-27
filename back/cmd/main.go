package main

import (
	"fmt"
	"net/http"
	"root/api"
	"root/example/worlds"
	"root/world"
)

func main() {
	w := exampleWorlds.RocketLaunch()

	recording := world.NewRecording("rocketLaunch", w, 1, 10000)
	recording.Simulate()

	router := api.NewRouter()

	go func() {
		fmt.Println("Server is running on port 8080")
		http.ListenAndServe(":8080", router)
	}()

	select {}
}
