**Owner:** Head of Specs Team
**Status:** Active
**Release:** v7.7
**Cycle:** 2026-07-21__release-v7.7
**Last Updated:** 2026-07-21

---

# Stage 4 Backlog Slice — v7.7

<!-- release-plan-marker: RP:v7.7:2026-07-21__release-v7.7 -->

EPIC-01 through EPIC-04 are **conditional**, not firm — see `release_plan.md` RISK-02. Sprint Planning may not seal these stories until `run design-gate --cycle 2026-07-21__release-v7.7` PASSes (all 4 carry observable UI acceptance criteria). EPIC-05 through EPIC-11 have no Design Gate dependency — no observable UI acceptance criteria.

`BLG-FEAT-73` and `BLG-FEAT-74` are named `v7.7` anchor items on `current_roadmap.md` §3 but are **excluded** from this slice — see `release_plan.md` §Scope "Items explicitly deferred" and `decisions--2026-07-21__release-v7.7.md`. This slice, not the roadmap anchor list, is the sole authoritative scope source for Sprint Planning.

## EPIC-01 — SI-04 Strategy Version Comparison
**Maps to:** S2-01
**Backlog source:** `BLG-FEAT-75`
**Sequencing:** Conditional on Design Gate PASS (RISK-02); sequenced first among design-gated items (largest effort); no blocking dependency

### ST-01 — Build SI-04 strategy-version performance comparison view
**Acceptance Criteria:**
- User can select two `strategy_rules.md` versions and see a side-by-side performance comparison for trades executed under each
- Comparison includes at minimum win rate, average R, and compliance rate per version
- Surfaced as a new panel in the Arc 5 compliance UI (via `BLG-FE-59`'s shared extension point) and/or a dedicated comparison view
- No trade-volume gate applies (PO decision, `decisions--2026-07-21__release-v7.7.md`)

---

## EPIC-02 — Consolidate notification/digest surfaces
**Maps to:** S2-02
**Backlog source:** `BLG-FE-114`
**Sequencing:** Conditional on Design Gate PASS (RISK-02); depends on `BLG-FE-112` (already shipped — audit basis only, no live dependency)

### ST-02 — Remove nav duplication and unify digest/notification concepts
**Acceptance Criteria:**
- No two nav entries route to the same page without visual indication they're the same
- Weekly Digest is discoverable from the same nav grouping/tab bar as Alerts/Notifications
- Weekly Digest's alert-count values link to the corresponding filtered notification history view
- "Daily Portfolio Summary" (notification preference) and "Weekly Digest" (page) concepts unified or clearly differentiated

---

## EPIC-03 — Confirm AiDailyBriefing light-theme rendering
**Maps to:** S2-03
**Backlog source:** `BLG-FE-113`
**Sequencing:** Conditional on Design Gate PASS (RISK-02); standalone, no dependencies

### ST-03 — Staging check and fix AiDailyBriefing light-theme contrast
**Acceptance Criteria:**
- Staging check performed and result recorded (pass/fail) for `AiDailyBriefing.js`/`Section` light-theme rendering
- If fail: explicit light-mode class pairs added (e.g. `bg-white dark:bg-slate-900`), verified in both themes
- If pass: item closed with staging evidence, no code change needed

---

## EPIC-04 — Shared toast/notification primitive for alert-style UI
**Maps to:** S2-04
**Backlog source:** `BLG-FE-120`
**Sequencing:** Conditional on Design Gate PASS (RISK-02); standalone, no dependencies (enabler for `BLG-FE-116`, out of this release's scope — RISK-03)

### ST-04 — Build shared "standing alert" component distinct from transient toast
**Acceptance Criteria:**
- Component built and documented in `design_system.md`
- At least one integration point identified for `BLG-FE-116`'s future implementation

---

## EPIC-05 — Investigate UX nudge to accelerate SI-02 trade-count gate
**Maps to:** S2-05
**Backlog source:** `BLG-FEAT-80`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (investigation output, no shipped UI)

### ST-05 — Review nudge feasibility for SI-02 gate acceleration
**Acceptance Criteria:**
- Review completed assessing whether a lightweight in-app nudge would meaningfully accelerate SI-02 gate clearance, given `BLG-FE-109` has been in production a full sprint cycle (shipped v7.3, 2026-07-16)
- Recommendation recorded: nudge feature proposed (with scope sketch), or explicit "no action — time-gated only" conclusion

---

## EPIC-06 — CI curl response validation (daily-snapshot.yml)
**Maps to:** S2-06
**Backlog source:** `BLG-OPS-108`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-06 — Add response validation to daily-snapshot.yml curl calls
**Acceptance Criteria:**
- `--fail` (or explicit status/body validation) added to all three curl invocations (Run Position Analysis, Create Portfolio Snapshot, Generate Signals) in `daily-snapshot.yml`
- A broken write path now surfaces as a failed CI run rather than a false-green status
- Other workflows posting to business endpoints audited for the same gap (confirm `backtest.yml`'s existing Python status-code validation is sufficient)

---

## EPIC-07 — PT-04 §13 compliance review (retroactive)
**Maps to:** S2-07
**Backlog source:** `BLG-GOV-28`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-07 — Run retroactive §13 compliance review against shipped PT-04
**Acceptance Criteria:**
- §13 checklist run against PT-04's shipped implementation (Setup Quality Score scoring algorithm + API endpoint)
- PASS/FAIL determination documented, with any binding conditions recorded
- Sign-off recorded by Head of Specs Team

---

## EPIC-08 — numpy-scalar regression coverage for create_rebalance_exit_signal
**Maps to:** S2-08
**Backlog source:** `BLG-QA-104`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-08 — Add automated regression test for numpy-scalar handling
**Acceptance Criteria:**
- Automated test added confirming `create_rebalance_exit_signal` (backend/database.py) safely handles numpy scalar inputs via `decimal_to_float()` upstream
- Test guards against recurrence of the PR #971 defect class (numpy≥2.0 scalar `repr()` reaching a raw psycopg2 INSERT)

---

## EPIC-09 — Nightly backtest job idempotency check
**Maps to:** S2-09
**Backlog source:** `BLG-BE-63`
**Sequencing:** Before EPIC-10; no Design Gate dependency (no UI)

### ST-09 — Verify nightly backtest job is safe against double-run/retry
**Acceptance Criteria:**
- Idempotency confirmed by test or code review — a retry or manual re-trigger must not produce duplicate or divergent results
- Any gap found filed as a P1/P2 correctness item per its severity

---

## EPIC-10 — Nightly backtest job monitoring/alerting
**Maps to:** S2-10
**Backlog source:** `BLG-OPS-110`
**Sequencing:** After EPIC-09; no Design Gate dependency (no UI)

### ST-10 — Add monitoring/alerting for nightly backtest failures or anomalies
**Acceptance Criteria:**
- Monitoring/alerting mechanism added for nightly backtest job failures or output anomalies
- Confirmed to fire on a simulated failure/anomaly

---

## EPIC-11 — Automate endpoint-count drift check (CLAUDE.md §2)
**Maps to:** S2-11
**Backlog source:** `BLG-QA-102`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-11 — Add CI lint step for router-decorator vs. SystemStatus.js fallback count
**Acceptance Criteria:**
- Lint step added to `quality_gate.yml` counting `@router` decorators across `backend/routers/` vs. the hardcoded fallback constant in `SystemStatus.js`
- Fails on a synthetic mismatch test case
- Passes on current repository state
