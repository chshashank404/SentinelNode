
---

# File Integrity Monitoring Module

**file_integrity.py** is a Python script designed to monitor critical files for unauthorized changes within the `algokit_sandbox_algod` Docker container in an Algorand LocalNet setup. It verifies the integrity of sensitive files by comparing their hashes to expected values. If tampering or unauthorized modifications are detected, it sends alerts to a specified Slack webhook.

This module includes:
- **file_integrity.py**: Main integrity-checking script
- **hash_calculations.sh**: Bash script to calculate and output hash values for critical files
- **requirements.txt**: List of required Python packages

## Prerequisites

1. **Install Python**:
   - Ensure Python 3 is installed in the `algokit_sandbox_algod` Docker container.
2. **Create a Virtual Environment**:
   - Set up a Python virtual environment within the container to manage dependencies.

## Setup and Execution Process

### 1. Access the Docker Container

Start by opening a terminal session in the `algokit_sandbox_algod` Docker container.

------ add a docker image here

### 2. Install Python3 and Set Up Virtual Environment

Inside the `algokit_sandbox_algod` Docker container:

1. **Install Python3** (if not already installed):
   ```bash
   apt update && apt install -y python3 python3-venv
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv nodeguard
   source nodeguard/bin/activate
   ```

### 3. Install Dependencies

Once the virtual environment is active, install the dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Calculate Hashes of Critical Files

To begin monitoring, you’ll need the expected hash values of each critical file. Run the `hash_calculations.sh` script in the container to calculate these hashes:

```bash
bash hash_calculations.sh
```

This script will output the hash values for each critical file. Copy these hash values and add them to the `file_integrity.py` file under the `critical_files` dictionary, replacing any placeholder values. For example:

```python
critical_files = {
    "/path/to/critical/file1": "calculated_hash_value1",
    "/path/to/critical/file2": "calculated_hash_value2",
    # Add more files as needed
}
```

### 5. Add Your Slack Webhook

In `file_integrity.py`, add your Slack webhook URL for receiving alerts. Replace the placeholder with your actual Slack webhook URL in the `send_alert` function:

```python
alert_webhook_url = "https://hooks.slack.com/services/your/webhook/url"
```

### 6. Run the Integrity Check

With the hashes and webhook in place, you can now run `file_integrity.py`:

```bash
python file_integrity.py
```

The script will:
- Check each critical file's hash against the expected value.
- Alert via Slack if any tampering or unauthorized changes are detected.

---

## Example Workflow

1. Open a terminal in the `algokit_sandbox_algod` Docker container:
   ```bash
   docker exec -it algokit_sandbox_algod /bin/bash
   ```

2. Install Python, set up a virtual environment, and activate it:
   ```bash
   apt update && apt install -y python3 python3-venv
   python3 -m venv nodeguard
   source nodeguard/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Calculate file hashes:
   ```bash
   bash hash_calculations.sh
   ```

5. Copy the calculated hash values to `file_integrity.py` and configure your Slack webhook.

6. Run the integrity check:
   ```bash
   python file_integrity.py
   ```

## Notes

- Ensure that `hash_calculations.sh` includes paths for all critical files you want to monitor.
- Review the permissions for each critical file to ensure that `file_integrity.py` has access.

This setup allows for secure and effective monitoring of critical files within your `algokit_sandbox_algod` Docker container, sending alerts upon detection of unauthorized changes.
