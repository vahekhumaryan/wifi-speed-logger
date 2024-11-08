import speedtest
import pandas as pd
import time
import csv
import datetime
import subprocess
import platform

# Path to the CSV log file
csv_file = 'wifi_speed_log.csv'

# Column headers
headers = ['Date', 'Time', 'Wi-Fi SSID', 'Download Speed (Mbps)', 'Upload Speed (Mbps)', 'Ping (ms)']

# Initialize CSV log file with headers if not present
try:
    with open(csv_file, 'x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
except FileExistsError:
    pass  # File already exists, skip writing headers

# Function to get the current Wi-Fi SSID
def get_wifi_ssid():
    try:
        if platform.system() == "Darwin":  # macOS
            ssid = subprocess.check_output(
                "system_profiler SPAirPortDataType | awk '/Current Network/ {getline;$1=$1; gsub(\":\", \"\"); print;exit}'",
                shell=True
            )
            ssid = ssid.decode("utf-8").strip()
            return ssid if ssid else "No Wi-Fi"
        else:  # Assume Linux
            result = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"])
            result = result.decode("utf-8").strip()
            for line in result.split('\n'):
                if line.startswith("yes:"):
                    return line.split(":")[1]
        return "No Wi-Fi"
    except subprocess.CalledProcessError:
        return "No Wi-Fi"

# Function to run speed test and return results
def get_speed_test_results():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Automatically select the best server based on ping
        download_speed = st.download() / 10**6  # Convert to Mbps
        upload_speed = st.upload() / 10**6  # Convert to Mbps
        ping = st.results.ping
        return round(download_speed, 2), round(upload_speed, 2), round(ping, 2)
    except (speedtest.ConfigRetrievalError, speedtest.SpeedtestException) as e:
        print(f"Network error occurred: {e}")
        return 0, 0, 0  # Return 0 for download, upload, and ping in case of error

# Main loop to log data every minute
while True:
    # Get current date and time
    current_datetime = datetime.datetime.now()
    date = current_datetime.strftime("%Y-%m-%d")
    time_now = current_datetime.strftime("%H:%M:%S")
    
    # Get Wi-Fi SSID and speed test results
    wifi_ssid = get_wifi_ssid()
    download_speed, upload_speed, ping = get_speed_test_results()
    
    # Log data to CSV
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, time_now, wifi_ssid, download_speed, upload_speed, ping])
    
    print(f"Logged: {date} {time_now} - SSID: {wifi_ssid}, Download: {download_speed} Mbps, Upload: {upload_speed} Mbps, Ping: {ping} ms")
    
    # Wait 1 minute before next entry
    time.sleep(60)
