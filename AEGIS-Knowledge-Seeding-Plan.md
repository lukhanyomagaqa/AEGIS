# AEGIS Knowledge Seeding Plan

**Status:** Proposed MVP onboarding plan  
**Version:** MVP / pre-1.0  
**Audience:** Engineering, IT operations, service desk, operations managers, knowledge owners, and future AEGIS agents  
**Scope:** Initial single-organization AEGIS deployment  
**Basis:** Approved AEGIS ADRs, MVP Functional Specification, Security Model, and Environment Knowledge Model

> **Planning note:** Counts, effort ranges, priority scores, and service examples are initial planning estimates, not an inventory of actual organizational systems. Validate them with source owners. Do not invent missing records or ingest a source just to meet a target. The ADRs approve PostgreSQL/pgvector and the Knowledge and Helpdesk Agents; they do not approve broad integrations or imply that particular sources are already available.

## 1 Executive Summary

### What knowledge seeding is

Knowledge seeding is the deliberate collection, validation, organization, and publication of a small, high-value body of organization-specific operational knowledge so AEGIS can answer useful questions from its first releases. Seeding includes the source and ownership metadata, access scope, review status, relationships, and citations needed to make each fact safe and trustworthy—not just copying text into a search index.

Knowledge seeding is critical because a general AI model does not inherently know which local server hosts a file share, which procedure the service desk approves, who owns a system, or which room has meeting equipment. The Knowledge Agent can retrieve and explain evidence, but it cannot manufacture reliable organizational facts. Helpdesk support likewise depends on current procedures, escalation paths, and support boundaries.

### Architecture versus organizational knowledge

- **Architecture** describes how AEGIS is built and operated: the approved single-organization modular monolith, FastAPI, React/TypeScript, PostgreSQL with pgvector, Redis for ephemeral uses, Entra ID authentication, and approval-based action execution.
- **Organizational knowledge** describes the environment AEGIS helps users understand: services, owners, file shares, devices, applications, procedures, source records, locations, and their relationships.

Architecture provides the means to protect and retrieve knowledge; it is not the knowledge itself. The MVP's Knowledge Agent and Helpdesk Agent use approved sources, apply source visibility before retrieval, and return traceable answers. Redis is not a system of record. LangGraph and broad tool integrations are not required for initial seeding.

Knowledge quality is more important than knowledge quantity. A short set of current, owned, access-controlled procedures is more useful and safer than thousands of stale or unreviewed files. Stale facts can misroute support, expose sensitive infrastructure, or lead to unsafe actions. AEGIS must say when it cannot verify an answer instead of filling gaps with model guesses.

**Success means AEGIS can answer organization-specific operational questions using current, authorized, attributable organizational evidence—and can disclose uncertainty when that evidence is absent, restricted, stale, or conflicting.**

## 2 Knowledge Seeding Strategy

### Guiding principles

1. **Start with high-value operational knowledge.** Seed facts that directly resolve frequent support and environment questions.
2. **Prioritize frequency and time saved.** Use service desk experience, common requests, and user research to validate the initial queue.
3. **Prefer trusted sources over large volumes.** Use systems of record and approved documentation first; label informal evidence as unverified.
4. **Focus on support efficiency first.** Help users identify the correct service, owner, procedure, location, and escalation route.
5. **Start manually before automating ingestion.** Validate fields, permissions, source ownership, and retrieval usefulness with a controlled set before building connectors.
6. **Preserve provenance and access rules.** Every published fact has an owner/source, lifecycle state, classification, audience, and review date; enforce access before retrieval.
7. **Link facts instead of duplicating them.** Prefer a relationship to the authoritative entity over competing copies of the same ownership or configuration fact.
8. **Separate fact from inference.** Explicitly distinguish source-recorded facts, technician observations, and model-generated explanations.
9. **Make uncertainty useful.** Surface missing/conflicting/stale information with an owner or next step; do not make unsupported confident claims.
10. **Treat action guidance conservatively.** Procedures include scope, prerequisites, stop conditions, and escalation. Consequential actions remain subject to the Security Model's approval controls.

### Seed immediately

- Identity and ownership references for the AEGIS knowledge sources themselves: source owner, permitted audience, classification, update/review cadence, and escalation contact.
- The most common approved support procedures for network drives, printers, Microsoft 365 sign-in, VPN/Wi-Fi, Teams, device setup, and boardroom support—only after service owners approve them.
- A small, prioritized service register: applications, owning departments, support groups, critical dependencies, and canonical support links.
- High-value environment lookups needed for support: file-share-to-host references, printer-to-location/department relationships, and boardroom equipment summaries. Exact IPs, host/network details, and restricted paths require classification and field-level access decisions.
- Current SharePoint knowledge locations and their owners, audience, and source-of-truth status; initially record metadata and links rather than ingesting all site content.
- Escalation routes, supported service boundaries, and “stop and escalate” criteria.
- A representative question set drawn from real, sanitized support questions to measure usefulness and retrieval quality.

### Delay until justified

- Broad mailbox and Teams chat ingestion; these contain personal, sensitive, informal, and frequently non-authoritative content.
- Historical ticket narratives and large historical documentation archives. Start with metadata and reviewed resolution patterns, not raw case dumps.
- Automated Graph, Intune, N-able, ticketing, Power Platform, and arbitrary database synchronization. These are future integration candidates, each requiring owner, security, access, and deletion review.
- Complete network topology, detailed configuration, user-level inventories, security-sensitive procedures, and secrets. Collect only approved operational fields and restrict visibility.
- Rarely used business processes, duplicate or unowned content, deprecated services, and records with no clear source or review path.
- Automated actions or broad integrations. Knowledge discovery does not authorize tool execution; consequential actions still require approval.

## 3 Phase-Based Seeding Roadmap

Effort is estimated as focused solo-developer effort plus owner/reviewer participation, not calendar duration. Confirm availability of source owners before committing dates. Phases can overlap when ownership and access decisions are resolved, but publication gates remain.

| Phase | Objectives | Initial sources | Estimated effort | Expected business value |
|---|---|---|---:|---|
| **Phase 1 — Foundational Operational Knowledge** | Establish data dictionary, source register, ownership and permission model; seed canonical departments, support groups, locations, core SharePoint knowledge sites, common service routes, and a small set of approved high-frequency support procedures. Create the initial representative query set. | Approved service catalogue, organizational directory, IT knowledge site, reviewed SOPs, service desk lead input. Primarily manual curation. | 5–10 developer days plus 3–6 stakeholder days. | Gives AEGIS safe, sourced answers to basic “who owns/supports this?” and first-line troubleshooting questions; tests the complete knowledge lifecycle. |
| **Phase 2 — IT Operations Knowledge** | Add high-value file shares, servers/hosting references, printers, endpoint/device standards, support dependencies, ticket categories, and escalation routes. Classify sensitive fields and test visibility. | Authoritative asset/service registers, infrastructure records, support procedures, technician workshops. Manual import or approved extracts. | 8–15 developer days plus 5–10 owner/reviewer days. | Reduces time spent locating infrastructure/resource facts and routing common support cases. |
| **Phase 3 — Business Systems Knowledge** | Establish application/service catalogue coverage, business and technical owners, dependencies, approved access route, criticality and support procedures. Include Power Apps where owners can validate purpose and connections. | Application register, application owners, department workshops, approved Power Platform register. | 8–15 developer days plus 6–12 owner/reviewer days. | Lets users and support staff answer which system serves a process, who supports it, and how to get help. |
| **Phase 4 — Process and Automation Knowledge** | Curate approved SOPs, incident and change process references, selected Power Automate flows, boardroom procedures, and reviewed ticket-resolution patterns. Clearly mark any operation that could cause a side effect. | Process owners, approved knowledge libraries, sanitized ticket metadata, Power Platform inventory, facilities records. | 10–20 developer days plus 8–15 owner/reviewer days. | Improves consistent handling and escalation; helps AEGIS recommend relevant procedures without enabling autonomous changes. |
| **Phase 5 — Advanced Organizational Knowledge** | Expand to broader approved sources and cross-domain relationships; evaluate automated sync, freshness alerts, knowledge quality reporting, and additional domains such as security or supplier services. | Approved Graph/SharePoint, Intune, N-able, ticketing, asset, security, and business systems integrations. | Discovery 5–10 days per source; implementation commonly 10–30+ days per connector, plus security and owner participation. | Enables fresher, wider environment intelligence at sustainable scale, subject to measurable value and approved source controls. |

Phase completion is based on approved coverage, access correctness, provenance, and retrieval evaluation—not on importing a fixed volume.

## 4 Priority Matrix

### Scoring definitions

The 1–5 scores below are provisional hypotheses for a typical internal IT environment and must be validated with local demand and owner interviews.

- **Business Value (BV):** 1 low, 5 very high operational/user value.
- **Maintenance Cost (MC):** 1 low, 5 very high ongoing effort. Lower is preferable.
- **Complexity (CX):** 1 straightforward, 5 very complex to collect, govern, or interpret. Lower is preferable.
- **Ease of Collection (EC):** 1 difficult, 5 readily available with an owner/source. Higher is preferable.
- **Frequency of Use (FU):** 1 rare, 5 very frequent.

Proposed priority score, range 1–5:

`Priority = (0.30 × BV) + (0.25 × FU) + (0.15 × EC) + (0.15 × (6 − MC)) + (0.15 × (6 − CX))`

Higher scores are earlier candidates. Security/access approval and owner availability are hard gates regardless of score. A score does not authorize ingestion.

| Rank | Knowledge source / topic | BV | MC | CX | EC | FU | Priority | Rationale / initial treatment |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Support Procedures | 5 | 2 | 2 | 4 | 5 | 4.55 | Directly resolves frequent support issues; start with owner-approved procedures and clear stop conditions. |
| 2 | Departments | 4 | 1 | 1 | 4 | 4 | 4.30 | Low-cost foundation for ownership and routing; validate current organization structure. |
| 3 | Escalation Paths | 5 | 2 | 2 | 4 | 4 | 4.30 | Quickly routes unresolved or high-risk issues; use group/role references rather than personal contact lists. |
| 4 | Knowledge Articles | 5 | 3 | 2 | 3 | 5 | 4.25 | High-frequency self-service content; curate current approved material, not volume. |
| 5 | Applications | 5 | 3 | 3 | 3 | 5 | 4.10 | High-value ownership and support lookup; begin with top user-facing services. |
| 6 | SharePoint Sites | 4 | 2 | 2 | 4 | 4 | 4.00 | Enables discovery of canonical knowledge locations; begin with site metadata and ACL/owner review. |
| 7 | Ticket Categories | 4 | 2 | 2 | 4 | 3 | 3.75 | Improves routing and normalizes support intent; confirm category taxonomy and assigned groups. |
| 8 | Printers | 3 | 2 | 2 | 4 | 4 | 3.70 | Repetitive support and location questions; manageable if an asset source exists. |
| 9 | File Shares | 4 | 3 | 3 | 3 | 4 | 3.55 | Useful “where hosted/who owns” lookups; restrict paths/IPs and avoid file-content ingestion by default. |
| 10 | Asset Registers | 4 | 3 | 3 | 3 | 3 | 3.30 | Potentially authoritative but often needs reconciliation and personal-data filtering. |
| 11 | Boardrooms | 3 | 2 | 2 | 3 | 3 | 3.30 | Useful for meeting support; seed location/equipment and procedures before configuration details. |
| 12 | Power Apps | 4 | 3 | 3 | 3 | 3 | 3.30 | Valuable process/application lookup; owner and dependency information may be incomplete. |
| 13 | SOPs | 4 | 3 | 3 | 3 | 3 | 3.30 | Important for consistent operations; publish only current, approved versions. |
| 14 | Servers | 4 | 4 | 4 | 3 | 3 | 3.00 | Valuable for IT operators; higher sensitivity and maintenance, so restrict details and audiences. |
| 15 | Historical Tickets | 3 | 4 | 4 | 3 | 4 | 2.95 | Can reveal repeated resolutions but requires privacy filtering and validation before promotion. |
| 16 | Teams Conversations | 2 | 5 | 5 | 2 | 4 | 2.20 | Informal, access-sensitive, difficult to govern; curate approved outcomes rather than ingesting conversations. |
| 17 | Email Archives | 2 | 5 | 5 | 1 | 3 | 1.80 | High privacy and noise risk; do not bulk ingest for MVP. Promote verified durable facts through approved channels. |

## 5 Environment Knowledge to Seed First

Start with a small, owner-verified record set. Use the Environment Knowledge Model's stable IDs, controlled statuses, provenance, relationships, classification, and review dates. Capture exact IP addresses only when operationally necessary, authorized, and classified; restrict them to a support audience and do not expose them in general user answers.

### File Servers and file shares

Model the server and each logical share separately so that “which server hosts this share?” is an explicit, sourced relationship.

| Field | Requirement |
|---|---|
| Server name | Canonical hostname and stable source identifier. |
| IP address | Optional restricted field; capture only if needed for support, with approved classification and authorized audience. Do not include in user-facing content by default. |
| Purpose | Business/technical role and environment. |
| Shares | Separate share name/identifier, purpose, source reference, and hosting relationship; avoid indexing file contents unless separately approved. |
| Ownership | Business owner department, technical owner role/group, and support group. |
| Dependencies | Storage service, network segment, DNS/DHCP/network service, application, or supplier references as permitted. |
| Common issues | Approved symptoms, known error category, linked procedure, last verified date; do not treat unreviewed ticket notes as authoritative. |
| Provenance and lifecycle | Source record, classification, ACL, status, last verified, review date, version. |

### Printers

Capture printer name, stable asset/source ID, model, physical location, department served (distinct from asset owner), optional restricted IP/network reference, operational status, support group, common approved support issues, linked procedure, source, classification, and last inventory/review date.

### Applications

Capture canonical application name/ID, purpose, business owner, technical owner, department, support group, authentication method at a high level (for example, Entra SSO or managed account—never credentials), dependencies, hosting or supplier reference, data classification, lifecycle state, user audience where permitted, support procedure, source, and review date.

### Departments

Capture canonical name/ID, aliases, manager role or approved service-owner reference, parent department where applicable, applications owned versus applications used, shared resources, support routes, source, effective dates, and visibility. Do not copy personal contact information or employee data without an approved need.

### Boardrooms

Capture room name/ID, building/floor/location, capacity and accessibility information where approved, equipment/asset relationships, video-conferencing platform, booking reference, support group, setup/troubleshooting procedure, source, classification, and last verified date. Exclude credentials and device administration secrets.

### SharePoint Sites

Capture site name/ID, canonical link, owner department and owner group, purpose, classification, source-of-truth designation, audience/ACL reference, review date, status, and linked Power Apps or Knowledge Articles. Preserve item-level access where it differs from site-level access.

### Power Apps

Capture app name/ID, purpose, business process supported, business and technical owners, environment, audience/security group reference, lifecycle status, support route, connected SharePoint/Dataverse sources, related flows, classification, source, and review date. Never store connection credentials, tokens, or unrestricted data extracts.

## 6 Support Knowledge to Seed First

Select procedures by observed ticket volume and impact. The table is a starting backlog, not a claim that every procedure applies to this organization. The named source of truth must be identified by the process owner; where none exists, create a draft and obtain approval before publication.

| Procedure | Why it is important | Required information | Source of truth | Suggested knowledge format |
|---|---|---|---|---|
| Network Drive Issues | Frequent access/mapping failures block file-based work and often depend on user, share, and network context. | Supported devices/network, access prerequisites, safe reconnect checks, symptoms, known outages, permissions/escalation route, stop conditions. | Approved file-service SOP and identity/access policy. | Decision tree with symptom → safe checks → result → escalation; link to share directory. |
| Printer Issues | High-volume, repeatable incidents; location and printer identity are often unclear. | Identify printer by location/name, supported user/device, queue/status checks, consumable/paper guidance, service route, restricted network detail handling. | Approved printer register plus print-support procedure. | Short checklist with “identify printer” prompt and location-specific links. |
| Outlook Problems | Common productivity issue with multiple client/service causes. | Supported client/device, service health check, safe profile/cache checks, data-loss warnings, account escalation and stop conditions. | Approved M365 support SOP and service status guidance. | Symptom decision tree; separate user-safe checks from technician-only steps. |
| M365 Login Issues | Authentication problems may indicate account or security risk. | Error capture without passwords/tokens, MFA/conditional-access route, service status, identity escalation, compromise indicators. | Identity team procedure and Entra-approved user guidance. | User checklist plus restricted technician escalation path; never request credentials. |
| Wi-Fi Issues | Common site/device issue requiring location and managed-device context. | Site/SSID scope if approved, supported device, safe reconnect checks, outage indicators, network escalation route. | Approved wireless support procedure and service status source. | Location-aware troubleshooting tree; sensitive network configuration restricted. |
| VPN Issues | Remote access failures can block work and may involve identity/network/security controls. | Supported client/device, service status, approved diagnostics, account/device eligibility, stop conditions, escalation. | Current VPN SOP and identity/network owner. | Ordered, versioned checklist with explicit security stop conditions. |
| Teams Issues | Meetings and calling depend on account, device, service and room equipment. | User vs room-device distinction, service health, client/device checks, room ID, booking/equipment context, escalation. | Approved collaboration support procedure and room register. | Branching checklist with links to room-specific records. |
| Laptop Setup | New or replacement devices require repeatable secure provisioning. | Eligibility, approved device standard, enrollment, software baseline, handoff checks, support route, prohibited bypasses. | Endpoint management build/provisioning SOP. | Role-based checklist with completion and escalation criteria; restricted technician steps. |
| Boardroom Support | Meeting disruption has time pressure and location-specific equipment. | Room identifier, platform/equipment inventory, pre-meeting checks, safe restart guidance, fallback, priority route. | Facilities/room register and approved meeting-room SOP. | Room lookup card plus quick-start checklist and escalation route. |
| Password Reset Process | Account recovery is security-sensitive and frequently requested. | Official self-service route, identity verification requirements, MFA recovery, service desk escalation, anti-phishing warnings. | Approved identity/access policy and service desk procedure. | User-facing approved instructions; never store/reset passwords or weaken verification via the agent. |
| New Starter Provisioning | Delays affect onboarding and access; steps span multiple owners. | Request lead time, authorized requester, approved checklist, role-based access approval, device/software dependencies, completion ownership. | HR/IT onboarding process and access-control policy. | Checklist/RACI with gates, owner roles, and status escalation; no automatic access grant by knowledge alone. |

For each article, include scope, audience, prerequisites, steps, expected result, stop conditions, escalation path, owner, reviewer/approver, source/version, classification, last verified, and next review. Separate user-safe guidance from restricted technician instructions.

## 7 Ticket Knowledge Seeding

Ticket history is evidence for learning what users ask and which resolutions may be reusable. It is not automatically approved knowledge. Seed category definitions and aggregate patterns first; promote individual solutions only after a technician/service owner validates them as repeatable and safe.

### What to derive

- **Ticket categories:** Controlled category, service affected, owning/support group, eligibility, priority guidance, and category review owner.
- **Common incidents:** Recurring symptom/service combinations and counts over an approved time window; aggregate where possible.
- **Repeated resolutions:** Candidate steps or known fixes that appear repeatedly; require owner validation and a published procedure/article before the Knowledge Agent presents them as approved guidance.
- **Root causes:** Use only confirmed root-cause records; distinguish “suspected cause” from verified cause and record source/incident reference.
- **Escalation paths:** Assigned group, escalation condition, hours/priority route, and authoritative source. Prefer group roles over named individuals.

### Sanitization before ingestion

1. Obtain ticket-system/data-owner, Security, and Privacy approval for the purpose, fields, population, access, retention, and processing location.
2. Prefer statistics, category counts, service references, and redacted resolution summaries over full ticket narratives.
3. Remove or mask names, email addresses, phone numbers, employee IDs, customer data, credentials, tokens, secrets, URLs containing tokens, and unnecessary device/user identifiers.
4. Remove sensitive security, HR, legal, health, financial, and privileged operational details unless separately approved for a restricted use case.
5. Check comments, attachments, quoted email chains, and pasted logs; sensitive content may be embedded there even when top-level fields look safe.
6. Preserve ticket access restrictions or use approved aggregate/curated output that does not expose the original case. Enforce access before retrieval.
7. Record sanitization method, reviewer, source version/window, and whether data is aggregate or a curated individual resolution. Do not assume embeddings anonymize content.
8. Re-test sanitized records for re-identification and leakage risk. If safe use cannot be demonstrated, do not ingest them.

### Metadata to retain

Retain only what supports routing, quality evaluation, and traceability: pseudonymous/stable ticket reference where permitted, category, affected service/entity IDs, priority/severity, created/resolved dates, assigned support group, sanitized symptom/resolution summary, resolution classification, verified root-cause flag, procedure/article relationship, source system/version, classification, ACL/scope, reviewer/owner, and confidence/trust level. Avoid requester identity, raw notes, full attachments, and unrestricted transcripts unless there is a specific approved requirement.

## 8 Knowledge Collection Workshops

Workshops validate the source inventory and expose undocumented ownership/relationships. Participants should review records against evidence, not rely on memory alone. Record disputed facts as unresolved and assign an owner instead of forcing agreement.

| Workshop | Goals | Outputs | Deliverables |
|---|---|---|---|
| **Infrastructure Team** | Identify authoritative server/share/network/storage registers; establish file-share-to-host and application dependencies; classify sensitive fields; identify common infrastructure incidents and escalation. | Source-of-truth map, owner list, validated top-priority records, restricted-field decisions, stale/conflict list. | Approved infrastructure seed template; initial server/share dataset or scoped extracts; verification and review cadence; unresolved-questions backlog. |
| **IT Support Team** | Rank frequent ticket categories and procedures; validate user-safe troubleshooting and stop conditions; map support groups, service hours, and escalations. | Top support question list, procedure backlog, category definitions, recurring-resolution candidates, safe redaction requirements. | Reviewed first-line procedures, escalation matrix, representative sanitized test queries, feedback/issue mechanism. |
| **Managers** | Confirm department names, service ownership, business-critical applications, shared resources, business process owners, and acceptable access boundaries. | Department/application/resource ownership relationships; decision owners; gaps and disputed ownership. | Approved department/service-owner register and nominated knowledge owners/reviewers. |
| **Power Platform Developers** | Inventory supported Power Apps/flows; document purpose, environment, owners, data connections, audiences, dependencies, operational impact, and support arrangements. | Validated app/flow register, connection references, owner gaps, lifecycle status, risk classification. | Approved Power Platform seed records and safe support guidance; no connection secrets or unsupported integration assumptions. |
| **Business Users** | Validate user language, common questions, pain points, system names/aliases, self-service clarity, and whether procedures resolve their actual task. | Representative user questions, vocabulary/aliases, article usability feedback, missing-service requests. | Prioritized query/evaluation set and approved user-facing article edits; feedback routed to owners. |

Recommended format: 60–90 minutes per workshop, a facilitator, a record-taker, and one source owner. Prepare candidate records in advance. Capture decisions, evidence, owner, confidence, access classification, and follow-up actions in the source register.

## 9 Knowledge Ownership Framework

Knowledge governance roles describe accountability for content, not AEGIS application authorization. Apply the Security Model's RBAC separately. Every published record has one accountable owner role or group, even when multiple teams contribute.

| Ownership category | Creating | Reviewing | Updating | Retiring |
|---|---|---|---|---|
| **Infrastructure Knowledge Owner** | Infrastructure facts, server/share/network relationships, technical scope, approved support references. | Verifies against authoritative inventory and checks restricted data classification. | Reconciles changes, outages, ownership and dependencies; updates review date. | Marks decommissioned/superseded records; confirms links, derived data, and access are retired. |
| **Application Owner** | Application purpose, business/technical ownership, dependencies, authentication method at high level, support routes. | Confirms current application state, owner, criticality, user audience, and procedure. | Updates material release, dependency, supplier, or support changes; alerts knowledge admin. | Confirms service retirement and disposition of linked procedures, data references, and user guidance. |
| **Department Owner** | Department scope, approved manager/service-owner role, shared resources, applications owned/used, aliases. | Validates relationships and business terminology; checks personal-data minimization. | Reports organizational changes, shared-resource changes, and new business processes. | Approves archive or reassignment when the department/process changes. |
| **Support Knowledge Owner** | Support articles, ticket category guidance, escalation paths, troubleshooting procedures. | Confirms steps are safe, in scope, current, and distinguish user vs technician actions. | Reviews ticket feedback and incidents; updates issue patterns and review dates. | Withdraws unsafe, obsolete, duplicated, or unsupported guidance and identifies replacement. |
| **Platform Administrator** | Creates/maintains source registry, metadata standards, controlled vocabularies, ingestion records, and audit evidence; does not author business truth by default. | Checks metadata, lifecycle state, provenance, access mapping, synchronization health, and quality flags. | Applies approved changes, propagates source updates/deletions, monitors stale records and reports gaps. | Executes owner-approved archival/deletion and records the action; does not unilaterally change source authority or broaden access. |

### Lifecycle responsibilities

- **Create:** Contributor drafts from a known source and proposes an owner, audience, classification, and relationships.
- **Review:** Reviewer and subject-matter owner verify accuracy, completeness, permissions, and procedure safety.
- **Update:** Owner responds to source changes, user feedback, incidents, and review reminders; administrator propagates approved changes.
- **Retire:** Owner approves retirement; administrator marks status and prevents obsolete content from ranking as current.
- **Delete:** Data/source owner authorizes; administrator propagates removal to text, vectors, caches, and derived copies subject to approved retention/legal holds.

## 10 Knowledge Quality Scoring

Score each published object on six dimensions from **0 to 5**. A score of 0 means missing, unverified, or unacceptable; 5 means complete and independently supported to the standard below. Review status has an explicit gate: an unapproved or rejected record cannot be published as trusted guidance regardless of its numeric score.

| Dimension | 0 | 1 | 3 | 5 |
|---|---|---|---|---|
| **Accuracy** | Unknown or contradicted. | Mostly unverified; significant gaps. | Checked against a source or knowledgeable owner, minor uncertainty disclosed. | Verified against the designated authoritative source or independent owner review; no known material conflict. |
| **Completeness** | No usable content/required identity. | Purpose or key fields missing. | Required fields present for the intended question; some optional relationships absent. | Complete for scope, relationships, audience, dependencies, prerequisites, stop conditions, and citations as applicable. |
| **Freshness** | Source date unknown or clearly obsolete. | Beyond review date with no confirmation. | Within the approved review interval or recently source-synchronized. | Verified on change or within the strictest applicable interval; freshness timestamp and source semantics are clear. |
| **Ownership** | No accountable owner. | Owner inferred or unreachable. | Named owner role/group with a route for review. | Accountable owner and backup/reviewer accepted responsibility with review cadence and escalation route. |
| **Trustworthiness** | No provenance or known unreliable source. | Informal/unreviewed evidence only. | Attributed technician note or partially corroborated documentation. | Designated Level 1 source for its fields, or approved Level 2 content with complete provenance and version. |
| **Review Status** | Rejected, withdrawn, or not reviewed. | Draft/pending or review overdue. | Approved and current for normal use. | Independently reviewed, approved, current, and any required security/process approval recorded. |

### Formula and ranges

`Knowledge Quality Score = 20 × (0.25A + 0.15C + 0.15F + 0.15O + 0.15T + 0.15R)`

Where `A, C, F, O, T, R` are the 0–5 dimension scores. Result is 0–100.

| Score | Interpretation | Retrieval treatment |
|---:|---|---|
| **90–100** | High quality | Eligible for normal ranking if status/access permit; still show source and date. |
| **75–89** | Good | Eligible; disclose material limitations and honor source priority. |
| **60–74** | Conditional | Use only as supporting evidence or with an explicit qualification; owner review action required. |
| **40–59** | Poor | Exclude from routine answers; retain only for controlled review or historical use. |
| **0–39** | Unusable | Do not publish for agent retrieval; return to owner or retire. |

### Publication gates

- Missing owner, source/provenance, classification/access decision, or lifecycle status is a hard block regardless of score.
- Draft, rejected, withdrawn, deleted, or superseded content is excluded from current-answer retrieval.
- A published high-risk procedure with overdue review is blocked or explicitly withdrawn pending owner confirmation.
- Access-control tests must pass before any restricted object becomes retrievable.
- Report the score components, not just a single aggregate; a high average must not conceal a zero in a critical dimension.

## 11 Manual Knowledge Seeding Plan

This four-week plan assumes one developer, stakeholder availability of roughly 2–4 hours per week per participating owner group, approved access to a limited set of source records, and no connector implementation. Work should be adjusted to actual source availability. “Collected” means records with traceable sources; “published” means reviewed and passing hard gates.

| Week | Focus and activities | Sources targeted | Planning volume (candidate → published) | Expected value delivered |
|---|---|---|---:|---|
| **Week 1 — Establish the seed process** | Confirm source owners and access rules; define templates/controlled fields; build an initial 30-question test set with support; collect department/support group/SharePoint metadata; classify sensitive fields. | Service desk lead, organization/service directory, approved SharePoint site register, existing knowledge catalogue. | 20–35 candidates → 10–20 approved records across departments, groups, and sites. | Search can identify where approved knowledge lives and who owns support; governance and quality baseline established. |
| **Week 2 — First-line support** | Workshop with service desk; draft and review highest-frequency procedures; build ticket-category/escalation mappings; test answers with provenance and no-answer behavior. | Approved SOPs/articles, support staff interviews, sanitized recent ticket categories. | 20–30 candidates → 10–15 procedures/categories/escalations. | First useful Helpdesk/Knowledge scenarios for common user issues. |
| **Week 3 — Environment lookups** | Collect prioritized file shares, core server relationships (restricted fields), printer records, top applications and their owners/support routes; validate against registers. | Infrastructure and asset records, application catalogue, manager/owner interviews. | 35–60 candidates → 25–45 reviewed entity records, depending on source readiness. | Answers to “where hosted?”, “which printer?”, “who owns/supports this application?” for the initial priority set. |
| **Week 4 — Validate and close gaps** | Seed initial Power Apps, boardrooms, and support articles; run retrieval/access tests; fix conflicts/stale metadata; score dataset; assign owners/review dates and backlog automation candidates. | Power Platform developers, facilities/room register, business users, knowledge owners. | 25–45 candidates → 20–35 approved records plus a prioritized gap list. | A tested, sourced initial dataset; known limitations and the next phase are visible rather than hidden. |

**Four-week planning estimate:** approximately 100–170 candidate records reviewed, with 55–100 records likely publishable if source quality and owner participation are adequate. A record may be a structured entity, relationship, article, or procedure. Do not treat the estimate as a quota: stop or defer when provenance, permission, or owner checks fail. Measure useful answer coverage, not raw count.

## 12 Automated Knowledge Ingestion Roadmap

Automate only after the manual process proves the schema, source trust, ACL mapping, freshness needs, deletion behavior, and owner workflow. Integration complexity is relative and assumes an approved, supported API/export. No listed integration is part of MVP by implication.

| Source | Integration complexity | Security considerations | Expected value |
|---|---|---|---|
| **Microsoft Graph** | High | Minimize delegated/application scopes; protect workload identity; preserve source ACLs and user context; avoid broad mailbox/chat ingestion; handle throttling and permission revocation. | Cross-domain identity, SharePoint and Microsoft 365 metadata where approved. |
| **SharePoint** | Medium–High | Site/library and item-level ACLs; version/deletion/retention handling; approved scopes and owners; avoid indexing drafts or hidden content. | High-value current documentation and lists, with provenance and updates. |
| **Intune** | Medium | Least-privilege read access; protect device/user-linked data; map compliance status carefully; handle device retirement and stale sync. | Current endpoint inventory and management-state relationships. |
| **N-able** | Medium | Vendor credential protection, narrow read scopes, endpoint allowlist, telemetry classification, rate limits and stale/failed sync detection. | Operational asset and monitoring context for support. |
| **Asset Registers** | Low–Medium if export/API is stable | Read-only access, field allowlist, reconciliation, personal/serial-number minimization, source-of-truth designation. | Authoritative lifecycle, location and assignment facts. |
| **Ticketing Systems** | Medium–High | Privacy approval, redaction, ACLs, retention, attachment/comment filtering, user identity minimization, avoid promoting one-off fixes. | Ticket categories, repeated issue patterns, routing and reviewed resolution candidates. |
| **Power Platform** | Medium–High | Restrict environment/app/flow inventory scopes; exclude connection secrets and sensitive run payloads; classify destructive flow impact; verify owners and sharing scope. | Current app/flow inventory, business purpose, ownership and dependencies. |
| **Knowledge Libraries** | Medium | Preserve document ACLs and lifecycle; handle version/retention/deletion; classify content and exclude drafts; test leakage across audiences. | Fresh, reviewable articles/SOPs with citations and less manual maintenance. |

### Automation entry criteria

Before enabling a connector: named source owner; approved business purpose and data fields; security/privacy review; stable IDs; documented trust level; validated ACL semantics; update and deletion SLA; source outage/partial sync behavior; test corpus; error monitoring; secret ownership/rotation; and an operational runbook. First release should be read-only. Consequential actions are not enabled by ingestion work.

## 13 Initial Knowledge Dataset Specification

The following quantities are **planning targets for coverage discussion**, not minimum acceptance gates or reasons to create artificial records. They assume the organization actually has those resources and that each record can be verified and safely published. Start with the highest-value subset; expand only when there are owners and source evidence.

| Dataset | Aspirational coverage target | Why this target is useful | MVP seeding rule |
|---|---:|---|---|
| Support Procedures | 20 | Covers a broad first-line support set, including common access, connectivity, collaboration and device issues. | Seed top 8–12 approved procedures first; grow toward 20 after review and usage evidence. |
| File Shares | 50 | Could cover frequently referenced business shares and hosting/ownership relationships. | Seed top 10–20 operationally important shares with access-controlled hosting details; do not index share contents by default. |
| Printers | 50 | Could provide location/department lookup for a multi-floor/site environment. | Seed known active, shared printers; exclude retired/duplicate devices and restrict IPs. |
| Applications | 20 | Provides a useful initial service catalogue spanning business and technical systems. | Seed top 10–15 user-facing or support-critical applications with owner/support/dependency fields. |
| Power Apps | 10 | Establishes visibility into business-built apps and ownership gaps. | Seed verified active apps only; do not infer missing owners or connections. |
| SharePoint Sites | 10 | Maps major approved knowledge repositories and business collaboration sites. | Start with all known approved knowledge sites (often fewer than 10); capture ACL and owner, not all contents. |
| Departments | 10 | Provides an initial organization ownership and routing vocabulary. | Seed all relevant departments if there are fewer; validate canonical names and aliases. |
| Boardrooms | 20 | Enables room equipment and support lookup where there are many bookable rooms. | Seed the rooms with dedicated VC equipment or highest support volume first. |
| Knowledge Articles | 50 | A larger current article set can answer varied self-service questions. | Start with 15–25 reviewed high-use articles; exclude duplicates, stale, unowned, or inaccessible content. |

Dataset acceptance is based on coverage of agreed user questions, correct access behavior, traceable sources, quality score, and owner acceptance. If a target is not applicable or source data is unreliable, record the gap and reason instead of manufacturing a record.

## 14 Knowledge Risks

Likelihood and impact are initial qualitative ratings to validate with source owners and Security.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Outdated Knowledge** | High | High | Require source/modified/verified/review dates; assign owners and freshness SLAs; flag overdue records; exclude or qualify high-risk stale procedures; invalidate changed/deleted content. |
| **Poor Documentation** | High | Medium/High | Use templates and completeness gates; workshop with subject-matter owners; distinguish known facts from assumptions; test procedures with support staff; do not publish drafts as authoritative. |
| **Conflicting Information** | Medium/High | High | Designate authoritative source per field; record effective dates/version; retain provenance; route conflicts to owner; expose unresolved conflicts rather than merging them. |
| **Missing Ownership** | High | High | Make owner a hard publication requirement; maintain source/entity owner register; block Level 1/2 status for unowned content; escalate overdue ownership actions. |
| **Information Silos** | High | Medium | Hold cross-functional workshops; build typed relationships; provide owners a controlled correction route; integrate only with approved scopes and ACL-aware connectors. |
| **Sensitive Information Exposure** | Medium | Very High | Classify before ingestion; minimize fields; preserve source ACLs and filter before retrieval; restrict IPs, identity, security, and ticket data; test cross-user/source access; redact ticket content; do not treat embeddings as anonymized. |
| **False Authority / Model Inference** | Medium | High | Never treat generated text as evidence; cite source records; separate fact and inference; calibrate confidence; require explicit uncertainty and safe “not found” behavior. |
| **Permission Drift** | Medium | High | Synchronize ACL changes; define revocation SLA; invalidate permission-sensitive caches; recheck authorization before retrieval/answer; test revoked and changed access. |
| **Unreviewed Ticket Fix Becomes Procedure** | Medium | High | Treat ticket data as candidate evidence; require technician/service owner validation, sanitization, and publication workflow before reuse as approved guidance. |
| **Source Sync Appears Current After Partial Failure** | Medium | Medium/High | Track watermark, successful coverage, failures, and sync lag; expose partial state; never update freshness timestamp as if full sync succeeded. |
| **Overcollection and Maintenance Burden** | Medium | Medium | Seed by use case and frequency; avoid bulk archive ingestion; use relevance/quality gates; retire low-value content and measure owner workload. |

## 15 Success Metrics

Establish a baseline during the first two weeks. Report metrics against a defined test set, population, and period. Separate “answered with an appropriate source” from fluent but unsupported answers.

| Metric | Definition | Proposed MVP target |
|---|---|---|
| **Percentage of Questions Answered** | On a reviewed representative query set, percentage with a relevant, access-permitted, correctly sourced answer. Report “safe no answer/clarification” separately from incorrect answers. | At least 70% of priority questions receive a useful sourced answer by MVP exit; 100% of unsupported/unknown test cases avoid fabricated facts. |
| **Reduction in Search Time** | Median time to find the required source/answer for matched common tasks, comparing baseline workflow with AEGIS. | At least 30% reduction for the first 10–20 agreed tasks in a small user pilot. |
| **Reduction in Repeated Support Questions** | Change in volume of selected repeatable categories after relevant approved knowledge is made discoverable, adjusted for ticket volume/seasonality. | Establish baseline during pilot; target 10% reduction for selected categories within 90 days of broader use, not as an MVP launch gate. |
| **Knowledge Coverage** | Percentage of prioritized questions/entities with an owned, current, accessible source and required relationship/procedure. | At least 80% of top-priority lookup questions covered; no claim that all organizational knowledge is indexed. |
| **Knowledge Freshness** | Share of active high-priority records within their approved review/update interval. | At least 90% current at launch; 100% of overdue high-risk procedures flagged or withheld. |
| **User Satisfaction** | User rating on helpfulness, accuracy, source usefulness, and ability to find next step; capture feedback volume and response rate. | Average ≥4/5 from at least 20 pilot evaluations where possible; review all low scores and correctness reports. |
| **Owner Assignment** | Published records with accountable owner, source, classification, review date, and status. | 100% for published records; incomplete records remain draft. |
| **Access-control correctness** | Authorized/unauthorized retrieval tests passing, including permission-change cases. | 100% pass for defined tests; any confirmed cross-scope disclosure is a release blocker. |
| **Citation/Provenance Coverage** | Factual answers with citations identifying the supporting record/version. | 100% for organization-specific factual claims in the evaluation set. |
| **Quality score distribution** | Published records meeting score and hard-gate requirements, segmented by domain. | ≥75 quality score for normal retrieval; high-risk procedure and access gates always pass. |

Review metrics monthly during MVP pilot. Metrics indicate product and data quality; they do not replace security acceptance, owner approval, or qualitative incident review.

## 16 First 30 Days Action Plan

This is a practical solo-developer sequence aligned with the requested priority order. It assumes the developer can schedule short owner workshops and receive approved, limited extracts. If owner approval or source evidence is unavailable, document a blocker and move to another approved source rather than scraping or guessing.

| Week | Priority and milestones | Expected deliverables |
|---|---|---|
| **Week 1 — File Servers and SharePoint Sites** | Confirm infrastructure/site owners, classification, visibility rules, and approved source records. Capture the highest-value active file-share/server relationships and the approved knowledge sites. Treat IPs and exact paths as restricted fields. | Source register; structured server/share records with provenance and access labels; site owner/purpose/ACL records; unresolved facts list; initial questions for “where hosted?” and “where is the approved guidance?” |
| **Week 2 — Applications and Departments** | Hold manager/application-owner workshop. Seed top user-facing/support-critical applications and canonical department records. Distinguish application owner from user department; capture high-level auth method and support route. | Application-to-department/owner/support relationships; department aliases and shared resources; review dates; validated test questions for ownership and escalation. |
| **Week 3 — Printers and Support Procedures** | Seed active high-use printer records and the first approved procedures: network drive, printer, M365 sign-in, VPN/Wi-Fi, Outlook/Teams as available. Review safe steps, stop conditions, escalation, privacy, and user/technician audience. | Printer/location/department records; 8–12 approved procedures or fewer if review is pending; mapped support groups and ticket categories; redaction and access tests. |
| **Week 4 — Power Apps and Boardrooms; evaluation** | Verify active Power Apps, their purpose/owner/business process and SharePoint/Dataverse relationships. Seed boardrooms with VC equipment and room support references. Evaluate retrieval, provenance, stale/conflicting knowledge, and access behavior; prioritize next-month work. | Approved Power App and boardroom seed records; initial dataset scorecard; evaluation results against query set; owner assignments and refresh backlog; integration candidates with explicit review needs. |

### Day-30 exit checklist

- Every published item has stable identity, owner, source/provenance, classification/access decision, lifecycle status, and review date.
- Priority fields and relationships are verified by source owner or authoritative record.
- Restricted IP/network, personal, ticket, and security details are not exposed to unauthorized users or general prompts.
- The initial query set covers the prioritized lookup/support use cases; each answer cites accessible evidence or safely reports a gap.
- User feedback and owner corrections have a recorded route and accountable handler.
- Dataset counts reflect real, validated records—not target quotas.
- A next-phase decision is made on whether the manual process has enough value and readiness for an automated source integration.
