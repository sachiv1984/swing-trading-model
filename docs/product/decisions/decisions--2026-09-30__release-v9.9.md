Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.9
Cycle: 2026-09-30__release-v9.9
Last Updated: 2026-10-06

Superseded by: v9.9 ship — 2026-10-06 — see docs/product/changelog.md#v9.9, cycle 2026-09-30__release-v9.9

## Planning Decisions — v9.9

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity — select ready P3/P4 debt items via category-balanced round-robin to near the top of the confirmed ~24–28 day band, after seating all 4 ready P2 items | Explicit user instruction: "plan release v9.9 full capacity." | Product Owner (direct user instruction, 2026-09-30) | 2026-09-30 |
| Seat `BLG-BE-135` (this cycle's PO Modify-recommended build-and-ship candidate, backend half of the `BLG-BE-135`/`BLG-FE-193` pair) as firm scope; leave `BLG-FE-193` (frontend half) out of scope this cycle | `BLG-FE-193` carries a formal `**Gate criteria:**` field requiring `BLG-BE-135`'s fields shipped and live on `GET /positions` — a same-cycle sequencing dependency is not equivalent to "shipped and available." First cycle since the PO Modify directive was raised (`v9.1`) where any genuine ungated U-shaped candidate exists to seat. | Release Planning Engine (Product Owner role, read of the ready pool) | 2026-09-30 |
| Exclude `BLG-FEAT-73` and `BLG-FEAT-76` from the ready pool despite passing the scripted scan's structural `gated=False` check | Individual read of each item's own gate text, per §1.3a's LL-v9.5-Release-01 note — a data-quality warning is not itself exclusionary, but each item's own body text states a genuine, still-unmet blocking condition (`FEAT-73`: PO-suspended re-check until 2026-11-09 or 10 new linked `trade_plans`; `FEAT-76`: hard-blocked on `FEAT-73`). Both remain substantively gate-blocked. | Release Planning Engine (Head of Specs Team role) | 2026-09-30 |
| Seat `BLG-GOV-356` (conducts the overdue 90-day AI adoption review) as firm scope, leaving the 8 downstream date-lapsed items (`BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`, `BLG-OPS-88`, `BLG-GOV-140`/`141`/`142`) gated with no individual gate-text edit this session | The review itself is the correct, centrally-tracked remediation (already filed as a follow-on to `BLG-GOV-351`, shipped `v9.8`) — editing 8 items' gate text ahead of the review actually running would risk stale or premature disposition. | Release Planning Engine (Head of Specs Team role) | 2026-09-30 |
| Rely on the `2026-09-30__scheduled` rebalance's STEP 8.1 Option(b) decision as §-1.2 precedent for opening `v9.9` | This rebalance ran same-day and postdates `v9.8` (the immediately-prior release-planning cycle) — a fresh record, first citation of it. `ESC-CLOSE-20260928-02`'s open reuse-limits question is not engaged this cycle. | Release Planning Engine (Head of Specs Team role) | 2026-09-30 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (Backend Reliability & Data Integrity) leads the release table | `BLG-BE-135` is this cycle's PO Modify-recommended build-and-ship candidate and the single largest item (8.00d) — the first cycle able to lead with a genuine ungated U-shaped item since the directive was raised. | Head of Specs Team | 2026-09-30 |
| `BLG-BE-135` (S2-01), `BLG-GOV-353` (S2-26), and `BLG-GOV-356` (S2-19) each flagged with a sequencing/risk note | Each item's own scope requires a decision or dependency outside plain implementation (RISK-01: mid-implementation spec query; RISK-02: routing/authority decision; RISK-03: likely Human-Delegation for live production data) before the item can be considered complete — sprint planning should phase each as a short sub-step ahead of the main build. | Head of Specs Team | 2026-09-30 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-09-30__release-v9.9
