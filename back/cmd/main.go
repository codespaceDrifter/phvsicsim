package main

import (
	"fmt"
	"log"
	"net/http"
	"root/api"
	exampleWorlds "root/example/worlds"
)


func main() {

	simulate := true

	if simulate {
		exampleWorlds.SimulateThreeBody()
		exampleWorlds.SimulateBillardBall()
	}

	router := api.NewRouter()



	fmt.Println("Server is running on port 80")
	err := http.ListenAndServe(":80", router)
	if err != nil {
		log.Fatalf("Server failed: %v", err)
	}

}
