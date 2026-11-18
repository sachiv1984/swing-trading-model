**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Complete
**Last Updated:** 2026-11-18

---

# Cycle Record — Roadmap Rebalance `2026-11-18__scheduled`

Working content for STEPS 2–8.5 (STEP 0.C: one labelled section per step). `run_manifest.md`, `cycle_summary.md` and `lessons_learnt.md` are separate.

## STEP 2 — Re-Validation

**Active initiatives:** 0 (20th consecutive cycle). `initiative_register.md` has no Priority 1/2 initiative; Priority 3 — Deferred held 7 at run start (4 killed this run, DL-090). There is nothing to classify 🔥/⚠/❌.

**Strategy Proximity / CPS (2.1–2.2):** CPS = N/A (no active initiatives); prior CPS N/A (`2026-11-03__scheduled`). No delta; no absolute alert. No Strategy Drift Alert.

### Horizon Review

- **Now (§3):** held only the DL-088 programme plan, all phases shipped (v9.15–v9.17) and the close-out re-review done 2026-11-17. That subsection retires at the next `manage roadmap` (BLG-GOV-406). This run adds the v9.18 section (STEP 8.1).
- **Next (§4, Arcs 1–2):** both arcs complete; nothing to promote.
- **Later (§5, Arcs 3–6):** every remaining item is gated. **SI-02:** `**Last formally confirmed:**` 0 linked trades (condition 1 NOT MET), condition 3 last confirmed failing; cited unchanged. **Credential fallback (v9.6):** no production API credential exists in this checkout; the sandbox `DATABASE_URL` is the staging database (context only), so no live re-check was attempted and no "live re-confirmed" claim is made. PO-02/03/04 and PS-01–05 remain data-gated. No promotion.
- **Other deferred items (§5):** Full Compliance Scoring and Customisable Dashboard Layout killed (DL-090, ST-45 flags).
- **Operating mode:** backlog-driven delivery; empty Next/Later movement is expected (v9.20), and each gate was checked against current data above.

## STEP 2.4 — Product Value Ratio

| Release | U | G | D | P | Total |
|---------|---|---|---|---|-------|
| v9.13–v9.17 (pooled, changelog tags) | 66 | 21 | 95 | 4 | 186 |

`user_value_ratio` = 66 ÷ 186 = **0.355 — Advisory** (2nd consecutive Advisory reading; prior 0.307). Effort-weighted **0.448** (U 62.45 of 139.25 effort-days; coverage 186/186). Facilitator surfaces the Advisory tier in STEP 8 (below). Sustained-Advisory pull-forward (3+): not triggered. History row appended (`product_value_ratio_history.md`, DL-089).

## STEP 3 — Backlog Health Review

340 active items at run start (A 246 · T 8 · D 22 · L 64; detail in `run_manifest.md`). Tags:

- **Obsolete / superseded:** `BLG-GOV-408` resolved by this run (✅ COMPLETE written). `BLG-UX-21`'s decision half resolved (remaining scope kept).
- **Duplicates:** none found among the 340 by title; `BLG-FE-268` and `BLG-FE-309` both concern the sidebar "Docs" link (FE-268 from the v9.15 design gate, FE-309 from the re-review) — flagged for `groom backlog` to merge.
- **Priority drift:** 12 of 13 P1 items are gated Arc 5/SI-02 work unchanged since 2026-07-28 → `BLG-GOV-428` filed.
- **Quick wins ignored:** the 7 XS items in Phase 4 are now seated by the plan.
- **Debt accumulating:** ready pool 90.75 days at v9.17 (gap 62.75, 2 consecutive increases) — STEP 7.3.

### 3.1 Actionable Backlog Assessment

Structural heuristic (≥ 150 items), script-assisted. A 72.4% — no Backlog Accessibility Warning. Date-lapse re-check: 0 lapsed. Gating-item-shipped flags (13) listed in `run_manifest.md` for Release Planning §1.3a.

**STEP 8.0.5 (first firing, candidate list compile):** the Phase 4 candidate list (31 re-review items) checked against `backlog.md` — all open, none archived or `✅ COMPLETE`; `BLG-UX-08` is archived (done) and is not a candidate.

## STEP 4 — Ideas

Loaded: 27 `Submitted` rows from the full-roster window `IW-20261118-01`. 0 parked rows. Pre-clean: `ideas_housekeeping` last ran 2026-11-06 at the v9.15 closure; the v9.16 and v9.17 closures had no terminal rows to archive (at this run's start the register held no open rows, only one terminal row that housekeeping keeps by design), so it was not re-run.

### Gate-Condition Re-Check

No loaded idea has a Park Rationale, so there is nothing to re-check.

### Per-Idea Classification (PO; Facilitator verified the overlap checks; Challenger challenged each)

| Idea ID | Challenger | PO classification | Filed as |
|---------|-----------|-------------------|----------|
| IDEA-ai-compliance-20261118-01 | The re-review already has the evidence (31 calls in 102 days). Rebuttal (PO): three of the features only became reachable with v9.15–v9.17 navigation; the review keeps its full window. | ❌ Reject — not strong | — |
| IDEA-api-contracts-20261118-01 | A header nobody sees? Rebuttal: the disk cache is the one copy of the data outside the database on a shared machine. Consolidated with Cybersecurity. | 📋 Backlog (ungated) | `BLG-SEC-47` (2 ideas) |
| IDEA-backend-engineering-20261118-01 | Splits are rare in a short-hold momentum book. Rebuttal: the consequence is a false exit recommendation on a held position; detection is cheap. | 📋 Backlog (ungated) | `BLG-BE-223` (4 ideas) |
| IDEA-base44-frontend-20261118-01 | Cosmetic. Rebuttal: §14.5 design direction is adopted (DL-089); colour should carry meaning. Stage 3. | 📋 Backlog (ungated) | `BLG-FE-321` |
| IDEA-challenger-20261118-01 | (Challenger's own.) PO response: Modify — measure *during* Phase 4, shipping the measurement in its first release; stages 3–4 are provisional and revisable with data. | 📋 Backlog (ungated) | `BLG-FEAT-103` (4 ideas) |
| IDEA-challenger-20261118-02 | (Challenger's own.) PO: accepted; a decision item, not a groom action, because only the PO sets priority. | 📋 Backlog (ungated) | `BLG-GOV-428` |
| IDEA-cybersecurity-20261118-01 | Consolidated with API Contracts (same middleware). | 📋 Backlog (ungated) | `BLG-SEC-47` (2 ideas) |
| IDEA-data-model-20261118-01 | Edit the entry fields instead? Rebuttal: an adjustment row keeps the original entry auditable. Consolidated. | 📋 Backlog (ungated) | `BLG-BE-223` (4 ideas) |
| IDEA-data-model-20261118-02 | Event tracking creep. Scope limited to the two steps no table records. Consolidated. | 📋 Backlog (ungated) | `BLG-FEAT-103` (4 ideas) |
| IDEA-director-of-hr-20261118-01 | A reserve legitimises the ceremony. Rebuttal: an uncounted cost cannot be reduced or shown to fall. Consolidated with FinOps. | 📋 Backlog (ungated) | `BLG-GOV-425` (2 ideas) |
| IDEA-director-of-quality-20261118-01 | Verification reports already record them. Rebuttal: nothing trends them across releases. | 📋 Backlog (ungated) | `BLG-QA-273` |
| IDEA-financial-reporting-20261118-01 | Holding periods are weeks; dividend income is taxed separately from the CGT report and is on the broker statement. PO: accepted. | ❌ Reject — not strong | — |
| IDEA-financial-reporting-20261118-02 | The DB backup exists. Rebuttal: that is an operator artefact; the owner holds no copy. | 📋 Backlog (ungated) | `BLG-FEAT-104` |
| IDEA-finops-20261118-01 | Commit counts are a poor proxy (audit's own limits). Accepted: reported as activity, not effort. Consolidated. | 📋 Backlog (ungated) | `BLG-GOV-425` (2 ideas) |
| IDEA-frontend-specs-20261118-01 | Cosmetic. Rebuttal: columns of figures are compared by shape; stage 3 of the adopted brief. | 📋 Backlog (ungated) | `BLG-FE-322` |
| IDEA-frontend-specs-20261118-02 | Needs the `navigation.md` revision first. Accepted: dependency recorded; same release. Consolidated. | 📋 Backlog (ungated) | `BLG-FE-323` (2 ideas) |
| IDEA-head-of-engineering-20261118-01 | No reported blank-page incident. Rebuttal: the failure mode hides the exit flow; low cost. | 📋 Backlog (ungated) | `BLG-FE-324` |
| IDEA-head-of-specs-20261118-01 | Batching delays real fixes. Scope: urgent patches still apply immediately. | 📋 Backlog (ungated) | `BLG-GOV-427` |
| IDEA-head-of-ux-20261118-01 | Same as Frontend Specs -02; consolidated. | 📋 Backlog (ungated) | `BLG-FE-323` (2 ideas) |
| IDEA-infra-ops-20261118-01 | GitHub Pages is reliable. Rebuttal: the failure that matters is a bad deploy, not a Pages outage; XS. | 📋 Backlog (ungated) | `BLG-OPS-222` |
| IDEA-metrics-20261118-01 | Consolidated into the core-loop item. | 📋 Backlog (ungated) | `BLG-FEAT-103` (4 ideas) |
| IDEA-pmo-lead-20261118-01 | Fewer commits lose granularity for audit. Rebuttal: the three records are always written together. | 📋 Backlog (ungated) | `BLG-GOV-426` |
| IDEA-product-owner-20261118-01 | Overlaps `BLG-UX-15` (Weekly Digest rewrite). Kept: UX-15 rewrites the copy; this adds a measured section. Consolidated with Metrics/Data Model/Challenger. | 📋 Backlog (ungated) | `BLG-FEAT-103` (4 ideas) |
| IDEA-qa-lead-20261118-01 | Overlaps `BLG-QA-270`'s manual pass. Rebuttal: automation keeps it true afterwards. Consolidated. | 📋 Backlog (ungated) | `BLG-QA-272` (2 ideas) |
| IDEA-qa-lead-20261118-02 | Consolidated with -01 (same mobile project). | 📋 Backlog (ungated) | `BLG-QA-272` (2 ideas) |
| IDEA-qa-testing-20261118-01 | Belongs in the split fix's ACs; consolidated. | 📋 Backlog (ungated) | `BLG-BE-223` (4 ideas) |
| IDEA-strategy-owner-20261118-01 | Rule text first, or the code guesses. Consolidated as the item's first scope line. | 📋 Backlog (ungated) | `BLG-BE-223` (4 ideas) |

**Consolidations (v9.0 convention):** 6. `BLG-BE-223` (4 ideas, same mechanism), `BLG-FEAT-103` (4, same loop), `BLG-SEC-47` (2, same header), `BLG-GOV-425` (2, same ceremony measure), `BLG-FE-323` (2, same §14.2 IA change), `BLG-QA-272` (2, same mobile project). Each consolidated item's `**Source:**` lists every contributing Idea ID, and each register row names its item. The four 2-idea consolidations are below the convention's typical 3–10; each was checked for genuine overlap (same mechanism or same file), not adjacency.

**Priorities:** `BLG-BE-223` P2 (a false exit recommendation on a held position is possible, but no split has occurred); all others P3. `BLG-FEAT-103` and `BLG-FE-323` are committed in the v9.18 section; `BLG-FE-321`, `BLG-FE-322`, `BLG-QA-272` carry Provisional-Target v9.19 (Phase 4 stages 3–4).

**Idea Participation Check (4.3):** 5 roles submitted 2 net-new ideas; 17 roles submitted 1 and recorded why no further net-new idea survived (listed in the window summary). Innovation-debt note: 17 of 22 roles below the §4 minimum, up from 12 at `IW-20261016-01`. Standard mode, so this is informational; with 340 active items the overlap checks remove most second topics (see `lessons_learnt.md` Friction Item 2).

**Queue verification:** "Advancing to STEP 5" = 0; queue rows = 0. Consistent.

### Submission Details (full template fields — `IW-20261118-01`)

#### IDEA-ai-compliance-20261118-01 — Bring the AI feature usage review (BLG-GOV-382) forward from 2027-01-03 to v9.18
*Submitter:* AI Compliance & Governance Officer
- **Problem Statement:** The re-review (§11.1, §15) reports 31 AI calls in 102 days and 3 of 6 AI features never used. `BLG-GOV-382` holds the retire/keep decision until 2027-01-03, and `BLG-UX-17` (chat from a trade) waits on it. Phase 4 designs pages that host these features in the meantime.
- **Strategic Alignment:** §13.2 (AI is advisory); §3 (decision support). Unused AI surfaces still carry §13 attestation and cost.
- **Proposed Solution:** Run the `BLG-GOV-382` review in v9.18 with the evidence already gathered.
- **Expected Value:** Retire/keep decision ~6 weeks earlier; Phase 4 stage 3 designs only for kept features.
- **Effort Estimate:** XS · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks:** Backlog: refines `BLG-GOV-382` (date only). Code: n/a (process).

#### IDEA-api-contracts-20261118-01 — Declare `Cache-Control: no-store` on every API response that carries portfolio data
*Submitter:* API Contracts & Documentation Owner
- **Problem Statement:** No route sets a caching header (0 matches in `backend/`); `openapi.yaml` declares none. Clients and intermediaries may cache position and trade responses.
- **Strategic Alignment:** §2 (single-user portfolio tracker — the owner's data stays the owner's); API contract governance (CLAUDE.md §2).
- **Proposed Solution:** One middleware adds `no-store` to data routes; a shared response header in `openapi.yaml`.
- **Expected Value:** Data-route responses with `no-store`: 0% → 100%.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: no `Cache-Control` item. Code: 0 matches.

#### IDEA-backend-engineering-20261118-01 — Detect a stock split on an open position before the split-day price reads as a stop breach
*Submitter:* Backend Engineering Patterns Owner
- **Problem Statement:** `backend/` never reads split history; a held share's price halves on a 2:1 split while the stored stop and entry stay pre-split, so the stop-breach path raises an exit recommendation (`replay_service.py:8` already notes splits break price comparisons).
- **Strategic Alignment:** §5 (stops), §8 (exits) — exit signals must reflect real price movement.
- **Proposed Solution:** Nightly check of split history for held tickers; suppress breach/exit until the adjustment is confirmed; show "Split detected".
- **Expected Value:** False exit recommendations on a split day: possible today → 0.
- **Effort Estimate:** Medium · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: "stock split", "corporate action": 0. Code: no `splits` use.

#### IDEA-base44-frontend-20261118-01 — Replace the decorative gradient buttons with one solid primary button
*Submitter:* Base44 Frontend Prompt Owner · **Build-and-ship candidate** (surface `src/pages/TradeEntry.js`, 4 gradient buttons)
- **Problem Statement:** 112 `bg-gradient-to` uses across 54 files; the re-review counts 26 decorative gradient buttons and calls the UI "dashboard template, not instrument" (§15 "UI"). `BLG-FE-304` covers card surfaces only.
- **Strategic Alignment:** §3 (decision support — emphasis should signal meaning); Phase 4 brief §14.5 (DL-089).
- **Proposed Solution:** One solid primary button variant in the shared component; replace gradients.
- **Expected Value:** Decorative gradient buttons: 26 → 0.
- **Effort Estimate:** Medium · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-FE-304` (cards, not buttons); `BLG-UX-21` records the direction, builds nothing. Code: confirmed.

#### IDEA-challenger-20261118-01 — Challenge: measure whether the core loop is used before committing a second UX programme
*Submitter:* Challenger
- **Problem Statement:** The re-review's own gap analysis says "nobody knows whether the app's core loop is used" and that "every product decision since v6.2 has been made without behavioural data". Committing a 2–3 release Phase 4 repeats that.
- **Strategic Alignment:** §3 (decision support — the tool must be used to support decisions); `current_roadmap.md` §7 Decision Framework item 2 ("used daily or weekly?").
- **Proposed Solution:** Instrument the loop first; decide Phase 4 scope with a month of data.
- **Expected Value:** Phase 4 scope set against measured step completion rates rather than expert review alone.
- **Effort Estimate:** Medium · **Reversibility:** Fully reversible · **What Would You Stop?** Phase 4 stages 3–4 until measured. · **Submitter Recommendation:** Now
- **Overlap checks:** Backlog: `BLG-FEAT-92`/`30` (screener funnel, D-gated) — different steps. Code: no loop counts.

#### IDEA-challenger-20261118-02 — Challenge: 12 Arc 5 items have been P1 since 2026-07-28 while gated on data that has not moved
*Submitter:* Challenger
- **Problem Statement:** 12 of 13 P1 items (`BLG-FE-43/45/54/58/59/62/63/68/69/70/71`, `BLG-FEAT-73`) are gated on SI-02/SI-05 data unchanged since July (0 linked trades). STEP 8.0 and Release Planning read P1 as urgent.
- **Strategic Alignment:** None (score 1 — process).
- **Proposed Solution:** PO re-rates each, or keeps P1 with a dated reason.
- **Expected Value:** P1 tier meaning restored; P1 count reflects unblocked urgent work.
- **Effort Estimate:** XS · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: no re-rating item. Code: n/a.

#### IDEA-cybersecurity-20261118-01 — Portfolio and trade responses can be cached by the browser and shared machines: send no-store
*Submitter:* Cybersecurity & Trust Lead
- **Problem Statement:** With no front-end sign-in (`BLG-SEC-46`) and no caching header, cached API responses keep positions, cash and journal text on disk after the tab closes.
- **Strategic Alignment:** §2 (single-user tracker); security baseline.
- **Proposed Solution:** `Cache-Control: no-store` and `Pragma: no-cache` on data routes.
- **Expected Value:** Cached financial responses after close: possible → none.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-SEC-46` (access decision, not caching). Code: 0 matches. Second topic (`robots.txt`) dropped for overlap with `BLG-SEC-46`.

#### IDEA-data-model-20261118-01 — Record a stock split as an adjustment row against the position, not as an edit of its entry fields
*Submitter:* Data Model & Domain Schema Owner
- **Problem Statement:** No schema exists for corporate actions; editing `entry_price`/`shares` in place would destroy the audit trail behind P&L and the tax-year report.
- **Strategic Alignment:** §5 (stops), records integrity (Financial Records domain).
- **Proposed Solution:** `position_adjustments` (ratio, effective date, source, confirmed_at); readers apply it.
- **Expected Value:** Original entry preserved for 100% of adjusted positions.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: none. Code: no adjustment table.

#### IDEA-data-model-20261118-02 — Store the core-loop events the existing tables cannot derive
*Submitter:* Data Model & Domain Schema Owner
- **Problem Statement:** Signals, plans (`signal_id`), positions and reflections already record their steps; "Weekly Digest opened" and "Due today action taken" leave no record.
- **Strategic Alignment:** §3 (decision support used in practice).
- **Proposed Solution:** One small events table for those two steps only.
- **Expected Value:** All five loop steps countable per week.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: none ("usage_events", "page view": 0). Code: none.

#### IDEA-director-of-hr-20261118-01 — Reserve explicit sprint capacity for per-story ceremony instead of leaving it uncounted
*Submitter:* Director of HR
- **Problem Statement:** Audit finding 2: ~1.7 process-only commits per shipped story, outside every sprint's capacity; velocity reads 1.00 regardless.
- **Strategic Alignment:** None (score 1 — capacity process).
- **Proposed Solution:** A named ceremony reserve in `sprint_capacity.md`, sized from measurement.
- **Expected Value:** Capacity plans that include their real overhead; reduction measurable.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: "ceremony": 0. Code: n/a.

#### IDEA-director-of-quality-20261118-01 — Track escaped defects per release as a quality trend
*Submitter:* Director of Quality
- **Problem Statement:** Accepted P2 found defects (v9.16: 5; v9.17: 1) and P3 `DEV-*` are filed each release but never trended, so first-time-right work cannot show an effect.
- **Strategic Alignment:** None (score 1 — quality process).
- **Proposed Solution:** Two columns in `velocity_metrics.md`, backfilled v9.13–v9.17.
- **Expected Value:** A visible escaped-defect trend per release.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks:** Backlog/archive: no trend item. Code: n/a.

#### IDEA-financial-reporting-20261118-01 — Record dividends received on held positions so P&L and the tax-year report include them
*Submitter:* Financial Reporting & Records Owner
- **Problem Statement:** No dividend handling in `backend/` (only a replay comment); total return on UK holdings is understated.
- **Strategic Alignment:** Records integrity.
- **Proposed Solution:** A dividend entry per position; include in P&L views.
- **Expected Value:** Total-return P&L for held positions.
- **Effort Estimate:** Medium · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks:** Backlog/archive: "dividend": 0. Code: none.

#### IDEA-financial-reporting-20261118-02 — Let the owner download all their records in one file
*Submitter:* Financial Reporting & Records Owner
- **Problem Statement:** Exports cover closed trades (CSV) and the tax-year PDF only; plans, journal, reflections, open positions and settings cannot be downloaded. The DB backup is an operator artefact.
- **Strategic Alignment:** Records integrity; §2 (single-user — the owner's record).
- **Proposed Solution:** "Download all my data" in Settings: zip of CSVs plus manifest.
- **Expected Value:** Record types the owner can hold a copy of: 2 → all.
- **Effort Estimate:** Medium · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: "data export": 0. Code: `trades_export.py` (trades only).

#### IDEA-finops-20261118-01 — Count process-only commits per release alongside velocity
*Submitter:* FinOps & Resource Architect
- **Problem Statement:** The audit's commit split was a one-off; no release records it.
- **Strategic Alignment:** None (score 1).
- **Proposed Solution:** Script the split into `velocity_metrics.md` at closure.
- **Expected Value:** Per-release ceremony activity trend.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: none. Code: `generate_ci_usage_report.py` counts CI minutes, not commits.

#### IDEA-frontend-specs-20261118-01 — Use tabular (fixed-width) numerals for every price, P&L, R and % figure
*Submitter:* Frontend Specifications & UX Documentation Owner · **Build-and-ship candidate** (surface `src/pages/Positions.js`, 0 `tabular-nums`)
- **Problem Statement:** 14 uses in `src/`, none on Positions; columns of figures cannot be compared by shape and shift as prices update.
- **Strategic Alignment:** §3 (decision support — legible figures); Phase 4 brief §14.5.
- **Proposed Solution:** Tabular numerals on all numeric cells; rule in `design_system.md`.
- **Expected Value:** Pages with tabular figures: 3 components → all numeric surfaces.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: "tabular": 0. Code: confirmed.

#### IDEA-frontend-specs-20261118-02 — Move Ticker Universe from Find trades into Settings (re-review §14.2)
*Submitter:* Frontend Specifications & UX Documentation Owner · **Build-and-ship candidate** (surface `src/pages/TickerUniverse.js`)
- **Problem Statement:** Ticker Universe is configuration but sits under Find trades; the target IA (§14.2) moves it to Settings. `BLG-UX-21` notes no item builds it.
- **Strategic Alignment:** §3; Phase 4 brief §14.2 (DL-089).
- **Proposed Solution:** Move under Settings with a redirect from the old route.
- **Expected Value:** Find trades holds only trade-finding pages.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-UX-21` (decision, no build). Code: route present under Find trades.

#### IDEA-head-of-engineering-20261118-01 — Add page-level error boundaries so one failing component does not blank the whole app
*Submitter:* Head of Engineering · **Build-and-ship candidate** (surface: `src/App.js` route tree)
- **Problem Statement:** No error boundary in `src/` (0 matches); any render exception blanks the app including the sidebar and exit flow.
- **Strategic Alignment:** §8 (exits must stay reachable); reliability.
- **Proposed Solution:** Boundary per routed page inside the layout, plus one around the chat widget.
- **Expected Value:** Pages that blank on a render error: all → none.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: "ErrorBoundary", "error boundary": 0. Code: 0.

#### IDEA-head-of-specs-20261118-01 — Apply non-urgent governance prompt patches in one batch at post-ship closure
*Submitter:* Head of Specs Team
- **Problem Statement:** Audit finding 3: ~19 prompt edits per cycle, each a four-file §6 checklist; out-of-PR edits keep breaking the size budget (`BLG-GOV-421`).
- **Strategic Alignment:** None (score 1).
- **Proposed Solution:** Urgent vs batchable classification; one batch at closure.
- **Expected Value:** Non-urgent bumps per prompt per release: many → ≤ 1.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-GOV-421` (enforcement, not batching). Code: n/a.

#### IDEA-head-of-ux-20261118-01 — Make Strategy Benchmark a "Strategy vs backtest" section of Performance (re-review §14.2)
*Submitter:* Head of UX & Design · **Build-and-ship candidate** (surface `src/pages/StrategyBenchmark.js`)
- **Problem Statement:** Strategy Benchmark compares live with backtest results but is a separate entry, splitting the review journey; §14.2 places it in Performance. No item builds it.
- **Strategic Alignment:** §3; Phase 4 brief §14.2.
- **Proposed Solution:** A section of Performance reachable from its section index; redirect the old route.
- **Expected Value:** Review journey in one place; sidebar entries 19 → 18 with the Ticker Universe move.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-UX-21` (decision only). Code: separate page and route.

#### IDEA-infra-ops-20261118-01 — Poll the GitHub Pages front end as well as the API's /health
*Submitter:* Infrastructure & Operations Owner
- **Problem Statement:** `health-check-alert.yml` polls only `${API_URL}/health`; a failed or stale front-end deploy is found only when the owner opens the app.
- **Strategic Alignment:** None (score 1 — operations).
- **Proposed Solution:** Add a front-end fetch to the same workflow and alert rule.
- **Expected Value:** Front-end outage detection: none → within 45 minutes.
- **Effort Estimate:** XS · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-OPS-76` (API dependencies). Code: confirmed API-only. Second topic (restore drill) dropped as implemented.

#### IDEA-metrics-20261118-01 — Define the core-loop step metrics (signal → plan → entry → reflection → weekly review)
*Submitter:* Metrics Definitions & Analytics Owner
- **Problem Statement:** No definition exists for loop steps or completion rates; any display would invent them.
- **Strategic Alignment:** §3.
- **Proposed Solution:** Five weekly counts and four rates in `metrics_definitions.md`, with worked examples (quiet week, cross-week reflection).
- **Expected Value:** One defined basis for loop measurement.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-FEAT-31` (research-to-trade rate, T-gated) — one step only. Code: n/a.

#### IDEA-pmo-lead-20261118-01 — Write each story's routine records (state, merge-gate record, escalation mirror) in one commit
*Submitter:* PMO Lead (Head of Specs Team's "generate by script" topic merged)
- **Problem Statement:** Audit: 628 process-only commits for 360 stories; records always written together go in separate commits.
- **Strategic Alignment:** None (score 1).
- **Proposed Solution:** One combined commit per story close; a script produces the records.
- **Expected Value:** Process-only commits per story below the v9.13–v9.17 mean.
- **Effort Estimate:** Medium · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: none. Code: n/a.

#### IDEA-product-owner-20261118-01 — Show this week's loop on the Weekly Digest: signals, plans, entries, reflections
*Submitter:* Product Owner · **Build-and-ship candidate** (surface `src/pages/WeeklyDigest.js`)
- **Problem Statement:** The Weekly Digest page reports figures but not whether the week's loop happened; the re-review (§15 "Conversion") says the loop is unmeasured and the weekly review is the weakest journey.
- **Strategic Alignment:** §3 (decision support); §11 review cadence.
- **Proposed Solution:** A "This week's loop" section with five counts linking to their pages.
- **Expected Value:** The owner sees loop completion weekly; Phase 4 gets its own evidence.
- **Effort Estimate:** Medium · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks:** Backlog: `BLG-UX-15` (copy rewrite), `BLG-UX-12` (links), `BLG-FEAT-92` (screener funnel, gated) — none counts the loop. Code: no loop section.

#### IDEA-qa-lead-20261118-01 — Automated 320 px reflow check on every route
*Submitter:* QA Lead
- **Problem Statement:** Reflow at 320 px (WCAG 1.4.10) is untested; `BLG-QA-270` is a one-off manual pass.
- **Strategic Alignment:** None (score 2 — quality).
- **Proposed Solution:** A 320 × 640 Playwright project failing on horizontal scroll.
- **Expected Value:** Routes with automated reflow coverage: 0 → all.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-QA-270` (manual), `BLG-QA-255` (two components). Code: no 320 project.

#### IDEA-qa-lead-20261118-02 — Run the Telegram-link → Dashboard journey on a mobile device profile in CI
*Submitter:* QA Lead
- **Problem Statement:** The heaviest phone path (digest link → Dashboard) is the least tested (§15 "Mobile").
- **Strategic Alignment:** None (score 2).
- **Proposed Solution:** A mobile-profile spec from a deep link through to the exit dialog.
- **Expected Value:** The most common phone journey covered in CI.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog: `BLG-QA-255` (Signals/Screener only). Code: none.

#### IDEA-qa-testing-20261118-01 — Test that a split-day price does not raise a stop breach or exit recommendation
*Submitter:* QA & Testing Owner
- **Problem Statement:** No fixture covers a split; the breach path would fire.
- **Strategic Alignment:** §5, §8.
- **Proposed Solution:** Backend tests with a 2:1 split fixture (US and `.L`).
- **Expected Value:** Regression protection for split handling.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** Backlog/archive: none. Code: none.

#### IDEA-strategy-owner-20261118-01 — Define in strategy_rules.md how a stock split adjusts entry, stop, ATR and R
*Submitter:* Strategy Rules & System Intent Owner
- **Problem Statement:** `strategy_rules.md` is silent on splits; code would have to guess how R and the stop carry over.
- **Strategic Alignment:** §5 (stops), §12.3 (change control).
- **Proposed Solution:** One rule: divide prices and ATR by the ratio, multiply quantity; R unchanged.
- **Expected Value:** A canonical rule before any code.
- **Effort Estimate:** XS · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks:** `strategy_rules.md`: "split", "dividend": 0. Backlog: none.

## STEP 5 — Debate

Queue empty — no debates required. No idea was classified ✅ Advance. (The Phase 4 adoption is a backlog-programme decision recorded under STEP 8, not an initiative add; the Challenger's case against it is `IDEA-challenger-20261118-01`, answered by the PO's Modify response above.)

## STEP 6 — Scoring

No surviving STEP 5 candidates, so there is nothing to score. `claude/scoring/scored_initiatives.md` is not rewritten this run.

## STEP 7 — Workforce Economics

No in-scope initiatives, so there is no FTE load to assess. Diagnostics (detail in `workforce_capacity.md` § Rebalance 2026-11-18__scheduled):

- **§7.1 Skill-Silo:** 60.2% pooled (56/93, v9.15–v9.17). Improving (68.3% → 60.2%), above the 40% ceiling: "unresolved" under the v9.35 definition; consecutive above-ceiling readings well over 3. **Sustained-failure clause applies** (≥ 2 build-and-ship U-items), met by 7 committed U-items in the v9.18 section. Gate verification and live-status cross-check: pass.
- **§7.2:** max 10.6% raw (Head of Engineering, tied with the Head of Engineering; Head of UX & Design bucket), no advisory. Source: `role_share_history.md`, with the v9.15–v9.17 rows appended via script this run.
- **§7.3:** newest row v9.17, gap 62.75 days; increased 2 consecutive releases — advisory only (trigger at 3). Runway N/A — pool growing.
- **< 20% floor:** not applicable.

## STEP 8 — Final Rebalance Decision

**Initiatives:** ❌ Kill ×4 — Position Correlation Analysis, Backtesting Module, Full Compliance Scoring, Customisable Dashboard Layout (Priority 3 — Deferred; ST-45 sunset review flags; PO decision in session) — DL-090. No adds. Stops (4) ≥ adds (0).

**Programme decision (`BLG-UX-21`):** Product Owner adopted the re-review's §14 target state in whole as the Site Structure & Usability Phase 4 brief — DL-089.

**`BLG-GOV-408`:** both v9.15 decision records linked as inputs (`run_manifest.md`); ST-44 flagged nothing; ST-45's four flags each disposed (killed). Item marked ✅ COMPLETE.

**Governance overhead audit (2026-11-02):** its three questions are answered by filed items (`BLG-GOV-425` ceremony capacity, `BLG-GOV-426` combined records, `BLG-GOV-427` batched prompt patches); not seated in v9.18 (the PO's v9.18 focus is Phase 4 and first-time-right).

**Facilitator advisory (STEP 2.4 Advisory tier):** PVR 0.355 surfaced before decisions; the v9.18 section is 13 U of 19 committed items.

**Displacement candidate flag:** none (no active initiatives). `displacement_debt_register.md` unchanged — the four kills resolve no "Named, not yet displaced" row.

### STEP 8.0 — Production Correctness Fast-Track

13 P0/P1 items scanned; none is a correctness or security item. No promotion. Recorded in `run_manifest.md`.

### STEP 8.0.5 / 8.2 — Candidate verification

For each of the 19 items in the v9.18 section (`BLG-GOV-422`, `BLG-QA-262`, `BLG-QA-260`, `BLG-FE-294`, `BLG-SEC-46`, `BLG-FE-311`, `BLG-FE-312`, `BLG-FE-318`, `BLG-QA-271`, `BLG-UX-21`, `BLG-UX-11`, `BLG-FE-308`, `BLG-UX-15`, `BLG-UX-12`, `BLG-UX-13`, `BLG-UX-19`, `BLG-FE-320`, `BLG-FE-323`, `BLG-FEAT-103`): active in `backlog.md`, no `✅ COMPLETE`, no `RA:` marker. Prose references checked too: `BLG-UX-08` (archived — named as done, not as a candidate), `BLG-UX-17` (active, gated — named as waiting, not committed). **STEP 8.2 verification complete — 19 items verified active, 0 items excluded.**

### STEP 8.1 — Empty Now Horizon Gate

Conditions 1a (no committed non-shipped items in Now; only the shipped DL-088 programme plan) and 2 (no v9.18 section) were true at run start.

**PO decision (STEP 8.1): Option (a) — next-release section added to current_roadmap.md. Section: v9.18 — Site Structure & Usability, Phase 4 (stages 1–2) and first-time-right. Rationale:** the Product Owner adopted Phase 4 and wants v9.18 planned next with the 2026-11-12 first-time-right items; a version-labelled section with 19 committed items lets Release Planning pass §-1.2 directly.

### STEP 8.1.5 — §13-Adjacent Initiative Expiry Review

⚠ **§13-adjacent expiry:** `BLG-FEAT-55` / `BLG-SPEC-65` / `BLG-SPEC-66` have been gated on an unopened §13 chat-persistence review since 2026-07-25, more than 2 rebalance cycles. Surfaced to the Strategy Rules & System Intent Owner again. Recorded response (agent-mediated): **"still not ready, re-check next cycle"** — chat remains stateless per SRB-v1.7, and the 2027-01-03 AI usage review (`BLG-GOV-382`) decides whether chat is kept at all; opening a persistence review before that would be premature. New this cycle: `BLG-UX-17` (chat from a trade) carries a §13 re-attestation and waits on the same review — first flagged this cycle, not yet past the 2-cycle threshold.

## STEP 8.5 — Stateless Write Safety Gate

### 8.5.A — Re-anchored decisions

1. Add a v9.18 Now section (STEP 8.1 Option (a)) with 19 committed items and the Phase 4 programme plan; §1 Next planned release → v9.18 (DL-089).
2. Kill 4 Priority 3 deferred initiatives (DL-090): `initiative_register.md` moves; `current_roadmap.md` §5 rows struck through.
3. File 15 backlog items from STEP 4; set Provisional-Target v9.18 (17 existing items) and v9.19 (17 existing items) for the committed and planned Phase 4 items; record the `BLG-UX-21` decision; mark `BLG-GOV-408` ✅ COMPLETE.
4. Set 27 register rows to terminal status (25 Promoted-Backlog, 2 Rejected).
5. Append DL-089, DL-090.
6. Append history rows (PVR; role share v9.15–v9.17) and a workforce section.

### 8.5.B — Write plan

| File | Change | Traceable to |
|------|--------|--------------|
| `claude/roadmap/current_roadmap.md` | §1 Next planned release → v9.18; §3 v9.18 section + Phase 4 programme plan; §5 two kills struck through; Last Updated / Last rebalance | (A) STEP 8.1, STEP 8 kills, DL-089/090 |
| `claude/roadmap/initiative_register.md` | 4 rows Priority 3 — Deferred → Killed; Last Updated | (A) STEP 8 kills |
| `claude/backlog/backlog.md` | Append 15 items (plus `BLG-GOV-429`, the STEP 11 deferred-patch tracking item); 34 Provisional-Target updates; `BLG-UX-21` decision line; `BLG-GOV-408` ✅ COMPLETE; Last Updated | (A) STEP 4, STEP 8 |
| `claude/roadmap/decision_log.md` | Append DL-089, DL-090 (count 88 → 90, verified; prior text byte-identical) | (A) STEP 8 |
| `claude/roadmap/product_value_ratio_history.md` | Append row, refresh sparkline | (A) STEP 2.4 |
| `claude/roadmap/role_share_history.md` | Append v9.15–v9.17 rows and breakdowns; rolling line | (A) §7.2 |
| `claude/roadmap/workforce_capacity.md` | Append "Rebalance 2026-11-18__scheduled" section | (A) STEP 7 |
| `claude/ideas/ideas_register.md` | 27 rows → terminal status | (A) STEP 4.2 |
| `claude/ideas/ideas_window.json`, `window_summary_IW-20261118-01.md` | Intake window (committed separately, intake STEP 5, `3f2d36bf`) | STEP -1.6 |
| `claude/cycles/2026-11-18__scheduled/*` | run_manifest, cycle_record, cycle_summary, lessons_learnt | Process |
| `.claude_current_state.json` | Rebalance keys (STEP 12) | Process |

**Register row status verification:** no `Advancing` rows, so nothing needs a terminal status.

**BLG-ID collision advisory:** highest IDs across `backlog.md` + `backlog_archive.md` before this run: `BLG-FE-320`, `BLG-BE-222`, `BLG-QA-271`, `BLG-GOV-424`, `BLG-SEC-46`, `BLG-OPS-221`, `BLG-FEAT-102`. New IDs start at highest+1. No collision.

### 8.5.C / D — Verification

Every file in the plan is within §4 write scope. The decision log is append-only (count verified 88 → 90, 0 removed lines). No formatting-only edits. Every write traces to (A). **PASS.**

### 9.0 — Net-Zero Displacement

Additions (✅ Advance) 0; confirmed kills 4. 0 ≤ 4, **passes**. Net displacement: −4 deferred initiatives.

**Post-write checks:** `scripts/check_backlog_item_integrity.py` passes on `backlog.md` (356 items after STEP 11). No park counts exist this cycle, so the park-count grep is not applicable.
