import hashlib
import requests
import os
import time
from datetime import datetime

# Critical files and their expected hashes
critical_files = {
    #Path to the critical files are to be placecd here.
}

# Slack webhook URL for alerts
alert_webhook_url = #"Slack Web Hook goes here."
ALERT_THRESHOLD = 3  # Number of integrity violations before alert
integrity_violations = 0  # Counter for integrity violations

# Check file integrity by comparing hash
def check_file_integrity(file_path, expected_hash):
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        file_hash = hashlib.sha256(file_content).hexdigest()

        if file_hash != expected_hash:
            print(f"Tampering detected: {file_path}")
            return False
        return True
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except PermissionError:
        print(f"Permission denied: {file_path}")
        return False

# Function to check file permissions (example: ensure read-only)
def check_file_permissions(file_path):
    try:
        st = os.stat(file_path)
        # Check if the file is not writable (only owner has read permission)
        if (st.st_mode & 0o222) != 0:
            print(f"Permission issue detected for {file_path}")
            return False
        return True
    except FileNotFoundError:
        print(f"File not found for permissions check: {file_path}")
        return False
    except PermissionError:
        print(f"Permission denied for permissions check: {file_path}")
        return False

# Send alert with retry logic
def send_alert(message):
    for _ in range(3):  # Retry 3 times
        try:
            response = requests.post(alert_webhook_url, json={"text": message})
            if response.status_code == 200:
                print("Alert sent successfully.")
                break
            else:
                print(f"Failed to send alert with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending alert: {e}")

# Monitor integrity of each critical file
def integrity_monitor():
    global integrity_violations
    for file, expected_hash in critical_files.items():
        # Check file integrity and permissions
        integrity_ok = check_file_integrity(file, expected_hash)
        permissions_ok = check_file_permissions(file)
        
        if not integrity_ok or not permissions_ok:
            integrity_violations += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            alert_message = (
                f"Tampering or permission issue detected!\n"
                f"File: {file}\n"
                f"Timestamp: {timestamp}\n"
                f"Expected Hash: {expected_hash}\n"
                f"Integrity check: {'FAILED' if not integrity_ok else 'PASSED'}\n"
                f"Permissions check: {'FAILED' if not permissions_ok else 'PASSED'}\n"
                f"Total Violations: {integrity_violations}"
            )
            print(alert_message)  # Log to console

            # Send alert if the number of violations reaches the threshold
            if integrity_violations >= ALERT_THRESHOLD:
                send_alert(alert_message)
                integrity_violations = 0  # Reset the counter after alert

# Run the integrity check periodically (e.g., every minute)
while True:
    integrity_monitor()
    time.sleep(60)
