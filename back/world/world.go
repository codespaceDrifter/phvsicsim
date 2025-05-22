package world

import (
	"time"
	"root/common"
	"root/mechanics"
)

type World struct {
	ID             string
	TimeStep       float32
	SleepTime      float32
	CurTime        float32
	Objects        []*common.Object
	InitialObjects []*common.Object
	ToReset        bool
}

func NewWorld(id string, timeStep float32, sleepTime float32) *World {
	return &World{
		ID:        id,
		TimeStep:  timeStep,
		SleepTime: sleepTime,
		ToReset:   false,
	}
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

func (w *World) SetToReset() {
	w.ToReset = true
}

func (w *World) Reset() {
	if w.ToReset {
		// Clear existing objects
		w.Objects = make([]*common.Object, len(w.InitialObjects))

		// Deep copy each object from InitialObjects to Objects
		for i, obj := range w.InitialObjects {
			w.Objects[i] = obj.DeepCopy()
		}
		w.ToReset = false

	}
}

// SaveInitialState saves the current state of Objects to InitialObjects
func (w *World) SaveInitialState() {
	w.InitialObjects = make([]*common.Object, len(w.Objects))
	for i, obj := range w.Objects {
		w.InitialObjects[i] = obj.DeepCopy()
	}
}

func (w *World) AllPairs() [][2]*common.Object {
	var pairs [][2]*common.Object
	for i := 0; i < len(w.Objects); i++ {
		for j := i + 1; j < len(w.Objects); j++ {
			pairs = append(pairs, [2]*common.Object{w.Objects[i], w.Objects[j]})
		}
	}
	return pairs
}

// Find all pairs of objects whose AABBs overlap
func (w *World) Overlaps() [][2]*common.Object {
	var overlaps [][2]*common.Object
	for i := 0; i < len(w.Objects); i++ {
		a := w.Objects[i]
		for j := i + 1; j < len(w.Objects); j++ {
			b := w.Objects[j]
			if a.TriangleOverlap(b) {
				overlaps = append(overlaps, [2]*common.Object{a, b})
			}
		}
	}
	return overlaps
}




func (w *World) Update() {

	w.Reset()

	w.CurTime += w.TimeStep

	overlapObjectPairs := w.Overlaps()

	for _, pair := range overlapObjectPairs {
		pair[0].StepBack(w.TimeStep)
		pair[1].StepBack(w.TimeStep)
		mechanics.ElasticCollisionResponse(pair[0], pair[1])
	}

	allPairs := w.AllPairs()

	for _, pair := range allPairs {
		mechanics.UniversalGravitationResponse(pair[0], pair[1])
	}

	for i := range w.Objects {
		w.Objects[i].Update(w.TimeStep)
	}


	if w.SleepTime > 0 {
		// Convert to float64 and multiply by seconds (1 billion nanoseconds) first, then convert to Duration(alias for int64)
		sleepDuration := time.Duration(float64(w.SleepTime) * float64(time.Second))
		time.Sleep(sleepDuration)
	}
}
