# AEGIS Sprint 1 Implementation Guide

**Sprint:** 1 — Platform Foundation  
**Status:** Proposed execution guide  
**Scope:** Repository setup, local containers, FastAPI and React scaffolds, PostgreSQL/pgvector and Redis connectivity, logging, health endpoints, and CI foundation  
**Backlog basis:** AEGIS MVP Backlog items TS-001, TS-002, TS-003, TS-019, and initial TS-020  
**Out of scope:** Business features, Entra sign-in/token validation, conversation or knowledge schemas, agents, external integrations, approval execution, production deployment, and LangGraph

> **Implementation assumptions:** The workspace currently contains planning documents rather than an initialized code repository. This guide describes the target files and sequence; it does not claim that they already exist. The architecture ADRs do not mandate programming-language patch versions, package managers, database image tags, repository host, or CI vendor. The tool choices below are proposed defaults to validate against organizational standards, then pin in lockfiles and container image tags before implementation. Use supported versions at implementation time.

## 1 Sprint Outcome

At Sprint 1 exit, a developer should be able to clone the repository, follow the README on Windows with Docker Desktop, start the React app, FastAPI API, PostgreSQL with pgvector, and Redis, verify liveness/readiness and dependency connectivity, run local checks, and receive a passing CI run.

The foundation must follow the approved modular-monolith model:

- One FastAPI backend deployable; thin HTTP routes.
- Domain/application boundaries independent from framework and infrastructure.
- React + TypeScript frontend consuming a versioned API.
- PostgreSQL is the durable system of record. Sprint 1 only verifies connectivity and pgvector availability; it creates no business-domain schema.
- Redis is optional and ephemeral; it is not authoritative for conversations, approvals, or audit.
- No production credentials, model/provider secrets, or Entra client secrets in source, frontend bundles, images, or logs.

## 2 Exact Sprint 1 Folder and File Structure

Create only files needed for the foundation. The structure below is the intended Sprint 1 result; future feature directories are intentionally absent.

```text
AEGIS/
├── .editorconfig
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── README.md
├── compose.yaml
├── docs/
│   ├── decisions/
│   │   └── sprint-1-decisions.md
│   └── development/
│       └── local-setup.md
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── src/
│   │   └── aegis/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── config.py
│   │       ├── api/
│   │       │   ├── __init__.py
│   │       │   └── health.py
│   │       └── observability/
│   │           ├── __init__.py
│   │           ├── logging.py
│   │           └── correlation.py
│   └── tests/
│       ├── conftest.py
│       ├── test_health.py
│       └── test_config.py
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── eslint.config.js
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── index.css
│       └── vite-env.d.ts
└── .github/
    └── workflows/
        └── ci.yml
```

### Directory boundaries

- `backend/src/aegis/api/`: HTTP transport only; use cases and domain rules are not added in this sprint.
- `backend/src/aegis/config.py`: typed, validated settings. Local secrets come from an ignored `.env`; `.env.example` contains placeholders only.
- `backend/src/aegis/observability/`: request correlation and safe structured logging.
- `backend/tests/`: smoke/unit tests for app lifecycle, configuration validation, and health behavior.
- `frontend/src/`: minimal React shell and build entry point; no login, chat, or business feature.
- `docs/decisions/`: records open decisions and approved Sprint 1 choices; it does not silently settle architecture questions.
- `.github/workflows/ci.yml`: use only if GitHub is the approved repository host. For another host, create the equivalent pipeline there and omit `.github/`.
- No `migrations/` or domain tables are needed yet. Add Alembic and the first migration with Sprint 2 persistence work.
- No empty feature modules, agent code, approval module, or integration adapters are created in Sprint 1.

## 3 File Creation Order

Follow this order so each layer has a runnable predecessor. Keep each step as a small change that can be independently checked.

1. **Repository safety and conventions**
   - `.gitignore`
   - `.editorconfig`
   - `CONTRIBUTING.md`
   - `README.md`
   - `docs/decisions/sprint-1-decisions.md`
2. **Backend package/toolchain**
   - `backend/pyproject.toml`
   - `backend/src/aegis/__init__.py`
   - `backend/src/aegis/config.py`
   - `backend/src/aegis/main.py`
   - `backend/src/aegis/api/__init__.py`
   - `backend/src/aegis/api/health.py`
   - `backend/src/aegis/observability/__init__.py`
   - `backend/src/aegis/observability/logging.py`
   - `backend/src/aegis/observability/correlation.py`
   - `backend/tests/conftest.py`, `test_config.py`, `test_health.py`
   - Resolve and commit `backend/uv.lock`.
3. **Frontend package/toolchain**
   - Scaffold `frontend/` using React + TypeScript + Vite.
   - Verify `package.json`, TypeScript config, ESLint config, `index.html`, `src/main.tsx`, and `src/App.tsx`.
   - Resolve and commit `frontend/package-lock.json`.
4. **Safe local configuration and developer documentation**
   - `.env.example` with names and non-secret placeholders.
   - Ignore populated `.env` files; do not generate or commit local credentials.
   - `docs/development/local-setup.md` with prerequisites and commands.
5. **Containers**
   - `backend/Dockerfile`
   - `backend/.dockerignore`
   - `frontend/Dockerfile`
   - `frontend/.dockerignore`
   - `compose.yaml` with API, web, PostgreSQL/pgvector and Redis services, health checks, and a private application network.
6. **Integration and smoke verification**
   - Wire typed settings to PostgreSQL/Redis connection checks.
   - Ensure readiness checks required dependencies and liveness does not.
   - Verify pgvector extension availability using a local setup/smoke check, not by exposing database details in a public health response.
7. **CI foundation**
   - `.github/workflows/ci.yml` or the approved host equivalent.
   - Add Python checks, frontend checks/build, tests, Compose/Docker build validation, and secret/dependency scanning appropriate to available approved tooling.
8. **Clean-checkout rehearsal**
   - Follow README/local setup from a fresh checkout, then run compose startup, health checks, tests, CI-equivalent commands, and shutdown.
   - Record gaps and decisions; do not mark a check complete based only on an existing developer cache.

## 4 Dependencies to Install

Use the approved package managers and commit lockfiles. Pin exact versions through the lockfiles and use supported runtime versions selected by the organization. Do not install dependencies unrelated to the foundation.

### Prerequisites on the developer workstation

| Tool | Purpose | Sprint 1 requirement |
|---|---|---|
| Git | Source control | Approved repository access; configure author identity without storing credentials in the repository. |
| Docker Desktop with Compose plugin | Local service orchestration | Verify Docker daemon and `docker compose` are available. |
| Python | Backend runtime and tooling | Use an organization-approved supported Python release; select one version and document it. |
| `uv` | Python dependency and lockfile management | Recommended default for reproducible sync and lock; use another approved manager if policy requires it. |
| Node.js LTS and npm | React/TypeScript toolchain | Pin the supported major/runtime in project documentation and CI; use the committed npm lockfile. |
| Visual Studio Code | Editor | Install recommended extensions in Section 5. |

### Backend runtime dependencies

| Package | Purpose | Sprint 1 use |
|---|---|---|
| `fastapi` | HTTP application and OpenAPI | App scaffold and health routes. |
| `uvicorn[standard]` | ASGI development server | Local API service. |
| `pydantic-settings` | Typed environment configuration | Required setting validation and safe local configuration. |
| `psycopg[binary]` | PostgreSQL driver | Local connection/readiness smoke check. For production, select the deployment-approved driver packaging strategy. |
| `redis` | Redis Python client | Optional connectivity check; no business data. |

Use the Python standard library `logging` with a structured formatter or a reviewed structured-logging package. Prefer starting with one logging approach, not several overlapping frameworks. If adopting `structlog`, record the decision and configure redaction/correlation consistently.

### Backend development/test dependencies

| Package | Purpose |
|---|---|
| `pytest` | Unit and API tests. |
| `httpx` | FastAPI test client transport. |
| `ruff` | Python linting and formatting. |
| `mypy` or an approved type checker | Static type checking; select one and document strictness. |

### Frontend runtime and development dependencies

Use the Vite React TypeScript scaffold, then verify the exact package list and lockfile.

| Package family | Purpose |
|---|---|
| `react`, `react-dom` | Frontend runtime. |
| `typescript` | Static typing. |
| `vite` | Development server and production build. |
| `@types/react`, `@types/react-dom` | React type definitions. |
| `eslint` with TypeScript/React plugins | Frontend linting. |
| `prettier` (optional if ESLint formatting is selected) | Consistent formatting; avoid competing formatting authorities. |
| `vitest` and `@testing-library/react` (if included in the initial check baseline) | Frontend unit/component test foundation. |

### Add later, not for Sprint 1

- `SQLAlchemy`, `Alembic`, and `pgvector` application models: introduce when implementing durable domain schema and migrations in Sprint 2/4.
- Entra/MSAL dependencies: introduce with approved identity flow work in Sprint 2/3.
- AI provider SDKs, embedding clients, LangGraph, external-system SDKs, and tool libraries: not installed for the platform-only sprint.
- Production database/cache credentials and cloud deployment SDKs: not required for local foundations.

## 5 VS Code Extensions Recommended

Install extensions only from the official VS Code Marketplace and follow organizational extension policy. Recommended:

| Extension | Use |
|---|---|
| **Python** (Microsoft) | Python interpreter and project integration. |
| **Pylance** (Microsoft) | Python language server, diagnostics, and navigation. |
| **Ruff** (Astral Software) | Python linting/formatting integration. |
| **Docker** (Microsoft) | Inspect and manage local images, containers, and Compose. |
| **Dev Containers** (Microsoft, optional) | Reproducible editor container workflow if the team elects to use it; not required for Docker Compose. |
| **ESLint** (Microsoft) | Frontend lint diagnostics. |
| **Prettier - Code formatter** (Prettier, optional) | Use if Prettier is the selected frontend formatter. |
| **EditorConfig for VS Code** | Apply repository editor conventions. |
| **YAML** (Red Hat) | Compose and CI YAML validation. |
| **GitHub Actions** (GitHub, only if using GitHub) | Workflow syntax and diagnostics. |
| **PostgreSQL** (optional, approved publisher) | Convenient local SQL browsing; not required if Docker/CLI checks suffice. |

Commit a workspace recommendation file only after repository host and extension policy are confirmed. Extensions do not replace command-line/CI checks.

## 6 Docker Configuration Requirements

### Compose services

Define four local services:

1. **`api`** — FastAPI/uvicorn development container, source mounted for reload, listening on the Compose network.
2. **`web`** — React/Vite development container, source mounted for hot reload.
3. **`db`** — PostgreSQL image with the compatible pgvector extension already available.
4. **`redis`** — Redis service for ephemeral cache/coordination development only.

### Requirements

- Use explicit, supported image tags and update them through reviewed changes; do not use floating `latest` tags for reproducible development.
- Place services on an application network. Expose only ports needed by a developer on the local machine; do not bind database/cache ports to all network interfaces.
- Use health checks for PostgreSQL and Redis. Application startup must tolerate dependency startup ordering and readiness must check actual required connections.
- Use a named local PostgreSQL volume for persistence. Do not add a persistent Redis volume unless a separately approved coordination requirement needs it.
- Compose files and Dockerfiles must not contain credentials. Read local values from an ignored `.env`; `.env.example` uses placeholders.
- Never pass production secrets as Docker build arguments or bake them into image layers. Build-time arguments are not secret storage.
- Use a non-root runtime user where practical; avoid privileged containers and unnecessary capabilities.
- Keep build contexts narrow and exclude `.env`, `.git`, virtual environments, node modules, caches, and local data with `.dockerignore`.
- Add stop/graceful-shutdown behavior and a clear developer reset process. Document that removing a local database volume destroys local development data.
- Health endpoints must not expose connection strings, raw exception messages, database hostnames, token claims, or secrets.
- Redis loss must not lose authoritative records. The API's initial connection check is diagnostic; do not make Redis a prerequisite for all application correctness.
- Do not add production deployment, ingress, TLS termination, secrets manager, or cloud network configuration until the deployment target is approved.

### Local configuration names

The exact environment variable names should be centralized and validated in backend settings. A minimal local set may include:

- `AEGIS_ENVIRONMENT`
- `AEGIS_LOG_LEVEL`
- `AEGIS_API_PREFIX`
- `AEGIS_DATABASE_URL`
- `AEGIS_REDIS_URL`
- `AEGIS_CORS_ORIGINS` (development origins only)

No values for Entra, model providers, external integrations, or production endpoints are needed in Sprint 1. Do not add placeholder secret values that look usable.

## 7 Database Setup Requirements

### Sprint 1 scope

- Start PostgreSQL with the required pgvector extension available.
- Configure a local-only development database and a dedicated local application user; do not use the database superuser as the API identity.
- Verify API connectivity and basic query execution (`SELECT 1`) through the selected driver.
- Verify pgvector extension availability using an explicit setup/smoke check.
- Add a health/readiness integration that reports only component status, not connection details.
- Persist local development state in a named database volume and document how to intentionally reset it.
- Record database image/extension version and driver configuration for reproducibility.
- No business schema, user table, conversation table, knowledge chunks, approvals, audit tables, or production migration is part of this sprint.

### Database requirements for follow-on sprints

- Introduce Alembic and SQLAlchemy/migration conventions when the first application-domain schema is implemented.
- Keep PostgreSQL the system of record for conversations, runs, approvals, audit, and knowledge metadata.
- Use migrations, constraints, foreign keys, and least-privilege application roles; define backup/restore before production.
- Apply source visibility and authorization filters before knowledge content is returned to an agent.
- Do not store authoritative conversation, approval, or audit records only in Redis.

## 8 Logging and Health Endpoints

### Logging baseline

- Use structured logs with timestamp, severity, service, environment, event name, duration/outcome, and request correlation ID.
- Generate a correlation ID when absent; validate client-supplied values and return the effective ID in a response header.
- Log request completion and exceptions without logging request bodies by default.
- Never log authorization headers, cookies, tokens, passwords, database URLs, API keys, or full chat content.
- Return safe error responses to clients and keep internal diagnostics in protected logs.
- Use UTC timestamps and document how logs are captured in local Compose and CI.

### Health behavior

- **Liveness:** Confirms the process/event loop is functioning; does not fail merely because PostgreSQL or Redis is unavailable.
- **Readiness:** Confirms required dependencies are reachable for the capability being served. It can report `database: unavailable` or `redis: unavailable` as status labels but must not return hostnames, credentials, or raw exceptions.
- Treat PostgreSQL as required for durable features. Treat Redis as optional unless a specific documented coordination feature is being exercised.
- Add tests for healthy dependencies, unavailable database, unavailable Redis, and safe response shape.
- Health endpoints are operational signals, not authorization or security controls.

## 9 CI/CD Foundation

Repository host is not specified in the ADRs. If GitHub is approved, use GitHub Actions and `.github/workflows/ci.yml`; otherwise implement the equivalent required checks in the approved CI platform.

### Pull request pipeline

Run on every pull request and the protected main branch:

1. **Repository checks:** whitespace/diff check and secret scanning.
2. **Backend:** install from lockfile; Ruff lint/format check; static type check; pytest unit/API tests.
3. **Frontend:** `npm ci`; ESLint; TypeScript check; production build; frontend tests if configured.
4. **Container:** build API and web images without injecting secrets. Compose validation/build where runner support allows.
5. **Dependency security:** scan Python and npm dependency lockfiles using the approved scanner; report findings and block according to organizational severity policy.
6. **Artifacts:** retain test and scan reports with access controls; never upload `.env`, tokens, production data, or sensitive test fixtures.

### Security and operational guardrails

- CI uses short-lived or narrowly scoped credentials; no production credential is required for Sprint 1 checks.
- Main branch merge requires passing tests, lint, type checks, and secret scanning.
- Container vulnerability scanning may begin in Sprint 1 if supported by approved tooling; formal image severity gates and remediation SLAs can be finalized during production hardening.
- Do not deploy to production from Sprint 1 CI. Deployment workflows require an approved target, environment protection, secret store, ownership, and release process.
- If CI cannot start services, keep unit checks in PR and run database/Redis integration smoke checks in a separate approved job; do not label them passed without execution.

## 10 Step-by-Step Implementation Checklist

### A. Repository and workstation

- [ ] Confirm approved repository host and create the private repository.
- [ ] Install Git, Docker Desktop/Compose, selected Python version, `uv`, Node.js LTS/npm, and VS Code.
- [ ] Record tool/runtime versions and supported Windows setup in README.
- [ ] Add `.gitignore` for `.env*` except `.env.example`, Python virtual environments, `__pycache__`, build output, `node_modules`, test caches, and local database artifacts.
- [ ] Add `.editorconfig` and contributor instructions.
- [ ] Create `docs/decisions/sprint-1-decisions.md` with owner/status/due date for open platform decisions.

### B. Backend scaffold

- [ ] Create `backend/pyproject.toml` with runtime and development dependency groups.
- [ ] Create the `src/aegis` package and import-safe FastAPI app factory.
- [ ] Add typed settings and explicit required-value validation.
- [ ] Add `/api/v1/health/live` and `/api/v1/health/ready` with safe response contracts.
- [ ] Add structured logging setup and request correlation middleware.
- [ ] Add tests for app startup, health response shape, config validation, and correlation behavior.
- [ ] Resolve and commit `uv.lock`.
- [ ] Run backend checks from a fresh environment.

### C. Frontend scaffold

- [ ] Initialize React + TypeScript using Vite (or the approved equivalent).
- [ ] Keep the initial UI to a neutral platform shell; add no sign-in/chat/business feature.
- [ ] Configure ESLint, TypeScript strictness, build, and test commands.
- [ ] Confirm generated bundles contain no server credentials or local environment secrets.
- [ ] Resolve and commit `package-lock.json`.
- [ ] Run frontend checks from a clean `npm ci`.

### D. Database and cache

- [ ] Select and pin the approved PostgreSQL + pgvector development image.
- [ ] Configure local database, dedicated application user, private Compose networking, health check, and named volume.
- [ ] Verify `SELECT 1` from API container using the application database identity.
- [ ] Verify pgvector extension availability with an explicit smoke check.
- [ ] Add Redis with health check and no authoritative persistence.
- [ ] Verify API connection behavior for both dependencies and document Redis optionality.
- [ ] Confirm stopping Redis does not affect PostgreSQL data or imply success for any operation requiring coordination.

### E. Docker Compose

- [ ] Add backend and frontend Dockerfiles and Compose services.
- [ ] Add `backend/.dockerignore` and `frontend/.dockerignore`; ensure build contexts exclude secrets and local artifacts.
- [ ] Bind developer ports to loopback where host access is required.
- [ ] Add health checks and dependency startup behavior.
- [ ] Start services from a clean checkout and confirm the web shell and API are reachable locally.
- [ ] Restart containers and verify PostgreSQL volume behavior.
- [ ] Document safe local data reset and shutdown steps.

### F. CI pipeline

- [ ] Confirm CI vendor; create pipeline in approved host.
- [ ] Run backend lint, type check, tests; frontend lint, type check, build, tests.
- [ ] Add secret scanning and dependency lockfile scanning.
- [ ] Build container images without secrets.
- [ ] Require passing CI checks before merge.
- [ ] Verify a deliberate test failure and controlled secret-scan fixture cause expected CI failure without using real credentials.
- [ ] Confirm reports/artifacts contain no sensitive data.

### G. Clean-checkout acceptance

- [ ] Follow README on a clean Windows checkout.
- [ ] Start local stack using documented Compose command.
- [ ] Verify API liveness/readiness, frontend shell, PostgreSQL connectivity/pgvector, Redis connectivity.
- [ ] Stop Redis and confirm the documented optional-dependency behavior.
- [ ] Run all backend/frontend checks and CI-equivalent commands.
- [ ] Review logs for correlation IDs and confirm tokens/secrets/request bodies are absent.
- [ ] Record completion evidence and blockers against TS-001, TS-002, TS-003, TS-019, and initial TS-020.

## 11 Sprint 1 Exit Criteria

Sprint 1 foundation is accepted when:

- The repository structure matches the active foundation needs and preserves modular-monolith boundaries.
- A clean checkout can start React, FastAPI, PostgreSQL/pgvector, and Redis locally using documented instructions.
- API liveness/readiness and OpenAPI are available with safe response behavior.
- PostgreSQL and Redis connectivity are verified; pgvector availability is proven; Redis is not authoritative.
- Structured logs and request correlation work without sensitive payload logging.
- Backend/frontend local checks and CI pass; secret scanning is active.
- CI builds containers without credentials and enforces required checks.
- No business feature or unresolved external decision has been smuggled into the scaffold.
- Open decisions blocking Sprint 2 have owners, due dates, and explicit status.

## 12 Decisions to Confirm Before Sprint 1 Starts

- Approved repository host and CI provider.
- Supported Python and Node.js versions and package-manager policy.
- Docker Desktop/image registry policy and approved PostgreSQL/pgvector and Redis image tags.
- Whether a structured logging package is preferred over standard-library logging.
- CI scanner/tooling and vulnerability severity gates.
- Local port binding and any corporate endpoint/network restrictions.
- Which local development values may be used and how `.env` is provisioned.

If a decision is not available, use only a reversible local-development default, record it as provisional, and do not deploy externally or use real organizational data.
