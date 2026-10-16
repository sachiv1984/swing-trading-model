**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 3.5
**Last Updated:** 2026-10-16 (roadmap rebalance `2026-10-16__scheduled` STEP -1.6 — inline full-roster intake `IW-20261016-01`: 32 rows appended as Submitted); prior — 2026-10-12 (ideas_housekeeping — 8 rows archived, post-ship closure 2026-10-08__release-v9.11: 8 Promoted-Backlog from IW-20261008-01; 1 Rejected-but-strong row kept); prior — 2026-10-08 (roadmap rebalance `2026-10-08__scheduled` — inline idea intake `IW-20261008-01` (8 submissions, reduced roster of 4 user-facing roles, user-approved) and STEP 4.2 dispositions: 8 Promoted-Backlog, filed as 6 backlog items after 2 consolidations); prior history retained — see prior entries in version control
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Ideas Register

Migrated from per-file model (44 submissions from IW-20260304-01) on 2026-03-17 per ST-19 (EPIC-06).
Schema: per `shared_standards.md §16.5`

| Idea ID | Title | Submitter | Window | Submitted At | Status | Park Count | Park Rationale | Step 4 | Step 5 |
|---------|-------|-----------|--------|--------------|--------|------------|----------------|--------|--------|
| IDEA-challenger-20260809-02 | Challenge: is the SI-02 ≥20-linked-trades gate threshold calibrated for this system's actual trade cadence? (9+ consecutive NOT MET readings) | Challenger | IW-20260809-01 | 2026-08-09 | Rejected | — | — | Reject — strong (already answered by BLG-GOV-237, v8.3, "still appropriate"; see rejected_but_strong.md) | N/A |
| IDEA-ai-compliance-20261016-01 | Bound the AI Post-Trade Debrief's red-flag context to the trade's own holding window | AI Compliance & Governance Officer | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-api-contracts-20261016-01 | CI check that every frontend API call (method + path) exists in openapi.yaml | API Contracts & Documentation Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-api-contracts-20261016-02 | `GET /digest/weekly` names journal completion rate `compliance_score_*` | API Contracts & Documentation Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-backend-engineering-20261016-01 | Stop silently discarding failed red-flag override writes | Backend Engineering Patterns Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-base44-frontend-20261016-01 | Trade Reflections shows "No closed trades yet" when a ticker search simply has no match | Base44 Frontend Prompt Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-base44-frontend-20261016-02 | Remove dead Base44 scaffold methods from `base44Client.js` that call routes the backend never had | Base44 Frontend Prompt Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-challenger-20261016-01 | Challenge: the Dashboard's Daily Position Monitor exit action has been broken since January — what is the debt process checking? | Challenger | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-challenger-20261016-02 | Challenge: full-roster idea windows require 2 ideas from every role, and 17 of 22 roles have no user-facing remit | Challenger | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-cybersecurity-20261016-01 | Remove the unused bearer-token path: the client sends any `localStorage` token as `Authorization` to an API that has no auth route | Cybersecurity & Trust Lead | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-cybersecurity-20261016-02 | Production API's CORS allow-list includes `http://localhost:3000` and the API's own origin | Cybersecurity & Trust Lead | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-data-model-20261016-01 | Link pre-entry override events to the position they led to | Data Model & Domain Schema Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-director-of-hr-20261016-01 | Append the role-share history row at post-ship closure, not only at a rebalance | Director of HR | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-director-of-quality-20261016-01 | Fail the Playwright suite on any 404 or 405 API response | Director of Quality | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-financial-reporting-20261016-01 | The Monitor's bulk exit would write a P&L that bypasses fees, broker fill and FX | Financial Reporting & Records Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-finops-20261016-01 | Skip the five code-test workflows on governance-only and docs-only pushes | FinOps & Resource Architect | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-frontend-specs-20261016-01 | Grace-period warning says "day 8 of 10" while Positions shows Day 9 for the same position | Frontend Specifications & UX Documentation Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-frontend-specs-20261016-02 | Alert History's compact values look for keys the backend never writes | Frontend Specifications & UX Documentation Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-head-of-engineering-20261016-01 | Make the Daily Position Monitor's "confirm exits" work: open the real exit flow for each selected position | Head of Engineering | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-head-of-engineering-20261016-02 | One shared exit-reason module for the four frontend files that each keep their own map | Head of Engineering | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-head-of-specs-20261016-01 | Reconcile shared_standards §2's "write Blocked state before halting" with the roadmap engine's state-write limits | Head of Specs Team | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-head-of-ux-20261016-01 | Trade Reflections cards show grey raw-uppercase exit badges because their colour map never matches | Head of UX & Design | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-head-of-ux-20261016-02 | Red Flag Journal offers three event-type filters that can never return a row | Head of UX & Design | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-infra-ops-20261016-01 | Nightly job chain is ordered by clock time only; rebalance-exit can run on a stale top-5 | Infrastructure & Operations Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-metrics-20261016-01 | Weekly Digest labels journal completion rate as "Compliance Score" | Metrics Definitions & Analytics Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-metrics-20261016-02 | "Alerts Dismissed (7d)" counts alerts created in the window that are now read, not alerts read in the window | Metrics Definitions & Analytics Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-pmo-lead-20261016-01 | Deferred roadmap patches go OVERDUE by carry count before their own target date | PMO Lead | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-product-owner-20261016-01 | The Daily Position Monitor cannot exit a position: fix it before the next stop or risk-off event | Product Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-product-owner-20261016-02 | The Daily Portfolio Summary notification says only how many positions are open | Product Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-qa-lead-20261016-01 | Regression test for the Daily Position Monitor confirm path | QA Lead | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-qa-testing-20261016-01 | Test that every red-flag event type the API accepts has at least one writer | QA & Testing Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-strategy-owner-20261016-01 | Month-end rebalance exits are live but not in `strategy_rules.md` | Strategy Rules & System Intent Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
| IDEA-strategy-owner-20261016-02 | Record `checklist_skipped` when a trade plan is saved with its checklist incomplete | Strategy Rules & System Intent Owner | IW-20261016-01 | 2026-10-16 | Submitted | — | — | — | — |
