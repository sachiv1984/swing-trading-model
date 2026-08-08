**Owner:** FinOps & Resource Architect
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-08
**Cycle:** 2026-08-07__release-v8.4 (ST-24 — BLG-OPS-72)

---

# AI API Cost Model — Arc 4 Journal Intelligence

## 1. Background

Arc 4 (`docs/product/arc4_data_requirements.md`) defines five journal-intelligence features (PO-01 through PO-05): Plan vs Reality comparison, AI-context pre-entry snapshots, an AI Journal, and PO-04/PO-05 qualitative pattern detection. None of these are built yet — Arc 4 remains a data-requirements capture document, not an implemented feature set (per that document's own scope note).

This model estimates the incremental Anthropic API cost Arc 4's AI-driven components would add, ahead of any implementation decision, so cost is a known input to Arc 4 sprint planning rather than discovered after the fact — the same reasoning `docs/ops/anthropic_api_tier_assessment.md` (BLG-OPS-37) applied to the existing thesis-generation feature.

**No live usage data exists for Arc 4 features** — they are unbuilt. This is a projection model, not a measured trend (contrast `docs/ops/anthropic_api_cost_trend_2026.md`, which measures the shipped thesis-generation + daily-cost-check features against real invocation counts). All volume figures below are estimates derived from the closest already-shipped analogue (AI thesis generation) and should be re-baselined against `claude_audit_log` once any Arc 4 feature ships.

---

## 2. Which PO-01–PO-05 components are AI-driven

| Feature | AI-driven? | Rationale |
|---------|-----------|-----------|
| PO-01 — Plan vs Reality structured comparison | **No** | Per `arc4_data_requirements.md` §3.1–3.2, this is a calculated/deterministic service (numeric planned vs. actual values, e.g. `stop_discipline`) — no narrative generation or LLM call implied by the spec. $0 incremental AI cost. |
| PO-02/PO-03 — Pre-entry state snapshot + AI context inputs | **Yes** | §3.3–3.4 explicitly frame `regime_at_open`/context fields as "AI context for [PO-03] AI Journal" — this is the first feature that actually invokes the model. |
| PO-03 — AI Journal | **Yes** | Narrative/reflective generation over trade history + context snapshot — the direct Arc 4 analogue of the existing `POST /trade-plans/{plan_id}/generate-thesis` call. |
| PO-04/PO-05 — Qualitative annotations / pattern detection | **Likely** | §3.5 and §4's P3 fields (`thesis_confirmed`, `exit_quality`) describe pattern detection across a trade history window — plausible as either an LLM call per trade or a periodic batch summarisation call. Not yet specified precisely enough to size independently; folded into the AI Journal estimate below as a shared per-trade-close invocation until PO-04/PO-05 gets its own spec. |

**Only PO-03 (AI Journal, covering PO-02/PO-03/PO-04/PO-05's shared invocation) carries a modelled AI cost.** PO-01 is excluded as non-AI.

---

## 3. Pricing baseline (unchanged since v4.1, confirmed current per BLG-OPS-65 v5.6 review)

| Input | Value |
|-------|-------|
| Model | Claude Haiku 4.5 (no upgrade trigger crossed per BLG-OPS-37's $5/month threshold — see §5) |
| Input tokens | $1.00 / 1M tokens |
| Output tokens | $5.00 / 1M tokens |

---

## 4. Volume estimate — closest shipped analogue

AI thesis generation (`POST /trade-plans/{plan_id}/generate-thesis`) is user-triggered once per trade plan created and is the only comparable per-trade AI invocation shipped to date. `anthropic_api_cost_trend_2026.md` (14-cycle trend, v4.4–v5.5) is used as the volume baseline:

| Metric | Value (source) |
|--------|-----------------|
| Baseline invocation rate | ~1.2 calls/day (BLG-OPS-36/37 baseline, confirmed still representative at BLG-OPS-65) |
| Baseline per-call cost | ~$0.0012 (BLG-OPS-37; source review window totalled 2,575 tokens across 6 calls — ~1,372 input + ~1,203 output — i.e. ~429 avg tokens/call, consistent with the ~430 tokens/call figure independently stated in `anthropic_api_cost_trend_2026.md`) |
| Baseline projected annual cost (thesis generation alone) | ~$0.54/year |

**Arc 4 AI Journal projection:** Modelled as a second per-trade-close invocation alongside thesis generation (one thesis call at plan open, one AI Journal call at trade close) — same order of magnitude, since both are single-call, single-trade, narrative-generation-shaped invocations against the same token-budget class of prompt (structured trade context in, short narrative out).

| Scenario | Assumption | Est. monthly cost | Est. annual cost |
|----------|-----------|--------------------|-------------------|
| Conservative (current volume) | 1 AI Journal call per closed trade, same ~2,575 avg tokens/call as thesis generation, ~1.2 trades/day | ~$0.045/month | ~$0.54/year |
| Growth (3x trade volume) | Same per-call cost, ~3.6 trades/day (plausible if journal use increases trading cadence or a backfill pass is run against existing closed trades) | ~$0.13/month | ~$1.62/year |
| Backfill one-off | One-time batch run of AI Journal against all historically closed trades (retroactive journaling) — sized at ~200 closed trades (rough order-of-magnitude, not a verified count) at ~2,575 tokens/call | ~$0.24 one-time | n/a (one-time, not recurring) |

All three scenarios are **well under the $5/month BLG-OPS-37 upgrade-tier threshold** individually and combined — Arc 4, on this model, does not by itself justify a pricing-tier change.

---

## 5. Combined projection (existing features + Arc 4 AI Journal)

| Component | Current annual cost | + Arc 4 AI Journal (conservative) | + Arc 4 AI Journal (growth) |
|-----------|---------------------|-------------------------------------|-------------------------------|
| Thesis generation + daily cost check (shipped) | ~$0.55/year (BLG-OPS-65 trend) | — | — |
| Arc 4 AI Journal (projected) | — | +~$0.54/year | +~$1.62/year |
| **Total** | **~$0.55/year** | **~$1.09/year** | **~$2.17/year** |

Even the growth scenario combined total (~$2.17/year, ~$0.18/month) remains roughly 27x below the $5/month upgrade threshold. **No pricing-tier action is implied by Arc 4 at any modelled volume.**

---

## 6. Cost controls identified

1. **Reuse the existing daily-cost-check pattern.** `POST /ai/check-daily-cost` (v4.1) already provides an automated ceiling check; extend its scope to include AI Journal invocations rather than building a second monitoring path.
2. **Cap backfill scope.** If a retroactive AI Journal backfill against historically closed trades is implemented (§4 "Backfill one-off" scenario), gate it behind an explicit one-time admin action rather than an automatic migration — a few hundred trades is cheap, but an unbounded backfill against a much larger future trade history should not run unattended.
3. **No model upgrade required.** Haiku 4.5 remains appropriate for both existing and Arc 4 narrative-generation call shapes (short structured-context-in, short-narrative-out) — this class of call does not need a higher-capability model tier.
4. **Re-baseline before shipping, not after.** Because §4's volume figures are estimated (no Arc 4 feature has real usage data yet), the first sprint that implements PO-03 should re-run this model against the actual prompt design (real token counts) before merge, the same way `claude_audit_log`-sourced trend analysis superseded the original BLG-OPS-37 5-day estimate once real data existed.

---

## 7. Review

**Reviewed by:** FinOps & Resource Architect (agent-mediated sign-off, per `claude/system/execution_prompt.md` §5.3 — no live production data was required for this projection; it is derivable entirely from shipped-feature trend data already on record in `docs/ops/anthropic_api_cost_trend_2026.md` and `docs/ops/anthropic_api_tier_assessment.md`).

**Conclusion:** Arc 4's AI-driven component (AI Journal, PO-02/03/04/05's shared invocation) is projected at $0.54–$1.62/year incremental cost at current-to-3x trade volume, well within the existing $5/month tier threshold. No cost blocker exists for Arc 4 sprint planning to proceed on this basis. Re-baseline against real usage once PO-03 ships (§6.4).
