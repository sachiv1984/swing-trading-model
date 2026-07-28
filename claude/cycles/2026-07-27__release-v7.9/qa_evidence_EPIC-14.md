Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

## Consolidation Block

**EPIC:** EPIC-14 — Displacement debt register — track unused named displacement candidates
**Cycle:** 2026-07-27__release-v7.9
**Sprint goal:** Ship all 15 v7.9 EPICs — the two P1 UX anchors and the 13 capacity-fill engineering-hardening items — with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** Derived from spec + AC — governance process artefact, verifiable by review.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-14 | This file, § "Displacement Debt Register — Design" | Log format designed and seeded with real history reconstructed from `claude/roadmap/decision_log.md` (2 roadmap-level candidates: 4.1c Server-Side PDF Report, CHART-IX). Actual file placement in `claude/roadmap/` handed off — see § "Write-scope note" below. | AC-01: Log format documented — Pass (documented in this file; physical placement in `claude/roadmap/` is a handoff, not a gap — see note). AC-02: Head of Specs Team sign-off — Pass (agent-mediated). | Pass with notes | None |

**QA test coverage:**
- Scenarios run: N/A — governance process artefact, verifiable by review only.
- Regression areas checked: None.
- Known deviations filed: None — write-scope handoff is not a spec deviation (same class of resolution as `BLG-BE-46` AC-04 and this cycle's `EPIC-03` AC-03).

---

## Displacement Debt Register — Design

### Purpose

STEP 8 of `roadmap_prompt.md` records a per-cycle "Displacement candidate flag" (`Displacement candidate: Yes — <rationale> — <date>`) in `claude/roadmap/initiative_register.md` when an initiative is named as the natural next-stop candidate. This is a point-in-time flag only — there is no cross-cycle view of how many named candidates are ever actually displaced versus repeatedly named and never used. This register closes that gap.

### Scope

Roadmap-level (STEP 8) displacement candidates only — the ones recorded in `initiative_register.md`. Backlog-level displacement (Adds/Kills recorded per-cycle in `decision_log.md`'s own "Displacement" lines) is already visible cycle-by-cycle in that log and does not need a separate rolling register.

### Log format

| Candidate | Rationale as flagged | First flagged | Times re-flagged | Disposition | Disposition date/cycle |
|-----------|----------------------|----------------|-------------------|-------------|--------------------------|
| \<name/ID\> | \<one-line rationale as recorded at first flag\> | \<DL-id, date\> | \<count\> | Displaced / Named, not yet displaced / Completed without displacement / Retired without use | \<DL-id, date — or "—" if not yet resolved\> |

**Disposition enum (4 values):**
- **Displaced** — a later Kill/Replace decision actually names this candidate as the item stopped.
- **Named, not yet displaced** — still an active initiative, flagged but not yet acted on.
- **Completed without displacement** — the candidate shipped via normal delivery (roadmap ran its course) while still carrying an open displacement flag; it was never actually used as a Kill/Replace target. This is a distinct, real outcome from "Displaced" — the flag added no signal in this case, which is itself worth tracking.
- **Retired without use** — descoped or killed for a reason unrelated to the displacement flag (e.g. superseded, no longer valuable) without ever being the actual displacement target.

**Update rule (for whoever maintains this going forward — see write-scope note):** each cycle STEP 8 writes a new "Displacement candidate: Yes" flag to `initiative_register.md`, check whether the named candidate already has a row here. If yes: increment "Times re-flagged" (unless this is the same cycle the row was first added). Resolve Disposition per the enum above once the candidate's fate is known (Displaced / Completed without displacement / Retired without use); leave as "Named, not yet displaced" while still open.

### Initial seed content (reconstructed from `claude/roadmap/decision_log.md` history)

| Candidate | Rationale as flagged | First flagged | Times re-flagged | Disposition | Disposition date/cycle |
|-----------|----------------------|----------------|-------------------|-------------|--------------------------|
| 4.1c — Server-Side PDF Report | Lowest-value existing roadmap item; natural displacement candidate if a future Add requires stops | DL-005, 2026-03-04 | 0 | Displaced | DL-008, 2026-03-15 (killed to create roadmap slot for BLG-OPS-01) |
| CHART-IX — Chart Interactivity Enhancements | Natural displacement candidate if a future roadmap-level Add requires stops; lowest strategic urgency relative to impact, smallest scope (S effort) | DL-009, 2026-03-17 | 0 | Completed without displacement | DL-011, 2026-03-21 (shipped v2.1 via normal delivery, 4 days after being flagged — never actually used as a Kill/Replace target) |

This seed content demonstrates the register's value immediately, and shows why the 4-value enum matters: 4.1c was named once and genuinely displaced 11 days later (the flag worked as intended); CHART-IX was named as a candidate but then shipped normally days later without ever being touched by a Kill/Replace decision — a case the plain "Displaced / Not yet" framing this backlog item's problem statement implies would have silently mis-recorded as either "still open" or "displaced". Neither historical case is actually an example of the "repeatedly named and never used" pattern the problem statement describes (no roadmap-level candidate has yet been re-flagged 2+ times in this repo's history) — the register's real value is in catching that pattern the first time it occurs, which this seed content cannot demonstrate retroactively.

### Write-scope note (hard gate — not a gap)

`claude/roadmap/*` is outside `execution_prompt.md` §7's write scope (hard gate) — this routine cannot create `claude/roadmap/displacement_debt_register.md` directly. The design above is complete and ready to use as-is; placement is a mechanical copy into that path. Handed off to the Roadmap Rebalance Engine (or Head of Specs Team) to:
1. Create `claude/roadmap/displacement_debt_register.md` using the format and seed content above.
2. Add one line to `roadmap_prompt.md` STEP 8's "Displacement candidate flag" instruction directing the engine to also update this register (in addition to the existing `initiative_register.md` write) — a `claude/system/` prompt edit, also outside this routine's write scope, so bundled into the same handoff.

This mirrors the same resolution already applied twice this cycle (`EPIC-03` AC-03) and once historically (`BLG-BE-46` AC-04) for artefacts that belong in a write-scope-restricted folder.

**Tracked as `ESC-EXEC-20260727-02`** (`execution_escalations.md`, non-blocking) per agent-mediated QA & Testing Owner review of PR #1101 — raised so the two-part handoff (file creation + `roadmap_prompt.md` STEP 8 edit, which must land together) doesn't fall through once this PR merges and this cycle's artefacts stop being actively read.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-14 only, autonomous)
- Criterion 2: All AC verifiable by code review alone — ✓ (documentation/design review)
- Criterion 3: No frontend-visible change — confirmed no file under `src/pages/**` or `src/components/**` was created or modified — ✓
- Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-27
- Comments: Autonomous class sign-off — all four qualifying criteria met. Head of Specs Team sign-off obtained separately via agent-mediated review (§5.3): first pass found the CHART-IX seed row factually wrong (claimed "not yet displaced" when it actually shipped via normal delivery per DL-011/2026-03-21, never displaced) — corrected (4th Disposition enum value "Completed without displacement" added, row and citations fixed, closing paragraph re-calibrated to not overclaim), then re-reviewed and approved.
