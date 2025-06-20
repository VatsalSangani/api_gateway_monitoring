# 🛡️ API Gateway with Rate Limiting, Monitoring & Admin Dashboard

A full-stack microservice setup built with FastAPI, Redis, Prometheus, Grafana, and Streamlit. It provides secure rate-limiting, service health monitoring, and restart capability via a UI dashboard.

---

## 📌 Features
- ✅ Reverse Proxy Gateway using FastAPI
- 🔐 Token-based Rate Limiting powered by Redis
- 🔁 Retry Mechanism with exponential backoff for microservices
- 📊 Monitoring via Prometheus + Grafana
- 🧪 Mock Microservice to simulate traffic
- 🧠 Streamlit Admin Dashboard to visualize usage + restart services
- 🐳 Dockerized microservices orchestrated via docker-compose

---

## 🛠️ Tech Stack & Tools
| Tool           | Purpose                                                  |
|----------------|-----------------------------------------------------------|
| **FastAPI**     | API Gateway with routing, retry, and admin endpoints     |
| **Redis**       | Store request token counters for rate limiting           |
| **httpx**       | Async request proxying with timeout + retries            |
| **Prometheus**  | Metrics scraping and instrumentation for FastAPI         |
| **Grafana**     | Visual dashboards for monitoring gateway metrics         |
| **Streamlit**   | Admin UI to monitor stats and trigger service restarts   |
| **Docker**      | Containerize and orchestrate all services                |
| **Docker Compose** | Manage multi-container setup easily                   |

---

## 📁 Project Structure

```
.
├── admin_dashboard/     # Streamlit-based admin GUI
├── gateway/             # FastAPI API Gateway
├── mock_service/        # Dummy microservice
├── prometheus/          # Prometheus config
├── grafana/             # (optional) Custom dashboards if added
├── docker-compose.yml   # Orchestration
└── README.md
```
---

## 📂 Services

| Service         | Port  | Description                                      |
|-----------------|-------|--------------------------------------------------|
| Gateway         | 8080  | FastAPI reverse proxy + rate limiting            |
| Mock Service    | 8001  | Dummy backend service for routing                |
| Redis           | 6379  | Token store for rate limiting                    |
| Prometheus      | 9090  | Metrics collection                               |
| Grafana         | 3000  | Monitoring dashboards (Login: `admin`/`admin`)   |
| Admin Dashboard | 8501  | Streamlit UI for restarts and insights           |

---

## 🚀 How to Run
### 1. Clone the project
```bash
git clone https://github.com/yourname/api_gateway_project.git
cd api_gateway_project
```
### 2. Start everything 🚀
```bash
docker-compose build
docker-compose up
```
---

## 🧪 How It Works
### 📦 API Gateway (/gateway)
- Routes traffic from /api/service1/<path> to mock_service.
- Enforces rate limiting using Redis tokens.
- Handles retry logic for 5xx failures.
- Exposes metrics at /metrics for Prometheus.

### 🎯 Rate Limiting
- Users send requests with Authorization: Bearer <token>.
- Redis key: ratelimit:<token> stores remaining quota.
- Hits 429 Too Many Requests if over limit.

### 🧪 Mock Service (/mock_service)
- Simple FastAPI service with a /users route returning JSON.

### 📊 Prometheus + Grafana
- Prometheus scrapes /metrics from the gateway every 5s
- Grafana dashboards visualize:
  - Request rate
  - Error count
  - Latency
  - Service Uptime

## 📋 Admin Dashboard (/admin_dashboard)
- Built in Streamlit
- Display Metrics like:
    - ✅ Total Requests
    - 🚫 Rate Limit Hits
    - ⚡ Avg Latency
- Also allows you to restart services via /admin/restart_service

## 📊 Grafana Login
- Visit: http://localhost:3000
- Username: admin
- Password: admin
- It may ask you change this Username and Password so set it accordingly.

## 🪪 License
MIT License — free to use, fork, and modify.

## 🙌 Credits
Made with ❤️ by [Vatsal Sangani].<br>
Powered by Python, Docker, and open-source magic 🪄

