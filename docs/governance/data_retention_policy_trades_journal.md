**Owner:** Data Model & Domain Schema Owner
**Class:** Policy Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-08 (ST-28, EPIC-04, v9.2, BLG-GOV-252 — policy documented)

---

# Data-Retention Policy — Closed-Trade and Journal Records

## 1. Scope

Closed trade records (positions that have reached a terminal state — closed, stopped out, or expired) and journal entries (free-text or structured notes attached to a trade or trade plan) held in the production database.

## 2. Policy

**Retain indefinitely — no scheduled deletion.** Rationale:
- Closed-trade records are the system's primary source of historical performance data (win rate, R-multiple distribution, strategy backtesting inputs per `metrics_definitions.md`). Deleting them would degrade every rolling-window metric that depends on sufficient historical sample size.
- Journal entries are user-authored reflective content tied to specific trades; there is no compliance or storage-cost driver identified today that would justify deletion, and deleting them would be a one-way, user-visible data loss with no compensating benefit.
- Data volume at current trading cadence is low (a single-portfolio system, not a multi-tenant brokerage) — storage cost is not a forcing function at any horizon currently foreseeable.

## 3. No Implementation Required Until Data Volume Warrants Action

This policy deliberately does not specify a deletion job, archival tier migration, or row-count trigger, because none is currently needed. A future trigger for revisiting this policy would be either:
- Database size or row count crossing a threshold that measurably affects query performance on the positions/journal tables (no such threshold has been observed), or
- A new compliance requirement (e.g. a data-minimisation obligation) not currently in force.

If either trigger is met, this policy must be revised — with an explicit retention period and archival mechanism defined at that time — before any deletion or archival job is implemented. Until then, "retain indefinitely, no action" is the policy in force.

## 4. Review Cadence

Revisit at the next lifecycle audit (`claude/audit.py`, every 3 cycles) as a standing check: has data volume crossed a performance-affecting threshold? If not, no action; if so, escalate to Data Model & Domain Schema Owner to define a revised policy.
