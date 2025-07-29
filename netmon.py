#!/usr/bin/env python3
import os
import subprocess
import time

def check_network_connectivity(host="8.8.8.8", count=3):
    """
    Checks network connectivity by pinging a specified host.
    Returns True if successful, False otherwise.
    """
    try:
        # Use subprocess to run the ping command
        # -c for count (number of pings)
        # -W for timeout (in seconds)
        subprocess.check_output(
            ["ping", "-c", str(count), "-W", "1", host],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def reboot_system():
    """
    Initiates a system reboot.
    This command requires appropriate permissions (e.g., running as root or with sudo).
    """
    print("Network lost. Initiating system reboot...")
    try:
        if os.name == "posix":  # Linux/macOS
            os.system("sudo reboot")
        elif os.name == "nt":  # Windows
            os.system("shutdown /r /t 0")
        else:
            print("Unsupported operating system for direct reboot.")
    except Exception as e:
        print(f"Error during reboot: {e}")

if __name__ == "__main__":
    ping_target = "8.8.8.8"  # Google Public DNS
    failure_threshold = 30   # Number of consecutive failures before reboot
    check_interval = 30      # Seconds between checks

    consecutive_failures = 0

    while True:
        #print ('net check...')
        if not check_network_connectivity(ping_target):
            consecutive_failures += 1
            print(f"Network check failed. Consecutive failures: {consecutive_failures}")
            if consecutive_failures >= failure_threshold:
                reboot_system()
                break  # Exit the loop after initiating reboot
        else:
            if consecutive_failures > 0:
                print("Network reconnected.")
            consecutive_failures = 0

        time.sleep(check_interval)
