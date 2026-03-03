# Internet Speed Logger

I started this project to prove to my internet provider that their internet sucks. It's a terminal-based speed logger written in Go that runs a test every 60 seconds and logs results to a CSV file, with a live-updating TUI dashboard — so I have the receipts.

## Features

- **Live TUI Dashboard**: Real-time display of speed test results using [Bubble Tea](https://github.com/charmbracelet/bubbletea) and [Lip Gloss](https://github.com/charmbracelet/lipgloss).
- **Automated Speed Tests**: Runs a test every 60 seconds with a visible countdown.
- **Connection Type Detection**: Identifies Wi-Fi, Ethernet, or other connections (macOS, Linux, Windows).
- **Wi-Fi SSID Logging**: Records the network name when on Wi-Fi.
- **CSV Logging**: Appends results to `wifi_speed_log.csv`.
- **Cross-Platform**: Works on macOS, Linux, and Windows.

## Quickstart

### Prerequisites

- [Go 1.21+](https://go.dev/dl/)

### Build and run

```bash
git clone https://github.com/vahekhumaryan/wifi-speed-logger.git
cd wifi-speed-logger/go-app
go build -o internet-speed-logger .
./internet-speed-logger
```

Press `q` or `Ctrl+C` to quit.

### Run without building

```bash
cd go-app
go run .
```

## Output

Results are saved to `wifi_speed_log.csv` in the working directory:

| Date       | Time     | Connection Type | Wi-Fi SSID | Download Speed (Mbps) | Upload Speed (Mbps) | Ping (ms) |
|------------|----------|-----------------|------------|-----------------------|---------------------|-----------|
| 2026-03-03 | 13:21:04 | Wi-Fi           | MyNetwork  | 85.12                 | 22.45               | 15.67     |
| 2026-03-03 | 13:22:29 | Ethernet        | N/A        | 120.50                | 45.30               | 8.20      |

## Project Structure

```
go-app/
  main.go          # TUI app (Bubble Tea model, view, update)
  speedtest.go     # Speed test runner (speedtest-go)
  network.go       # Connection type & SSID detection (macOS/Linux/Windows)
  csv_logger.go    # CSV logging and test orchestration
  go.mod / go.sum  # Go module dependencies
```

## License

See [LICENSE](LICENSE) for details.
