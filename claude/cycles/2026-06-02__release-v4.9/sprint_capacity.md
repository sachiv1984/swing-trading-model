**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-02
**Cycle:** 2026-06-02__release-v4.9

---

# Sprint Capacity — v4.9

## Capacity Inputs

**Source:** `workforce_capacity.md` (revised 2026-05-27) + `release_plan.md ## Capacity Check`

```
Sprint duration:    ~12–14 working days (solo developer, evenings/weekends)
Available FTE:      1 (solo developer)
Total capacity:     ~12–14 capacity days
Skill constraints:  Backend Engineering, QA Lead, Head of Specs Team — all available
                    No scarce skill conflicts identified for v4.9 scope
```

## Item Effort Mapping

### EPIC-01 — Security & Dependency Hardening

| Story | Description | Effort | Delegation Class |
|-------|-------------|--------|-----------------|
| ST-01 | npm devDependency HIGH CVE remediation | S (~0.5 day) | autonomous |
| ST-02 | Anthropic SDK upgrade 0.40.0 → latest | S–M (~0.5–1 day) | autonomous |
| **EPIC-01 total** | | **~1–1.5 days** | |

### EPIC-02 — CI/QA Infrastructure Strengthening

| Story | Description | Effort | Delegation Class |
|-------|-------------|--------|-----------------|
| ST-03 | Wire Phase B CI with real Postgres service | M (~1–2 days) | autonomous |
| ST-04 | Schema smoke test: lifecycle columns on positions table | S (~0.5 day) | autonomous |
| **EPIC-02 total** | | **~1.5–2.5 days** | |

### EPIC-03 — Governance Debt Clearance

| Story | Description | Effort | Delegation Class |
|-------|-------------|--------|-----------------|
| ST-05 | roadmap_prompt.md STEP 8.1 Empty Now Horizon gate strengthening | S (~0.5 day) | autonomous |
| **EPIC-03 total** | | **~0.5 day** | |

## Total Effort vs Capacity

| Category | Effort | Status |
|----------|--------|--------|
| Firm scope (EPIC-01 + EPIC-02 + EPIC-03) | ~3–4.5 days | **PASS** — well within 12–14 day capacity |
| Conditional (EPIC-04, deferred at planning) | ~2–3 days | Deferred — gate not met |
| **Sprint total (firm)** | **~3–4.5 days** | **PASS** |

**Capacity outcome:** PASS — firm scope is approximately 25–35% of available capacity. No over-allocation.

## Conditional (Deferred)

| EPIC | Story | Effort | Gate Condition | Gate Clears |
|------|-------|--------|----------------|-------------|
| EPIC-04 | ST-06 — SI-05 Phase 1 backend service + Telegram delivery | M (~1.5–2 days) | SI-01 + SI-03 live ≥ 30 days (from SI-03 ship 2026-05-22) | 2026-06-21 |
| EPIC-04 | ST-07 — SI-05 Phase 1 Playwright coverage | S–M (~0.5–1 day) | Same as ST-06; depends on ST-06 | 2026-06-21 |

> **Gate re-invocation:** If the gate condition above is met during the sprint (on or after 2026-06-21), do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-02__release-v4.9 --reason "EPIC-04 gate met: SI-01 + SI-03 live ≥ 30 days"`) to add the items to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
