Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-11
Cycle: 2026-11-11__release-v9.17
Release: v9.17

# Backlog Slice — v9.17

<!-- release-plan-marker: RP:v9.17:2026-11-11__release-v9.17 -->

20 stories across 7 EPICs, 27.95 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-11-11).

**Ready pool:** 180 items, 90.75 days (after the STEP 4 calibration raises, applied to the whole pool before selection).

**Selection method** (`release_planning_prompt.md` §1.4c, v2.74):
0. **Programme-phase hold (step 0):** nothing held. Phase 3 is provisional for v9.17, this release. The Close-out phase (`BLG-UX-08`, v9.18) is already gated.
1. No ready P1 item. The ready P2 items in ascending ID order: `BLG-BE-211`, `BLG-FE-254` (split-achievability remainder only), `BLG-FE-260`, `BLG-FE-278`, `BLG-FE-281`, `BLG-FE-282` and `BLG-OPS-217`. `BLG-TECH-21` stays deferred (standing override).
2. Step 1a, deferred lessons-learnt patch items targeted at v9.17: `BLG-GOV-419` (`LL-v9.16-Release-03`).
3. **Step 1b, current programme phase tier (first use, v2.74):** Phase 3's P3 items `BLG-FE-257`, `258`, `259`, `261`, `262`, `263`, `265`, and `BLG-BE-205`, which the Phase 2 row names and which Phase 2 still waits on (an earlier, unfinished phase).
4. A category-balanced, oldest-first round-robin over P3/P4, run until 0.05 days were left.

**Where an item's own AC is stale, untestable, missing or points at text outside the slice, the AC below restates it.** Each change from the source backlog item is marked *(restated)* with the reason. Scope bullets are copied from the source item for convenience; the source item stays authoritative for Problem text.

**Gates cleared this run:** none. The scan listed 0 date-lapsed items, and each of the 14 gating-item-shipped items still has an unmet limb.

**`strategy_rules.md` writes (case (c), `execution_prompt.md` §7):** ST-19 may add the Exit Zone threshold to `strategy_rules.md` §11 if the Strategy Rules & System Intent Owner chooses that option. ST-12's acknowledgement approach is that owner's decision. Both are listed as pre-seal decisions (RISK-05).

**§13 clause-citation rule (v2.61):** no seated AC requires a §13 review, determination or sign-off.

**Post-merge, production and console ACs (Sprint Planning STEP 6.2):** ST-15 needs a production `api_call_log` read and, after the fix deploys, a production weekly report (7 days). ST-11's backfill and ST-09's migration run against production at deploy. Sprint Planning marks each `post-merge` with a named tracking item before the seal.

**Conditional stories (§1.4b):** none. No seated item has a calendar-date gate inside the sprint window.

---

## EPIC-01 — Site Structure & Usability Phase 3: Positions Redesign (build-and-ship)

**Maps to:** S2-01 – S2-04
**Owner:** Head of Engineering; Head of UX & Design
**Description:** Make the Positions page decision-first: an urgency-ordered table with about 6 leading columns, a card layout on narrow screens, one warning strip in place of four banners, and one grace-period view that the Dashboard and Risk Dashboard link to.
**Estimated days:** 7.50

### ST-01 — Decision-first Positions table
**Source:** BLG-FE-260
**Priority:** P2
**Effort:** M (~2-3 days)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** First in EPIC-01. ST-02 reuses its urgency order and leading fields; ST-03 and ST-04 edit the same page after it.
**UI-facing:** Yes
**Scope:**
- Sort by urgency (exit fired → stop breached → near stop → rest); lead with ticker, distance to stop (R and %), action needed; remaining columns in an expandable row; positions page spec updated
**Acceptance Criteria:**
- Default view shows about 6 columns in urgency order; expanding a row shows the rest; Playwright coverage passes

### ST-02 — Card layout for Positions on narrow screens
**Source:** BLG-FE-261
**Priority:** P3
**Effort:** M (~2 days)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** After ST-01.
**UI-facing:** Yes
**Scope:**
- A card layout below `md` with the same urgency order and leading fields as `BLG-FE-260` (ST-01)
**Acceptance Criteria:**
- At 390px width, Positions shows cards with no horizontal page scroll; Playwright coverage passes

### ST-03 — Combine the four banners above the Positions table into one strip
**Source:** BLG-FE-262
**Priority:** P3
**Effort:** S (~1 day)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** After ST-01. Before ST-04, which removes `GracePeriodAlertZone`'s detail from the strip's grace entry.
**UI-facing:** Yes
**Scope:**
- One summary strip listing the active warnings (`MetricsStalenessIndicator`, `DrawdownReviewPrompt`, `ConcentrationLimitsWarning`, `GracePeriodAlertZone`), each expandable to its current content
**Acceptance Criteria:**
- With all four conditions active, one strip shows four entries and each expands; Playwright coverage passes

### ST-04 — Show grace period in one place, linked from the others
**Source:** BLG-FE-257
**Priority:** P3
**Effort:** M (~2 days)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Sequencing:** Last in EPIC-01 (after ST-03).
**UI-facing:** Yes
**Scope:**
- One grace view on Positions; the Dashboard and Risk Dashboard show a count and link to it; short spec note in the affected page specs
**Acceptance Criteria:**
- Grace detail renders in one component on one page; the other surfaces link to it; Playwright coverage passes

---

## EPIC-02 — Site Structure & Usability Phase 3: Journal & Performance Consolidation (build-and-ship)

**Maps to:** S2-05 – S2-07
**Owner:** Head of Engineering; Head of UX & Design; Metrics Definitions & Analytics Canonical Owner
**Description:** Build the single Journal area from the v9.15 Journal spec (`BLG-SPEC-216`), merge Reports and Performance Analytics into one Performance page, and give the remaining long single-scroll pages section tabs or an index.
**Estimated days:** 9.50

### ST-05 — Build the single Journal area
**Source:** BLG-FE-258
**Priority:** P3
**Effort:** L (~3-4 days)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** Independent within EPIC-02. Its redirects and the Performance redirects (ST-06) both update `navigation.md` v2's areas and the command palette, so ST-05 and ST-06 merge one after the other (RISK-04).
**UI-facing:** Yes
**Scope:**
- Implement the Journal spec (`BLG-SPEC-216`, approved at v9.15), redirects from the old routes and the Positions journal view change
**Acceptance Criteria:**
- Every observable AC in the Journal spec has Playwright coverage that passes; old routes redirect

### ST-06 — Merge Reports and Performance Analytics into one Performance page
**Source:** BLG-FE-259
**Priority:** P3
**Effort:** L (~3-4 days)
**Owner:** Head of Engineering; Head of UX & Design; Metrics Definitions & Analytics Canonical Owner (KPI definitions)
**Sequencing:** Spec first (sub-step 1), reviewed at the design gate if drafted before it, otherwise by the Head of UX & Design before the build. After ST-05 for the shared navigation edits.
**UI-facing:** Yes
**Scope:**
- A short spec for one Performance page (sections: summary, monthly/tax-year reports, analytics, compliance), then the build with redirects; Metrics Definitions & Analytics Owner confirms each KPI keeps its canonical definition
**Acceptance Criteria:**
- One Performance page; old routes redirect; each KPI appears once; Playwright coverage passes
- The Metrics Definitions & Analytics Canonical Owner's confirmation that each KPI keeps its canonical definition is recorded with a date in the QA evidence *(restated: the source item's Scope requires the confirmation but no AC records it)*

### ST-07 — Use tabs or sections on the long single-scroll pages
**Source:** BLG-FE-263
**Priority:** P3
**Effort:** M (~2-3 days)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** Independent. Edits `TradePlan.js`, which EPIC-05's ST-12 and ST-14 also edit (RISK-01).
**UI-facing:** Yes
**Scope:**
- Section tabs or an in-page section index on Trade Plan and Strategy Benchmark, keeping the current content (Reports is handled by ST-06)
**Acceptance Criteria:**
- Each page shows its sections as tabs or an index; each section is reachable in one click; Playwright coverage passes

---

## EPIC-03 — Site Structure & Usability Phase 3: Semantic Colour Token Sweep (build-and-ship)

**Maps to:** S2-08
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Description:** Move the remaining pages onto the semantic colour tokens that v9.16 ST-09 (`BLG-FE-264`) built for the shells, so the light theme passes contrast checks on every routed page.
**Estimated days:** 3.50

### ST-08 — Move the remaining pages onto the semantic colour tokens
**Source:** BLG-FE-265
**Priority:** P3
**Effort:** L (~3-4 days)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Sequencing:** EPIC-03 merges last, after every other UI EPIC, and regenerates the visual baselines for both themes (RISK-02).
**UI-facing:** Yes
**Calibration (STEP 4, sweep):** held at L with the count named (grep, 2026-11-11): `src/pages/` has 231 `text-white` and 205 `bg-slate-800/900` in 21 files; `src/components/` has 251 and 233 in 87 files. Filing counted 376 and 331. Sprint Planning confirms the boundary (RISK-02).
**Scope:**
- Replace page-level dark-only colour classes with the tokens; remove redundant `dark:` pairs; update `design_system.md`
- On completion, `BLG-FE-224` and `BLG-FE-242` are superseded, unless shipped earlier (DL-088 programme note)
**Acceptance Criteria:**
- axe `color-contrast` passes in the light theme on every routed page; no bare `text-white` remains outside coloured fills

---

## EPIC-04 — Site Structure & Usability Phase 2 Completion: Stops Moved Group

**Maps to:** S2-09 – S2-10
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Description:** Record when the nightly job last moved each position's stop, then test the Dashboard Today list's "Stops moved" group (TL-09/TL-10). This finishes `BLG-FE-254`, open since v9.16 (closure §6 row 3; Carry-Forward #4).
**Estimated days:** 2.00

### ST-09 — Record when the nightly job last moved each position's stop
**Source:** BLG-BE-205
**Priority:** P3 (seated by §1.4c step 1b: named in the Phase 2 row, which `BLG-FE-254` keeps unfinished)
**Effort:** M (~1 day); calibrated to 1.5 days (migration plus a nightly-job write and contract change, v9.16)
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Sequencing:** First in EPIC-04. ST-10 follows.
**UI-facing:** No (`RecentActivityCard.js`'s dead branch is removed with no visible change)
**Scope:**
- Migration: `stop_last_moved_date` and `previous_stop` on positions (`data_model.md`)
- `run_nightly_trailing_stop_update()` writes both only when the stop actually moves (the §7.3 ratchet raises it)
- Return both fields read-only on `GET /positions`; update `position_endpoints.md` and `docs/reference/openapi.yaml`
- Remove `RecentActivityCard.js`'s dead `stop_updated_date` branch
**Acceptance Criteria:**
- After a nightly run that raises a stop, the position's `stop_last_moved_date` is that run's date and `previous_stop` is the stop before the move (pytest)
- A run that leaves the stop unchanged leaves both fields unchanged (pytest)
- Contract and OpenAPI document the fields; drift checks pass

### ST-10 — Today list "Stops moved" group: TL-09 and TL-10
**Source:** BLG-FE-254 (split-achievability remainder; v9.16 ST-06 shipped everything else)
**Priority:** P2
**Effort:** L (~3-4 days) for the whole item; **0.5 days for this remainder** (two Playwright ACs and the group's render once the fields exist)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** After ST-09.
**UI-facing:** Yes
**Scope:**
- Render the "Stops moved" group from `stop_last_moved_date` and `previous_stop`, per `dashboard.md` §1B
**Acceptance Criteria:**
- `dashboard.md` §1B TL-09 and TL-10 have Playwright coverage that passes, in light and dark themes *(restated: v9.16 ST-06 covered TL-01..TL-29 except these two; v9.16 closure §6 row 3)*
- With ST-09 merged, `BLG-FE-254` can be bannered ✅ COMPLETE at Post-Ship Closure *(restated)*

---

## EPIC-05 — Trade Plan Found Defects (v9.16 Carry-Forward)

**Maps to:** S2-11 – S2-14
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner (consulted)
**Description:** Four P2 defects found in v9.16's Arc 2 review and accepted by the Product Owner and Director of Quality at close (v9.16 Carry-Forward #1): plans stay active after their trade closes; an edited plan keeps a stale acknowledgement; Research creates UK plans as US; and the plan stop is not pre-filled from §5.
**Estimated days:** 2.90

### ST-11 — Move a linked trade plan to `closed` when its position closes
**Source:** BLG-BE-211
**Priority:** P2
**Effort:** S (~0.5–1 day); calibrated to 1.25 days (one-off backfill of existing rows, v9.15 `BLG-BE-186` precedent)
**Owner:** Head of Engineering
**Sequencing:** Independent. Before ST-12 and ST-14 only in the sense that all three touch trade plan flows; no file is shared with them.
**UI-facing:** Yes (the lifecycle Playwright test asserts the Trade Plans "Closed" badge)
**Scope:**
- In the `POST /positions/{id}/exit` full-exit path, set `status = 'closed'` on the plan linked to the position (best-effort, like the link step); a partial exit leaves the plan `active`
- One-off backfill: plans with `status = 'active'` whose linked position is `closed` become `closed`
- pytest for the full-exit, partial-exit and no-plan cases
**Acceptance Criteria:**
- After a full exit, the linked plan's status is `closed`; after a partial exit it stays `active`
- Existing `active` plans whose position is already closed are backfilled to `closed`
- `tests/e2e/trade-plan-lifecycle.spec.js`'s exit mock sets `closed`, and the test asserts the Trade Plans "Closed" badge after the exit

### ST-12 — Reset the Trade Plan pre-entry acknowledgement when the check result changes
**Source:** BLG-FE-278
**Priority:** P2
**Effort:** S (~0.5d)
**Owner:** Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Sequencing:** Decision first (RISK-05). Edits `TradePlan.js` with ST-07 and ST-14 (RISK-01).
**UI-facing:** Yes
**Overlap:** unseated `BLG-FE-269` (P3) covers the same reset in the shared `PreEntryValidationPanel.js`, plus auto-expand. If this story's change satisfies `BLG-FE-269`'s first AC, record that for `groom backlog`.
**Scope:**
- Decide with the Strategy Rules & System Intent Owner: clear the box when `advisory_status` or `checks` change, or store the acknowledgement inside the dated snapshot
- Implement in `TradePlan.js` (and Trade Entry if the panel is shared) and update `trade_plan.md` §5e
**Acceptance Criteria:**
- Editing an acknowledged plan so that a new WARN/FAIL appears leaves the box unticked until the user ticks it (Playwright)
- A plan saved without re-acknowledging shows the Trade Entry panel with the unacknowledged reason line (Playwright)

### ST-13 — Pass the market from Research View's "Create Trade Plan" so a UK plan is not created as US
**Source:** BLG-FE-281
**Priority:** P2
**Effort:** XS (<1h plus a Playwright test)
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Add `market` (from the research response's `market`) to the "Create Trade Plan" URL in `Research.js`; check the "View full plan" link carries it too
- Playwright: a UK ticker's Research View → "Create Trade Plan" opens a UK plan
**Acceptance Criteria:**
- From the Research View of a UK ticker, "Create Trade Plan" opens a Trade Plan with market UK and £ amounts; a US ticker still opens US
- Playwright coverage passes

### ST-14 — Pre-fill the Trade Plan stop from the §5 suggested stop and flag a typed stop that differs
**Source:** BLG-FE-282
**Priority:** P2
**Effort:** S (~1 day)
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner (consulted)
**Sequencing:** Edits `TradePlan.js` with ST-07 and ST-12 (RISK-01). Closes the `DEV-v9.16-ST27-01` Known Deviations row in `trade_plan.md` (v9.16 closure §6 row 1).
**UI-facing:** Yes
**Scope:**
- Pre-fill Stop Level from the signal's suggested stop per §5a.3 (new plans with signal context; never overwrite a typed value)
- When the typed stop differs from the §5 stop (entry − 5×ATR, where ATR is known), show next to the suggested size that Trade Entry will store the §5 stop, with that stop's value
- Playwright coverage; `trade_plan.md` §5a.3/§5f updated if wording changes
**Acceptance Criteria:**
- Opening a plan from a signal ("Plan this" or the watchlisted lookup) pre-fills Stop Level with entry − 5×ATR; a typed value is not overwritten
- With a typed stop that differs from the §5 stop, the page states the stop Trade Entry will store
- Playwright coverage passes
- `trade_plan.md`'s `DEV-v9.16-ST27-01` Known Deviations row is marked resolved *(restated: added at v9.16 Post-Ship Closure STEP 5 for this gap, closure §6 row 1)*

---

## EPIC-06 — Market-Data Reliability & Sizing Correctness

**Maps to:** S2-15 – S2-17
**Owner:** Infrastructure & Operations Owner; Head of Engineering; FinOps & Resource Architect
**Description:** Find and fix the on-demand Yahoo failures that v9.16's first production weekly report showed, alert when weekly call volume passes 2× the now-recorded baseline, and keep batch sizing within available cash once fees are added.
**Estimated days:** 2.00

### ST-15 — Find out why most on-demand Yahoo calls fail on production (earnings, positions, gap risk, research)
**Source:** BLG-OPS-217
**Priority:** P2
**Effort:** S (~0.5d); calibrated to 1.0 day (production diagnosis and a post-fix production report)
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Delegation note:** Human-Delegation for the production `api_call_log` breakdown and the post-fix weekly report (RISK-03).
**Sequencing:** Before ST-16, so the alert's baseline reflects the post-fix failure counts, or ST-16 reads §4 whatever its state.
**UI-facing:** No (the "what the user sees" check may file follow-ups; no observable AC here)
**Scope:**
- Break the failures down by `endpoint` (provider path) and ticker from production `api_call_log` for each of the four features, and find the cause
- Fix what is broken, or document an expected failure (for example a symbol with no earnings data) so it is not counted as a provider failure
- Check what the user sees when these calls fail (earnings badge, gap-risk warning, positions prices, research)
- If the failure count changes materially, re-record §4's failure column from a new production weekly report
**Acceptance Criteria:**
- Each of the four features has a recorded cause for its failures
- After the fix, one production weekly report shows each feature's failure rate below 10%, or the remaining failures are documented as expected *(post-merge: needs 7 days of production data after the fix deploys)*
- `data_pipeline_cost_baseline.md` §4 failures reflect the post-fix state, or state why they were kept

### ST-16 — Alert when weekly market-data call volume exceeds 2× the baseline
**Source:** BLG-OPS-195
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Dependency:** met. `data_pipeline_cost_baseline.md` §4 was recorded on 2026-11-11 (v9.16 ST-13).
**Sequencing:** After ST-15 (see ST-15).
**UI-facing:** No
**Scope:**
- A weekly scheduled workflow that calls `GET /ops/api-call-attribution?window=weekly`, compares each source's calls, failures and estimated cost with the recorded baseline, and sends a Telegram message naming the source and the top features when any exceeds 2×
- Keep the baseline figures in one place the check reads, not copied into the workflow
**Acceptance Criteria:**
- A test with a report over 2× baseline produces the advisory message, and one under it produces none
- A failed report call fails the workflow loudly (as `ai-daily-cost-check.yml` does)

### ST-17 — Batch signal sizing can allocate more than available cash once fees are added
**Source:** BLG-BE-178
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Size against cash net of estimated fees (or reduce shares until fees fit), per signal or per batch
- Unit tests for UK, US and mixed batches
**Acceptance Criteria:**
- For UK, US and mixed batches, the sum of `total_cost` is ≤ `available_cash` (unit test)

---

## EPIC-07 — Governance, Strategy Copy & Drift Tooling

**Maps to:** S2-18 – S2-20
**Owner:** Head of Specs Team; PMO Lead; Frontend Specifications & UX Documentation Owner; QA & Testing Owner
**Description:** Let a §1.3a gate clearance also clear a gate-worded `Provisional-Target`, settle the Positions page's 2R Exit Zone threshold, and stop the data-model drift detector reading rollback-only index names.
**Estimated days:** 0.55

### ST-18 — Release Planning §1.3a: let a gate clearance also set a gate-worded Provisional-Target to TBD
**Source:** BLG-GOV-419
**Priority:** P3 (seated by §1.4c step 1a: `LL-v9.16-Release-03`)
**Effort:** XS (<1h)
**Owner:** Head of Specs Team; PMO Lead
**Sequencing:** Early in the sprint, so the change is live before the next Release Planning run.
**UI-facing:** No
**Scope:**
- In `release_planning_prompt.md` §1.3a bound 2, allow the same dated clearance note to replace gate language in `Provisional-Target` with `TBD`, and nothing else in that field
- Confirm with the Head of Specs Team that this stays within the `ESC-CLOSE-20261007-01` ruling, or record the ruling extension
- Apply the CLAUDE.md §6 checklist
**Acceptance Criteria:**
- §1.3a states that a gate clearance may set a gate-worded `Provisional-Target` to `TBD` in the same edit, and lists it in `run_manifest.md`
- The next Release Planning gate scan after a clearance does not list the cleared item as a data-quality warning for its `Provisional-Target` *(post-merge: met at the next Release Planning run that clears a gate)*

### ST-19 — Define or remove the 2R Exit Zone threshold the Positions page states
**Source:** BLG-SPEC-202
**Priority:** P3
**Effort:** XS (~0.25 day)
**Owner:** Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Sequencing:** Decision first (RISK-05). The tooltip is in `src/pages/Positions.js`, which EPIC-01 rewrites, so the change lands on EPIC-01's version of the file (RISK-01).
**UI-facing:** Yes (tooltip wording)
**Scope:**
- Find where the Exit Zone threshold is computed; with the strategy owner, either add it to `strategy_rules.md` §11 (then to `src/constants/strategy.js` and the lint) or reword the tooltip to describe the shipped behaviour without a rule number
**Acceptance Criteria:**
- The tooltip's threshold is either defined in `strategy_rules.md` and imported from `src/constants/strategy.js`, or no longer stated as a number; `scripts/check_strategy_copy.py` passes

### ST-20 — Stop check_data_model_drift.py reading index names from rollback blocks
**Source:** BLG-QA-223
**Priority:** P4
**Effort:** XS (<1h)
**Owner:** QA & Testing Owner; Data Model & Domain Schema Owner
**Sequencing:** Independent. ST-09 adds a migration to `data_model.md`; run the detector after both merge.
**UI-facing:** No
**Scope:**
- Exclude SQL inside blocks introduced by `Reversible:` or under a `Down Migration` heading from index and CHECK-constraint name parsing
- Add a unit test with a fixture containing a rollback-only index name
- Keep each run's `--json` output (for example, a dated file under `docs/ops/` committed with the triage that uses it), so later triage can name every finding
**Acceptance Criteria:**
- Running the detector against `data_model.md` no longer reports `idx_trade_plans_ticker`
- A unit test fails if a rollback-only index name is reported again
- The detector's documented usage, or the triage procedure, says where a run's `--json` output is kept, and the next triage cites it
