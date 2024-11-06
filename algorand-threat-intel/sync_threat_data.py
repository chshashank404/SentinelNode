import os
import time
import requests
import json

# GitHub repository URL for the raw JSON file (replace with your actual repository path)
GITHUB_REPO_URL = "https://github.com/chshashank404/SentinelNode/raw/refs/heads/main/algorand-threat-intel/threat_data.json"

# Local path to store the downloaded threat data
LOCAL_DATA_PATH = "./local_threat_data.json"

# Sync interval (in seconds) - Adjust as needed
SYNC_INTERVAL = 3600  # Sync every hour

def download_threat_data():
    try:
        response = requests.get(GITHUB_REPO_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the threat data to the local file
        with open(LOCAL_DATA_PATH, "w") as f:
            f.write(response.text)
        print(f"Threat data synced successfully at {time.ctime()}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading threat data: {e}")

def periodic_sync():
    while True:
        download_threat_data()
        time.sleep(SYNC_INTERVAL)

# Run the periodic sync function
if __name__ == "__main__":
    periodic_sync()
yali
