**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-28
**Cycle:** 2026-05-27__release-v4.2

---

# Sprint Capacity — v4.2

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint capacity baseline | ~12–14 working days per sprint (revised 2026-05-27 per workforce_capacity.md) |
| Warn threshold | Effort > 14 days per sprint |
| Available FTE | Solo developer (evenings/weekends) |
| Skill constraints | ST-04/ST-06: live environment timing run requires Infrastructure & Operations Owner coordination; ST-05: actual API call volume/cost data access required |
| Source | `claude/roadmap/workforce_capacity.md` (revised 2026-05-27), `claude/cycles/2026-05-27__release-v4.2/release_plan.md ## Capacity Check` |

**Capacity WARN advisory (from release plan):** The release plan recorded a `WARN` for Sprint 2 (~7.75 days vs old ~8–10 day baseline). Under the revised capacity baseline of 12–14 days/sprint this is within capacity. Sprint 1 (~4.75 days) and Sprint 2 (~7.75 days with ST-10 included) are both comfortably within the 14-day warn threshold. No over-allocation exists. Product Owner acknowledgement recorded (capacity_warn_acknowledged = true from prior cycle state; confirmed valid under revised baseline).

---

## Item Effort Mapping

### Sprint 1

| EPIC | ST | Title | Effort Band | Est. Days | Delegation Class |
|------|----|-------|-------------|-----------|-----------------|
| EPIC-01 | ST-01 | Anthropic API Accountability & Key Security | XS | ~0.75 | delegated_decision |
| EPIC-01 | ST-02 | Anthropic Model Version Pinning Policy | S | ~0.5 | autonomous |
| EPIC-01 | ST-03 | Claude API Log Hygiene Policy | S | ~0.5 | delegated_decision |
| EPIC-02 | ST-04 | API Performance Baseline Update (OA-3) | S | ~0.5 | delegated_backend |
| EPIC-02 | ST-05 | Claude API First Monthly Cost Review | S | ~1.0 | delegated_decision |
| EPIC-02 | ST-06 | Claude API Thesis Generation Latency Baseline | S | ~1.0 | delegated_backend |
| **Sprint 1 total** | | | | **~4.75 days** | |

Sprint 1 verdict: **PASS** (4.75 days < 14-day warn threshold)

---

### Sprint 2

| EPIC | ST | Title | Effort Band | Est. Days | Delegation Class |
|------|----|-------|-------------|-----------|-----------------|
| EPIC-04 | ST-11 | SI-02 Sprint Planning Prerequisites Checklist | S | ~0.5 | autonomous |
| EPIC-04 | ST-12 | SI-04 Strategy Version Comparison Pre-Planning | S | ~1.0 | delegated_decision |
| EPIC-04 | ST-13 | v4.1 Staging Sign-Off Review & Backlog Namespace Audit | S | ~1.25 | autonomous |
| EPIC-03 | ST-07 | Claude API Audit Trail Implementation | M | ~2.0 | autonomous |
| EPIC-03 | ST-08 | AI Thesis API Contract Update for Claude | S | ~0.5 | autonomous |
| EPIC-03 | ST-09 | Claude API Playwright Mock Strategy | S | ~0.5 | autonomous |
| EPIC-03 | ST-10 | Claude API Prompt Caching Assessment (Optional) | S | ~0.5 | autonomous |
| **Sprint 2 total** | | | | **~6.25 days** | |

Sprint 2 verdict: **PASS** (6.25 days < 14-day warn threshold)

> **Note on ST-10 (BLG-BE-22):** Included in scope. Marked optional in the backlog slice — first candidate for deferral if Sprint 2 actual load exceeds estimates. Under the revised capacity baseline, inclusion is appropriate.

---

## Total Effort vs Capacity

| Sprint | Estimated Effort | Capacity Baseline | Verdict |
|--------|-----------------|-------------------|---------|
| Sprint 1 | ~4.75 days | 12–14 days | PASS |
| Sprint 2 | ~6.25 days | 12–14 days | PASS |
| **Total** | **~11.0 days** | **24–28 days across 2 sprints** | **PASS** |

---

## Conditional (Deferred) Items

No items deferred at planning time. ST-10 (BLG-BE-22) is in scope but flagged as the first deferral candidate if Sprint 2 load materialises higher than estimated.

> **Gate re-invocation:** If any item's gate condition is met during the sprint, do not add items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-05-27__release-v4.2 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
