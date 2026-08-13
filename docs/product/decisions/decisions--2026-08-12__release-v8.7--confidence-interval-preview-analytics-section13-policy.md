**Owner:** Strategy Rules & System Intent Owner
**Class:** Operational Record (Class 3)
**Status:** Active — DETERMINATION RECORDED
**Last Updated:** 2026-08-13
**Cycle:** 2026-08-12__release-v8.7
**Story:** ST-20 (EPIC-07)
**Backlog ref:** BLG-GOV-305

**Write-scope note:** This determination is recorded as a standalone linked policy note per the story's own AC ("Determination recorded in `strategy_rules.md` §13 or a linked policy note") — `execution_prompt.md` §7 prohibits Sprint Execution from writing to `claude/strategy/strategy_rules.md` directly. `strategy_rules.md` §13 itself should gain a cross-reference to this document (matching the existing pattern at §13.5's feature-review table) at the next opportunity a routine with `claude/strategy/` write access runs — flagged, not actioned here.

---

# §13 Policy Determination — Confidence-Interval-Qualified "Preview" Analytics

## The Question

`BLG-GOV-305`: Arc 6 items (PS-01/PS-02-style) are gated on trade-count thresholds (50+/100+) before shipping. Would a **confidence-interval-qualified "preview" version below the gate** — explicitly labelled as statistically provisional, showing the same underlying descriptive statistic with an honest uncertainty caveat — remain §13-compliant? Could it offer earlier partial value without violating the deterministic/non-predictive boundary (§13.1/§13.2)?

## Determination: **Permitted, with conditions**

A confidence-interval-qualified preview of a retrospective descriptive statistic (win rate, average R, expectancy, profit factor — the PS-01/PS-02 class) does **not** violate §13.1/§13.2, subject to the four conditions in §3 below.

## 1. Reasoning against §13.1 (deterministic decision-support engine)

The underlying computation of a preview is **identical in kind** to the full, gated version — the same deterministic aggregate arithmetic (count, mean, ratio) over the same closed-trade rows, just applied to a smaller current sample. Reducing the sample size does not change the computation from deterministic to something else; a win rate over 12 trades is exactly as deterministic as a win rate over 100 trades (`wins / total`, computed identically). What changes with sample size is **statistical reliability**, not **computational nature**. §13.1 constrains what kind of system this is (deterministic vs. adaptive/predictive), not how confident a given deterministic output should be treated — that is a separate, legitimate statistical-communication question, answered by showing the confidence interval rather than by refusing to show the number at all below an arbitrary threshold.

## 2. Reasoning against §13.2 (not a machine-learning or prediction system)

A confidence interval on a retrospective statistic is not a forecast. It answers "how much would this number plausibly move if we had more data," not "what will happen next." This is the same category of honest-uncertainty communication used throughout descriptive statistics and polling (e.g. "52% ± 5%") — it does not predict a future trade outcome, does not adapt system behaviour, and does not introduce a machine-learning component. §13.2's prohibition targets systems that generate forward-looking inferences or adapt their own rules from data; a labelled-provisional descriptive statistic does neither.

**Explicit scope boundary — this determination does NOT extend to genuinely forward-looking analytics.** PS-03 (Monte Carlo Simulation) is materially different in kind: its output is a simulated *projection* of future outcome ranges, not a retrospective descriptive statistic, even though its execution is itself deterministic (same seed/inputs → same output). Whether a confidence-interval-qualified "preview" of PS-03 specifically would also be §13-compliant is **not decided by this determination** and would require its own separate assessment weighing the forward-looking nature of a simulated projection against §13.2's prediction exclusion — flagged as a distinct open question, not silently folded into this Permitted ruling.

## 3. Conditions

For any preview implementation to remain within this determination's Permitted scope:

1. **The confidence interval (or an equivalent honest uncertainty indicator) must always be shown alongside the point estimate below the full gate threshold** — never a bare number presented with the same visual confidence as the fully-gated version. Omitting this is the one change that would functionally misrepresent a wide-uncertainty small-sample statistic as a reliable one, which risks the same practical effect as an implicit recommendation even though the underlying math is unchanged.
2. **No default call-to-action or recommendation derived from the preview value** — matching the same no-default-CTA principle already established for the `gated` `DataState` variant (`design_system.md` §Shared UI Components, ST-21 this same cycle: "not user-actionable"). The preview is informational only; the human draws their own conclusion, per §13.1's human-in-the-loop principle.
3. **Explicit, specific provisional labelling** — state the actual current sample size and the full-gate threshold it falls short of (e.g. "Preview — based on 12 of the 50 trades needed for a stable reading"), not a vague generic disclaimer. This mirrors the precision already required of the `gated` variant's copy pattern ("states the gate condition... not a live progress count" — here, inverted: a preview *does* want to show the live count, specifically to contextualise the interval).
4. **This determination is scoped to the retrospective/descriptive analytics class only** (PS-01, PS-02, and any future feature of the same shape — closed-trade aggregate statistics). It does not pre-clear PS-03 (Monte Carlo Simulation) or any other genuinely forward-looking or adaptive feature — see the scope boundary in §2.

## 4. Relationship to existing gates

This determination does not itself change PS-01/PS-02's existing gate thresholds (50+/100+ trades) — those remain the bar for the **full, non-provisional** version. It clears the way for a *product decision* (not made here — that is Product Owner authority, not this §13 determination) about whether to build a preview variant at all, and if so, at what interim sample-size threshold it would first appear (e.g. "show a labelled preview from 10 trades onward, full unlocked version at 50"). That threshold-selection and prioritisation decision is out of this determination's scope; this determination only answers the compliance question that decision depends on.

## Sign-off

**Strategy Rules & System Intent Owner (agent-mediated, §5.3):** Confirmed — 2026-08-13. Determination: Permitted, with the four conditions in §3. Reasoning distinguishes computational determinism (unchanged by sample size) from statistical reliability (the actual variable at stake), and explicitly scopes the ruling away from genuinely forward-looking analytics (PS-03) rather than over-generalising a retrospective-statistics-specific finding to the whole Arc 6 feature set.
