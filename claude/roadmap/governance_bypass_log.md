**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-04
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Created by:** ST-13 (BLG-GOV-269, EPIC-03, v8.2)

---

# Governance Bypass Log

## Purpose

Structured, append-only log of every occasion a governed routine (roadmap rebalance, release planning, sprint planning/execution, design gate) was bypassed by a direct write to its output artefacts instead of being invoked normally — whether the bypass was an ungoverned out-of-band write authorised in-session by the Product Owner, or a governed emergency exception mechanism (`amend cycle`) used in place of the routine change would otherwise have gone through.

This log exists to make the *frequency and pattern* of bypasses visible over time — a question no single decision record answers on its own, since each is filed independently in `decision_log.md` or an amendment folder without cross-referencing the others. PMO Lead reviews this log as an input to process-health assessment (e.g. whether a recurring bypass pattern indicates a genuine, permanent gap in a governed routine's write scope that should be closed, rather than re-litigated informally each time it recurs).

**This log does not itself resolve or prevent bypasses** — it is a traceability record only. Closing an identified structural gap (e.g. adding a new condition to `roadmap_prompt.md` STEP 8.1) remains a separate governance-prompt-edit action, tracked via the normal 4-step edit checklist (`CLAUDE.md` §6) and `prompt_change_log.md`.

## Append-Only Rule

New rows are appended at the bottom of the table below, in chronological order. Existing rows are never edited or removed — if a decision reference in this log is later superseded or corrected, add a note in a new row rather than editing the original.

## Bypass Type Classification

| Type | Meaning |
|------|---------|
| **Ungoverned direct-write** | No governed routine's Write Scope covers the scenario; the write was made directly by explicit Product Owner authorisation, with no compliant path available at the time. |
| **Governed-path-declined** | A compliant governed path existed (e.g. `run roadmap --reason "scheduled"`) but was explicitly bypassed by Product Owner choice in favour of a lower-overhead direct write, for a scope/complexity the PO judged disproportionate to a full routine invocation. |
| **Governed emergency exception** | The bypass itself went through a governed exception mechanism (`amend cycle`, restricted to `emergency-fix`/`hard-blocker` reasons per `amendment_cycle_prompt.md` §11) rather than an ungoverned direct write — included here for completeness since it is still a deviation from the sprint's normal sealed-scope flow, even though procedurally correct.

## Log

| Date | Ref | Type | File(s) Written | Reason Given | Routine Bypassed |
|------|-----|------|------------------|---------------|-------------------|
| 2026-05-23 | AMD-20260523-01 | Governed emergency exception | Sprint backlog slice, `release_plan.md` (v4.0) | Emergency-fix — ratification pending Product Owner + Director of Quality | Normal sealed-sprint-scope flow (`amendment_cycle_prompt.md` governed exception path) |
| 2026-07-16 | DL-068 | Ungoverned direct-write | `current_roadmap.md` §1/§3 (v7.3 anchor label) | No governed engine had a compliant write path for "formally version-label a non-empty, already-committed, but unversioned Now-horizon carry-forward" — `roadmap_prompt.md` STEP 8.1 condition 1 required an empty horizon; Release Planning's write scope only permits annotating an existing release section | `release_planning_prompt.md` STEP -1.2 preflight / `roadmap_prompt.md` STEP 8.1 |
| 2026-07-17 | DL-069 | Ungoverned direct-write | `workforce_capacity.md` (Sprint Capacity Baseline raised ~12–14 → ~24–28 days) | Narrow, well-evidenced scope (5 cycles of `execution_state.json` timestamp evidence); full rebalance judged disproportionate for a single-field capacity correction | Roadmap Rebalance Engine STEP 7 (Workforce Economics Gate) |
| 2026-07-17 | DL-071 | Governed-path-declined | `current_roadmap.md` §1/§3 (v7.5 anchor label) | A compliant path now existed (`roadmap_prompt.md` v9.2 STEP 8.1 condition 1b, closed the DL-068 gap) but was bypassed by explicit PO direction, repeating the established low-overhead direct-write pattern at every release boundary since v7.2→v7.3 | `run roadmap` (STEP 8.1 condition 1b path) |
| 2026-07-20 | DL-072 | Governed-path-declined | `current_roadmap.md` §1/§3 (v7.6 anchor, new — Now horizon was empty) | Original "Empty Now Horizon Gate" scenario `roadmap_prompt.md` STEP 8.1 was built to handle; a fully compliant `run roadmap --reason "scheduled"` path existed and was recommended first, but PO directed the bypass over a full scheduled rebalance | `run roadmap --reason "scheduled"` (full rebalance) |
| 2026-07-20 | DL-073 | Ungoverned direct-write | `release_plan.md`, `stage4_backlog_slice.md`, `stage4_issue_manifest.json`, `cycle_summary.md`, scope doc, decisions record, `current_roadmap.md` §3, `backlog.md` (v7.6 scope expansion, +6 EPICs) | Both governed paths checked and correctly declined to apply: Amendment Cycle Engine restricted to `emergency-fix`/`hard-blocker` only (this was routine scope growth); re-invoking `plan release` blocked by its own Terminal State Guard (`status = Published`). No compliant path existed; PO-authorised bypass reopening just-published artefacts | `amend cycle` / `plan release --version "v7.6"` |
| 2026-07-21 | DL-074 | Governed-path-declined | `current_roadmap.md` §1/§3 (v7.7 anchor, 7 named items) | PO asked to "file" 7 already-identified/prioritised items directly; a compliant `run roadmap --reason "scheduled"` path existed but would additionally trigger mandatory idea intake (register under the 20-item threshold) — PO chose the lighter direct-write pattern established at DL-068/DL-071/DL-072/DL-073 instead | `run roadmap --reason "scheduled"` (full rebalance, including STEP -1.6 mandatory idea intake) |
| 2026-07-17 | AMD-20260717-01 | Governed emergency exception | v7.4 sprint scope (`release_plan.md`, backlog slice — 4 of 5 items removed) | Hard-blocker — Design Gate found no approved design artefact for 4 items, and those artefacts structurally could not exist before Sprint Planning's Design-Gate-Passed precondition; ratified by Product Owner + Head of Specs Team | Sprint Planning's normal Design-Gate-Passed lifecycle precondition |

## Cross-Reference

Full rationale for each row is filed at its `Ref` column's source: `DL-*` entries in `claude/roadmap/decision_log.md`; `AMD-*` entries at `claude/cycles/<cycle_id>/amendments/<AMD-ID>/amendment_manifest.md`. This log is a summary index only — it does not duplicate the full rationale text.

## Backfill Note (ST-13, EPIC-03, v8.2)

The 8 rows above were identified by systematically scanning `claude/roadmap/decision_log.md` for entries whose `Cycle` field reads "out-of-band write" or whose `Rationale` describes bypassing a governed routine (`DL-060` through `DL-077` reviewed; `DL-070`, `DL-075`, `DL-076`, `DL-077` confirmed as normal governed rebalances, not bypasses, and excluded), plus both `amendment_manifest.md` files found under `claude/cycles/*/amendments/`. No bypass instances were found before `2026-05-23` (`AMD-20260523-01` is the earliest amendment on record) or between `2026-07-21` (`DL-074`) and this story's authoring date (`2026-08-04`) — `DL-075`–`DL-077` and all subsequent scheduled rebalances through post-ship closure `2026-08-03__release-v8.1` ran as normal governed cycles with no bypass.

## Sign-off

- **PMO Lead:** agent-mediated sign-off — 2026-08-04 (ST-13, EPIC-03, v8.2)
