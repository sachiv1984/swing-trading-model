**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-18__release-v3.7
**Story:** ST-06 (EPIC-02) — PT-04 frontend
**Sources:** PT-04 (Arc 2 roadmap), trade_plan.md v0.4, pre_trade_research.md v0.1
**Gate condition:** EPIC-02 gate — Product Owner must confirm 20+ closed trades before this artefact activates
**Approved by:** Product Owner
**Approved date:** 2026-05-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — PT-04 Setup Quality Score Display

This spec defines the frontend display of the Setup Quality Score on the Trade Plan detail view and Pre-Trade Research View. The score is a deterministic 0–100 value calculated from the user's own closed trade history.

---

## 1. Design Intent

The Setup Quality Score surfaces a self-referential quality signal: how similar is this setup to the user's own historically successful entries? The score is derived entirely from the user's own trade history using deterministic rules (no ML), and is explicitly framed as historical context — not a recommendation.

The display must clearly communicate:
- The score value (or "insufficient history" state)
- The data source ("your own trade history")
- That it is not a prediction or recommendation

---

## 2. Placement — Trade Plan Detail View

The Setup Quality Score is displayed in the **Trade Plan detail view** (route: `/trade-plans/{id}`), as a read-only field alongside the existing plan fields.

**Recommended position:** Below the status badge and core fields, above the Pre-Trade Checklist read-only section.

| Element | Source |
|---------|--------|
| Label | "Setup Quality Score" |
| Value | `GET /trade-plans/{id}/quality-score` → `score` (integer 0–100) |
| Insufficient history | `GET /trade-plans/{id}/quality-score` → `score: null, reason: "insufficient_history"` |
| Sub-label | "Based on your own trade history" (muted, smaller text) |

**Score display — sufficient history (≥ 20 closed trades):**
- Numeric value: `{N}/100`
- Optional colour band:
  - 0–39: red text or muted styling
  - 40–69: amber text
  - 70–100: green text

**Insufficient history state:**
- Display: **"N/A — insufficient history"**
- Tooltip or sub-text (optional): "Score requires 20 or more closed trades"
- No score bar or numeric value shown

---

## 3. Placement — Pre-Trade Research View

The Setup Quality Score is also displayed on the **Pre-Trade Research View** (route: `/research/{ticker}`), alongside existing metrics in the Price and Signal Region (§5 of pre_trade_research.md).

**Recommended position:** Added as a new row in §5 (Price and Signal Region) of the Research View:

| Element | Source |
|---------|--------|
| Label | "Setup Quality Score" |
| Value | `GET /trade-plans/{id}/quality-score` for the most recent active/draft trade plan for this ticker, or `—` if no plan exists |
| Insufficient history | "N/A — insufficient history" (same as detail view) |
| Sub-label | "Based on your trade history" (muted) |

**If no trade plan exists for the ticker:** the score is not shown (no plan to score).

---

## 4. Read-Only Nature

- The score is always read-only — no editing, no input
- No action button or CTA adjacent to the score
- The label "Based on your own trade history" is mandatory — it must appear adjacent to the score on both pages to prevent the score from being mistaken for a market prediction

---

## 5. Loading and Error States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton placeholder (inline, single-line width) |
| Error (endpoint fails) | Field hidden silently — do not block the page; do not show an error for this field |
| No trade plan (Research View only) | Score field omitted entirely |
| Insufficient history | "N/A — insufficient history" (not an error — expected state when < 20 closed trades) |

---

## 6. §13 Compliance

- Display-only; no automated trade actions triggered
- Score is labelled as based on historical data ("your own trade history")
- Explicitly not presented as a prediction, recommendation, or instruction
- The "insufficient history" state is a data completeness indicator, not a system judgement

---

## 7. Non-Regression Rules

- No regression to trade plan detail view layout (existing fields, checklist, action buttons)
- No regression to pre_trade_research.md §5 existing elements (current price, momentum signal, ATR)
- Score field absence (no plan, error, loading) must not cause layout shift
