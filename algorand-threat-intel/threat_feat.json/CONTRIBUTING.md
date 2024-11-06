# Contributing to Algorand Threat Intelligence Repository

Thank you for considering contributing to this open-source threat intelligence repository! By sharing known malicious addresses, suspicious domains, and other indicators of compromise, you help make blockchain networks more secure.

## How to Contribute

1. **Fork the Repository**
   - Click on the "Fork" button at the top-right corner of this page.
   - This creates a copy of the repository in your GitHub account.

2. **Clone the Forked Repository**
   - Clone your fork to your local machine using:
     ```bash
     git clone https://github.com/YOUR_USERNAME/algorand-threat-intel.git
     cd algorand-threat-intel
     ```

3. **Create a New Branch**
   - Create a new branch for your contribution:
     ```bash
     git checkout -b add-new-threat-data
     ```

4. **Add or Update Threat Data**
   - Open the `threat_data.json` file.
   - Add or update entries in the relevant sections: `malicious_wallets`, `suspicious_domains`, `phishing_sites`, `compromised_smart_contracts`, or `malicious_ips`.
   - Ensure each entry includes:
     - A valid format for each field (see examples below).
     - An appropriate `category` and `description` to provide context.

5. **Commit Your Changes**
   - Once you’ve made your changes, commit them:
     ```bash
     git add threat_data.json
     git commit -m "Add new malicious wallet address for Algorand"
     ```

6. **Push and Create a Pull Request**
   - Push your changes to your GitHub repository:
     ```bash
     git push origin add-new-threat-data
     ```
   - Go to the main repository and create a pull request.

## Contribution Requirements

- **Required Fields:** Ensure all required fields (`address`, `network`, `category`, etc.) are filled.
- **Data Format:** Contributions should follow the exact format in `threat_data.json`.
- **Verification:** Where possible, add information on why an address or domain is suspicious.

## Code of Conduct

Please ensure contributions are respectful and accurate. Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---

**Examples for Contribution**

### Malicious Wallet
```json
{
  "address": "ALGO1234EXAMPLExyz1234ALGO",
  "network": "Algorand",
  "category": "Phishing",
  "description": "Used in phishing attempts.",
  "last_seen": "2024-11-01"
}
```

### Suspicious Domain
```json
{
  "domain": "example-phishing.com",
  "category": "Phishing",
  "description": "Pretends to be an official wallet provider.",
  "last_seen": "2024-10-29"
}
```

Thank you for helping build a safer blockchain environment!
