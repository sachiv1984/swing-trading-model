Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-30
Cycle: 2026-09-28__release-v9.8

---

# Closure Escalations — 2026-09-28__release-v9.8

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20260930-01

| Field | Value |
|-------|-------|
| Issue | Release Planning `lessons_learnt.md` Friction Item 1 (`2026-09-28__release-v9.8`): the PO Modify directive (seat ≥1-2 build-and-ship U-items, per the `2026-09-28__scheduled` rebalance's PVR 0.089 🔴 Alert reading) has gone unsatisfiable for lack of ready candidates across 5 non-consecutive cycles (v9.1–v9.4, now v9.8), with no change in backlog composition. The only `BLG-FEAT-*` items ever filed remain `73`/`76` (structurally gate-blocked) plus the now-shipped-and-retired `74`. No new feature-shaped idea has surfaced through several consecutive idea-intake windows. |
| Type | Decision required — product/process review |
| Escalated to | Product Owner |
| Reason | Re-flagging an empty ungated-U-item pool each cycle without addressing the intake side will keep producing the same finding. A ruling is needed on whether idea-intake windows are adequately prompting for genuine build-and-ship candidates, and if not, what intake-process change would surface them. |
| Tracking | SLA 2026-10-03 (72h from filing) |
| Disposition | Resolved — 2026-10-05. Product Owner ruling, agent-mediated on 2026-10-05 (`execution_prompt.md` §5.3) and confirmed by the human Product Owner on 2026-10-05. Idea-intake windows did not reliably prompt for build-and-ship candidates. Under identical instructions, the same roles produced 1 candidate in one window (`IW-20260914-01` → `BLG-FEAT-95`) and 6 in the next (`IW-20260919-01` → `BLG-FEAT-96/97/98`, `BLG-FE-180/181/182`). The release that honoured the directive used up each pool (v9.4, v9.6). The reduced-roster `IW-20260928-01` exercised no user-facing role, which left the directive unsatisfiable at v9.8. Applied as `idea_intake_prompt.md` v2.9→v2.10 (see `prompt_change_log.md` 2026-10-05): - §2.1 step 2a: each participating user-facing role must submit at least 1 build-and-ship candidate. It must pass the `roadmap_prompt.md` §7.1 content test, be grounded in a named live surface plus evidence of need, and pass the §2.0 overlap checks. A recorded "none found" answer replaces any quota. - A roster rule for reduced windows while a pull-forward is mandatory. - A STEP 4 Notes tally line. Premise correction: the escalation's statement that no new feature-shaped idea had surfaced was inaccurate. The pool emptied; it did not fail to fill. Near-term pool for v9.10: - `BLG-FE-193`, seatable once `BLG-BE-135` (v9.9) ships; - `BLG-FEAT-59`, gate cleared 2026-10-05 per `docs/ops/ai_feature_usage_review_2026-09-24.md`. Open follow-up: whether reduced-roster windows should be permitted at all. This is referred to the Head of Specs Team as BLG-GOV-364. |

---

## ESC-CLOSE-20260930-02

| Field | Value |
|-------|-------|
| Issue | `lessons_learnt_cycle.md` Phase 3 Friction Item 1 (`2026-09-28__release-v9.8`): `execution_state.json` top-level summary arrays/fields (`merge_gate.epics_merged`/`epics_pending`, `completed_items`, `process_notes`, per-story `deviations_filed`) went stale relative to per-story/per-EPIC ground truth at least 3 separate times this cycle, each self-corrected at the next resume or at sprint close rather than prevented at the moment of the underlying write. This is the same defect class first raised at `2026-09-21__release-v9.6`, carried unapplied through `2026-09-23__release-v9.7`, and now recurring a 3rd time at `2026-09-28__release-v9.8` — 2 full carries with no `execution_prompt.md` STEP 3.1/3.1.D structural patch shipped, crossing the `lessons_learnt_prompt.md §3.7` mandatory 2-cycle recurrence-escalation threshold. |
| Type | Recurrence escalation — `lessons_learnt_prompt.md §3.7` mandatory trigger (deferred patch carried 2+ cycles without a `prompt_change_log.md` entry) |
| Escalated to | Head of Specs Team |
| Reason | Three separate backstops (STEP 4 resume-sync, STEP 5.1 item-count reconciliation, STEP 5.1 deviations-filed enforcement) already catch every instance before seal, but nothing prevents the underlying per-story write from going stale in the first place. A ruling is needed on whether to implement a same-step self-verification read-back for STEP 3.1.A's per-story writes generally (extending the pattern already applied narrowly to `deviations_filed` by `LL-v9.0-P3-01` and to the merge-state persist by `LL-v9.2-P3-01`), or an alternative structural fix — not actioned in this closure, as no unambiguous fix wording exists yet for a general-purpose read-back mechanism. |
| Tracking | SLA 2026-10-03 (72h from filing) |
| Disposition | Resolved — 2026-10-05, Head of Specs Team ruling (agent-mediated, §5.3, user-directed). Adopted a general same-step self-verification rule rather than another read-back for one field. Applied as `execution_prompt.md` v3.80→v3.81: - §9.2: the top-level summary arrays and `merge_gate` are projections, rebuilt from per-story and per-EPIC records in the same write, and every state write ends with a read-back from disk checking 4 equalities before advancing. - §10 step 3a: on resume, pushed commits are reconciled before any `not_started`/`in_progress` item runs. This closes the §3.7 recurrence (v9.6→v9.7→v9.8). The fourth instance at v9.9 (EPIC-03 PR #1888 state; ST-33/ST-34 left `not_started`) is cited as evidence. Follow-up: a backlog item to script the read-back check (`/backlog-add`, owner Head of Engineering). Follow-up filed: BLG-GOV-363. |

---

## ESC-CLOSE-20260930-03

| Field | Value |
|-------|-------|
| Issue | `lessons_learnt_cycle.md` Phase 4 Friction Item 1 (`2026-09-28__release-v9.8`): `delivery_verification_prompt.md §7`'s Known Deviations sync note (`LL-v2.3-CL-03`) is scoped to deviations formally filed via `sprint_close.md`'s "Deviations filed this sprint" register. This cycle's register was empty, but QA evidence separately recorded 3 `Pass_with_deviation` results — a distinct unregistered category — one of which (ST-17/`BLG-OPS-171`) names a genuine canonical spec (`health_endpoints.md`) in its `spec_references`, the same shape the sync note is meant to catch, yet the sync note never triggered because the item was never filed as a STEP 3 deviation. Even had it been read as applicable, Delivery Verification's own write-scope restriction (§5) forbids modifying canonical spec files, so the sync note's instruction could not have been executed there without violating that restriction. |
| Type | Governance-prompt scope ambiguity — decision required |
| Escalated to | Head of Specs Team |
| Reason | Ruling needed on whether a QA-evidence `Pass_with_deviation` classification whose `spec_references` include a genuine canonical spec should (a) be treated as a STEP 3-equivalent deviation, with Known Deviations sync performed by a downstream engine that holds spec write-authority (e.g. Post-Ship Closure), or (b) remain a QA-evidence-only category exempt from the sync note, with the note's own scope line narrowed to say so explicitly. Not actioned in this closure — Post-Ship Closure's own write-scope permits canonical-spec edits only for deviation-compliance field completeness (§5), not for authoring a new Known Deviations entry outside that narrow carve-out. |
| Tracking | SLA 2026-10-03 (72h from filing) |
| Disposition | Resolved — 2026-10-05, Head of Specs Team ruling (agent-mediated, §5.3, user-directed). Option (b), with a narrow exception. A QA-evidence `Pass_with_deviation` result is exempt from the Known Deviations sync note even when its `spec_references` name a canonical spec. The exception: when the `Comments` show the shipped behaviour contradicts the spec, it is treated as an unfiled STEP 3 deviation. The separate conflict between the sync note and Delivery Verification §5's write scope is also fixed: Delivery Verification now detects a missing entry and routes it, and Post-Ship Closure STEP 5 creates it under its deviation-compliance carve-out. Applied as `delivery_verification_prompt.md` v3.12→v3.13 (STEP 3) and `post_ship_closure.md` v2.36→v2.37 (§5, STEP 5). ST-17/`BLG-OPS-171` at v9.8 is confirmed exempt, so no retroactive spec entry is owed. (The note sits under STEP 3, not §7 as the record cited.) |

---

**Carried from prior cycle (not re-filed here):** `ESC-CLOSE-20260928-02` (Release Planning `§-1.2` Option(b) rebalance-equivalence precedent reuse ruling, filed at `2026-09-23__release-v9.7` closure) remains **Open**, SLA 2026-10-01 — 1 day from this closure's filing date. Not yet breached at time of this closure, but due imminently; the next routine to read `.claude_current_state.json.open_escalations` should check it first.
