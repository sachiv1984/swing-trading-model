Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Complete
Last Updated: 2026-08-17
Cycle: 2026-08-14__release-v8.8

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v8.8 — Live Data-Integrity, Backend Hardening & Debt Closure
Run: 2026-08-14__release-v8.8
Reviewed by: PMO Lead
Date filed: 2026-08-17
Prior cycle checked: 2026-08-12__release-v8.7 (`lessons_learnt_closure.md`) — Carry-Forward: 0 items; no open action items from that closure carried into this run beyond what `lessons_learnt_cycle.md`'s own Phase 4 "Prior cycle checked" note already tracks (2 deferred Phase 4 patches, re-deferred below, not yet at the §6.4 escalation threshold).

---

## What worked well

- All 29 in-scope stories reached `done`/`merged` with zero deviations filed and zero QA `Fail` results — the cleanest delivery-verification pass on record for this project (per Phase 4's own Carry-Forward note). Closure reconciliation confirmed this cleanly: no returned items, no P2/P3 deviation items, no test scenario gap items needed adding at STEP 3.2.
- The `execution_state.json`→`backlog.md` reconciliation (STEP 3) traced all 29 `ST-xx` items to their `BLG-xx` source entries via the ephemeral Release Slice table with zero ambiguity — every mapping resolved on the first lookup.
- Document closure was low-friction across the board this cycle: roadmap, scope, and decisions documents were all exactly where `release_plan.md`/`.claude_current_state.json` said they'd be; the Specs Index §6/§7/TSG register had zero open items to reconcile; the endpoint-coverage-drift check (`scripts/check_api_performance_baseline_drift.py`) ran clean with no new gap.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** Not checkable (no prior file) — first time this specific gap was observed at closure; not previously tracked as a recurring pattern.

**What happened:** Three of the 29 shipped backlog items (`BLG-SEC-18`, `BLG-SEC-28`, `BLG-SPEC-118`) were missing the standard `**Effort:**`/`**Provisional-Target:**` fields entirely at STEP 3 (mark-shipped-complete) time, unlike the other 26 items which all carried a `**Provisional-Target:**` field (either `vX.Y` or a descriptive placeholder) ready to be overwritten with the completion marker. All three originated as "discovered mid-sprint, out-of-scope finding" items filed directly during a prior sprint's execution rather than through the standard backlog-add flow.

**Where in the routine:** STEP 3.1 — Mark shipped items complete.

**Root cause:** template omission (item filed without the full field set at authoring time).

**Blast radius analysis:**
- What would have propagated: had this gone unnoticed, these 3 items would have had no completion marker at all, making them appear open/unshipped to the next scheduled rebalance and to `groom backlog`'s own health check.
- When it would have surfaced: next `run roadmap --reason scheduled` or `groom backlog` pass, as a false "still open" read on 3 already-shipped items.
- Recovery cost if uncaught: low (single-file fix — a `**Provisional-Target:**` line inserted after `**Source:**` for each, applied this run).

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/backlog_management_prompt.md` (or the `backlog-add` skill definition, wherever out-of-scope mid-sprint findings are filed)
  - Section: item-authoring template / field-completeness check
  - Change required: require `**Effort:**` and `**Provisional-Target:**` as mandatory fields at filing time for backlog items filed as mid-sprint out-of-scope discoveries, not only for items filed through the standard `run ideas`/rebalance flow — or add a `groom backlog` health check that flags any `### BLG-xx` entry missing either field.
  - Owner: Head of Specs Team
  - Target: next `backlog_management_prompt.md` revision

---

## Consolidated Action Summary (STEP 8 — all records reviewed)

Records reviewed: `lessons_learnt.md` (Release Planning), `lessons_learnt_cycle.md` §Phase 3 + §Phase 4 (Sprint Execution + Delivery Verification).

**Immediate actions applied:** 1
- `CLAUDE.md` §8 step 2a extended to require checking every co-bumped file individually for version collisions, not treating one caught collision as clearing the commit's other co-bumped files (Phase 3 friction item 2). Applied during Sprint Execution STEP 5.4, not this closure run — `prompt_change_log.md` rows dated 2026-08-17 confirm the patch, plus the paired `post_ship_closure.md` v2.27→v2.28 / `OPERATIONAL_GUIDE.md` v4.162→v4.163 collision renumbering it was found alongside. Disposition confirmed immediate/complete; no further action needed at closure.

**Deferred to next cycle:** 6
1. `merge_gate`/per-EPIC `pr_status` mid-session staleness between individual human-driven PR merges (Phase 3 friction item 1, 4th consecutive cycle of the general staleness pattern, new mechanism this cycle) — Owner: Head of Specs Team — Target: next `execution_prompt.md` revision (either a `governance_sync.yml` on-merge trigger, or an explicit STEP 8 re-check instruction).
2. `execution_state.json`'s `test_scenarios` field-shape inconsistency between an empty-array and a populated-prose-string convention for governance-only EPICs (Phase 4 friction item) — Owner: Head of Specs Team — Target: next `execution_prompt.md` revision touching `test_scenarios` population.
3. *(carried from v8.7, cycle 2 of tracking)* `qa_evidence_template.md`/`execution_prompt.md §5.3` CI-green restatement requirement clarified as per-fix, not per-EPIC — Owner: Head of Specs Team — Target: next revision touching either file. Not yet at the §6.4 2-cycle-without-application escalation threshold (this is the 1st cycle transition since filing).
4. *(carried from v8.7, cycle 2 of tracking)* Canonical "Sandbox Access Constraint" disclosure block for `shared_standards.md` — Owner: Head of Specs Team — Target: next `shared_standards.md` revision. Same threshold status as #3.
5. Release Planning: make "surface the widen-vs-tight sizing decision explicitly to the Product Owner" the default behaviour when `plan release` runs without an explicit capacity directive and the `Provisional-Target`-tagged pool alone leaves significant headroom (Release Planning observation) — Owner: Head of Specs Team — Target: next `release_planning_prompt.md` revision.
6. Backlog item field-completeness gap for mid-sprint out-of-scope filings (this closure's own Friction Item 1) — Owner: Head of Specs Team — Target: next `backlog_management_prompt.md` revision.

**Escalated for decision:** 0 — no item required a named-authority decision this cycle.

**Roadmap/backlog observation (not a process patch, informational):** the ungated P1/P2 backlog pool is nearly exhausted (7 items existed at `plan release v8.8` scoping time; 6 were pulled into this cycle's scope) — flagged in `lessons_learnt.md` for the next scheduled rebalance as a scoping-input signal. No engine action required this closure; recorded here for continuity.

---

## Process improvements actioned this run

None applied directly by this closure run (the one immediate action identified above was already applied during Sprint Execution, prior to this closure invocation).

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| N/A | N/A | N/A | N/A | N/A |

---

## New files created this run

- `claude/cycles/2026-08-14__release-v8.8/closure_state.json`
- `claude/cycles/2026-08-14__release-v8.8/lessons_learnt_closure.md` (this file)
- `claude/cycles/2026-08-14__release-v8.8/closure_record.md` (produced next, STEP 9)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | STEP 8 / merge-gate sync | Structural fix for mid-session `merge_gate`/`pr_status` staleness between individual PR merges | Head of Specs Team | Next `execution_prompt.md` revision |
| `claude/system/execution_prompt.md` | `test_scenarios` field population (STEP 3/5) | Require empty array `[]` for "no automated scenarios"; move manual-review rationale to `qa_evidence_EPIC-xx.md` prose | Head of Specs Team | Next `execution_prompt.md` revision touching `test_scenarios` |
| `claude/system/templates/qa_evidence_template.md` / `execution_prompt.md §5.3` | Standard Sign-Off Block | Clarify CI-green restatement requirement is per-fix, not per-EPIC (carried from v8.7, cycle 2 of tracking) | Head of Specs Team | Next revision touching either file |
| `claude/system/shared_standards.md` | New section required | Canonical "Sandbox Access Constraint" disclosure block (carried from v8.7, cycle 2 of tracking) | Head of Specs Team | Next `shared_standards.md` revision |
| `claude/system/release_planning_prompt.md` | Sizing/capacity decision step | Default to explicitly surfacing the widen-vs-tight scope decision to the Product Owner when no capacity directive is given and `Provisional-Target` pool alone leaves headroom | Head of Specs Team | Next `release_planning_prompt.md` revision |
| `claude/system/backlog_management_prompt.md` | Item-authoring template / health check | Require `Effort`/`Provisional-Target` fields for mid-sprint out-of-scope backlog filings, or add a `groom backlog` completeness check | Head of Specs Team | Next `backlog_management_prompt.md` revision |

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The ungated P1/P2 backlog pool was nearly exhausted at `v8.8` scoping time (7 items total, 6 pulled into scope) — the next release's P1/P2 scope will draw almost entirely from newly-filed items or gate-clearance events rather than an existing ready pool. | Treat as a scoping-input signal at the next scheduled rebalance; do not assume a ready P1/P2 pool exists without checking. | Roadmap |
| 2 | Two Phase 4 deferred patches (CI-green per-fix restatement clarification; canonical Sandbox Access Constraint block) have now carried across one full cycle transition (v8.7 → v8.8) without a `prompt_change_log.md` entry. | If either remains unapplied after the *next* cycle transition (v8.8 → v8.9), the §6.4 2-cycle-without-application threshold is crossed and both must be escalated to Head of Specs Team rather than re-deferred a 3rd time. | All |
