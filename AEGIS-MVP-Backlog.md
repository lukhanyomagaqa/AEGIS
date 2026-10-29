# AEGIS MVP Backlog

**Status:** Proposed execution baseline for product/engineering approval  
**Version:** MVP / pre-1.0  
**Audience:** Solo developer, product owner, IT operations, Security, and reviewers  
**Planning horizon:** Six two-week sprints plus stabilization  
**Backlog owner:** AEGIS product/service owner (to be assigned)  
**Implementation owner:** Solo developer (initial assumption)

> **Source-of-truth note:** This backlog converts the approved ADRs and the MVP Functional Specification, Security Model, Environment Knowledge Model, and Knowledge Seeding Plan into executable work. Architecture decisions are treated as constraints. Backlog ordering, estimates, role mappings, data policy, provider configuration, and integration details are proposed planning assumptions requiring confirmation where noted. Keep status, owner, estimate, dependency, and acceptance evidence current in the team's chosen tracker; this document is the baseline, not a substitute for tracking completed work.

## 1 Executive Summary

This backlog is the implementation-oriented source of truth for planning and tracking the AEGIS MVP. It turns product behavior and architectural/security boundaries into milestones, epics, features, user stories, technical stories, acceptance criteria, dependencies, and release gates.

The MVP is an internal, single-organization IT Operations Assistant with a FastAPI modular-monolith backend, React/TypeScript frontend, PostgreSQL with pgvector, optional Redis for ephemeral uses, Microsoft Entra ID authentication, durable conversations, approved knowledge ingestion, Knowledge and Helpdesk Agents, audit logging, and approval workflows for any enabled consequential action. LangGraph, other agents, multi-tenancy, and broad unreviewed automation are out of scope.

### Delivery approach

- Deliver a usable, tested vertical slice each sprint: identity and persistence first, then retrieval and agents, then the user experience and guarded operations.
- Keep domain logic behind application interfaces and keep route handlers thin. The initial dispatcher is explicit and testable; do not introduce LangGraph.
- Seed approved knowledge manually before building automated connectors. A source must have an owner, permitted access scope, provenance, classification, status, and review date before publication.
- Make authorization, source visibility, exact-action approval, explicit error behavior, and durable audit release requirements, not post-launch enhancements.
- Treat product/provider/identity and data-governance decisions as external dependencies with named decision owners.

### Solo-developer assumptions

- One developer owns design, implementation, tests, documentation, deployment setup, and coordination; product/security/source owners provide timely decisions and content reviews.
- Six two-week sprints are the requested baseline sequence, not a guaranteed calendar commitment. For a focused, near-full-time solo developer, use **18–22 points per two-week sprint** as an initial planning range and recalibrate after Sprint 1. Part-time work extends calendar time; it does not compress the same scope into six elapsed two-week periods.
- Estimates assume a small, approved first knowledge source, one approved model/provider configuration, no broad external tool integration, and no autonomous consequential execution in the initial release.
- Entra app registration, provider selection, data classification/retention, approver policy, deployment target, and initial source ACL semantics must be resolved before affected work can complete.
- The sprint plan is a proposed sequence. Re-estimate after Sprint 1 and at each sprint review.

### Backlog conventions

- **Priority:** `P0` = mandatory MVP/release gate; `P1` = expected MVP capability; `P2` = defer unless capacity and approvals permit.
- **Status:** All items begin `Backlog`; update to `Ready`, `In Progress`, `Blocked`, or `Done` in the tracker. A story is not `Done` until its acceptance evidence is linked.
- **Dependencies:** IDs name actual prerequisites; sequence alone does not imply a dependency.
- **Estimates:** Story points are relative effort/risk, not hours. A 13-point item should normally be split before commitment.
- **Scope guard:** An integration listed as a candidate is not committed MVP work until its owner, access, security, and operational policies are approved.

## 2 MVP Milestones

| Milestone | Business goal | Deliverables | Dependencies | Success criteria |
|---|---|---|---|---|
| **M1 — Project Foundation** | Establish a repeatable, testable application foundation. | Repository conventions; Python/TypeScript toolchains; Docker local stack; FastAPI modular monolith skeleton; PostgreSQL/pgvector and Redis configuration; CI checks; structured logging/health baseline. | Approved runtime/toolchain and repository access. | Developer can start the documented stack; CI runs lint, type checks, and tests; secrets are absent from source; module boundaries are documented. |
| **M2 — Identity and Security** | Ensure only valid organizational principals access authorized resources. | Entra sign-in; API token validation; internal principal mapping; initial approved role mapping; backend authorization; denial and authentication audit events. | M1; Entra registration/audience/scopes and role-mapping decisions. | Valid tokens are accepted; invalid/wrong-audience tokens rejected; resource-level authorization tests pass; no browser-side authorization is relied on. |
| **M3 — Conversations and Persistence** | Let authenticated users create and revisit durable, private conversations. | User records; conversations/messages/runs persistence; conversation APIs; ownership checks; versioned API errors/contracts; persistence tests. | M1, M2, DB migrations. | Authenticated user can create, send, list, and retrieve own conversation; another user cannot access it; data survives restart. |
| **M4 — Knowledge Platform** | Establish governed, permission-aware organizational knowledge. | Entity/source/article metadata; manual ingestion workflow; lifecycle/status/version; approved seed set; pgvector embeddings and metadata; keyword/semantic retrieval and citations. | M1, M2, M3; source owner, classification, ACL, initial source and model/provider decisions. | Approved content can be ingested, updated, withdrawn, and retrieved with source references; visibility tests pass before chunks reach an agent. |
| **M5 — Knowledge Agent** | Answer environment-specific questions from approved evidence. | Agent contract; explicit dispatcher; Knowledge Agent; citations/confidence/uncertainty; provider adapter and failure mapping; representative evaluation set. | M3, M4; provider and data-handling approval. | Questions receive sourced answers or explicit safe “not found/conflict/failure”; unauthorized content is never included. |
| **M6 — Helpdesk Agent** | Provide supported first-line IT guidance and route requests safely. | Helpdesk Agent; supported intent/procedure set; run states; safe escalation and unsupported behavior; read-only tool policy if any. | M3, M4, M5 shared agent contract; approved support procedures and escalation map. | Representative requests route correctly; procedures respect scope/stop conditions; no unsupported operation is reported as completed. |
| **M7 — Approvals and Audit** | Prevent unapproved consequential changes and preserve attributable evidence. | Durable approval lifecycle; exact-action binding; reviewer UI/API; audit events for approvals, tool decisions, executions, and security events; state-transition tests. | M2, M3, tool classification/approver policy, approved audit/retention decisions. | Consequential actions cannot execute without valid matching approval; rejection, expiry, revocation, replay, and parameter changes block execution; records survive restart. |
| **M8 — Frontend Dashboard** | Give users a complete, understandable experience for the MVP capabilities. | Entra sign-in UI; chat; conversation history; status/errors; citations; approval review where enabled; typed API client. | M2, M3, M5, M6; API contracts. | User completes sign-in, chat, history, source inspection, and eligible approval review without trusting UI for security enforcement. |
| **M9 — Production Hardening** | Demonstrate release readiness, recovery, observability, and operational ownership. | End-to-end tests; backup/restore verification; security/dependency/container scans; production configuration; alerts/runbooks; access/retention decisions; release checklist. | M1–M8; deployment target, RPO/RTO, retention and incident policy. | Acceptance tests pass in production-like environment; no open release-blocking security issues; rollback, restore, monitoring, and support handoff verified. |

Milestones may overlap in implementation, but each milestone's exit criteria are gates. No consequential tool may be enabled merely because the approval UI or database schema exists; the operation, requester/approver roles, expiry, retry, and execution policy must also be approved.

## 3 Product Epics

### EPIC-001 — Platform Foundations

- **Vision:** A modular monolith and local/deployment foundation that is secure, repeatable, and straightforward for one developer to maintain.
- **Business value:** Reduces delivery friction and operational complexity while protecting module boundaries.
- **Dependencies:** Repository, runtime, hosting/container assumptions.
- **Risks:** Overbuilding infrastructure; hidden environment-specific configuration; accidental secrets in local setup.
- **Definition of Done:** Docker-based local stack and CI work from documented steps; module boundaries, configuration and health checks are explicit; tests and secret scanning pass.
- **Features:** Repository/toolchain setup; Docker Compose; FastAPI application lifecycle; PostgreSQL/pgvector and Redis; API versioning/error envelope; CI and configuration management.

### EPIC-002 — Authentication and Identity

- **Vision:** Authenticate users with Microsoft Entra ID and establish a stable internal principal.
- **Business value:** Provides organization-aligned sign-in and a trusted identity boundary for all use cases.
- **Dependencies:** EPIC-001; Entra application registration, issuer/audience/scopes, and role-mapping decisions.
- **Risks:** Identity configuration delays; invalid claim/tenant assumptions; token leakage or acceptance of ID tokens.
- **Definition of Done:** API validates signature, issuer, audience, expiry and required claims; maps issuer/subject to internal ID; invalid tokens are rejected; sign-in/logout behavior and tests are documented.
- **Features:** Entra login; API token validation; principal provisioning/mapping; logout/session behavior; role mapping; authentication audit events.

### EPIC-003 — Conversation System

- **Vision:** Provide durable, private conversations and traceable agent runs.
- **Business value:** Gives users continuity and supplies reliable context for support and evaluation.
- **Dependencies:** EPIC-001 and EPIC-002.
- **Risks:** Cross-user access, unclear message/run state, sensitive data retention not defined.
- **Definition of Done:** Conversation/message/run records persist in PostgreSQL; every read/write enforces owner/resource access; failure and cancellation states are explicit; restart-persistence and authorization tests pass.
- **Features:** Conversation CRUD/list; message submission/history; run records/status; ownership enforcement; retention/deletion hooks.

### EPIC-004 — Knowledge Management

- **Vision:** Curate and maintain approved organizational knowledge with ownership, provenance, ACLs, lifecycle, and relationships.
- **Business value:** Makes AEGIS useful for organization-specific questions without treating a document dump as intelligence.
- **Dependencies:** EPIC-001, EPIC-002; approved source owner, initial source, classification, visibility, and retention policies.
- **Risks:** Stale/conflicting content, unowned knowledge, permission drift, overcollection.
- **Definition of Done:** Manual seed can be created, reviewed, published, updated, superseded, and withdrawn with source/owner/classification/status/review metadata; access rules are enforced before retrieval.
- **Features:** Source registry; entity/article metadata; manual ingestion; review/publication lifecycle; versioning and deletion propagation; quality scoring; knowledge search/admin surfaces.

### EPIC-005 — Knowledge Retrieval

- **Vision:** Find relevant, accessible, authoritative evidence and return traceable results.
- **Business value:** Supports accurate, verifiable answers and avoids disclosure through semantic retrieval.
- **Dependencies:** EPIC-004; PostgreSQL/pgvector; approved embedding/model configuration.
- **Risks:** Retrieval leakage; bad ranking; stale cache; embedding/model changes.
- **Definition of Done:** Keyword and semantic/hybrid retrieval apply access and metadata filters before agent use; citations include source/version; model metadata supports controlled re-indexing; retrieval tests pass.
- **Features:** Chunking/embedding; keyword/vector search; hybrid ranking; ACL filtering; citations/confidence; re-index and cache invalidation.

### EPIC-006 — Knowledge Agent

- **Vision:** Answer supported organizational questions from approved retrieved context.
- **Business value:** Reduces search time and makes operational knowledge accessible through conversation.
- **Dependencies:** EPIC-003, EPIC-005, shared agent contract, approved provider and data-use terms.
- **Risks:** Hallucination, prompt injection, unsupported certainty, provider outage/cost.
- **Definition of Done:** Agent uses only authorized supplied context, cites factual claims, reports uncertainty/no-result/failure explicitly, and passes representative and adversarial tests.
- **Features:** Provider-neutral agent interface; prompt/context policy; question handling; citation answer formatting; confidence and no-answer behavior; evaluation set.

### EPIC-007 — Helpdesk Agent

- **Vision:** Resolve supported first-line questions and recommend approved procedures/escalations.
- **Business value:** Improves consistency and routing for repeatable IT support requests.
- **Dependencies:** EPIC-003, EPIC-004, EPIC-006 common contracts; approved support procedures and escalation paths.
- **Risks:** Unsafe or out-of-scope instructions; repeated fixes become unreviewed policy; accidental side effects.
- **Definition of Done:** Supported intents route to approved procedures; unsupported requests are explicit; agent cannot bypass tool policy or approval; procedure prerequisites and stop conditions are retained.
- **Features:** Helpdesk intent routing; procedure recommendations; safe troubleshooting output; escalation guidance; reviewed read-only tool boundary.

### EPIC-008 — Approval Framework

- **Vision:** Ensure a consequential action executes only after attributable approval for the exact proposed operation.
- **Business value:** Enables safe, auditable human oversight while preventing model authority from becoming execution authority.
- **Dependencies:** EPIC-002, EPIC-003, EPIC-009; approved operation classification, approver roles, expiry, rejection/cancellation/retry policy.
- **Risks:** Replay, action tampering, self-approval, race conditions, ambiguous external execution.
- **Definition of Done:** Durable state machine, canonical action binding, atomic one-time execution, permission revalidation, expiry/rejection/revocation behavior, and full tests. Tier 4 actions remain unavailable to MVP agents.
- **Features:** Approval request; action canonicalization/binding; decision authorization; lifecycle transitions; execution gate; approval UI/status; retry/reconciliation rules.

### EPIC-009 — Audit Framework

- **Vision:** Preserve security-relevant, attributable history for identity, authorization, knowledge, agent runs, tools, approvals, and administration.
- **Business value:** Enables operations, investigation, governance, and proof that approval and access policies were enforced.
- **Dependencies:** EPIC-001, EPIC-002, EPIC-003; approved retention/access policy.
- **Risks:** Missing events, sensitive payload leakage, mutable audit evidence, unavailable audit persistence.
- **Definition of Done:** Structured correlated events are durable in PostgreSQL, access/mutation is restricted, payloads are minimized, critical operations fail closed when required audit persistence fails, and coverage tests pass.
- **Features:** Audit event model/writer; auth/authorization events; agent/tool/approval events; audit access/export; retention and integrity controls.

### EPIC-010 — Frontend Experience

- **Vision:** Let users safely sign in, chat, inspect citations, track runs, manage conversations, and review approvals where enabled.
- **Business value:** Converts backend capability into a discoverable and comprehensible product.
- **Dependencies:** EPIC-002, EPIC-003, EPIC-006, EPIC-007, EPIC-008 API contracts.
- **Risks:** UI gives false impression of authorization or success; accessibility and error handling overlooked.
- **Definition of Done:** React/TypeScript features consume typed versioned APIs; loading/empty/error states are clear; client hides but does not enforce permissions; key user journeys pass end-to-end.
- **Features:** Entra client; chat and conversation list; run status; citations; approval inbox/review; error/unsupported display; accessible responsive layout.

### EPIC-011 — Operations and Monitoring

- **Vision:** Run, diagnose, secure, recover, and release AEGIS predictably.
- **Business value:** Reduces operational risk and enables a production-supported MVP.
- **Dependencies:** EPIC-001; environment owners and deployment/backup/incident decisions.
- **Risks:** Provider cost, missing alerts/runbooks, untested recovery, vulnerable images/dependencies.
- **Definition of Done:** Health/readiness and structured logs available; secrets managed; backup/restore and deployment validation tested; scans run; monitoring, incident and support runbooks assigned.
- **Features:** Health/readiness; request correlation and metrics; Docker release configuration; CI/CD; security scans; backups/DR; cost/usage controls; runbooks and release evidence.

### Feature breakdown

Feature priorities: `P0` release-essential; `P1` expected MVP; `P2` defer unless justified. Complexity is relative: `S`, `M`, `L`.

| Epic | Feature | Description | Priority | Complexity | Dependencies |
|---|---|---|---|---|---|
| EPIC-001 | Repository and toolchain | Establish API/web structure, lint/type/test commands, configuration conventions and module rules. | P0 | M | None |
| EPIC-001 | Docker local stack | Start API, web, PostgreSQL/pgvector and Redis with safe local configuration. | P0 | M | Repository |
| EPIC-001 | FastAPI lifecycle | App factory, thin routes, dependency setup, startup/shutdown, health/readiness. | P0 | M | Repository |
| EPIC-001 | API contract baseline | Versioned routes, validation and consistent errors/OpenAPI. | P0 | M | FastAPI lifecycle |
| EPIC-001 | PostgreSQL and migrations | Durable schema, migrations, least-privilege app connection. | P0 | M | Docker/runtime |
| EPIC-001 | Redis ephemeral integration | Optional cache/rate limits with TTL and graceful cache loss. | P1 | S | Docker/runtime |
| EPIC-002 | Entra login | Browser OIDC Authorization Code + PKCE through approved client configuration. | P0 | M | Entra registration |
| EPIC-002 | Token validation | API signature/issuer/audience/expiry/claims checks. | P0 | M | Entra audience/scopes |
| EPIC-002 | User provisioning | Stable internal user ID mapped to issuer/subject. | P0 | S | Token validation, DB |
| EPIC-002 | Role mapping | Approved Entra claims/groups to server-side application permissions. | P0 | M | Role policy decision |
| EPIC-002 | Permission evaluation | Backend action and object-level authorization. | P0 | M | Principal and role mapping |
| EPIC-003 | Conversation APIs | Create/list/retrieve/update/archive own conversations. | P0 | M | Auth, persistence |
| EPIC-003 | Message/run persistence | Persist message, run status, agent reference, correlation and timestamps. | P0 | M | Conversation APIs |
| EPIC-003 | Ownership isolation | Deny cross-user conversation/message/run access. | P0 | M | Resource model |
| EPIC-004 | Source/entity registry | Store owner, authority, ACL reference, classification, lifecycle and source identifiers. | P0 | M | Data dictionary/owner decisions |
| EPIC-004 | Manual ingestion | Controlled entry/upload and validation for initial approved sources. | P0 | M | Source registry |
| EPIC-004 | Review/version lifecycle | Draft/review/publish/supersede/archive/delete with history. | P0 | M | Manual ingestion, owner workflow |
| EPIC-004 | Knowledge seed set | Curate first procedures, articles, services and environment relationships. | P0 | M | Workshops, approved sources |
| EPIC-004 | Quality and freshness | Score required metadata, flag stale/unowned/conflicting records. | P1 | M | Lifecycle metadata |
| EPIC-005 | Chunk/embed/index | Preserve source/version/model metadata and index approved content in pgvector. | P0 | M | Approved model/embedding config |
| EPIC-005 | Keyword/vector/hybrid retrieval | Exact identifier and semantic retrieval with rank controls. | P0 | M | Index |
| EPIC-005 | ACL and metadata filters | Filter before text reaches agent; include effective visibility. | P0 | L | Approved ACL semantics |
| EPIC-005 | Citation/provenance | Return source title/reference/version and scoped relationship evidence. | P0 | M | Retrieval |
| EPIC-006 | Shared agent contract/dispatcher | Typed request/response and deterministic routing without LangGraph. | P0 | M | Run persistence |
| EPIC-006 | Knowledge response policy | Grounded answer, citations, uncertainty, prompt injection resistance. | P0 | M | Retrieval, provider |
| EPIC-006 | Model provider adapter | Configured provider, timeout, bounded retries, error mapping and usage telemetry. | P0 | M | Provider decision |
| EPIC-007 | Helpdesk intent set | Supported intents mapped to procedures/categories and explicit exclusions. | P0 | M | Seed procedures |
| EPIC-007 | Procedure recommendation | Preserve scope, prerequisites, stop conditions and escalation. | P0 | M | Helpdesk intent set |
| EPIC-007 | Read-only tool boundary | Only individually reviewed and authorized operations, if enabled. | P1 | M | Tool inventory/policy |
| EPIC-008 | Approval policy/state machine | Durable pending/approved/rejected/expired/cancelled/revoked/executed states. | P0 | M | Approver policy |
| EPIC-008 | Exact-action binding | Canonical parameters, requester, policy and expiry bound to approval. | P0 | M | State machine |
| EPIC-008 | Execute/replay protection | Recheck roles/approval and atomically consume approval before execution. | P0 | L | Exact binding |
| EPIC-009 | Audit writer | Structured durable events and correlation IDs. | P0 | M | DB model |
| EPIC-009 | Event coverage/retention | Auth, denials, knowledge changes, agents, tools, approvals; restrict access. | P0 | M | Audit writer, policy |
| EPIC-010 | Sign-in and typed API client | Entra client, token use and typed versioned API integration. | P0 | M | API contracts |
| EPIC-010 | Chat/history dashboard | Conversation list, messaging, statuses, empty/loading/error states. | P0 | M | Conversation APIs |
| EPIC-010 | Citations/answer states | Show citations, uncertainty, no-result, unsupported and provider errors. | P0 | M | Knowledge Agent contract |
| EPIC-010 | Approval review UI | Show exact proposal and decision to authorized approvers. | P0 if action enabled | M | Approval APIs/policy |
| EPIC-011 | Health/logging/metrics | Readiness, structured logs, request correlation, dependency status. | P0 | M | API lifecycle |
| EPIC-011 | CI/release pipeline | Tests, lint, type checks, container build and release controls. | P0 | M | Repository |
| EPIC-011 | Security/dependency scans | Secret, dependency and image scanning with remediation gates. | P0 | M | CI |
| EPIC-011 | Backup/restore/runbooks | Retention, tested restore, incident, rollback and operational instructions. | P0 | M | Deployment target/DR policy |

## 4 User Stories

Stories below are the product-facing backlog. Acceptance criteria are testable outcomes; implementation details belong in linked technical stories. Unless stated otherwise, every story requires server-side authorization, explicit errors, and no secret-bearing logs. Story-point totals and sprint assignments are planning estimates.

### EPIC-002 — Authentication and identity

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-001 | As an organizational user, I want to sign in with Entra ID so that I can access AEGIS using my work identity. | Valid configured user completes approved OIDC flow; failed/cancelled sign-in grants no API access; no SPA secret is required. | TS-001, TS-002; Entra registration | 2 | P0 |
| US-002 | As the API, I want to accept only valid AEGIS access tokens so that requests cannot rely on forged or misdirected identity. | Wrong issuer/audience, invalid signature, expired token, missing required claims, and ID token are rejected; valid API token is accepted. | US-001, TS-003 | 3 | P0 |
| US-003 | As an administrator, I want first-time users mapped to stable internal identities so that records remain attributable across sessions. | Valid issuer/subject maps uniquely to internal user ID; display attributes update safely; duplicate mapping is rejected and audited. | US-002, TS-004 | 2 | P0 |
| US-004 | As a security owner, I want roles derived from approved server-side mappings so that client claims cannot grant permissions. | Only configured mappings grant roles; unknown/missing role defaults to least privilege; role changes are recorded. | US-003; role policy decision | 3 | P0 |
| US-005 | As a user, I want to sign out and clear local application state so that shared devices do not retain my visible session. | UI clears local state/token cache and invokes configured Entra sign-out; protected UI/API requests require valid authentication afterward; token revocation limitations are documented. | US-001 | 2 | P1 |

### EPIC-003 — Conversation system

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-006 | As an authenticated user, I want to create a conversation so that I can start a distinct support request. | Conversation has stable ID, owner, status, timestamps; belongs to current principal; invalid input returns documented error. | US-003, US-004, TS-005 | 2 | P0 |
| US-007 | As an authenticated user, I want to submit a message to my conversation so that AEGIS can process my request. | Message persists with actor/time/status; conversation ownership checked; empty/oversized input rejected; run is created with correlation ID. | US-006, TS-006 | 3 | P0 |
| US-008 | As a user, I want to list and reopen my conversations so that I can continue prior work. | List is scoped to current user, ordered by recent activity, paginated, and excludes unauthorized records; data survives restart. | US-006, TS-005 | 2 | P0 |
| US-009 | As a user, I want to view messages and run outcomes so that I can understand what AEGIS did. | Returns authorized conversation messages and explicit run state; failed/unsupported/cancelled states are not presented as success. | US-007, TS-006 | 2 | P0 |
| US-010 | As a user, I want to archive a conversation so that my history remains manageable. | Archive changes status without deleting audit evidence; only owner or authorized role can archive; archived content is not submitted as new context unless policy permits. | US-006, TS-005 | 2 | P1 |
| US-011 | As a security reviewer, I want cross-user conversation access denied so that private support history is isolated. | Tests cover guessed IDs, list/detail/message/run endpoints; unauthorized access returns standard denial without leaking record content. | US-006–US-009 | 3 | P0 |

### EPIC-004 — Knowledge management

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-012 | As a knowledge administrator, I want to register an approved source so that its ownership and trust are explicit. | Source has owner, source ID, authority/trust, classification, visibility, update method, status and review cadence; incomplete source remains disabled. | TS-007; owner/policy decisions | 3 | P0 |
| US-013 | As a knowledge contributor, I want to create a structured environment record so that AEGIS can answer operational lookups. | Supported entity has stable ID, canonical name, purpose, source, owner, status, classification, review date and typed relationships; missing mandatory metadata blocks publication. | US-012, TS-008 | 3 | P0 |
| US-014 | As a knowledge contributor, I want to add an approved article or procedure so that users can find validated support guidance. | Content/reference includes audience, scope, prerequisites, steps, stop conditions, escalation, source/version and owner; secrets are rejected/redacted. | US-012, TS-008 | 3 | P0 |
| US-015 | As a knowledge reviewer, I want to review and approve a draft so that unverified content is not treated as authoritative. | Draft can be approved/rejected with actor/time/reason; author cannot self-approve high-risk content where separation policy applies; only approved content is retrievable. | US-013/US-014; review policy | 2 | P0 |
| US-016 | As a knowledge owner, I want to supersede or withdraw stale content so that AEGIS does not present it as current. | Status/version change is durable; old content is excluded from current ranking; affected chunks/cache invalidated; history is attributable. | US-015, TS-009 | 3 | P0 |
| US-017 | As a knowledge owner, I want to see missing or overdue metadata so that I can improve quality before users rely on the record. | Dashboard/report identifies missing owner/source/classification/review date, stale status, and unresolved relationships; drafts are not ranked as current. | US-013–US-016 | 2 | P1 |
| US-018 | As an authorized user, I want knowledge access to reflect source permissions so that retrieval cannot expose another audience's content. | Access filter is applied before text/chunks go to agent; tests include different scopes, revoked access, and cross-source results. | US-012, TS-010; ACL decision | 5 | P0 |
| US-019 | As a knowledge administrator, I want source deletion and ACL changes propagated so that removed or restricted knowledge stops appearing. | Change/deletion recorded; index and reconstructible cache invalidated within approved SLA; failed propagation is visible and retried safely. | US-012, US-016, TS-009/010 | 3 | P0 |
| US-020 | As a knowledge owner, I want to record relationships between departments, systems, resources and procedures so that AEGIS can answer multi-entity questions. | Relationship has type, source, effective dates and confidence; unknown/conflicting links are not silently inferred; each edge can be cited. | US-013, TS-008 | 3 | P1 |

### EPIC-005 — Knowledge retrieval

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-021 | As a user, I want exact identifiers and names searched so that I can find a server, share, printer, room or app directly. | Keyword search matches canonical IDs/names and approved aliases; inactive/deleted records are excluded by default; access filters apply. | US-013, US-018, TS-011 | 2 | P0 |
| US-022 | As a user, I want natural-language semantic search so that differently worded questions can find relevant approved guidance. | Semantic retrieval returns only authorized published content and includes source IDs; model/version metadata is recorded; no result is reported honestly. | US-014, US-018, TS-011 | 3 | P0 |
| US-023 | As a user, I want results ranked by source authority and freshness so that current authoritative records appear before informal or stale notes. | Ranking uses configured trust/status/recency and query relevance; stale/conflicting items are qualified or excluded per policy; copied sources are not treated as independent corroboration. | US-012, US-016, US-021/022 | 3 | P0 |
| US-024 | As a user, I want citations on organization-specific answers so that I can verify the source and version. | Results include accessible source title/reference/version/date; multi-hop responses preserve relevant relationship provenance; inaccessible source details are not disclosed. | US-020–US-023 | 2 | P0 |
| US-025 | As a knowledge administrator, I want embeddings tracked by model/version so that provider changes can be re-indexed in a controlled way. | Each embedding/index record identifies model/version and source version; re-index can be triggered without changing authoritative source records; failed run is visible. | US-014, TS-011 | 2 | P1 |
| US-026 | As a user, I want AEGIS to explain when evidence is missing or conflicts so that I know not to rely on a guess. | No-result, conflict, stale, and permission-denied outcomes are distinct; answer does not invent a fact or reveal restricted content; suggests an approved next step when known. | US-018, US-023, US-024 | 3 | P0 |

### EPIC-006 — Knowledge Agent

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-027 | As a user, I want my supported question routed to the Knowledge Agent so that AEGIS can answer from approved organizational evidence. | Dispatcher selects Knowledge Agent for supported knowledge requests; records run/agent; routing is deterministic/testable; LangGraph is not required. | US-007, US-022, TS-012 | 3 | P0 |
| US-028 | As a user, I want the Knowledge Agent to answer from retrieved context so that factual claims are grounded in permitted sources. | Agent receives only authorized/minimized context; cites supporting records; unsupported claims are qualified or omitted; retrieval policy is enforced outside model prompts. | US-018, US-024, US-027 | 5 | P0 |
| US-029 | As a security reviewer, I want prompt-injection content treated as untrusted data so that document instructions cannot override policy. | Adversarial tests show retrieved/user instructions cannot reveal other sources, change roles, or trigger tools; system policy and access checks are deterministic. | US-018, US-027/028 | 3 | P0 |
| US-030 | As a user, I want model/provider failure reported clearly so that a failed run is not mistaken for a reliable answer. | Timeout, quota, provider and malformed-output errors map to safe statuses; bounded retries; no success-shaped fallback; failure is observable and correlated. | US-027, TS-013 | 2 | P0 |

### EPIC-007 — Helpdesk Agent

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-031 | As a user, I want common supported IT requests routed to Helpdesk Agent so that I receive relevant first-line guidance. | Agreed intent set routes to Helpdesk; unsupported request is clearly identified; run and agent are persisted. | US-007, US-014, US-027, TS-012 | 3 | P0 |
| US-032 | As a user, I want a troubleshooting procedure recommended for my issue so that I can follow approved steps. | Procedure is current, audience-authorized and in scope; answer preserves prerequisites, ordered steps, stop conditions, and escalation; source is cited. | US-015, US-023/024, US-031 | 3 | P0 |
| US-033 | As a user, I want the Helpdesk Agent to ask for necessary non-sensitive context so that guidance is relevant without collecting secrets. | Required disambiguation is limited to approved fields; agent never requests passwords/tokens; sensitive values are not persisted unnecessarily. | US-031, security review | 2 | P0 |
| US-034 | As a support user, I want an explicit escalation route when self-service is insufficient so that the issue reaches the correct support group. | Route is sourced, current and visible to the user; high-risk/stop conditions escalate immediately; personal contact data is minimized. | US-020, US-032 | 2 | P0 |
| US-035 | As a service owner, I want read-only operations restricted to reviewed tools so that support lookups cannot exceed user or tool policy. | No tool outside allowlist executes; actor and resource permissions checked; operation and result summary audited; tool failure is explicit. | US-031, US-018, tool policy | 3 | P1 |

### EPIC-008 — Approval framework

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-036 | As an authorized requester, I want a consequential action saved as a pending approval so that no side effect occurs before review. | Exact action/target/parameters/requester/policy/expiry persist in PostgreSQL; no execution occurs at proposal; invalid/unclassified operation is disabled. | US-003, US-007, TS-014; approval policy | 3 | P0 |
| US-037 | As an approver, I want to review the exact proposed action so that I can make an informed decision. | UI/API shows canonical operation, target, material parameters, requester, risk, and expiry; only authorized approver sees decision controls. | US-036, US-004 | 3 | P0 |
| US-038 | As an authorized approver, I want to approve or reject a request with an attributable decision so that action authority is clear. | Decision actor/time/status/reason are durable and audited; self-approval denied by default; duplicate/conflicting decisions are prevented. | US-037, US-004, TS-014 | 3 | P0 |
| US-039 | As the system, I want rejected, expired, cancelled or revoked requests blocked so that stale consent cannot authorize execution. | All terminal states fail execution; expiry uses server time; cancellation/revocation is attributable; state transitions are atomic. | US-036–US-038 | 3 | P0 |
| US-040 | As an operator, I want execution to revalidate and consume approval atomically so that changed parameters or replay cannot cause an unauthorized action. | Execution loads stored action; checks digest/binding, expiry, requester and approver authority, policy and one-time state; test covers race/replay/parameter changes; failure is audited and closed. | US-038/039, tool execution decision | 5 | P0 |
| US-041 | As a service owner, I want ambiguous tool outcomes handled safely so that retries do not duplicate consequential changes. | Retry requires idempotency/reconciliation; ambiguous completion is not automatically retried; expired/changed approvals cannot be reused. | US-040, tool-specific policy | 3 | P0 |

### EPIC-009 — Audit framework

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-042 | As a security operator, I want authentication and authorization events logged so that access decisions can be investigated. | Events include actor/principal, result, time, reason category, resource reference and correlation ID; secrets/tokens are absent; denials are searchable by authorized roles. | US-002/004, TS-015 | 2 | P0 |
| US-043 | As an auditor, I want approval and tool activity recorded so that consequential operations are attributable end-to-end. | Request, decision, policy, execution attempt/outcome link by ID; records are durable and append-oriented; access is restricted. | US-036–US-040, TS-015 | 3 | P0 |
| US-044 | As an operations engineer, I want agent runs and knowledge-source use recorded so that failures and provenance can be diagnosed. | Run ID, agent, status, source identifiers, tool name, timing and outcome are available; prompts/secrets are not logged by default. | US-027/031, US-024, TS-015 | 2 | P0 |
| US-045 | As a security owner, I want audit retention and access controls configured so that records are protected and retained under approved policy. | Retention is set from approved decision; ordinary app users cannot alter audit history; failed durable audit write is observable and critical actions fail closed. | US-042–US-044; retention decision | 3 | P0 |

### EPIC-010 — Frontend experience

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-046 | As an authenticated user, I want a dashboard showing my conversations so that I can resume prior support work. | Displays only authorized records; loading, empty and error states work; list refresh reflects persisted state. | US-008, TS-016 | 2 | P0 |
| US-047 | As a user, I want to send a message and see run progress so that I know whether AEGIS is processing or has failed. | Submit prevents duplicate accidental sends; status transitions shown; explicit failure/unsupported/cancelled outcomes displayed. | US-007, US-009, TS-016 | 3 | P0 |
| US-048 | As a user, I want answers and citations shown together so that I can inspect evidence behind a response. | Citation link/title/version and accessible source details are rendered; hidden sources do not leak through UI metadata; no-result is clear. | US-024, US-028 | 2 | P0 |
| US-049 | As an approver, I want an approval inbox and decision view so that I can review eligible requests. | Pending requests are scoped to approver permission; exact action summary and expiry visible; approve/reject sends backend decision; outcome refreshes. | US-037/038 | 3 | P0 if consequential action enabled |
| US-050 | As a user, I want understandable authentication, validation and service errors so that I know what to do next. | API error envelope maps to safe UI messages; no stack traces/secrets shown; retry guidance does not imply failed action succeeded. | TS-016, US-030 | 2 | P0 |
| US-051 | As a user with accessibility needs, I want keyboard-operable and readable core workflows so that I can use AEGIS effectively. | Sign-in return, conversation list, chat, citations and approval review have labels, keyboard navigation, focus handling and contrast checks. | Frontend foundation | 2 | P1 |

### Cross-cutting user stories: administration and governance

| ID | User story | Acceptance criteria | Dependencies | SP | Priority |
|---|---|---|---|---:|---|
| US-052 | As a knowledge administrator, I want to see ingestion status and rejected records so that incomplete imports are not mistaken for current knowledge. | Last successful sync/manual import, counts, validation failures and stale state are visible; partial failure does not refresh full-source freshness. | US-012–019 | 2 | P1 |
| US-053 | As a platform administrator, I want to view health/readiness so that I can determine whether dependencies are available. | Liveness and readiness are distinct; readiness checks required dependencies without exposing secrets or internal details publicly. | TS-017 | 2 | P0 |
| US-054 | As a data owner, I want to apply an approved retention/deletion request so that data lifecycle obligations are respected. | Authorized deletion removes/de-indexes content and derived vectors/caches within approved policy; legal holds are respected; action is audited without preserving deleted content. | US-019, US-045; governance decision | 3 | P0 |
| US-055 | As a product owner, I want a curated evaluation set of environment questions so that release quality is measured against actual use cases. | Test set includes answerable, unanswerable, conflicting and access-restricted cases; expected sources and answer policy are reviewed by owners. | Knowledge workshops, US-024/026 | 2 | P0 |
| US-056 | As a security administrator, I want privileged actions separated from normal user access so that platform control is not implicitly granted by chat access. | Admin operations require server-side privileged permission; no admin role exposes secrets by default; all privileged changes are audited. | US-004, US-042 | 3 | P0 |
| US-057 | As a user, I want an explicit unsupported-request response so that I can redirect my request rather than trust an out-of-scope answer. | Unsupported intents are identified; no tool/action executes; response offers approved support route if known; run state is not successful. | US-027, US-031 | 2 | P0 |
| US-058 | As an operations owner, I want backup and restore evidence for durable AEGIS records so that service recovery can be demonstrated. | PostgreSQL backup/restore test includes conversations, approvals, audit, and knowledge metadata; vector rebuild/recovery expectations and RPO/RTO are documented. | TS-018; DR decisions | 3 | P0 |

**User-story minimum:** 58 stories. Sprint commitment depends on estimates, owner decisions, review lead time, and technical stories in Section 6.

## 5 Technical Stories

Technical stories implement cross-cutting foundations and quality attributes. They are tracked separately for visibility; do not double-count work if a user-story implementation already fully satisfies a technical acceptance criterion.

| ID | Purpose | Dependencies | Acceptance criteria | SP |
|---|---|---|---|---:|
| TS-001 | Establish repository layout, branch/change conventions, Python and frontend toolchains, formatting, lint, type-check, and test commands. | Repository access | New developer can install/run documented checks; module ownership and inward dependency direction documented; no secrets committed. | 3 |
| TS-002 | Create Docker local environment for API, React app, PostgreSQL/pgvector, Redis. | TS-001 | Documented startup and shutdown work; health checks available; data persists as intended locally; safe sample config only; no production credential defaults. | 3 |
| TS-003 | Implement FastAPI app lifecycle, API versioning, request validation, consistent error envelope, OpenAPI generation, and health endpoints. | TS-001 | Contract is versioned; validation errors are stable and safe; OpenAPI reflects routes; startup/shutdown and readiness are tested. | 3 |
| TS-004 | Add Entra validation, principal mapping and identity database migration. | TS-003; Entra decisions | Tests cover valid/invalid claims and unique issuer/subject; external identity maps to stable internal ID; no competing JWT. | 5 |
| TS-005 | Establish PostgreSQL migrations, repositories, transaction conventions, constraints and least-privilege application DB role. | TS-002/003 | Clean DB migrates; rollback/recovery path documented; app does not connect as superuser; integration tests run against PostgreSQL. | 5 |
| TS-006 | Define persistence models and repositories for conversations, messages, runs, events and ownership indexes. | TS-005 | Foreign keys/status constraints and owner query patterns exist; restart persistence and isolation integration tests pass. | 5 |
| TS-007 | Define knowledge data dictionary, source registry, metadata vocabulary, controlled values and access mapping contract. | TS-005; source owners | Schema has stable IDs, trust/status/version/provenance/classification/ACL/review fields; policy gaps explicitly assigned. | 3 |
| TS-008 | Implement manual knowledge import/entry validation and lifecycle transitions. | TS-007 | Invalid/missing mandatory metadata blocks publish; draft/approved/superseded/deleted states persist and audit; source/version references retained. | 5 |
| TS-009 | Implement chunking, embedding adapter, pgvector index, model/version tracking and re-index lifecycle. | TS-008; provider/embedding decision | Authorized content only is embedded; model version stored; re-index and deletion tested; failed indexing is visible. | 5 |
| TS-010 | Implement authorization-aware retrieval filters and permission-change invalidation. | TS-007/009; ACL decision | Visibility filters apply before candidate text reaches agent; cross-scope and revoked-access tests pass; cache never overrides access. | 5 |
| TS-011 | Implement keyword/vector/hybrid retrieval, metadata/trust ranking, citations and evaluation harness. | TS-009/010 | Exact identifiers and natural language tested; output carries provenance; ranking behavior documented; representative set yields measured baseline. | 5 |
| TS-012 | Define typed agent contracts, explicit application dispatcher and provider-neutral orchestration seam. | TS-003/006 | Knowledge and Helpdesk route is deterministic and unit tested; failure/cancellation states explicit; no LangGraph dependency/state. | 3 |
| TS-013 | Implement approved AI provider adapter with timeout, bounded retries, error mapping, usage/cost telemetry and data minimization. | TS-012; provider decision | Credentials server-side; provider failures explicit; prompts omit secrets; timeout/quota tests and usage events available. | 5 |
| TS-014 | Implement approval schema/state transitions, canonical action binding and execution gate. | TS-005/006; approver/tool policy | Durable exact-action binding; atomic one-time consume; expiry/replay/tampering/self-approval tests pass; side-effecting tools remain disabled until policy approval. | 8 |
| TS-015 | Implement structured request correlation, audit writer, redaction rules, audit access restrictions and event coverage. | TS-003/005; retention decision | Auth/denial/agent/knowledge/tool/approval events are durable; secrets and unnecessary content absent; critical write failure fails closed. | 5 |
| TS-016 | Create React/TypeScript build, typed API client, Entra sign-in plumbing and component/test conventions. | TS-001/003/004 | Frontend builds and checks pass; API types align with OpenAPI; tokens are not stored in unsafe custom persistence without approval; no secrets bundled. | 5 |
| TS-017 | Add health/readiness, structured operational logs, dependency status and baseline metrics/alerts. | TS-003/015 | Readiness reflects required dependencies; sensitive detail hidden; request correlation supports tracing; failure signals documented. | 3 |
| TS-018 | Configure PostgreSQL backup/restore, Docker image build/release, environment separation and runbooks. | TS-002/005/017; deployment and DR decisions | Restore test verifies key records; images build reproducibly; secrets come from approved injection; rollback and recovery steps reviewed. | 5 |
| TS-019 | Add CI workflow for unit/integration/e2e checks, frontend/backend lint/type checks and container build. | TS-001/002 | CI is repeatable; failure blocks release; test services are isolated; pipeline credentials are least privilege. | 5 |
| TS-020 | Add dependency, image and secret scanning with vulnerability handling guidance. | TS-019 | Scans run in CI; secrets finding blocks merge/release; critical/high findings have documented remediation or approved exception. | 3 |
| TS-021 | Build seed-data quality scoring, representative question set and retrieval/access regression suite. | TS-008/011; knowledge workshops | Evaluation set covers answerable/no-answer/conflict/restricted cases; metrics separate grounded answer from safe abstention. | 3 |
| TS-022 | Define operational configuration, managed secret store references, rotation ownership and environment-specific settings. | TS-001/002; deployment target | No secret committed or embedded in image; dev/test/prod separated; rotation and incident revocation owners documented. | 3 |

## 6 Sprint Breakdown

Six two-week sprints plus one stabilization week are the delivery shape requested by the ADR plan. The stories listed are candidate sprint contents; technical story IDs are included alongside related product stories. The total must be rebalanced after estimates and actual developer capacity are known. With part-time availability, retain the sprint goals but extend calendar duration rather than dropping P0 acceptance/security controls.

### Sprint 1 — Foundation and decisions

- **Goals:** Establish runnable local skeleton, CI baseline, data/security decisions, and initial architecture boundaries.
- **Candidate stories:** TS-001, TS-002, TS-003, TS-019 (initial pipeline); decision tasks for Entra, provider, source owner, classification, approver policy, retention, deployment and RPO/RTO.
- **Expected outputs:** FastAPI and React skeletons; PostgreSQL/pgvector and Redis containers; health baseline; CI checks; decision log with owners/dates; local setup documentation.
- **Risks:** Entra and hosting decisions delayed; toolchain or Docker issues consume capacity.
- **Exit criteria:** New developer starts stack from docs; lint/type/unit checks run; secrets absent; open blocking decisions have owners and due dates.

### Sprint 2 — Identity, authorization, and durable core

- **Goals:** Secure API boundary and persist user/conversation primitives.
- **Candidate stories:** TS-004, TS-005, TS-006 (initial models), US-001–US-004, US-006, US-011 (authorization test foundation), US-053.
- **Expected outputs:** Entra flow/token validation, internal principal mapping, initial role policy, migrations, conversation API skeleton, health/readiness.
- **Risks:** Identity app registration/scopes unavailable; role mapping unsettled; DB schema churn.
- **Exit criteria:** Valid/invalid token tests pass; unknown role denies; resource ownership approach demonstrated; clean migrations work.

### Sprint 3 — Conversation workflow and web shell

- **Goals:** Complete authenticated chat persistence and user-visible core shell.
- **Candidate stories:** US-007–US-010, US-046–US-047, US-050, TS-016, remaining TS-006.
- **Expected outputs:** Create/list/reopen conversations; messages/run records; typed API client; sign-in and chat shell; consistent statuses/errors.
- **Risks:** Frontend/API contract drift; ownership failures; persistence/retention decision delays.
- **Exit criteria:** Authenticated user can create a conversation, send a message through a stub dispatcher, reload history, and cannot access another user's content.

### Sprint 4 — Knowledge management and retrieval

- **Goals:** Curate initial seed and return access-filtered, cited evidence.
- **Candidate stories:** US-012–US-026, US-017–US-020; TS-007–TS-011, TS-021; US-048.
- **Expected outputs:** Source registry; manual ingestion and lifecycle; initial approved dataset; pgvector/keyword retrieval; visibility filters; citations; seed evaluation set.
- **Risks:** Initial source/ACL semantics unknown; content owners unavailable; embedding/provider approval delayed; poor seed quality.
- **Exit criteria:** At least one approved source and useful seed set retrieved with citations; access tests pass before content reaches agent; deletion/withdrawal test passes.

### Sprint 5 — Knowledge and Helpdesk agents; guarded operation foundation

- **Goals:** Deliver the two approved agents and safe procedure guidance.
- **Candidate stories:** US-027–US-035, US-055, TS-012, TS-013; approval/audit design tasks TS-014/015 may start with approved policy.
- **Expected outputs:** Explicit dispatcher; provider adapter; Knowledge Agent with grounded responses; Helpdesk intent/procedure set; unsupported/error behavior; evaluation results.
- **Risks:** Provider terms/cost; prompt injection; supported procedure set not approved; insufficient evaluation coverage.
- **Exit criteria:** Both agents route representative requests; factual answers cite allowed sources; unknown/failed cases abstain clearly; no unreviewed tool is callable.

### Sprint 6 — Approvals, complete frontend, integration hardening

- **Goals:** Complete MVP approval lifecycle, audit coverage, and user/approver flows.
- **Candidate stories:** US-036–US-045, US-049, US-051–US-052, US-054, US-056–US-058; finish TS-014/015/017.
- **Expected outputs:** Approval state machine/API/UI; durable audit; helpdesk and conversation UX complete; data deletion and admin/health surfaces; end-to-end suite.
- **Risks:** Approver roles/expiry/retry not approved; broad scope exceeds capacity; audit retention decision unresolved.
- **Exit criteria:** Approval exact-action, expiry, rejection, revocation, self-approval, replay and parameter-tampering tests pass; audit events correlate; app passes production-like end-to-end tests.

### Stabilization and release week

- **Goals:** Resolve release blockers, validate operational recovery, and make go/no-go decision.
- **Candidate work:** TS-018, TS-020, security acceptance checklist, penetration/security review where available, load/error testing, backup restore, deployment rehearsal, runbooks and known-limitations review.
- **Expected outputs:** Release candidate, test evidence, scan results, restore evidence, risk acceptance record, rollback plan, support/owner handoff.
- **Risks:** Discovery of access-control gaps, backups not restorable, unresolved high vulnerabilities, scope creep.
- **Exit criteria:** Section 12 checklist approved; no open critical/high release blocker without formally approved exception; rollback and restore proven; owners sign off.

### Capacity control

The 58 product stories estimate to **155 points** (P0: **137**, P1: **18**); technical stories are separately estimated at 95 points. Many technical criteria overlap with product-story implementation, so do **not** add these totals mechanically. During Sprint 1, identify overlap and establish a de-duplicated release forecast. The six-sprint target is aggressive even for a focused solo developer: P0 product scope alone averages about 23 points per sprint before any non-overlapping technical work. It requires tightly bounded integrations, prompt stakeholder decisions, and deferral of nonessential work. If the de-duplicated estimate exceeds calibrated capacity, re-baseline the calendar or split release scope—never waive P0 security or acceptance criteria.

For each sprint, plan no more than 70–80% of observed capacity to committed stories; reserve the remainder for stakeholder review, integration failures, security fixes, and documentation. If actual capacity is below 18 points per two-week sprint, reduce P1 scope and extend the roadmap. Part-time work should be planned in available effort, not assumed elapsed weeks.

## 7 Story Point Framework

Points estimate relative complexity, uncertainty, integration risk, and testing—not elapsed time or individual productivity.

| Points | Meaning | Example |
|---:|---|---|
| **1** | Trivial, well understood, low-risk, one narrow outcome. | Add a simple status field or a focused validation test. |
| **2** | Small change with clear acceptance and limited integration. | Conversation archive state or basic UI error state. |
| **3** | Moderate, several paths/tests, bounded uncertainty. | Entra principal mapping or source metadata lifecycle. |
| **5** | Significant cross-layer work or meaningful policy/integration complexity. | Authorization-aware retrieval or provider adapter. |
| **8** | Large, uncertain, multiple components, substantial security/testing needs. Split if possible. | Exact-action approval execution gate. |
| **13** | Too large or uncertain for a single sprint commitment. Must be decomposed before commitment. | End-to-end identity, knowledge and action framework as one item. |

Estimate as a team-of-one using a stable reference story and include implementation, tests, documentation, integration/debugging, and review evidence. Recalibrate after Sprint 1. If blocked by external decisions, track the dependency and do not inflate points to hide waiting time. Compare planned versus completed work to forecast capacity, not to judge performance.

## 8 Definition of Ready

A story may enter `Ready` only when:

- The user/business outcome is clear and in MVP scope; acceptance criteria are observable and testable.
- Dependencies are named by ID, available, or have a tracked owner/date; no hidden external approval is assumed.
- Required API/data behavior and relevant entity/source contracts are understood.
- Security considerations are recorded: identity, authorization, data classification, source ACLs, secrets, audit, prompt/tool exposure, and failure mode as applicable.
- Architecture is consistent with the accepted ADRs: modular monolith; FastAPI; React/TypeScript; PostgreSQL/pgvector; Redis ephemeral only; Entra; dispatcher; LangGraph deferred.
- Test strategy and required test data/source access are identified; test data is safe and does not contain production secrets or unnecessary personal data.
- For knowledge work, source owner, authority/trust level, permitted audience, provenance, lifecycle, and deletion/update behavior are known.
- For tool/approval work, operation tier, requester/approver roles, exact action fields, expiry, rejection, revocation, retry and audit policy are approved.
- Open decisions are either resolved or explicitly excluded from the story; assumptions are documented.
- Estimate is at most 8 points; 13-point work has been decomposed.

## 9 Definition of Done

A story can be closed only when:

- Implementation is complete, consistent with modular boundaries, and reviewed by an independent reviewer where available; for a solo developer, use a documented self-review checklist and request targeted peer/security review for high-risk changes.
- Unit/integration/UI tests cover acceptance criteria and relevant negative/error/authorization paths; no failing required test is waived silently.
- Lint, formatting, type checks, migrations, and build pass in CI.
- API contracts/OpenAPI, operational docs, user/knowledge owner docs, or decision records are updated where affected.
- Authentication/authorization and data visibility are enforced server-side and tested; browser/model output is not treated as a security authority.
- Errors are explicit and safe; failures do not return success-shaped fallbacks; relevant logs and audit events exist without tokens, secrets, or unnecessary sensitive payloads.
- Knowledge records have provenance, owner, classification/access decision, status, version, freshness and review metadata; unauthorized source content cannot reach the agent.
- Consequential operations cannot bypass a durable, current, exact-action approval; denied/rejected/expired/replayed actions are tested.
- Secret, dependency and container scans meet release policy or have a formally approved exception.
- Deployment/local setup is validated; where data persistence changes, migration and restart behavior are tested.
- Work item links implementation, tests, review evidence, known limitations, and follow-up tasks; status is set to `Done`.

## 10 Risk Backlog

Likelihood and impact are initial estimates. Risk owner is a role to assign, not a named person. Track each risk with status, due date, evidence, and residual-risk acceptance in the issue tracker.

| Risk ID | Risk | Probability | Impact | Mitigation / trigger | Owner |
|---|---|---|---|---|---|
| R-001 | Knowledge quality is too low, stale, or unowned for useful answers. | High | High | Manual seed; owner/source/review gates; quality scoring; overdue flags; representative query evaluation; no unsupported claims. Trigger: priority coverage or freshness below target. | Knowledge Owner / IT Operations Manager |
| R-002 | Entra registration, claims, audience, or group mapping is delayed or wrong. | Medium | High | Assign identity decision owner in Sprint 1; validate issuer/audience/claims early; fail closed; test role revocation. Trigger: unresolved config blocks Sprint 2. | Identity Administrator / Security |
| R-003 | Model/provider cost, quota, privacy terms, or availability are unacceptable. | Medium | High | Approve provider/data use; set quotas/budget alerts; minimize context; timeout/retry limits; explicit failure; evaluate cheaper/smaller approved option. | Product Owner / Security / Finance |
| R-004 | Retention, deletion, classification, or source ACL policy is undefined. | High | Very High | Gate production ingestion on owner/Security/Privacy decision; minimize data; define backup/provider retention and deletion SLA. Trigger: source cannot demonstrate permissions/deletion. | Data Owner / Security / Privacy |
| R-005 | Retrieval quality or latency is poor on actual organizational questions. | Medium | Medium/High | Build test set early; baseline keyword/vector/hybrid; tune after measurement; constrain context and indexes; document safe abstention. | Developer / Knowledge Owner |
| R-006 | Approval is forged, replayed, self-approved, stale, or bound to changed parameters. | Medium | Very High | Durable exact-action binding; atomic one-time consume; separate requester/approver; recheck permissions and expiry; adversarial tests; do not enable tools until accepted. | Security / Tool Owner |
| R-007 | Sensitive content leaks through knowledge retrieval, vectors, logs, or UI citations. | Medium | Very High | ACL filter before retrieval, field minimization, source-specific tests, log redaction, restricted metadata, cache invalidation and security review. | Security / Knowledge Owner |
| R-008 | Tool integration is broader or riskier than the approved user need. | Medium | High | Per-operation allowlist and tier; least-privilege identity; individual review; no broad Graph/PowerShell/network access in MVP; Tier 4 excluded. | Tool Owner / Security |
| R-009 | Solo developer capacity or external review availability misses six-sprint target. | High | High | Limit WIP; reserve capacity; prioritize P0 vertical slice; timebox decisions; extend calendar for part-time; defer P1 rather than remove gates. | Product Owner |
| R-010 | Provider/model output includes hallucination or prompt-injection instructions. | High | High | Trusted backend policy, context minimization, source filtering, structured outputs, adversarial evaluation, citations and safe abstention. | AI/Knowledge Owner / Security |
| R-011 | Database/cache outage or restore failure loses or misrepresents data. | Medium | High | PostgreSQL system of record, Redis optional only; backup/restore drills; readiness, alerts, reconciliation; fail closed for critical operations. | Platform Administrator |
| R-012 | External source updates/ACL revocations are not propagated promptly. | Medium | High | Source-specific freshness/deletion SLA; track sync watermark and failures; invalidate indexes/cache; manual fallback before connector automation. | Knowledge Administrator / Source Owner |

## 11 MVP Release Checklist

Every item must be checked with evidence or have a formally approved exception by the accountable owner. “Planned” is not “passed.”

| Category | Release check | Evidence / owner sign-off |
|---|---|---|
| **Architecture** | Single-organization modular monolith; FastAPI backend and React/TypeScript frontend; no tenant control plane; LangGraph not included. | Architecture review, dependency/module check |
| **Database** | PostgreSQL migrations, constraints, least-privilege credentials, durable conversation/run/approval/audit/knowledge records, restart test. | Migration and integration test results |
| **Authentication** | Entra registration/config approved; token issuer/audience/signature/expiry/claims validated; invalid/ID tokens rejected; logout behavior documented. | Identity owner sign-off and tests |
| **Authorization** | Backend role and object checks for conversations, knowledge, approvals, tools/admin; default deny; role mapping and access review approved. | Security tests and role matrix |
| **Knowledge** | Initial source owner, authority, ACL, classification, version, review/freshness, deletion behavior approved; seed is reviewed and traceable. | Owner sign-off, quality report |
| **Agents** | Only Knowledge and Helpdesk available; routing tested; provider terms/config approved; citation, no-answer, failure and prompt-injection cases pass. | Evaluation results |
| **Approvals** | Consequential operations classified; exact action binding, authorized approver, separation of duties, expiry/reject/revoke/retry defined; execution rechecks approval. | Policy sign-off and test evidence |
| **Audit** | Auth, authorization, agent, source, tool, approval and security events durable, correlated, access-controlled and retained under approved policy. | Audit coverage and access test |
| **Frontend** | Chat/history/activity/citations/errors work; approval UI only appears when applicable; UI does not enforce authorization; accessibility basics checked. | E2E and UX checks |
| **Operations** | Health/readiness, structured logs, correlation, alerting, cost/quota awareness and service owner/runbooks available. | Operational readiness review |
| **Documentation** | Setup, configuration, role/source governance, supported intents, limitations, retention, incident, backup/restore, deployment and rollback documented. | Documentation review |
| **Security** | TLS, at-rest encryption, managed secrets, secret scan, dependency/container scan, threat review, vulnerability disposition, no broad tools. | Security acceptance/sign-off |
| **Testing** | Unit/integration/e2e; authorization, retrieval, approval state transitions, error, restart, backup restore and representative query set pass. | CI and test report |
| **Deployment** | Production-like deployment rehearsal; environment configuration separated; secrets injected; migrations/rollback and recovery validated. | Deployment and DR rehearsal |

Release blockers include any cross-scope knowledge disclosure, invalid token acceptance, conversation ownership bypass, consequential execution without exact valid approval, missing durable audit for critical actions, unrecoverable required data, or unresolved critical vulnerability without approved exception.

## 12 Post-MVP Backlog

All items below are **Out of Scope for MVP**. Reassess after stable MVP contracts, measured demand, an accountable owner, and security/operational review. No future agent or connector should be exposed in MVP UI as available.

| Future item | Status | Entry criteria / notes |
|---|---|---|
| LangGraph orchestration | **Out of Scope for MVP; Phase 3 candidate** | Stable dispatcher/agent contracts and concrete need for branching, resumability, or multi-step workflows; parity tests for authorization, audit, errors, cancellation, and persistence. |
| Cybersecurity Agent | **Out of Scope for MVP** | Security team ownership, sensitive-data boundaries, approved sources, misuse testing, and explicit permitted actions. |
| Automation Agent | **Out of Scope for MVP** | Defined workflow use cases, tool tiers, approval policies, rollback/idempotency and operational support. |
| Developer Agent | **Out of Scope for MVP** | Separate developer use cases, repository/code access model, secret handling, and safe execution boundary. |
| Power Platform Agent | **Out of Scope for MVP** | Power Platform inventory governance, owner approval, environment ACLs, flow impact classification and connector review. |
| Teams Integration | **Out of Scope for MVP** | Explicit use cases and team-owner approval; preserve conversation ACLs; avoid broad transcript ingestion. |
| Microsoft Graph Integration | **Out of Scope for MVP unless a single approved source is explicitly selected** | Least-privilege scopes, consent, source ACL preservation, privacy/data minimization and deletion behavior. |
| N-able Integration | **Out of Scope for MVP** | Monitoring owner, scopes, data classification, freshness/error handling and vendor credential controls. |
| Voice Interface | **Out of Scope for MVP** | Accessibility/privacy review, identity continuity, transcription/retention policy, user testing and secure action confirmation. |
| Predictive Analytics | **Out of Scope for MVP** | Data quality/coverage baseline, bias/impact review, explainability, approved retention and measurable decision benefit. |

Other deferred candidates include multi-tenancy, broad PowerShell/Graph/SharePoint/Intune/network tool coverage, plugin marketplace, agent-to-agent messaging, workflow designer, enterprise reporting suite, and guaranteed real-time streaming.

## 13 Prioritized Build Order

This is the recommended sequence of implementation capabilities. Some foundations run in parallel, but dependencies and security gates take precedence. Audit event design starts with platform/identity work because later features need it; the full audit framework and completeness pass follows approval implementation. Approval policy and data model must be designed before any consequential tool, even if the approval UI is delivered later.

| Order | Work | Why this order |
|---:|---|---|
| 1 | **Repository Setup** | Establish repeatable conventions, quality checks, modular boundaries, and safe configuration before feature code accumulates. |
| 2 | **Docker** | Make API, frontend, PostgreSQL/pgvector, and Redis reproducible locally; expose integration issues early. |
| 3 | **FastAPI** | Create lifecycle, versioned API/error contracts, validation and health baseline. |
| 4 | **PostgreSQL** | Establish migrations and durable source of truth before conversations, knowledge, audit, or approvals. Redis remains optional and non-authoritative. |
| 5 | **Authentication** | Establish Entra validation, internal principal and authorization policy before storing user-owned data. |
| 6 | **Conversation Engine** | Deliver a secure vertical slice with owner-scoped durable conversations/messages/runs and clear statuses. |
| 7 | **Knowledge Base** | Define ownership/ACL/provenance/lifecycle and seed approved content manually before embedding/indexing. |
| 8 | **Knowledge Agent** | Use tested retrieval and citations to deliver organization-specific answers; provider is configured only after approval. |
| 9 | **Helpdesk Agent** | Reuse agent contracts and approved procedures; explicitly handle unsupported cases and escalation. |
| 10 | **Frontend** | Build complete chat/history/status/citation flows against stable API contracts; implement approval surfaces only for approved policies. A thin shell/sign-in may be developed earlier to validate the vertical slice. |
| 11 | **Approvals** | Implement exact-action workflow and execution gate before enabling any consequential operation. Policy design begins earlier; no action is enabled until lifecycle policy is approved. |
| 12 | **Audit** | Complete event coverage and retention/integrity verification across authentication, retrieval, agents, tools and approvals. Basic correlated audit primitives begin at Step 1/5/6. |
| 13 | **Hardening** | Perform threat/security tests, backup/restore, scanning, operational runbooks, deployment rehearsal, performance/failure testing and release sign-off. |

Redis integration, CI and security scans are foundational/cross-cutting; implement the minimal reliable form in Step 1–3 and complete them during hardening. Do not wait until the end to discover secrets, logging, or dependency problems.

## 14 Solo Developer Roadmap

### Timeline ranges

These are planning ranges, not commitments. They assume the MVP remains bounded to two agents, one initial approved knowledge source or manual seed path, no broad external tool integrations, and timely decisions/reviews.

| Scenario | Assumption | Estimated elapsed time |
|---|---|---|
| **Best case** | Near full-time focus (30–35 hours/week), Entra/provider/deployment decisions ready, source owners responsive, limited scope and no major rework. | 14–18 weeks including stabilization; six two-week sprints are an aggressive target and require early scope confirmation. |
| **Expected** | Part-time focus (15–20 hours/week), the six-sprint sequence takes longer in calendar time; moderate stakeholder wait and iteration. | 6–9 months including stabilization and release review. |
| **Conservative** | 8–12 hours/week, delayed identity/security/source decisions, significant knowledge cleanup or integration rework. | 9–15 months; prioritize the secured vertical slice and defer P1 items. |

Calendar estimates should be recalculated after Sprint 1 using actual completed points and blocking time. The sprint table is a six-sprint delivery sequence; it is not evidence that the full backlog fits into twelve calendar weeks. If the refined P0 forecast exceeds capacity, maintain milestone order and add sprint cycles rather than compromising controls.

### Critical path

1. Entra app registration, API audience/scopes, role mapping and test tenant.
2. PostgreSQL schema/migrations and authorization-safe internal principal/conversation model.
3. Initial source owner, classification, access-control semantics, and approved seed data.
4. Provider/model and data-handling approval; embedding and answer-generation configuration.
5. Access-filtered retrieval with citations and representative evaluation.
6. Approved support intent/procedure set for Helpdesk Agent.
7. Approver roles, action classification, expiry/rejection/revocation/retry policy before any consequential tool.
8. Deployment target, secret store, backup/restore objectives, retention and incident owner before release.

### Potential blockers

- No timely Entra application registration, scopes, test account or group/role mapping.
- Knowledge sources have no accountable owner, reliable ACL metadata, or current system-of-record data.
- Provider contract/data-handling approval or budget/quota is unresolved.
- Data retention, deletion, classification, legal hold, or audit retention is not decided.
- Approval policy and separation of duties are undefined while a side-effecting tool is expected.
- Deployment environment, secret store, monitoring, or recovery objectives are unavailable.
- Solo developer has no independent security/code reviewer for high-risk changes; arrange targeted review before production.

### Quick wins

- Build Docker Compose and CI immediately to reduce repeated setup/debug time.
- Create an approved source register and a 20–30-question evaluation set before large-scale ingestion.
- Manually curate the top 8–12 support procedures and high-use ownership/SharePoint records.
- Implement stable API errors, request correlation, and health/readiness early.
- Test cross-user conversation and source ACL boundaries before populating broad data.
- Keep external tools disabled initially; implement and test the approval framework against a safe stub rather than delaying release for broad automation.

### Progress and milestone control

At each sprint boundary, update story status, estimate, dependency, decision owner, acceptance evidence, and risk state. Review delivered behavior with IT support and knowledge owners. Re-plan when:

- Actual capacity differs from the 18–22 point near-full-time starting assumption by more than 20%, or the part-time calendar forecast changes materially.
- Any P0 dependency is blocked for more than five working days.
- Knowledge access, approval, or audit acceptance tests fail.
- A new provider, connector, agent, or consequential tool is proposed.

Defer P1 scope or extend the calendar; never silently weaken authentication, authorization, source visibility, approval, audit, recovery, or release acceptance to preserve a date.
