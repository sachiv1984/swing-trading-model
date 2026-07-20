**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-20
**Approved by:** Product Owner — 2026-07-20
**Story:** ST-07 — Add consolidated Gemini + Claude monthly cost summary (EPIC-07, BLG-FEAT-77)
**Cycle:** 2026-07-20__release-v7.6

---

# UX Specification — Consolidated Monthly AI Cost View

## 1. Context

`BLG-FEAT-77`: Gemini thesis-generation cost tracking (`gemini_audit_log`) and Claude API cost tracking (`POST /ai/check-daily-cost`) exist today as two separate cost-monitoring surfaces with **no frontend rendering at all** — both are backend/ops-only (`docs/ops/gemini_cost_tracking.md`, `docs/ops/claude_cost_review_2026-05.md`). No per-provider AI cost figure is displayed anywhere in the app today. This item is the first frontend surface for either.

The AC names "an existing settings/reports surface" without specifying which. Neither existing page is a clean fit as-is:
- **Reports** (`reports.md`) is scoped to trade performance (P&L, tax year) — AI spend is not trade data.
- **Settings** (`settings.md`) is scoped to editable configuration (strategy parameters, fees, preferences, limits) — this is a read-only monitoring figure, not a setting to change.

## 2. Placement Decision

**Settings**, as a new read-only section. Rationale:
- Settings already houses a cost-adjacent domain (§2 Commission & Fees) — users already look here for "what does this cost me" figures, even though that section is trading fees rather than AI spend. It is the closer conceptual neighbour of the two candidates.
- Reports is exclusively trade-performance data sourced from `trade_history`/`trade_plans`; mixing in an unrelated operational-cost figure would break that page's single-purpose framing (confirmed against `reports.md` §1 Purpose & User Goals).
- Settings already tolerates non-form, display-only content precedent is new with this item, but the SectionCard layout (icon, title, content) accommodates a read-only card as easily as a form card — no structural change needed.

New section: **"AI Usage & Costs"**, added as a 6th SectionCard, after the existing **Analytics** section (i.e. last on the page). It is monitoring/informational, not configuration, so it is placed after all editable sections rather than interleaved with them.

## 3. Decision — Content and Layout

### 3.1 Section Card

| Element | Content |
|---------|---------|
| Icon | `DollarSign` (lucide-react) or equivalent cost icon, consistent with other SectionCard icons |
| Title | "AI Usage & Costs" |
| Subtitle/helper text | "Combined AI provider spend for the current calendar month" |

### 3.2 Fields (read-only, no form controls)

| Row | Source | Format |
|-----|--------|--------|
| Gemini (thesis generation) | `gemini_audit_log`, current-month sum | `$X.XX` |
| Claude (trade plan / chat) | `POST /ai/check-daily-cost` equivalent monthly aggregate | `$X.XX` |
| **Combined total** | Client-side sum of the two rows above | `$X.XX`, bold, visually separated (top border) from the two provider rows — same "combined total" treatment as `reports.md`'s Monthly P&L Report Combined Total line |

No new combined-total endpoint: the total is computed client-side as the sum of the two provider figures, matching the AC's requirement that it "matches the sum of the two existing per-provider sources" by construction, and following the existing `reports.md` Combined Total precedent (client-side sum, no new endpoint).

### 3.3 No Save/Edit Behaviour

This section does not participate in the page's `Save Settings` mutation — it renders independent of `formData` and does not call `PUT /settings`. It is excluded from the Save button's scope (which remains "Strategy Parameters" through "Risk Limits" as today).

### 3.4 Data Loading

- Loaded via its own query (independent of the main settings `GET /settings` query), so a slow/failed cost fetch never blocks the rest of the Settings page from being usable.
- Loading: inline skeleton within the card only (matches `trade_plan.md` §7a's "inline skeleton placeholder" convention for a self-contained async section).
- Error: card shows "AI cost data unavailable" with no numeric fallback (never render `$0.00` or `—` as if it were a real reading) — section does not block the rest of the page (matches `trade_plan.md` §7a's "error hidden silently... does not block page" precedent, adapted to show an explicit unavailable message here since this section's entire content is the cost figures — silently hiding the whole card would look like the feature doesn't exist).

## 4. §13 Compliance

Display-only monitoring figure. No automated decision-making, no trade or position-sizing logic, no alerting/threshold behaviour introduced by this item (the existing backend `check-daily-cost` alerting is unchanged and out of scope).

## 5. States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton in place of the three rows |
| Loaded | Gemini row, Claude row, Combined Total row (bold, separated) |
| Error | "AI cost data unavailable" message; rest of Settings page unaffected |

## 6. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-20
- **Product Owner:** Approved — 2026-07-20
