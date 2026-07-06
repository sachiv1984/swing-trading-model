Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-04__release-v6.6
Release: v6.6
Last Updated: 2026-07-06
Authority: Post-Ship Closure Engine v2.17

---

# Lessons Learnt — Closure Summary: v6.6

Reviewed by: PMO Lead
Date filed: 2026-07-06
Prior cycle checked: claude/cycles/2026-07-02__release-v6.5/lessons_learnt_closure.md

## Classification Summary

| Count | Category |
|-------|----------|
| 2 | Immediate (prompt patches applied in this post-ship session) |
| 1 | Immediate (analysis/finding resolved this session, no prompt change) |
| 1 | Deferred (carry to v6.7 as Outstanding Action) |
| 1 | Escalated (decision required — recurrence threshold crossed) |

---

## Action Classification Detail

### Immediate Actions Applied (2 prompt patches + 1 analysis)

| ID | Source | Document | Change | Version |
|----|--------|----------|--------|---------|
| IM-01 | Release Planning lessons_learnt.md LP-01 (carries v6.5 DF-16, 2-cycle recurrence) | `claude/system/release_planning_prompt.md` | STEP 4.1 no longer writes `design_gate_required`/`design_gate_status` directly to `.claude_current_state.json` (state.json only); STEP 7's intermediate sync now carries both fields into `.claude_current_state.json` atomically with `active_cycle`. Resolves the 2-cycle-recurring transient-state contradiction (v6.5 Friction Item 1, v6.6 recurrence). | v2.40→v2.41 |
| IM-02 | Release Planning lessons_learnt.md LP-05 (Friction Item 2, first identified this cycle) | `claude/system/roadmap_prompt.md` | §7.1 Skill-Silo Alert — pull-forward candidate selection now requires reading the candidate's own `**Gate criteria:**` backlog line and confirming it is met/near-term before naming it; unmet-gate candidates must be flagged `[gate status unverified/unmet]` rather than named silently. Fixes the gap that let `2026-07-03__scheduled` name BLG-FEAT-52 despite its own unmet PO-02 gate. | v8.1→v8.2 |
| IM-03 | Release Planning lessons_learnt.md LP-06 / carries v6.5 DF-17 (LP-04) | Analysis only — no file changed | Confirmed v6.6's ship-time classification: of the 2 "nominal U-items" named at planning (BLG-FE-82, BLG-FE-40), only **1** genuinely classifies as `U` at ship (BLG-FE-40 — a real shipped feature). BLG-FE-82/ST-01 classifies `D` (findings-only audit, no in-story fix, Design Not Applicable) — see `docs/product/changelog.md#v6.6` inline tags. This is the **2nd consecutive cycle** (v6.5, v6.6) where a nominally-2-U-item release resolved to only 1 genuine U-item at ship. See Friction Item 3 below and Carry-Forward #2. | N/A |

LP-07 (also from `lessons_learnt.md`, the `/commit-check` diff-verification patch) was reviewed and classified `decision_required` / escalated — see Escalations below. It is outside this routine's write scope (`.claude/skills/` is not a permitted path per `post_ship_closure.md` §5), and has now crossed the `lessons_learnt_prompt.md` §3.7 2-cycle-carry-forward automatic-escalation threshold (v6.4→v6.5→v6.6, no `prompt_change_log.md` entry).

---

## Friction Log (this closure run)

### Friction Item 1 — LP-01 confirmed resolved (2-cycle recurrence closed)

**Classification:** Type C — Dependency Stall (a sequencing dependency between two steps was invisible in the prompt text; recurrence of v6.5 Friction Item 1)
**Recurrence:** Yes — appeared in `2026-07-02__release-v6.5` (Friction Item 1, DF-16) and `2026-07-04__release-v6.6` (Release Planning `lessons_learnt.md` Friction Item 1, 2nd consecutive occurrence).

**What happened:** Identical to v6.5's instance — STEP 4.1 wrote `design_gate_status: not_started` to `.claude_current_state.json` while `active_cycle` still pointed at the just-closed prior cycle, transiently overwriting that cycle's own completed design-gate record before STEP 7's intermediate sync advanced `active_cycle`. v6.5's closure deferred this (DF-16) because two alternative fixes were proposed with no design decision made between them. This session resolved that ambiguity by selecting the lower-risk option (defer the `.claude_current_state.json` write entirely to STEP 7, rather than attempt an atomic combined write across two non-adjacent steps).

**Where in the routine:** `release_planning_prompt.md` STEP 4.1 (Design Gate Classification) / STEP 7 (Cycle Summary, intermediate sync).

**Root cause:** process gap — two steps wrote to the same global state file at different points in the same session with no ordering guarantee between them.

**Blast radius analysis:**
- What would have propagated: a 3rd consecutive cycle of the identical transient contradiction, and (per `lessons_learnt_prompt.md` §3.7) an automatic recurrence escalation to Head of Specs Team had it not been resolved this session.
- When it would have surfaced: next release planning cycle's STEP 4.1/STEP 7 window.
- Recovery cost if uncaught: low (transient, self-correcting within the same session) but compounding — a 3rd occurrence would have triggered a harder escalation.

**Process patch:**
→ Immediate patch applied this run:
  - File: `claude/system/release_planning_prompt.md`
  - Section: STEP 4.1 — Design Gate Classification; STEP 7 — Cycle Summary (intermediate sync)
  - Change: STEP 4.1 writes `attributes.design_gate_required` to `state.json` only; STEP 7's intermediate sync now carries `design_gate_required`/`design_gate_status` into `.claude_current_state.json` atomically with `active_cycle`.
  - Version: 2.40→2.41
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

### Friction Item 2 — LP-05: roadmap pull-forward candidate naming did not verify the candidate's own gate status

**Classification:** Type C — Dependency Stall (a gate condition on the candidate item itself was not checked before the candidate was surfaced to the PO)
**Recurrence:** No — first identified this cycle (Release Planning `lessons_learnt.md` Friction Item 2).

**What happened:** The `2026-07-03__scheduled` rebalance named BLG-FE-82 and BLG-FEAT-52 as Skill-Silo pull-forward candidates. BLG-FE-82 was ungated and valid; BLG-FEAT-52 carried its own unmet gate (Arc 4 PO-02 sprint planning imminent, itself blocked on a data-density gate with no confirmed near-term clearance) — discoverable directly from the item's own backlog entry. Release planning caught this via manual cross-check before v6.6 scope was sealed; had it not, BLG-FEAT-52 would likely have entered scope and returned to backlog at sprint close.

**Where in the routine:** `roadmap_prompt.md` §7.1 — Skill-Silo Alert, pull-forward candidate selection.

**Root cause:** process gap — the candidate-selection step named "no blockers" as a descriptive criterion but had no explicit verification instruction requiring the engine to actually check the candidate's own `Gate criteria:` line before naming it.

**Blast radius analysis:**
- What would have propagated: a gated item entering firm sprint scope, only to return to backlog at sprint close (the exact within-sprint-gate failure pattern §1.4b already guards against for calendar gates, here recurring for a state-based gate).
- When it would have surfaced: sprint close, if release planning's manual cross-check had not caught it first.
- Recovery cost if uncaught: medium (a full sprint slot wasted on a story that cannot proceed).

**Process patch:**
→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: §7.1 — Skill-Silo Alert
  - Change: Added explicit candidate gate verification — read the candidate's own `**Gate criteria:**` backlog line before naming it; unmet/unverifiable gates must be flagged, not silently named.
  - Version: 8.1→8.2
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

### Friction Item 3 — LP-06/DF-17: 2nd consecutive cycle where a nominal U-item did not classify as genuine U at ship

**Classification:** Type B — Semantic Mismatch (a story counted as "user-facing" at scoping time did not match its own ship-time outcome)
**Recurrence:** Yes — appeared in `2026-07-02__release-v6.5` (DF-17/LP-04: "only 1 of 2 nominal v6.5 U-items classified U") and recurred identically at v6.6.

**What happened:** v6.6 was scoped with 2 nominally user-facing items (BLG-FE-82 contrast audit, BLG-FE-40 RFJ persistence) specifically to correct the worsening Skill-Silo rolling average. At ship, BLG-FE-40 is genuinely `U` (a real shipped, user-visible feature). BLG-FE-82/ST-01, however, resolved to an audit-only, findings-only outcome (Design Not Applicable design-gate classification, no in-story fix) — correctly tagged `D` (debt clearance / audit) in `docs/product/changelog.md#v6.6`, not `U`. This is the identical pattern flagged at v6.5 closure (DF-17): a story classified as "nominal U" at planning time systematically under-delivers to U at ship when its own acceptance criteria are audit/investigation-shaped rather than build-and-ship-shaped.

**Where in the routine:** `release_planning_prompt.md` / scope decision time (item selection for Skill-Silo correction) — the mismatch is only visible at `post_ship_closure.md` STEP 1 (ship-time changelog tagging).

**Root cause:** naming inconsistency / severity classification error — an audit/investigation-class story's AC ("produce findings, file follow-ups") cannot structurally guarantee a `U` outcome the way a build-and-ship story's AC can, but nothing in scope selection distinguishes the two story shapes when counting "nominal U-items" for Skill-Silo correction purposes.

**Blast radius analysis:**
- What would have propagated: continued reliance on "nominal U-item count" as a planning-time proxy for genuine Skill-Silo correction, when the ratio has now been 1-of-2 for two consecutive cycles — the correction is running at half its intended strength without anyone re-deriving why.
- When it would have surfaced: the next roadmap rebalance's STEP 2.4 Product Value Ratio Diagnostic (now reads the ship-time tag directly per v8.1, so it will see this accurately) — but the *scoping* practice that keeps producing this gap would not self-correct without a specific recommendation.
- Recovery cost if uncaught: medium — the Skill-Silo Alert could remain unresolved for a 3rd+ cycle if scoping keeps counting audit/investigation stories as reliable U-items.

**Process patch:**
→ Deferred patch (cannot apply this run — requires a scoping-heuristic design decision, not a mechanical fix):
  - File: `claude/system/roadmap_prompt.md` (§7.1 Skill-Silo Alert candidate selection) and/or `claude/system/release_planning_prompt.md` (scope decision stage)
  - Section: Skill-Silo pull-forward candidate selection / scope decision recording
  - Change required: When selecting or confirming a Skill-Silo correction candidate, distinguish build-and-ship story shapes (AC requires a shipped user-visible change) from audit/investigation story shapes (AC requires findings/decision only) — only count the former as reliable `U` toward the correction target; the latter should be flagged as `D`-leaning at scoping time, not assumed `U`.
  - Owner: Head of Specs Team
  - Target: Next `roadmap_prompt.md` / `release_planning_prompt.md` revision (v6.7 rebalance or later)

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| `/commit-check` skill should diff `git add`'s staged target list against the intended file set before multi-file governance commits — deferred v6.4 (target v6.5), still deferred v6.5 (target v6.6), still unapplied at v6.6 (no `prompt_change_log.md` entry across the full carry) | 2026-06-24__release-v6.4 | Deferred, owner Head of Specs Team, target `2026-07-02__release-v6.6` (this cycle) — per v6.5 DF-18 | Head of Specs Team |

This item crosses the `lessons_learnt_prompt.md` §3.7 2-cycle-carry-forward automatic-escalation threshold this cycle. Recorded as `ESC-CLOSE-20260706-01` in `claude/cycles/2026-07-04__release-v6.6/closure_escalations.md` (24-hour SLA, Lifecycle trigger).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/release_planning_prompt.md` | STEP 4.1 / STEP 7 | Deferred `.claude_current_state.json` design-gate write from STEP 4.1 to STEP 7's intermediate sync (atomic with `active_cycle`) | v2.40→v2.41 | Yes |
| `claude/system/roadmap_prompt.md` | §7.1 Skill-Silo Alert | Added candidate gate-status verification before naming a pull-forward candidate | v8.1→v8.2 | Yes |

---

## New files created this run

None.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` and/or `claude/system/release_planning_prompt.md` | Skill-Silo pull-forward candidate selection / scope decision recording | Distinguish build-and-ship story shapes from audit/investigation story shapes when counting "nominal U-items" for Skill-Silo correction — only the former should count as reliable U at scoping time | Head of Specs Team | Next `roadmap_prompt.md` / `release_planning_prompt.md` revision (v6.7 rebalance or later) |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `/commit-check` skill diff-verification patch deferred across 3 cycles (v6.4→v6.5→v6.6) with no `prompt_change_log.md` entry; `.claude/skills/` remains outside every governed routine's declared write scope | Recurrence | Head of Specs Team | Crosses `lessons_learnt_prompt.md` §3.7 automatic-escalation threshold this cycle. See `ESC-CLOSE-20260706-01`, `closure_escalations.md` — 24-hour SLA. |

---

## Closure-Phase Observations

- **DF-16 (LP-01) closed cleanly on its own carried-forward target** — v6.5 deferred it specifically because two alternative fixes existed with no design decision between them; this closure session picked the lower-risk option (defer the `.claude_current_state.json` write to STEP 7 rather than force an atomic write across two non-adjacent steps) and applied it, closing a 2-cycle recurrence.
- **DF-17 (LP-04/LP-06) confirms a real, now-2-cycle pattern rather than a one-off:** bundling 2 nominal U-items into a release does not reliably produce 2 genuine U-items at ship if one of them is audit/investigation-shaped. This is now specific enough to act on — recorded as a deferred scoping-heuristic patch rather than left as an open monitoring question for a 3rd cycle.
- **DF-18 (`/commit-check`) has now crossed the automatic-escalation threshold exactly as v6.5's closure predicted** ("a 2nd consecutive miss at v6.6 would trigger the recurrence-escalation rule") — escalated this run per `lessons_learnt_prompt.md` §3.7, rather than deferred a 4th time.
- **Endpoint coverage drift check (STEP 6) found no gap this cycle** — confirmed via direct `git diff --stat` against all 4 merged commits: zero changes under `backend/routers/` this cycle. Consistent with v6.6's UX/QA-debt scope (no new endpoints).
- **Specs Index TSG reconciliation (§7.3) found nothing to reconcile** — no pre-v6.6 open TSG items existed at cycle start (all resolved as of §33/v6.5); §34 added cleanly for v6.6 (0 gaps).

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `/commit-check` diff-verification patch is now an open escalation (`ESC-CLOSE-20260706-01`) with no routine holding write scope for `.claude/skills/`. | Head of Specs Team must apply the patch directly or formally amend a routine's write scope before the next cycle's Phase 3 friction review — do not let a 4th cycle pass without a `prompt_change_log.md` entry. | All |
| 2 | 2nd consecutive cycle (v6.5, v6.6) where an audit/investigation-shaped story counted as "nominal U" at scoping resolved to `D` at ship, leaving only 1 of 2 planned U-items genuinely user-facing. | When selecting Skill-Silo correction candidates, treat audit/investigation-shaped stories as `D`-leaning, not `U`, until a scoping-heuristic fix is applied (see Outstanding Deferred Patches). | Roadmap |
