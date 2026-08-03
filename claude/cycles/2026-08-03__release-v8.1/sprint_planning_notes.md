# Sprint Planning Notes — 2026-08-03__release-v8.1

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-03
**Cycle:** 2026-08-03__release-v8.1

## Backlog Slice Source

Original — `claude/cycles/2026-08-03__release-v8.1/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in both `.claude_current_state.json` and `state.json`; no amendment in effect).

## Deferred Items

None. All 19 items in the authoritative backlog slice are classified `include` — full scope enters the sprint. No items were deferred at Sprint Planning (capacity check outcome `pass`, no over-allocation).

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 – ST-19 (all) | None | — | No cross-item dependencies identified — `release_plan.md ## Execution Plan` records "Sequencing constraint: None" for all 7 EPICs |

No circular dependencies. No spec-lock dependencies (Design Gate already Passed for the one EPIC with a UI surface, ST-01; all others are Design Not Applicable).

**Acceptance criteria confirmation (STEP 4):** All 19 items carry acceptance criteria in `stage4_backlog_slice.md` (bullet-list convention, consistent with this project's established backlog-slice format). Reviewed for Section 7 adequacy: each item's bullets collectively state observable/testable technical criteria, a verification method (sign-off role, Playwright/staging evidence, or CI check), and — where applicable — explicit security criteria (ST-08's PII scan gate). Items with no security surface change (the majority — governance/documentation/process items) carry an implicit "N/A — no security surface changed" per Section 7's permitted justification; no item is missing verification evidence. No `[AC REQUIRED]` placeholders needed.

**Staging-only AC check (pre-staged per Section 7 / STEP 6.2):**
- **ST-01** (EPIC-01): observable UI interaction AC (keyboard/focus tag-suggestion), but Playwright-verifiable in CI (extends the existing correct `TradeEntry.js` pattern) — **not** staging-only-evidence; Playwright coverage or staging sign-off is required as the general CLAUDE.md §2 observable-AC rule, not because CI cannot reproduce it.
- **ST-10** (EPIC-04): `stage4_backlog_slice.md` EPIC-04 header states "ST-10 is itself a staging-only verification task (no CI-reproducible equivalent)" — genuinely staging-only (live market price crossing, live Telegram delivery). This story **is** the backlog item that closes the obligation (`BLG-QA-115`) — no further backlog filing needed per CLAUDE.md §2's "file before PR opens" clause, since the staging run itself is the story's deliverable.
- All other items (ST-02–ST-09, ST-11–ST-19): no live external API / staging-only verification implied — verifiable via code review, CI, or the standard test suite.

## Execution Sequence

**Sequencing note (dependency-based override of numeric EPIC order):** EPIC-07 (`ST-19`) is sequenced **first**, ahead of EPIC-01, because it implements the new per-EPIC `execution_state.json` mechanism (Option 1) that this very item delivers. RISK-02's stated mitigation intent is for this sprint to be the mechanism's first live use — landing EPIC-07 before any other EPIC branch opens for execution avoids a mixed sprint where 6 EPICs write to the legacy shared `execution_state.json` and EPIC-07 migrates mid-flight. See "Multi-EPIC Execution Notes" below.

1. **EPIC-07** — Cross-EPIC Execution State Structural Fix (ST-19) — `autonomous`
2. **EPIC-01** — User-Facing Accessibility Fix (ST-01) — `autonomous`
3. **EPIC-03** — Governance Process Hardening (ST-03–ST-09) — `autonomous` (all 7)
4. **EPIC-06** — Backend Hardening (ST-17, ST-18) — `autonomous`
5. **EPIC-04** — QA Process & Debt Closure (ST-11, ST-12, ST-13 `autonomous`; ST-10 `delegated_qa`)
6. **EPIC-02** — Operational Safety (ST-02) — `delegated_backend`
7. **EPIC-05** — Spec Debt: SI-02 Definitional Clarity (ST-15 `autonomous`; ST-14, ST-16 `delegated_decision`)

Rationale: after EPIC-07 (structural prerequisite) and the quick EPIC-01 win, remaining `autonomous` EPICs (03, 06) are grouped ahead of EPICs carrying delegated items (04, 02, 05), per STEP 5.2's "group autonomous items before delegated items to unblock delegation early."

**Delegation class assignment (STEP 3.1):**

| Item | Delegation Class | Rationale |
|------|-------------------|-----------|
| ST-01 | autonomous | Prop/attribute fix (`onMouseDown`→`onClick`) against an existing, already-correct reference pattern in `TradeEntry.js`; no UX change — BLG-GOV-72 fast-path (a) |
| ST-02 | delegated_backend | Requires live production Supabase infrastructure access (cron/schedule configuration, restore dry-run against a non-production target) — not implementable by the execution engine alone |
| ST-03 | autonomous | Governance criteria drafting + retroactive application; documentation task |
| ST-04 | autonomous | Escalation-clause drafting for `roadmap_prompt.md` STEP 2.4; documentation task |
| ST-05 | autonomous | Capacity-buffer-floor recommendation drafting; documentation task |
| ST-06 | autonomous | Consolidated registry build from existing backlog categories; documentation task |
| ST-07 | autonomous | Rotation-guideline documentation; no execution decision required |
| ST-08 | autonomous | CI check implementation (regex scan over `openapi.yaml` schemas) + self-verifiable test-PR firing; no UX/human decision |
| ST-09 | autonomous | Governance file edit (one of two named remediation paths) via the standard edit checklist |
| ST-10 | delegated_qa | Staging-only evidence — human staging run against live market price + Telegram delivery required |
| ST-11 | autonomous | Scriptable audit comparing `@router.*` decorators against `test.py` entries |
| ST-12 | autonomous | Consolidation review of existing DEV-* records; documentation task |
| ST-13 | autonomous | Shard-runtime audit against existing CI data |
| ST-14 | delegated_decision | Product/strategy threshold decision (Gate Condition 2/3 definitions) — requires Product Owner + Strategy Rules & System Intent Owner judgment, not an engineering determination |
| ST-15 | autonomous | Documentation note addition to `strategy_rules.md`; confirms existing scope, no new decision |
| ST-16 | delegated_decision | Product/strategy threshold decision (exact trade-count/window definition) — same class as ST-14 |
| ST-17 | autonomous | Backend pattern documentation + helper implementation + reference migration; no UX/human decision |
| ST-18 | autonomous | Backfill scoping document (technical approach, effort, risk) — a deliverable document, not a live decision |
| ST-19 | autonomous | Engineering implementation of an already-reviewed-and-signed-off design (per `release_plan.md` Execution Plan note) — implementation-only |

**LL-v2.2-SP-01 (blocked-decision design artefact, advisory):** ST-14 and ST-16 are `delegated_decision` items. No dedicated HoST design-session artefact exists for either (they are product/strategy threshold decisions, not UX-shaped work, so a HoST design session is not the natural artefact type) — `docs/product/decisions/decisions--2026-08-03__release-v8.1.md` does not cover these thresholds. Advisory: a Product Owner + Strategy Rules & System Intent Owner decision session should be scheduled before ST-14/ST-16 execute.

**LL-v2.0-P4-2 (test-scenario gap):** Not applicable — no `delegated_frontend` item in this sprint's scope.

## Multi-EPIC Execution Notes

**`execution_state.json` ownership (Required — 7 EPICs in scope):** EPIC-07 is designated the `execution_state.json` structural-transition owner and is sequenced first (see Execution Sequence above). Until EPIC-07 merges to `main`, any EPIC branch that must open before it lands is subject to the **legacy** shared `execution_state.json` mechanism (`shared_standards.md` §12: merge in dependency order, keep the later-merged branch's state on conflict, GOVERNANCE-commit reconciliation after each merge). Once EPIC-07 merges, subsequent EPIC branches (EPIC-01, 03, 06, 04, 02, 05 in that order) should create their own `execution_state/EPIC-xx.json` file per the new mechanism rather than writing to the legacy shared file — this sprint is the mechanism's first live use, consistent with RISK-02's stated intent in `release_plan.md`.

**Shared file ownership advisory (Required — 7 EPICs in scope):**

| Shared file | EPICs touching it | Ownership / rebase note |
|---|---|---|
| `execution_state.json` (legacy) → `execution_state/EPIC-xx.json` (new) | All 7 (structural transition owned by EPIC-07) | EPIC-07 merges first; all other EPICs create their own per-EPIC file after EPIC-07 lands |
| `shared_standards.md` | EPIC-07 (ST-19 — §12 Rule 2 retirement + reference update) and possibly EPIC-03 (ST-09 — if the §17 standing-authority-extension remediation path is chosen) | EPIC-07 merges first (sequence position 1); if ST-09's branch also touches `shared_standards.md`, it must rebase onto `main` after EPIC-07 merges before finalising its own edit |
| `OPERATIONAL_GUIDE.md` §14 | Any EPIC-03 item that bumps a governance prompt version (ST-04, ST-07, ST-09 candidates) and EPIC-07 (bumps `execution_prompt.md`, `delivery_verification_prompt.md`, `post_ship_closure.md`) | EPIC-07 merges first; EPIC-03 branches rebase onto `main` after EPIC-07 lands before finalising their own §14 row updates |
| `prompt_change_log.md` | Same set as above (append-only — low conflict risk, but rebase still required to avoid stale insertion point) | Same rebase-after-EPIC-07 rule applies |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — Design Gate already PASSED (Design Pre-Approved, `design_gate.md`); Playwright coverage (extending `TradeEntry.js`'s existing pattern) or recorded staging sign-off remains an execution-phase evidence obligation per CLAUDE.md §2 |
| RISK-02 | EPIC-07 (ST-19) | Valid — mitigation requires Head of Engineering sign-off before the new mechanism is used live; sequencing this EPIC first (see Execution Sequence) directly operationalises the mitigation's intent that this sprint be a clean first live use; legacy `shared_standards.md` §12 mechanism remains the documented fallback |
| RISK-03 | Release-level (product-value scarcity) | Advisory only — not actionable at Sprint Planning; belongs to the next `run roadmap` rebalance per `release_plan.md`'s own recommendation. No sprint-scope action taken here. |
| RISK-04 | Release-level (~92-107% utilisation) | Valid — STEP 1 capacity recheck (`sprint_capacity.md`) confirms no over-allocation against the ~24-28 day ceiling; EPIC-03 (7 divisible items) remains the natural trim candidate if early velocity signals overrun |

**Multi-vehicle fix-choice risk check (LP-14):** ST-09 (EPIC-03) names two alternative remediation paths at execution kickoff — (a) a narrow `shared_standards.md` §17 standing-authority extension, or (b) a `roadmap_prompt.md` STEP 8.1 condition-1 amendment. Checked for material effort divergence: both paths fall within the same S (~1.0 day) effort band recorded in `sprint_capacity.md` — no material sizing difference. No `### Phasing Recommendation` exists this cycle (capacity outcome was `pass`, not `warn`), so no boundary cross-reference is needed. The choice is left to resolve at execution kickoff per the item's own acceptance criteria; recorded here per LP-14 to surface the risk at planning time rather than defer the sizing question invisibly.

## Pre-Sprint Vulnerability Scan

`pip-audit` is not installed in this environment (`pip-audit: command not found`). Scan could not run. Advisory only — does not block sprint planning. Recommend installing `pip-audit` before sprint execution begins so STEP -1's vulnerability scan can produce a real result at the next invocation.

## Carry-Forward Items

Carry-forward items reviewed: 2 items from cycle `2026-07-30__release-v8.0` (`lessons_learnt_closure.md`):
1. `BLG-OPS-111` endpoint-list drift (3rd consecutive cycle) — tagged Engine: Post-Ship Closure, not directly actionable at Sprint Planning; noted for awareness.
2. `execution_prompt.md`/`delivery_verification_prompt.md` sign-off-string disagreement for delegated-heavy EPICs (`ESC-CLOSE-20260731-01`) — tagged Engine: Sprint Planning. This sprint has 2 delegated-heavy EPICs by story mix (EPIC-04, EPIC-05) — awareness only, no scope action needed; friction may recur at EPIC-level sign-off consolidation for these two EPICs at sprint close.

## Pre-Sprint Backlog Advisory

No backlog items found with `Provisional-Target: Before v8.1 sprint planning` (checked via direct grep — zero matches).

## Hygiene Advisory

⚠ Prompt change log gap: `sprint_planning_prompt.md` current v3.13 — last logged transition in `prompt_change_log.md` is v3.11→v3.12 (2026-07-02). The v3.13 bump itself was never logged. Advisory only per CLAUDE.md §6 / `shared_standards.md` §11 — does not block this sprint planning run; flagged here as an outstanding action for the Head of Specs Team.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Install `pip-audit` in the execution environment so future pre-sprint scans can run | Infrastructure & Operations Owner | No |
| Log the `sprint_planning_prompt.md` v3.12→v3.13 transition in `prompt_change_log.md` (retroactive) | Head of Specs Team | No |
| Schedule a Product Owner + Strategy Rules & System Intent Owner decision session for ST-14/ST-16 threshold definitions before those items execute | Product Owner | No |
| Resolve ST-09's two-vehicle remediation choice at execution kickoff | Head of Specs Team | No |
