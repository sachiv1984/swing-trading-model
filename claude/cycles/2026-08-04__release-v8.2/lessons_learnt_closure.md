Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-05
Cycle: 2026-08-04__release-v8.2

# Lessons Learnt — Post-Ship Closure — v8.2

Feature / Trigger: Ship v8.2's curated full-capacity scope — five ready user-facing/UX improvements leading the release, staging/production security hardening, an 11-item governance-process integrity cluster, CI/operations hardening, and QA/spec debt cleanup.
Run: 2026-08-04__release-v8.2
Reviewed by: PMO Lead
Date filed: 2026-08-05
Prior cycle checked: 2026-08-03__release-v8.1

---

## What worked well

- The STEP 6 Endpoint Coverage Drift Check's "script-derived tracking-item handoff" mechanism (AUD-2026-08-03-003) again produced a fresh, copy-paste-ready re-derived 19-endpoint gap list rather than requiring a manual re-diff, and confirmed the gap is unchanged in composition since `v8.1`'s closure — a clean second live exercise of the mechanism.
- All three source lessons-learnt records (`lessons_learnt.md`, `lessons_learnt_cycle.md` Phase 3 + Phase 4) again arrived with every action item pre-classified with a disposition (`action-now`/`defer`), and Phase 4's own cross-check confirmed both of its two carried-forward deferred patches from `v8.1` (STEP -1.3A PR-recovery write target; `completed_items` cross-EPIC reconciliation) were independently verified landed in the relevant prompt files before being marked resolved — not assumed resolved on faith.
- Zero deviations, zero returned items, zero test scenario gaps, and a fully clean Director of Quality / Product Owner sign-off pairing meant STEP 5 (Deviation Compliance Check) and STEP 7 (Specs Index Review) both required no writes this cycle — confirmed via direct read rather than skipped.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift (a documented carry-forward action was not corrected at its own named trigger point)

**Recurrence:** Yes — first flagged at `2026-08-03__release-v8.1`'s Release Planning lessons learnt (Carry-Forward Item 3: "not corrected by that cycle's post-ship closure").

**What happened:** `.claude_current_state.json.prior_cycle` still read `2026-07-21__release-v7.7` at this closure's STEP 0 — four releases stale (correct value at this point in the chain: `2026-08-03__release-v8.1`). `v8.1`'s own lessons learnt named this exact gap and explicitly assigned its correction to "the next time [Post-Ship Closure] runs" (i.e., this run), but no step in `post_ship_closure.md` STEP 10 lists `prior_cycle` among the fields it writes, so the field was silently skipped again at `v8.1`'s own closure.

**Where in the routine:** STEP 10 — Global State Update.

**Root cause:** Template omission — STEP 10's field list never included `prior_cycle`, so a routine, faithful application of the STEP 10 checklist does not touch it, regardless of how stale it becomes.

**Blast radius analysis:**
- What would have propagated: any future routine reading `prior_cycle` for cross-cycle comparison (e.g. a recurrence check, a "cycles since X" calculation) would silently use a four-cycle-old value with no error raised.
- When it would have surfaced: the next time a governed routine actually depended on `prior_cycle` for a correctness-sensitive calculation, rather than as an informational field — currently no engine reads it for a hard gate, so the failure mode remains silent.
- Recovery cost if uncaught: low (single field correction), but the staleness compounds by one release every cycle it is missed.

**Process patch:**
→ Immediate patch applied this run:
  - File: `.claude_current_state.json`
  - Section: `prior_cycle` field
  - Change: Corrected `2026-07-21__release-v7.7` → `2026-08-03__release-v8.1` at STEP 10 of this run.
  - Version: N/A (state data field, not a versioned prompt/template)
  - Confirmed by: PMO Lead
  - Prompt change log entry: Not applicable (state correction, not a prompt/template change)

This closes the immediate gap operationally but does not add a standing instruction to `post_ship_closure.md` STEP 10 — see Outstanding deferred patches below for the structural fix (a step that does not name the field it must maintain will drift again the next time a cycle boundary is missed for any reason).

---

## Recurrence Escalations

**Recurrence Escalation 1:** The Release Planning canonical gate-detection scan procedure patch (`release_planning_prompt.md` ungated-candidate scope-selection scan) has now been deferred at three consecutive Post-Ship Closures without a `prompt_change_log.md` entry: filed `2026-07-31__release-v8.0` closure (as a Recurrence Escalation from that cycle's own Release Planning lessons learnt), re-deferred `2026-08-03__release-v8.1` closure ("2nd consecutive"), and `lessons_learnt.md` this cycle self-reports a 3rd consecutive self-caught scan miss (`BLG-OPS-48`) and names this as crossing its own previously-stated mandatory-action-now threshold. Per this prompt's own §3.7 cross-cycle rule ("carried forward without a prompt_change_log entry for two or more cycles" = automatic recurrence escalation), this is now formally escalated to Head of Specs Team. **This is the first action recommended for the next session with `claude/backlog/backlog.md` write authority** (`groom backlog` or `run roadmap`) — file the `BLG-GOV-*` canonical, scripted gate-detection procedure item before any other backlog action that session.

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| Release Planning ungated-candidate scan has no canonical, mechanically-reliable field-detection procedure — 3 consecutive self-caught misses (`v8.0`, `v8.1`, `v8.2`) | `2026-07-31__release-v8.0` closure | File `BLG-GOV-*` canonical scripted gate-detection procedure item (deferred at `v8.0` and `v8.1` closures, still unfiled) | Head of Specs Team |

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `.claude_current_state.json` | `prior_cycle` field | Corrected stale `2026-07-21__release-v7.7` → `2026-08-03__release-v8.1` (see Friction Item 1) | N/A (state field) | Not applicable |

---

## New files created this run

- `claude/cycles/2026-08-04__release-v8.2/closure_state.json`
- `claude/cycles/2026-08-04__release-v8.2/lessons_learnt_closure.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/post_ship_closure.md` | STEP 10 — Global State Update | Add `prior_cycle` to the named field list STEP 10 maintains, so its correction is not dependent on a lessons-learnt carry-forward catching the drift each time (see Friction Item 1). Also revisit STEP 5.1's own cadence-field write instruction, deferred at `v8.1` closure and still not codified in the prompt text (operationally handled again this run via direct state write, per the same workaround `v8.1`'s closure used). | Head of Specs Team | Next `post_ship_closure.md` revision cycle |
| `claude/backlog/backlog.md` (`BLG-OPS-13` entry body) | Endpoint list | Reconcile against the current live gap — unchanged from `v8.1`'s closure (same 19 endpoints, same composition): `GET /analytics/market-correlation`, `GET /analytics/metrics`, `GET /analytics/tag-performance`, `GET /portfolio/pre-entry-validation`, `GET /positions/analyze`, `GET /positions/grace-period-alerts`, `GET /positions/tags`, `GET /positions/{id}`, `GET /positions/{id}/stop-trail`, `PATCH /notifications/preferences`, `PATCH /watchlist/{id}`, `POST /ai/check-daily-cost`, `POST /alerts/rules`, `POST /positions/nightly-stop-update`, `POST /positions/risk-off-alerts`, `POST /positions/{id}/refresh-state`, `POST /settings`, `POST /signals/rebalance-exit`, `POST /test/endpoints`. `BLG-OPS-13`'s own list (last updated 2026-05-31) still names the entirely different, stale v2.8–v4.6 set — 2nd consecutive cycle this delta has been recorded without action. Outside Post-Ship Closure's backlog write scope (mark-shipped-complete / add-missing-Phase-4-items only). | Infrastructure & Operations Owner | Next `groom backlog` or endpoint performance baseline review |
| `claude/system/roadmap_prompt.md` or `release_planning_prompt.md` | Ungated-candidate scope-selection scan | File `BLG-GOV-*`: canonical, scripted gate-detection procedure (full-block scan, canonical field-name list including gate conditions embedded in `Provisional-Target` text) — see Recurrence Escalation 1. **Action-now priority for the next session with backlog write authority.** | PMO Lead / Head of Specs Team | Next `groom backlog` or `run roadmap` session |
| `claude/backlog/backlog.md` (`BLG-OPS-48` entry body) | `Provisional-Target` field | Collapse duplicate `**Provisional-Target:**` field into a single line; add explicit `**Gate criteria:**` field, so this specific item stops being a repeat scan-miss source (2 of 3 recorded misses trace to this one item's data quality). | Infrastructure & Operations Owner / Head of Specs Team | Next session with `backlog.md` content-edit authority |
| `claude/system/execution_prompt.md` | §3.1.B / §5.1 | Define an explicit sub-path for in-session credential provisioning (user supplies a credential mid-session rather than the standard park-and-wait delegation flow), per this cycle's EPIC-02 (ST-06/ST-07) deviation. | Head of Specs Team | Next `execution_prompt.md` revision touching §3.1.B or §5.1 |
| `.github/workflows/*.yml` (workflow-authoring guidance) | New CI lint or documented checklist entry | GitHub Actions `run:` steps default to `bash -e {0}` with no `pipefail` unless `shell: bash` is declared — silently defeats `cmd \| tee file; echo $?` exit-code capture. Consider a repo-wide grep-based CI lint or a workflow-authoring checklist entry. | Head of Engineering | Next CI/workflow-authoring pass |
| `claude/system/execution_prompt.md` | §7 — Write Scope Restriction | Formally sanction mid-sprint `backlog.md` additions for genuinely out-of-scope discoveries (currently an informal, tolerated precedent per `backlog.md`'s own header history, not a documented write path) — 3 items filed this way again this cycle (`BLG-OPS-129`, `BLG-OPS-130`, `BLG-OPS-131`). | Head of Specs Team | Next `execution_prompt.md` §7 revision |
| `claude/system/CLAUDE.md` §8 (Cross-EPIC Merge Conflict Resolution) | Named check | Add an explicit "identical-text masks differing semantics" check (two branches independently bumping a shared prompt file to the same literal version number for different changes is not flagged by git as conflicting). Deferred at `v8.1` closure; not exercised this cycle (no cross-EPIC merge conflicts occurred) and still not codified. | Head of Specs Team | Next `sprint_planning_prompt.md` / `CLAUDE.md` §8 revision cycle |

---

## Escalations

None beyond Recurrence Escalation 1 above (already routed to Head of Specs Team in that section per §3.7's recurrence-escalation path — not duplicated here).

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The Release Planning ungated-candidate scan gap has now crossed its own named mandatory-action-now threshold (3 consecutive self-caught misses, `v8.0`–`v8.2`) without the corresponding `BLG-GOV-*` item ever being filed, because no engine in the chain (Release Planning → Post-Ship Closure) has `backlog.md` write scope broad enough to file a brand-new process-patch item. | The next `groom backlog` or `run roadmap` session must file this item as its first action, not as one item among many — see Recurrence Escalation 1. | Roadmap / groom backlog |
| 2 | `BLG-FEAT-73`/`BLG-FEAT-74` are now at 3 of 4 consecutive Option (a) perennial-return dispositions (carried from `lessons_learnt.md` this cycle). | If `v8.3` also defers both under an unchanged rationale, the STEP 1.4a.1 mandatory sunset trigger fires and the next Release Planning session must force Option (b) or document a materially new gate-clearance path. | Release Planning |
| 3 | `post_ship_closure.md` STEP 10's field list has now been shown twice to omit fields a prior lessons-learnt cycle explicitly asked it to maintain (`v8.1`: STEP 5.1 cadence fields, handled operationally not textually; `v8.2`, this cycle: `prior_cycle`, same pattern). | The deferred STEP 10 prompt patch (see Outstanding deferred patches) should be treated as higher priority than a routine backlog item — it is the second, not first, instance of this exact failure mode. | Post-Ship Closure |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-08-04__release-v8.2",
  "phase": "Post-Ship",
  "filed_utc": "2026-08-05T08:30:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 7,
  "escalation_count": 1,
  "overdue_patches": 1,
  "status": "Complete"
}
```
