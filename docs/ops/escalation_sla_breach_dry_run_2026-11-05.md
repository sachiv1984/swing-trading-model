**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-11-05
**Source:** ST-43 (BLG-GOV-193, EPIC-07, cycle `2026-11-03__release-v9.15`)

---

# Escalation SLA-Breach Path — Dry Run

## Purpose

The `BLOCKED_SLA_BREACH` notice (`shared_standards.md` §4 SLA Breach Rule and §16.4) and Release Planning's `SLA_BREACH_CARRIED` halt (`release_planning_prompt.md` STEP -1.6) had never been exercised end to end (BLG-GOV-193). This dry run exercises both against a synthetic escalation backdated past its 72-hour SLA, on a scratch copy of the state files. The live `.claude_current_state.json` is never written.

## Method

`scripts/escalation_sla_dry_run.py` (run with `--now 2026-11-05T15:00:00Z`):

1. Copies `.claude_current_state.json` and `claude/cycles/2026-11-03__release-v9.15/execution_escalations.md` into a temporary directory.
2. Adds five synthetic escalations to the copy's `open_escalations`. Two are under test, both `Open`, raised 80h earlier with `sla_due_utc` 72h after raising (8h past due): `ESC-EXEC-DRYRUN-01` (`blocks_execution: true`) and `-02` (`false`). Three are controls: `-03` `Deferred` past due, `-04` `Resolved` past due, and `-05` `Open` but 10h old and inside its SLA.
3. Evaluates, on the copy, the trigger predicate each rule states, and applies §16.4's writes (notice appended to the copy's escalations file, `blocked_sla_breached: true` in the copy's state file).
4. Runs the embedded Python of `.github/workflows/escalation-sla-reminder.yml` verbatim in the scratch directory, with `gh` replaced by a stub that records each call.

The prompt rules are instructions an engine follows, so step 3 checks what each rule's written predicate selects. Step 4 is the only mechanical part, and it runs as written. `tests/test_escalation_sla_dry_run.py` re-runs the dry run in CI Pytest and checks the results below, including that the live state file is byte-identical afterwards.

## Results

| Check | Rule text applied | Fires for | Outcome |
|-------|-------------------|-----------|---------|
| `BLOCKED_SLA_BREACH` (gate `SLA_BREACH`) | §4 / §16.4: open ≥72h without resolution, any trigger type | DRYRUN-01, -02, -03 | **Fires.** Notice appended to the scratch `execution_escalations.md` for each; scratch `blocked_sla_breached` set `true`; the engine halts |
| Non-blocking advisory | `execution_prompt.md` STEP -1.2A / §16.4.1: `Open` and `sla_due_utc` < now | DRYRUN-01, -02 | Fires (advisory, no halt) |
| `SLA_BREACH_CARRIED` | `release_planning_prompt.md` STEP -1.6: `Open` and now ≥ `sla_due_utc` | DRYRUN-01, -02 | **Fires.** Release Planning halts |
| Daily reminder workflow | non-terminal (not `Resolved`/`Closed`/`Withdrawn`) and `sla_due_utc` < now | DRYRUN-01, -02, -03 | Fires: `gh issue create` with label `escalation-sla`; with an existing issue, `gh issue comment` instead |

Controls: `-04` (`Resolved`) and `-05` (inside its SLA) are selected by no check. Baseline (live state, no synthetic records): no check fires, and the workflow prints "No open escalation past SLA." This matches the live state: all 46 `open_escalations` entries are `Resolved`. The one long-running item, `ESC-EXEC-20260910-01`, is kept under `deferred_escalations`, which none of the four checks reads. That is by design, since its re-check is driven by its own `deferred_trigger`.

Both checks named in the acceptance criteria fire for a synthetic `Open` escalation past its 72h SLA.

## Defects found

| ID | Defect | Filed as |
|----|--------|----------|
| 1 | §4/§16.4 halt any escalation open ≥72h "regardless of trigger type", but §16.4.1 says a `blocks_execution: false` escalation never triggers that halt. DRYRUN-02 halts under one reading and not the other. | `BLG-GOV-410` (P3) |
| 2 | The checks use different disposition sets. STEP -1.2A and STEP -1.6 count only `Open`; the workflow also counts `Deferred` and `Accepted Risk`. DRYRUN-03 (`Deferred`) is reported by the workflow but by neither engine check. §4 names no set. | `BLG-GOV-411` (P3) |

## Observations (not defects)

- §4/§16.4 measure 72h from `raised_utc`, whatever the type, while STEP -1.2A and STEP -1.6 measure from `sla_due_utc` (24h for a Lifecycle escalation). So a Lifecycle escalation 30h old halts Release Planning but not Sprint Execution. §4 states that the 72-hour clock overrides the type SLA for the engine halt only, so the difference is consistent with the written rules.
- The workflow's run logs for the last five daily runs (2026-10-31 to 2026-11-04, all `success`) were not retrievable, but its behaviour on the live state ("No open escalation past SLA") matches the absence of any `escalation-sla` issue.
