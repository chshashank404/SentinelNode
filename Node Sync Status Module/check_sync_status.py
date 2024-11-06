import requests
import time
from collections import deque

# Node and alert configurations
node_url = "http://localhost:4001"  # LocalNet Algorand node URL
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # Replace with your LocalNet API token
alert_webhook_url = #"Slack Webhook goes here."   Replace with your Slack webhook URL

headers = {"X-Algo-API-Token": algod_token}
round_threshold = 10  # Threshold for time-since-last-round in seconds
max_round_history = 5  # Number of rounds to track in history

# Track recent rounds and sync times
round_history = deque(maxlen=max_round_history)
time_since_last_round_history = deque(maxlen=max_round_history)

# Function to check sync status on LocalNet
def check_sync_status():
    try:
        response = requests.get(f"{node_url}/v2/status", headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Retrieve round and time-since-last-round
            last_round = data.get("last-round", None)
            time_since_last_round = data.get("time-since-last-round", None)

            # Log status for debugging
            print(f"Node Sync Status: last-round = {last_round}, time-since-last-round = {time_since_last_round} seconds")

            # Store recent history
            if last_round is not None:
                round_history.append(last_round)
            if time_since_last_round is not None:
                time_since_last_round_history.append(time_since_last_round)

            # Calculate average time-since-last-round
            if time_since_last_round_history:
                avg_time_since_last_round = sum(time_since_last_round_history) / len(time_since_last_round_history)
            else:
                avg_time_since_last_round = 0

            # Determine if alert is needed based on threshold and history
            if last_round is None or time_since_last_round is None:
                send_alert("Node sync check error: Missing 'last-round' or 'time-since-last-round'.")
            elif time_since_last_round > round_threshold:
                send_alert(
                    f"High time-since-last-round detected: {time_since_last_round} seconds "
                    f"(Avg: {avg_time_since_last_round:.2f}s over last {len(time_since_last_round_history)} rounds)."
                )
        else:
            send_alert("Node health check failed with status code: " + str(response.status_code))
    except requests.exceptions.RequestException as e:
        print(f"Network error during sync check: {e}")
        send_alert(f"Network error in sync check: {e}")
    except Exception as e:
        print(f"Error checking sync status: {e}")
        send_alert(f"Error in node sync check: {e}")

# Function to send alerts with improved context
def send_alert(message):
    print("Alert:", message)
    try:
        response = requests.post(alert_webhook_url, json={"text": message})
        if response.status_code == 200:
            print("Alert sent successfully.")
        else:
            print(f"Failed to send alert with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending alert: {e}")

# Periodically run the sync status check
while True:
    check_sync_status()
    time.sleep(20)  # Check every 20 seconds
