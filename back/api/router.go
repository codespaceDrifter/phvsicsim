package api

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/cors"
)

func NewRouter() http.Handler {
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

	r.Get("/recordings/{name}/{chunk}", func(w http.ResponseWriter, r *http.Request) {
		GetRecordingHandler(w, r)
	})

	return r
}
