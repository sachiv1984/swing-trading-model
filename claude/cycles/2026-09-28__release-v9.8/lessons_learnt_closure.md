Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-30

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Clear the full v9.8 full-capacity debt slice — 39 stories across 6 EPICs spanning frontend/UX consistency, backend reliability, QA/test coverage, operations/security hardening, spec & API contract debt, and governance/process debt, with no anchor feature.
Run: 2026-09-28__release-v9.8
Reviewed by: PMO Lead
Date filed: 2026-09-30
Prior cycle checked: 2026-09-23__release-v9.7 (`lessons_learnt_closure.md`)

---

## What worked well

- All 39 shipped backlog-slice items traced cleanly to their `BLG-*` source items in one pass (STEP 3) via each `stage4_backlog_slice.md` entry's own `**Source:**` field — mechanical and error-free across all 6 EPICs, batch-applied via script rather than 39 individual edits.
- The STEP 6 Endpoint Coverage Drift Check (`scripts/check_api_performance_baseline_drift.py`) found a clean 0-gap result — this cycle added no new backend routes (EPIC-05's slice was documentation/openapi-schema authoring only), so no `SystemStatus.js` `categorizeEndpoint()` follow-up was needed this time (unlike `v9.7`'s `BLG-FE-191` finding, itself shipped this cycle as ST-04).
- STEP 7.3's full-document TSG sweep again found 0 Open entries — the reconciliation discipline established across the last several closures continues to hold.
- 1 delegation record this cycle (`DEL-20260929-01`, ST-15) and 6 `delegated_decision` escalations all reached terminal resolution within the sprint, none carried past sprint close.
- The Telegram changelog digest step (STEP 1.5) failed to send (no `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` configured in this sandbox execution environment) but correctly did not block closure, per the routine's own non-blocking hard rule — the script's designed failure mode worked as intended.

---

## Friction Log

**Closure-phase finding (STEP 8):** Release Planning `lessons_learnt.md` Friction Item 3 recommends adding a worked example to `claude/roadmap/workforce_capacity.md`'s effort-to-days precedence rule (covering an `XS (<1h)` hour-denominated qualifier). The fix itself is unambiguous, but `workforce_capacity.md` is not named in `post_ship_closure.md §5`'s permitted write-scope list (which names `current_roadmap.md`, `backlog.md`, and "templates and prompt files" generically, but not this specific `claude/roadmap/*` reference document) — and this cycle's own Phase 3 Friction Item 2 independently documents `claude/roadmap/*` as a recurring write-scope cost centre (4 near-misses this cycle alone, `workforce_capacity.md` itself being the sole existing carve-out, granted to Sprint Execution Engine specifically). Rather than assume the "templates and prompt files" language extends to this file, it was left unwritten and deferred — see Outstanding deferred patches below. Type A — Governance Drift: the write-scope list's own specificity did its job here, at the cost of a 1-cycle delay on an otherwise-ready fix.

No other closure-phase friction — STEPs 1–7 (changelog, roadmap, backlog reconciliation, scope/decisions supersession, deviation compliance, operational docs, Specs Index) completed with no missing documents and no discrepancies between the authoritative backlog slice and `backlog.md`.

**Deviation consolidation review (STEP 5.1):** Not due this cycle — `deviation_consolidation_review_cycle_count` was `0` (reset at the 6th run, `2026-09-28__release-v9.7` closure); this is cycle 1 of 3 since last run. Logged per the routine's own cadence rule; counter advanced to `1` at STEP 10.

---

## Recurrence Escalations

Three new decision-required/recurrence escalations raised this closure (`lessons_learnt_prompt.md §3.7` and general decision-required classification), filed as `ESC-CLOSE-20260930-01`/`-02`/`-03` in `closure_escalations.md`, all SLA 2026-10-03:

1. **Release Planning `lessons_learnt.md` Friction Item 1 — PO Modify directive (seat ≥1-2 build-and-ship U-items) unsatisfiable for lack of ready candidates.** Recurred across 5 non-consecutive cycles (`v9.1`–`v9.4`, now `v9.8`) with no change in backlog composition. Escalated to Product Owner for an idea-intake-process review, since re-flagging an empty pool each cycle without addressing intake will keep producing the same finding.
2. **`lessons_learnt_cycle.md` Phase 3 Friction Item 1 — `execution_state.json` top-level summary array/field staleness (`merge_gate`, `completed_items`, `deviations_filed`) self-corrected at resume/close rather than prevented at write time.** First raised at `2026-09-21__release-v9.6`, carried unapplied through `2026-09-23__release-v9.7`, and confirmed recurring a 3rd time this cycle (3 separate instances, all caught by existing backstops before seal). Crosses the `§3.7` two-cycle automatic-escalation threshold. No unambiguous general-purpose fix wording exists yet — escalated for a Head of Specs Team ruling on a STEP 3.1/3.1.D self-verification read-back rather than implemented blind.
3. **`lessons_learnt_cycle.md` Phase 4 Friction Item 1 — `delivery_verification_prompt.md §7`'s Known Deviations sync note scope ambiguity for QA-evidence `Pass_with_deviation` items.** A new-this-cycle finding (ST-17/`BLG-OPS-171` names a genuine canonical spec in a QA-evidence-only deviation category the sync note's scope line does not clearly cover). Escalated to Head of Specs Team for a scope ruling.

Two further deferred-patch carries were checked and found **not** to have crossed the threshold:
- Phase 3 Friction Item 2 (`claude/roadmap/*` write-scope near-misses, 4 this cycle) — 1st cycle, filed as a secondary recommendation inside `BLG-GOV-355` rather than a separate escalation.
- Phase 4 Friction Item 2 (agent-mediated signer format mandate) — 1st carry (`v9.7`→`v9.8`), symptom did not recur this cycle (all 6 EPICs' signer labels independently confirmed consistent).

**Carried from prior cycle, still open, not re-filed:** `ESC-CLOSE-20260928-02` (Release Planning `§-1.2` Option(b) rebalance-equivalence precedent-reuse ruling) remains open, SLA 2026-10-01 — due the day after this closure.

---

## Process improvements actioned this run

None. All 3 non-escalated deferred items (the `workforce_capacity.md` worked example, the `claude/roadmap/*` pre-sprint write-scope check, and the agent-mediated signer format mandate) required either a change outside this engine's permitted write scope or design input beyond a mechanical text fix — see Outstanding deferred patches below. Unlike `v9.7`'s closure (which applied Release Planning Friction Item 1 directly, having concrete unambiguous wording and an in-scope target file), no candidate this cycle met both conditions simultaneously.

---

## New files created this run

- `claude/cycles/2026-09-28__release-v9.8/closure_state.json`
- `claude/cycles/2026-09-28__release-v9.8/closure_escalations.md` — 3 decision-required/recurrence escalations raised (see Escalations below)
- `claude/cycles/2026-09-28__release-v9.8/closure_record.md`
- `claude/cycles/2026-09-28__release-v9.8/lessons_learnt_closure.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Cycles carried |
|------|---------|----------------|-------|--------|-----------------|
| `claude/roadmap/workforce_capacity.md` | Effort Band → Days Conversion Table | Add one worked example covering an `XS (<1h)` (hour-denominated) qualifier's canonical-table fallback, so a future session does not need to re-derive the inference (Release Planning Friction Item 3). | Head of Specs Team | Next session with write authority over `workforce_capacity.md` (e.g. Sprint Planning or Roadmap Rebalance) | 1st cycle (new this closure) |
| `claude/system/sprint_planning_prompt.md` (or `roadmap_prompt.md`) | Pre-sprint classification | Add a check that flags any backlog item whose AC names a `claude/roadmap/*` target file (beyond `workforce_capacity.md`) and either grants a per-item write-scope note at sealing time or routes the item to the Roadmap Rebalance Engine directly (Phase 3 Friction Item 2 — hit or near-hit 4 times this cycle). | PMO Lead; Head of Specs Team | Next cycle scoping `sprint_planning_prompt.md`'s pre-sprint classification step, or `BLG-GOV-355`'s own resolution, whichever comes first | 1st cycle (new this closure) |
| `claude/system/execution_prompt.md` | §3.2.A | QA evidence sign-off protocol — mandate the fully-qualified agent-mediated label format whenever the actual reviewer is an agent rather than the literal human role-holder. | Head of Specs Team | Next `execution_prompt.md` revision touching §3.2.A / QA evidence sign-off protocol | 1st carry (`v9.7`→`v9.8`) |
| `claude/system/execution_prompt.md` | STEP 3.1 / §3.1.D | Same-step self-verification read-back for per-story writes generally, to prevent `execution_state.json` top-level summary array/field staleness at the source rather than catching it via downstream backstops. | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 3.1/3.1.D | 3rd cycle — past the `§3.7` two-cycle automatic-escalation threshold. **Escalated** — see `ESC-CLOSE-20260930-02`. |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| PO Modify directive (seat ≥1-2 build-and-ship U-items) unsatisfiable across 5 non-consecutive cycles — idea-intake candidate generation review needed. | Decision required | Product Owner | Ruling needed on whether idea-intake windows adequately prompt for genuine build-and-ship candidates. Tracking: `ESC-CLOSE-20260930-01`, SLA 2026-10-03. |
| `execution_state.json` top-level summary array/field staleness — 3rd recurrence, no structural fix shipped. | Recurrence escalation (`§3.7` mandatory) | Head of Specs Team | Ruling needed on a STEP 3.1/3.1.D self-verification read-back mechanism, or an alternative structural fix. Tracking: `ESC-CLOSE-20260930-02`, SLA 2026-10-03. |
| `delivery_verification_prompt.md §7` Known Deviations sync note scope ambiguity for QA-evidence `Pass_with_deviation` items. | Governance-prompt scope ambiguity | Head of Specs Team | Ruling needed on whether such items should be treated as a STEP 3-equivalent deviation or remain a QA-evidence-only exempt category. Tracking: `ESC-CLOSE-20260930-03`, SLA 2026-10-03. |

---

## Carry-Forward
Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Four open decision-required/recurrence escalations (`ESC-CLOSE-20260928-02`, `ESC-CLOSE-20260930-01`, `-02`, `-03`) are outstanding at this closure — one due 2026-10-01, three due 2026-10-03. | If any breaches SLA before the next routine invocation reads `.claude_current_state.json.open_escalations`, the `BLOCKED_SLA_BREACH` rule (`shared_standards.md` IMP-40) applies on the next invocation. | Post-Ship Closure / any next-invoked routine |
| 2 | Phase 3 Friction Item 2 (`claude/roadmap/*` write-scope near-misses) is at its 1st carry (raised this cycle). | Watch at the next cycle's closure — a second unresolved carry crosses the `§3.7` two-cycle threshold. | Post-Ship Closure |
| 3 | Phase 4 Friction Item 2 (agent-mediated signer format mandate) is at its 1st carry, unapplied but not currently symptomatic. | Watch at the next cycle's closure — a second unresolved carry crosses the `§3.7` two-cycle threshold. | Post-Ship Closure |
