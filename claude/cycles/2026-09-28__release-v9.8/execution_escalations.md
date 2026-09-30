Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-30 (ESC-EXEC-20260930-02 added and resolved same-session)

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

## ESC-EXEC-20260930-01

- **Raised at:** 2026-09-30T08:16:52Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-28__release-v9.8
- **Step:** STEP 3.1.D
- **ST/EPIC item:** ST-38 / EPIC-06
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-38 (`BLG-GOV-351`) requires deciding which governed routine owns firing the 90-day post-ship AI feature usage review (`BLG-FEAT-59/60/63`, `BLG-FE-84`, `BLG-OPS-88`, `BLG-GOV-140/141/142` cluster — found 4 days overdue at `2026-09-28__scheduled`'s roadmap rebalance, with no trigger mechanism). `sprint_backlog.md`'s own Notes for ST-38 (RISK-02) require this design decision to be resolved by Head of Specs Team / PMO Lead as a first sub-step before the build sub-step begins — not engine-determinable per the sealed sprint backlog's own `delegated_decision` classification.
- **Owning authority:** Head of Specs Team; PMO Lead
- **Unblock criteria:** Head of Specs Team / PMO Lead records which routine owns firing this review (post-ship closure's own cadence checks vs. a standalone lightweight scheduled cadence doc vs. both), so the trigger mechanism can be built against a locked design.
- **SLA due-by:** 2026-10-01T08:16:52Z
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** Head of Specs Team / PMO Lead (2026-09-30T08:16:52Z, in-session via `AskUserQuestion`): Post-Ship Closure gets a new mandatory STEP (alongside its existing always-run STEPs 11/12/12.5). Implemented as `post_ship_closure.md` STEP 12.6 (v2.35→v2.36) — scans `claude/backlog/backlog.md` via `scripts/scan_backlog_gate_conditions.py` for a lapsed AI-feature-usage-review-shaped gate on every cycle close, surfaces it in the Advisory Summary if due, and files (or confirms already filed) a tracking backlog item. Trigger mechanism only, per this story's own scope — does not conduct the review itself.

## ESC-EXEC-20260930-02

- **Raised at:** 2026-09-30T09:12:04Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-28__release-v9.8
- **Step:** STEP 3.1.D
- **ST/EPIC item:** ST-33 / EPIC-06
- **Trigger type:** Write-Scope
- **Blocking statement:** ST-33 (`BLG-GOV-341`) requires persisting the STEP 7.2 role-share tally as a structured history file. The natural location, mirroring `product_value_ratio_history.md`'s own precedent, is `claude/roadmap/role_share_history.md` — but `execution_prompt.md` §7's write-scope restriction only carves out `claude/roadmap/workforce_capacity.md` (BLG-GOV-337) for direct engine writes to `claude/roadmap/*`, and that ruling explicitly states it extends to no other roadmap file. `sprint_backlog.md`'s ST-33 Notes field does not name a target path or authorise a `claude/roadmap/*` write — only "History backfilled for the last 3 cycles (explicit AC)." Not engine-determinable: proceeding would repeat the same class of out-of-scope write already self-corrected once earlier this session (`current_roadmap.md`).
- **Owning authority:** PMO Lead (ST-33's Owner)
- **Unblock criteria:** PMO Lead records where the persisted history file should live given the write-scope conflict.
- **SLA due-by:** 2026-10-02T09:12:04Z
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** PMO Lead (2026-09-30T09:12:04Z, in-session via `AskUserQuestion`): file a backlog item deferring the canonical `claude/roadmap/role_share_history.md` placement to the roadmap engine (`BLG-GOV-353`); this sprint, deliver the backfilled data and computation script at an in-scope interim location (`claude/cycles/2026-09-28__release-v9.8/role_share_history.md`). `roadmap_prompt.md` §7.2 is **not** updated this sprint — that change is deferred to `BLG-GOV-353`'s resolution, since it would read from a file this engine has no authority to create. ST-33 closes with this AC-half deferred and documented, not silently dropped.
