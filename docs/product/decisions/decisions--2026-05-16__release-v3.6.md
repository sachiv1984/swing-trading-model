Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.6
Cycle: 2026-05-16__release-v3.6
Last Updated: 2026-05-16

## Planning Decisions — v3.6 Arc 4 Data Integrity + Arc 2 Quality Score + Debt Clearance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Prioritise planned_entry_price data capture (S2-01) over new Arc 4 analytics | Every trade entry without the snapshot loses data permanently. Arc 4 analytics (PO-02/03/04) depend on accumulated data; the capture fix must precede data accumulation pressure. | Product Owner | 2026-05-16 |
| Defer PO-02/03/04/05 (Arc 4 analytics) to v3.7+ | PO-02 requires 6+ months of AI-summarised journal entries; AI Journal Summarisation shipped 2026-04-20 (~1 month ago). Gate not met. PO-03/04 depend on PO-02. PO-05 is VH effort. | Product Owner | 2026-05-16 |
| Include PT-04 (S2-02) as conditional scope | Last remaining Arc 2 feature; gate is 20+ closed trades (likely met given live since v1.5 ~Jan 2026). Conditional: PO must confirm gate before sprint planning seals; if not confirmed, EPIC-02 defers to v3.7. | Product Owner | 2026-05-16 |
| Bundle aged backlog items (S2-03) into one EPIC | BLG-FE-32, TEST-GAP-EPIC-03-v33, BLG-SPEC-27, BLG-FE-26 all 2–3 cycles deferred. Bundling into one EPIC prevents further drift and is within solo-dev S-effort range. | Product Owner + PMO Lead | 2026-05-16 |
| Governance patches (S2-04) follow v3.5 LL pattern | 4 execution_prompt.md patches deferred from v3.5 LL closure (Head of Specs Team). Continuing the EPIC-04 governance patch pattern proven effective in v3.4/v3.5. | Product Owner | 2026-05-16 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-04 and EPIC-03 in Sprint 1 | Governance patches and QA/spec debt are Sprint 1 priorities: low risk, autonomous delivery, unblock downstream work | PMO Lead | 2026-05-16 |
| EPIC-01 backend (ST-01) in Sprint 1, frontend (ST-02) in Sprint 2 | Backend data model must precede frontend display. Sprint 1 captures the schema migration; Sprint 2 surfaces it in UI. | PMO Lead | 2026-05-16 |
| EPIC-02 conditional on Sprint 1 gate confirmation | PT-04 gate (20+ closed trades) must be confirmed by Sprint 1 close. If confirmed: EPIC-02 Sprint 2. If not: EPIC-02 defers to v3.7. | Product Owner | 2026-05-16 |
| Merge order: EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02 | Governance first (no shared file conflicts); QA/spec second; Arc 4 data capture third; PT-04 last (most dependent) | PMO Lead | 2026-05-16 |

### Accepted risks

None — no escalations raised this cycle. RISK-02 (PT-04 gate) is a conditional gate, not an accepted risk; it defers the EPIC rather than accepting risk.

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-05-16__release-v3.6
