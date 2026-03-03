package main

import (
	"fmt"
	"log"

	"github.com/showwin/speedtest-go/speedtest"
)

// SpeedResult holds the results of a speed test.
type SpeedResult struct {
	Download float64 // Mbps
	Upload   float64 // Mbps
	Ping     float64 // ms
}

// RunSpeedTest performs an internet speed test and returns the results.
func RunSpeedTest() (*SpeedResult, error) {
	client := speedtest.New()

	serverList, err := client.FetchServers()
	if err != nil {
		return nil, fmt.Errorf("failed to fetch servers: %w", err)
	}

	if len(serverList) == 0 {
		return nil, fmt.Errorf("no servers available")
	}

	server := serverList[0]

	if err := server.PingTest(nil); err != nil {
		log.Printf("Ping test failed: %v", err)
	}
	if err := server.DownloadTest(); err != nil {
		log.Printf("Download test failed: %v", err)
	}
	if err := server.UploadTest(); err != nil {
		log.Printf("Upload test failed: %v", err)
	}

	return &SpeedResult{
		Download: float64(server.DLSpeed) / 1_000_000,
		Upload:   float64(server.ULSpeed) / 1_000_000,
		Ping:     float64(server.Latency.Milliseconds()),
	}, nil
}
