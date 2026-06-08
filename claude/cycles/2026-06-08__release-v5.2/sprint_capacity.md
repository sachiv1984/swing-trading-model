**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2

---

# Sprint Capacity — v5.2 Governance Debt, SI-05 Ops & Spec Compliance

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | ~13 working days (2026-06-08 → 2026-06-21; solo developer, evenings/weekends) |
| Available FTE | 1 (solo developer) |
| Total capacity baseline | ~12–14 working days per sprint (per workforce_capacity.md, revised 2026-05-27) |
| Warn threshold | Effort > 14 days |
| Skill constraints | None scarce — EPIC-02 backend delegated; EPIC-03/04 review/doc work autonomous or delegated_backend |

*Source: `claude/roadmap/workforce_capacity.md` (Sprint Capacity Baseline effective 2026-05-27) and `claude/cycles/2026-06-08__release-v5.2/release_plan.md ## Capacity Check`.*

---

## Item Effort Mapping

### EPIC-01 — Governance Prompt Patches & Spec Compliance (Execution sequence: 4 — merge last)

| ST | Story | Effort band | Delegation class |
|----|-------|-------------|-----------------|
| ST-01 | OA-01: release_planning_prompt.md §-1.2 patch | S (~0.5 day) | autonomous |
| ST-02 | OA-02: execution_prompt.md §3.1.A test-authoring guidance | S (~0.5 day) | autonomous |
| ST-03 | BLG-SPEC-47: SI-05 pass_rate computation alignment | S (~0.5 day) | autonomous (spec) + delegated_backend (if impl.) |
| ST-04 | BLG-SPEC-48: POST /digest/si05/send API contract | XS–S (~0.25–0.5 day) | autonomous |
| **EPIC-01 subtotal** | | **~1.75–2.0 days** | |

### EPIC-02 — SI-05 Backend Reliability & Operations (Execution sequence: 2)

| ST | Story | Effort band | Delegation class |
|----|-------|-------------|-----------------|
| ST-05 | BLG-BE-32: Telegram delivery retry and failure handling | S (~0.5–1 day) | delegated_backend |
| ST-06 | BLG-BE-33: SI-05 digest delivery log table | S (~1 day) | delegated_backend |
| ST-07 | BLG-OPS-55: Deployment runbook update | XS (~0.25 day) | autonomous |
| ST-08 | BLG-OPS-56: Health check procedure | XS (~0.25 day) | autonomous |
| **EPIC-02 subtotal** | | **~2.0–2.5 days** | |

### EPIC-03 — SI-05 Security Reviews & Endpoint Compliance (Execution sequence: 1 — merge first)

| ST | Story | Effort band | Delegation class |
|----|-------|-------------|-----------------|
| ST-09 | BLG-GOV-97: Claude API model deprecation check | XS (~0.25 day) | autonomous |
| ST-10 | BLG-GOV-98: Telegram bot token security review | S (~0.5 day) | autonomous |
| ST-11 | BLG-GOV-99: SI-05 digest endpoint auth review | S (~0.5 day) | autonomous (review) + delegated_backend (if fix) |
| ST-12 | BLG-GOV-100: Backend endpoint documentation audit | S (~0.5–1 day) | autonomous |
| **EPIC-03 subtotal** | | **~1.75–2.25 days** | |

### EPIC-04 — SI-05 QA, Verification & Product Governance (Execution sequence: 3)

| ST | Story | Effort band | Delegation class |
|----|-------|-------------|-----------------|
| ST-13 | BLG-QA-46: Edge case test gap analysis | XS (~0.25 day) | autonomous |
| ST-14 | BLG-QA-47 + BLG-GOV-94: Acceptance test + delivery verification protocol | S (~0.5–1 day) | autonomous |
| ST-15 | BLG-QA-48: Regression test baseline refresh | XS (~0.25 day) | autonomous |
| ST-16 | BLG-GOV-96: SI-05 effectiveness measurement criteria | S (~0.5 day) | autonomous |
| **EPIC-04 subtotal** | | **~1.5–2.0 days** | |

---

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Confirmed capacity | ~12–14 working days |
| Total estimated effort (16 in-scope stories) | ~7.0–8.75 days (low–high mid) |
| Effort mid-point | ~7.9 days |
| Utilisation | ~56–65% of available capacity |
| Over-allocation | No |
| Capacity warn triggered | Yes (state.json `stage4_5_capacity_check=warn` from release planning) — see note below |

**Capacity WARN note:** The `warn` in `state.json` was computed at release planning against an earlier estimate of 10–11 days total (17+1 stories including ST-17 conditional). With ST-17 deferred at sprint planning (gate not cleared), in-scope effort is ~7.9 days mid-point — well within the 12–14 day capacity baseline. Product Owner acknowledges the WARN; no scope reduction required.

---

## Conditional (Deferred at Planning)

| EPIC | ST | Story | Effort | Gate condition |
|------|----|-------|--------|---------------|
| EPIC-04 | ST-17 | BLG-FE-64: BLG-FE-41 Red Flag Journal visual design review pre-brief | S (~0.5 day) | SI-03 Red Flag Journal live ≥ 30 days; gate clears 2026-06-21; not confirmed clear at sprint planning 2026-06-08 — deferred to v5.3 |

> **Gate re-invocation:** If the ST-17 gate condition above is met during the sprint, do not add this item informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-08__release-v5.2 --reason "BLG-FE-64 gate confirmed clear 2026-06-21"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
