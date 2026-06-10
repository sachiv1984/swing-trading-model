**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Published
**Last Updated:** 2026-06-10
**Cycle:** 2026-06-10__release-v5.5

---

# Backlog Slice — v5.5

<!-- release-plan-marker: RP:v5.5:2026-06-10__release-v5.5 -->

**Release:** v5.5
**Cycle:** 2026-06-10__release-v5.5
**Total stories:** 14 firm (10 Sprint 1, 4 Sprint 2)
**Conditional stories:** 0

---

## EPIC-01: Governance Prompt Hardening

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Head of Specs Team
**Sprint:** 1

Resolves all three v5.4 lessons-learnt carry-forwards requiring governance prompt updates. Each story modifies a different governed prompt; CLAUDE.md §6 checklist applies to each.

### ST-01 — sprint_planning_prompt.md within-sprint date gate advisory

**Source:** BLG-GOV-116
**Priority:** P2
**Effort:** S (~0.5 day)
**Maps to:** S2-01 / EPIC-01

**Acceptance Criteria**
- sprint_planning_prompt.md updated: stories with a within-sprint date gate must be marked `Status at sprint open: conditional — gate <date>` in sprint_backlog.md at planning time
- Version bumped per CLAUDE.md §6: §14 OPERATIONAL_GUIDE updated; prompt_change_log.md entry appended
- Head of Specs Team sign-off

---

### ST-02 — execution_prompt.md pr_status read-after-open improvement

**Source:** BLG-GOV-117
**Priority:** P2
**Effort:** S (~0.5 day)
**Maps to:** S2-02 / EPIC-01

**Acceptance Criteria**
- execution_prompt.md updated: after `gh pr create`, immediately read `gh pr view <number> --json state,mergeStateStatus` and write the actual state to execution_state.json
- Version bumped; OPERATIONAL_GUIDE §14 updated; prompt_change_log.md entry appended per CLAUDE.md §6
- Head of Specs Team sign-off

---

### ST-03 — qa_evidence commit discipline advisory in execution_prompt.md

**Source:** BLG-GOV-118
**Priority:** P2
**Effort:** S (~0.5 day)
**Maps to:** S2-03 / EPIC-01

**Acceptance Criteria**
- execution_prompt.md updated: advisory added before PR-opening step: "verify qa_evidence_EPIC-xx.md is committed to the EPIC branch before opening the PR"
- Version bumped; OPERATIONAL_GUIDE §14 updated; prompt_change_log.md entry appended per CLAUDE.md §6
- Head of Specs Team sign-off

---

## EPIC-02: Trade Data Density Visibility

**Maps to:** S2-04, S2-05
**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner
**Sprint:** 1

Introduces a backend gate-monitoring view and a visible trade count display. Multiple high-value features (PT-04, SI-02 frontend, Arc 6) are gated on trade counts currently invisible between sprint planning sessions.

### ST-04 — Trade count gate-monitoring view (backend)

**Source:** BLG-BE-34
**Priority:** P2
**Effort:** S (~0.5 day)
**Maps to:** S2-04 / EPIC-02

**Acceptance Criteria**
- Database view or PostgreSQL function `get_gate_metrics()` created, returning: closed_trades_count, closed_trades_with_plans, active_positions_count, ai_journal_entry_count (if table exists), oldest_trade_date, newest_trade_date
- Optionally: `GET /portfolio/gate-metrics` endpoint (read-only) exposing the view — if endpoint added, must be registered in backend/routers/test.py and openapi.yaml per CLAUDE.md §2
- Data Model & Domain Schema Owner sign-off
- Unit test covers at least the happy-path query result shape

---

### ST-05 — Trade data density progress tracker (frontend display)

**Source:** BLG-GOV-120
**Priority:** P2
**Effort:** S (~0.5 day)
**Maps to:** S2-05 / EPIC-02
**Depends on:** ST-04 (backend view/endpoint)

**Acceptance Criteria**
- Trade count display added to System Status page OR added as a data density line in SI-05 weekly digest template: "Closed trades: N / Gate 1: 20 / Gate 2: 50 / Gate 3: 100"
- Count queries real production data (not hardcoded); sources ST-04 view or direct query
- If System Status page: Playwright scenario covers trade count display OR human staging sign-off recorded with date
- If System Status fallback count updated: SC-SS-01b in tests/e2e/system-status.spec.js updated per CLAUDE.md §2
- Infrastructure & Operations Owner sign-off

---

## EPIC-03: API Baseline & Documentation Clearance

**Maps to:** S2-06, S2-07, S2-08, S2-09, S2-10
**Owner:** Infrastructure & Operations Owner; QA Lead; Head of UX & Design
**Sprint:** 1

Clears the long-outstanding API performance baseline backlog (endpoints from v2.8 through v5.4), produces the formal QA regression baseline, and delivers the SI-05 UX journey map.

### ST-06 — v2.8–v4.6 endpoint performance baseline re-run (24 endpoints)

**Source:** BLG-OPS-13
**Priority:** P3
**Effort:** M (~2 days)
**Maps to:** S2-06 / EPIC-03

**Acceptance Criteria**
- All 24 endpoints from v2.8–v4.6 (as listed in BLG-OPS-13 source) have baseline rows added to docs/ops/api_performance_baseline.md
- Measurements made against live/staging environment (p50/p95/p99 + any threshold flags)
- Infrastructure & Operations Owner sign-off

---

### ST-07 — v5.1–v5.4 endpoint baseline extension

**Source:** BLG-OPS-61
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Maps to:** S2-07 / EPIC-03

**Acceptance Criteria**
- v5.1–v5.4 new endpoints added to api_performance_baseline.md (POST /digest/si05/send + paper-positions enhancements + any v5.2 routes from BLG-SPEC-49–52 not already present)
- Measurements made against live environment
- Infrastructure & Operations Owner sign-off

---

### ST-08 — POST /digest/si05/send to api_performance_baseline.md

**Source:** BLG-OPS-54
**Priority:** P3
**Effort:** XS (~1–2 hours)
**Maps to:** S2-08 / EPIC-03

**Note:** May overlap with ST-07 (BLG-OPS-61) — if ST-07 already includes this endpoint, ST-08 is trivially complete. Sprint Planning to confirm and merge into ST-07 if appropriate.

**Acceptance Criteria**
- POST /digest/si05/send present in api_performance_baseline.md with baseline measurements recorded (p50/p95/p99)
- Measurements from live/staging environment
- Infrastructure & Operations Owner sign-off

---

### ST-09 — Formal regression test suite baseline document

**Source:** BLG-QA-50
**Priority:** P3
**Effort:** S (~0.5 day)
**Maps to:** S2-09 / EPIC-03

**Acceptance Criteria**
- Formal regression baseline document created in docs/qa/ or docs/testing/
- All backend/routers/test.py entries mapped to features with version history
- All tests/e2e/*.spec.js files listed with scenario count and feature mapping
- Director of Quality sign-off

---

### ST-10 — User journey map: SI-05 Telegram digest to app action

**Source:** BLG-FE-65
**Priority:** P3
**Effort:** S (~1 day)
**Maps to:** S2-10 / EPIC-03

**Acceptance Criteria**
- User journey map document produced: entry points (links in digest), navigation steps to relevant app screen, friction findings
- Any significant friction filed as a separate backlog item
- Head of UX & Design sign-off

---

## EPIC-04: SI-05 Effectiveness Review & UX Pre-work

**Maps to:** S2-11, S2-12, S2-13, S2-14
**Owner:** Head of UX & Design; Infrastructure & Operations Owner; Product Owner; Metrics Definitions & Analytics Owner
**Sprint:** 2
**Sprint 2 gate:** All S2-12/13/14 stories gated on 2026-07-04 SI-05 effectiveness review; S2-11 gated on 2026-06-21

### ST-11 — Red Flag Journal visual design review pre-brief (gate 2026-06-21)

**Source:** BLG-FE-64
**Priority:** P2
**Effort:** S (~0.5 day)
**Maps to:** S2-11 / EPIC-04
**Gate:** SI-03 Red Flag Journal live ≥ 30 days — clears 2026-06-21
**Status at sprint open: conditional — gate 2026-06-21**

**Acceptance Criteria**
- Design review brief produced for BLG-FE-41: scope (filters UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, expected deliverable
- Brief reviewed by Head of UX & Design; sign-off recorded
- Gate confirmed (2026-06-21 or later) before work begins

---

### ST-12 — SI-05 p99 production latency baseline review (gate ≥2026-07-04)

**Source:** BLG-OPS-59
**Priority:** P2
**Effort:** S (~0.5 day)
**Maps to:** S2-12 / EPIC-04
**Gate:** ≥2026-07-04 (4 weeks of production operation)
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria**
- p99 latency extracted from Render logs for POST /digest/si05/send after ≥2026-07-04
- Compared against BLG-OPS-54 pre-launch baseline
- PASS (p99 < 2× baseline) or performance investigation item filed
- Infrastructure & Operations Owner sign-off

---

### ST-13 — SI-05 digest weekly cadence review (gate 2026-07-04)

**Source:** BLG-GOV-112
**Priority:** P2
**Effort:** S (~0.5 day)
**Maps to:** S2-13 / EPIC-04
**Gate:** 2026-07-04 SI-05 effectiveness review complete
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria**
- Cadence review document produced after 2026-07-04 effectiveness review
- Recommendation made with data backing (si05_digest_log delivery count, BLG-GOV-96 criteria assessment)
- Recommendation: maintain weekly / move to bi-weekly / adaptive cadence
- Product Owner sign-off

---

### ST-14 — SI-05 digest actionability metric definition (gate 2026-07-04)

**Source:** BLG-GOV-115
**Priority:** P2
**Effort:** S (~0.5–1 day)
**Maps to:** S2-14 / EPIC-04
**Gate:** 2026-07-04 effectiveness review (BLG-GOV-113 protocol) complete
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria**
- 2–4 actionability metrics formally defined with data source mapping (si05_digest_log, red_flag_events, trade data)
- Metrics document reviewed by Metrics Definitions & Analytics Owner
- Gate condition verified (2026-07-04 review complete before authoring)
- Metrics feed BLG-GOV-112 cadence review and BLG-GOV-96 effectiveness criteria

---
