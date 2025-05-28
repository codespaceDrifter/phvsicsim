package api

import (
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
)

func GetRecordingHandler(w http.ResponseWriter, r *http.Request) {
	name := chi.URLParam(r, "name")
	chunk := chi.URLParam(r, "chunk")

	fmt.Println("name", name)
	fmt.Println("chunk", chunk)

	path := fmt.Sprintf("../../logs/%s/%s.bin", name, chunk)
	file, err := os.Open(path)
	if err != nil {
		w.WriteHeader(http.StatusNotFound)
		return
	}
	defer file.Close()
	w.Header().Set("Content-Type", "application/octet-stream")
	io.Copy(w, file)
}
