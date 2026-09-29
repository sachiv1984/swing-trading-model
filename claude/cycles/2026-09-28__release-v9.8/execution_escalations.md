Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-29

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
- **Disposition:** Open
- **Resolution summary:**

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
- **Disposition:** Open
- **Resolution summary:**
