**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.5

---

# Sprint Capacity — v4.5

---

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | ~12–14 working days per sprint (solo developer, evenings/weekends) |
| Available FTE | 1 (solo developer) |
| Total capacity per sprint | ~12–14 days |
| Warn threshold | Effort > 14 days |
| Source | `claude/roadmap/workforce_capacity.md` (effective 2026-05-27 revision) |

**Skill constraints:**
- Sprint 1: No scarce skill constraints — all items are `autonomous`; Head of Specs Team (sole role)
- Sprint 2: `delegated_decision` items require Strategy Rules & System Intent Owner (ST-06), Metrics Definitions & Analytics Canonical Owner (ST-07), Data Model & Domain Schema Owner (ST-08) — all conditional on EPIC-03 gate

---

## Item Effort Mapping

### Sprint 1 (Firm)

| EPIC | Story | Title | Effort | Source |
|------|-------|-------|--------|--------|
| EPIC-01 | ST-01 | DEL terminal-status write split | XS (~0.5 hr) | stage4_backlog_slice.md |
| EPIC-01 | ST-02 | STEP 3.2.B explicit pr_status sync | XS (~0.5 hr) | stage4_backlog_slice.md |
| EPIC-01 | ST-03 | Verification-class sub-criterion | XS (~0.5 hr) | stage4_backlog_slice.md |
| EPIC-01 | ST-04 | spec_references policy for doc-creation stories | XS (~0.5 hr) | stage4_backlog_slice.md |
| EPIC-02 | ST-05 | Standardize 5 agent file role headers | S (~1 hr) | stage4_backlog_slice.md |
| **Sprint 1 total** | | | **~4.5 hrs (~0.6 days)** | |

*Release plan capacity check used conservative estimate (~10 hrs for Sprint 1). Story-level estimates used here. Sprint 1 is comfortably within capacity under either figure.*

### Sprint 2 (Conditional — EPIC-03 gate)

| EPIC | Story | Title | Effort | Gate condition |
|------|-------|-------|--------|---------------|
| EPIC-03 | ST-06 | SI-02 §13 formal boundary review | S (~0.5 day / ~4 hrs) | PO confirms SI-02 sprint planning imminent |
| EPIC-03 | ST-07 | SI-02 drift detection score metric definition | S (~1 day / ~8 hrs) | PO confirms SI-02 sprint planning imminent; depends ST-06 PASS |
| EPIC-03 | ST-08 | SI-02 data schema pre-definition | M (~1–2 days / ~8–16 hrs) | PO confirms SI-02 sprint planning imminent; informed by ST-07 |
| **Sprint 2 conditional total** | | | **~20–28 hrs (~2.5–3.5 days)** | |

---

## Total Effort vs Capacity

| Sprint | Firm effort | Capacity | Utilisation |
|--------|-------------|----------|-------------|
| Sprint 1 | ~4.5 hrs (~0.6 days) | ~12–14 days | ~5% — well within capacity |
| Sprint 2 (conditional) | ~20–28 hrs (~2.5–3.5 days) | ~12–14 days | ~20–25% — within capacity |
| **Total (both sprints)** | **~24–32 hrs (~3–4 days)** | ~24–28 days total | **~12–15%** |

**Capacity verdict:** WARN — inherited from release plan stage4_5_capacity_check. Sprint 1 is well within capacity. Sprint 2 is conditional; if gate is not met by Sprint 2 seal, Sprint 2 closes with no EPIC-03 stories and the cycle completes with Sprint 1 only (5 stories).

**WARN acknowledged:** Product Owner acknowledges WARN. Sprint 1 proceeds. Sprint 2 gate decision (SI-02 20-closed-trades confirmation) to be resolved before Sprint 2 seal.

---

## Sprint 2 (EPIC-03 — Gate Confirmed 2026-05-30)

Gate confirmed by Product Owner 2026-05-30. EPIC-03 promoted from conditional to in-scope Sprint 2.

| EPIC | Story | Effort | Status |
|------|-------|--------|--------|
| EPIC-03 | ST-06 | S (~4 hrs) | **In-scope Sprint 2** — gate confirmed |
| EPIC-03 | ST-07 | S (~8 hrs) | **In-scope Sprint 2** — gate confirmed; depends ST-06 PASS |
| EPIC-03 | ST-08 | M (~8–16 hrs) | **In-scope Sprint 2** — gate confirmed; informed by ST-07 |
