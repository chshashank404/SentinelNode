# Algorand Node NGINX Hardening Module

## Project Overview

This repository provides an NGINX hardening module for enhancing the security and stability of Algorand nodes running within Docker. The module introduces a hardened configuration tailored for blockchain infrastructure, with a focus on Algorand, to safeguard against common threats, improve performance, and ensure reliable access to node services.

### Key Features
- **Rate Limiting & Connection Control**: Prevents abuse through configurable request rate limits and connection quotas.
- **Security Headers**: Adds industry-standard headers to mitigate XSS, clickjacking, and content-sniffing attacks.
- **IP Whitelisting**: Optionally restricts access to trusted IPs only.
- **Enhanced Logging Options**: Logs are suppressed by default but can be enabled for debugging purposes.

---

## Configuration Explanation

The following key settings are configured in the NGINX hardening module:

- **Rate Limiting (`limit_req_zone` and `limit_req`)**: Controls the rate of incoming requests to prevent denial-of-service (DoS) attacks.
  - `limit_req_zone $binary_remote_addr zone=api_limit:10m rate=5r/s;` limits each client to 5 requests per second.
  - `limit_req zone=api_limit burst=10 nodelay;` allows occasional bursts of 10 requests with no delay.
  
- **Connection Limiting (`limit_conn_zone` and `limit_conn`)**: Restricts the maximum number of simultaneous connections per client.
  - `limit_conn_zone $binary_remote_addr zone=conn_limit:10m;` tracks connections by client IP.
  - `limit_conn conn_limit 20;` limits each client to 20 concurrent connections.

- **Security Headers**:
  - `X-Content-Type-Options "nosniff";` prevents browsers from interpreting files as a different MIME type.
  - `X-Frame-Options "DENY";` blocks the page from being displayed in a frame, preventing clickjacking attacks.
  - `X-XSS-Protection "1; mode=block";` enables XSS filtering and blocks the page if an attack is detected.
  - `Strict-Transport-Security "max-age=31536000; includeSubDomains" always;` enforces HTTPS for 1 year.
  - `Content-Security-Policy "default-src 'self'; frame-ancestors 'none';";` restricts the sources of content and disables framing.

- **CORS Configuration (`map` and `add_header`)**: Configures Cross-Origin Resource Sharing for private network requests.
  - `map` and `add_header` directives allow the Algorand node to communicate securely within a private network.

- **IP Whitelisting** *(Optional)*:
  - The configuration includes an optional whitelist for trusted IPs.
  - Uncomment and configure IP addresses to allow only specific clients to access the node.

---

## Usage

### Prerequisites
1. **Docker**: Ensure Docker is installed and running.
2. **NGINX in Docker**: This configuration assumes NGINX is running as a reverse proxy for Algorand services in a Docker container.
3. **Access to NGINX Container**: You should have permissions to modify the NGINX configuration inside the Docker container.

### Applying the Configuration
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/algorand-nginx-hardening.git
   cd algorand-nginx-hardening
   ```

2. **Copy Hardened NGINX Configuration**:
   - Replace the existing NGINX configuration with the hardened version.
   ```bash
   docker cp hardened_nginx.conf <nginx_container_name>:/etc/nginx/nginx.conf
   ```

3. **Reload NGINX**:
   - Restart NGINX to apply the changes.
   ```bash
   docker exec <nginx_container_name> nginx -s reload
   ```

### Verifying the Setup
1. **Check NGINX Status**:
   - Ensure NGINX is running correctly by checking logs and container status:
   ```bash
   docker logs <nginx_container_name>
   ```

2. **Test Rate Limiting**:
   - Try sending rapid, repeated requests from a single IP to verify rate limiting. If configured correctly, requests should be throttled after the limit is reached.

3. **Inspect Security Headers**:
   - Use `curl` or a browser’s Developer Tools to check for security headers in the response.
   ```bash
   curl -I http://localhost:4001
   ```

4. **IP Whitelisting (If Enabled)**:
   - Attempt accessing from both a whitelisted IP and a non-whitelisted IP to verify access control.

---

## Testing the Configuration

To test the hardened NGINX setup, perform the following checks:

1. **Rate Limiting Test**:
   - Use a tool like `ab` (Apache Bench) or `curl` in a loop to send multiple requests and observe if NGINX starts limiting requests.
   ```bash
   ab -n 100 -c 10 http://localhost:4001/
   ```
   - You should see HTTP 429 errors ("Too Many Requests") when the rate limit is exceeded.

2. **Security Header Test**:
   - Verify the response headers using `curl` or browser tools:
   ```bash
   curl -I http://localhost:4001
   ```
   - Confirm that `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Strict-Transport-Security`, and `Content-Security-Policy` headers are present.

3. **Connection Limiting Test**:
   - Open multiple connections (more than the configured limit) and verify that additional connections are dropped.
   - Example with `curl`:
   ```bash
   for i in {1..25}; do curl http://localhost:4001 & done
   ```

### Additional Tips
- For production, monitor the logs to adjust rate limits and connection counts based on real traffic patterns.
- Regularly check for any NGINX updates or patches, as new security improvements may become available.

---

This NGINX hardening module enhances the reliability and security of Algorand nodes. We encourage contributions to expand or further optimize this configuration for different environments.
