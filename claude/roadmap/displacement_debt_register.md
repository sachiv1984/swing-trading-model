# Displacement Debt Register

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-07 (created — ST-26, EPIC-04, v9.1, BLG-GOV-264, closing `ESC-EXEC-20260727-02`/`ESC-EXEC-20260818-02`)

> ⚠️ Standing Notice: This register is a planning inventory only. It does not constitute canonical specification.

---

## Purpose

`roadmap_prompt.md` STEP 8 records a per-cycle "Displacement candidate flag" (`Displacement candidate: Yes — <rationale> — <date>`) in `claude/roadmap/initiative_register.md` when an initiative is named as the natural next-stop candidate. This is a point-in-time flag only — there was no cross-cycle view of how many named candidates are ever actually displaced versus repeatedly named and never used. This register closes that gap.

## Scope

Roadmap-level (STEP 8) displacement candidates only — the ones recorded in `initiative_register.md`. Backlog-level displacement (Adds/Kills recorded per-cycle in `decision_log.md`'s own "Displacement" lines) is already visible cycle-by-cycle in that log and does not need a separate rolling register.

## Log

| Candidate | Rationale as flagged | First flagged | Times re-flagged | Disposition | Disposition date/cycle |
|-----------|----------------------|----------------|-------------------|-------------|--------------------------|
| 4.1c — Server-Side PDF Report | Lowest-value existing roadmap item; natural displacement candidate if a future Add requires stops | DL-005, 2026-03-04 | 0 | Displaced | DL-008, 2026-03-15 (killed to create roadmap slot for BLG-OPS-01) |
| CHART-IX — Chart Interactivity Enhancements | Natural displacement candidate if a future roadmap-level Add requires stops; lowest strategic urgency relative to impact, smallest scope (S effort) | DL-009, 2026-03-17 | 0 | Completed without displacement | DL-011, 2026-03-21 (shipped v2.1 via normal delivery, 4 days after being flagged — never actually used as a Kill/Replace target) |

**Disposition enum (4 values):**
- **Displaced** — a later Kill/Replace decision actually names this candidate as the item stopped.
- **Named, not yet displaced** — still an active initiative, flagged but not yet acted on.
- **Completed without displacement** — the candidate shipped via normal delivery (roadmap ran its course) while still carrying an open displacement flag; it was never actually used as a Kill/Replace target. This is a distinct, real outcome from "Displaced" — the flag added no signal in this case, which is itself worth tracking.
- **Retired without use** — descoped or killed for a reason unrelated to the displacement flag (e.g. superseded, no longer valuable) without ever being the actual displacement target.

**What the seed content shows:** 4.1c was named once and genuinely displaced 11 days later (the flag worked as intended); CHART-IX was named as a candidate but then shipped normally days later without ever being touched by a Kill/Replace decision — a case a plain "Displaced / Not yet" framing would have silently mis-recorded as either "still open" or "displaced." Neither historical case is an example of the "repeatedly named and never used" pattern the register primarily exists to catch (no roadmap-level candidate has yet been re-flagged 2+ times in this repo's history) — the register's real value is in catching that pattern the first time it occurs.

**Currency check (2026-09-07, at file creation):** confirmed no roadmap-level STEP 8 displacement candidate has been flagged in `initiative_register.md`/`decision_log.md` between this register's original design (`2026-07-27__release-v7.9`, ST-14/EPIC-14) and this file's physical creation — the seed content above (2 candidates) remains the complete, current history. (The one other "displacement" mention found in `decision_log.md` in that window — BLG-FE-27, a backlog-level deprioritisation — is out of this register's scope per the Scope section above, not a missed roadmap-level candidate.)

## Update Rule

Each cycle, `roadmap_prompt.md` STEP 8 writes a new "Displacement candidate: Yes" flag to `initiative_register.md`; in the same step (per that prompt's own STEP 8 instruction, wired at ST-21/EPIC-06/v8.9/BLG-GOV-264), check whether the named candidate already has a row here:
- If yes: increment "Times re-flagged" by 1 (unless this is the same cycle the row was first added).
- If no: add a new row (`Candidate`, `Rationale as flagged`, `First flagged` = this cycle's Decision Log ID and date, `Times re-flagged` = 0, `Disposition` = "Named, not yet displaced", `Disposition date/cycle` = "—").

Separately — whenever a Kill/Replace decision names a candidate that already carries an open "Named, not yet displaced" row here, resolve that row's Disposition to "Displaced" with the resolving cycle's Decision Log ID and date. "Completed without displacement" and "Retired without use" are typically resolved at Backlog/Roadmap Management time, once an initiative's actual fate becomes known.

---

## Provenance

Format and seed content designed at `claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md#Displacement Debt Register — Design` (ST-14, EPIC-14, BLG-GOV-258). `roadmap_prompt.md` STEP 8's write instruction for this file was wired at `2026-08-17__release-v8.9` (ST-21, EPIC-06, BLG-GOV-264, `roadmap_prompt.md` v9.15→v9.16). Physical file creation — the one remaining piece of that two-part handoff — completed here (ST-26, EPIC-04, v9.1, BLG-GOV-264), closing `ESC-EXEC-20260727-02` and `ESC-EXEC-20260818-02`. Created directly per explicit user/Product Owner direction (2026-09-07) rather than via a full `run roadmap` invocation — a targeted, scoped action using the already-designed, already-reviewed content verbatim, not a substitute for that routine's own STEP 8 write path going forward (which remains the authoritative future maintainer of this file, per the Update Rule above).
