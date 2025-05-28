package main

import (
	"fmt"
	"net/http"
	"root/api"
	exampleWorlds "root/example/worlds"
)

func main() {
	exampleWorlds.SimulateThreeBody()
	exampleWorlds.SimulateBillardBall()

	router := api.NewRouter()

	go func() {
		fmt.Println("Server is running on port 8080")
		http.ListenAndServe(":8080", router)
	}()

	select {}
}
