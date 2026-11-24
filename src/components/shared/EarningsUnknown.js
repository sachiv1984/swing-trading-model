import React, { useId } from "react";
import PropTypes from "prop-types";
import { EARNINGS_UNKNOWN_TOOLTIP } from "../../lib/earningsDataStatus";

// ST-33 (BLG-FE-294, v9.18): a failed earnings lookup. Muted missing-data text,
// never the GAP RISK badge's colour or wording (positions.md §Earnings Unknown,
// screener_results.md v1.12, watchlist.md §Earnings Cell).
export default function EarningsUnknown({ label = "Unknown", testId = "earnings-unknown" }) {
  const descId = useId();
  return (
    <>
      <span className="text-xs text-app-muted" title={EARNINGS_UNKNOWN_TOOLTIP} aria-describedby={descId} data-testid={testId}>
        {label}
      </span>
      {/* Outside the labelled span and hidden, so a screen reader reads the
          description once (aria-describedby still resolves hidden elements). */}
      <span id={descId} hidden>{EARNINGS_UNKNOWN_TOOLTIP}</span>
    </>
  );
}

EarningsUnknown.propTypes = { label: PropTypes.string, testId: PropTypes.string };
