import { format } from "date-fns";

export const FX_SOURCE_LIVE = "live";
export const FX_SOURCE_LAST_KNOWN = "last_known";
export const FX_SOURCE_CONSTANT = "constant";

const RATE_DECIMALS = 4;
const MS_PER_MINUTE = 60000;
const MINUTES_PER_HOUR = 60;
const HOURS_PER_DAY = 24;
const HOURS_SHOWN_BEFORE_DAYS = 48;

export function formatFxRate(rate) {
  return Number(rate).toFixed(RATE_DECIMALS);
}

export function formatFxAge(asOf, now = new Date()) {
  const minutes = Math.max(0, Math.floor((now.getTime() - new Date(asOf).getTime()) / MS_PER_MINUTE));
  if (minutes < MINUTES_PER_HOUR) return `${minutes} min ago`;
  const hours = Math.floor(minutes / MINUTES_PER_HOUR);
  if (hours < HOURS_SHOWN_BEFORE_DAYS) return `${hours} h ago`;
  return `${Math.floor(hours / HOURS_PER_DAY)} days ago`;
}

export function fxSourceNotice(source, rate, asOf) {
  if (rate == null) return null;
  const shown = formatFxRate(rate);
  if (source === FX_SOURCE_LAST_KNOWN && asOf) {
    const age = formatFxAge(asOf);
    return {
      text: `⚠ FX rate not live: GBP/USD ${shown} from ${age}`,
      shortText: `Not live: from ${age}`,
      description: `The live GBP/USD rate is unavailable. US values, P&L and heat use the last fetched rate, ${shown} at ${format(new Date(asOf), "dd MMM yyyy, HH:mm")}. Reload the page to try again.`,
    };
  }
  if (source === FX_SOURCE_CONSTANT) {
    return {
      text: `⚠ FX rate unavailable: using fixed GBP/USD ${shown}`,
      shortText: "Fixed fallback",
      description: `No GBP/USD rate could be fetched, so a fixed fallback of ${shown} is used. US values, P&L and heat are approximate. Reload the page to try again.`,
    };
  }
  return null;
}
