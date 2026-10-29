# AEGIS MVP Functional Specification

**Status:** Draft for product and engineering review  
**Version:** MVP / pre-1.0  
**Audience:** Product, engineering, security, and IT operations  
**Source of truth:** Approved AEGIS Architecture Decision Records (ADRs)

## 1 Executive Summary

### What AEGIS is

AEGIS (Adaptive Enhanced General Intelligence System) is an internal, AI-powered IT Operations Assistant for one organization. The MVP provides an authenticated web experience in which employees can ask supported IT questions and receive answers from two narrowly scoped capabilities:

- **Knowledge Agent:** finds relevant information in approved, access-controlled knowledge sources and returns an answer with source references.
- **Helpdesk Agent:** handles supported IT support questions and approved helpdesk workflows.

The application presents those capabilities through conversations. It uses a FastAPI backend, a React and TypeScript frontend, PostgreSQL with pgvector for durable application data and knowledge retrieval, Redis for optional ephemeral caching and coordination, and Microsoft Entra ID for authentication. Agent routing is implemented by an explicit application-level dispatcher; LangGraph is not part of the MVP.

AEGIS may perform read-only operations when the user and tool policy permit them. A consequential operation must not execute until an authorized approver has approved the exact proposed action. The MVP may deliver the approval workflow without enabling high-impact or broad tool integrations.

### MVP objectives

Before version 1.0, AEGIS must:

1. Let a user authenticate through Microsoft Entra ID and use the application under server-enforced authorization.
2. Let that user create and revisit durable conversations, submit messages, and see run/activity status and useful outcomes.
3. Route supported requests to the Knowledge Agent or Helpdesk Agent and return traceable results.
4. Retrieve only knowledge the current user is permitted to see, and show provenance for retrieved knowledge.
5. Give explicit, useful outcomes for unsupported requests, provider failures, and other unsuccessful runs rather than presenting them as successful answers.
6. Prevent any enabled consequential action from executing without a valid approval bound to the exact action and revalidated at execution time.
7. Preserve conversation, run, approval, and audit records across application restarts.
8. Provide the tests, operational health signals, and local setup needed to verify and run the MVP reliably without committing credentials to the repository.

### Expected business value

- **Faster access to IT knowledge:** Users can ask questions conversationally and receive answers grounded in approved sources, with references that help them verify the response.
- **More consistent first-line helpdesk support:** The Helpdesk Agent can answer supported questions and guide approved workflows through a common interface.
- **Safer use of automation:** Approval gates, authorization checks, and audit records establish human oversight before consequential changes.
- **Lower initial delivery and operating complexity:** A single-organization modular monolith and two agents focus delivery on useful MVP outcomes instead of premature multi-tenant infrastructure, service decomposition, or broad automation.
- **A path to measured expansion:** Typed agent contracts and a replaceable dispatcher allow later capabilities to be considered without making deferred agents or LangGraph part of the MVP commitment.

## 2 Product Scope

The MVP is the smallest production-oriented release that satisfies the objectives above. Scope is limited to one organization, the two approved agents, and individually reviewed capabilities. Inclusion in this specification does not imply that an external integration or consequential tool is enabled; such tools require their own authorization, safety, and operational review.

### In Scope

| Capability | MVP behavior | Why it is included |
|---|---|---|
| Single-organization access | Operate for one organization. Authenticate users and authorize access to their conversations, permitted knowledge, and permitted actions. Do not add tenant routing or a tenant administration control plane. | This is the approved deployment boundary; user- and resource-level authorization is still required. |
| Microsoft Entra ID sign-in | The web client obtains an API access token through the approved Entra flow. The API validates token signature, issuer, audience, expiry, and required claims, then maps the identity to an internal user principal. Enforce authorization in the backend, not in the browser. | Provides organization-aligned authentication and a consistent server-side security boundary. |
| Conversation and message workflow | An authenticated user can create a conversation, submit messages, and revisit conversation history. Enforce conversation ownership on reads and writes. Persist conversation and message records in PostgreSQL. | Conversations are the primary user interaction and must remain available after restarts. |
| Agent dispatch and run visibility | Route each supported request to the Knowledge Agent or Helpdesk Agent through an explicit application-level dispatcher. Record the selected agent, run status, and traceable run/activity information. Return an explicit outcome when a request is unsupported or a run fails. | Makes the two approved capabilities usable while keeping orchestration simple, testable, and replaceable. |
| Knowledge Agent | Search approved knowledge sources using PostgreSQL and pgvector. Apply the user's source visibility permissions before results are returned or used. Provide source references with answers so the UI can show provenance. | Delivers the MVP's grounded knowledge-answering capability while preserving access boundaries. |
| Helpdesk Agent | Handle the set of supported IT support questions and approved workflows established for the MVP. Use only individually reviewed and authorized operations. Clearly report when a request is unsupported or cannot be completed. | Delivers a focused helpdesk capability without promising general IT automation. |
| Read-only operations | Permit a read-only tool operation only when that operation has been reviewed and the current user is authorized under tool policy. | Read-only access is allowed by the ADR but is not an unrestricted permission to access external systems. |
| Approval workflow | Represent a consequential operation as an approval request. Show the proposed action to an authorized approver, capture an attributable decision, and execute only after approval is validated against the exact action and current permissions. Persist approval and audit records. The MVP may provide these records and review flow without enabling high-impact actions. | Human approval is a core safety requirement for side effects; durable records support accountability and recovery. |
| Basic operational web UI | Provide chat, conversation history, run/activity status, and approval review when approval execution is enabled. Show knowledge references and explicit error or unsupported-request outcomes where applicable. | Exposes the MVP capabilities and their status without presenting deferred agents as available. |
| Durable data and vector retrieval | Use PostgreSQL as the system of record for application and operational records, and pgvector for knowledge similarity retrieval. Use migrations and define backup/restore procedures. Persist embedding model/version metadata for controlled re-indexing. | Durable persistence and traceable retrieval are required for reliable conversations, approvals, and knowledge answers. |
| Redis for optional ephemeral needs | Use Redis only for reconstructible cache entries, rate limits, or short-lived coordination where needed. Define TTLs and invalidation. The application remains correct if cached data expires or Redis is unavailable, except for any explicitly documented coordination feature. | Provides a bounded performance/coordination option without making Redis authoritative. |
| Operational readiness | Provide structured logs, health/readiness endpoints, request correlation, explicit error handling, and audit events for authentication-sensitive and tool/approval events. Include tests for authorization, routing, retrieval filtering, approval transitions, and error behavior. | These are necessary to operate, diagnose, and verify an internal system that handles identity, knowledge, and actions. |
| Developer and delivery baseline | Provide Docker-based local development and CI workflows for tests, checks, and container builds. Document setup so a developer can start the local stack without repository-embedded credentials. | Enables repeatable development and release verification while keeping credentials out of source control. |

#### User interaction flows

1. **Sign in and start a conversation:** The user signs in with Entra ID, opens the chat, creates a conversation, and submits an IT question. The API validates the access token and checks the user's authorization.
2. **Receive a knowledge answer:** The dispatcher selects the Knowledge Agent for a supported knowledge request. The agent retrieves only sources visible to the user, produces an answer with references, and the UI presents the answer and provenance. If suitable accessible knowledge is unavailable or retrieval fails, the system reports that outcome explicitly rather than implying it found an answer.
3. **Receive helpdesk support:** The dispatcher selects the Helpdesk Agent for a supported IT support request. The user sees the response and run/activity outcome. Unsupported requests and failed runs are clearly identified.
4. **Review a consequential action:** If a supported workflow proposes a consequential action, the system records the exact proposed parameters and creates an approval request. An authorized approver can review and decide on that request. The system revalidates the approval, permissions, and action parameters immediately before execution. Without a valid matching approval, the action does not execute.
5. **Return to prior work:** The user can revisit their persisted conversations. Authorization is checked on every request; a UI-hidden item is not considered protected unless the API also denies access.

The MVP does not require guaranteed real-time token streaming. The UI must provide a clear run/activity status and final outcome; streaming is included only if product discovery validates it as critical and it is separately agreed.

### Out of Scope

| Capability | MVP boundary | Why it is excluded |
|---|---|---|
| Multi-tenant product capabilities | No tenant identifiers, tenant routing, tenant administration, or tenant-specific control plane. | The approved deployment serves one organization; multi-tenancy would add complexity without an MVP requirement. |
| Agents beyond Knowledge and Helpdesk | Do not implement or present other agents as available in the MVP UI. | The ADR limits MVP scope to two agents to reduce delivery complexity and focus evaluation. |
| LangGraph orchestration | Do not use LangGraph in the MVP foundation or initial agent implementations. | It is explicitly deferred to Phase 3; the MVP uses a testable dispatcher and agent interfaces. |
| Unreviewed autonomous consequential actions | No consequential action executes without authorized approval of the exact proposed action. | Autonomous side effects are prohibited by the approved safety decision. |
| Broad external tool coverage | No blanket integration commitment for PowerShell, Microsoft Graph, SharePoint, Intune, N-able, or arbitrary network operations. An individual operation may be added only after review, authorization, and applicable approval controls. | Broad tool coverage increases security and operational risk and is not required to deliver the two MVP agents. |
| Workflow designer, agent-to-agent messaging, and plugin marketplace | No self-service workflow construction, autonomous agent collaboration, or third-party plugin marketplace. | These are generalized extensibility features beyond the focused MVP user journeys. |
| Enterprise reporting and advanced analytics | No reporting suite or generalized analytics product. Operational logs, health signals, audit records, and basic run/activity status remain in scope. | Product analytics are not necessary to meet MVP user needs; operational observability and auditability are. |
| Guaranteed real-time streaming | Do not promise streaming as a release requirement. | The ADR defers it unless discovery confirms it is product-critical; reliable status and final outcomes are sufficient baseline behavior. |
| Redis as a system of record | Do not store authoritative conversation, approval, or audit records only in Redis. | PostgreSQL is the approved durable source of truth; cache loss must not lose business records. |
| Premature service decomposition | Do not split the backend into independently deployed services for the MVP. | The modular monolith is the approved architecture and reduces early deployment and operational overhead. |

### MVP release boundary and acceptance

Version 1.0 is ready for release only when the following conditions are met:

1. A user with a valid Entra access token can create a conversation and submit a message; invalid tokens are rejected.
2. The system routes supported requests to the Knowledge or Helpdesk capability and returns a traceable result.
3. Knowledge retrieval enforces source visibility before returning results and provides references suitable for display in the UI.
4. Unsupported or failed requests return explicit, useful outcomes and are not represented as successful answers.
5. No enabled consequential action executes without a valid approval for the exact proposed action; execution rechecks approval and permissions.
6. Conversation, run, approval, and audit records survive application restarts.
7. Automated tests cover authorization boundaries, agent routing, retrieval filtering, approval state transitions, and error behavior.
8. The local development stack can be started using documented instructions without credentials embedded in the repository.
9. Health/readiness, structured logs, and audit events needed for operational diagnosis are available.

### Decisions required before enabling affected functionality

The ADRs approve the architecture and boundaries but leave several implementation policies open. These must be resolved before the affected capability is enabled; they must not be silently inferred from this specification:

- **Identity and authorization:** Entra application registrations and audiences, group/role mapping, and local development sign-in.
- **Knowledge access:** Initial approved knowledge source, source ownership, access-control semantics, ingestion/update schedule, and deletion propagation.
- **Consequential actions:** Definition of consequential operations, eligible approver roles, separation-of-duties rules, approval expiry, rejection/cancellation behavior, escalation, and retry policy. Do not enable a side-effecting tool until its lifecycle and policy are defined.
- **Model operations:** Provider choice per environment, deployment configuration, data-handling constraints, quotas, budget alerts, and fallback policy.
- **Data governance:** Conversation and audit retention, sensitive-data handling, and applicable export/deletion requirements.
- **Deployment and recovery:** Container runtime, managed database/cache, secret store, monitoring stack, and disaster-recovery objectives.
- **Asynchronous execution:** Whether SSE or a separate worker/queue is required. Add queue infrastructure only when an identified workload or reliability need justifies it.
