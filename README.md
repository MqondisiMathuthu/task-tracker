# Task Tracker — End-to-End DevOps Project

A simple Flask + Redis task API used as a vehicle to build a complete,
production-style DevOps pipeline from scratch — containerization, CI/CD,
infrastructure as code, Kubernetes orchestration, and monitoring.

## Architecture

```
git push ──> GitHub Actions ──> tests (pytest)
                 │
                 └─ on pass ──> Docker build ──> GHCR (ghcr.io image registry)
                                                    │
                                   ./deploy.sh ─────┘
                                        │
                                        ▼
        Kubernetes (Minikube) ── Deployment: web ×2 (gunicorn + Flask)
                                 Deployment: redis
                                 Services, readiness probes, resource limits
                                        │
                        Prometheus (ServiceMonitor scrape /metrics)
                                        │
                                     Grafana dashboards
```

## Stack

| Concern            | Tool                                   |
|--------------------|----------------------------------------|
| App                | Python / Flask / gunicorn              |
| Data store         | Redis                                  |
| Containers         | Docker, docker-compose                 |
| CI/CD              | GitHub Actions → GHCR                  |
| IaC                | Terraform (Docker provider)            |
| Orchestration      | Kubernetes (Minikube), kubectl, Helm   |
| Monitoring         | kube-prometheus-stack (Prometheus + Grafana) |

## Highlights

- **CI gate:** every push runs pytest; images are built and pushed to GHCR
  only when tests pass (pipeline caught a real breaking change during development).
- **Zero-downtime deploys:** rolling updates gated by a readiness probe on `/health`.
- **Self-healing & scaling:** Deployment maintains replica count; scaled 2→5→2 live.
- **Observability:** app exposes Prometheus metrics; a ServiceMonitor adds it
  to the scrape pool; request rate and latency visible in Grafana.
- **Right-sized resources:** CPU/memory requests and limits set from measured
  usage in Grafana, not guesses.

## Run it locally

```bash
# with docker compose
docker compose up -d --build
curl localhost:5000/health

# on a cluster
minikube start --driver=docker
kubectl apply -f k8s/
./deploy.sh
```

## Repo layout

```
app.py            Flask API (tasks stored in Redis, /metrics exposed)
test_app.py       pytest suite (CI gate)
Dockerfile        gunicorn-based production image
docker-compose.yml  local two-container dev stack
.github/workflows/ci.yml  test → build → push pipeline
terraform/        IaC for the Docker-based stack
k8s/              Deployments, Services, ServiceMonitor
deploy.sh         apply manifests + rolling restart
```
