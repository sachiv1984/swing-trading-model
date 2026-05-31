**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-31
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Backlog ref:** BLG-OPS-37
**Cycle:** 2026-05-31__release-v4.7 (ST-08)
**Gate verified:** BLG-OPS-36 (Claude API first monthly review) — completed 2026-05-28

---

# Anthropic API Tier Cost Assessment

**Review date:** 2026-05-31
**Reviewed by:** FinOps & Resource Architect
**Closes:** BLG-OPS-37

---

## 1. Background

BLG-OPS-36 (Claude API first monthly review) was completed in v4.2 (2026-05-28), covering 5 days of post-v4.0 launch usage. With actual usage data now available, this assessment performs the pricing tier comparison and defines the threshold at which a paid-tier upgrade becomes cost-effective.

**Data source:** `docs/ops/claude_cost_review_2026-05.md` (BLG-OPS-36)

---

## 2. Baseline Usage Data (from BLG-OPS-36)

| Metric | Value |
|--------|-------|
| Review period | 2026-05-22 – 2026-05-26 (5 days, post-launch) |
| Total API calls | 6 |
| Total tokens | 2,575 (1,372 input + 1,203 output) |
| Estimated total cost (5 days) | $0.007387 |
| Average cost per call | $0.0012 |
| Projected annual cost (current rate, 1.2 calls/day) | ~$0.54/year |
| Current daily rate | ~$0.0015/day |
| Current model | Claude Haiku 4.5 |

Usage is currently at very low volume — primarily thesis generation triggered by user action. No background processing or batch jobs.

---

## 3. Anthropic API Pricing Tiers

### 3.1 Free Tier

| Parameter | Value |
|-----------|-------|
| Monthly usage limit | None (pay-as-you-go) |
| Rate limits | Lower — default API rate limits for new accounts |
| Access | All Claude models (Haiku, Sonnet, Opus) |
| SLA / support | No uptime SLA; community support |
| Batch API discount | No |
| Prompt cache | Available (90% discount on cache reads) |

### 3.2 Claude Haiku 4.5 Pricing (current model)

| Component | Rate |
|-----------|------|
| Input tokens | $1.00 per 1M tokens ($0.000001/token) |
| Output tokens | $5.00 per 1M tokens ($0.000005/token) |
| Prompt cache read | $0.10 per 1M tokens (90% savings vs input) |
| Prompt cache write | $1.25 per 1M tokens |

### 3.3 Upgrade Path Considerations

Anthropic does not offer a traditional "paid tier" subscription distinct from pay-as-you-go usage. The pricing structure is usage-based. Upgrades to higher API rate limits or to an Anthropic business account unlock:
- Higher rate limits (tokens per minute, requests per minute)
- Enterprise SLA and dedicated support
- Custom contracts for high-volume usage

For practical purposes, the relevant decision is:
1. **Model upgrade** — moving from Haiku 4.5 to Sonnet 4.6 or Opus 4.8 for better quality at higher cost
2. **Rate limit upgrade** — relevant only if hitting default limits at current usage

---

## 4. Usage Threshold Analysis

### 4.1 Current vs Threshold Modelling

At current usage (1.2 calls/day, 2,575 tokens/call average):

| Scenario | Calls/day | Tokens/call | Monthly cost | Annual cost |
|----------|-----------|-------------|--------------|-------------|
| Current (baseline) | 1.2 | ~430 avg | ~$0.05 | ~$0.54 |
| Moderate adoption | 10 | ~430 | ~$0.40 | ~$4.80 |
| Active daily use | 30 | ~500 | ~$1.35 | ~$16.20 |
| Heavy use / team | 100 | ~500 | ~$4.50 | ~$54.00 |
| Scale trigger | 500 | ~600 | ~$24.00 | ~$288.00 |

Note: Token counts are based on the BLG-OPS-36 average (2,575 tokens / 6 calls ≈ 430 tokens/call). Heavier prompts (more trade history context) could push this to 600–1,000 tokens/call.

### 4.2 Model Upgrade Threshold

| Scenario | Haiku 4.5 | Sonnet 4.6 | Ratio |
|----------|-----------|------------|-------|
| Input rate | $1.00/1M | $3.00/1M | 3× |
| Output rate | $5.00/1M | $15.00/1M | 3× |
| Quality uplift | Baseline | Significantly better reasoning | — |
| Recommendation | Current | When thesis quality insufficient | — |

**Model upgrade threshold:** Consider Sonnet 4.6 when thesis quality becomes a limiting factor, not purely on cost grounds. At current volume, the cost difference is < $5/year — immaterial. The trigger is user-observed thesis quality, not cost.

---

## 5. Decision Framework

### 5.1 Current Recommendation

**No tier or model upgrade required at this time.**

Rationale:
1. Monthly cost is < $0.05 — negligible
2. Rate limits are not being approached (6 calls in 5 days)
3. Claude Haiku 4.5 is adequate for the thesis generation use case at current quality bar
4. The existing daily cost alert ($1.00/day threshold) provides a 667× buffer over current spend

### 5.2 Upgrade Triggers (When to Revisit)

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Monthly spend | > $5.00/month | Review model tier; consider Sonnet 4.6 for quality-sensitive use cases |
| Daily cost alert fires | > $1.00/day (any day) | Investigate spike cause; reassess if recurring |
| Thesis quality feedback | User reports poor thesis quality | Evaluate Sonnet 4.6 upgrade ($3/1M input vs $1/1M) |
| Call volume | > 100 calls/day sustained | Assess rate limit headroom; contact Anthropic for business tier |
| Monthly spend | > $50.00/month | Full cost-benefit review; consider enterprise contract |

### 5.3 Monitoring Cadence

The monthly review cadence established in `docs/ops/claude_cost_review_2026-05.md §5` (first Thursday monthly) is the correct vehicle for tracking progress toward these thresholds. No separate monitoring is required.

---

## 6. Prompt Caching Advisory

Prompt caching (BLG-OPS-36 §4 note) offers 90% savings on cache reads. If system prompts or strategy context are repeated across thesis generation calls, enabling prompt caching could reduce input token costs significantly. This is relevant when:
- Input tokens per call exceed 1,000 (indicating substantial repeated context)
- Monthly spend crosses $1.00/month

At current usage (avg ~229 input tokens/call), prompt caching is not cost-justified. Revisit when volume or prompt size increases.

---

## 7. BLG-OPS-37 Closure

BLG-OPS-37 marked COMPLETE in `claude/backlog/backlog.md` — 2026-05-31, cycle 2026-05-31__release-v4.7, ST-08 (EPIC-04).

---

## 8. Sign-Off

**Signed off by:** FinOps & Resource Architect
**Date:** 2026-05-31
**Decision:** **No upgrade required — current Haiku 4.5 pay-as-you-go adequate**
**Comments:** Based on BLG-OPS-36 monthly review data (6 calls, $0.007 total, 5-day post-launch window), Anthropic API cost is negligible and no tier or model upgrade is warranted. Upgrade thresholds defined: monthly spend > $5 triggers model review; > $50 triggers enterprise contract review. Daily cost alert ($1.00/day) provides adequate spike protection. BLG-OPS-37 closed.
