Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-18

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Clear the full v9.5 debt-reduction scope — 43 items across 6 EPICs — at the top of confirmed sprint capacity, resolving the cycle's two genuine ungated P1 items first.
Run: 2026-09-15__release-v9.5
Reviewed by: PMO Lead
Date filed: 2026-09-18
Prior cycle checked: 2026-09-14__release-v9.4

---

## What worked well

- All 43 shipped stories traced cleanly to their `BLG-*` source items in one pass (STEP 3) — the `**Source:**` field on every `stage4_backlog_slice.md` entry made the ST→BLG mapping mechanical and error-free across all 6 EPICs.
- The STEP 6 Endpoint Coverage Drift Check (with the v2.33 Markdown-normalisation fix applied) found a genuine 0-gap result on a re-run against 146 normalised `openapi.yaml` endpoints — the normalisation fix from `2026-09-07__release-v9.2` closure continues to hold up under real use.
- Both Release Planning friction items (`LL-v9.5-Release-01`, `LL-v9.5-Release-02`) had concrete, unambiguous recommended wording already spelled out in their own originating records despite neither explicitly flagging itself "ready to apply now" — the same-cycle application pattern (formalised v2.32) continues to correctly favour applying now over deferring on a technicality.
- Zero formal `DEV-*` deviations meant STEP 5 (Canonical Spec Deviation Compliance Check) and STEP 5.1's per-cycle scope were both trivially clean this run, leaving full attention for the cross-cycle consolidation cadence check.

---

## Friction Log

No new closure-phase friction items this cycle. STEPs 1–7 (changelog, roadmap, backlog reconciliation, scope/decisions supersession, deviation compliance, operational docs, Specs Index) all completed with no missing documents, no stale references requiring correction beyond the routine dated-section appends, and no discrepancies between the authoritative backlog slice and `backlog.md`.

---

## Recurrence Escalations

None. Both deferred patches carried forward from `2026-09-14__release-v9.4`'s own Carry-Forward item 1 (release-planning over-capacity selection method; SLA mid-sprint surfacing) were confirmed already resolved at `v9.4`'s own closure itself (Outstanding Actions #3 and #4, `prompt_change_log.md` 2026-09-15 rows) — not carried into this cycle, and not a recurrence.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/release_planning_prompt.md` | §1.3a | Added an explicit note that a data-quality warning from the scripted gate-detection scan is not itself exclusionary — each flagged item's own body text and `Type` field must still be read individually before deciding ready/not-ready (`LL-v9.5-Release-01`). | 2.52 → 2.53 | Yes — appended to `claude/system/prompt_change_log.md` |
| `claude/system/release_planning_prompt.md` | §1.4c step 1 | Renamed "P2-first" → "P1-then-P2-first" so the canonical selection method's text matches its evident intent now that a cycle (`v9.5`) has held genuine ready P1 items (`LL-v9.5-Release-02`). | 2.52 → 2.53 | Yes — appended to `claude/system/prompt_change_log.md` |

`claude/system/OPERATIONAL_GUIDE.md` was bumped to v4.197 in the same run to reflect both changes (§6B source-prompt line, §14 table row, §14 self-row, Change Log top row) — recorded as a companion entry, not a separate lessons-learnt action.

---

## New files created this run

None.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `.claude/skills/governance-drift/SKILL.md` (or its underlying check script) | Self-consistency check | Extend the existing `OPERATIONAL_GUIDE.md` §14 self-consistency check to also verify the `Last Updated` cell, not only the `Version` cell, in each table row — closes the gap that let the `Last Updated` cell go unedited across 6 consecutive `Version` bumps in PR #1716 despite each commit message claiming it was updated. | Head of Specs Team | `BLG-GOV-336` |
| `claude/system/execution_prompt.md` | §3.2.A | Consider a same-EPIC cross-story consistency check for "testing-gap disclosure" as its own category (not only the existing `spec_references` roll-up) — ST-42 filed `BLG-QA-180` for a missing Playwright duration assertion; sibling story ST-41 had the identical gap but only surfaced via independent PR review, not the story's own execution. | Head of Specs Team | Next `execution_prompt.md` revision touching §3.2.A |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| ST-37/ST-38 (EPIC-05) wrote to `claude/roadmap/workforce_capacity.md`, a path `execution_prompt.md` §7 lists under "Must not modify: `claude/roadmap/*`" with no carve-out — treated as implicitly authorised via `sprint_backlog.md`'s own sequencing note, not an explicit §7 exception. | Authority ambiguity | Product Owner + Head of Specs Team | Ruling needed on whether this should become a standing, narrow write-scope exception, analogous to the existing documented `backlog.md` new-item exception. Tracking item: `BLG-GOV-337`. |
| `qa_evidence_EPIC-04.md`'s own autonomous-class eligibility check (ST-22) disclosed a genuine self-graded ambiguity in `BLG-GOV-19` Criterion 1 and explicitly stated its own sign-off "should not be treated as final" without human Director of Quality confirmation — PR #1715 merged, and this cycle's (also agent-mediated) delivery verification reached the same evidence without that confirmation occurring. | Governance gap | Head of Specs Team | No mechanism currently forces a genuinely human decision point when both the authoring and verifying steps are agent-mediated and the authoring step discloses self-doubt about its own gate eligibility. Tracking item: `BLG-GOV-335`. |

---

## Carry-Forward
Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Two open decision-required escalations (`BLG-GOV-337` write-scope exception ruling; `BLG-GOV-335` autonomous-class self-certification ruling) remain unresolved at this closure — both are P3-tracked backlog items, not blocking, but both name Head of Specs Team (one jointly with Product Owner) as the deciding authority with no formal SLA clock started. | Watch for both to cross 2+ consecutive cycles without a ruling — at that point escalate per `lessons_learnt_prompt.md §3.7`'s recurrence-escalation threshold rather than letting them coast as open backlog items indefinitely. | Post-Ship Closure |
| 2 | This is the first cycle since the `governance-drift` skill was introduced that its own self-consistency check was found to cover only the `Version` cell of an `OPERATIONAL_GUIDE.md` §14 table row, not the sibling `Last Updated` cell in the same row — a 6-commit-long drift went undetected until an independent PR review pass caught it. | If `BLG-GOV-336`'s skill-check extension is not applied within 1–2 cycles, consider whether the governance-drift skill needs a broader audit for other single-field-only checks with an unstated but assumed sibling-field guarantee. | Post-Ship Closure |
