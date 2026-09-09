Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.2
Cycle: 2026-09-07__release-v9.2
Last Updated: 2026-09-09

## Planning Decisions — v9.2 Full-Capacity Debt Clearance & Arc 5 Advisory

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope set to the top of the confirmed ~24–28 day capacity band (final: 27.55 days, 56 items, 5 EPICs) | Explicit user instruction: "use full capacity" (mirrors the v9.1 precedent phrasing). `BLG-FEAT-44` is the sole ungated build-adjacent item; remaining scope assembled from the ungated P2/P3 pool across 4 curated debt themes. | Product Owner | 2026-09-07 |
| `BLG-FEAT-44` gate condition confirmed met by calendar-date arithmetic (v4.1 shipped 2026-05-27; 103 days elapsed ≥ 3-month/~90-day threshold) and promoted from conditional to firm scope | First cycle since v4.1 shipped that this gate has cleared. Per §1.4b, promotion requires only that the gate condition be objectively met — the item's own AC additionally requires named-owner sign-off, tracked separately as a Pre-sprint Planning Required Decision (RISK-06). | Product Owner (delegated authority) | 2026-09-07 |
| `BLG-FEAT-92` remains excluded from scope — standing `BLG-FEAT-30` sub-scope reconciliation from `2026-09-03__release-v9.1` reaffirmed, not re-litigated | No new evidence this cycle that the inherited gate (screener live ≥60 days AND ≥60 closed trades with attribution) has cleared; the prior Product Owner decision stands unchanged. 4th consecutive cycle this exclusion has held (v8.9, v9.0, v9.1, v9.2). | Product Owner (delegated authority) | 2026-09-07 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 and EPIC-02 sequenced first for a shared design-gate pass | Both carry observable UI ACs (`design_gate_required = true`); running one combined design gate first unblocks sprint planning for the remaining backend/QA/governance-only EPICs without a dependency wait. | Product Owner | 2026-09-07 |
| EPIC-04's governance-prompt-touching stories sequenced serially within the EPIC rather than run on parallel sub-branches | 26 items in one EPIC, several independently bumping `OPERATIONAL_GUIDE.md`/individual prompt versions — serial execution avoids the version-bump collision pattern documented in CLAUDE.md §8 step 2a. | Product Owner | 2026-09-07 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| — | — | None. *(No Accepted Risk escalations raised this cycle — 0 open, 0 deferred escalations.)* | — | — |

### Supersession note

Superseded by: v9.2 ship — 2026-09-09
Changelog: docs/product/changelog.md#v9.2
Cycle: 2026-09-07__release-v9.2
