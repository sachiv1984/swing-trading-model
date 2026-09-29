Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-29 (ESC-EXEC-20260929-03 added and resolved same-session)

## ESC-EXEC-20260929-01

- **Raised at:** 2026-09-29T12:06:33Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-28__release-v9.8
- **Step:** STEP 3.1.D
- **ST/EPIC item:** ST-17 / EPIC-04
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-17's scope (BLG-OPS-169) explicitly names 3 alternative implementation vehicles for detecting that staging did not redeploy after a merge (extending `staging-smoke-test.yml`, a new post-merge workflow, or a cycle-close verification step) and defers the choice to implementation. `sprint_backlog.md`'s own Notes for ST-17 require this design decision to be resolved by the Infrastructure & Operations Owner as a first sub-step before the build sub-step begins — no HoST design-session artefact exists yet (LL-v2.2-SP-01 advisory). This is not engine-determinable per the sealed sprint backlog's own classification (`delegated_decision`).
- **Owning authority:** Infrastructure & Operations Owner
- **Unblock criteria:** Infrastructure & Operations Owner records which of the 3 named vehicles to use (or an alternative), including whether/how a build-commit indicator is added to an existing health/status endpoint, so implementation can proceed against a locked design.
- **SLA due-by:** 2026-10-02T12:06:33Z
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** Infrastructure & Operations Owner (2026-09-29T12:35:00Z, in-session via `AskUserQuestion`): extend the existing `staging-smoke-test.yml` scheduled workflow (not a new dedicated workflow, not a cycle-close step); confirm the deployed commit via a new `deployed_commit_sha` field on `GET /health/detailed` (not a Render-deploy-hook-fired confirmation alone). Implemented in commit `78f4a991` — see `docs/ops/staging_deploy_notes.md` §7 for the full design record. Staging-only AC-01 evidence deferred to `BLG-OPS-171` (filed before this EPIC's PR opened, per `sprint_backlog.md` ST-17 Notes).

## ESC-EXEC-20260929-02

- **Raised at:** 2026-09-29T12:06:33Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-28__release-v9.8
- **Step:** STEP 3.1.D
- **ST/EPIC item:** ST-18 / EPIC-04
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-18 (BLG-OPS-170) requires documenting, in `docs/infrastructure/staging_setup.md` §8, which read-only query patterns a governed session may run against the staging DB's read-only role without seeking additional confirmation each time. `sprint_backlog.md`'s own Notes for ST-18 state this is "a security-sensitive policy call — requires Infrastructure & Operations Owner / Cybersecurity & Trust Lead sign-off, not engine-determinable." No HoST design-session artefact exists yet (LL-v2.2-SP-01 advisory).
- **Owning authority:** Infrastructure & Operations Owner / Cybersecurity & Trust Lead
- **Unblock criteria:** Infrastructure & Operations Owner and Cybersecurity & Trust Lead jointly record the pre-approved read-only query-pattern allow-list (scope and any exclusions) so the engine can write it into `docs/infrastructure/staging_setup.md` §8 verbatim.
- **SLA due-by:** 2026-10-02T12:06:33Z
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** Infrastructure & Operations Owner (2026-09-29T12:35:00Z, in-session via `AskUserQuestion`): aggregate counts only (`SELECT COUNT(*)`-shaped, no row-level columns), against a table already named in an existing `current_roadmap.md` gate condition — matching `BLG-OPS-170`'s own drafted scope. Today that's `trade_history`/`trade_plans` (the SI-02 gate's own query). Implemented in commit `f95a4a89` — see `docs/infrastructure/staging_setup.md` §8.

## ESC-EXEC-20260929-03

- **Raised at:** 2026-09-29T14:47:45Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-28__release-v9.8
- **Step:** STEP 3.1.D
- **ST/EPIC item:** ST-29 / EPIC-05
- **Trigger type:** Strategy
- **Blocking statement:** IT-06's original §13 review (`decisions--2026-05-15__release-v3.5--IT-06-section13-review.md`) PASSED on the explicit condition that the Alpaca paper-trading sync is read-only (GET only; "must not include any POST, PUT, PATCH, or DELETE calls to the Alpaca API"). Code review of `backend/services/alpaca_paper_sync_service.py` found this has never been true — the service POSTs a paper order on real position open and DELETEs the paper position on real position close, present since the original ST-02/ST-03 commit (`b496f5ef`, v3.5), not a later scope-creep addition. No follow-up §13 review reconciled this. `po05_section13_preassessment.md` (2026-09-21, PASS) explicitly relies on "IT-06's existing binding conditions (read-only Alpaca access...)" still holding, so this gap could be resting on a false premise there too. `sprint_backlog.md`'s own Notes for ST-29 require the disposition to be recorded by the Strategy Rules & System Intent Owner — not engine-determinable.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** Strategy Rules & System Intent Owner determines whether the shipped mirror-write mechanism (a deterministic 1:1 mirror of the user's own real trade action — idempotent client_order_id, best-effort/never-blocking, zero real capital, no signal/decision logic reads from the paper side) is §13-compliant in substance despite the original record's incorrect "read-only" description, or whether remediation (strip to genuinely read-only, or a fresh review) is required.
- **SLA due-by:** 2026-10-02T14:47:45Z
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** Strategy Rules & System Intent Owner (2026-09-29T14:47:45Z, in-session via `AskUserQuestion`): **Re-affirm PASS, correct the record.** The mirror-write mechanism is §13-compliant in substance — every paper order/close is a deterministic, synchronous mirror of a user-initiated action the system did not decide, never generates or acts on any signal, involves no real capital, and is best-effort/non-blocking on the primary (real) operation. The original review's "read-only" description was a factually incorrect characterisation of an already-compliant mechanism, not a boundary violation requiring remediation. Addendum added to `decisions--2026-05-15__release-v3.5--IT-06-section13-review.md` correcting the technical description and re-confirming PASS under corrected conditions (mirror-write permitted only as a deterministic, idempotent reflection of a user-initiated real-position event; no independently-originated order; no signal path from paper data). `po05_section13_preassessment.md`'s reliance on IT-06's conditions remains valid — the *substance* of those conditions (no autonomous order origination, paper-data isolation) was never actually violated, only their prior written description.
