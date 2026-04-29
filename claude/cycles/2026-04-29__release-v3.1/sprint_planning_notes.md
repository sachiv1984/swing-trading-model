**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-29
**Cycle:** 2026-04-29__release-v3.1

---

# Sprint Planning Notes — 2026-04-29__release-v3.1

## Backlog Slice Source

Original — `claude/cycles/2026-04-29__release-v3.1/stage4_backlog_slice.md` (no amendment active)

---

## Carry-Forward Items Reviewed

3 items from cycle `2026-04-25__release-v3.0` (lessons_learnt_closure.md ## Carry-Forward):

| # | Item | Disposition |
|---|------|-------------|
| CF-01 | execution_prompt.md §3.1.A reclassification backfill | Converted to ST-13 in EPIC-04 ✓ |
| CF-02 | execution_prompt.md STEP 8.5 output target fix | Converted to ST-14 in EPIC-04 ✓ |
| CF-03 | Playwright `waitFor` pattern advisory | Advisory only — not a sprint story; QA & Testing Owner to apply at next E2E authoring session |

---

## Capacity WARN Acknowledgement

Capacity check outcome from release plan: **WARN** (~18.75 days estimated vs ~10 days available capacity).

Product Owner acknowledged at sprint planning initiation (2026-04-29). Over-allocation accepted on the basis that:
1. Solo dev historically compresses spec authoring overhead during execution
2. Phasing from release plan followed exactly (Sprint 1: ~9.0 days, Sprint 2: ~9.75 days)
3. No deferral of stories to v3.2 elected — all 14 stories remain in scope

`capacity_warn_acknowledged: true` recorded.

---

## Pre-Sprint Vulnerability Scan

pip-audit run against `backend/requirements.txt` (2026-04-29):
**Result: clean — no known vulnerabilities found** across all 68 dependencies.

---

## Deferred Items

No items deferred this sprint. All 14 stories from stage4_backlog_slice.md are included in scope.

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | — | — |

---

## Test Scenario Gap Flags (LL-v2.0-P4-2)

The following `delegated_frontend` items introduce new UI controls on existing pages — flag `test_scenarios` in `execution_state.json` as pending at execution time:

| Story | EPIC | New UI Surface | Flag |
|-------|------|----------------|------|
| ST-03 | EPIC-01 | Trade Plan creation form (new data entry surface) | `test_scenarios`: "pending — QA & Testing Owner to author before next sprint on this domain" |
| ST-08 | EPIC-03 | Earnings Calendar display (new badge/column on 3 pages: screener, watchlist, positions) | `test_scenarios`: "pending — QA & Testing Owner to author before next sprint on this domain" |

---

## Dependency Map

| Item | Depends On | Type | Status | Sprint |
|------|-----------|------|--------|--------|
| ST-02 | ST-01 | Internal (spec-first) | Resolved — ST-01 sequenced first | Sprint 1 |
| ST-03 | ST-02 | Internal (backend-first) | Resolved — ST-02 Sprint 1, ST-03 Sprint 2 | Sprint 2 |
| ST-04 | ST-02 | Internal (data model context) | Resolved — ST-02 Sprint 1, ST-04 Sprint 2 | Sprint 2 |
| ST-05 | ST-04 | Internal (spec-first) | Resolved — ST-04 first in Sprint 2 | Sprint 2 |
| ST-08 | ST-07 | Internal (backend-first) | Resolved — ST-07 Sprint 1, ST-08 Sprint 2 | Sprint 2 |
| ST-10 | ST-09 | Internal (protocol reference) | Resolved — ST-09 Sprint 1, ST-10 Sprint 2 | Sprint 2 |
| ST-03 | Design gate | External (design gate) | Resolved — design gate passed 2026-04-29 | Sprint 2 |
| ST-08 | Design gate | External (design gate) | Resolved — design gate passed 2026-04-29 | Sprint 2 |

No circular dependencies detected.

---

## Execution Sequence

### Sprint 1 (recommended order)

1. **ST-06** — P1 bug fix first (UK ticker display + watchlist promotion; blocks UK-market users)
2. **ST-07** — Earnings Calendar spec + backend (independent; delivers DS-04 backend foundation for Sprint 2 ST-08)
3. **ST-01** — Trade Plan spec authoring (unblocks ST-02; must precede any backend work)
4. **ST-09** — Screener accuracy test protocol (independent; referenced by ST-10 in Sprint 2)
5. **ST-02** — Trade Plan backend (depends on ST-01; unblocks ST-03 and ST-04 in Sprint 2)
6. **ST-11** — Monthly P&L feature (independent; backend + frontend extending existing reporting)
7. **ST-12** — Security policy docs (independent; documentation only)
8. **ST-13 + ST-14** — Governance prompt patches CF-01 + CF-02 (independent; can be combined in one commit)

### Sprint 2 (recommended order)

1. **ST-04** — Pre-Trade Research spec (depends on ST-02 data model; unblocks ST-05)
2. **ST-03** — Trade Plan frontend (depends on ST-02 backend + design gate)
3. **ST-08** — Earnings Calendar frontend (depends on ST-07 backend)
4. **ST-05** — Pre-Trade Research backend (depends on ST-04 spec)
5. **ST-10** — Screener scenario library (depends on ST-09 protocol)

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01, ST-02) | Valid — ST-01 sequenced first; Data Model Owner + HoST sign-off required before ST-02 |
| RISK-02 | EPIC-01 (ST-03), EPIC-02 | Valid — design gate passed 2026-04-29; PT-02 frontend deferred to v3.2 |
| RISK-03 | EPIC-03 (ST-07, ST-08) | Valid — spec authoring (ST-07) validates Yahoo Finance data quality; graceful null display if unavailable |
| RISK-04 | EPIC-04 (ST-13, ST-14) | Valid — CLAUDE.md §6 checklist enforced at commit-check; commit blocked until all 4 steps complete |

---

## Prompt Change Log Hygiene Advisory (STEP -1.11)

Scan complete: all governed prompt current versions match last log entries. No gap detected.

---

## Outstanding Actions

| Action | Owner | Blocker? |
|--------|-------|---------|
| CF-03: Adopt Playwright `waitFor` pattern at next E2E authoring session | QA & Testing Owner | No |
