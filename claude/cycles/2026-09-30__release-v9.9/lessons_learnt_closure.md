Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-06

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Ship the canonical ATR/stop-recalculation path with timestamps on `GET /positions` (`BLG-BE-135`, this cycle's PO Modify build-and-ship candidate), while clearing the full-capacity v9.9 debt slice — 35 stories across 6 EPICs.
Run: 2026-09-30__release-v9.9
Reviewed by: PMO Lead
Date filed: 2026-10-06
Prior cycle checked: 2026-09-28__release-v9.8 (`lessons_learnt_closure.md`)

---

## What worked well

- All 35 shipped stories traced to their `BLG-*` source items in one scripted pass (STEP 3) using each `stage4_backlog_slice.md` entry's `**Source:**` field. Each COMPLETE banner records the EPIC PR and commit SHA from `execution_state.json`.
- The split-achievability carve-out (STEP 3.1) was checked against every story's notes. No partial landing was found: ST-17's AC records the required-check state "either way", and ST-11's matrix shipped with its gaps filed as backlog items.
- The ESC-CLOSE-20260930-03 ruling (`post_ship_closure.md` v2.37) worked cleanly on its first live use. ST-01's `Pass_with_deviation` was read as exempt from a Known Deviations entry directly from the prompt text, so STEP 5 had nothing to create.
- All four v9.8 closure escalations (`ESC-CLOSE-20260928-02`, `ESC-CLOSE-20260930-01/02/03`) were resolved on 2026-10-05, before this closure. None carried forward.
- The cycle's own PR reviews caught all 4 test-coverage weaknesses and backlogged them (`BLG-QA-204/210/212/213`) before verification. STEP 7 only had to register them as §49 entries.
- Endpoint coverage drift (STEP 6): 0 gaps, with no new routes this cycle.

---

## Friction Log

**Closure-phase finding — STEP 1.5 command does not run as written.** `post_ship_closure.md` STEP 1.5 says to run `python3 scripts/send_changelog_digest.py --version "v<X.Y>"`. That command fails here with `ModuleNotFoundError` (`psycopg2` first, then `utils`). It ran only as `PYTHONPATH=backend backend/.venv/bin/python3 scripts/send_changelog_digest.py ...`, using a stub `DATABASE_URL`, and then returned `sent: false` because Telegram credentials are absent. CLAUDE.md §9 already says to use the venv for pytest, but the STEP 1.5 command does not reflect that, and the `PYTHONPATH` requirement is not written down anywhere. The step is non-blocking, so nothing was lost. However, a literal reading would log "attempted" against a crash rather than a real send attempt. Type A — Governance Drift. Deferred; see below.

**Closure-phase finding — Specs Index header drift.** The `docs/specs/Specs_Index.md` header `**Last Updated:**` still read 2026-09-28 (the v9.7 closure), even though the v9.8 closure added §48 and a Changelog row on 2026-09-30. It was corrected this run and disclosed in the Changelog row. This is a one-off miss, already covered by CLAUDE.md §2's `Last Updated` rule, so no new action is needed.

**Closure-phase finding — ideas archive header drift.** The `claude/ideas/ideas_register_archive.md` header `**Last Updated:**` still read 2026-08-12, although at least 3 later housekeeping runs had appended `## Archived` sections (most recently 2026-09-30). It was corrected this run. This is the same class of one-off miss as the Specs Index header and is already covered by CLAUDE.md §2, so no new action is needed.

**Deviation consolidation review (STEP 5.1):** not due. This is cycle 2 of 3 since the last run (2026-09-28). The counter advances to `2` at STEP 10.

---

## Recurrence Escalations

One new `§3.7` recurrence escalation was raised this closure and filed as `ESC-CLOSE-20261006-01` in `closure_escalations.md` (SLA 2026-10-09):

1. **`claude/roadmap/*` / existing-`backlog.md`-item write-scope boundary** (Phase 3 Friction Item 2, a recurrence of v9.8 Phase 3 Friction Item 2 after 1 carry). It now also covers the v9.8 `workforce_capacity.md` worked-example patch (2nd carry), which is blocked by the same boundary. The proposal is consolidated in `BLG-GOV-362`, owned by Head of Specs Team.

The Phase 4 §3.7 escalation (agent-mediated signer-format mandate, 2nd carry) was **not** re-filed as an escalation. Its own recommendation offered two acceptable options, and the cross-reference option was unambiguous, so it was applied immediately (see below). That closes the carry.

---

## Process improvements actioned this run

Two immediate actions were applied under the same-cycle application pattern (`post_ship_closure.md` STEP 8). Both are in `claude/system/execution_prompt.md` v3.81→v3.82:

1. **LL-v9.9-P3-01 (Phase 3 Friction Item 1, `BLG-GOV-368`).** §3.2.B gains a hard cross-EPIC commit pre-PR check: `git log origin/main..HEAD` must list no commit tagged with another EPIC's `[EPIC-yy]`, with `[GOVERNANCE]` commits exempt. This is the PR #1886 root cause. The fix wording was concrete and the target file is in scope. The optional `quality_gate.yml` mirror is not applied; it stays open on `BLG-GOV-368` for the owner.
2. **LL-v9.9-P4-02 (Phase 4 Friction Item 2, carried since v9.7).** §3.2.A gains a one-line cross-reference to `qa_evidence_template.md`'s agent-mediated provenance requirement. This is the item's own recommended option, and it closes the mechanical carry.

The CLAUDE.md §6 checklist is complete: `execution_prompt_changelog.md` row 3.82; `OPERATIONAL_GUIDE.md` v4.220→v4.221, with the §8 source-prompt header, the §14 Execution Engine Source row and the §14 self-row; and 2 rows in `prompt_change_log.md`.

---

## New files created this run

- `claude/cycles/2026-09-30__release-v9.9/closure_state.json`
- `claude/cycles/2026-09-30__release-v9.9/closure_escalations.md` — 1 recurrence escalation (`ESC-CLOSE-20261006-01`)
- `claude/cycles/2026-09-30__release-v9.9/closure_record.md`
- `claude/cycles/2026-09-30__release-v9.9/lessons_learnt_closure.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Cycles carried |
|------|---------|----------------|-------|--------|-----------------|
| `claude/system/post_ship_closure.md` | STEP 1.5 | Make the digest command run as written: `PYTHONPATH=backend backend/.venv/bin/python3 scripts/send_changelog_digest.py --version "v<X.Y>"` (matching CLAUDE.md §9). Alternatively, make the script self-locating so that it puts `backend/` on `sys.path` itself and imports `psycopg2` lazily. | Head of Specs Team (prompt) / Head of Engineering (script option) | Next `post_ship_closure.md` revision, or a backlog item if the script option is chosen | 1st cycle (new this closure). Not applied now, because the owner has to choose between a prompt fix and a script fix, and this engine should not edit its own prompt mid-run without that choice. |
| `claude/system/delivery_verification_prompt.md` | STEP 2.1/2.3 | Define a path for a `Pass_with_deviation` whose gap is fully disposed of by a recorded Owner/authority ruling: either cite the decision record in place of a backlog item, or require `Pass with notes` (Phase 4 Friction Item 1). | Head of Specs Team | Next `delivery_verification_prompt.md` revision touching STEP 2.1/2.3 | 1st cycle (new this closure) |
| `shared_standards.md` §16.4.1 / `.github/workflows/` | SLA-breach surfacing | A scheduled reminder that notifies when an `Open` escalation passes `sla_due_utc` between sessions (Phase 3 Friction Item 3). | PMO Lead | Next lifecycle audit (`run audit`) | 1st cycle (new this closure) |
| `claude/roadmap/workforce_capacity.md` | Effort Band → Days Conversion Table | `XS (<1h)` worked example (v9.8 Release Planning Friction Item 3). | Head of Specs Team | Folded into `ESC-CLOSE-20261006-01` (same write-scope boundary) | 2nd carry, **escalated** |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `claude/roadmap/*` / existing-`backlog.md`-item write-scope boundary: 3 per-story rulings this cycle, recurrence of v9.8 Phase 3 Friction Item 2. | Recurrence escalation (`§3.7` mandatory) | Head of Specs Team (with PMO Lead) | A ruling on `BLG-GOV-362`'s options is needed before the next `plan sprint` seals. Tracking: `ESC-CLOSE-20261006-01`, SLA 2026-10-09. |

---

## Carry-Forward
Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `ESC-CLOSE-20261006-01` is open (SLA 2026-10-09). | If it breaches its SLA before the next routine reads `open_escalations`, the SLA-breach advisory applies. Sprint Planning for v9.10 should not seal an AC naming a `claude/roadmap/*` file or an existing `backlog.md` field without first checking the ruling. | Sprint Planning / any next-invoked routine |
| 2 | `BLG-FE-193`'s gate (`BLG-BE-135` shipped on `GET /positions`) is now met. Its Provisional-Target is still `TBD`. | v9.10 release planning should treat it as a should-seat build-and-ship U-item candidate (v9.9 Release Planning Friction Item 1). `BLG-FEAT-59` is also gate-cleared. | Roadmap Rebalance / Release Planning |
| 3 | `BLG-GOV-368`'s prompt half is applied (`execution_prompt.md` v3.82). Only the optional `quality_gate.yml` mirror remains. | The owner should narrow or close the item at the next `groom backlog`, so it is not re-seated for work already done. | Backlog Management / Head of Specs Team |
