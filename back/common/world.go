package common

import (
	"time"
)

type World struct {
	ID             string
	TimeStep       float32
	SleepTime      float32
	CurTime        float32
	Objects        []Object
	InitialObjects []Object
}

func (w *World) Flatten() (float32, []string, [][]float32, [][]float32, [][]uint32, []string) {
	IDArray := make([]string, 0, len(w.Objects))
	PositionArrays := make([][]float32, 0, len(w.Objects))
	VertexArrays := make([][]float32, 0, len(w.Objects))
	IndexArrays := make([][]uint32, 0, len(w.Objects))
	ColorArray := make([]string, 0, len(w.Objects))

	for _, obj := range w.Objects {
		id, pos, verts, inds, color := obj.Flatten()
		IDArray = append(IDArray, id)
		PositionArrays = append(PositionArrays, pos)
		VertexArrays = append(VertexArrays, verts)
		IndexArrays = append(IndexArrays, inds)
		ColorArray = append(ColorArray, color)
	}

	return w.CurTime, IDArray, PositionArrays, VertexArrays, IndexArrays, ColorArray
}

func (w *World) Update() {
	w.CurTime += w.TimeStep
	for i := range w.Objects {
		w.Objects[i].UpdatePosition(w.TimeStep)
	}
	if w.SleepTime > 0 {
		// Convert to float64 and multiply by seconds (1 billion nanoseconds) first, then convert to Duration(alias for int64)
		sleepDuration := time.Duration(float64(w.SleepTime) * float64(time.Second))
		time.Sleep(sleepDuration)
	}
}

func (w *World) Reset() {
	// Clear existing objects
	w.Objects = make([]Object, len(w.InitialObjects))

	// Deep copy each object from InitialObjects to Objects
	for i, obj := range w.InitialObjects {
		w.Objects[i] = obj.DeepCopy()
	}
}

// SaveInitialState saves the current state of Objects to InitialObjects
func (w *World) SaveInitialState() {
	w.InitialObjects = make([]Object, len(w.Objects))
	for i, obj := range w.Objects {
		w.InitialObjects[i] = obj.DeepCopy()
	}
}
