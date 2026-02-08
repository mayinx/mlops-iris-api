# 🏛️ MLOps Reference Project: Iris API "The Fortress"
### A Scalable, Secure, and Observable Machine Learning Deployment

## 🎭 Tech Stack Overview
🐋 **DOCKER** (Containerization) | 🛡️ **NGINX** (Security & Load Balancing) | 🔥 **PROMETHEUS** (Metrics) | 📊 **GRAFANA** (Visualization) | 🐍 **FASTAPI** (ML Logic) | 🐍 PYTHON

## 🛠️ Engineering Audit & Refactor
This project is based on the **Nginx & MLOps** series by DataScientest. While the tutorial provides the baseline, this repository represents a **hardened refactor** to address real-world production blockers found during implementation:

* **The Monitoring "Backdoor":** Resolved an internal loop where the Nginx Exporter was trapped by global HTTPS redirects. I implemented a Port 80 status "backdoor" to allow metric scraping without SSL handshake overhead.
* **CIDR Subnet Portability:** Replaced hardcoded `/24` sniper IPs with a `/12` "Docker City" mask, ensuring the infrastructure is portable across different host environments.
* **Nginx Configuration Hardening:** Corrected syntax errors in the `allow` directives and optimized the `server_name` matching to support internal Docker DNS resolution (the usage of `localhost` is not supported in Nginx).
* **Scale-Out Architecture:** Verified and stress-tested the 3-replica load-balancing setup via automated shell-scripts.

## 🧠 Key DevOps Concepts Applied
* **Reverse Proxying:** Nginx hides the API from the world for security.
* **Load Balancing:** (Round Robin: Traffic is distributed across 3 API replicas/containers to prevent crashes. If one container is busy, Nginx moves to the next.
* **Rate Limiting:** Protects against DDoS attacks by capping requests at 10/sec.
* **Observability / Pull-Based Monitoring:** Using a **Pull-based** monitoring system (Prometheus) to track "System Health." Prometheus "pulls" data from the sidecar exporter. This is safer than the API "pushing" data, as it won't crash the API if the monitoring server goes down.
* **Network Masking:** Using `/12` subnetting in Nginx (`allow 172.16.0.0/12`) as "City-Wide"-mask to ensure the config is portable across different Docker environments where subnets might change.  
* **Health Endpoint:** The API includes a /health endpoint used by DevOps tools to verify the application is operational before sending traffic.

---

## 🎯 1. Project Purpose & Success Metrics
This project is a **Golden Reference** for moving ML models from a laptop to a production-ready state. It doesn't just "serve" a model; it "defends" and "monitors" it.

### Key Features:
A production-ready blueprint for deploying ML models. This project demonstrates:

1.  **High Availability:** 3 parallel API replicas ensure no single point of failure.
2.  **Hardened Security:** SSL/TLS encryption, Basic Authentication, and a 10 req/sec Rate Limiter.
3.  **Advanced Networking:** Utilizes `/12` CIDR masking to ensure the configuration is portable across any Docker subnet.
4.  **Full Observability:** Real-time health tracking with a dedicated monitoring "backdoor" to avoid SSL handshake loops.


## 🎯 Project Purpose
A production-ready blueprint for deploying ML models. This project demonstrates:
1. **Scalability:** 3 replicas of a FastAPI service behind a Load Balancer.
2. **Security:** SSL/TLS encryption, Basic Auth, and Rate Limiting.
3. **Observability:** Metric scraping via Prometheus and visualization via Grafana.



---

## 🏗️ 2. System Architecture
How the data and metrics flow through your system:

## 🏗 System Architecture

### Components
* **FastAPI (mlops-iris-api):** The "Engine." Predicts Iris species from input data.
* **Nginx (nginx_revproxy):** The "Gatekeeper." Handles HTTPS, Auth, and routes traffic.
* **Nginx Exporter:** The "Translator." Converts Nginx status into Prometheus format.
* **Prometheus:** The "Historian." Scrapes and stores metrics over time.
* **Grafana:** The "Dashboard." Visualizes metrics for human monitoring.

### Visual


```text
          [ USER REQUEST ]
                  |
        ( Port 443 / HTTPS )
                  |
      +-----------V-----------+       +-----------------------+
      |      🛡️ NGINX        | <---- |  📊 NGINX EXPORTER    |
      |   (The Gatekeeper)    |       |  (Internal Scraper)   |
      +-----------+-----------+       +-----------^-----------+
                  |                               |
      +-----------+-----------+       +-----------+-----------+
      |   📦 DOCKER NETWORK   |       |   🔥 PROMETHEUS      |
      | (172.16.0.0/12 Mask)  |       |   (The Historian)     |
      +-----------+-----------+       +-----------+-----------+
                  |                               |
      +-----------+-----------+       +-----------V-----------+
      |   🌸 IRIS API        |       |    🎨 GRAFANA         |
      | (3 x Load Balanced)   |       |   (The Dashboard)     |
      +-----------------------+       +-----------------------+
```

## 📁 3. Project Structure & Role Definitions


### Key Components

| Component | Tech | Role/Prupose |
| :--- | :---: | :--- |
| **Orchestrator** | 🐋 | Manages the entire service lifecycle, networking, and internal DNS naming so services can find each other by name. |
| **Reverse Proxy** | 🛡️ | Offloads heavy security tasks like SSL termination and Basic Auth, allowing the Python API to stay "light" and performant. |
| **Rate Limiter** | 🛡️ | Acts as a digital bouncer, preventing DDoS attacks or accidental spam by capping requests at 10/second per IP. |
| **Time-Series DB** | 🔥 | Collects and stores system "Health" metrics (Prometheus) in the background without slowing down the user's API response time. |



### Project Structure 

```bash
.
├── deployments/
│   ├── nginx/
│   │   ├── certs/          # 🔒 SSL/TLS Keys & CretsCerts (Generate locally; ignore in Git)
│   │   ├── .htpasswd       # 🔑 ncrypted credentials for Basic Auth
│   │   ├── Dockerfile      # 🐋 Builds Nginx image with custom configs
│   │   └── nginx.conf      # 🧠 The brain of the security and traffic routing (Routing logic, Rate Limiting, & Load Balancing)
│   └── prometheus/
│       └── prometheus.yml  # 🔥 Monitoring targets and scrape intervals
├── models/
│   └── model.joblib        # 🌸 The trained + serialized Scikit-learn model
├── src/
│   └── api/
│       ├── Dockerfile      # 🐋 Python/FastAPI environment
│       ├── main.py         # 🐍 The Python application logic (Fast API Endpoints (/predict + /health) + Model Inference logic)
│       └── requirements.txt # 📋 Python library dependencies
├── .dockerignore           # 🚫 Prevents local junk or security sesitive details from entering images
├── docker-compose.yml      # 🐋 The Orchestrator wiring all 5 services together 
├── Makefile                # 📜 Shortcut commands for dev/ops lifecycle
└── request.json            # 🧪 Example JSON payload template for API testing
```

### Key Files 

| File | Tech Logo | Purpose & "Why" |
| :--- | :---: | :--- |
| `docker-compose.yml` | 🐋 | **The Orchestrator:** Defines services, internal networks, and scaling (3x API replicas). |
| `nginx.conf` | 🛡️ | **The Gatekeeper:** Handles SSL termination, Load Balancing (Round Robin), and Rate Limiting. |
| `main.py` | 🐍 | **The Brain:** FastAPI application that loads the `.joblib` model and serves predictions. |
| `prometheus.yml` | 🔥 | **The Config:** Instructs Prometheus to scrape the Nginx Exporter every 3 seconds. |
| `Makefile` | 📜 | **The Remote:** Short-hand commands to build, start, and stop the entire complex stack. |
| `.htpasswd` | 🔑 | **The Vault:** Stores encrypted credentials for Basic Authentication. |
| `nginx.crt/key` | 🔒 | **The ID:** SSL/TLS certificates for encrypted HTTPS communication. |

### 🏛️ Component Logic & Service Roles

| Component | Technical Role | Role / Purpose |
| :--- | :--- | :--- |
| **Nginx** | Reverse Proxy | Offloads SSL termination and Authentication tasks so the Python API remains lightweight and focused on inference. |
| **Upstream** | Load Balancer | Distributes incoming traffic across 3 replicas to ensure high availability and prevent system-wide crashes if one instance fails. |
| **Exporter** | Sidecar | Acts as a metrics translator; it scrapes the raw Nginx status and formats it for Prometheus without needing to modify the Nginx source code. |
| **Subnet Mask** | CIDR `/12` | Defines a broad "trust zone" (172.16.0.0 to 172.31.255.255) ensuring Nginx allows monitoring traffic even if Docker dynamically changes the subnet IPs. |

## 🚀 4. Quick Start: Spinning up the Fortress

### Step 1: Security Setup - Generate Certs

These files are excluded from Git for security. You must generate them locally.

```bash
# Generate SSL Certificate
mkdir -p deployments/nginx/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout deployments/nginx/certs/nginx.key \
  -out deployments/nginx/certs/nginx.crt \
  -subj "/CN=localhost"

# Create Basic Auth to ptotect the api
# - Credentials (f.i.): User: admin | Pass: admin
# - Requires 'apache2-utils' installed
htpasswd -bc deployments/nginx/.htpasswd admin admin
```

### Step 2: Orchestration

```bash
# Launch the stack: Clean build and start all 5 services in detached mode
# (see Makefile for command details)
make start-project

# View the dashboard links
make links
```

## 🧪 5. Verification & Testing

### Verify Metrics "Heartbeat"
Check if Nginx is talking to the Exporter correctly:

- Browse to: `http://localhost:9113/metrics`
- Search for: `nginx_up 1`

### Successful Prediction Request (Verifying API, HTTPS + Auth):

```bash
curl -X POST "https://localhost/predict" \
    -H "Content-Type: application/json" \
    -d '{"petal_length":6.5, "petal_width":0.8}' \
    --user admin:admin \
    --`cacert ./deployments/nginx/certs/nginx.crt
```

### Flood Test / 503 Protection: Triggering the Security Rate-Limit  

Run this to see Nginx block traffic with 503 Service Unavailable after the "burst" limit is hit:

```bash
# Flood the API with 20 rapid-fire requests to trigger 503 errors
for i in {1..20}; do 
    curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST "https://localhost/predict" \
    -H "Content-Type: application/json" \
    -d '{"petal_length":6.5, "petal_width":0.8}' \
    --user "admin:admin" \
    --cacert ./deployments/nginx/certs/nginx.crt; 
done
```

### Internal Health Check (Verifying internal connectivity)

```bash
docker exec nginx_revproxy curl -s http://mlops-iris-api:8000/health
```

## 📊 6. Monitoring Dashboards

### Prometheus: 

http://localhost:9090 (Verify nginx_up 1 here)

### Grafana:

http://localhost:3000 (User: admin | Pass: admin)

> **Import Dashboard ID: 12708:** Use the Dashboard ID: 12708 to import the Nginx performance template.

---


## ⚖️ Credits & Provenance
* **Model Logic:** The Scikit-Learn Iris model and base API structure were provided by [Original Author/Bootcamp Name].
* **Infrastructure & Security:** All Nginx configurations, Docker orchestration fixes, SSL/Auth implementations, and the Prometheus/Grafana monitoring stack were architected and debugged by me to create a production-ready environment.
