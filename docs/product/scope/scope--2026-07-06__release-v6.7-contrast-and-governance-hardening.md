Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v6.7
Cycle: 2026-07-06__release-v6.7
Last Updated: 2026-07-08

Superseded by: v6.7 ship — 2026-07-08
Changelog: docs/product/changelog.md#v6.7
Verification report: claude/cycles/2026-07-06__release-v6.7/verification_report.md
Cycle: 2026-07-06__release-v6.7

## Release Scope — v6.7 Contrast Remediation & Governance Hardening

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Dark-theme secondary-text contrast fix (BLG-FE-87) |
| S2-02 | EPIC-01 | Light-theme secondary-text contrast fix (BLG-FE-88) |
| S2-03 | EPIC-01 | Shared secondary-text design token/component (BLG-FE-89) |
| S2-04 | EPIC-02 | `.claude/skills/` write-scope authority + commit-check patch (BLG-GOV-167) |
| S2-05 | EPIC-02 | Structural guard for 4 append-only governance logs (BLG-GOV-168) |
| S2-06 | EPIC-02 | `audit.py` SLA — same-session commit requirement (BLG-GOV-169) |
| S2-07 | EPIC-02 | Delivery Verification STEP 6 status-line documentation (BLG-GOV-170) |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| SI-02 (Behavioural Drift Detection) | Trade-count condition unresolved (15 confirmed vs. 20 self-reported); re-verification attempt this cycle blocked by missing API credentials | Re-check at next release/roadmap cycle |
| PO-02/PO-04 (Arc 4 remainder) | Data-density gates not met | Re-check at next release planning readiness scan |
| BLG-SPEC-35 (PO-02 §13 boundary review) | Gate: PO-02 sprint planning imminent — not met | Re-review when PO-02 sprint planning becomes imminent |
| All 2026-07-06__scheduled rebalance new items not listed above (BLG-FE-90, BLG-BE-43/44/45, BLG-QA-75–78, BLG-OPS-88–92, BLG-SPEC-67, BLG-FEAT-61/62/63, BLG-GOV-171–177, BLG-SEC-10) | Gate-conditional (design-phase trigger, stability window, signal-triggered, or audit-bundle); none carry `Provisional-Target: v6.7` | Re-evaluate as respective gates clear |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-07-06__release-v6.7
