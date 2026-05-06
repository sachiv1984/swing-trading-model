**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-06
**Cycle:** 2026-05-05__release-v3.2

---

# Sprint Capacity — 2026-05-05__release-v3.2

---

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | ~10–12 working days (2 sprints, solo developer evenings/weekends) |
| Available FTE | 1 (solo developer, part-time) |
| Total capacity | ~10–12 capacity days |
| Capacity check outcome | ⚠ WARN |

**Skill constraints:**
- Frontend (React) — primary constraint; EPIC-01 and EPIC-02 are the largest consumers
- Governance — low overhead; EPIC-03 prompt patches are XS effort (30–60 min each)
- Documentation — EPIC-04 items estimated 0.5–2 days each, time-insensitive
- QA — ST-11 and ST-12 are test registration/verification tasks, S-effort

---

## Item Effort Mapping

### EPIC-01 — Pre-Trade Research View (Sprint 1)

| ST | Title | Effort | Skill Domain |
|----|-------|--------|-------------|
| ST-01 | Pre-trade research view component — data display | M (~2–3 days) | Frontend |
| ST-02 | Trade plan context panel in research view | M (~1–2 days) | Frontend |
| ST-03 | Prospective heat at entry metric integration (PT-03) | S (~0.5–1 day) | Frontend |
| ST-04 | Navigation integration — screener and watchlist entry points | S (~0.5–1 day) | Frontend |
| **EPIC-01 subtotal** | | **~5–8 days** | Frontend + UX |

### EPIC-02 — Pre-Trade Entry Checklist (Sprint 2)

| ST | Title | Effort | Skill Domain |
|----|-------|--------|-------------|
| ST-05 | Entry checklist schema, component, and Trade Plan form integration | M (~1–2 days) | Frontend + Backend |
| ST-06 | Checklist pre-population from trade plan data and research view link | M (~1 day) | Frontend |
| **EPIC-02 subtotal** | | **~2–3 days** | Frontend + Backend |

### EPIC-03 — Governance & Process Hardening (Sprint 1)

| ST | Title | Effort | Skill Domain |
|----|-------|--------|-------------|
| ST-07 | sprint_planning_prompt.md STEP 0 main-branch verification | XS (~0.5h) | Governance |
| ST-08 | execution_prompt.md STEP 5.1 deviations_filed enforcement | XS (~0.5h) | Governance |
| ST-09 | execution_prompt.md §3.1.A test_scenarios post-story advisory | XS (~0.5h) | Governance |
| ST-10 | Playwright waitFor pattern — test authoring standard | XS (~0.5h) | Governance + QA |
| ST-11 | Trade Plan domain test scenario registration (TEST-GAP-EPIC-01) | S (~0.5 day) | QA |
| ST-12 | Earnings Calendar and UK screener test registration (TEST-GAP-EPIC-03) | S (~0.5 day) | QA |
| **EPIC-03 subtotal** | | **~2–3 days** | Governance + QA |

### EPIC-04 — Documentation, Security & Backlog Clearance (Sprint 2)

| ST | Title | Effort | Skill Domain |
|----|-------|--------|-------------|
| ST-13 | React component inventory (BLG-FE-16) | M (~1–2 days) | Documentation |
| ST-14 | Design system document (BLG-FE-21) | M (~1 day) | Documentation |
| ST-15 | Alpaca credential audit and rotation policy (BLG-SEC-05) | S (~0.5 day) | Security |
| ST-16 | External API dependency risk register (BLG-GOV-18) | S (~0.5 day) | Governance |
| ST-17 | Cycle artefact inventory and maintenance review (BLG-GOV-11) | M (~1–2 days) | Governance |
| **EPIC-04 subtotal** | | **~3–5 days** | Documentation + Security |

---

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~10–12 days |
| Total estimated effort (all 17 stories) | ~12–19 days |
| Midpoint estimate | ~15 days |
| Over-allocation at midpoint | Yes (~4 days) |
| Over-allocation outcome | ⚠ WARN |

**Mitigating factors:**
- EPIC-03 stories (ST-07 to ST-10) are prompt file edits; each estimated 30–60 minutes — well below S-effort typical floor
- EPIC-04 stories are documentation tasks with lower execution friction than feature stories
- Historical velocity = 1.00 across last 6 cycles at similar scopes (v3.0: 16 stories, v3.1: 14 stories)
- 2-sprint phasing distributes load: Sprint 1 EPIC-01+03, Sprint 2 EPIC-02+04
- EPIC-01 is the primary capacity driver; all other EPICs are lightweight relative to their estimates

**Product Owner capacity WARN acknowledgement:** Required before scope selection seals. See sprint_backlog.md sign-off block.
