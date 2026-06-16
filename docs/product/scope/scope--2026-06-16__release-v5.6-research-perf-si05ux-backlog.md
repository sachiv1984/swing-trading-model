**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Release:** v5.6
**Cycle:** 2026-06-16__release-v5.6
**Last Updated:** 2026-06-16
**Supersession note:** (completed at Post-Ship Closure)

---

# Scope Document — v5.6

**Theme:** Research Performance, SI-05 UX Improvements & Backlog Clearance

## Items in scope

| S2-ID | Backlog item | Priority | Effort | EPIC |
|-------|-------------|----------|--------|------|
| S2-01 | BLG-FE-73 — Add deep links from SI-05 digest to relevant app screens | P2 | S | EPIC-01 |
| S2-02 | BLG-FE-74 — Clarify N/A pass rate reason in SI-05 digest message | P3 | XS | EPIC-01 |
| S2-03 | BLG-OPS-22 — Research data caching layer | P2 | M | EPIC-02 |
| S2-04 | BLG-OPS-62 — Investigate GET /portfolio/concentration-status high latency | P3 | S | EPIC-02 |
| S2-05 | BLG-OPS-63 — Investigate GET /portfolio/red-flag-journal high latency | P3 | S | EPIC-02 |
| S2-06 | BLG-OPS-64 — Investigate GET /analytics/behavioural-drift high latency | P3 | S | EPIC-02 |
| S2-07 | BLG-GOV-106 — PT-04 trade count gate re-verification | P1 | S | EPIC-03 |
| S2-08 | BLG-QA-45 — Arc 5 QA completion criteria definition | P2 | S | EPIC-03 |
| S2-09 | BLG-QA-49 — Arc 5 test scenario completeness assessment | P2 | S-M | EPIC-03 |
| S2-10 | BLG-OPS-65 — Anthropic API cost 14-cycle trend analysis | P3 | S | EPIC-03 |
| S2-11 | BLG-FE-64 — RFJ visual design review pre-brief [CONDITIONAL — gate 2026-06-21] | P2 | S | EPIC-01 |

**Firm items: 10 (S2-01 through S2-10)**
**Conditional items: 1 (S2-11 — gate: SI-03 live ≥30 days, clears 2026-06-21)**

## Items explicitly deferred

| Item | Reason |
|------|--------|
| BLG-GOV-74 — AI feature quarterly review | Gate: first review due 2026-08-29 (3 months post v4.0); too far out |
| BLG-GOV-122 — strategy_rules.md §11 parameter annual review | Gate: requires 12 months of data; not yet due |
| BLG-QA-55 — SI-02 Playwright scaffold readiness | Gate: ≥20 closed trades (not met) |
| All Arc 4/5/6 gated features | Data density gates not met (trade count, journal history) |
| BLG-FE-41 — RFJ visual design review (full) | Prerequisite: BLG-FE-64 pre-brief must complete first |
