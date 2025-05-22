package api

import (
	"encoding/json"
	"net/http"
	"root/world"

	"github.com/go-chi/chi/v5"
)

type WorldResponse struct {
	CurTime        float32     `json:"CurTime"`
	IDArray        []string    `json:"IDArray"`
	PositionArrays [][]float32 `json:"PositionArrays"`
	VertexArrays   [][]float32 `json:"VertexArrays"`
	IndexArrays    [][]uint32  `json:"IndexArrays"`
	ColorArray     []string    `json:"ColorArray"`
}

func GetWorldObjectsHandler(w http.ResponseWriter, r *http.Request, worlds map[string]*world.World) {
	id := chi.URLParam(r, "id")

	world := worlds[id]

	CurTime, IDArray, PositionArrays, VertexArrays, IndexArrays, ColorArray := world.Flatten()

	response := WorldResponse{
		CurTime:        CurTime,
		IDArray:        IDArray,
		PositionArrays: PositionArrays,
		VertexArrays:   VertexArrays,
		IndexArrays:    IndexArrays,
		ColorArray:     ColorArray,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func ResetWorldHandler(w http.ResponseWriter, r *http.Request, worlds map[string]*world.World) {
	id := chi.URLParam(r, "id")
	world := worlds[id]
	world.SetToReset()
	// No need to update the map since we're using pointers

}
