import { useState, useEffect, useCallback } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { createPageUrl } from "./utils";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  Briefcase,
  PlusCircle,
  History,
  Settings,
  Menu,
  X,
  Sun,
  Moon,
  TrendingUp,
  ExternalLink,
  FileBarChart,
  Zap,
  Activity,
  ShieldAlert,
  Bell,
  Eye,
  CalendarDays,
  ChevronRight,
  ScanSearch,
  Globe,
  Flag,
  BarChart2,
  Search,
} from "lucide-react";
import { Button } from "./components/ui/button";
import { cn } from "./lib/utils";
import { apiFetch } from "./api/base44Client";
import CommandPalette, { OPEN_COMMAND_PALETTE_EVENT } from "./components/CommandPalette";
import { toast } from "sonner";

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const NOTIFICATIONS_PAGES = ["notifications", "NotificationPreferences"];

// Keyboard shortcuts: keys available on each page (ST-11)
const PAGE_SHORTCUTS = {
  Positions:     [{ key: "n", label: "New trade" }, { key: "r", label: "Refresh" }],
  TradeHistory:  [{ key: "n", label: "New trade" }, { key: "r", label: "Refresh" }],
  Screener:      [{ key: "w", label: "Add to watchlist" }, { key: "r", label: "Refresh" }],
  Watchlist:     [{ key: "w", label: "Add to watchlist" }, { key: "r", label: "Refresh" }],
};
const DEFAULT_SHORTCUTS = [{ key: "r", label: "Refresh" }];

// Nav group structure — per navigation.md v1.4 (ST-02, EPIC-02, v7.7, BLG-FE-114)
// v1.4: "Alerts" (formerly Tools group) removed — duplicate destination of
// "Notifications" (System group), which is now the sole nav path and inherits
// the alert-count badge. "Weekly Digest" moved from Analytics to System,
// positioned directly above "Notifications" (both are activity-summary surfaces).
const NAV_GROUPS = [
  {
    label: "Trading",
    key: "trading",
    items: [
      { name: "Positions",     icon: Briefcase,   page: "Positions" },
      { name: "Trade Entry",   icon: PlusCircle,  page: "TradeEntry" },
      { name: "Trade History", icon: History,     page: "TradeHistory" },
      { name: "Reflections",   icon: FileBarChart, page: "TradeReflection" },
      { name: "Red Flag Journal", icon: Flag, page: "RedFlagJournal" },
    ],
  },
  {
    label: "Analytics",
    key: "analytics",
    items: [
      { name: "Analytics",           icon: TrendingUp,   page: "PerformanceAnalytics" },
      { name: "Strategy Benchmark",  icon: BarChart2,    page: "StrategyBenchmark" },
      { name: "Risk Dashboard",      icon: ShieldAlert,  page: "RiskDashboard" },
      { name: "Signals",             icon: Zap,          page: "Signals" },
      { name: "Reports",             icon: FileBarChart,  page: "Reports" },
    ],
  },
  {
    label: "Tools",
    key: "tools",
    items: [
      { name: "Screener",         icon: ScanSearch, page: "Screener" },
      { name: "Watchlist",        icon: Eye,        page: "Watchlist" },
      { name: "Ticker Universe",  icon: Globe,      page: "TickerUniverse" },
    ],
  },
  {
    label: "System",
    key: "system",
    items: [
      { name: "Settings",      icon: Settings,  page: "Settings" },
      { name: "System Status", icon: Activity,  page: "SystemStatus" },
      { name: "Weekly Digest", icon: CalendarDays, page: "WeeklyDigest" },
      { name: "Notifications", icon: Bell,      page: "notifications", alertBadge: true },
    ],
  },
];

function getActiveGroupKey(pageName) {
  // alertBadge items are shortcut badges — they don't anchor the active group
  for (const group of NAV_GROUPS) {
    if (
      group.items.some(
        (item) =>
          !item.alertBadge && (
            item.page === pageName ||
            (item.page === "notifications" && NOTIFICATIONS_PAGES.includes(pageName))
          )
      )
    ) {
      return group.key;
    }
  }
  return null;
}

function buildDefaultCollapse(pageName) {
  const activeKey = getActiveGroupKey(pageName);
  return NAV_GROUPS.reduce(
    (acc, g) => ({ ...acc, [g.key]: g.key !== activeKey }),
    {}
  );
}

export default function Layout({ children, currentPageName }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  // ST-11 (BLG-FE-93, EPIC-04, v8.5): lazy-initialise from localStorage
  // directly instead of defaulting to "dark" and correcting in a mount
  // effect. Persistence itself was already correct (localStorage survives
  // indefinitely; a storage-clearing event cleanly falls back to "dark"
  // via `|| "dark"`) -- the gap found by this story's audit was a
  // flash-of-wrong-theme on every load/reload when the persisted theme is
  // "light": the old default state briefly rendered dark before the mount
  // effect corrected it. Reading synchronously at initial-render time
  // removes the flash entirely.
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "dark");
  const location = useLocation();
  const navigate = useNavigate();

  // ST-06 (BLG-FE-145, EPIC-03, v8.5) follow-up, found live via that story's
  // own new Playwright tests failing in real CI: tailwind.config.js's
  // darkMode: ["class"] requires an ANCESTOR element carrying the literal
  // "dark" class for any dark: variant to apply -- but that class was only
  // ever applied to this component's own wrapper <div> below, never to
  // document.documentElement. Radix's DialogPortal (src/components/ui/dialog.js)
  // renders its content into document.body, OUTSIDE this wrapper's DOM
  // subtree -- so every dark: variant and every CSS custom property that
  // differs between :root and .dark (src/index.css) has always resolved to
  // its LIGHT value inside every Dialog-based component app-wide (14+
  // consumers: CommandPalette, ExportModal, WatchlistModal, WidgetLibrary,
  // PositionEntryModal, etc.), regardless of the user's actual theme
  // setting. Syncing the class onto documentElement (an ancestor of every
  // portal, since portals still mount under <body>/<html>) fixes this for
  // all of them at the root cause, not just this story's own call sites.
  // (No separate mount effect re-reads localStorage here -- ST-11's lazy
  // useState initialiser above already handles that synchronously.)
  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);
  };

  // ST-01 (EPIC-01, BLG-FE-115): mouse fallback for the global command palette
  const openCommandPalette = () => {
    window.dispatchEvent(new CustomEvent(OPEN_COMMAND_PALETTE_EVENT));
  };
  const isMac = typeof navigator !== "undefined" && /Mac/i.test(navigator.platform || "");

  const isActive = (pageName) =>
    pageName === "notifications"
      ? NOTIFICATIONS_PAGES.includes(currentPageName)
      : currentPageName === pageName;

  // Collapse state — persisted in sessionStorage, resets on full page reload
  const [groupCollapse, setGroupCollapse] = useState(() => {
    try {
      const stored = sessionStorage.getItem("nav-group-collapse");
      if (stored) {
        const parsed = JSON.parse(stored);
        // Always ensure active group is expanded
        const activeKey = getActiveGroupKey(currentPageName);
        if (activeKey) parsed[activeKey] = false;
        return parsed;
      }
    } catch {}
    return buildDefaultCollapse(currentPageName);
  });

  // Expand active group automatically on page change
  useEffect(() => {
    const activeKey = getActiveGroupKey(currentPageName);
    if (!activeKey) return;
    setGroupCollapse((prev) => {
      if (!prev[activeKey]) return prev;
      const next = { ...prev, [activeKey]: false };
      try { sessionStorage.setItem("nav-group-collapse", JSON.stringify(next)); } catch {}
      return next;
    });
  }, [currentPageName]);

  const toggleGroup = (key) => {
    if (key === getActiveGroupKey(currentPageName)) return; // active group cannot collapse
    setGroupCollapse((prev) => {
      const next = { ...prev, [key]: !prev[key] };
      try { sessionStorage.setItem("nav-group-collapse", JSON.stringify(next)); } catch {}
      return next;
    });
  };

  const isDark = theme === "dark";

  // ST-10 (BLG-FE-05): unacknowledged alert count — fetched once on mount, cleared on Alerts page visit
  const [alertCount, setAlertCount] = useState(0);

  useEffect(() => {
    const lastVisit = sessionStorage.getItem("alerts-last-visit");
    apiFetch(`${API_BASE_URL}/alerts/history`)
      .then((r) => (r.ok ? r.json() : null))
      .then((json) => {
        if (!json?.data?.evaluations) return;
        const evals = json.data.evaluations;
        const count = lastVisit
          ? evals.filter((e) => e.evaluation_timestamp > lastVisit).length
          : evals.length;
        setAlertCount(count);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (NOTIFICATIONS_PAGES.includes(currentPageName)) {
      sessionStorage.setItem("alerts-last-visit", new Date().toISOString());
      setAlertCount(0);
    }
  }, [currentPageName]);

  // ST-11: Global keyboard shortcuts
  const handleKeyDown = useCallback(
    (e) => {
      const tag = document.activeElement?.tagName?.toUpperCase();
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      if (e.key === "r") {
        e.preventDefault();
        window.dispatchEvent(new CustomEvent("app:refresh"));
      } else if (e.key === "n" && (currentPageName === "Positions" || currentPageName === "TradeHistory")) {
        e.preventDefault();
        navigate(createPageUrl("TradeEntry"));
      } else if (e.key === "w" && (currentPageName === "Screener" || currentPageName === "Watchlist")) {
        e.preventDefault();
        window.dispatchEvent(new CustomEvent("app:add-to-watchlist"));
      }
    },
    [currentPageName, navigate]
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  // ST-01 (EPIC-01, BLG-FE-115): first-session-only dismissible tooltip
  // pointing at the command palette affordance — per ux_spec.md §5.
  useEffect(() => {
    let seen;
    try {
      seen = localStorage.getItem("command-palette-tooltip-seen");
    } catch {
      seen = "true"; // no storage access — don't surface the hint
    }
    if (seen) return;
    const markSeen = () => {
      try { localStorage.setItem("command-palette-tooltip-seen", "true"); } catch {}
    };
    const timer = setTimeout(() => {
      toast.info("Press ⌘K (or Ctrl K) to search pages, tickers, and trade plans.", {
        duration: 8000,
        onDismiss: markSeen,
        onAutoClose: markSeen,
      });
    }, 1200);
    return () => clearTimeout(timer);
  }, []);

  const renderNavGroups = (onItemClick) => (
    <div className="space-y-1">
      {NAV_GROUPS.map((group) => {
        const isCollapsed = groupCollapse[group.key];
        const isActiveGroup = group.key === getActiveGroupKey(currentPageName);
        const showBadge = group.key === "system" && isCollapsed && alertCount > 0;

        return (
          <div key={group.key}>
            {/* Group header */}
            <button
              onClick={() => toggleGroup(group.key)}
              disabled={isActiveGroup}
              className={cn(
                "w-full flex items-center justify-between px-4 py-2 mt-2 rounded-lg transition-all",
                isActiveGroup
                  ? "cursor-default"
                  : isDark
                    ? "hover:bg-slate-800/40 cursor-pointer"
                    : "hover:bg-slate-100/80 cursor-pointer"
              )}
            >
              <div className="flex items-center gap-2">
                <span
                  className={cn(
                    "text-[10px] font-semibold tracking-[0.15em] uppercase",
                    "font-variant-numeric-tabular",
                    isDark ? "text-slate-400" : "text-slate-600"
                  )}
                  style={{ fontVariant: "small-caps" }}
                >
                  {group.label}
                </span>
                {showBadge && (
                  <span className="inline-flex items-center justify-center min-w-[16px] h-4 px-1 rounded-full bg-red-600 text-white text-[9px] font-bold leading-none">
                    {alertCount > 99 ? "99+" : alertCount}
                  </span>
                )}
              </div>
              <motion.div
                animate={{ rotate: isCollapsed ? 0 : 90 }}
                transition={{ duration: 0.18, ease: "easeInOut" }}
              >
                <ChevronRight
                  className={cn(
                    "w-3 h-3",
                    isDark ? "text-slate-600" : "text-slate-400"
                  )}
                />
              </motion.div>
            </button>

            {/* Group items */}
            <AnimatePresence initial={false}>
              {!isCollapsed && (
                <motion.div
                  key="items"
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2, ease: "easeInOut" }}
                  className="overflow-hidden"
                >
                  <div className="mt-0.5 space-y-0.5 pb-1">
                    {group.items.map((item) => {
                      const Icon = item.icon;
                      // alertBadge items are badge carriers — suppress active state to avoid dual-highlight
                      const active = !item.alertBadge && isActive(item.page);
                      const showItemBadge = item.alertBadge && alertCount > 0;
                      return (
                        <Link
                          key={item.name}
                          to={createPageUrl(item.page)}
                          onClick={onItemClick}
                          className={cn(
                            "flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all ml-3 border-l-2",
                            active
                              ? isDark
                                ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400 border-l-cyan-500/60 shadow-sm shadow-cyan-500/10"
                                : "bg-gradient-to-r from-cyan-500/10 to-violet-500/10 text-cyan-600 border-l-cyan-500/40"
                              : isDark
                                ? "text-slate-400 hover:text-white hover:bg-slate-800/50 border-l-slate-700/40"
                                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-slate-200"
                          )}
                        >
                          <span className="relative shrink-0">
                            <Icon className="w-4 h-4" />
                            {showItemBadge && (
                              <span className="absolute -top-1.5 -right-1.5 min-w-[14px] h-3.5 px-0.5 rounded-full bg-red-600 text-white text-[8px] font-bold leading-[14px] text-center">
                                {alertCount > 99 ? "99+" : alertCount}
                              </span>
                            )}
                          </span>
                          {item.name}
                        </Link>
                      );
                    })}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}
    </div>
  );

  return (
    <div
      className={cn(
        "min-h-screen transition-colors duration-300",
        isDark ? "dark bg-slate-950 text-white" : "bg-slate-100 text-slate-900"
      )}
    >
      {/* Gradient background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div
          className={cn(
            "absolute -top-40 -right-40 w-96 h-96 rounded-full blur-3xl",
            isDark ? "bg-cyan-500/10" : "bg-cyan-500/20"
          )}
        />
        <div
          className={cn(
            "absolute top-1/2 -left-40 w-96 h-96 rounded-full blur-3xl",
            isDark ? "bg-violet-500/10" : "bg-violet-500/15"
          )}
        />
        <div
          className={cn(
            "absolute -bottom-40 right-1/3 w-96 h-96 rounded-full blur-3xl",
            isDark ? "bg-fuchsia-500/10" : "bg-fuchsia-500/15"
          )}
        />
      </div>

      {/* Mobile Header */}
      <header
        className={cn(
          "lg:hidden fixed top-0 left-0 right-0 z-50 border-b backdrop-blur-xl print-hide",
          isDark
            ? "border-slate-800/50 bg-slate-950/80"
            : "border-slate-200 bg-white/80"
        )}
      >
        <div className="flex items-center justify-between px-4 h-16">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 via-violet-500 to-fuchsia-500 flex items-center justify-center shadow-lg shadow-violet-500/25">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">
              Position Manager
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={openCommandPalette}
              aria-label="Open command palette"
              data-testid="command-palette-trigger-mobile"
              className={cn(
                "h-9 w-9",
                isDark
                  ? "text-slate-400 hover:text-white hover:bg-slate-800"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-200"
              )}
            >
              <Search className="w-5 h-5" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              data-testid="theme-toggle-mobile"
              aria-label="Toggle theme"
              onClick={toggleTheme}
              className={cn(
                "h-9 w-9",
                isDark
                  ? "text-slate-400 hover:text-white hover:bg-slate-800"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-200"
              )}
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(true)}
              className={cn(
                "h-9 w-9",
                isDark
                  ? "text-slate-400 hover:text-white hover:bg-slate-800"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-200"
              )}
            >
              <Menu className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile Sidebar Overlay */}
      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
            />
            <motion.aside
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 300 }}
              className={cn(
                "lg:hidden fixed top-0 right-0 bottom-0 z-50 w-72 border-l print-hide",
                isDark
                  ? "bg-slate-900 border-slate-800"
                  : "bg-white border-slate-200"
              )}
            >
              <div
                className={cn(
                  "flex items-center justify-between p-4 border-b",
                  isDark ? "border-slate-800" : "border-slate-200"
                )}
              >
                <span
                  className={cn(
                    "font-semibold",
                    isDark ? "text-white" : "text-slate-900"
                  )}
                >
                  Menu
                </span>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setSidebarOpen(false)}
                  className={
                    isDark
                      ? "text-slate-400 hover:text-white"
                      : "text-slate-600 hover:text-slate-900"
                  }
                >
                  <X className="w-5 h-5" />
                </Button>
              </div>

              {/* Mobile: Dashboard shortcut + groups */}
              <nav className="p-4 space-y-1 overflow-y-auto h-[calc(100%-65px)]">
                <Link
                  to={createPageUrl("DashboardHome")}
                  onClick={() => setSidebarOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all mb-3",
                    isActive("DashboardHome")
                      ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-600 border border-cyan-500/30"
                      : isDark
                        ? "text-slate-400 hover:text-white hover:bg-slate-800/50"
                        : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                  )}
                >
                  <LayoutDashboard className="w-4 h-4 shrink-0" />
                  Dashboard
                </Link>
                {renderNavGroups(() => setSidebarOpen(false))}
              </nav>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Desktop Sidebar */}
      <aside
        className={cn(
          "hidden lg:flex flex-col fixed top-0 left-0 bottom-0 w-64 backdrop-blur-xl border-r z-40 print-hide",
          isDark
            ? "bg-slate-900/50 border-slate-800/50"
            : "bg-white/70 border-slate-200"
        )}
      >
        {/* Logo */}
        <div
          className={cn(
            "flex items-center gap-3 px-6 h-16 border-b shrink-0",
            isDark ? "border-slate-800/50" : "border-slate-200"
          )}
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 via-violet-500 to-fuchsia-500 flex items-center justify-center shadow-lg shadow-violet-500/25">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-lg bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">
            Position Manager
          </span>
        </div>

        {/* ST-01 (EPIC-01, BLG-FE-115): command palette search affordance */}
        <div className="px-4 pt-4">
          <button
            type="button"
            onClick={openCommandPalette}
            aria-label="Open command palette"
            data-testid="command-palette-trigger-desktop"
            className={cn(
              "w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-all border",
              isDark
                ? "bg-slate-800/40 border-slate-800/60 text-slate-400 hover:text-white hover:bg-slate-800/70"
                : "bg-slate-100/80 border-slate-200 text-slate-500 hover:text-slate-900 hover:bg-slate-200/70"
            )}
          >
            <Search className="w-4 h-4 shrink-0" />
            <span className="flex-1 text-left">Search…</span>
            <kbd
              className={cn(
                "inline-flex items-center justify-center px-1.5 h-5 rounded text-[10px] font-mono font-semibold border shrink-0",
                isDark
                  ? "bg-slate-900/60 border-slate-700 text-slate-500"
                  : "bg-white border-slate-300 text-slate-500"
              )}
            >
              {isMac ? "⌘K" : "Ctrl K"}
            </kbd>
          </button>
        </div>

        {/* Navigation — scrollable */}
        <nav className="flex-1 overflow-y-auto px-4 py-4 space-y-1">
          {/* Dashboard — ungrouped home link */}
          <Link
            to={createPageUrl("DashboardHome")}
            className={cn(
              "flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all mb-3",
              isActive("DashboardHome")
                ? isDark
                  ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400 border border-cyan-500/30 shadow-lg shadow-cyan-500/10"
                  : "bg-gradient-to-r from-cyan-500/10 to-violet-500/10 text-cyan-600 border border-cyan-500/20"
                : isDark
                  ? "text-slate-400 hover:text-white hover:bg-slate-800/50"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            )}
          >
            <LayoutDashboard className="w-4 h-4 shrink-0" />
            Dashboard
          </Link>

          {/* Collapsible groups */}
          {renderNavGroups(null)}
        </nav>

        {/* Footer */}
        <div
          className={cn(
            "p-4 border-t shrink-0",
            isDark ? "border-slate-800/50" : "border-slate-200"
          )}
        >
          <div className="flex items-center justify-between mb-4">
            <span
              className={cn(
                "text-xs",
                isDark ? "text-slate-400" : "text-slate-600"
              )}
            >
              Theme
            </span>
            <Button
              variant="ghost"
              size="sm"
              data-testid="theme-toggle-desktop"
              aria-label="Toggle theme"
              onClick={toggleTheme}
              className={cn(
                "h-8 gap-2",
                isDark
                  ? "text-slate-400 hover:text-white hover:bg-slate-800"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-200"
              )}
            >
              {isDark ? (
                <>
                  <Sun className="w-4 h-4" />
                  Light
                </>
              ) : (
                <>
                  <Moon className="w-4 h-4" />
                  Dark
                </>
              )}
            </Button>
          </div>
          {/* Keyboard shortcut hints */}
          {(() => {
            const shortcuts = PAGE_SHORTCUTS[currentPageName] || DEFAULT_SHORTCUTS;
            return (
              <div className="mb-3 space-y-1">
                {shortcuts.map(({ key, label }) => (
                  <div key={key} className="flex items-center justify-between">
                    <span className={cn("text-xs", isDark ? "text-slate-400" : "text-slate-600")}>
                      {label}
                    </span>
                    <kbd
                      className={cn(
                        "inline-flex items-center justify-center w-5 h-5 rounded text-[10px] font-mono font-semibold border",
                        isDark
                          ? "bg-slate-800 border-slate-700 text-slate-400"
                          : "bg-slate-100 border-slate-300 text-slate-600"
                      )}
                    >
                      {key}
                    </kbd>
                  </div>
                ))}
              </div>
            );
          })()}
          <div
            className={cn(
              "flex items-center justify-between text-xs",
              isDark ? "text-slate-400" : "text-slate-600"
            )}
          >
            <span>v1.0.0</span>
            <a
              href="#"
              className="flex items-center gap-1 hover:text-slate-400 transition-colors"
            >
              Docs
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main
        className={cn(
          "lg:ml-64 min-h-screen pt-16 lg:pt-0 relative",
          isDark ? "bg-slate-950" : "bg-slate-100"
        )}
      >
        <div className="p-4 lg:p-8 max-w-7xl mx-auto">{children}</div>
      </main>

      {/* ST-01 (EPIC-01, BLG-FE-115): global command palette — mounted once, present on every page */}
      <CommandPalette />
    </div>
  );
}
