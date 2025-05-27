package world

import (
	"root/common"
	"root/mechanics"
)

type World struct {
	ID       string
	TimeStep float32
	CurTime  float32
	Objects  []*common.Object
}

type Frame struct {
	CurTime        float32
	IDArray        []string
	PositionArrays [][]float32
	VertexArrays   [][]float32
	IndexArrays    [][]uint32
	ColorArray     []string
}

func NewWorld(id string, timeStep float32) *World {
	return &World{
		ID:       id,
		TimeStep: timeStep,
	}
}

func (w *World) Flatten() Frame {
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

	return Frame{
		CurTime:        w.CurTime,
		IDArray:        IDArray,
		PositionArrays: PositionArrays,
		VertexArrays:   VertexArrays,
		IndexArrays:    IndexArrays,
		ColorArray:     ColorArray,
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

}
