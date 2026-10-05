Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-05

# QA Evidence Log — EPIC-05

**EPIC:** EPIC-05 — Spec & Data-Model Debt Clearance
**Cycle:** 2026-09-30__release-v9.9
**Sprint goal:** Ship a single canonical ATR/stop-recalculation implementation with timestamp visibility on `GET /positions` (`BLG-BE-135`), while clearing the queued backend, security, QA, governance, spec, and frontend debt items that make up the rest of v9.9's full-capacity scope.
**Test scenarios used:** `tests/test_check_data_model_drift.py`

## Process Deviation — Merged to main via EPIC-02's PR without its own merge gate

This EPIC's story commits were never merged through an EPIC-05 PR. They were made on the same linear branch history as EPIC-04's, which EPIC-02's branch was later cut on top of, so PR #1886 (merged as `362ff619`) carried them into `main`. Neither PR #1886's body nor `qa_evidence_EPIC-02.md` named any EPIC-05 story, so none of this EPIC's work received a Director of Quality review or Product Owner acceptance before reaching `main`.

- **Commits affected (this EPIC):** `3677d86e` (ST-33), `ebc23c14` (ST-34), `e0026238` (ST-31 escalation), `62eebdd8` (ST-32), `241db980` (ST-29/ST-30 delegation), `aba5e44b` (ST-28), `9bc5b07e` (ST-28 record).
- **Rule breached:** CLAUDE.md §2 — story commits must land on the branch matching their EPIC prefix; never merge a PR without QA sign-off and Product Owner acceptance.
- **State staleness also found:** `execution_state.json` still showed ST-33/ST-34 as `not_started` although both commits were on `main`. Backfilled 2026-10-05 (SHA, authored-timestamp `completed_utc`, spec references, `deviations_filed`) after re-verifying both stories' AC on `main`.
- **Disposition (user direction, 2026-10-05):** retroactive merge gate. The code stays on `main`; the sign-off block below is left blank for the Director of Quality. Product Owner acceptance must also be recorded. Also recorded in `qa_evidence_EPIC-02.md` and `qa_evidence_EPIC-04.md`.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-28 | `scripts/check_data_model_drift.py` | Read-only drift detector comparing the live schema with `data_model.md`; lists undocumented and missing objects. Of the 5 known divergence classes, the 2 still live (orphaned columns BLG-SPEC-150; missing index BLG-SPEC-148, still applying on staging) are reproduced. The other 3, already resolved in docs and live, are correctly reported clean. New findings filed as BLG-SPEC-178. | Covers AC-01 (5 known divergences reproduced), AC-02 (output lists undocumented and missing objects) | Pass with notes — 3 of 5 divergence classes no longer exist live, so the tool reports them clean rather than reproducing them | None (BLG-SPEC-178 incidental finding) |
| ST-29 | `docs/specs/data_model.md#DS-24` | 4 orphaned, always-NULL `positions` columns (`atr_value`, `stop_price`, `fees`, `pnl_percent`) dropped live by the user (write credential) on staging then production, after a NULL pre-check (staging 2/2 rows, production 27/27 all NULL); no `CASCADE`; verification returned 0 columns in both. Code paths re-verified first (the analytics `stop_price` key is an alias of `positions.initial_stop`). `data_model.md` v2.47: DS-24 migration record with all outputs; orphaned-column notes point to it. | Covers AC-01 (columns no longer exist live — verification output recorded), AC-02 (Migration History records the drop) | Pass | None (DEL-20261001-02 Unblocked in-session) |
| ST-30 | `docs/specs/data_model.md#DS-23`, `docs/specs/data_model_positions_dictionary.md` | Disposition (agent-mediated Data Model & Domain Schema Owner): re-apply `NOT NULL` — no write path produces NULL and `exit_position()` raises on one. Applied live by the user on staging then production (pre-check 0/0 NULL rows; now `is_nullable = NO`). Both environments had no column default although the doc said `DEFAULT 0`; the Product Owner chose no default (option A). `data_model.md` v2.48 and the dictionary v0.2 corrected; the manual chart-QA seed (`backend/test_data/seed_chart_test_data.sql`), the only insert omitting the column, now passes `fees_paid` (all 12 seeded totals equal shares × price/100 (prices in pence), so 0.00 is the true fee). BLG-SPEC-180 filed. | Covers AC-01 (disposition recorded with reasoning), AC-02 (doc and live schema agree — NOT NULL, no default, both environments) | Pass | None (DEL-20261001-03 Unblocked in-session) |
| ST-31 | `docs/specs/metrics/si02_drift_score.md#2.4`, `claude/roadmap/current_roadmap.md` | One line added to `current_roadmap.md`'s SI-02 gate confirmation status block cross-referencing the canonical "linked trade plan" definition (Head of Specs Team write-scope ruling ESC-EXEC-20261001-05); `si02_drift_score.md` §2.4's stale "deferred" note replaced. Inserted paraphrase checked against §2.4's text. | Covers AC-01 (SI-02 field cross-references the definition), AC-02 (v9.7 ST-23's AC now fully met) | Pass | None (ESC-EXEC-20261001-05 Resolved) |
| ST-32 | `docs/specs/data_model.md#DS-19` | DS-19 Verification status rewritten to state what was confirmed live on staging, and when: both CHECK constraints and the unique index, via read-only user-approved queries. Header/footer version drift fixed in the same file. | Covers AC-01 (no "never run" claim; states what/where/when), AC-02 (header/footer versions in sync) | Pass | None |
| ST-33 | `docs/specs/api_contracts/ai_endpoints.md`, `docs/ops/external_api_dependency_register.md` | Corrected 4 citations in `ai_endpoints.md` plus CFM-03 in the dependency register from `BLG-BE-128` to `BLG-BE-129`. Documentation only. | Covers AC-01 (no misattributed BLG-BE-128 remains — re-verified by grep 2026-10-05), AC-02 (BLG-BE-128's own references untouched) | Pass — text-only change, verified by code review per CLAUDE.md §2's FI-P3-02 exception | None |
| ST-34 | `docs/specs/frontend/pages/notifications.md`, `docs/testing/alert_thresholds_empty_state_scenarios.md` | Dropped the trailing period from both empty-state headings in the spec and the scenario doc, matching shipped code and `design_system.md` §Data States. DEV-v9.7-ST05-01 marked Resolved citing ST-34/BLG-SPEC-169. | Covers AC-01 (both headings without trailing period — re-verified by grep 2026-10-05), AC-02 (DEV-v9.7-ST05-01 resolved with this item's ID) | Pass — wording-only, verified by code review per CLAUDE.md §2's FI-P3-02 exception | None (closes DEV-v9.7-ST05-01) |

**QA test coverage:**
- Scenarios run: `tests/test_check_data_model_drift.py` (ST-28). Re-run retroactively 2026-10-05 together with EPIC-04's tests: 22 passed.
- Regression areas checked: `data_model.md` (DS-19, version header/footer), `ai_endpoints.md`, dependency register, `notifications.md` empty states
- Known deviations: None found — all 7 stories' deviation checks completed with nothing new to file. ST-34 closed the pre-existing DEV-v9.7-ST05-01. Process deviation above (merge-gate bypass) recorded separately; it is not a spec deviation.
- Re-run 2026-10-05 on `exec/2026-09-30__release-v9.9/EPIC-05` @ `14051c3e`: `tests/test_check_data_model_drift.py` plus `tests/test_check_orphaned_specs.py` and `tests/test_generate_spec_debt_dashboard.py` — 36 passed. ST-28's row above reflects the live state when it shipped: the orphaned-column class it reproduced has since been removed by ST-29, and `fees_paid` nullability by ST-30.
- Live-change evidence: ST-29 and ST-30's pre-check, change and verification outputs for both staging and production are recorded verbatim in `data_model.md` DS-24 and DS-23.
- Same-EPIC cross-story testing-gap check (AUD-2026-09-28-002): no story in this EPIC filed a testing-gap backlog item, so no sibling story owes an equivalent one.
- Frontend testing gate: N/A — no file under `src/` changed in this EPIC (the seed file is backend test data).
- Story-level authority sign-offs (BLG-GOV-14 consolidation), all cleared: ST-29, ST-30 — Data Model & Domain Schema Owner (agent-mediated content) with live application by the user, and the Product Owner's no-default decision (ST-30). ST-31 — Head of Specs Team write-scope ruling (agent-mediated). ST-32 — read-only live staging queries, user-approved.

---

## Standard Sign-Off Block

> Autonomous class (BLG-GOV-19) not applicable: Criterion 1 is unmet — ST-29/ST-30 were live schema changes and ST-32 used live staging queries (BLG-GOV-335). The merge-gate bypass above is reviewed here as part of the retroactive gate. Agent-mediated Director of Quality sign-off authorised by the user on 2026-10-05 ("go ahead with the sign-offs and PRs"), superseding the earlier note that left this block for a human reviewer; Product Owner acceptance remains with the human Product Owner.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend-visible change in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-10-05
- Comments:
  Agent-mediated Director of Quality review (user-authorised 2026-10-05), read-only against EPIC-05 @ d53b77e6, covering ST-28..ST-34. It also serves as the retroactive merge gate for ST-28/32/33/34, which reached main via PR #1886 (process deviation recorded above). All 7 stories' AC were re-verified against stage4_backlog_slice.md.

  ST-29/ST-30 checks:
  - Every INSERT INTO positions in backend/, scripts/, tests/ and backend/test_data/ supplies fees_paid or is safe. create_position() is fed only by the numeric fee calc; seed_portfolio_trades.sql passes 11.95; the SQLite migration test uses its own schema.
  - The chart seed's 12 inserts each have 14 columns and 14 values. total_cost = shares x price/100 in every row, so fees_paid 0.00 is correct.
  - No backend code reads or writes atr_value, stop_price, fees or pnl_percent on positions, and no startup DDL re-adds them.
  - data_model.md v2.48: CREATE TABLE, the Fields row, DS-23, DS-24, the v1.6 note and the header/footer agree (NOT NULL, no default). Dictionary v0.2 matches.
  - The live pre-check, change and verification outputs are user-attested and recorded verbatim in DS-23/DS-24. They were not re-queried, because this review had no database access.

  ST-31: the roadmap line matches si02 §2.4 and cites ESC-EXEC-20261001-05 (Resolved).

  General checks:
  - spec_references resolve.
  - deviations_filed is true on all 7 stories.
  - No P0/P1 deviations; no open escalations, blocked items or delegated items.
  - Frontend testing gate N/A: no src/ or tests/e2e/ file changed.
  - No same-EPIC testing gap.
  - Autonomous class correctly not applied (BLG-GOV-335).

  Tests (stub DATABASE_URL): drift/orphan/dashboard tests 36 passed; full tests/ 2054 passed, 16 skipped, 0 failed.

  Non-blocking findings:
  (1) metrics_definitions.md:687 and :1110, and the database.py:2421 docstring, still cite the dropped positions.stop_price column. No runtime impact, because the action-rate metric is not computed yet. Filed as BLG-SPEC-181.
  (2) The ST-30 row's "shares x price" wording — corrected to "shares x price/100 (pence)" in this commit.
  (3) Cosmetic execution_state/backlog header staleness (ST-33/34 substep; backlog.md header "pending live").

  Product Owner acceptance is still required.
