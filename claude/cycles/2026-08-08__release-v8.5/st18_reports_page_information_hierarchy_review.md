**Owner:** Head of UX & Design
**Class:** Design Review (Class 4)
**Status:** Complete
**Last Updated:** 2026-08-10

# Reports Page Information Hierarchy Review (ST-18)

## Scope

Review of `src/pages/Reports.js` for visual clutter/hierarchy issues introduced by the SI-02 gate visibility indicator (`SI02GateStatusSection`, `BLG-FEAT-71`, v6.8).

## Method

Direct review of `src/pages/Reports.js` (1117 lines) — page structure, the `SI02GateStatusSection` component (lines 429-556) and its position/interaction relative to sibling content, and a `dark:` variant density check across the file to establish whether the page is theme-aware as a baseline (it is — 44 `dark:` occurrences across shared secondary-text tokens) before assessing whether the SI-02 section deviates from that baseline.

## Findings

### H-01 — Hierarchy/placement: correctly deprioritised, no issue found

The SI-02 Gate Status section renders **last** in the Tax Year Report flow, after the reconciliation table and the Unrealised P&L card, and is **collapsed by default** (`useState(true)`, `SI02GateStatusSection` line 437). This is the right hierarchy call — SI-02 gate status is a secondary, occasionally-relevant compliance signal, not the page's primary purpose (tax-year P&L reporting). It does not compete visually with the primary content above it, and a user who doesn't care about it never sees its content expanded. No clutter/hierarchy issue at the placement or default-disclosure level.

### H-02 — Genuine issue found: SI-02 section hardcodes dark-theme-only structural styling (not a hierarchy issue per se, but a real visual defect "introduced by" this component)

While the rest of `Reports.js` is theme-aware (44 `dark:` variant pairs for secondary text elsewhere in the file — e.g. `text-slate-600 dark:text-slate-400` used consistently for labels/scope notes throughout), `SI02GateStatusSection`'s own structural elements are hardcoded dark-only, with no `dark:` pairing at all:

- Outer container: `bg-slate-800/50 rounded-lg border border-slate-700/50` (line 487)
- Toggle hover state: `hover:bg-slate-700/20` (line 492)
- Heading: `text-white` (line 494)
- Condition badges' row background: `bg-slate-800/50 border border-slate-700/50` (×3, lines 517/521/525)
- Value text: `text-white` (lines 509, 513, 538, 544) and `text-slate-300` (line 518, 522, 526)
- Loading skeleton: `bg-slate-800/50 animate-pulse` (line 501)

In a light-themed session, this section would render as a dark panel with white/light text sitting inside an otherwise light-themed page — a jarring visual break, not a subtle contrast issue. This is the same recurring defect class named elsewhere this sprint (`BLG-FE-87/88/95/125/129`, and `BLG-FE-150` filed at `EPIC-04/ST-13` for an analogous hardcoded-dark pattern in Dialog components) — a component shipped and reviewed before the project's later light-theme-completeness conventions matured, never retrofitted.

**Disposition:** Per this story's own scope ("findings documented; any fix filed as a follow-up if not resolved in-story" — deferral is the expected outcome, not a shortfall), not fixed in-story. Filed as `BLG-FE-151`.

### H-03 — Related, out-of-scope observation: Unrealised P&L card has the same defect, but is not introduced by SI-02

The immediately-preceding card (`Unrealised P&L Card`, lines 401-414) has the identical structural pattern — `border-slate-600/50 bg-slate-800/30` container (line 403) and `text-slate-300` heading (line 404), both hardcoded, while its own body text correctly uses the `dark:` pair (line 410). This predates the SI-02 section (different feature, no `BLG-FEAT-71` connection) and is therefore out of this story's named scope, but is worth recording since it's visually adjacent and shares the same root cause. Filed separately as `BLG-FE-152` rather than folded into `BLG-FE-151`, since fixing one does not require touching the other.

## Backlog Items Filed

| ID | Title | Priority |
|----|-------|----------|
| BLG-FE-151 | SI-02 Gate Status section (Reports.js) hardcodes dark-theme-only structural styling | P3 |
| BLG-FE-152 | Unrealised P&L card (Reports.js) hardcodes dark-theme-only structural styling (out-of-scope observation, same root cause as BLG-FE-151) | P3 |

## Disposition

No live UI change this cycle (review-only story, consistent with the Design Not Applicable framing used elsewhere in this EPIC for audit-only stories). Placement/default-disclosure hierarchy confirmed correct (H-01). One genuine, well-scoped visual defect found and filed as a follow-up (H-02/BLG-FE-151), plus one related out-of-scope observation (H-03/BLG-FE-152) — both deferred per this story's own expected-path Notes.

## Sign-off

- Reviewed by: Head of UX & Design (agent-mediated, per `execution_prompt.md` §5.3)
- Date: 2026-08-10
