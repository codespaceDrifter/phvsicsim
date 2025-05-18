package main

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"
	"time"
)

// PhysicalObject represents a physical object in the simulation
type PhysicalObject struct {
	ID       string     `json:"id"`
	Position [3]float64 `json:"position"` // x, y, z
	Velocity [3]float64 `json:"velocity"` // vx, vy, vz
	Size     [3]float64 `json:"size"`     // width, height, depth (rectangular shape)
}

// SimulationWorld manages the simulation
type SimulationWorld struct {
	Objects     map[string]*PhysicalObject `json:"objects"`
	TimeStep    float64                    `json:"timeStep"` // seconds
	ElapsedTime float64                    `json:"elapsedTime"`
	mu          sync.Mutex
}

// NewSimulationWorld creates a new simulation world
func NewSimulationWorld() *SimulationWorld {
	return &SimulationWorld{
		Objects:     make(map[string]*PhysicalObject),
		TimeStep:    0.01, // 10ms default timestep
		ElapsedTime: 0,
	}
}

// AddObject adds a physical object to the simulation
func (w *SimulationWorld) AddObject(obj *PhysicalObject) {
	w.mu.Lock()
	defer w.mu.Unlock()
	w.Objects[obj.ID] = obj
}

// Update updates the state of all objects based on their velocity
func (w *SimulationWorld) Update() {
	w.mu.Lock()
	defer w.mu.Unlock()

	// Update positions based on velocity
	for _, obj := range w.Objects {
		// Apply velocity to position (p = p + v*t)
		for i := 0; i < 3; i++ {
			obj.Position[i] += obj.Velocity[i] * w.TimeStep
		}
	}

	// Increment elapsed time
	w.ElapsedTime += w.TimeStep
}

// SimulationHandler handles the simulation state as JSON
func (w *SimulationWorld) SimulationHandler(rw http.ResponseWriter, r *http.Request) {
	w.mu.Lock()
	defer w.mu.Unlock()

	rw.Header().Set("Content-Type", "application/json")
	rw.Header().Set("Access-Control-Allow-Origin", "*")

	json.NewEncoder(rw).Encode(w)
}

func main() {
	simulation := NewSimulationWorld()

	// Add some test objects
	simulation.AddObject(&PhysicalObject{
		ID:       "obj1",
		Position: [3]float64{0, 0, 0},
		Velocity: [3]float64{1, 0.5, 0},
		Size:     [3]float64{1, 1, 1},
	})

	simulation.AddObject(&PhysicalObject{
		ID:       "obj2",
		Position: [3]float64{-5, 2, 0},
		Velocity: [3]float64{-0.5, -0.2, 0},
		Size:     [3]float64{2, 1, 3},
	})

	// Start the simulation loop in a goroutine
	go func() {
		ticker := time.NewTicker(time.Duration(simulation.TimeStep * float64(time.Second)))
		defer ticker.Stop()

		for range ticker.C {
			simulation.Update()
		}
	}()

	// HTTP server
	http.HandleFunc("/simulation", simulation.SimulationHandler)

	// Serve static files for the frontend
	fs := http.FileServer(http.Dir("./frontend"))
	http.Handle("/", fs)

	log.Println("Starting physics simulation server on :8000")
	log.Fatal(http.ListenAndServe(":8000", nil))
}
