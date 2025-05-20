package api

import (
	"encoding/json"
	"net/http"
	"root/common"

	"github.com/go-chi/chi/v5"
)

type WorldResponse struct {
	IDArray        []string    `json:"IDArray"`
	PositionArrays [][]float32 `json:"PositionArrays"`
	VertexArrays   [][]float32 `json:"VertexArrays"`
	IndexArrays    [][]uint32  `json:"IndexArrays"`
	CurTime        float32     `json:"CurTime"`
}

func GetWorldObjectsHandler(w http.ResponseWriter, r *http.Request, worlds map[string]*common.World) {
	id := chi.URLParam(r, "id")

	world := worlds[id]

	IDArray, PositionArrays, VertexArrays, IndexArrays, CurTime := world.Flatten()

	response := WorldResponse{
		IDArray:        IDArray,
		PositionArrays: PositionArrays,
		VertexArrays:   VertexArrays,
		IndexArrays:    IndexArrays,
		CurTime:        CurTime,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func ResetWorldHandler(w http.ResponseWriter, r *http.Request, worlds map[string]*common.World) {
	id := chi.URLParam(r, "id")
	world := worlds[id]
	world.Reset()
	// No need to update the map since we're using pointers

}
