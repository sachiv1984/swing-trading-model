import { format } from "date-fns";
import { MINUS, MISSING } from "../../lib/format";

// ST-26 (BLG-SEC-41, EPIC-04, v9.12): the Settings save bar's last-change line
// (settings.md v1.9 §Last Change Line). Reads GET /settings `last_change`; nothing
// is computed client-side.
export const SETTINGS_FIELD_LABELS = {
  default_risk_percent: "Default Risk % Per Trade",
  uk_commission: "UK Commission (£)",
  us_commission: "US Commission ($)",
  stamp_duty_rate: "UK Stamp Duty Rate",
  fx_fee_rate: "US FX Fee Rate",
  default_currency: "Default Currency",
  theme: "Theme",
  concentration_position_threshold_pct: "Position Concentration Limit (%)",
  concentration_sector_threshold_pct: "Sector Concentration Limit (%)",
  min_trades_for_analytics: "Minimum Trades for Analytics",
  min_hold_days: "Minimum Hold Days",
  atr_period: "ATR Period",
  atr_multiplier_initial: "Initial Stop (ATR Multiple)",
  atr_multiplier_trailing: "Trailing Stop (ATR Multiple)",
};

const SOURCE_LABELS = { settings_page: "Settings page" };

function formatValue(value) {
  if (value === null || value === undefined || value === "") return MISSING;
  if (/^-?\d+(\.\d+)?$/.test(value)) {
    return Number(value).toLocaleString("en-GB", { maximumFractionDigits: 6 }).replace("-", MINUS);
  }
  return value;
}

function describe(change) {
  const label = SETTINGS_FIELD_LABELS[change.field] || change.field;
  return `${label} ${formatValue(change.old_value)} → ${formatValue(change.new_value)}`;
}

export function lastChangeText(lastChange) {
  if (!lastChange) return { text: "No changes recorded yet.", title: undefined };
  const changes = lastChange.changes?.length ? lastChange.changes : [lastChange];
  const more = changes.length > 1 ? ` and ${changes.length - 1} more` : "";
  const when = format(new Date(lastChange.changed_at), "d MMM yyyy, HH:mm");
  const source = SOURCE_LABELS[lastChange.request_source] || "API";
  return {
    text: `Last change: ${describe(changes[0])}${more} · ${when} · ${source}`,
    title: changes.length > 1 ? changes.map(describe).join("\n") : undefined,
  };
}

export default function SettingsLastChange({ lastChange }) {
  const { text, title } = lastChangeText(lastChange);
  return (
    <p
      data-testid="settings-last-change"
      title={title}
      className="w-full sm:w-auto text-xs text-slate-600 dark:text-slate-400"
    >
      {text}
    </p>
  );
}
