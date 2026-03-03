# Internet Speed Logger

This script automatically logs your internet speed every minute to a CSV file. It records the date, time, connection type (Wi-Fi, Ethernet, etc.), Wi-Fi SSID (when on Wi-Fi), download and upload speeds (in Mbps), and ping (in ms).

## Features

- **Automated Speed Tests**: Runs a speed test every 60 seconds.
- **Connection Type Detection**: Identifies whether you're on Wi-Fi, Ethernet, or another connection.
- **Wi-Fi SSID Logging**: Records the network name when connected via Wi-Fi.
- **CSV Logging**: Saves results to a `wifi_speed_log.csv` file with headers.
- **Cross-Platform Launchers**: Double-click launchers for macOS and Windows, terminal UI for Linux.
- **Error Handling**: Gracefully handles network errors and continues running.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vahekhumaryan/wifi-speed-logger.git
   cd wifi-speed-logger
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Using the Launcher (Recommended)

- **macOS**: Double-click `start_logger_mac.command`. A window will appear confirming the logger is running. Click **Quit** to stop.
- **Windows**: Double-click `start_logger_windows.bat`. A window will appear confirming the logger is running. Click **Quit** to stop.
- **Linux**: Run the launcher from the terminal:
  ```bash
  python launcher.py
  ```
  A styled banner will confirm the logger is running. Press `Ctrl+C` to stop.

### Running Directly

```bash
python wifi_speed_logger.py
```

## Output Example (`wifi_speed_log.csv`)

| Date       | Time     | Connection Type | Wi-Fi SSID | Download Speed (Mbps) | Upload Speed (Mbps) | Ping (ms) |
|------------|----------|-----------------|------------|-----------------------|---------------------|-----------|
| 2024-11-08 | 13:21:04 | Wi-Fi           | MyNetwork  | 85.12                 | 22.45               | 15.67     |
| 2024-11-08 | 13:22:29 | Ethernet        |            | 120.50                | 45.30               | 8.20      |
