package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/signal"
	"runtime"
	"syscall"
)

// Define the struct that matches the JSON data.
// For example, suppose we have a JSON object representing a person.
type Person struct {
	Name  string `json:"name"`
	Age   int    `json:"age"`
	Children []Person `json:"children,omitempty"`
}

func memstats(prefix string) {
	return
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	fmt.Println( prefix)
	fmt.Printf("Alloc = %v MiB", m.Alloc / 1024 / 1024)
	fmt.Printf("\tTotalAlloc = %v MiB", m.TotalAlloc / 1024 / 1024)
	fmt.Printf("\tSys = %v MiB", m.Sys / 1024 / 1024)
	fmt.Printf("\tNumGC = %v\n", m.NumGC)
}

func main() {
	parentPID := os.Getppid()
	// fmt.Println("Parent pid:", parentPID)
	channel := make(chan os.Signal)
	signal.Notify(channel, syscall.SIGUSR2)

	memstats("baseline")
	data, err := os.ReadFile("foo.json")
	if err != nil {
		panic(err)
	}
	// parentPID
	syscall.Kill(parentPID, syscall.SIGUSR1)
	_ = <-channel
	memstats("raw data")
	// Create an instance of Person to hold the parsed data
	var p Person

	// Parse (unmarshal) the JSON data into the struct
	err = json.Unmarshal([]byte(data), &p)
	data = nil
	runtime.GC()
	memstats("after GC")
	if err != nil {
		log.Fatalf("Error parsing JSON: %s", err)
	}

	// parentPID
	syscall.Kill(parentPID, syscall.SIGUSR1)
	// Use the parsed data (for example, print it)
	_ = <-channel
	memstats("struct")
	// fmt.Printf("Parsed struct: %+v\n", p)
}
