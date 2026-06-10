**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-10
**Cycle:** 2026-06-10__release-v5.5

---

# Sprint Backlog — v5.5

**Cycle:** 2026-06-10__release-v5.5
**Sprint 1 stories:** 10 (EPIC-01, EPIC-02, EPIC-03)
**Sprint 2 stories:** 4 (EPIC-04, gated)
**Total:** 14 firm

---

## Sprint Scope

### Merge Order (Sprint 1)

**EPIC-01 → EPIC-02 → EPIC-03**

- `execution_state.json` owner: **EPIC-01** (first EPIC in execution order)
- EPIC-02 and EPIC-03 must check for `execution_state.json` before creating; read and append their section if found
- No shared source files across EPICs — no rebase ordering constraint for shared files
- Sprint 2: EPIC-04 merges after gate confirmation (ST-11: 2026-06-21; ST-12/13/14: 2026-07-04)

---

## Sprint 1

### EPIC-01: Governance Prompt Hardening

**Owner:** Head of Specs Team
**Branch:** `exec/2026-06-10__release-v5.5/EPIC-01`
**Sprint:** 1
**execution_state.json owner:** Yes (EPIC-01 is owner)

---

#### ST-01 — sprint_planning_prompt.md within-sprint date gate advisory

**Source:** BLG-GOV-116
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**Spec references:** `stage4_backlog_slice.md#ST-01`
**Staging-only ACs:** None
**Status at sprint open:** ready

**Acceptance Criteria**
- sprint_planning_prompt.md updated: stories with a within-sprint date gate must be marked `Status at sprint open: conditional — gate <date>` in sprint_backlog.md at planning time
- Version bumped per CLAUDE.md §6: §14 OPERATIONAL_GUIDE updated; prompt_change_log.md entry appended
- Head of Specs Team sign-off

**Verification:** Director of Quality confirms sprint_planning_prompt.md version bumped, §14 updated, changelog entry present, and the advisory text covers the within-sprint date gate case.

---

#### ST-02 — execution_prompt.md pr_status read-after-open improvement

**Source:** BLG-GOV-117
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**Spec references:** `stage4_backlog_slice.md#ST-02`
**Staging-only ACs:** None
**Status at sprint open:** ready

**Acceptance Criteria**
- execution_prompt.md updated: after `gh pr create`, immediately read `gh pr view <number> --json state,mergeStateStatus` and write the actual state to execution_state.json
- Version bumped; OPERATIONAL_GUIDE §14 updated; prompt_change_log.md entry appended per CLAUDE.md §6
- Head of Specs Team sign-off

**Verification:** Director of Quality confirms execution_prompt.md version bumped, §14 updated, changelog entry present, and the pr_status read-after-open instruction is in the correct STEP.

---

#### ST-03 — qa_evidence commit discipline advisory in execution_prompt.md

**Source:** BLG-GOV-118
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**Spec references:** `stage4_backlog_slice.md#ST-03`
**Staging-only ACs:** None
**Status at sprint open:** ready

**Acceptance Criteria**
- execution_prompt.md updated: advisory added before PR-opening step — "verify qa_evidence_EPIC-xx.md is committed to the EPIC branch before opening the PR"
- Version bumped; OPERATIONAL_GUIDE §14 updated; prompt_change_log.md entry appended per CLAUDE.md §6
- Head of Specs Team sign-off

**Verification:** Director of Quality confirms advisory text is present before the PR-open step, version bumped, §14 updated, changelog entry present.

> Note: ST-02 and ST-03 both modify `execution_prompt.md` — both may be implemented in the same commit. If so, apply CLAUDE.md §6 once for the combined version transition; commit message must reference both `[ST-02][ST-03]` per CLAUDE.md §2.

---

### EPIC-02: Trade Data Density Visibility

**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner
**Branch:** `exec/2026-06-10__release-v5.5/EPIC-02`
**Sprint:** 1

---

#### ST-04 — Trade count gate-monitoring view (backend)

**Source:** BLG-BE-34
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Head of Backend Engineering
**Delegation class:** autonomous
**Spec references:** `stage4_backlog_slice.md#ST-04`
**Staging-only ACs:** None
**Status at sprint open:** ready

**Acceptance Criteria**
- Database view or PostgreSQL function `get_gate_metrics()` created, returning: closed_trades_count, closed_trades_with_plans, active_positions_count, ai_journal_entry_count (if table exists), oldest_trade_date, newest_trade_date
- Optionally: `GET /portfolio/gate-metrics` endpoint (read-only) exposing the view — if endpoint added, must be registered in backend/routers/test.py and openapi.yaml per CLAUDE.md §2
- Data Model & Domain Schema Owner sign-off
- Unit test covers at least the happy-path query result shape

**Verification:** Director of Quality confirms `get_gate_metrics()` exists, unit test passes in CI, and if endpoint added: registered in test.py and openapi.yaml in same commit.

---

#### ST-05 — Trade data density progress tracker (frontend display)

**Source:** BLG-GOV-120
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner
**Delegation class:** autonomous
**Depends on:** ST-04 (backend view/endpoint)
**Spec references:** `stage4_backlog_slice.md#ST-05`
**Staging-only ACs:** AC-3 (Playwright scenario OR human staging sign-off with date — if Playwright coverage is not added, staging sign-off is staging-only evidence; backlog item to be filed before PR opens per CLAUDE.md §2)
**Status at sprint open:** ready

**Acceptance Criteria**
- Trade count display added to System Status page OR added as a data density line in SI-05 weekly digest template: "Closed trades: N / Gate 1: 20 / Gate 2: 50 / Gate 3: 100"
- Count queries real production data (not hardcoded); sources ST-04 view or direct query
- If System Status page: Playwright scenario covers trade count display OR human staging sign-off recorded with date
- If System Status fallback count updated: SC-SS-01b in tests/e2e/system-status.spec.js updated per CLAUDE.md §2
- Infrastructure & Operations Owner sign-off

**Verification:** Director of Quality confirms trade count display sources real data; either Playwright test exists and passes or human staging sign-off is recorded with date in DoQ block.

> Staging-only AC note (RISK-02): If Playwright coverage is deferred, a backlog item must be filed before the PR opens. This is a seal gate condition per CLAUDE.md §2.

---

### EPIC-03: API Baseline & Documentation Clearance

**Owner:** Infrastructure & Operations Owner; QA Lead; Head of UX & Design
**Branch:** `exec/2026-06-10__release-v5.5/EPIC-03`
**Sprint:** 1

---

#### ST-06 — v2.8–v4.6 endpoint performance baseline re-run (24 endpoints)

**Source:** BLG-OPS-13
**Priority:** P3
**Effort:** M (~2 days)
**Owner:** Infrastructure & Operations Owner
**Delegation class:** delegated_backend
**Spec references:** `stage4_backlog_slice.md#ST-06`
**Staging-only ACs:** AC-1, AC-2 (measurements from live/staging environment — cannot be performed in CI; human operator required)
**Status at sprint open:** ready (requires Infrastructure & Operations Owner to coordinate live env access)

**Acceptance Criteria**
- All 24 endpoints from v2.8–v4.6 (as listed in BLG-OPS-13 source) have baseline rows added to docs/ops/api_performance_baseline.md
- Measurements made against live/staging environment (p50/p95/p99 + any threshold flags)
- Infrastructure & Operations Owner sign-off

**Verification:** Director of Quality confirms 24 endpoint rows present in api_performance_baseline.md with p50/p95/p99 measurements and sign-off recorded.

---

#### ST-07 — v5.1–v5.4 endpoint baseline extension

**Source:** BLG-OPS-61
**Priority:** P3
**Effort:** S (~0.75 day)
**Owner:** Infrastructure & Operations Owner
**Delegation class:** delegated_backend
**Spec references:** `stage4_backlog_slice.md#ST-07`
**Staging-only ACs:** AC-1, AC-2 (measurements from live environment)
**Status at sprint open:** ready (sequence after ST-06)

**Acceptance Criteria**
- v5.1–v5.4 new endpoints added to api_performance_baseline.md (POST /digest/si05/send + paper-positions enhancements + any v5.2 routes from BLG-SPEC-49–52 not already present)
- Measurements made against live environment
- Infrastructure & Operations Owner sign-off

**Verification:** Director of Quality confirms v5.1–v5.4 endpoints present in api_performance_baseline.md with measurements.

---

#### ST-08 — POST /digest/si05/send to api_performance_baseline.md

**Source:** BLG-OPS-54
**Priority:** P3
**Effort:** XS (~0.25 day)
**Owner:** Infrastructure & Operations Owner
**Delegation class:** delegated_backend
**Spec references:** `stage4_backlog_slice.md#ST-08`
**Staging-only ACs:** AC-1 (measurements from live/staging environment)
**Status at sprint open:** ready (confirm ST-07 coverage first — may be trivially complete)

**Acceptance Criteria**
- POST /digest/si05/send present in api_performance_baseline.md with baseline measurements recorded (p50/p95/p99)
- Measurements from live/staging environment
- Infrastructure & Operations Owner sign-off

**Verification:** Director of Quality confirms POST /digest/si05/send row present with measurements. If ST-07 already covers it, confirm with Infrastructure & Operations Owner and close as trivially complete.

---

#### ST-09 — Formal regression test suite baseline document

**Source:** BLG-QA-50
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** QA Lead
**Delegation class:** autonomous
**Spec references:** `stage4_backlog_slice.md#ST-09`
**Staging-only ACs:** None
**Status at sprint open:** ready

**Acceptance Criteria**
- Formal regression baseline document created in docs/qa/ or docs/testing/
- All backend/routers/test.py entries mapped to features with version history
- All tests/e2e/*.spec.js files listed with scenario count and feature mapping
- Director of Quality sign-off

**Verification:** Director of Quality confirms document exists, all test.py entries mapped, all e2e spec files listed, and sign-off recorded.

---

#### ST-10 — User journey map: SI-05 Telegram digest to app action

**Source:** BLG-FE-65
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Head of UX & Design
**Delegation class:** delegated_qa
**Spec references:** `stage4_backlog_slice.md#ST-10`
**Staging-only ACs:** AC-1 (requires human walkthrough of live Telegram digest → app navigation)
**Status at sprint open:** ready (SI-05 confirmed operational)

**Acceptance Criteria**
- User journey map document produced: entry points (links in digest), navigation steps to relevant app screen, friction findings
- Any significant friction filed as a separate backlog item
- Head of UX & Design sign-off

**Verification:** Director of Quality confirms journey map document exists with entry points, navigation steps, friction findings, and sign-off recorded. Any friction backlog items confirmed filed.

---

## Sprint 2

### EPIC-04: SI-05 Effectiveness Review & UX Pre-work

**Owner:** Head of UX & Design; Infrastructure & Operations Owner; Product Owner; Metrics Definitions & Analytics Owner
**Branch:** `exec/2026-06-10__release-v5.5/EPIC-04`
**Sprint:** 2
**Sprint 2 gate:** ST-11 gated on 2026-06-21; ST-12/ST-13/ST-14 gated on 2026-07-04

> Sprint 2 must not open until gate clearance confirmed for each story. Do not invoke Sprint 2 execution before confirming gate dates have passed and conditions are met.

---

#### ST-11 — Red Flag Journal visual design review pre-brief

**Source:** BLG-FE-64
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Head of UX & Design
**Delegation class:** delegated_decision
**Spec references:** `stage4_backlog_slice.md#ST-11`
**Staging-only ACs:** None
**Status at sprint open: conditional — gate 2026-06-21**

**Acceptance Criteria**
- Design review brief produced for BLG-FE-41: scope (filters UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, expected deliverable
- Brief reviewed by Head of UX & Design; sign-off recorded
- Gate confirmed (2026-06-21 or later) before work begins

**Verification:** Director of Quality confirms design review brief exists, Head of UX & Design sign-off recorded, and gate clearance date confirmed.

---

#### ST-12 — SI-05 p99 production latency baseline review

**Source:** BLG-OPS-59
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner
**Delegation class:** delegated_backend
**Spec references:** `stage4_backlog_slice.md#ST-12`
**Staging-only ACs:** AC-1, AC-2 (Render log extraction post-2026-07-04 from live production)
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria**
- p99 latency extracted from Render logs for POST /digest/si05/send after ≥2026-07-04
- Compared against BLG-OPS-54 pre-launch baseline
- PASS (p99 < 2× baseline) or performance investigation item filed
- Infrastructure & Operations Owner sign-off

**Verification:** Director of Quality confirms p99 measurement present, comparison to baseline documented, result (PASS or investigation item) recorded.

---

#### ST-13 — SI-05 digest weekly cadence review

**Source:** BLG-GOV-112
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Product Owner
**Delegation class:** delegated_decision
**Spec references:** `stage4_backlog_slice.md#ST-13`
**Staging-only ACs:** None
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria**
- Cadence review document produced after 2026-07-04 effectiveness review
- Recommendation made with data backing (si05_digest_log delivery count, BLG-GOV-96 criteria assessment)
- Recommendation: maintain weekly / move to bi-weekly / adaptive cadence
- Product Owner sign-off

**Verification:** Director of Quality confirms cadence review document exists, recommendation is data-backed, Product Owner sign-off recorded.

---

#### ST-14 — SI-05 digest actionability metric definition

**Source:** BLG-GOV-115
**Priority:** P2
**Effort:** S (~0.75 day)
**Owner:** Metrics Definitions & Analytics Owner
**Delegation class:** delegated_decision
**Spec references:** `stage4_backlog_slice.md#ST-14`
**Staging-only ACs:** None
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria**
- 2–4 actionability metrics formally defined with data source mapping (si05_digest_log, red_flag_events, trade data)
- Metrics document reviewed by Metrics Definitions & Analytics Owner
- Gate condition verified (2026-07-04 review complete before authoring)
- Metrics feed BLG-GOV-112 cadence review and BLG-GOV-96 effectiveness criteria

**Verification:** Director of Quality confirms metrics document exists with 2–4 metrics, data source mapping, gate confirmation noted, and Metrics Definitions & Analytics Owner sign-off recorded.

---

## Product Owner Sign-Off

Product Owner: Confirmed — `plan sprint` issued 2026-06-10
Date: 2026-06-10

Capacity WARN acknowledged: yes (Sprint 1 ~6.5 days vs 12–14 day revised baseline; WARN from old 5–7 day baseline — within current capacity)
Deferred execution blockers: none
