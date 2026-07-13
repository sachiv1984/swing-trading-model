**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-12
**Approved by:** Product Owner — 2026-07-12
**Story:** ST-05 — GAP RISK / RISK OFF combined-badge visual differentiation review (BLG-FE-104)
**Cycle:** 2026-07-12__release-v7.0

---

# UX Decision Record — Combined GAP RISK / RISK OFF Badge Differentiation

## 1. Question

When a position has both `risk_off_exit = true` and `gap_risk.flagged = true`, RISK OFF and GAP RISK badges stack vertically in the same Alerts cell (Table View) / alert-icon row (Grid View), per `positions.md` §Alerts Column ("Stacking" note, v6.9). No design review previously confirmed the combined, stacked state remains visually distinguishable — this is safety-relevant: a user must be able to tell the two alert types apart at a glance, not just notice "something is flagged."

## 2. Review Findings

Existing approved specs already establish:

- **Hue separation:** RISK OFF = `#1E40AF` (blue-800); GAP RISK = `#D97706` (amber-600). These sit in different hue families (blue vs. amber) — not adjacent shades of the same colour, and not a red/green pair that would fail for common colour-vision deficiencies.
- **Label separation:** Each badge always renders its text label ("RISK OFF" / "GAP RISK") — colour is never the sole differentiator (positions.md §Alerts Column; gap-risk-flag/ux_spec.md §7, v6.9).
- **Shape:** Both are rounded pills of the same shape/size family — shape is not a differentiator, which is fine given hue + label already carry it.

**Gap found:** no prior review addressed spacing/legibility of the *stacked* state specifically — risk of the two pills visually merging into a single block at small viewport widths, or Grid View's tighter card layout causing label truncation.

## 3. Decision

Confirmed distinguishable, subject to one addition to the existing spec (applied in `positions.md` STEP 3 of this design gate):

| Element | Spec |
|---|---|
| Vertical gap between stacked badges | `4px` minimum (`gap-1` in Tailwind terms) — prevents visual merging into a single block |
| Stack order | RISK OFF above GAP RISK (regime signal takes visual priority — matches existing column introduction order, v6.2 before v6.9) |
| Truncation | Neither label may truncate; if horizontal space is insufficient (Grid View narrow card), badges wrap to full width individually rather than sharing a row |
| Grid View | Same stacking rule applies to the card's alert-icon row (positions.md §Grid View, line ~167) |

No colour or label change required — the existing v6.2/v6.9 approved values already satisfy WCAG 1.4.1 (colour not sole differentiator) and sufficient hue distance. Only the stacking spacing/order rule was missing and is added here.

## 4. §13 Compliance

Display-only clarification of existing display-only badges. No new automation, no new data source. Not in scope for §13 review.

## 5. Sign-off

- **Head of UX & Design:** Confirmed distinguishable per above — 2026-07-12
- **Product Owner:** Approved — 2026-07-12
