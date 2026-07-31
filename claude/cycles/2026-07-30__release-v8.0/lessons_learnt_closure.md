Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-31
Cycle: 2026-07-30__release-v8.0

# Lessons Learnt — Post-Ship Closure — v8.0

Feature / Trigger: Close outstanding backend error-masking, security-hardening, and FX/data-spec debt; ship keyboard/focus accessibility fixes to the Trade Plan flow; strengthen QA/CI test infrastructure; harden operational alerting and disaster-recovery readiness; fix the recurring cross-EPIC `execution_state.json` merge-conflict pattern.
Run: 2026-07-30__release-v8.0
Reviewed by: PMO Lead
Date filed: 2026-07-31
Prior cycle checked: 2026-07-28__release-v7.10

---

## What worked well

- All three source records (`lessons_learnt.md`, `lessons_learnt_cycle.md` Phase 3 + Phase 4) were pre-classified with a disposition per action item — closure review confirmed each rather than performing first-pass triage from raw prose.
- The one unambiguous, well-specified Phase 3 friction item (infra/ops verification delegation sub-pattern) was applied immediately within this routine's write scope, consistent with the "immediate action rule" — closing it same-cycle rather than leaving it as a second deferred patch behind the governance_sync.yml fix.
- The Endpoint Coverage Drift Check (STEP 6) correctly picked up the `BLG-OPS-111` tracking item across a second cycle boundary and computed an accurate normalised delta (6 resolved since v7.10, 4 new gaps) rather than re-deriving from scratch.

---

## Friction Log

### Friction Item 1

**Classification:** Type B — Stale record claim (lessons-learnt record asserted a fix had not landed when it had)

**Recurrence:** No — first observed instance of this specific claim-vs-reality mismatch.

**What happened:** `lessons_learnt_cycle.md` Phase 4's "Outstanding deferred patches" table carried forward a claim that the `completed_items` cross-EPIC union pre-seal check "has not yet landed in the prompt itself" (`execution_prompt.md` STEP 5 — Sprint Close seal step). This is inaccurate: the check was formally added at STEP 7 (Seal Execution Record) as part of `2026-07-28__release-v7.10`'s own post-ship closure (`execution_prompt.md` v3.60→v3.61, `OPERATIONAL_GUIDE.md` §14 entry 4.122, both confirmed present and correctly versioned). The Phase 4 record's author evidently was not aware the v7.10 closure had already landed the fix, or conflated the general principle (STEP 5 vs. the actual STEP 7 sub-check) with an unapplied state.

**Where in the routine:** STEP 8 — Lessons Learnt Review and Application (closure-phase cross-check against the actual prompt content, not just the lessons-learnt record's own claim).

**Root cause:** No step in `execution_prompt.md` or `delivery_verification_prompt.md` cross-checks a "still outstanding" claim in a carried-forward deferred-patch table against the actual current state of the target file before re-recording it. The claim was copied forward from a genuine v7.10 gap without re-verifying it was still open at v8.0 (it had in fact been closed by v7.10's own closure run, one cycle before this claim was written).

**Blast radius analysis:**
- What would have propagated: a false "still open" outstanding action would have been recorded again in this cycle's closure record, and potentially carried forward indefinitely as a phantom deferred patch — no functional risk, but ongoing confusion and wasted review cycles at every future closure that re-reads it.
- When it would have surfaced: whenever someone finally checked the actual prompt content against the claim (as done here) — could have persisted for many cycles undetected, since the check the claim describes is genuinely satisfied in the artefact itself.
- Recovery cost if uncaught: low (a documentation correction), but compounding — each cycle that copies the stale claim forward without verification adds review noise.

**Process patch:**
→ Corrected in this run's closure record (§5/§6) rather than filed as a further deferred patch — the fix already exists, so the only action needed is retiring the incorrect claim. No prompt change required.

---

## Recurrence Escalations

None new. Friction Item 1 above is a documentation-accuracy correction, not a recurrence of a prior open action.

**Escalation trigger honoured from prior cycle:** `2026-07-28__release-v7.10`'s own `lessons_learnt_closure.md` Carry-Forward item 1 stated: "If a third consecutive cycle finds `BLG-OPS-111`'s list still misaligned against the live gap, this should be escalated from an advisory delta note to a mandatory reconciliation action at that cycle's Post-Ship Closure STEP 6." This is that third consecutive cycle (v7.9 → v7.10 → v8.0). STEP 6 found 19 normalised endpoint gaps this run against `BLG-OPS-111`'s originally-filed list of 21 — 6 endpoints resolved since filing, but 4 different endpoints (`PATCH /notifications/preferences`, `PATCH /watchlist/{id}`, `POST /alerts/rules`, `POST /settings`) are newly missing and not on `BLG-OPS-111`'s list. Per the honoured trigger, this is recorded in the closure record §6 Outstanding Actions as a **mandatory reconciliation action** (not a further advisory delta note) for the Infrastructure & Operations Owner.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §5.1 — Delegation Classification, Classification rules | New sub-pattern: infra/ops verification/configuration task requiring live external dashboard/production access → `delegated_backend`, regardless of whether code is written (closes Phase 3 friction item — 6 of 19 v8.0 stories, 32% of scope, were initially misclassified `autonomous`). | v3.61→v3.62 | Yes |

This change additionally required an `OPERATIONAL_GUIDE.md` §14 governance-table update (v4.124→v4.125) and its dedicated changelog file (`changelogs/execution_prompt_changelog.md`), per CLAUDE.md §6.

---

## New files created this run

- `claude/cycles/2026-07-30__release-v8.0/closure_state.json`
- `claude/cycles/2026-07-30__release-v8.0/closure_escalations.md` (1 entry — `ESC-CLOSE-20260731-01`)
- `claude/cycles/2026-07-30__release-v8.0/lessons_learnt_closure.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `.github/workflows/governance_sync.yml` | Issue auto-close step | Add a precondition guard so a commit's `[ST-xx]` prefix only auto-closes the issue if the story's `execution_state.json` status is not `blocked_*` (or requires an explicit completion marker in the commit message). Outside Post-Ship Closure's write scope (`.github/workflows/` not a permitted path). | Infrastructure & Operations Owner (with Head of Engineering) | Next sprint planning cycle |
| `claude/backlog/backlog.md` | `BLG-OPS-111` entry body | **Escalated to mandatory reconciliation (3rd consecutive cycle — see Recurrence Escalations).** Reconcile the item's endpoint list against the current live gap: remove 6 now-resolved endpoints (`GET /analytics/strategy-version-comparison`, `GET /trade-plans/tags`, `GET /v1beta1/news`, `GET /v2/stocks/{symbol}/bars`, `POST /strategy/benchmark/import`, `POST /trade-plans/generate-plan`); add 4 newly-missing endpoints (`PATCH /notifications/preferences`, `PATCH /watchlist/{id}`, `POST /alerts/rules`, `POST /settings`). Outside Post-Ship Closure's backlog write scope (mark-shipped-complete / add-missing-Phase-4-items only — not existing-item body edits). | Infrastructure & Operations Owner | Before next post-ship closure (mandatory, not advisory, per honoured 3rd-cycle escalation trigger) |
| `release_planning_prompt.md` (scope-selection guidance) | Ungated-pool scan field-name list | Watch item (Release Planning `lessons_learnt.md` Carry-Forward, not yet actionable): if a second instance of a gate expressed via a field name other than `**Gate criteria:**`/`**Gate:**` is found at a future release planning session, file a `BLG-GOV-*` item extending the scan with an explicit canonical gate-field list. | Head of Specs Team | Next release planning session where a second instance is found |

---

## Escalations

| Escalation | Question | Owner | Deadline |
|-----------|----------|-------|----------|
| `ESC-CLOSE-20260731-01` | Reconcile `execution_prompt.md` EPIC-level sign-off consolidation vs. `delivery_verification_prompt.md` STEP -1.3's recognised-format list for `delegated_backend`/`delegated_decision`-heavy EPICs — select Option (a) extend the recognised-format list, or Option (b) standardise the consolidation step's literal signer string. | Head of Specs Team | 2026-08-03 (72h) |

Full record: `claude/cycles/2026-07-30__release-v8.0/closure_escalations.md`.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-OPS-111`'s endpoint list has now drifted for a third consecutive cycle (v7.9: understated by 4; v7.10: 4 resolved + 3 new; v8.0: 6 resolved + 4 new) — the honoured escalation trigger from v7.10's own Carry-Forward has converted this to a mandatory reconciliation action this cycle (see Outstanding deferred patches). If the item is not reconciled before the next post-ship closure, the pattern should prompt a structural fix (e.g. a script-derived endpoint list rather than a manually-maintained one) instead of a further manual reconciliation. | If still misaligned at next closure despite this cycle's mandatory-action escalation, raise a `BLG-GOV-*` item proposing the tracking item's endpoint list be script-derived at check time rather than maintained as static prose. | Post-Ship Closure |
| 2 | `execution_prompt.md`'s EPIC-level sign-off consolidation step and `delivery_verification_prompt.md` STEP -1.3's recognised-format list disagree on compliant signer strings for delegated-heavy EPICs (`ESC-CLOSE-20260731-01`). | Sprint Planning and Release Planning should expect this friction to recur at the next EPIC dominated by `delegated_backend`/`delegated_decision` stories until the escalation is resolved; no scope action needed, awareness only. | Sprint Planning |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-07-30__release-v8.0",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-07-31T14:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 3,
  "escalation_count": 1,
  "overdue_patches": 0,
  "status": "Complete"
}
```
