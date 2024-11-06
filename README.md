---

# **SentinelNode**
Welcome to **SentinelNode**, an open-source security framework designed to enhance the security and resilience of blockchain nodes, specifically focusing on Algorand but extensible to other blockchains. The project aims to provide a comprehensive suite of tools that monitor, protect, and harden blockchain nodes at the system level. Our goal is to make node-level security tools accessible to developers, researchers, and node operators, fostering a community-driven approach to improving the security of blockchain infrastructure.

---

## Project Overview

As blockchain technology matures, securing individual nodes has become increasingly important, especially in decentralized networks where each node plays a critical role in maintaining the security and integrity of the network. **SentinelNode** addresses node-level security concerns through a suite of independent but interoperable modules, each targeting specific aspects of node security. These modules are:

- **Node Health Monitoring**: Monitors CPU, memory, and other resource usage, sending alerts for anomalies.
- **File Integrity Monitoring**: Ensures critical files on the node remain untampered, alerting on unauthorized changes.
- **Node Sync Status**: Continuously checks the node’s synchronization with the blockchain, notifying if it falls behind.
- **NGINX Hardening**: Provides a hardened NGINX configuration for nodes acting as API gateways, helping mitigate attack vectors.
- **Threat Intelligence and Anomaly Detection**: A community-driven threat intelligence module to detect suspicious activity and known malicious addresses.

Each module is designed to be modular and open-source, making it easy for developers to implement, modify, and contribute to the project. SentinelNode is ideal for Algorand node operators and can be adapted for other blockchain ecosystems.

---

## Modules

### 1. Node Health Monitoring Module

**Directory:** `/node_health_monitoring`

The **Node Health Monitoring Module** tracks key system metrics such as CPU, memory, disk usage, and network bandwidth in real-time. It ensures the node is running optimally by:
- Monitoring CPU, memory, and disk usage, alerting on anomalies.
- Providing Slack webhook alerts for resource threshold breaches.
- Detecting abnormal patterns in resource usage, potentially indicating security threats.

### 2. File Integrity Module

**Directory:** `/file_integrity`

The **File Integrity Module** is critical for protecting sensitive files associated with the node’s operation and configuration. This module:
- Calculates and stores the hash of critical files, such as keys and configuration files.
- Periodically verifies file integrity against stored hashes, alerting if any tampering is detected.
- Ensures only authorized changes are made to key files, enhancing node security.

### 3. Node Sync Status Module

**Directory:** `/node_sync_status`

The **Node Sync Status Module** monitors the synchronization status of the Algorand node with the blockchain. Key features include:
- Regular checks of the node’s sync status and time since the last round.
- Alerts if the node falls behind or experiences delays in processing new rounds.
- Helps ensure the node is correctly participating in the blockchain’s consensus process, critical for maintaining network integrity.

### 4. NGINX Hardening Module

**Directory:** `/nginx_hardening`

The **NGINX Hardening Module** provides a hardened configuration for nodes that act as API gateways or handle external requests. By implementing security best practices for NGINX, this module:
- Enforces rate limiting to mitigate DDoS attacks.
- Adds security headers to protect against common web-based attacks.
- Configures access restrictions and disables unused protocols.
- Offers a secure setup that can be adapted for Algorand nodes and other blockchain-related applications.

### 5. Algorand Threat Intelligence and Anomaly Detection Module

**Directory:** `/algorand_threat_intel`

The **Algorand Threat Intelligence and Anomaly Detection Module** is a collaborative effort to track and detect known malicious addresses, suspicious domains, and other indicators of compromise. This module:
- Regularly syncs with a GitHub-hosted threat intelligence repository.
- Integrates with real-time monitoring to detect and alert on suspicious activity associated with known malicious addresses.
- Provides an open-source threat database where developers can contribute new threat indicators.
- Aims to enhance Algorand node security by identifying and responding to known threats.

---

## How to Use SentinelNode

1. **Clone the Repository**: Start by cloning the SentinelNode repository to your local environment:
   ```bash
   git clone https://github.com/chshashank404/SentinelNode.git
   cd SentinelNode
   ```

2. **Install Dependencies**: Each module has its own set of dependencies. Refer to the `requirements.txt` in each module's directory and install dependencies as needed:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Configuration Files**: Each module includes configuration options. Edit the configuration files according to your node setup (e.g., adding Slack webhook URLs, setting thresholds for alerts, specifying critical file paths).

4. **Run Modules Individually or Collectively**: You can run each module individually by navigating to the module directory and executing the relevant Python scripts, or integrate them into a larger monitoring system.

---

## Future Goals

- **Cross-Blockchain Compatibility**: Extend compatibility to other blockchains beyond Algorand.
- **Advanced Anomaly Detection**: Leverage machine learning for more accurate anomaly detection.
- **Improved Threat Intelligence**: Enhance the Algorand-Threat-Intel module with more granular threat data.

---

Thank you for using **SentinelNode** and contributing to a safer blockchain ecosystem. Together, we’re building a robust, community-driven framework for node-level security.
