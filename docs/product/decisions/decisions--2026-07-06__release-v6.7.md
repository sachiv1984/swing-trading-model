Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v6.7
Cycle: 2026-07-06__release-v6.7
Last Updated: 2026-07-06

## Planning Decisions — v6.7 Contrast Remediation & Governance Hardening

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-FE-87 and BLG-FE-88 as firm scope | Satisfies the mandatory Skill-Silo pull-forward clause (`roadmap_prompt.md` §7.1 v8.3) requiring ≥2 build-and-ship-shaped U-items; both named directly by the `2026-07-06__scheduled` rebalance | Product Owner (via Release Planning Engine) | 2026-07-06 |
| Include BLG-FE-89 alongside BLG-FE-87/88 | Same audit source (BLG-FE-82/ST-01 v6.6); prevents a third recurrence of the ad hoc secondary-text colour defect class | Product Owner (via Release Planning Engine) | 2026-07-06 |
| Include the full BLG-GOV-167–170 audit improvement bundle | All 4 items originate from Lifecycle Audit AUD-2026-07-06 (score 81, 17 prior findings resolved); BLG-GOV-167 directly resolves a 3-cycle-carried escalation (ESC-CLOSE-20260706-01) that must not persist a 4th cycle | Head of Specs Team (via Release Planning Engine) | 2026-07-06 |
| Defer SI-02, PO-02, PO-04, BLG-SPEC-35 | Data-density/dependency gates not met; SI-02's trade-count condition remains formally unresolved despite a re-verification attempt this session | Product Owner (via Release Planning Engine) | 2026-07-06 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| BLG-FE-88 (S2-02) must land after BLG-FE-87 (S2-01) merges | BLG-FE-88's own AC states this explicitly — a dark-theme-only fix landing first on the same class would require rework if not sequenced | Head of Specs Team (via Release Planning Engine) | 2026-07-06 |
| BLG-FE-89 (S2-03) recommended last within EPIC-01 | Documents the canonical treatment based on the concrete fixes landed in S2-01/S2-02 | Head of Specs Team (via Release Planning Engine) | 2026-07-06 |
| EPIC-02 (S2-04–07) has no ordering dependency on EPIC-01 | Governance/process items are independent of the frontend contrast work; may proceed in parallel | Head of Specs Team (via Release Planning Engine) | 2026-07-06 |

### Accepted risks
None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-06__release-v6.7
