package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestCreateTaskValidation(t *testing.T) {
	store := NewStore()
	if _, err := store.Create("x"); err == nil {
		t.Fatal("expected validation error")
	}
}

func TestHealthRoute(t *testing.T) {
	server := NewServer(NewStore())
	request := httptest.NewRequest(http.MethodGet, "/healthz", nil)
	response := httptest.NewRecorder()

	server.routes().ServeHTTP(response, request)

	if response.Code != http.StatusOK {
		t.Fatalf("status = %d", response.Code)
	}
	if !strings.Contains(response.Body.String(), "ok") {
		t.Fatalf("body = %s", response.Body.String())
	}
}

