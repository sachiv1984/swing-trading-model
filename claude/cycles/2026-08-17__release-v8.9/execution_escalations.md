Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-20 (EPIC-06 merge reconciliation — add/add conflict combining EPIC-04's ESC-EXEC-20260818-01 (+ resolution addendum) and EPIC-06's ESC-EXEC-20260818-02, both filed independently before either branch merged)

# Execution Escalations — 2026-08-17__release-v8.9

Append-only. Never edit a previous entry.

---

## ESC-EXEC-20260818-01

- **Raised at:** 2026-08-18T08:35:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-17__release-v8.9
- **Step:** 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-13 / EPIC-04
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-13 (BLG-QA-150) requires a Product Owner decision on treatment for `trade_plans.setup_type`, which currently has no server-side default or required-field guarantee outside the linked-signal pre-population path in `TradePlan.js`. Any creation path other than "ticker with a matching watchlisted signal" (manual entry, Ticker Universe, Research CTA with no matching signal, direct API use) saves `setup_type: null`, undercounting Arc 6/SI-02's future `win_rate_by_setup_type` analysis. Three treatment options are on the table: (a) make `setup_type` a required form field, (b) add an explicit "Unclassified"/"Other" default so null rows still group predictably, (c) accept as-is with documented rationale.
- **Owning authority:** Product Owner (co-consulted: Frontend Specifications & UX Documentation Owner, per BLG-QA-150's dual ownership and sprint_backlog.md's RISK-04 note)
- **Unblock criteria:** A decision recorded (one of the three options above, or a reasoned variant) with rationale; if a fix is chosen, implemented; Product Owner sign-off.
- **SLA due-by:** 2026-08-19T08:35:00Z (24h — Human-Delegation trigger)
- **Blocks execution:** No — EPIC-04's other stories (ST-12, ST-14, ST-15) proceed independently per execution_prompt.md §3.1.D step 4 ("Continue to next item").
- **Disposition:** Open
- **Resolution summary:** (to be completed on resolution)

---

## ESC-EXEC-20260818-01 — Resolution (Addendum)

- **Refers to:** ESC-EXEC-20260818-01 above. This file is append-only — recording the resolution as a new entry rather than editing the original.
- **Resolved at:** 2026-08-18T08:55:00Z (well within the 24h SLA due 2026-08-19T08:35:00Z)
- **Disposition:** Resolved
- **Resolution summary:** Agent-mediated Product Owner decision (§5.3): option (b) — normalize null/absent/empty `setup_type` to the existing canonical value `"Other"` server-side, in `backend/routers/trade_plans.py::create_plan()`'s `_create()` closure (commit `bdf8fee2`). Rationale: `"Other"` already exists as a canonical, live `SETUP_TYPE_OPTIONS`/`SETUP_TYPES` value in both backend and frontend, so this covers every creation path (frontend and direct API) at the single choke point with no new UI or enum value, and does not trigger a design-gate return per RISK-04. Evidence: `tests/test_trade_plan_setup_type_default.py` (4 new tests, all passing); `docs/specs/api_contracts/trade_plan_endpoints.md` v0.12→v0.13 documents the new default. Full backend suite: 1178 passed, 5 skipped, no regressions. See `execution_state.json` ST-13 for the full sign-off record.

---

## ESC-EXEC-20260818-02

- **Raised at:** 2026-08-18T13:15:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-17__release-v8.9
- **Step:** 3.1 (write-scope self-correction)
- **ST/EPIC item:** ST-21 / EPIC-06
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-21 (BLG-GOV-264) requires "`claude/roadmap/displacement_debt_register.md` created with the seeded content" as AC-1. `claude/roadmap/*` is unconditionally listed as "Must not modify" in `execution_prompt.md` §7's write-scope hard gate, with no exception (unlike `claude/system/*` governance prompts, which CLAUDE.md §6 explicitly sanctions for sprint-story edits, and unlike `claude/backlog/backlog.md`, which has its own narrow explicit carve-out). This engine initially created the file directly (an error, self-caught and reverted before commit) — the file genuinely cannot be created by Sprint Execution Engine, only by a live Roadmap Rebalance Engine invocation (`run roadmap` / `manage roadmap`), which does hold that write scope. This is the same conclusion the original ST-14 design (`claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md`) reached, tracked as `ESC-EXEC-20260727-02` in that (now-sealed) cycle's own `execution_escalations.md`.
- **Owning authority:** Roadmap Rebalance Engine / Head of Specs Team
- **Unblock criteria:** At the next `run roadmap` or `manage roadmap` invocation, `roadmap_prompt.md` STEP 8 (v9.16, already wired by this cycle's ST-21) creates `claude/roadmap/displacement_debt_register.md` on its first trigger (a new displacement candidate is flagged), using the create-if-absent instruction and seed content already in place. If no displacement candidate is flagged for several cycles, Head of Specs Team may create the file directly outside a governed routine instead of waiting indefinitely.
- **SLA due-by:** N/A — Workforce/Capacity-class, no fixed due-by; tracked for the next natural trigger.
- **Blocks execution:** No — the prompt-wiring half of ST-21 (STEP 8 instruction, `roadmap_prompt.md` v9.15→v9.16) is genuinely completable by Sprint Execution and is done; only the physical file-creation half is deferred.
- **Disposition:** Open
- **Resolution summary:** (to be completed when a live Roadmap Rebalance Engine invocation creates the file) — this record supersedes, without touching, the sealed `ESC-EXEC-20260727-02` in `claude/cycles/2026-07-27__release-v7.9/execution_escalations.md` (CLAUDE.md "never modify sealed artefacts" — that cycle has `closure_record.md`/`closure_state.json`, so its own escalation entry cannot be edited or closed from this cycle). When the file is eventually created, both this record AND the original `ESC-EXEC-20260727-02`'s intent are satisfied; the original sealed record should be left as-is (a resolved-in-spirit historical artefact), with the actual live resolution tracked here instead.
