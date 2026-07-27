import { useQueryClient } from "@tanstack/react-query";
import OpenPositionsCard from "../components/dashboard/home/OpenPositionsCard";
import PortfolioHeatCard from "../components/dashboard/home/PortfolioHeatCard";
import GracePeriodCard from "../components/dashboard/home/GracePeriodCard";
import SignalStatusCard from "../components/dashboard/home/SignalStatusCard";
import RecentActivityCard from "../components/dashboard/home/RecentActivityCard";
import MorningBriefing from "../components/dashboard/home/MorningBriefing";
import GateProgressStrip from "../components/dashboard/home/GateProgressStrip";
import AiDailyBriefing from "../components/dashboard/home/AiDailyBriefing";
import WhatsNewCard from "../components/dashboard/home/WhatsNewCard";

const DASHBOARD_QUERY_KEYS = [
  "home-open-positions",
  "home-portfolio-heat",
  "home-grace-period",
  "home-market-status",
  "home-signals-today",
  "home-recent-activity",
  "morning-screener-hits",
  "morning-grace-alerts",
  "morning-positions",
  "morning-red-flags",
  "morning-compliance-7d",
  "morning-compliance-30d",
  "home-whats-new",
];

export default function DashboardHome() {
  const queryClient = useQueryClient();

  const handleRetry = () => {
    DASHBOARD_QUERY_KEYS.forEach(key => queryClient.invalidateQueries({ queryKey: [key] }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">Dashboard</h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">Session summary — live data</p>
      </div>

      {/* ST-03 (EPIC-01, v7.3): briefing section — visually distinguished from the
          status-card grid below via an accent border/tint, and placed first so
          it is visible on page load without scrolling past other cards. */}
      <div className="rounded-2xl border border-indigo-500/30 bg-indigo-500/5 dark:bg-indigo-500/10 p-4 md:p-6 space-y-4">
        <MorningBriefing />
        <AiDailyBriefing />
      </div>

      {/* Top row: Open Positions, Portfolio Heat, In Grace Today */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <OpenPositionsCard />
        <PortfolioHeatCard />
        <GracePeriodCard />
      </div>

      {/* Bottom row: Signal Status, Recent Activity */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <SignalStatusCard />
        <RecentActivityCard />
      </div>

      {/* Trade gate proximity strip — hidden silently on error */}
      <GateProgressStrip />

      {/* ST-01 (EPIC-01, v7.8, BLG-FE-128): in-app "What's New" panel — dashboard.md §6A */}
      <WhatsNewCard />

      {/* All-endpoints-failed retry (spec §5) — hidden by default, shown via retry button */}
      <div className="hidden" id="dashboard-retry-root">
        <button
          onClick={handleRetry}
          className="mt-4 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-sm"
        >
          Retry
        </button>
      </div>
    </div>
  );
}
