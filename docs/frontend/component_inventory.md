**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2) — Living Reference
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-06
**Source:** BLG-FE-16 (v3.2 ST-13)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# React Component Inventory

**Purpose:** Catalogue of all React UI components in the swing-trading-model frontend. This document is a mandatory living reference — it must be updated whenever a component is added, removed, or significantly changed during Arc 2 development.

---

## Maintenance Obligation

Any engineer adding, removing, or significantly changing a component during Arc 2 development must update this document in the same PR. "Significantly changed" means: renamed, new required props added, variants added/removed, or usage location changes materially. Cosmetic changes (Tailwind class tweaks) do not require an update.

---

## 1. UI Primitives (`src/components/ui/`)

These are shadcn/ui components (built on Radix UI primitives) with local Tailwind styling. They wrap Radix accessibility-compliant primitives and expose a consistent API.

| Component | File | Purpose | Key Props | Notes |
|-----------|------|---------|-----------|-------|
| `DataState` | `DataState.js` | Three-state wrapper: loading / error / empty / children | `loading`, `error`, `onRetry`, `empty`, `emptyIcon`, `emptyHeading`, `emptyBody`, `emptyAction`, `children`, `className` | Custom. Primary pattern for all API-backed views. Priority: loading > error > empty > children |
| `PageHeader` | `PageHeader.js` | Animated page title + description + right-side actions | `title`, `description`, `actions` | Custom. Used on every page. Framer Motion fade-in-down animation |
| `StatsCard` | `StatsCard.js` | Metric card with icon, value, trend indicator, tooltip | `title`, `value`, `subtitle`, `icon`, `trend` (up/down/neutral), `trendValue`, `gradient`, `className`, `tooltip` | Custom. Portal-based tooltip. Used on Dashboard, PerformanceAnalytics |
| `StatusBadge` | `StatusBadge.js` | Coloured pill badge for trade/regime status | `status` (risk_on/risk_off/open/closed/active/draft/…), `className` | Custom. Supports open, closed, risk_on, risk_off, active, draft |
| `DataTable` | `DataTable.js` | Sortable/filterable table with row click | `data`, `columns`, `onRowClick` | Custom. Used on TradeHistory |
| `Button` | `button.js` | Primary action button | `variant` (default/outline/ghost/link/destructive/secondary), `size` (default/sm/lg/icon) | shadcn/radix |
| `Badge` | `badge.js` | Inline status label | `variant` (default/secondary/destructive/outline) | shadcn/radix |
| `Card`, `CardHeader`, `CardContent`, `CardFooter` | `card.js` | Content card container | — | shadcn/radix |
| `Dialog`, `DialogContent`, `DialogHeader`, etc. | `dialog.js` | Modal overlay | `open`, `onOpenChange` | shadcn/radix |
| `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent` | `tabs.js` | Tabbed navigation | `defaultValue`, `value`, `onValueChange` | shadcn/radix |
| `Select`, `SelectContent`, etc. | `select.js` | Dropdown selector | `value`, `onValueChange` | shadcn/radix |
| `Input` | `input.js` | Text input | `type`, `value`, `onChange`, `placeholder`, `disabled` | shadcn/radix |
| `Textarea` | `textarea.js` | Multi-line text input | `rows`, `value`, `onChange`, `placeholder` | shadcn/radix |
| `Checkbox` | `checkbox.js` | Boolean checkbox | `checked`, `onCheckedChange`, `id` | shadcn/radix |
| `Switch` | `switch.js` | Toggle switch | `checked`, `onCheckedChange` | shadcn/radix |
| `Slider` | `slider.js` | Range slider | `value`, `onValueChange`, `min`, `max`, `step` | shadcn/radix |
| `Separator` | `separator.js` | Horizontal/vertical divider | `orientation` | shadcn/radix |
| `Skeleton` | `skeleton.js` | Loading placeholder | `className` | shadcn/radix |
| `Toast`, `Toaster` | `toast.js`, `toaster.js` | Notification toasts | Triggered via `use-toast.js` hook | shadcn/radix |
| `Tooltip`, `TooltipContent`, etc. | `tooltip.js` | Hover tooltip | `delayDuration` | shadcn/radix |
| `Accordion`, `AccordionItem`, etc. | `accordion.js` | Collapsible section list | `type`, `collapsible` | shadcn/radix |
| `AlertDialog` | `alert-dialog.js` | Confirmation dialog | `open`, `onOpenChange` | shadcn/radix |
| `Alert`, `AlertDescription`, `AlertTitle` | `alert.js` | Inline alert banner | `variant` (default/destructive) | shadcn/radix |
| `Popover`, `PopoverContent`, `PopoverTrigger` | `popover.js` | Floating content panel | `open`, `onOpenChange` | shadcn/radix |
| `DropdownMenu` and sub-components | `dropdown-menu.js` | Context/action menu | `open`, `onOpenChange` | shadcn/radix |
| `Sheet`, `SheetContent`, etc. | `sheet.js` | Slide-in drawer panel | `open`, `onOpenChange`, `side` | shadcn/radix |
| `Progress` | `progress.js` | Progress bar | `value` (0–100) | shadcn/radix |
| `Avatar`, `AvatarImage`, `AvatarFallback` | `avatar.js` | User avatar | `src`, `alt` | shadcn/radix |
| `Chart` | `chart.js` | Recharts wrapper | `config` | shadcn/radix |
| `Table`, `TableHead`, `TableRow`, etc. | `table.js` | Styled HTML table primitives | — | shadcn/radix |
| `Label` | `label.js` | Form label | `htmlFor` | shadcn/radix |
| `Form` and sub-components | `form.js` | React Hook Form integration | — | shadcn/radix |
| `Command` | `command.js` | Command palette | `value`, `onValueChange` | shadcn/radix |
| `Sidebar` | `sidebar.js` | Navigation sidebar scaffold | — | shadcn/radix |
| `Pagination` | `pagination.js` | Page navigation | — | shadcn/radix |
| `ScrollArea` | `scroll-area.js` | Custom-scrollbar container | — | shadcn/radix |
| `Drawer` | `drawer.js` | Bottom sheet drawer | `open`, `onOpenChange` | shadcn/radix |
| `Collapsible` | `collapsible.js` | Toggle-show section | `open`, `onOpenChange` | shadcn/radix |
| `Calendar` | `calendar.js` | Date picker calendar | `selected`, `onSelect`, `mode` | shadcn/radix |
| `Carousel` | `carousel.js` | Content carousel | — | shadcn/radix |
| `HoverCard` | `hover-card.js` | Hover-triggered card | `openDelay` | shadcn/radix |
| `NavigationMenu` | `navigation-menu.js` | Top-level nav | — | shadcn/radix |
| `Menubar` | `menubar.js` | Horizontal menu bar | — | shadcn/radix |
| `ContextMenu` | `context-menu.js` | Right-click context menu | — | shadcn/radix |
| `RadioGroup`, `RadioGroupItem` | `radio-group.js` | Mutually exclusive selection | `value`, `onValueChange` | shadcn/radix |
| `InputOtp` | `input-otp.js` | OTP entry | `maxLength` | shadcn/radix |
| `Resizable` | `resizable.js` | Resizable panel layout | — | shadcn/radix |
| `AspectRatio` | `aspect-ratio.js` | Fixed-ratio container | `ratio` | shadcn/radix |
| `Breadcrumb` | `breadcrumb.js` | Navigation breadcrumb | — | shadcn/radix |
| `Sonner` | `sonner.js` | Alternative toast (sonner) | — | shadcn/radix |
| `Toggle`, `ToggleGroup` | `toggle.js`, `toggle-group.js` | Press-to-toggle button | `pressed`, `variant`, `size` | shadcn/radix |
| `use-mobile` | `use-mobile.js` | Hook: mobile breakpoint detection | Returns `boolean` | shadcn hook |
| `use-toast` | `use-toast.js` | Hook: trigger/dismiss toasts | Returns `{ toast, dismiss }` | shadcn hook |

**Duplication note:** `StatusBadge.js` and inline signal badge definitions (in Watchlist.js, Research.js, Screener.js) overlap. Arc 2 work should consolidate signal/status badge variants into `StatusBadge.js`.

---

## 2. Analytics Components (`src/components/analytics/`)

Used exclusively in `PerformanceAnalytics.js`.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `AdvancedMetricsGrid` | `AdvancedMetricsGrid.js` | Grid of advanced statistical metrics | `data` (analytics response) |
| `BestWorstTrades` | `BestWorstTrades.js` | Top/bottom performer table | `data` |
| `CohortAnalysis` | `CohortAnalysis.js` | Time-cohort performance breakdown | `data` |
| `ConsistencyMetrics` | `ConsistencyMetrics.js` | Win-rate streaks and consistency stats | `data` |
| `DisciplineComplianceSection` | `DisciplineComplianceSection.js` | Compliance rule adherence summary | `data` |
| `ExecutiveSummaryCards` | `ExecutiveSummaryCards.js` | Top-level KPI cards row | `data` |
| `ExitReasonTable` | `ExitReasonTable.js` | Exit reason breakdown table | `data` |
| `KeyInsightsCard` | `KeyInsightsCard.js` | Text insight cards | `data` |
| `MarketComparison` | `MarketComparison.js` | Portfolio vs benchmark chart | `data` |
| `MarketCorrelationSection` | `MarketCorrelationSection.js` | Correlation scatter/table | `data` |
| `MetricsStalenessIndicator` | `MetricsStalenessIndicator.js` | Warning when analytics data is stale | `lastUpdated` |
| `MonthlyHeatmap` | `MonthlyHeatmap.js` | Month-by-month P&L heatmap grid | `data` |
| `RMultipleAnalysis` | `RMultipleAnalysis.js` | R-multiple distribution stats | `data` |
| `RMultipleDistribution` | `RMultipleDistribution.js` | R-multiple histogram chart | `data` |
| `TagPerformance` | `TagPerformance.js` | Performance breakdown by trade tag | `data` |
| `TimeBasedCharts` | `TimeBasedCharts.js` | Time-series equity/P&L charts | `data` |
| `TopPerformers` | `TopPerformers.js` | Best-performing tickers | `data` |
| `UnderwaterChart` | `UnderwaterChart.js` | Drawdown from peak over time | `data` |
| `WinRateByMonth` | `WinRateByMonth.js` | Monthly win rate trend | `data` |

---

## 3. Chart Components (`src/components/charts/`)

Recharts-based chart wrappers. Used across Dashboard and Reports pages.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `AllocationChart` | `AllocationChart.js` | Pie/donut sector allocation | `data` |
| `PnLBarChart` | `PnLBarChart.js` | Bar chart of P&L by period | `data` |
| `PortfolioChart` | `PortfolioChart.js` | Equity curve line chart | `data` |
| `WinRateChart` | `WinRateChart.js` | Win rate over time | `data` |

---

## 4. Dashboard Components (`src/components/dashboard/`)

Used in `Dashboard.js` and `DashboardHome.js`.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `DashboardWidget` | `DashboardWidget.js` | Wrapper tile for dashboard widgets | `title`, `children`, `className` |
| `MarketRegimeCard` | `MarketRegimeCard.js` | Current market regime display | `regime` |
| `QuickActions` | `QuickActions.js` | Fast-action button grid | — |
| `WidgetLibrary` | `WidgetLibrary.js` | Widget selection/add panel | `onAdd` |
| `useDashboardLayout` | `useDashboardLayout.js` | Hook: persisted widget layout | Returns `{ layout, setLayout }` |
| `DashboardCard` | `home/DashboardCard.js` | Card scaffold for home dashboard | `title`, `children` |
| `GracePeriodCard` | `home/GracePeriodCard.js` | Holds-within-grace-period metric | `data` |
| `OpenPositionsCard` | `home/OpenPositionsCard.js` | Summary of open positions | `data` |
| `PortfolioHeatCard` | `home/PortfolioHeatCard.js` | Portfolio heat gauge on home screen | `data` |
| `RecentActivityCard` | `home/RecentActivityCard.js` | Recent trade activity feed | `data` |
| `SignalStatusCard` | `home/SignalStatusCard.js` | Active momentum signal count | `data` |
| `CurrentDrawdownWidget` | `widgets/CurrentDrawdownWidget.js` | Live drawdown metric widget | `data` |
| `RecentTradesWidget` | `widgets/RecentTradesWidget.js` | Recent trade list widget | `data` |
| `StatsWidgets` | `widgets/StatsWidgets.js` | Collection of stat metric widgets | `data` |

---

## 5. Position Components (`src/components/positions/`)

Used in `Positions.js`.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `ExitModal` | `ExitModal.js` | Exit position dialog | `position`, `open`, `onClose`, `onExited` |
| `JournalView` | `JournalView.js` | Trade journal entry viewer | `position` |
| `PositionCard` | `PositionCard.js` | Mobile card view of a position | `position`, `onAction` |
| `PositionModal` | `PositionModal.js` | Edit position details modal | `position`, `open`, `onClose` |
| `StrategyCompliancePanel` | `StrategyCompliancePanel.js` | ATR/grace period compliance flags | `position` |

---

## 6. Reports Components (`src/components/reports/`)

Used in `Reports.js`.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `ExportModal` | `ExportModal.js` | CSV export dialog | `open`, `onClose` |
| `PerformanceSummary` | `PerformanceSummary.js` | High-level performance summary | `data` |
| `PortfolioGrowthChart` | `PortfolioGrowthChart.js` | Portfolio value over time | `data` |
| `TradeBreakdown` | `TradeBreakdown.js` | Trade-by-trade table | `data` |

---

## 7. Risk Components (`src/components/risk/`)

Used in `RiskDashboard.js`.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `DrawdownSummary` | `DrawdownSummary.js` | Drawdown metrics summary | `data` |
| `GracePeriodPanel` | `GracePeriodPanel.js` | Grace period position tracker | `data` |
| `HeatGauge` | `HeatGauge.js` | Circular portfolio heat gauge | `heat` (0–1 float) |
| `PositionRiskTable` | `PositionRiskTable.js` | Per-position ATR/stop risk table | `positions` |
| `ProspectiveHeatPanel` | `ProspectiveHeatPanel.js` | Prospective heat for hypothetical entry | `ticker`, `shares`, `entryPrice`, `stopPrice` |

**Note:** `ProspectiveHeatPanel` and the heat region in `Research.js` (ST-03) serve overlapping purposes. Arc 2 should evaluate unifying these into a shared component.

---

## 8. Signals Components (`src/components/signals/`)

Used in `Signals.js`.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `MarketStatusBar` | `MarketStatusBar.js` | Regime/market status banner | `status` |
| `PositionEntryModal` | `PositionEntryModal.js` | Confirm entry from signal | `signal`, `open`, `onClose` |
| `SignalCard` | `SignalCard.js` | Individual momentum signal card | `signal`, `onAction` |

---

## 9. Trades Components (`src/components/trades/`)

Used in `TradeHistory.js` and `TradeEntry.js`.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `PositionSizingWidget` | `PositionSizingWidget.js` | ATR-based position size calculator | `ticker`, `market`, `price`, `atr` |
| `TradeHistoryTable` | `TradeHistoryTable.js` | Closed trade table | `trades`, `onSelect` |
| `TradeReflectionModal` | `TradeReflectionModal.js` | Post-trade reflection form | `trade`, `open`, `onClose` |

---

## 10. Watchlist Components (`src/components/watchlist/`)

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `WatchlistModal` | `WatchlistModal.js` | Add/edit/delete watchlist entry modal | `mode` (add/edit/edit-confirm), `entry`, `onAdded`, `onUpdated`, `onDeleted`, `onClose` |

---

## 11. Notification Components (`src/components/notifications/`)

Used in `Notifications.js` and `NotificationPreferences.js`.

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `AlertThresholdsSection` | `AlertThresholdsSection.js` | Alert threshold config section | `thresholds`, `onChange` |
| `NotificationRow` | `NotificationRow.js` | Single notification item row | `notification`, `onDismiss` |
| `NotificationTabBar` | `NotificationTabBar.js` | Tab bar for notification categories | `activeTab`, `onTabChange` |
| `PreferenceRow` | `PreferenceRow.js` | Single notification preference toggle | `pref`, `onChange` |

---

## 12. Monitor Components (`src/components/monitor/`)

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `MonitorModal` | `MonitorModal.js` | Real-time monitor/log modal | `open`, `onClose` |

---

## 13. Cash Components (`src/components/cash/`)

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `CashManagementModal` | `CashManagementModal.js` | Cash deposit/withdrawal modal | `open`, `onClose`, `onSuccess` |

---

## 14. Top-Level Components (`src/components/`)

| Component | File | Purpose | Key Props |
|-----------|------|---------|-----------|
| `UserNotRegisteredError` | `UserNotRegisteredError.js` | Error screen when user not registered in system | — |

---

## Hooks (`src/hooks/`)

| Hook | File | Purpose | Returns |
|------|------|---------|---------|
| `useEarnings` | `useEarnings.js` | Fetch earnings date for a ticker | `{ data, loading }` — polls `GET /earnings/{ticker}?market={m}` |
| `use-mobile` | `src/components/ui/use-mobile.js` | Detect mobile viewport | `boolean` |
| `use-toast` | `src/components/ui/use-toast.js` | Toast notification control | `{ toast, dismiss }` |
| `useDashboardLayout` | `src/components/dashboard/useDashboardLayout.js` | Persist dashboard widget layout | `{ layout, setLayout }` |

---

## Duplication and Reuse Opportunities

| Issue | Components Involved | Recommendation |
|-------|--------------------|-|
| Signal badge inline definitions | `Watchlist.js` (SignalBadge), `Research.js` (SignalBadge), `Screener.js` (inline) | Extract to `src/components/ui/SignalBadge.js` and share |
| Market badge inline definitions | `Watchlist.js` (MarketBadge), `Screener.js` (MarketBadge) | Extract to `src/components/ui/MarketBadge.js` |
| Prospective heat display | `ProspectiveHeatPanel.js` vs heat region in `Research.js` | Evaluate unifying into a shared `HeatDisplay` component in Arc 2 |
| Relative time formatting | `Screener.js` (relativeTime), `Research.js` (relativeTime), `Watchlist.js` (news) | Extract to `src/lib/formatters.js` |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-06 | Initial inventory. v3.2 ST-13 (BLG-FE-16). All components at time of v3.2 Sprint 2 start. |
