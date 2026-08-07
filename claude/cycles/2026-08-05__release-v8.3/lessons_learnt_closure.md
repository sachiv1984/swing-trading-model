Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-07
Cycle: 2026-08-05__release-v8.3

# Lessons Learnt — Post-Ship Closure — v8.3

Feature / Trigger: Ship v8.3's backlog-driven, debt-clearance scope — SI-05 weekly digest pipeline root-cause and fix (with delivery-failure alerting) leading two P1 operational items, backend engineering hardening, frontend/design-system debt, QA/spec debt, a governance-process cluster, and the Monthly P&L format retrospective.
Run: 2026-08-05__release-v8.3
Reviewed by: PMO Lead
Date filed: 2026-08-07
Prior cycle checked: 2026-08-04__release-v8.2

---

## What worked well

- All three source lessons-learnt records (`lessons_learnt.md`, `lessons_learnt_cycle.md` Phase 3 + Phase 4) again arrived with every action item pre-classified with a disposition (action-now / defer / escalate), and Phase 3's own Recurrence Escalation for the backlog write-scope tension was already correctly self-identified and routed per `lessons_learnt_prompt.md §6.4` by the Sprint Execution engine itself — this closure did not need to discover the recurrence independently, only consolidate it.
- Zero deviations, zero returned items, zero test scenario gaps, zero delegated/blocked items, and a fully clean Director of Quality / Product Owner sign-off pairing meant STEP 3 (Backlog Reconciliation), STEP 5 (Deviation Compliance Check), and STEP 7 (Specs Index Review) all required no exception handling this cycle — every one of the 27 shipped items reconciled cleanly against `execution_state.json` on the first pass.
- The STEP 6 Endpoint Coverage Drift Check's path-parameter normalisation step correctly surfaced the same-composition 19-endpoint gap already known from `v8.1`/`v8.2` closures, but this time found no existing open general tracker to reference (`BLG-OPS-111`, the prior general tracker, was retired at `2026-08-03__release-v8.1` in favour of this very script-derived reconciliation mechanism, per `AUD-2026-08-03-003`) — correctly triggering a fresh backlog filing (`BLG-OPS-133`) rather than silently skipping the advisory because no tracker existed to update.

---

## Friction Log

### Friction Item 1

**Classification:** Type B — Semantic Mismatch (two backlog items now cover overlapping problem space under different identities)

**Recurrence:** No — first observed this cycle; the underlying condition (`BLG-OPS-111` retirement) was created at `2026-08-03__release-v8.1` but its consequence (a stale sibling item, `BLG-OPS-13`, left unreconciled) was not previously flagged as a friction item.

**What happened:** STEP 6's endpoint coverage drift check found no open general tracking item for the current 19-endpoint gap (`BLG-OPS-111` was retired at `v8.1` closure per `AUD-2026-08-03-003`, in favour of this script-derived check), so a new item, `BLG-OPS-133`, was correctly filed per the routine's own instruction. However, `claude/backlog/backlog.md` already contains a separate, still-open item, `BLG-OPS-13` ("Add new v2.8/v2.9/v3.0/v3.4/v3.9/v4.6 endpoints to `api_performance_baseline.md` re-run"), whose own endpoint list predates and does not overlap with the current 19-item gap — most of its named routes (`/ticker-universe`, `/trade-plans/*`, `/screener/*`) do not even appear in the current `openapi.yaml` gap scan, suggesting its content may already be substantially stale or resolved. `v8.2`'s own closure lessons already deferred a reconciliation of `BLG-OPS-13`'s body (Outstanding deferred patch, target "next `groom backlog` or endpoint performance baseline review") without acting on it, and this cycle's filing of `BLG-OPS-133` now creates a second, undifferentiated tracking item in the same problem space without a check confirming the two do not need consolidating.

**Where in the routine:** STEP 6 — Operational Documents Reconciliation, Endpoint Coverage Drift Check.

**Root cause:** Process gap — the STEP 6 "check for an existing open tracking item first" instruction greps for the *current* gap's own class of finding but has no step confirming an *unrelated, stale* item in the same namespace/topic isn't sitting alongside it unreconciled. `BLG-OPS-13` was not caught because its own endpoint list does not textually overlap with the current gap list, so a naive existing-item search correctly found no exact match — the gap is structural (no cross-item topic-consolidation check), not a search-string miss.

**Blast radius analysis:**
- What would have propagated: `BLG-OPS-13` and `BLG-OPS-133` both remain open indefinitely, each implying a different (stale vs current) endpoint list, until a human happens to read both side-by-side at `groom backlog`.
- When it would have surfaced: next `groom backlog`'s Governance Prompt Duplicate Cross-Check-style pass, if it is ever extended to non-governance namespaces — currently that check is scoped to `BLG-GOV-*` only.
- Recovery cost if uncaught: low (single-item consolidation or retirement), but compounds each cycle both items remain independently open.

**Process patch:**
→ Deferred patch (cannot apply this run):
  - File: `claude/backlog/backlog.md` (`BLG-OPS-13` entry body)
  - Section: `BLG-OPS-13` and `BLG-OPS-133` entries
  - Change required: Reconcile `BLG-OPS-13`'s endpoint list against the current live `openapi.yaml`/`api_performance_baseline.md` diff — retire or merge into `BLG-OPS-133` if fully superseded, or correct its list if a genuine residual subset remains.
  - Owner: Infrastructure & Operations Owner
  - Target: Next `groom backlog` run

---

## Recurrence Escalations

**Recurrence Escalation 1 (carried from Sprint Execution, consolidated here per this engine's meta-consumer role):** Per `lessons_learnt_cycle.md` Phase 3, the backlog write-scope tension (mid-sprint `backlog.md` additions for genuinely out-of-scope findings, outside `execution_prompt.md`'s formal STEP 5.2 write-scope) has now recurred across at minimum `v8.1`, `v8.2`, and `v8.3` — 3 consecutive cycles, each time deferred to "next `execution_prompt.md` §7 revision" without that revision landing (confirmed absent from `claude/system/prompt_change_log.md` across this span). Per `lessons_learnt_prompt.md §3.7`, a deferred patch carried 2+ cycles without a `prompt_change_log.md` entry is an automatic recurrence escalation regardless of this cycle's own friction-item status. Already escalated to Head of Specs Team by the Sprint Execution engine within `lessons_learnt_cycle.md` Phase 3 (§6.4 path) — not re-escalated as a duplicate, only consolidated into this closure-level record per §3.5's cross-cycle pattern detection remit.

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| `execution_prompt.md` §7 has no documented, sanctioned write path for genuine out-of-scope findings surfaced mid-sprint — 3 consecutive cycles operating on informal precedent instead (`v8.1`, `v8.2`, `v8.3`) | `2026-08-03__release-v8.1` (named as a deferred patch at that cycle's own closure) | Formally sanction (a) or explicitly reaffirm-and-close (b) the informal precedent in `execution_prompt.md` §7 | Head of Specs Team |

---

## Process improvements actioned this run

None applied this run. All identified action items were either already resolved during Phase 3 execution (the DoQ sign-off staleness lint self-referential false positive, commit `428782d6` — see `lessons_learnt_cycle.md` Phase 3), deferred pending their named owner's next relevant session, or already escalated (see above) — none required or permitted an immediate template/prompt patch within this engine's own write scope this run.

---

## New files created this run

- `claude/cycles/2026-08-05__release-v8.3/closure_state.json`
- `claude/cycles/2026-08-05__release-v8.3/lessons_learnt_closure.md` (this file)
- `claude/cycles/2026-08-05__release-v8.3/closure_record.md` (STEP 9, filed immediately after this record per the documented sequencing note)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/backlog/backlog.md` (`BLG-OPS-13` entry body) | Endpoint list | Reconcile against the current live gap, or retire/merge into `BLG-OPS-133` — see Friction Item 1 | Infrastructure & Operations Owner | Next `groom backlog` |
| `docs/specs/frontend/design_system.md` / `claude/system/execution_prompt.md` | Frontend-testing-gate | Close the environment-parity gap between sandboxed pre-merge review and real-CI Playwright execution for focus/interaction-timing ACs specifically (surfaced by ST-11's `SC-CR-11` real-CI catch) — see `lessons_learnt_cycle.md` Phase 3 | Base44 Frontend Prompt Owner | Next `design_system.md`/`execution_prompt.md` revision touching the frontend-testing-gate |
| CI/workflow tooling (new script or checklist) | — | No scripted way to distinguish infra-outage CI failures (e.g. the 2026-08-06 GitHub Actions outage) from real ones, and no safe automated retry path for a stuck rerun attempt — see `lessons_learnt_cycle.md` Phase 3 | Head of Engineering | Next CI/workflow-tooling pass |
| `.github/workflows/*.yml` (workflow-authoring guidance) | `pipefail`/`tee` exit-code capture | Carried unresolved from `v8.2` closure — GitHub Actions `run:` steps default to `bash -e {0}` with no `pipefail` unless `shell: bash` is declared, silently defeating `cmd \| tee file; echo $?` patterns. No new instance this cycle (confirmed via `lessons_learnt_cycle.md` Phase 3 recurrence note), but still unresolved — 2nd consecutive cycle carried | Head of Engineering | Next CI/workflow-authoring pass |
| `claude/system/execution_prompt.md` | §3.1.B / §5.1 | Carried unresolved from `v8.2` closure — define an explicit sub-path for in-session credential provisioning. No new instance this cycle (`delegated_items` empty). | Head of Specs Team | Next `execution_prompt.md` revision touching §3.1.B or §5.1 |
| `claude/system/CLAUDE.md` §8 (Cross-EPIC Merge Conflict Resolution) | Named check | Carried unresolved from `v8.2` closure — add an "identical-text masks differing semantics" check. This cycle DID exercise a cross-EPIC merge (`8a62cfc1`, EPIC-06/ST-27 merging EPIC-03+EPIC-04 content into EPIC-06) but no lessons-learnt record confirms whether this specific check-gap was tested by it — worth a targeted look at that merge commit before next revision | Head of Specs Team | Next `sprint_planning_prompt.md`/`CLAUDE.md` §8 revision cycle |
| `claude/backlog/backlog.md` (`BLG-GOV-286` — already filed) | — | Pull `BLG-GOV-286` (canonical, scripted gate-detection procedure covering 4 observed field-name variants) into a sprint — see `lessons_learnt.md` (Release Planning), 4th consecutive self-caught scan miss this cycle (`BLG-GOV-74`) | Head of Specs Team / Sprint Planning | Next sprint planning session with capacity available |

---

## Escalations

None beyond Recurrence Escalation 1 above (already routed to Head of Specs Team in that section — not duplicated here).

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-OPS-13` and `BLG-OPS-133` are now both open and cover overlapping endpoint-coverage-drift problem space under different identities, with no cross-item consolidation check outside the `BLG-GOV-*`-scoped Governance Prompt Duplicate Cross-Check. | The next `groom backlog` run should reconcile or retire `BLG-OPS-13` against the current gap — see Friction Item 1. | Backlog Management (groom backlog) |
| 2 | The `execution_prompt.md` §7 backlog write-scope escalation is now 3 consecutive cycles unresolved (`v8.1`→`v8.2`→`v8.3`) without a `prompt_change_log.md` entry. | Per Sprint Execution's own escalation, the next `run sprint` invocation without resolution should be treated as a standing process gap requiring PMO Lead attention regardless of this escalation's own outcome. | Sprint Execution / PMO Lead |
| 3 | A genuine cross-EPIC merge conflict occurred this cycle (EPIC-06/ST-27, merging EPIC-03+EPIC-04 content) — the first real exercise since the "identical-text masks differing semantics" `CLAUDE.md` §8 gap was named at `v8.1` closure, but no lessons-learnt record confirms whether that specific failure mode was or wasn't present in this merge. | Worth a targeted retrospective look at commit `8a62cfc1` before the next `CLAUDE.md` §8 revision, rather than continuing to carry the deferred patch on theoretical grounds alone. | Post-Ship Closure / Head of Specs Team |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-08-05__release-v8.3",
  "phase": "Post-Ship",
  "filed_utc": "2026-08-07T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 7,
  "escalation_count": 1,
  "overdue_patches": 0,
  "status": "Complete"
}
```
