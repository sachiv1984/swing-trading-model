**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-19__release-v3.8
**Stories:** ST-06 (Setup Type field), ST-07 (News Context Panel), ST-08 (AI Thesis Generation) — EPIC-03
**Sources:** BLG-FEAT-23, BLG-FE-36, BLG-FEAT-24; trade_plan.md v0.6; strategy_rules.md §13
**Approved by:** Product Owner
**Approved date:** 2026-05-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Trade Plan Form Enhancements (v3.8)

This spec covers three interrelated enhancements to the trade plan creation and edit form. They are documented together because they share layout positioning within the form.

> **§13 Compliance:** All three features are advisory/decision-support. No automated position recommendation is generated. Setup Type and news headlines are user-inputted context. AI thesis generation is template-based and explicitly labelled as a draft. Override and edit capabilities are always present.

---

## Section A — Setup Type Classification Field (ST-06)

### A.1 Field Specification

| Attribute | Value |
|-----------|-------|
| Field label | "Setup Type" |
| Field type | Select (dropdown) |
| Required | No (nullable) |
| DB column | `setup_type` VARCHAR, nullable, on `trade_plans` |
| Position in form | Above the Setup Thesis textarea (§A.3 for full form order) |

### A.2 Options

| Value | Display label |
|-------|--------------|
| `breakout` | Breakout |
| `pullback_to_ma` | Pullback to MA |
| `momentum_continuation` | Momentum Continuation |
| `mean_reversion` | Mean Reversion |
| `catalyst_driven` | Catalyst-driven |
| `other` | Other |

Placeholder text: "Select setup type…" (unset state)

### A.3 Signal-Driven Default

When the trade plan form is opened from a momentum signal context (i.e. the URL includes `?signal_id=…` or the Signal Context Panel (§5a of trade_plan.md) is present and active), the Setup Type dropdown defaults to **"Momentum Continuation"** on initial load. This default is advisory — user may change.

In all other contexts: no default. Field starts unset.

### A.4 Persistence

- `POST /trade-plans` accepts `setup_type` (string or null)
- `PUT /trade-plans/{id}` accepts `setup_type` (string or null)
- `GET /trade-plans/{id}` includes `setup_type` in response
- Existing plans without `setup_type` display field as unset — no migration required for display

### A.5 Read View

Setup Type shown in the Trade Plan detail view below ticker/status, above stop level. Label: "Setup Type". Display value is the display label (e.g. "Breakout"), not the raw key. Unset: "—"

---

## Section B — News Context Panel (ST-07)

### B.1 Presence Condition

- Shown in the trade plan creation form when a US ticker is set
- Not shown for UK tickers (Alpaca News API covers US only)
- Hidden entirely if news API returns no results (not an error state — just hidden)
- Positioned above the Setup Type dropdown (§A) and setup thesis textarea

### B.2 Panel Content

**Panel header:** "News Context" (read-only section, visually distinct — muted background `bg-gray-50`)

Per headline (up to 5 most recent):

| Element | Display |
|---------|---------|
| Headline text | Full title, truncated at 100 chars with "…" |
| Source | Publisher name (e.g. "Reuters", "Bloomberg") |
| Age | Relative time (e.g. "2h ago", "1d ago") |

No sentiment labels, scores, or click-through links.

### B.3 Collapsed State

- Panel is collapsible via a chevron toggle in the panel header
- Collapsed state persisted in `localStorage` keyed by `news-panel-{ticker}` (boolean: collapsed/expanded)
- Default state: expanded on first load for a given ticker

### B.4 API

- **New endpoint:** `GET /news/{ticker}` — proxies to Alpaca News API; returns up to 5 headlines
  - OR reuse existing screener news route if one exists with the same response contract
- If API call fails: panel hidden silently (not an error state; form submission unaffected)
- While loading: single-line skeleton placeholder in panel body (panel header visible)

### B.5 Edit Mode

Panel hidden in edit mode (no regression to saved plan fields).

---

## Section C — AI-Assisted Thesis Generation (ST-08)

### C.1 Form Element

A **"Generate thesis"** button positioned adjacent to (right of, or below) the Setup Thesis textarea label. The button is always visible in creation mode when a ticker is set. It is never auto-triggered.

### C.2 Template Engine (Phase 1 — No API)

On button click, a template is populated from available context in the following priority order:

| Source | Data used |
|--------|-----------|
| Setup Type (§A) | Describes the trade setup pattern |
| Signal Context Panel (trade_plan.md §5a) | Rank, momentum %, MA position, regime |
| News Context Panel (§B) | Top 2 headline texts (if panel present and loaded) |
| Current price | From signal context or most recent price |

Template output example:
> "Momentum Continuation setup. Rank #3 signal with +8.2% momentum; price 12.4% above 200-day MA; US regime on. Recent catalyst: [headline 1 text]. Entry thesis: [space for user to extend]."

The generated text is placed directly into the Setup Thesis textarea, replacing any existing content (user has clicked the button consciously).

**Fallback:** If no signal context is available, the template uses only setup type and available price data. If setup type is also unset, a minimal template is generated: "Setup type: [unset]. Enter your thesis here."

### C.3 "AI Draft" Badge

- An **"AI draft"** badge (small grey pill) appears adjacent to the textarea after generation
- Badge clears on the user's first keystroke within the textarea (i.e. on first edit after generation)
- The badge is purely informational — it does not affect save behaviour

### C.4 Gemini Integration (Phase 2 — Env-Var Gated)

- An **"Improve with AI"** button is shown adjacent to the textarea **only when** `GEMINI_API_KEY` is configured in the environment
- If `GEMINI_API_KEY` is absent or empty: button is hidden entirely (not disabled — not rendered)
- When shown: sends the current textarea content + trade context to Gemini Flash; replaces textarea content with the improved version
- "AI draft" badge re-applied after Gemini improvement

### C.5 Save Behaviour

- Saved plan stores the user's final edited version of the setup thesis, not a flag indicating AI involvement
- No AI metadata is persisted to the database

### C.6 Edit Mode

"Generate thesis" button hidden in edit mode to avoid overwriting existing saved rationale.

---

## Form Layout Order (Creation Mode)

After this spec is applied, the trade plan creation form order is:

1. Ticker symbol (§5.1)
2. Market (§5.1)
3. Status (§5.1)
4. Stop Level (§5.1)
5. Risk/Reward Notes (§5.1)
6. **Signal Context Panel** (§5a — conditional, shown when linked signal exists)
7. **News Context Panel** (§B — conditional, shown for US tickers with news results)
8. **Setup Type dropdown** (§A — always shown)
9. Setup Thesis textarea + **"Generate thesis"** button (§C) + "AI draft" badge (§C.3) + **"Improve with AI"** button (§C.4, env-gated)
10. Pre-Trade Entry Checklist (§6)
11. Save / Cancel (§5.2)
