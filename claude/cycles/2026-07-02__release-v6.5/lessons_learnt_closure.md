Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-02__release-v6.5
Release: v6.5
Last Updated: 2026-07-03
Authority: Post-Ship Closure Engine v2.16

---

# Lessons Learnt — Closure Summary: v6.5

Reviewed by: PMO Lead
Date filed: 2026-07-03
Prior cycle checked: claude/cycles/2026-07-02__release-v6.4/lessons_learnt_closure.md

## Classification Summary

| Count | Category |
|-------|----------|
| 3 | Immediate (applied in this post-ship session) |
| 3 | Deferred (carry to v6.6 as Outstanding Actions) |
| 0 | Escalated (decision required) |
| 1 | Confirmed already satisfied at its own target — no action required |
| 1 | Resolved as a side effect of this run's STEP 12 archiving (DF-19) |

---

## Action Classification Detail

### Immediate Actions Applied (3)

| ID | Source | Document | Change | Version |
|----|--------|----------|--------|---------|
| IM-01 | Release Planning lessons_learnt.md LP-02 (Friction Item 2) | `claude/system/release_planning_prompt.md` | STEP 5 Roadmap Annotation — added explicit fallback wording: if no formal `## vX.Y` roadmap section exists for the release, annotate the `**Next planned release:**` line in §1 instead | v2.39→v2.40 |
| IM-02 | Release Planning lessons_learnt.md LP-03 (Friction Item 3) | `claude/system/release_planning_prompt.md` | §1.4a Perennial-Return Check — added third named disposition option "(c) Resolve directly this cycle" for low-effort items where the cheapest fix is closure rather than further deferral or parking | v2.39→v2.40 (same commit as IM-01) |
| IM-03 | Self-identified this closure run (Friction Log below) | `claude/system/post_ship_closure.md` | STEP 2 — added clarifying note that the `*RA:<release> retired...*` annotation line is written by STEP 11 (`roadmap_management_prompt.md`), not STEP 2; prevents a premature write recording an archival that has not yet happened | v2.15→v2.16 |

LP-01 and LP-04 (also from `lessons_learnt.md`) were reviewed and classified `deferred` — see below; both specify either an ambiguous fix (LP-01, two named alternatives) or depend on next cycle's context (LP-04, a monitoring check), so neither qualifies for the non-deferrable immediate-action rule.

---

### Confirmed Already Satisfied At Its Own Target — No Action Required (1)

| ID | Source | Finding |
|----|--------|---------|
| DF-11 (v6.4) | v6.4 Phase 3 friction 1 — STEP 4 resume-sync branch check | Applied **at its own named target cycle**, during this cycle's own sprint execution (`execution_prompt.md` v3.50→v3.51, STEP 5.4, 2026-07-03) — not deferred a further cycle. Confirmed via `prompt_change_log.md` 2026-07-03 entry and `lessons_learnt_cycle.md` Phase 3 Recurrence Notes ("Recurred as predicted, and resolved this cycle"). |

### Resolved As A Side Effect Of This Run's Archiving (1)

| ID | Source | Finding |
|----|--------|---------|
| DF-19 | v6.5 Phase 4 friction — `backlog.md` entry header swap | `backlog.md` entry headers for `BLG-GOV-157` and `BLG-GOV-159` were swapped relative to their actual titles (confirmed at Sprint Planning, Sprint Execution, Delivery Verification). Both items shipped this cycle and were fully archived at STEP 12 (`groom backlog`, below) — their `backlog_archive.md` entries were written fresh with each item's correct title, cross-checked against `execution_state.json`/`stage4_backlog_slice.md` (BLG-GOV-157 = ST-01/"Lifecycle/prompt/state wording and consistency fixes"; BLG-GOV-159 = ST-03/"OPERATIONAL_GUIDE/prompt version-sync drift"). The permanent record is now correct; the mis-titled active-`backlog.md` entries no longer exist (removed on archiving, not edited in place). No further action needed — this resolves as a byproduct of the normal shipped-item archiving flow rather than requiring a dedicated content-correction write. |

---

### Deferred Items — carry to v6.6

| ID | Source | Summary | Owner | Target |
|----|--------|---------|-------|--------|
| DF-16 | Release Planning lessons_learnt.md LP-01 | STEP 4.1's `.claude_current_state.json` write and STEP 7's intermediate active_cycle sync are not atomic, creating a transient state contradiction (old `active_cycle`, new cycle's `design_gate_status`) for several steps. Two alternative fixes proposed (make the writes atomic, or defer the STEP 4.1 write to STEP 7 entirely) — ambiguous which to apply without a design decision, so not actioned as an immediate patch this run. | Head of Specs Team | Next `release_planning_prompt.md` revision |
| DF-17 | Release Planning lessons_learnt.md LP-04 / carries v6.4 DF-13 | Skill-Silo rolling-3-cycle average was 64.8% (Alert, worse than prior 53.2%) at the rebalance that shaped v6.5's scope; v6.5 responded by including 2 U-items (BLG-FE-46, BLG-FEAT-41) rather than the single pull-forward tried at v6.4. Confirm at the next roadmap rebalance whether 2 U-items in one release moves the average meaningfully — this informs whether "≥2 U-items per release" should become a standing rule. | PMO Lead | Next roadmap rebalance |
| DF-18 | v6.5 Phase 3 friction 2 / carries v6.4 DF-12 | `/commit-check` should diff `git add`'s target list against the intended file set before multi-file governance commits — deferred at v6.4 (target v6.5), **not applied this cycle either**: `.claude/skills/commit-check/SKILL.md` is outside `run sprint`'s declared write scope (Section 7 permits `claude/system/`, `claude/charter/`, `claude/agents/`, not `.claude/skills/`). This is the 1st missed target since the v6.4 defer, not yet a 2-cycle carry-forward per `lessons_learnt_prompt.md` §3.7 (which requires 2+ cycles without a `prompt_change_log.md` entry) — so not an automatic escalation, but flagged for priority attention: a 2nd consecutive miss at v6.6 would trigger the recurrence-escalation rule. Needs a routine with skill-file write authority, or an explicit Head of Specs Team-directed edit outside any single governed routine's write scope. | Head of Specs Team | 2026-07-02__release-v6.6 (next cycle) |

---

## Friction Log (this closure run)

### Friction Item 1 — STEP 2 / STEP 11 roadmap-retirement boundary was not explicit in the prompt

**Classification:** Type C — Dependency Stall (a sequencing dependency between two steps was invisible in the prompt text and only visible by inference from prior cycles' document state)
**Recurrence:** No — first identified this cycle; no prior closure_record.md or lessons_learnt_closure.md flags this boundary.

**What happened:** At STEP 2 (Roadmap Update), the existing pattern in `current_roadmap.md` shows a `*RA:<release> retired — see roadmap_archive.md...*` line immediately adjacent to each retired release's Current Version entry. Pattern-matching against that existing content, this run initially wrote a `*RA:v6.5 retired...*` line at STEP 2 — before STEP 11 (which actually performs the archival, later in the same routine) had run. This would have recorded an archival that had not yet happened. Caught by self-review before the STEP 2 write was finalized; corrected in the same session, no incorrect state was ever committed.

**Where in the routine:** STEP 2 — Roadmap Update.

**Root cause:** process gap / template omission — STEP 2's instructions (mark ✅ Complete, update Current Version, update Next planned release) do not mention the retirement annotation at all, but the adjacent visual pattern in the document from prior cycles made it easy to assume STEP 2 owns that line too.

**Blast radius analysis:**
- What would have propagated: `current_roadmap.md` would have claimed v6.5 was archived before STEP 11 (`manage roadmap`) actually ran it — a false claim that could mislead a reader of the roadmap between STEP 2 and STEP 11 of the same session, or worse, persist if STEP 11 were skipped/failed for any reason.
- When it would have surfaced: Immediately, on any reader checking `roadmap_archive.md` for the referenced entry and not finding it — likely the next roadmap rebalance's STEP 0 gap-check.
- Recovery cost if uncaught: Low (single-file, single-line fix) — but corrected before commit, so no actual recovery was needed.

**Process patch:**
→ Immediate patch applied this run:
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 2 — Roadmap Update
  - Change: Added a note clarifying the retirement annotation line is written by STEP 11, not STEP 2, and must not be written early.
  - Version: 2.15→2.16
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

## Recurrence Escalations

None. DF-18 (commit-check diff verification) is a 1st missed target, not yet a 2-cycle carry-forward under `lessons_learnt_prompt.md` §3.7 — tracked as a deferred item above, not an escalation.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/release_planning_prompt.md` | §1.4a Perennial-Return Check | Added third disposition option "(c) Resolve directly this cycle" | v2.39→v2.40 | Yes |
| `claude/system/release_planning_prompt.md` | STEP 5 Roadmap Annotation | Added fallback wording for releases with no formal `## vX.Y` roadmap section | v2.39→v2.40 | Yes |
| `claude/system/post_ship_closure.md` | STEP 2 Roadmap Update | Clarified STEP 2 / STEP 11 retirement-annotation ownership boundary | v2.15→v2.16 | Yes |

---

## New files created this run

None.

---

## Outstanding deferred patches

See "Deferred Items — carry to v6.6" table above (DF-16 through DF-19). All four rows have a named owner and a target.

---

## Escalations

None.

---

## Closure-Phase Observations

- **The non-deferrable immediate-action rule produced a clean same-day application this cycle:** LP-02 and LP-03 (Release Planning Friction Items 2 and 3) were applied at this closure rather than lagging a cycle, unlike v6.3's DF-02/DF-04 which sat unapplied through the entirety of v6.4 before being caught at v6.4's own closure. Both had unambiguous, single-sentence fixes named in `lessons_learnt.md`, which made them straightforward to apply without further design input.
- **DF-11 (v6.4's branch-check patch) landing exactly on its own named target is a positive validation of the deferred-item tracking process** — flagged in v6.4 lessons_learnt_closure.md, picked up and applied during v6.5 sprint execution itself (not even needing to wait for this closure), and the underlying defect pattern it was designed to prevent (orphaned merge-gate sync write on a stale branch) recurred exactly as predicted and was avoided in the same session.
- **Specs Index TSG reconciliation (STEP 7) closed a 2-cycle recurrence escalation this cycle:** TSG-v60-01 (BLG-QA-61), open since v6.2 and escalated to Head of Specs Team at v6.4 closure, was resolved this cycle via Release Planning's new "(c) Resolve directly this cycle" disposition (LP-03) — applied to BLG-QA-61 itself at release planning, ahead of the prompt patch that formalizes the option existing at all. TSG-v64-01 (the v6.4 Panel 0 Playwright gap) was also closed in the same cycle it was filed in — no carry-forward.
- **DF-19 (the `BLG-GOV-157`/`BLG-GOV-159` header swap) resolved itself as a byproduct of ordinary archiving, without needing a dedicated content-correction write:** both items shipped this cycle, and STEP 12's `groom backlog` archiving wrote each item's `backlog_archive.md` entry fresh, with the correct title looked up from `execution_state.json` rather than copied verbatim from the (mis-titled) active `backlog.md` heading. This is a useful general pattern — a labelling-drift item that's otherwise stuck outside every routine's write scope can still get fixed for free once the item itself ships and is archived.
- **Endpoint coverage drift check (STEP 6) found no gap this cycle** — no new endpoints were introduced in v6.5 (ST-07 rides the existing trade-plans PUT/POST payload); this breaks the 2-cycle-running pattern of a new Strategy Benchmark endpoint always trailing its performance-baseline registration by one cycle (v6.3→v6.4 BLG-OPS-82, v6.4→v6.5 BLG-OPS-83). Nothing to file this cycle.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | DF-16 (LP-01): STEP 4.1 / STEP 7 state-sync sequencing in `release_planning_prompt.md` remains unresolved — two alternative fixes proposed, needs a design decision rather than a mechanical patch. | Head of Specs Team should pick one of the two named approaches (atomic single write, or defer STEP 4.1's `.claude_current_state.json` write to STEP 7) at the next `release_planning_prompt.md` revision. | Release Planning |
| 2 | DF-17 (LP-04): v6.5 bundled 2 U-items (BLG-FE-46, BLG-FEAT-41) into one release specifically to test whether that corrects a rolling Skill-Silo Alert more effectively than the single-item pull-forward tried at v6.4. | Check at the next roadmap rebalance whether the rolling-3-cycle average moved back under the Alert threshold; this determines whether "≥2 U-items per release" becomes a standing rule. | Roadmap |
| 3 | DF-18: `/commit-check`'s pathspec-diff reinforcement has now missed its target once (v6.4→v6.5); `.claude/skills/` is outside every governed routine's declared write scope, so no routine can apply this patch as an in-scope immediate action. | If still unapplied at v6.6, this becomes a 2-cycle carry-forward and an automatic recurrence escalation per `lessons_learnt_prompt.md` §3.7 — Head of Specs Team should apply it directly, outside any single routine, before that threshold is reached. | Release Planning |
