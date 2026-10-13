**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-10-13
**Cycle:** 2026-10-12__release-v9.12
**Release:** v9.12
**Sprint Goal:** Restore AI journal summaries for UUID trade IDs (BLG-BE-162, P1); make signal sizing, stops and position status correct across Signals, Positions and Risk; and let Trade Entry show the stop, risk and size before save. Also ship v9.12's accessibility, security, operations, spec and governance hygiene items.
**Backlog Slice Source:** Original: `claude/cycles/2026-10-12__release-v9.12/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-23, ST-24, ST-10 and ST-22)

# Sprint Backlog — 2026-10-12__release-v9.12

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-06 → EPIC-05 → EPIC-02 → EPIC-03 → EPIC-04.
- **EPIC-01** goes first because it carries the P1 anchor (ST-01).
- **EPIC-06** goes second, so ST-39's backlog-integrity check (RISK-07) and ST-46's `utils.*` stub guard are on `main` before the larger merges.
- **EPIC-05** precedes EPIC-02, so ST-37's §13 record refresh lands before ST-14's addendum.
- **EPIC-04** goes last: ST-26 follows ST-16/ST-20/ST-21 (RISK-05), and ST-28 needs the final tree.

**Fallback:** if EPIC-05 waits on the ST-34 or ST-38 delegations, EPIC-02 may merge first. ST-37 then keeps ST-14's appended addendum intact on rebase.

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch checks whether the file exists before creating its own. If it exists, the branch appends its own section and never overwrites.

**Shared files across EPICs:**
- **`openapi.yaml`** (EPIC-01 ST-01; EPIC-02 ST-10/15; EPIC-03 ST-17; EPIC-04 ST-26; EPIC-05 ST-33): EPIC-01 owns it. Take the union of additions and the highest version.
- **Route-registration chain** (`routers/test.py`, `SystemStatus.js` fallback count, `SC-SS-01b`; EPIC-02 ST-10 Branch A, EPIC-03 ST-17): EPIC-02 owns it. EPIC-03 recomputes the count from the merged `test.py`.
- **`data_model.md`** (EPIC-01 ST-01; EPIC-05 ST-34/38; EPIC-04 ST-26): EPIC-01 owns it. Keep migration blocks in ascending order.
- **`Positions.js` / `PositionCard.js`** (EPIC-02 ST-10/15; EPIC-03 ST-21/22/24): EPIC-02 owns them.
- **Settings page and create path** (EPIC-02 ST-16; EPIC-03 ST-20/21; EPIC-04 ST-26): EPIC-03 owns the page and EPIC-02 owns the create path.
- **The Gap Risk Flag §13 decision record** (EPIC-05 ST-37 body; EPIC-02 ST-14 addendum): EPIC-05 owns it.
- **`src/constants/strategy.js`** (moved from `src/lib/strategyParameters.js` by ST-21): EPIC-03 owns it.
- **`OPERATIONAL_GUIDE.md` and `prompt_change_log.md`** (EPIC-06 only): run the CLAUDE.md §6 checklist and the §8 step 2a check per file.
- **`backlog.md`:** new items only via `/backlog-add`, plus ST-29's `BLG-OPS-181` Notes line. Re-check new IDs after rebasing.

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — AI Feature Correctness & Cost Visibility

**Maps to:** S2-01 – S2-06
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Estimated effort:** 2.80 days
**Risk IDs:** RISK-01, RISK-04
**Execution sequence:** 1

#### ST-01 — Accept UUID trade IDs in the journal summary, end to end

**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (ST-06 lands after it: shared `ai_endpoints.md`)

**Notes:** P1, the release anchor (v9.11 verification acceptance condition, DL-085). Code, the backend test, `data_model.md`, `ai_endpoints.md` and `openapi.yaml` proceed autonomously in one commit. The `INTEGER[]`→`UUID[]` migration on staging and production and the Trade History staging run are Human-Delegation to the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner (RISK-01, DS-27/28/29 precedent). Raise at sprint start.

**Staging-only ACs:** AC 1 (journal summary from Trade History on staging returns content). AC 4, live-application half only (migration applied on staging and production, with verification output).

**Status at sprint open: ready**

---

#### ST-02 — Drop briefing actions that name a ticker outside the context

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** First of three stories in the briefing module. Each of ST-02/03/04 bumps `BRIEFING_PROMPT_VERSION`; execution may combine the ST-02 and ST-03 bumps into one, recorded in the golden fixtures.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-03 — Label available cash and starting capital separately in the briefing context

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-02 (same prompt module)

**Notes:** Prompt-context wording only.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-04 — Check that briefing and chat responses citing a stop include its recalculation time

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-02, ST-03 (same briefing module)

**Notes:** First sub-step: the AI Compliance & Governance Officer signs off the failure action (append the time from context, or log and count). Raise at sprint start. Applies to both briefing and chat.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-05 — Widen the monthly P&L narrative's instrument-directive scan to inflected and indirect wording

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Tightens the directive check that the v9.11 ST-25 §13 review's conditions rely on (design gate §13 pre-check).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-06 — Make the daily AI cost alert count Claude calls

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** ST-01 (shared `ai_endpoints.md`; land after it or rebase)

**Notes:** AC 3's "ST-23 cost estimate" is `docs/ops/ai_monthly_pnl_narrative_cost_estimate_2026-10-08.md` (v9.11 ST-23). If the scheduler that calls `POST /ai/check-daily-cost` is outside GitHub Actions and its run history cannot be read, AC 2's run record becomes a Human-Delegation to the Infrastructure & Operations Owner.

**Staging-only ACs:** AC 2, last-successful-run half only (the live scheduler's run record; naming the scheduler is a doc change).

**Status at sprint open: ready**

---

### EPIC-06 — Governance Tooling & Test Integrity

**Maps to:** S2-39 – S2-48
**Owner:** Head of Specs Team; PMO Lead; QA & Testing Owner; Director of Quality
**Estimated effort:** 5.40 days
**Risk IDs:** RISK-06, RISK-07
**Execution sequence:** 2

#### ST-39 — Check backlog item integrity after every cross-EPIC merge resolution

**Owner:** PMO Lead; Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** None (first in EPIC-06)

**Notes:** Edits CLAUDE.md §8 under Head of Specs Team authority, named in the AC (RISK-06). Until it merges, the v9.11 Carry-Forward #3 manual check applies after every merge resolution (RISK-07).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-40 — Report gated items whose gating backlog item has shipped, and read that list in Release Planning §1.3a

**Owner:** Head of Specs Team; Head of Engineering
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`

**Dependencies:** ST-39 (EPIC-06 order); before ST-41/42/43 (sequential governance bumps)

**Notes:** `release_planning_prompt.md` §1.3a edit with the full CLAUDE.md §6 checklist in the same commit. v9.11 closure action #8(b) edits the same section but is **not** added to this story's AC. It is a separate Head of Specs Team change (see Outstanding Actions). If it lands first, apply the CLAUDE.md §8 step 2a version check.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-41 — Script the execution_state.json read-back check from execution_prompt.md §9.2

**Owner:** Head of Engineering; Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-41`

**Dependencies:** ST-40 (sequential governance bumps)

**Notes:** `execution_prompt.md` §9.2 with the CLAUDE.md §6 checklist.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-42 — Name one Skill-Silo aggregation method in roadmap_prompt.md §7.1

**Owner:** Metrics Definitions & Analytics Owner; Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-42`

**Dependencies:** ST-41 (sequential governance bumps)

**Notes:** Any method-break note goes in `roadmap_prompt.md` §7.1, not `claude/roadmap/decision_log.md` (restated in the slice).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-43 — Rule on reduced-roster idea-intake windows, and cap them if permitted

**Owner:** Head of Specs Team; Product Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-43`

**Dependencies:** ST-42 (sequential governance bumps)

**Notes:** First sub-step: a Head of Specs Team + Product Owner ruling. Raise at sprint start. No design session artefact exists; the ruling is scoped by the AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-44 — Add a split-credit secondary tally to compute_role_share_history.py

**Owner:** Director of HR; PMO Lead
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-44`

**Dependencies:** ST-45 (extends its test file)

**Notes:** Named-file write: `claude/roadmap/role_share_history.md` (split-credit column). Kept `delegated_decision` per the release plan's RISK-06 mitigation (`ESC-CLOSE-20261006-01`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-45 — Add unit tests for compute_role_share_history.py and a STEP 7.1 pin

**Owner:** QA & Testing Owner; PMO Lead
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-45`

**Dependencies:** None (before ST-44)

**Notes:** None.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-46 — Scope utils.* test stubs so a reordered run passes

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-46`

**Dependencies:** None

**Notes:** 11 test files reference `sys.modules["utils…"]`. Run pytest via `backend/.venv/bin/python3` with a stub `DATABASE_URL`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-47 — Guard the positions.fees_paid NOT NULL invariant in the entry flow and SQL seeds

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-47`

**Dependencies:** None

**Notes:** Stub `DATABASE_URL`; no live DB access.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-48 — Remove the leaked sandbox /tmp path from backend/setup.cfg

**Owner:** QA Lead
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-48`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-05 — Spec & Data Model Hygiene

**Maps to:** S2-33 – S2-38
**Owner:** Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** 2.10 days
**Risk IDs:** RISK-01, RISK-04
**Execution sequence:** 3

#### ST-33 — Reconcile DELETE /trade-plans/{id}'s success envelope with conventions.md §12

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** None

**Notes:** Live behaviour is checked with the API test client.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-34 — Triage the drift detector's new live-vs-doc findings

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None (before ST-38: both edit `data_model.md`)

**Notes:** Finding 1 (DS-17's index absent on staging) needs a read of production's `pg_indexes`: Human-Delegation to the Data Model & Domain Schema Owner (RISK-01). Raise at sprint start. Findings 2–5 proceed autonomously. Any genuine gap is filed as a **new** backlog item (`BLG-SPEC-150`/`151` precedent); no existing item is edited.

**Staging-only ACs:** AC 1, finding 1 only (production `pg_indexes` read).

**Status at sprint open: ready**

---

#### ST-35 — Name the Gap Risk Badge's real data source in positions.md

**Owner:** Head of Specs Team; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None

**Notes:** `positions.md` v2.16 §Gap Risk Badge already names `GET /positions/{position_id}/gap-risk` (design gate). The story confirms that no other reference claims a `gap_risk` field on `GET /positions` and makes its own version bump. Owner corrected from the backlog's non-canonical "Frontend Specification Owner".

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-36 — Replace positions.stop_price with current_stop in the action-rate spec and docstring

**Owner:** Metrics Definitions & Analytics Owner; Data Model & Domain Schema Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-37 — Refresh the Gap Risk Flag §13 decision record to match strategy_rules.md v1.14

**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** None (before ST-14's addendum, EPIC-02)

**Notes:** Refreshes the body of the Gap Risk Flag §13 record. ST-14's dated addendum is appended to the same file later. If EPIC-02 merges first, ST-37 keeps that addendum intact on rebase.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-38 — Settle positions.entry_price's currency in the specs

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** ST-34 (same `data_model.md`)

**Notes:** The Data Model & Domain Schema Owner signs off the doc-fix vs code-fix decision. A code fix must not change displayed values without a design pass. The read-only live US-row sample is supporting evidence: the sandbox `DATABASE_URL` is staging and needs the user's permission before any query, and a production sample is Human-Delegation (RISK-01). A code fix is the pessimistic case (LP-14 note).

**Staging-only ACs:** AC 1, supporting evidence only (read-only live US-row `entry_price` sample). The AC itself is met from code and specs.

**Status at sprint open: ready**

---

### EPIC-02 — Stop, Sizing & Position Correctness (build-and-ship)

**Maps to:** S2-07 – S2-16
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Estimated effort:** 5.55 days
**Risk IDs:** RISK-02, RISK-04, RISK-05
**Execution sequence:** 4

#### ST-07 — Give zero-ATR signals no allocation in batch sizing

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None (first in EPIC-02)

**Notes:** Design Pre-Approved (`signals.md` v0.4 locked). The new `reason` field is API-only this release.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-08 — Include entry fees in batch signal total cost

**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-07 (same function)

**Notes:** Design Pre-Approved (`signals.md` v0.4 locked).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-09 — Assert the §4.1.5 FX defaulting/echo and §4.1.6 insufficient-cash sizing results in CI

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** ST-07, ST-08 (same service module)

**Notes:** Tests and traceability matrix only.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-10 — Make the Trail Stop action work against a real route, or remove it; stop ignoring a supplied entry stop

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** 0.75
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** Strategy Rules & System Intent Owner ruling under `strategy_rules.md` §7.3 (first sub-step)

**Notes:** RISK-02. Raise the ruling at sprint start. Addendum: the "Lower stop to {value}" label is removed under either ruling, and a no-raise note shows instead. Branch A adds `PATCH /positions/{id}/stop` with the full registration chain (RISK-04). Branch B makes the modal read-only and renames the button "View Trail". Delete the branch not taken from `positions.md` §Trail Stop Action in the same commit as the code. AC 3: the design recommends rejecting a supplied entry `stop_price` with a 400. Design gate Playwright beyond the slice AC: the no-raise note when `trail_difference ≤ 0`; add it or file a backlog item before the PR opens. Effort: 0.5–1d midpoint 0.75; Branch A is the pessimistic case (LP-14 note in `sprint_planning_notes.md`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-11 — Never let 2-dp rounding lower a stored stop

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None (before ST-12: same two recompute paths)

**Notes:** None.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-12 — Recompute US positions with a NULL fill_price without error, and add US parity cases

**Owner:** Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** ST-11 (same recompute paths)

**Notes:** None.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-13 — Decide Risk page LOSING/PROFITABLE on native P&L, matching the lifecycle badge

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Design Pre-Approved (`risk_dashboard.md` v0.1.13 §6 locked). Changes which existing status a US row shows; unit test covers it.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-14 — Use the US exchange calendar for the gap-risk "next trading session"

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** ST-37 (EPIC-05) for the §13 record body; the addendum is appended after ST-37's refresh

**Notes:** RISK-02. The slice AC says this story changes §13.3's "next trading session" limb, so a dated addendum by the Strategy Rules & System Intent Owner in `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` is expected. It answers §13.3 and §13.5. Raise at sprint start. The calendar must be deterministic, with no network call at request time.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-15 — Show the user when a position's stop is frozen for lack of ATR

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** ST-10 (both touch the Positions stop area)

**Notes:** BLG-GOV-72 fast-path (c): locked spec `positions.md` v2.16 §Frozen Stop Indicator, with Playwright in the decision record. Adds `stop_frozen_reason` to `GET /positions` in `position_endpoints.md` and `openapi.yaml` in the same commit. Design gate Playwright beyond the slice AC: no indicator during grace; add it or file a backlog item before the PR opens.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-16 — Keep first-time Settings saves from writing NULL strategy columns; snapshot §11 values on trade plans

**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None (before ST-26, EPIC-04: same `create_settings` path, RISK-05)

**Notes:** None.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-03 — Trade Entry, Settings & Accessibility (build-and-ship)

**Maps to:** S2-17 – S2-24
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 7.05 days
**Risk IDs:** RISK-03 (resolved), RISK-04, RISK-05, RISK-06
**Execution sequence:** 5

#### ST-17 — Add an ATR preview endpoint so Trade Entry shows the stop, risk and size before save

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None (first in EPIC-03)

**Notes:** BLG-GOV-72 fast-path (c): locked spec `components/position_form.md` v1.9. New route `GET /market/atr/{ticker}` with the full registration chain in one commit: `##` contract heading, `openapi.yaml`, `routers/test.py`, `SystemStatus.js` fallback count and `SC-SS-01b` (RISK-04). Reuses Trade Entry's 300 ms debounce. The fetched ATR is shown as a "Fetched:" hint and never placed in the input, so `atr_source` stays `system`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-18 — Show the currency unit on Trade Entry's ATR field and reject implausible typed ATRs

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** ST-17 (same page)

**Notes:** Locked spec `components/position_form.md` v1.9 §ATR, §Validation Errors. Disabling submit for an implausible typed ATR is the only blocking validation on Trade Entry.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-19 — Cover the §4.1.7 sizing-widget behaviours with Playwright

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** ST-17, ST-18 (tests the changed page)

**Notes:** Mocked `POST /portfolio/size`; matrix rows updated.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-20 — Correct the Settings helper text for the fixed strategy parameters

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None (before ST-21)

**Notes:** Wording only (FI-P3-02). New text is in `settings.md` v1.9 §1. Playwright text assertions per AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-21 — Strategy-copy conformance: a frontend constants module, a CI lint for UI text restating §5–§11, and a named owner

**Owner:** Head of Specs Team; Frontend Specifications & UX Documentation Owner; Director of HR
**Estimated effort:** 1.25
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** ST-20, ST-18 (before ST-26, EPIC-04)

**Notes:** Director of HR authority over the charter change in `claude/agents/frontend_specs_ux_documentation_owner.md` (RISK-06). Raise at sprint start. **AC interpretation (Head of Specs Team, 2026-10-13):** create `src/constants/strategy.js` and move the existing display mirror `src/lib/strategyParameters.js` into it. Repoint every importer and `tests/test_strategy_parameter_parity.py`, so one source remains. Do not leave both modules. No visible change is intended. Any difference the lint surfaces must match the locked specs (`settings.md` v1.9, `positions.md` v2.16, `components/position_form.md` v1.9, `trade_plan.md` v1.18 §5a).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-22 — Link each Grace Period row to its position, and align the panel's text and date format with the spec

**Owner:** Head of UX & Design; Product Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None

**Notes:** Addendum: the Product Owner keeps the spec's wording, so AC 2 aligns the shipped text to `risk_dashboard.md` §5.2. AC 1 is met by the new `?position={id}` deep link (`positions.md` v2.16 §Position Deep Link: scroll into view, 2000 ms highlight, parameter stripped), implemented in `Positions.js`. Design gate Playwright beyond the slice AC: `data-highlighted` on the target row; add it or file a backlog item before the PR opens.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-23 — Make the Reports and Notifications pages pass WCAG colour contrast in the light theme

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None

**Notes:** RISK-03 resolved at the design gate: light mode is supported, so AC 1 applies and AC 2 does not (addendum). Tokens come from the decision record's §3 table, added to `docs/specs/frontend/design_system.md`. Correct the stale "dark-only" statement in `docs/frontend/design_system.md` §6. Remove the four `:light` `color-contrast` entries from `KNOWN_VIOLATIONS` in the same commit. Replay's light-theme baseline stays with its own item.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-24 — Move white-on-amber-600 badges to a passing contrast outside Replay

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24` (read with `stage4_backlog_slice_addendum.md`)

**Dependencies:** None

**Notes:** Addendum: also move the three sites the literal grep misses to amber-700. They are `TradePlans.js` `research_pending`, the `TradePlan.js` "Abandon Plan" button (`bg-amber-700 hover:bg-amber-800`), and the Gap Risk badge's `#D97706` → `#B45309` in `Positions.js` and `PositionCard.js`. Update `tests/e2e/strategy-benchmark.spec.js` (asserts `bg-amber-600`) in the same commit.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-04 — Security, Operations & Platform

**Maps to:** S2-25 – S2-32
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead; FinOps & Resource Architect
**Estimated effort:** 5.05 days
**Risk IDs:** RISK-01, RISK-05
**Execution sequence:** 6

#### ST-25 — Stop the post-grace stop-health monitor alerting on the morning a position's grace ends

**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None (first in EPIC-04)

**Notes:** Defaults to option (a), which needs no ruling. If option (b) is chosen, it changes live stop behaviour: stop, record a Strategy Rules & System Intent Owner ruling first, and reclassify the story as `delegated_decision` in `execution_state.json`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-26 — Audit trail for strategy-parameter changes in Settings

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** ST-16 (EPIC-02), ST-20 and ST-21 (EPIC-03); cross-EPIC, RISK-05

**Notes:** Adds `last_change` to `GET /settings` (`settings_endpoints.md`, `openapi.yaml`), with the last-change line from `settings.md` v1.9. Code, tests and `data_model.md` proceed autonomously. The live migration on staging and production is Human-Delegation to the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner (RISK-01). Raise at sprint start.

**Staging-only ACs:** AC 3, live-application half only (migration applied on staging and production, with verification output).

**Status at sprint open: ready**

---

#### ST-27 — Re-assess the bundled `REACT_APP_API_KEY` against its actual write scope

**Owner:** Cybersecurity & Trust Lead; Product Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** Decision: a narrower frontend key, or an explicit Product Owner accept-risk recorded in `credential_policy.md`. Raise at sprint start. A narrower key is the pessimistic case (LP-14 note).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-28 — Apply the in-range dependency patch/minor bumps from the October 2026 quarterly review

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** 0.75
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** Late in the sprint, after the other EPIC-03/EPIC-04 frontend changes, so one full CI run covers the final tree

**Notes:** One PR for all 8 backend and 20 frontend bumps (`docs/security/dependency_update_review_2026-10-06.md` §3–§5). If the governed environment cannot run the staging check, it is Human-Delegation to the Infrastructure & Operations Owner.

**Staging-only ACs:** AC 2 (staging check of yfinance price and ATR fetches for one US and one UK ticker on the bumped build).

**Status at sprint open: ready**

---

#### ST-29 — Find out why a staging-deploy.yml hook deploy of a governance-only commit never went live

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None (before ST-30)

**Notes:** Needs Render dashboard access: Human-Delegation to the Infrastructure & Operations Owner (RISK-01). Check the staging service's Settings → Build Filters as well as the deploy's final state, because dashboard-only Build Filters are invisible to the repo. AC 1's "recorded against this item" means a `Notes` line on `BLG-OPS-181` in `claude/backlog/backlog.md` (named-file write).

**Staging-only ACs:** AC 1 (the cause is read from the Render dashboard). AC 2 is a doc change and is not staging-only.

**Status at sprint open: ready**

---

#### ST-30 — Live-fire the stale-staging check from main against a deliberate divergence

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** ST-29 (both concern staging deploys)

**Notes:** Needs control of staging deploys and a real Telegram receipt: Human-Delegation to the Infrastructure & Operations Owner (RISK-01). Run the workflow-viability pre-check (`execution_prompt.md` §3.1.B step 2a) before requesting the live fire.

**Staging-only ACs:** AC 1 (failing `main` run URL with `STALE STAGING DEPLOY` and the Telegram alert received). AC 2 (passing `main` run URL after restore).

**Status at sprint open: ready**

---

#### ST-31 — Add requirements-dev.txt to the local backend setup instructions

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None

**Notes:** The AC needs no CLAUDE.md edit. Mentioning `requirements-dev.txt` in CLAUDE.md §9 is optional and needs Head of Specs Team agreement if done.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-32 — Inventory the scheduled GitHub workflows: owner, cron, tables written, monthly minutes

**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days (top edge 28.00) |
| Total estimated effort (in-scope) | 27.95 days (48 stories) |
| Utilisation | 99.8% (above the §1.5 95% buffer floor; Product Owner: proceed at ceiling, 2026-10-13) |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | None. All 48 slice items are in scope. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-03 light-mode decision (ST-23) | Head of UX & Design; Product Owner | No. Done 2026-10-12 (supported) |
| ST-21 constants-module interpretation | Head of Specs Team | No. Done 2026-10-13 (move into `src/constants/strategy.js`) |
| ST-10 §7.3 ruling and ST-14 §13 addendum, raised at sprint start | Strategy Rules & System Intent Owner | No |
| ST-04 failure-action sign-off | AI Compliance & Governance Officer | No |
| ST-21 charter-change authority | Director of HR | No |
| ST-27 key decision | Cybersecurity & Trust Lead; Product Owner | No |
| ST-38 doc fix vs code fix sign-off | Data Model & Domain Schema Owner | No |
| ST-43 ruling | Head of Specs Team; Product Owner | No |
| Human-Delegation: ST-01 and ST-26 live migrations; ST-28 staging check; ST-29 Render dashboard; ST-30 live fire; ST-34 production read; ST-38 live sample | Infrastructure & Operations Owner; Data Model & Domain Schema Owner | No |
| Playwright for the ST-10 no-raise note, ST-15 no-indicator-in-grace and ST-22 `data-highlighted`, or backlog items filed before the PR opens | QA & Testing Owner | No |
| Backlog item for the design gate observation (`strategy_benchmark.md` §7 badge style; `bg-teal-600 text-white` about 3.7:1), filed at execution | Frontend Specifications & UX Documentation Owner | No |
| v9.11 closure action #8(b) (`release_planning_prompt.md` §1.3a bound 5), overdue; a separate change, not bundled into ST-40 | Head of Specs Team | No |

---

## Product Owner Sign-Off

Sprint goal: Confirmed (as drafted), 2026-10-13
Buffer floor (99.8%): Proceed at ceiling, 2026-10-13
Sprint split (RISK-08): Single sprint, 2026-10-13
Deferred execution blockers accepted: N/A (none)
RISK-03 pre-sprint decision: Light mode supported, ruled by the Head of UX & Design with the Product Owner, 2026-10-12 (design gate)

### Named-file writes

- Named-file write: `claude/roadmap/role_share_history.md` (split-credit column; ST-44) — authorised under execution_prompt.md §7 named-file rule. This is a `claude/roadmap/*` write, listed for information; it needs no separate confirmation.
- Named-file write: `claude/backlog/backlog.md` `BLG-OPS-181` `Notes` line (ST-29) — authorised under execution_prompt.md §7 named-file rule. This is a `Notes` edit, listed for information; it needs no separate confirmation.
- No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

Sprint backlog: Confirmed, 2026-10-13
Signed off by: Product Owner
