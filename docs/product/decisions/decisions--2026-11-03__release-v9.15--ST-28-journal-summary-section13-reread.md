Owner: Strategy Rules & System Intent Owner
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-05 (initial re-read, ESC-EXEC-20261105-02; corrected after the agent-mediated Director of Quality review: §13.2 is one sentence, and the briefing/chat check gap is stated)
Cycle: 2026-11-03__release-v9.15
Story: ST-28 (EPIC-04, BLG-GOV-194)
Escalation ref: ESC-EXEC-20261105-02

---

# §13 Boundary Re-Read: AI Journal Summary

**Feature:** `POST /ai/journal-summary`. It summarises the user's own entry and exit journal notes from closed trades, using an external model (Claude Haiku, `JOURNAL_SUMMARY_PROMPT_VERSION` v1.1).
**Review type:** a dated re-read of `strategy_rules.md` §13 against one shipped feature (`BLG-GOV-194`). It is a clarity check on the boundary language, not a fresh §13 review.
**Governance reference:** `claude/strategy/strategy_rules.md` §13 as at v1.24, read on 2026-11-05. v1.25 applies this record's outcome.
**AC reference:** `claude/cycles/2026-11-03__release-v9.15/stage4_backlog_slice.md#ST-28`
**Citation rule:** cite every §13 clause whose text names the feature's subject (§13 clause-citation rule, v2.61).
**Related rulings:**
- `ESC-EXEC-20261027-03` (A), v9.13 ST-18: the output-language check (prescriptive scan, plus wording that suggests changing stops, sizing or setups).
- `ESC-EXEC-20261030-02` (A′), v9.14 ST-15 (`BLG-AI-20`): five advisory phrasing forms.
- `ESC-EXEC-20261105-01` (A″), v9.15 ST-25/ST-27 (`BLG-AI-24`, `BLG-AI-26`): fixes for false positives and missed forms.
**Precedent:** `docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`, the daily briefing and chat review. It already describes a journal summariser as "analogous" to that narrative layer, but it never reviewed the endpoint itself.

---

## 1. What the Feature Does

- **Input:** the `entry_note` and `exit_note` text of closed trades, chosen by `trade_ids` or by a date range (`backend/routers/ai.py`, `fetch_journal_notes`).
- **Output:** 2–4 paragraphs of plain text. The prompt says: "Do not make investment recommendations. Describe what the notes record; do not suggest changing stops, position sizing or setups."
- **Output check:** every summary goes through `journal_summary_language_failures()`, which is the debrief's `scan_prescriptive` plus the stop, sizing and setup-change patterns. A summary that fails is regenerated once. If it fails again, the endpoint returns a code-written withheld message instead.
- **Writes:** one `ai_audit_log` row and one `claude_audit_log` row per model call. It writes no trade, position, plan, signal, stop or settings data (B-JS-03).
- **Use of the output:** display only. Nothing calculates from it, and nothing stores it as a recommendation.

## 2. Clauses Cited

No §13 clause names the journal summary, AI-written narrative or journal notes. The determination therefore rests on §13.1 and §13.2. §13.3 (gap risk), §13.4 (compliance recheck) and §13.6 (SI-02 gate history) do not name the subject. §13.5 is answered separately in §4 below.

| Clause | Text | Reading for the journal summary | Holds? |
|--------|------|---------------------------------|--------|
| §13.1 | "a deterministic decision-support engine" | The summary is not a decision, and no decision is computed from it. Signals, stops, sizing and exits stay deterministic. The summary describes text the user wrote. | Yes |
| §13.1 | "a single, explicit, human-designed strategy" | The summary changes no rule or parameter, and nothing reads it as one. | Yes |
| §13.1 | "human-in-the-loop by design" | The user asks for the summary, reads it, and acts on nothing through it. | Yes |
| §13.2 | "not … an automated trading bot", "not … a broker execution engine" | It has no trade or order side effects (B-JS-03). | Yes |
| §13.2 | "not … a discretionary or adaptive rule system" | This is the clause the three rulings relied on. If AI-written text tells the user to tighten stops, resize positions or change setups, it invites changes to the strategy's parameters outside §12's parameter governance. The output check withholds such text. | Yes, but only by inference (see §3) |
| §13.2 | "not … a machine-learning or AI-driven prediction system" | The summary predicts nothing. It describes past notes. | Yes |

## 3. Is the Boundary Language Unambiguous?

**No. It holds, but it is not stated.** §13.2 excludes a "discretionary or adaptive rule system". It does not say that AI-written text describing the user's own data must not suggest changing the strategy's parameters. Three separate rulings had to infer that exclusion from §13.2 (`ESC-EXEC-20261027-03`, `ESC-EXEC-20261030-02`, `ESC-EXEC-20261105-01`). The other AI narrative features have no stated basis for this either. The post-trade debrief and monthly P&L narrative run `scan_prescriptive`. The daily briefing and chat have no check against advice to change stops, sizing or setups: they check only tickers and stop times. A boundary that every new check must re-derive is not explicit enough to be a boundary.

## 4. §13.5 Re-Attestation Roster

The journal summary is an AI feature that shipped under a §13 determination: the rulings above, each answering §13.1 and §13.2. It is not on §13.5's roster, so the first semi-annual re-attestation on 2027-02-06 would skip it. **It belongs on the roster**, with this record as its clearance reference.

## 5. Outcome

**Clarified.** This is the Strategy Rules & System Intent Owner's ruling on `ESC-EXEC-20261105-02`, outcome (1), given in session by the user acting in that role on 2026-11-05. `strategy_rules.md` v1.25 makes the change. It is a case (c) named-file write, confirmed at the Sprint Planning seal on 2026-11-03, and it is documentation only.

1. §13.2 gains one sentence: AI-written text that describes the user's data (daily briefing, chat, post-trade debrief, monthly P&L narrative, journal summary) must not suggest changing stops, position sizing, setups or any other strategy parameter, because that would make the system a discretionary or adaptive rule system by another route. The sentence sets the boundary. It does not claim that every named feature already enforces it in code. The daily briefing and chat have no such output check today; `BLG-AI-29` tracks that gap.
2. §13.5 gains a roster row: "AI journal summary (`POST /ai/journal-summary`)", citing this record, cleared v9.13 and clarified v9.15.

No rule, parameter or live behaviour changes, so backtests and live trades stay comparable (§12.3).

**Sign-off:** Strategy Rules & System Intent Owner, 2026-11-05. The ruling was given in session by the user acting in that role (ESC-EXEC-20261105-02). This record was drafted by the Sprint Execution Engine.
