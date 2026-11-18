**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-11-18
**Cycle:** 2026-11-18__release-v9.18
**Release:** v9.18
**Sprint Goal:** Ship Site Structure & Usability Phase 4 stages 1–2 (Level A keyboard and label fixes, truthful Telegram alert delivery, a one-line quiet-day Dashboard, the two navigation moves, and a readable, linked Weekly Digest with this week's loop), put the first-time-right checks in place before v9.19's design gate, and make position figures correct across native entry, live FX and stock splits.
**Backlog Slice Source:** Original: `claude/cycles/2026-11-18__release-v9.18/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-03, ST-04, ST-07–ST-14, ST-16, ST-17, ST-27, ST-30, ST-33)

# Sprint Backlog — 2026-11-18__release-v9.18

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-04 → EPIC-07 → EPIC-05 → EPIC-06 → EPIC-02 → EPIC-03.
- **EPIC-01** goes first. It owns `accessibility-axe-scan.spec.js`/`runAxeScan`, the alerts contract (ST-03) and `notifications.md`.
- **EPIC-04** goes second. ST-20 rebases on EPIC-01's axe changes. It owns the `src/lib` unit-test job and `positionUrgency.test.js` (ST-19), and every governance-file bump (ST-18, ST-21–ST-23).
- **EPIC-07** goes third. Backend only, independent.
- **EPIC-05** goes fourth. It owns `data_model.md` (split adjustment migration), `strategy_rules.md` §9.1, `Positions.js`/`positions.md`, the settings path (ST-29) and tier 0 in `positionUrgency.js` (rebased on ST-19).
- **EPIC-06** goes fifth. ST-38 follows ST-29; ST-33 rebases on EPIC-05's `Positions.js`. ST-32 is conditional (gate 2026-11-20).
- **EPIC-02** goes sixth. It owns `navigation.md`, the Dashboard cards and `dashboard.md`, and `metrics_definitions.md` (ST-13); ST-10 rebases `positionUrgency.js` on EPIC-04/05.
- **EPIC-03** goes last. It takes the next `data_model.md` migration number after EPIC-05, rebases `metrics_definitions.md` on ST-13, and regenerates the Weekly Digest baselines last.

**Fallback:** **ST-34** (EPIC-06) may merge on its own ahead of the sequence, and should, before any EPIC regenerates baselines. EPIC-07 may merge at any point. EPIC-02 and EPIC-03 may swap only if EPIC-03 does not touch `navigation.md` or `metrics_definitions.md` before EPIC-02's versions are on `main`.

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch checks whether the file exists before creating its own. If it exists, the branch appends its own section and never overwrites. No story is `deferred_at_planning`; ST-32 is recorded as conditional (gate 2026-11-20).

**Shared files across EPICs:**
- **`accessibility-axe-scan.spec.js`, `runAxeScan`** (EPIC-01 ST-01/ST-02; EPIC-04 ST-20): EPIC-01 owns.
- **`src/lib/positionUrgency.js` + unit tests** (EPIC-04 ST-19; EPIC-05 ST-27; EPIC-02 ST-10): EPIC-04 owns the tests; EPIC-05 then EPIC-02 add cases.
- **`openapi.yaml`, `api_changelog.md`, contracts** (ST-03, ST-13, ST-14, ST-16, ST-17, ST-33): union of paths, highest version (CLAUDE.md §8 step 3).
- **`data_model.md`** (EPIC-05 ST-27, ST-28; EPIC-03 ST-17): EPIC-05 owns; EPIC-03 takes the next migration.
- **`metrics_definitions.md`** (EPIC-02 ST-13; EPIC-03 ST-14, ST-17): EPIC-02 owns.
- **`navigation.md`** (EPIC-02 ST-07/ST-08; EPIC-03 ST-16): EPIC-02 owns.
- **`Positions.js`, `positions.md`** (EPIC-05 ST-27; EPIC-06 ST-33): EPIC-05 owns.
- **Governance files and `.githooks/pre-commit`** (EPIC-04 only): sequential commits; CLAUDE.md §6, and §8 step 2a per co-bumped file.
- **`.github/workflows/`** (ST-06, ST-19, ST-23, ST-34, ST-36): separate jobs/files where possible; the Playwright workflow is owned by ST-36.
- **Visual baselines:** ST-34 first; each EPIC regenerates what it changes after rebasing; EPIC-03 last.
- **`claude/backlog/backlog.md`:** follow-ups via `/backlog-add` only; run `scripts/check_backlog_item_integrity.py` after each §8 merge (step 2c).

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — Site Structure & Usability Phase 4, Stage 1: Correct and Safe (build-and-ship)

**Maps to:** S2-01 – S2-06
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Cybersecurity & Trust Lead
**Estimated effort:** 3.65 days
**Risk IDs:** RISK-01, RISK-06
**Execution sequence:** 1

#### ST-01 — Make the four mouse-only controls keyboard-operable

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first in EPIC-01)

**Notes:** Design Pre-Approved (`design_system.md` v1.27 §Accessibility). Owns the new axe scans in `accessibility-axe-scan.spec.js` (RISK-01); ST-20 rebases on it.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-02 — Link the Exit dialog's labels to their inputs

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (same spec file)

**Notes:** Axe scan of the open Exit dialog in both themes.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-03 — Say Telegram, not email, and show when an alert was not sent

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None

**Notes:** Addendum: `GET /notifications` gains derived `delivery_status` (`sent | not_requested | pending | not_sent`), contract `alerts_endpoints.md` + `openapi.yaml` in the same commit; backend error strings renamed to Telegram wording; "Not sent" on Feed rows only. Locked `notifications.md` v0.12; `alert-delivery-truth/decision_record.md` §2–§3. Related follow-up filed: BLG-BE-224.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-04 — Fix Alert History compact values

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-03

**Notes:** Addendum: regime keys (`spy_risk_on`/`ftse_risk_on`) also mapped; prices in the row's market currency. `notifications.md` v0.12 §Alert History Values.

**Staging-only ACs:** Addendum step: one real UK row checked on staging before the commit (staging read, with the user's permission). The AC itself is unit/Playwright.

**Status at sprint open: ready**

---

#### ST-05 — Re-review the accepted open-access risk

**Owner:** Cybersecurity & Trust Lead; Product Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None (raise at sprint start)

**Notes:** Review and decision story; any remedy filed as its own item via `/backlog-add` (RISK-06). No design artefact (LL-v2.2-SP-01 advisory: HoST session recommended).

**Staging-only ACs:** None (decision recorded in `credential_policy.md` §1.1)

**Status at sprint open: ready**

---

#### ST-06 — Measure Core Web Vitals and update the performance budget

**Owner:** QA & Testing Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Record whether the Performance baseline was measured before or after ST-08 merged (BLG-QA-274, filed at planning). Lighthouse CI job is a new workflow job; see shared-file advisory.

**Staging-only ACs:** None (AC 2 is shown on this story's own PR)

**Status at sprint open: ready**

---

### EPIC-02 — Site Structure & Usability Phase 4, Stage 2: Home Page and Navigation (build-and-ship)

**Maps to:** S2-07 – S2-13
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 6.15 days
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 6

#### ST-07 — Revise navigation.md and design_system.md for the Phase 4 target state

**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (first in EPIC-02)

**Notes:** Addendum: the design gate wrote `navigation.md` v2.5 (HoUX approval 2026-11-18). This story writes `design_system.md` §14.5 and records the dated Head of UX & Design approval of both files. Decision half met by DL-089.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-08 — Move Strategy Benchmark into Performance and Ticker Universe into Settings

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-07 (`navigation.md` half done at gate)

**Notes:** Addendum: Ticker Universe at `/settings/ticker-universe` (Settings §3 "Screener universe" row); Strategy Benchmark filter bar not sticky and its own §3a index retired; SC-SIX-06–08 moved or removed; `pageLabels.js`, command palette and `Layout.js` updated. Specs `navigation.md` v2.5, `performance.md` v1.3, `strategy_benchmark.md` v0.12, `ticker_universe.md` v1.3, `settings.md` v1.11.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-09 — Make the quiet-day Dashboard a single line

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-07

**Notes:** Addendum: the folded line reads "Nothing to show: …" (`dashboard.md` v4.4 §3A), not "All clear". Regenerates Dashboard baselines after ST-34 is on `main`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-10 — Use one grace-period definition across the Dashboard

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-09; ST-19 (unit-test convention)

**Notes:** Addendum: Card 3 (`GracePeriodCard.js`) in scope; `nextEndsText` moves into `src/lib/positionUrgency.js` with unit tests; Positions to Watch drops "exit zone" wording (`dashboard.md` v4.4 §4B). At the top of its estimate: slippage watch item.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-11 — Offer "Plan this" on the Today list's New signals rows

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-10

**Notes:** Addendum: Product Owner chose to add it, on `new` and `watchlisted` rows only, using the `signals.md` route incl. `entry_price` (`dashboard.md` v4.4 §1B, TL-30).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-12 — Show machine-checkable checklist items as automatic status

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** Strategy Rules & System Intent Owner confirmation (dated) of the `trade_plan.md` v1.30 §6 §13-note amendment, before the build

**Notes:** Addendum: "Position size within heat limits" becomes "Position size checks" (cash, sector concentration, sizing validity); AC 1 applies to "Position size checks" and "Stop level defined".

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-13 — Filter Trade History and Journal by rules followed or broken

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 1.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** Metrics Definitions & Analytics Owner definition in `metrics_definitions.md`, before the build

**Notes:** Addendum: `GET /trades` gains server-computed `rules_followed: true|false|null` and `rules_broken: string[]` (`trade_endpoints.md`, `openapi.yaml`, pytest); UI adds "Not known"; Journal red-flags filter decided not needed (`trade_history.md` v1.18). The Metrics Definitions & Analytics Owner writes the definition.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-03 — Site Structure & Usability Phase 4, Stage 2: Weekly Review Loop (build-and-ship)

**Maps to:** S2-14 – S2-17
**Owner:** Head of UX & Design; Metrics Definitions & Analytics Owner; Product Owner
**Estimated effort:** 4.25 days
**Risk IDs:** RISK-01, RISK-03
**Execution sequence:** 7

#### ST-14 — Rename the Weekly Digest's journal completion figure

**Owner:** Metrics Definitions & Analytics Owner; API Contracts & Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (first in EPIC-03)

**Notes:** Addendum: adds `closed_trades_total` (contract, `openapi.yaml`) so the page can say "No closed trades yet"; confirm the digest and `GET /analytics/compliance-metrics` predicates match, or align the digest to `metrics_definitions.md`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-15 — Rewrite the Weekly Digest as a readable weekly summary

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-14; built with ST-16

**Notes:** `weekly_digest.md` v0.3 §2; `weekly-review/decision_record.md` §3. Spec rename to "Weekly review" is not in scope (BLG-UX-22, filed at planning).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-16 — Link the Weekly Digest figures to their pages

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-14; with ST-15

**Notes:** Addendum: journal completion links to `/Performance?section=compliance` (recorded in `navigation.md` v2.5); `GET /digest/weekly` gains `red_flags_7d` (`digest_endpoints.md`, `openapi.yaml`, pytest).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-17 — Measure the core loop and show this week's loop on the Weekly Digest

**Owner:** Product Owner; Metrics Definitions & Analytics Owner; Data Model & Domain Schema Owner
**Estimated effort:** 2.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-15; Metrics Definitions & Analytics Owner sign-off of the five step definitions

**Notes:** Addendum: counts only (no step-to-step rates); caption names the ISO-week dates; the opened event is written once per page load, not on Refresh (`weekly_digest.md` v0.3). New events table: `data_model.md` migration block (takes the number after EPIC-05's). If an endpoint is added: contract + `openapi.yaml` + `backend/routers/test.py` + `SystemStatus.js` fallback + `SC-SS-01b` in the same commit. Production migration at deploy is a Human-Delegation deploy step (Infrastructure & Operations Owner), not an AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-04 — First-Time-Right Checks (Product Owner direction, 2026-11-12)

**Maps to:** S2-18 – S2-24
**Owner:** Head of Specs Team; QA & Testing Owner; Head of Engineering
**Estimated effort:** 3.70 days
**Risk IDs:** RISK-04
**Execution sequence:** 2

#### ST-18 — Design gate data-source, writer and worked-example checks

**Owner:** Head of Specs Team; Head of UX & Design
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None (first in EPIC-04; early in the sprint)

**Notes:** CLAUDE.md §6 checklist (`design_gate_prompt.md`, `OPERATIONAL_GUIDE.md` §14 and phase header, `prompt_change_log.md`). Dry runs on the v9.17 `positions-decision-first` record and `dashboard.md` v4.0 §1B recorded in the commit or a docs/ops note. Head of UX & Design role agent-mediated.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-19 — Unit-test pure frontend logic in CI

**Owner:** QA & Testing Owner; Head of Engineering
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None (early in EPIC-04)

**Notes:** Owns `positionUrgency.test.js` and the `src/lib` unit-test convention that ST-10 and ST-27 follow.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-20 — Fail the axe scan on incomplete colour-contrast results

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** ST-01, ST-02 on `main` (or rebased on EPIC-01)

**Notes:** Seated by Product Owner direction (2026-11-12, DL-089).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-21 — Script the locator-collision check and run it from commit-check

**Owner:** Head of Specs Team; QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Edits `execution_prompt.md` §3.1.A step 13 (CLAUDE.md §6 checklist); `commit-check` skill edit under `shared_standards.md` §17. Test inputs are v9.17 ST-01 `b2d93f6d` and v9.17 ST-03's pre-fix diff.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-22 — Require the pre-commit code review in execution_prompt.md

**Owner:** Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None (rebase on ST-21's `execution_prompt.md` bump if it lands first)

**Notes:** CLAUDE.md §6 checklist; `governance-drift` skill must pass.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-23 — Enforce the prompt size budget on direct commits to main

**Owner:** Head of Specs Team; Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** ST-22

**Notes:** Bumps `post_ship_closure.md` and `roadmap_prompt.md` (CLAUDE.md §6 for both).

**Staging-only ACs:** AC 3 `post-merge` (next post-ship closure raises no baseline in a later PR); tracked by **BLG-GOV-421** (source item stays open until met)

**Status at sprint open: ready**

---

#### ST-24 — Count an item as shipped only on a ✅ COMPLETE banner line

**Owner:** Head of Specs Team; Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-05 — Position Data Correctness

**Maps to:** S2-25 – S2-31
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 6.65 days
**Risk IDs:** RISK-05, RISK-03
**Execution sequence:** 4

#### ST-25 — Use one native-entry function on every position path

**Owner:** Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None (first in EPIC-05)

**Notes:** No behaviour change.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-26 — Use the live FX rate, not a hard-coded 1.27

**Owner:** Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** ST-25

**Notes:** Named-file write (if needed for AC 3): `BLG-BE-213` `Notes` line, authorised under `execution_prompt.md` §7.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-27 — Handle a stock split on an open position

**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 3.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** Strategy Rules & System Intent Owner approval (dated) of the exact §9.1 text before the build; ST-19 (unit-test convention)

**Notes:** RISK-05 direction decided at seal (see sign-off). Named-file write: `strategy_rules.md` new §9.1 + §8.1 cross-reference + Change log row (case (c)). Addendum: urgency tier 0 "Split to confirm" in `positionUrgency.js` with unit tests; `positions.md` v2.30 §Split Detected State (no "Not a split" option). Odd lots: user enters the post-split share count. Production migration at deploy is a Human-Delegation deploy step, not an AC. Owns `data_model.md`, `Positions.js` and `positions.md` for this sprint.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-28 — Tag lifecycle transitions caused by the v9.12 currency correction

**Owner:** Head of Engineering; Metrics Definitions & Analytics Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** Documents the convention in `data_model.md` (EPIC-05 owns).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-29 — Keep GET /settings working when the change-log read fails

**Owner:** Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** ST-38 (EPIC-06) follows on the same settings path.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-30 — Make the Reports unrealised P&L match the Positions basis

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None

**Notes:** Addendum: direction (a), compute live (Product Owner at gate); `reports.md` v0.28. Mark `DEV-REPORTS-ST06-01` resolved and remove the v0.10 snapshot bullet.

**Staging-only ACs:** AC 1 (Reports and Positions unrealised figures match at the same moment, verified on staging). If the staging run is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2).

**Status at sprint open: ready**

---

#### ST-31 — Cache the Trade Entry ATR preview per ticker and market

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None

**Notes:** Design Pre-Approved (`position_form.md` v1.14 §ATR preview).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-06 — Market-Data Reliability and CI

**Maps to:** S2-32 – S2-38
**Owner:** Infrastructure & Operations Owner; Head of Engineering; QA & Testing Owner
**Estimated effort:** 2.55 days
**Risk IDs:** RISK-03, RISK-07
**Execution sequence:** 5

#### ST-32 — Finish the on-demand Yahoo failure diagnosis (remainder)

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** 0.25
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** Production weekly report ≥ 2026-11-20 (Human-Delegation, Infrastructure & Operations Owner)

**Notes:** Conditional (§1.4b, RISK-07). Promoted to firm only when the Infrastructure & Operations Owner confirms the report (dated); otherwise returns to backlog at sprint close. AC 1 met by v9.17 ST-15.

**Staging-only ACs:** AC 2 and AC 3 `post-merge` (production weekly report over 7 days after PR #2259); tracked by **BLG-OPS-217** (source item stays open until met)

**Status at sprint open: conditional — gate 2026-11-20**

---

#### ST-33 — Show "earnings unknown" when an earnings or gap-risk lookup fails

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-32 only if its cause changes which lookups fail

**Notes:** Addendum: Screener UK rows make no earnings lookup (`screener_results.md` v1.12); "unknown" is muted and never uses the GAP RISK badge's colour or wording; cite the gap-risk §13 review's binding conditions. `data_status` in `earnings_endpoints.md` + `openapi.yaml`. Rebases on EPIC-05's `Positions.js`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-34 — Let the visual-baseline workflow push regenerated snapshots

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None (early: may merge on its own ahead of the EPIC sequence)

**Notes:** Tracks `LL-v9.17-P3-03`.

**Staging-only ACs:** None (AC 1 is a GitHub Actions `workflow_dispatch` run on the EPIC branch, in-sprint)

**Status at sprint open: ready**

---

#### ST-35 — Seed staging's UK positions with the .L suffix

**Owner:** Infrastructure & Operations Owner; QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None (staging write needs the user's permission)

**Notes:** —

**Staging-only ACs:** AC 2 (staging `GET /positions` returns `price_is_stale: false` for both UK positions after the staging correction, with the user's permission). If deferred past merge, file a backlog item before the PR opens.

**Status at sprint open: ready**

---

#### ST-36 — Build the E2E bundle once per Playwright run

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** ST-34

**Notes:** Owns the Playwright workflow edit; other EPICs editing it rebase.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-37 — Keep a bare root pytest out of the mutmut pilot tests

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-38 — Run the settings change-log SQL against real Postgres in CI

**Owner:** Director of Quality; Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** ST-29 (EPIC-05) on `main`

**Notes:** Phase B skips cleanly without a real `DATABASE_URL`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-07 — AI Output Boundary

**Maps to:** S2-39 – S2-40
**Owner:** AI Compliance & Governance Officer; Product Owner; Backend Engineering Patterns Owner
**Estimated effort:** 1.00 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-39 — Check daily briefing and chat output against §13.2

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** AI Compliance & Governance Officer ruling recorded before the code

**Notes:** Cites `strategy_rules.md` §13.2 and the §13.5 row for the BLG-FEAT-50/51 review.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-40 — Decide whether the debrief may say more than one restating sentence

**Owner:** AI Compliance & Governance Officer; Product Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`

**Dependencies:** Production debrief sample (Human-Delegation)

**Notes:** Decision story; any implementation filed as its own item. Cites §13.2 and the §13.5 row for the ST-06 debrief review. A `strategy_rules.md` §13.5 change is not authorised by this plan. Slice owner "AI Compliance Governance Officer" normalised to the canonical role name. Precondition BLG-BE-152 shipped.

**Staging-only ACs:** AC 1 needs a sample of real production debriefs (Human-Delegation). If the sample is not available in-sprint, AC 1 is `post-merge`; tracked by **BLG-GOV-378** (source item stays open until met)

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units (28.00 ceiling) |
| Total estimated effort (in-scope) | 27.95 days (40 stories, 7 EPICs); firm 27.70, conditional 0.25 (ST-32) |
| Utilisation | 99.8% of the band ceiling. Above the 95% advisory buffer floor; the Product Owner chose to proceed, 2026-11-18 |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | None. All 40 slice items are in scope. ST-32 is conditional (gate 2026-11-20) and returns to the backlog only if its gate is not met. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-05: ST-27 stock-split rule direction | Strategy Rules & System Intent Owner | No. **Resolved 2026-11-18** (see sign-off below) |
| Human-Delegations at sprint start: ST-32 production weekly report (≥ 2026-11-20); ST-40 production debrief sample; ST-17 and ST-27 production migrations at deploy | Infrastructure & Operations Owner; AI Compliance & Governance Officer | No |
| In-story sign-offs before build: ST-27 exact §9.1 text; ST-12 §13-note; ST-13 and ST-17 metric definitions; ST-07 dated approval; ST-05 decision; ST-39 ruling | Strategy Rules & System Intent Owner; Metrics Definitions & Analytics Owner; Head of UX & Design; Cybersecurity & Trust Lead; Product Owner; AI Compliance & Governance Officer | No |
| Staging permission: ST-35 write; ST-04 UK row read; ST-30 staging check | Product Owner | No |
| Post-merge ACs tracked by BLG-OPS-217 (ST-32 AC 2, AC 3), BLG-GOV-421 (ST-23 AC 3), BLG-GOV-378 (ST-40 AC 1, if the sample is not available in-sprint): source items stay open until met | Sprint Execution Engine; Post-Ship Closure Engine | No |
| For any other staging-only AC whose sign-off is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |
| HoST design session for ST-05 (LL-v2.2-SP-01, advisory) | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (as drafted), 2026-11-18
**Scope confirmed:** Confirmed: 40 stories across 7 EPICs in a single sprint; ST-32 conditional (gate 2026-11-20); none deferred, 2026-11-18
**Capacity confirmed:** Confirmed: 27.95 / 28.00 (99.8%), proceeding above the 95% buffer floor, 2026-11-18
**Deferred execution blockers accepted (if any):** N/A (none)
**Release-plan judgement calls:** Confirmed, 2026-11-18: `BLG-OPS-220` seated under §1.4c step 1a; `BLG-OPS-217` seated as its 0.25d remainder (conditional); `BLG-GOV-422`'s 2026-11-13 extension restated as three ACs (+0.25d)
**Pre-sprint decision RISK-05 (Strategy Rules & System Intent Owner):** Resolved, 2026-11-18. ST-27's rule goes in a new `strategy_rules.md` §9.1 "Stock split on an open position". For a ratio r (2:1 → r = 2): quantity × r; entry, initial stop and trailing stop ÷ r; ATR from split-adjusted history; per-share risk ÷ r, so currency risk and R-multiples are unchanged. Until the user confirms the adjustment, the position gets no stop-breach alert and no exit recommendation. The adjustment is a unit change, not a §7.3 stop movement. The original entry fields stay stored. A ratio that leaves a non-whole quantity is not confirmed automatically: Positions asks the user to enter the post-split share count. The exact text is approved in the story (AC 6)
**Post-merge trackers:** Confirmed, 2026-11-18: source items `BLG-OPS-217`, `BLG-GOV-421`, `BLG-GOV-378` stay open as trackers
**Pre-seal backlog filings:** BLG-UX-22, BLG-SPEC-241, BLG-BE-224, BLG-QA-274 (design gate observations), authorised and filed 2026-11-18

### Named-file writes

- `claude/strategy/strategy_rules.md`: new §9.1 "Stock split on an open position" (content per RISK-05 above), a one-line §8.1 cross-reference (an unconfirmed detected split suppresses the stop-loss trigger), and the file's Change log row (ST-27, case (c)).
  **Strategy Rules & System Intent Owner confirmation:** Confirmed, 2026-11-18
- `BLG-BE-213` `Notes` line, only if `compliance_service.py`'s `fx_rate` does not convert a money value (ST-26 AC 3). For information.

No `claude/roadmap/*` write is planned. No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

For information, outside the named-file rule: ST-18, ST-21, ST-22 and ST-23 edit `design_gate_prompt.md`, `execution_prompt.md`, `post_ship_closure.md`, `roadmap_prompt.md`, `OPERATIONAL_GUIDE.md` and `prompt_change_log.md` under the CLAUDE.md §6 checklist.

**Signed off by:** Product Owner
**Date:** 2026-11-18
