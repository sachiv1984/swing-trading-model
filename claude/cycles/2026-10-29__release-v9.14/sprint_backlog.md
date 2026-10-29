**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-10-29
**Cycle:** 2026-10-29__release-v9.14
**Release:** v9.14
**Sprint Goal:** Restore the production frontend deploy (BLG-OPS-193, P1) so shipped UI reaches GitHub Pages again, and stop a Yahoo Finance outage from silently giving a risk-on regime and a frozen 1.27 FX rate while System Status reports healthy. Also fix US position sizing's FX inversion (BLG-BE-190) and ship v9.14's AI output safety, reporting, test, operations and governance items.
**Backlog Slice Source:** Original: `claude/cycles/2026-10-29__release-v9.14/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-03, ST-04 and ST-05)

# Sprint Backlog — 2026-10-29__release-v9.14

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-06 → EPIC-03 → EPIC-04 → EPIC-07 → EPIC-05.
- **EPIC-01** goes first. It carries the P1 anchor (ST-01), ST-30 needs ST-01 on `main`, and it owns `openapi.yaml`, `position_service.py` and the first `strategy_rules.md` bump (ST-03, conditional).
- **EPIC-02** goes second. ST-29 (EPIC-05) asserts ST-10's error codes, and ST-09 takes the second `strategy_rules.md` bump.
- **EPIC-06** goes third. It is small and touches no shared file except `ai_endpoints.md` (ST-41).
- **EPIC-03** goes fourth. It owns the route-removal chain (ST-22: `routers/test.py`, `SystemStatus.js` fallback count, `SC-SS-01b`) and the third `strategy_rules.md` bump.
- **EPIC-04** goes fifth. ST-28 rebases on ST-22's `SystemStatus.js` and `system-status.spec.js` changes, and ST-24 owns `metrics_definitions.md` ahead of ST-48.
- **EPIC-07** goes sixth. ST-48 rebases on ST-24, and ST-47 bumps `risk_dashboard.md` after the design gate's v0.1.14.
- **EPIC-05** goes last. Its delegation (ST-30) runs longest, and ST-36 touches many test files, so it is best merged over the final tree.

**Fallback:** if EPIC-05 is ready before EPIC-07, it may merge first; EPIC-07 then rebases. EPIC-05 may never merge before EPIC-02 (ST-29 needs ST-10).

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch checks whether the file exists before creating its own. If it exists, the branch appends its own section and never overwrites.

**Shared files across EPICs:**
- **`claude/strategy/strategy_rules.md`** and `backend/strategy_version_registry.py` (EPIC-01 ST-03, ruling-dependent; EPIC-02 ST-09; EPIC-03 ST-22): EPIC-01 owns them. These are case (c) named-file writes confirmed in the sign-off below. Bumps go in merge order, and the later branch takes the next free version (CLAUDE.md §8 step 2a, checked per file).
- **`openapi.yaml`** and `api_changelog.md` (EPIC-01 ST-03, ST-04/05, ST-07; EPIC-02 ST-10 if documentation changes; EPIC-03 ST-22; EPIC-04 ST-24): EPIC-01 owns them. Take the union of additions and the highest version.
- **Route-registration chain** (`routers/test.py`, `SystemStatus.js` fallback count, `SC-SS-01b`; EPIC-03 ST-22): EPIC-03 owns it. EPIC-04 ST-28 edits `SystemStatus.js` and `system-status.spec.js`, so it rebases and recomputes the count from the merged `test.py`.
- **`metrics_definitions.md`** (EPIC-04 ST-24; EPIC-07 ST-48; ST-50 reads it): EPIC-04 owns it. Run §8 step 2a's version check on this file.
- **`risk_dashboard.md`** (EPIC-01 ST-05/ST-08 implement against v0.1.14; EPIC-07 ST-47 edits it to v0.1.15+): EPIC-07 owns any edit.
- **`position_service.py`, `portfolio` service and `market` service** (EPIC-01 ST-02 to ST-07; EPIC-02 ST-09, ST-12): EPIC-01 owns them. EPIC-02 rebases.
- **`ai_service.py` and `ai_s13_boundary_test_suite.md`** (EPIC-03 ST-15 to ST-20): within EPIC-03 only. Order ST-15 → ST-18, and ST-16 → ST-17 with ST-20 first or rebased.
- **`OPERATIONAL_GUIDE.md`, `prompt_change_log.md` and governance prompts** (EPIC-07 ST-44, ST-45): within EPIC-07. Apply the CLAUDE.md §6 checklist and §8 step 2a per co-bumped file.
- **`tests/conftest.py`** (EPIC-05 ST-32, ST-36): within EPIC-05. ST-32 lands first.
- **`claude/backlog/backlog.md`:** new items only, via `/backlog-add`. No existing item is edited. Run `scripts/check_backlog_item_integrity.py` after each §8 merge.

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — Production Deploy & Market-Data Resilience (build-and-ship)

**Maps to:** S2-01 – S2-08
**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; Head of UX & Design
**Estimated effort:** 4.65 days
**Risk IDs:** RISK-01, RISK-02, RISK-03, RISK-04, RISK-05, RISK-06
**Execution sequence:** 1

#### ST-01 — Restore eslint-config-react-app so the frontend builds and deploys again

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first in the sprint; ST-30 depends on it)

**Notes:** P1 release anchor. Lockfile fix and the CI production-build step proceed autonomously. Removing the Render dashboard-only `DISABLE_ESLINT_PLUGIN` workaround, or recording it in `render.yaml`, needs the Infrastructure & Operations Owner's Render dashboard access (RISK-01). Raise the Human-Delegation at sprint start. RISK-06: the production build may fail for a second reason once the config is restored; the new CI step surfaces it before merge.

**Staging-only ACs:** AC 1 `post-merge` (`deploy.yml` on `main` and production serving the build), tracked by **BLG-OPS-200**. AC 2 staging-only (Render staging build from `main` with no dashboard-only workaround).

**Status at sprint open: ready**

---

#### ST-02 — Compute the SPY market regime from Alpaca bars when Yahoo Finance fails

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (ST-03 follows it; same function `check_market_regime()`)

**Notes:** RISK-03: same branch and fixed order as ST-03 to ST-06.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-03 — Show an unknown market regime instead of silently defaulting to risk-on

**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner; Head of UX & Design
**Estimated effort:** 1.00
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-02 (must complete first)

**Notes:** First sub-step: the Strategy Rules & System Intent Owner's dated ruling on what "regime unknown" means for §4.2.1 entries and the §8.2 risk-off job. Raise at sprint start (RISK-05). Estimate raised 0.50 → 1.00 at planning (Product Owner, 2026-10-29) for the addendum's scope: four regime surfaces (Dashboard Card 4, the Signals market status bar, the customisable Dashboard regime widgets and the dashboard), local frontend fallbacks defaulting to `"unknown"`, `GET /market/status` and `GET /market/regime` contract and `openapi.yaml` changes, and the extra Signals-bar Playwright check. Read with `stage4_backlog_slice_addendum.md` and `market-regime-unknown/decision_record.md`. The `strategy_rules.md` §4.2.1/§8.2 write is a case (c) named-file write, confirmed at seal and applying only if the ruling changes the behaviour those sections describe.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-04 — Use the last good GBP/USD rate, with its age, before the fixed 1.27 fallback

**Owner:** Backend Engineering Patterns Owner; Head of UX & Design
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (ST-05 and ST-06 follow it)

**Notes:** BLG-GOV-72 fast-path (c): locked `fx-rate-source-indicator/decision_record.md`. The addendum adds `fx_rate_source`/`fx_rate_as_of` to `GET /market/status` and removes the Signals page's 1.3611 constant. The estimate is held, because the field set is shared with ST-05.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-05 — Flag an FX fallback instead of applying it silently

**Owner:** Backend Engineering Patterns Owner; Head of UX & Design
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-04 (must complete first)

**Notes:** Reuses ST-04's stored rate, source and age (RISK-03). Contracts and `openapi.yaml` go in the same commit. The Signals FX tile source-line Playwright check comes from the decision record.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-06 — Make the System Status Yahoo Finance check detect an outage

**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** ST-03, ST-04 (must complete first)

**Notes:** Design Pre-Approved (`system_status.md` v1.4). `details` carries a plain `reason` string.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-07 — Flag stale prices on GET /positions and the Positions page

**Owner:** Backend Engineering Patterns Owner; Head of UX & Design
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None (ST-08 follows it)

**Notes:** Locked `stale-price-marker/decision_record.md`; `positions.md` v2.21. Contract and `openapi.yaml` in the same commit.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-08 — Make the stale-price explanation reachable on touch, keyboard and screen readers

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-07 (must complete first)

**Notes:** BLG-GOV-72 fast-path (c): wording is locked in the decision record. The decision record's added accessible-description checks (Dashboard Card 2 link and the Positions marker) are needed, or filed before the PR opens.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-02 — Sizing, Exit & Position Correctness

**Maps to:** S2-09 – S2-14
**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner; Head of UX & Design; Data Model & Domain Schema Owner
**Estimated effort:** 2.30 days
**Risk IDs:** RISK-02, RISK-04, RISK-05
**Execution sequence:** 2

#### ST-09 — US position sizing divides the stop distance by the GBP/USD rate

**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None (first in EPIC-02; ST-13 follows it)

**Notes:** First sub-step: the Strategy Rules & System Intent Owner's dated FX-convention confirmation against §4.1.2/§4.1.5 (RISK-05). The fix is needed whatever the ruling. The `strategy_rules.md` §4.1.5 Known Deviation closure (and §4.1.3 if ambiguous) is a case (c) named-file write confirmed at seal. Design Pre-Approved if the Trade Entry risk display carries the same inversion.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-10 — POST /positions/{id}/exit returns its documented 404 and 400, not 500

**Owner:** Backend Engineering Patterns Owner; API Contracts & Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None (ST-29 in EPIC-05 depends on it)

**Notes:** Cross-EPIC: EPIC-02 merges before EPIC-05.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-11 — Daily Position Monitor stops suggesting "Stop Loss Hit" during the grace period

**Owner:** Frontend Specifications & UX Documentation Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Locked `monitor-grace-aware-suggestions/decision_record.md`. The Monitor's positions must carry `grace_period`, `current_trailing_stop` and `risk_off_exit`. The record's added Playwright checks (hold reason; risk-off precedence) are needed, or filed before the PR opens.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-12 — GET /portfolio P&L handles a US position whose fill_price is NULL

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-13 — Positions data dictionary states that entry_price is stored in GBP

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** ST-09 (must complete first)

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-14 — Review-cadence grace suppression and the grace alert agree once grace has ended

**Owner:** Frontend Specifications & UX Documentation Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Design gate chose option (a), the code fix (`last-reviewed-ended-grace/decision_record.md`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-06 — Operations, Cost & Security

**Maps to:** S2-38 – S2-43
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Head of Engineering; Cybersecurity & Trust Lead
**Estimated effort:** 4.05 days
**Risk IDs:** RISK-01
**Execution sequence:** 3

#### ST-38 — Arc 2 compute cost review

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** None (ST-39 follows it)

**Notes:** Gate verified at Release Planning (`run_manifest.md`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-39 — Compute cost trending by feature area

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** ST-38 (must complete first)

**Notes:** The report method and structure proceed autonomously. Populating it needs production cost data: Human-Delegation (RISK-01).

**Staging-only ACs:** AC 2 `post-merge`/production data (populated for a complete month), tracked by **BLG-OPS-201**.

**Status at sprint open: ready**

---

#### ST-40 — CI pipeline runtime audit

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`

**Dependencies:** None

**Notes:** Reads 3 recent `main` runs through `gh`. Candidates are filed through `/backlog-add`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-41 — Daily AI cost check covers the last hours of the day

**Owner:** FinOps & Resource Architect; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-41`

**Dependencies:** None

**Notes:** `ai_endpoints.md` §POST /ai/check-daily-cost updated.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-42 — Make ci-usage-report.yml's monthly commit succeed

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-42`

**Dependencies:** None

**Notes:** The workflow fix proceeds autonomously. The confirming run must be on `main` (`workflow_dispatch`, `year_month=2026-09`), and may need a branch-rule bypass (RISK-01).

**Staging-only ACs:** AC 1 and AC 2 `post-merge` (a run on `main` succeeds; `2026-09.md` exists), tracked by **BLG-OPS-202**.

**Status at sprint open: ready**

---

#### ST-43 — Per-environment CORS allow-list

**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-43`

**Dependencies:** None

**Notes:** Code and test proceed autonomously. Setting the per-environment variable on Render needs dashboard access (Human-Delegation, RISK-01). The slice's header says "ST-43 AC 1", but the post-merge AC is AC 2 (preflight checks); AC 1 is CI-verifiable.

**Staging-only ACs:** AC 2 staging-only and `post-merge` (staging and production preflight checks on the deployed services), tracked by **BLG-SEC-44**.

**Status at sprint open: ready**

---

### EPIC-03 — AI Output Safety & Audit Hygiene

**Maps to:** S2-15 – S2-23
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 3.60 days
**Risk IDs:** RISK-01, RISK-02, RISK-04, RISK-05
**Execution sequence:** 4

#### ST-15 — Journal summary catches advisory phrasings the trading-change check misses

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (ST-18 follows it; shared `ai_s13_boundary_test_suite.md`)

**Notes:** First sub-step: the AI Compliance & Governance Officer's extension of ruling `ESC-EXEC-20261027-03` (A), a §13 determination answering §13.1/§13.2 (RISK-05).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-16 — Daily briefing ticker caveat ignores indicator and macro acronyms

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None (ST-17 follows it)

**Notes:** AC 4: the live-log review of further tokens runs only if the user grants a read; otherwise it is filed. Neither path blocks the story.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-17 — Chat stop-time note is not attributed to the focus ticker when a sentence names another ticker

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** ST-16 (must complete first)

**Notes:** First sub-step: the AI Compliance & Governance Officer's amendment of `ESC-EXEC-20261027-01` (B) condition 3, answering §13.2 and the §13.5 "BLG-FEAT-50/51" roster row (RISK-05). ST-20 lands first or rebases (same stop-time formatter).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-18 — Monthly P&L narrative scan stops flagging retrospective and discourse wording

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** ST-15 (must complete first)

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-19 — A debrief that fails compliance then errors writes one audit row

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None (ST-21 follows it)

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-20 — Stop recalculation times in briefing and chat are converted to UTC

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None (land before ST-17, or rebase onto it)

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-21 — Run the claude_audit_log column checks once per process

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** ST-19 (must complete first)

**Notes:** Calibrated 0.5 → 1.0d at Release Planning for the `ensure_*` sweep.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-22 — Retire the unused POST /trade-plans/{plan_id}/generate-thesis endpoint

**Owner:** Backend Engineering Patterns Owner; API Contracts & Documentation Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None (coordinate with ST-28; whichever merges second rebases)

**Notes:** Route removal chain in one commit: `routers/test.py` entry, `SystemStatus.js` fallback count, `SC-SS-01b`, `openapi.yaml`, `api_changelog.md`. The `strategy_rules.md` §13.5 "Gemini thesis generation" roster row update is a case (c) named-file write confirmed at seal.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-23 — First live quarterly AI output sample against the §13 boundary

**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** ST-15, ST-16, ST-17, ST-18 (must complete first)

**Notes:** Reading production samples needs a production credential: Human-Delegation to the AI Compliance & Governance Officer with the Infrastructure & Operations Owner (RISK-01). Raise at sprint start. AC 3 re-acknowledges `ESC-EXEC-20260910-01` (deferred trigger met).

**Staging-only ACs:** AC 1 `post-merge`/production data (10 production AI outputs reviewed), tracked by **BLG-GOV-399**.

**Status at sprint open: ready**

---

### EPIC-04 — Reports, Dashboard & System Status UI (build-and-ship)

**Maps to:** S2-24 – S2-28
**Owner:** Financial Reporting & Records Owner; Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 2.60 days
**Risk IDs:** RISK-04
**Execution sequence:** 5

#### ST-24 — Monthly P&L breakdown by §8 exit condition

**Owner:** Financial Reporting & Records Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None (first in EPIC-04)

**Notes:** BLG-GOV-72 fast-path (c): locked `monthly-pnl-exit-condition-breakdown/decision_record.md`; `reports.md` v0.26. Adds `by_exit_condition` on `GET /reports/monthly-pnl` (contract and `openapi.yaml` in the same commit). The record's added checks ("unavailable" state; light-theme axe with the card shown) are needed, or filed before the PR opens.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-25 — Recent Trades glyph and amount agree at a half-penny loss

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** Design Pre-Approved (`dashboard.md` v3.10 §Card 5).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-26 — Pluralise the month counts in the monthly P&L summary fallback

**Owner:** Financial Reporting & Records Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None (ST-27 follows it)

**Notes:** Wording only: the FI-P3-02 code-review exception applies.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-27 — Keep a generated monthly P&L summary visible after switching tax year and back

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** ST-26 (must complete first)

**Notes:** Design Pre-Approved (`reports.md` v0.26 §AI Summary, Behaviour → Load).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-28 — Group /reports endpoints on the System Status page

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None (coordinate with ST-22; EPIC-03 merges first, so EPIC-04 rebases)

**Notes:** `/reports` → Analytics, per `system_status.md` v1.4.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-07 — Specs & Governance

**Maps to:** S2-44 – S2-54 (S2-51 deferred at planning)
**Owner:** Head of Specs Team; PMO Lead; Metrics Definitions & Analytics Owner; Strategy Rules & System Intent Owner; API Contracts & Documentation Owner; Frontend Specifications & UX Documentation Owner; Challenger
**Estimated effort:** 6.30 days
**Risk IDs:** RISK-04, RISK-05
**Execution sequence:** 6

**Deferred at planning:** ST-51 (`BLG-GOV-185`, 0.50d). Its AC is already met by `docs/specs/metrics_definitions.md` `## Appendix D — Change Log` (rows to v1.33.0, 2026-10-27). Product Owner, 2026-10-29. Recorded as `deferred_at_planning` for delivery verification traceability.

#### ST-44 — check_execution_state_consistency.py checks deviations_filed and the escalation map

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-44`

**Dependencies:** None (ST-45 follows it)

**Notes:** Product Owner override (`LL-v9.13-P3-04`). Edits `execution_prompt.md` §9.2 under the CLAUDE.md §6 checklist (version bump, `OPERATIONAL_GUIDE.md` §14 and phase header, `prompt_change_log.md`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-45 — Give the gate scan's "gating item shipped" findings a write-back path

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.25
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-45`

**Dependencies:** ST-44 (must complete first; both bump `OPERATIONAL_GUIDE.md`)

**Notes:** First sub-step: the Head of Specs Team chooses option (a) `release_planning_prompt.md` §1.3a carve-out or (b) a `groom backlog` standing step (RISK-05). Both are pre-specified. CLAUDE.md §6 checklist; §8 step 2a per file against ST-44. The live cases `BLG-OPS-85`/`BLG-OPS-21` ship in this release (ST-38/ST-39), so the AC 2 check needs another open item at the next engine run.

**Staging-only ACs:** AC 2 `post-merge` (after the next run of the chosen engine), tracked by **BLG-GOV-400**.

**Status at sprint open: ready**

---

#### ST-46 — Document the gate-status indicator as a reusable component pattern

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-46`

**Dependencies:** None

**Notes:** The owner's review is recorded in-story.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-47 — risk_dashboard.md names only fields GET /portfolio returns

**Owner:** Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-47`

**Dependencies:** None

**Notes:** Edits `risk_dashboard.md` on top of the design gate's v0.1.14. Bump to v0.1.15 or later. EPIC-01's ST-05 implements against the same file.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-48 — Align Appendix F's effort-weighted PVR table and status with the script

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-48`

**Dependencies:** None (the ST-51 dependency is void: ST-51 is deferred at planning as already met)

**Notes:** Writes its changelog row to the existing `metrics_definitions.md` `## Appendix D — Change Log`. `metrics_definitions.md` is shared with ST-24 (EPIC-04 merges first).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-49 — Trade plan contract lists the 7 DS-21 statuses

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-49`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-50 — Confirm "win rate" is computed the same way on every surface

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-50`

**Dependencies:** None

**Notes:** Discrepancies are filed through `/backlog-add`, not fixed.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-52 — §13 boundary worked examples

**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-52`

**Dependencies:** None

**Notes:** Companion doc `docs/product/decisions/section13_boundary_examples.md`, so there is no `strategy_rules.md` write. The Strategy Rules & System Intent Owner's review is recorded in-story, answering each cited clause.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-53 — Governance overhead audit

**Owner:** PMO Lead; Challenger
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-53`

**Dependencies:** None

**Notes:** AC 2's link to the next rebalance is recorded as a carry-forward in this cycle's closure, so no `claude/roadmap/*` write is needed.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-54 — Spec debt aging report

**Owner:** Head of Specs Team
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-54`

**Dependencies:** None

**Notes:** Wiring it into a governance prompt is filed separately, not done here.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-05 — Test Coverage & Test Tooling

**Maps to:** S2-29 – S2-37
**Owner:** Director of Quality; QA & Testing Owner; API Contracts & Documentation Owner
**Estimated effort:** 4.50 days
**Risk IDs:** RISK-01, RISK-04
**Execution sequence:** 7

#### ST-29 — Cover the Positions-page Exit modal submit in Playwright

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** ST-10 (EPIC-02, must complete first)

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-30 — Staging visual check of the layout changed by tailwind-merge in cn()

**Owner:** Director of Quality; Head of UX & Design
**Estimated effort:** 0.50
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** ST-01 (EPIC-01, must complete first)

**Notes:** A human staging pass in both themes (Head of UX & Design or Director of Quality), Human-Delegation (RISK-01). Results are recorded in this cycle's QA evidence.

**Staging-only ACs:** AC 1 staging-only (human staging run in both themes; date and pages recorded).

**Status at sprint open: ready**

---

#### ST-31 — Pre-commit OpenAPI contract check reads staged content

**Owner:** QA & Testing Owner; API Contracts & Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None (early in EPIC-05)

**Notes:** Product Owner override (`LL-v9.13-P3-01`). Implement first on the EPIC-05 branch. Other EPICs benefit only once EPIC-05 merges (it merges last), so the benefit to this sprint's other commits is limited.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-32 — Confirm the conftest.py AST scan still covers every backend module

**Owner:** QA & Testing Owner
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** Shares `tests/conftest.py` with ST-36; land ST-32 first.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-33 — Behaviour test: the grace warning ignores settings.min_hold_days

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-34 — Assert the stop-details tooltip time under a non-UTC browser timezone

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-35 — Assert the applied theme in every Reports/Notifications axe scan

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-36 — Stop test files adding backend/services/ to sys.path

**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** None (merges late in EPIC-05)

**Notes:** Touches many test files and `tests/conftest.py` (after ST-32).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-37 — Stop the ⌘K hint toast intercepting the chat submit click in SC-AC-03

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units (28.00 ceiling) |
| Total estimated effort (in-scope) | 28.00 days (53 stories) |
| Utilisation | 100% of the band ceiling. This is above the 95% advisory buffer floor; the Product Owner chose to proceed at the ceiling, 2026-10-29 |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-51 (`BLG-GOV-185`) | EPIC-07 | Already met: `metrics_definitions.md` has `## Appendix D — Change Log`. Product Owner, 2026-10-29. `deferred_at_planning`; the 0.50d moved to ST-03. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-02: Strategy Rules & System Intent Owner confirmation of the three case (c) `strategy_rules.md` lines | Strategy Rules & System Intent Owner | No. **Resolved 2026-10-29: all three confirmed (see sign-off below)** |
| Rulings raised at sprint start: ST-03, ST-09 (Strategy Rules & System Intent Owner); ST-15, ST-17 (AI Compliance & Governance Officer); ST-45 (Head of Specs Team) | As listed | No |
| Human-Delegation raised at sprint start: ST-01 Render dashboard; ST-23 production AI samples; ST-30 human staging pass in both themes; ST-39 production cost data; ST-42 run on `main` (possible branch-rule bypass); ST-43 Render environment variable | Infrastructure & Operations Owner; AI Compliance & Governance Officer; Director of Quality; FinOps & Resource Architect | No |
| Post-merge ACs tracked by BLG-OPS-200 (ST-01), BLG-GOV-399 (ST-23), BLG-OPS-201 (ST-39), BLG-OPS-202 (ST-42), BLG-SEC-44 (ST-43), BLG-GOV-400 (ST-45), filed 2026-10-29 | Sprint Execution Engine | No |
| For any other staging-only AC whose sign-off is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |
| Initialise ST-51 as `deferred_at_planning` in `execution_state.json` (STEP 5.2 traceability) | Sprint Execution Engine | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (as drafted), 2026-10-29
**Scope confirmed:** Confirmed: 53 stories across 7 EPICs in a single sprint. ST-51 is deferred at planning as already met, 2026-10-29
**Capacity confirmed:** Confirmed: 28.00 / 28.00 (100%), proceeding at the ceiling above the 95% buffer floor. ST-03 rises 0.50 → 1.00d for the addendum's four-surface scope; ST-04/ST-05 estimates held, 2026-10-29
**Deferred execution blockers accepted (if any):** N/A (none)
**Pre-sprint decision RISK-02:** Resolved. All three case (c) lines below are confirmed by the Strategy Rules & System Intent Owner, 2026-10-29

### Named-file writes

- Named-file write: `claude/strategy/strategy_rules.md` §4.2.1 and/or §8.2, the regime-unknown behaviour text, only if ST-03's ruling changes the behaviour those sections describe, with its `STRATEGY_VERSION_REGISTRY` entry. Authorised under execution_prompt.md §7 named-file rule, case (c) (ST-03).
  **Strategy Rules & System Intent Owner confirmation:** Confirmed, 2026-10-29
- Named-file write: `claude/strategy/strategy_rules.md` §4.1.5, closing the Known Deviations entry for `BLG-BE-190`; and §4.1.3, stating the US sizing formula if the owner finds it ambiguous. Registry entry included. Authorised under execution_prompt.md §7 named-file rule, case (c) (ST-09).
  **Strategy Rules & System Intent Owner confirmation:** Confirmed, 2026-10-29
- Named-file write: `claude/strategy/strategy_rules.md` §13.5, updating the "Gemini thesis generation" roster row to cite the surviving contract or record the endpoint's retirement. Registry entry included. Authorised under execution_prompt.md §7 named-file rule, case (c) (ST-22).
  **Strategy Rules & System Intent Owner confirmation:** Confirmed, 2026-10-29

Each write ships in one commit with its §16 Change Log row, its `backend/strategy_version_registry.py` entry (with `tests/test_strategy_version_registry.py` passing) and the §15 re-run. Bumps are taken in merge order (CLAUDE.md §8 step 2a).

No `claude/roadmap/*` write is planned. No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

For information, outside the named-file rule: ST-44 and ST-45 edit governance prompts (`execution_prompt.md`; `release_planning_prompt.md` or `backlog_management_prompt.md`), with `OPERATIONAL_GUIDE.md` and `prompt_change_log.md`, under the CLAUDE.md §6 governance edit checklist.

**Signed off by:** Product Owner
**Date:** 2026-10-29
