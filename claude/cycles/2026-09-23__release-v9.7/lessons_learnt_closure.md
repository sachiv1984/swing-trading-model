Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-28

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Clear the full v9.7 scope — 29 backlog-slice items (31 `execution_state.json` story entries, ST-01 phased into ST-01a/b/c) across 7 EPICs, PO-05 Lightweight Replay Mode shipped as the cycle's flagship feature alongside category-balanced debt clearance.
Run: 2026-09-23__release-v9.7
Reviewed by: PMO Lead
Date filed: 2026-09-28
Prior cycle checked: 2026-09-21__release-v9.6 (`lessons_learnt_closure.md`)

---

## What worked well

- All 29 shipped backlog-slice items (31 story entries) traced cleanly to their `BLG-*` source items in one pass (STEP 3) via each `stage4_backlog_slice.md` entry's own `**Source:**` field — mechanical and error-free across all 7 EPICs, including the ST-01a/b/c phasing.
- The STEP 6 Endpoint Coverage Drift Check found a genuine 0-gap result (147 normalised `openapi.yaml` endpoints; this cycle's sole new endpoint, `POST /replay/run`, was already registered in `api_performance_baseline.md` during sprint execution) — confirming the v2.33 Markdown-normalisation fix continues to hold.
- The cross-cycle `DEV-*` consolidation review (STEP 5.1, cadence-triggered, 6th run) found and fixed a genuine compliance gap in `ai_endpoints.md` (a stale "None at v1.10" Known Deviations summary sitting alongside an already-disclosed won't-fix deviation) — the recurring-pattern tracking this review exists for is doing real work, not just re-confirming a stable baseline each time.
- Release Planning lessons_learnt.md Friction Item 1 had concrete, unambiguous recommended wording already spelled out in its own originating record — applied now at this closure per the same-cycle application pattern (v2.32), closing a real recurrence (`BLG-FE-189` slipped through this cycle's own release-planning selection the same way a `v9.6`-flagged gap predicted it could).
- 3 delegation records this cycle (`DEL-20260924-01`, `DEL-20260924-02`, `DEL-20260924-03`) all reached terminal resolution within the sprint — 2 unblocked with real evidence (a live-Postgres test, a human-operator staging verification), 1 cleanly reclassified `autonomous` on explicit user direction rather than left dangling.

---

## Friction Log

**Closure-phase finding (STEP 6):** `src/pages/SystemStatus.js`'s `categorizeEndpoint()` has no case for the new `/replay` path prefix introduced by this cycle's `POST /replay/run` — falls into the catch-all `'Other'` dashboard category. Filed as `BLG-FE-191` (P4) rather than fixed directly (outside this routine's write scope — `src/pages/` is not a permitted closure write path). Type A — Governance Drift: the STEP 6 advisory check that exists specifically to catch this class of gap worked as designed.

**Closure-phase finding (STEP 5.1):** `docs/specs/api_contracts/ai_endpoints.md`'s `## Known Deviations` section read "None at v1.10." despite an already-disclosed, already-dispositioned won't-fix deviation (`BLG-BE-128`, documented only in the Changelog table and an inline note) — the third instance of the "deviation-shaped disclosure with no `DEV-<id>`, or in this case not even reflected in the section summary" pattern the 5th consolidation review first flagged. Fixed in this commit (added `DEV-v9.7-ST13-01`); the underlying process-discipline gap (file a `BLG-GOV-*` item requiring `DEV-<id>` assignment at filing time) remains unfiled after being recommended across 3 consecutive review runs — see Recurrence Escalations below is not triggered for this specific item only because the 6th review's own recommendation was to escalate filing at the *next* opportunity, not immediately; flagged here for visibility.

No other closure-phase friction — STEPs 1–7 (changelog, roadmap, backlog reconciliation, scope/decisions supersession, deviation compliance, operational docs, Specs Index) otherwise completed with no missing documents and no discrepancies between the authoritative backlog slice and `backlog.md`.

---

## Recurrence Escalations

Two mandatory recurrence escalations raised this closure (`lessons_learnt_prompt.md §3.7`), both filed as `ESC-CLOSE-20260928-01`/`-02` in `closure_escalations.md`, both SLA 2026-10-01:

1. **`execution_prompt.md §3.2.A` same-EPIC cross-story testing-gap disclosure consistency check** — deferred at `2026-09-15__release-v9.5` closure, carried unapplied through `2026-09-21__release-v9.6` closure (flagged there as "2nd cycle — watch"), confirmed still unapplied at this closure (`execution_prompt.md` remains v3.79, no matching `prompt_change_log.md` entry found by topic search). Crosses the 2-cycle automatic-escalation threshold. No concrete replacement wording exists yet — escalated for a Head of Specs Team ruling rather than implemented blind.
2. **`release_planning_prompt.md §-1.2` Option(b) rebalance-equivalence precedent-reuse** (Release Planning lessons_learnt.md Friction Item 3) — this is a related but distinct instance of the general staleness-of-precedent pattern already normal in this repo; escalated for a Head of Specs Team ruling on whether §-1.2 should require the cited record to postdate the immediately-prior cycle.

One further deferred-patch carry was checked and found **not** to have crossed the threshold: `execution_prompt.md` STEP 3.1/§3.1.D's `open_escalations`/`completed_items`/`blocked_items` sync fix, first deferred at this same `2026-09-23__release-v9.7` cycle's own Phase 3/Phase 4 lessons (not at `v9.6`) — this is its 1st carry only, watch at `v9.8`.

**Release Planning Friction Item 1 was a recurrence with a concrete fix and was resolved directly, not escalated** — see Process improvements actioned this run below.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `scripts/scan_backlog_gate_conditions.py` | New already-resolved-banner detection | Added a scan for `**Resolution (...):**`/`**Resolved (...):**` anywhere in an item's body, reported as a new "already-resolved — verify before seating" list independent of gated status. Resolves Release Planning lessons_learnt.md Friction Item 1 — `BLG-FE-189` slipped through this cycle's own selection despite a same-session resolution note, because the only prior sibling check (`v9.6` Friction Item 1) looked for a `✅ COMPLETE` banner only. | N/A — plain utility script, no version header | No — not a governance prompt itself |
| `claude/system/release_planning_prompt.md` | §1.3a Gate-Detection Procedure | Text updated to require the new already-resolved list be read and each item verified before the ready pool is fixed. | v2.55→v2.56 | Yes — see `prompt_change_log.md` 2026-09-28 entry |
| `claude/system/OPERATIONAL_GUIDE.md` | §6B source prompt header, §14 table, §14 self-row, Change Log | Synced to `release_planning_prompt.md` v2.56 per the CLAUDE.md §6 checklist. | v4.206→v4.207 | Yes — see `prompt_change_log.md` 2026-09-28 entry |
| `docs/specs/api_contracts/ai_endpoints.md` | `## Known Deviations` | Corrected stale "None at v1.10." summary to a proper `DEV-v9.7-ST13-01` entry for the already-disclosed `BLG-BE-128` won't-fix (STEP 5.1 finding). | v1.14 (no bump — non-normative deviation-note compliance fix, per the established retroactive-DEV-ID-assignment precedent) | No — not a version-numbered governance change |

---

## New files created this run

- `claude/cycles/2026-09-23__release-v9.7/closure_state.json`
- `claude/cycles/2026-09-23__release-v9.7/closure_escalations.md` — 2 decision-required/recurrence escalations raised (see Escalations below)
- `docs/governance/deviation_consolidation_review_2026-09-28.md` — 6th cadence-triggered cross-cycle `DEV-*` consolidation review
- `claude/cycles/2026-09-23__release-v9.7/closure_record.md`
- `claude/cycles/2026-09-23__release-v9.7/lessons_learnt_closure.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Cycles carried |
|------|---------|----------------|-------|--------|-----------------|
| `claude/roadmap/workforce_capacity.md` | Canonical Effort Band → Days Conversion Table | Add a `VH` row once a second real `VH`-effort item is scored (Release Planning Friction Item 2 — `BLG-FEAT-74` was the first, an ad hoc 12.0d Product Owner estimate was used). Not actionable yet — needs a second data point. | Head of Specs Team | Once a 2nd `VH` item is scored | 1st cycle (new this closure) |
| `claude/system/execution_prompt.md` | STEP 3.1 / §3.1.D | Broaden the "resolve a delegated item" write to also sync, in the same commit: `.claude_current_state.json.open_escalations` disposition, `execution_state.json`'s own top-level `open_escalations` array, and the top-level `completed_items`/`blocked_items` arrays. Recurred this cycle in the same shape (EPIC-04/ST-18 stale `blocked_items` entry, corrected only at a later resume-sync). | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 3.1/3.1.D | 1st carry (first raised at this cycle's own Phase 3/4 lessons, not at `v9.6`) — **watch:** a second unresolved carry at `v9.8` crosses the `§3.7` two-cycle threshold. |
| `claude/system/execution_prompt.md` | §3.2.A | QA evidence sign-off protocol — mandate the fully-qualified agent-mediated label format whenever the actual reviewer is an agent rather than the literal human role-holder (closes the gap that let `EPIC-04`/`EPIC-07`'s `qa_evidence` files this cycle use the bare literal `"Director of Quality"` signer while their own Comments disclosed agent-mediation). | Head of Specs Team | Next `execution_prompt.md` revision touching §3.2.A / QA evidence sign-off protocol | 1st cycle (new this closure) |
| `claude/system/execution_prompt.md` | §3.2.A | Same-EPIC cross-story consistency check for "testing-gap disclosure" as its own category — carried from `2026-09-15__release-v9.5`'s own Outstanding deferred patches table, through `2026-09-21__release-v9.6`. No `prompt_change_log.md` entry found for it this cycle either. **Escalated** — see `ESC-CLOSE-20260928-01`. | Head of Specs Team | Ruling due 2026-10-01 | 3rd cycle — past the `§3.7` two-cycle automatic-escalation threshold. |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `execution_prompt.md §3.2.A` same-EPIC cross-story testing-gap disclosure consistency check — 3rd consecutive cycle carried unapplied, no concrete wording ever locked down. | Recurrence escalation (`§3.7` mandatory) | Head of Specs Team | Ruling needed: lock concrete §3.2.A wording and apply, or explicitly retire this deferred patch. Tracking: `ESC-CLOSE-20260928-01`, SLA 2026-10-01. |
| `release_planning_prompt.md §-1.2`'s Option(b) rebalance-equivalence rationale cited a 2nd time beyond the release it was written to justify. | Governance-prompt scope ambiguity | Head of Specs Team | Ruling needed on whether §-1.2 should require the cited record to postdate the immediately-prior release-planning cycle, or whether unlimited reuse until the next rebalance is by design. Tracking: `ESC-CLOSE-20260928-02`, SLA 2026-10-01. |

---

## Carry-Forward
Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Two open decision-required/recurrence escalations (`ESC-CLOSE-20260928-01`, `ESC-CLOSE-20260928-02`) remain unresolved at this closure, both 72h-SLA items due 2026-10-01. | If either breaches SLA before the next routine invocation reads `.claude_current_state.json.open_escalations`, the `BLOCKED_SLA_BREACH` rule (`shared_standards.md` IMP-40) applies on the next invocation. | Post-Ship Closure / any next-invoked routine |
| 2 | The `execution_prompt.md` STEP 3.1/§3.1.D `open_escalations`/`completed_items`/`blocked_items` sync gap is now at its 1st carry (raised this cycle, not yet fixed). | Watch at `v9.8` post-ship closure — a second unresolved carry crosses the `§3.7` two-cycle automatic-escalation threshold. | Post-Ship Closure |
| 3 | The `DEV-<id>`-assignment-at-filing-time process gap (6th consolidation review Finding 1) has now recurred 3 times (`v9.1`/`v9.3` originals, `v9.6`'s `BLG-BE-127`/`128`, this cycle's own `ai_endpoints.md` finding) with the same "file a `BLG-GOV-*` item" recommendation unfiled across the 5th and 6th review runs. | Escalate filing this item directly at the next `groom backlog` or Post-Ship Closure pass rather than deferring a 4th time. | `groom backlog` / Post-Ship Closure |
