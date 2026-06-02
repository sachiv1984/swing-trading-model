**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-02
**Cycle:** 2026-06-02__release-v4.9

---

# Sprint Planning Notes — 2026-06-02__release-v4.9

## Backlog Slice Source

Original — `claude/cycles/2026-06-02__release-v4.9/stage4_backlog_slice.md`

No amendment file in use (`amended_backlog_slice_path` is empty in `.claude_current_state.json`).

## Carry-Forward Items

Carry-forward items reviewed: 2 items from cycle `2026-06-01__release-v4.8`

| # | Item | Status |
|---|------|--------|
| 1 | SI-05 Phase 1 gate (ST-08 from v4.8) | Included as conditional EPIC-04; gate clears 2026-06-21 ✓ |
| 2 | SI-02 data density gate (monitor) | Background monitor — gate NOT MET (~Nov 2026) ✓ |

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-06 — SI-05 Phase 1 backend service + Telegram delivery | EPIC-04 | Gate not met: SI-01 + SI-03 live ≥ 30 days — gate clears 2026-06-21 (today: 2026-06-02) | Yes — via amendment cycle on/after 2026-06-21 |
| ST-07 — SI-05 Phase 1 Playwright coverage | EPIC-04 | Same gate condition; depends on ST-06 | Yes — with ST-06 via same amendment |

**Deferred item traceability note for Execution Engine:** When initialising `execution_state.json`, include:
```yaml
epics.EPIC-04.stories.ST-06:
  status: deferred_at_planning
  gate_condition: "SI-01 + SI-03 live ≥ 30 days — gate clears 2026-06-21; invoke amendment cycle to add"
epics.EPIC-04.stories.ST-07:
  status: deferred_at_planning
  gate_condition: "Same as ST-06; depends on ST-06"
```

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-04 | ST-03 | Internal (within EPIC-02) | Resolved — ST-03 must complete before ST-04 |
| ST-07 | ST-06 | Internal (within EPIC-04, deferred) | N/A — both deferred at planning |
| ST-01 | None | — | Independent |
| ST-02 | None | — | Independent |
| ST-03 | None | — | Independent |
| ST-05 | None | — | Independent |

**Cross-EPIC dependencies:** None. EPIC-01, EPIC-02, and EPIC-03 are fully independent of each other.

## Multi-EPIC Execution Notes

**Active EPICs:** EPIC-01, EPIC-02, EPIC-03 (EPIC-04 deferred)

**execution_state.json owner:** EPIC-01 — first in execution order.

All other EPIC branches (EPIC-02, EPIC-03) must check for `execution_state.json` existence before creating their own version. If found, read it and append their EPIC's section rather than overwrite.

**Shared file ownership:**

| File | EPICs Touching | Owner | Advisory |
|------|----------------|-------|---------|
| `backend/security_register.md` | EPIC-01 (ST-01 + ST-02 both document findings here) | EPIC-01 | ST-01 and ST-02 are in the same EPIC; no cross-EPIC conflict |
| `ci-tests.yml` | EPIC-02 only | EPIC-02 | No cross-EPIC conflict |
| `claude/system/roadmap_prompt.md` | EPIC-03 only | EPIC-03 | No cross-EPIC conflict |
| `claude/system/OPERATIONAL_GUIDE.md` | EPIC-03 only | EPIC-03 | No cross-EPIC conflict |
| `claude/system/prompt_change_log.md` | EPIC-03 only | EPIC-03 | No cross-EPIC conflict |

No shared-file cross-EPIC conflicts identified.

## Execution Sequence

```
Sprint 1 (all firm items):

Phase A (can execute in parallel):
  EPIC-01 (P1 — Security):
    1. ST-01 — npm devDependency HIGH CVE remediation
    2. ST-02 — Anthropic SDK upgrade 0.40.0 → latest

  EPIC-02 (P2 — CI/QA):
    3. ST-03 — Wire Phase B CI with real Postgres service
    4. ST-04 — Schema smoke test (depends on ST-03)

  EPIC-03 (P3 — Governance):
    5. ST-05 — roadmap_prompt.md STEP 8.1 gate strengthening

Merge order: EPIC-01 → EPIC-02 → EPIC-03

Phase B (conditional, not yet in scope):
  EPIC-04 (conditional — gate 2026-06-21):
    — ST-06, ST-07 — deferred; require amendment cycle on/after 2026-06-21
```

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 / ST-02 | Valid — Anthropic SDK 65 minor versions; changelog review + full backend test suite + staging validation (AC-04 staging-only); risk acknowledged at planning |
| RISK-02 | EPIC-02 / ST-03 | Valid — Phase B real Postgres CI may surface masked failures; accepted as quality improvement; fix any surfaced failures |
| RISK-03 | EPIC-04 | N/A — EPIC-04 deferred at planning; gate deterministic (2026-06-21) |

## Pre-Sprint Vulnerability Scan

**pip-audit result:** Clean — no known vulnerabilities in `backend/requirements.txt` (scan run 2026-06-02).

**Note:** `anthropic==0.40.0` is 65 minor versions behind latest. No CVEs reported by pip-audit but upgrade is tracked as ST-02 (BLG-OPS-50, P2). Frontend npm HIGH CVEs (21) are build-toolchain only (react-scripts devDependency chain); addressed by ST-01.

## Delegation Class Decisions

All 5 firm stories classified `autonomous`:

| Story | Classification | Justification |
|-------|---------------|---------------|
| ST-01 | autonomous | `npm audit fix` to devDependency chain; no UX change; no human decision required |
| ST-02 | autonomous | SDK version bump + changelog review + test run; staging AC-04 documented as staging-only evidence |
| ST-03 | autonomous | GitHub Actions workflow edit; no UX change; deterministic CI config addition |
| ST-04 | autonomous | Pytest test addition against locked schema; no UX change |
| ST-05 | autonomous | Governance prompt edit against locked spec (AC-01–AC-07 fully defined); no UX change |

No `delegated_frontend` override required. BLG-GOV-72 default-autonomous fast-path applies to all.

## Pre-Sprint Backlog Advisory

No items with `Provisional-Target: Before v4.9 sprint planning` found in `claude/backlog/backlog.md`.

**Advisory from cycle_summary OA-MANIFEST-03:** BLG-GOV-74 Provisional-Target should be updated from `v4.9` to `v4.10+` (gate date 2026-08-29, post v4.9 ship). Advisory only — not a sprint seal blocker.

## Outstanding Actions

| Action | Owner | Blocker? |
|--------|-------|---------|
| BLG-GOV-74 Provisional-Target update (v4.9 → v4.10+) | PMO Lead | No — advisory only |
| ST-02 AC-04: staging sign-off for AI endpoint (POST /trade-plans/{plan_id}/generate-thesis, POST /ai/check-daily-cost) post-SDK-upgrade | Infrastructure & Operations Owner | No — staging-only evidence; DoQ sign-off at delivery verification |
| ST-07 (EPIC-04) AC-09: Telegram staging sign-off — deferred with EPIC-04 until gate confirms | Infrastructure & Operations Owner | No — EPIC-04 deferred at planning |

No actions marked `Blocker? Yes`. Sprint may proceed to seal.
