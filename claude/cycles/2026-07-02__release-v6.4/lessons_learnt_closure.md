Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-02__release-v6.4
Release: v6.4
Last Updated: 2026-07-02
Authority: Post-Ship Closure Engine v2.15

---

# Lessons Learnt — Closure Summary: v6.4

## Classification Summary

| Count | Category |
|-------|----------|
| 2 | Immediate (applied in this post-ship session) |
| 5 | Deferred (carry to v6.5 as Outstanding Actions) |
| 1 | Escalated (decision required — Head of Specs Team) |
| 3 | Confirmed already satisfied — no action required |
| 1 | Validated pattern confirmed (LP-01 — FI-P3-01/FI-P3-02/FI-P4-01 all closed via ST-06 as planned) |

---

## Action Classification Detail

### Immediate Actions Applied (2)

| ID | Source | Document | Change | Version |
|----|--------|----------|--------|---------|
| IM-01 | v6.3 Phase 4 friction 1 (DF-04) | `claude/system/templates/qa_evidence_template.md` | Signer format requirement made explicit in the Standard Sign-Off Block (exact compliant `Signed off by:` string set) | v1.5→v1.6 |
| IM-02 | v6.3 Phase 3 friction (DF-02) | `claude/system/execution_prompt.md` | `qa_signed_off` elevated from advisory note to hard STEP 4 merge-gate table row | v3.49→v3.50 |

Both were deferred at v6.3, targeted at v6.4, and had **not** been applied by v6.4 sprint execution or planning — confirmed via `prompt_change_log.md` cross-check (§3.7 Cross-Cycle Recurrence Check). Applying them now rather than deferring a second time, per the non-deferrable immediate-action rule.

---

### Confirmed Already Satisfied — No Action Required (3)

| ID | Source | Finding |
|----|--------|---------|
| DF-01 | v6.3 Phase 3 friction | `execution_prompt.md` step 10a already implements the deviations_filed atomic write (LL-v3.7-EX-01, applied 2026-05-18, predates the v6.3 request) — the v6.3 ask was effectively a restatement of an existing patch. |
| DF-05 | v6.3 Phase 4 friction | `execution_prompt.md` §5.3A already has a post-write verification step (AUD-2026-06-22-001, `grep -c "Sprint: <cycle_id>"`) confirming the System Status Report section exists immediately after write. |
| DF-06 | v6.3 Phase 4 friction | Confirmed applied in `sprint_backlog.md` this cycle — ST-08's note explicitly cites and applies the ≥5-AC Playwright scenario stub threshold (per `sprint_planning_notes.md` Outstanding Actions). |

DF-03 (v6.3 Phase 3 friction — "pre-halt checklist verifying deviations_filed/qa_signed_off before EPIC merge halt output") is treated as structurally redundant: the STEP 4 merge gate table already blocks the merge itself on `deviations_filed = true` (and now, per IM-02, on `qa_signed_off = true`) before the halt message can fire — a merge-gate failure and a halt cannot both occur for the same EPIC in the same pass. No separate pre-halt checklist is needed on top of the merge gate. Recorded here rather than as a deferred item.

---

### Deferred Items — carry to v6.5

| ID | Source | Summary | Owner | Target |
|----|--------|---------|-------|--------|
| DF-11 | Phase 3 friction 1 | STEP 4's "on session resume — merge gate state sync" sub-step has no branch check of its own; a fresh session resuming after an EPIC merge can land on any `exec/**` branch, and the merge-gate sync write can be orphaned on a stale branch. Add an explicit branch check mirroring STEP 5's branch-ordering gate. | Head of Specs Team | v6.5 |
| DF-12 | Phase 3 friction 2 | ST-07 commit split: a `git add` pathspec error caused an orphan-file deletion to land in a separate commit from the rest of the story's changes (both carried the correct tag, so governance_sync.yml was unaffected, but it is the kind of staging slip `/commit-check` exists to catch). Reinforce `/commit-check` to explicitly diff `git add`'s target list against the intended file set before committing multi-file governance changes. | Head of Specs Team | v6.5 |
| DF-13 | LP-02 monitoring | Skill-Silo rolling-3-cycle average was 53.2% (Alert) at the 2026-07-01 rebalance that pulled BLG-FEAT-54 forward into v6.4 alongside the 4 audit-remediation items; confirm at the next roadmap rebalance whether the bundling approach brought the rolling average back under the 40% ceiling. | PMO Lead | Next roadmap rebalance |
| DF-14 | LP-04 monitoring | Standing AI safety checklist proposal (originally raised v6.3 LP-04, carried as DF-09) remains un-actioned for a 2nd consecutive cycle — v6.4's AI-adjacent items (BLG-SEC-01/02) were again derived from the original ST-04 risk assessment rather than a standing checklist. Per the LP-04 escalation rule, if a 3rd consecutive release derives AI/security scope ad hoc, escalate from advisory to a scoped backlog item at v6.5 release planning. | PMO Lead | v6.5 release planning |
| DF-15 | Specs Index §31 TSG reconciliation | TSG-v60-01 (BLG-QA-61 — signals_scenarios.md review against ST-01 signal sizing model changes) is unresolved for a 3rd consecutive cycle (v6.2→v6.3→v6.4). Per the v6.3 note this now formally triggers the 2-cycle recurrence escalation. See Escalations below — this row is retained here only as the carry-forward record once a disposition is set. | Head of Specs Team | Immediate (see Escalations) |

---

### Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|--------------|--------|
| BLG-QA-61 / TSG-v60-01 (signals_scenarios.md review against ST-01 signal sizing model changes) | Recurrence — 3 consecutive cycles unresolved (v6.2, v6.3, v6.4) | Head of Specs Team | No document/prompt patch closes this — it requires a named disposition (resolve, reassign, or explicitly re-park with written rationale) within 72 hours of this closure, per the escalation format in `shared_standards.md`. Continuing to silently re-defer without a named decision is itself the governance gap. |

---

### Validated Patterns

**LP-01 CONFIRMED — carry-forward-by-AC folding pattern works:**
FI-P3-01, FI-P3-02, and FI-P4-01/DF-10 (each 2-cycle-carried, at or past the audit SLA escalation threshold) were folded into `BLG-GOV-152` (ST-06)'s concrete acceptance criteria at release planning rather than re-carried as free-floating notes. `execution_state.json` confirms all three closed within this sprint (ST-06 notes: "Resolves FI-P3-01 (2nd recurrence), FI-P3-02 and FI-P4-01/DF-10 ... now closed within-sprint per LP-01 monitoring item"). The release-planning decision to attach carry-forward items to a scheduled story's ACs — rather than a free-floating note — is validated as an effective anti-drop mechanism and should be the default pattern for future carry-forwards with 2+ cycles of age.

---

## Closure-Phase Observations

- **Specs Index reconciliation surfaced a real gap this cycle:** cross-referencing §31's TSG-v60-01 note against `backlog.md` (STEP 7 of this routine) is what caught the BLG-QA-61 3rd-cycle recurrence — this check would have been silently skipped if STEP 7's TSG reconciliation sub-step had been treated as a formality rather than an actual cross-check. No process patch needed; this is confirmation the existing STEP 7.3 sub-step is doing its job.
- **Endpoint coverage drift check (STEP 6) found exactly one gap** — `GET /strategy/benchmark/open-positions` (BLG-FEAT-54, ST-08) — filed as `BLG-OPS-83`, mirroring the identical pattern from v6.3 (BLG-OPS-82). This is now a 2-cycle-running pattern (a new Strategy Benchmark endpoint ships, its performance baseline registration is deferred to the following cycle) — not yet a recurrence problem, since each instance is closed within one cycle, but worth naming: it may be more efficient to register the perf baseline within the same sprint that ships the endpoint if the shipping EPIC has spare capacity, rather than always deferring to next-cycle Ops.
- **Deferred-patch audit (§3.7 Cross-Cycle Recurrence Check) found real drift:** of the 10 items in v6.3's Deferred Items table (DF-01–DF-10), only DF-10 had a confirmed `prompt_change_log.md` entry applying it before this closure ran. DF-04 and DF-02 were applied only now, at v6.4 closure — meaning they sat unapplied through the entirety of v6.4 sprint execution despite being "targeted at v6.4." DF-01/DF-05/DF-06 turned out to already be satisfied by unrelated prior patches, which is a lucky outcome, not evidence the deferred-item tracking process is working — it means 3 of 10 deferred items would have been carried forward as still-open despite already being resolved, and 2 of 10 would have gone a full cycle unactioned had this closure run's cross-check not caught it. Recommendation folded into DF-13 through DF-15 above: the recurrence check performed here should ideally run earlier — e.g., at Release Planning STEP 0 — rather than only being caught retrospectively at the following Post-Ship Closure.

---

## Carry-Forward

Items: 5

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | BLG-QA-61 / TSG-v60-01 has gone 3 consecutive cycles without resolution or a named re-park decision. | Head of Specs Team must action a disposition before the next release plan opens — resolve, reassign owner, or formally re-park with written rationale. | Release Planning |
| 2 | Deferred lessons-learnt patches from the immediately-prior cycle are not being applied during the following cycle's sprint execution — 2 of 3 substantive v6.3 deferred patches (DF-02, DF-04) were only caught and applied at this closure, a full cycle late. | Consider surfacing the prior cycle's still-open Deferred Items table as an explicit STEP 0 read at Release Planning, so patches can be scheduled as scope rather than only caught retrospectively at the next Post-Ship Closure. | Release Planning |
| 3 | STEP 4's merge-gate resume-sync sub-step has no branch check, risking an orphaned write on a stale `exec/**` branch. | Add an explicit branch check to the resume-sync sub-step, mirroring STEP 5's existing branch-ordering gate. | Sprint Planning |
| 4 | Skill-Silo rolling-3-cycle average was in Alert territory (53.2%) at the rebalance that shaped this cycle's scope. | Confirm at the next rebalance whether bundling BLG-FEAT-54 alongside the audit-remediation cluster brought the average back under the 40% ceiling, validating (or invalidating) the bundling approach as a repeatable corrective. | Roadmap |
| 5 | AI-adjacent security items have now been derived ad hoc from the same ST-04 risk assessment for 2 consecutive cycles rather than from a standing checklist. | If a 3rd consecutive release repeats this pattern, escalate the standing AI safety checklist proposal (DF-09) from advisory to a scoped backlog item. | Release Planning |

---

## v6.4 Outcome Summary

| Metric | Value |
|--------|-------|
| Stories planned | 13 |
| Stories delivered | 13 |
| Velocity | 1.00 |
| Spec deviations | 0 |
| TSG items filed this cycle | 1 (TSG-v64-01) |
| TSG items resolved this cycle | 2 (TSG-v63-01, TSG-v63-02) |
| Phase 3 friction items | 3 (1 action-now resolved in-session, 2 deferred to v6.5) |
| Phase 4 friction items | 1 (deferred from v6.3, resolved this closure) |
| Carry-forward from v6.3 | 10 items (DF-01–DF-10): 2 resolved this closure, 1 resolved via ST-06 this sprint (DF-10), 3 confirmed already satisfied, 1 treated as redundant, 3 continue as monitoring items into v6.5 |
| New escalations | 1 (BLG-QA-61 / TSG-v60-01, 3-cycle recurrence) |
| Immediate actions this closure | 2 |
| Validated patterns | 1 (LP-01 carry-forward-by-AC folding) |

---

// ARTEFACT_STATUS
{
  "phase": "Post-Ship",
  "cycle": "2026-07-02__release-v6.4",
  "release": "v6.4",
  "status": "complete",
  "completed_at": "2026-07-02"
}
