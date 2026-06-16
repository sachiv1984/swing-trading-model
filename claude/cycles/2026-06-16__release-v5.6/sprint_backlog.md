**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-16
**Cycle:** 2026-06-16__release-v5.6
**Release:** v5.6
**Sprint Goal:** Ship the PT-04 governance gate re-verification, Arc 5 QA completion criteria, and SI-05 UX improvements in Sprint 1; deliver research and portfolio performance optimisations in Sprint 2.
**Backlog Slice Source:** original — claude/cycles/2026-06-16__release-v5.6/stage4_backlog_slice.md

---

# Sprint Backlog — 2026-06-16__release-v5.6

## Sprint Scope

### Merge Order

**EPIC-03 → EPIC-01 → EPIC-02**

- EPIC-03 is the `execution_state.json` owner (first in merge order)
- EPIC-01 must check for `execution_state.json` before creating; append rather than overwrite
- EPIC-02 (Sprint 2) must check and append similarly
- EPIC-02 merges after Sprint 1 EPICs; rebase onto main after EPIC-03 and EPIC-01 merge

No shared source files identified across Sprint 1 EPICs. EPIC-02 Sprint 2 branch should be created from main after Sprint 1 merges are complete.

---

## Sprint 1

### EPIC-03 — QA & Gate Governance

**Maps to:** S2-07, S2-08, S2-09, S2-10
**Owner:** PMO Lead; Director of Quality; FinOps & Resource Architect
**Estimated effort:** ~3–4 days (S + S + S-M + S)
**Risk IDs:** RISK-03
**Execution sequence:** 1 (execution_state.json owner — first in merge order)
**Branch:** exec/2026-06-16__release-v5.6/EPIC-03

---

#### ST-08 — BLG-GOV-106: PT-04 trade count gate re-verification

**Owner:** PMO Lead; Product Owner
**Estimated effort:** S (~0.5 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None — run first; result affects Arc 2 horizon assessment

**Notes:** P1 priority. Execute first in EPIC-03. Either outcome (gate met or not met) closes BLG-GOV-106. Per RISK-03: result is advisory, not a sprint blocker.

**Staging-only ACs:** None — all ACs verifiable via SQL query and roadmap/backlog file updates in the repo.

**Status at sprint open: ready**

---

#### ST-09 — BLG-QA-45: Arc 5 QA completion criteria definition

**Owner:** Director of Quality; QA Lead
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None — can run in parallel with ST-10; after ST-08 preferred but not required

**Notes:** Output is a document (criteria list) committed to the cycle artefacts. Product Owner and Director of Quality sign-off required per AC-04.

**Staging-only ACs:** None — all ACs satisfied by document production and sign-off in the repo.

**Status at sprint open: ready**

---

#### ST-10 — BLG-QA-49: Arc 5 test scenario completeness assessment

**Owner:** QA Lead; Director of Quality
**Estimated effort:** S-M (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None — covers SI-01, SI-03, SI-05 Phase 1 (all shipped); no execution prerequisite

**Notes:** Coverage map must include SI-01 (PreEntryValidationPanel), SI-03 (RedFlagJournal.js), SI-05 (allocation_insufficient badge). Director of Quality sign-off required per AC-04.

**Staging-only ACs:** None — Playwright test enumeration and coverage map are repo-based; Director of Quality sign-off is document-based.

**Status at sprint open: ready**

---

#### ST-11 — BLG-OPS-65: Anthropic API cost 14-cycle trend analysis

**Owner:** FinOps & Resource Architect
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None — standalone analysis document

**Notes:** Analysis covers cycles v4.4–v5.5 (14 cycles). Source: claude_audit_log. Assess against BLG-OPS-37 $5/month threshold. FinOps & Resource Architect sign-off required per AC-04.

**Staging-only ACs:** None — analysis produced from log data in repo; sign-off is document-based.

**Status at sprint open: ready**

---

### EPIC-01 — SI-05 UX & Digest Improvements

**Maps to:** S2-01, S2-02 (firm); S2-11 conditional (deferred at planning)
**Owner:** Head of Backend Engineering; Head of UX & Design
**Estimated effort:** ~1 day firm (S + XS)
**Risk IDs:** RISK-01
**Execution sequence:** 2 (after EPIC-03)
**Branch:** exec/2026-06-16__release-v5.6/EPIC-01

---

#### ST-01 — BLG-FE-73: Add deep links from SI-05 digest to relevant app screens

**Owner:** Head of Backend Engineering; Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Links must use the app's public URL with correct hash/route. Head of UX & Design sign-off required per AC-04. At least one deep link per AC-01.

**Staging-only ACs:** AC-02 (link navigates correctly on mobile Telegram) [staging-only evidence] — requires Telegram mobile client testing; CI cannot reproduce mobile Telegram navigation behaviour. If staging sign-off is deferred to post-merge, file a backlog item before PR opens.

**Status at sprint open: ready**

---

#### ST-02 — BLG-FE-74: Clarify N/A pass rate reason in SI-05 digest message

**Owner:** Head of Backend Engineering
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Code change in `si05_digest_service.py`. "No events" and "data unavailable" must produce distinct messages per AC-02.

**Staging-only ACs:** None — AC-01 and AC-02 verifiable by unit test; AC-03 (no regression) verifiable by existing digest tests.

**Status at sprint open: ready**

---

## Sprint 2

### EPIC-02 — Performance & Latency Hardening

**Maps to:** S2-03, S2-04, S2-05, S2-06
**Owner:** Infrastructure & Operations Owner; Head of Backend Engineering
**Estimated effort:** ~3.5–4.5 days (M + S + S + S)
**Risk IDs:** RISK-02
**Execution sequence:** 3 (Sprint 2 — after EPIC-03 and EPIC-01 merge)
**Branch:** exec/2026-06-16__release-v5.6/EPIC-02

> **Sprint 2 gate:** EPIC-02 executes as Sprint 2. Per LL-P3-03-v55 lesson, if Sprint 2 cannot execute due to capacity or other constraints, EPIC-02 items return to backlog without blocking the release. All items are P2/P3 and standalone.

---

#### ST-04 — BLG-OPS-62: Investigate GET /portfolio/concentration-status high latency

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None — run before ST-07 (findings may inform caching strategy)

**Notes:** Baseline p95=5,917ms. Target ≤1,000ms. Infrastructure & Operations Owner sign-off after re-measurement per AC-04.

**Staging-only ACs:** AC-03 (p95 latency re-measured on production), AC-04 (Infrastructure & Operations Owner sign-off after re-measurement) [staging-only evidence] — production latency re-measurement requires deployed environment.

**Status at sprint open: ready**

---

#### ST-05 — BLG-OPS-63: Investigate GET /portfolio/red-flag-journal high latency

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Baseline p95=3,200ms. Target ≤1,000ms. Infrastructure & Operations Owner sign-off after re-measurement per AC-04.

**Staging-only ACs:** AC-03 (p95 latency re-measured on production), AC-04 (Infrastructure & Operations Owner sign-off after re-measurement) [staging-only evidence] — production latency re-measurement requires deployed environment.

**Status at sprint open: ready**

---

#### ST-06 — BLG-OPS-64: Investigate GET /analytics/behavioural-drift high latency

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Baseline p95=3,798ms. Implement TTL-based result cache (15–30 min). Infrastructure & Operations Owner sign-off after re-measurement per AC-05.

**Staging-only ACs:** AC-03 (p95 latency for cached calls on production), AC-04 (cache hit rate ≥50% under typical usage), AC-05 (Infrastructure & Operations Owner sign-off after re-measurement) [staging-only evidence] — requires deployed caching environment with real traffic.

**Status at sprint open: ready**

---

#### ST-07 — BLG-OPS-22: Research data caching layer

**Owner:** Infrastructure & Operations Owner; Head of Backend Engineering
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** ST-04/05/06 (informational — run investigations first; findings may inform cache approach). ST-07 is independently deliverable if investigations find different root causes.

**Notes:** Gate already cleared (p95=4,601ms > 3,000ms threshold, confirmed 2026-06-11). TTL-based cache (Redis or in-memory), 15-minute TTL per ticker. Cache invalidation on screener run. AC-06 requires gate condition documented in QA evidence.

**Staging-only ACs:** AC-04 (research view p95 ≤2,000ms for cached tickers on production), AC-05 (cache hit rate ≥50% in typical usage) [staging-only evidence] — requires deployed caching environment with real research view traffic.

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Sprint 1 | Sprint 2 | Total |
|--------|----------|----------|-------|
| Confirmed capacity | ~12–14 days | ~12–14 days | ~24–28 days |
| Estimated effort (in-scope) | ~2.5–4 days | ~3.5–4.5 days | ~6–8.5 days firm |
| Utilisation | ~18–29% | ~25–32% | ~24–35% |
| Over-allocation | No | No | No |

**Capacity WARN acknowledged:** Release-level total approaches 2-sprint boundary (WARN in release plan). Product Owner acknowledges risk; phased delivery across 2 sprints accepted.

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-03 (BLG-FE-64: RFJ design review pre-brief) | EPIC-01 | Gate 2026-06-21 not cleared at planning (today: 2026-06-16). Gate condition: SI-03 live ≥30 days. Invoke amendment cycle if gate clears during sprint. |

## Deferred Execution Blockers Accepted

*(No deferred execution blockers — `deferred_execution_blockers` was empty in state.json)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Prompt change log entries for roadmap_prompt.md v6.9→v7.0 and v7.0→v7.1 missing | PMO Lead / Head of Specs Team | No |
| If BLG-FE-64 gate clears 2026-06-21, invoke amendment cycle | PMO Lead | No |

No blockers. Sprint is sealed.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** ✅ Confirmed — 2026-06-16
**Scope confirmed:** ✅ Confirmed — 10 firm stories (ST-01/02/04/05/06/07/08/09/10/11); ST-03 deferred conditional on gate 2026-06-21
**Capacity WARN acknowledged:** ✅ Confirmed — phased 2-sprint delivery accepted
**Date:** 2026-06-16
