**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-16
**Cycle:** 2026-09-15__release-v9.5

# Sprint Planning Notes — 2026-09-15__release-v9.5

## Backlog Slice Source

Original — `claude/cycles/2026-09-15__release-v9.5/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in both `.claude_current_state.json` and `state.json` — no amendment sealed this cycle).

## Carry-Forward Items

Reviewed `claude/cycles/2026-09-14__release-v9.4/lessons_learnt_closure.md ## Carry-Forward` (most recently completed cycle, `post_ship_complete = true`): 4 items present. Item 1 (release-planning over-capacity selection method / SLA mid-sprint surfacing carry) and item 2 (stale-carry-forward-claim finding) are scoped to `Release Planning`/`Post-Ship Closure`. Item 3 (deviation-consolidation scan-method watch) and item 4 (same-cycle-application pattern confirmation) are scoped to `Post-Ship Closure`. None targets `Sprint Planning` or `All`. No action required this run.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v9.5 sprint planning` — 0 matches. No unconverted items to surface.

## Deferred Items

All 43 items in the authoritative backlog slice enter this sprint (`include`) — see STEP 3 Scope Selection. No item is deferred out of the sealed slice at Sprint Planning. Items excluded from v9.5 scope entirely were dispositioned at Release Planning (not re-litigated here, per §1 — this routine does not alter the release plan):

| Item | Reason | Next Sprint Candidate? |
|------|--------|-------------------------|
| `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` | Substantively gate-blocked by their own body text (no formal `Gate` field but explicitly not-ready) | Yes, once gate fields are normalised |
| 130 formally gated/conditional items | No clearance evidence this cycle (data-density/AI-adoption/§13-review gates unchanged) | Gate-dependent |
| 19 further ungated P3/P4 items (~16.80d) | Capacity — ready pool (62 items/~43.79d) exceeds the confirmed band even at full-capacity selection | Yes — available for `plan release v9.6` |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-24 (`BLG-SPEC-57`, data model v3 pre-def) | ST-23 (`BLG-SPEC-56`, Arc 4 API contract stubs) | Internal (soft) | ST-24's own AC requires the Arc 4 API contracts to "reference the pre-defined model where applicable" — sequence ST-24's model pre-definition before or alongside ST-23 so the cross-reference has something to point to; if both land in the same session, add the cross-link last |
| ST-42 (`BLG-FE-176`, toast timing) | ST-41 (`BLG-FE-175`, motion timing) | Shared-file (spec) | Both edit `design_system.md` — ST-41 removes components from the known-non-compliant list, ST-42 updates the non-conforming-screens table. Different sections, but sequence sequentially (not parallel commits) or combine into one commit to avoid a collision on the same file, mirroring the EPIC-05 pattern below |
| ST-38 (`BLG-GOV-323`, cost-per-cycle rollup) | ST-37 (`BLG-GOV-322`, pairing rotation note) | Shared-file (spec) | Both add new sections to `workforce_capacity.md` (per RISK-05) — sequence one commit landing before the other starts editing, or implement both in a single commit with both sections present |
| EPIC-01 (ST-01) | — | N/A | `BLG-BE-117` is CI-blocking for every open/future PR — sequence ST-01 first within EPIC-01 and ideally first across the whole cycle so downstream EPIC PRs stop inheriting a red CI state |

No circular dependencies identified. No dependency crosses an EPIC boundary this cycle — each EPIC's touched files (backend modules, `docs/ops/*`, `docs/specs/*`, `workforce_capacity.md`, frontend components) are domain-distinct from every other EPIC's, unlike `2026-09-14__release-v9.4`'s cross-EPIC `design_system.md`/`dashboard.md` contention.

## Execution Sequence

Per `release_plan.md ## Execution Plan`: EPIC-02 through EPIC-06 carry "No UI ACs; independent of other EPICs" (EPIC-06 is UI-bearing but self-contained) — no forced cross-EPIC ordering except EPIC-01's CI-blocking priority. Chosen execution order (also the merge order — see `sprint_backlog.md`):

1. **EPIC-01** — Backend & Platform Engineering Debt (`ST-01`/`BLG-BE-117` is CI-blocking — land first across the whole cycle; `execution_state.json` owner)
2. **EPIC-02** — Operations & Security Debt (no cross-EPIC dependency)
3. **EPIC-03** — QA & Test Coverage Debt (no cross-EPIC dependency)
4. **EPIC-04** — Spec & Documentation Debt (no cross-EPIC dependency; internally, ST-24 before/alongside ST-23)
5. **EPIC-05** — Governance Process Debt (internally, ST-37 before ST-38 on `workforce_capacity.md`)
6. **EPIC-06** — Frontend & UX Debt (internally, ST-41 before ST-42 on `design_system.md`; design-gate-cleared)

**Multi-EPIC `execution_state.json` ownership:** EPIC-01 (first in execution order) owns `execution_state.json`. EPIC-02 through EPIC-06 must check for its existence before creating their own version — if found, read and append their own EPIC section rather than overwrite.

**Shared file ownership advisory:** No file is touched by more than one EPIC this cycle — the only shared-file contention is intra-EPIC (`workforce_capacity.md` within EPIC-05; `design_system.md` within EPIC-06), both resolved by within-EPIC sequencing above, not by a cross-EPIC merge-order rule.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|------------------|--------------------|
| RISK-01 | EPIC-01 (ST-04) | Valid — diff all 3 existing ATR trailing-stop implementations line-by-line before writing the shared version; preserve whichever behaviour the existing passing tests actually exercise; file any unclear divergence as its own item rather than guess |
| RISK-02 | EPIC-02 (ST-05) | Valid, with an added environment note: `BLG-OPS-159`/ST-12 (this same EPIC) documents a prior confirmed gotcha that Render dashboard-only settings (deploy path filters) are invisible to repo search — the same class of gap plausibly applies to dashboard-configured cron schedules. ST-05's "Render dashboard checked" AC therefore likely requires a live login to the Render dashboard UI, not something derivable from `render.yaml` or other repo config alone. Classified `delegated_decision` in `sprint_backlog.md` for this reason. Scope remains capped to investigation + documentation per RISK-02's original mitigation — any confirmed live gap's remediation is filed as a new backlog item, not absorbed here |
| RISK-03 | EPIC-03 (ST-18, ST-21) | Valid — re-count against current repository state before applying any fix, rather than trusting the filed 39/30 counts as still accurate |
| RISK-04 | EPIC-04 (ST-22) | Valid — re-confirmed this session (`DATABASE_URL` still unset in this execution environment, consistent with every prior cycle's own risk register back to v9.2). Implement/prepare the confirmation query regardless; disclose explicitly rather than fabricate if still unavailable at execution. Classified `delegated_decision` in `sprint_backlog.md` |
| RISK-05 | EPIC-05 (ST-37, ST-38) | Valid — sequencing (ST-37 before ST-38 on `workforce_capacity.md`) adopted in Dependency Map above as the primary mitigation |
| RISK-06 | EPIC-06 (ST-40–ST-43) | **Resolved** — `run design-gate --cycle 2026-09-15__release-v9.5` passed (`design_gate.md`, 2026-09-15, 43/43 cleared, 0 blocked); `sprint_planning_pre_condition` met |

No risk has materialised since Release Planning; all mitigation approaches remain valid as stated. One additional intra-EPIC file-contention note (ST-41/ST-42 on `design_system.md`) was found during this session's own dependency mapping and is recorded above — it was not named in the release-planning risk register.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` — **clean**. 58 dependencies scanned, 0 known vulnerabilities, 0 fixes required. Trend row appended to `docs/ops/pip_audit_trend_log.md` in this session (see that file for the full row).

## Recurring Endpoint Test Coverage Audit

`python3 scripts/audit_endpoint_test_coverage.py` — **clean**. 91 route decorators scanned across 26 router files; 8 documented `KNOWN_GAPS` exclusions; 0 undocumented gaps.

## Prompt Change Log Gap Check

Applied the date-scan method (`shared_standards.md §11.1`) across all 12 Class 6 prompt files under `claude/system/*_prompt.md`, not just `sprint_planning_prompt.md` itself: for each filename, collected every matching row in `prompt_change_log.md`, selected the latest-dated row, and compared its target version against the file's current header. All 12 match with no gap:

| File | Header version | Latest logged | Gap? |
|------|-----------------|----------------|------|
| `amendment_cycle_prompt.md` | v1.9 | v1.9 (2026-07-02) | No |
| `backlog_management_prompt.md` | v1.17 | v1.17 (2026-09-09) | No |
| `delivery_verification_prompt.md` | v3.11 | v3.11 (2026-09-14) | No |
| `design_gate_prompt.md` | v1.10 | v1.10 (2026-09-08) | No |
| `execution_prompt.md` | v3.76 | v3.76 (2026-09-15) | No |
| `idea_intake_prompt.md` | v2.8 | v2.8 (2026-07-27) | No |
| `ideas_housekeeping_prompt.md` | v1.2 | v1.2 (2026-08-04) | No |
| `lessons_learnt_prompt.md` | v1.14 | v1.14 (2026-09-14) | No |
| `release_planning_prompt.md` | v2.52 | v2.52 (2026-09-15) | No |
| `roadmap_management_prompt.md` | v1.5 | v1.5 (2026-08-18) | No |
| `roadmap_prompt.md` | v9.21 | v9.21 (2026-09-15) | No |
| `sprint_planning_prompt.md` | v3.18 | v3.18 (2026-09-08) | No |

## Preflight Vocabulary Drift Advisory (found this session)

`sprint_planning_prompt.md` STEP -1 Hard Gate 1 text requires the root `.claude_current_state.json.status` to be `Published`, `Validated`, or `Committed` at invocation. The actual value at this invocation was `Design_Gate_Passed` — not in that literal list. This engine instead applied the authoritative Lifecycle Guard (`shared_standards.md §10.1`), which explicitly names `Design_Gate_Passed` as a valid Sprint Planning from-state, and proceeded on that basis — `Design_Gate_Passed` is the correct, expected status once a design-gate-required cycle has passed its gate (as this one did, `design_gate.md`, 2026-09-15). Separately, Hard Gate 2 requires the cycle-level `state.json.status` to read `Published`; the actual value is `Validated` (matching `release_planning_prompt.md`'s own STEP 6B.6/line-1151 terminology and the identical pattern already present in the immediately prior cycle, `2026-09-14__release-v9.4`, which sealed and closed successfully under the same reading). Both readings are treated as satisfied under the current, more specific governing text rather than the older literal enum in STEP -1 itself. Recommend filing a backlog item to reconcile STEP -1's Hard Gates 1 and 2 wording with `shared_standards.md §10.1` and `release_planning_prompt.md`'s current status vocabulary, so a future reviewer does not have to re-derive this cross-reference from scratch. No halt was warranted — both the Lifecycle Guard and the cycle's own `state.json` (`publish_eligible: true`, `open_escalations: []`) independently confirm this cycle is genuinely sealed and ready.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|-------------------------|
| Buffer-floor-exceeded acknowledgement (27.99d / 28d = 99.96%) | Product Owner | No — advisory only; acknowledged via the standing "use full capacity" instruction (see `sprint_capacity.md §1.5`) |
| File a backlog item reconciling `sprint_planning_prompt.md` STEP -1 Hard Gates 1–2 status-vocabulary wording against `shared_standards.md §10.1` | Head of Specs Team | No — advisory, not a seal blocker |
| Confirm at execution whether ST-05's "Render dashboard checked" AC requires a live dashboard login (no repo-derivable substitute per the `BLG-OPS-159` gotcha) | Infrastructure & Operations Owner | No — captured in `sprint_backlog.md` delegation class, not a seal blocker |
| Confirm at ST-43 execution whether the new threshold/remaining-count copy needs a new Playwright assertion beyond the existing `arc5-compliance-section.spec.js` suite, or whether existing coverage already exercises it; file a backlog item before the PR opens if deferred to staging (per CLAUDE.md §2) | Base44 Frontend Prompt Owner / Director of Quality | No — flagged in `sprint_backlog.md`, resolved at execution time |

No outstanding action is marked `Blocker? Yes`.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-09-16 | Initial publication — dependency map, execution/merge sequence, risk flags, and hygiene checks for 2026-09-15__release-v9.5. |
