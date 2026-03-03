import platform
import threading
import signal
import sys
import os
import subprocess

# Ensure we're running from the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from wifi_speed_logger import main as run_logger, CSV_FILE


def open_csv():
    """Opens the CSV file with the system's default application."""
    csv_path = os.path.abspath(CSV_FILE)
    os_name = platform.system()
    if os_name == "Darwin":
        subprocess.Popen(["open", csv_path])
    elif os_name == "Windows":
        os.startfile(csv_path)
    else:
        subprocess.Popen(["xdg-open", csv_path])


def launch_gui():
    """Launches a tkinter GUI window (macOS/Windows) with live results."""
    import tkinter as tk
    from queue import Queue

    result_queue = Queue()

    def on_result(entry):
        result_queue.put(entry)

    def start_logger():
        run_logger(callback=on_result)

    thread = threading.Thread(target=start_logger, daemon=True)
    thread.start()

    root = tk.Tk()
    root.title("Internet Speed Logger")
    root.resizable(False, False)

    window_width, window_height = 520, 420
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # --- Header ---
    header_frame = tk.Frame(root, padx=20, pady=15)
    header_frame.pack(fill="x")

    status_dot = tk.Label(header_frame, text="\u25cf", fg="#34C759", font=("Helvetica", 18))
    status_dot.pack(side="left", padx=(0, 8))

    status_label = tk.Label(
        header_frame,
        text="Internet Speed Logger is ON",
        font=("Helvetica", 16, "bold"),
    )
    status_label.pack(side="left")

    # --- Separator ---
    tk.Frame(root, height=1, bg="#CCCCCC").pack(fill="x", padx=20)

    # --- Latest result display ---
    result_frame = tk.Frame(root, padx=20, pady=15)
    result_frame.pack(fill="x")

    waiting_label = tk.Label(
        result_frame,
        text="Running speed test...",
        font=("Helvetica", 12),
        fg="#888888",
    )
    waiting_label.pack()

    latest_frame = tk.Frame(result_frame)

    labels = {}
    fields = [
        ("Connection", "connection"),
        ("Network", "ssid"),
        ("Download", "download"),
        ("Upload", "upload"),
        ("Ping", "ping"),
        ("Time", "time"),
    ]
    for i, (display_name, key) in enumerate(fields):
        tk.Label(latest_frame, text=f"{display_name}:", font=("Helvetica", 12, "bold"), anchor="e", width=12).grid(row=i, column=0, sticky="e", pady=2)
        labels[key] = tk.Label(latest_frame, text="--", font=("Helvetica", 12), anchor="w")
        labels[key].grid(row=i, column=1, sticky="w", padx=(10, 0), pady=2)

    # --- Separator ---
    tk.Frame(root, height=1, bg="#CCCCCC").pack(fill="x", padx=20)

    # --- Log history ---
    history_frame = tk.Frame(root, padx=20, pady=10)
    history_frame.pack(fill="both", expand=True)

    tk.Label(history_frame, text="Recent Tests", font=("Helvetica", 11, "bold"), anchor="w").pack(fill="x")

    history_text = tk.Text(history_frame, height=5, font=("Courier", 10), state="disabled", bg="#F5F5F5", relief="flat")
    history_text.pack(fill="both", expand=True, pady=(5, 0))

    # --- Buttons ---
    button_frame = tk.Frame(root, padx=20, pady=12)
    button_frame.pack(fill="x")

    open_csv_btn = tk.Button(
        button_frame, text="Open CSV File", command=open_csv,
        font=("Helvetica", 12), width=14,
    )
    open_csv_btn.pack(side="left")

    quit_button = tk.Button(
        button_frame, text="Quit", command=root.destroy,
        font=("Helvetica", 12), width=10,
    )
    quit_button.pack(side="right")

    def poll_results():
        while not result_queue.empty():
            entry = result_queue.get()
            date, time_val, conn_type, ssid, download, upload, ping = entry

            # Hide waiting label, show results
            waiting_label.pack_forget()
            latest_frame.pack()

            # Update latest result
            labels["connection"].config(text=conn_type)
            labels["ssid"].config(text=ssid if ssid else "--")
            labels["download"].config(text=f"{download} Mbps")
            labels["upload"].config(text=f"{upload} Mbps")
            labels["ping"].config(text=f"{ping} ms")
            labels["time"].config(text=f"{date}  {time_val}")

            # Add to history
            line = f"{time_val}  {conn_type:<10} \u2193{download:>8} Mbps  \u2191{upload:>8} Mbps  {ping:>6} ms\n"
            history_text.config(state="normal")
            history_text.insert("1.0", line)
            history_text.config(state="disabled")

        root.after(500, poll_results)

    root.after(500, poll_results)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()


def launch_terminal():
    """Launches a styled terminal UI (Linux)."""
    result_queue = []

    def on_result(entry):
        date, time_val, conn_type, ssid, download, upload, ping = entry
        network = f" ({ssid})" if ssid else ""
        print(f"  \033[1;36m{time_val}\033[0m  {conn_type}{network}  "
              f"\033[1;32m\u2193 {download} Mbps\033[0m  "
              f"\033[1;33m\u2191 {upload} Mbps\033[0m  "
              f"\033[1;35m{ping} ms\033[0m")

    thread = threading.Thread(target=run_logger, args=(on_result,), daemon=True)
    thread.start()

    banner = """
\033[1;32m\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557
\u2551                                                  \u2551
\u2551        Internet Speed Logger is ON               \u2551
\u2551                                                  \u2551
\u2551   Logging speed data every 60 seconds...         \u2551
\u2551   Press Ctrl+C to shut down.                     \u2551
\u2551                                                  \u2551
\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\033[0m
"""
    print(banner)

    def handle_signal(sig, frame):
        print("\n\033[1;31mShutting down Internet Speed Logger...\033[0m")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)

    # Keep the main thread alive
    signal.pause()


if __name__ == "__main__":
    os_name = platform.system()
    if os_name in ("Darwin", "Windows"):
        launch_gui()
    else:
        launch_terminal()
