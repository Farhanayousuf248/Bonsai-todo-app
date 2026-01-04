# Todo App Phase IV: Local Kubernetes Deployment - Constitution

**Project**: Todo App - Phase IV Kubernetes Deployment
**Maintainer**: Farhana Yousuf (GIAIC)
**Version**: 4.0.0
**Ratified**: 2026-01-02
**Last Amended**: 2026-01-02
**Status**: Constitutional Framework Active

---

## Executive Summary

Phase IV represents a transformational shift from a Python CLI application to a **cloud-native, containerized microservice** deployed on local Kubernetes infrastructure. This phase bridges traditional software development and modern DevOps/AIOps practices while maintaining the disciplined engineering standards established in Phases I-III.

**Transition Statement**: Phase IV evolves the Todo App from an in-memory CLI tool to a **containerized service** with persistent storage, orchestrated by Kubernetes, managed by Helm, and prepared for AIOps observability integration.

---

## Core Principles

### I. Cloud-Native Architecture (NON-NEGOTIABLE)

**Principle**: The Todo App MUST transition to a containerized, stateless microservice architecture following the [Twelve-Factor App](https://12factor.net/) methodology.

**Requirements**:
- **Containerization**: Application MUST run in Docker containers with reproducible builds
- **Statelessness**: Application logic MUST be stateless; state stored externally (persistent volumes, databases)
- **Configuration as Environment Variables**: All configuration MUST be externalized (ports, database URIs, feature flags)
- **Process Isolation**: Each service component MUST run as an independent, replaceable process
- **Port Binding**: Services MUST expose functionality via port binding (HTTP/REST API)
- **Disposability**: Containers MUST start/stop quickly (<10 seconds) with graceful shutdown
- **Dev/Prod Parity**: Development (Minikube) and production environments MUST be as similar as possible

**Rationale**: Cloud-native design ensures the application can scale horizontally, recover from failures automatically, and integrate with modern orchestration platforms like Kubernetes.

---

### II. Containerization Standards (Docker)

**Principle**: All application components MUST be containerized using Docker with multi-stage builds, minimal base images, and security best practices.

**Requirements**:
- **Base Image**: Use official Python slim images (`python:3.11-slim` or `python:3.11-alpine`)
- **Multi-Stage Builds**: Separate build and runtime stages to minimize image size
- **Layer Optimization**: Order Dockerfile instructions from least to most frequently changing
- **Non-Root User**: Containers MUST run as non-root user (UID/GID > 1000)
- **Health Checks**: Implement `HEALTHCHECK` directives in Dockerfiles
- **Secrets Management**: No secrets, credentials, or API keys in images or environment variables (use Kubernetes Secrets)
- **Image Tagging**: Use semantic versioning tags (e.g., `v4.0.0`, `v4.0.0-rc1`) and `latest` tag
- **Image Size**: Production images SHOULD be <200MB where possible
- **Vulnerability Scanning**: Images MUST be scanned with `docker scout` or `trivy` before deployment

**Dockerfile Structure**:
```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
RUN useradd -m -u 1001 todouser
USER todouser
ENV PATH=/root/.local/bin:$PATH
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "-m", "src.main"]
```

**Rationale**: Docker containers provide reproducible, portable environments. Security and optimization best practices prevent vulnerabilities and reduce attack surface.

---

### III. Local Kubernetes Deployment (Minikube)

**Principle**: The Todo App MUST deploy successfully on local Kubernetes clusters using Minikube for development, testing, and educational purposes.

**Requirements**:
- **Minikube Compatibility**: Application MUST run on Minikube v1.30+ with Docker driver
- **Namespace Isolation**: Deploy all resources in a dedicated namespace (e.g., `todo-app`)
- **Resource Limits**: Define CPU/memory requests and limits for all pods
  - Requests: `cpu: 100m, memory: 128Mi`
  - Limits: `cpu: 500m, memory: 512Mi`
- **Liveness/Readiness Probes**: All pods MUST define both probes
  - Liveness: HTTP GET `/health` (initialDelaySeconds: 10, periodSeconds: 10)
  - Readiness: HTTP GET `/ready` (initialDelaySeconds: 5, periodSeconds: 5)
- **Service Types**: Use `ClusterIP` for internal services, `NodePort` or `LoadBalancer` for external access
- **Persistent Storage**: Use `PersistentVolumeClaim` (PVC) with `hostPath` or `local` storage class for data persistence
- **ConfigMaps/Secrets**: Store configuration in ConfigMaps, sensitive data in Secrets
- **Rolling Updates**: Deployments MUST use `RollingUpdate` strategy with `maxUnavailable: 1, maxSurge: 1`
- **Label Standards**: All resources MUST have consistent labels:
  - `app.kubernetes.io/name: todo-app`
  - `app.kubernetes.io/version: <version>`
  - `app.kubernetes.io/component: <backend|frontend|database>`
  - `app.kubernetes.io/managed-by: helm`

**Minikube Setup Checklist**:
```bash
# Start Minikube with resource allocation
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Verify cluster health
kubectl cluster-info
kubectl get nodes
```

**Rationale**: Minikube provides a local Kubernetes environment for development without cloud costs. Proper resource management and health checks ensure production-like behavior.

---

### IV. Helm Chart Orchestration

**Principle**: All Kubernetes resources MUST be managed through Helm charts (v3.10+) to enable parameterized deployments, versioning, and repeatable infrastructure-as-code.

**Requirements**:
- **Helm Version**: Use Helm v3.10 or higher (no Tiller, cluster-side component)
- **Chart Structure**: Follow standard Helm chart directory layout:
  ```
  todo-app-chart/
  ├── Chart.yaml          # Metadata (name, version, appVersion)
  ├── values.yaml         # Default configuration values
  ├── values-dev.yaml     # Development overrides
  ├── values-prod.yaml    # Production overrides
  ├── templates/
  │   ├── deployment.yaml
  │   ├── service.yaml
  │   ├── ingress.yaml
  │   ├── configmap.yaml
  │   ├── secret.yaml
  │   ├── pvc.yaml
  │   ├── hpa.yaml        # HorizontalPodAutoscaler (optional)
  │   ├── _helpers.tpl    # Template helpers
  │   └── NOTES.txt       # Post-install instructions
  ├── .helmignore
  └── README.md
  ```
- **Semantic Versioning**: `Chart.yaml` MUST follow semver (e.g., `version: 4.0.0`)
- **Parameterization**: All hardcoded values MUST be extracted to `values.yaml` (image tags, replicas, resources, etc.)
- **Template Functions**: Use Helm built-in functions (`include`, `toYaml`, `quote`, `default`)
- **Dependency Management**: External dependencies (e.g., PostgreSQL, Redis) MUST be declared in `Chart.yaml` dependencies
- **Hooks**: Use Helm hooks for pre-install/post-install tasks (e.g., database migrations)
- **Testing**: Include `templates/tests/` directory with test pods for smoke tests

**Helm Commands**:
```bash
# Lint chart
helm lint ./todo-app-chart

# Dry run with debug
helm install todo-app ./todo-app-chart --dry-run --debug

# Install chart
helm install todo-app ./todo-app-chart -n todo-app --create-namespace

# Upgrade release
helm upgrade todo-app ./todo-app-chart -n todo-app --values values-dev.yaml

# Rollback release
helm rollback todo-app 1 -n todo-app

# Uninstall release
helm uninstall todo-app -n todo-app
```

**Rationale**: Helm provides templating, versioning, and rollback capabilities. Infrastructure-as-code ensures reproducible deployments and simplifies environment management.

---

### V. Persistent Storage Strategy

**Principle**: The Todo App MUST transition from in-memory storage to persistent storage using Kubernetes PersistentVolumes (PV) and PersistentVolumeClaims (PVC).

**Requirements**:
- **Phase IV Constraint Relaxation**: The "in-memory only" constitutional constraint from Phases I-III is **LIFTED** for Phase IV
- **Storage Backend Options** (choose one based on requirements):
  1. **File-Based Persistence**: JSON file storage on PersistentVolume
  2. **SQLite**: Lightweight embedded database on PersistentVolume
  3. **PostgreSQL**: Full relational database deployed as StatefulSet or external service
- **PersistentVolumeClaim Specification**:
  - Access Mode: `ReadWriteOnce` (RWO)
  - Storage Class: `standard` (Minikube default) or `local-path`
  - Storage Size: Minimum 1Gi, recommended 5Gi
- **Data Migration**: Provide utility script to migrate Phase III in-memory data to persistent storage
- **Backup/Restore**: Document backup strategy using `kubectl cp` or volume snapshots
- **Data Encryption**: Sensitive data SHOULD be encrypted at rest (future consideration)

**Example PVC**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: todo-app-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

**Rationale**: Persistent storage is mandatory for production deployments. Kubernetes PVs/PVCs abstract storage provisioning and enable data durability across pod restarts.

---

### VI. API-First Design & Service Exposure

**Principle**: The Todo App MUST expose a RESTful API (HTTP/JSON) instead of relying solely on CLI interaction, enabling programmatic access and future integrations.

**Requirements**:
- **API Framework**: Use lightweight Python framework:
  - **Option 1**: `Flask` (minimal, beginner-friendly)
  - **Option 2**: `FastAPI` (modern, async, auto-generated OpenAPI docs)
- **API Endpoints**: Implement CRUD operations as REST endpoints:
  - `POST /tasks` - Create task
  - `GET /tasks` - List all tasks
  - `GET /tasks/{id}` - Get task by ID
  - `PUT /tasks/{id}` - Update task
  - `DELETE /tasks/{id}` - Delete task
  - `GET /health` - Health check (for probes)
  - `GET /ready` - Readiness check
- **API Versioning**: Use URL versioning (e.g., `/api/v1/tasks`)
- **Input Validation**: Validate all input using Pydantic models (FastAPI) or request schemas (Flask)
- **Error Handling**: Return standard HTTP status codes (200, 201, 400, 404, 500) with JSON error messages
- **OpenAPI Documentation**: Auto-generate API documentation (FastAPI provides `/docs` endpoint)
- **CLI Backward Compatibility**: Maintain CLI interface as a client that calls the REST API (optional)

**Example FastAPI Implementation**:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    description: str
    priority: str = "medium"
    category: str = "other"

@app.post("/api/v1/tasks")
def create_task(task: Task):
    # Business logic here
    return {"id": 1, "description": task.description}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**Rationale**: RESTful APIs enable programmatic access, testing automation, and future integrations (web UI, mobile apps, CI/CD pipelines). Health endpoints support Kubernetes probes.

---

### VII. AIOps Observability Standards

**Principle**: The Todo App MUST implement comprehensive observability (logging, metrics, tracing) following AIOps best practices to enable automated monitoring, alerting, and anomaly detection.

**Requirements**:

#### 7.1 Structured Logging
- **Logging Library**: Use Python `structlog` or `python-json-logger` for structured JSON logs
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Format**: JSON with mandatory fields:
  - `timestamp` (ISO 8601)
  - `level` (log level)
  - `service` (application name)
  - `version` (app version)
  - `message` (log message)
  - `trace_id` (distributed tracing ID)
  - `request_id` (per-request ID)
- **Log Aggregation**: Logs MUST be written to stdout/stderr (captured by Kubernetes)
- **Future Integration**: Logs SHOULD be compatible with ELK stack (Elasticsearch, Logstash, Kibana) or Loki

#### 7.2 Prometheus Metrics
- **Metrics Exporter**: Expose `/metrics` endpoint in Prometheus format
- **Required Metrics**:
  - **Application Metrics**:
    - `todo_tasks_total{status="active|completed"}` (Gauge)
    - `todo_api_requests_total{method,endpoint,status}` (Counter)
    - `todo_api_request_duration_seconds{method,endpoint}` (Histogram)
  - **System Metrics**:
    - `process_cpu_seconds_total` (Counter)
    - `process_memory_bytes` (Gauge)
    - `process_uptime_seconds` (Gauge)
- **Metrics Library**: Use `prometheus-client` Python library
- **Prometheus Integration**: Document Prometheus scrape configuration

#### 7.3 Distributed Tracing (Optional)
- **Tracing Standard**: OpenTelemetry (OTLP)
- **Trace Propagation**: W3C Trace Context (traceparent header)
- **Backend**: Jaeger or Zipkin (future integration)

#### 7.4 Health Monitoring
- **Health Endpoint**: `/health` returns JSON with component status:
  ```json
  {
    "status": "healthy",
    "version": "4.0.0",
    "components": {
      "database": "healthy",
      "storage": "healthy"
    }
  }
  ```
- **Readiness Endpoint**: `/ready` performs dependency checks (database connectivity, etc.)

#### 7.5 Alerting Rules (Future)
- Define Prometheus alerting rules for:
  - High error rate (>5% of requests return 5xx)
  - High latency (p95 > 500ms)
  - Pod restarts (>3 restarts in 15 minutes)
  - Low disk space (<10% available)

**Rationale**: Observability is critical for production readiness. Structured logs, metrics, and tracing enable proactive monitoring, incident response, and AIOps-driven automation.

---

### VIII. Testing & Quality Assurance

**Principle**: Phase IV MUST maintain the 100% test pass rate from Phase III while adding containerization and Kubernetes-specific tests.

**Requirements**:

#### 8.1 Unit Tests
- **Coverage**: Maintain 100% test coverage for business logic
- **Framework**: Continue using `unittest` or migrate to `pytest`
- **Mocking**: Mock external dependencies (database, filesystem, API calls)

#### 8.2 Integration Tests
- **API Testing**: Test all REST endpoints with `requests` library or `httpx`
- **Database Testing**: Test persistence layer with test database
- **Contract Testing**: Verify API contract compliance (request/response schemas)

#### 8.3 Container Tests
- **Image Build**: Verify Dockerfile builds successfully
- **Image Scanning**: Scan images for vulnerabilities (`trivy scan <image>`)
- **Container Startup**: Verify container starts and health checks pass
- **Resource Limits**: Test behavior under CPU/memory limits

#### 8.4 Kubernetes Tests
- **Helm Lint**: `helm lint ./todo-app-chart` must pass with 0 errors
- **Helm Template**: `helm template` must generate valid YAML
- **Dry Run**: `helm install --dry-run` must succeed
- **Deployment Test**: Deploy to Minikube and verify:
  - All pods reach `Running` state
  - Health/readiness probes pass
  - Service endpoints are accessible
  - PVC is bound and data persists across pod restarts
- **Helm Test**: Execute `helm test` with test pods

#### 8.5 Smoke Tests
- **Post-Deployment**: Automated smoke test suite:
  - Create task via API
  - Retrieve task via API
  - Update task via API
  - Delete task via API
  - Verify data persistence after pod restart

**Test Automation**:
```bash
# Run all tests before release
./scripts/test-phase4.sh
  ├── Unit tests (pytest)
  ├── API integration tests
  ├── Docker build & scan
  ├── Helm lint & template validation
  ├── Minikube deployment test
  └── Smoke tests
```

**Rationale**: Comprehensive testing ensures Phase IV changes don't introduce regressions. Kubernetes-specific tests validate deployment correctness.

---

### IX. Documentation Standards

**Principle**: Phase IV MUST provide comprehensive documentation for developers, operators, and end-users covering setup, deployment, and troubleshooting.

**Required Documentation**:

#### 9.1 README.md Updates
- Add Phase IV overview section
- Update architecture diagram (CLI → API + Kubernetes)
- Document new dependencies (Docker, Minikube, Helm, kubectl)
- Update quick start instructions

#### 9.2 Deployment Guide (DEPLOYMENT_PHASE4.md)
- **Prerequisites**: Required tools and versions
- **Minikube Setup**: Step-by-step installation and configuration
- **Docker Build**: How to build and tag images
- **Helm Installation**: How to install/upgrade releases
- **Configuration**: How to customize `values.yaml`
- **Troubleshooting**: Common issues and solutions

#### 9.3 API Documentation (API_REFERENCE_PHASE4.md)
- OpenAPI/Swagger specification
- Endpoint descriptions with request/response examples
- Authentication/authorization (if implemented)
- Error codes and messages

#### 9.4 Operations Runbook (OPERATIONS_PHASE4.md)
- Monitoring setup (Prometheus, Grafana)
- Log access and analysis
- Backup and restore procedures
- Scaling guidelines (HPA configuration)
- Disaster recovery procedures

#### 9.5 Architecture Decision Records (ADRs)
- Document key decisions:
  - ADR-001: Why FastAPI over Flask
  - ADR-002: Why PostgreSQL over SQLite
  - ADR-003: Storage strategy selection
  - ADR-004: Observability stack choices

#### 9.6 Migration Guide (MIGRATION_PHASE3_TO_PHASE4.md)
- Breaking changes from Phase III
- Data migration scripts
- CLI to API transition guide
- Rollback procedures

**Rationale**: Comprehensive documentation reduces onboarding time, prevents misconfigurations, and serves as a knowledge base for troubleshooting.

---

### X. Security Best Practices

**Principle**: Phase IV MUST implement security best practices for containerized applications and Kubernetes deployments.

**Requirements**:

#### 10.1 Container Security
- **Non-Root User**: Containers MUST run as non-root (enforced by securityContext)
- **Read-Only Filesystem**: Root filesystem SHOULD be read-only where possible
- **No Privileged Containers**: `privileged: false` in securityContext
- **Drop Capabilities**: Drop unnecessary Linux capabilities
- **Image Scanning**: Scan images for vulnerabilities before deployment
- **Private Registry**: Use private container registry for production (future)

#### 10.2 Kubernetes Security
- **RBAC**: Define ServiceAccount, Role, and RoleBinding with least privilege
- **Network Policies**: Implement NetworkPolicy to restrict pod-to-pod traffic (future)
- **Pod Security Standards**: Enforce `restricted` pod security standard
- **Secrets Management**: Store sensitive data in Kubernetes Secrets (base64 encoded)
  - Future: Integrate with external secret managers (HashiCorp Vault, AWS Secrets Manager)
- **Resource Quotas**: Define ResourceQuota to prevent resource exhaustion

#### 10.3 API Security
- **Input Validation**: Validate all user input to prevent injection attacks
- **Rate Limiting**: Implement rate limiting to prevent abuse (future)
- **Authentication**: Implement API key or JWT authentication (future Phase V consideration)
- **HTTPS/TLS**: Use TLS for all external communication (Ingress with cert-manager)

#### 10.4 Secrets Management Example
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
type: Opaque
data:
  database-password: <base64-encoded>
  api-key: <base64-encoded>
```

**Rationale**: Security is non-negotiable in production environments. Implementing security best practices from the start prevents vulnerabilities and compliance issues.

---

### XI. CI/CD Integration Preparation

**Principle**: Phase IV MUST prepare the application for automated CI/CD pipelines in future phases (GitHub Actions, GitLab CI, Jenkins).

**Requirements**:

#### 11.1 Repository Structure
- **Dockerfiles**: Store in `./docker/` directory
- **Helm Charts**: Store in `./helm/todo-app-chart/` directory
- **Kubernetes Manifests**: Store raw YAML in `./k8s/` (for reference)
- **Scripts**: Automation scripts in `./scripts/`
  - `build.sh` - Build Docker image
  - `push.sh` - Push to container registry
  - `deploy.sh` - Deploy to Kubernetes
  - `test.sh` - Run all tests

#### 11.2 Makefile
Provide `Makefile` with common commands:
```makefile
.PHONY: build test deploy clean

build:
	docker build -t todo-app:latest -f docker/Dockerfile .

test:
	pytest tests/
	helm lint ./helm/todo-app-chart

deploy:
	helm upgrade --install todo-app ./helm/todo-app-chart -n todo-app

clean:
	helm uninstall todo-app -n todo-app
	docker rmi todo-app:latest
```

#### 11.3 Version Management
- **Git Tags**: Tag releases with semantic versioning (e.g., `v4.0.0`)
- **Image Tags**: Docker images tagged with Git commit SHA and version
- **Helm Chart Version**: Synchronized with application version

#### 11.4 Pre-Commit Hooks (Optional)
- Lint Dockerfile (`hadolint`)
- Lint Helm charts (`helm lint`)
- Run unit tests
- Format code (Black, isort)

**Rationale**: Preparing for CI/CD enables automated testing and deployment. Standardized scripts and structure simplify pipeline integration.

---

## Phase Transition Rules

### XII. Constitutional Evolution from Phase III to Phase IV

**Breaking Changes**:
1. **Storage Architecture**: In-memory constraint LIFTED; persistent storage REQUIRED
2. **Interface**: CLI-first → API-first (CLI becomes optional client)
3. **Deployment**: Local Python process → Containerized Kubernetes deployment
4. **Dependencies**: No external packages → Docker, Kubernetes, Helm, Flask/FastAPI required

**Preserved Principles**:
1. **Spec-Driven Development**: Constitution → Specification → Plan → Execution → QA → Checklist
2. **100% Test Coverage**: All features MUST be tested
3. **Quality Standards**: 100/100 quality score target
4. **Documentation**: Comprehensive docs for all features

**Backward Compatibility**:
- Phase III functionality (27 features) MUST remain accessible via API
- Data migration tool MUST convert Phase III in-memory data to Phase IV persistent storage
- CLI interface MAY be preserved as API client wrapper

---

## Development Workflow

### XIII. Phase IV Implementation Workflow

**Step 1: Constitution (Current Document)**
- ✅ Define Phase IV principles and constraints

**Step 2: Specification (SPECIFICATION_PHASE4.md)**
- Detail functional requirements for:
  - REST API endpoints
  - Dockerization
  - Kubernetes resources
  - Helm chart structure
  - Observability implementation
  - Data migration

**Step 3: Planning (PLAN_PHASE4.md)**
- Break down implementation into sub-phases:
  - 4.1: API Development (Flask/FastAPI)
  - 4.2: Dockerization
  - 4.3: Kubernetes Resources
  - 4.4: Helm Chart Development
  - 4.5: Observability Integration
  - 4.6: Testing & Documentation

**Step 4: Execution (EXECUTION_LOG_PHASE4.md)**
- Implement features incrementally
- Test after each sub-phase
- Document progress and blockers

**Step 5: QA Validation (QA_VALIDATION_PHASE4.md)**
- Execute comprehensive test suite
- Validate acceptance criteria
- Performance testing
- Security scanning

**Step 6: Checklist Verification (CHECKLIST_PHASE4.md)**
- Verify constitutional compliance
- Validate documentation completeness
- Confirm deployment readiness

---

## Governance

### XIV. Amendment Process

**Constitutional Amendments**:
- Amendments require documented justification and impact analysis
- Version increments follow semantic versioning
- All stakeholders must review and approve major changes

**Compliance Verification**:
- All pull requests MUST verify Phase IV constitutional compliance
- Pre-deployment checklist MUST confirm adherence to all principles
- Quarterly reviews to assess constitutional effectiveness

**Exception Handling**:
- Exceptions to constitutional principles require:
  1. Written justification with technical rationale
  2. Approval from project maintainer
  3. Documentation in ADR (Architecture Decision Record)
  4. Sunset clause (timeline to resolve exception)

---

## Technology Stack

### XV. Approved Technologies

**Core Stack**:
- **Language**: Python 3.11+
- **API Framework**: FastAPI (recommended) or Flask
- **Container Runtime**: Docker 24.0+
- **Orchestration**: Kubernetes 1.28+ (via Minikube)
- **Package Manager**: Helm 3.10+

**Storage Options** (choose one):
- **Option 1**: JSON file storage (simplest, Phase III-like)
- **Option 2**: SQLite 3.40+ (embedded, no external service)
- **Option 3**: PostgreSQL 15+ (full-featured, deployed as StatefulSet)

**Observability Stack** (future integration):
- **Logging**: Structlog + ELK/Loki
- **Metrics**: Prometheus + Grafana
- **Tracing**: OpenTelemetry + Jaeger

**Development Tools**:
- **Containerization**: Docker, docker-compose
- **Kubernetes**: kubectl, minikube, k9s (optional)
- **Helm**: helm CLI
- **Testing**: pytest, requests/httpx, pytest-cov
- **Linting**: flake8, black, isort, mypy
- **Security**: trivy, hadolint

---

## Success Criteria

### XVI. Phase IV Completion Criteria

**Functional Requirements**:
- ✅ All 27 Phase III features accessible via REST API
- ✅ Dockerfile builds successfully with <200MB image size
- ✅ Application deploys to Minikube without errors
- ✅ Helm chart installs/upgrades/rollbacks correctly
- ✅ Data persists across pod restarts
- ✅ Health and readiness probes pass consistently
- ✅ API documentation auto-generated and accessible

**Quality Metrics**:
- ✅ 100% test pass rate (unit, integration, smoke tests)
- ✅ 0 critical/high vulnerabilities in container images
- ✅ Helm lint passes with 0 errors
- ✅ Constitutional compliance: 100%
- ✅ Documentation completeness: 100%

**Performance Targets**:
- ✅ API response time: p95 < 200ms, p99 < 500ms
- ✅ Container startup time: < 10 seconds
- ✅ Pod restart time: < 15 seconds
- ✅ Resource usage: < 100MB memory idle, < 200MB under load

**Operational Readiness**:
- ✅ Deployment guide tested and validated
- ✅ Troubleshooting runbook complete
- ✅ Monitoring dashboards configured
- ✅ Backup/restore procedures documented and tested
- ✅ Migration scripts tested with Phase III data

---

## Future Phases

### XVII. Phase V+ Roadmap (Informational)

**Phase V: Production Kubernetes Deployment**
- Deploy to managed Kubernetes (AWS EKS, GKE, AKS)
- Implement CI/CD pipelines (GitHub Actions, ArgoCD)
- Production-grade observability (ELK stack, Prometheus federation)
- Auto-scaling (HPA, Cluster Autoscaler)
- Multi-environment strategy (dev, staging, production)

**Phase VI: Advanced AIOps**
- Anomaly detection with ML models
- Predictive scaling based on historical patterns
- Automated incident response (self-healing)
- Chaos engineering (Chaos Mesh)

**Phase VII: Multi-Tenancy & SaaS**
- Multi-tenant architecture
- API authentication (OAuth 2.0, JWT)
- Web frontend (React/Vue.js)
- Mobile app integration

---

## Appendices

### Appendix A: Glossary

- **AIOps**: Artificial Intelligence for IT Operations - using ML/AI to automate monitoring, alerting, and remediation
- **Helm**: Kubernetes package manager for templated deployments
- **Minikube**: Local Kubernetes cluster for development
- **PVC**: PersistentVolumeClaim - Kubernetes abstraction for storage
- **StatefulSet**: Kubernetes workload for stateful applications
- **Twelve-Factor App**: Methodology for building SaaS applications

### Appendix B: Reference Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Kubernetes Cluster (Minikube)         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Namespace: todo-app                      │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  Deployment: todo-app (3 replicas)              │ │ │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │ │ │
│  │  │  │  Pod 1   │  │  Pod 2   │  │  Pod 3   │      │ │ │
│  │  │  │ (API)    │  │ (API)    │  │ (API)    │      │ │ │
│  │  │  └──────────┘  └──────────┘  └──────────┘      │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │                           │                           │ │
│  │  ┌────────────────────────▼────────────────────────┐ │ │
│  │  │  Service: todo-app-service (ClusterIP)         │ │ │
│  │  └────────────────────────┬────────────────────────┘ │ │
│  │                           │                           │ │
│  │  ┌────────────────────────▼────────────────────────┐ │ │
│  │  │  Ingress: todo-app-ingress                      │ │ │
│  │  │  (External Access: http://todo-app.local)       │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  PersistentVolumeClaim: todo-app-data           │ │ │
│  │  │  (5Gi, ReadWriteOnce)                           │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  ConfigMap: todo-app-config                     │ │ │
│  │  │  Secret: todo-app-secrets                       │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

                      Managed by Helm Chart
                          (version 4.0.0)
```

### Appendix C: Quick Reference Commands

```bash
# Docker Commands
docker build -t todo-app:v4.0.0 .
docker run -p 8080:8080 todo-app:v4.0.0
docker images | grep todo-app
trivy image todo-app:v4.0.0

# Minikube Commands
minikube start --cpus=4 --memory=8192
minikube dashboard
minikube service todo-app-service -n todo-app
minikube tunnel  # For LoadBalancer services

# Kubectl Commands
kubectl get all -n todo-app
kubectl describe pod <pod-name> -n todo-app
kubectl logs -f <pod-name> -n todo-app
kubectl port-forward svc/todo-app-service 8080:8080 -n todo-app
kubectl exec -it <pod-name> -n todo-app -- /bin/bash

# Helm Commands
helm lint ./helm/todo-app-chart
helm install todo-app ./helm/todo-app-chart -n todo-app --create-namespace
helm upgrade todo-app ./helm/todo-app-chart -n todo-app
helm rollback todo-app 1 -n todo-app
helm list -n todo-app
helm uninstall todo-app -n todo-app

# Testing Commands
pytest tests/ -v --cov=src
helm test todo-app -n todo-app
./scripts/test-phase4.sh
```

---

**Version**: 4.0.0
**Ratified**: 2026-01-02
**Last Amended**: 2026-01-02
**Status**: ✅ Active and Enforceable

---

**Maintainer Sign-Off**:
This constitution establishes the foundational principles for Todo App Phase IV: Local Kubernetes Deployment. All subsequent specifications, plans, and implementations MUST adhere to these principles unless formally amended through the governance process.

**Farhana Yousuf**
GIAIC Student & Project Maintainer
2026-01-02
