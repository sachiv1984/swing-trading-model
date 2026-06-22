# Sprint Capacity — 2026-06-22__release-v6.1

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-22
**Cycle:** 2026-06-22__release-v6.1

---

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | ~3 weeks (2 sprints of ~1.5 weeks each) |
| Available FTE | 1 (solo developer, evenings/weekends) |
| Capacity baseline | ~12–14 working days/sprint (revised 2026-05-27, workforce_capacity.md) |
| Warn threshold | Effort > 14 days/sprint |
| Total window | ~20–45 hrs available across 2-sprint window |
| Skill constraints | None scarce — all stories autonomous or delegated_frontend (reclassified autonomous); sole operator |

_Source: `claude/roadmap/workforce_capacity.md` (effective 2026-05-27); `claude/cycles/2026-06-22__release-v6.1/release_plan.md ## Capacity Check`_

---

## Item Effort Mapping

### Sprint 1

| EPIC | Story | Title | Effort | Type |
|------|-------|-------|--------|------|
| EPIC-01 | ST-01 | Release planning: Design Gate Required flag | S (~0.5 day) | G |
| EPIC-01 | ST-02 | Sprint planning: Design Gate hard gate at preflight | S (~0.5 day) | G |
| EPIC-03 | ST-06 | Portfolio sector heat-map visualization | M (~2–3 days) | U |
| EPIC-03 | ST-07 | Trade gate proximity indicator on dashboard | S (~0.5 day) | U |
| EPIC-04 | ST-08 | Setup Quality Score — backend engine (PT-04) | S (~1–2 days) | U |

**Sprint 1 estimated effort: ~5–7 hrs**
**Sprint 1 G+D+P%: 2/5 = 40%** (at Skill-Silo ceiling; compliant)

### Sprint 2

| EPIC | Story | Title | Effort | Type |
|------|-------|-------|--------|------|
| EPIC-01 | ST-03 | Governance overhead ceiling metric and accountability mechanism | S (~0.5–1 day) | G |
| EPIC-02 | ST-04 | Register morning-briefing.spec.js and screener-quality.spec.js in playwright.yml | XS (<1 hour) | D |
| EPIC-02 | ST-05 | Add PATCH /trades/{id}/costs to api_performance_baseline.md | XS (<1 hour) | D |
| EPIC-04 | ST-09 | Setup Quality Score — frontend display (PT-04) | S (~1–2 days) | U |

**Sprint 2 estimated effort: ~3–5 hrs**
**Sprint 2 G+D+P%: 3/4 = 75%** ⚠ above 40% Skill-Silo ceiling — structural limitation (see note below)

---

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total firm stories | 9 |
| Total estimated effort | ~17–29 hrs across 2-sprint window |
| Available capacity (2-sprint) | ~20–45 hrs |
| Assessment | Within 2-sprint capacity — **WARN (phasing required)** |
| Over-allocation | No — fits within 2-sprint window; capacity_warn_acknowledged = true (PO, 2026-06-22) |

---

## Skill-Silo Ceiling Advisory

**Sprint 1:** G+D+P% = 2/5 = 40% — at ceiling, compliant. ✅

**Sprint 2:** G+D+P% = 3/4 = 75% — above 40% ceiling. ⚠

**Structural root cause:** This release contains 5 G+D stories (ST-01, ST-02, ST-03, ST-04, ST-05) and 4 U stories (ST-06, ST-07, ST-08, ST-09). No 2-sprint arrangement can achieve ceiling compliance in Sprint 2 while completing all 5 G+D stories. The ceiling-optimal arrangement (Sprint 1 at 40%) is chosen; Sprint 2 overage is acknowledged as a structural constraint of this release's composition, not a planning failure. Product Owner accepted at capacity acknowledgement (2026-06-22).

---

## Gate-Conditional Deferred Items

No items deferred at planning — all 9 stories included as firm scope per Product Owner decision (2026-06-22). EPIC-04 (ST-08, ST-09) reclassified from conditional to firm: feature handles gate_not_met state gracefully per AC-03 in both stories; score path activates automatically when ≥20 closed trades (current: 15, projected: ~2026-07-02). No execution gate blocking story start.

> **Gate re-invocation:** No deferred items remain. If a previously parked story is proposed for addition mid-sprint, invoke the amendment cycle (`amend cycle --cycle 2026-06-22__release-v6.1 --reason "<reason>"`) to add it to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
