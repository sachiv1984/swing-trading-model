**Owner:** Strategy Rules & System Intent Owner
**Class:** Operational Record (Class 3)
**Status:** Active — CONDITIONAL
**Last Updated:** 2026-10-05 (appendix: wording as applied to strategy_rules.md v1.14 via BLG-GOV-360, after an amended second-pass review); prior — 2026-10-05 (created)
**Cycle:** 2026-09-30__release-v9.9
**Story:** ST-20 (EPIC-04)
**Backlog ref:** BLG-GOV-358 (this review) / BLG-FEAT-65 (feature reviewed, shipped v6.9)
**Escalation ref:** ESC-EXEC-20261001-03


**Write-scope note:** This determination is recorded as a standalone decision record. That satisfies ST-20's first acceptance criterion ("new `docs/product/decisions/` file, or a `strategy_rules.md` §13.3/§13.5 wording update"). Sprint Execution may not write to `claude/strategy/strategy_rules.md` (`claude/system/execution_prompt.md:230`). The §13.3 clarification and §13.5 roster row this record calls for (Binding Condition 9) are therefore recorded as exact proposed text in the appendix below, for a routine or a human that has `claude/strategy/` write access (tracked as BLG-GOV-360). The same pattern is used by `decisions--2026-08-12__release-v8.7--confidence-interval-preview-analytics-section13-policy.md`'s own write-scope note.

---

# §13 Boundary Review — Overnight/Weekend Gap Risk Flag (Retroactive)

**Feature:** Overnight/weekend gap risk flag for open positions (BLG-FEAT-65; ST-02, EPIC-02, `2026-07-10__release-v6.9`). Consists of `backend/services/gap_risk_service.py`, `GET /positions/{position_id}/gap-risk`, `src/hooks/useGapRisk.js`, `GapRiskBadge` (`src/pages/Positions.js`) and `GapRiskCardBadge` (`src/components/positions/PositionCard.js`)
**Review type:** §13 System Boundary Review — **retroactive**, against the already-shipped implementation, focused on §13.3's explicit gap-risk exclusion
**Cycle:** 2026-09-30__release-v9.9
**Governance reference:** `claude/strategy/strategy_rules.md` §13 (v1.13)
**Shipped:** v6.9, 2026-07-10. Ship decision record: `docs/product/decisions/decisions--2026-07-10__release-v6.9.md`
**Agent-mediated:** Sprint Execution Engine, acting as the Strategy Rules & System Intent Owner jointly with the Head of Specs Team per `claude/system/execution_prompt.md` §5.3, under explicit user direction to resolve open escalations
**Precedent reviews:**
- `docs/product/decisions/decisions--2026-07-21__release-v7.7--PT-04-section13-review.md` (PT-04, PASS). Closest structural precedent: a retroactive review of a shipped feature whose design artefacts had only inline §13 assertions.
- `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md` (SI-01, PASS). Cleared the §4.2.3 earnings-proximity advisory that this feature extends to held positions.
- `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (ST-06, CONDITIONAL). Format precedent for binding conditions.
- `strategy_rules.md` §13.4 (on-demand compliance recheck, BLG-FEAT-64, which shipped in the same v6.9 cycle and did receive a §13 continuity note)

---

## Review Summary

`strategy_rules.md` §13.3 (`claude/strategy/strategy_rules.md:501`) says: *"Gap risk monitoring is excluded by design because the system operates on a daily decision cadence and cannot act on gaps at the moment they occur. Exposing a gap risk metric would increase noise without enabling a decision."* That text was added in v1.1 (18 February 2026, `strategy_rules.md:27`), five months before the gap risk flag shipped in v6.9.

**Correction to the backlog item's premise.** BLG-GOV-358 (`claude/backlog/backlog.md:4138-4147`) says the feature shipped "without a recorded §13 review". That is only partly accurate. A §13 sign-off was recorded at ship time: `claude/cycles/2026-07-10__release-v6.9/qa_evidence_EPIC-02.md:33-39` ("ST-02 AC-04: Approved", Strategy Rules & System Intent Owner, agent-mediated §5.3, 2026-07-10). However, the sign-off was scoped by AC-04's wording to one question: "no prediction of gap direction or magnitude" (`qa_evidence_EPIC-02.md:35`; `stage4_backlog_slice.md:75` of that cycle). That is a **§13.2** (prediction) test. Neither the sign-off, the UX spec's §13 section (`docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md:95-97`), the API contract's scope constraint (`docs/specs/api_contracts/position_endpoints.md:969-972`), nor the ship decision record (`decisions--2026-07-10__release-v6.9.md:1-37`, which has no §13 reference) tested the feature against **§13.3**, the clause that names gap risk explicitly. In addition, no standalone §13 review record was produced. The §13.4-style continuity note written for the sibling v6.9 feature (BLG-FEAT-64, `strategy_rules.md:505-507`) has no counterpart for this feature, and the feature has no row in §13.5's re-attestation roster (`strategy_rules.md:515-526`).

**The finding is therefore a genuine coverage gap.** A shipped feature sits in direct textual tension with a named §13.3 exclusion and was never reviewed against it. This record closes that gap.

---

## §13 Boundary Criteria (from strategy_rules.md §13)

### §13.1 — This system IS:
- A deterministic decision-support engine
- A risk-managed momentum framework
- A single, explicit, human-designed strategy
- Human-in-the-loop by design

### §13.2 — This system is NOT:
- An automated trading bot
- A broker execution engine
- A discretionary or adaptive rule system
- A multi-strategy or configurable strategy platform
- A machine-learning or AI-driven prediction system
- An options or futures trading system
- A real-time streaming or execution system

### §13.3 — Design boundary rationale (the clause under review)
> Gap risk monitoring is excluded by design because the system operates on a daily decision cadence and cannot act on gaps at the moment they occur. Exposing a gap risk metric would increase noise without enabling a decision.

The exclusion rests on two premises. Each must be tested separately against the shipped feature:
- **Premise A (actionability):** the user cannot act on a gap at the moment it occurs, given the daily decision cadence.
- **Premise B (signal value):** exposing the metric adds noise without enabling a decision.

---

## Feature Description (As Shipped)

**Backend, `backend/services/gap_risk_service.py`:**
- `get_gap_risk(ticker, market)` (`:97-140`) returns `{flagged, reasons, avg_gap_pct, event_count, insufficient_history}`.
- **Earnings trigger** (`:112-115`): `reasons` gains `"earnings"` when the DS-04 earnings calendar's `days_until_earnings` is 0 or 1 (`_EARNINGS_NEXT_SESSION_WINDOW_DAYS = 1`, `:37`). This is a known, dated event specific to the position's ticker.
- **Weekend-hold trigger** (`:117-119`, `:40-43`): `reasons` gains `"weekend_hold"` whenever the server's `date.today().weekday() == 4`. This is true **for every open position, for the whole of each Friday (server date)**. It does not depend on anything about the position or ticker.
- **Historical statistic** (`:46-94`): computed only when a flag fires (`:121-132`). It is the arithmetic mean of absolute historical overnight gaps, or weekend gaps when the weekend trigger applies, over 2 years of daily OHLCV, as `|open[t] − close[t−1]| / close[t−1]`. It is suppressed below `MIN_HISTORICAL_EVENTS = 10` (`:28`, `:85-86`). It is direction-agnostic (absolute value, `:82`) and does not forecast anything.
- The module docstring asserts "Deterministic only … does not predict gap direction or magnitude" (`:11-12`).

**Endpoint:** `GET /positions/{position_id}/gap-risk`, `backend/main.py:1759-1789`. It is a read-only GET, computed on request, with no write path. Contract: `docs/specs/api_contracts/position_endpoints.md:960-` and `docs/reference/openapi.yaml:2040`. It is registered in `backend/routers/test.py:172`.

**Frontend:**
- `src/hooks/useGapRisk.js:10-39` lazily fetches the endpoint once per position. Results are held in a module-level cache (`:5`, `:16-20`) for the lifetime of the page session. There is no polling or background refresh.
- `GapRiskBadge` (`src/pages/Positions.js:469-493`) renders an amber "GAP RISK" pill in the Table View Alerts cell (`:495-524`).
- `GapRiskCardBadge` (`src/components/positions/PositionCard.js:23-` and `:66-75`) renders the same pill in Grid View.
- The tooltip shows the reason label(s) and `±{avg_gap_pct}% avg ({event_count} events)` or "insufficient history" (`Positions.js:470-476`).
- The reason label for the weekend trigger reads "Weekend hold (flagged at Friday close)" (`Positions.js:466`; `PositionCard.js:19`).
- There is no action affordance or dismiss control (`ux_spec.md:108`).

**Reach check:** a repository-wide search for `gap_risk|gap-risk|GAP RISK` across `backend/`, `src/`, `tests/` and `scripts/` finds no consumer other than the endpoint, the hook, the two badges and their tests. The flag does **not** feed the AI daily briefing or chat (BLG-FEAT-50/51), SI-01 pre-entry validation, the SI-02 drift gate, PT-04 scoring, the notification/alert dispatch path, stop calculation (§7), or exit signals (§8).

---

## §13 Compliance Assessment

### Criterion 1 — Determinism (§13.1)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Pure computation, with no ML or probabilistic model | ✅ COMPLIANT | Date comparisons (`gap_risk_service.py:40-43`, `:112-115`) and an arithmetic mean (`:89`). No model or randomness. |
| Same inputs give the same output | ✅ COMPLIANT | Deterministic given the same earnings-calendar response, OHLCV history and server date. Upstream yfinance data can change between calls, but that is external data variability, not system non-determinism. It is the same class of variation already accepted for `GET /earnings/{ticker}` and SI-01 §4.2.3. |

**Criterion 1 determination: COMPLIANT**

### Criterion 2 — Non-Predictive Output (§13.2)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| No forecast of gap direction | ✅ COMPLIANT | Absolute-value gaps only (`gap_risk_service.py:82`). No sign or direction is surfaced. |
| No forecast of the upcoming event's magnitude | ✅ COMPLIANT | `avg_gap_pct` is a retrospective mean labelled "avg (N events)" (`Positions.js:475`). It is not a prediction interval, probability, or position-scaled loss estimate. |

**Criterion 2 determination: COMPLIANT.** This confirms the original v6.9 AC-04 sign-off (`qa_evidence_EPIC-02.md:37`) on the question it actually addressed.

### Criterion 3 — Decision-Support Only / Human-in-the-Loop (§3, §13.1)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| No automated action or write path | ✅ COMPLIANT | GET-only endpoint (`backend/main.py:1759-1789`). No caller in any write path. |
| No effect on canonical exit conditions | ✅ COMPLIANT | §8 lists exactly three exit conditions (`strategy_rules.md:387-403`). The flag adds none and changes none. A manual exit (§8.3) stays entirely the user's decision. |
| Non-prescriptive copy | ✅ COMPLIANT | The tooltip states the reason and the historical statistic only. Unlike the RISK OFF badge's "consider exit" (`Positions.js:512`), which is correct there because §8.2 is a canonical exit condition, the gap risk copy carries no action recommendation. |
| No action affordance | ✅ COMPLIANT | No button or CTA, and no dismiss (`ux_spec.md:108`). |

**Criterion 3 determination: COMPLIANT**

### Criterion 4 — §13.3 Gap-Risk Exclusion (the clause not previously reviewed)

The two triggers must be assessed separately. They stand differently against §13.3's two premises.

**4a. Earnings-triggered flag — outside the exclusion (distinguishable).**

| §13.3 premise | Holds for the earnings trigger? | Reasoning and evidence |
|---|---|---|
| A — "cannot act on gaps at the moment they occur" | **No** | The flag is raised 0–1 calendar days *before* a known, scheduled event (`gap_risk_service.py:37`, `:114`). It does not detect or react to a gap as it occurs. The user can act within the existing daily cadence, before the gap, through a manual exit, which is permitted "at any time" (§8.3, `strategy_rules.md:401-403`). §13.3's premise is about the moment of the gap. This flag is about the session before it. |
| B — "noise without enabling a decision" | **No** | The trigger is specific to the position and ticker, and rare (a few times a year per holding). The strategy itself already treats earnings gap risk as decision-relevant: §4.2.3 (`strategy_rules.md:270-275`) warns at entry because "earnings announcements can cause large overnight gaps that bypass the trailing stop entirely", and SI-01 cleared that advisory under §13. Showing the same calendar fact for a position already held carries the canonical §4.2.3 rationale through the holding period. It does not add a new kind of signal. |

The repository's own past reading of §13.3 supports this distinction. `position_endpoints.md:40` and `:727` apply "§13.3 constraint" to mean "Display-only. No automated notification, alert, or action is generated". In other words, the exclusion has in practice been read as a bar on *active, standing monitoring*, not on every display of a dated risk fact.

**Determination for 4a:** the earnings trigger, together with the historical statistic shown alongside it, is **outside** §13.3's exclusion. It is permitted subject to the binding conditions below. However, §13.3's text does not make this distinction itself: read literally, "exposing a gap risk metric" covers `avg_gap_pct`. A wording clarification is therefore required (Binding Condition 9).

**4b. Weekend-hold-triggered flag — within the spirit of the exclusion (genuine gap).**

| §13.3 premise | Holds for the weekend-hold trigger? | Reasoning and evidence |
|---|---|---|
| A — actionability | Partly | The flag is shown all day Friday (server date, `gap_risk_service.py:40-43`), so in practice the user can act before Friday's close. However, the shipped label, the UX spec and the frontend spec all describe it as raised "at Friday close" (`Positions.js:466`; `PositionCard.js:19`; `ux_spec.md:76`; `docs/specs/frontend/pages/positions.md:484`). Taken literally, that wording describes exactly the post-close moment at which §13.3 says no decision can be made. Spec, label and code disagree on this point. |
| B — signal value | **Yes — the premise holds** | The trigger fires for **every open position, every Friday**. It does not depend on the ticker, the event or the position (`gap_risk_service.py:117-119`). The only per-position content is the historical weekend-gap average shown in the tooltip. A flag that marks the whole book identically every week does not single out a position for a decision. The only decision it points towards is "do I hold momentum positions over weekends at all", which is a whole-strategy question already settled by the strategy's intent: §2 items 1–2 (`strategy_rules.md:49-50`) are to capture medium- to long-term trends and to "avoid premature exits caused by early volatility". This is the "noise without enabling a decision" §13.3 describes. Recurring uniform amber badges also wear down the meaning of the Alerts column, which the strategy relies on for RISK OFF (§8.2). |

**Determination for 4b:** the standalone weekend-hold trigger falls **within the spirit** of §13.3's exclusion. This is a genuine boundary gap. It is not a safety defect: the flag is display-only, triggers no automated action and has no write path. The ongoing cost is noise and erosion of the Alerts column's signal value. Remediation is required (Binding Condition 6 and Remediation Item 1). The feature may stay live until that remediation is dispositioned.

**Criterion 4 determination: CONDITIONAL.** The earnings trigger is compliant subject to the conditions below and the §13.3 wording clarification. The weekend-hold-only trigger needs remediation.

---

## Critical §13 Boundary Questions

**1. Is this "gap risk monitoring"?**
For the earnings trigger, no. There is no continuous or background evaluation, no detection of realised gaps, no polling (`useGapRisk.js:5`, `:14-36`: fetched once per page session and cached), and no notification dispatch. It is an on-request display of a dated calendar fact, which is the same pattern as the existing Earnings column (`GET /earnings/{ticker}`). Extending it to background evaluation, push or Telegram alerts, or realised-gap detection *would* be monitoring and is excluded (Binding Conditions 2–3).

**2. Is `avg_gap_pct` the "gap risk metric" §13.3 says would increase noise?**
Literally, yes. That is why §13.3's wording needs clarifying. In substance, it is shown only as context *when* a position-specific dated event is flagged. It is never shown as a standing per-position metric on every row. That conditional, contextual display is what separates it from the standing metric §13.3 contemplates. Condition 4 keeps it that way.

**3. Does the flag encourage discretionary deviation from the canonical exit rules (§13.2 "not a discretionary … rule system")?**
No new rule is introduced. A manual exit (§8.3) is already a canonical, user-initiated exit that is "available at any time". Showing a factual risk event before an existing user discretion is the §3 decision-support model (`strategy_rules.md:59-65`). The line that must not be crossed is wording or behaviour that turns the flag into a quasi-exit-signal, such as "consider exit" or "reduce position". Condition 5 enforces this.

**4. Why was this missed at v6.9?**
AC-04 in the v6.9 slice was framed only as "no prediction of gap direction or magnitude" (`stage4_backlog_slice.md:75` of that cycle). The sign-off therefore answered the §13.2 question it was asked. Nobody asked the §13.3 question, even though §13.3 names gap risk explicitly. The v6.9 cycle summary expected a "fast pass given SI-01 precedent" (`claude/cycles/2026-07-10__release-v6.9/cycle_summary.md:32`), which likely reduced scrutiny. Process lesson: when a feature's subject is named in any §13 clause, the §13 AC must cite that clause. This is proposed as Remediation Item 3.

---

## Binding Conditions (Forward-Looking — Binding on the Shipped Feature and Any Extension)

1. **Display-only, with no automated action.** The flag must never write to any position, trade plan or settings record, and must never affect stop calculation (§7), exit signals (§8), position states (§9), SI-01 pre-entry validation, the SI-02 drift gate or PT-04 scoring. Any proposal to make it gate, block or modify a workflow requires a new §13 review.
2. **On-request computation only — no monitoring.** The flag is computed only when the user views the Positions page. No scheduled or background evaluation, no push, email or Telegram notification, and no entry in any notification or alert dispatch path. Adding any of these turns the feature into the "gap risk monitoring" §13.3 excludes and requires a new §13 review.
3. **No realised-gap or intraday detection.** The feature must not detect, measure or react to a gap as or after it occurs (for example "this position gapped down X% at open"). That falls under both §13.3 Premise A and §13.2 ("not a real-time streaming … system").
4. **Retrospective, contextual statistic only.** `avg_gap_pct` stays an arithmetic mean of historical absolute gaps, labelled as historical with its event count, and shown only alongside a flagged position-specific event. It must not become a standing per-row metric, a direction or probability, a forecast interval, or a position-size-scaled projection such as "expected £ loss". Each of those would be a forward-looking position-level risk estimate and requires a new §13 review.
5. **Non-prescriptive copy.** Badge, tooltip and aria text must state facts (reason, date, historical statistic) only. Imperative or advisory wording ("consider exit", "reduce", "hedge", "sell before") is prohibited, because gap risk is not a canonical exit condition under §8.
6. **Every trigger must be specific to the position.** Each trigger must be a known, dated event specific to the position's ticker that falls before the position's next trading session. A trigger that flags every open position identically, as the shipped standalone `weekend_hold` trigger does, does not meet this condition. It must be dispositioned per Remediation Item 1 no later than the first §13.5 semi-annual re-attestation (**2027-02-06**, `strategy_rules.md:535`). Until then the shipped behaviour may remain live.
7. **No downstream consumption without review.** The flag or its statistic must not be fed into the AI briefing or chat, AI thesis generation, the AI post-trade debrief, or any other feature's inputs without a new §13 review of that consuming feature.
8. **Code-level citation.** `gap_risk_service.py`'s module docstring must cite this record. It currently cites only "§13, AC-04" (`:12`). This is folded into Remediation Item 1's scope.
9. **Canonical registration.** `strategy_rules.md` §13.3 gains the clarification, and §13.5's roster gains this feature's row, per the exact text in this record's companion follow-up proposal. Both are applied by a routine or human with `claude/strategy/` write access, in one commit with a v1.14 version bump. §13.5's Maintenance rule (`strategy_rules.md:537`) requires the roster row "in the same commit that records their own initial §13 clearance". Sprint Execution cannot write `strategy_rules.md` (`execution_prompt.md:230`), so the row lands in the first commit that can carry it. That lag is disclosed here rather than silently accepted.

No binding condition requires an immediate code change to the earnings trigger. Conditions 1–5 and 7 describe the feature as it is already shipped. Condition 6 is the only one the shipped code does not meet, and it has a dated remediation path.

---

## Remediation Items Filed

Filed in `claude/backlog/backlog.md` on 2026-10-05:

1. **Weekend-hold trigger disposition and label/spec alignment** (BLG-BE-136, P2). Remove the standalone `weekend_hold` trigger and make the earnings window trading-session-aware, so that a Friday view still flags Monday-morning earnings. Alternatively, the Product Owner and the Strategy Rules & System Intent Owner record a position-specific justification and the §13.3 clarification is extended to cover it. Also align the "flagged at Friday close" label and spec with whatever the actual trigger timing is, and add the Condition 8 docstring citation.
2. **Positions frontend spec data-source drift** (BLG-SPEC-179, P3). `docs/specs/frontend/pages/positions.md:482` still says the data source is "`gap_risk` object from `GET /positions` (new field)". The shipped implementation uses the dedicated `GET /positions/{position_id}/gap-risk` endpoint (`position_endpoints.md` 2.4.0 changelog row, `:37`).
3. **§13 acceptance criteria must cite every §13 clause naming the feature's subject** (BLG-GOV-359, P3). This is the process lesson from Critical Question 4.
4. **Apply the §13.3 clarification and §13.5 roster row to `strategy_rules.md`** (BLG-GOV-360, P2). Binding Condition 9's canonical registration; exact text in the appendix below.

---

## Determination

**Determination: CONDITIONAL**

Criteria 1 (determinism), 2 (non-predictive) and 3 (decision-support only) are COMPLIANT. Criterion 4 (§13.3 gap-risk exclusion) is CONDITIONAL:
- The **earnings-triggered flag** is a display-only flag shown on request, tied to a dated event specific to the position. It is distinguishable from the "gap risk monitoring" §13.3 excludes, because both of §13.3's premises fail for it: it can be acted on within the daily cadence, before the gap, and it signals a specific decision already recognised by §4.2.3.
- The **standalone weekend-hold trigger** falls within the spirit of §13.3's noise rationale. It is a genuine gap, remediated under Binding Condition 6 and Remediation Item 1 by 2027-02-06.

The feature remains live. It enters the §13.5 semi-annual re-attestation roster as CONDITIONAL with nine binding conditions.

---

## FAIL Implications (for reference)

If this had been a FAIL, the feature would have been withdrawn from the Positions page pending redesign. The RISK OFF badge, which shares the Alerts column, would have been unaffected. BLG-FEAT-65's scope would have been re-opened as a §13.3 exception request requiring a `strategy_rules.md` change under §12.3/§16. A FAIL is not warranted: the earnings trigger has a strategy-grounded rationale (§4.2.3), and the weekend-hold problem is noise, not a breach of any hard boundary in §13.1/§13.2.

---

## Sign-Off

**Signed off by:** Strategy Rules & System Intent Owner, jointly with Head of Specs Team (agent-mediated, `claude/system/execution_prompt.md` §5.3, Sprint Execution Engine under explicit user direction to resolve ESC-EXEC-20261001-03)
**Date:** 2026-10-05
**Determination:** **CONDITIONAL**
**Comments (Strategy Rules & System Intent Owner):** §13.3 was written to stop the system pretending it can manage gaps that happen when it cannot act. It was not written to hide dated, known risk facts from a human who *can* act on them a session earlier. The strategy already holds that view at entry (§4.2.3). The earnings flag applies it consistently through the holding period and is accepted. The weekend-hold trigger is the part §13.3 actually warns against: a uniform weekly flag on every position that, at most, invites premature exits contrary to §2 item 2. It must be removed or given a position-specific justification. §13.3's text must be clarified so the next reader does not see a contradiction where there is, on substance, a distinction.
**Comments (Head of Specs Team, §5 quality bar):** "Specs do not drift silently from reality" (`head_of_specs_team.md` §5). This feature drifted in three places. The canonical strategy text contradicts it on its face (§13.3). The frontend spec names the wrong data source (`positions.md:482`). The trigger-timing wording ("at Friday close") disagrees with the code (all-day Friday). Each has an owned, filed remediation. The original v6.9 AC-04 sign-off was correct for the question it was asked. The defect was in how the AC was framed, which is addressed by Remediation Item 3.

**AC sign-off (ST-20, `claude/cycles/2026-09-30__release-v9.9/stage4_backlog_slice.md:194-200`):**
- ✅ A dated determination is recorded: this document, 2026-10-05.
- ✅ The determination is CONDITIONAL and finds a genuine gap. Nine binding conditions are recorded above, and remediation items BLG-BE-136, BLG-SPEC-179, BLG-GOV-359 and BLG-GOV-360 are filed.

**Ownership note:** `sprint_backlog.md:404` lists ST-20's owners as "Head of Specs Team; PMO Lead". The source item (`backlog.md:4141`) and the escalation's owning authority (`execution_escalations.md`, ESC-EXEC-20261001-03) name the Strategy Rules & System Intent Owner and the Head of Specs Team. This determination is signed by the latter pair, who match the escalation's owning authority. No PMO Lead sign-off is required for a §13 boundary determination.

---

## Appendix — strategy_rules.md Wording as Applied

Applied to `claude/strategy/strategy_rules.md` v1.14 on 2026-10-05 (BLG-GOV-360), in ST-20's own commit on the user's explicit instruction. The first-pass draft originally recorded here was superseded by an independent second-pass Strategy Rules & System Intent Owner review (agent-mediated, §5.3, Approved with amendments), which: (1) narrowed the permitted carve-out from any dated position-specific event to events a canonical rule already recognises as gap risk (today only earnings, §4.2.3), with every new event type or trigger needing its own §13 review; (2) recorded the standalone weekend-hold trigger in §13.3 itself as a time-boxed deviation (BLG-BE-136, due 2027-02-06), since the clarified exclusion describes it exactly and §14 makes the document prevail over code; (3) moved the re-attestation escalation instruction into the §13.5 roster row. The applied text follows.

### §13.3 Clarification

```
Gap risk monitoring is excluded by design because the system operates on a daily decision cadence and cannot act on gaps at the moment they occur. Exposing a standing or real-time gap risk metric — one evaluated continuously or in the background, one pushed as a notification or alert, one that detects or reacts to gaps as or after they occur, or one that flags every position uniformly regardless of any event specific to that position's ticker — would increase noise without enabling a decision.

This exclusion does not cover a display-only flag, computed on request, that is tied to a known, dated event specific to the position's ticker, falls before that position's next trading session, and is already recognised as a gap-risk event by a canonical rule in this document. The only such event recognised today is a scheduled earnings date (§4.2.3). The user can act on such an event within the daily cadence, before the gap, through a manual exit (§8.3). Each flag of this kind, and each new event type or trigger added to one, requires its own §13 review before it ships and is permitted only under that review's binding conditions.

The shipped Overnight/Weekend Gap Risk Flag (BLG-FEAT-65, v6.9) is governed by `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` (CONDITIONAL, 2026-10-05). Its earnings trigger is cleared under the paragraph above. Its standalone weekend-hold trigger flags every open position each Friday and does not meet this clarification; it is a recorded, time-boxed deviation that must be removed, or given a position-specific justification signed off under that record with this section amended to match, no later than 2027-02-06 (BLG-BE-136). Any extension towards background evaluation, notification, realised-gap detection or forward-looking gap estimates requires a new §13 review.
```

### §13.5 Roster Row

```
| Overnight/Weekend Gap Risk Flag (BLG-FEAT-65) | `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` | v6.9 shipped; retroactive §13 review v9.9 (**CONDITIONAL** — 9 binding conditions; reviewed against §13.3 as well as §13.1/§13.2, so re-attestation must also confirm its §13.3 standing; earnings trigger cleared as outside §13.3's exclusion; standalone weekend-hold trigger found within §13.3's noise rationale and must be dispositioned per Binding Condition 6 / `BLG-BE-136` by this cadence's first review date, 2027-02-06 — if it has not been, record that re-attestation's outcome as escalated, not unchanged. Original v6.9 AC-04 sign-off, `claude/cycles/2026-07-10__release-v6.9/qa_evidence_EPIC-02.md`, covered §13.2 only) |
```
