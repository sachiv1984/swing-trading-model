**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-16__release-v9.13
**Story:** ST-03 (EPIC-01, BLG-FE-227)

# Decision Record — One Exit-Reason Vocabulary: Labels and Badge Colours

## 1. Problem

`ExitModal.js` stores six title-case values: "Manual Exit", "Stop Loss Hit", "Trailing Stop", "Risk-Off Signal", "Target Reached" and "Partial Profit Taking". Trade Reflections (`TradeReflection.js`, `TradeReflectionModal.js`) and Performance Analytics map only legacy keys (`stop_hit`, `manual`, `target`, `market_regime`). So every Reflections card shows a grey badge with raw upper-case text. Trade History (`TradeHistoryTable.js`) maps all six values, but with its own copy. `ExportModal.js`, `TradeBreakdown.js` and `MonthlyHeatmap.js` keep further copies.

The existing tinted badges use dark-only text (`text-*-400` on `*-500/20`). That measures 1.4–2.1:1 in the light theme, which `design_system.md` §Light-Theme Colour Tokens rule 1 counts as a defect.

## 2. Decision

### 2.1 Vocabulary

`src/constants/exitReasons.js` holds one entry per stored value. The §8 category comes from ST-02's mapping in `data_model.md`. The column below shows the expected mapping and is not this record's decision.

| Stored value | Full label | Short label (badges) | Colour family | §8 category (from ST-02) |
|--------------|------------|----------------------|---------------|--------------------------|
| "Stop Loss Hit" | Stop Loss Hit | Stop Hit | rose | §8.1 Stop-loss trigger |
| "Trailing Stop" | Trailing Stop | Trailing Stop | cyan | §8.1 Stop-loss trigger |
| "Risk-Off Signal" | Risk-Off Signal | Risk-Off | amber | §8.2 Market risk-off override |
| "Manual Exit" | Manual Exit | Manual | violet | §8.3 Manual exit |
| "Target Reached" | Target Reached | Target | emerald | §8.3 Manual exit |
| "Partial Profit Taking" | Partial Profit Taking | Partial | blue | §8.3 Manual exit |

- **Legacy aliases** resolve to a stored value before lookup: `stop_hit` → Stop Loss Hit; `manual`, `manual_exit` → Manual Exit; `target`, `target_reached` → Target Reached; `market_regime`, `risk_off`, `risk_off_signal` → Risk-Off Signal; `trailing_stop` → Trailing Stop; `partial`, `partial_profit_taking` → Partial Profit Taking.
- **Unknown value:** shown as stored (not upper-cased), with the slate badge. **Null:** "—".
- Colour is per value, matching the six colours Trade History already ships. The label carries the meaning, so colour is never the only signal.

### 2.2 Where each label is used

- **Badges** (Trade Reflections cards, Trade History rows, Trade Reflection modal header if a badge is shown): short label.
- **Text fields and tables** (Trade Reflection modal "Exit Reason" summary row, `ExitModal`'s select, Performance by Exit Reason table, exports): full label.

### 2.3 Badge tokens (light and dark)

Every exit-reason badge uses `rounded-full border px-2 py-0.5 text-xs font-medium` with this pair per colour family `{c}`:

`bg-{c}-100 text-{c}-800 border-{c}-200 dark:bg-{c}-500/20 dark:text-{c}-400 dark:border-{c}-500/30`

The slate fallback is `bg-slate-100 text-slate-800 border-slate-200 dark:bg-slate-500/20 dark:text-slate-400 dark:border-slate-500/30`.

Measured contrast (WCAG 2.1):

| Family | Light (`-800` on `-100`) | Dark (`-400` on `-500/20` over the `bg-slate-800/50` card on `slate-900`) |
|--------|-------------------------|---------------------------------------------------------------------------|
| rose | 6.68 | 4.96 |
| cyan | 6.49 | 6.32 |
| amber | 6.37 | 6.77 |
| violet | 7.57 | 4.77 |
| emerald | 6.78 | 6.00 |
| blue | 7.15 | 4.89 |
| slate | 13.35 | 5.10 |

All pass 4.5:1. The dark values are unchanged from today's Trade History badges. `-700` text on the `-500/20` tint was rejected: amber (4.32) and cyan (4.44) fail on white.

## 3. §13 Compliance

Display only. The category is descriptive and drives no behaviour.

## 4. Frontend Spec Impact

- `reflections.md` v0.2 → v0.3: §5.2 Exit Reason Badge replaced by a reference to the shared vocabulary and tokens.
- `trade_reflection.md` v0.3 → v0.4: §4 Exit Reason format is the full label from the shared module.
- `trade_history.md` v1.15 → v1.16: new §Exit Reason Labels and Badges, which holds the canonical table for all consumers.

## 5. Obligations for Sprint Execution

- Every frontend exit-reason map imports the module, including the three not named in the AC's parenthetical: `ExportModal.js`, `TradeBreakdown.js` and `MonthlyHeatmap.js` (AC 3: "no frontend file"). `src/lib/exitCondition.js`'s three `EXIT_REASON_*` constants re-export from the module. See the addendum.
- `StrategyBenchmark.js`'s map covers backtest-engine reasons (`exit_stop`, `exit_rebalance`, …), not stored `exit_reason` values. It is out of scope.

## 6. Testability (CLAUDE.md §2)

- Playwright: mocked trades with each of the six stored values plus one legacy key. Each Trade Reflections card badge shows its short label, and `toHaveCSS('background-color', …)` matches its family, in both themes (AC 2, AC 4).
- The light-theme axe scan of Trade Reflections reports no `color-contrast` violation on the badges.
- Unit: every alias resolves, and every stored value has exactly one §8 category.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-16.
Product Owner: confirmed, 2026-10-16.
