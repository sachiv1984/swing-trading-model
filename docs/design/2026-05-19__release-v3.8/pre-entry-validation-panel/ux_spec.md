**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-19__release-v3.8
**Story:** ST-03 (EPIC-01) — SI-01 Frontend Pre-Entry Validation Panel
**Sources:** BLG-FEAT-25; trade_plan.md v0.6; strategy_rules.md §11, §13
**Gate condition:** ST-01 §13 Review Gate must PASS before this artefact activates. If ST-01 FAILS, this artefact is suspended and EPIC-01 is removed from sprint scope.
**Approved by:** Product Owner (conditional — activates on ST-01 §13 PASS)
**Approved date:** 2026-05-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — SI-01 Pre-Entry Validation Panel (ST-03)

This spec defines the frontend advisory panel surfacing pre-entry rule validation results within the Trade Plan creation flow. This is a decision-support tool — non-blocking, advisory only.

> **§13 Compliance:** This panel is display-only advisory. No automated blocking of plan submission is generated. All checks produce informational results only. The user may override any advisory result and proceed. This panel does not generate position recommendations or trading signals.

---

## 1. Presence Condition

The Pre-Entry Validation Panel is rendered in the Trade Plan creation form after **both** a ticker and a quantity are set.

- Hidden if ticker is unset
- Hidden if quantity is unset or zero
- Panel is below the setup thesis section and above the Pre-Trade Entry Checklist (§6 of trade_plan.md)

---

## 2. Panel Structure

**Panel header:** "Pre-Entry Validation" (advisory section, visually distinct — muted background `bg-gray-50`, amber-left-border to signal advisory status)

Sub-header text (muted): "Advisory checks based on strategy rules. Non-blocking — you may proceed regardless of results."

### 2.1 Rule Checks

Five checks displayed as a vertical list of rows:

| Rule | Label | Source in §11 |
|------|-------|---------------|
| Regime gate | "Market regime" | strategy_rules.md §11 regime gate |
| Position sizing | "Position size within limits" | §11 position sizing limits |
| Sector concentration | "Sector concentration" | §11 sector concentration threshold |
| Earnings proximity | "Earnings proximity" | §11 earnings proximity warning |
| Cash constraint | "Available cash" | §11 cash constraint |

### 2.2 Per-Row Display

Each row shows:

| Element | Display |
|---------|---------|
| Rule label | As per §2.1 table |
| Status indicator | Icon + text: ✅ Pass (green) / ⚠️ Warn (amber) / ❌ Advisory fail (red, labelled "Advisory — not blocking") |
| Detail | Short explanation from API response (e.g. "Regime: On", "Position: 5.2% heat — within 8% limit", "Sector: Technology at 18% — approaching 20% threshold") |

### 2.3 Aggregate Status Bar

Above the rule rows: a single line summarising overall result.

| Outcome | Display |
|---------|---------|
| All pass | "All checks passed" (green text) |
| Any warn, no fail | "Review warnings before entering" (amber text) |
| Any advisory fail | "Advisory issues noted — you may still proceed" (red text, with note: "not blocking") |

---

## 3. Override Flow

When one or more rules return advisory fail:

- **"Acknowledge and proceed"** button appears below the rule list (secondary style, amber outlined)
- Clicking records an acknowledgement on the trade plan object: `override_acknowledged: true`
- Once acknowledged: button disappears; a muted note appears: "Issues acknowledged. Plan will save with override noted."
- The **"Save Trade Plan"** button is always available regardless of override state

**No hard blocking of plan submission at any point.**

---

## 4. Loading and Error States

| State | Behaviour |
|-------|-----------|
| Loading (ticker/quantity just set) | Skeleton row for each check (5 rows); header visible |
| Error (endpoint unreachable) | Panel hidden silently; form submission unaffected |
| Partial (some rules missing from response) | Show only rules present in response; missing rules omitted |

---

## 5. API

- **Endpoint:** `GET /portfolio/pre-entry-validation?ticker={ticker}&quantity={n}`
- Response includes per-rule results and aggregate advisory status
- Canonical contract defined in ST-02 backend story

---

## 6. Edit Mode

Panel hidden in edit mode (existing plan already submitted; re-validation is not surfaced on edit).

---

## 7. Playwright Coverage Requirements

| Scenario | Description |
|----------|-------------|
| Panel renders | Set ticker + quantity → panel appears with 5 rule rows |
| Override flow | Advisory fail present → "Acknowledge" button visible → click → button replaced by muted note |
| Plan saves | Submit plan with override acknowledged → plan saved successfully |
| Panel hidden | No ticker set → panel not present |
