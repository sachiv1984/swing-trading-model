Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-12

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Make the post-trade debrief state R achieved and the stop at exit (`BLG-BE-152`, P1 Correctness Fast-Track). Confirm every AI feature works after the v9.4–v9.10 import defect (`BLG-BE-150`). Make the Risk Dashboard and Positions page show real prices, GBP entry values, true stop distance and calendar-day grace (`BLG-BE-154`, `BLG-FE-206`, build-and-ship). Ship the AI monthly P&L narrative (`BLG-FEAT-59`) and clear v9.11's records, spec and governance hygiene items. 43 stories across 6 EPICs.
Run: 2026-10-08__release-v9.11
Reviewed by: PMO Lead
Date filed: 2026-10-12
Prior cycle checked: 2026-10-06__release-v9.10 (`lessons_learnt_closure.md`)

---

## What worked well

- **Tracing.** All 43 shipped stories traced to their `BLG-*` source items in one scripted pass (STEP 3), using each slice entry's `**Source:**` field. Every COMPLETE banner carries the EPIC PR and the story commit SHA from `execution_state.json`. The split-achievability carve-out was checked against every story's notes. ST-29 (backend remainder `BLG-BE-156`) and ST-33 (ruling with no remainder) leave no partial scope on their own source items, so all 43 were correctly marked COMPLETE.
- **Changelog `User Impact` parsed as intended.** The v9.11 entry was read back through `get_latest_changelog_entry()` before moving on. It returns the 4 user-facing EPIC rows and excludes the 2 `—` rows. One row was reworded after that read-back so that it states the stale-price behaviour plainly.
- **All four v9.10 carry-forward items closed in-cycle.**
  - `ESC-CLOSE-20261007-01` was resolved on 2026-10-07.
  - `run audit` ran (`AUD-2026-10-08`) and shipped the SLA reminder workflow.
  - A scheduled rebalance ran (`2026-10-08__scheduled`), and `BLG-GOV-355` shipped as ST-34.
  - `BLG-BE-147` was seated and shipped as ST-14.
- **Same-cycle application pattern held.** All three Phase 3 and Phase 4 prompt patches with unambiguous fix text were applied at this closure (`execution_prompt.md` v3.85, `delivery_verification_prompt.md` v3.15), with `OPERATIONAL_GUIDE.md` §14 and the phase headers re-checked for drift afterwards.

---

## Friction Log

### Friction Item 1

**Classification:**
- Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced

**Recurrence:** No

**What happened:**
STEP 0's Audit Cadence Check read `completed_cycle_count` = 87 and `last_audit_cycle_count` = 87. The modulo condition (`87 % 3 == 0`) fired "AUDIT DUE". But `AUD-2026-10-08` had already run at count 87: the v9.10 closure took the count to 87, and the audit then wrote `last_audit_cycle_count` = 87 before v9.11's sprint began. The modulo branch has no check for an audit already run at the current count, so it advised an audit that had just been done. The gap-based branch already uses `last_audit_cycle_count`; the modulo branch did not.

**Where in the routine:**
STEP 0 — Audit Cadence Check

**Root cause:**
process gap

**Blast radius analysis:**
- What would have propagated: a spurious "run audit before next Phase 1B" advisory in this closure's Advisory Summary, and a second audit inside one 3-cycle window.
- When it would have surfaced: next session, when a reader compared the advisory with `last_audit_id`. Otherwise never, and a redundant audit would have been run.
- Recovery cost if uncaught: low (single file fix)

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 0 — Audit Cadence Check
  - Change: The modulo condition fires only when `completed_cycle_count % 3 == 0` **and** `last_audit_cycle_count` ≠ `completed_cycle_count`.
  - Version: v2.39 → v2.40
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to claude/system/prompt_change_log.md

### Friction Item 2

**Classification:**
- Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced

**Recurrence:** No

**What happened:**
STEP 6's `categorizeEndpoint()` follow-up only asks whether a *new* top-level path prefix was introduced this cycle. This cycle's new routes (`GET /market/regime`, `GET`/`POST /reports/monthly-pnl/narrative`) all sit under existing prefixes, so the check passed. However, `/reports` itself has no `includes()` case in `src/pages/SystemStatus.js`. Every `/reports/*` endpoint in `backend/routers/test.py` (6 entries) falls into `'Other'` on the System Status page. Because the prefix is not new, no cycle's STEP 6 check will ever flag it.

**Where in the routine:**
STEP 6 — Advisory: Endpoint Coverage Drift Check (`categorizeEndpoint()` follow-up)

**Root cause:**
process gap

**Blast radius analysis:**
- What would have propagated: the System Status page keeps grouping Reports endpoints under "Other", and the group grows as Reports gains routes (2 more this cycle).
- When it would have surfaced: never — silent failure (cosmetic grouping only; endpoint tests still run)
- Recovery cost if uncaught: low (single file fix)

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `src/pages/SystemStatus.js`
  - Section: `categorizeEndpoint()`
  - Change required: Add a `/reports` case, returning the existing `'Analytics'` group or a new `'Reports'` group, chosen by the frontend owner, together with a Playwright assertion on the System Status grouping. The file is application source and outside this routine's write scope.
  - Owner: Head of Engineering
  - Target: file via `/backlog-add` before `plan release v9.12`

---

## Recurrence Escalations

None.

**Recurrence Notes (§3.7 row-completeness reconciliation of the v9.10 Outstanding deferred patches table):**
1. **`scan_backlog_gate_conditions.py`, treat `Gate criteria: None`/`N/A` as ungated.** Re-checked against the current script: no `None`/`N/A` handling is present, and `BLG-GOV-373` is still open. **Carried, 2nd cycle** (see table below). Not escalated: it is a script change with no `prompt_change_log.md` vehicle, and its named target ("next `groom backlog`") is this closure's own STEP 12. The v9.10 groom ran in the same session that filed the patch.
2. **Refresh pre-clearance ACs when a gate clears.** **Folded into `ESC-CLOSE-20261007-01`**: `release_planning_prompt.md` v2.60, §1.3a bound 5. ACs are listed in the clearance note and restated in the slice, not edited. That ruling covers gates cleared by Release Planning's date-lapse procedure. This cycle's Release Planning Friction Item 3 is a **recurrence on a different branch**: gates removed by a Product Owner decision outside Release Planning (`BLG-FEAT-59/60/63`, `BLG-FE-84`, `BLG-SPEC-174`, 2026-10-05). The prior action was resolved for its scope, so §3.7's automatic-escalation trigger (recurrence *with an open* prior action) does not fire. Filed as a new deferred patch below.
3. **Scheduled SLA-breach reminder.** **Applied**: `.github/workflows/escalation-sla-reminder.yml`, commit `82633f58` (AUD-2026-10-08-003). Phase 3 Friction Item 2 found that its input was not populated for execution escalations. That gap is closed this run by `execution_prompt.md` v3.85 (LL-v9.11-P3-02).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | ESCALATION HANDLING SUBROUTINE; §7 | Mirror each `ESC-EXEC-*` record into `.claude_current_state.json.open_escalations` and commit it to `main`. Update its `disposition` on resolution. §7 names the write (LL-v9.11-P3-02, Phase 3 Friction Item 2) | v3.84 → v3.85 | Yes |
| `claude/system/execution_prompt.md` | §9.2 | Read-back item (5): after an EPIC DoQ sign-off write, `qa_signed_off` = `true` and EPIC `status` = `done`, in the same commit as `qa_evidence_EPIC-xx.md` (LL-v9.11-P3-03, Phase 3 Friction Item 3) | v3.84 → v3.85 (same bump) | Yes |
| `claude/system/delivery_verification_prompt.md` | STEP 2.1 | `Pass_with_deviation` found-defect severity: a pre-existing defect the story found takes its filed backlog priority, and a P1/P2 takes §7's PO + DoQ path (LL-v9.11-P4-01, Phase 4 Friction Item 1) | v3.14 → v3.15 | Yes |
| `claude/system/post_ship_closure.md` | STEP 0 — Audit Cadence Check | Modulo condition suppressed when `last_audit_cycle_count` equals `completed_cycle_count` (LL-v9.11-Closure-01, Friction Item 1 above) | v2.39 → v2.40 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §8, §9, §10 source-prompt headers; §14 | Versions synced for the three prompt bumps above; Change Log row added | v4.232 → v4.233 | Yes |

Size budget (`shared_standards.md` §11): `execution_prompt.md` (~134,000 bytes) and `post_ship_closure.md` (~70,900 bytes) both exceed 68,500. Their split items are already open (`BLG-GOV-379`, `BLG-GOV-381`), so no new item was filed. Each addition is kept to the minimum process text.

---

## New files created this run

None. This record, `closure_record.md` and `closure_state.json` are the routine's standard outputs.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Cycles carried |
|------|---------|----------------|-------|--------|-----------------|
| `scripts/scan_backlog_gate_conditions.py` | Gate parsing | Treat a literal `Gate criteria: None`/`N/A` as ungated (v9.10 Release Planning Friction Item 1). Vehicle: `BLG-GOV-373` | Head of Specs Team / Head of Engineering | `BLG-GOV-373` / this closure's STEP 12 `groom backlog` review | 2nd cycle |
| `scripts/scan_backlog_gate_conditions.py`; `claude/system/release_planning_prompt.md` §1.3a | "Gating item shipped — verify" output | Add a list of gated items whose gate names only `BLG-*` items no longer in the active backlog, mirroring the date-lapsed list, and read it in §1.3a's pool-fixing step (v9.11 Release Planning Friction Item 1: 26 such items, at least 2 genuinely ready) | Head of Specs Team / Head of Engineering | File via `/backlog-add` before `plan release v9.12` | 1st cycle (new) |
| `claude/system/release_planning_prompt.md` | §1.3a / STEP 3.9 | Acquire `claude/backlog/.lock` before the first §1.3a in-place gate edit, or move those edits after STEP 3.9. A design choice between the two options is required (v9.11 Release Planning Friction Item 2) | Head of Specs Team | 2026-10-20 | 1st cycle (new) |
| `claude/system/release_planning_prompt.md` (or `backlog_management_prompt.md`) | §1.3a bound 5 | Extend the "list affected ACs and restate in the slice" rule to gates removed by a Product Owner decision outside Release Planning, not only date-lapsed gates (v9.11 Release Planning Friction Item 3; recurrence of the v9.10 item on a new branch). Engine ownership needs a Head of Specs Team call | Head of Specs Team | Next `release_planning_prompt.md` revision; no later than `plan release v9.12` | 1st cycle (new) |
| `CLAUDE.md` | §8 (new step 2c) | After any cross-EPIC merge resolution: diff `execution_state.json` EPIC/story records and `backlog.md` item bodies against both parents, and confirm that no field moved backwards and every item body matches one parent (v9.11 Phase 3 Friction Item 1). `CLAUDE.md` is outside this routine's write scope | Head of Specs Team | `BLG-GOV-385` (P2), next sprint that seats it | 1st cycle (new) |
| `src/pages/SystemStatus.js` | `categorizeEndpoint()` | Add a `/reports` case plus a Playwright grouping assertion (Friction Item 2 above) | Head of Engineering | File via `/backlog-add` before `plan release v9.12` | 1st cycle (new) |

---

## Escalations

None. Every deferred item has a named file, owner and target.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `next_release` still reads `v9.11`, the release just shipped, and roadmap §1 "Next planned release" is `[TBD]`. | Run `run roadmap --reason scheduled` (or make a scoping decision) before `plan release v9.12`, despite the odd cycle count. | Roadmap |
| 2 | `BLG-BE-162` (journal summary HTTP 422, P1) was accepted at verification on condition that it stays P1 and is seated in v9.12. | The next rebalance and `plan release v9.12` must seat it. Re-prioritising below P1 needs a new Product Owner decision. | Roadmap / Release Planning |
| 3 | A clean `git merge` resolution reset an EPIC record and spliced two backlog item bodies (`3237cb5e`). `BLG-GOV-385` is still open. | Until it lands, after every CLAUDE.md §8 merge resolution, diff `execution_state.json` EPIC/story records and `backlog.md` item bodies against both parents before committing. | All |
