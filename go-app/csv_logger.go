package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"time"
)

const csvFile = "wifi_speed_log.csv"

var csvHeaders = []string{
	"Date", "Time", "Connection Type", "Wi-Fi SSID",
	"Download Speed (Mbps)", "Upload Speed (Mbps)", "Ping (ms)",
}

// LogEntry represents a single speed test result.
type LogEntry struct {
	Date       string
	Time       string
	ConnType   string
	SSID       string
	Download   float64
	Upload     float64
	Ping       float64
}

// InitializeCSV creates the CSV file with headers if it doesn't exist.
func InitializeCSV() error {
	if _, err := os.Stat(csvFile); err == nil {
		return nil // file already exists
	}

	f, err := os.Create(csvFile)
	if err != nil {
		return fmt.Errorf("failed to create CSV file: %w", err)
	}
	defer f.Close()

	w := csv.NewWriter(f)
	if err := w.Write(csvHeaders); err != nil {
		return fmt.Errorf("failed to write CSV headers: %w", err)
	}
	w.Flush()
	return w.Error()
}

// LogSpeedData appends a log entry to the CSV file.
func LogSpeedData(entry LogEntry) error {
	f, err := os.OpenFile(csvFile, os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf("failed to open CSV file: %w", err)
	}
	defer f.Close()

	w := csv.NewWriter(f)
	record := []string{
		entry.Date,
		entry.Time,
		entry.ConnType,
		entry.SSID,
		fmt.Sprintf("%.2f", entry.Download),
		fmt.Sprintf("%.2f", entry.Upload),
		fmt.Sprintf("%.2f", entry.Ping),
	}
	if err := w.Write(record); err != nil {
		return fmt.Errorf("failed to write CSV record: %w", err)
	}
	w.Flush()
	return w.Error()
}

// RunSingleTest performs one complete speed test cycle and returns the log entry.
func RunSingleTest() (*LogEntry, error) {
	now := time.Now()
	connType := GetConnectionType()

	ssid := "N/A"
	if connType == "Wi-Fi" {
		ssid = GetWiFiSSID()
	}

	result, err := RunSpeedTest()
	if err != nil {
		return nil, fmt.Errorf("speed test failed: %w", err)
	}

	entry := &LogEntry{
		Date:     now.Format("2006-01-02"),
		Time:     now.Format("15:04:05"),
		ConnType: connType,
		SSID:     ssid,
		Download: result.Download,
		Upload:   result.Upload,
		Ping:     result.Ping,
	}

	if err := LogSpeedData(*entry); err != nil {
		return entry, fmt.Errorf("failed to log data: %w", err)
	}

	return entry, nil
}
