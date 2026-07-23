**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-07-21
**Cycle:** 2026-07-21__release-v7.7
**Story:** ST-03 (EPIC-03, BLG-FE-113)

---

# UX Decision Record — AiDailyBriefing Light-Theme Classification

## 1. Classification Downgrade

Default classification per §6 of the design gate prompt is **Design Required**. This item is downgraded to **Design Pre-Approved**, with explicit confirmation, per the following reasoning:

- The AI Daily Briefing Card is an existing, already-specified component (`dashboard.md` §5, v3.1, last updated 2026-07-15) — no new component, layout, page, or interaction is introduced.
- The card's spec already establishes and uses the light/dark token-pairing convention this story is verifying (e.g. Advisory Label: `text-slate-700 dark:text-slate-300`, explicitly documented with a contrast note: "light companion added v2.6/BLG-FE-88").
- ST-03's scope is a **staging verification pass** against the existing spec, with a conditional fix that — if needed — applies the same already-established `dark:` token-pairing pattern already in use elsewhere on this exact card. It does not introduce a new visual language or require a wireframe.
- This is execution-phase QA work (staging check, pass/fail recorded, evidence-based closure) rather than design-phase work (new layout/interaction decisions).

This mirrors the precedent set by the card header icon addition (v7.2, dashboard-briefing-hierarchy) and Advisory Label contrast fix (v2.5/v2.6, BLG-UX-01/BLG-FE-88) — both were token-level corrections against an existing spec, not new design artefacts.

## 2. What "Design Pre-Approved" means here

No new wireframe or interaction spec is produced. `dashboard.md` §5 is the locked spec reference. If the staging check (performed during Sprint Execution, per ST-03's own AC) finds a contrast failure on an element not already covered by an explicit light/dark pair in §5, the fix must use the existing token conventions documented there (`text-slate-700 dark:text-slate-300`-style pairing, `bg-white dark:bg-slate-900`-style pairing) — no new colour values are to be introduced without a follow-up Head of UX & Design review.

Elements in §5 with only a single hex value and no documented light/dark variant (the action-type chip colours: `EXIT #DC2626`, `ENTER #16A34A`, `MONITOR #D97706`, `HOLD #6B7280`) are exactly the kind of gap ST-03's staging check exists to surface — these are flagged as the most likely fail points, since the spec doesn't currently state whether they were verified against a light background.

## 3. Approval

Product Owner: confirmed downgrade 2026-07-21 (per §6: "Product Owner confirms design-not-applicable classifications for borderline items" — here confirming Pre-Approved, the parallel borderline case).
Head of UX & Design: confirmed 2026-07-21.
