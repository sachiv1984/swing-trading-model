**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-11-03
**Cycle:** 2026-11-03__release-v9.15
**Release:** v9.15
**Sprint Goal:** Make every route into Trade Entry show the §4.2 pre-entry checks and pre-fill the live FX rate (BLG-FE-244, BLG-FE-245, P1). Deliver Site Structure & Usability Phase 1: navigation v2/glossary, Dashboard "Today" and Journal area specs approved, one name per page, legacy Dashboard route removed, per-page tab titles. Ship v9.15's metric-correctness, AI-check, operations, data-model and governance items alongside.
**Backlog Slice Source:** Original: `claude/cycles/2026-11-03__release-v9.15/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-01 and ST-16)

# Sprint Backlog — 2026-11-03__release-v9.15

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-03 → EPIC-02 → EPIC-04 → EPIC-06 → EPIC-07 → EPIC-05.
- **EPIC-01** goes first. It carries the P1 anchors (ST-01, ST-02) and owns `openapi.yaml`, `strategy_rules.md` with `strategy_version_registry.py`, and `positions.md` §Trail Stop Action (ST-06).
- **EPIC-03** goes second. ST-17 rebases on ST-06's `positions.md` and modal changes, and it must be on `main` before ST-42 (EPIC-07) renames SC-TS-* IDs.
- **EPIC-02** goes third. Its three spec stories run longest while waiting on approval, so it merges after the two short build EPICs. ST-12 deletes `Dashboard.js`, so any ST-04 (EPIC-01) edit to that file is already merged and is removed with the page.
- **EPIC-04** goes fourth. `ai_service.py`, `_NON_TICKER_WORDS` and `ai_s13_boundary_test_suite.md` are touched only within it. ST-28 takes the next free `strategy_rules.md` version after EPIC-01 and EPIC-03.
- **EPIC-06** goes fifth. It owns the `data_model.md` DS-xx blocks (ST-35, ST-36) ahead of ST-33's DS-36 entry.
- **EPIC-07** goes sixth. ST-42 renames over ST-17's assertions, and ST-37, ST-38 and ST-43 may bump governance files under CLAUDE.md §6.
- **EPIC-05** goes last. ST-33 is conditional (gate 2026-11-09) and ST-31 changes the CI workflows, so it is best merged over the final tree.

**Fallback:** EPIC-04 and EPIC-06 may swap. EPIC-02 may merge before EPIC-03 only if ST-17 does not yet touch `positions.md`, and EPIC-07 may never merge before EPIC-03 (ST-42 needs ST-17).

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch checks whether the file exists before creating its own. If it exists, the branch appends its own section and never overwrites. At initialisation, record ST-16 as `deferred_at_planning` (see Items Deferred This Sprint).

**Shared files across EPICs:**
- **`claude/strategy/strategy_rules.md`** and `backend/strategy_version_registry.py` (EPIC-01 ST-01 Branch A; EPIC-03 ST-20; EPIC-04 ST-28; all conditional on their rulings): EPIC-01 owns them. These are case (c) named-file writes confirmed in the sign-off below. Bumps go in merge order, and the later branch takes the next free version (CLAUDE.md §8 step 2a, checked per file).
- **`openapi.yaml`** and `api_changelog.md` (EPIC-01 ST-01, ST-06, ST-07; EPIC-03 ST-21 if changed; EPIC-06 ST-34): EPIC-01 owns them. Take the union of additions and the highest version.
- **`docs/specs/frontend/pages/positions.md`** and the Trail Stop modal in `Positions.js` (EPIC-01 ST-06; EPIC-03 ST-17): EPIC-01 owns them. ST-17 rebases and takes the next version.
- **SC-TS-* Playwright scenarios** (EPIC-03 ST-17; EPIC-07 ST-42): EPIC-03 owns the assertions; ST-42 renames after ST-17 is on `main`.
- **`src/pages/Dashboard.js`** (EPIC-01 ST-04 peak date; EPIC-02 ST-12 deletes it): EPIC-02 owns it. ST-12 removes the page with any ST-04 edit.
- **`docs/specs/metrics_definitions.md`** (EPIC-03 ST-15 if needed, ST-21 if the terminal-result set changes, ST-23): within EPIC-03. Run §8 step 2a's version check if a second EPIC touches it.
- **`docs/specs/data_model.md`** (EPIC-06 ST-35, ST-36; EPIC-05 ST-33): EPIC-06 owns it. EPIC-05 rebases.
- **`src/Layout.js`, `CommandPalette.js`, `navigation.md`, `glossary.md` and the nav/palette Playwright specs** (EPIC-02 ST-08, ST-11 to ST-14): within EPIC-02. ST-12 goes before ST-11 on `CommandPalette.js`.
- **`OPERATIONAL_GUIDE.md`, `prompt_change_log.md` and governance prompts** (EPIC-07 ST-37, ST-38, ST-43, ST-44 if any changes a prompt): within EPIC-07. Apply the CLAUDE.md §6 checklist and §8 step 2a per co-bumped file.
- **`tests/conftest.py`** (EPIC-07 ST-41; ST-40 if it adds fixtures): within EPIC-07.
- **`claude/backlog/backlog.md`:** new items via `/backlog-add`, plus ST-12's Notes line on `BLG-FE-240`. Run `scripts/check_backlog_item_integrity.py` after each §8 merge.

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — Trade Entry Integrity & Sizing (build-and-ship)

**Maps to:** S2-01 – S2-07
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 5.05 days
**Risk IDs:** RISK-06, RISK-07
**Execution sequence:** 1

#### ST-01 — Show the pre-entry checks on every route into Trade Entry, not only from a Trade Plan

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 2.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (first in EPIC-01 and in the sprint)

**Notes:** P1 release anchor. First sub-step: the Strategy Rules & System Intent Owner's dated ruling on the acknowledgement against `strategy_rules.md` §4.2.6 and §4.2.1 (addendum). Branch A disables Submit until a WARN/FAIL is acknowledged; Branch B keeps it advisory. Both are designed in `trade-entry-pre-entry-checks/decision_record.md` and `position_form.md` v1.12; delete the branch not taken. Raise the ruling at sprint start (RISK-07). Branch A's `strategy_rules.md` clarification is a case (c) named-file write, confirmed at seal. `POST /portfolio/position` gains optional `pre_entry_override_acknowledged`: contract and `openapi.yaml` in the same commit. RISK-06: reuse the Trade Plan panel and validation endpoint; one branch for all Trade Entry stories.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-02 — Pre-fill Trade Entry's FX rate from the live rate, not a fixed 1.27

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (same page as ST-01; ST-03 follows)

**Notes:** BLG-GOV-72 fast-path (c): locked `trade-entry-fx-rate/decision_record.md` and `position_form.md` v1.12 §FX Rate. Both `"1.27"` literals leave `TradeEntry.js`; the rate comes from `GET /market/status`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-03 — Label the FX rate the same way on entry and exit

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-02 (same FX field)

**Notes:** Wording only (FI-P3-02): code review of the static label text is the evidence. Specs: `position_form.md` v1.12, `exit_modal.md` v1.2, `trade_plan.md` v1.21 §5d.2.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-04 — Default trade, exit and cash dates to the user's local date, not the UTC date

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Design Pre-Approved. 15 `toISOString()` sites in 10 files. `Dashboard.js` (peak date) is deleted by ST-12 (EPIC-02): skip that site if ST-12 has merged, otherwise fix it and let ST-12 delete it. Owner normalised to the canonical role name (`check_sprint_backlog_owners.py`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-05 — Normalise the Trade Entry ticker the same way for the ATR preview and for save

**Owner:** Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-06 — Trail Stop modal's ATR trail value uses a hardcoded 2.0 multiplier and no breakeven floor

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None (shares `trail-stop-modal-wording/decision_record.md` and `positions.md` §Trail Stop Action with ST-17, EPIC-03)

**Notes:** Uses the §7.2 formula and §11 multipliers from `backend/strategy_parameters.py`; no strategy ruling needed. Footnote wording is FI-P3-02; the value has a unit test. `position_endpoints.md` stop-trail description updated (response shape unchanged); `openapi.yaml` only if the description is mirrored there. EPIC-01 owns `positions.md` v2.22+; ST-17 rebases.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-07 — Label signal cost as including fees, and make the zero-ATR sizing reason plain English

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Locked `signal-card-cost-and-sizing-reason/decision_record.md`; `signals.md` v0.8. `signal_endpoints.md` lists the two new zero-ATR `reason` strings.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-03 — Metric & Display Correctness

**Maps to:** S2-15 – S2-23
**Owner:** Metrics Definitions & Analytics Owner; Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.90 days
**Risk IDs:** RISK-04, RISK-07
**Execution sequence:** 2

**Deferred at planning:** ST-16 (`BLG-FE-240`), superseded by ST-12. See Items Deferred This Sprint.

#### ST-15 — Trade History counts a break-even trade as a win

**Owner:** Metrics Definitions & Analytics Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (owns the first `metrics_definitions.md` edit in EPIC-03 if one is needed)

**Notes:** Design Pre-Approved. The Avg Loss treatment of `pnl = 0` follows `metrics_definitions.md` §Win Rate/§Avg Loss as written; if the definition is silent, record the Metrics Definitions & Analytics Owner's choice in the QA evidence. Owner normalised to the canonical role name.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-17 — Align the View Trail modal wording with the read-only ruling

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** ST-06 (EPIC-01, `positions.md` §Trail Stop Action and the modal); coordinate SC-TS-* IDs with ST-42 (EPIC-07)

**Notes:** Locked `trail-stop-modal-wording/decision_record.md`. The tooltip is FI-P3-02; the heading and label have Playwright. EPIC-03 merges before EPIC-07, so ST-42 renames IDs over ST-17's updated assertions.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-18 — Fix the Strategy Benchmark Rebalance badge's contrast and settle tinted vs filled exit-reason badges

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Locked `exit-reason-badges/decision_record.md` (filled badges); `strategy_benchmark.md` v0.9 §7.3. SC-SB-04a's `bg-teal-600` becomes `bg-teal-700`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-19 — Price-alert duplicate fallback returns 500 when the threshold has more than 4 decimal places

**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** The DS-28 real-Postgres suite runs in CI.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-20 — Use the deploy date, not the ruling date, as strategy v1.15's effective date

**Owner:** Strategy Rules & System Intent Owner; Financial Reporting & Records Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** First sub-step: the Strategy Rules & System Intent Owner's ruling on behavioural effective dates (ruling date vs deploy date). If the deploy date: the `strategy_rules.md` Change Log row 1.15 Date changes to the deploy date, because `test_registered_effective_dates_match_change_log` requires the match. This is a case (c) named-file write, confirmed at seal. AC 2 is met by a test (preferred) or by query output.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-21 — Show the code-written fallback when the monthly P&L summary's regeneration call fails

**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Design Pre-Approved (`reports.md` v0.26 §AI Summary fallback row). `reports_endpoints.md` 503 row and `openapi.yaml` in the same commit if changed.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-22 — Gap-risk weekend statistic: pick it by the exchange calendar and count ordinary weekends

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Binding Condition 4 re-confirmation goes in the §13 record's next addendum only if the statistic's definition changes. The Strategy Rules & System Intent Owner signs that addendum (agent-mediated draft).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-23 — Open-position pnl: code uses the live FX rate and does not deduct fees; the dictionary says entry-time FX, fees deducted

**Owner:** Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None (EPIC-03 owns `metrics_definitions.md`; after ST-15 if both edit it)

**Notes:** First sub-step: the Data Model & Domain Schema Owner's ruling on the open-position P&L FX basis and fee treatment (RISK-07). Design Pre-Approved: a code change keeps the same fields, and any tooltip or label stating the basis follows the ruling. A new display element needs its own design pass. Owner normalised to the canonical role name.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-02 — Site Structure & Usability Phase 1 — Specs, Vocabulary & Quick Wins

**Maps to:** S2-08 – S2-14
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design; Head of Engineering
**Estimated effort:** 8.50 days
**Risk IDs:** RISK-02, RISK-04
**Execution sequence:** 3

#### ST-08 — Navigation spec v2: job-based areas, plus a UI-label section in the glossary

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 2.00
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None (first in EPIC-02; blocks ST-11)

**Notes:** Conditionally cleared at the design gate: the spec is the deliverable. Approval by the Head of UX & Design is a named sub-step (RISK-02). Brief: `site-structure-phase1/decision_record.md` §2.1. `navigation.md` v1.8 → v2.0 keeps the ST-12–ST-14 sections. If not approved by close, the story returns with a reason and ST-11 stays not-ready.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-09 — Dashboard spec: a prioritised "Today" action list

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 2.00
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Conditionally cleared. Brief: `site-structure-phase1` §2.2, including the §13 constraint (no ranking or "do this" wording in the Today list without its own §13 confirmation). `dashboard.md` is Class 1: Head of Specs Team approval as well as the Head of UX & Design. Every observable behaviour gets a testable AC for `BLG-FE-254`. ST-16 is deferred as superseded; no home-page win rate is added unless this spec specifies one for a later release.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-10 — Spec for one Journal area combining reflections, red flags and position notes

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 2.00
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Conditionally cleared. Brief: `site-structure-phase1` §2.3. Two sub-steps: the Strategy Rules & System Intent Owner's §13 confirmation (AC 2; §13.1, §13.2, §13.5 roster if AI journal summaries surface) and the Head of UX & Design's approval.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-11 — Use one name per page and action across sidebar, page headings and command palette

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** ST-08 (must be approved first)

**Notes:** Conditionally cleared on ST-08's approval; rule fixed at `site-structure-phase1` §3.1 (one label source for sidebar, heading, palette and tab title). Autonomous once the glossary section is approved (BLG-GOV-72 (c)). Shares `Layout.js` and `CommandPalette.js` with ST-12–ST-14 (same EPIC).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-12 — Remove the legacy widget Dashboard route and its duplicate command-palette entry

**Owner:** Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None (the ST-16 dependency is void: ST-16 deferred as superseded)

**Notes:** Design: `site-structure-phase1` §3.3; `navigation.md` §Legacy Dashboard Route. Scope bullet 1 is answered at planning: no `DashboardHome` site exists (addendum). Add a Notes line to `BLG-FE-240` recording that the defect leaves with the page (named-file write). Removes `WinRateWidget` and `WinRateChart` with the page.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-13 — Set a browser-tab title for each page

**Owner:** Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None (uses ST-08's labels if approved; otherwise the current labels)

**Notes:** Design: `site-structure-phase1` §3.2; `navigation.md` §Browser Tab Title.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-14 — Fix three small chrome defects: version label, What's New heading, sidebar height

**Owner:** Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Design: `site-structure-phase1` §3.4; `navigation.md` §Sidebar Footer and Height, `dashboard.md` §6A. The dead footer "Docs" link is out of scope (filed as BLG-FE-268).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-04 — AI Output Checks & §13 Boundary

**Maps to:** S2-24 – S2-28
**Owner:** AI Compliance & Governance Officer; Strategy Rules & System Intent Owner
**Estimated effort:** 2.20 days
**Risk IDs:** RISK-03, RISK-07
**Execution sequence:** 4

#### ST-24 — Review logged briefing ticker-caveat tokens for further non-tickers

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None (shares `_NON_TICKER_WORDS` with ST-26)

**Notes:** Human-Delegation: AC 1 needs the logged caveat tokens since 2026-10-30, a production read the user permits or runs (RISK-01). The code half (adding tokens and tests) proceeds once the list is in hand.

**Staging-only ACs:** AC 1 needs a production read (Human-Delegation, in-sprint). If it is still outstanding at PR time, file a tracking item before the PR opens (CLAUDE.md §2).

**Status at sprint open: ready**

---

#### ST-25 — Journal summary advisory check: remaining false positives and misses

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None (ST-27 follows)

**Notes:** First sub-step: the AI Compliance & Governance Officer's ruling on the check forms; record it before the code change (AC 1). One ruling can cover ST-27. Updates `ai_s13_boundary_test_suite.md` B-JS-04.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-26 — Chat stop-time focus rule: ignore common upper-case non-ticker words

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None (after ST-24 on `_NON_TICKER_WORDS`, or rebase)

**Notes:** Within ruling `ESC-EXEC-20261027-02` (B): condition 2 is a minimum list, so additions need no new ruling. Record the AI Compliance & Governance Officer's agent-mediated confirmation in the QA evidence.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-27 — Journal summary advisory check: do not flag "could/may help explain"

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** ST-25 (ruling)

**Notes:** Implemented under ST-25's ruling.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-28 — §13 boundary language clarity pass — AI journal summarisation

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 1.25
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** First sub-step: the Strategy Rules & System Intent Owner's dated §13 re-read (RISK-03). The §13 clarification, if the re-read finds the language ambiguous, is a case (c) named-file write confirmed at seal, with its Change Log row and `strategy_version_registry.py` entry. Coordinate with ST-10's §13 confirmation (same clauses).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-06 — Data Model & Spec Debt

**Maps to:** S2-34 – S2-36
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team; API Contracts & Documentation Owner
**Estimated effort:** 2.00 days
**Risk IDs:** RISK-01, RISK-04
**Execution sequence:** 5

#### ST-34 — Clear the 8 pre-existing success-example drifts so check_contract_example_freshness.py exits 0

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None

**Notes:** Each correction is recorded in the changed contract's changelog; `openapi.yaml` changes follow the EPIC-01 ownership rule.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-35 — Re-apply NOT NULL on positions.portfolio_id and positions.total_cost

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None (either order with ST-36; owns the `data_model.md` DS-xx block)

**Notes:** Human-Delegation: staging and production constraint changes need the user's permission, and the user runs production (RISK-01). Read-only pre-checks first; any NULL row needs a backfill decision before migrating.

**Staging-only ACs:** AC 1 staging-only (staging confirmation, in-sprint delegation); AC 1 production half `post-merge`, tracked by **BLG-SPEC-217**.

**Status at sprint open: ready**

---

#### ST-36 — Apply DS-17's open-position unique index to staging

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** None (either order with ST-35)

**Notes:** Human-Delegation: staging index change with the user's permission (RISK-01).

**Staging-only ACs:** AC 1 and AC 2 staging-only (in-sprint delegation). If still outstanding at PR time, file a tracking item before the PR opens.

**Status at sprint open: ready**

---

### EPIC-07 — QA & Governance Tooling

**Maps to:** S2-37 – S2-45
**Owner:** Director of Quality; Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner; Product Owner
**Estimated effort:** 5.70 days
**Risk IDs:** RISK-04, RISK-07
**Execution sequence:** 6

#### ST-37 — Gate scan treats a shipped roadmap feature ID (PT-xx, SI-xx, PO-xx) as a met gate

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** None

**Notes:** Early in EPIC-07 (deferred lessons-learnt patch, §1.4c step 1a). If a governance prompt changes, apply the CLAUDE.md §6 checklist in the same commit.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-38 — Make the execution-state consistency check count EPICs not yet initialised as pending

**Owner:** Director of Quality; Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** None

**Notes:** Early in EPIC-07 (deferred patch). Script and tests only.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-39 — Behavioural tests for live holding days in the compliance and AI briefing readers

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-40 — Real-Postgres tests for the ai_audit_log UUID[] path and the claude_audit_log daily cost sum

**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`

**Dependencies:** None

**Notes:** Phase B real-Postgres tests run in CI.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-41 — Extend the utils.* leak guard to attributes patched on the real utils modules

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-41`

**Dependencies:** None

**Notes:** Touches `tests/conftest.py`. Run default and reverse-order full suites with the venv Python (CLAUDE.md §9).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-42 — Make SC-TS-* Playwright scenario IDs unique across tests/e2e

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-42`

**Dependencies:** ST-17 (EPIC-03) on `main` first

**Notes:** Renames over ST-17's updated SC-TS-* assertions; updates citations in `docs/` and `claude/cycles/` (not sealed artefacts).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-43 — Escalation SLA breach dry-run test

**Owner:** PMO Lead
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-43`

**Dependencies:** None

**Notes:** Dry-run on a scratch copy only; never the live `.claude_current_state.json`. Defects found are filed via `/backlog-add`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-44 — Strategic exclusions review cadence

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 1.25
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-44`

**Dependencies:** None

**Notes:** Decision by the Strategy Rules & System Intent Owner with the Product Owner. No `current_roadmap.md` write: any §2 change is left to the next `run roadmap` (BLG-GOV-408). If the cadence goes into a governance prompt, apply CLAUDE.md §6 in the same commit.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-45 — Sunset review for Priority 3 — Deferred initiatives

**Owner:** Product Owner
**Estimated effort:** 1.25
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-45`

**Dependencies:** None

**Notes:** Product Owner decision. No `initiative_register.md` write.

**Staging-only ACs:** AC 2 `post-merge` (link the decision record as the next `run roadmap`'s input), tracked by **BLG-GOV-408**.

**Status at sprint open: ready**

---

### EPIC-05 — Operations, Security & Market-Data Monitoring

**Maps to:** S2-29 – S2-33
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead; FinOps & Resource Architect
**Estimated effort:** 2.15 days
**Risk IDs:** RISK-01, RISK-05
**Execution sequence:** 7

#### ST-29 — ANTHROPIC_API_KEY 6-month scope audit

**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** Human-Delegation: key permissions and rotation are read from the Anthropic console by the Cybersecurity & Trust Lead (RISK-01). The endpoint register cross-check proceeds autonomously.

**Staging-only ACs:** AC 1 and AC 2 need Anthropic console access (Human-Delegation, in-sprint). If still outstanding at PR time, file a tracking item before the PR opens.

**Status at sprint open: ready**

---

#### ST-30 — Rebalance-exit generation should check that today's screener run completed

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-31 — Skip the five code-test workflows on governance-only and docs-only pushes

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None (merges with EPIC-05, last)

**Notes:** Pass-through jobs keep required checks reporting (`backlog_archive.md:2167` constraint). AC 2 is checked on the EPIC-05 PR itself.

**Staging-only ACs:** AC 1 `post-merge` (first governance-only PR on `main` after merge), tracked by **BLG-OPS-211**.

**Status at sprint open: ready**

---

#### ST-32 — Tell "no qualifying tickers" apart from "momentum run missing" in the month-end rebalance job

**Owner:** Infrastructure & Operations Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** §8.4 recommendations are existing behaviour; no ruling needed.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-33 — Record the weekly market-data call-volume baseline from production

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** None (BLG-OPS-195 waits on it; not in v9.15)

**Notes:** Conditional (§1.4b, RISK-05). Promote to firm only on a dated confirmation that 7 full days after the 2026-11-02 deploy have elapsed and production read access is granted. A return to backlog is expected-path, not a deviation.

**Staging-only ACs:** AC 1 and AC 2 `post-merge` / production data, tracked by **BLG-OPS-197** (this story's own source item, which stays open until both are recorded).

**Status at sprint open: conditional — gate 2026-11-09**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units (28.00 ceiling) |
| Total estimated effort (in-scope) | 27.50 days (44 stories; ST-33's 0.15d is conditional) |
| Utilisation | 98.2% of the band ceiling. This is above the 95% advisory buffer floor; the Product Owner chose to proceed, 2026-11-03 |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-16 (`BLG-FE-240`) | EPIC-03 | Superseded by ST-12. Both win-rate widgets exist only on legacy `Dashboard.js`, which ST-12 deletes; `DashboardHome` has none (addendum). Product Owner, 2026-11-03. `deferred_at_planning`; ST-12 adds a Notes line to `BLG-FE-240` recording that the defect leaves with the page. 0.50d released, not reassigned. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-03: Strategy Rules & System Intent Owner confirmation of ST-28's case (c) `strategy_rules.md` line | Strategy Rules & System Intent Owner | No. **Resolved 2026-11-03: confirmed (see sign-off below)** |
| ST-16 disposition (addendum) | Product Owner | No. **Resolved 2026-11-03: deferred as superseded** |
| Rulings raised at sprint start: ST-01, ST-20, ST-28, ST-44 (Strategy Rules & System Intent Owner); ST-23 (Data Model & Domain Schema Owner); ST-25 (AI Compliance & Governance Officer); ST-45 (Product Owner); spec approvals ST-08, ST-09, ST-10 (Head of UX & Design; Head of Specs Team for ST-09) | As listed | No |
| Human-Delegations raised at sprint start: ST-24 production log read; ST-29 Anthropic console; ST-35 staging and production constraints; ST-36 staging index; ST-33 production read (from 2026-11-09) | AI Compliance & Governance Officer; Cybersecurity & Trust Lead; Data Model & Domain Schema Owner; FinOps & Resource Architect | No |
| Post-merge ACs tracked by BLG-OPS-211 (ST-31), BLG-SPEC-217 (ST-35), BLG-GOV-408 (ST-45), BLG-OPS-197 (ST-33), filed or confirmed 2026-11-03 | Sprint Execution Engine | No |
| For any other staging-only AC whose sign-off is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |
| Initialise ST-16 as `deferred_at_planning` in `execution_state.json` (STEP 5.2 traceability) | Sprint Execution Engine | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (as drafted), 2026-11-03
**Scope confirmed:** Confirmed: 44 stories across 7 EPICs in a single sprint. ST-16 is deferred at planning as superseded by ST-12; ST-33 is conditional (gate 2026-11-09), 2026-11-03
**Capacity confirmed:** Confirmed: 27.50 / 28.00 (98.2%), proceeding above the 95% buffer floor, 2026-11-03
**Deferred execution blockers accepted (if any):** N/A (none)
**Pre-sprint decision RISK-03:** Resolved. ST-28's case (c) line below is confirmed by the Strategy Rules & System Intent Owner, 2026-11-03
**Pre-seal backlog filings:** BLG-OPS-211, BLG-SPEC-217, BLG-GOV-408 (post-merge trackers) and BLG-FE-267, BLG-FE-268 (design gate observations), authorised and filed 2026-11-03

### Named-file writes

- Named-file write: `claude/strategy/strategy_rules.md` §13.1/§13.2 clarified boundary text and/or a §13.5 roster row for the AI journal summary, only if ST-28's dated re-read finds the boundary language ambiguous, with its Change Log row and `STRATEGY_VERSION_REGISTRY` entry. Authorised under execution_prompt.md §7 named-file rule, case (c) (ST-28, RISK-03).
  **Strategy Rules & System Intent Owner confirmation:** Confirmed, 2026-11-03
- Named-file write: `claude/strategy/strategy_rules.md` §4.2.6 (a user-passable acknowledgement is not a "hard submission gate") and/or §4.2.1 ("are blocked" wording for unknown-regime entries), only if ST-01's ruling selects Branch A and the text needs clarifying, with its Change Log row and registry entry. Authorised under execution_prompt.md §7 named-file rule, case (c) (ST-01).
  **Strategy Rules & System Intent Owner confirmation:** Confirmed, 2026-11-03
- Named-file write: `claude/strategy/strategy_rules.md` Change Log row 1.15, Date column changed from "9 October 2026" to the production deploy date, only if ST-20's ruling makes the deploy date the behavioural effective date, with the matching `strategy_version_registry.py` `effective_date` (`test_registered_effective_dates_match_change_log`). Authorised under execution_prompt.md §7 named-file rule, case (c) (ST-20).
  **Strategy Rules & System Intent Owner confirmation:** Confirmed, 2026-11-03
- Named-file write: `claude/backlog/backlog.md` `BLG-FE-240` Notes line, recording that the defect leaves with the legacy Dashboard page (ST-12). Authorised under execution_prompt.md §7 named-file rule. For information; no separate confirmation needed.

Each `strategy_rules.md` write ships in one commit with its §16 Change Log row, its `backend/strategy_version_registry.py` entry (with `tests/test_strategy_version_registry.py` passing) and the §15 re-run. Bumps are taken in merge order (CLAUDE.md §8 step 2a).

No `claude/roadmap/*` write is planned: ST-44 and ST-45 leave `current_roadmap.md` §2 and `initiative_register.md` to the next `run roadmap` (BLG-GOV-408). No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

For information, outside the named-file rule: ST-37, ST-38, ST-43 and ST-44 may edit governance prompts or `OPERATIONAL_GUIDE.md`, under the CLAUDE.md §6 governance edit checklist.

**Signed off by:** Product Owner
**Date:** 2026-11-03
