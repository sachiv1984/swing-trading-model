Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.8
Cycle: 2026-09-28__release-v9.8
Last Updated: 2026-09-30

Superseded by: v9.8 ship — 2026-09-30 — see docs/product/changelog.md#v9.8, cycle 2026-09-28__release-v9.8

## Planning Decisions — v9.8 Full-Capacity Debt Clearance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity — select ready P3/P4 debt items via category-balanced round-robin to the top of the confirmed ~24–28 day band, despite 0 ready P1 and only 3 ready P2 items | Explicit user instruction: "plan release v9.8. full capacity." No ready P1/P2 pool alone would come close to filling the band. | Product Owner (direct user instruction, 2026-09-28) | 2026-09-28 |
| Accept that the PO Modify directive (seat ≥1-2 build-and-ship U-items, per the `2026-09-28__scheduled` rebalance's PVR 0.089 🔴 Alert reading) cannot be satisfied this cycle | 0 genuine ready ungated U-shaped (new-feature) candidates exist in the backlog — the only `BLG-FEAT-*` items are `73`/`76` (both structurally gate-blocked) and `74` (already shipped v9.7, retired). Same finding as `v9.1`–`v9.4`. | Release Planning Engine (Product Owner role, read of the ready pool) | 2026-09-28 |
| Retain `BLG-SPEC-156` from the scan's 3 data-quality-warning items; exclude `BLG-FEAT-73` and `BLG-FEAT-76` | Individual read of each item's own gate text, per §1.3a's LL-v9.5-Release-01 note — a data-quality warning is not itself exclusionary. `SPEC-156` describes pre-work ahead of the PO-04 gate, not work blocked by it (same disposition as `v9.6`/`v9.7`'s equivalent pattern); `FEAT-73`/`76` remain substantively gate-blocked by their own text/`Depends on` chain. `SPEC-156` was subsequently selected on capacity grounds (S2-39/EPIC-06). | Release Planning Engine (Head of Specs Team role) | 2026-09-28 |
| Leave the 8-item AI-adoption-review date-lapsed cluster (`BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`, `BLG-OPS-88`, `BLG-GOV-140`/`141`/`142`) gated, with no individual gate-text edit this session | The underlying 90-day review remains genuinely not conducted (confirmed by this morning's `2026-09-28__scheduled` rebalance, 4 days overdue). `BLG-GOV-351` (filed by that same rebalance) is seated this cycle as the fix for the missing trigger mechanism — editing 8 items' gate text in the same session that already produced the tracking item would risk conflicting edits within hours of each other. | Release Planning Engine (Head of Specs Team role) | 2026-09-28 |
| Rely on the `2026-09-28__scheduled` rebalance's STEP 8.1 Option(b) decision as §-1.2 precedent for opening `v9.8` | This rebalance ran same-day and postdates `v9.7` (the immediately-prior release-planning cycle) — the first time in several cycles this precedent is fresh rather than reused a second time from a stale record, directly addressing (by favourable timing, not by ruling) the ambiguity `ESC-CLOSE-20260928-02` raised. That escalation remains open for the general-case ruling. | Release Planning Engine (Head of Specs Team role) | 2026-09-28 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (Frontend & UX Debt Clearance) leads the release table | Skill-Silo Alert rolling-3-cycle average remains at 85.7% (still well above the 40% ceiling, though improving) with no ready build-and-ship U-item available this cycle to lead with directly (per the PO Modify directive finding above) — EPIC-01 is the most execution-heavy category with genuine ready scope, the closest available honouring of the rotation guideline's intent. | Head of Specs Team | 2026-09-28 |
| EPIC-04 (`BLG-OPS-169`) and EPIC-06 (`BLG-GOV-351`) each flagged with a sequencing note for their own design-decision sub-step | Both items' own Scope text requires a design/ownership decision (where the check runs; which routine owns firing the review) before implementation can begin — sprint planning should phase each as a short decision sub-story ahead of the build, not a single undifferentiated story. | Head of Specs Team | 2026-09-28 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-09-28__release-v9.8
