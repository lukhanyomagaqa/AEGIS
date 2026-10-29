# AEGIS Repository Structure and Sprint 1 Implementation Plan

**Status:** Proposed implementation plan  
**Source:** Approved AEGIS MVP Backlog  
**Sprint:** Sprint 1 — Foundation and decisions  
**Duration:** Two weeks of focused effort; extend calendar for part-time availability  
**Implementation owner:** Solo developer  
**Workspace note:** The current AEGIS workspace contains planning documents, not an initialized application repository. The structure below is a proposed target; it does not imply that code has already been scaffolded.

## 1 Sprint 1 Goal

Establish a repeatable, secure local development foundation for the AEGIS modular monolith and React client. At the end of Sprint 1, a developer should be able to start the local stack from documented instructions, run baseline checks, and understand which architecture and policy decisions block the next milestones.

Sprint 1 is foundation work, not delivery of user-facing AI features. It must not silently decide unresolved Entra role mappings, provider/data-handling terms, data retention, approval policy, or production hosting.

### Backlog alignment

| Backlog item | Sprint 1 treatment |
|---|---|
| TS-001 — Repository layout/toolchain | Complete foundation conventions, module boundaries, local checks and developer documentation. |
| TS-002 — Docker local environment | Provide local API, frontend, PostgreSQL/pgvector and Redis services with health checks and safe local configuration. |
| TS-003 — FastAPI lifecycle/API baseline | Establish app startup/shutdown, versioned API shell, safe error convention, OpenAPI and health endpoints. |
| TS-019 — CI workflow | Implement an initial pipeline for repository checks and container/build validation; add broader integration/e2e coverage as those tests exist. |
| TS-020 — Security scanning | Decide the first pipeline scan gates and add available secret/dependency checks only if they fit the approved pipeline/tooling. Complete container vulnerability policy in the hardening milestone if it requires deployment-specific decisions. |
| Sprint 1 decision tasks | Assign owners and due dates for identity, provider, data governance, knowledge source, approver policy, deployment, backup/DR and retention decisions. |

### Explicitly not Sprint 1 scope

- Entra production application configuration, full token validation, role mapping, or user provisioning (Sprint 2; Sprint 1 only records owners/configuration prerequisites).
- Conversation/approval/audit/knowledge schema implementation beyond health and service connectivity needed by the foundation.
- Model/provider integration, vector ingestion, Knowledge Agent, Helpdesk Agent, or broad source connectors.
- Consequential tool execution.
- Production deployment, production credentials, or a full backup/DR implementation.
- LangGraph, multi-tenancy, additional agents, or broad external integrations.

## 2 Proposed Repository Structure

The structure follows the ADR's modular-monolith decision and inward dependency direction. It is intentionally a target layout, not a requirement to create every directory in Sprint 1. Create a directory when the corresponding code or documentation is needed; avoid empty scaffolding.

```text
AEGIS/
├── README.md
├── CONTRIBUTING.md
├── .gitignore
├── .editorconfig
├── .env.example
├── compose.yaml
├── Makefile                         # Optional; use only if useful on supported developer platforms
├── docs/
│   ├── decisions/                   # Approved ADRs and decision log
│   ├── architecture/
│   ├── security/
│   ├── operations/
│   └── development/
├── backend/
│   ├── pyproject.toml               # Python tool/dependency configuration
│   ├── lockfile                     # Chosen Python package manager lockfile
│   ├── Dockerfile
│   ├── alembic.ini                  # Introduce with database migrations
│   ├── migrations/                  # Introduce with the first persisted domain schema
│   ├── src/
│   │   └── aegis/
│   │       ├── main.py              # FastAPI composition/application entry point
│   │       ├── config/              # Typed settings, environment validation
│   │       ├── api/
│   │       │   └── v1/              # Versioned routes, schemas, API dependencies
│   │       ├── application/          # Use cases and application services
│   │       ├── domain/               # Framework-independent entities, rules, ports
│   │       ├── infrastructure/       # DB, Redis, provider, identity, integration adapters
│   │       ├── modules/
│   │       │   ├── identity/
│   │       │   ├── conversations/
│   │       │   ├── knowledge/
│   │       │   ├── agents/
│   │       │   ├── approvals/
│   │       │   └── audit/
│   │       └── observability/        # Structured logging, correlation, health
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── contract/
├── frontend/
│   ├── package.json
│   ├── lockfile                     # Chosen frontend package manager lockfile
│   ├── tsconfig.json
│   ├── vite.config.ts               # Or another approved React build tool
│   ├── Dockerfile
│   ├── src/
│       ├── app/                     # App composition, routing, providers
│       ├── features/
│       │   ├── auth/
│       │   ├── chat/
│       │   ├── conversations/
│       │   ├── knowledge/
│       │   └── approvals/
│       ├── services/                # Typed API client and auth integration
│       ├── components/              # Shared UI components
│       └── types/
│   └── tests/
├── infra/
│   ├── docker/                      # Local/development container configuration
│   └── deployment/                  # Add only after deployment target is approved
├── scripts/                         # Cross-platform developer/CI helpers, if needed
└── .github/
    └── workflows/                   # CI workflows if GitHub is the approved repository host
```

### Structure rules

- Keep domain rules independent of FastAPI, SQLAlchemy/database libraries, Entra SDKs, and AI-provider SDKs.
- Keep HTTP route handlers thin: validate/translate requests and call application use cases.
- Modules own their rules and persistence interfaces. Cross-module use goes through application-facing contracts rather than importing another module's internals.
- Keep all environment-specific settings in validated configuration. `.env.example` contains placeholders only; populated `.env` files are ignored and never committed.
- Keep provider credentials, database credentials, tokens, and production configuration out of the frontend bundle, source control, container images, and logs.
- Use one backend deployable for the MVP. Do not create separately deployed services for modules.
- Keep `approvals/` and `audit/` as explicit domain boundaries, even if their implementation begins after Sprint 1.
- Keep LangGraph-specific dependencies and state out of the MVP structure.
- Do not add a directory or technology merely because it appears in the target tree; confirm it is needed and fits the approved architecture.

## 3 Sprint 1 Tasks

Estimates are initial story-point allocations for a solo developer and should be adjusted during Sprint Planning. They include tests and documentation. Decision tasks are timeboxed coordination tasks, not code story points.

### S1-01 — Confirm sprint scope and decision owners

- **Backlog mapping:** Sprint 1 decision tasks; TS-001 prerequisite.
- **Estimate:** 1 point.
- **Dependencies:** Product/service owner availability.
- **Actions:**
  - Confirm the repository host and access model.
  - Assign decision owners and due dates for Entra registration/scopes, role mapping, provider/data handling, initial knowledge source/ACL, retention/deletion, approval policy, deployment target, secret store, logging, and RPO/RTO.
  - Record decisions as approved, open, or explicitly deferred; do not treat silence as approval.
- **Acceptance criteria:**
  - A decision register exists with owner, due date, impact, and blocked backlog items.
  - Sprint 1 implementation choices do not pre-empt unresolved security/product decisions.

### S1-02 — Establish repository conventions and module boundaries

- **Backlog mapping:** TS-001.
- **Estimate:** 2 points.
- **Dependencies:** Repository host/access.
- **Actions:**
  - Create the root documentation and source layout needed for active Sprint 1 code.
  - Add `.gitignore`, editor conventions, and contributor instructions.
  - Document backend module ownership and dependency direction.
  - Choose Python and frontend toolchains supported by the developer environment; commit lockfiles.
- **Acceptance criteria:**
  - A clean checkout has a documented path to install dependencies and run checks.
  - Source control ignores local secrets, environments, build output, test artifacts, and caches.
  - No actual credentials, tokens, or production configuration are present in tracked files.

### S1-03 — Configure backend development checks

- **Backlog mapping:** TS-001.
- **Estimate:** 2 points.
- **Dependencies:** S1-02.
- **Actions:**
  - Configure the selected Python formatter/linter, type-checker, and unit-test runner.
  - Define a minimal FastAPI package entry point and import-safe app factory.
  - Add a small passing test that proves the test command works.
- **Acceptance criteria:**
  - One documented command runs Python formatting/lint, type checks, and unit tests.
  - Checks pass from a clean environment and return nonzero on an intentional failure.
  - Domain/application package layout does not depend on FastAPI.

### S1-04 — Configure frontend development checks

- **Backlog mapping:** TS-001, TS-016 foundation.
- **Estimate:** 2 points.
- **Dependencies:** S1-02.
- **Actions:**
  - Initialize the React/TypeScript client using an approved build tool.
  - Configure lint, type-check, build, and frontend test commands.
  - Establish feature-based source organization and typed API-service boundary.
- **Acceptance criteria:**
  - One documented command runs frontend lint/type/build checks.
  - Production build contains no API keys or server-side credentials.
  - A clean install is reproducible from the committed lockfile.

### S1-05 — Implement FastAPI application lifecycle and baseline API

- **Backlog mapping:** TS-003.
- **Estimate:** 3 points.
- **Dependencies:** S1-03.
- **Actions:**
  - Create the FastAPI application entry point and explicit startup/shutdown lifecycle.
  - Add a versioned API namespace and a minimal safe error response convention.
  - Add liveness and readiness endpoint placeholders; readiness must not expose internal secrets.
  - Ensure OpenAPI is available for the API contract.
- **Acceptance criteria:**
  - API starts and shuts down predictably.
  - Versioned health endpoint returns documented response; readiness distinguishes application liveness from required dependency status.
  - Validation/exception responses do not leak stack traces, tokens, or configuration.
  - Focused API tests pass.

### S1-06 — Define local configuration and secret-safe defaults

- **Backlog mapping:** TS-001, TS-002, TS-022.
- **Estimate:** 2 points.
- **Dependencies:** S1-02, S1-05.
- **Actions:**
  - Define typed settings and fail-fast validation for required configuration.
  - Add `.env.example` with placeholders and document local configuration loading.
  - Ensure the application does not silently substitute production-like credentials or disable TLS verification.
- **Acceptance criteria:**
  - Missing required settings produce an explicit, safe startup error.
  - Example configuration contains no usable secrets.
  - Secret scan is run against the initial repository.

### S1-07 — Add PostgreSQL/pgvector local service

- **Backlog mapping:** TS-002; foundation for TS-005.
- **Estimate:** 2 points.
- **Dependencies:** S1-06.
- **Actions:**
  - Select a PostgreSQL container image that includes the approved pgvector extension.
  - Configure a local-only database, health check, and named persistent development volume.
  - Document that local credentials are development-only and must not be reused.
- **Acceptance criteria:**
  - Database service becomes healthy and accepts a local connection from the API network.
  - pgvector extension availability is verified.
  - Restart retains intended local development data; reset procedure is explicit and non-destructive to production data.
  - No database port is exposed beyond the documented local-development need.

### S1-08 — Add Redis local service with ephemeral-use boundary

- **Backlog mapping:** TS-002; ADR-006.
- **Estimate:** 1 point.
- **Dependencies:** S1-06.
- **Actions:**
  - Add a local Redis service with health check and isolated service network.
  - Document intended use: reconstructible cache/rate limits/short-lived coordination only.
  - Avoid adding persistence or authoritative business data.
- **Acceptance criteria:**
  - API can establish a local connection when configured.
  - Redis can be stopped without losing PostgreSQL business records.
  - No conversation, approval, or audit record is stored solely in Redis.

### S1-09 — Containerize backend and frontend for local development

- **Backlog mapping:** TS-002.
- **Estimate:** 3 points.
- **Dependencies:** S1-03, S1-04, S1-05, S1-07, S1-08.
- **Actions:**
  - Add development-appropriate Dockerfiles and compose service definitions.
  - Use health checks and service dependencies without assuming a dependency is always healthy at startup.
  - Keep build and runtime configuration separate; do not bake secrets into image layers.
- **Acceptance criteria:**
  - Documented compose command starts web, API, PostgreSQL/pgvector, and Redis.
  - Health checks report dependency readiness accurately.
  - Application logs remain available through the normal development output.
  - Container configuration does not run as an unnecessarily privileged user where practical.
  - Build contexts exclude local secrets and unrelated artifacts.

### S1-10 — Add request correlation and structured logging baseline

- **Backlog mapping:** TS-003; foundation for TS-015/017.
- **Estimate:** 2 points.
- **Dependencies:** S1-05.
- **Actions:**
  - Generate or accept a validated correlation ID at the API boundary.
  - Add structured request start/completion/error logging with duration and safe route/outcome metadata.
  - Establish redaction rules before adding request bodies or identity claims to logs.
- **Acceptance criteria:**
  - Correlation ID appears consistently in response headers and associated logs.
  - Tokens, cookies, secrets, and message bodies are not logged by default.
  - Failure paths produce explicit correlated events without success-shaped fallbacks.

### S1-11 — Add continuous integration baseline

- **Backlog mapping:** TS-019 (initial).
- **Estimate:** 3 points.
- **Dependencies:** S1-03, S1-04.
- **Actions:**
  - Configure CI on the approved repository host.
  - Run backend lint/type/unit checks and frontend lint/type/build checks.
  - Add a Docker image/build validation step where runner support allows.
  - Ensure test/report artifacts do not contain secrets.
- **Acceptance criteria:**
  - CI runs on proposed changes and blocks merge/release on required-check failure.
  - A clean branch produces a successful run.
  - CI credentials use least privilege; no production credential is required for baseline validation.

### S1-12 — Add initial secret/dependency scanning

- **Backlog mapping:** TS-020 (initial).
- **Estimate:** 2 points.
- **Dependencies:** S1-11.
- **Actions:**
  - Select repository-compatible secret and dependency scanners that fit approved tooling.
  - Define what findings block a change versus require triage.
  - Document a response process for an accidentally committed credential, including revocation/rotation rather than only deleting the file.
- **Acceptance criteria:**
  - Scans run in CI or an approved pre-merge workflow.
  - A controlled test finding demonstrates reporting/blocking behavior without using a real secret.
  - Finding ownership and remediation path are documented.

### S1-13 — Write local development and architecture documentation

- **Backlog mapping:** TS-001, TS-002, TS-003.
- **Estimate:** 2 points.
- **Dependencies:** S1-02 through S1-11.
- **Actions:**
  - Document prerequisites, startup, health checks, tests, stop/restart behavior, local data reset, and common troubleshooting.
  - Document module boundaries, dependency direction, configuration and secret rules, and the explicit dispatcher/agent seam planned for later work.
  - Link the approved ADRs and product/security/knowledge documents.
- **Acceptance criteria:**
  - A second developer can follow instructions on a clean checkout without oral setup help.
  - Documentation clearly distinguishes local development from production deployment.
  - No undocumented credentials, external service subscriptions, or network assumptions are required for the local foundation.

### S1-14 — Sprint review and next-sprint readiness

- **Backlog mapping:** Sprint planning governance.
- **Estimate:** 1 point.
- **Dependencies:** S1-01 through S1-13.
- **Actions:**
  - Demonstrate clean checkout to local stack, health, CI, and security scans.
  - Review decision register and assign follow-up owners/dates.
  - Refine Sprint 2 stories based on actual capacity and unresolved identity decisions.
- **Acceptance criteria:**
  - Sprint exit evidence is linked to tasks.
  - Blocked decisions have an owner and escalation date.
  - Sprint 2 backlog meets Definition of Ready; no external dependency is hidden in committed work.

**Indicative Sprint 1 effort:** approximately 28 points including decision and review work. This exceeds the backlog's nominal near-full-time 18–22 point planning range. Do not force completion into two weeks: either reduce the committed scope (preserving P0 checks), split the work, or extend the sprint calendar based on actual part-time capacity.

### Recommended commitment if capacity is limited

Commit first to S1-01 through S1-10 and S1-13 for a minimum runnable foundation. Treat S1-11 and S1-12 as mandatory before accepting contributions or treating the repository as release-capable; if they do not fit, explicitly extend Sprint 1 or use the repository host's approved baseline protections while CI work completes. S1-14 is the review/transition task, not optional documentation.

## 4 Sprint 1 Daily Sequence

This sequence is a suggestion, not a fixed work-hour schedule.

| Days | Focus | Expected checkpoint |
|---|---|---|
| 1–2 | S1-01, S1-02 | Repository boundaries and decision register exist; toolchain chosen. |
| 3–4 | S1-03, S1-04 | Backend/frontend checks run locally. |
| 5–6 | S1-05, S1-06 | FastAPI lifecycle, API baseline, configuration validation and safe examples. |
| 7–8 | S1-07, S1-08 | PostgreSQL/pgvector and Redis local services healthy. |
| 9–10 | S1-09, S1-10 | Compose stack runs; correlation and structured logs verified. |
| 11–12 | S1-11, S1-12 | CI and initial security scans run on a clean change. |
| 13 | S1-13 | Setup/architecture documentation tested from clean checkout. |
| 14 | S1-14 | Demonstration, evidence capture, decision escalation and Sprint 2 refinement. |

If availability is part-time, treat these as effort-day checkpoints and spread them across more calendar days.

## 5 Sprint 1 Definition of Done

Sprint 1 is complete when:

- The repository has an approved root structure with backend, frontend, documentation, and infrastructure boundaries.
- Local environment starts the API, frontend, PostgreSQL with pgvector, and Redis using documented commands.
- FastAPI exposes the initial versioned health/OpenAPI surface with explicit safe errors and lifecycle handling.
- Backend and frontend formatting/lint/type/build/test checks run locally and in CI.
- CI validates changes; baseline secret/dependency scanning is operating or an explicitly approved short-term gap is tracked with owner and due date.
- Local settings are validated and examples contain placeholders only; no secrets are present in source or images.
- Structured logs include request correlation without tokens or user message bodies by default.
- Redis is documented and configured only for optional ephemeral use; PostgreSQL remains the durable system of record.
- Module boundaries and deferred technologies (especially LangGraph) are documented.
- Setup documentation has been followed successfully from a clean checkout.
- Entra/provider/source/retention/approval/deployment decisions needed for Sprint 2 and later have owners and dates.
- Demonstration and test evidence are linked; next sprint work is ready or explicitly blocked.

## 6 Sprint 1 Risks and Responses

| Risk | Response |
|---|---|
| Repository host or organizational access is not available. | Track as a day-one blocker; use only an approved temporary repository location; do not copy source to an unapproved external system. |
| Entra/provider/source decisions are delayed. | Record the owner and due date; do not implement a guessed production configuration. Continue with local stubs/configuration boundaries that do not grant access or send data. |
| Docker image/tool choice is incompatible with the developer environment. | Validate minimal images and toolchains early; record versions; avoid adding unrelated services. |
| Sprint scope exceeds part-time capacity. | Protect secure configuration, tests and a runnable stack; extend calendar or move nonessential scanning refinements while retaining approved repository protections. |
| “Health” endpoint exposes internals. | Separate liveness/readiness and return minimal public status; keep detailed dependency/diagnostic data protected. |
| Sample configuration accidentally contains a credential. | Use placeholders only, run secret scanning, and document immediate revoke/rotate procedure for any exposure. |

## 7 Sprint 1 Exit Decision

At Sprint Review, the product/service owner and developer should decide:

1. Is the repository structure clear enough to add identity and persistence modules without restructuring?
2. Can a clean checkout start the complete local stack and run baseline checks?
3. Are identity, role mapping, initial source/ACL semantics, provider/data handling, retention, and deployment decisions assigned and scheduled?
4. Is the Sprint 2 scope supportable at observed developer capacity?
5. Are any security or operational blockers serious enough to halt feature work?

A “no” answer on secure repository handling, token/configuration decisions needed by Sprint 2, or repeatable local setup must produce a tracked action before expanding feature scope.
