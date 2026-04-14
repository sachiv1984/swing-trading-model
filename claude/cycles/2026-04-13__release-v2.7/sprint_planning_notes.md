**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-14
**Cycle:** 2026-04-13__release-v2.7

---

# Sprint Planning Notes — 2026-04-13__release-v2.7

## Backlog Slice Source

Original — `claude/cycles/2026-04-13__release-v2.7/stage4_backlog_slice.md`

No amendment file in use (`amended_backlog_slice_path` is empty in state.json and `.claude_current_state.json`).

---

## Carry-Forward Advisory (from v2.6 — cycle 2026-04-11__release-v2.6)

2 items from prior cycle `lessons_learnt_closure.md ## Carry-Forward`:

1. **BLG-GOV-17 (Sprint Close trigger)** — ✅ RESOLVED. Completed 2026-04-13 (OA-1). `execution_prompt.md` patched to v3.4; `OPERATIONAL_GUIDE.md` updated to v3.55. Sprint Close STEP 3.2.D post-merge reminder now unconditional. No Sprint Planning gate action required.
2. **BLG-QA-11 (Playwright page.route() intercept failure)** — ✅ Scoped into v2.7 as ST-06 (EPIC-03). Growing test coverage debt addressed; ST-07 gated on ST-06.

Carry-forward items reviewed: 2 items from cycle `2026-04-11__release-v2.6`. Both resolved or scoped. No outstanding carry-forward risk.

---

## Deferred Items

No items deferred from this sprint. All 11 ST items are within confirmed capacity and have defined acceptance criteria.

| Item | Reason | Next Sprint Candidate? |
|------|--------|------------------------|
| — | No deferrals — all items included | — |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal — EPIC-01 | ST-01 staging verification must complete before ST-02 DB connection measurement is valid |
| ST-07 | ST-06 | Internal — EPIC-03 | Playwright intercept fix pattern must be working before System Status spec is written |
| ST-01 | None | — | Independent (but human-delegated: Render env var update) |
| ST-03, ST-04, ST-05 | None | — | Independent of each other and EPIC-01/03 |
| ST-08, ST-09 | None | — | Independent of each other; EPIC-04 independent of Sprint 1 |
| ST-10, ST-11 | None | — | Independent of each other; EPIC-05 independent of Sprint 1 |

No circular dependencies detected.

---

## Execution Sequence

### Sprint 1 — EPIC-01, EPIC-02, EPIC-03

1. **ST-01** (EPIC-01, `delegated_backend`) — Infrastructure/Ops Owner updates Render env vars to Supavisor pooler connection string. **Human action required first.** Engine proceeds after confirmation staging is using pooler endpoint.
2. **ST-02** (EPIC-01, `autonomous`) — Refactor `get_portfolio_summary()` single DB connection. Begins after ST-01 staging verification confirms pooler in use.
3. **ST-03** (EPIC-02, `autonomous`) — `execution_prompt.md §3.2.B` PR gate + `commit-check` skill update. Independent; recommended first in EPIC-02 as foundational governance gate.
4. **ST-04** (EPIC-02, `autonomous`) — Autonomous DoQ sign-off class definition (`execution_prompt.md §3.2.A` + `delivery_verification_prompt.md` STEP -1.3). Director of Quality to review qualifying criteria at sprint start.
5. **ST-05** (EPIC-02, `autonomous`) — Add `main` to `governance_sync.yml` `on.push.branches`. Independent.
6. **ST-06** (EPIC-03, `autonomous`) — Investigate Playwright page.route() root cause (3 hypotheses in priority order); fix intercept mechanism; validate 4 existing spec files.
7. **ST-07** (EPIC-03, `autonomous`) — Write `tests/e2e/system-status.spec.js` using ST-06 fix pattern. **Gated: do not begin until ST-06 is complete and intercept pattern verified.**

Sequencing rationale: ST-01 is first as a delegated human prerequisite for ST-02. EPIC-02 (ST-03/04/05) is independent and can run concurrently with EPIC-01 in planning, but is sequenced after ST-01 delegation to allow engine focus. ST-07 is strictly gated on ST-06. EPIC-02 and EPIC-03 EPICs share no dependencies with each other or EPIC-01.

### Sprint 2 — EPIC-04, EPIC-05

8. **ST-08** (EPIC-04, `autonomous`) — New `GET /analytics/market-correlation` endpoint + frontend display. `openapi.yaml` update in same commit. EPIC-04 independent of Sprint 1.
9. **ST-09** (EPIC-04, `autonomous`) — Add 4 supplementary fields to `POST /signals/generate`. `signal_endpoints.md` + `openapi.yaml` updates in same commit. Can run in parallel with ST-08.
10. **ST-10** (EPIC-05, `autonomous`) — Create `docs/specs/spec_dependency_map.md`. Head of Specs Team sign-off on completeness in QA evidence.
11. **ST-11** (EPIC-05, `autonomous`) — Governance health score formula + OPERATIONAL_GUIDE.md + roadmap rebalance STEP -1 advisory. Head of Specs Team sign-off on formula in QA evidence.

Sequencing rationale: EPIC-04 and EPIC-05 are independent of each other and of Sprint 1. ST-08 and ST-09 can begin simultaneously. ST-10 and ST-11 can begin simultaneously. No intra-sprint dependencies in Sprint 2.

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status | Notes |
|---------|----------------|------------------|-------|
| RISK-01 | EPIC-01 (ST-01, ST-02) | Valid | Supavisor (pgbouncer=true) pgbouncer compatibility: test on staging before production cutover; ST-02 explicitly sequenced after ST-01 staging verification. If staging test reveals incompatibility, ST-02 pauses and escalation filed. |
| RISK-02 | EPIC-02 (ST-04) | Valid | Director of Quality qualifying criteria draft already in backlog slice. DoQ to review before ST-04 begins. Sign-off in QA evidence before merge — not a planning gate, but a story-level AC. |
| RISK-03 | EPIC-03 (ST-06, ST-07) | Valid | Investigation approach (3 root cause hypotheses in priority order) and descope trigger criteria ("if root cause cannot be fixed in this sprint, ST-07 is descoped") already defined in `stage4_backlog_slice.md#ST-06`. QA & Testing Owner recommended to formally acknowledge approach at sprint start. See Outstanding Actions. |
| RISK-04 | EPIC-04 (ST-08) | Valid | Yahoo Finance availability: existing `check_market_regime()` pattern already validated; 1-day TTL cache reduces call frequency; graceful error handling (not 500) required in AC. Low risk. |
| RISK-05 | EPIC-05 (ST-10) | Valid | Spec Dependency Map scope: Head of Specs Team signs off completeness at authoring time; explicit staleness acknowledgement header required in doc. M effort estimate assumes ~22 canonical specs. |

---

## Pre-Sprint Vulnerability Scan

pip-audit result: 1 finding

| Package | Version | CVE | Severity | Fix | Notes |
|---------|---------|-----|----------|-----|-------|
| pytest | 9.0.2 | CVE-2025-71176 (GHSA-6w46-j5rx-g56g) | Medium — UNIX local DoS/privilege escalation via `/tmp/pytest-of-{user}` directory pattern | Upgrade to 9.0.3 | Test framework only — not a production runtime dependency. Local attack vector; no network exposure. |

All other 57 packages: ✅ no known vulnerabilities.

Assessment: Medium severity, local attack vector, test/dev framework only. Not classified high/critical — no mandatory PO/HoE acceptance required per sprint planning standard. Recommendation: upgrade pytest to ≥9.0.3 during Sprint 1. Record as advisory in QA evidence if not resolved before sprint close.

---

## Blocked-Decision Advisory (ST-04, EPIC-02)

ST-04 (BLG-GOV-19 — Autonomous DoQ sign-off class): Design artefact exists in backlog slice as qualifying criteria draft (4-point checklist). A formal HoST design session or DoQ pre-review before sprint start would reduce mid-sprint overhead. Director of Quality review of qualifying criteria is an AC requirement (must occur before merge, not before sprint start). No design artefact gap — advisory only.

---

## Test Scenario Gap Flag

ST-07 (`delegated_qa`-class spec authoring): The System Status Playwright spec is a new test file, not a UX-facing page/control addition. No `test_scenarios` field gap applies — this IS the test scenario. No pending test scenario flag required.

ST-08 (EPIC-04): New Analytics page display — `delegated_frontend` criteria: new frontend display introduced. Flag: EPIC-04 `test_scenarios` in `execution_state.json` to be authored by QA & Testing Owner if not present before Sprint 2 execution begins.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-03: QA & Testing Owner to formally confirm ST-06 investigation approach (3 root cause hypotheses in priority order) and ST-07 descope trigger criteria at sprint start. Content already defined in ratified `stage4_backlog_slice.md#ST-06`. | QA & Testing Owner | No — backlog slice content is the ratified planning record; formal acknowledgement is recommended pre-execution advisory only |
| pytest CVE-2025-71176: Upgrade pytest from 9.0.2 to 9.0.3. | Head of Engineering | No — advisory; resolve during Sprint 1 |
| EPIC-04 test_scenarios: QA & Testing Owner to author test scenarios for ST-08 Analytics page display before Sprint 2 execution begins. | QA & Testing Owner | No — flag for Sprint 2 readiness |
