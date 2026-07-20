Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-20__release-v7.6

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v7.6 PDF / Print-Friendly Export
Run: 2026-07-20__release-v7.6
Reviewed by: PMO Lead
Date filed: 2026-07-20
Prior cycle checked: 2026-07-17__release-v7.5 (`lessons_learnt_closure.md`)

---

## What worked well

- The Phase 4 friction item (`.claude_current_state.json`'s stale `amended_backlog_slice_path` pointer to the already-closed `2026-07-17__release-v7.4`/`AMD-20260717-01`) had a precise, unambiguous fix identified at Phase 4 review time — this run authored the missing rule directly into `post_ship_closure.md` STEP 10 (LL-v7.6-P4-01, v2.17→v2.18) and applied it immediately rather than deferring a further cycle, per the non-deferrable immediate-action rule.
- Backlog reconciliation (STEP 3) and scope/decisions supersession (STEP 4) both located every target artefact on the first lookup — no missing documents this cycle, and no drift between `scope--2026-07-20__release-v7.6-pdf-print-friendly-export.md`'s 8 in-scope items (S2-01–S2-08, including the DL-073 capacity-fill expansion) and `execution_state.json`'s 8 completed stories.
- STEP 6 endpoint coverage drift check came back clean: the `GET /ai/monthly-cost` baseline-registration gap flagged mid-sprint (`sprint_close.md` Process Notes — missed in the signed-off commit, caught by the ST-12 CI gate) had already been fully resolved in a follow-up commit before this closure ran, so no fresh `BLG-OPS` item was needed. `categorizeEndpoint()` in `SystemStatus.js` also already handles `/ai` as a top-level prefix, so v7.6's one new endpoint required no frontend follow-up.
- ESC-EXEC-20260720-01 (EPIC-07's Gemini/Claude premise error) was fully resolved in-session by the Product Owner during Phase 3 with a clean audit trail (`execution_escalations.md`) — nothing remained open for this closure to disposition.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** No — different root cause from v7.5's closure friction item (that was a companion-changelog staleness gap; this is a same-commit `prompt_change_log.md` append gap)

**What happened:** Sprint execution's Phase 3 action-now lessons-learnt fix (`execution_prompt.md` v3.57→v3.58, adding the API performance baseline pre-PR check, LL-v7.6-P3-01) was correctly applied and correctly reflected in `OPERATIONAL_GUIDE.md` (v4.103→v4.104, §8/§14 both updated) — but the corresponding `prompt_change_log.md` append (CLAUDE.md §6 step 4, mandatory in the same commit as any governance prompt edit) was never made. This was only discovered at this closure's own STEP 8 review, when the file was read to append this cycle's Phase 4 fix and both rows were found absent.

**Where in the routine:** STEP 8 — Lessons Learnt Review and Application (cross-referencing `prompt_change_log.md` before appending this run's own entry)

**Root cause:** process gap — the Phase 3 action-now application correctly completed 3 of CLAUDE.md §6's 4 mandatory steps (version bump, `OPERATIONAL_GUIDE.md` §14 table, phase-section header) but missed step 4 (the changelog append) entirely, with no downstream check catching the omission before this closure ran.

**Blast radius analysis:**
- What would have propagated: no functional impact — the prompt version bump itself was correctly applied and correctly reflected in `OPERATIONAL_GUIDE.md`, so no engine would have misread the current version. The only exposure is an incomplete audit trail in `prompt_change_log.md` for anyone reconstructing why `execution_prompt.md` changed between v3.57 and v3.58.
- When it would have surfaced: next `governance-drift` skill check or lifecycle audit cross-referencing prompt versions against `prompt_change_log.md` entries.
- Recovery cost if uncaught: low (single-file backfill, no downstream engine reads were affected).

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/prompt_change_log.md`
  - Section: end of table (append-only)
  - Change: backfilled the two missing rows (`execution_prompt.md` v3.57→v3.58 and `OPERATIONAL_GUIDE.md` v4.103→v4.104), each marked `(backfilled at post-ship closure 2026-07-20__release-v7.6 STEP 8)`, then appended this run's own two rows (`post_ship_closure.md` v2.17→v2.18 and `OPERATIONAL_GUIDE.md` v4.104→v4.105).
  - Version: n/a (append-only log, not itself versioned)
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — this row is itself the append

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| Cross-EPIC shared-file merge-conflict pattern (`execution_state.json`, and per `2026-07-17__release-v7.5` closure, `backend/routers/test.py`/`src/pages/SystemStatus.js`/`tests/e2e/system-status.spec.js`/`docs/specs/data_model.md`/`docs/ops/api_performance_baseline.md`/`docs/reference/openapi.yaml`) recurred a 3rd consecutive multi-EPIC cycle (`2026-07-10__release-v6.9` → `2026-07-17__release-v7.5` → `2026-07-20__release-v7.6`, this cycle: every one of 8 EPICs after the first hit an `execution_state.json` `completed_items` conflict, resolved per CLAUDE.md §8). | `2026-07-17__release-v7.5` (`lessons_learnt_closure.md` Outstanding Deferred Patches) | Structural fix (e.g. per-EPIC append-only manifest files aggregated at build/CI time) to remove the recurring cross-EPIC merge-conflict surface — Owner: Head of Engineering; Target: next roadmap review | Head of Specs Team |

Per `lessons_learnt_prompt.md` §3.7: this item recurred while the prior cycle's outstanding action remained unresolved (no `run roadmap` invocation has occurred since `2026-07-17__release-v7.5` closed — both `v7.6`'s roadmap formalization and its capacity-fill expansion used direct-write/PO-bypass patterns instead, per DL-072/DL-073 — so the named target "next roadmap review" has not yet arrived). Recorded as an automatic escalation rather than re-deferred a third time.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/post_ship_closure.md` | STEP 10 | New amendment field reset rule (LL-v7.6-P4-01): if `active_amendment` is non-empty and its originating cycle has reached `Closed`/`Closed_with_actions`, clear `amended_backlog_slice_path`, `amendment_sealed_utc`, `active_amendment`, `amendment_status` in the same STEP 10 write | 2.17 → 2.18 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §10, §14, document header | Source prompt header, governance table row, and self-version updated to match the bump above | 4.104 → 4.105 | Yes |
| `claude/system/changelogs/post_ship_closure_changelog.md` | Table (top row) | Current-version entry added (v2.14–v2.17 not backfilled — those versions predate the 2026-07-17 companion-changelog rule) | n/a (companion changelog) | Not applicable |
| `claude/system/prompt_change_log.md` | Table (append-only) | Backfilled 2 missing Phase 3 rows + appended 2 rows for this run's own changes (see Friction Item 1) | n/a | Yes (self) |
| `.claude_current_state.json` | Global state (STEP 10) | Applied the new LL-v7.6-P4-01 rule immediately: `amended_backlog_slice_path`, `amendment_sealed_utc`, `active_amendment`, `amendment_status` cleared — `2026-07-17__release-v7.4`/`AMD-20260717-01` confirmed `Closed_with_actions` | n/a | Not applicable |

This resolves `lessons_learnt_cycle.md` Phase 4's single friction item in full (`defer` classification at Phase 4 time; re-classified `immediate` here since the fix required only a post-ship-closure-scoped prompt edit, squarely within this routine's own write scope, and applied per the non-deferrable immediate-action rule).

---

## New files created this run

None (`closure_state.json`, `closure_record.md`, and this file are standard STEP 0/STEP 9/STEP 8.5 outputs, not "improvement" artefacts).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/changelogs/delivery_verification_changelog.md` | Table body | Backfill missing 2.4–3.4 historical version rows (carried from `2026-07-17__release-v7.5` — target not yet arrived, no roadmap review has run since) | Head of Specs Team | next roadmap review |
| Coding standard / lint rule | n/a | Require `Array.isArray(...)` guards on any `.map()`/`.filter()` call over a JSON API response field (carried from `2026-07-17__release-v7.5` — target not yet arrived) | Head of Engineering | next roadmap review |
| `src/pages/SystemStatus.js` `categorizeEndpoint()` | Function body | Add `/price-alerts` and `/saved-filters` `includes()` branches (carried from `2026-07-17__release-v7.5`, still unaddressed 1 cycle later; not urgent — both endpoints degrade gracefully to `'Other'`) | Frontend engineer | before next System Status review |

Note: the cross-EPIC merge-conflict structural-fix patch (also carried from v7.5) is **not** repeated in this table — per `lessons_learnt_prompt.md` §3.7, its recurrence this cycle makes it an automatic Recurrence Escalation (see above) rather than a re-deferred outstanding action.

---

## Escalations

None beyond the Recurrence Escalation recorded above.

---

## Carry-Forward
Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | This is the 3rd consecutive cycle (`2026-07-17__release-v7.4` AMD, `2026-07-17__release-v7.5` direct-write formalization, `2026-07-20__release-v7.6` DL-073 capacity-fill bypass) needing an ad hoc PO-directed bypass for a routine, non-emergency, same-session scope change on an already-Published or already-formalized cycle — no governed engine currently accepts this class of request. | Release Planning should evaluate whether a bounded, governed "reopen with zero downstream consumption" path is worth adding (per this cycle's own `lessons_learnt.md` Friction Item 2), rather than requiring a fresh PO bypass each time. | Release Planning |
| 2 | The empty-Now-horizon roadmap formalization direct-write pattern (DL-068/DL-071/DL-072) has now been exercised for both the pure-relabel case and the scope-selection case (this cycle, selecting a new anchor item from an empty horizon) via the same mechanism, with no distinct governance track distinguishing the two — the scope-selection case is a materially larger authority step. | Head of Specs Team should consider whether an empty-Now-horizon scope-selection reopen needs its own confirmation step, distinct from a pure carry-forward relabel, if this pattern recurs a second time under the scope-selection case specifically. | Roadmap |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-07-20__release-v7.6",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-07-20T22:45:00Z",
  "friction_item_count": 1,
  "action_now_count": 2,
  "deferred_count": 3,
  "escalation_count": 1,
  "carry_forward_count": 2,
  "status": "Complete"
}
```
