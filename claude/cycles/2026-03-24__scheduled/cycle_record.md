**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-24

---

# Cycle Record — Roadmap Rebalance 2026-03-24__scheduled

**Run type:** Scheduled
**Completion event:** N/A — scheduled run
**Cycle ID:** 2026-03-24__scheduled
**Date:** 2026-03-24
**Mode:** Standard
**Run tier:** Extended

---

## STEP 2 — Re-Validation

**Authorities:** Product Owner + Strategy Rules & System Intent Owner

### Active Initiatives Reviewed

Zero active roadmap initiatives at the start of this run. The Active Initiatives table in `initiative_register.md` reads: "No active initiatives as of 2026-03-21. All v2.1 items shipped. v2.2 scope TBD — pending release planning." v2.2 has since shipped (2026-03-24). The register is current.

**Result:** Zero active roadmap initiatives to re-validate. All previously active items are in the Completed table.

### Strategy Proximity Scores (SPS)

Zero active initiatives → no SPS computation required.

**Gated initiatives** (not consuming resources — no SPS scoring required per protocol):
- AI-SUM: §13 boundary decision pending
- TECH-IND: Strategy rules review pending
- MKT-COR: External data pipeline decision pending

### Cycle Proximity Score (CPS)

- **CPS this cycle:** N/A — zero active initiatives. Recorded as **0.0**.
- **Prior CPS:** 0.0 (cycle 2026-03-21__item-3.5 — also zero active initiatives post v2.1 ship)
- **Trend:** 0.0 delta. No change.
- **Drift alert:** Not triggered (CPS = 0.0 < 2.5 absolute threshold; delta = 0.0 < 0.5 delta threshold).

*Strategy Rules & System Intent Owner acknowledgement: No active initiatives to score. No drift alert issued. Gated items remain appropriately gated.*

### Horizon Review

**(Extended tier — explicit Now→Next promotion check required)**

**Horizon structure:**

- **Now** (committed delivery): Empty — v2.2 shipped; v2.3 release planning not yet run.
- **Next** (1–3 releases, planned in principle): No items currently placed here. The 15-item active backlog represents the candidate pool for v2.3 scope.
- **Later** (3+ releases, strategic intent only): Position Correlation Analysis, Backtesting Module, Multi-Portfolio Support, Mobile App, Full Compliance Scoring, BLG-TECH-05 Prometheus, Customisable Dashboard Layout.
- **Gated** (awaiting pre-conditions): AI-SUM, TECH-IND, MKT-COR.

**Extended tier Now→Next promotion check:**

For each "Later" item — has context changed to warrant promotion to "Next"?

| Later item | Assessment |
|-----------|------------|
| Position Correlation Analysis | No change. Single-user scale still constrains value. |
| Backtesting Module | No change. Significant scope; no triggering event. |
| Multi-Portfolio Support | No change. Low value at current scale. |
| Mobile App | Indefinitely deferred. Web experience sufficient. |
| Full Compliance Scoring | BLG-FEAT-11 (display-only compliance score) ships in v2.3 — lightweight version in progress. Full version still post-v2.3. |
| BLG-TECH-05 Prometheus | No new operational need. Deferred. |
| Customisable Dashboard Layout | High build cost; low current priority. No change. |
| AI-SUM (gated) | §13 boundary decision still open. No triggering event. Remains gated. |
| TECH-IND (gated) | Strategy rules review still pending. Remains gated. |
| MKT-COR (gated) | No data pipeline decision. Remains gated. |

**Horizon review outcome: No movements recommended.** Gated items remain appropriately gated; deferred items have no new triggering events post-v2.2. BLG-FEAT-11 partial delivery addresses the "compliance scoring" later item without promoting it to full scope.

---

## STEP 3 — Backlog Health

**Authorities:** Head of Specs Team (process), Product Owner (planning ownership)

### Backlog Health Summary

The backlog was groomed 2026-03-24 (GROOM-20260324-01). 15 active items confirmed. No further grooming needed this cycle.

**Active item health:**

| Item | Priority | Type | Status | Notes |
|------|----------|------|--------|-------|
| BLG-TECH-05 | P3 | Observability | Stale target (v2.2 → now v2.3) | Still deferred; low urgency |
| BLG-QA-01 | P2 | QA Automation | Active (v2.3) | Clear AC; depends on Playwright |
| BLG-BE-04 | P3 | Backend | Active (v2.3) | Small fix; sequencing flexible |
| TEST-GAP-EPIC-05-SLIP | P3 | QA Coverage | Active (v2.3) | Clear scope |
| BLG-GOV-03 | P3 | Governance | Active (v2.3) | Clean scope |
| BLG-UX-01 | P2 | UX | Active (v2.3) | PO design decision still pending |
| BLG-FEAT-11 | P2 | Feature SPS=4 | Active (v2.3) | Scope constraint documented; SPS=4 review required at delivery |
| BLG-FEAT-09 | P2 | Feature | Active (v2.3) | Gate cleared (BLG-FEAT-03 slippage shipped) |
| BLG-FE-02 | P3 | Frontend | Active (v2.3) | Clear scope |
| BLG-OPS-05 | P3 | Operational | Active (v2.3) | Clear scope |
| BLG-FE-03 | P3 | Frontend | Active (v2.3) | Gate cleared (BLG-SPEC-G2 shipped) |
| BLG-SPEC-D14 | P2 | Spec Debt | Active (v2.3 Sprint 1) | Small; high priority given spec drift |
| BLG-FE-04 | P3 | Frontend | Active (v2.3) | Small; spec compliance |
| BLG-GOV-07 | P3 | Governance | Active (v2.3) | Small; execution_prompt update |
| BLG-GOV-08 | P3 | Governance | Active (v2.3) | L effort; prompt compression |

**Health observations:**
- **No duplicates:** GROOM-20260324-01 resolved BLG-BE-02/BLG-BE-04 and TEST-GAP-EPIC-02/TEST-GAP-NOTIF-01 duplicate IDs. ✅
- **No obsolete items:** All 15 items remain strategically relevant.
- **BLG-TECH-05 target stale:** Still lists v2.2 target — update to v2.3 at next backlog write.
- **Quick wins identified:** BLG-SPEC-D14 (XS), BLG-FE-04 (XS), BLG-GOV-07 (XS), BLG-OPS-05 (S) — four quick-win items. Release planning should prioritise these for Sprint 1 to generate early momentum.
- **BLG-GOV-08 large:** L effort prompt compression — should be scoped as its own sprint item with adequate time.
- **Promotion candidates from groom:** BLG-SPEC-D14 and BLG-GOV-07 were flagged by GROOM-20260324-01 as promotion candidates. Both are already in the backlog.

**Conclusion:** Backlog is healthy. No deletions or rewrites required. 15 items are appropriately described and ready for release planning.

---

## STEP 4 — Ideas

**Authorities:** Facilitator (review), Product Owner (classification decisions)

### Intake Status

- Idea intake engine not run this cycle (≥ 20 open ideas — threshold met; intake skipped per STEP -1.6)
- Total submissions loaded: 40 (Parked-cycle-5: 5; Parked-cycle-1: 35)
- Window: Not run this cycle

### Stale Ideas (≥ 3 cycles parked — mandatory active PO disposition)

| Idea ID | Title | Cycles Parked | Disposition | Rationale |
|---------|-------|--------------|-------------|-----------|
| IDEA-frontend-ux-20260304-02 | Accessibility Baseline for Critical UI Components | 5 | 🅿 Re-park (cycle-6) | Still not blocking core delivery; accessibility investment deferred to post-v2.3. Revisit when UI component inventory (IDEA-frontend-ux-20260321-02) ships. |
| IDEA-head-of-ux-20260304-02 | Design Token System | 5 | ❌ Reject (not strong) | 5 cycles with no triggering event. Single-user system with no design team; design token investment not justified at current scale. Permanently close. |
| IDEA-infra-ops-20260304-02 | System Health Check Playbook | 5 | ✅ Advance | BLG-OPS-06 (health endpoint) shipped v2.2 — monitoring gap addressed. Playbook documentation now warranted as a light companion document. |
| IDEA-pmo-lead-20260304-02 | Delivery State Report (CI-Generated) | 5 | 🅿 Re-park (cycle-6) | v2.3 has governance items already (BLG-GOV-07, BLG-GOV-08). CI investment for delivery state report deferred further — revisit post-v2.3. |
| IDEA-qa-lead-20260304-01 | Canonical Test Execution Report Template | 5 | ✅ Advance | BLG-QA-02 (automation readiness assessment) shipped v2.2 — gate cleared. Readiness assessment recommended standardised reporting. |

### Per-Idea Classification — Parked-cycle-1 (IW-20260321-01)

**Advancing to STEP 5:**

| Idea ID | Title | Gate cleared | Displacement named |
|---------|-------|-------------|-------------------|
| IDEA-qa-testing-20260321-01 | Integration Test Coverage Report | BLG-QA-02 shipped | BLG-FE-03 deprioritised in priority queue |
| IDEA-qa-testing-20260321-02 | Critical-path Smoke Test (Playwright) | BLG-QA-02 shipped | BLG-FE-02 deprioritised in priority queue |
| IDEA-infra-ops-20260321-02 | Staging Data Reset Script | BLG-QA-02 shipped | TEST-GAP-EPIC-05-SLIP deprioritised in priority queue |
| IDEA-finops-20260321-02 | Database Size Monitoring Alert | BLG-OPS-06 shipped | BLG-TECH-05 deprioritised in priority queue |
| IDEA-base44-frontend-20260321-02 | Alert Notification Badge in Nav | BLG-FEAT-12 shipped | BLG-FE-04 deprioritised in priority queue |
| IDEA-director-of-quality-20260321-02 | Test Data Seed Script Library | BLG-QA-02 shipped | BLG-OPS-05 deprioritised in priority queue |

**Re-parked (Parked-cycle-2):**

| Idea ID | Title | Rationale |
|---------|-------|-----------|
| IDEA-product-owner-20260321-02 | Weekly trading review digest | v2.3 product scope rich (BLG-FEAT-11, BLG-FEAT-09). Defer until compliance score and staleness indicator land and usage patterns are clearer. Revisit post-v2.3. |
| IDEA-head-of-specs-20260321-01 | Spec dependency map | BLG-SPEC-T01 shipped — gate cleared. But simpler v2.3 spec wins (BLG-SPEC-D14) should land first. Revisit post-v2.3 once spec debt is lower. |
| IDEA-head-of-specs-20260321-02 | Machine-readable spec front-matter | BLG-SPEC-T01 shipped. Capacity constrained with BLG-GOV-08 (engine compression) in v2.3 scope. Revisit post-v2.3. |
| IDEA-pmo-lead-20260321-01 | Cycle velocity metric | Governance tooling; capacity constrained with BLG-GOV-07 and BLG-GOV-08 in v2.3. Revisit post-v2.3. |
| IDEA-pmo-lead-20260321-02 | Governance health score | Same as above — capacity constrained. Revisit post-v2.3. |
| IDEA-strategy-owner-20260321-02 | §13 boundary review cadence | §13 is stable post-v2.2. No boundary proximity event. Revisit when AI Journal Summarisation gate approaches. |
| IDEA-finops-20260321-01 | Render hosting tier review | BLG-OPS-04 (cron) shipped. Let scheduling run for one sprint to observe actual costs before formal review. Revisit at v2.3 sprint planning. |
| IDEA-challenger-20260321-01 | SPS≥4 mandatory §13 review gate | roadmap_prompt already handles SPS≥4 via STEP 5 Score-4 rule. No additional formal gate warranted. |
| IDEA-challenger-20260321-02 | Complexity budget tracking | No implementation path defined. v2.3 scope being set. Revisit post-v2.3. |
| IDEA-backend-engineering-20260321-02 | Alert evaluation idempotency | BLG-OPS-04 shipped. Architectural design needed before implementing idempotency — observe alert scheduling behaviour for one sprint first. |
| IDEA-ai-compliance-20260321-01 | Governed decision audit log | decision_log.md already provides coverage at current scale. Not worth separate system. |
| IDEA-ai-compliance-20260321-02 | Model version contract | Governance hygiene; not urgent. Revisit when governance cadence more established. |
| IDEA-metrics-analytics-20260321-01 | Consecutive losing streak metric | v2.3 has BLG-FEAT-11 (compliance score, M-L effort). Park until compliance score ships — metrics spec update needed. |
| IDEA-metrics-analytics-20260321-02 | ATR-normalised sizing retrospective | Needs more trade history data to be meaningful. |
| IDEA-head-of-engineering-20260321-02 | Background task scheduler | v3.0 scope (broker API integration architectural dependency). |
| IDEA-base44-frontend-20260321-01 | Keyboard shortcuts for trading actions | Awaiting BLG-FE-02 and BLG-FE-03 (loading state, error mapping) — revisit once those land. |
| IDEA-data-model-owner-20260321-02 | Position tags normalisation | Low urgency at current scale. Revisit if tag-based filtering becomes a requested feature. |
| IDEA-financial-reporting-20260321-01 | Monthly P&L summary report | Tax year report just shipped — need more trade history. Revisit for v2.3 after more data accumulates. |
| IDEA-financial-reporting-20260321-02 | Net-of-costs performance tracking | Requires data model change; not urgent for initial system. |
| IDEA-director-of-hr-20260321-01 | Agent role effectiveness review | v2.2 just shipped. Governance capacity focused on BLG-GOV-07/08 for v2.3. Revisit after v2.3 ships. |
| IDEA-director-of-hr-20260321-02 | New agent onboarding checklist | Team stable; low urgency. |
| IDEA-api-contracts-20260321-01 | API version sunset policy | Single-user; no external consumers yet. |
| IDEA-api-contracts-20260321-02 | Webhook event catalogue | v3.0 scope. |
| IDEA-qa-lead-20260321-01 | QA sign-off SLA standard | Current turnaround acceptable. |
| IDEA-qa-lead-20260321-02 | Bug severity classification matrix | Not blocking. |
| IDEA-frontend-ux-20260321-01 | Frontend performance budget | Awaiting BLG-OPS-05 (API baseline). Revisit after API baseline ships. |
| IDEA-frontend-ux-20260321-02 | React component inventory | Awaiting BLG-FE-02/BLG-FE-03. Revisit once loading state and error mapping land. |
| IDEA-head-of-ux-20260321-01 | Responsive layout breakpoints spec | Mobile app indefinitely deferred. Revisit when mobile app enters roadmap scope. |
| IDEA-head-of-ux-20260321-02 | Design system document | Not urgent. Revisit alongside design tokens idea at post-v2.3. |

### Idea Summary

- Window: Not run this cycle
- Total submissions loaded: 40
- **Advancing to STEP 5:** 8 (2 stale-advance + 6 new-advance)
- **Parked (cycle-2):** 29
- **Parked (cycle-6, stale re-park):** 2
- **Rejected:** 1 (IDEA-head-of-ux-20260304-02 — not strong)
- **Stale ideas (≥3 cycles parked) surfaced:** 5
- **Stale ideas closed this cycle:** 3 (1 rejected, 2 re-parked with written rationale)

### Innovation Debt Notes

Idea intake engine was not run this cycle (≥ 20 open ideas threshold). 8 out of 22 agents have 0 submissions from IW-20260321-01 remaining in Submitted status — all from IW-20260321-01 have been classified. No innovation debt gap at this time.

### STEP 5 Debate Queue

| IDEA ID | Title | Source |
|---------|-------|--------|
| IDEA-infra-ops-20260304-02 | System Health Check Playbook | stale (cycle-5) |
| IDEA-qa-lead-20260304-01 | Canonical Test Execution Report Template | stale (cycle-5) |
| IDEA-qa-testing-20260321-01 | Integration Test Coverage Report | new (cycle-1) |
| IDEA-qa-testing-20260321-02 | Critical-path Smoke Test (Playwright) | new (cycle-1) |
| IDEA-infra-ops-20260321-02 | Staging Data Reset Script | new (cycle-1) |
| IDEA-finops-20260321-02 | Database Size Monitoring Alert | new (cycle-1) |
| IDEA-base44-frontend-20260321-02 | Alert Notification Badge in Nav | new (cycle-1) |
| IDEA-director-of-quality-20260321-02 | Test Data Seed Script Library | new (cycle-1) |

Queue count: 8. Advancing count: 8. ✅ Match confirmed.

---

## STEP 5 — Debate

**Authorities:** Product Owner (chair) + Challenger (non-decision challenge)

**Strategy constraints restated (per STEP 5 pre-requirement):**
1. All initiatives must stay within the deterministic, single-user decision-support system boundary (§13). No automation, no ML, no external data dependency unless explicitly gated.
2. Zero-sum applies: any item advancing must name a displacement. This run targets backlog-level promotion only (no roadmap-level Adds); displacement is priority-queue ordering within the backlog.

**STEP 5 Debate Queue preflight:** 8 IDEA IDs in queue. All 8 will receive debate entries below before this section is marked complete. ✅

**STEP 5.0.B Score-5 presence check:** No candidate has SPS=5. No veto authority required.

---

### Debate 1 — IDEA-infra-ops-20260304-02 — System Health Check Playbook

**5.0 Required Case (Product Owner):**
1. *Problem:* BLG-OPS-06 (GET /health endpoint) shipped in v2.2, but no operational runbook documents how to use the health signals in practice — what to do when the endpoint reports an error, how to diagnose DB connectivity failures, etc. Users and operators have no guidance.
2. *Strategy intent served:* §3 (human-in-the-loop) — this supports human decision-making when the system signals degraded state. The deterministic system requires humans to respond to monitoring signals; this playbook enables that.
3. *What if we don't:* The health endpoint is deployed but silent in practice — operators cannot respond to its outputs without documented procedures.
4. *Displacement:* BLG-GOV-03 (artefact sealing simplification, P3) is deprioritised in the backlog priority queue. BLG-GOV-03 is internal process improvement; the health playbook has direct operational value.

**5.1 Challenger Counter-Argument:**
Challenger position: Clearance
Evidence: strategy_rules.md §3 (human-in-loop) — reviewed; §13 boundaries — reviewed.
Cleared — this is a pure operational documentation item. SPS=1. No §13 boundary contact. BLG-OPS-06 shipped and the health endpoint is live. A companion playbook is appropriate post-delivery. No strategy boundaries are engaged. Economic constraint: S effort (~0.5–1 day). Opportunity cost is within acceptable range given the direct operational safety value.

**5.2 Product Owner Response:**
Advance ✅ — Challenger's clearance accepted. Playbook is a natural companion to BLG-OPS-06.

**Outcome: ✅ Advance → BLG-OPS-07**

---

### Debate 2 — IDEA-qa-lead-20260304-01 — Canonical Test Execution Report Template

**5.0 Required Case (Product Owner):**
1. *Problem:* BLG-QA-02 (automation readiness assessment) shipped in v2.2. The assessment established a baseline but there is no standard for how test execution results are reported. Each sprint produces ad-hoc test output notes. A canonical template ensures consistency and comparability across cycles.
2. *Strategy intent served:* Governance quality — consistent test reporting supports the Director of Quality's sign-off workflow and makes QA evidence comparable across cycles.
3. *What if we don't:* Test execution reports remain informal and difficult to compare across cycles. QA evidence for DoQ sign-off lacks a standard structure.
4. *Displacement:* BLG-BE-04 (R-Multiple Analysis fix, P3) is deprioritised. The R-Multiple display issue is a minor visual bug; the test report template has broader governance value.

**5.1 Challenger Counter-Argument:**
Challenger position: Clearance
Cleared — QA process governance template, SPS=1. No §13 boundary contact. BLG-QA-02 automation readiness assessment shipped and its recommendations now warrant standardised reporting as a follow-on. strategy_rules.md §3 does not apply to reporting templates. Effort S (~0.5 day). Opportunity cost within acceptable range.

**5.2 Product Owner Response:**
Advance ✅ — gate cleared; follows logically from BLG-QA-02 completion.

**Outcome: ✅ Advance → BLG-QA-03**

---

### Debate 3 — IDEA-qa-testing-20260321-01 — Integration Test Coverage Report

**5.0 Required Case (Product Owner):**
1. *Problem:* The CI pipeline runs integration tests but there is no generated report showing which API endpoints have coverage vs which are untested. As endpoints are added, coverage gaps accumulate silently.
2. *Strategy intent served:* §3 (human-in-loop quality assurance) — makes test coverage visible to humans making release decisions.
3. *What if we don't:* Coverage gaps accumulate silently. The DoQ sign-off is based on partial visibility.
4. *Displacement:* BLG-FE-03 (error message mapping, P3) is deprioritised. Both are P3; coverage visibility has broader governance value than error message polish.

**5.1 Challenger Counter-Argument:**
Challenger position: Clearance
Cleared — CI tooling item, SPS=1. No §13 boundary contact. BLG-QA-02 readiness assessment specifically called out coverage reporting as a next step. strategy_rules.md §3 applies in that this improves human decision-making visibility, not that it restricts the item. Effort M (~1 day). Opportunity cost within acceptable range.

**5.2 Product Owner Response:**
Advance ✅ — directly follows from BLG-QA-02 findings.

**Outcome: ✅ Advance → BLG-QA-04**

---

### Debate 4 — IDEA-qa-testing-20260321-02 — Critical-path Smoke Test (Playwright)

**5.0 Required Case (Product Owner):**
1. *Problem:* BLG-QA-02 shipped and identified that three critical paths (add trade, view portfolio, view alerts) have no automated test coverage. Manual testing on every PR is slow and error-prone as the UI grows. BLG-QA-01 (Playwright for chart scenarios) is already in the backlog; this item adds coverage for the three most-used flows.
2. *Strategy intent served:* §3 (human-in-loop) — the smoke test provides supporting evidence for DoQ sign-off, reducing cognitive load on the human reviewer for basic flow validation.
3. *What if we don't:* Critical path regressions are caught only by manual DoQ review, which misses fast-moving bugs in complex interactions.
4. *Displacement:* BLG-FE-02 (loading state standardisation, P3) is deprioritised. Loading states are a UX polish item; smoke test coverage is a quality safety net.

**5.1 Challenger Counter-Argument:**
Challenger position: **Park** (Type A)
Evidence: strategy_rules.md §3 — human-in-the-loop exit discipline.
Reason: Automated smoke tests risk becoming a de facto hard gate on human confirmation if the Playwright pass/fail is treated as blocking rather than advisory. Specifically: a smoke test failure caused by an unrelated CI infrastructure issue (flaky network, missing seed data) could block a valid release if the pass is treated as a prerequisite for DoQ sign-off rather than supporting evidence. The failure mode is subtle — it would appear as a "quality gate" but would actually be an infrastructure failure preventing human review.
Consequence: If the scope is not explicitly bounded to "supporting evidence — not a DoQ gate replacement," the test suite could erode the human-in-loop principle in practice, even if not by design.

**5.2 Product Owner Response:**
Rebut — Advance ✅
The Challenger's concern is valid but already addressed by the existing scope in BLG-QA-01 and by this item's backlog entry: "DoQ can rely on Playwright pass as primary evidence for non-visual AC; visual AC (colours, ring) remain manual." The AC explicitly states that Playwright pass is primary evidence for non-visual AC only — not a DoQ gate replacement. The distinction between "supporting evidence" and "hard gate" is preserved by design. The AC should be replicated in BLG-QA-05 with the same explicit framing. §3 is upheld: DoQ human sign-off is never replaced by an automated pass.

**Scope note appended:** "Playwright pass is supporting evidence for non-visual AC — not a replacement for DoQ human sign-off. Flaky test failures must not block human review."

**Outcome: ✅ Advance → BLG-QA-05 (with explicit §3 scope constraint)**

*Note: Challenger issued Type A counter-argument — STEP 8.6 guardrail pre-satisfied.*

---

### Debate 5 — IDEA-infra-ops-20260321-02 — Staging Data Reset Script

**5.0 Required Case (Product Owner):**
1. *Problem:* Staging DB accumulates state between QA runs, causing test pollution where one session's data affects the next. BLG-QA-02 flagged reproducible test execution as a gap. A seeded reset script eliminates this class of QA failure.
2. *Strategy intent served:* §3 (human-in-loop quality assurance) — reproducible test execution makes DoQ sign-off more reliable.
3. *What if we don't:* QA runs on staging produce inconsistent results due to accumulated state. DoQ sign-off is less reliable.
4. *Displacement:* TEST-GAP-EPIC-05-SLIP (slippage test scenarios, P3) is deprioritised. Slippage scenarios can be authored after the reset script enables clean staging runs.

**5.1 Challenger Counter-Argument:**
Challenger position: Clearance
Cleared — operational QA infrastructure item, SPS=1. No §13 boundary contact. The item is a direct complement to the BLG-QA-05 smoke test (which needs clean seed data). strategy_rules.md §3 supports this item — reproducible testing enables human sign-off. Effort S (~0.5 day).

**5.2 Product Owner Response:**
Advance ✅

**Outcome: ✅ Advance → BLG-OPS-08**

---

### Debate 6 — IDEA-finops-20260321-02 — Database Size Monitoring Alert

**5.0 Required Case (Product Owner):**
1. *Problem:* The system runs on Render free tier with a Postgres DB size limit. BLG-OPS-06 (health endpoint) shipped and now provides a monitoring hook. Without a size alert, the DB could silently fill to the limit and cause data loss with no warning.
2. *Strategy intent served:* §3 (human-in-loop safety) — the alert surfaces a risk condition for human response; it does not take automated action.
3. *What if we don't:* Silent data loss when DB hits the Render free tier limit. No warning before the system stops accepting writes.
4. *Displacement:* BLG-TECH-05 (Prometheus metrics endpoint, P3) is deprioritised. Prometheus observability is nice-to-have at current scale; DB size monitoring addresses an active data safety risk.

**5.1 Challenger Counter-Argument:**
Challenger position: Clearance
Cleared — lightweight operational monitoring item, SPS=1. No §13 boundary contact. BLG-OPS-06 shipped — the monitoring infrastructure exists. The alert is display-only / notification-only (consistent with §3 human-in-loop). Effort S.

**5.2 Product Owner Response:**
Advance ✅

**Outcome: ✅ Advance → BLG-OPS-09**

---

### Debate 7 — IDEA-base44-frontend-20260321-02 — Alert Notification Badge in Nav

**5.0 Required Case (Product Owner):**
1. *Problem:* BLG-FEAT-12 (alert history table) shipped v2.2. The system now persists a record of all fired alerts. Without a visible nav badge, users must navigate to the Alerts page to discover unacknowledged alerts. A persistent badge provides ambient awareness without requiring proactive navigation.
2. *Strategy intent served:* §3 (human-in-loop) — the badge surfaces unacknowledged alert state to the human user; it does not trigger any automated action.
3. *What if we don't:* Unacknowledged alerts are invisible unless the user navigates to the Alerts page. The alert system loses discoverability value.
4. *Displacement:* BLG-FE-04 (alert thresholds CTA button, P3 XS) is deprioritised. Both are small; the badge has higher daily-use value.

**5.1 Challenger Counter-Argument:**
Challenger position: Clearance
Cleared — frontend UX enhancement, SPS=2 (alert system adjacent — displays, not generates alert state). strategy_rules.md §3 is not violated: the badge reads existing alert state and presents it to the human; no automated action is triggered. §13 boundary review: no automation, no external data, no strategy modification. BLG-FEAT-12 shipped — the underlying alert history data is available. Effort S.

**5.2 Product Owner Response:**
Advance ✅

**Outcome: ✅ Advance → BLG-FE-05**

---

### Debate 8 — IDEA-director-of-quality-20260321-02 — Test Data Seed Script Library

**5.0 Required Case (Product Owner):**
1. *Problem:* BLG-QA-02 (automation readiness assessment) shipped and identified that reproducible test data is a prerequisite for automation. Ad-hoc seed data in each test author's environment means tests cannot be run by others or in CI without environment-specific setup.
2. *Strategy intent served:* §3 (human-in-loop quality assurance) — reproducible, shareable seed scripts enable consistent DoQ sign-off across environments.
3. *What if we don't:* Test automation (BLG-QA-01, BLG-QA-05) cannot run reliably in CI without seed data. The readiness assessment's recommendations are unactionable.
4. *Displacement:* BLG-OPS-05 (API performance baseline, P3 S) is deprioritised. Both are P3; seed scripts are a prerequisite for the smoke test work.

**5.1 Challenger Counter-Argument:**
Challenger position: Clearance
Cleared — QA infrastructure item, SPS=1. No §13 boundary contact. BLG-QA-02 readiness assessment specifically identified test data reproducibility as a gap; this item directly implements that recommendation. The item is scoped to three domains (alerts, watchlists, chart-interactivity) — not unbounded QA infrastructure investment. Effort S–M.

**5.2 Product Owner Response:**
Advance ✅

**Outcome: ✅ Advance → BLG-QA-06**

---

### STEP 5 Debate Queue Verification

| IDEA ID | Debate entry present | Outcome |
|---------|---------------------|---------|
| IDEA-infra-ops-20260304-02 | ✅ | Advance → BLG-OPS-07 |
| IDEA-qa-lead-20260304-01 | ✅ | Advance → BLG-QA-03 |
| IDEA-qa-testing-20260321-01 | ✅ | Advance → BLG-QA-04 |
| IDEA-qa-testing-20260321-02 | ✅ | Advance → BLG-QA-05 |
| IDEA-infra-ops-20260321-02 | ✅ | Advance → BLG-OPS-08 |
| IDEA-finops-20260321-02 | ✅ | Advance → BLG-OPS-09 |
| IDEA-base44-frontend-20260321-02 | ✅ | Advance → BLG-FE-05 |
| IDEA-director-of-quality-20260321-02 | ✅ | Advance → BLG-QA-06 |

Queue count: 8. Debate entries: 8. ✅ All queue items debated.

All 8 candidates: ✅ Advance. No Parks. No Rejects.

---

## STEP 6 — Scoring Matrix Overlay

**Authority:** Facilitator

*Scoring scale: 1 (low/poor) → 5 (high/excellent). WF Intensity: 1=high effort, 5=hours only. TTV: 1=slow, 5=immediate.*

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-OPS-07 System Health Check Playbook | 2 | 2 | 3 | 5 | 5 | 5 | 1 | S |
| BLG-QA-03 Canonical Test Execution Report Template | 2 | 2 | 3 | 5 | 5 | 5 | 1 | S |
| BLG-QA-04 Integration Test Coverage Report | 3 | 2 | 4 | 4 | 4 | 5 | 1 | M |
| BLG-QA-05 Critical-path Smoke Test (Playwright) | 4 | 2 | 4 | 3 | 4 | 4 | 1 | M |
| BLG-OPS-08 Staging Data Reset Script | 3 | 2 | 4 | 5 | 5 | 5 | 1 | S |
| BLG-OPS-09 Database Size Monitoring Alert | 3 | 3 | 5 | 5 | 5 | 5 | 1 | S |
| BLG-FE-05 Alert Notification Badge | 3 | 3 | 2 | 5 | 4 | 5 | 2 | S |
| BLG-QA-06 Test Data Seed Script Library | 3 | 2 | 4 | 4 | 4 | 5 | 1 | S–M |

**Facilitator observations:**
- Highest-value items: BLG-OPS-09 (data safety, risk=5), BLG-QA-05 (quality safety net, strat=4), BLG-QA-04 (coverage visibility)
- All items SPS=1 or SPS=2 — no strategy boundary proximity
- All items S or M effort — quick wins at v2.3
- All items high reversibility (5) — low lock-in risk
- Release planning should sequence BLG-OPS-08 (seeds) before BLG-QA-05 (smoke test) and BLG-QA-04 (coverage report) as it is a prerequisite

---

## STEP 7 — Workforce Economics Gate

**Authority:** FinOps & Resource Architect

### FTE Estimates — New Backlog Items

| Item | Effort | Skill domain | FTE-days |
|------|--------|-------------|----------|
| BLG-OPS-07 | S | Documentation (Infrastructure & Ops) | ~0.5 |
| BLG-QA-03 | S | QA process governance | ~0.5 |
| BLG-QA-04 | M | Engineering / CI | ~1.0 |
| BLG-QA-05 | M | QA / Frontend automation | ~2.0 |
| BLG-OPS-08 | S | Infrastructure / DevOps | ~0.5 |
| BLG-OPS-09 | S | Infrastructure / Backend | ~0.5 |
| BLG-FE-05 | S | Frontend | ~0.5 |
| BLG-QA-06 | S–M | QA / Backend | ~1.0 |
| **Total new** | | | **~6.5 days** |

Combined with existing 15 active backlog items (~30–40 days total estimated), v2.3 pool now represents ~37–47 days of estimated work. This is larger than a typical sprint capacity — release planning will need to scope a realistic sprint plan from this pool.

**Skill domain summary (new items):**
- QA / Test automation: 4 items (~4.5 days) — dominant skill domain
- Infrastructure / Ops: 3 items (~1.5 days)
- Frontend: 1 item (~0.5 days)

**No scarce skill conflicts** identified. QA automation skill is already represented by BLG-QA-01 (Playwright — existing) and BLG-QA-02 (readiness assessment shipped).

### Skill-Silo Alert (§7.1)

- Governance-heavy items in this cycle's new additions: 0 (all execution-heavy)
- **Governance load %:** 0% (well below 60% ceiling — no Skill-Silo Alert)
- **Sign-off capacity floor check (governance load < 20%):** Governance load is 0% for new additions.
  - Product Owner must confirm adequate review and sign-off capacity for v2.3 volume.
  - *PO confirmation: v2.3 will be scoped by release planning; review capacity is not constrained at this time. No critical spec approvals or decision records are deferred without acknowledgement. Sign-off capacity confirmed.* ✅
  - Note: This advisory is recorded per §7.1. No governance capacity risk triggered.

---

## STEP 8 — Final Rebalance Decision

**Authority:** Product Owner

### Per-initiative decisions

| Item | Decision | Rationale |
|------|----------|-----------|
| BLG-OPS-07 | ➕ Add (backlog) | Health playbook follows BLG-OPS-06 delivery. S effort, high operational value. |
| BLG-QA-03 | ➕ Add (backlog) | Test report template follows BLG-QA-02 readiness. S effort, governance value. |
| BLG-QA-04 | ➕ Add (backlog) | Integration coverage report follows BLG-QA-02 findings. M effort. |
| BLG-QA-05 | ➕ Add (backlog) | Critical-path smoke test follows BLG-QA-02 readiness. M effort. §3 scope constraint recorded. |
| BLG-OPS-08 | ➕ Add (backlog) | Staging reset script follows BLG-QA-02 findings. S effort. |
| BLG-OPS-09 | ➕ Add (backlog) | DB size monitoring follows BLG-OPS-06 delivery. S effort. Active data safety risk. |
| BLG-FE-05 | ➕ Add (backlog) | Alert badge follows BLG-FEAT-12 delivery. S effort. |
| BLG-QA-06 | ➕ Add (backlog) | Test data seed library follows BLG-QA-02 findings. S–M effort. |
| Roadmap-level initiatives | No-change | Zero active initiatives. No roadmap-level Add, Replace, Defer, or Kill required. Gated items remain gated. Delivery Plan (§3) to be updated with v2.3 horizon note. |

**Roadmap level:** 0 Adds. Net-zero: 0 Adds ≤ 0 Kills ✅.

**Displacement candidate flag (no changes to prior):** No active initiatives; displacement candidate tracking not applicable this cycle. Existing initiative_register.md displacement notes remain in place.

### Skill-Silo Check (recorded per completion condition)

Governance load: 0% of new FTE additions are governance-heavy. Below 20% floor. PO sign-off capacity confirmed. No governance capacity risk. No Skill-Silo Alert.

### Carry-Forward Advisories (STEP 0 — from v2.2 closure)

| # | Item | Status at this rebalance |
|---|------|--------------------------|
| 1 | Sprint planning `blocked_decision` items without prior HoST design session | Advisory noted. No roadmap-level action required; Sprint Planning engine should surface advisory when scheduling. Deferred patch targeting sprint_planning_prompt.md already exists in v2.2 closure outstanding actions. |
| 2 | Delegation log not updated in-flight | Advisory noted. Deferred patch targeting execution_prompt.md already exists in v2.2 closure outstanding actions. |
| 3 | Backlog ID uniqueness scan missing (LL-RP-v22-01) | Advisory noted. Deferred patch targeting backlog_management_prompt.md already in v2.2 closure. GROOM-20260324-01 applied a manual scan and resolved the duplicate IDs. Patch still needed in engine. |

These carry-forward advisories are informational — no blocking action required at this roadmap rebalance. All three have active deferred patches in the v2.2 closure record.

---

## STEP 8.5 — Stateless Write Safety Gate

### 8.5.A Context Re-Anchoring

Disregarding all debate prose. Re-anchoring to:
- STEP 8 decisions: 8 backlog-level Adds (BLG-OPS-07/08/09, BLG-QA-03/04/05/06, BLG-FE-05); 0 roadmap-level changes; roadmap §3 v2.3 horizon note; initiative_register.md no-change.
- Existing on-disk content: current_roadmap.md (§3 empty, v2.3 next release noted), backlog.md (15 active items), decision_log.md (DL-011 is latest), workforce_capacity.md, initiative_register.md.

### 8.5.B Write Plan

| File | Action | Reason | Traceability |
|------|--------|--------|--------------|
| `claude/cycles/2026-03-24__scheduled/run_manifest.md` | Create | STEP 1 required output | STEP 1.1 |
| `claude/cycles/2026-03-24__scheduled/cycle_record.md` | Create | STEP 2–8 working content | STEPS 2–8 |
| `claude/scoring/scored_initiatives.md` | Modify (append) | STEP 6 scoring matrix | STEP 6 — 8 new items scored |
| `claude/ideas/ideas_register.md` | Modify | §4.2 document management — Status updates for 40 rows | STEP 4 and STEP 5 decisions |
| `claude/backlog/backlog.md` | Modify | Reconcile — add 8 new items | STEP 8 — 8 backlog Adds |
| `claude/roadmap/decision_log.md` | Append-only | Record DL-012 — scheduled run | STEP 8 — No-change + 8 backlog Adds |
| `claude/roadmap/current_roadmap.md` | Modify | Update Last Updated + §3 v2.3 horizon note; Last rebalance date | STEP 8 / STEP 9 lifecycle compliance |
| `claude/roadmap/initiative_register.md` | Modify | Update Last Updated + note v2.2 completion | STEP 9 lifecycle compliance |
| `claude/roadmap/workforce_capacity.md` | Modify (append) | STEP 7 economics for 8 new items | STEP 7 |
| `claude/cycles/2026-03-24__scheduled/cycle_summary.md` | Create | STEP 10 required output | STEP 10 |
| `claude/cycles/2026-03-24__scheduled/lessons_learnt.md` | Create | STEP 11 required output | STEP 11 |
| `claude/cycles/2026-03-24__scheduled/meta_review.md` | Create | STEP 11.4 meta-review due (3rd cycle) | STEP 11.4 |
| `.claude_current_state.json` | Modify | STEP 12 state update | STEP 12.1 |

### 8.5.B Register Row Verification (LL-02-patch)

8 rows marked Advancing in §4.2:
- IDEA-infra-ops-20260304-02 → BLG-OPS-07 (Promoted-Added)
- IDEA-qa-lead-20260304-01 → BLG-QA-03 (Promoted-Added)
- IDEA-qa-testing-20260321-01 → BLG-QA-04 (Promoted-Added)
- IDEA-qa-testing-20260321-02 → BLG-QA-05 (Promoted-Added)
- IDEA-infra-ops-20260321-02 → BLG-OPS-08 (Promoted-Added)
- IDEA-finops-20260321-02 → BLG-OPS-09 (Promoted-Added)
- IDEA-base44-frontend-20260321-02 → BLG-FE-05 (Promoted-Added)
- IDEA-director-of-quality-20260321-02 → BLG-QA-06 (Promoted-Added)

All 8 Advancing rows accounted for in write plan. ✅

### 8.5.C Verification

- All files within Section 5 write scope: ✅
- Every write traceable to STEP 8 decision or lifecycle compliance: ✅
- No formatting-only edits: ✅
- Decision log append-only, duplicate-checked: ✅ (DL-012 is new)
- Backlog edits reconciliation-only: ✅ (add new items only)
- PoG documents: Not applicable (no Score-5 items)
- Hard gate "complete" markings: Not applicable
- Displacement candidate flags written to initiative_register.md only: ✅ Not applicable (no displacement candidates)
- Effort bands recorded for all new items: ✅ (in scored_initiatives.md)
- Action-now prompt patches: Not applicable (no action-now patches this run)
- Deferred prompt patches: Not applicable (no new deferred patches this run)
- Meta-review: ✅ Due and conducted — meta_review.md to be created

Write plan passes. Proceed to STEP 9. ✅

---

## STEP 8.6 — Run-Level Disagreement Guardrail

Check:
1. Candidate parked or rejected? — None parked or rejected in STEP 5.
2. Challenger issued a Type A counter-argument? — **Yes.** IDEA-qa-testing-20260321-02 (Debate 4) received a Type A counter-argument from Challenger citing §3 human-in-loop risk. PO rebutted with valid evidence and maintained Advance.
3. Single-candidate run? — No (8 candidates).

**Guardrail: PASSES** (condition 2 satisfied). ✅ Proceed to STEP 9.
