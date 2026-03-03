import speedtest
import time
import csv
import datetime
import subprocess
import platform
import logging

# --- Configuration ---
CSV_FILE = 'wifi_speed_log.csv'
LOG_FILE = 'wifi_speed_logger.log'
HEADERS = ['Date', 'Time', 'Connection Type', 'Wi-Fi SSID', 'Download Speed (Mbps)', 'Upload Speed (Mbps)', 'Ping (ms)']

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def initialize_csv():
    """Initializes the CSV log file with headers if it doesn't exist."""
    try:
        with open(CSV_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
            logging.info(f"CSV file '{CSV_FILE}' created with headers.")
    except FileExistsError:
        logging.info(f"CSV file '{CSV_FILE}' already exists.")

def get_connection_type():
    """Detects the active network connection type (Wi-Fi, Ethernet, etc.)."""
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            # Get the default route interface
            route = subprocess.check_output(
                ["route", "-n", "get", "default"], text=True, stderr=subprocess.DEVNULL
            )
            interface = ""
            for line in route.split('\n'):
                if "interface:" in line:
                    interface = line.split(":")[1].strip()
                    break
            if not interface:
                return "Unknown"
            # Map interface name to type
            hardware = subprocess.check_output(
                ["networksetup", "-listallhardwareports"], text=True
            )
            port_name = ""
            for line in hardware.split('\n'):
                if line.startswith("Hardware Port:"):
                    port_name = line.split(":", 1)[1].strip()
                elif line.startswith("Device:") and interface in line:
                    if "Wi-Fi" in port_name:
                        return "Wi-Fi"
                    elif "Ethernet" in port_name or "LAN" in port_name or "Thunderbolt" in port_name:
                        return "Ethernet"
                    else:
                        return port_name
            return "Unknown"
        elif os_name == "Linux":
            result = subprocess.check_output(
                ["nmcli", "-t", "-f", "device,type,state"], text=True
            ).strip()
            for line in result.split('\n'):
                parts = line.split(":")
                if len(parts) >= 3 and parts[2] == "connected":
                    dev_type = parts[1]
                    if dev_type == "wifi":
                        return "Wi-Fi"
                    elif dev_type == "ethernet":
                        return "Ethernet"
                    else:
                        return dev_type.capitalize()
            return "Unknown"
        elif os_name == "Windows":
            result = subprocess.check_output(
                "netsh interface show interface", shell=True, text=True
            )
            for line in result.split('\n'):
                if "Connected" in line:
                    if "Wi-Fi" in line or "Wireless" in line:
                        return "Wi-Fi"
                    elif "Ethernet" in line or "Local Area" in line:
                        return "Ethernet"
                    else:
                        return line.split()[-1]
            return "Unknown"
        else:
            return "Unknown"
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.error(f"Could not determine connection type on {os_name}.")
        return "Unknown"

def get_wifi_ssid():
    """Gets the current Wi-Fi SSID for macOS, Linux, and Windows."""
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            command = "system_profiler SPAirPortDataType | awk '/Current Network/ {getline;$1=$1; gsub(\":\", \"\"); print;exit}'"
            ssid = subprocess.check_output(command, shell=True, text=True).strip()
        elif os_name == "Linux":
            command = ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"]
            result = subprocess.check_output(command, text=True).strip()
            for line in result.split('\n'):
                if line.startswith("yes:"):
                    return line.split(":")[1]
            return ""
        elif os_name == "Windows":
            command = "netsh wlan show interfaces"
            result = subprocess.check_output(command, shell=True, text=True)
            for line in result.split('\n'):
                if "SSID" in line and ":" in line:
                    return line.split(":")[1].strip()
            return ""
        else:
            return ""
        return ssid if ssid else ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.error(f"Could not determine Wi-Fi SSID on {os_name}.")
        return ""

def get_speed_test_results():
    """Runs a speed test and returns the download, upload, and ping speeds."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 10**6  # Convert to Mbps
        upload_speed = st.upload() / 10**6  # Convert to Mbps
        ping = st.results.ping
        return round(download_speed, 2), round(upload_speed, 2), round(ping, 2)
    except (speedtest.ConfigRetrievalError, speedtest.SpeedtestException) as e:
        logging.error(f"Speed test failed: {e}")
        return 0, 0, 0

def log_speed_data(data):
    """Appends a new row of speed test data to the CSV file."""
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    """Main loop to log Wi-Fi speed data every minute."""
    initialize_csv()
    while True:
        current_datetime = datetime.datetime.now()
        date = current_datetime.strftime("%Y-%m-%d")
        time_now = current_datetime.strftime("%H:%M:%S")

        connection_type = get_connection_type()
        wifi_ssid = get_wifi_ssid() if connection_type == "Wi-Fi" else ""
        download, upload, ping = get_speed_test_results()

        log_entry = [date, time_now, connection_type, wifi_ssid, download, upload, ping]
        log_speed_data(log_entry)

        logging.info(f"Logged: Type: {connection_type}, SSID: {wifi_ssid}, Download: {download} Mbps, Upload: {upload} Mbps, Ping: {ping} ms")

        time.sleep(60)

if __name__ == "__main__":
    main()
