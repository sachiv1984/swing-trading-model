import OpenPositionsCard from "@/components/dashboard/home/OpenPositionsCard";
import PortfolioHeatCard from "@/components/dashboard/home/PortfolioHeatCard";
import GracePeriodCard from "@/components/dashboard/home/GracePeriodCard";
import SignalStatusCard from "@/components/dashboard/home/SignalStatusCard";
import RecentActivityCard from "@/components/dashboard/home/RecentActivityCard";

export default function DashboardHome() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Dashboard</h1>
        <p className="text-sm text-slate-400 mt-1">Session summary — live data</p>
      </div>

      {/* Top row: 3 cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <OpenPositionsCard />
        <PortfolioHeatCard />
        <GracePeriodCard />
      </div>

      {/* Bottom row: 2 cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <SignalStatusCard />
        <RecentActivityCard />
      </div>
    </div>
  );
}
