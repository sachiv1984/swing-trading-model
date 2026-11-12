**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-11-12
**Cycle:** 2026-11-11__release-v9.17
**Release:** v9.17
**Sprint Goal:** Ship Site Structure & Usability Phase 3 complete (decision-first Positions page with narrow-screen cards, one warning strip and one grace view; the single Journal area; one Performance page; section indexes on Trade Plan and Strategy Benchmark; the semantic colour token sweep), finish Phase 2's Stops moved group, and fix the four v9.16 Trade Plan found defects.
**Backlog Slice Source:** Original: `claude/cycles/2026-11-11__release-v9.17/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-01, ST-03/ST-04, ST-06, ST-07 and ST-14)

# Sprint Backlog — 2026-11-11__release-v9.17

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-04 → EPIC-07 → EPIC-06 → EPIC-05 → EPIC-02 → EPIC-03.
- **EPIC-01** goes first. It owns `Positions.js`, `positions.md` and the Dashboard Card 3 / Risk Dashboard grace links.
- **EPIC-04** goes second. It owns `data_model.md`, `openapi.yaml` and `position_endpoints.md` (ST-09), and rebases the Today list (ST-10) on EPIC-01's Dashboard changes.
- **EPIC-07** goes third. ST-19 lands on EPIC-01's `Positions.js`; ST-20 runs the drift detector after EPIC-04's migration; ST-18 owns the governance-file bumps.
- **EPIC-06** goes fourth. Backend and workflow only; it rebases on EPIC-04's contracts if it touches any.
- **EPIC-05** goes fifth. It owns `TradePlan.js` and `trade_plan.md` (ST-12, ST-14).
- **EPIC-02** goes sixth. ST-07 rebases on EPIC-05's `TradePlan.js` and takes the next `trade_plan.md` version; ST-06 merges after ST-05 (RISK-04).
- **EPIC-03** goes last. ST-08 regenerates both themes' visual baselines over every other UI EPIC (RISK-02).

**Fallback:** EPIC-05 may merge after EPIC-02 if EPIC-02 is ready first; ST-12/ST-14 then rebase on ST-07's section index. EPIC-07's ST-18 may merge on its own early (it touches no product file); ST-19 must still follow EPIC-01. EPIC-03 may never merge before another UI EPIC.

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch checks whether the file exists before creating its own. If it exists, the branch appends its own section and never overwrites. No story is `deferred_at_planning`.

**Shared files across EPICs:**
- **`src/pages/Positions.js`, `positions.md`** (EPIC-01 ST-01–ST-04; EPIC-07 ST-19; EPIC-03 ST-08): EPIC-01 owns; later EPICs rebase.
- **`src/pages/TradePlan.js`, `trade_plan.md`** (EPIC-05 ST-12, ST-14; EPIC-02 ST-07; EPIC-03 ST-08): EPIC-05 owns; ST-07 takes the next spec version.
- **Dashboard components and `dashboard.md`** (EPIC-01 ST-04; EPIC-04 ST-10): EPIC-01 owns; EPIC-04 rebases.
- **`data_model.md`, `openapi.yaml`, `position_endpoints.md`, `api_changelog.md`** (EPIC-04 ST-09; EPIC-05 ST-11 if recorded; EPIC-07 ST-20 reads): EPIC-04 owns. CLAUDE.md §8 step 3.
- **`navigation.md`, command palette, `glossary.md`** (EPIC-02 ST-05, ST-06): EPIC-02 internal; ST-06 after ST-05.
- **`release_planning_prompt.md`, `OPERATIONAL_GUIDE.md`, `prompt_change_log.md`** (EPIC-07 ST-18; spec-bump rows from EPIC-01/02/05): EPIC-07 owns. CLAUDE.md §6 and §8 step 2a, checked per co-bumped file.
- **Visual baselines** (both themes): EPIC-03 regenerates last.
- **`claude/backlog/backlog.md`:** follow-ups via `/backlog-add` only; run `scripts/check_backlog_item_integrity.py` after each §8 merge (step 2c).

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — Site Structure & Usability Phase 3: Positions Redesign (build-and-ship)

**Maps to:** S2-01 – S2-04
**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 7.50 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Decision-first Positions table

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (first in EPIC-01; ST-02 and ST-03 follow)

**Notes:** Addendum: near stop = within 5% of the trailing stop, post-grace (Risk Dashboard band); in-grace positions never enter the stop tiers. Locked `positions.md` v2.25 §Decision-First Table; design `positions-decision-first/decision_record.md` §2–§3, §10. Owns `Positions.js` (RISK-01). Head of UX & Design reviews the build against the spec; Head of Engineering implements.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-02 — Card layout for Positions on narrow screens

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01

**Notes:** `positions.md` v2.25 §Responsive Behavior; design §4. Same urgency order and leading fields as ST-01. Note BLG-SPEC-230 (two default views named in `positions.md`) is filed separately, not in scope.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-03 — Combine the four banners above the Positions table into one strip

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-01

**Notes:** Addendum: ST-03 builds the strip with the grace entry expanding to today's `GracePeriodAlertZone` content; ST-04 then replaces it with `GracePeriodView`. `positions.md` v2.25 §Warning Strip; design §6.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-04 — Show grace period in one place, linked from the others

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-03

**Notes:** Addendum: `GracePeriodView` lists every in-grace position, no dismiss; Dashboard Card 3 and the Risk Dashboard Grace panel link to `/Positions?grace=open`. Days-remaining pills, Today-list "Grace ends today" rows and "Not enforced (grace)" cells stay. Design gate obligations: remove `grace_alert_dismissed_*` reads; turn `positions.md` §Grace Period Alert Zone into a "Superseded" stub. Specs: `positions.md` v2.25, `dashboard.md` v4.2, `risk_dashboard.md` v0.1.16.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-02 — Site Structure & Usability Phase 3: Journal & Performance Consolidation (build-and-ship)

**Maps to:** S2-05 – S2-07
**Owner:** Head of Engineering; Head of UX & Design; Metrics Definitions & Analytics Owner
**Estimated effort:** 9.50 days
**Risk IDs:** RISK-01, RISK-04
**Execution sequence:** 6

#### ST-05 — Build the single Journal area

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 3.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None (merges before ST-06)

**Notes:** Locked `journal.md` v1.0 (JA-01..JA-21). Redirects from old routes; Positions journal view change. Shares `navigation.md` and the command palette with ST-06 (RISK-04).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-06 — Merge Reports and Performance Analytics into one Performance page

**Owner:** Head of Engineering; Head of UX & Design; Metrics Definitions & Analytics Owner
**Estimated effort:** 3.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-05 (merge order); Head of UX & Design approval of `performance.md` before the build

**Notes:** Addendum: build may not start until `docs/specs/frontend/pages/performance.md` exists, meets `performance-page-brief/decision_record.md` §2 and carries a dated Head of UX & Design approval. Metrics Definitions & Analytics Owner confirms KPI definitions (AC 2, dated in QA evidence). Record whether `BLG-FE-237` (Reports tab bar overflow) AC is met, for `groom backlog`. Design gate obligations: retire `reports.md` and the Performance Analytics part of `analytics.md`; revise `navigation.md`, command palette, `glossary.md` §UI Labels.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-07 — Use tabs or sections on the long single-scroll pages

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (rebases on EPIC-05's `TradePlan.js`)

**Notes:** Addendum: a sticky in-page section index, not tabs; on Strategy Benchmark only the Benchmark tab gets the index. `trade_plan.md` v1.25 §5g, `strategy_benchmark.md` v0.10 §3a; design `long-page-section-index/decision_record.md`. Thesis AI controls unchanged.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-03 — Site Structure & Usability Phase 3: Semantic Colour Token Sweep (build-and-ship)

**Maps to:** S2-08
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 3.50 days
**Risk IDs:** RISK-02
**Execution sequence:** 7

#### ST-08 — Move the remaining pages onto the semantic colour tokens

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 3.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** Every other UI EPIC merged (EPIC-01, -02, -04, -05, -07)

**Notes:** **Boundary (RISK-02, PMO Lead and Product Owner, 2026-11-12):** all of `src/pages/` (436 dark-only classes in 21 files, 2026-11-11), plus any component that fails axe `color-contrast` on a routed page in the light theme. AC "no bare `text-white` outside coloured fills" applies to `src/pages/`. Component-only remainder: **BLG-FE-288**. Tokens per `design_system.md` v1.26. Regenerates visual baselines for both themes. On completion `BLG-FE-224`/`BLG-FE-242` are superseded (note for Post-Ship Closure).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-04 — Site Structure & Usability Phase 2 Completion: Stops Moved Group

**Maps to:** S2-09 – S2-10
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Estimated effort:** 2.00 days
**Risk IDs:** RISK-03
**Execution sequence:** 2

#### ST-09 — Record when the nightly job last moved each position's stop

**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None (first in EPIC-04)

**Notes:** Migration (`stop_last_moved_date`, `previous_stop`), nightly-job write only when the §7.3 ratchet moves the stop, read-only on `GET /positions`; `position_endpoints.md` + `openapi.yaml` in the same commit. Remove `RecentActivityCard.js` dead branch. Production migration at deploy is a Human-Delegation deploy step (Infrastructure & Operations Owner, RISK-03); staging first. Owns `data_model.md`/`openapi.yaml` ahead of EPIC-05/EPIC-07.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-10 — Today list "Stops moved" group: TL-09 and TL-10

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** ST-09

**Notes:** Locked `dashboard.md` §1B TL-09/TL-10. Playwright in light and dark themes. AC 2 is a Post-Ship Closure banner on `BLG-FE-254`, not an in-sprint write.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-05 — Trade Plan Found Defects (v9.16 Carry-Forward)

**Maps to:** S2-11 – S2-14
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 2.90 days
**Risk IDs:** RISK-01, RISK-03, RISK-05, RISK-07
**Execution sequence:** 5

#### ST-11 — Move a linked trade plan to `closed` when its position closes

**Owner:** Head of Engineering
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Full-exit path sets the linked plan `closed` (best-effort); partial exit leaves it `active`. Backfill is idempotent, tested in CI (pytest) and on staging first; the production run is a deploy step (RISK-03). Lifecycle Playwright asserts the "Closed" badge.

**Staging-only ACs:** AC 2 (existing `active` plans whose position is closed are backfilled): the backfill logic is verified in CI; the production run is `post-merge`, tracked by **BLG-BE-211** (this story's source item, which stays open until the production row count is recorded).

**Status at sprint open: ready**

---

#### ST-12 — Reset the Trade Plan pre-entry acknowledgement when the check result changes

**Owner:** Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** RISK-05 decision (resolved 2026-11-12)

**Notes:** **RISK-05 decision: option (a), clear on change** (Strategy Rules & System Intent Owner, 2026-11-12): `pre_entry_override_acknowledged` set `false` whenever the result key (`advisory_status` + `{rule, status}` pairs) changes; Trade Entry read path unchanged. Delete option (b) from `trade_plan.md` §5e. UI per `trade-plan-found-defects/decision_record.md` §2.1 (`acknowledgement-reset-note`). Record whether the change meets `BLG-FE-269` AC 1 (RISK-07). Owns `TradePlan.js` ahead of EPIC-02 ST-07.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-13 — Pass the market from Research View's "Create Trade Plan" so a UK plan is not created as US

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** `/TradePlan?ticker={ticker}&market={market}`; "View full plan" uses edit mode (confirm by test). `research_view.md` v1.5 §4.7; design §3.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-14 — Pre-fill the Trade Plan stop from the §5 suggested stop and flag a typed stop that differs

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (shares `TradePlan.js` with ST-12)

**Notes:** Addendum: the pre-fill uses the Signal Context panel's "Suggested stop" (signal `initial_stop`, else `current_price − 5 × atr_value`) from one shared helper; the stored-stop line compares with Planned Entry − 5 × `atr_value`. `trade_plan.md` v1.25 §5a.3, §5f. Closes the `DEV-v9.16-ST27-01` Known Deviations row (AC 4; spec file, not a named-file write). Strategy Rules & System Intent Owner consulted.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-06 — Market-Data Reliability & Sizing Correctness

**Maps to:** S2-15 – S2-17
**Owner:** Infrastructure & Operations Owner; Head of Engineering; FinOps & Resource Architect
**Estimated effort:** 2.00 days
**Risk IDs:** RISK-03
**Execution sequence:** 4

#### ST-15 — Find out why most on-demand Yahoo calls fail on production (earnings, positions, gap risk, research)

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (ST-16 follows)

**Notes:** Human-Delegation at sprint start: production `api_call_log` breakdown by `endpoint` and ticker for the four features (Infrastructure & Operations Owner). Code fixes proceed regardless. The "what the user sees" check may file follow-ups via `/backlog-add`.

**Staging-only ACs:** AC 1 (recorded cause per feature) needs a production `api_call_log` read: Human-Delegation, in-sprint, not merge-dependent. AC 2 (post-fix production weekly report, failure rate < 10% or documented as expected) `post-merge` (needs 7 days of production data), tracked by **BLG-OPS-217** (this story's source item, which stays open until the report is recorded). AC 3 (`data_pipeline_cost_baseline.md` §4 reflects the post-fix state) `post-merge`, tracked by **BLG-OPS-217**.

**Status at sprint open: ready**

---

#### ST-16 — Alert when weekly market-data call volume exceeds 2× the baseline

**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** ST-15 (soft: reads §4 whatever its state)

**Notes:** Weekly scheduled workflow calling `GET /ops/api-call-attribution?window=weekly`; baseline read from one place; fail loudly like `ai-daily-cost-check.yml`. ACs are test-verified in CI.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-17 — Batch signal sizing can allocate more than available cash once fees are added

**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Size against cash net of estimated fees; unit tests for UK, US and mixed batches.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-07 — Governance, Strategy Copy & Drift Tooling

**Maps to:** S2-18 – S2-20
**Owner:** Head of Specs Team; PMO Lead; Frontend Specifications & UX Documentation Owner; QA & Testing Owner
**Estimated effort:** 0.55 days
**Risk IDs:** RISK-05, RISK-06
**Execution sequence:** 3

#### ST-18 — Release Planning §1.3a: let a gate clearance also set a gate-worded Provisional-Target to TBD

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None (start early)

**Notes:** Head of Specs Team confirms (agent-mediated, §5.3) that the change stays within `ESC-CLOSE-20261007-01`, or records the extension (RISK-06). CLAUDE.md §6 checklist: version bump, OPERATIONAL_GUIDE §14 + phase header, `prompt_change_log.md`; run the prompt size budget check. Owns governance-file bumps.

**Staging-only ACs:** AC 2 (next Release Planning gate scan after a clearance shows no data-quality warning for the cleared item's `Provisional-Target`) `post-merge`, tracked by **BLG-GOV-419** (this story's source item, which stays open until the next Release Planning run that clears a gate).

**Status at sprint open: ready**

---

#### ST-19 — Define or remove the 2R Exit Zone threshold the Positions page states

**Owner:** Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** EPIC-01 on `main` (`Positions.js`); RISK-05 decision (resolved 2026-11-12)

**Notes:** **RISK-05 decision: option (b), reword without a number** (Strategy Rules & System Intent Owner, 2026-11-12). PROFITABLE tooltip: "Advances to Exit Zone when the price is well above the initial risk taken. The app's lifecycle labels mark this; it is not a strategy rule." EXIT ZONE tooltip: "The price is well above the initial risk taken. Review the stop or exit." (`positions-decision-first/decision_record.md` §7). Delete the option (a) row from `positions.md`. No `strategy_rules.md`, constants or lint change; `scripts/check_strategy_copy.py` must pass. Wording-only AC (FI-P3-02): code review of the static text may substitute for staging sign-off.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-20 — Stop check_data_model_drift.py reading index names from rollback blocks

**Owner:** QA & Testing Owner; Data Model & Domain Schema Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** EPIC-04 ST-09 on `main` (run the detector after its migration lands)

**Notes:** Exclude `Reversible:` / `Down Migration` SQL from name parsing; unit test with a rollback-only fixture; document where `--json` output is kept.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units (28.00 ceiling) |
| Total estimated effort (in-scope) | 27.95 days (20 stories, 7 EPICs) |
| Utilisation | 99.8% of the band ceiling. This is above the 95% advisory buffer floor; the Product Owner chose to proceed, 2026-11-12 |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | None. All 20 slice items are in scope; none is conditional. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-05: ST-12 storage option and ST-19 wording option | Strategy Rules & System Intent Owner | No. **Resolved 2026-11-12** (see sign-off below) |
| RISK-02: ST-08 sweep boundary | PMO Lead; Product Owner | No. **Resolved 2026-11-12**; remainder filed as BLG-FE-288 |
| Human-Delegations raised at sprint start: ST-15 production `api_call_log` read; ST-09 production migration and ST-11 production backfill at deploy | Infrastructure & Operations Owner | No |
| ST-06: dated approval of `performance.md` before the build; dated KPI confirmation (AC 2) | Head of UX & Design; Metrics Definitions & Analytics Owner | No |
| Post-merge ACs tracked by BLG-OPS-217 (ST-15 AC 2, AC 3), BLG-BE-211 (ST-11 AC 2 production run), BLG-GOV-419 (ST-18 AC 2): source items stay open until met | Sprint Execution Engine; Post-Ship Closure Engine | No |
| For any other staging-only AC whose sign-off is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (as drafted), 2026-11-12
**Scope confirmed:** Confirmed: 20 stories across 7 EPICs in a single sprint; no conditional or deferred stories, 2026-11-12
**Capacity confirmed:** Confirmed: 27.95 / 28.00 (99.8%), proceeding above the 95% buffer floor, 2026-11-12
**Deferred execution blockers accepted (if any):** N/A (none)
**Release-plan judgement calls:** Confirmed, 2026-11-12: `BLG-BE-205` seated by §1.4c step 1b as a Phase 2 item; `BLG-FE-254` seated as its 0.5d remainder
**Pre-sprint decision RISK-05 (Strategy Rules & System Intent Owner):** Resolved, 2026-11-12. (1) ST-12: option (a), clear the acknowledgement when the check result changes. (2) ST-19: option (b), reword the tooltip without a number; no `strategy_rules.md` §11 write
**ST-08 boundary RISK-02 (PMO Lead and Product Owner):** Resolved, 2026-11-12: all of `src/pages/` plus components failing axe on a routed page in the light theme; component remainder BLG-FE-288
**Post-merge trackers:** Confirmed, 2026-11-12: source items `BLG-OPS-217`, `BLG-BE-211`, `BLG-GOV-419` stay open as trackers
**Pre-seal backlog filings:** BLG-SPEC-230, BLG-SPEC-231 (design gate observations) and BLG-FE-288 (ST-08 remainder), authorised and filed 2026-11-12

### Named-file writes

None. ST-19's option (b) removes the only candidate case (c) `strategy_rules.md` write. No `claude/roadmap/*` write is planned. No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

For information, outside the named-file rule: ST-18 edits `release_planning_prompt.md`, `OPERATIONAL_GUIDE.md` and `prompt_change_log.md` under the CLAUDE.md §6 governance edit checklist.

**Signed off by:** Product Owner
**Date:** 2026-11-12
