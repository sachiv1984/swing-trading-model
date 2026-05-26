**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-25 (rebalance 2026-05-25__scheduled — DL-034 no-change; 39 backlog adds; BLG-FEAT-38 gate cleared; SI-05 phased delivery note added; CPS=2.69 Strategy Drift Alert acknowledged)
**Last rebalance:** 2026-05-25 (cycle 2026-05-25__scheduled — Standard-tier, no-change; 44 ideas from IW-20260525-01; 39 Promoted-Backlog, 11 Parked, 4 Rejected; DL-034)

> ⚠️ **Standing Notice:** This document records product intent and prioritisation thinking. All implementation detail (formulas, schemas, endpoint paths) is illustrative and indicative only. Before any feature moves to implementation, the relevant canonical specifications must be authored or updated by the appropriate domain owner. This document must not be cited as canonical intent.

-----

## 1. Current Version

**v4.0** — Arc 5 Analytics Foundation + Spec Closure + Gemini Compliance — ✅ Shipped 2026-05-25
**Next planned release:** **v4.1** — Governance Hardening, Spec Debt, Arc 5 Compliance + SI-02 Pre-Planning

<!-- roadmap-annotation-marker: RA:v4.1:2026-05-26__release-v4.1 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-05-26__release-v4.1
- Plan published: 2026-05-26
- Cycle folder: claude/cycles/2026-05-26__release-v4.1/
- Backlog slice: claude/cycles/2026-05-26__release-v4.1/stage4_backlog_slice.md
- Status at annotation: Validated

*RA:v4.0 retired — see roadmap_archive.md 2026-05-25 (post-ship closure 2026-05-22__release-v4.0).*

*RA:v3.9 retired — see roadmap_archive.md 2026-05-22 (post-ship closure 2026-05-21__release-v3.9).*
*RA:v3.8 retired — see roadmap_archive.md 2026-05-20 (post-ship closure 2026-05-19__release-v3.8).*
*RA:v3.7 retired — see roadmap_archive.md 2026-05-19 (post-ship closure 2026-05-18__release-v3.7).*
*RA:v3.6 retired — see roadmap_archive.md 2026-05-17 (post-ship closure 2026-05-16__release-v3.6).*
*RA:v3.5 retired — see roadmap_archive.md 2026-05-15 (post-ship closure 2026-05-15__release-v3.5).*
*RA:v3.4 retired — see roadmap_archive.md 2026-05-14 (post-ship closure 2026-05-14__release-v3.4).*

*RA:v3.3 retired — see roadmap_archive.md 2026-05-13.*

-----

## 2. Strategic Scope

### This system is

- A deterministic, human-in-the-loop momentum stock discovery and trading intelligence system
- A risk-managed framework built around ATR-based trailing stops and regime detection
- A single-user portfolio tracker with journalling, analytics, and strategy enforcement

### Strategic exclusions (canonical — see `docs/specs/strategy_rules.md §13`)

These are not deferred features. They are formally recorded as system boundaries in the Strategy Rules canonical spec and prevail over any planning document:

- **Not an automated trading bot.** All exits require manual confirmation.
- **Not a configurable strategy builder.** The strategy is a fixed, versioned behavioural contract.
- **Not an ML-based prediction system.** The system is explicitly deterministic.

> **Important distinction:** Deterministic screening, rules-based scoring, and structured decision support are all within §13 bounds. The boundary is prediction and automation — not intelligence or research depth.

### Product scope exclusions (deferred, not strategically excluded)

These may be revisited in future versions without any canonical spec change:

- Broker API integration (execution)
- Real-time streaming prices
- Social / community features
- Options and futures trading support

-----

## 2a. North Star

> *A momentum stock discovery and trading intelligence system that finds candidates matching your strategy, validates and plans entries with discipline, manages open positions with structured prompts, enforces your own rules back to you, and compounds every trade into a continuously improving edge — without ever making a decision for you.*

The system’s current foundation — trade tracking, analytics, risk monitoring, signals, alerts, watchlists, and market correlation — is strong. What it lacks is the front of the funnel: a systematic way to find stocks worth watching in the first place, and a coherent flow from discovery through to a confirmed, planned entry.

The roadmap beyond v2.8 is organised around **six named arcs**. Each arc has a purpose, a defined end state, and a sequencing rationale. Features belong to an arc. Arcs are sequenced intentionally. The arcs are not six separate products — they are six layers of the same system, each one building on the last.

-----

## 2b. The Six Arcs — Overview

|Arc      |Theme                        |Horizon  |One-line purpose                                                                    |
|---------|-----------------------------|---------|------------------------------------------------------------------------------------|
|**Arc 1**|Stock Discovery & Screening  |v2.9–v3.1|Find momentum candidates that match your strategy rules today                       |
|**Arc 2**|Pre-Trade Research & Planning|v3.1–v3.3|Validate a candidate, build a structured trade plan, confirm the entry              |
|**Arc 3**|In-Trade Risk Management     |v3.3–v3.5|Active position lifecycle management with structured human-confirmed prompts        |
|**Arc 4**|Post-Trade Intelligence      |v3.5–v3.8|Journal, plan vs reality analysis, AI pattern recognition across your trade history |
|**Arc 5**|Strategy Integrity           |v3.8–v4.0|Enforce your own rules at entry, detect behavioural drift, validate strategy changes|
|**Arc 6**|Performance Science          |v4.0+    |Edge analysis, regime-conditional performance, Monte Carlo, strategy decay detection|


> **Arc 5 runs partially in parallel with Arc 3.** Some Strategy Integrity features (pre-entry rule validation, compliance gate) are high-value earlier than the full sequence implies and will be reviewed for pull-forward at Arc 3 planning.

-----

## 2c. The Six Arcs — Detail

-----

### Arc 1 — Stock Discovery & Screening (v2.9–v3.1)

**Purpose:** Build the front of the funnel. The system knows your strategy rules — ATR multipliers, regime gate, grace period logic, position sizing constraints. It should be able to apply those rules as a deterministic screen across a universe of stocks and surface candidates that *currently meet your entry conditions*. This is not prediction. It is your own rules applied systematically to market data.

Today you find stocks through external research and add them to the watchlist manually. Arc 1 inverts that: the system finds candidates and surfaces them for your review.

**Why first:** Everything downstream — research, planning, position management, learning — depends on having good candidates in the funnel. A great trade management system that starts with poor candidate selection is solving the wrong problem.

**§13 compliance:** Deterministic screening against fixed, versioned strategy rules is fully compliant. The system applies your rules; it does not generate predictions or adaptive signals. Every screen result is reproducible and auditable.

**Data sources:**

- Yahoo Finance — price history, ATR, 200-day MA, sector/industry classification, earnings calendar
- Alpaca Markets API — higher-quality OHLCV bars for US tickers (replaces Yahoo for US market leg); Alpaca News API for ticker-level news context (display-only, no sentiment scoring)
- Existing signals endpoint — momentum signal integration for screened candidates

**Features:**

|ID   |Feature                          |Effort|Notes                                                                                                                                                                                           |
|-----|---------------------------------|------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|DS-01|Strategy-Rules Screener Engine   |H     |Backend screening engine applying §11 parameters as deterministic filters across a configurable ticker universe; UK (.L) and US markets; results ranked by signal strength, not predicted return|
|DS-02|Screener Results Page            |M     |Frontend view of screener output — ticker, market, ATR, regime status, signal score, sector, proximity to entry zone                                                                            |
|DS-03|Sector & Industry Classification |S     |Yahoo Finance sector/industry data enrichment on all screened tickers and open positions; feeds Arc 1 concentration awareness                                                                   |
|DS-04|Earnings Calendar Integration    |M     |Upcoming earnings dates surfaced on screener results, watchlist, and open positions; data-agnostic source (Yahoo Finance default)                                                               |
|DS-05|Alpaca US Market Data Integration|M     |Replace Yahoo Finance for US ticker OHLCV data; higher quality bars for ATR calculation and signal generation; scoped to US market leg only                                                     |
|DS-06|Alpaca News Panel                |S     |Ticker-level news context panel (display-only; count + headlines; no sentiment scoring); surfaces on screener results and watchlist; §13 COMPLIANT — read-only context                          |
|DS-07|Watchlist Promotion Flow         |S     |One-click promotion from screener result to watchlist; screener becomes the primary watchlist input mechanism                                                                                   |

**End state:** You open the screener each morning and see a ranked list of momentum candidates that pass your strategy’s regime gate, ATR filter, and signal conditions — right now, today. You promote interesting ones to the watchlist for deeper research in Arc 2.

-----

### Arc 2 — Pre-Trade Research & Planning (v3.1–v3.3)

**Purpose:** Transform the watchlist from a passive list into an active research and planning surface. For each watchlisted candidate, Arc 2 provides the context needed to make a high-quality entry decision, then captures that decision as a structured **trade plan** — a first-class object that links to the position and becomes the basis for post-trade learning.

**Why sequenced after Arc 1:** Research and planning is only valuable when candidates are good. Arc 1 ensures the watchlist contains strategy-compliant candidates. Arc 2 provides the tools to choose between them and commit with discipline.

**Features:**

|ID   |Feature                  |Effort|Notes                                                                                                                                                                                                                                                   |
|-----|-------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|PT-01|Trade Plan Object        |M     |New data model: trade plan linked to position at entry. Fields: setup thesis, entry rationale, regime context at entry, R target, early exit conditions, confirmation criteria. Becomes the comparison object for Arc 4 plan vs reality analysis        |
|PT-02|Pre-Trade Research View  |M     |Unified per-ticker research surface: signal strength, market correlation (v2.7 backend), regime status, sector context, earnings proximity, Alpaca news panel, prospective heat. Single view — no tab-switching                                         |
|PT-03|Prospective Heat at Entry|S     |`GET /portfolio/prospective-heat` shipped v2.0 (BLG-BE-02); surface within Pre-Trade Research View and Trade Plan flow — frontend integration only                                                                                                      |
|PT-04|Setup Quality Score      |M     |Deterministic score (0–100) against your own historical win conditions: when you have entered with these regime/signal/ATR conditions before, your win rate was X. No ML. Calculated from your own trade history. Gate: 20+ closed trades               |
|PT-05|Pre-Trade Entry Checklist|M     |Structured checklist embedded in Trade Plan flow — regime gate, signal confirmation, position sizing, heat impact, earnings proximity, sector concentration. All items deterministic and rules-based. Checklist completion recorded on trade plan object|

**End state:** For any watchlisted candidate, you can open a single research view, review all relevant context, complete a structured checklist, capture your thesis and R target in a trade plan, and enter the position — with the full plan saved and linked. The quality of that entry decision is now measurable, not assumed.

-----

### Arc 3 — In-Trade Risk Management (v3.3–v3.5)

**Purpose:** Evolve risk management from passive monitoring to active, timely, structured prompts. The Risk Dashboard (v1.8) shows what is happening. Arc 3 tells you what to do about it — at the right moment, in the right form, without making the decision for you.

**Why sequenced after Arc 2:** Position management prompts are more useful when entry quality is known. The stop management workflow, for example, is more meaningful when you can compare current position state against the original trade plan.

**Features:**

|ID   |Feature                         |Effort|Notes                                                                                                                                                                                                                                                                              |
|-----|--------------------------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|IT-01|Position Lifecycle Manager      |M     |Explicit position state machine surfaced in UI — GRACE → LOSING → PROFITABLE → EXIT ZONE. Current state visible on positions page with days in state and next state trigger. Replaces implicit state inference with explicit display                                               |
|IT-02|Grace Period Decision Support   |S     |Structured prompt at grace period day 8 — “this position exits grace in 2 days; review thesis.” Links to original trade plan. Human-confirmed, not automated                                                                                                                       |
|IT-03|Stop Management Workflow        |M     |Guided ATR trail step — shows current stop, new calculated stop, difference in R terms. Structured manual confirmation required. Uses stop price join (shipped v2.4). §13 COMPLIANT — recommendation only                                                                          |
|IT-04|Drawdown-Triggered Review Prompt|M     |Structured portfolio review prompt when drawdown exceeds user-defined threshold (default: 10%). Surfaces open positions by state, portfolio heat, and regime status. Human-in-loop — no automated action                                                                           |
|IT-05|Position Concentration Limits   |S     |Warning when single-position heat exceeds configurable % of portfolio or sector concentration exceeds threshold (feeds from DS-03 sector data). Uses existing heat calculation                                                                                                     |
|IT-06|Alpaca Paper Trading Integration|H     |US market positions mirrored to Alpaca paper account for tracking against real market conditions without real capital. Enables hypothetical position tracking and future lightweight backtesting foundation. Scoped: US market only. Gate: §13 review required before pre-alignment|

**End state:** Every open position has a visible lifecycle state. The system surfaces the right prompt at the right moment — grace period expiry, stop trail opportunity, drawdown threshold, concentration breach — and you confirm or dismiss each one. Nothing happens automatically. Every decision is yours, made with full context.

> **v3.3 partial delivery (2026-05-13):** IT-01 backend (position_lifecycle_service.py, DS-05 migration, enriched GET /positions, POST /positions/{id}/refresh-state), IT-02 backend (GET /positions/grace-period-alerts), and IT-03 backend (GET /positions/{id}/stop-trail) shipped. Frontend display for IT-01/02/03 (ST-03, ST-05, ST-07) deferred to v3.4. IT-04, IT-05, IT-06 remained planned.
>
> **v3.4 delivery (2026-05-14):** IT-01 frontend (LifecycleBadge), IT-02 frontend (GracePeriodAlertZone), IT-03 frontend (TrailStopModal), IT-04 backend+frontend (DrawdownReviewPrompt), IT-05 backend+frontend (ConcentrationLimitsWarning) — all shipped. IT-06 (Alpaca paper trading) deferred to v3.5+. **Arc 3 features IT-01 through IT-05 ✅ Complete.**
>
> **v3.5 delivery (2026-05-15):** IT-06 §13 review PASS (Strategy Rules & System Intent Owner, 4 binding conditions); alpaca_paper_sync_service.py + GET /portfolio/paper-positions backend; PaperAccountPanel frontend on Positions page; 5 Playwright scenarios pass. **Arc 3 ✅ Fully Complete — all six features IT-01 through IT-06 shipped (v3.3–v3.5).**

-----

### Arc 4 — Post-Trade Intelligence (v3.5–v3.8)

**Purpose:** Close the feedback loop. Arc 4 takes the trade plan (Arc 2), the position lifecycle data (Arc 3), the journal entries, and the AI summarisation (v2.8) and turns them into structured, compounding learning. The central concept is **plan vs reality** — not just “how did I feel about this trade” but “did reality match the plan I wrote before entry, and if not, why not?”

**Why last in the post-trade sequence:** This arc requires data density. AI Journal Summarisation (v2.8) must be live and used. Trade plans (Arc 2) must exist to compare against. Position lifecycle data (Arc 3) must be captured. The foundation is built in Arcs 1–3; Arc 4 mines it.

**Features:**

|ID   |Feature                         |Effort|Notes                                                                                                                                                                                                                                                           |
|-----|--------------------------------|------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|PO-01|Plan vs Reality Analysis        |H     |✅ Shipped v3.5–v3.6 — arc4_data_requirements.md v1.0 + plan_vs_reality_service + GET /trades/{id}/plan-vs-reality + PlanVsReality component (v3.5); planned_entry_price snapshot at trade entry + entry_delta_pct display in PlanVsReality (v3.6) — **Arc 4 PO-01 fully complete**|
|PO-02|Journal Pattern Recognition     |H     |Cross-entry AI analysis: recurring themes, emotional patterns, setup types, conditions present at winning vs losing entries. Requires 6+ months of AI-summarised journal entries (BLG-FEAT-16 must be live and actively used)                                   |
|PO-03|Behavioural Error Taxonomy      |M     |Auto-classify journal entries and plan vs reality deviations by error type (entry too early, held too long, sized incorrectly, ignored regime, etc.). Track frequency over time. Feeds Arc 5 drift detection                                                    |
|PO-04|Reflection ↔ Outcome Correlation|H     |Does journal depth correlate with trade quality? Does plan completion score predict win rate? Requires PO-01 and PO-02 data foundation; gate: 50+ trades with plans                                                                                             |
|PO-05|Lightweight Replay Mode         |VH    |Replay historical signals against your own strategy rules on your own trade history. Not a full backtester — a replay of what the system would have signalled, compared to what you actually did. Requires Alpaca paper trading foundation (IT-06) for US market|

**End state:** Every closed trade produces a structured plan vs reality comparison. Over time, the system surfaces your recurring errors, your strongest setup conditions, and the gap between your written strategy and your actual behaviour. Learning is systematic, not accidental.

> **v3.6 delivery (2026-05-17):** planned_entry_price snapshot at trade exit; entry_delta_pct computed and surfaced in PlanVsReality component (SC-PVR-03/04/05). **PO-01 Plan vs Reality Analysis fully complete (v3.5 + v3.6).**

-----

### Arc 5 — Strategy Integrity (v3.8–v4.0)

**Purpose:** The system knows your rules. Arc 5 makes it enforce them — not by blocking you, but by making every deviation visible, deliberate, and recorded. This is the arc that separates a tracking tool from a genuine trading intelligence platform.

**Why sequenced here:** Strategy Integrity requires the full data model established by Arcs 1–4 — trade plans, lifecycle data, journal patterns, behavioural error taxonomy. Without that foundation, integrity checking is shallow. With it, the system can compare your actual behaviour against your stated rules with precision.

> **Note:** SI-01 (Pre-Entry Rule Validation Gate) and SI-03 (Red Flag Journal) are high-value earlier than this sequence implies. Both are candidates for pull-forward into Arc 3 releases and will be reviewed at Arc 3 planning.

**Features:**

|ID   |Feature                         |Effort|Notes                                                                                                                                                                                                                                                                                                       |
|-----|--------------------------------|------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|SI-01|Pre-Entry Rule Validation Gate  |M     |✅ Shipped v3.8 (2026-05-20) — §13 PASS (ST-01); strategy_rules.md v1.4 §4.2 formalised 5 checks; GET /portfolio/pre-entry-validation + PreEntryValidationPanel with override acknowledgement; 17 unit tests + SC-TP-17–20 Playwright pass|
|SI-02|Behavioural Drift Detection     |H     |Rolling analysis: are your actual entries drifting from your stated setup criteria? Are you entering earlier in the signal cycle than your rules permit? Are you sizing up in losing streaks? Detected from trade history and trade plan data                                                               |
|SI-03|Red Flag Journal                |M     |✅ Shipped v3.9 (2026-05-22) — red_flag_events table; GET /portfolio/red-flag-journal (paginated, filterable); SI-01 override event write path; RedFlagJournal.js frontend with filters, pagination, empty state, Trading nav link; SC-RFJ-01/02/03 Playwright pass|
|SI-04|Strategy Version Comparison     |H     |When `strategy_rules.md` is incremented, the system compares trade history performance before and after the change. Did the parameter update actually improve outcomes? Requires version-tagged trade history                                                                                               |
|SI-05|Weekly Strategy Integrity Digest|M     |Combines Red Flag Journal (SI-03), behavioural drift signals (SI-02), and compliance score trend into a single weekly review. Delivered via existing Telegram notification infrastructure (shipped v2.4). **Phased delivery (BLG-GOV-54):** Phase 1 = Red Flag summary + compliance score trend via Telegram (no SI-02 component); Phase 2 = SI-02 drift signal integration. SI-05 remains Next horizon until Phase 2 ships.|

**End state:** Your written strategy and your actual behaviour converge over time — not because the system forces you, but because every deviation is visible, recorded, and reviewed. The gap between the trader you intend to be and the trader you are becomes measurable and shrinkable.

> **v4.0 delivery (2026-05-25):** Arc 5 compliance analytics layer shipped — GET /analytics/arc5-compliance (validation_pass_rate_by_rule, events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate); Arc5ComplianceSection.js on PerformanceAnalytics; SI-01→SI-03 Playwright integration suite (8 scenarios). Also shipped: Gemini Flash base wiring (POST /trade-plans/{plan_id}/generate-thesis), gemini_audit_log, cost tracking, CI/CD staging auto-deploy, starlette CVE remediation, ticker symbol validation, red flag endpoint security review. EPIC-04 PT-04 conditional deferred (gate not met — <20 closed trades, 4th deferral).

-----

### Arc 6 — Performance Science (v4.0+)

**Purpose:** Understand the system as a whole. Arc 6 answers the questions that matter most over a long trading horizon: does this strategy have a genuine edge, where does that edge come from, under what conditions does it perform best, and is it eroding?

**Why last:** Arc 6 requires substantial trade history (100+ trades with plans, lifecycle data, and journal entries) and the full analytical foundation built by Arcs 1–5. It is the highest-value arc for a trader with 2+ years of data. It is not meaningful before then.

**Features:**

|ID   |Feature                       |Effort|Notes                                                                                                                                                                                                                                                               |
|-----|------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|PS-01|Edge Analysis Dashboard       |H     |Positive expectancy confirmation: win rate, average R, expectancy per trade, profit factor — broken down by market, sector, regime, and setup type. Answers: where does my edge actually come from?                                                                 |
|PS-02|Regime-Conditional Performance|M     |Win rate, average R, and expectancy broken down by regime at entry — trending vs choppy, high-VIX vs low-VIX. Tells you when to press and when to reduce size. Gate: 50+ trades with regime-at-entry captured (Arc 2)                                               |
|PS-03|Monte Carlo Simulation        |M     |Given your actual trade distribution, what is the realistic range of outcomes over the next 50 and 100 trades? Not prediction — statistical context for drawdown psychology and position sizing decisions. Deterministic simulation, §13 COMPLIANT. Gate: 50+ trades|
|PS-04|Strategy Decay Detection      |H     |Rolling window expectancy analysis: is your edge getting smaller over time? Flags statistical divergence from your own historical baseline — not from an external benchmark. Gate: 18+ months of trade history                                                      |
|PS-05|Personal Benchmark Comparison |S     |Compare current period performance against your own best periods. “You are currently performing in the bottom quartile of your own history” is more actionable than any index comparison. Gate: 12+ months of history                                               |

**End state:** You have a rigorous, data-driven answer to the question every systematic trader eventually asks: *does this actually work, and is it still working?* Not based on feeling — based on your own data, your own rules, and statistical analysis of both.

-----

## 3. Delivery Plan — Horizon: Now

*v4.0 shipped 2026-05-25 (Verified). RA:v4.0 annotation retired (post-ship closure 2026-05-22__release-v4.0).*
*v2.5 shipped 2026-04-10 (Verified_with_deviations). RA:v2.5 annotation retired to roadmap_archive.md 2026-04-10.*
*v2.6 shipped 2026-04-11 (Verified). RA:v2.6 annotation retired 2026-04-16 (post-ship closure v2.7 — v2.6 closure was not run standalone).*
*v2.7 shipped 2026-04-16 (Verified). RA:v2.7 annotation retired to roadmap_archive.md 2026-04-16 (post-ship closure v2.7).*
*v2.8 shipped 2026-04-20 (Verified). RA:v2.8 annotation retired to roadmap_archive.md 2026-04-20 (post-ship closure v2.8).*
*v2.9 shipped 2026-04-24 (Verified_with_deviations). RA:v2.9 annotation retired to roadmap_archive.md 2026-04-28 (post-ship closure v3.0).*
*v3.0 shipped 2026-04-27 (Verified). RA:v3.0 annotation retired to roadmap_archive.md 2026-04-28 (post-ship closure v3.0).*
*v3.1 shipped 2026-05-05 (Verified). RA:v3.1 annotation retired to roadmap_archive.md 2026-05-05 (post-ship closure v3.1).*
*v3.2 shipped 2026-05-08 (Verified). RA:v3.2 annotation retired to roadmap_archive.md 2026-05-08 (post-ship closure v3.2).*

-----

## 4. Priority 2 — Horizon: Next Phase (Arcs 1 & 2)

Items in this section are sequenced and ready for planning when the current version closes. They are not gated — they are next.

### Arc 1 — Stock Discovery & Screening (v2.9–v3.1)

**Status (2026-05-05):** Complete. DS-03, DS-05, DS-06 (watchlist) delivered v2.9. DS-01, DS-02, DS-06 (screener), DS-07 delivered v3.0. **DS-04 (Earnings Calendar) delivered v3.1 — Arc 1 fully complete.**

|Feature                          |ID   |Effort|Status                                                                                                                |
|---------------------------------|-----|------|----------------------------------------------------------------------------------------------------------------------|
|Sector & Industry Classification |DS-03|S     |✅ Shipped v2.9                                                                                                       |
|Alpaca US Market Data Integration|DS-05|M     |✅ Shipped v2.9                                                                                                       |
|Strategy-Rules Screener Engine   |DS-01|H     |✅ Shipped v3.0                                                                                                       |
|Screener Results Page            |DS-02|M     |✅ Shipped v3.0                                                                                                       |
|Alpaca News Panel                |DS-06|S     |✅ Shipped v3.0 (watchlist v2.9; screener results v3.0 ST-07)                                                        |
|Watchlist Promotion Flow         |DS-07|S     |✅ Shipped v3.0                                                                                                       |
|Earnings Calendar Integration    |DS-04|M     |✅ Shipped v3.1                                                                                                       |

**Arc 1 end-state target achieved (2026-04-27):** Each morning the screener surfaces a ranked list of momentum candidates that pass your strategy’s regime gate, ATR filter, and signal conditions. You review, promote to watchlist, and move to Arc 2 research. The top of the funnel is systematic, not ad hoc. DS-04 (earnings calendar) remains as v3.1 enhancement.

*RA:v2.9 retired — see roadmap_archive.md 2026-04-28.*

### Arc 2 — Pre-Trade Research & Planning (v3.1–v3.3)

**Sequencing note:** PT-01 (Trade Plan Object) is a data model change and must be delivered first — it is the foundation for all other Arc 2 items and all of Arc 4.

|Feature                  |ID   |Effort|Sequencing note                                                                                      |
|-------------------------|-----|------|-----------------------------------------------------------------------------------------------------|
|Trade Plan Object        |PT-01|M     |✅ Shipped v3.1 — data model, backend CRUD, frontend creation/edit/view flow                         |
|Pre-Trade Research View  |PT-02|M     |✅ Shipped v3.2 — frontend delivered (research page, ticker data, news, nav integration)             |
|Prospective Heat at Entry|PT-03|S     |✅ Shipped v3.2 — prospective heat metric integrated into research view                             |
|Pre-Trade Entry Checklist|PT-05|M     |✅ Shipped v3.2 — checklist component in Trade Plan form, pre-population, persistence               |
|Setup Quality Score      |PT-04|M     |Deterministic score from own trade history; gate: 20+ closed trades; depends on PT-01 — ⏸️ Parked (v3.6/v3.7/v3.8/v3.9/v4.0 conditional defers — 5 consecutive cycles; gate not met; PO decision 2026-05-19 to park formally — re-open when 20+ closed trades confirmed; PO written rationale required at v4.1 sprint planning per verification_report.md §5(c))|

**Arc 2 end-state target:** Every entry is preceded by a structured research view, a completed checklist, and a saved trade plan. The quality of entry decisions is captured and measurable, not assumed.

-----

## 5. Priority 3 — Horizon: Later (Arcs 3–6)

### Arc 3 — In-Trade Risk Management (v3.3–v3.5)

**Status (2026-05-15):** IT-01 through IT-05 complete (v3.3–v3.4). IT-06 (Alpaca Paper Trading) ✅ Complete v3.5.

|Feature                         |ID   |Effort|Status / Notes                                                                              |
|--------------------------------|-----|------|--------------------------------------------------------------------------------------------|
|Position Lifecycle Manager      |IT-01|M     |✅ Shipped v3.3 (backend) + v3.4 (frontend)                                                 |
|Grace Period Decision Support   |IT-02|S     |✅ Shipped v3.3 (backend) + v3.4 (frontend)                                                 |
|Stop Management Workflow        |IT-03|M     |✅ Shipped v3.3 (backend) + v3.4 (frontend)                                                 |
|Drawdown-Triggered Review Prompt|IT-04|M     |✅ Shipped v3.4 (backend + frontend)                                                        |
|Position Concentration Limits   |IT-05|S     |✅ Shipped v3.4 (backend + frontend)                                                        |
|Alpaca Paper Trading Integration|IT-06|H     |✅ Shipped v3.5 (2026-05-15) — §13 PASS; US positions mirrored to Alpaca paper account; GET /portfolio/paper-positions; PaperAccountPanel frontend; foundational for PO-05 replay mode|


> **§13 note:** IT-01 through IT-05 are structured prompts requiring human confirmation — fully §13 COMPLIANT. IT-06 §13 review complete — PASS (2026-05-15); four binding conditions recorded in decisions document.

### Arc 4 — Post-Trade Intelligence (v3.5–v3.8)

|Feature                         |ID   |Effort|Gate / pre-condition                                                                           |
|--------------------------------|-----|------|-----------------------------------------------------------------------------------------------|
|Plan vs Reality Analysis        |PO-01|H     |✅ Shipped v3.5 (2026-05-15) — foundation: arc4_data_requirements.md + plan_vs_reality_service + GET /trades/{id}/plan-vs-reality + PlanVsReality frontend; entry_delta_pct deferred to Arc 4 (planned_entry_price not yet snapshotted)|
|Journal Pattern Recognition     |PO-02|H     |Requires 6+ months of AI-summarised journal entries (BLG-FEAT-16 live and actively used)       |
|Behavioural Error Taxonomy      |PO-03|M     |Requires PO-01 and PO-02 data; complements Arc 5 drift detection                               |
|Reflection ↔ Outcome Correlation|PO-04|H     |Requires PO-01 + PO-02; gate: 50+ trades with plans                                            |
|Lightweight Replay Mode         |PO-05|VH    |Requires IT-06 (Alpaca paper trading) for US market; highest-value long-term validation feature|

### Arc 5 — Strategy Integrity (v3.8–v4.0)

|Feature                         |ID   |Effort|Gate / pre-condition                                                                |
|--------------------------------|-----|------|------------------------------------------------------------------------------------|
|Pre-Entry Rule Validation Gate  |SI-01|M     |✅ Shipped v3.8 (2026-05-20)                                                        |
|Behavioural Drift Detection     |SI-02|H     |Requires PO-01 + PO-03 data foundation                                              |
|Red Flag Journal                |SI-03|M     |✅ Shipped v3.9 (2026-05-22)                                                        |
|Strategy Version Comparison     |SI-04|H     |Requires version-tagged trade history from Arc 2 onwards                            |
|Weekly Strategy Integrity Digest|SI-05|M     |Extends existing Telegram digest (shipped v2.4); depends on SI-02 + SI-03           |

### Arc 6 — Performance Science (v4.0+)

|Feature                       |ID   |Effort|Gate / pre-condition                                      |
|------------------------------|-----|------|----------------------------------------------------------|
|Edge Analysis Dashboard       |PS-01|H     |Gate: 100+ trades with plans and lifecycle data           |
|Regime-Conditional Performance|PS-02|M     |Gate: 50+ trades; requires regime-at-entry capture (Arc 2)|
|Monte Carlo Simulation        |PS-03|M     |Gate: 50+ trades; deterministic simulation, §13 COMPLIANT |
|Strategy Decay Detection      |PS-04|H     |Gate: 18+ months of trade history                         |
|Personal Benchmark Comparison |PS-05|S     |Gate: 12+ months of history                               |

### Other deferred items

|Feature                                  |Effort|Rationale for deferral                                                                      |
|-----------------------------------------|------|--------------------------------------------------------------------------------------------|
|Multi-Portfolio Support                  |H     |Low value at current scale                                                                  |
|Mobile App                               |VH    |Web experience sufficient                                                                   |
|Full Compliance Scoring                  |H     |Lightweight version shipped v1.9; Arc 5 SI-01 supersedes this                               |
|BLG-TECH-05 — Prometheus metrics endpoint|L–M   |Defer until operational need or multi-user                                                  |
|Customisable Dashboard Layout            |H     |High build cost, low current priority; defer indefinitely at current scale                  |
*BLG-GOV-08 — Engine prompt compression — ❌ Retired 2026-05-13 (DL-026): 9+ consecutive deferrals; primary value delivered by roadmap_prompt.md v6.0 refactor (AUD-2026-05-13). Archived in backlog_archive.md.*

-----

## 6. Gated Features — Awaiting Pre-Conditions

|Feature                     |Gate condition                                                                                                                  |Gate owner                          |Status                                                                                                                                                    |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
|Alpaca Paper Trading (IT-06)|§13 review — paper trading touches execution infrastructure; must confirm it does not constitute an automated trading capability|Strategy Rules owner                |✅ Gate cleared — §13 PASS determination 2026-05-15 (ST-01; four binding conditions documented; IT-06 shipped v3.5)                                       |

-----

## 7. Decision Framework

When evaluating new features:

1. Does it help find better stocks or make better trading decisions?
1. Will it be used daily or weekly?
1. Can it be implemented in under a week?
1. Does it require external dependencies, and are those dependencies resilient?
1. Does it conflict with system boundaries in `strategy_rules.md §13`? If yes, do not proceed without a canonical spec change.
1. Is it deterministic and rules-based, or does it involve prediction or adaptive logic? Prediction and adaptive logic are outside §13 bounds. Deterministic screening and rules-based scoring are within bounds.
1. Does it belong to one of the six strategic arcs? If not, articulate why it is additive rather than distracting from the North Star.
1. Does it require pre-work (data model changes, canonical updates, decision records, external API integrations) that is not yet complete? If yes, add the pre-work as an explicit roadmap item before the feature.

-----

## 8. Release Summary

|Release      |Theme                                                                 |Key deliveries                                                                                                                            |
|-------------|----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
|**v1.5**     |Performance Analytics                                                 |Unified analytics endpoint, validation endpoint — ✅ Shipped *(retired to archive 2026-03-15)*                                             |
|**v1.6**     |Position Sizing                                                       |Calculator, settings default risk % — ✅ Shipped                                                                                           |
|**v1.6.1**   |Correctness & Quick Wins                                              |Quick Wins Bundle (6 features) — ✅ Shipped 2026-03-01                                                                                     |
|**v1.7**     |Foundation                                                            |CI/CD gate, §13 boundary review, metrics definitions, observability, API versioning decision — ✅ Shipped 2026-03-03                       |
|**v1.8**     |Risk Dashboard                                                        |Full risk page — heat, drawdown, grace period, position-level risk — ✅ Shipped 2026-03-06                                                 |
|**v1.9**     |User Value & Insight                                                  |Structured Trade Reflection, Cohort Analysis, Dashboard Homepage, Compliance Metrics — ✅ Shipped 2026-03-13                               |
|**v1.10**    |Operations & Quality                                                  |Staging environment, CI/CD auto-deploy, CohortAnalysis refactor, integration tests — ✅ Shipped 2026-03-16                                 |
|**v2.0**     |Reporting & Alerts                                                    |Tax-year P&L statement, signal exposure controls (top_n, lookback_days), prospective heat endpoint — ✅ Shipped 2026-03-17                 |
|**v2.1**     |Alerts, Watchlists & Enhancements                                     |ADR-003, Alerts & Notifications (Telegram), Watchlists & Screening, Chart Interactivity — ✅ Shipped 2026-03-21                            |
|**v2.2**     |Security, Alert Maturity & Quality                                    |API Key Auth, CSP, alert scheduling, thresholds, history — ✅ Shipped 2026-03-24                                                           |
|**v2.3**     |Quality Automation & User Insight                                     |Strategy Compliance Panel, Metrics Staleness Indicator, QA automation — ✅ Shipped 2026-03-30                                              |
|**v2.4**     |Correctness, Insight & Governance Hardening                           |ATR fix, alert deduplication, stop price join, P&L GBP column, weekly digest — ✅ Shipped 2026-04-03                                       |
|**v2.5**     |Integration Baseline, Quick Wins & Governance Debt                    |System Status (26 endpoints), Fee Drag % metric, governance patches — ✅ Shipped 2026-04-10                                                |
|**v2.6**     |Backend Integration Completion, Test Automation & Governance Hardening|Playwright fix, System Status spec, audit, Spec Dependency Map — ✅ Shipped 2026-04-11                                                     |
|**v2.7**     |Performance, Governance Hardening & Market Intelligence               |Supavisor pooling, portfolio DB refactor, market correlation API, supplementary signal indicators — ✅ Shipped 2026-04-16                  |
|**v2.8**     |Frontend Completion, Test Quality & AI Journal Feature                |Market Correlation frontend, test coverage, governance patches, AI Journal Summarisation (Arc 4 foundation) — ✅ Shipped 2026-04-20        |
|**v2.9**     |Arc 1 Foundation: Stock Discovery & Screening Spec & Infrastructure   |Arc 1 specs (BLG-SPEC-21/22/23, BLG-FE-17), DS-03 sector enrichment, DS-05 Alpaca US data, DS-06 news panel (watchlist), CI mock harness, governance debt — ✅ Shipped 2026-04-24|
|**v3.0**     |Arc 1 Screener Engine & Results Page                                  |DS-01 screener engine, DS-02 screener results page, DS-06 news panel (BLG-FE-18 resolved), DS-07 watchlist promotion, keyboard shortcuts, health extension, AI metrics, streak metric — ✅ Shipped 2026-04-27 — cycle: 2026-04-25__release-v3.0|

*RA:v3.0 retired — see roadmap_archive.md 2026-04-28.*

|**v3.1**     |Arc 2 Trade Plan Foundation                                           |PT-01 Trade Plan Object (full), PT-02 Pre-Trade Research View (backend), DS-04 Earnings Calendar, BLG-FE-20 UK screener fix, BLG-QA-10/11 screener QA docs, BLG-FEAT-19 Monthly P&L report, security docs, CF-01/CF-02 governance patches — ✅ Shipped 2026-05-05 — cycle: 2026-04-29__release-v3.1|

*RA:v3.1 retired — see roadmap_archive.md 2026-05-05.*

|**v3.1–v3.2** ✅|Arc 2: Pre-Trade Research & Planning (partial)                       |PT-01 (v3.1), PT-02 + PT-03 + PT-05 (v3.2) — ✅ Complete. PT-04 (Setup Quality Score) deferred to v3.3+                                 |
|**TBD (gate)**|Arc 2: Pre-Trade Research & Planning (remainder)                      |PT-04 Setup Quality Score — ⏸️ Parked — gate not met for 3 consecutive cycles (v3.6, v3.7, v3.8); PO decision 2026-05-19 to formally park; re-open when PO confirms 20+ closed trades  |
|**v3.3** ✅  |Arc 3: In-Trade Risk Management (partial)                              |IT-01/02/03 backend (lifecycle state machine, grace period alerts, stop trail); research view spec closure (BLG-SPEC-24/25/26, BLG-FE-28); entry checklist E2E; governance patches (OA-01–05); feature flag infra (BLG-FEAT-13); trade plan abandonment backend (BLG-FEAT-21 partial) — ✅ Shipped 2026-05-13 — cycle: 2026-05-09__release-v3.3|
|**v3.4** ✅  |Arc 3: In-Trade Risk Management (continued)                            |IT-01 lifecycle badge frontend, IT-02 grace period alert frontend, IT-03 stop trail frontend, IT-04 drawdown review prompt (backend+frontend), IT-05 concentration limits (backend+frontend); v3.3 deferred frontend quick wins; spec/QA debt — ✅ Shipped 2026-05-14 — cycle: 2026-05-14__release-v3.4|
|**v3.5** ✅  |Arc 3 Completion + Arc 4 Foundation                                   |IT-06 Alpaca paper trading (§13 PASS; backend sync + frontend panel + Playwright); PO-01 Plan vs Reality (arc4_data_requirements.md v1.0 + backend + frontend + Playwright); spec/QA debt (BLG-SPEC-29/30/31, BLG-QA-19); governance patches (BLG-GOV-22, execution_prompt.md v3.20) — ✅ Shipped 2026-05-15 — cycle: 2026-05-15__release-v3.5|
|**v3.6** ✅  |Arc 4 Data Integrity + Arc 2 Quality Score + Debt Clearance           |planned_entry_price snapshot at trade entry; entry_delta_pct in PlanVsReality; SC-RV-18/19 Playwright coverage; research endpoint 404/503 error codes; research page regime lozenge + font fix; execution_prompt.md v3.22 governance patches — ✅ Shipped 2026-05-17 — cycle: 2026-05-16__release-v3.6 — Verified_with_deviations (1 P3)|
|**v3.7** ✅  |Signal-to-Watchlist Workflow + Arc 2 Completion + Governance Hardening|EPIC-01: signals `watchlisted` status + PATCH /signals/{id}; Add to Watchlist CTA on signal cards; SignalContextPanel in trade plan form (entry_rationale + confirmation_criteria pre-pop); 7 Playwright scenarios. EPIC-03: execution_prompt.md v3.24 (3 patches); qa_evidence_template.md v1.1. EPIC-04: BLG-QA-20/OPS-16/FE-35/GOV-23 debt clearance; OA-RP-05 resolved. EPIC-02 (PT-04) deferred — gate not met (< 20 closed trades) — ✅ Shipped 2026-05-18 — cycle: 2026-05-18__release-v3.7|
|**v3.8** ✅  |Arc 5 Strategy Integrity Foundation + Trade Plan Form Enhancements + Ticker Universe Management|EPIC-04: TickerUniverse.js management page (add/toggle/delete/filter); public.tickers startup sync retired; ticker_universe sole authoritative source; BLG-GOV-24 governance debt (gh_issue_template.md §14 + PR template). EPIC-03: setup_type dropdown (6 options, BLG-FEAT-23); collapsible news context panel (BLG-FE-36); AI thesis generation template engine + Gemini-gated "Improve with AI" (BLG-FEAT-24). EPIC-01: SI-01 §13 gate PASS (8 binding conditions); GET /portfolio/pre-entry-validation (5 rules, strategy_rules.md v1.4 §4.2, 17 unit tests); PreEntryValidationPanel with override acknowledgement. Verified_with_deviations (1 P3 — resolved same release) — ✅ Shipped 2026-05-20 — cycle: 2026-05-19__release-v3.8|
|**v3.9** ✅  |Screener Quality & Reliability + Arc 5 Red Flag Journal + Governance Patches|EPIC-01: Yahoo Finance crumb/401 retry + exponential backoff (ST-01); sector/industry fields restored (ST-02); DAY ticker removed + startup deactivation (ST-03); degraded-run warning banner (ST-04). EPIC-02: .L suffix stripped from Ticker Universe display (ST-05); company_name column + CSV backfill (ST-06). EPIC-03: Arc 5 SI-03 Red Flag Journal — red_flag_events table, GET /portfolio/red-flag-journal, SI-01 override event write, RedFlagJournal.js frontend (ST-07/08). EPIC-04: 5 governance carry-forward patches — execution_prompt.md v3.26, sprint_planning_prompt.md v3.4, release_planning_prompt.md v2.31, delivery_verification_prompt.md v2.5, PR template v1.2 (ST-09/10/11/12). Zero deviations — ✅ Shipped 2026-05-22 — cycle: 2026-05-21__release-v3.9|
|**v4.0** ✅  |Arc 5 Analytics Foundation + Spec Closure + Gemini Compliance         |EPIC-01: GET /analytics/arc5-compliance (5 metrics); Arc5ComplianceSection.js; SI-01→SI-03 Playwright integration (8 scenarios). EPIC-02: ticker symbol validation (422 gate); red flag security review (PASS); starlette CVE (1.0.1). EPIC-03: Gemini Flash wiring (POST /trade-plans/{plan_id}/generate-thesis); gemini_audit_log; cost tracking; CI/CD staging auto-deploy. Zero deviations — ✅ Shipped 2026-05-25 — cycle: 2026-05-22__release-v4.0|
|**v4.0+**    |Arc 4: Post-Trade Intelligence (remainder)                            |PO-02 journal pattern recognition, PO-03 behavioural error taxonomy, PO-04 reflection/outcome correlation — 📋 Planned                    |
|**v4.0+**    |Arc 5: Strategy Integrity (remainder)                                 |SI-02 behavioural drift detection, SI-04 strategy version comparison, SI-05 weekly digest — 📋 Planned                                    |
|**v4.0+**    |Arc 6: Performance Science                                            |Edge analysis, regime-conditional performance, Monte Carlo, strategy decay detection — 📋 Horizon                                          |

-----

*For delivery history, see `docs/product/changelog.md`.*
*For backlog and quick wins, see `claude/backlog/backlog.md`.*
*For strategic constraints and system boundaries, see `docs/specs/strategy_rules.md`.*
*For initiative detail (Arc 4 / AI-SUM), see `claude/roadmap/initiative_register.md`.*
*For external API integration decisions, see `docs/product/decisions/`.*