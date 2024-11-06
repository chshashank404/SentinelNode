import json
import time
import requests

# Paths and configurations
LOCAL_THREAT_DATA_PATH = "./local_threat_data.json"
SLACK_WEBHOOK_URL = #"Slack Webhook goes here"   Replace with your actual Slack webhook URL

# Load threat data from the local JSON file
def load_threat_data():
    try:
        with open(LOCAL_THREAT_DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Local threat data file not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding threat data JSON: {e}")
        return {}

# Check if any given input matches known threats
def check_for_threats(activity_data, threat_data):
    alerts = []
    
    # Check for malicious wallet addresses
    for wallet in threat_data.get("malicious_wallets", []):
        if activity_data.get("wallet_address") == wallet["address"]:
            alerts.append(f"Malicious wallet address detected: {wallet['address']} ({wallet['category']})")

    # Check for suspicious domains
    for domain in threat_data.get("suspicious_domains", []):
        if activity_data.get("domain") == domain["domain"]:
            alerts.append(f"Suspicious domain detected: {domain['domain']} ({domain['category']})")

    # Check for phishing sites
    for site in threat_data.get("phishing_sites", []):
        if activity_data.get("url") == site["url"]:
            alerts.append(f"Phishing site detected: {site['url']} ({site['category']})")

    # Check for malicious IP addresses
    for ip in threat_data.get("malicious_ips", []):
        if activity_data.get("ip_address") == ip["ip_address"]:
            alerts.append(f"Malicious IP address detected: {ip['ip_address']} ({ip['category']})")

    return alerts
# Send alert to Slack
def send_alert(message):
    try:
        requests.post(SLACK_WEBHOOK_URL, json={"text": message})
    except requests.exceptions.RequestException as e:
        print(f"Error sending alert: {e}")

# Anomaly detection function
def detect_anomalies(activity_data):
    threat_data = load_threat_data()
    alerts = check_for_threats(activity_data, threat_data)

    for alert in alerts:
        print(alert)
        send_alert(alert)

# Example usage
if __name__ == "__main__":
    # Simulated activity data to check
    activity_sample = {
        "wallet_address": "ALGO1234EXAMPLExyz1234ALGO",
        "domain": "example-phishing.com",
        "url": "https://scam-site.io",
        "ip_address": "192.168.1.100"
    }

    # Run anomaly detection
    detect_anomalies(activity_sample)
