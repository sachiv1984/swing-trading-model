Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.7
Cycle: 2026-09-23__release-v9.7
Last Updated: 2026-09-23

## Planning Decisions — v9.7 PO-05 Replay Mode & Full-Capacity Debt Clearance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Seat `BLG-FEAT-74` (PO-05 Lightweight Replay Mode) as firm P1 scope, effort estimated at 12.0 days (Product Owner ad hoc estimate — no canonical `VH` midpoint exists in `workforce_capacity.md`) | §13 pre-clearance PASSed this week (`ESC-EXEC-20260921-05`, `docs/product/decisions/po05_section13_preassessment.md`); Arc 4's flagship feature, gate-blocked since 2026-07-10; §1.4c requires ready P1 items seat before P2. Surfaced to the Product Owner directly given the stakes of a VH item with an open scope-definition question. | Product Owner (direct user instruction, 2026-09-23) | 2026-09-23 |
| Continue category-balanced round-robin fill to the top of the confirmed ~24–28 day capacity band despite `BLG-FEAT-74`'s size | Explicit user instruction: "also use the full capacity" — the large P1 item must not crowd out the rest of the release's debt-clearance scope. | Product Owner (direct user instruction, 2026-09-23) | 2026-09-23 |
| Exclude `BLG-FE-189` from scope | Already resolved same-session (2026-09-22, hotfix branch, Playwright-covered) — not open work, despite the gate scan surfacing it as an ungated P1 candidate. | Release Planning Engine (Head of Specs Team role, read of item body) | 2026-09-23 |
| Retain `BLG-FEAT-74` and `BLG-SPEC-156` from the scan's 4 data-quality-warning items; exclude `BLG-FEAT-73` and `BLG-FEAT-76` | Individual read of each item's own gate text, per §1.3a's LL-v9.5-Release-01 note — a data-quality warning is not itself exclusionary. `FEAT-74`'s gate genuinely cleared; `SPEC-156` describes pre-work ahead of a gate, not work blocked by one; `FEAT-73`/`76` remain substantively gate-blocked. | Release Planning Engine (Head of Specs Team role) | 2026-09-23 |
| Reuse the `2026-09-19__scheduled` rebalance's STEP 8.1 Option(b) decision as §-1.2 precedent for opening `v9.7`, despite that record's own prose naming `v9.6` specifically | No newer rebalance has run since `v9.6` shipped; the underlying condition (empty Now horizon, backlog-driven cadence) is unchanged. Flagged as a friction item for a future Head of Specs Team ruling on whether this reuse pattern needs a tighter rule. | Release Planning Engine (Head of Specs Team role) | 2026-09-23 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (`BLG-FEAT-74` alone) leads the release as the largest, highest-priority, and most sequencing-sensitive item | Its own scope note requires exact-scope confirmation before implementation begins; sprint planning should treat this as a phased build (spec/scope confirmation → backend replay → frontend selector/output view) rather than a single undifferentiated story. | Product Owner / Head of Specs Team | 2026-09-23 |
| EPIC-02 (Frontend/UX) sequenced independent of EPIC-01 | No dependency between the P&L/Setup-Type frontend fixes and the replay-mode build; can run in parallel. | Head of Specs Team | 2026-09-23 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-09-23__release-v9.7
