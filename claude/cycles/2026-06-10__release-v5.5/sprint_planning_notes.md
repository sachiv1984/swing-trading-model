**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-10
**Cycle:** 2026-06-10__release-v5.5

---

# Sprint Planning Notes — v5.5

## Carry-Forward Items Reviewed

4 carry-forward items from cycle `2026-06-09__release-v5.4`:

| ID | Description | Disposition |
|----|-------------|-------------|
| LL-RP-01 | Roadmap candidate list pruning at rebalance advisory | Actioned in AUD-2026-06-10 (roadmap_prompt v7.0 STEP 8.0.5) — closed pre-sprint |
| LL-P3-01 | Sprint planning within-sprint date gate advisory | Targeted by ST-01 (BLG-GOV-116) in EPIC-01 Sprint 1 |
| LL-P3-02 | qa_evidence commit discipline (monitor) | Targeted by ST-03 (BLG-GOV-118) in EPIC-01 Sprint 1 |
| LL-P3-03 | Stale pr_status in execution_state.json (monitor) | Targeted by ST-02 (BLG-GOV-117) in EPIC-01 Sprint 1 |

All 4 carry-forwards are directly addressed in this sprint.

---

## Capacity WARN Acknowledgement

The `stage4_5_capacity_check` outcome is `warn`. Context: Sprint 1 estimate is ~6.5 days against the revised 12–14 day capacity baseline (workforce_capacity.md 2026-05-27). The WARN was set under the old 5–7 day baseline; against the current baseline, Sprint 1 is comfortably within capacity. Product Owner acknowledged the WARN by issuing `plan sprint` on 2026-06-10. `capacity_warn_acknowledged = true` set in global state.

---

## Pre-Sprint Backlog Advisory

No backlog items found with `Provisional-Target: Before v5.5 sprint planning`.

---

## Prompt Change Log Hygiene Advisory

⚠ Potential changelog gap: `claude/system/delivery_verification_prompt.md` current **v3.0** — last logged entry shows v2.8→v2.9 (2026-05-30). One or more version transitions (v2.9→v3.0) may be unlogged. Advisory only — does not block sprint planning. Recommend investigating and adding missing rows per CLAUDE.md §6 in a future governance cycle.

⚠ Potential changelog gap: `claude/system/release_planning_prompt.md` current **v2.34** — last visible log entry shows v2.31→v2.32 (2026-05-29). Versions v2.32→v2.33→v2.34 may be missing or in later (older) sections of the log. Advisory only.

---

## Scope Selection — Classification

All 14 firm stories from `stage4_backlog_slice.md` are classified `include`. No stories deferred for capacity or dependency reasons. All 14 enter the sprint backlog.

| ST | Classification | Delegation class | Justification |
|----|----------------|-----------------|---------------|
| ST-01 | include | autonomous | Governance prompt text edit; no UX change; locked scope per BLG-GOV-116 |
| ST-02 | include | autonomous | Governance prompt text edit; no UX change; locked scope per BLG-GOV-117 |
| ST-03 | include | autonomous | Governance prompt text edit; no UX change; locked scope per BLG-GOV-118 |
| ST-04 | include | autonomous | Backend view/function creation; no UX; optional endpoint follows CLAUDE.md §2 |
| ST-05 | include | autonomous | New display on existing System Status page; BLG-GOV-72(c): new section on existing component; Playwright coverage required per AC |
| ST-06 | include | delegated_backend | Requires live/staging environment access for actual API performance measurements; engine cannot initiate production traffic measurements |
| ST-07 | include | delegated_backend | Requires live environment access for baseline measurements; same pattern as ST-06 |
| ST-08 | include | delegated_backend | Trivially complete if ST-07 covers POST /digest/si05/send; otherwise same live-env delegation as ST-06/07 |
| ST-09 | include | autonomous | Document creation reading existing test files; no environment dependency |
| ST-10 | include | delegated_qa | Journey map requires human walkthrough of Telegram digest → app navigation |
| ST-11 | include | delegated_decision | Design review brief requiring Head of UX & Design involvement; conditional gate 2026-06-21 |
| ST-12 | include | delegated_backend | Requires Render log extraction post-2026-07-04; engine cannot access production logs directly |
| ST-13 | include | delegated_decision | Cadence review requires PO decision with data backing; gate 2026-07-04 |
| ST-14 | include | delegated_decision | Metrics definition requires Metrics Analytics Owner; gate 2026-07-04 |

---

## Dependency Map

### Intra-EPIC dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| ST-04 → ST-05 | Hard prerequisite | ST-05 frontend display sources the view/endpoint created in ST-04 |
| ST-06 → ST-07 | Recommended sequence | Both are baseline docs; sequential avoids race condition on api_performance_baseline.md |
| ST-07 → ST-08 | Soft prerequisite | ST-08 trivially complete if ST-07 includes POST /digest/si05/send |

### Cross-EPIC dependencies

None identified. EPIC-01, EPIC-02, EPIC-03 are independent and can be worked in parallel.

### External dependencies

| Story | Dependency | Gate |
|-------|------------|------|
| ST-06, ST-07, ST-08 | Live/staging environment access for API measurements | Infrastructure & Operations Owner coordination (RISK-03) |
| ST-10 | Telegram digest sent and received (SI-05 operational) | SI-05 already live — confirmed operational |
| ST-11 | SI-03 Red Flag Journal live ≥ 30 days | Gate 2026-06-21 |
| ST-12, ST-13, ST-14 | SI-05 effectiveness review data (≥4 weeks operation) | Gate 2026-07-04 |

### Spec dependencies

None — all stories either modify existing governance prompts or create new documents from existing data.

---

## Multi-EPIC Execution Notes

Sprint 1 has 3 EPICs. Designated `execution_state.json` owner: **EPIC-01** (first in execution order).

EPIC-02 and EPIC-03 must check for `execution_state.json` existence at branch creation. If found, read and append their EPIC section rather than overwrite.

**Shared files (Sprint 1):**

| File | EPICs touching it | Canonical owner | Advisory |
|------|-------------------|-----------------|---------|
| `claude/system/execution_prompt.md` | EPIC-01 only | EPIC-01 | No conflict |
| `claude/system/prompt_change_log.md` | EPIC-01 only | EPIC-01 | No conflict |
| `docs/reference/openapi.yaml` | EPIC-02 only (if endpoint added) | EPIC-02 | No conflict |
| `backend/routers/test.py` | EPIC-02 only (if endpoint added) | EPIC-02 | No conflict |
| `docs/ops/api_performance_baseline.md` | EPIC-03 only | EPIC-03 | No conflict |

No shared files across EPICs — no rebase ordering constraint for shared file ownership.

**Recommended merge order (Sprint 1):** EPIC-01 → EPIC-02 → EPIC-03

Rationale: EPIC-01 (3 × S, governance doc edits) is simplest; merge first. EPIC-02 (backend + frontend) second. EPIC-03 (delegated baseline + docs) last. Arbitrary ordering since no shared files; EPIC-01 first as execution_state.json owner.

**Sprint 2 merge:** EPIC-04 merges after Sprint 2 gate confirmations (ST-11 after 2026-06-21; ST-12/13/14 after 2026-07-04).

---

## Risk Flags

| RISK-ID | Mitigation confirmed |
|---------|---------------------|
| RISK-01 (EPIC-01 CLAUDE.md §6 checklist) | Apply §6 explicitly for each ST; commit-check skill before committing — recorded |
| RISK-02 (EPIC-02 Playwright or staging sign-off for ST-05) | Playwright scenario for trade count display added to AC; flagged in staging-only check |
| RISK-03 (EPIC-03 live env access) | ST-06/07/08 classified `delegated_backend`; Infrastructure & Operations Owner coordination required |
| RISK-04 (Sprint 2 gate dates may shift) | Sprint 2 opens only after gate confirmation; ST-11 gate (2026-06-21) clears during Sprint 1 |

---

## Planning-Deferred Item Traceability

No items are deferred at planning. All 14 stories from `stage4_backlog_slice.md` enter the sprint backlog. `execution_state.json` initialisation will record all stories with `status: planned`.

Sprint 2 stories (ST-11–ST-14) are `planned` with `gate_condition` noted at initialisation (not `deferred_at_planning`).

---

## Director of Quality Readiness Check

EPIC-01: QA criteria are text-verification of governance files and version bump confirmation — sufficient for DoQ sign-off.
EPIC-02: ST-04 unit test covers happy-path query shape; ST-05 requires Playwright coverage or human staging sign-off — flagged in AC staging-only check.
EPIC-03: ST-06/07/08 are documentation evidence checks; ST-09 is document creation; ST-10 is qualitative document. DoQ sign-off criteria are review-based — sufficient.
EPIC-04: All stories are gate-conditional documents; DoQ sign-off is review-based.

No QA coverage gaps flagged by Director of Quality.
