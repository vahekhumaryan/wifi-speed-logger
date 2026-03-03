import platform
import threading
import signal
import sys
import os

# Ensure we're running from the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from wifi_speed_logger import main as run_logger


def run_logger_thread():
    """Runs the speed logger in a background thread."""
    thread = threading.Thread(target=run_logger, daemon=True)
    thread.start()
    return thread


def launch_gui():
    """Launches a tkinter GUI window (macOS/Windows)."""
    import tkinter as tk

    run_logger_thread()

    root = tk.Tk()
    root.title("Internet Speed Logger")
    root.resizable(False, False)

    window_width, window_height = 420, 180
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    frame = tk.Frame(root, padx=30, pady=20)
    frame.pack(expand=True, fill="both")

    status_label = tk.Label(
        frame,
        text="The Internet Speed Logger is ON.",
        font=("Helvetica", 16, "bold"),
    )
    status_label.pack(pady=(10, 5))

    info_label = tk.Label(
        frame,
        text="To shut down, quit the app.",
        font=("Helvetica", 12),
        fg="#555555",
    )
    info_label.pack(pady=(0, 15))

    quit_button = tk.Button(
        root,
        text="Quit",
        command=root.destroy,
        font=("Helvetica", 12),
        width=10,
    )
    quit_button.pack(pady=(0, 15))

    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()


def launch_terminal():
    """Launches a styled terminal UI (Linux)."""
    run_logger_thread()

    banner = """
\033[1;32m╔══════════════════════════════════════════════════╗
║                                                  ║
║        Internet Speed Logger is ON               ║
║                                                  ║
║   Logging speed data every 60 seconds...         ║
║   Press Ctrl+C to shut down.                     ║
║                                                  ║
╚══════════════════════════════════════════════════╝\033[0m
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
