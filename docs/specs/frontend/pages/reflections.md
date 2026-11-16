**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.4
**Last Updated:** 2026-11-16 (ST-05, EPIC-02, v9.17, BLG-FE-258 — §2, §3 and §10 superseded by `journal.md`: the reflections are the Journal page's Reflections section; the card body is the modal button and "View trade" is a sibling footer link); prior — 2026-10-16 (v9.13 design gate — ST-03/BLG-FE-227: §5.2 Exit Reason Badge uses the shared exit-reason vocabulary and light/dark badge tokens); prior — 2026-07-06
**Design Source (v0.3 exit-reason badges):** docs/design/2026-10-16__release-v9.13/exit-reason-badges/decision_record.md
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

> **Superseded by `journal.md` (v0.4, ST-05, EPIC-02, v9.17, BLG-FE-258).** The reflections now live in the Journal page's Reflections section (`/Journal?section=reflections`); `/TradeReflection` redirects there. The page heading is "Journal" (`journal.md` §2–§3).

| Element | Spec |
|---------|------|
| Title | "Trade Reflections" |
| Description | "Review and revisit your structured post-trade reflections." |
| Component | `PageHeader` |

---

## 3. Search / Filter Bar

> **Superseded by `journal.md` (v0.4, ST-05, EPIC-02, v9.17, BLG-FE-258).** The search input is replaced by the Journal's shared ticker filter (`journal.md` §3): partial, case-insensitive, ".L" ignored. When the filter matches no closed trade, the empty state reads "No closed trades match {TICKER}." with a "Clear filter" button; the §6 message stays for no closed trades at all (user ruling 2026-11-16, `journal.md` v1.1).

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

*(v0.3 — ST-03, BLG-FE-227; design source `docs/design/2026-10-16__release-v9.13/exit-reason-badges/decision_record.md`)* The badge shows the **short label** and colour from the shared exit-reason module (`src/constants/exitReasons.js`). The canonical table is `trade_history.md` §Exit Reason Labels and Badges. In summary:

| Stored value (legacy aliases resolve first) | Label | Colour family |
|---------------------------------------------|-------|---------------|
| "Stop Loss Hit" (`stop_hit`) | Stop Hit | rose |
| "Trailing Stop" (`trailing_stop`) | Trailing Stop | cyan |
| "Risk-Off Signal" (`market_regime`, `risk_off`, `risk_off_signal`) | Risk-Off | amber |
| "Manual Exit" (`manual`, `manual_exit`) | Manual | violet |
| "Target Reached" (`target`, `target_reached`) | Target | emerald |
| "Partial Profit Taking" (`partial`, `partial_profit_taking`) | Partial | blue |
| Unknown value | As stored (not upper-cased) | slate |
| null | — | — |

Tokens per family `{c}`: `bg-{c}-100 text-{c}-800 border-{c}-200 dark:bg-{c}-500/20 dark:text-{c}-400 dark:border-{c}-500/30`. This replaces the v0.1 legacy-key table, which matched no stored value.

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

> **Superseded by `journal.md` (v0.4, ST-05, EPIC-02, v9.17, BLG-FE-258).** Each card is no longer one `<button>`. The card body is the button that opens the reflection modal, and a sibling "View trade" link in the card footer goes to `/TradeHistory?ticker={ticker}`, so no interactive element is nested in another (`journal.md` §4).

- Each card is a `<button>` element with full click affordance
- No `aria-label` overrides needed — ticker is visible and unambiguous
- `TradeReflectionModal` has its own `aria-label` per `trade_reflection.md`

---

## 11. Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.4 | 2026-11-16 | ST-05 (EPIC-02, v9.17, BLG-FE-258), per `journal.md` §2: §2, §3 and §10 carry a "superseded by `journal.md`" note. The page becomes the Journal's Reflections section; the card body button plus a sibling "View trade" footer link replaces the single card button; the shared ticker filter replaces the search bar; a filtered-empty message is added. Card fields, empty (no trades), loading and modal behaviour unchanged. |
| 0.3 | 2026-10-16 | v9.13 design gate (ST-03, EPIC-01, BLG-FE-227): §5.2 Exit Reason Badge maps the six stored values (legacy keys as aliases) to short labels and light/dark badge tokens from the shared exit-reason module. Design source: `docs/design/2026-10-16__release-v9.13/exit-reason-badges/decision_record.md`. Head of UX & Design sign-off: 2026-10-16. Product Owner approved: 2026-10-16. Head of Specs Team confirmed. |
| 0.2 | 2026-07-06 | v6.7 design gate — R-Multiple N/A / loading-dash text contrast fix (ST-01/ST-02, BLG-FE-87/BLG-FE-88): `text-slate-500` → `text-slate-600 dark:text-slate-400` (bare class failed 3.07–4.24:1 dark-theme and had no light-mode companion). Icon-only usages (§6 empty-state `BookOpen`, §7 loading-spinner `Loader2`) are out of scope per the design decision record's §5 scope boundary — not text, not remediated this cycle. Design source: `docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md`. Head of UX & Design sign-off: 2026-07-06. Head of Specs Team confirmed. |
| 0.1 | 2026-06-26 | Initial spec — v6.3 EPIC-01 ST-02. Covers card grid, R-Multiple display rules (N/A vs —), exit reason badges, search filter, empty state, loading state. Design source: r-multiple-reflection-fix/ux_spec.md. Approved: Product Owner 2026-06-26. Head of Specs Team confirmed. |
