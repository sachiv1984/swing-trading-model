**Owner:** Data Model & Domain Schema Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-03
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# `trade_plans.position_id` Historical Backfill — Scoping Document

## Purpose

`BLG-BE-52` (Product Owner decision, 2026-07-09) declined to backfill the 11 historical `trade_plans` rows left permanently unlinked (`position_id: null`) by the bug `BLG-BE-46` forward-fixed. That decision was a **disposition**, not a **design** — no backfill was ever actually scoped (technical approach, effort, risk), only declined on the strength of a prior engineering assessment (`BLG-BE-46` RISK-01: "no reliable ticker/time match exists"). This document is that scoping — it exists so that if circumstances ever change (e.g. the SI-02 gate remains permanently stuck and 11 additional linked rows become worth pursuing despite their capped value), a future decision-maker has an actual design to evaluate rather than re-deriving one from scratch, and so the current "no backfill" disposition is a documented trade-off rather than a closed door with no paper trail behind it.

**This document does not reopen or challenge BLG-BE-52's decision.** No backfill is implemented or recommended here. It is a scoping artefact only, per `ST-18`'s acceptance criteria.

## 1. Scope of the affected rows

11 `trade_plans` rows (baseline count as of `BLG-BE-52`, 2026-07-09) with `position_id IS NULL`, predating `BLG-BE-46`'s forward-fix (v6.8, `add_position()` auto-link). **This count should be re-confirmed via a live query (`SELECT COUNT(*) FROM trade_plans WHERE position_id IS NULL`) at implementation time, not assumed unchanged** — no new unlinked rows should accumulate going forward given the forward-fix, but this document does not itself re-verify the count live.

## 2. Why this is hard: no direct foreign-key path

`trade_plans` and `trade_history` have no direct relationship — `trade_plans.position_id` references `positions(id)`, and `trade_history` separately carries its own `position_id` reference to the same `positions` table (once a position closes, it typically becomes a `trade_history` row). A historical `trade_plans` row with `position_id: null` has no key linking it to any `positions` or `trade_history` row at all — the link has to be *inferred*, not looked up.

`trade_plans` carries no entry price, entry date, or share count of its own (per `docs/specs/data_model.md` §trade_plans schema) — only `ticker`, `market`, `created_at`, and narrative/reasoning fields (`setup_thesis`, `entry_rationale`, etc.). This rules out any exact-match approach (e.g. matching on price + date + shares, as could be done for two rows that both independently record the same trade's mechanics). The only usable signal is `(portfolio_id, ticker, market)` plus **temporal proximity** between `trade_plans.created_at` (when the plan was written, normally shortly before entry) and `trade_history.entry_date` / `positions.entry_date` (when the position was actually opened).

## 3. Technical approach (if ever undertaken)

**Not an automated backfill.** Per `BLG-BE-52`'s own rationale — writing uncertain fuzzy-matched links into `position_id` risks trading a visible, honest gap for silent wrong data, which is a worse outcome for a gate (SI-02) specifically about strategy-adherence integrity. Any future approach must preserve that principle: **candidate generation with mandatory human review**, never a blind write.

1. **Candidate generation query:** for each unlinked `trade_plans` row, find `positions`/`trade_history` rows in the same `portfolio_id` with the same `ticker` (and `market`, if populated on both sides) whose `entry_date` falls within a configurable window of the trade plan's `created_at` (e.g. ±7 days — a trade plan is normally written same-day-to-a-few-days before entry, per the existing product convention of writing a plan ahead of execution).
2. **Ambiguity classification:** for each unlinked `trade_plans` row, the candidate query returns 0, 1, or 2+ matches:
   - **0 candidates:** no plausible link exists — leave `position_id: null` permanently, no further action.
   - **Exactly 1 candidate:** a plausible single match — still not auto-applied; surfaced for human confirmation (see step 3).
   - **2+ candidates:** genuinely ambiguous (e.g. the same ticker traded twice in the matching window) — cannot be resolved by this heuristic at all; requires the human reviewer to use judgment (thesis text content, if any, may help) or accept as unresolvable.
3. **Human review UI (or, at minimum, an admin script with a review CSV/report — no new UI is implied as required):** present each single-candidate and multi-candidate row to a human (Product Owner or Head of Engineering) with the trade plan's `setup_thesis`/`entry_rationale` text alongside the candidate position(s)' ticker/entry_date/entry_price, for a manual accept/reject decision per row. Only human-confirmed links are written.
4. **Write path:** a one-off, single-use admin script (not a recurring job, not a new API endpoint) that applies only the human-confirmed `(trade_plan_id, position_id)` pairs via a direct `UPDATE trade_plans SET position_id = %s WHERE id = %s`, run once, then retired — mirroring the "one-off admin script" framing already used in `BLG-BE-52`'s own scope note.

## 4. Effort estimate

| Step | Effort |
|------|--------|
| Candidate generation query + ambiguity classification script | XS (2–4 hours) — a single read-only SQL query against existing tables/columns, no schema change |
| Human review pass (11 rows, by definition a small, bounded set) | XS (30–60 minutes of human time, not engineering time) |
| One-off write script + execution + verification | XS (1–2 hours, including a dry-run mode that prints proposed updates without applying them) |
| **Total** | **S (≤1 day)**, the large majority of which is engineering time for the candidate/write scripts; the human review step is fast precisely because the row count (11) is small and bounded — this would not scale the same way to a much larger historical gap |

## 5. Risk of a future backfill

- **Primary risk (unchanged from `BLG-BE-46`'s original RISK-01 and `BLG-BE-52`'s rationale): false-positive links.** Even with human review, a plausible-looking single-candidate match could be wrong (e.g. the user opened and closed two similar positions in the same ticker close together, and the trade plan actually belonged to the other one). A human-confirmed but factually wrong link is *more* dangerous than a `null`, because it looks authoritative to any downstream reader (including the SI-02 gate's "linked closed trades" count) — the null at least signals "we don't know," while a wrong link signals false confidence.
- **Capped value, unchanged from `BLG-BE-52`:** at most 11 additional linked rows, against SI-02's 20-linked-closed-trade gate threshold. Even a fully successful backfill of all 11 would not by itself clear the gate (current live count remains 0/20 as of this cycle's `current_roadmap.md` structured field) — the effort does not buy gate clearance on its own, only incremental progress toward it.
- **One-off script risk:** a hand-run `UPDATE` script against production, even scoped to ≤11 rows with human-confirmed input, carries the standard one-off-script risks (wrong `WHERE` clause, wrong environment) — mitigated by the dry-run mode named in §3 step 4, which is a hard requirement for any future implementation of this design, not optional.
- **Opportunity cost:** engineering time spent on this (even at S/≤1 day) is time not spent on `BLG-FE-109`-style forward improvements (making linkage the path of least resistance for new plans), which `BLG-BE-52`'s own rationale already identified as the higher-value investment.

## 6. Disposition

**No change to `BLG-BE-52`'s "no backfill" decision.** This scoping exists so that decision is now backed by an actual design-and-risk assessment rather than resting solely on the original RISK-01 prose — if the calculus ever changes (e.g. a much larger future data-integrity gap makes fuzzy-match-with-human-review tooling worth building anyway, and this backfill becomes a cheap incremental add-on to that tooling), this document is the starting point, not a re-derivation from zero.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Data Model & Domain Schema Owner role — §5.3)
- Date: 2026-08-03
- Comments: Reviewed the proposed candidate-generation approach against `trade_plans`'/`trade_history`'s actual schema (`docs/specs/data_model.md`) — confirmed no exact-match field exists (no price/shares on `trade_plans`), correctly scoping the approach to fuzzy ticker+temporal matching with mandatory human review, consistent with `BLG-BE-52`'s original integrity rationale. Effort estimate (S, ≤1 day) is proportionate to an 11-row, human-reviewed, one-off script.
