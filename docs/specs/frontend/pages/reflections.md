**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.2
**Last Updated:** 2026-07-06
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Release:** v6.7
**EPIC:** EPIC-01
**Design Source:** docs/design/2026-06-26__release-v6.3/r-multiple-reflection-fix/ux_spec.md
**Design Source (v0.2 additions):** docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md (BLG-FE-87/88 remediation)
**Confirmed by:** Head of Specs Team — 2026-06-26

---

# Frontend Specification — Reflections Page

## 1. Purpose & User Goals

The Reflections page provides a navigable gallery of all closed trades for which structured post-trade reflections are available. Users can review past trade outcomes at a glance and open the full reflection modal for any trade.

**Route:** `/reflections`
**Navigation label:** "Reflections"
**Source component:** `src/pages/TradeReflection.js`

Users should be able to:
- Scan closed trades and their key metrics (P&L, R-Multiple, hold period, exit reason)
- Filter trades by ticker to find a specific trade quickly
- Open the reflection modal to read or edit a structured reflection

---

## 2. Page Header

| Element | Spec |
|---------|------|
| Title | "Trade Reflections" |
| Description | "Review and revisit your structured post-trade reflections." |
| Component | `PageHeader` |

---

## 3. Search / Filter Bar

| Element | Spec |
|---------|------|
| Input | Text field, `placeholder="Search by ticker…"` |
| Filter scope | `ticker` field only (case-insensitive) |
| Width | `max-w-sm` |
| Icon | `Search` (Lucide), left-inset |
| Behaviour | Real-time filter as user types; no submit button |

---

## 4. Card Grid Layout

| Breakpoint | Columns |
|-----------|---------|
| Default (mobile) | 1 column |
| `md` (≥ 768px) | 2 columns |
| `xl` (≥ 1280px) | 3 columns |

Each card is a clickable button; full card surface is the click target.

---

## 5. Card — Field Specifications

### 5.1 Card Header Row

| Field | Source | Format |
|-------|--------|--------|
| Ticker | `r.ticker` | `text-lg font-bold text-white`; hover: `text-cyan-400` |
| Market badge | `r.market` | Small pill badge; "—" if absent |
| Exit reason badge | `r.exit_reason` | See §5.2 |

### 5.2 Exit Reason Badge

| Exit Reason | Label | Colour |
|-------------|-------|--------|
| `stop_hit` | STOP | `bg-rose-500/20 text-rose-400 border-rose-500/30` |
| `manual` | MANUAL | `bg-violet-500/20 text-violet-400 border-violet-500/30` |
| `target` | TARGET | `bg-emerald-500/20 text-emerald-400 border-emerald-500/30` |
| `market_regime` | REGIME | `bg-amber-500/20 text-amber-400 border-amber-500/30` |
| other / null | Uppercased raw value | Slate default |

### 5.3 Metrics Row (3-column grid within card)

| Metric | Label | Source | Format | Colour |
|--------|-------|--------|--------|--------|
| P&L | "P&L" | `r.pnl` | `+£X.XX` / `£X.XX`; 2dp | Profit: `text-emerald-400`; Loss: `text-rose-400` |
| R-Multiple | "R-Multiple" | `r.r_multiple` | See §5.4 | See §5.4 |
| Hold | "Hold" | `r.hold_days` | `Nd` (e.g. "14d"); "—" if null | `text-slate-300` |

### 5.4 R-Multiple Display Rules

| Condition | Display | Colour | Tooltip |
|-----------|---------|--------|---------|
| Value present, ≥ 0 | `+X.XXR` (signed, 2dp, "R" suffix) | `text-emerald-400` | None |
| Value present, < 0 | `-X.XXR` (signed, 2dp, "R" suffix) | `text-rose-400` | None |
| Value null — no stop loss | `N/A` | `text-slate-600 dark:text-slate-400` | "No stop loss recorded for this trade — R cannot be computed" |
| Value null — loading | `—` (em dash) | `text-slate-600 dark:text-slate-400` | None |

**Distinction (hard rule):** `N/A` is used only when `r_multiple` is null AND the trade has been resolved (data is settled, not loading). The em dash `—` is reserved for loading or unresolved states. Do not display `N/A` during loading.

### 5.5 Card Footer

| Field | Source | Format |
|-------|--------|--------|
| Exit date | `r.exit_date` | `Calendar` icon + "DD Mon YYYY"; "—" if null |

### 5.6 Card Interaction

| State | Behaviour |
|-------|-----------|
| Default | `border-slate-700/50` |
| Hover | `border-cyan-500/40 shadow-lg shadow-cyan-500/5` |
| Click | Opens `TradeReflectionModal` with this trade as prop |

---

## 6. Empty State

Shown when no closed trades match the current search (or no trades at all):

| Element | Spec |
|---------|------|
| Icon | `BookOpen` (Lucide), `text-slate-600` |
| Message | "No closed trades yet — close a trade to write your first reflection." |
| Container | Full-width card: `bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center` |

---

## 7. Loading State

Full-page spinner centred vertically:

| Element | Spec |
|---------|------|
| Icon | `Loader2` (Lucide), `w-8 h-8 animate-spin text-slate-500` |
| Container | `flex items-center justify-center py-24` |

---

## 8. Data Source

| Source | Endpoint |
|--------|---------|
| Trade reflection list | `base44.entities.TradeReflection.list()` (GET /trades with reflection data) |

**Query key:** `["trade-reflections-list"]`

---

## 9. Reflection Modal Integration

On card click, `TradeReflectionModal` opens with `trade={r}` and `open={true}`.

On close: `setSelectedTrade(null)` — modal closes; grid view remains.

The modal spec is documented separately in `trade_reflection.md`.

---

## 10. Accessibility

- Each card is a `<button>` element with full click affordance
- No `aria-label` overrides needed — ticker is visible and unambiguous
- `TradeReflectionModal` has its own `aria-label` per `trade_reflection.md`

---

## 11. Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.2 | 2026-07-06 | v6.7 design gate — R-Multiple N/A / loading-dash text contrast fix (ST-01/ST-02, BLG-FE-87/BLG-FE-88): `text-slate-500` → `text-slate-600 dark:text-slate-400` (bare class failed 3.07–4.24:1 dark-theme and had no light-mode companion). Icon-only usages (§6 empty-state `BookOpen`, §7 loading-spinner `Loader2`) are out of scope per the design decision record's §5 scope boundary — not text, not remediated this cycle. Design source: `docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md`. Head of UX & Design sign-off: 2026-07-06. Head of Specs Team confirmed. |
| 0.1 | 2026-06-26 | Initial spec — v6.3 EPIC-01 ST-02. Covers card grid, R-Multiple display rules (N/A vs —), exit reason badges, search filter, empty state, loading state. Design source: r-multiple-reflection-fix/ux_spec.md. Approved: Product Owner 2026-06-26. Head of Specs Team confirmed. |
