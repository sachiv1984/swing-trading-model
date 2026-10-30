import { Clock } from "lucide-react";
import ExplainedMarker from "./ExplainedMarker";

const LEAD = "Live price unavailable, so the last stored price is shown.";
const TAIL = "use this price until a live price is fetched. Reload the page to try again.";

export const STALE_EXPLANATION_RISK = `${LEAD} Value, P&L and heat ${TAIL}`;
export const STALE_EXPLANATION_POSITIONS = `${LEAD} Value and P&L ${TAIL}`;

export default function StaleMarker({ explanation }) {
  return (
    <ExplainedMarker
      label="Price stale"
      description={explanation}
      testId="price-stale-marker"
      className="ml-1.5 align-middle text-amber-700 dark:text-amber-400 ring-amber-500"
    >
      <Clock className="w-3.5 h-3.5" aria-hidden="true" />
      <span className="text-xs">stale</span>
    </ExplainedMarker>
  );
}
