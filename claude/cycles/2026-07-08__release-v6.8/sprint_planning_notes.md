**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-09
**Cycle:** 2026-07-08__release-v6.8

# Sprint Planning Notes — 2026-07-08__release-v6.8

## Backlog Slice Source

Original — `claude/cycles/2026-07-08__release-v6.8/stage4_backlog_slice.md`. `.claude_current_state.json` and `state.json` both carry `amended_backlog_slice_path: ""` — no amendment in effect.

## Design Gate Root-State Sync Gap (Process Deviation — Advisory)

`claude/cycles/2026-07-08__release-v6.8/state.json` correctly records `design_gate_status: "Passed"`, `design_gate_completed_utc: "2026-07-08T20:15:00Z"`, `design_gate_record: "claude/cycles/2026-07-08__release-v6.8/design_gate.md"` (commit `028e7fed`, "17 items cleared, 0 blocked"). However, unlike every prior design-gate run (v6.1 through v6.7, each of which wrote `status: "Design_Gate_Passed"` and mirrored the `design_gate_*` fields back to the root `.claude_current_state.json`), the v6.8 design-gate commit only updated the cycle-level `state.json` — the root pointer was left at `status: "Published"` / `design_gate_status: "not_started"`. This is a real gap against established practice, not an unresolved gate: the underlying condition (Design Gate Passed) is independently verified in the cycle's own `state.json` and `design_gate.md`. Per `sprint_planning_prompt.md` STEP -1 gate 1 (`status` must be `Published`, `Validated`, or `Committed`) and gate 3 (reads `design_gate_status` from `state.json`, not the root pointer), this does not block sprint planning. The STEP 7 global state write below backfills the missed `design_gate_*` fields on the root pointer alongside the sprint-planning fields, to restore an accurate root state record — this is a data-consistency correction, not a scope decision.

## Acceptance Criteria Confirmation (STEP 4)

All 17 items' acceptance criteria (as filed in `stage4_backlog_slice.md`) confirmed against the §7 standard (Technical / Quality / Security / Verification). None required drafting from scratch — mapped below for Head of Specs Team sign-off. One AC (ST-04 AC-02) is newly flagged `[staging-only evidence]` per LL-v3.9-P3-2 (see note below the table).

| Item | Technical | Quality | Security | Verification |
|------|-----------|---------|----------|---------------|
| ST-01 (BLG-BE-46) | AC-01/02: root cause documented; if a bug, fix implemented so a newly closed trade with a plan shows `position_id` set | AC-02: confirmed via `GET /trade-plans` API response for a newly closed trade | N/A — data-linkage fix, no new external input surface | AC-03/04: backfill decision recorded; `current_roadmap.md` SI-02 row updated with corrected linked-plan count |
| ST-02 (BLG-SEC-08) | AC-01: dict keys validated against an allowlist before use as SQL column names in `update_signal()` | AC-02: regression test confirms rejection of an unrecognised key | AC-01 IS the security fix — closes a SQL-column-name injection-adjacent vector | AC-02: regression test passing in CI |
| ST-03 (BLG-SEC-07) | AC-01: manual review of existing signal records for anomalous ticker/market values | Findings documented; any anomalies filed as follow-up BLG items | Review activity itself is the security control (data-integrity audit) | Direct read of findings document confirms review completed |
| ST-04 (BLG-OPS-99) | AC-01: application `X-API-Key` provisioned and documented (storage location) | AC-02: a governed routine successfully uses it to confirm a gate condition | RISK-02: least-privilege read-only key; value never committed to a tracked file, storage location only | AC-02 **[staging-only evidence]** — requires the live production key against live production data; CI cannot reproduce this (no production credential in CI). If evidence is deferred to a post-merge live run, a backlog item must be filed before the PR opens (CLAUDE.md §2 / LL-v3.9-P3-2). |
| ST-05 (BLG-FEAT-52) | AC-01/02/03: tag add/remove endpoints, `GET /analytics/tag-performance`, PerformanceAnalytics filter UI | AC-04: confirmed at this sprint planning — `trade_tags` has no FK/service dependency on `trade_annotations`/PO-02 (descoped 2026-07-08, see `cycle_summary.md`) | New endpoints — `openapi.yaml` + `docs/specs/api_contracts/` + `backend/routers/test.py` registration required same-commit (CLAUDE.md hard rule) | AC-05: Playwright coverage (CI-capable) or recorded staging sign-off for tag input/filter UI |
| ST-06 (BLG-FEAT-71) | AC-01/02/03: indicator shows total/linked closed-trade counts and 3 gate-condition MET/NOT MET states, read live from existing endpoints | AC-04: confirmed at this sprint planning — `BLG-BE-46` (ST-01) is unresolved as of planning (20 closed trades, 0 linked, per the 2026-07-08 rebalance finding); since AC-03 requires live reads (not hardcoded), the indicator will correctly show 0 linked / NOT MET at build time and will self-correct once ST-01 merges — no additional build-time branching logic required | No new data model; reads existing `GET /trades`, `GET /trade-plans`, `GET /analytics/arc5-compliance` only | AC-05: Playwright coverage (CI-capable) or recorded staging sign-off for the indicator panel |
| ST-07 (BLG-SPEC-58) | AC-01: visual hierarchy review of dashboard homepage completed | Findings documented against post-v6.2 layout changes; gaps filed as follow-up items | N/A — review/documentation only | Direct read of review document |
| ST-08 (BLG-SPEC-59) | AC-01: canonical R-multiple cross-currency normalization spec produced | AC-02: reviewed/signed off by Metrics & Analytics Owner | N/A — spec-authoring only | Metrics & Analytics Owner sign-off recorded |
| ST-09 (BLG-SPEC-60) | AC-01: frontend spec for trailing-stop visual indicator (states/colours/placement) | AC-02: reviewed/signed off by Head of UX & Design | N/A — spec document, no UI ships | Head of UX & Design sign-off recorded |
| ST-10 (BLG-SPEC-61) | AC-01: trailing-stop effectiveness metric definition, consistent with existing conventions | AC-02: tooling assessment on version-tagging drift-detection value recorded | N/A — documentation only | Direct read confirms both ACs present |
| ST-11 (BLG-QA-64) | AC-01: each of 12 dark spec files investigated, fixed or deleted with rationale | AC-02: no remaining dark spec files per same glob-discovery method, re-run to confirm | N/A — test/spec wiring remediation | AC-02's re-run of the glob-discovery method is the verification step |
| ST-12 (BLG-GOV-134) | AC-01: CI check flags `openapi.yaml` endpoints not reflected in `api_performance_baseline.md` | AC-02: check runs in the existing quality-gate workflow | N/A — CI/CD tooling only | Quality-gate workflow run confirms the new check executes |
| ST-13 (BLG-OPS-74) | AC-01: morning briefing call logs token usage and cost | AC-02: logged data queryable/reviewable for cost-trend analysis | N/A — internal observability, no new external input surface | Unit test on the logging wrapper (CI-capable, mocks the API call) |
| ST-14 (BLG-FE-77) | AC-01: `Watchlist.js` passes ESLint with zero warnings/errors | AC-02: no functional/visual behaviour change, confirmed by existing test suite passing unmodified | N/A — pure refactor | Existing test suite + lint run in CI |
| ST-15 (BLG-OPS-61) | AC-01: v5.1/v5.2 new endpoints get latency entries in `api_performance_baseline.md` | AC-02: consistent with existing measurement methodology | N/A — documentation of latency baselines | AC-03: Infrastructure & Operations Owner sign-off |
| ST-16 (BLG-GOV-123) | AC-01/02: §14 content moved from `execution_prompt.md` to `shared_standards.md`, replaced with a reference line | Governance File Edit Checklist (CLAUDE.md §6) applies same-commit — version bump both files | N/A — governance prompt text only | AC-03/04: version bumps, changelog entries, OPERATIONAL_GUIDE §14 sync, Head of Specs Team sign-off |
| ST-17 (BLG-OPS-71) | AC-01: `docs/security/threat_model.md` covering attack surfaces, data classifications, threat actors, mitigations, gaps | AC-02: any gaps produce separate BLG items before sign-off | AC-01 IS the security deliverable | AC-03: reviewed/signed off by Cybersecurity & Trust Lead and Infrastructure & Operations Owner |

**LL-v3.9-P3-2 staging-only flag applied:** ST-04 AC-02 newly flagged `[staging-only evidence]` at this sprint planning (not pre-flagged in the backlog slice) — it requires the live production `X-API-Key` to confirm a real gate condition against live production trade data, which CI cannot reproduce without embedding a production credential. Carried into `sprint_backlog.md`'s Staging-only ACs field for ST-04.

**Director of Quality readiness check:** No test coverage gaps flagged. ST-05/ST-06 QA evidence will require either a passing Playwright suite entry or a dated staging sign-off note per CLAUDE.md's frontend-visible-change rule; ST-04's AC-02 requires a recorded live-run evidence note (see staging-only flag above) or a pre-PR backlog filing if deferred; all other items are backend/documentation/governance changes verified by direct read, CI test, or named-role sign-off — no coverage gap exists for these.

**Staging-only AC check (STEP 6.2):** ST-05 and ST-06's Verification ACs each offer Playwright (CI-capable) as a sufficient evidence path, with staging sign-off as an alternative, not a CI-incapable requirement — **Staging-only ACs: None** for both. ST-04 AC-02 is genuinely CI-incapable — **Staging-only ACs: AC-02** for ST-04. All other 14 stories: **Staging-only ACs: None** (verifiable by direct file read, CI test, or named-role sign-off).

No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders remain.

## Deferred Items

None. All 17 ST items from the authoritative backlog slice are classified `include` — within capacity (≈13.9d of ≈12–14d), owned, AC-complete, no unresolved dependency or escalation blocking any item.

## Delegation Class Confirmation

| Item | Delegation class | Justification |
|------|------------------|----------------|
| ST-01 | `autonomous` | Backend correctness fix with existing-endpoint verification path; no UX change. Design gate: Pre-Approved. |
| ST-02 | `autonomous` | Backend security fix (allowlist validation); no UI. Design gate: Pre-Approved. |
| ST-03 | `autonomous` | Manual data review/audit activity producing a findings document; no code shipped. Design gate: Not Applicable. |
| ST-04 | `autonomous` | Infrastructure/credential provisioning; no user-visible effect. Design gate: Not Applicable. |
| ST-05 | `delegated_frontend` | New user-facing capability (tag add/remove, filter controls) — design gate Required, cleared with approved `ux_spec.md` and locked frontend specs (`trade_plan.md` v0.9, `analytics.md` v2.0). Does not qualify for BLG-GOV-72 autonomous fast-path (new UX design was required, not a prop/state fix, rename, or build against a pre-existing locked spec). |
| ST-06 | `delegated_frontend` | New user-facing Reports-page section — design gate Required, cleared with approved `ux_spec.md` and locked `reports.md` v0.6. Same fast-path exclusion as ST-05 (new UX design required). |
| ST-07 – ST-17 | `autonomous` | Spec-authoring, documentation, CI tooling, refactor-with-no-behaviour-change, and governance-text items — no UX design decision required for any of the 11. Design gate: Not Applicable for all (per `design_gate.md`). |

LL-v2.0-P4-2 (test scenario gap) check: **ST-05 and ST-06 both introduce new user-facing controls** (tag input/filter UI; SI-02 gate visibility panel) and are `delegated_frontend` — per the rule, EPIC-02's `test_scenarios` must be set to `"pending — QA & Testing Owner to author before next sprint on this domain"` in `execution_state.json` at Sprint Execution's STEP 0 initialisation (`execution_state.json` is outside this engine's write scope — flagged here for the Execution Engine to apply).

LL-v2.2-SP-01 (blocked-decision design artefact) check: no item in this slice is classified `delegated_decision`. Not applicable.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-06 | ST-01 (soft) | Internal (data-coherence, not a code dependency — ST-06 AC-03 requires live reads, so it self-corrects once ST-01 merges; no build-time blocking) | Confirmed not blocking — see ST-06 AC-04 confirmation above |
| EPIC-02 (ST-05, ST-06) | EPIC-01 begun | Internal (sequencing, not blocking — release_plan.md: "After EPIC-01 begins (not blocking)") | Satisfied by Execution Sequence below |
| EPIC-03 (ST-07–ST-17) | None | — | N/A — independent of EPIC-01/EPIC-02 per `release_plan.md` Execution Plan ("Independent... all 11 items parallelisable") |

No circular dependencies detected.

## Execution Sequence

1. **EPIC-01 — Production Correctness, Security & Infrastructure** (ST-01 → ST-02, ST-03, ST-04) — sequenced first per `release_plan.md`'s explicit sequencing constraint ("S2-01's root-cause finding may affect S2-06's display of corrected linkage data"). All 4 items `autonomous`. ST-01 first (root-cause finding informs ST-06); ST-02/ST-03/ST-04 have no internal dependency and may run in any order alongside or after ST-01.
2. **EPIC-02 — Product Value Pull-Forward** (ST-05, ST-06) — begins once EPIC-01 is underway (not blocking on EPIC-01's completion). Both `delegated_frontend`; no internal dependency between ST-05 and ST-06 (may run in parallel).
3. **EPIC-03 — Spec & Governance Debt Clearance** (ST-07–ST-17) — independent of EPIC-01/EPIC-02, all 11 items `autonomous` and parallelisable per the "autonomous before delegated" grouping rule (STEP 5.2) and the release plan's own sequencing note (lowest strategic weight — first candidates to trim if capacity slips).

### Multi-EPIC Execution Notes

3 EPICs in scope (> 1) — `execution_state.json` ownership rule applies. **`execution_state.json` owner: EPIC-01** (first in execution order — explicit sequencing constraint in `release_plan.md`). EPIC-02 and EPIC-03 branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

### Shared File Ownership Advisory

Identified shared-file touchpoints across EPICs this sprint:

- **`docs/reference/openapi.yaml`, `docs/specs/api_contracts/`, `backend/routers/test.py`:** touched only by EPIC-02 (ST-05, 2 new endpoints) — no overlap with EPIC-01 or EPIC-03 (ST-12 reads `openapi.yaml` for its CI check but does not add endpoints to it).
- **`docs/operations/api_performance_baseline.md`:** touched by **both** EPIC-02 (ST-05 — new-endpoint entries required same-commit per CLAUDE.md hard rule) and EPIC-03 (ST-15 — historical v5.1/v5.2 backfill entries). Different rows, low collision risk, but EPIC-03's ST-15 branch should rebase onto `main` after EPIC-02 merges (per merge order below) to avoid a stale-file diff conflict.
- **`current_roadmap.md`:** touched by EPIC-01 (ST-01 AC-04 — SI-02 gate row correction) only.
- **Governance files (`execution_prompt.md`, `shared_standards.md`, `OPERATIONAL_GUIDE.md`, `prompt_change_log.md`):** touched by EPIC-03 (ST-16) only — CLAUDE.md §6 Governance File Edit Checklist applies same-commit.

Merge order for STEP 6.1: **EPIC-01 → EPIC-02 → EPIC-03** — matches the execution sequence above and resolves the one identified shared-file overlap (`api_performance_baseline.md`) without requiring EPIC-03 to wait on EPIC-02's full completion, only its merge.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — item's own AC-03 allows a documented decision (bug fixed / backfill deferred with rationale) as a valid completion path; investigation time-boxed to the first half-day before committing to full-fix scope, per `release_plan.md`. |
| RISK-02 | EPIC-01 (ST-04) | Valid — mitigated by scoping to a read-only, least-privilege application key; value never committed to a tracked file, storage location documented only. ST-04 AC-02 additionally flagged `[staging-only evidence]` this sprint (see AC Confirmation table). |
| RISK-03 | EPIC-02 (ST-05, ST-06) | Valid — design gate already cleared for both (`design_gate.md`, ✅ Cleared); ST-05's new-endpoint registration (openapi.yaml / api_contracts / test.py) is called out explicitly in this document's Shared File Ownership Advisory so it isn't missed at execution. |
| RISK-04 | EPIC-03 (ST-07–ST-17) | Valid — 11 concurrent items sit near the top of the 12–14 day capacity baseline (see `sprint_capacity.md` §1.3); mitigation is that all 11 are independent/parallelisable and are the first candidates to trim if early-sprint velocity signals slippage — no cross-EPIC dependency is broken by deferring any subset. |
| RISK-05 | EPIC-03 (ST-16) | Valid — ST-16's own AC-03 already requires the version bump + changelog entry + OPERATIONAL_GUIDE §14 sync; flagged here as a reminder given this is a specific, easy-to-skip checklist (CLAUDE.md §6). |

No risk has materialised since release planning. All five remain valid with their originally-recorded mitigation approach.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — no known vulnerabilities found. No High/Critical CVEs; no PO/Head of Engineering risk acceptance required.

## Hygiene Advisories (STEP -1.7)

- **Prompt change log gaps:** 5 of 12 Class 6 governed prompts have a current `**Version:**` header that exceeds the most recent target version logged in `prompt_change_log.md` (file is prepended newest-first; latest matching row checked per file):
  - `release_planning_prompt.md` — current v2.42, last logged target v2.41 (1 version gap)
  - `execution_prompt.md` — current v3.52, last logged target v3.50 (2 version gap)
  - `delivery_verification_prompt.md` — current v3.3, last logged target v3.1 (2 version gap)
  - `backlog_management_prompt.md` — current v1.11, last logged target v1.9 (2 version gap; matches `.claude_current_state.json`'s `last_rebalance_outcome` note that v1.10→v1.11 was resolved at the 2026-07-08 rebalance)
  - `roadmap_prompt.md` — current v8.4, last logged target v8.2 (2 version gap; matches the same rebalance note for v8.3→v8.4)

  Advisory only per CLAUDE.md §6 / `governance-drift` — does not block this sprint. Surfaced for Head of Specs Team follow-up; not in this engine's write scope to correct (`prompt_change_log.md` is not a Write Scope Restriction (§6) permitted path for Sprint Planning).
- **"Before Sprint Planning" backlog items:** Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v6.8 sprint planning` — no matches found. No unconverted "Before Sprint Planning" items.

## Carry-Forward Items

Most recently completed cycle: `2026-07-06__release-v6.7` (`post_ship_complete = true`). Read `lessons_learnt_closure.md ## Carry-Forward` — 2 items:

| # | Observation | Implication | Engine | Status re: v6.8 |
|---|-------------|-------------|--------|------------------|
| 1 | SI-02's trade-count gate condition remains formally unresolved for a 2nd consecutive governed-routine invocation (15 formally confirmed vs. 20 self-reported) due to no governed routine holding an application-level API key. | Roadmap/Release Planning should treat SI-02 as still gated until `LP-08` (credential provisioning) is resolved — do not accept a self-reported trade count as gate clearance. | Roadmap | **Actioned this cycle** — ST-04 (BLG-OPS-99) is firm scope in EPIC-01, directly resolving `LP-08`. ST-01 (BLG-BE-46) independently confirmed the gate is worse than tracked (0 linked, not 15) and is also firm scope. |
| 2 | `post_ship_closure.md` §7.3 cross-references a "§27 Technical Specification Gaps" section that no longer exists by that name in `Specs_Index.md`. | Next `post_ship_closure.md` revision should correct the §7.3 cross-reference. | All | Not in this sprint's scope — `post_ship_closure.md` is not touched by any of the 17 v6.8 items; no engine action required at sprint planning. |

Recorded per `shared_standards.md §16.8` — advisory only, no halt. Carry-forward items reviewed: 2 items from cycle `2026-07-06__release-v6.7`; item 1 directly actioned this sprint, item 2 out of this sprint's scope.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Backfill `design_gate_*` fields and `status` on root `.claude_current_state.json` at STEP 7 (see "Design Gate Root-State Sync Gap" above) | PMO Lead (this engine, STEP 7) | Yes — part of this run's own completion condition, not a seal blocker in the AC sense |
| Prompt change log gaps (5 files) — see Hygiene Advisories | Head of Specs Team | No — advisory only |

No outstanding action is a seal blocker.

## Capacity WARN Acknowledgement

Not applicable — capacity check outcome is `pass` (≈13.9d vs ~12–14d available, near top of range but within it). `capacity_warn_acknowledged` will be omitted/`false` at STEP 7.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v6.8 sprint planning` — no matches found. No unconverted "Before Sprint Planning" items.
