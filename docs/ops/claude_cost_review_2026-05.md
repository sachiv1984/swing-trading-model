**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-28
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Claude API Cost Review — May 2026

---

## 1. Overview

This is the first monthly review of Claude API usage for thesis generation, covering the period from v4.0 launch (2026-05-22) through 2026-05-26. Data source: `gemini_audit_log` table (staging DB). The `claude_audit_log` table (added in v4.2 EPIC-03) was not yet live during this review period; `gemini_audit_log` is the authoritative source for pre-v4.2 Claude API calls.

**Review date:** 2026-05-28  
**Review period:** 2026-05-22 – 2026-05-26 (5 days, post-v4.0 launch)  
**Reviewed by:** FinOps & Resource Architect; Infrastructure & Operations Owner (agent-mediated)

---

## 2. Usage Data

| Metric | Value |
|--------|-------|
| Total API calls | 6 |
| Total input tokens | 1,372 |
| Total output tokens | 1,203 |
| Total tokens | 2,575 |
| First call | 2026-05-25 20:10:09 UTC |
| Last call | 2026-05-26 20:21:14 UTC |
| Estimated total cost (USD) | $0.007387 |

**Cost calculation** (Claude Haiku 4.5 rates — $1.00/1M input, $5.00/1M output):

| Component | Tokens | Rate | Cost |
|-----------|--------|------|------|
| Input | 1,372 | $1.00/1M | $0.001372 |
| Output | 1,203 | $5.00/1M | $0.006015 |
| **Total** | **2,575** | — | **$0.007387** |

**Average cost per call:** $0.0012 (< 0.2 cents per thesis generation)

---

## 3. Usage Context

The 6 calls span 2 days of active usage (2026-05-25 and 2026-05-26). No calls were recorded in the first 3 days after v4.0 launch (2026-05-22 to 2026-05-24), consistent with early post-launch staging usage only.

**Annualised projection** (based on current call rate, 1.2 calls/day):
- ~438 calls/year
- ~$0.54/year at current pricing and prompt sizes

Usage is extremely low and cost is negligible at this stage. Growth is expected as the thesis generation feature is adopted in production.

---

## 4. Daily Cost Threshold

The daily cost threshold is configured at **$1.00/day** via `AI_DAILY_COST_THRESHOLD` in `backend/config.py`. The `POST /ai/check-daily-cost` endpoint evaluates this threshold and sends a Telegram alert if exceeded. At current usage levels (~$0.001/day), the threshold provides a 1,000× buffer — appropriate for early-stage monitoring.

**Threshold setting:** $1.00/day — **no change required at this time**.

---

## 5. Monthly Monitoring Cadence

| Parameter | Value |
|-----------|-------|
| Review frequency | Monthly |
| Review trigger | First Thursday of each calendar month |
| Review owner | FinOps & Resource Architect |
| Data source | `claude_audit_log` (v4.2+); `gemini_audit_log` (pre-v4.2 history) |
| Report location | `docs/ops/claude_cost_review_YYYY-MM.md` |
| Escalation threshold | Monthly spend > $5.00 triggers review escalation to Head of Engineering |

**Next review due:** First Thursday of June 2026 (2026-06-05).

---

## 6. Cost Alert Threshold

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Daily alert (existing) | $1.00/day | ~1,000× current daily rate; catches unexpected spikes |
| Monthly escalation | $5.00/month | ~680× current monthly rate; triggers FinOps review if adoption accelerates sharply |

Both thresholds are deliberately conservative for the early adoption phase. These will be reviewed when `gemini_audit_log` (or `claude_audit_log`) shows sustained usage growth exceeding 100 calls/month.

---

## 7. BLG-OPS-30 Continuity Note

**BLG-OPS-30** (Gemini API usage first monthly review) was completed in v4.1 (2026-05-27) covering Gemini Flash API usage prior to the Gemini → Claude API switch. That item is archived.

This document supersedes BLG-OPS-30 for Claude API monitoring going forward. **BLG-OPS-36** (Claude API usage first monthly review) is satisfied by this report. Future reviews follow the cadence defined in §5.

---

## 8. Sign-Off

| Role | Reviewer | Date | Outcome |
|------|----------|------|---------|
| FinOps & Resource Architect | Agent-mediated | 2026-05-28 | APPROVED — cost negligible; cadence and thresholds defined |
| Infrastructure & Operations Owner | Agent-mediated | 2026-05-28 | APPROVED — `gemini_audit_log` data confirmed; daily alert threshold unchanged |

---

## 9. Document History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2026-05-28 | FinOps & Resource Architect | Initial report — first monthly Claude API cost review (v4.0 launch data) |
