import { useState, useEffect, useMemo, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
} from "./ui/command";
import { createPageUrl } from "../utils";
import { apiFetch, API_BASE_URL, api } from "../api/base44Client";
import { PAGES } from "../pages.config";
import { Briefcase, Eye, FileText } from "lucide-react";

// ST-01 (EPIC-01, BLG-FE-115): human-readable labels for page keys —
// page keys like "TradeHistory" are not directly presentable per
// docs/specs/blg_fe_115_pre_implementation_readiness_pass.md AC-01.
const PAGE_LABELS = {
  DashboardHome: "Dashboard",
  Dashboard: "Dashboard",
  Positions: "Positions",
  Reports: "Reports",
  Settings: "Settings",
  Signals: "Signals",
  TradeEntry: "Trade Entry",
  TradeHistory: "Trade History",
  SystemStatus: "System Status",
  PerformanceAnalytics: "Analytics",
  RiskDashboard: "Risk Dashboard",
  TradeReflection: "Trade Reflection",
  Watchlist: "Watchlist",
  WeeklyDigest: "Weekly Digest",
  Screener: "Screener",
  TradePlan: "Trade Plan",
  TradePlans: "Trade Plans",
  TickerUniverse: "Ticker Universe",
  RedFlagJournal: "Red Flag Journal",
  StrategyBenchmark: "Strategy Benchmark",
};

// Recent/frequent pages shown when the input is empty (top-level nav items) —
// per ux_spec.md §2.3 "Empty input state".
const FREQUENT_PAGE_KEYS = [
  "DashboardHome",
  "Positions",
  "Watchlist",
  "TradePlans",
  "Screener",
  "Settings",
];

const DYNAMIC_QUERY_STALE_TIME_MS = 60000;

export const OPEN_COMMAND_PALETTE_EVENT = "app:open-command-palette";

export default function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  // Cmd/Ctrl-K global invocation — suppressed while focus is inside a text
  // input/textarea/select, matching Layout.js's existing shortcut convention.
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key?.toLowerCase() !== "k" || !(e.metaKey || e.ctrlKey)) return;
      const tag = document.activeElement?.tagName?.toUpperCase();
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      e.preventDefault();
      setOpen((prev) => !prev);
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Mouse fallback — nav-bar search affordance dispatches this event.
  useEffect(() => {
    const handleOpenEvent = () => setOpen(true);
    window.addEventListener(OPEN_COMMAND_PALETTE_EVENT, handleOpenEvent);
    return () => window.removeEventListener(OPEN_COMMAND_PALETTE_EVENT, handleOpenEvent);
  }, []);

  useEffect(() => {
    if (!open) setQuery("");
  }, [open]);

  // Dynamic "Your Data" index — tickers/positions/trade plans already loaded
  // client-side elsewhere in the app; fetched lazily only while the palette
  // is open (no background fetch), per ux_spec.md §2.3.
  const { data: positions = [] } = useQuery({
    queryKey: ["command-palette-positions"],
    queryFn: () => api.positions.list(),
    enabled: open,
    staleTime: DYNAMIC_QUERY_STALE_TIME_MS,
  });

  const { data: watchlistEntries = [] } = useQuery({
    queryKey: ["command-palette-watchlist"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE_URL}/watchlist`);
      const json = await res.json();
      return json?.data || [];
    },
    enabled: open,
    staleTime: DYNAMIC_QUERY_STALE_TIME_MS,
  });

  const { data: tradePlans = [] } = useQuery({
    queryKey: ["command-palette-trade-plans"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE_URL}/trade-plans`);
      const json = await res.json();
      return json?.data || [];
    },
    enabled: open,
    staleTime: DYNAMIC_QUERY_STALE_TIME_MS,
  });

  const pageEntries = useMemo(
    () => Object.keys(PAGES).map((key) => ({ key, label: PAGE_LABELS[key] || key })),
    []
  );

  const frequentPageEntries = useMemo(
    () =>
      FREQUENT_PAGE_KEYS.filter((key) => PAGES[key]).map((key) => ({
        key,
        label: PAGE_LABELS[key] || key,
      })),
    []
  );

  const handleSelectPage = useCallback(
    (pageKey) => {
      setOpen(false);
      navigate(createPageUrl(pageKey));
    },
    [navigate]
  );

  const handleSelectPosition = useCallback(() => {
    setOpen(false);
    navigate(createPageUrl("Positions"));
  }, [navigate]);

  const handleSelectWatchlistTicker = useCallback(() => {
    setOpen(false);
    navigate(createPageUrl("Watchlist"));
  }, [navigate]);

  // Navigates directly to the trade plan's detail view — the app's actual
  // TradePlan detail route is query-param based (`/TradePlan?edit={id}...`),
  // not the path-param `/trade-plans/{id}` the ux_spec assumed. Same intent
  // (jump straight to that plan's detail, ID already known) — implementation
  // note per LL-v3.4-P3-03, not a deviation.
  const handleSelectTradePlan = useCallback(
    (plan) => {
      setOpen(false);
      navigate(
        `/TradePlan?edit=${plan.id}&ticker=${plan.ticker}&market=${plan.market || "US"}`
      );
    },
    [navigate]
  );

  const emptyMessage = query ? `No results for '${query}'.` : "No results found.";

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput
        placeholder="Search pages, tickers, trade plans…"
        value={query}
        onValueChange={setQuery}
        data-testid="command-palette-input"
      />
      <CommandList>
        <CommandEmpty data-testid="command-palette-empty">{emptyMessage}</CommandEmpty>

        {!query && (
          <CommandGroup heading="Pages">
            {frequentPageEntries.map(({ key, label }) => (
              <CommandItem
                key={key}
                value={label}
                onSelect={() => handleSelectPage(key)}
                data-testid={`command-palette-page-${key}`}
              >
                {label}
              </CommandItem>
            ))}
          </CommandGroup>
        )}

        {query && (
          <>
            <CommandGroup heading="Pages">
              {pageEntries.map(({ key, label }) => (
                <CommandItem
                  key={key}
                  value={label}
                  onSelect={() => handleSelectPage(key)}
                  data-testid={`command-palette-page-${key}`}
                >
                  {label}
                </CommandItem>
              ))}
            </CommandGroup>

            <CommandGroup heading="Your Data">
              {positions.map((p) => (
                <CommandItem
                  key={`position-${p.ticker}`}
                  value={`${p.ticker} position`}
                  onSelect={handleSelectPosition}
                  data-testid={`command-palette-position-${p.ticker}`}
                >
                  <Briefcase className="mr-2 h-4 w-4 shrink-0 opacity-60" />
                  {p.ticker} — open position
                </CommandItem>
              ))}
              {watchlistEntries.map((w) => (
                <CommandItem
                  key={`watchlist-${w.ticker}`}
                  value={`${w.ticker} watchlist`}
                  onSelect={handleSelectWatchlistTicker}
                  data-testid={`command-palette-watchlist-${w.ticker}`}
                >
                  <Eye className="mr-2 h-4 w-4 shrink-0 opacity-60" />
                  {w.ticker} — watchlist
                </CommandItem>
              ))}
              {tradePlans.map((plan) => (
                <CommandItem
                  key={`plan-${plan.id}`}
                  value={`${plan.ticker} trade plan`}
                  onSelect={() => handleSelectTradePlan(plan)}
                  data-testid={`command-palette-plan-${plan.id}`}
                >
                  <FileText className="mr-2 h-4 w-4 shrink-0 opacity-60" />
                  {plan.ticker} — trade plan
                </CommandItem>
              ))}
            </CommandGroup>
          </>
        )}
      </CommandList>
    </CommandDialog>
  );
}
