**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-10-16
**Cycle:** 2026-10-16__release-v9.13
**Release:** v9.13
**Sprint Goal:** Make the Daily Position Monitor's exit confirmation record real exits through `POST /positions/{id}/exit` (BLG-FE-226, P1), give exit reasons one allowed list mapped to §8, and make CI fail on any frontend call to a route that does not exist. Also ship v9.13's stop and sizing correctness, AI output safety, operations and governance items.
**Backlog Slice Source:** Original: `claude/cycles/2026-10-16__release-v9.13/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-03, ST-21 and ST-25)

# Sprint Backlog — 2026-10-16__release-v9.13

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-06 → EPIC-02 → EPIC-03 → EPIC-05 → EPIC-04.
- **EPIC-01** goes first. It carries the P1 anchor (ST-01), and ST-23/ST-24 need ST-01 on `main`.
- **EPIC-06** goes second. It is small and mostly autonomous, and it takes the certain `strategy_rules.md` bump (ST-38 + ST-39) early.
- **EPIC-02** and then **EPIC-03** follow. EPIC-02 owns the route-registration chain, and EPIC-03's ST-22 recomputes the endpoint count from the merged `test.py`.
- **EPIC-05** goes fifth because its delegations run longest.
- **EPIC-04** goes last. ST-24's suite-wide 404/405 fixture and ST-23's static check then run over the final tree, and ST-25's `cn()` change lands after every other EPIC's buttons (RISK-05).

**Fallback:** if EPIC-05 is still waiting on delegations, EPIC-04 may merge before it. EPIC-05 then rebases and must pass ST-23's check and ST-24's fixture.

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch checks whether the file exists before creating its own. If it exists, the branch appends its own section and never overwrites.

**Shared files across EPICs:**
- **`claude/strategy/strategy_rules.md`** (EPIC-06 ST-38/39; EPIC-01 ST-05 and EPIC-02 ST-06/07, ruling-dependent): EPIC-06 owns it. Writes are authorised for these five stories only (RISK-02 option (a)). Bumps go in merge order, and the later branch takes the next free version (CLAUDE.md §8 step 2a).
- **`openapi.yaml`** (EPIC-02 ST-08, ST-10 if a route is added; EPIC-03 ST-22; EPIC-05 ST-28; EPIC-04 ST-23 reads it): EPIC-02 owns it. Take the union of additions and the highest version.
- **Route-registration chain** (`routers/test.py`, `SystemStatus.js` fallback count, `SC-SS-01b`; EPIC-03 ST-22, EPIC-02 ST-10 if a route is added): EPIC-02 owns it. EPIC-03 recomputes the count from the merged `test.py`.
- **`data_model.md`** (EPIC-01 ST-02; EPIC-03 ST-22): EPIC-01 owns it. Keep migration blocks in ascending order.
- **`metrics_definitions.md`** (EPIC-01 ST-02; EPIC-02 ST-10, ST-11; EPIC-03 ST-22): EPIC-01 owns it. Run CLAUDE.md §8 step 2a's version check on this file.
- **`ai_endpoints.md`** (EPIC-03 ST-18, ST-19, ST-22; EPIC-05 ST-28): EPIC-03 owns it.
- **`cn()` / `Button` and `KNOWN_VIOLATIONS`** (EPIC-04 ST-25, ST-26; EPIC-03 ST-21; any new coloured button in EPIC-01/03): EPIC-04 owns `cn()`. EPIC-03 owns `KNOWN_VIOLATIONS` until EPIC-04 merges.
- **`base44Client.js`** (EPIC-01 ST-01 removes `Position.update`; EPIC-04 ST-23 allow-lists dead methods): EPIC-01 owns it.
- **`claude/backlog/backlog.md`:** new items only, via `/backlog-add` (ST-24, ST-34 and Playwright-gap items). No existing item is edited. Run `scripts/check_backlog_item_integrity.py` after each §8 merge.
- **`claude/roadmap/role_share_history.md`:** EPIC-06 ST-40 only (named-file write).

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — Exit Flow, Exit Reasons & Red Flag Journal (build-and-ship)

**Maps to:** S2-01 – S2-05
**Owner:** Head of Engineering; Head of UX & Design; Strategy Rules & System Intent Owner; Data Model & Domain Schema Owner
**Estimated effort:** 5.50 days
**Risk IDs:** RISK-01, RISK-02, RISK-04
**Execution sequence:** 1

#### ST-01 — Make the Daily Position Monitor's exit confirmation open the real exit flow

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first in EPIC-01; ST-03, ST-23 and ST-24 follow it)

**Notes:** P1, the release anchor (roadmap-committed, DL-086). BLG-GOV-72 fast-path (c): locked spec `positions.md` v2.20 §Daily Position Monitor Exit Queue and `monitor-exit-queue/decision_record.md`, with both Playwright tests in the AC. Removing `Position.update` from `base44Client.js` is what lets ST-23's check pass on `main`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-02 — Define the allowed exit reasons and map each to one of §8's three exit conditions

**Owner:** Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner
**Estimated effort:** 1.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (ST-03 follows it)

**Notes:** Spec, `data_model.md` and `metrics_definitions.md` edits proceed autonomously. The legacy-spelling backfill and the CHECK constraint on staging and production are Human-Delegation to the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner (RISK-01, DS-23 pattern). Raise at sprint start.

**Staging-only ACs:** AC 2, live half only (pre-check counts, backfill and constraint applied on staging and production, with the DS-xx Live Confirmation recorded)

**Status at sprint open: ready**

---

#### ST-03 — One shared exit-reason module so Trade Reflections badges and labels match stored values

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-02 (§8 category per reason); ST-01 (ExitModal edits)

**Notes:** Read with the addendum: AC 3 covers eight files, adding `ExportModal.js`, `TradeBreakdown.js` and `MonthlyHeatmap.js`, and `src/lib/exitCondition.js` re-exports from the module. Sprint Planning checked the estimate: the three extra files are import swaps and stay within the S range (0.5–1d), so 0.75d holds (Product Owner, 2026-10-16). Labels and tokens are fixed by `exit-reason-badges/decision_record.md`; colour tests cover both themes.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-04 — Record checklist_skipped events and stop offering journal filters that can never match

**Owner:** Backend Engineering Patterns Owner; Head of UX & Design
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Locked spec `red_flag_journal.md` v1.4 and `red-flag-journal-recorded-types/decision_record.md`. The writer-coverage test's allow-list entries for the two prompt types are dated.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-05 — Strategy determination on month-end rebalance exits, which are live but not in strategy_rules.md

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.75
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** Strategy Rules & System Intent Owner determination (first sub-step)

**Notes:** Raise the determination at sprint start. The interim "outside §8 — informational" label (Playwright) proceeds regardless. Both outcomes are designed (`rebalance-exit-interim-label/decision_record.md`); delete the unused branch at implementation. **RISK-02 write authorisation:** the user and the Strategy Rules & System Intent Owner authorised named `claude/strategy/strategy_rules.md` writes for ST-05, ST-06, ST-07, ST-38 and ST-39 only, at sprint planning on 2026-10-16 (option (a)). The commit message must cite this line. Version bumps are taken in merge order; a later-merging branch rebases and takes the next free version (CLAUDE.md §8 step 2a).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-02 — Stop, Sizing & Position Data Correctness

**Maps to:** S2-06 – S2-14
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; Metrics Definitions & Analytics Owner
**Estimated effort:** 2.75 days
**Risk IDs:** RISK-02, RISK-03, RISK-04
**Execution sequence:** 3

#### ST-06 — Reject a fetched ATR that puts the initial stop at or below zero

**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** Strategy Rules & System Intent Owner ruling: reject with 400 or floor (first sub-step)

**Notes:** Raise the ruling at sprint start. Both branches are designed (`initial-stop-at-or-below-zero/decision_record.md`, `components/position_form.md` v1.10). A `strategy_rules.md` §5 edit is needed only if the ruling changes stop behaviour. **RISK-02 write authorisation:** the user and the Strategy Rules & System Intent Owner authorised named `claude/strategy/strategy_rules.md` writes for ST-05, ST-06, ST-07, ST-38 and ST-39 only, at sprint planning on 2026-10-16 (option (a)). The commit message must cite this line. Version bumps are taken in merge order; a later-merging branch rebases and takes the next free version (CLAUDE.md §8 step 2a).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-07 — Align the standalone position_manager.py with §6.3 (no stop ratchet during grace)

**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** Strategy Rules & System Intent Owner choice: align the code or record an exception (first sub-step)

**Notes:** The default (align the code, with a unit test) needs no strategy change (RISK-03). The `strategy_rules.md` exception branch is covered by the RISK-02 authorisation. **RISK-02 write authorisation:** the user and the Strategy Rules & System Intent Owner authorised named `claude/strategy/strategy_rules.md` writes for ST-05, ST-06, ST-07, ST-38 and ST-39 only, at sprint planning on 2026-10-16 (option (a)). The commit message must cite this line. Version bumps are taken in merge order; a later-merging branch rebases and takes the next free version (CLAUDE.md §8 step 2a).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-08 — Reject or flag the four fixed strategy-parameter fields on Settings writes

**Owner:** API Contracts & Documentation Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** API Contracts & Documentation Owner choice: 400 or deprecation warning (first sub-step)

**Notes:** The default is a 400 naming the §11 rule (RISK-03). `settings_endpoints.md` and `openapi.yaml` change in the same commit (RISK-04). If the Settings page sends these fields, stop it sending them in this story; that is a defect, not a design change (design gate).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-09 — Keep the Monthly P&L report up when the snapshot store fails

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Design Pre-Approved against `reports.md` v0.24 §Monthly Restatement Marker, Failure.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-10 — Define a stop-freshness metric and show it on System Status

**Owner:** Metrics Definitions & Analytics Owner; Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Locked spec `system_status.md` v1.3 §Stop Freshness Panel and `stop-freshness-status/decision_record.md`. If a new endpoint is added, the full registration chain applies in the same commit: contract, `openapi.yaml`, `routers/test.py`, `SystemStatus.js` fallback count and `SC-SS-01b` (RISK-04).

**Staging-only ACs:** AC 2, manual-check half only (the displayed value checked by hand against a deployed environment's open positions, recorded). The live DB needs the user's permission before any query.

**Status at sprint open: ready**

---

#### ST-11 — Correct metrics_definitions.md's claim about NULL positions.fees_paid

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Spec text only.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-12 — Mock get_settings() so the stored ATR multiplier is asserted exactly

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Test only.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-13 — Test the entry required-field set and the non-blocking advisory panel at their boundary

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Design Pre-Approved; locked references `trade_plan.md` v1.19 and `components/position_form.md` v1.10.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-14 — Give the valid-input sizing property a lower bound

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Test only.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-03 — AI Output Safety, Debrief & Chat

**Maps to:** S2-15 – S2-22
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 3.10 days
**Risk IDs:** RISK-01, RISK-03, RISK-04
**Execution sequence:** 4

#### ST-15 — Treat UK .L and bare tickers as the same instrument in the briefing ticker filter

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (first in EPIC-03)

**Notes:** Its normalisation is reused by ST-16 and ST-17.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-16 — Attribute chat stop citations to the focused ticker and case-normalise action tickers

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** ST-15; AI Compliance & Governance Officer sign-off (first sub-step)

**Notes:** Raise the sign-off at sprint start. AC 4 records the Head of UX & Design's answer on visible "system-added" styling; any styling change is filed separately (design gate).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-17 — Check the briefing summary text for tickers outside the context

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** ST-15; AI Compliance & Governance Officer sign-off on the action (first sub-step)

**Notes:** Raise the sign-off at sprint start.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-18 — Add an output-language check to the journal summary

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** AI Compliance & Governance Officer sign-off on the failure action (first sub-step)

**Notes:** Raise the sign-off at sprint start. Bump `JOURNAL_SUMMARY_PROMPT_VERSION` if the prompt text changes.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-19 — Label available cash and starting capital separately in the AI chat context

**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Prompt-context wording; record any prompt-version bump in the golden fixtures.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-20 — Keep the debrief card populated when Regenerate returns no data

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None (ST-21 follows it in the same file)

**Notes:** Design Pre-Approved against `trade_history.md` v1.16 §Post-Trade Debrief.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-21 — Give the debrief error text a light-theme colour that passes contrast

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** ST-20 (same file)

**Notes:** Read with the addendum: the light-theme fix covers the whole debrief section (card `bg-white`, heading, badge, muted text) and the error text uses `text-rose-700 dark:text-rose-400`, per `trade_history.md` v1.16 §Post-Trade Debrief §Light Theme. Sprint Planning checked the estimate: the tokens are fixed by the gate and the change is in one file, so the XS figure holds (Product Owner, 2026-10-16). Remove any matching `KNOWN_VIOLATIONS` entry in the same commit.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-22 — Add a useful / not-useful rating to each AI chat answer

**Owner:** Head of Engineering; Data Model & Domain Schema Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Locked spec `positions.md` v2.20 §AI Trade Advisor Widget §Answer Rating and `chat-answer-rating/decision_record.md`. The new route takes the full registration chain in one commit (contract, `openapi.yaml`, `routers/test.py`, `SystemStatus.js` fallback count, `SC-SS-01b`; RISK-04). The migration on staging and production is Human-Delegation to the Data Model & Domain Schema Owner (RISK-01). Raise at sprint start.

**Staging-only ACs:** AC 2, live half only (DS entry's Live Confirmation on staging and production)

**Status at sprint open: ready**

---

### EPIC-04 — API Call Integrity & UI Rendering

**Maps to:** S2-23 – S2-27
**Owner:** Director of Quality; API Contracts & Documentation Owner; Head of Engineering
**Estimated effort:** 6.25 days
**Risk IDs:** RISK-03, RISK-04, RISK-05
**Execution sequence:** 6

#### ST-23 — CI check that every frontend API call exists in openapi.yaml

**Owner:** Director of Quality; API Contracts & Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** ST-01 (EPIC-01) on `main`

**Notes:** Dead Base44 methods that `BLG-FE-230` will remove go on a dated allow-list naming `BLG-FE-230` (restated AC).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-24 — Fail Playwright on any 404/405 from the app's API and sweep state-changing actions

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 3.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** ST-01 (EPIC-01) on `main`; ST-23

**Notes:** Largest story (RISK-05). Kept as one story; the Product Owner did not split it into fixture and sweep (2026-10-16). Defects the fixture exposes are filed via `/backlog-add`, not fixed here. Uncovered actions get a dated backlog item.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-25 — Make coloured Buttons render their colour (fix cn() at the root)

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** Read with the addendum: the Screener (~329, ~1065) and Cash Management deposit fills become `bg-emerald-700 hover:bg-emerald-800 text-white`, and AC 2 asserts `rgb(4, 120, 87)` for them. Rose-600 hovers move to rose-700. `text-white` is added where a button inherits `text-primary-foreground`. "Abandon Plan" drops the `!` prefixes. Decision record: `coloured-button-fills/decision_record.md`. The `design_system.md` rule is added in-story.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-26 — Fix the Replay page's light-theme colour contrast

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** Applies the v9.12 light-theme token rule; spec `replay_mode.md` v0.4 §Light Theme. Remove the three `Replay*:light` entries from `KNOWN_VIOLATIONS` in the same commit.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-27 — Decide how real-database-bound modules may persist across pytest files

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** Director of Quality review of the test-isolation decision (first sub-step)

**Notes:** Run pytest with a stub `DATABASE_URL`, never the live one.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-05 — Operations, Cost & Platform

**Maps to:** S2-28 – S2-34
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Head of Engineering
**Estimated effort:** 8.50 days
**Risk IDs:** RISK-01, RISK-04
**Execution sequence:** 5

#### ST-28 — Make the daily AI cost alert fail loudly on query or workflow failure

**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** A response-shape change to `POST /ai/check-daily-cost` updates `ai_endpoints.md` and `openapi.yaml` in the same commit. The real failed-run Telegram receipt is Human-Delegation to the Infrastructure & Operations Owner (RISK-01).

**Staging-only ACs:** AC 2 (a failed `ai-daily-cost-check.yml` run sends a Telegram notification; real receipt)

**Status at sprint open: ready**

---

#### ST-29 — Deploy both staging services from staging-deploy.yml and wait on each

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** Copying the two deploy hooks from the Render dashboard and setting the GitHub secrets is Human-Delegation to the Infrastructure & Operations Owner (RISK-01). Raise at sprint start: other stories' staging checks depend on staging deploys working. Check Render Build Filters if a deploy skips a change.

**Staging-only ACs:** AC 1, live half only (the two secrets set from the Render dashboard). AC 2 (a live `staging-deploy.yml` run on `main` with both services on the run's commit). AC 4 (smoke test confirms the host behind `STAGING_API_URL`)

**Status at sprint open: ready**

---

#### ST-30 — Produce the combined data-pipeline cost baseline

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** None (ST-31 follows it)

**Notes:** Live usage figures may need read access via Human-Delegation (RISK-01). The gate condition (`BLG-OPS-17` shipped v9.3) was verified at Release Planning.

**Staging-only ACs:** AC 1 (the weekly baseline uses live usage figures)

**Status at sprint open: ready**

---

#### ST-31 — Attribute each external API call to the feature that triggered it

**Owner:** FinOps & Resource Architect; Head of Engineering
**Estimated effort:** 2.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** ST-30

**Notes:** The tagging and its tests proceed autonomously. Naming the top 3 contributors needs live usage data (RISK-01).

**Staging-only ACs:** AC 2 (the attribution report run on live data names the top 3 contributors)

**Status at sprint open: ready**

---

#### ST-32 — Benchmark the full screener run

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** Runs against a deployed environment's full ticker universe (500+ tickers); Human-Delegation if the run cannot be triggered (RISK-01).

**Staging-only ACs:** AC 1 (p50/p95 from a full-universe run on a deployed environment)

**Status at sprint open: ready**

---

#### ST-33 — Assess data-provider risk and failover options

**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** Infrastructure & Operations Owner and FinOps & Resource Architect sign-off on the accepted-risk statement

**Notes:** Documentation; the sign-off is the closing sub-step.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-34 — Assess the major and breaking dependency upgrades from the October 2026 review

**Owner:** Head of Engineering
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None

**Notes:** Assessment only. Approved upgrades are filed via `/backlog-add` as separate items. tailwindcss 4 stays with `BLG-TECH-21`. A framer-motion or lucide-react upgrade that changes motion or icons needs its own design pass (design gate).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-06 — Governance & Spec Tooling

**Maps to:** S2-35 – S2-40
**Owner:** Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner; Data Model & Domain Schema Owner
**Estimated effort:** 1.90 days
**Risk IDs:** RISK-02, RISK-04
**Execution sequence:** 2

#### ST-35 — Treat Gate criteria: None/N/A as ungated in the gate scan

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None (first in EPIC-06; ST-36 follows it)

**Notes:** Run tests via `backend/.venv/bin/python3 -m pytest`. The PR description records the ready-pool view of the 17 items; `backlog.md` is not edited.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-36 — Known-false-positive allow-list for the gate scan

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** ST-35 (same script)

**Notes:** Tested with a fixture (restated AC).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-37 — Compare documented column defaults in check_data_model_drift.py

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** None

**Notes:** The tool stays read-only. Tests use fixtures; do not query the live DB without the user's permission.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-38 — Update strategy_rules.md §13.3 now the Gap Risk Flag's weekend-hold trigger is gone

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** None (ST-39 follows it)

**Notes:** Documentation-only edit to text already reviewed. Shares one version bump with ST-39. **RISK-02 write authorisation:** the user and the Strategy Rules & System Intent Owner authorised named `claude/strategy/strategy_rules.md` writes for ST-05, ST-06, ST-07, ST-38 and ST-39 only, at sprint planning on 2026-10-16 (option (a)). The commit message must cite this line. Version bumps are taken in merge order; a later-merging branch rebases and takes the next free version (CLAUDE.md §8 step 2a).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-39 — Correct strategy_rules.md §13.5's PO-05 roster row

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** ST-38 (shared version bump)

**Notes:** Wording per the source item's Scope. **RISK-02 write authorisation:** the user and the Strategy Rules & System Intent Owner authorised named `claude/strategy/strategy_rules.md` writes for ST-05, ST-06, ST-07, ST-38 and ST-39 only, at sprint planning on 2026-10-16 (option (a)). The commit message must cite this line. Version bumps are taken in merge order; a later-merging branch rebases and takes the next free version (CLAUDE.md §8 step 2a).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-40 — Correct the v9.8–v9.10 compound Owner count in role_share_history.md

**Owner:** PMO Lead
**Estimated effort:** 0.15
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`

**Dependencies:** None

**Notes:** Named-file write: `claude/roadmap/role_share_history.md`, v9.8–v9.10 rolling line, compound count to 17 of 21, matching `scripts/compute_role_share_history.py` (authorised under `execution_prompt.md` §7 named-file rule). Kept `delegated_decision` as the slice states (`ESC-CLOSE-20261006-01`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units (28.00 ceiling) |
| Total estimated effort (in-scope) | 28.00 days |
| Utilisation | 100% of the band ceiling (above the 95% advisory buffer floor; Product Owner: proceed at ceiling, 2026-10-16) |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | None. All 40 slice items are in sprint scope. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-02: write route for `strategy_rules.md` | Strategy Rules & System Intent Owner; Product Owner | No. **Resolved 2026-10-16: option (a), named writes authorised for ST-05, ST-06, ST-07, ST-38 and ST-39** |
| Rulings and sign-offs raised at sprint start: ST-05, ST-06, ST-07 (Strategy Rules & System Intent Owner); ST-08 (API Contracts & Documentation Owner); ST-16, ST-17, ST-18 (AI Compliance & Governance Officer); ST-27 (Director of Quality); ST-33 (Infrastructure & Operations Owner; FinOps & Resource Architect) | As listed | No |
| Human-Delegation raised at sprint start: ST-02 and ST-22 live changes; ST-28 Telegram receipt; ST-29 Render dashboard and live run; ST-30/ST-31 live usage data; ST-32 full-universe run; ST-10 manual check against a deployed environment | Infrastructure & Operations Owner; Data Model & Domain Schema Owner | No |
| For any staging-only AC whose sign-off is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (as drafted), 2026-10-16
**Scope confirmed:** Confirmed: 40 stories across 6 EPICs, single sprint, ST-24 not split, 2026-10-16
**Capacity confirmed:** Confirmed: 28.00 / 28.00 (100%), proceed at ceiling above the 95% buffer floor; ST-03 and ST-21 estimates held after the addendum check, 2026-10-16
**Deferred execution blockers accepted (if any):** N/A (none)
**Pre-sprint decision RISK-02:** Option (a), named `strategy_rules.md` writes authorised for ST-05, ST-06, ST-07, ST-38 and ST-39, by the user with the Strategy Rules & System Intent Owner, 2026-10-16

### Named-file writes

- Named-file write: `claude/roadmap/role_share_history.md` (v9.8–v9.10 rolling line, compound count) — authorised under execution_prompt.md §7 named-file rule (ST-40). For information; no separate confirmation needed.

No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

For information, outside the named-file rule: `claude/strategy/strategy_rules.md` writes for ST-05, ST-06, ST-07 (ruling-dependent), ST-38 and ST-39, authorised under RISK-02 option (a) above.

**Signed off by:** Product Owner
