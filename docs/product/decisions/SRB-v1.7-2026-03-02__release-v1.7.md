**Owner:** Product Owner (with Strategy Rules & System Intent Owner co-sign)
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Superseded by:** Sprint shipped and verified — outcomes recorded in `claude/cycles/2026-03-02__release-v1.7/verification_report.md` and `docs/product/changelog.md` v1.7 entry. §13-gated features cleared per conditions stated in this record.
**Cycle:** 2026-03-02__release-v1.7
**Last Updated:** 2026-03-03

---

# Strategy Boundary Review — v1.7
## Decision Record: SRB-v1.7-2026-03-02

**Review Session:** 2026-03-02
**Participants (Delegated Authority):** Strategy Rules & System Intent Owner · Product Owner · Head of Specs Team
**Maps to:** EPIC-02 (S2-02), Tasks TASK-01 through TASK-05
**Governing Document:** `claude/strategy/strategy_rules.md` v1.3

---

## Purpose

This document records the §13 strategy boundary review conducted as part of the v1.7 release cycle. Per `stage4_backlog_slice.md`, three candidate features were assessed against the §13 strategy boundary rules before they may enter pre-alignment for v1.8 or later cycles.

§13 establishes two hard constraints:

- **§13.1** — The system is a _deterministic_ decision-support tool. Human-in-the-loop is mandatory for all buy/sell execution.
- **§13.2** — The system is NOT a configurable strategy builder and NOT an AI-driven trading system.

---

## Feature Reviews

### Feature 1 — Signal Parameter Exposure (4.3)
**Description:** Exposing `top_n` (number of top signals returned) and `lookback_days` (signal calculation window) as user-configurable query/display parameters via the signals API.

**§13 Concern:** §13.2 states the system is "not a configurable strategy builder." Does allowing users to adjust `top_n` and `lookback_days` constitute strategy configuration?

**Analysis (Strategy Rules & System Intent Owner):**
These parameters are display and query-scope controls, not strategy execution parameters. The underlying signal generation algorithm, scoring formula, and ranking methodology are fixed in code and not subject to user override. `top_n` controls how many pre-ranked results are returned — the ranking itself is canonical. `lookback_days` scopes the query window for historical data retrieval; it does not alter the signal calculation logic applied to any given data point.

Analogy: filtering a sorted list by N items or by date range does not make the list's sorting algorithm configurable.

**Decision: COMPLIANT**
Signal Parameter Exposure (4.3) does not violate §13.2. Feature may proceed to pre-alignment.

**Condition:** Parameters must remain query/display controls only. Any future change that allows users to modify signal weights, scoring logic, or ranking methodology would require a new §13 review.

---

### Feature 2 — AI Journal Summarisation
**Description:** Using a language model to summarise a user's trade journal entries as a UX convenience feature. The summary is displayed in the UI for the user's reference.

**§13 Concern:** §13.1 requires deterministic decision-support. AI output is non-deterministic. §13.2 prohibits AI-driven trading decisions.

**Analysis (Strategy Rules & System Intent Owner):**
The relevant test is whether the AI output feeds into, or could be reasonably construed as influencing, a trading decision in an automated or semi-automated way.

Journal summarisation as a **pure UX aid** — where the summarised text is displayed alongside the raw journal, is not surfaced in the signal pipeline, is not used as an input to any calculation, and carries an explicit "informational only" label — does not cross the §13 boundary. The human retains full interpretive authority. The system is not acting on the summary.

However, if the AI summary is used to: (a) flag positions for automatic review, (b) feed into signal scoring, or (c) generate buy/sell recommendations — it would violate both §13.1 and §13.2.

**Decision: CONDITIONALLY COMPLIANT**
AI Journal Summarisation is permitted as a UX convenience display feature only.

**Mandatory Conditions:**
1. AI summary output must NOT be used as input to any signal, scoring, or recommendation calculation.
2. The UI must display a clear label: "AI-generated summary — for reference only. Not a trading recommendation."
3. Implementation must be reviewed by Strategy Rules owner before any integration into the signal pipeline.
4. Any expansion of scope beyond read-only display requires a new §13 review before pre-alignment.

---

### Feature 3 — New Technical Indicators
**Description:** Adding new technical indicators (e.g., ATR, Bollinger Bands, additional moving averages) to the system's signal calculation suite.

**§13 Concern:** §13.2 states the system is "not a configurable strategy builder." Does adding new indicators constitute building a configurable strategy platform?

**Analysis (Strategy Rules & System Intent Owner):**
The distinction turns on whether indicators are **canonical (fixed in code and applied uniformly)** versus **user-selectable (the user chooses which indicators to apply)**. Canonical indicators are part of the system's fixed decision-support methodology, analogous to updating the system's analytical model. User-selectable indicators would turn the system into a configurable strategy builder, directly violating §13.2.

A second consideration: indicators that are used only as supporting display data (e.g., overlaying a moving average on a chart) carry lower §13 risk than indicators that are incorporated into the signal score or ranking.

**Decision: COMPLIANT (with scope constraints)**

| Indicator Type | Classification | §13 Status |
|---|---|---|
| Fixed canonical indicators added by engineering | Core methodology update | COMPLIANT |
| Indicators incorporated into signal scoring | Core methodology update | COMPLIANT (requires version bump to signal model) |
| User-selectable indicator toggles | Configurable strategy builder | NOT COMPLIANT — requires new §13 review |
| Chart-overlay display-only indicators | UX enhancement | COMPLIANT |

**Mandatory Conditions:**
1. No user interface shall allow selection or deselection of which indicators are applied to signal scoring.
2. New indicators added to signal scoring require an engineering change and must be documented in the signal model version history.
3. If a future sprint proposes indicator selection UI, a §13 review must be completed before that feature enters pre-alignment.

---

## strategy_rules.md Update Assessment (TASK-03)

**Determination:** No update to `strategy_rules.md` required for this review cycle.

The three features above are addressed by existing §13.1 and §13.2 language. The conditions recorded in this document are sufficient to govern feature execution. No boundary changes were found that would require the canonical strategy rules document to be amended.

**Rationale:** `strategy_rules.md` encodes the _system's strategic intent boundaries_ — it is not a log of individual feature decisions. This decision record (SRB-v1.7) is the appropriate artifact for feature-level boundary findings.

---

## Head of Specs Team Sign-Off (TASK-05)

**Sign-off Date:** 2026-03-02
**Authority:** Head of Specs Team (Delegated Authority — per v1.7 execution grant)

This document is reviewed against the Document Lifecycle Guide v2.4:

- **Class:** Class 4 (Planning Document) ✅ — Decision records under `docs/product/decisions/` are Class 4.
- **Header completeness:** Owner, Class, Status, Cycle, Last Updated all present ✅
- **Status:** Active ✅ — Review session completed; findings are current.
- **Content completeness:** All three mandated features reviewed; each contains explicit §13 determination ✅
- **TASK-03 disposition:** No `strategy_rules.md` update required — documented with rationale ✅
- **Cross-reference:** Maps correctly to EPIC-02 (S2-02) in `stage4_backlog_slice.md` ✅

**Sign-off: GRANTED.** This document is lifecycle-compliant. §13-gated features may now proceed to pre-alignment per the conditions stated above.

---

## Acceptance Criteria Confirmation

| Criterion | Status |
|-----------|--------|
| Review session completed with both owners present | ✅ |
| Decision record filed with compliant Class 4 header | ✅ |
| All three features explicitly addressed | ✅ |
| strategy_rules.md update: not required (documented) | ✅ |
| Head of Specs Team lifecycle sign-off obtained | ✅ |
| §13-gated features may proceed to pre-alignment per stated conditions | ✅ |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-03-02 | Initial §13 boundary review — v1.7 cycle. All three features assessed. No strategy_rules.md changes required. |
