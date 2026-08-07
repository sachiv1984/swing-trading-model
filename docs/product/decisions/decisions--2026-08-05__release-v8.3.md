Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.3
Cycle: 2026-08-05__release-v8.3
Last Updated: 2026-08-07

Superseded by: v8.3 ship — 2026-08-07
Changelog: docs/product/changelog.md#v8.3
Cycle: 2026-08-05__release-v8.3

## Planning Decisions — v8.3 Operational Reliability & Debt Clearance

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| No explicit "focus" instruction this session — scope selected by curated highest-value ready item selection across categories, balanced to avoid repeating v8.2's self-flagged governance-cluster concentration (RISK-03 there) | No user scope-priority instruction given; delegated Product Owner authority applied | Product Owner | 2026-08-05 |
| `BLG-OPS-129`/`BLG-OPS-130` (P1, SI-05 digest pipeline) lead EPIC-01 | Both are P1, both are direct findings from v8.2's own SI-05 effectiveness review — a broken production-facing feature with a 7-week silent failure | Product Owner | 2026-08-05 |
| `BLG-FEAT-73`/`BLG-FEAT-74` formally parked (Option (b), STEP 1.4a.1 mandatory sunset trigger — 4th consecutive Option (a) would otherwise have fired) | No materially new gate-clearance path since v8.1; mandatory per §1.4a.1 at exactly this count | Product Owner | 2026-08-05 |
| `BLG-FEAT-45` promoted conditional → firm (STEP 1.4b) | Date gate `≥ 2026-08-05` objectively met as of this session | Product Owner | 2026-08-05 |
| `BLG-GOV-74` excluded despite passing the initial ungated-candidate scan | Full-text re-read found a `**Gate date:** First review due 2026-08-29` field outside this cycle's execution window | Product Owner | 2026-08-05 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| `BLG-OPS-130` sequenced after `BLG-OPS-129` | Alerting design should follow root-cause understanding of the digest pipeline failure (item's own `Depends on` field) | Product Owner | 2026-08-05 |
| `BLG-BE-69` to be implemented incrementally across multiple PRs, not one large diff | Item's own scope note: ~17 files touched, "apply incrementally... to keep review scope manageable" | Product Owner | 2026-08-05 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | — | — | — |

*(No Accepted Risk escalations raised this cycle.)*

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-05__release-v8.3
