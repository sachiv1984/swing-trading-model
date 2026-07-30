**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-30
**Cycle:** 2026-07-30__release-v8.0

# Sprint Planning Notes — 2026-07-30__release-v8.0

## Backlog Slice Source

Original — `claude/cycles/2026-07-30__release-v8.0/stage4_backlog_slice.md`. `.claude_current_state.json` `amended_backlog_slice_path` is empty; no amendment has sealed for this cycle.

## Deferred Items

None. All 19 ST items from the authoritative backlog slice enter this sprint's scope (see `sprint_capacity.md ## Conditional (Deferred)` — 0 items deferred at planning).

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-13 | ST-14 | Internal | Resolved — sequencing constraint, both in EPIC-04, no blocker |

No other cross-item dependencies identified across the 19 items. No circular dependencies found.

## Execution Sequence

1. **EPIC-01** — Data Model & Spec Integrity (ST-01, ST-02, ST-03) — fully autonomous, no dependencies. **Designated `execution_state.json` owner** (first in execution order — see Multi-EPIC Execution Notes below).
2. **EPIC-03** — QA & Test Infrastructure Hardening (ST-10, ST-11, ST-12) — fully autonomous, no dependencies.
3. **EPIC-05** — Frontend Technical Debt (ST-18) — fully autonomous, no dependencies.
4. **EPIC-02** — Security Hardening (ST-04, ST-05, ST-06, ST-07, ST-08, ST-09) — mostly autonomous; ST-08 is `delegated_backend` (live production verification).
5. **EPIC-04** — Operations & Reliability (ST-13, ST-14, ST-15, ST-16, ST-17) — all `delegated_backend` (Render dashboard / GitHub Actions secrets access required); ST-14 must land before/alongside ST-13 (shared credential pair).
6. **EPIC-06** — Governance & Engineering Process Hardening (ST-19) — `delegated_decision`, highest single-item effort (L, ~3-5 days); no other EPIC depends on it, sequenced last.

Rationale: autonomous-only EPICs (01, 03, 05) sequenced first to unblock delegation early and bank capacity; EPIC-02 next (mostly autonomous, one delegated item); EPIC-04 (fully delegated, external dashboard/secret access) and EPIC-06 (delegated decision, largest single item) sequenced last, per §5.2 "groups autonomous items before delegated items where possible."

### Multi-EPIC Execution Notes

This sprint has 6 EPIC branches active. **`execution_state.json` owner: EPIC-01** (first in execution order). All other EPIC branches (02, 03, 04, 05, 06) must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite, per `shared_standards.md §12` Rule 3 (GOVERNANCE commit after each merge) and CLAUDE.md §8 (Cross-EPIC Merge Conflict Resolution).

**Shared file ownership advisory:**

| Shared file | Owning EPIC | Note |
|-------------|-------------|------|
| `execution_state.json` | EPIC-01 | See Multi-EPIC Execution Notes above; later-merging EPICs must rebase onto `main` after EPIC-01 merges before finalising their own state additions. |
| `data_model.md` | EPIC-01 (ST-01) | No other EPIC in this sprint's scope touches `data_model.md`; recorded for completeness per §5.2 — no conflict expected. |
| `shared_standards.md` | EPIC-06 (ST-19) | ST-19's AC explicitly requires a §12 update to reference the new merge-conflict mechanism; no other EPIC in this sprint touches this file. |

No two EPICs in this sprint's scope modify the same source file outside the standard `execution_state.json` collision surface — low cross-EPIC conflict risk this sprint.

**Planning-deferred item traceability (AUD-2026-05-21-002):** 0 ST items from the authoritative backlog slice are excluded from this sealed sprint backlog — no `deferred_at_planning` entries required in `execution_state.json` at initialisation.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-02 (ST-06, ST-07) | Valid — Design Gate PASSED 2026-07-30 with decision records + `trade_plan.md` v1.3; Playwright coverage or recorded staging sign-off still required per CLAUDE.md §2 before these ACs are considered met. |
| RISK-02 | EPIC-02 (ST-08) | Valid — mitigation (narrow `--forwarded-allow-ips` scoping, live re-verification of independent rate-limit buckets) unchanged since release planning. |
| RISK-03 | EPIC-02 (ST-09) | Valid — mitigation (explicit `condition = "AND"`/`regexTarget = "match"`, local `gitleaks detect` verification per block) unchanged since release planning. |
| RISK-04 | EPIC-06 (ST-19) | Valid — mitigation (Head of Engineering sign-off before live use; existing reactive `shared_standards.md §12` mechanism kept as documented fallback) unchanged since release planning. |
| RISK-05 | Release-level | Valid — ~94-109% utilisation confirmed at STEP 4.5 Capacity Feasibility (`pass`, not `warn`); EPIC-06 (single item, most divisible) remains the natural trim candidate if early sprint velocity signals overrun. |

No risk has materialised since release planning (`release_plan.md`, 2026-07-30). No multi-vehicle fix-choice risk (§5.3 LP-14 check) identified in the risk register above — none of RISK-01 through RISK-05 name alternative fix vehicles requiring a pick-one decision at execution kickoff; all name a single mitigation path.

**LL-v2.2-SP-01 — Blocked-decision design artefact check:** ST-19 is the only `delegated_decision` item this sprint. No HoST design session or equivalent design artefact was found for it (EPIC-06 is classified `Design Not Applicable` at the Design Gate — governance/engineering mechanism, no UI). Advisory: a Head of Specs Team design/technical-approach session should be scheduled before ST-19's execution begins, given its RISK-04 mitigation explicitly requires Head of Engineering sign-off before the new mechanism is used live.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — 0 vulnerabilities found across all 59 resolved dependencies (fastapi 0.135.1, starlette 1.3.1, uvicorn 0.24.0, pandas 3.0.3, and 55 others). No high/critical CVEs to record; no PO/Head of Engineering risk acceptance required.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Schedule a HoST design/technical-approach session for ST-19 before its execution begins (LL-v2.2-SP-01 advisory) | Head of Specs Team | No — advisory only, does not block seal |
| `sprint_planning_prompt.md` itself has advanced to v3.13 with no matching `prompt_change_log.md` entry (last logged transition: v3.11→v3.12, 2026-07-02) — hygiene gap, per STEP -1 advisory 7 | Head of Specs Team | No — advisory only, does not block seal |

No outstanding action is marked `Blocker? Yes`.

## Carry-Forward Items

Carry-forward items reviewed: 1 item from cycle `2026-07-28__release-v7.10` (`lessons_learnt_closure.md ## Carry-Forward`) — `BLG-OPS-111`'s endpoint list has drifted for a 2nd consecutive cycle (composition misaligned against the live gap); implication is engine = "Post-Ship Closure" (escalate to mandatory reconciliation only if a 3rd consecutive cycle finds it still misaligned). Not actionable by Sprint Planning; no action taken here beyond this advisory note.

## Pre-Sprint Backlog Advisory

None. No items in `claude/backlog/backlog.md` carry `Provisional-Target: Before v8.0 sprint planning` (0 matches on scan).
