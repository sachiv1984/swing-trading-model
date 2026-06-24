**Owner:** Strategy Rules & System Intent Owner
**Class:** Operational Record (Class 3)
**Status:** Active — PASS
**Last Updated:** 2026-06-24
**Cycle:** 2026-06-24__release-v6.2
**Backlog refs:** BLG-FEAT-50 (AI daily briefing), BLG-FEAT-51 (AI chat advisor)
**Stories in scope:** ST-06, ST-07, ST-08, ST-09 (EPIC-02)

---

# §13 Boundary Review — BLG-FEAT-50/51: AI Advisory Layer

**Features:**
- BLG-FEAT-50 — AI daily briefing endpoint (`POST /ai/daily-briefing`) and Dashboard card (ST-06, ST-07)
- BLG-FEAT-51 — Conversational AI trade advisor (`POST /ai/chat`) and chat widget (ST-08, ST-09)

**Review type:** §13 System Boundary Compliance Review
**Cycle:** 2026-06-24__release-v6.2
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**Sprint backlog AC references:** `claude/cycles/2026-06-24__release-v6.2/stage4_backlog_slice.md#ST-06`, `#ST-07`, `#ST-08`, `#ST-09`
**Precedent reviews:**
- `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`
- `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md`

---

## Review Summary

This record documents the formal §13 boundary review required before EPIC-02 stories may proceed to sprint execution. Sprint planning for v6.2 may not seal until this review produces a PASS or FAIL determination.

The primary §13 tension being assessed: BLG-FEAT-50/51 introduce a large language model (`claude-sonnet-4-6`) into the system. §13.2 states the system is not "a machine-learning or AI-driven prediction system." This review determines whether the AI advisory features cross that boundary or remain within the decision-support design intent of §13.1.

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

---

## Feature Descriptions

### BLG-FEAT-50 — AI Daily Briefing

`POST /ai/daily-briefing` assembles a read-only context object comprising: current portfolio state, today's top-5 momentum signals, per-position trailing stops (from ST-01), regime status, and the month-end rebalance date check. This context is passed to `claude-sonnet-4-6` as a system prompt. The LLM generates a plain-English summary and an ordered action list (e.g. "3 positions are within 5% of their trailing stop — monitor closely today").

**What the LLM does:** synthesises already-computed structured data into a human-readable briefing. It does not generate trading signals. It does not predict stock prices. It reads trailing stops, regime status, and signals — all of which were computed by the deterministic strategy engine — and explains them in plain English.

**Output format (from AC-04 of ST-06):** `{ summary: string, actions: [{type, ticker, description}] }`
**Advisory metadata (from AC-06 of ST-06):** response carries `advisory: true`
**Frontend labelling (from AC-04 of ST-07):** card displays "AI Advisory — all actions require your confirmation"

### BLG-FEAT-51 — Conversational AI Trade Advisor

`POST /ai/chat` accepts a user question with optional context (ticker, position_id) and returns a response grounded in the full live portfolio + signal state. The LLM is injected with the live portfolio context as a system prompt (AC-02 of ST-08). Conversations are **stateless per request** — no session memory is maintained across calls (AC-05 of ST-08).

**What the LLM does:** answers ad-hoc portfolio questions ("What's my largest position relative to my trailing stop?", "Which positions are in a risk-off regime?") by reasoning over the live structured data injected into its context.

**What the LLM does NOT do:** predict stock price movements, generate new trading signals, modify any position or trade plan, or store state between interactions.

**Advisory labelling (from AC-03 of ST-09):** widget "clearly labelled as AI advisory; trade actions not executable from widget"

---

## §13 Compliance Assessment

### §13 Critical Question: Does the LLM make the system an AI-driven prediction system?

The determination rests on a key distinction: **where decisions are made**.

In BLG-FEAT-50/51, all trading decisions — trailing stop values, momentum signal rankings, regime determinations, inv-vol position sizing — are made by the deterministic strategy engine (the `production_strategy.py` logic now being ported to live via EPIC-01). The LLM receives these pre-computed values as read-only context and generates a plain-English explanation of them.

The LLM is a **presentation layer**, not a decision layer. It does not:
- Generate trading signals
- Predict future prices or returns
- Modify any strategy parameter
- Block, gate, or influence any trade plan submission
- Trigger any automated action

This is analogous to a trade journal summariser: it reads structured data about trades already computed by deterministic rules and produces a human-readable narrative. The strategy remains human-designed and human-in-the-loop.

---

### Criterion 1 — Determinism

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Underlying strategy computations (trailing stops, signals, regime status) remain deterministic | ✅ COMPLIANT | EPIC-01 implements these as pure deterministic computations matching `production_strategy.py`. The LLM context is a read-only snapshot of these deterministic outputs. |
| LLM output itself is non-deterministic (acknowledged) | ⚠️ NOTED | LLM responses may vary on identical inputs. This is acceptable because the LLM output is advisory-only and does not affect any downstream deterministic computation. The strategy decisions themselves remain deterministic. |
| No random element introduced into any strategy rule | ✅ COMPLIANT | LLM does not write to any data store used by the strategy engine. All trailing stop values, signal rankings, and regime states are computed independently of LLM output. |

**Criterion 1 determination: COMPLIANT** — LLM non-determinism is confined to the advisory presentation layer. It does not propagate into strategy execution.

---

### Criterion 2 — Display-Only / Advisory-Only

| Requirement | Status | Evidence |
|-------------|--------|----------|
| All AI outputs labelled as advisory | ✅ COMPLIANT | AC-06 of ST-06: `advisory: true` in response metadata. AC-04 of ST-07: "AI Advisory — all actions require your confirmation" label on dashboard card. AC-03 of ST-09: "clearly labelled as AI advisory" on chat widget. |
| No AI output gates, blocks, or modifies any trade plan or position entry | ✅ COMPLIANT | Neither endpoint writes to `trade_plans`, `portfolio/positions`, `settings`, or any table in the strategy execution path. Both are pure read + LLM synthesis. |
| Trade actions not executable from AI widget | ✅ COMPLIANT | ST-09 AC-03 explicitly: "trade actions not executable from widget." Widget is observation and question-answer only. |
| No AI output used as a submission constraint | ✅ COMPLIANT | `POST /ai/daily-briefing` and `POST /ai/chat` have no integration with `POST /trade-plans` or any position entry path. API design confirms clean separation. |

**Criterion 2 determination: COMPLIANT**

---

### Criterion 3 — No Adaptive Learning / Strategy Modification

| Requirement | Status | Evidence |
|-------------|--------|----------|
| AI features do not modify strategy parameters | ✅ COMPLIANT | No write path from either AI endpoint to `strategy_rules.md`, settings, or any configuration that affects trailing stop, sizing, or exit logic. |
| No learning from user interactions | ✅ COMPLIANT | ST-08 AC-05 explicitly: "Conversation is stateless per request (no session memory across calls)." No fine-tuning, no interaction logging that feeds back into model behaviour. |
| AI does not adapt the momentum strategy based on portfolio outcomes | ✅ COMPLIANT | The LLM receives a static snapshot as context. It does not observe performance over time and does not adjust any strategy rule. |
| LLM used as text synthesis tool, not strategy optimiser | ✅ COMPLIANT | The system prompt for both endpoints contains structured portfolio state. The LLM generates plain-English explanations. There is no prompt design that asks the LLM to improve or revise strategy parameters. |

**Criterion 3 determination: COMPLIANT**

---

### Criterion 4 — No Automated Action

| Requirement | Status | Evidence |
|-------------|--------|----------|
| AI endpoints must not call Alpaca client or any order execution path | ✅ REQUIRED — binding condition | No AC references Alpaca client calls. Binding condition: code review at EPIC-02 closure must confirm no `alpaca_client` call from `ai_service.py` or any module invoked by POST /ai/daily-briefing or POST /ai/chat. |
| AI output must not trigger automated notifications or alerts | ✅ COMPLIANT | Neither endpoint is wired to the Telegram notification path. The briefing card and chat widget are UI-only. No alert_rules entry for AI output types. Binding condition: this must remain true in implementation. |
| No automated position modification or stop adjustment from AI layer | ✅ COMPLIANT | The AI endpoints are read-only synthesis. No write path to `positions`, `stops`, or any trade execution table. |
| Token usage logged for audit (not for adaptive decisions) | ✅ COMPLIANT | AC-05 of ST-06 and AC-06 of ST-08 require token usage logged to `claude_audit_log`. This is an audit trail only — logs are not used to modify system behaviour. |

**Criterion 4 determination: COMPLIANT**

---

## Critical §13 Boundary Questions

**1. Do the AI features make the system an "AI-driven prediction system" (§13.2)?**

No. The system remains human-designed and deterministic in its decision-making. The LLM operates exclusively on pre-computed deterministic outputs (trailing stops, momentum signals, regime states) and generates advisory plain-English summaries. No price predictions, signal generation, or strategy adaptation occurs. The trading strategy is unchanged; only the presentation of its computed outputs is enhanced.

**2. Does the daily briefing's "action list" imply automated execution?**

No. The action list format `{type, ticker, description}` is a structured advisory summary — equivalent to "here are the things you might want to look at today." Each action requires explicit human confirmation (AC-04 of ST-07: "all actions require your confirmation"). The widget has no execution affordance; the user must navigate to the relevant page and submit a trade plan manually.

**3. Could the chat advisor be misused to generate unauthorised signals?**

The chat advisor is grounded exclusively in live portfolio state (existing positions, existing signals, existing regime data). It cannot generate new momentum signals because it has no access to the signal computation engine and no write path to the signals table. A user asking "what should I buy?" would receive a response grounded in the already-computed signal list — not a novel LLM prediction. This is consistent with §3 (decision-support only, not decision-making).

**4. Does LLM non-determinism undermine the §13.1 "deterministic" requirement?**

The §13.1 "deterministic" requirement applies to the **strategy engine** — trailing stop rules, sizing rules, exit conditions, regime gates. These all remain fully deterministic. The LLM is a post-computation synthesis layer that does not feed into any strategy computation. The same trailing stop value is computed identically regardless of what the LLM says about it. LLM non-determinism is therefore scoped to the advisory text layer only, which is acceptable.

---

## Binding Conditions for EPIC-02 Implementation

The following conditions are mandatory. They are not optional.

1. **Advisory label is non-negotiable.** Both AI endpoints must return `advisory: true` in response metadata. The dashboard card and chat widget must carry visible advisory labels without requiring hover or expansion. Labels must remain present in all non-error states.

2. **No write path from AI service to strategy execution tables.** The AI service layer (`ai_service.py` or equivalent) must not call: Alpaca client, position service write methods, trade plan write methods, signal write methods, or settings write methods. The only permitted writes are token usage logs to `claude_audit_log`. Code review at EPIC-02 closure must confirm this.

3. **No execution affordance in the frontend.** The daily briefing card and chat widget must carry no button, link, or control that submits a trade, modifies a position, or triggers any backend write other than the AI endpoints themselves. The "Regenerate" button (ST-07 AC-03) is the only permitted action — it calls `POST /ai/daily-briefing` only.

4. **Stateless per request.** No session state, conversation history, or user interaction log may be stored or passed between AI endpoint calls. Each call must be fully self-contained. This is a hard requirement binding on the backend implementation (ST-08 AC-05).

5. **LLM system prompt must be grounded in live portfolio data only.** The system prompt for both endpoints must consist of live, already-computed portfolio state (trailing stops, signals, regime status). The LLM must not be given strategy parameters or prompted to modify, optimise, or critique the strategy rules.

6. **No Alpaca client call from AI service.** The AI service must not call the Alpaca client directly. If the AI service needs market data, it must call internal portfolio/signals read endpoints only.

7. **API contract compliance.** Both `POST /ai/daily-briefing` and `POST /ai/chat` must be documented in `docs/specs/api_contracts/` with an explicit advisory declaration in the contract: "display-only advisory; no position write; no automated action; §13 PASS — decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md."

8. **Token audit log.** Token usage for every AI endpoint call must be written to `claude_audit_log` per the established pattern. This provides visibility into AI usage volume and cost. Logs must not be used to modify system behaviour.

9. **Future scope boundary.** Any future extension to EPIC-02 scope that introduces: (a) AI-generated trade signals, (b) automated position modification, (c) price prediction or return forecasting, (d) session memory across requests, or (e) any hard gate on trade plan submission — requires a new §13 review before implementation. This review covers BLG-FEAT-50/51 as specified in v6.2 ACs only.

---

## FAIL Implications (for reference)

Had this been a FAIL:
- EPIC-02 stories (ST-06 through ST-09) would be removed from the sprint backlog
- BLG-FEAT-50/51 would be re-parked with a §13 blocking objection in the backlog
- Sprint planning for v6.2 would seal with Sprint 1 scope only (EPIC-01 + EPIC-03)
- A redesign removing the LLM or restricting it to purely deterministic output would be required before re-review

---

## Sign-Off

**Signed off by:** Strategy Rules & System Intent Owner
**Date:** 2026-06-24
**Determination:** **PASS**

**Rationale:** BLG-FEAT-50 and BLG-FEAT-51 are advisory presentation features built on top of the deterministic strategy engine. The LLM synthesises already-computed structured data — trailing stops, momentum signals, regime states — into plain-English summaries. It does not generate signals, predict prices, modify strategy parameters, or enable automated execution. All frontend components carry mandatory advisory labels and carry no execution affordances.

The critical §13.2 concern — "a machine-learning or AI-driven prediction system" — does not apply because the LLM is not making predictions; it is summarising deterministic outputs in natural language. The strategy remains human-designed, deterministic in its decision-making, and human-in-the-loop. The LLM is a presentation layer only.

Nine binding conditions above are mandatory for EPIC-02 implementation. All four §13 criteria confirmed COMPLIANT.
