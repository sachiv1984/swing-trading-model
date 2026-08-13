Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-13
Cycle: 2026-08-12__release-v8.7

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Post-ship closure of v8.7 — User Features, Data-Integrity Closure & Cross-Domain Hardening (21/21 stories shipped, Verified, 0 deviations filed this sprint)
Run: 2026-08-12__release-v8.7
Reviewed by: PMO Lead
Date filed: 2026-08-13
Prior cycle checked: 2026-08-11__release-v8.6 (`lessons_learnt_closure.md`)

---

## What worked well

- STEP 3 (Backlog Reconciliation) was mechanically simple: all 21 shipped items located via the v8.7 Release Slice table's exact ST→backlog-ID mapping and marked `✅ COMPLETE`, cross-confirmed against `execution_state.json`'s `completed_items` array — no missing-entry gaps, 4 Phase 4 traceability items (`BLG-SPEC-129`, `BLG-FE-159`, `BLG-FE-160`, `BLG-SEC-33`) all pre-confirmed present with correct cycle references, 0 new additions required.
- STEP 5.1's Cross-Cycle Deviation Consolidation Review (cadence-triggered, 3rd invocation) earned its keep a 2nd time: it caught a genuine resolution-status drift on `DEV-v8.6-ST02-01` (accepted-as-shippable at v8.6, root cause actually closed this cycle by ST-03/`BLG-BE-95`, but the canonical spec's Known Deviations row was never updated to reflect it) — the same drift class the review's own first run (2026-08-03) was built to catch, now confirmed recurring rather than one-off.
- The prior cycle's (`v8.6`) `lessons_learnt_closure.md` had 0 open Escalations and 0 unresolved Outstanding Actions carried into this closure — confirmed clean at STEP 0, nothing pre-existing to action before this cycle's own work began.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** Yes — appeared in `2026-08-03__release-v8.1` (first run) and not in `2026-08-08__release-v8.4` (second run); this is the pattern's 2nd confirmed instance across 3 review runs, not a repeat of a specific still-open prior item.

**What happened:** `DEV-v8.6-ST02-01` (the "AI draft" badge omission on the Setup Thesis Digest panel, `trade_plan.md`) was accepted-as-shippable at v8.6 pending `BLG-BE-95` (persist `is_ai_draft` server-side). `BLG-BE-95` shipped this cycle as v8.7 ST-03 — `qa_evidence_EPIC-01.md` confirms AC-03 ("badge shown when true") passed and the story's own notes state it closes the deviation's root cause. The canonical spec's Known Deviations row, however, was never updated by ST-03 itself to reflect the resolution — it still read `Disposition: Accepted as shippable ... Unscheduled` until this closure's STEP 5.1 caught and corrected it.

**Where in the routine:** STEP 5.1 — Cross-Cycle Deviation Consolidation Review.

**Root cause:** process gap — no step in the normal `plan release → sprint execution` flow re-visits a *pre-existing* deviation row when the story that closes its root cause is a different, later story than the one that originally filed it. `execution_prompt.md`'s STEP 3.1.A deviation-check flow only checks for *new* deviations against the story's own current work, not whether the story just closed an older, already-filed deviation's root cause.

**Blast radius analysis:**
- What would have propagated: `trade_plan.md`'s Known Deviations table continuing to show a resolved gap as open/accepted indefinitely, misleading any future spec reader or the next deviation consolidation review's own register into re-flagging it as neglected.
- When it would have surfaced: only at the next full-document deviation sweep (this cycle's STEP 5.1) or a future spec author manually cross-referencing the row against current code — no automated gate would have caught it otherwise.
- Recovery cost if uncaught: low (single-row correction) but same recurring pattern as the first run's `DEV-ST14-01` finding — evidence this is a real, if infrequent, gap class rather than a one-off.

**Process patch:**

→ Immediate patch applied this run:
  - File: `docs/specs/frontend/pages/trade_plan.md`
  - Section: Known Deviations table, `DEV-v8.6-ST02-01` row
  - Change: Row updated to append a `**RESOLVED (v8.7, ST-03, BLG-BE-95)**` note citing the persisted `is_ai_draft` column and the passing AC-03 evidence; `Target resolution` field changed from `Unscheduled` to `Resolved — v8.7 (ST-03, BLG-BE-95)`.
  - Version: N/A — corrected in place per the same-commit-correction precedent set by the first review run's `DEV-ST14-01` fix (`docs/governance/deviation_consolidation_review_2026-08-03.md` Recommendation 1); no header/changelog bump made there either.
  - Confirmed by: Head of Specs Team (agent-mediated, per §5.3 convention)
  - Prompt change log entry: Not applicable — this is a canonical spec content correction, not a governance prompt/template edit.

→ Deferred patch (cannot apply this run):
  - File: `sprint_planning_prompt.md` or `execution_prompt.md` (exact location not yet decided)
  - Section: New — a story-completion check requiring any story that closes a *pre-existing* deviation's root cause (named via its own `Backlog reference` field, e.g. `BLG-BE-95`) to also update that deviation's canonical Known Deviations row in the same commit
  - Change required: The structural fix first recommended by the deviation consolidation review's first run (2026-08-03, Recommendation 3) and re-escalated by this run (2026-08-13, `docs/governance/deviation_consolidation_review_2026-08-13.md` Recommendation 2) — now recommended for filing as a `BLG-GOV-*` backlog item given 2 confirmed occurrences across 3 review runs
  - Owner: Head of Specs Team
  - Target: File as a backlog item before the next `plan release`

---

### Friction Item 2

**Classification:** Type D — Cognitive Fatigue

**Recurrence:** No (new observation this cycle)

**What happened:** `lessons_learnt_cycle.md` Phase 4 friction item 1 found that the newly-applied `LL-v8.5-P4-01` post-open CI-fix restatement requirement (`qa_evidence_template.md` v1.10, live for exactly one cycle before this) was satisfied for ST-08's post-open CI fix but not for ST-09's separate, independent post-open CI fix within the same EPIC's `qa_evidence_EPIC-03.md` — the requirement's wording did not make clear it applies per-fix rather than once-per-EPIC, and the first real-world use of the patch exposed that ambiguity.

**Where in the routine:** Sprint Execution STEP 3.2.A / Delivery Verification STEP 3 (traceability read of `qa_evidence_EPIC-03.md`).

**Root cause:** template omission — the requirement's original wording (added the day before this cycle began) did not anticipate the multi-fix-per-EPIC case explicitly.

**Blast radius analysis:**
- What would have propagated: future EPICs with multiple independently-fixed stories could continue satisfying the restatement requirement for only the first fix, leaving later fixes' CI-confirmation implicit rather than stated — a traceability gap that compounds as EPIC story-counts grow.
- When it would have surfaced: the next Delivery Verification session doing a literal per-story restatement check, or never, if verification continued reading "the EPIC restated a CI run" as sufficient.
- Recovery cost if uncaught: low (wording clarification only) — no incorrect verification outcome resulted this cycle since the underlying CI evidence was independently re-confirmed regardless.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/templates/qa_evidence_template.md`
  - Section: Standard Sign-Off Block, `LL-v8.5-P4-01` post-open CI-fix restatement requirement
  - Change: Appended a one-line clarification (`LL-v8.7-P4-01`) stating the requirement applies per CI-triggered fix, not once per EPIC — each story's own `Comments:` field must carry its own restatement when more than one story in an EPIC independently required a post-open fix.
  - Version: 1.10 → 1.11
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md` (2 rows: template edit + `OPERATIONAL_GUIDE.md` v4.160→v4.161 sync)

---

## Recurrence Escalations

None. Friction Item 1 recurs as a *pattern class* (2nd confirmed instance of spec/QA-doc resolution-status drift across 3 deviation consolidation review runs) but is not a specific still-open prior-cycle outstanding action — each instance has been corrected in the same commit it was found, per established precedent. Friction Item 2 is newly identified this cycle. No deferred patch from `2026-08-11__release-v8.6`'s closure was carried forward without a `prompt_change_log.md` entry (that closure had none outstanding).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `docs/specs/frontend/pages/trade_plan.md` | Known Deviations, `DEV-v8.6-ST02-01` | Resolution-status drift corrected — row marked Resolved v8.7 (ST-03, BLG-BE-95) | N/A (content correction, no version field) | Not applicable |
| `claude/system/templates/qa_evidence_template.md` | Standard Sign-Off Block | Post-open CI-fix restatement requirement clarified as per-fix, not per-EPIC (LL-v8.7-P4-01) | 1.10 → 1.11 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §14 QA Evidence Template row + self-row + Change Log | Synced to qa_evidence_template.md v1.11 | 4.160 → 4.161 | Yes |

---

## New files created this run

- `docs/governance/deviation_consolidation_review_2026-08-13.md` — 3rd cadence-triggered run of the cross-cycle `DEV-*` consolidation review (STEP 5.1). 12 deviation records catalogued (2 new since the 2nd run); 1 resolution-status drift found and corrected (`DEV-v8.6-ST02-01`, see Friction Item 1).

If none beyond the above: none.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `sprint_planning_prompt.md` (location TBD) | New — pre-seal stale-story check | Confirm a story's referenced feature/roadmap item isn't already shipped before pulling it into scope (carried from `lessons_learnt_cycle.md` Phase 3 friction item 2 — ST-12/`BLG-BE-30` was scoped in despite its target feature having shipped 4 releases earlier) | Head of Specs Team | Next `sprint_planning_prompt.md` revision or `groom backlog` pass |
| `claude/system/shared_standards.md` | New — canonical "Sandbox Access Constraint" disclosure block | Define one reusable disclosure statement (e.g. `SBX-NO-LIVE-DB`/`SBX-NO-LIVE-STAGING`) for the recurring "no live staging/production access in this sandbox" constraint, hit independently by 3 stories this cycle (ST-07, ST-13, ST-15) with slightly different re-derived phrasing each time (carried from `lessons_learnt_cycle.md` Phase 4 friction item 2) | Head of Specs Team | Next `shared_standards.md` revision |
| Backlog (`claude/backlog/backlog.md`) | New `BLG-GOV-*` item | File the structural fix recommended by the deviation consolidation review (require any story closing a pre-existing deviation's root cause to also update that deviation's canonical Known Deviations row in the same commit) — recommended twice (2026-08-03, 2026-08-13) without being filed as a trackable item | Head of Specs Team | Before next `plan release` |

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The deviation consolidation review's structural-fix recommendation (resolving-commit-must-update-canonical-spec discipline) has now been made twice across 3 runs without being filed as a backlog item — soft recommendations alone are not converting into tracked action. | Post-Ship Closure or Head of Specs Team should file this as a `BLG-GOV-*` item at the next opportunity rather than re-recommending a 4th time; if the pattern recurs a 3rd time before it's filed, treat as a recurrence escalation. | Post-Ship Closure |
| 2 | 3 independent stories this cycle (ST-07, ST-13, ST-15) each re-derived similar-but-not-identical "no live staging/production access" disclosure prose — a higher density than prior cycles, per `lessons_learnt_cycle.md` Phase 4 friction item 2. | If a canonical disclosure block is added to `shared_standards.md`, Sprint Execution should reference it directly rather than re-deriving prose, going forward. | Sprint Execution |
