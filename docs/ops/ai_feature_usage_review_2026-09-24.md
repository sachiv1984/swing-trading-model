**Owner:** Head of Specs Team; PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-05 (created — ST-19, EPIC-04, `2026-09-30__release-v9.9`, BLG-GOV-356; 90-day review due 2026-09-24, conducted 2026-10-05 against production data)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# 90-Day AI Feature Usage Review

## Purpose

The v6.2 AI features (daily briefing, AI chat) shipped on 2026-06-25. Governance set a review 90 days later, due 2026-09-24, to assess adoption, cost per use and whether continued AI investment is justified (BLG-GOV-74 cadence; BLG-GOV-142's assessment criteria). Eight backlog items were gated on its outcome. This is that review, conducted 11 days late on 2026-10-05. The file is named for the gate date so `post_ship_closure.md` STEP 12.6's artefact check (`docs/ops/*ai*usage*review*<date>*.md`) recognises it.

Unlike the 2026-09-07 quarterly review (`docs/governance/ai_feature_usage_quarterly_review_2026-09-07.md`), which was code-based only because no live data was available, this review uses **real production usage data**.

## Data Source and Method

- **Source:** the production PostgreSQL database, queried read-only by the Product Owner on 2026-10-05 (the Sprint Execution sandbox has only a read-only staging credential, whose seeded data says nothing about real use — see `ESC-EXEC-20261001-02`).
- **Window:** 2026-06-25 (v6.2 ship) to 2026-10-05 — **102 days**, 15 calendar weeks.
- **Tables:**
  - `claude_audit_log` — one row per call for the 5 Claude-backed endpoints: daily briefing, chat, trade plan generation, setup thesis generation and trade debrief (call sites verified: `ai_service.py`, `gemini_service.py`, `debrief_service.py`).
  - `ai_audit_log` — the journal summary endpoint, which logs separately and records no cost.
  - `gemini_audit_log` excluded on purpose: it is a legacy dual-write of `claude_audit_log` for 2 endpoints and would double-count.

Queries run:

```sql
-- 1. Per-endpoint usage and cost
SELECT endpoint, model_id, COUNT(*) AS calls,
       COUNT(DISTINCT generated_at::date) AS active_days,
       MIN(generated_at)::date AS first_call, MAX(generated_at)::date AS last_call,
       ROUND(SUM(cost_usd)::numeric, 4) AS total_cost_usd,
       ROUND(AVG(cost_usd)::numeric, 6) AS avg_cost_per_call_usd,
       ROUND(AVG(input_tokens)) AS avg_input_tokens, ROUND(AVG(output_tokens)) AS avg_output_tokens
FROM claude_audit_log WHERE generated_at >= '2026-06-25'
GROUP BY endpoint, model_id ORDER BY calls DESC;

-- 2. Weekly trend
SELECT date_trunc('week', generated_at)::date AS week, COUNT(*) AS calls,
       ROUND(SUM(cost_usd)::numeric, 4) AS cost_usd
FROM claude_audit_log WHERE generated_at >= '2026-06-25' GROUP BY 1 ORDER BY 1;

-- 3. Journal summary
SELECT COUNT(*) AS calls, COUNT(*) FILTER (WHERE summary_produced) AS summaries_produced,
       COUNT(DISTINCT invoked_at::date) AS active_days,
       MIN(invoked_at)::date AS first_call, MAX(invoked_at)::date AS last_call,
       ROUND(AVG(duration_ms)) AS avg_duration_ms
FROM ai_audit_log WHERE invoked_at >= '2026-06-25';
```

## Results

### Usage and cost by feature

| Feature | Endpoint | Model | Calls | Active days | First / last use | Avg cost per call | Total cost |
|---|---|---|---|---|---|---|---|
| Daily briefing | `POST /ai/daily-briefing` | claude-sonnet-4-6 | 14 | 2 | 2026-06-29 / **2026-06-30** | $0.0080 | $0.1125 |
| AI chat | `POST /ai/chat` | claude-sonnet-4-6 | 10 | 3 | 2026-06-25 / **2026-08-17** | $0.0048 | $0.0482 |
| Trade plan generation | `POST /trade-plans/generate-plan` | claude-haiku-4-5 | 7 | 3 | 2026-07-02 / 2026-09-22 | $0.0017 | $0.0117 |
| Setup thesis | `POST /trade-plans/{plan_id}/generate-thesis` | claude-haiku-4-5 | 0 | 0 | never | — | — |
| Trade debrief | `POST /trades/{trade_id}/debrief` | claude-haiku-4-5 | 0 | 0 | never | — | — |
| Journal summary | `POST /journal-summary` | claude-haiku-4-5-20251001 | 0 | 0 | never | — | (not logged) |
| **Total** | | | **31** | | | | **≈ $0.17** |

Average tokens per call: briefing 339 in / 468 out; chat 344 / 253; plan generation 482 / 238.

### Weekly trend

| Week starting | Calls | Cost | Which features (reconciled against the per-feature table) |
|---|---|---|---|
| 2026-06-22 | 1 | $0.0039 | Chat (launch day) |
| 2026-06-29 | **23** | $0.1531 | 14 briefing, 8 chat, 1 plan generation |
| 2026-08-03 | 1 | $0.0017 | Plan generation |
| 2026-08-17 | 1 | $0.0054 | Chat (last chat use) |
| 2026-09-21 | 5 | $0.0085 | Plan generation |
| Other 10 weeks | 0 | — | — |

The weekly totals (31 calls, $0.1726) match the per-feature totals (31 calls, $0.1724) to within rounding.

## Findings

1. **Adoption is low and was concentrated at launch.** 74% of all AI calls (23 of 31) happened in the first full week after release. AI was used in 5 of 15 weeks; there were 7 calls in total from July onwards, and none at all in July.
2. **The daily briefing was trialled and dropped.** 14 calls on 2 days in launch week, none since 2026-06-30. Chat has been idle since 2026-08-17. Plan generation is the only feature in recent use (5 calls in the week of 2026-09-21).
3. **Half the AI features have never been used.** Setup thesis, trade debrief and journal summary have 0 calls since launch.
4. **Cost is not a constraint.** About $0.17 in 102 days. The Sonnet-backed features (briefing, chat) cost roughly 3–5× more per call than the Haiku ones, but at this volume the difference is immaterial. Cost per use: $0.0017–$0.0080.
5. **Usage has stabilised near zero**, not at a steady working level. The "usage patterns have stabilised" condition the gated items were waiting on is met in the literal sense, but it does not on its own show demand for more AI features.

**Data caveat:** `database.create_claude_audit_entry()` swallows any exception on insert (`except Exception: pass`). A failed log write is therefore silent, and these counts are a floor rather than a guaranteed exact figure. Logging demonstrably works (rows exist up to 2026-09-22, and the weekly and per-feature queries reconcile), so the figures are credible. This is relevant to BLG-GOV-141's logging completeness audit (see below). The Anthropic console's usage page is an independent cross-check if one is wanted.

## Continued-Investment Assessment

- **On cost:** continued investment is justified. AI spend is negligible.
- **On adoption alone:** the data does not show demand for further AI features. The existing ones are barely used.
- **Product Owner decision (2026-10-05, human):** remove the gate and allow the gated AI features to be built regardless of current engagement. In the Product Owner's words: *"remove the gate, no harm in building the items even if not used now. There is still low engagement but more features making it easier may help increase engagement."* This is a product judgement the Product Owner is entitled to make; the review records it alongside the data rather than overriding it.
- **Recommendation that follows from that decision:** sequence BLG-FEAT-60 (AI chat engagement metric) early, so the hypothesis that more features raise engagement can actually be measured, and compare against this review's baseline (31 calls / 102 days; 7 calls since July).

## Dispositions of the Gated Items

Recorded on each item in `claude/backlog/backlog.md` on 2026-10-05, under the Product Owner's authorisation as owner of that file.

| Item | Title | Disposition |
|---|---|---|
| BLG-FEAT-59 | AI-assisted monthly P&L narrative | **Gate cleared** — Product Owner decision; ready for release planning |
| BLG-FEAT-63 | P&L report AI narrative cost estimate | **Gate cleared** — follows BLG-FEAT-59 |
| BLG-FEAT-60 | AI chat engagement metric | **Gate cleared** — recommended to sequence early (see above) |
| BLG-FE-84 | AI chat UI interaction study protocol | **Gate cleared** |
| BLG-OPS-88 | Render dyno right-sizing review | **Unbundled and re-gated** — AI load (31 calls in 102 days) gives no dyno-sizing signal; now gated on a Render resource alert or a backend latency breach |
| BLG-GOV-140 | AI chat advisory §13 quarterly self-audit checklist | **Gate cleared** — its first-review date has passed; the checklist itself is still to be written, so the item stays open and is ready to schedule |
| BLG-GOV-141 | AI model output logging completeness audit | **Gate cleared** — still to be done; ready to schedule. Should cover the silent-failure caveat above |
| BLG-GOV-142 | AI feature ROI assessment at the 3-month mark | **Resolved** — this review is that assessment (adoption, cost per use, recommendation, Product Owner decision) |

The shared "90-Day AI Feature Usage Review Gate" statement added to `backlog.md` earlier the same day (ST-24) is removed in the same commit, as its own text requires once no item cites it. BLG-SPEC-65 carries a separate, stale copy of the adoption-window condition alongside a §13 condition; its adoption half is now met by this review, which is noted on BLG-GOV-361 (the item tracking that stale copy).

## Next Review

The quarterly AI usage review cadence (BLG-GOV-63/BLG-GOV-74) continues. The next review falls 90 days after this one: **2027-01-03**. It should repeat the same three queries so the results are directly comparable, and report whether the features built under the Product Owner's decision changed engagement.

## Sign-Off

- **Review and dispositions drafted:** Head of Specs Team; PMO Lead (agent-mediated, `execution_prompt.md` §5.3, Sprint Execution Engine on the user's direction), 2026-10-05.
- **Production data supplied by:** Product Owner, 2026-10-05.
- **Continued-investment decision and backlog edits authorised by:** Product Owner (human), 2026-10-05.
