**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Complete
**Last Updated:** 2026-11-03

---

# Cycle Record — Roadmap Rebalance `2026-11-03__scheduled`

Working content for STEPs 2–8.5 (`roadmap_prompt.md` v9.36, STEP 0.C). Tier: **Standard** (scheduled; 18 days since the last scheduled rebalance; CPS N/A).

## STEP 2 — Re-Validation

**Active initiatives:** 0, the 19th consecutive cycle with none (unchanged since 2026-04-03). No 🔥/⚠/❌ classifications are required.

**Strategy Proximity / CPS (2.1–2.2):** CPS = N/A (no active initiatives). Prior cycle CPS N/A, so delta N/A. No Strategy Drift Alert. For reference only (backlog items, not initiatives): the Strategy Rules & System Intent Owner scored `BLG-FE-244` at **3** (standard feature; §4.2) when confirming its scope; every other programme item is 2 (standard improvement; None).

### Horizon Review

- **Now:** empty at run start (v9.14 had no §3 section; `manage roadmap` at v9.14 closure retired nothing). STEP 8 adds a `v9.15` section (STEP 8.1).
- **Next / Later / Gated:** no movement. **SI-02:** `**Last formally confirmed:**` cited unchanged (NOT MET); no live check attempted — no production credential in this checkout, and the sandbox `DATABASE_URL` is staging and was not queried (credential fallback, v9.6). **PO-02 / PO-04 / trade-plan gates:** unchanged. **Arc 5:** not complete (SI-02 not shipped), so `BLG-FE-54`'s gate stays unmet.
- **Operating mode:** backlog-driven delivery with empty Arc horizons (§2.3, v9.20 note). Expected, not a process failure. This run adds a provisional multi-release programme plan inside the Now section; it does not move Next/Later items.

## STEP 2.4 — Product Value Ratio

| Release | Source | Total |
|---------|--------|-------|
| v9.10–v9.14 | `docs/product/changelog.md` inline `[U|G|D|P]` tags | 205 |

**Totals:** U=63, G=25, D=115, P=2 of 205 (`scripts/compute_rebalance_diagnostics.py`; tags read, not re-derived).

**user_value_ratio = 0.307 — Advisory tier**, the first reading out of the Alert tier after 8 consecutive Alert readings (0.204 at `2026-10-16__scheduled`). Sustained-Advisory clause: 1 consecutive Advisory reading, not applicable. The Facilitator surfaces the Advisory reading at STEP 8.

**Effort-weighted reading: 0.376** (U 52.57 of 139.82 effort-days), coverage **205/205**, no exclusions. Computed by hand per STEP 2.4: the window v9.10–v9.14 is not in `scripts/compute_effort_weighted_pvr.py`'s `WINDOWS` map, so the script was not run or edited; its parsing helpers and the Appendix F normalisation were called from a scratch script. Diagnostic only.

**Challenger (Product Velocity Concern):** ratio 0.307 < 0.50. The proposed pull-forward is this window's programme: 26 of the 27 new items are build-and-ship U-items grounded in direct reads of live surfaces.

**PO written response — Modify:** commit 7 build-and-ship U-items and 3 specs to v9.15 (STEP 8.1), with Phase 2–3 provisionally targeted at v9.16–v9.17.

## STEP 3 — Backlog Health Review

Tags: no obsolete or duplicate items among items touched this run. Quick wins noted for Release Planning: `BLG-FE-246`, `BLG-FE-247`, `BLG-FE-249`, `BLG-FE-266` (each S ~0.5 day). Technical debt accumulating: the light-theme defect class (`BLG-FE-224`, `BLG-FE-242`), now addressed at root by `BLG-FE-264`/`265`.

### 3.1 Actionable Backlog Assessment

**Method:** structural heuristic (257 active items at scan time, ≥ 150), script-assisted (`scripts/scan_backlog_gate_conditions.py --as-of 2026-11-03 --json`), the same method as the last 6 rebalances. The script now reports explicitly-ungated items separately (10), so the prior cycle's manual "None"-gate adjustment is no longer needed — methodology note, not a series break in A's meaning.

| Category | Count (of 257 scanned) |
|----------|-------|
| A (157 ungated + 1 date-lapsed) | 158 (61.5%) |
| T | 10 |
| D | 19 |
| L | 70 |

**Date-lapsed (A — verify):** `BLG-OPS-48` (ANTHROPIC_API_KEY 6-month scope audit; "No earlier than 2026-11-01"). No remaining non-date condition. Carried into the cycle summary's capacity outlook. The script also lists 5 `already_resolved` items (`BLG-OPS-200`, `202`, `203`, `204`, `BLG-SEC-44`) and 20 "gating item shipped — verify" items; both lists are left for Release Planning §1.3a.

**D-gated:** the PO-02 cluster and the SI-02 cluster (`**Last formally confirmed:**` NOT MET; no clearance estimate).

**T-gated:** `BLG-FEAT-26`, `BLG-FEAT-30`, `BLG-FEAT-31`, `BLG-BE-24`, `BLG-OPS-41`, `BLG-OPS-53`, `BLG-GOV-144`, `BLG-OPS-84`, `BLG-FEAT-92`, `BLG-GOV-382`.

**L-gated top 5:** `BLG-FE-43/45/54/58/59` (P1, Arc-5 sprint-entry gates). None more than 12 months away; no archive candidates.

**Backlog Accessibility Warning:** 61.5% ≥ 30%, not triggered.

## STEP 4 — Ideas

Pre-clean: `ideas_housekeeping_prompt.md` ran at v9.14 post-ship STEP 12.5 (`closure_record.md` §STEP 12.5: 0 rows archived), so it is not re-run. Loaded: 11 `Submitted` rows from `IW-20261103-01`; 0 parked.

### Gate-Condition Re-Check

No loaded idea has a Park Rationale (all new). N/A.

### Per-Idea Classification (PO; Facilitator verified the overlap checks; Challenger challenged each)

| Idea | Challenger challenge | PO classification | Filed as |
|------|---------------------|-------------------|----------|
| IDEA-head-of-ux-20261103-01 | Does §4.2 even apply to unplanned entries, or is this a new rule? Rebuttal: Strategy Rules & System Intent Owner confirmed §4.2 covers every manual entry; display-only, no new blocking (§3 intact). | 📋 Backlog (ungated) | `BLG-FE-244` (P1, STEP 8.0) |
| IDEA-head-of-ux-20261103-02 | A home redesign is churn for a single user. Rebuttal: the regime (§4.2.1) sits in row 4; the change reorders existing content, spec first. | 📋 Backlog (ungated) | `BLG-SPEC-215`, `BLG-FE-254` |
| IDEA-head-of-ux-20261103-03 | v8.5's ST-15 already said "no redesign". Rebuttal: ST-15 assessed the sidebar pattern only; this keeps the pattern and changes grouping, labels and links. | 📋 Backlog (ungated) | `BLG-SPEC-214` (consolidated with frontend-specs-01), `BLG-FE-247`, `249`, `250`, `251`, `252`, `253` |
| IDEA-head-of-ux-20261103-04 | Duplicates `BLG-FE-54`. Rebuttal: `BLG-FE-54` is a gated exploration on the planned path; these are two ungated build slices. PO keeps `BLG-FE-54`'s gate and cross-references. | 📋 Backlog (ungated) | `BLG-FE-255`, `BLG-FE-256` |
| IDEA-head-of-ux-20261103-05 | Merges risk breaking §13-cleared journal surfaces. Modify: `BLG-SPEC-216` carries a Strategy Owner §13 confirmation AC before build. | 📋 Backlog (ungated) | `BLG-SPEC-216`, `BLG-FE-257`, `258`, `259`, `263` |
| IDEA-head-of-ux-20261103-06 | Column cuts hide data. Rebuttal: expandable rows keep every column; only the default order changes. | 📋 Backlog (ungated) | `BLG-FE-260`, `261`, `262` |
| IDEA-head-of-ux-20261103-07 | A review is not build-and-ship. Accepted: it is review-shaped by design (the user's request) and gated so it cannot be seated early. | 📋 Backlog (gate-conditional) | `BLG-UX-08` (gate: every other programme item complete) |
| IDEA-frontend-specs-20261103-01 | Copy changes are cosmetic. Rebuttal: the inverted FX label is a correctness risk of the `BLG-BE-190` class. | 📋 Backlog (ungated) | `BLG-FE-246`, `BLG-FE-248`; glossary section in `BLG-SPEC-214` |
| IDEA-frontend-specs-20261103-02 | The backend already falls back safely (`BLG-BE-194`). Rebuttal: the UI pre-fill never asks the backend; it hard-codes 1.27. | 📋 Backlog (ungated) | `BLG-FE-245` (P1, STEP 8.0) |
| IDEA-frontend-specs-20261103-03 | A token migration is large and risky. Modify: split into shells (`BLG-FE-264`, v9.16) and a sweep (`BLG-FE-265`, v9.17). | 📋 Backlog (ungated) | `BLG-FE-264`, `BLG-FE-265` |
| IDEA-frontend-specs-20261103-04 | Too small for a roadmap. Accepted as a quick win, not a roadmap item. | 📋 Backlog (ungated) | `BLG-FE-266` |

**Idea Consolidation convention:** applied once — `IDEA-head-of-ux-20261103-03` and `IDEA-frontend-specs-20261103-01` converge on `BLG-SPEC-214` (navigation spec + glossary labels share one owner and one revision). Both register rows name it.

**Queue check:** 0 ideas classified ✅ Advance → STEP 5 Debate Queue has 0 rows; "Advancing to STEP 5" = 0. Consistent.

### Idea Participation Check

Reduced-roster window (§4.1): 2 of 22 roles opened, both met the minimum (7 and 4). No innovation-debt note for opened roles; the 20 roles not opened are not a shortfall under §4.1.

### Submission Details (full template fields — `IW-20261103-01`)

Source for every submission below: the Head of UX & Design website review held in session on 2026-11-03 (first-principles target vs current site; navigation/IA, page architecture and user-journey lenses; IA verdict "modify substantially, don't redesign"). Evidence is cited by file and line as read on `main` at `ab7fbf23`. Overlap checks (§2.0 steps 5–6) are recorded per idea.

#### IDEA-head-of-ux-20261103-01 — Run the pre-entry checks on every route into Trade Entry

- **Submitted by:** Head of UX & Design · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** The §4.2 pre-entry checks (regime gate, sector concentration, earnings proximity, cash, sizing validity) run only on the Trade Plan page (`src/pages/TradePlan.js` "Pre-Entry Checks", `EntryChecklist`, acknowledgement box). The three most prominent routes into a new trade skip them: the sidebar "Trade Entry" link, the Positions "New Position" button and the `n` keyboard shortcut (on Positions and Trade History, `Layout.js` global handler) all open `src/pages/TradeEntry.js`, which has no pre-entry check, regime read or checklist (grep for `regime|pre-entry|checklist` in `TradeEntry.js` finds none). A trader can record an entry in a risk-off or unknown-regime market (§4.2.1, §8.2 as amended v1.20) without seeing the gate. This is a contradiction between what the system enforces on one path and what it lets through on the others.
- **2. Strategic Alignment:** §4.2 — Pre-Entry Advisory Checks; §4.2.1 unknown regime (v1.20); §3 human-in-the-loop. Rationale: §4.2 defines the checks as the advisory conditions for every entry, not for planned entries only; §3 keeps the human deciding, so the checks must be in front of the human at the point of decision on every path. Advisory display only — no automatic blocking beyond what §4.2 already defines.
- **3. Proposed Solution:** Trade Entry shows the same pre-entry check panel (regime, concentration, earnings, cash, sizing) whenever the entry is not linked to a Trade Plan that already passed them, with the same acknowledge-to-proceed step the plan uses. Plan-linked entries keep their existing flow. No new check logic; reuse the existing validation endpoint and components.
- **4. Expected Value:** 3 of 3 unchecked entry routes closed (100% of new entries pass through the §4.2 checks, from roughly 1 path in 4 today). Override events from the direct path become visible to the Red Flag Journal / SI-05 digest, which today undercount them.
- **5. Effort Estimate:** Small — days to 1 week. Constraints: reuses `EntryChecklist`/pre-entry validation; needs a Strategy Rules & System Intent Owner confirmation that the §4.2 wording covers unplanned entries.
- **6. Reversibility:** Fully reversible — a UI panel on one page. Reasoning: no data model or rule change.
- **7. What Would You Stop?:** No view — leave to debate. (Now horizon is empty.)
- **8. Submitter Recommendation:** Now. Reasoning: it is a strategy-integrity gap on the most-used path.
- **Overlap checks:** backlog — `BLG-FE-54` (unified pre-entry gateway, UX exploration, gated on Arc 5 completion) and `BLG-FE-58/62` (panel grouping/specification) cover consolidating SI-01 and PT-05 on the planned path; none covers the unchecked direct path. This idea refines `BLG-FE-54` with an ungated, build-shaped slice. Codebase — confirmed absent in `TradeEntry.js`.

#### IDEA-head-of-ux-20261103-02 — Turn the Dashboard into a prioritised "Today" action list

- **Submitted by:** Head of UX & Design · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** `src/pages/DashboardHome.js` renders 13 blocks of near-equal visual weight (5 morning-briefing cards, the exit-conditions card, the AI briefing, Open Positions, Portfolio Heat, In Grace Today, Signal Status, Recent Activity, the gate-progress strip, What's New). The regime — the condition that decides whether any entry is allowed — sits in the 4th row inside "Signal Status". On a quiet day the baseline screenshot (`tests/e2e/__snapshots__/visual-regression-baselines.spec.js/dashboard-home-dark-chromium.png`) shows 11 empty-state boxes each saying "nothing here". The page reports status; it does not say what to do.
- **2. Strategic Alignment:** §3 human-in-the-loop execution; §4.2.1 regime gate; §8 exit conditions. Rationale: the system's job (§3) is decision support for a trader who acts manually; the home surface should present the decisions due today in the order the strategy imposes them — regime, then exits/stop changes, then qualifying entries.
- **3. Proposed Solution:** A "Today" list at the top of the Dashboard: market regime per market first, then exits and stop changes due, then qualifying entries, each item one click from its action (existing deep links such as `/Positions?exit=<id>` reused). Quiet days show a single "Nothing to do today" line. Status cards, What's New and gate progress move below the fold. Requires a `dashboard.md` spec revision first (Class 1, Frontend Specifications & UX Documentation Owner; Head of Specs Team approval).
- **4. Expected Value:** Time-to-first-action on the daily review falls from scanning 13 blocks to reading the first list item; regime visible without scrolling (row 4 → row 1); empty-state boxes on a quiet day 11 → 1.
- **5. Effort Estimate:** Medium — 1–3 weeks. Constraints: spec revision (`dashboard.md` v3.10 → next major) before build; Playwright coverage for each observable AC.
- **6. Reversibility:** Mostly reversible — the existing cards remain, re-ordered. Reasoning: layout and composition change, no data change.
- **7. What Would You Stop?:** No view — leave to debate.
- **8. Submitter Recommendation:** Now. Reasoning: the home page is the daily entry point.
- **Overlap checks:** backlog — `BLG-FE-240` (win-rate widgets on the legacy widget dashboard) and `BLG-FE-70` (compliance trend widget, gate-conditional) touch dashboard content but not structure; no overlap. Codebase — `ExitConditionsCard` already exists and is reused, not duplicated.

#### IDEA-head-of-ux-20261103-03 — Re-group navigation around the trader's jobs and fix wayfinding

- **Submitted by:** Head of UX & Design · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** `src/Layout.js` `NAV_GROUPS` holds 18 entries in 4 groups named by feature type (Trading, Analytics, Tools, System), 3 collapsed by default. Signals (an action surface) sits under Analytics; Weekly Digest under System. Trade Plans — where the pre-entry checks live — has no sidebar entry (reachable only via the command palette). The legacy `src/pages/Dashboard.js` is still routed and the command palette lists two entries both labelled "Dashboard" (`CommandPalette.js` `PAGE_LABELS`). Eight pages are dead ends with no onward link (Reports, Red Flag Journal, Trade Reflections, Replay, Strategy Benchmark, Ticker Universe, System Status, Notification History). No page sets a browser-tab title (`public/index.html` "Position Manager" only). Detail pages (Trade Plan, Research, notification sub-pages) have no parent link. The SI-05 digest deep link lands at the top of Risk Dashboard, not the relevant section (`docs/ux/si05_user_journey_map.md` F-04).
- **2. Strategic Alignment:** §3 human-in-the-loop execution; §4.2 pre-entry checks (Trade Plans discoverability). Rationale: navigation that follows the daily routine (regime → exits → entries → record → review) puts the strategy's decision points one click away; a hidden Trade Plans page pushes users onto the unchecked direct-entry path.
- **3. Proposed Solution:** About five job-based areas (Today · Portfolio · Find trades · Review · Settings), groups expanded by default; Trade Plans and Research surfaced; the legacy Dashboard route and its palette duplicate removed; per-page browser-tab titles; a parent link on detail pages; an onward next-step link on each dead-end page; section anchors on Risk Dashboard for digest links. Requires a `navigation.md` revision (Class 2, v1.7) first.
- **4. Expected Value:** Sidebar entries 18 → ~12 visible in ≤5 groups; undiscoverable pages 2 → 0; dead-end pages 8 → 0; duplicate palette entries 1 → 0; tab titles 0 of 25 pages → 25 of 25.
- **5. Effort Estimate:** Medium — 1–3 weeks. Constraints: `navigation.md` revision; existing Playwright nav tests (`alert-nav-badge.spec.js`, `command-palette.spec.js`, `keyboard-shortcuts.spec.js`) updated in the same stories.
- **6. Reversibility:** Mostly reversible. Reasoning: routes stay stable; only grouping, labels and links change.
- **7. What Would You Stop?:** No view — leave to debate.
- **8. Submitter Recommendation:** Now.
- **Overlap checks:** backlog — no active item; archive `BLG-FE-114` (shipped v7.7, notification nav duplication) and `BLG-FE-154` (count correction). The v8.5 exploration `claude/cycles/2026-08-08__release-v8.5/st15_nav_bar_redesign_exploration.md` recommended keeping the collapsible-sidebar *pattern* on real-estate grounds; it did not assess grouping logic, labels, discoverability or onward links, which are this idea's scope. The sidebar pattern itself is kept. Codebase — confirmed in `Layout.js`, `CommandPalette.js`, `App.js`, `utils/index.js`.

#### IDEA-head-of-ux-20261103-04 — One flow from signal to entered trade

- **Submitted by:** Head of UX & Design · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** Getting from a signal to an entered, checked trade takes 5 pages: Signals (only per-row action is "Add to Watchlist", `components/signals`) → Watchlist → Research → Trade Plan (~14 fields + checklist + acknowledgement) → "Start trade" → Trade Entry. Screener rows link to Research or the watchlist only (`Screener.js:525–532`). On Trade Plan the "Planned Shares" input (`TradePlan.js:976`) is asked before the system's own sizing preview is shown (`WhatIfSizingPreview`, `TradePlan.js:1215`), so the user types a number the system could suggest.
- **2. Strategic Alignment:** §4.1 position sizing (canonical risk-based size); §4.2 pre-entry checks; §3. Rationale: the strategy defines size from risk and stop (§4.1); asking for shares before showing the §4.1 suggestion invites off-rule sizing, and a long hop chain encourages the unchecked shortcut (IDEA-head-of-ux-20261103-01).
- **3. Proposed Solution:** A "Plan this" action on Signals and Screener rows that opens a Trade Plan pre-filled with the signal's ticker, market, price and signal context; the plan shows the §4.1 suggested size before the shares field, pre-filling it. Re-scope `BLG-FE-54` (remove its Arc 5 gate) as the design pass for the combined plan-and-check screen.
- **4. Expected Value:** Pages from signal to entry 5 → 2 (plan, then confirm fill); retyped fields (ticker/market/price) 3 → 0; share counts entered without seeing the §4.1 suggestion → 0.
- **5. Effort Estimate:** Medium — 1–3 weeks. Constraints: depends on IDEA-head-of-ux-20261103-01 for the checks on the direct path; `BLG-FE-54` gate removal is a PO decision.
- **6. Reversibility:** Mostly reversible.
- **7. What Would You Stop?:** No view — leave to debate.
- **8. Submitter Recommendation:** Now.
- **Overlap checks:** backlog — `BLG-FE-54` (refined, see above); `BLG-FEAT-33` (plan approval workflow) is a different scope. Codebase — `TradePlan.js` already reads `?ticker=` and `SignalContextPanel`; this idea adds the entry points and the field order.

#### IDEA-head-of-ux-20261103-05 — One place per concept: grace period, journal, performance

- **Submitted by:** Head of UX & Design · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** Grace period appears in 4 places (Dashboard "In Grace Today", Dashboard "Positions to Watch", Positions `GracePeriodAlertZone`, Risk Dashboard `GracePeriodPanel`). Journaling is split across Trade Reflections, Red Flag Journal and the Journal view inside Positions (which retitles Positions as "Trade Journal"). Win rate, profit factor and total P&L appear on both Reports and Performance Analytics. Reports (1,287 lines), Trade Plan (1,313) and Strategy Benchmark (1,149) are long single scrolls with no tabs (0 `TabsTrigger` across pages).
- **2. Strategic Alignment:** §6 grace period; §12 review and calibration. Rationale: one authoritative view per concept removes the risk of the surfaces disagreeing (precedent: `BLG-BE-183`, grace-period day numbering differs between pages) and makes the periodic review in §12 a single journey.
- **3. Proposed Solution:** One grace view (Positions), linked from the Dashboard and Risk Dashboard; one Journal area combining reflections, red flags and position notes; one Performance page combining Reports and Analytics; tabs or sections on the long pages. Each merge gets a short UX spec before build.
- **4. Expected Value:** Grace surfaces 4 → 1 (+2 links); journal surfaces 3 → 1; duplicated KPI sets 2 → 1; long single-scroll pages 3 → 0.
- **5. Effort Estimate:** Large — 1+ month (three merges). Constraints: Class 1 spec changes for each merged page; the journal merge touches AI-summarised journal surfaces with §13 roster rows (PO-02), so the Strategy Rules & System Intent Owner confirms no §13 boundary moves.
- **6. Reversibility:** Partially reversible — merged pages change URLs and saved habits.
- **7. What Would You Stop?:** No view — leave to debate.
- **8. Submitter Recommendation:** Soon. Reasoning: larger and lower-urgency than ideas 01–04.
- **Overlap checks:** backlog — `BLG-BE-183` (grace numbering) is a symptom this idea removes; `BLG-FE-237` (Reports tab bar overflow at phone width) indicates Reports has a tab bar component on one section — the tabs proposal extends, not duplicates, it; `BLG-FE-72`/`BLG-FEAT-58` (PO-02 journal pattern, gated) are separate. Codebase — confirmed.

#### IDEA-head-of-ux-20261103-06 — Decision-first Positions table, with a phone layout

- **Submitted by:** Head of UX & Design · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** `src/pages/Positions.js` table view has 14 equal-weight columns (Ticker, Entry, Current, Stop, Shares, P&L, P&L %, Days, State, Grace, Earnings, Alerts, Last Reviewed, Actions). What needs a decision — distance to stop and whether an exit condition has fired — is split across Stop, State and Alerts. Four warning banners (`MetricsStalenessIndicator`, `DrawdownReviewPrompt`, `ConcentrationLimitsWarning`, `GracePeriodAlertZone`) sit between the header and the table. The table scrolls sideways (`DataTable` `overflow-x-auto`) and there is no narrow-screen layout, although the SI-05 Telegram digest sends the user into the app from a phone.
- **2. Strategic Alignment:** §7 trailing stop; §8 exit conditions. Rationale: the strategy's in-trade decisions are stop proximity and exit triggers; the primary table should lead with them.
- **3. Proposed Solution:** Rows sorted by urgency (exit fired → stop breached → near stop → rest); leading columns ticker, distance to stop (R and %), action needed; the remaining columns in an expandable row; the four banners combined into one summary strip; a card layout below the `md` breakpoint.
- **4. Expected Value:** Columns visible by default 14 → ~6; banners above the table 4 → 1; horizontal scroll at 390px width eliminated.
- **5. Effort Estimate:** Medium — 1–3 weeks. Constraints: `positions` page spec revision; existing Positions Playwright suites updated.
- **6. Reversibility:** Mostly reversible.
- **7. What Would You Stop?:** No view — leave to debate.
- **8. Submitter Recommendation:** Soon.
- **Overlap checks:** backlog — no active item; archive Positions-table items fixed individual columns, not layout. Codebase — confirmed.

#### IDEA-head-of-ux-20261103-07 — First-principles UX re-review when the programme completes

- **Submitted by:** Head of UX & Design · **Window:** IW-20261103-01 · **Build-and-ship candidate:** No (review-shaped, by design)
- **1. Problem Statement:** The user asked (2026-11-03) that once the last change from this review ships, the site is reviewed again against the same first-principles target and the result confirms or revises the review's verdict. Without a tracked item, nothing triggers that review: the governed routines would close the last story and move on.
- **2. Strategic Alignment:** §12 review and calibration. Rationale: §12 requires periodic review that the system still serves its intent; this applies the same discipline to the experience layer after a large structural change.
- **3. Proposed Solution:** A final item, sequenced after every other item from this programme, owned by the Head of UX & Design: repeat the review using the same method (label audit, inter-page link graph, page-section order, four journey walkthroughs with step and input counts, light/dark screenshots), compare against the 2026-11-03 baseline, and record whether the verdict and top 5 still stand. New findings are filed as backlog items.
- **4. Expected Value:** A recorded before/after comparison on the same metrics (entry routes checked, nav entries, dead ends, signal-to-entry pages, columns, duplicate surfaces); confirmation or revision of the IA verdict.
- **5. Effort Estimate:** Small — days to 1 week. Constraints: runs only after every other programme item is complete; benefits from a running staging app for screenshots.
- **6. Reversibility:** Fully reversible — a review document.
- **7. What Would You Stop?:** Nothing — it closes the programme.
- **8. Submitter Recommendation:** Now (as the programme's final, sequenced item).
- **Overlap checks:** backlog — no active item. Codebase — n/a (process).

#### IDEA-frontend-specs-20261103-01 — Use one name per concept across sidebar, headings and command palette, and fix the inverted FX label

- **Submitted by:** Frontend Specifications & UX Documentation Owner · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** The FX rate is labelled "FX Rate (USD/GBP)" on Trade Entry (`TradeEntry.js:475`) and "FX Rate (GBP/USD)" on the Exit dialog (`ExitModal.js:380`) for the same quantity (USD per £1, `strategy_rules.md` §4.1.3 as amended v1.21). Page names differ between the sidebar, page heading and command palette: Analytics / "Performance Analytics" (+ "Performance Analytics Report"); Positions / "Open Positions" or "Trade Journal"; Trade Entry / "Enter New Position" / "New Position" button / "New trade" shortcut; Reflections / "Trade Reflections" / "Trade Reflection"; Signals / "Monthly Signals"; Replay / "Replay Mode"; Notifications / "Alert History". "Trade" and "position" are used for the same act. `docs/reference/glossary.md` defines domain terms but has no UI-label section.
- **2. Strategic Alignment:** §4.1.3 FX convention (v1.21); §1 purpose (this document prevails over UI interpretation). Rationale: an FX label whose direction flips between entry and exit invites an inverted input — the same class of error `BLG-BE-190` fixed in sizing.
- **3. Proposed Solution:** Add a UI-label section to `glossary.md` (one canonical label per page and action); align sidebar, page headings, command-palette labels and buttons to it; label FX identically on every input as "USD per £1 (GBP/USD)" with a one-line hint.
- **4. Expected Value:** Pages with mismatched names 7 → 0; FX inputs with inverted labels 1 → 0.
- **5. Effort Estimate:** Small — days to 1 week.
- **6. Reversibility:** Fully reversible — copy changes.
- **7. What Would You Stop?:** No view — leave to debate.
- **8. Submitter Recommendation:** Now. Reasoning: the FX label is a correctness risk.
- **Overlap checks:** backlog — none active; archive `BLG-NEW-11` (glossary, complete) and `BLG-SPEC-126` (glossary consolidation) — domain terms only. Codebase — confirmed both labels.

#### IDEA-frontend-specs-20261103-02 — Pre-fill Trade Entry's FX rate from the live rate, not 1.27

- **Submitted by:** Frontend Specifications & UX Documentation Owner · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** `TradeEntry.js:45` and `:213` pre-fill the FX field with a fixed `"1.27"` for US trades. The Exit dialog already uses `position.live_fx_rate` (`ExitModal.js:54`), and the backend exposes the live and last-good rate with its source and age (`BLG-BE-194`, `MarketStatusBar` fx props on Signals). Since the v9.14 sizing fix (`BLG-BE-190`, §4.1.3 v1.21) US share counts scale with FX², so a stale default distorts the suggested size and the recorded GBP cost when the user does not overwrite it.
- **2. Strategic Alignment:** §4.1.3 US sizing formula (v1.21); §4.1.4 sizing validity. Rationale: the canonical size depends on the FX rate; the default the UI offers should be the system's best current rate, labelled with its source.
- **3. Proposed Solution:** Pre-fill the FX field from the live (or last-good) rate the backend already serves, show its source and age, and keep it editable.
- **4. Expected Value:** US entries saved with the hard-coded default → 0. At FX 1.35 vs the 1.27 default, the suggested size error is about 13% (FX² ratio), removed.
- **5. Effort Estimate:** Small — days to 1 week.
- **6. Reversibility:** Fully reversible.
- **7. What Would You Stop?:** No view — leave to debate.
- **8. Submitter Recommendation:** Now. Reasoning: correctness — candidate for STEP 8.0 fast-track.
- **Overlap checks:** backlog — `BLG-BE-199` (reject non-positive FX override in `POST /portfolio/size`) is backend validation, not the UI default; archive `BLG-BE-169`/`BLG-BE-194` fixed the backend fallback, not the Trade Entry default; `BLG-FE-164` (What-If preview sends no fx override) is a different component. Codebase — confirmed both lines.

#### IDEA-frontend-specs-20261103-03 — Semantic colour tokens so the light theme stops breaking piecemeal

- **Submitted by:** Frontend Specifications & UX Documentation Owner · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** `design_system.md` v1.1 declares light mode supported, but the shared shells are dark-only: `src/index.css` sets `body` to `bg-slate-950 text-white` for both themes; `DashboardCard.js:21` and `ui/DataTable.js` use `bg-slate-800/50` / `from-slate-900 to-slate-800` with no light pair. `src/` has 376 bare `text-white` and 331 bare `bg-slate-800/900` classes. The light baselines show an invisible empty-state heading on Positions, illegible RISK-ON badges and a black gate strip. Fixes arrive one element at a time (`BLG-FE-87/88/95/200/224/242`).
- **2. Strategic Alignment:** §1 purpose — what the user sees must not misrepresent system state. Rationale: an illegible regime badge in one theme is a display defect on a §4.2.1 decision input.
- **3. Proposed Solution:** Define semantic tokens (surface, surface-raised, text, text-muted, positive, negative, warning) for both themes; convert the base, card and table shells first, then migrate pages, retiring the per-element dark/light pairs.
- **4. Expected Value:** Light-theme contrast failures on shared shells → 0 (axe `color-contrast` on Dashboard, Positions, Trade Plan, Settings); new piecemeal light-theme items per release → near 0.
- **5. Effort Estimate:** Medium — 1–3 weeks (shell conversion), then a page sweep. Constraints: `design_system.md` update in the same PRs.
- **6. Reversibility:** Mostly reversible.
- **7. What Would You Stop?:** Stop filing per-element light-theme fixes; fold `BLG-FE-224`/`BLG-FE-242` into this.
- **8. Submitter Recommendation:** Soon.
- **Overlap checks:** backlog — refines `BLG-FE-224` and `BLG-FE-242` (per-element fixes) with the root-cause change; neither proposes tokens. Codebase — `tailwind.config.js` registers 9 shadcn tokens (v8.6) but the app's own shells do not use them.

#### IDEA-frontend-specs-20261103-04 — Fix three small chrome defects: version label, What's New heading, sidebar height

- **Submitted by:** Frontend Specifications & UX Documentation Owner · **Window:** IW-20261103-01 · **Build-and-ship candidate:** Yes
- **1. Problem Statement:** The sidebar footer shows a hard-coded `v1.0.0` (`Layout.js:814`) while the product is at v9.14. `WhatsNewCard.js:41` renders "What's New — undefined" whenever the changelog payload has no `version` (seen in the dashboard baselines). The desktop sidebar background stops part-way down long pages (dashboard baselines).
- **2. Strategic Alignment:** §1 purpose — displayed information matches the system. Rationale: a wrong version label misleads anyone checking which release they are using against the changelog.
- **3. Proposed Solution:** Show the real release version from the changelog endpoint; omit the version suffix when absent; make the sidebar background full height.
- **4. Expected Value:** 3 visible defects → 0.
- **5. Effort Estimate:** Small — days to 1 week.
- **6. Reversibility:** Fully reversible.
- **7. What Would You Stop?:** No view — leave to debate.
- **8. Submitter Recommendation:** Soon.
- **Overlap checks:** backlog — none. Codebase — confirmed.

## STEP 5 — Debate

Queue empty — no debates required. No idea was classified ✅ Advance.

## STEP 6 — Scoring

No surviving STEP 5 candidates, so there is nothing to score. `claude/scoring/scored_initiatives.md` is not rewritten this run.

## STEP 7 — Workforce Economics

No in-scope initiatives, so there is no FTE load to assess. Programme load is recorded in `workforce_capacity.md` (v9.15 ≈11.5-13 days committed; v9.16 ≈15.5, v9.17 ≈20.5, v9.18 ≈1 provisional).

- **§7.1 Skill-Silo:** 68.1% pooled (96/141, v9.12–v9.14). Above the 40% ceiling; under the v9.35 definition the run of unresolved readings is well over 3. **Sustained-failure clause applies:** ≥2 build-and-ship U-items at v9.15 — met by `BLG-FE-244`, `BLG-FE-245` (and `BLG-FE-246`, `247`, `248`, `249`, `266`). Candidate gate verification: none has a `**Gate criteria:**` line. Live-status cross-check: all active, filed this run. Cross-role pairing note read (advisory).
- **§7.2:** max 9.2% raw (AI Compliance & Governance Officer; Backend Engineering Patterns Owner, v9.12–v9.14) — no advisory. Source `role_share_history.md`, v9.13 and v9.14 rows appended via script this run.
- **§7.3:** `ready_pool_history.md` newest row v9.14: gap 53.55 days; series v9.12 26.70 → v9.13 36.65 → v9.14 53.55, 2 consecutive increases — below the 3-release trigger; advisory only. Runway: N/A — pool growing. This run adds ≈49 days to the pool.
- **< 20% floor:** not applicable.

## STEP 8 — Final Rebalance Decision

**Initiatives:** no change (0 active). Valid "no change" outcome for initiatives; `Last Updated` refreshed and DL-088 logged.

**Facilitator (STEP 2.4 Advisory surfaced before decisions):** PVR 0.307 Advisory. PO response recorded at STEP 2.4 (Modify).

**Displacement candidate flag:** none (no initiatives). `displacement_debt_register.md` and `initiative_register.md` unchanged.

### STEP 8.0 — Production Correctness Fast-Track

Scanned 13 pre-existing P0/P1 items (`BLG-FEAT-73`, `BLG-FE-43/45/54/58/59/62/63/68/69/70/71`, `BLG-SPEC-35`): none is a correctness or security item. **`BLG-FE-244` and `BLG-FE-245` (P1, filed this run) qualify** — an entry path that skips the §4.2 gate, and a hard-coded FX pre-fill that distorts §4.1.3 sizing. **Promoted to the v9.15 Now horizon** ("Correctness Fast-Track Promotion", DL-088). No PO override: both can affect a trading decision.

### STEP 8.0.5 / 8.2 — Candidate verification

For each of the 10 v9.15 items (`BLG-FE-244`, `245`, `246`, `247`, `248`, `249`, `266`, `BLG-SPEC-214`, `215`, `216`) and the 17 provisionally targeted items: active in `backlog.md`, no `✅ COMPLETE`, no `RA:` marker. **STEP 8.2 verification complete — 27 items verified active, 0 items excluded.**

### STEP 8.1 — Empty Now Horizon Gate

Conditions 1a (Now empty) and 2 (no next-release section) were true at run start.

**PO decision (STEP 8.1): Option (a) — next-release section added to current_roadmap.md. Section: v9.15 — Site Structure & Usability, Phase 1. Rationale:** the user asked for the Head of UX & Design review to become the roadmap's focus; a version-labelled section with 10 committed items lets Release Planning pass §-1.2 directly, and the programme plan records the provisional v9.16–v9.18 phasing.

### STEP 8.1.5 — §13-Adjacent Initiative Expiry Review

⚠ **§13-adjacent expiry:** `BLG-FEAT-55` / `BLG-SPEC-65` / `BLG-SPEC-66` have been gated on an unopened §13 chat-persistence review since 2026-07-25, more than 2 rebalance cycles. Surfaced to the Strategy Rules & System Intent Owner. Recorded response (agent-mediated, §5.3, unchanged basis): **"still not ready, re-check next cycle"** — chat remains stateless per SRB-v1.7 and no persistence design exists to review. Clears this cycle's surfacing. `BLG-GOV-391` (last cycle's related item) has since shipped (archived).

## STEP 8.5 — Stateless Write Safety Gate

### 8.5.A — Re-anchored decisions

1. Add a `v9.15` Now section (STEP 8.1 Option (a)) with 10 items and the programme plan; §1 Next planned release → v9.15.
2. File 27 backlog items from STEP 4.
3. Set 11 register rows to `Promoted-Backlog`.
4. Append DL-088.
5. Append history rows (PVR; role share v9.13 + v9.14) and a workforce section.
6. Make no initiative changes; `BLG-FE-54` unchanged (PO: keep gate; cross-referenced from the new items).

### 8.5.B — Write plan

| File | Change | Traceable to |
|------|--------|--------------|
| `claude/roadmap/current_roadmap.md` | §1 Next planned release → v9.15; §3 v9.15 section + programme plan; Last Updated / Last rebalance | (A) STEP 8.1, 8.0, §7.1, STEP 2.4 |
| `claude/backlog/backlog.md` | Append 27 items (STEP 4) and 3 deferred-patch tracking items `BLG-GOV-405`–`407` (STEP 11, `BLG-GOV-393` precedent); Last Updated | (A) STEP 4; process (STEP 11.2) |
| `claude/roadmap/decision_log.md` | Append DL-088 (count 50 → 51, verified; prior text byte-identical) | (A) STEP 8 |
| `claude/roadmap/product_value_ratio_history.md` | Append row, refresh sparkline; Last Updated | (A) STEP 2.4 |
| `claude/roadmap/role_share_history.md` | Append v9.13 and v9.14 rows and breakdowns; rolling line; Last Updated | (A) §7.2 |
| `claude/roadmap/workforce_capacity.md` | Append "Rebalance 2026-11-03__scheduled" section; Last Updated | (A) STEP 7 |
| `claude/ideas/ideas_register.md` | 11 rows → `Promoted-Backlog` | (A) STEP 4.2 |
| `claude/ideas/ideas_window.json`, `window_summary_IW-20261103-01.md` | Intake window (committed separately, intake STEP 5, `61dbc2f5`) | STEP -1.6 |
| `claude/cycles/2026-11-03__scheduled/*` | run_manifest, cycle_record, cycle_summary, lessons_learnt, escalations | Process |
| `.claude_current_state.json` | Rebalance keys (STEP 12) | Process |

Written before this plan, in its own commit (`c06e05f3`), at STEP -1.5: `post_ship_closure.md`, `changelogs/post_ship_closure_changelog.md`, `OPERATIONAL_GUIDE.md`, `prompt_change_log.md` — the OVERDUE patch application (Head of Specs Team, user acting in role, `ESC-RB-20261103-01`), within §4's `claude/system/*` scope.

**Register row status verification:** no `Advancing` rows, so nothing needs a terminal status.

**BLG-ID collision advisory:** highest IDs across `backlog.md` + `backlog_archive.md` before this run: `BLG-FE-243`, `BLG-SPEC-213`, `BLG-UX-07`. New IDs `BLG-FE-244`–`266`, `BLG-SPEC-214`–`216`, `BLG-UX-08`; each verified absent from the archive and present once in `backlog.md`. No collision.

### 8.5.C / D — Verification

Every file in the plan is within §4 write scope. Decision log append-only (50 → 51, no prior text changed). No formatting-only edits. Every write traces to (A). **PASS.**

### 9.0 — Net-Zero Displacement

Additions (✅ Advance) 0; confirmed kills 0. 0 ≤ 0, **passes**.

**Post-write checks:** `scripts/check_backlog_item_integrity.py` passes on `backlog.md`. No park counts this cycle, so the park-count grep is not applicable.
