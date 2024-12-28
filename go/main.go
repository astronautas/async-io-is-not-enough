package main

import (
	"fmt"
	"io"
	"math"
	"net/http"
	"runtime"
	"sync"
	"time"
)

func fakeCPUOperation(iterations int, noise float64) {
	result := 0.0

	for i := 0; i < iterations; i++ {
		result += math.Sqrt(12345.6789 * noise) // Perform a CPU-intensive operation
	}
}

func fakeIoOp(seconds int) {
	url := fmt.Sprintf("https://httpbin.org/delay/%d", seconds)

	// Create an HTTP client with a timeout
	client := &http.Client{
		Timeout: 10 * time.Second,
	}

	// Make the GET request
	// fmt.Printf("Making request to %s...\n", url)
	resp, err := client.Get(url)
	if err != nil {
		fmt.Printf("Error making request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	io.ReadAll(resp.Body)
}

func work(wg *sync.WaitGroup) {
	defer wg.Done()
	// ~1s
	// fakeCPUOperation(1_500_000_000, rand.Float64())
	fakeIoOp(1)
}

func getGOMAXPROCS() int {
	return runtime.GOMAXPROCS(0)
}

// interestng. time sleep fails because it relies on wall clock
func main() {
	fmt.Printf("GOMAXPROCS is %d\n", getGOMAXPROCS())

	var wg sync.WaitGroup

	for _, num_experiments := range [6]int{1, 2, 4, 8, 16, 32} {
		fmt.Printf("Tasks: %d \n", num_experiments)

		startTime := time.Now()

		for i := 0; i <= num_experiments; i++ {
			wg.Add(1)

			// run as go routine to speed-up IO
			go work(&wg)
		}

		wg.Wait()

		fmt.Println("Elapsed time:", time.Since(startTime))
	}
}
