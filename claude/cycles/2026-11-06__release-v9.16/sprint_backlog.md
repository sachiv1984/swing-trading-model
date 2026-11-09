**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-11-09
**Cycle:** 2026-11-06__release-v9.16
**Release:** v9.16
**Sprint Goal:** Ship Site Structure & Usability Phase 2 complete (job-based sidebar with parent and onward links, the Dashboard Today list, "Plan this" with suggested size, the plan-linked pre-entry acknowledgement fix `BLG-FE-271`, and the first semantic colour tokens), and close the Anthropic key exposure by rotating the overdue key (`BLG-OPS-214`, P1) and removing the key secret from the public Pages build (`BLG-OPS-213`).
**Backlog Slice Source:** Original: `claude/cycles/2026-11-06__release-v9.16/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-03, ST-04, ST-05, ST-07 and ST-12)

# Sprint Backlog — 2026-11-06__release-v9.16

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-05 → EPIC-07 → EPIC-06 → EPIC-03 → EPIC-04.
- **EPIC-01** goes first. It owns `Layout.js`, the nav Playwright specs and `navigation.md` §Onward Links.
- **EPIC-02** goes second. It owns `TradePlan.js` (ST-05, ST-07, ST-08), the Dashboard Today components and `strategy_rules.md`. ST-07 rebases on EPIC-01's `navigation.md`.
- **EPIC-05** goes third. Backend fixes and spec debt; it owns `data_model.md` ahead of EPIC-04 ST-13.
- **EPIC-07** goes fourth. It owns the governance-file bumps (`post_ship_closure.md`, `OPERATIONAL_GUIDE.md`, `prompt_change_log.md`).
- **EPIC-06** goes fifth. ST-26/ST-27 need EPIC-02 on `main`; ST-25's possible `shared_standards.md` bump rebases on EPIC-07 and is renumbered per CLAUDE.md §8 step 2a, per file.
- **EPIC-03** goes sixth. ST-09 regenerates visual baselines for both themes over EPIC-01 and EPIC-02 (RISK-03); ST-10 rebases on every `src/` input change.
- **EPIC-04** goes last. ST-13 and ST-14 are conditional on dates inside the sprint (2026-11-09, ~2026-11-12). ST-11's P1 rotation and revocation are console/Render work raised at sprint start and do not wait for the merge.

**Fallback:** EPIC-04 may merge first if ST-13 and ST-14 have both cleared or been returned by then (this brings `BLG-OPS-215`'s secret deletion forward); it then rebases nothing and EPIC-02 rebases on its `TradePlan.js` change. EPIC-03 may never merge before EPIC-01 or EPIC-02.

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch checks whether the file exists before creating its own. If it exists, the branch appends its own section and never overwrites. No story is `deferred_at_planning`.

**Shared files across EPICs:**
- **`src/pages/TradePlan.js`** (EPIC-02 ST-05, ST-07, ST-08; EPIC-04 ST-12; EPIC-03 ST-10): EPIC-02 owns; later EPICs rebase.
- **`docs/specs/frontend/pages/navigation.md`** (EPIC-01 ST-03; EPIC-02 ST-07): EPIC-01 owns; ST-07 takes the next version.
- **`DashboardHome`, `DashboardCard`, `DataTable`, `PageHeader` and visual baselines** (EPIC-02 ST-06; EPIC-03 ST-09): EPIC-02 owns the components; EPIC-03 regenerates baselines last.
- **`docs/specs/data_model.md`** (EPIC-05 ST-22; EPIC-04 ST-13): EPIC-05 owns; EPIC-04 rebases.
- **`OPERATIONAL_GUIDE.md`, `prompt_change_log.md`, governance prompts** (EPIC-07 ST-28, ST-29 if any, ST-30; EPIC-06 ST-25): EPIC-07 owns. Apply CLAUDE.md §6 and §8 step 2a per co-bumped file.
- **`claude/strategy/strategy_rules.md`, `backend/strategy_version_registry.py`** (EPIC-02 ST-05 only).
- **`claude/backlog/backlog.md`:** new items via `/backlog-add` (ST-27 and any follow-ups). Run `scripts/check_backlog_item_integrity.py` after each §8 merge (step 2c).

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — Site Structure & Usability Phase 2: Navigation & Wayfinding (build-and-ship)

**Maps to:** S2-01 – S2-04
**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 6.00 days
**Risk IDs:** RISK-03
**Execution sequence:** 1

#### ST-01 — Build the job-based sidebar and surface Trade Plans and Research

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first in EPIC-01; ST-02 and ST-03 follow)

**Notes:** BLG-GOV-72 fast-path (c): locked `navigation.md` v2.0 (§Areas, §Page Placement, §Default Expansion, §Area Header, §Active Item, §Alert Badge Integration, §Responsive Behaviour). Desktop and mobile drawer. Owns `Layout.js` and the nav Playwright specs (RISK-03). Head of UX & Design reviews the build against the spec; Head of Engineering implements.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-02 — Add a parent link on detail pages

**Owner:** Head of Engineering
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01

**Notes:** Locked `navigation.md` v2.0 §Parent Links: Trade Plan, Research `/research/:ticker`, Notification Preferences, Notification History.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-03 — Give each dead-end page an onward next-step link

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** ST-01

**Notes:** Addendum: 11 dead-end pages, not 8 (adds Settings, Trade History, Analytics empty state). Links per `navigation.md` v2.0 §Onward Links. EPIC-01 owns `navigation.md`; ST-07 later adds its two rows.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-04 — Anchor the digest's Risk Dashboard link to the right section

**Owner:** Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None

**Notes:** Addendum (Product Owner, 2026-11-06): `?section=strategy-compliance` on Analytics (`analytics.md` v2.3 §19.1), plus a third digest footer link "Strategy Compliance"; Risk Dashboard link stays page-level. Design: `digest-section-link/decision_record.md` (scroll timing, reduced motion, focus, unknown-id fallback). Also update `si05_digest_service.py` `_format_deep_links()` and its test, and mark journey map F-04 resolved in `docs/ux/si05_user_journey_map.md`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-02 — Site Structure & Usability Phase 2: Today List & Signal-to-Entry Flow (build-and-ship)

**Maps to:** S2-05 – S2-08
**Owner:** Head of Engineering; Head of UX & Design; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 7.75 days
**Risk IDs:** RISK-02, RISK-03, RISK-04
**Execution sequence:** 2

#### ST-05 — Require the acknowledgement on plan-linked Trade Entry when the plan's checks were WARN/FAIL

**Owner:** Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (first in EPIC-02)

**Notes:** Addendum: `TradePlan.js` must start sending `pre_entry_validation_snapshot` on save (`trade_plan.md` v1.22 §5e: `captured_at`, `advisory_status`, `checks`, `inputs`; JSONB, no migration). Age threshold 24 hours (`position_form.md` v1.14); acknowledgement = `pre_entry_override_acknowledged: true`. Design: `plan-linked-pre-entry-checks/decision_record.md`; add a pointer from §2.1 of the v9.15 `trade-entry-pre-entry-checks/decision_record.md`. AC 4 is a case (c) named-file write, confirmed at seal (RISK-02, below): ship it in one commit with its §16 Change Log row, `DOCUMENTATION_ONLY_VERSIONS` entry (`tests/test_strategy_version_registry.py` passing) and §15 re-run. Frontend Specifications & UX Documentation Owner implements the spec/UI; Strategy Rules & System Intent Owner owns the AC 4 closure.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-06 — Build the "Today" action list on the Dashboard

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 3.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Locked `dashboard.md` v4.0 §1B (TL-01..TL-29) except TL-09/TL-10 (RISK-04: Stops moved group not rendered until `BLG-BE-205`). Playwright in light and dark. Owns `DashboardHome`; merges before EPIC-03 regenerates baselines.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-07 — Add "Plan this" to Signals and Screener rows

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (before ST-08)

**Notes:** Addendum: from Signals, pass `signal_id`; Trade Plan §5a.1 shows Signal Context for any status except `dismissed`; Screener rows pass no `signal_id`; clicking does not change signal status. Design: `signal-to-plan-flow/decision_record.md`; specs `signals.md` v0.9, `screener_results.md` v1.11 §11.1, `trade_plan.md` v1.22 §2/§5a.1. Add Signals → Trade Plan and Screener → Trade Plan rows to `navigation.md` §Onward Links (rebase on EPIC-01).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-08 — On Trade Plan, show the suggested size before asking for shares

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-07

**Notes:** `trade_plan.md` v1.22 §5f; deterministic §4.1 size, advisory and editable (`signal-to-plan-flow`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-03 — Site Structure & Usability Phase 2: Colour Tokens & Input Contrast (build-and-ship)

**Maps to:** S2-09 – S2-10
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 3.00 days
**Risk IDs:** RISK-03
**Execution sequence:** 6

#### ST-09 — Semantic colour tokens for the base, card and table shells

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** EPIC-01 and EPIC-02 on `main` (baselines)

**Notes:** Design: `semantic-colour-tokens/decision_record.md`; `design_system.md` v1.25 §Semantic Colour Tokens. No new colours: eight `app-*` tokens reuse measured v1.23 pairs. Regenerate visual baselines for both themes after EPIC-01/02 merge (RISK-03).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-10 — Inputs apply dark:text-slate-400 to typed text instead of the placeholder

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** ST-09 (if it adopts the text token)

**Notes:** `design_system.md` v1.25 §Input Text Colours. 18 sites in 8 files under `src/` (count named at v9.14). Rebases on everything else.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-04 — Anthropic Key Security & Operations Baselines

**Maps to:** S2-11 – S2-15
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 1.10 days
**Risk IDs:** RISK-01, RISK-05
**Execution sequence:** 7

#### ST-11 — Rotate the Anthropic API key (overdue since 2026-08-25) and revoke the old key

**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None (P1: delegation raised first in the sprint)

**Notes:** Human-Delegation at sprint start: new key in the Anthropic console, `ANTHROPIC_API_KEY` on Render staging (check one AI endpoint) then production, revoke the 2026-05-25 key. Revoking is safe before ST-12 merges: the Pages build only tests the secret's presence and makes no Anthropic call (`BLG-OPS-213` Problem). Secret deletion is ST-12's post-merge step (`BLG-OPS-215`), not this story's. Repo AC 3 (inventory and schedule dates) is autonomous once the date is known.

**Staging-only ACs:** AC 1 (console: one active key, old key revoked) and AC 2 (AI endpoint succeeds on staging and production) need console and Render access — Human-Delegation, in-sprint, not merge-dependent. If either is still outstanding at PR time, file a tracking item before the PR opens (CLAUDE.md §2).

**Status at sprint open: ready**

---

#### ST-12 — Stop injecting REACT_APP_ANTHROPIC_API_KEY into the public GitHub Pages build

**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None (paired with ST-11)

**Notes:** Code change autonomous: replace or remove `HAS_AI` (`TradePlan.js:122`, `:946`), remove the secret from `deploy.yml:33`. Addendum: "behave as before" is measured against the production Pages build; controls appearing in local/CI builds is expected — update any Playwright spec asserting their absence. Do not delete the GitHub secret before this story is on `main` and Pages has redeployed. Rebases on EPIC-02 (`TradePlan.js`).

**Staging-only ACs:** AC 2 (`gh secret list` no longer lists the secret) `post-merge`, tracked by **BLG-OPS-215**. AC 3 (key the secret held revoked in console) staging-only — console, Human-Delegation, done with ST-11 in-sprint. AC 4 (AI controls behave as before) — Playwright in CI covers the build behaviour; the production Pages check is `post-merge`, tracked by **BLG-OPS-215**.

**Status at sprint open: ready**

---

#### ST-13 — Record the weekly market-data call-volume baseline from production

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** 2026-11-09 gate (7 days of production data after the 2026-11-02 deploy)

**Notes:** Conditional (§1.4b, RISK-05). Promote to firm only on a dated confirmation in execution; returned once at v9.15. Closes `DEL-20261027-04` and `DEL-20261027-06`. A return at sprint close is expected-path.

**Staging-only ACs:** AC 1 (DS-36 production Live Confirmation) and AC 2 (§4 weekly report) need production reads — Human-Delegation; production data, tracked by **BLG-OPS-197** (this story's own source item, which stays open until both are recorded).

**Status at sprint open: conditional — gate 2026-11-09**

---

#### ST-14 — Record the full screener run p50/p95 baseline from production

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** ≥10 nightly production screener runs after 2026-11-02 (~2026-11-12)

**Notes:** Conditional (§1.4b, RISK-05). Promote to firm only on a dated confirmation. Closes `DEL-20261027-05`.

**Staging-only ACs:** AC 1 (benchmark against production with the production API key) — Human-Delegation; production data, tracked by **BLG-OPS-198** (this story's own source item, which stays open until recorded).

**Status at sprint open: conditional — gate 2026-11-12**

---

#### ST-15 — Fail the staging smoke host check when the backend reports no Render service ID

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (`BLG-OPS-196` complete)

**Notes:** `scripts/staging_smoke_test.py` currently returns "known limit" on a missing `render_service_id`; make it a failure, read the expected ID from `STAGING_SERVICES` (single definition), update `tests/test_staging_smoke_test.py`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-05 — Backend Correctness, AI Ticker Check & Spec Debt

**Maps to:** S2-16 – S2-23
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; AI Compliance & Governance Officer; Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.20 days
**Risk IDs:** RISK-01, RISK-07
**Execution sequence:** 3

#### ST-16 — Exiting a US position with a NULL fill_price fails in the P&L arithmetic

**Owner:** Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None (before ST-17)

**Notes:** `native_entry_price(position, <stored fx_rate, else the exit fx_rate>)` in `exit_position()`; unit test.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-17 — Lifecycle badge and Risk page disagree for a US row with no fill_price and no fx_rate

**Owner:** Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** ST-16

**Notes:** Choose one fallback (all UNKNOWN or all live-rate) against `position_endpoints.md`'s `position_state` note; equal effort either way.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-18 — Frozen-stop marker is not written when the on-load recompute has no live price

**Owner:** Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Write the marker, or document the exclusion in `position_endpoints.md`; either satisfies the AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-19 — Read production briefing ticker-caveat tokens and add any non-tickers

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None (before ST-20)

**Notes:** Human-Delegation at sprint start: the user supplies the token list with counts since 2026-10-30 from production Render logs, or grants a one-off read. Second attempt (v9.15 ST-24 left it `TBD`).

**Staging-only ACs:** AC 1 (token list with counts) needs a production log read — Human-Delegation, in-sprint, not merge-dependent. If still outstanding at PR time, `BLG-AI-27` (this story's source) stays open as its tracker and the reason is recorded in QA evidence.

**Status at sprint open: ready**

---

#### ST-20 — Handle `_NON_TICKER_WORDS` entries that are also real tickers deliberately

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** ST-19; AI Compliance & Governance Officer ruling

**Notes:** First sub-step: the AI Compliance & Governance Officer rules on collisions (PM, MA, ON and any other universe collision) before code. Then implement, test, and state the handling in `ai_endpoints.md` check 3 and the chat focus paragraph.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-21 — Journal summary: remove the stale AI_MODEL override line, or cost the model actually used

**Owner:** API Contracts & Documentation Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Either option satisfies the AC. If a contract changes, keep `openapi.yaml` consistent in the same commit.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-22 — Add the 11 missing positions columns to the positions data dictionary

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Decide `exit_note`: remove or keep as a marked historical row (both meet the AC). EPIC-05 owns `data_model.md` edits ahead of EPIC-04 ST-13's DS-36 entry.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-23 — Point settings.md at the moved strategy constants module

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** `settings.md:121` still names `src/lib/strategyParameters.js`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-06 — Arc 2 Retrospective: QA Protocol, Lifecycle Test & Journey Map

**Maps to:** S2-24 – S2-27
**Owner:** QA Lead; Head of Specs Team; Head of UX & Design; Product Owner
**Estimated effort:** 6.50 days
**Risk IDs:** RISK-06, RISK-07
**Execution sequence:** 5

#### ST-24 — Arc 2 end-to-end QA protocol

**Owner:** QA Lead
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** ST-26

**Notes:** Protocol in `docs/qa/`; Playwright happy path may reuse ST-26. Cleared-gate evidence (PT-04 ✅ Shipped v6.1; Arc 2 ✅ Fully Complete, `current_roadmap.md`) confirmed at seal by the QA Lead (agent-mediated) and the Product Owner — AC 3 met.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-25 — Arc 2 DoQ standards review

**Owner:** QA Lead; Head of Specs Team
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** If it amends `shared_standards.md`, apply CLAUDE.md §6 and coordinate version bumps with EPIC-07 (RISK-07; EPIC-07 merges first). Cleared-gate evidence confirmed at seal by the QA Lead (agent-mediated) — AC 3 met.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-26 — Trade plan lifecycle end-to-end test

**Owner:** QA Lead
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** EPIC-02 ST-07 and ST-08 merged

**Notes:** Must exercise the "Plan this" and suggested-size flow as built. Cleared-gate evidence confirmed at seal by the QA Lead (agent-mediated) and the Product Owner — AC 2 met.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-27 — Arc 2 user journey map

**Owner:** Head of UX & Design
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** ST-07

**Notes:** In `docs/ux/` alongside `si05_user_journey_map.md`. Cross-check findings against Site Structure & Usability programme items (incl. held Phase 3 `BLG-FE-257`–`263`, `265`) before filing via `/backlog-add`. Cleared-gate evidence confirmed at seal by the Product Owner — AC 3 met.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-07 — Governance Process

**Maps to:** S2-28 – S2-30
**Owner:** Head of Specs Team; PMO Lead; Base44 Frontend Prompt Owner
**Estimated effort:** 2.40 days
**Risk IDs:** RISK-07
**Execution sequence:** 4

#### ST-28 — Split-achievability carve-out: close a source item whose whole remainder has its own backlog items

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None (early in EPIC-07)

**Notes:** Deferred lessons-learnt patch (§1.4c step 1a). `post_ship_closure.md` STEP 3.1 and `OPERATIONAL_GUIDE.md` under the CLAUDE.md §6 checklist; per-file §8 step 2a check at merge.

**Staging-only ACs:** AC 2 (`BLG-AI-23`/`BLG-OPS-48` bannered or reasoned at the next `groom backlog`) `post-merge`, tracked by **BLG-GOV-414**.

**Status at sprint open: ready**

---

#### ST-29 — Arc velocity tracking dashboard

**Owner:** PMO Lead
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** Arc 2 report (v3.1–v6.1) from `claude/cycles/velocity_metrics.md` and cycle records; reusable format. Any governance prompt change making it a Release Planning input follows CLAUDE.md §6 in the same commit; otherwise file a backlog item. Cleared-gate evidence confirmed at seal by the PMO Lead (agent-mediated) — AC 3 met.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-30 — Base44 prompt versioning convention

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 1.25
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** Base44 Frontend Prompt Owner decision

**Notes:** First sub-step: dated decision on where the ST-id is recorded for each Base44 prompt draft. Then write it into `OPERATIONAL_GUIDE.md`/`execution_prompt.md` under CLAUDE.md §6, or into `base44_frontend_prompt_owner.md` working notes.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units (28.00 ceiling) |
| Total estimated effort (in-scope) | 27.95 days (30 stories; ST-13 and ST-14's 0.30d is conditional) |
| Utilisation | 99.8% of the band ceiling. This is above the 95% advisory buffer floor; the Product Owner chose to proceed, 2026-11-09 |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | None. All 30 slice items are in scope; ST-13 and ST-14 are conditional, not deferred. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-02: Strategy Rules & System Intent Owner confirmation of ST-05's case (c) `strategy_rules.md` line | Strategy Rules & System Intent Owner | No. **Resolved 2026-11-09: confirmed (see sign-off below)** |
| Human-Delegations raised at sprint start: ST-11 (P1, console + Render) and ST-12 console revocation; ST-19 production log tokens; ST-13 production read (gate 2026-11-09); ST-14 production benchmark (~2026-11-12) | Cybersecurity & Trust Lead; Infrastructure & Operations Owner; AI Compliance & Governance Officer; FinOps & Resource Architect | No |
| Rulings raised at sprint start: ST-20 (AI Compliance & Governance Officer); ST-30 (Base44 Frontend Prompt Owner) | As listed | No |
| Post-merge ACs tracked by BLG-OPS-215 (ST-12), BLG-GOV-414 (ST-28), BLG-OPS-197 (ST-13), BLG-OPS-198 (ST-14), filed or confirmed 2026-11-09 | Sprint Execution Engine | No |
| For any other staging-only AC whose sign-off is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (as drafted), 2026-11-09
**Scope confirmed:** Confirmed: 30 stories across 7 EPICs in a single sprint; ST-13 (gate 2026-11-09) and ST-14 (gate ~2026-11-12) conditional, 2026-11-09
**Capacity confirmed:** Confirmed: 27.95 / 28.00 (99.8%), proceeding above the 95% buffer floor, 2026-11-09
**Deferred execution blockers accepted (if any):** N/A (none)
**Pre-sprint decision RISK-02:** Resolved. ST-05's case (c) line below is confirmed by the Strategy Rules & System Intent Owner, 2026-11-09
**Cleared-gate evidence (ST-24, ST-26, ST-27):** Confirmed by the Product Owner, 2026-11-09 — PT-04 ✅ Shipped v6.1 and Arc 2 ✅ Fully Complete (`current_roadmap.md`). QA Lead (ST-24, ST-25, ST-26) and PMO Lead (ST-29) confirmed, agent-mediated (§5.3), 2026-11-09
**Pre-seal backlog filings:** BLG-OPS-215, BLG-GOV-414 (post-merge trackers) and BLG-SPEC-224, BLG-SPEC-225 (design gate observations), authorised and filed 2026-11-09

### Named-file writes

- Named-file write: `claude/strategy/strategy_rules.md` §4.2.1 Known deviation (v1.26) marked resolved as a documentation-only version, with its Change Log row and `backend/strategy_version_registry.py` `DOCUMENTATION_ONLY_VERSIONS` registry entry, once ST-05's fix ships. Authorised under execution_prompt.md §7 named-file rule, case (c) (ST-05 AC 4, RISK-02).
  **Strategy Rules & System Intent Owner confirmation:** Confirmed, 2026-11-09

The write ships in one commit with its §16 Change Log row, its registry entry (with `tests/test_strategy_version_registry.py` passing) and the §15 re-run.

No `claude/roadmap/*` write is planned. No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

For information, outside the named-file rule: ST-25, ST-28, ST-29 and ST-30 may edit governance prompts or `OPERATIONAL_GUIDE.md`, under the CLAUDE.md §6 governance edit checklist.

**Signed off by:** Product Owner
**Date:** 2026-11-09
