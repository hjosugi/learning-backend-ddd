package main

import (
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"strings"
	"sync"
)

type Task struct {
	ID     int    `json:"id"`
	Title  string `json:"title"`
	Status string `json:"status"`
}

type Store struct {
	mu     sync.Mutex
	nextID int
	tasks  []Task
}

func NewStore() *Store {
	store := &Store{nextID: 1}
	_, _ = store.Create("Read the contract")
	return store
}

func (s *Store) Create(title string) (Task, error) {
	title = strings.TrimSpace(title)
	if len(title) < 3 {
		return Task{}, errors.New("title must be at least 3 characters")
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	task := Task{ID: s.nextID, Title: title, Status: "open"}
	s.nextID++
	s.tasks = append(s.tasks, task)
	return task, nil
}

func (s *Store) List() []Task {
	s.mu.Lock()
	defer s.mu.Unlock()
	return append([]Task(nil), s.tasks...)
}

type Server struct {
	store *Store
}

func NewServer(store *Store) *Server {
	return &Server{store: store}
}

func (s *Server) routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /healthz", s.health)
	mux.HandleFunc("GET /tasks", s.listTasks)
	mux.HandleFunc("POST /tasks", s.createTask)
	return mux
}

func (s *Server) health(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func (s *Server) listTasks(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, s.store.List())
}

func (s *Server) createTask(w http.ResponseWriter, r *http.Request) {
	var body struct {
		Title string `json:"title"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid json"})
		return
	}
	task, err := s.store.Create(body.Title)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, task)
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("content-type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func main() {
	server := NewServer(NewStore())
	log.Println("listening on http://127.0.0.1:8081")
	log.Fatal(http.ListenAndServe("127.0.0.1:8081", server.routes()))
}

