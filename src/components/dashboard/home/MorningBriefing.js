import ScreenerHitsCard from "./morning/ScreenerHitsCard";
import ExitZoneCard from "./morning/ExitZoneCard";
import RedFlagsCard from "./morning/RedFlagsCard";
import EarningsAlertCard from "./morning/EarningsAlertCard";
import ComplianceCard from "./morning/ComplianceCard";
import ExitConditionsCard from "./morning/ExitConditionsCard";

export default function MorningBriefing() {
  return (
    <section data-testid="morning-briefing">
      <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-3">Morning Briefing</p>
      <ExitConditionsCard />
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <ScreenerHitsCard />
        <ExitZoneCard />
        <RedFlagsCard />
        <EarningsAlertCard />
        <ComplianceCard />
      </div>
    </section>
  );
}
