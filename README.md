# Wi-Fi Speed Logger

This script automatically logs your Wi-Fi speed every minute to a CSV file. It records the date, time, Wi-Fi SSID, download and upload speeds (in Mbps), and ping (in ms).

## Features

- **Automated Speed Tests**: Runs a speed test every 60 seconds.
- **CSV Logging**: Saves results to a `wifi_speed_log.csv` file with headers.
- **Cross-Platform**: Supports macOS, Linux, and Windows.
- **Error Handling**: Gracefully handles network errors and continues running.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/wifi-speed-logger.git
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

Once the setup is complete, you can run the script with the following command:

```bash
python wifi_speed_logger.py
```

The script will print the logged data to the console and append it to the `wifi_speed_log.csv` file.

## Output Example (`wifi_speed_log.csv`)

| Date       | Time     | Wi-Fi SSID | Download Speed (Mbps) | Upload Speed (Mbps) | Ping (ms) |
|------------|----------|------------|-----------------------|---------------------|-----------|
| 2023-10-27 | 10:00:00 | MyNetwork  | 85.12                 | 22.45               | 15.67     |
| 2023-10-27 | 10:01:00 | MyNetwork  | 88.90                 | 21.88               | 14.99     |
