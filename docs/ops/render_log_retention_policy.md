**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-31
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Backlog ref:** BLG-OPS-31
**Cycle:** 2026-05-31__release-v4.7 (ST-07)

---

# Render Log Retention Policy

**Review date:** 2026-05-31
**Reviewed by:** Infrastructure & Operations Owner
**Closes:** BLG-OPS-31

---

## 1. Background

As Arc 5 compliance data accumulates (SI-01 validation events, SI-03 red flag events, Claude API audit records), and Gemini audit logs are retained in database tables, it is operationally prudent to clarify Render's log retention boundaries and confirm whether the application's database audit tables provide sufficient durable audit trail independent of Render's platform logs.

This document records the policy review and the decision made by the Infrastructure & Operations Owner.

---

## 2. Render Log Retention — Current Plan

| Parameter | Value | Notes |
|-----------|-------|-------|
| Platform | Render (production and staging hosting) |  |
| Current plan tier | Starter / Indie (as of v4.0) | Render Starter plan for web services |
| Log retention window | **7 days** (Render default for Starter tier) | Render streams logs in real-time; retained logs viewable in dashboard for 7 days |
| Log types covered | Application stdout/stderr (FastAPI/Uvicorn output) | HTTP request logs, exception traces, startup/shutdown messages |
| Log export | Not configured (manual only via dashboard copy) | No automated log shipping to external store (S3, Datadog, etc.) |
| Log search | Available in dashboard within retention window | No long-term search capability beyond 7 days |

**Render's 7-day retention window means application stdout logs older than 7 days are not recoverable from the Render dashboard.** This is a structural constraint of the current plan tier and cannot be extended without upgrading to a paid Render plan that includes log drain or extended retention.

---

## 3. Database Audit Tables Assessment

The application maintains two primary audit tables that persist independently of Render platform logs:

### 3.1 claude_audit_log (Arc 5 AI thesis generation)

| Attribute | Value |
|-----------|-------|
| Table | `claude_audit_log` (added v4.2 EPIC-03) |
| Records | Every Claude API call: model, input/output token counts, cost estimate, request timestamp, success/error status |
| Retention | PostgreSQL database — no row-level expiry configured; rows persist indefinitely |
| Durability | Render PostgreSQL managed database — data survives Render service restarts and plan changes |
| Audit trail for | Claude API cost monitoring, thesis generation history, daily cost threshold evaluation |

**Assessment: DURABLE** — `claude_audit_log` provides a persistent, queryable record of all Claude API interactions. It is independent of Render's 7-day application log window.

### 3.2 red_flag_events (Arc 5 SI-03 override events)

| Attribute | Value |
|-----------|-------|
| Table | `red_flag_events` (added v3.8) |
| Records | Every override acknowledgement: ticker, event_type, severity, timestamp, rule_breach details |
| Retention | PostgreSQL database — no row-level expiry configured; rows persist indefinitely |
| Durability | Render PostgreSQL managed database — same durability as claude_audit_log |
| Audit trail for | Compliance behaviour tracking, override frequency analysis, Arc 5 compliance score |

**Assessment: DURABLE** — `red_flag_events` provides a persistent record of all override acknowledgements. It is independent of Render's platform logs and serves as the primary durable record for SI-01/SI-03 compliance audit purposes.

### 3.3 Other Relevant Tables

| Table | Purpose | Durable |
|-------|---------|---------|
| `trade_plans` | Trade plan lifecycle, entry/exit parameters | ✅ Yes |
| `trade_history` | Closed trade P&L, dates, outcomes | ✅ Yes |
| `positions` | Open position state | ✅ Yes |
| `settings` | Current strategy parameters | ✅ Yes |

All application data tables reside in the Render PostgreSQL managed database and are durable independent of Render's application log retention.

---

## 4. Gap Analysis

| Audit need | Covered by database tables | Covered by Render logs | Gap |
|------------|---------------------------|----------------------|-----|
| Claude API usage and cost | ✅ claude_audit_log | Partial (stdout) | No gap — database table authoritative |
| Override acknowledgements | ✅ red_flag_events | Not stored in logs | No gap — database table authoritative |
| Application errors / exceptions | ❌ No dedicated error table | ✅ (7 days only) | **Gap: errors older than 7 days unrecoverable** |
| HTTP request history | ❌ No request log table | ✅ (7 days only) | **Gap: request history older than 7 days unrecoverable** |
| Authentication events | N/A (no auth layer) | ✅ (7 days only) | Low risk — no auth model |
| Deployment events | ❌ No deployment log table | ✅ Render dashboard | Gap: no permanent deploy history in application |

---

## 5. Policy Decision

**Decision: Render logs + database tables are sufficient for current operational needs.**

**Rationale:**

1. **All compliance-relevant audit data is in the database.** The two tables that matter most for Arc 5 governance (claude_audit_log, red_flag_events) are durable, queryable, and independent of Render's 7-day window. There is no compliance risk from Render log expiry.

2. **Application error history beyond 7 days is not operationally required at current scale.** The system has no SLA requiring post-incident investigation of errors older than 7 days. Render's 7-day window is sufficient for timely incident response. If a post-mortem requires older context, trade and event tables provide behavioural evidence.

3. **Log drain (external log shipping) is not cost-justified at this time.** Render log drain to an external store (e.g., Datadog, Papertrail, AWS CloudWatch) would add cost and operational overhead. The risk this addresses (inability to query errors older than 7 days) is low given the application's current incident frequency and scale.

4. **Review trigger is defined.** If the application encounters recurring production incidents where post-7-day log access is needed, or if Render raises its log drain cost to an accessible threshold, log drain should be reconsidered. The monitoring cadence in `docs/ops/claude_cost_review_2026-05.md §5` (first Thursday monthly review) is an appropriate review point.

**Decision: No additional archiving required at this time.**

---

## 6. Conditions for Revisiting

This policy decision should be reconsidered if any of the following conditions are met:

1. A production incident is investigated where root-cause evidence requires logs older than 7 days
2. Render releases a free or low-cost log drain tier compatible with the current hosting plan
3. A compliance requirement (regulatory or contractual) is introduced that mandates longer application log retention
4. The application processes > 100 trades/month (sustained), at which point a formal operational audit framework may be warranted

---

## 7. BLG-OPS-31 Closure

BLG-OPS-31 marked COMPLETE in `claude/backlog/backlog.md` — 2026-05-31, cycle 2026-05-31__release-v4.7, ST-07 (EPIC-03).

---

## Sign-Off

**Signed off by:** Infrastructure & Operations Owner
**Date:** 2026-05-31
**Decision:** **Render logs + database tables sufficient — no additional archiving required**
**Comments:** All compliance-relevant audit data (AI thesis calls, override events) is stored in durable PostgreSQL tables independent of Render's 7-day application log retention. The 7-day window is adequate for operational incident response at current scale. Log drain is not cost-justified. Policy decision recorded. BLG-OPS-31 closed.
