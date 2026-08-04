# Sprint Planning Notes — 2026-08-04__release-v8.2

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-04
**Cycle:** 2026-08-04__release-v8.2

## Backlog Slice Source

Original — `claude/cycles/2026-08-04__release-v8.2/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in both `.claude_current_state.json` and `state.json`; no amendment in effect).

## Deferred Items

None. All 25 items in the authoritative backlog slice are classified `include` — full scope enters the sprint. No items were deferred at Sprint Planning (capacity check outcome `pass`, no over-allocation).

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-06 (EPIC-02, BLG-SEC-27) | — | sequencing precedence | Should land before/alongside ST-07 (RISK-02 — both touch staging environment config) |
| ST-07 (EPIC-02, BLG-OPS-128) | ST-06 (soft — coordinate, not blocking) | sequencing precedence | Per RISK-02 mitigation: sequence after or alongside ST-06; if run in parallel, note the key-rotation window in the ST-07 PR so a transient drift reading isn't mistaken for a genuine webhook failure |
| All other items (ST-01–ST-05, ST-08–ST-25) | None | — | `release_plan.md ## Execution Plan` records "Sequencing constraint: None" for EPIC-01, EPIC-03, EPIC-04, EPIC-05 |

No circular dependencies. No spec-lock dependencies outstanding — Design Gate already Passed for EPIC-01 (the only EPIC with a UI surface); all other EPICs are Design Not Applicable.

**Acceptance criteria confirmation (STEP 4):** All 25 items carry acceptance criteria in `stage4_backlog_slice.md` (bullet-list convention, consistent with this project's established backlog-slice format). Reviewed for Section 7 adequacy: each item's bullets collectively state observable/testable technical criteria, a verification method (sign-off role, Playwright/staging evidence, or CI/audit check), and — where applicable — explicit security criteria. Items with no security surface change (the majority — governance/documentation/process/CI items) carry an implicit "N/A — no security surface changed" per Section 7's permitted justification; ST-06/ST-07 (EPIC-02) carry explicit security criteria inherently (credential rotation, staging drift detection). No item is missing verification evidence. No `[AC REQUIRED]` placeholders needed.

**Staging-only AC check (pre-staged per Section 7 / STEP 6.2):**
- **ST-01–ST-04** (EPIC-01): `stage4_backlog_slice.md` EPIC-01 header names these plus ST-01 as carrying observable UI acceptance criteria (RISK-01) requiring Design Gate PASS (already confirmed, `design_gate.md`) plus Playwright coverage or a recorded staging sign-off. All four are standard render/interaction/colour/focus-ring assertions — Playwright-verifiable in CI (extending existing component test patterns, per the design gate's confirmed-pattern rationale for ST-03/ST-04/ST-05). **Not** staging-only-evidence; Playwright coverage or staging sign-off is required as the general CLAUDE.md §2 observable-AC rule, not because CI cannot reproduce it (same treatment as `v8.1` ST-01 precedent).
- **ST-06** (EPIC-02): AC "Confirmed live: the old shared key no longer works against production after rotation" is genuinely CI-unreproducible — requires live production credential rotation and a post-rotation confirmation against the real production API. Flagged **`[staging-only evidence]`**. The delegated_backend implementer performs this confirmation as part of delivering the story itself (same pattern as `v8.1` ST-10: the story *is* the live-verification deliverable) — no separate pre-PR backlog item required under CLAUDE.md §2, since the evidence is not being deferred past the PR, it's produced within it.
- **ST-07** (EPIC-02): "Confirmed firing correctly on a deliberately-stale test" is achievable via a simulated stale-SHA test harness within CI/repo tooling, not requiring a live production hit — **not** staging-only-evidence. Root-cause diagnosis of the GitHub↔Render webhook itself may require the Render dashboard (build/deploy filter configuration is dashboard-only and not visible via repo search or CLI — a known operational gotcha); this is a delegation-class consideration (see below), not a staging-only-AC one.
- All other items (ST-08–ST-05 excluded above, ST-08–ST-25 minus ST-06/ST-07): no live external API / staging-only verification implied — verifiable via code review, CI, audit script, or documentation review.

## Execution Sequence

**Sequencing note:** EPIC-01, EPIC-03, EPIC-04, and EPIC-05 carry no cross-item or cross-EPIC dependencies and are entirely `autonomous` (see Delegation Class table below) — sequenced first, per STEP 5.2's "group autonomous items before delegated items where possible." EPIC-02 (both items `delegated_backend`) is sequenced last. Within EPIC-02, ST-06 precedes ST-07 per RISK-02. EPIC-01 leads the autonomous block, consistent with the release's explicit "user features first" instruction (`release_plan.md §Readiness`) and its already-cleared Design Gate.

1. **EPIC-01** — User-Facing Features & UX (ST-01–ST-05) — `autonomous` (all 5)
2. **EPIC-03** — Governance Process Integrity Cluster (ST-08–ST-18) — `autonomous` (all 11)
3. **EPIC-04** — Operations & CI Hardening (ST-19–ST-21) — `autonomous` (all 3)
4. **EPIC-05** — QA & Spec Debt Cleanup (ST-22–ST-25) — `autonomous` (all 4)
5. **EPIC-02** — Staging/Production Security Hardening (ST-06, ST-07) — `delegated_backend` (both)

**Delegation class assignment (STEP 3.1):**

| Item | Delegation Class | Rationale |
|------|-------------------|-----------|
| ST-01 | autonomous | New reconciliation view against an already-produced design decision record (`pnl-reconciliation-report/decision_record.md`) and locked spec (`reports.md` v0.13); implementation-only, no outstanding UX decision |
| ST-02 | autonomous | New empty-state implemented against a locked spec (`positions.md` v2.7) with confirmed Playwright feasibility — BLG-GOV-72 fast-path (c) |
| ST-03 | autonomous | Pre-approved 3-line CSS colour-token change per the existing v6.0 RFJ design review — BLG-GOV-72 fast-path (a)-adjacent, no new UX decision |
| ST-04 | autonomous | Prop/class fix against an already-mandated pattern (`design_system.md` v1.4); no UX change — BLG-GOV-72 fast-path (a) |
| ST-05 | autonomous | New stat card reusing an existing verified display pattern (`SI02GateStatusSection`); metric-definition task, no new UI decision |
| ST-06 | delegated_backend | Requires live production credential provisioning/rotation and a live post-rotation confirmation against production — not implementable by the execution engine alone |
| ST-07 | delegated_backend | Diagnosing the GitHub↔Render webhook failure plausibly requires the Render dashboard (build/deploy path filters are dashboard-only, not visible via repo search — a known operational gotcha); sequenced alongside ST-06 per RISK-02, both touch staging environment config outside the repo |
| ST-08 | autonomous | Evidence compilation + Product Owner activation-decision recording, within the routine's own agent-mediated Product Owner role; documentation/review task |
| ST-09 | autonomous | Row-count audit against `claude/cycles/`; scriptable/verifiable directly |
| ST-10 | autonomous | Formula review against `metrics_definitions.md` and the v6.9 recheck event type; documentation review task |
| ST-11 | autonomous | Governance prompt logic amendment (`post_ship_closure.md`); standard governance file edit |
| ST-12 | autonomous | Desk review of vendor ToS/DPA terms against known financial-data handling; documentation task, no live vendor negotiation required |
| ST-13 | autonomous | Structured append-only log creation + backfill from known historical instances; documentation task |
| ST-14 | autonomous | Retrospective against existing idea-intake window records; documentation task |
| ST-15 | autonomous | Decision recording (option (a) or (b)); if option (a) is chosen and requires live production credential provisioning, that sub-step would need `delegated_backend` — flagged under Risk Flags (LP-14) below, resolved at execution kickoff |
| ST-16 | autonomous | Governance prompt amendment (`design_gate_prompt.md`); standard governance file edit |
| ST-17 | autonomous | Documentation convention added to `shared_standards.md`; standard governance file edit |
| ST-18 | autonomous | CI/CD automation fix (`governance_sync.yml` regex) + documentation; no live decision required |
| ST-19 | autonomous | Cadence documentation + first review scheduling; no execution decision required |
| ST-20 | autonomous | CI cache configuration tuning (dependency/browser-binary caching) for the Playwright job; repo-scoped change |
| ST-21 | autonomous | Pre-commit hook script addition; repo-scoped change |
| ST-22 | autonomous | Snapshot/assertion test addition against an AST-derived count; scriptable |
| ST-23 | autonomous | Changelog reconstruction from `git log -p`; documentation task |
| ST-24 | autonomous | Dead-code removal; repo-scoped change |
| ST-25 | autonomous | Governance prompt checklist addendum (`design_gate_prompt.md`); standard governance file edit |

**LL-v2.2-SP-01 (blocked-decision design artefact, advisory):** No `delegated_decision` items this sprint — not applicable.

**LL-v2.0-P4-2 (test-scenario gap):** Not applicable — no `delegated_frontend` item in this sprint's scope (EPIC-01's items are all `autonomous`, implemented against already-locked specs/decision records with confirmed Playwright feasibility).

## Multi-EPIC Execution Notes

**Per-EPIC `execution_state` mechanism (current standard, `shared_standards.md` §12.1 — retired the legacy shared-file mechanism as of `v8.1` ST-19):** Each EPIC branch owns exactly one file, `claude/cycles/2026-08-04__release-v8.2/execution_state/EPIC-xx.json`, and writes only to it. Cycle-level fields (`sprint_goal`, `backlog_slice_source`, `invoked_utc`, `mode`, `open_escalations`, `process_notes`, `sealed`, `sealed_utc`) live in `claude/cycles/2026-08-04__release-v8.2/execution_state/_cycle_meta.json`, owned by **EPIC-01** (first EPIC in execution order, per the standing "first to open, absent a designation" rule). `claude/cycles/2026-08-04__release-v8.2/execution_state.json` is a computed, regenerate-on-read summary (`generate_execution_summary.py`) — never hand-edited or hand-merged; regenerate it after every EPIC merge per `shared_standards.md` §12.1 Rule 3.

**Shared file ownership advisory:**

| Shared file | EPICs touching it | Ownership / rebase note |
|---|---|---|
| `execution_state/_cycle_meta.json` | All 5 (cycle-level fields) | EPIC-01 owns it (first to open); the per-EPIC mechanism means no other EPIC writes to it |
| `claude/system/design_gate_prompt.md` | EPIC-03 (ST-16 — mandatory §13 boundary pre-check addition) and EPIC-05 (ST-25 — motion/timing-sensitive interaction checklist addendum) | EPIC-03 merges before EPIC-05 in execution sequence (position 2 vs. 4); EPIC-05's branch must rebase onto `main` after EPIC-03 merges before finalising its own `design_gate_prompt.md` edit, and apply the standard governance file edit checklist (CLAUDE.md §6) reflecting both changes' cumulative version bump |
| `claude/system/shared_standards.md` | EPIC-03 only (ST-17 retention convention, ST-18 §8 convention documentation) — both within the same EPIC, sequential within-EPIC edits, no cross-EPIC conflict | N/A — single-EPIC ownership |
| `OPERATIONAL_GUIDE.md` §14 / `prompt_change_log.md` | Any EPIC-03 item bumping a governance prompt version (ST-11, ST-16, ST-17) and EPIC-05 (ST-25) | Same rebase-after-EPIC-03 rule applies to EPIC-05 for its `design_gate_prompt.md`-driven §14 row update |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01–ST-04) | Valid — Design Gate already PASSED (`design_gate.md`, ST-01/ST-02 Design Required with decision records + spec bumps; ST-03/ST-04/ST-05 Design Pre-Approved); Playwright coverage or recorded staging sign-off remains an execution-phase evidence obligation per CLAUDE.md §2 (see Staging-only AC check above) |
| RISK-02 | EPIC-02 (ST-06, ST-07) | Valid — mitigation operationalised via Execution Sequence (ST-06 before ST-07, both sequenced last as the sprint's only delegated EPIC) and the rotation-window note required in the ST-07 PR |
| RISK-03 | Release-level (EPIC-03 governance-process skew, ~44% of scope) | Advisory only — not actionable at Sprint Planning; EPIC-03's 11 items are individually small and independently divisible, confirmed as the natural trim candidate if velocity signals overrun (unchanged from `release_plan.md`) |
| RISK-04 | Release-level (~88-103% utilisation) | Valid — STEP 1 capacity recheck (`sprint_capacity.md`) confirms no over-allocation against the ~24-28 day ceiling; buffer-floor advisory (§1.5) surfaced and acknowledged by Product Owner (see `sprint_capacity.md`) |

**Multi-vehicle fix-choice risk check (LP-14):** ST-15 (EPIC-03, BLG-GOV-279) names two alternative remediation paths — (a) persist the credential into checked-in-but-gitignored environment config, or (b) formally accept the fallback-citation pattern as standing behaviour. Checked for material effort divergence: both paths fall within the same S (~1.0 day) effort band recorded in `sprint_capacity.md` — no material sizing difference recorded, though option (a) would additionally require `delegated_backend` handling for the actual credential provisioning step if chosen (see Delegation Class table). No `### Phasing Recommendation` exists this cycle (capacity outcome was `pass`, not `warn`), so no boundary cross-reference is needed. The choice is left to resolve at execution kickoff per the item's own acceptance criteria; recorded here per LP-14 to surface the risk at planning time.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` run via `backend/.venv/bin/python3 -m pip_audit` (the project virtualenv per CLAUDE.md §9 — the bare `pip-audit` binary is not on PATH). Result: **clean** — no known vulnerabilities across all 58 resolved dependencies. Advisory check only; no action required.

## Endpoint Test Coverage Audit (STEP -1.8, ST-11 v3.15 addition)

`python3 scripts/audit_endpoint_test_coverage.py`: 78 route decorators scanned across 23 router files. 8 documented `KNOWN_GAPS` exclusions, 0 undocumented gaps. **Clean.**

## Carry-Forward Items

Carry-forward items reviewed: 2 items from cycle `2026-08-03__release-v8.1` (`lessons_learnt_closure.md`):
1. Only 1 of 19 scoped items at `v8.1` was genuinely user-facing, despite explicit instruction to prioritise user features — tagged Engine: Roadmap, not directly actionable at Sprint Planning. Note: `v8.2`'s own scope shows material improvement on this front (5 of 25 items, ~24% of effort, are user-facing/user-adjacent per `release_plan.md`'s own Advisory Findings) — awareness only.
2. `post_ship_closure.md` STEP 5.1 cross-cycle deviation consolidation review cadence-field initialisation — tagged Engine: Post-Ship Closure, not actionable at Sprint Planning.

Neither carry-forward item requires a Sprint Planning action this cycle.

## Pre-Sprint Backlog Advisory

No backlog items found with `Provisional-Target: Before v8.2 sprint planning` (checked via direct grep — zero matches).

## Hygiene Advisory

`sprint_planning_prompt.md` current v3.15 — last logged transition in `prompt_change_log.md` is v3.14→v3.15 (2026-08-03). No gap. Clean.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Provision live production credential rotation and post-rotation confirmation as part of ST-06's own delivery evidence | Cybersecurity & Trust Lead | No |
| Coordinate the ST-06/ST-07 staging-config rotation window and note it in the ST-07 PR (RISK-02) | Infrastructure & Operations Owner | No |
| Resolve ST-15's two-vehicle remediation choice at execution kickoff (LP-14) | Product Owner | No |
| Rebase EPIC-05's `design_gate_prompt.md` edit onto `main` after EPIC-03 merges, before finalising ST-25 | Head of UX & Design / Head of Engineering | No |
