Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.0
Cycle: 2026-04-25__release-v3.0
Last Updated: 2026-04-25

---

# Release Plan — v3.0 Arc 1 Remainder: Screener Engine & Results Page

---

## Readiness

**Release:** v3.0 | **Prior release:** v2.9 (Verified_with_deviations, 2026-04-24) | **Velocity:** 1.00 (6-cycle rolling)

**Prerequisite specs confirmed present:**
- BLG-SPEC-21: Screener Engine Spec ✅ (v2.9 ST-01)
- BLG-SPEC-22: Alpaca API Integration Contract ✅ (v2.9 ST-02)
- BLG-SPEC-23: Screener Internal API Contract ✅ (v2.9 ST-03)
- screener_results.md: DS-02 UX Spec ✅ (v2.9 ST-04, BLG-FE-17)
- BLG-QA-08: Mock Harness ✅ (v2.9 ST-09)
- BLG-QA-09: Screener Test Data Library ✅ (v2.9 ST-10)
- DS-05: Alpaca Integration Service ✅ (v2.9 ST-05/ST-06)
- DS-03: Sector Classification ✅ (v2.9 ST-07)

**Infrastructure baseline:** sector_service.py, alpaca_service.py, yahoo_finance_service.py all operational post-v2.9.

Backlog Age Advisory: PASS — no spec/doc debt items aged 2+ cycles without story assignment.
Provisional-Target Advisory: 6 items Provisional-Target: v3.0 in scope; 4 deferred.
Design-Gate Language Scan: 0 items flagged. DS-02 fully specced via screener_results.md.

---

## Scope

### Items in scope

| S2-ID | EPIC | Description | Source | Effort |
|-------|------|-------------|--------|--------|
| S2-01 | EPIC-01 | DS-01 Strategy-Rules Screener Engine — ticker universe, OHLCV pipeline, ATR + regime + signal scoring, batch orchestration, API endpoints | Roadmap Arc 1 | H |
| S2-02 | EPIC-02 | DS-02 Screener Results Page — frontend implementation per screener_results.md | Roadmap Arc 1 | M |
| S2-03 | EPIC-02 | DS-07 Watchlist Promotion Flow — one-click screener → watchlist promotion | Roadmap Arc 1 | S |
| S2-04 | EPIC-02 | BLG-FE-18 Screener News Panel Attachment — wire GET /news/{ticker} to screener results page per screener_results.md §9 | Backlog v3.0 | S |
| S2-05 | EPIC-03 | BLG-OPS-12 External API Health Check Extension — Alpaca + YF status in GET /health | Backlog v3.0 | S |
| S2-06 | EPIC-03 | BLG-OPS-14 AI Journal Monitoring Metrics — AI usage/error/latency in GET /health | Backlog v3.0 | S |
| S2-07 | EPIC-03 | TEST-GAP-ST14 AI Audit Service Unit Tests — ai_audit_service.py unit test coverage | Backlog | S |
| S2-08 | EPIC-03 | BLG-FE-19 Keyboard Shortcuts — 'n', 'w', 'r' shortcut keys for trading actions | Backlog v3.0 | S |
| S2-09 | EPIC-04 | v2.9 Deferred Patch: execution_prompt.md §2 — EPIC execution_state.json owner designation | v2.9 Friction Item 1 | S |
| S2-10 | EPIC-04 | v2.9 Deferred Patch: execution_prompt.md §3.1.A — test_scenarios field population note | v2.9 Friction Item 2 | S |
| S2-11 | EPIC-04 | OA-v29-01: prompt_change_log.md retrospective entries for sprint_planning_prompt.md | v2.9 OA | S |
| S2-12 | EPIC-04 | BLG-FEAT-18 Consecutive Losing Streak Metric — analytics + metrics spec entry | Backlog v3.0 | S |
| S2-13 | EPIC-04 | BLG-AI-02 Model Version Contract for AI Journal — Claude model version document | Backlog v3.0 | S |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| DS-04 Earnings Calendar Integration | No spec exists; independent of screener engine flow; M effort | v3.1 |
| BLG-FEAT-13 Feature Flags | P3, M effort; lower priority than Arc 1 delivery | v3.1 |
| BLG-FEAT-19 Monthly P&L Summary | P2, S effort; Arc 2 reporting scope | v3.1 |
| BLG-FE-16 React Component Inventory | P3, M effort; capacity constraint | v3.1 |
| BLG-GOV-11 Cycle Artefact Inventory | P3, M effort; capacity constraint | v3.1 |
| BLG-OPS-13 API Performance Baseline | Requires live environment; human coordination | Ops OA |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-04-25__release-v3.0

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sprint | Sequencing constraint |
|---------|-------------|-------|----------|--------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering + Backend Engineering Patterns Owner | RISK-01 | Sprint 1 | No hard prerequisites (DS-05/DS-03 shipped v2.9) |
| EPIC-02 | S2-02, S2-03, S2-04 | Base44 Frontend Prompt Owner | RISK-02 | Sprint 2 | After EPIC-01 (needs GET /screener/results endpoint) |
| EPIC-03 | S2-05, S2-06, S2-07, S2-08 | Infrastructure & Operations Owner + QA & Testing Owner | RISK-03 | Sprint 2 | Independent of EPIC-01/02 |
| EPIC-04 | S2-09, S2-10, S2-11, S2-12, S2-13 | Head of Specs Team + PMO Lead | — | Sprint 1 | Independent of Arc 1 EPICs |

**EPIC-01 note:** DS-01 is the heaviest EPIC in v3.0 (H effort). Ticker universe model (ST-01) must ship before batch engine work (ST-02/ST-03) to avoid schema churn. Screener API endpoints (ST-04) are the hand-off to EPIC-02.

**EPIC-02 note:** EPIC-02 cannot begin until EPIC-01 ST-04 is merged to main. Design gate must pass before Sprint 2 opens. BLG-FE-18 (ST-07) is display-only per BLG-GOV-16 §13 sign-off conditions; Strategy Rules Owner counter-sign required.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | DS-01 implementation complexity — OHLCV pipeline + ATR + regime + signal scoring is the most complex backend work to date; BLG-SPEC-21 provides guidance but edge cases may surface during implementation | Medium | BLG-SPEC-21 + BLG-SPEC-22 + BLG-QA-09 provide strong scaffolding; BLG-QA-08 mock harness enables CI testing without live API; sector_service/alpaca_service baseline operational | null |
| RISK-02 | EPIC-02 | EPIC-02 hard dependency on EPIC-01 — screener frontend cannot be developed until GET /screener/results contract is delivered and stable; any EPIC-01 slip cascades to EPIC-02 | Medium | Serialised sprint plan (EPIC-01 Sprint 1, EPIC-02 Sprint 2); BLG-SPEC-23 defines the API contract explicitly — frontend can begin component work against contract before backend lands | null |
| RISK-03 | EPIC-03 | BLG-FE-19 keyboard shortcuts may interfere with existing text input fields — requires careful event handling | Low | Acceptance criteria explicitly includes "shortcuts do not interfere with text input fields"; implementable with input-focus guard in event handler | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**S2-ID completeness:** 13 scope items, all assigned S2-01 through S2-13 ✅
**EPIC-ID completeness:** 4 EPICs (EPIC-01 through EPIC-04), all with Maps-to S2 items ✅
**RISK-ID completeness:** 3 risks registered; all referenced in EPIC table ✅
**S2→EPIC mapping:** Every S2 item maps to exactly one EPIC ✅
**EPIC→S2 coverage:** Every EPIC covers at least one S2 item ✅
**Deferred item list complete:** 6 items explicitly deferred with reasons ✅

stage3_5_model_integrity: **PASS**
attributes.plan_executable: true

---

## Capacity Check

**Effort estimates (from roadmap + backlog):**

| EPIC | Stories | Effort Band | Estimated days |
|------|---------|-------------|----------------|
| EPIC-01 | ST-01–ST-04 (4) | H (roadmap) | ~4–6 days |
| EPIC-02 | ST-05–ST-07 (3) | M + S + S | ~2–3 days |
| EPIC-03 | ST-08–ST-11 (4) | 4 × S | ~2 days |
| EPIC-04 | ST-12–ST-16 (5) | 5 × S | ~2–3 days |
| **Total** | **16 stories** | — | **~10–14 days** |

**Effort band sources:** DS-01=H (roadmap table); DS-02=M (roadmap); DS-07/BLG-FE-18=S; BLG-FE-19=S (scored_initiatives.md); BLG-OPS-14=S (scored_initiatives.md); all others=S (backlog items).

**Historical capacity baseline:** v2.9 = 15 stories delivered at 1.00 velocity; v2.7/v2.8 = 11/8 stories at 1.00. Rolling 6-cycle velocity: 1.00.

**Assessment:** Total estimated effort (~10–14 days) is within the 2-sprint delivery window at historical velocity. EPIC-01 (H effort) is the primary capacity risk. Sprint 1 (EPIC-01 + EPIC-04 = 9 stories, ~6–9 days) is the heavier sprint.

**Outcome:** WARN — DS-01 (H effort) and 16 total stories is the most ambitious scope since v1.10. Historical velocity supports delivery but DS-01 implementation depth should be scoped conservatively at sprint planning (ST-02/ST-03 may be split further if needed).

### Phasing Recommendation

Total estimated effort mid-point: ~12 days. 2-sprint plan:

- **Sprint 1 (EPIC-01 + EPIC-04):** ST-01 through ST-04 (backend engine) + ST-12 through ST-16 (governance/deferred patches) — estimated ~6–9 days. EPIC-04 is fully independent and can run in parallel with EPIC-01.
- **Sprint 2 (EPIC-02 + EPIC-03):** ST-05 through ST-11 (screener frontend + ops/QA/shortcuts) — estimated ~4–5 days. EPIC-02 requires EPIC-01 ST-04 merged to main before Sprint 2 opens; design gate should run between sprints.

Ordering rationale: EPIC-01 first because EPIC-02 depends on it; EPIC-04 governance patches are independent and unblock prompt improvements before execution begins; EPIC-03 ops/QA items are independent and suitable for Sprint 2 alongside frontend work.

stage4_5_capacity_check: **WARN** (standard mode — warn allowed)
attributes.capacity_feasible: warn

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**S2→EPIC→ST mapping verification:**

| S2-ID | EPIC | Sprint | ST | Status |
|-------|------|--------|----|--------|
| S2-01 | EPIC-01 | 1 | ST-01, ST-02, ST-03, ST-04 | ✅ |
| S2-02 | EPIC-02 | 2 | ST-05 | ✅ |
| S2-03 | EPIC-02 | 2 | ST-06 | ✅ |
| S2-04 | EPIC-02 | 2 | ST-07 | ✅ |
| S2-05 | EPIC-03 | 2 | ST-08 | ✅ |
| S2-06 | EPIC-03 | 2 | ST-09 | ✅ |
| S2-07 | EPIC-03 | 2 | ST-10 | ✅ |
| S2-08 | EPIC-03 | 2 | ST-11 | ✅ |
| S2-09 | EPIC-04 | 1 | ST-12 | ✅ |
| S2-10 | EPIC-04 | 1 | ST-13 | ✅ |
| S2-11 | EPIC-04 | 1 | ST-14 | ✅ |
| S2-12 | EPIC-04 | 1 | ST-15 | ✅ |
| S2-13 | EPIC-04 | 1 | ST-16 | ✅ |

**Every S2 item has at least one ST ✅**
**No orphan STs ✅**
**EPIC sprint assignments consistent with phasing recommendation ✅**
**RISK IDs all referenced in EPIC table ✅**
**No deferred item appears in scope table ✅**

stage5_5_cross_stage_integrity: **PASS**
attributes.cross_stage_integrity: pass

---

## Integrity Validation — 5.7 Decision Record Integrity

Decisions record created: `docs/product/decisions/decisions--2026-04-25__release-v3.0.md`

**Scope decisions:**
- DS-04 deferral documented ✅
- BLG-FEAT-13/19/FE-16/GOV-11 deferrals documented ✅
- BLG-OPS-13 Ops OA documented ✅

**Sequencing decisions:**
- EPIC-01 before EPIC-02 (hard dependency) ✅
- EPIC-04 in Sprint 1 (parallel to EPIC-01, independent) ✅
- Design gate between Sprint 1 and Sprint 2 ✅

**Accepted risks:** None — all risks mitigated at planning level; no Accepted Risk escalations.

stage5_7_decision_record_integrity: **PASS**
attributes.decisions_validated: pass
