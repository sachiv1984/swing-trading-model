**Owner:** Financial Reporting & Records Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-08 (ST-23, EPIC-04, v9.11, BLG-FEAT-63 — estimate produced before ST-25 is built)
**Source:** ST-23 (`BLG-FEAT-63`), EPIC-04, cycle `2026-10-08__release-v9.11`
**Feeds:** ST-25 (`BLG-FEAT-59`, AI-assisted monthly P&L narrative): the cost-gating input to its AI endpoint security checklist (`docs/specs/security/ai_endpoint_security_checklist.md`)

---

# AI Monthly P&L Narrative — Cost Estimate

## Purpose

ST-25 adds an optional AI-written narrative to the Monthly P&L report. This estimate gives the expected cost per generation and per month before it is built, so the AI endpoint security checklist can set its cost gate on real numbers. The gate (`BLG-FEAT-59`'s adoption window) was removed by Product Owner decision on 2026-10-05, so the estimate is produced now, ahead of the build, as the sprint plan requires.

ST-25's design is not yet fixed (its §13 determination and design record come first), so the assumptions below are stated explicitly. They should be checked against the built prompt and re-run once the feature has a month of real audit-log data.

## Inputs

**Prices** (per million tokens, the rates the code already uses in `debrief_service.py` and `ai_service.py` for `claude_audit_log.cost_usd`):

| Model (pinned ID, `backend/ai_models.py`) | Input | Output |
|---|---|---|
| Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) | $1.00 | $5.00 |
| Claude Sonnet 4.6 (`claude-sonnet-4-6`) | $3.00 | $15.00 |

**Token profile per generation (assumed):**

| Part | Tokens | Basis |
|---|---|---|
| System prompt (advisory framing, §13 rules, no-prediction and verbatim-number rules) | ~450 | The debrief focus-area system prompt is about 400 tokens and carries the same kind of rules |
| Monthly P&L data (rolling 12–13 months: realised P&L, trade count, win rate, fees, restatement flags) | ~600–1,200 | About 50–90 tokens per month row in a compact table |
| **Input total** | **~1,050–1,650** | Use 1,650 as the planning figure |
| Narrative output (one or two short paragraphs) | ~250–400 | The daily briefing averages 468 output tokens for a summary plus actions (2026-09-24 usage review) |

**Retry factor:** if ST-25 adopts the debrief's output-side check (numeric cross-check and prescriptive-language scan, regenerate once on failure), a failing first attempt costs a second call. Worst case: 2 calls per generation.

## Cost per Generation

| Model | Typical (1,650 in / 400 out) | Worst case (2 calls) |
|---|---|---|
| Haiku 4.5 | 1,650 × $1/M + 400 × $5/M = **$0.0037** | **$0.0073** |
| Sonnet 4.6 | 1,650 × $3/M + 400 × $15/M = **$0.0110** | **$0.0219** |

## Monthly Cost by Usage Scenario

The narrative is generated on request from the Monthly P&L view. The scenarios assume each generation is a fresh model call (no caching):

| Scenario | Generations / month | Haiku 4.5 | Sonnet 4.6 | Basis |
|---|---|---|---|---|
| Current adoption | ~3 | $0.01–0.02 | $0.03–0.07 | All six AI features together averaged about 9 calls a month in the 102 days to 2026-10-05, 74% of them in launch week |
| Monthly review habit | ~10 | $0.04–0.07 | $0.11–0.22 | One look after each month closes, plus a few regenerations |
| Heavy use | ~120 (4 a day) | $0.44–0.88 | $1.32–2.63 | Upper bound for one user |
| Runaway (rate limit at 10/min/IP, sustained 1 hour) | 600 in one hour | $2.19–4.38 | $6.57–13.14 | What the rate limit alone allows in an hour; the daily cost alert (`POST /ai/check-daily-cost`, $1.00 threshold) fires well before this |

For scale: the whole AI feature set cost about $0.17 in its first 102 days.

## Recommendation for ST-25's Cost Gate

1. **Model: Haiku 4.5.** Narrative over already-computed figures does not need Sonnet's reasoning, and Haiku costs about a third as much. The debrief, the nearest precedent (single-subject, number-heavy prose with a verbatim-number check), already uses Haiku.
2. **Cache one narrative per month and data version.** Store the generated text against the month and a hash of its input figures, and return the stored text on later views. Regenerate only on an explicit Regenerate action or when the month's figures change (a restatement). This makes cost scale with distinct months viewed, not page views, and keeps the "current adoption" and "monthly review" scenarios below $0.10 a month.
3. **Rate limit at 10 requests per minute per IP**, the same as `POST /ai/daily-briefing`.
4. **Log every call to `claude_audit_log`** (cost, tokens, `prompt_version`, compliance result, and the `prompt_hash` / `response_length` columns added by ST-06), so the existing daily cost alert and `GET /ai/monthly-cost-by-feature` cover it with no new monitoring. ST-26's usage counter reads the same rows.
5. **No new budget line.** At the recommended settings, expected spend is under $0.10 a month and the heavy-use bound is under $1 a month, inside the existing $1.00 daily alert threshold. Revisit at the 2027-01-03 AI feature usage review (ST-28) with real data.

## Re-estimation Trigger

Re-run this estimate if ST-25's built prompt exceeds 2,500 input tokens, if it uses Sonnet, or if real monthly spend for the narrative endpoint passes $0.50 in any calendar month (visible in `GET /ai/monthly-cost-by-feature`).
