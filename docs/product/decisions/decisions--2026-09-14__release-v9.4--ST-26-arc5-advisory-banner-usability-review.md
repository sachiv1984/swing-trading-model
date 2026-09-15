**Owner:** Head of UX & Design
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-15 (ST-26, EPIC-06, v9.4, BLG-UX-03: initial version)

---

# Usability Review — Arc 5 Low-Trade-Volume Advisory Banner

**Added:** ST-26 (EPIC-06, v9.4, BLG-UX-03)

## 1. Scope of This Review

`BLG-UX-03` asked for a usability pass on "the Arc 5 compliance advisory banner," described in its own problem statement as having "been through 3 UI revisions since its original ship." The banner matching this description is the **Low-Trade-Volume Advisory** inside `Arc5ComplianceSection.js` (`docs/specs/frontend/components/arc5_compliance_section.md#Low-Trade-Volume Advisory`) — the only Arc-5-labelled, compliance-adjacent, explicitly-named "banner" in the frontend spec corpus.

## 2. Correction to the Backlog Item's Own Framing

The actual revision history, read directly from `arc5_compliance_section.md`'s Changelog (§ below), does **not** show 3 revisions to the banner itself:

| Version | Date | Touches the banner? |
|---------|------|----------------------|
| 1.0.0 | 2026-05-27 | No — banner did not exist yet (initial spec, no advisory) |
| 1.1.0 | 2026-09-04 | No — documented a Card 3 (unrelated stat card) deviation |
| 1.2.0 | 2026-09-07 | **Yes** — banner added (`ST-01`, `BLG-FEAT-44`) |
| 1.3.0 | 2026-09-07 | No — corrected Card 3's documented format, not the banner |

The banner has had **one** revision (its own addition) since the component's original ship, not three. This is disclosed here rather than silently assumed correct: the idea that generated `BLG-UX-03` (`IDEA-head-of-ux-20260914-01`) appears to have overstated the banner's own change count, possibly conflating it with the component's overall changelog length (4 entries) or with unrelated revisions to sibling cards. This does not change the review's usefulness — a usability pass is worth doing regardless of how many prior revisions there were — but the record should reflect what's actually true rather than restate an inaccurate premise.

## 3. Review Against Original Intent

**Original intent** (`docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/decision_record.md`, `assessment.md`): when a portfolio has fewer than 20 closed trades, the four Arc 5 compliance stat cards are computed from too thin a sample to display with unqualified confidence. The advisory exists so a user with a young trading history sees an explanatory note instead of a bare number that could be mistaken for a reliable reading.

**Current implementation** (`Arc5ComplianceSection.js`, verified by reading the shipped JSX):
- Renders only when `total_closed_trades` is a non-null number below 20 — correctly excludes loading/error/unknown states (treats "unknown" ≠ "low volume", per spec).
- Copy: *"Based on {N} closed trade(s) — treat these figures as indicative until more trade history accumulates."*
- Static, non-dismissible, Info-tone styling (blue), positioned below the four-card stat grid.

**Does the text hierarchy still read correctly?** Yes on its own terms — the copy is short, the icon and tone correctly signal "informational, not urgent," and it doesn't compete visually with the stat cards above it (matches `role="status"`, appropriately non-intrusive). No regression from cumulative changes was found, because — per §2 above — no cumulative changes to this specific banner actually occurred.

## 4. Usability Observations (Not Fixed Inline — Filed Separately Per AC)

Two genuine gaps found on independent reading of the copy against its own stated purpose:

1. **The threshold itself is never stated.** A user reading "treat these figures as indicative until more trade history accumulates" has no way to know what "enough" means — 20 trades is known only to someone who has read the spec, not the on-screen user.
2. **Placement is caveat-after-numbers, not caveat-before-numbers.** The advisory sits below the four stat cards, so a user reads the (possibly low-confidence) numbers first and the qualifying context second — the opposite of how a disclaimer is usually most effective.

Filed as `BLG-UX-05` (Frontend & UX Backlog, §3) per this story's AC — **not** fixed as part of this review. Head of UX & Design owns the decision on whether either change is worth making.

## 5. Recommendation

**Option A (recommended):** Action `BLG-UX-05` at the next convenient frontend cycle — both changes are small (XS effort) and directly serve the banner's own stated purpose.
**Option B:** Keep the banner as-is; the current copy is not wrong, only less informative than it could be, and the simplicity may be an intentional trade-off worth preserving.

This review does not select between A and B — that decision belongs to `BLG-UX-05`'s own resolution, per this story's AC ("any recommended change filed as its own item, not fixed inline").

## 6. Sign-Off

- Signed off by: <fill in — pending §5.3 agent-mediated review>
- Date: <fill in — must be non-blank>
- Comments:

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-15 | ST-26 (EPIC-06, v9.4, BLG-UX-03): Initial version. Usability review of the Arc 5 low-trade-volume advisory banner, correcting the backlog item's "3 revisions" framing against the component's actual changelog, and filing `BLG-UX-05` for the two usability gaps found. |
