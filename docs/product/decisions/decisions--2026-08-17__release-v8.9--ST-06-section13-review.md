Owner: Strategy Rules & System Intent Owner
Class: Operational Record (Class 3)
Status: Active — CONDITIONAL
Last Updated: 2026-08-21 (Known Deviations section added — DEV recorded for Condition 1's literal "Nth trade" example, superseded by BLG-TECH-17/ST-04, v9.0)
Cycle: 2026-08-17__release-v8.9
Story: ST-23 (EPIC-02)
Scoping ref: docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-gate-story-scoping.md
Escalation ref: ESC-20260817-01
Design gate ref: claude/cycles/2026-08-17__release-v8.9/design_gate.md

---

# §13 System Boundary Review — ST-06: Automated AI Post-Trade Debrief

**Feature:** ST-06 — Automated AI Post-Trade Debrief (EPIC-02, BLG-FEAT-90)
**Review type:** §13 System Boundary Review
**Cycle:** 2026-08-17__release-v8.9
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**Sprint backlog AC reference:** `claude/cycles/2026-08-17__release-v8.9/stage4_backlog_slice.md#ST-06`
**Precedent reviews:**
- `docs/product/decisions/arc6_ps03_section13_preassessment.md` (PS-03, PASS — nearest structural precedent: statistical/decision-support output framing)
- `docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` (AI Advisory Layer — daily briefing + chat, nearest precedent for free-text AI-generated output)
- `docs/specs/api_contracts/gemini_thesis_generation.md` §13 compliance note (nearest precedent for a single-feature AI-generation compliance note, though narrower in scope than a standalone review)

---

## Review Summary

This document is the formal §13 System Boundary Review for ST-06 (Automated AI Post-Trade Debrief), produced by the Sprint 1 gate story (ST-23) scoped in the referenced decision record. ST-06's implementation stories (Sprint 2) may not begin execution until this review reaches a PASS or CONDITIONAL determination (per `execution_prompt.md` §5.1's `LL-v3.5-SP-01` pattern and the scoping decision record §2).

ST-06 synthesises three inputs — plan-vs-reality delta (entry/exit/stop vs. plan), linked journal entries where present, and SI-02 drift context — into a new AI-generated free-text debrief for each newly-closed trade, including "one suggested focus area" for the user's attention. This is a materially new AI-provider use: it is neither an extension of `gemini_thesis_generation.md`'s pre-trade thesis generation (a different purpose — forward-looking rationale vs. backward-looking review) nor of PS-03's deterministic statistical simulation (Monte Carlo has no free-text generative component). It requires its own review.

---

## §13 Boundary Criteria (from `strategy_rules.md §13`)

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

## ST-06 Feature Description

Per `stage4_backlog_slice.md#ST-06`:

> Every newly-closed trade has an AI-generated debrief available shortly after close (real-time generation, or on-demand if real-time isn't feasible). Debrief references plan-vs-reality data and any linked journal entries where present. Generation is logged to `claude_audit_log` per existing AI governance policy. AI Compliance & Governance Officer sign-off (per standing AI-generated-content governance requirement).

**Implementation scope (anticipated, Sprint 2):**

| Component | Description |
|-----------|-------------|
| Trigger | Position close event (`status: closed` on `trade_history`), or an on-demand "Generate Debrief" action if real-time generation proves infeasible within the close-event flow |
| Backend generation service | Gemini call assembling a prompt from: the trade's own `trade_plans` row (entry/exit/stop plan), the resulting `trade_history` row (actual entry/exit/stop/pnl), any linked `journal_entries` rows for the ticker/date range, and the position's most recent SI-02 drift-check result if one exists |
| Backend persistence | Debrief text persisted against the closed trade (new column or child table — exact shape is an implementation decision, not a §13 concern); generation call logged to `claude_audit_log` per the standing AI governance policy (mirrors `gemini_thesis_generation.md`'s existing audit-log requirement) |
| Frontend display | Read-only debrief panel on the closed-trade / trade-history detail view — text output plus the one suggested focus area, no action affordances |

---

## §13 Compliance Assessment

### Criterion 1 — Determinism

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Generation uses no ML model or trained inference | ⚠️ CONDITIONAL | Unlike PS-03 (pure statistical resampling), ST-06 *does* call a generative language model (Gemini) to produce free-text output. This is consistent with the system's **existing, already-cleared** precedent for AI-generated advisory text (`gemini_thesis_generation.md`, BLG-FEAT-50/51 daily briefing + chat) — §13.1's "deterministic decision-support engine" has already been interpreted, in those clearances, as compatible with an LLM-generated *narrative/advisory layer* sitting outside the system's own deterministic trading logic (position sizing, stop calculation, gate checks), provided the LLM output never feeds back into that deterministic logic. ST-06 follows the same shape: the debrief is read-only narrative text layered on top of already-computed, deterministic plan-vs-reality data. It does not compute or alter any deterministic value. |
| Same inputs produce same outputs | ⚠️ CONDITIONAL | LLM generation is not bit-for-bit reproducible in the way Monte Carlo with a fixed seed is. This is consistent with the precedent already accepted for `gemini_thesis_generation.md` and the AI Advisory Layer — §13.1 determinism is satisfied at the level of the **system's own trading rules and gates**, not at the level of every generated sentence of advisory prose. Binding condition: the debrief's *quantitative claims* (P&L, entry/exit/stop values, drift-check result) must be sourced directly and only from the already-computed deterministic `trade_history`/`trade_plans`/SI-02 fields passed into the prompt — the model may not compute or restate a number it wasn't given. |
| No adaptive parameters updated by generation | ✅ COMPLIANT | The debrief is generated once (or regenerated on-demand) per closed trade and displayed. It must not write back to strategy parameters, stop multipliers, risk percentages, sizing inputs, or any other configurable value. |

**Criterion 1 determination: CONDITIONAL** — compliant under the same "narrative layer, not deterministic-logic layer" reading already established for `gemini_thesis_generation.md` and BLG-FEAT-50/51, subject to the quantitative-grounding binding condition below.

---

### Criterion 2 — Own-Data Only

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Input data sourced exclusively from the user's own data | ✅ COMPLIANT | Prompt inputs are the trade's own `trade_plans` row, its own `trade_history` row, the user's own linked `journal_entries`, and the position's own SI-02 drift-check result. No cross-user data, no external benchmark, no peer cohort. |
| No external market models or factor models | ✅ COMPLIANT | The debrief is a summary of what happened on this specific trade against this specific plan — it makes no market-condition or macro claims. |
| No external benchmark comparison | ✅ COMPLIANT | The comparison is plan (this trade's own stated intent) vs. reality (this trade's own outcome) — not against an index, peer average, or other traders' outcomes. |

**Criterion 2 determination: COMPLIANT**

---

### Criterion 3 — Non-Predictive Output

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Output is backward-looking review, not a forward prediction | ✅ COMPLIANT | Unlike `gemini_thesis_generation.md` (forward-looking, pre-trade rationale) and PS-03 (forward-looking outcome envelopes), ST-06 is explicitly a *post-trade* debrief — it reviews a trade that has already closed. There is no future outcome being forecast. |
| Output does not claim to predict the outcome of future trades | ✅ COMPLIANT, subject to binding condition | The debrief must confine itself to what happened on the trade just closed. It must not extrapolate ("your next trade will likely...") — this is a framing requirement, not a structural one, and is carried forward as a binding condition. |
| "One suggested focus area" does not read as a forecast | ✅ COMPLIANT, subject to binding condition | See Critical Boundary Question 1 below — this is assessed under Criterion 4 (decision-support vs. recommendation), not Criterion 3, since a "focus area" is retrospective attention-direction, not a claim about future price/outcome. |

**Criterion 3 determination: COMPLIANT** — ST-06's backward-looking framing is structurally *stronger* against Criterion 3 than either existing AI-output precedent, since there is no future state to mispredict.

---

### Criterion 4 — Decision-Support Only

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Output does not gate, block, or auto-trigger any trade action | ✅ COMPLIANT | The debrief is generated after the trade has already closed. There is no trade action left for it to gate — the position is already exited. This is a structurally safer position than SI-01/SI-02 (which sit in front of an open decision) or even PS-03/gemini_thesis_generation (which inform a decision not yet made). |
| Human-in-the-loop preserved | ✅ COMPLIANT | The user reads the debrief and applies their own judgment to future trades. No system action is triggered by any debrief content. |
| No auto-remediation affordance | ✅ COMPLIANT | The frontend display must contain no buttons, links, or prompts that auto-adjust strategy parameters, journal entries, or any other record based on debrief content. |
| "One suggested focus area" does not cross into a system recommendation | ⚠️ CONDITIONAL — see Critical Boundary Question 1 | This is the specific boundary risk the scoping decision record flagged as "most likely to draw a CONDITIONAL rather than a clean PASS." Addressed in full below. |

**Criterion 4 determination: CONDITIONAL** — compliant subject to the focus-area framing binding conditions below.

---

## Critical §13 Boundary Questions

**1. Does "one suggested focus area" constitute a system recommendation rather than decision-support context? (the flagged boundary risk)**

This is the question the scoping decision record specifically called out as the area most likely to produce a CONDITIONAL rather than a clean PASS, and it is assessed directly here rather than folded into the generic four-criteria pass.

A "suggested focus area" sits on a spectrum:
- At one end: *purely descriptive* ("Your exit was 40% earlier than your plan's exit rule — this is the third trade this month where the exit deviated from plan.") — this is decision-support: it surfaces a pattern from the user's own data and leaves the interpretation and any resulting action entirely to the user.
- At the other end: *prescriptive* ("You should hold winners longer" or "Reduce position size on high-volatility setups like this one") — this would cross into the system telling the user what to do, which is a materially different function than SI-01's deterministic pre-entry gate (SI-01 checks compliance against the user's *own pre-declared* rules; it does not invent new advice) and is not covered by any existing §13 clearance.

**Assessment:** COMPLIANT only if the "suggested focus area" is constrained to *pattern-surfacing from the user's own data*, phrased as an observation about what happened, not an instruction about what to do differently. This is carried forward as a binding condition (Condition 1 below), and is the single most important condition in this review.

**2. Is generative (non-deterministic) text output compatible with §13.1 "deterministic decision-support engine"?**

As discussed under Criterion 1: §13.1 has already been interpreted, in two prior clearances (`gemini_thesis_generation.md`, BLG-FEAT-50/51), as governing the system's own *trading logic* (sizing, stops, gates) rather than every word of AI-generated advisory prose layered on top of that logic. ST-06 does not alter this interpretation — it applies the same narrative-layer/logic-layer separation already established. What is new here is a binding requirement (Condition 2) that any *quantitative* claim inside the generated text (a P&L figure, an entry/exit/stop value, a drift-check verdict) must be sourced verbatim from the deterministic data passed into the prompt, not computed or asserted by the model itself — this closes a gap neither prior AI-output review needed to address as explicitly, since neither `gemini_thesis_generation.md` (pre-trade, no "actual outcome" numbers exist yet) nor the daily briefing (aggregate, not single-trade) makes claims about a specific already-known numeric outcome the way a post-trade debrief inherently will.

**Assessment:** COMPLIANT, subject to Condition 2.

**3. Does referencing SI-02 drift context in the debrief create a new dependency that could turn the debrief into an enforcement mechanism?**

SI-02 (drift detection) is itself already §13-cleared as decision-support, non-blocking. ST-06 reading SI-02's *already-computed, already-cleared* drift result and restating it in prose does not add a new enforcement path — the debrief has no mechanism to act on the drift result, it can only describe it. This is materially different from SI-02 itself gating an action.

**Assessment:** COMPLIANT — no new boundary risk. The debrief is a read-only consumer of an already-cleared upstream signal.

**4. Is there scope-creep risk in a future "generate follow-up trade idea" extension?**

A natural extension of a post-trade debrief is to suggest a specific follow-up trade ("Consider re-entering AAPL on the next pullback"). This would be a materially new function — moving from reviewing a closed trade to proposing a new one — and would fail Criterion 4 outright (this is precisely the kind of system-initiated trade suggestion §13.2 excludes: "a discretionary or adaptive rule system").

**Assessment:** Any future extension that proposes a specific new trade, ticker, or entry point requires a new §13 review before implementation. This is carried forward as Condition 7.

---

## §13 Conditions for Implementation (Binding on ST-06 Sprint 2)

The following conditions are mandatory for the ST-06 implementation sprint. They are not optional. Sprint 2 planning for ST-06 may not seal without confirmation that all conditions are carried forward, and the implementation must cite this document per Condition 6.

1. **"Suggested focus area" must be pattern-surfacing, not prescriptive.** The focus area must describe an observed pattern from the user's own trade/plan data (e.g. "this is the Nth trade where X occurred") and must not instruct the user to take a specific future action, change a specific parameter, or adopt a specific new behaviour. Prescriptive phrasing ("you should...", "reduce...", "increase...", "consider doing X next time") is prohibited; observational phrasing ("your exit deviated from plan by X", "this is the Nth consecutive trade where Y") is required.

2. **Quantitative claims must be sourced verbatim from deterministic inputs.** Any number appearing in the generated text (P&L, entry/exit/stop price, R-multiple, drift-check verdict) must be taken directly from the `trade_plans`/`trade_history`/SI-02 data passed into the prompt. The model must not be asked to compute, estimate, or restate a numeric value from memory or inference.

3. **Output framing must be retrospective, not forward-looking.** Language must describe what happened on the trade that closed ("your exit was...", "compared to your plan..."), not what will happen on future trades. Predictive framing ("your next trade will likely...", "expect similar results if...") is prohibited.

4. **No action affordances in the frontend display.** The debrief panel must contain no buttons, links, or prompts that auto-adjust strategy parameters, create a new trade plan, or modify any record based on debrief content.

5. **Generation logged to `claude_audit_log`.** Every debrief generation call (real-time or on-demand) must be logged per the standing AI governance policy, consistent with the existing `gemini_thesis_generation.md` audit-log requirement — same table, same logging contract.

6. **§13 compliance note required in the backend generation service file.** The backend debrief-generation service must include a comment referencing this review and affirming: "post-trade review only; pattern-surfacing focus area, not prescriptive advice; no position/trade-plan write; no automated action; §13 CONDITIONAL PASS — docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md."

7. **Any extension proposing a specific new trade/ticker/entry requires a new §13 review.** A future "suggest a follow-up trade" extension is out of scope for this clearance and must not be implemented under it.

8. **AI Compliance & Governance Officer sign-off required in addition to this review**, per the sprint backlog's own AC5 and the standing AI-generated-content governance requirement — this §13 review clears the system-boundary question; it does not substitute for the separate AI-content governance sign-off named in `stage4_backlog_slice.md#ST-06`.

9. **Output-side enforcement is mandatory — a prompt instruction alone does not satisfy Conditions 1 or 2.** Conditions 1 and 2 above describe what the model must be *instructed* to do; this condition requires that compliance be *verified on the generated output itself*, server-side, before the debrief is shown or persisted. LLM generation is not deterministic (Criterion 1 above) — a system-prompt instruction not to be prescriptive, or not to fabricate numbers, is a known-imperfect control on its own and is insufficient by itself for a feature whose entire output is free text making numeric claims about a specific closed trade. The generation service must implement, at minimum:
   - **Prescriptive-language check:** a post-generation automated scan of the "suggested focus area" text for prescriptive constructs (e.g. imperative/advisory phrasing such as "you should", "consider doing", "reduce", "increase", "try", "next time, do X") before display or persistence. On a match: regenerate **once**, then re-run this same check against the regenerated text before it may be shown or persisted — a second failure (on the regenerated text) is treated as terminal for this generation attempt and must fall back to omitting the focus-area sentence for that debrief (the plan-vs-reality summary may still display), never a second regeneration. Non-compliant text is never shown, on either attempt.
   - **Numeric cross-check:** every numeric token in the generated debrief text that purports to be a trade fact (P&L, entry/exit/stop price, R-multiple) must be programmatically matched against the actual `trade_plans`/`trade_history`/SI-02 values passed into the prompt before the debrief is shown or persisted. A number that does not match any source value fails the check; treat with the identical one-regenerate-then-recheck-then-fallback sequence as the prescriptive-language check above (fallback: a numbers-free summary). If both checks fail on the same generation attempt, one regeneration covers both — do not regenerate twice for two distinct failure types on the same attempt.
   - Both checks are implementation, not aspiration: they must exist as code in the generation service (not merely documented as an instruction to the model), and their pass/fail outcome — not just "generation succeeded" — must be part of what is logged to `claude_audit_log` per Condition 5, so a compliance failure is auditable even when the fallback path silently protects the user-facing display.
   - This condition constrains Sprint 2's implementation design (the output-side checks must sit in the generation service before persistence, not be left as a DoQ-time spot-check) and must be confirmed present, with test coverage, before ST-06's own DoQ sign-off — not deferred to a later hardening pass.

---

## Determination

**Determination: CONDITIONAL**

Criteria 2 (own-data only) and 3 (non-predictive output) are cleanly COMPLIANT — ST-06's backward-looking, own-trade-only framing is structurally favourable relative to prior AI-output clearances. Criteria 1 (determinism) and 4 (decision-support only) are CONDITIONAL: compliant under the same narrative-layer/logic-layer interpretation of §13.1 already established for `gemini_thesis_generation.md` and BLG-FEAT-50/51, and subject in particular to Condition 1 (the "suggested focus area" must remain pattern-surfacing, not prescriptive) — the specific risk area the scoping decision record identified in advance.

This CONDITIONAL determination satisfies the gate: per the scoping decision record §2 and `execution_prompt.md` §5.1's `LL-v3.5-SP-01` pattern, a PASS or CONDITIONAL determination unblocks ST-06 for Sprint 2 execution, subject to the **nine** binding conditions above (Condition 9 added on internal re-review — see the Sign-Off section's Revision note). All nine conditions carry forward and must be confirmed in place at ST-06's own DoQ sign-off before merge — Condition 9 in particular is a hard pre-DoQ requirement, not a later hardening pass.

---

## FAIL Implications (for reference)

Had this been a FAIL:
- ST-06 would be re-parked in the backlog with a blocking §13 objection
- The AI post-trade debrief feature would require redesign (most likely: removing the "suggested focus area" output entirely, reducing scope to a pure factual plan-vs-reality summary) before a new §13 review could be submitted
- Sprint 2 planning could not include ST-06

---

## Sign-Off

**Signed off by:** Strategy Rules & System Intent Owner
**Date:** 2026-08-18
**Determination:** **CONDITIONAL**
**Comments:** ST-06's core structure — a backward-looking, own-trade-only, read-only debrief — is well within §13 boundaries and is, on Criteria 2 and 3, cleaner than either existing AI-output precedent (`gemini_thesis_generation.md`, BLG-FEAT-50/51 daily briefing). The one genuine boundary risk, flagged correctly in advance by the scoping decision record, is the "one suggested focus area" output: it must be implemented as an observation about a pattern in the user's own data, never as an instruction about what the user should do differently. Condition 1 makes this explicit and non-negotiable. Condition 2 (verbatim quantitative sourcing) closes a secondary risk specific to post-trade review — that the model could restate or subtly alter an already-known numeric outcome — that neither prior AI-output review needed to address as directly, since neither operates on an already-known specific numeric result the way a post-trade debrief inherently does.

**Revision note (self-review before finalising, two passes):** the initial draft of this determination relied on Conditions 1 and 2 as prompt-design instructions alone, with compliance "confirmed in place at ST-06's own DoQ sign-off" — on reflection this is insufficient given free-text LLM generation is explicitly non-deterministic (Criterion 1) and this is the highest-risk free-text surface reviewed under §13 to date (per-trade, numeric-claim-bearing, discretionary-sounding focus area). A prompt instruction not to be prescriptive is a known-imperfect control; a design-time check confirms the prompt was written correctly, not that every generated output complied. Condition 9 was added to close this gap: an output-side, server-side enforcement mechanism (automated prescriptive-language scan + numeric cross-check against source data, both pre-display/persistence, both audit-logged), required implemented and test-covered before ST-06's own DoQ sign-off. A second pass then caught that the Determination section still referenced "eight" conditions after Condition 9 was added — corrected to nine throughout — and tightened Condition 9's regenerate-then-recheck sequencing to make explicit that a second check failure on regenerated text is terminal (mandatory fallback, no second regeneration), rather than leaving that inferred.

**AC sign-off (per scoping decision record §2 / this story's ACs 1–5):**
- AC-01: ✅ §13 review document produced at this path
- AC-02: ✅ Assessment addresses determinism, own-data-only, non-predictive-output, and decision-support-only criteria specifically against the "one suggested focus area" output — see Criterion 1, Criterion 4, and Critical Boundary Question 1
- AC-03: ✅ Binding conditions documented — nine conditions above (Condition 9 added on internal re-review: output-side enforcement, not prompt-instruction-only, for Conditions 1 and 2)
- AC-04: ✅ Explicit Determination recorded: **CONDITIONAL**
- AC-05: ✅ Strategy Rules & System Intent Owner sign-off recorded above

---

## Known Deviations

### DEV — Condition 1's literal "Nth trade" example superseded by BLG-TECH-17/ST-04 (v9.0)

**Filed:** 2026-08-21, during ST-04 (BLG-TECH-17, EPIC-01, cycle 2026-08-21__release-v9.0)
**Priority:** P3 (Low)
**Target resolution release:** v9.0 (implementation already applied; this record confirms the spec text)
**Owner:** AI Compliance & Governance Officer (co-owner of BLG-TECH-17); Strategy Rules & System Intent Owner (this document's owner)
**Backlog reference:** BLG-TECH-17

**Description:** Condition 1 (line 158 above) states observational phrasing including `"this is the Nth consecutive trade where Y"` **is required**. `backend/services/debrief_service.py`'s `_FOCUS_AREA_SYSTEM` prompt, prior to v9.0, echoed this "pattern in this trade's own data" framing but never computed or passed any cross-trade frequency/count into `source_values` for `numeric_cross_check()` (Condition 9) to verify such a claim against — a gap found via agent-mediated Director of Quality review on ST-06's own PR (#1460) and filed as BLG-TECH-17. Any such count the model stated would either fail Condition 9's numeric cross-check (losing the feature's value on a frequent, silent fallback) or coincidentally match an unrelated approved number (e.g. `holding_days`, `r_target`) and pass despite being an ungrounded guess — undermining Condition 2's verbatim-sourcing guarantee in a way Condition 1's own literal example invites.

**Resolution applied (ST-04, v9.0):** `_FOCUS_AREA_SYSTEM` now explicitly prohibits count/frequency/cross-trade-comparison claims (including literally the "Nth time"/"Nth consecutive trade" phrasing Condition 1 names as a required example), scoping the encouraged observational phrasing to single-trade, verifiable facts only. This satisfies Condition 1's *substantive* intent (pattern-surfacing, non-prescriptive, decision-support-only) and Condition 9's numeric-verifiability requirement, but diverges from Condition 1's literal example text.

**Disposition:** Not treated as a compliance failure — Condition 9 (output-side numeric verifiability, added on this document's own internal re-review) already establishes verifiability as the controlling requirement, and Criterion 1 (determinism) analysis above already flags free-text generation as "a known-imperfect control." Condition 1's literal "Nth trade" example is the part that needs updating, not ST-04's fix. Recorded here rather than silently reconciled, per AI Compliance & Governance Officer co-ownership — a future revision of this document should replace Condition 1's example phrasing with a single-trade-scoped example consistent with the current prompt (e.g. `"your exit deviated from plan by X"`, already given alongside the now-superseded example on the same line).
