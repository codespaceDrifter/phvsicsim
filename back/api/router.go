package api

import (
	"net/http"
	"root/world"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/cors"
)

func NewRouter(worlds map[string]*world.World) http.Handler {
	r := chi.NewRouter()

	// CORS middleware
	r.Use(cors.Handler(cors.Options{
		// Allow all origins
		AllowedOrigins: []string{"*"},
		// Allow all methods
		AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		// Allow all headers
		AllowedHeaders: []string{"*"},
		// Allow credentials
		AllowCredentials: true,
	}))

	r.Get("/worlds/{id}", func(w http.ResponseWriter, r *http.Request) {
		GetWorldObjectsHandler(w, r, worlds)
	})

	r.Post("/worlds/{id}/reset", func(w http.ResponseWriter, r *http.Request) {
		ResetWorldHandler(w, r, worlds)
	})

	return r
}
