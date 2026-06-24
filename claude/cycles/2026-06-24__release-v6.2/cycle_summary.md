**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.2
**Cycle:** 2026-06-24__release-v6.2
**Last Updated:** 2026-06-24
**Design Gate Required:** true

---

# Cycle Summary — v6.2 Production Strategy Parity & AI Intelligence

**Cycle ID:** 2026-06-24__release-v6.2
**Release:** v6.2
**Plan published:** 2026-06-24
**Theme:** Close the gap between the live system and `production_strategy.py` backtest logic (P1 cluster), then layer AI decision support (P2 cluster). First release to address production strategy parity.

---

## Scope Summary

| EPIC | Description | Stories | Sprint | Status |
|------|-------------|---------|--------|--------|
| EPIC-01 | Strategy Parity: Core Engine Alignment (BLG-FEAT-46–49) | ST-01 to ST-05 | Sprint 1 | Planned |
| EPIC-02 | AI Intelligence Layer (BLG-FEAT-50–51) | ST-06 to ST-09 | Sprint 2 | Conditional |
| EPIC-03 | Governance & QA Debt (BLG-GOV-135/136, BLG-OPS-75, BLG-QA-62) | ST-10 to ST-13 | Sprint 1 | Planned |

**Total stories:** 13 (9 firm, 4 conditional — EPIC-02 subject to §13 review)
**Total estimated effort:** ~12.5 days
**Capacity:** WARN — 2-sprint plan required; EPIC-01 + EPIC-03 in Sprint 1; EPIC-02 in Sprint 2

---

## Key Planning Decisions

1. **P1 cluster prioritised above AI intelligence:** EPIC-01 (strategy parity) must ship before EPIC-02 (AI briefing/chat) as EPIC-02 depends on live trailing stop, rebalance exit, and risk-off data.
2. **EPIC-03 runs Sprint 1 alongside EPIC-01:** All governance/QA items are XS–S effort and independent. Keeps governance overhead minimal (addressing Skill-Silo Alert G+D+P=79.1%).
3. **§13 review required for EPIC-02 before sprint planning seal:** BLG-FEAT-50/51 are AI-driven advisory endpoints; SRSI Owner must confirm advisory-only, no automated execution.

---

## Risks

| RISK-ID | Description | Priority | Status |
|---------|-------------|----------|--------|
| RISK-01 | §13 compliance not formally reviewed for BLG-FEAT-50/51 | High | Open — required at sprint planning |
| RISK-02 | Capacity risk — 12.5 days total; 2-sprint plan | Medium | Mitigated by phasing |
| RISK-03 | BLG-FEAT-48 replaces core sizing path for signal entries; regression risk | High | Mitigated by regression test requirement |

---

## Design Gate Status

**Design Gate Required:** `true`

Items with observable UI ACs: ST-02 (trailing stop badge), ST-03 (rebalance exit label/styling), ST-05 (risk-off alert), ST-07 (AI briefing card), ST-09 (AI chat widget).

**Next step:** Run `run design-gate --cycle 2026-06-24__release-v6.2` before `plan sprint`.

---

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] §13 compliance review for BLG-FEAT-50 (AI daily briefing) and BLG-FEAT-51 (AI chat advisor) — confirm advisory-only, no automated execution — Owner: Strategy Rules & System Intent Owner

---

## Capacity Check

**Outcome:** WARN

| Phase | EPICs | Estimated effort |
|-------|-------|-----------------|
| Sprint 1 | EPIC-01 + EPIC-03 | ~8.5 days |
| Sprint 2 | EPIC-02 | ~4 days |

Capacity warn acknowledged: 2-sprint plan explicitly phased in this cycle. Product Owner to confirm at sprint planning.

---

## Next Steps (in order)

1. Run `run design-gate --cycle 2026-06-24__release-v6.2`
2. Complete RISK-01 §13 review (Strategy Rules & System Intent Owner) before sprint planning
3. Run `plan sprint --cycle 2026-06-24__release-v6.2`
