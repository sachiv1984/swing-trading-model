**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-21
**Cycle:** 2026-06-21__release-v5.1

---

# Sprint Capacity — v5.1 SI-05 Phase 1 & Governance Debt

## Capacity Baseline

```
Sprint duration:    1 sprint (~12–14 working days available)
Available FTE:      1 (solo developer, evenings/weekends)
Total capacity:     ~12–14 working days
Warn threshold:     Effort > 14 days
Capacity check:     pass
Skill constraints:  None — all items are backend, governance, Playwright, or documentation
```

*Source: `workforce_capacity.md` (revised baseline 2026-05-27: ~12–14 days/sprint)*

---

## Item Effort Mapping

| EPIC | ST | Title | Class | Effort | Estimate source |
|------|-----|-------|-------|--------|----------------|
| EPIC-01 | ST-01 | SI-05 Phase 1 backend + Telegram implementation | Autonomous | M (~2–3 days) | release_plan.md §Capacity Check |
| EPIC-01 | ST-02 | BLG-SPEC-45 SI-05 financial reporting scope verification | Autonomous | XS (~1 hour) | release_plan.md §Capacity Check |
| EPIC-02 | ST-03 | delivery_verification_prompt.md §-1.3 Tier 2 fix | Autonomous | S (~0.5 day) | release_plan.md §Capacity Check |
| EPIC-03 | ST-04 | BLG-FE-61 SignalCard allocation_insufficient Playwright E2E | Autonomous | XS (<1 hour) | release_plan.md §Capacity Check |
| EPIC-03 | ST-05 | BLG-QA-43 compliance_summary field population validation | Autonomous | XS (~1–2 hours) | release_plan.md §Capacity Check |
| EPIC-03 | ST-06 | BLG-GOV-89 Staged verification sprint protocol document | Autonomous | S (~0.5 day) | release_plan.md §Capacity Check |

---

## Total Effort vs Capacity

| Measure | Value |
|---------|-------|
| Total estimated effort | ~4.5 days (mid-point) |
| Sprint capacity | ~12–14 working days |
| Utilisation | ~32–38% |
| Result | **PASS — well within capacity** |

No over-allocation. All 6 items confirmed `include`.

---

## Conditional (Deferred)

None. All 6 backlog slice items are included in the sprint. No gate-conditional deferred items.

---

## Risk Register

| RISK-ID | EPIC | Description | Mitigation |
|---------|------|-------------|------------|
| RISK-01 | EPIC-01 | SI-05 gate clears exactly on 2026-06-21 | Confirmed cleared at sprint planning: SI-03 shipped 2026-05-22; 30 days elapsed as of 2026-06-21 ✓ |
| RISK-02 | EPIC-01 | No SI-05 API contract exists; must be authored same-sprint | ST-01 scope includes contract + openapi.yaml + test.py in same commit |
| RISK-03 | EPIC-02 | CLAUDE.md §6 governance checklist required for delivery_verification_prompt.md patch | Well-established pattern; HoST owns and applies checklist |
