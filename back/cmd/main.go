package main

import (
	"fmt"
	"net/http"
	"root/api"
	"root/world"
	"root/example/worlds"
)

func main() {
	worlds := map[string]*world.World{}

	world := exampleWorlds.ThreeBody()

	worlds[world.ID] = world

	router := api.NewRouter(worlds)

	// Start the HTTP server in a separate goroutine
	go func() {
		fmt.Println("Server is running on port 8080")
		if err := http.ListenAndServe(":8080", router); err != nil {
			fmt.Println("Server error:", err)
		}
	}()

	// Continuous simulation
	for {
		world.Update()
	}
}
