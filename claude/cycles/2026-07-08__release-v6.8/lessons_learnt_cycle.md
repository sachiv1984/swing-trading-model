Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-09
Cycle: 2026-07-08__release-v6.8

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-08__release-v6.8
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-09
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-07-06__release-v6.7 (`lessons_learnt_cycle.md` `## Phase 3`)

### What went well

- All 17 in-scope ST items delivered across three EPICs (the largest single-sprint story count since v6.3/v6.4) — zero items returned to backlog, both delegated_frontend items (ST-05, ST-06) delivered directly by the engine with clean `Unblocked` delegation log terminal states.
- Agent-mediated Director of Quality review caught two genuine, material bugs before merge: ST-06's linked-closed-trade count was missing a `status='closed'` condition required by `reports.md`'s literal field definition (fixed in-session, commit `02423690`, new Playwright scenario added); and a post-PR-merge CI failure on ST-11's `SC-ARC5-03` traced to a real `page.route()` registration-order bug (not the flake it was first assumed to be), fixed and independently re-verified 5/5 deterministic before approval.
- Two pre-met items (ST-13, ST-15) were correctly identified and processed via the LL-v2.4-P4-02 pre-met path — full `qa_evidence_EPIC-03.md` entries with verification method and DoQ sign-off recorded rather than being silently skipped as "already done."
- Root-cause investigation on BLG-SPEC-71 (Reports.js sections claimed shipped but never implemented) used `git log -S` across full history to definitively distinguish "spec-authored, never built" from "built, then removed" — a reusable investigative pattern worth naming for future spec-debt items.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| All three EPIC branches this sprint (EPIC-01, EPIC-02, EPIC-03) received one or more commits *after* their own PR had already merged into `main` — a state-persist commit per STEP 4 §3a, and on EPIC-02, two `[GOVERNANCE]` backlog filings (BLG-SPEC-71 update, BLG-SPEC-72). Since a GitHub PR merge only brings in the diff as of merge time, every one of these commits was stranded on the now-inert feature branch. STEP 4's existing LL-v3.9-P3-1 resync only re-checks `execution_state.json`'s own `merge_gate` fields via `gh pr view` — it has no mechanism to detect or reconcile an arbitrary orphaned commit on a merged branch. EPIC-03's orphaned `execution_state.json` commit (`80772225`) had genuinely not reached `main` (still showed `status: "done"` / `pr_status: "open"` / `merge_gate.all_merged: false`) and required manual reconciliation at this sprint's close. EPIC-01's and EPIC-02's orphaned commits were found to already be present on `main` in equivalent form — but only incidentally, via a later EPIC branch's rebase carrying the content forward, not by any designed mechanism. | Phase 3 | C | action-now | Applied this session: `execution_prompt.md` STEP 4 — new **Orphaned post-merge commit check (LL-v6.8-P3-01)** added immediately after the LL-v3.9-P3-1 note. On merge-gate resume, for every confirmed-merged EPIC: `git fetch origin` then diff `origin/main..origin/exec/<cycle_id>/<epic_id>`; any listed commit is orphaned — inspect and, if it carries content not already on `main`, reconcile it directly (commit format `[EPIC-xx] Reconcile orphaned post-merge commit <sha> onto main`). Each check (reconciled or redundant) is logged to a new `execution_state.json.process_notes` array, which STEP 5.3 rolls up into `sprint_close.md`'s Process Notes section (new bullet added to STEP 5.3's Must-Include list). `execution_prompt.md` v3.53→v3.54; `OPERATIONAL_GUIDE.md` v4.86→v4.87; `prompt_change_log.md` entry appended. Reviewed for duplication against LL-v3.9-P3-1, LL-v2.0-P3-5, and CLAUDE.md §8 (none found) via agent-mediated Head of Specs Team sign-off before being applied. | Head of Specs Team | — (applied this run) |
| **Separate observation, not actioned this run:** STEP 4's own steps 3a/3b instruct committing `execution_state.json`/governance files to the EPIC branch *after* the PR has already merged (step 1 of the merge sequence) — this is the root cause generating an orphaned commit on essentially every EPIC merge this sprint, not an edge case specific to one branch. The LL-v6.8-P3-01 patch above is a sound detection-and-reconciliation net, but the underlying instruction should eventually be corrected to commit onto `main` directly rather than the now-inert branch, removing the need for detection entirely. | Phase 3 | A | defer | Change required: `execution_prompt.md` STEP 4 §3a/§3b — redirect the post-merge persist-state and governance-file commits to land on `main` directly (after the branch-safety checkout used elsewhere in STEP 5/8) rather than on the just-merged EPIC branch. | Head of Specs Team | Next scheduled prompt review |

**Recurrence Notes:** None. No friction item in this cycle matches a prior-cycle (v6.7) item — v6.7's friction log covered scripted-remediation directory scoping and `dark:`-variant selector staleness, both unrelated to this cycle's findings.

---

## Phase 4

*(To be appended by Delivery Verification — STEP 8.5 of `delivery_verification_prompt.md`.)*
