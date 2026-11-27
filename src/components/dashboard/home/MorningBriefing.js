import ScreenerHitsCard from "./morning/ScreenerHitsCard";
import ExitZoneCard from "./morning/ExitZoneCard";
import RedFlagsCard from "./morning/RedFlagsCard";
import EarningsAlertCard from "./morning/EarningsAlertCard";
import ComplianceCard from "./morning/ComplianceCard";
import { useQuietDay } from "./QuietDay";
import { MORNING_BRIEFING_KEYS, mdGridCols, shownCount } from "../../../lib/quietDay";

export default function MorningBriefing() {
  // dashboard.md v4.4 §3A (ST-09): folded cards leave no gap; with all five
  // folded the section is hidden (kept mounted, so the cards keep loading).
  const quietDay = useQuietDay();
  const shown = quietDay ? shownCount(MORNING_BRIEFING_KEYS, quietDay.folded, quietDay.revealed) : MORNING_BRIEFING_KEYS.length;
  return (
    <section data-testid="morning-briefing" hidden={shown === 0}>
      <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-3">Morning Briefing</p>
      <div className={`grid grid-cols-1 ${mdGridCols(shown)} gap-4`}>
        <ScreenerHitsCard />
        <ExitZoneCard />
        <RedFlagsCard />
        <EarningsAlertCard />
        <ComplianceCard />
      </div>
    </section>
  );
}
