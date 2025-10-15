import subprocess
import psutil
import csv
import time
from datetime import datetime

# Function to ping and return status and response time
def ping():
    try:
        # For Linux/Mac use "ping -c 1 8.8.8.8"
        # For Windows use "ping -n 1 8.8.8.8"
        response = subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True)
        
        if response.returncode == 0:  # Success
            # Extract the response time from the output
            ping_ms = float(response.stdout.split("time=")[1].split(" ms")[0])
            return "UP", ping_ms
        else:
            return "DOWN", -1
    except Exception as e:
        return "DOWN", -1

# Function to log system metrics
def log_system_metrics(log_file='log.csv'):
    # Open or create the log CSV file
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Check if file is empty, if so, write headers
        if file.tell() == 0:
            writer.writerow(["Timestamp", "CPU", "Memory", "Disk", "Ping_Status", "Ping_ms"])
        
        # Capture the system metrics
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        ping_status, ping_ms = ping()
        
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Write a new log entry
        writer.writerow([timestamp, cpu, memory, disk, ping_status, ping_ms])

# Main function to execute and log 5 entries with a 10-second delay
def main():
    for _ in range(5):
        log_system_metrics()
        time.sleep(10)  # Wait for 10 seconds between logs

if __name__ == "__main__":
    main()
