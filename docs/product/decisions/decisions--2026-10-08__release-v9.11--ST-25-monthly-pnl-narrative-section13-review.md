Owner: Strategy Rules & System Intent Owner
Class: Operational Record (Class 3)
Status: Active — CONDITIONAL
Last Updated: 2026-10-09 (initial determination, ESC-EXEC-20261008-02)
Cycle: 2026-10-08__release-v9.11
Story: ST-25 (EPIC-04, BLG-FEAT-59)
Escalation ref: ESC-EXEC-20261008-02
Design gate ref: claude/cycles/2026-10-08__release-v9.11/design_gate.md (§13 PRE-CHECK REQUIRED; `stage4_backlog_slice_addendum.md` §ST-25 step 1)

---

# §13 System Boundary Determination — ST-25: AI-Assisted Monthly P&L Narrative

**Feature:** ST-25 — an optional, AI-written narrative on the Monthly P&L report (EPIC-04, `BLG-FEAT-59`)
**Review type:** §13 confirmation route (RISK-06, ruled at Sprint Planning 2026-10-08) — a recorded PASS / CONDITIONAL / FAIL determination, not a full §13 review
**Governance reference:** `claude/strategy/strategy_rules.md` §13 — §13.1–§13.4 and §13.6 as at v1.14 (unchanged by EPIC-03's v1.15 §6.3 edit); v1.16 adds this feature's §13.5 roster row
**AC reference:** `claude/cycles/2026-10-08__release-v9.11/stage4_backlog_slice.md#ST-25` AC 2
**Citation rule:** `release_planning_prompt.md` STEP 4 / `design_gate_prompt.md` §13 pre-check (ST-35, EPIC-06, v9.11, commit `c299a1ce` on the EPIC-06 branch, pending merge): cite every §13 clause whose text names the feature's subject
**Advisory-only reference:** `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md` (§13 advisory-only constraint named in ST-25 AC 2); `docs/specs/qa/ai_s13_boundary_test_suite.md` (D1–D4 boundary dimensions)
**Precedent records:**
- `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (post-trade debrief, CONDITIONAL — nearest precedent: backward-looking, number-heavy AI prose with output-side checks; Conditions 1, 2 and 9 are mirrored here)
- `docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` (daily briefing and chat — the original narrative-layer/logic-layer reading of §13.1)
- `docs/ops/ai_monthly_pnl_narrative_cost_estimate_2026-10-08.md` (ST-23 — model and caching assumptions this determination relies on)

---

## 1. Feature Under Review

The Monthly P&L report (`docs/specs/frontend/pages/reports.md` §Monthly P&L Report, `GET /reports/monthly-pnl`) shows deterministic, month-by-month realised P&L for a selected UK tax year. ST-25 adds an optional section in which an AI model writes one or two short paragraphs describing those figures in plain language.

**What the model receives (the whole prompt input):** the rows of the selected range as already computed by `reports_service.get_monthly_pnl_report()` — `year`, `month`, `realised_pnl_gbp`, `trade_count`, `null_fee_trade_count`, `restated`, `restated_diff_gbp` — plus a small set of range figures computed server-side by deterministic code before the call (range total, total trades, best and worst month, count of profitable and losing months, number of months in the range, and the tax-year label with its tokens, e.g. `2025/26`, `2025`, `26`, `6 April`, `5 April`) and the table's net/gross basis caption. Nothing else: no tickers, no trade-level rows, no journal or note text, no market data, no benchmark, no unrealised estimate.

**What it produces:** descriptive prose shown in a labelled, dismissible section of the page. It is generated only on the user's request and stored in its own store (not `monthly_pnl_snapshots`), keyed on the tax year and a hash of its input figures. A repeat view therefore does not call the model again. A restatement changes the hash and so invalidates the stored text. It is never written into any figure, export, snapshot or report record.

ST-23 recommendation 2 assumed one stored narrative per month. Keying on the tax year means one call covers up to 12 months, so calls per month viewed are equal or fewer and ST-23's cost bounds still hold.

---

## 2. §13 Clauses Cited

Per the citation rule, subject terms searched across all of §13: *AI*, *machine learning*, *prediction*, *generation*, *automat*, *narrative*, *report/reporting*, *financial*, *P&L*, *tax*, *advisory*.

| Clause | Matching text (or why it is cited) | Applies? |
|--------|-----------------------------|----------|
| §13.1 | No subject term. Cited under the rule's fallback ("no clause names the subject; §13.1/§13.2 apply"): "a deterministic decision-support engine", "human-in-the-loop by design" | Yes — the governing test for any AI output layer (named at minimum by ESC-EXEC-20261008-02) |
| §13.2 | "a machine-learning or AI-driven prediction system"; also "an automated trading bot" (*automat*) | Yes. The first phrase is the primary exclusion this feature must stay outside. The second is not engaged, because nothing here trades. |
| §13.3 | "machine learning-based signal generation would change the nature of the system" | Yes — the narrative must not become a signal |
| §13.4 | "no new automation or prediction surface" (continuity note, recheck feature) | Cited for completeness: it names *prediction* but governs only the on-demand compliance recheck. Not engaged by this feature. |
| §13.5 | "Every shipped AI/automation-adjacent feature that previously cleared a §13 boundary review is re-attested"; roster Maintenance rule | Yes — the narrative joins the roster in the same commit as this determination |
| §13.6 | Only *automat* in its sign-off line ("automatic-escalation"), which is unrelated | No. SI-02-only cadence; not engaged. |

§13.4 and §13.5 also match *automat* ("automation"), which adds nothing beyond their rows above. No hits for *narrative*, *report*, *financ*, *P&L*, *tax*.

**No §13 clause names financial reporting, P&L or reports.** The financial-reporting question (AI text inside a financial record) is therefore assessed under §13.1/§13.2's decision-support reading and SRB-v1.7's advisory-only constraint. It is controlled by Conditions 5 and 6 below rather than by a clause of its own. This gap is recorded, not resolved here: if the Owner later wants a §13 clause naming AI text in financial reports, that is a `strategy_rules.md` change of its own.

---

## 3. Assessment

### 3.1 Determinism (§13.1, §13.2, §13.3)

The narrative is generated by a language model, so its wording is not reproducible. As in the debrief and the briefing/chat clearances, §13.1's "deterministic decision-support engine" governs the system's trading logic (sizing, stops, gates, P&L computation), not every sentence of advisory prose layered over it. The narrative reads already-computed figures and writes nothing back, so no deterministic value depends on it.

The risk specific to this feature is that the text sits beside authoritative financial figures. A model that restates a figure wrongly, or computes a new one (a percentage change, an average, a projection), would put an unverified number inside a financial report. That is controlled by Condition 3 (verbatim numbers, plus server-side value and direction checks) and Condition 4 (deterministic fallback), both test-covered before DoQ.

**CONDITIONAL** — Conditions 2, 3 and 4.

### 3.2 Own data only

The input is the user's own realised P&L aggregates. There is no cross-user data, peer cohort, index, benchmark or external model. Sending tickers or trade-level rows is excluded (Condition 2), which also keeps the narrative from drifting into stock-specific commentary.

**COMPLIANT**, subject to Condition 2 holding the input set fixed.

### 3.3 Non-predictive output (§13.2 "prediction system")

The narrative describes months that have already happened (the current month only as "so far"). It must not forecast the coming months, set or imply a target, or extrapolate a trend ("on this pace…", "you are likely to…"). Like the debrief, this is structurally backward-looking, so the risk is framing, not function.

**COMPLIANT**, subject to Condition 1 and the output check in Condition 4.

### 3.4 Decision-support only (§13.1 human-in-the-loop, §13.3 signal generation)

The narrative gates nothing and triggers nothing. The boundary risk is prescriptive content: advice on trading behaviour ("trade less in volatile months"), sizing, strategy changes, or tax actions ("realise losses before 5 April"). Each would turn a summary into a recommendation that no §13 clearance covers, and tax-action advice would also be regulated-advice territory inside a financial report.

**CONDITIONAL** — Conditions 1, 4, 6 and 7.

### 3.5 Financial-report integrity (no named clause — see §2)

The Monthly P&L figures feed the Tax Year view, the CSV exports, month-end snapshots (`monthly_pnl_snapshots`, DS-20) and the reconciliation report. AI text must never enter any of these or be presented as part of the record.

**CONDITIONAL** — Condition 5.

---

## 4. Binding Conditions

Binding on ST-25's design and implementation, and to be confirmed in place at EPIC-04's DoQ sign-off.

1. **Backward-looking and descriptive only.** The narrative describes the months in the selected range. No forecast, projection, target, pace or trend extrapolation for any future period. The in-progress month may be described only as "so far".
2. **Fixed, aggregate-only input set.** The prompt receives only the fields listed in §1. Adding any other input (tickers, trade rows, journal text, unrealised estimate, market or benchmark data) needs this determination re-confirmed first.
3. **Verbatim numbers and correct direction, checked on the output.** Every number in the generated text must match a value passed in the prompt: a monthly field or a server-computed range figure. The model is instructed not to compute, estimate or restate from memory. Two server-side checks verify the text before it is shown or stored:
   - **Value check:** a numeric cross-check, reusing `debrief_service.numeric_cross_check` or an equivalent. As built, that check accepts a passed value at 0, 1 or 2 decimal places and ignores sign (`_allowed_number_strings`). So it proves that a figure came from the data, not that its direction is right.
   - **Direction check:** for every signed money figure (`realised_pnl_gbp`, `restated_diff_gbp`, range total, best and worst month) whose magnitude appears in the text, the sentence containing it must not describe a negative value with gain/profit wording, or a positive value with loss wording. A negative value must carry a minus sign or loss wording.
   
   A failure of either check is a Condition 3 failure.
4. **Non-prescriptive and non-forward-looking, checked on the output, with a deterministic fallback.** A server-side scan rejects prescriptive phrasing (the debrief's `scan_prescriptive` patterns), forward-looking phrasing ("will", "expect", "on track", "likely", "next month") and tax-advice phrasing ("tax liability", "allowance", "HMRC", "you owe", "harvest", "offset against"). The tax year may be named only as a label. On failure of Condition 3 or 4: regenerate once and re-check both. On a second failure, show a deterministic summary rendered by code from the same range figures, with no model text. Non-compliant text is never shown or stored. One regeneration covers both checks.

   **Test coverage before DoQ:** each output-side control must have backend tests before EPIC-04's DoQ sign-off; confirming them by code review is not enough. The controls are the value check, the direction check, the prescriptive/forward/tax scan, the regenerate-once path and the deterministic fallback. Each check needs at least one passing case and one failing case. There must also be one case where both attempts fail and the deterministic fallback is shown.
5. **Separate from the financial record (SRB-v1.7 advisory-only).** The narrative is never included in the PDF or CSV exports, month-end snapshots, the reconciliation report or any stored figure. It is never used to compute, alter or annotate a figure. The table's figures stay authoritative, and the section is placed so it cannot be mistaken for part of the table.
6. **Advisory framing.** The section carries the `AdvisoryBadge` (`design_system.md` §Shared UI Components) with the caption "Describes your recorded figures only. Not a forecast, recommendation or tax advice." The response payload carries `advisory: true`. The endpoint is added to `docs/specs/qa/ai_s13_boundary_test_suite.md`, with scenarios for D1–D4 and CI tests for D1 and D3, as that suite requires for every AI advisory endpoint.
7. **Optional, on request, dismissible, no action affordances.** The narrative is generated only when the user asks. There is no automatic, scheduled or background generation and no notification. The user can hide the section. Apart from Generate/Regenerate and Hide, the section has no buttons, links or prompts, and nothing that creates a plan, changes a setting or edits a record.
8. **Audit-logged with the check outcome.** Every model call is logged to `claude_audit_log` under its own feature name, with cost, tokens, `prompt_version`, `prompt_hash`, `response_length` and the pass/fail result of Conditions 3 and 4. ST-26's usage counter reads these rows. A fallback after a failed check is auditable.
9. **§13 compliance note in the generation service.** The service file carries a comment: "Monthly P&L narrative: descriptive, backward-looking, own aggregate figures only; verbatim-number, direction and prescriptive/forward/tax-language checks on output; no write to any figure, export or snapshot; §13 CONDITIONAL — docs/product/decisions/decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md."
10. **§13.5 roster.** The feature joins the §13.5 roster as CONDITIONAL in the same commit as this determination, and is re-attested on that cadence (first date 2027-02-06).
11. **Extensions need a new review.** Any extension that adds trade-level or ticker commentary, compares against a benchmark, looks forward, generates without a user request, or moves the narrative into an export or report document requires a fresh §13 review before it is built.

12. **Scope of this determination.** It clears the system-boundary question only. It does not stand in for any AI-content governance or security review. The AI endpoint security checklist (`stage4_backlog_slice_addendum.md` step 2) is owned by the Cybersecurity & Trust Lead and recorded separately.

---

## 5. Determination

**Determination: CONDITIONAL**

Own-data and non-predictive criteria are compliant: the narrative is a backward-looking description of the user's own aggregates. Determinism and decision-support are compliant under the established narrative-layer reading of §13.1, subject to output-side enforcement (Conditions 3 and 4) with test coverage, not prompt instructions alone. The financial-report question, which no §13 clause names, is controlled by keeping the text out of every record and export (Condition 5).

This is a confirmation, not a finding that a full §13 review is needed. ST-25 continues with `stage4_backlog_slice_addendum.md` steps 2 and 3 (AI endpoint security checklist; design decision record with Product Owner approval; `reports.md` update) before any implementation commit. ST-26 inherits this ordering.

---

## 6. Sign-Off

**Signed off by:** Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3)
**Date:** 2026-10-09
**Determination:** CONDITIONAL
**Comments:** Confirmed CONDITIONAL on the RISK-06 confirmation route; no full §13 review is needed. I searched all of `strategy_rules.md` §13 for the feature's subject terms. AI, machine learning, prediction, generation and automat hit only §13.2–§13.6, and narrative, report, financial, P&L and tax have no hits, so the clause table is complete and the absence of a financial-reporting clause is recorded, not argued away. The prompt input matches the row fields returned by `reports_service.get_monthly_pnl_report()`. The output-side controls build on `debrief_service.scan_prescriptive` and `numeric_cross_check`, which exist. Condition 3 now states that the numeric check tolerates rounding and ignores sign, and adds a direction check for signed money figures. Every control and the deterministic fallback must have tests before DoQ. Keeping the narrative out of every export, snapshot and figure (Condition 5, SRB-v1.7) is the control this role relies on most for AI text placed beside the tax-year record.

**Review record:** agent-mediated per `execution_prompt.md` §5.3 at the user's direction (2026-10-09). First pass: Blocked, with 2 blocking findings (the numeric check is sign-blind; no test-coverage requirement for the output checks) and 6 non-blocking ones. All 8 were applied. Second pass: Approved, with 2 wording fixes applied.
