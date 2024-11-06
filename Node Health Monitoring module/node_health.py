import docker
import time
import requests
import psutil  # For disk usage
from datetime import datetime

# Initialize Docker client and container
client = docker.from_env()
container = client.containers.get("algokit_sandbox_algod")

# Initialize previous CPU and system usage values
previous_cpu = 0
previous_system = 0

# Slack webhook URL for alerts
alert_webhook_url = #"Slack Web hook goes here."

# Thresholds
CPU_THRESHOLD = 80  # 80% CPU usage
MEMORY_THRESHOLD_MB = 2048  # 2GB in MB
DISK_USAGE_THRESHOLD = 80  # 80% Disk usage
NETWORK_RATE_THRESHOLD = 100 * 1024 * 1024  # 100MB per minute

# Track historical CPU and memory for calculating averages
historical_cpu = []
historical_memory = []

def calculate_cpu_percent():
    global previous_cpu, previous_system
    try:
        stats = container.stats(stream=False)
        cpu_delta = float(stats['cpu_stats']['cpu_usage']['total_usage']) - previous_cpu
        system_delta = float(stats['cpu_stats']['system_cpu_usage']) - previous_system

        # Update previous values for the next calculation
        previous_cpu = float(stats['cpu_stats']['cpu_usage']['total_usage'])
        previous_system = float(stats['cpu_stats']['system_cpu_usage'])

        # Calculate CPU percentage
        if system_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * 100.0
        else:
            cpu_percent = 0.0  # Avoid division by zero

        # Track historical CPU usage
        historical_cpu.append(cpu_percent)
        if len(historical_cpu) > 30:
            historical_cpu.pop(0)  # Keep the last 30 records

        return round(cpu_percent, 2)

    except docker.errors.NotFound:
        print("Container not found.")
        return None
    except Exception as e:
        print(f"Error calculating CPU usage: {e}")
        return None

def get_memory_usage():
    try:
        stats = container.stats(stream=False)
        memory_usage = stats['memory_stats']['usage']
        memory_limit = stats['memory_stats']['limit']
        memory_percent = (memory_usage / memory_limit) * 100 if memory_limit > 0 else 0
        
        # Track historical memory usage
        historical_memory.append(memory_percent)
        if len(historical_memory) > 30:
            historical_memory.pop(0)  # Keep the last 30 records

        return round(memory_usage / 1024**2, 2), round(memory_percent, 2)  # MB and percentage

    except docker.errors.NotFound:
        print("Container not found.")
        return None, None
    except Exception as e:
        print(f"Error calculating memory usage: {e}")
        return None, None

def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return disk_usage.percent

def monitor_network():
    stats = container.stats(stream=False)
    network_rx = stats['networks']['eth0']['rx_bytes']
    network_tx = stats['networks']['eth0']['tx_bytes']
    return network_rx, network_tx

def calculate_average(metrics_list):
    return round(sum(metrics_list) / len(metrics_list), 2) if metrics_list else 0

def send_alert(message):
    try:
        response = requests.post(alert_webhook_url, json={"text": message})
        if response.status_code == 200:
            print("Alert sent successfully.")
        else:
            print(f"Failed to send alert: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending alert: {e}")

# Monitor CPU, memory, disk, and network every 10 seconds
while True:
    # CPU and Memory Monitoring
    cpu_percent = calculate_cpu_percent()
    memory_usage, memory_percent = get_memory_usage()
    disk_usage = get_disk_usage()
    network_rx, network_tx = monitor_network()

    # Output metrics
    if cpu_percent is not None:
        print(f"CPU Usage: {cpu_percent}% (Average: {calculate_average(historical_cpu)}%)")
        if cpu_percent > CPU_THRESHOLD:
            send_alert(f"High CPU usage detected: {cpu_percent}%")

    if memory_usage is not None:
        print(f"Memory Usage: {memory_usage} MB ({memory_percent}%) (Average: {calculate_average(historical_memory)}%)")
        if memory_usage > MEMORY_THRESHOLD_MB:
            send_alert(f"High Memory usage detected: {memory_usage} MB ({memory_percent}%)")

    # Disk Usage Monitoring
    print(f"Disk Usage: {disk_usage}%")
    if disk_usage > DISK_USAGE_THRESHOLD:
        send_alert(f"High Disk usage detected: {disk_usage}%")

    # Network Usage Monitoring (output for inspection)
    print(f"Network Rx: {network_rx / 1024**2:.2f} MB, Tx: {network_tx / 1024**2:.2f} MB")
    if network_rx + network_tx > NETWORK_RATE_THRESHOLD:
        send_alert("High network traffic detected!")

    time.sleep(10)
