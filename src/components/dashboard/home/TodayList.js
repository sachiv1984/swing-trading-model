import { useId } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { format } from "date-fns";
import { api } from "../../../api/base44Client";
import { Skeleton } from "../../ui/skeleton";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "../../ui/tooltip";
import { REGIME_RISK_ON, REGIME_UNKNOWN, regimeStatusOf, unknownRegimeExplanation } from "../../../lib/regime";
import { getExitCondition } from "../../../lib/exitCondition";
import { formatCurrency, currencyForMarket } from "../../../lib/format";

// ST-06 (BLG-FE-254, EPIC-02, v9.16): dashboard.md v4.0 §1B Today list ("Due today").
// Display-only: every item is a link to the page where the user acts; nothing
// here executes, confirms or pre-fills an action (§1B Strategy constraints, §13).
// ST-10 (BLG-FE-254, EPIC-04, v9.17): the Stops moved group (TL-09/TL-10) reads
// GET /positions' stop_last_moved_date/previous_stop (ST-09, BLG-BE-205).

export const TODAY_QUERY_KEYS = ["today-market-status", "today-positions", "today-signals"];

const MAX_ITEMS = 5;
const MARKETS = [
  { key: "US", index: "SPY", label: "US (SPY)", field: "spy" },
  { key: "UK", index: "FTSE", label: "UK (FTSE)", field: "ftse" },
];
const GROUP_NAMES = {
  regime: "Market regime",
  exits: "Exits due",
  grace: "Grace ends today",
  stops: "Stops moved",
  signals: "New signals",
};

const BADGE = "text-xs font-semibold px-2 py-0.5 rounded-full";
const TEXT = "text-slate-900 dark:text-white";
const MUTED = "text-slate-600 dark:text-slate-400";
const LINK = "text-cyan-700 hover:text-cyan-800 dark:text-cyan-400 dark:hover:text-cyan-300 underline underline-offset-2";

function RegimeBadge({ market, status, descriptionId }) {
  if (status === REGIME_UNKNOWN) {
    const explanation = unknownRegimeExplanation(market.key);
    return (
      <TooltipProvider delayDuration={200}>
        <Tooltip>
          <TooltipTrigger asChild>
            <span
              data-testid={`regime-unknown-${market.index}`}
              aria-describedby={descriptionId}
              className={`${BADGE} bg-slate-200 text-slate-800 dark:bg-slate-500/20 dark:text-slate-300`}
            >
              UNKNOWN ?
            </span>
          </TooltipTrigger>
          <TooltipContent className="max-w-xs text-left">{explanation}</TooltipContent>
        </Tooltip>
      </TooltipProvider>
    );
  }
  const isOn = status === REGIME_RISK_ON;
  return (
    <span
      data-testid={`regime-badge-${market.index}`}
      className={`${BADGE} ${isOn
        ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/20 dark:text-emerald-400"
        : "bg-rose-100 text-rose-800 dark:bg-rose-500/20 dark:text-rose-400"}`}
    >
      {isOn ? "RISK-ON ✓" : "RISK-OFF ✗"}
    </span>
  );
}

function GroupHeader({ name, count }) {
  return (
    <p className={`text-xs font-medium uppercase tracking-wider ${MUTED}`} data-testid="today-header">
      {count == null ? name : `${name} · ${count}`}
    </p>
  );
}

function SkeletonGroup({ group }) {
  return (
    <div data-testid={`today-group-${group}`} aria-busy="true">
      <Skeleton data-testid={`today-skeleton-${group}`} className="h-4 w-full max-w-md bg-slate-300/60 dark:bg-slate-700/60" />
    </div>
  );
}

function ErrorGroup({ group, onRetry }) {
  return (
    <div data-testid={`today-group-${group}`} className="space-y-1">
      <GroupHeader name={GROUP_NAMES[group]} />
      <p data-testid={`today-error-${group}`} className={`text-sm ${MUTED}`}>
        Couldn't load {GROUP_NAMES[group]}.{" "}
        <button type="button" onClick={onRetry} className={`text-sm ${LINK}`}>
          Retry
        </button>
      </p>
    </div>
  );
}

function Overflow({ group, count, to }) {
  if (count <= 0) return null;
  return (
    <Link to={to} data-testid={`today-overflow-${group}`} className={`inline-block text-xs ${LINK}`}>
      +{count} more
    </Link>
  );
}

// Grace ends today and Stops moved rows: ticker and a muted line, linking to the position.
function PositionLinkGroup({ group, items, text }) {
  const { shown, overflow } = capped(items);
  return (
    <div data-testid={`today-group-${group}`} className="space-y-1">
      <GroupHeader name={GROUP_NAMES[group]} count={items.length} />
      <ul className="space-y-1">
        {shown.map((p) => (
          <li key={p.id}>
            <Link
              to={`/Positions?position=${encodeURIComponent(p.id)}`}
              data-testid={`today-item-${group}-${p.ticker}`}
              className="flex items-center gap-3 text-sm rounded hover:bg-slate-100 dark:hover:bg-slate-700/40"
            >
              <span className={`font-semibold ${TEXT}`}>{p.ticker}</span>
              <span className={MUTED}>{text(p)}</span>
            </Link>
          </li>
        ))}
      </ul>
      <Overflow group={group} count={overflow} to="/Positions" />
    </div>
  );
}

const stopMovedText = (p) => {
  const currency = currencyForMarket(p.market);
  return `Stop moved from ${formatCurrency(p.previous_stop, { currency })} to ${formatCurrency(p.current_trailing_stop_native, { currency })}`;
};

function capped(items) {
  return { shown: items.slice(0, MAX_ITEMS), overflow: Math.max(0, items.length - MAX_ITEMS) };
}

const byTicker = (a, b) => String(a.ticker || "").localeCompare(String(b.ticker || ""));

export function selectExitsDue(positions) {
  const rows = positions
    .map((p) => ({ position: p, condition: getExitCondition(p) }))
    .filter(({ condition }) => condition.reason);
  return [
    ...rows.filter((r) => r.condition.riskOff).sort((a, b) => byTicker(a.position, b.position)),
    ...rows.filter((r) => !r.condition.riskOff).sort((a, b) => byTicker(a.position, b.position)),
  ];
}

export function selectGraceEndsToday(positions) {
  return positions.filter((p) => Number(p.grace_days_remaining) === 1 && p.grace_days_remaining != null).sort(byTicker);
}

// Stops moved (dashboard.md §1B, TL-09; DEV-EPIC04-ST10-01). GET /positions has no run
// date, so "the latest nightly run" is read as a window: moves whose stop_last_moved_date
// (UTC) is today or the previous weekday (ruling 2026-11-13, Frontend Specifications & UX
// Documentation Owner / Head of UX & Design). The nightly job runs 22:30 UTC Mon–Fri and
// the snapshot recompute 16:00 UTC, so the window always covers the last run. A row needs
// both fields and a current stop above the previous one. A–Z by ticker.
export function stopsMovedWindow(now = new Date()) {
  const iso = (d) => d.toISOString().slice(0, 10);
  const prev = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  do {
    prev.setUTCDate(prev.getUTCDate() - 1);
  } while (prev.getUTCDay() === 0 || prev.getUTCDay() === 6);
  return [iso(now), iso(prev)];
}

export function selectStopsMoved(positions, window) {
  return positions
    .filter((p) => p.stop_last_moved_date && window.includes(String(p.stop_last_moved_date).slice(0, 10)))
    .filter((p) => p.previous_stop != null && Number(p.current_trailing_stop_native) > Number(p.previous_stop))
    .sort(byTicker);
}

// Same filter as the v3.11 Card 4 (SignalStatusCard.js, removed in v9.16): local signal_date, or
// created_date starting with it; every status counts. API order is kept.
export function selectTodaySignals(signals, today) {
  return signals.filter((s) => s.signal_date === today || s.created_date?.startsWith(today));
}

export default function TodayList() {
  const usDescriptionId = useId();
  const ukDescriptionId = useId();
  const descriptionIds = { US: usDescriptionId, UK: ukDescriptionId };
  const today = format(new Date(), "yyyy-MM-dd");

  const marketQuery = useQuery({
    queryKey: ["today-market-status"],
    queryFn: () => api.market.getStatus(),
    retry: 1,
  });
  const positionsQuery = useQuery({
    queryKey: ["today-positions"],
    queryFn: () => api.positions.list(),
    retry: 1,
  });
  const signalsQuery = useQuery({
    queryKey: ["today-signals"],
    queryFn: () => api.signals.list(),
    retry: 1,
  });

  const queries = [marketQuery, positionsQuery, signalsQuery];
  const allFailed = queries.every((q) => q.isError);
  const anyFailed = queries.some((q) => q.isError);
  const allResolved = queries.every((q) => !q.isLoading);

  const mktData = marketQuery.data?.data ?? marketQuery.data;
  const regimes = MARKETS.map((m) => ({ market: m, status: regimeStatusOf(mktData?.[m.field]) }));

  const positions = Array.isArray(positionsQuery.data) ? positionsQuery.data : [];
  const exits = selectExitsDue(positions);
  const grace = selectGraceEndsToday(positions);
  const stops = selectStopsMoved(positions, stopsMovedWindow());
  const signals = selectTodaySignals(Array.isArray(signalsQuery.data) ? signalsQuery.data : [], today);

  const isQuiet = allResolved && !anyFailed && exits.length === 0 && grace.length === 0 && stops.length === 0 && signals.length === 0;

  const retryAll = () => queries.forEach((q) => q.refetch());

  let body;
  if (allFailed) {
    body = (
      <p data-testid="today-unavailable" className={`text-sm ${MUTED}`}>
        Today's list is unavailable.{" "}
        <button type="button" onClick={retryAll} className={`text-sm ${LINK}`}>
          Retry
        </button>
      </p>
    );
  } else if (isQuiet) {
    body = (
      <p data-testid="today-quiet" className={`text-sm leading-7 ${MUTED}`}>
        Nothing due today
        {regimes.map(({ market, status }) => (
          <span key={market.key}>
            {" · "}
            {market.key}{" "}
            <RegimeBadge market={market} status={status} descriptionId={descriptionIds[market.key]} />
          </span>
        ))}
      </p>
    );
  } else {
    body = (
      <div className="space-y-4">
        {/* 1. Market regime: always shown */}
        {marketQuery.isLoading ? (
          <SkeletonGroup group="regime" />
        ) : marketQuery.isError ? (
          <ErrorGroup group="regime" onRetry={() => marketQuery.refetch()} />
        ) : (
          <div data-testid="today-group-regime" className="space-y-1">
            <GroupHeader name={GROUP_NAMES.regime} />
            <ul className="space-y-1">
              {regimes.map(({ market, status }) => (
                <li key={market.key}>
                  <Link
                    to="/Signals"
                    data-testid={`today-item-regime-${market.key}`}
                    aria-describedby={status === REGIME_UNKNOWN ? descriptionIds[market.key] : undefined}
                    className="flex items-center gap-3 text-sm rounded hover:bg-slate-100 dark:hover:bg-slate-700/40"
                  >
                    <span className={TEXT}>{market.label}</span>
                    <RegimeBadge market={market} status={status} descriptionId={descriptionIds[market.key]} />
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 2. Exits due, 3. Grace ends today and 4. Stops moved: GET /positions */}
        {positionsQuery.isLoading ? (
          <>
            <SkeletonGroup group="exits" />
            <SkeletonGroup group="grace" />
            <SkeletonGroup group="stops" />
          </>
        ) : positionsQuery.isError ? (
          <>
            <ErrorGroup group="exits" onRetry={() => positionsQuery.refetch()} />
            <ErrorGroup group="grace" onRetry={() => positionsQuery.refetch()} />
            <ErrorGroup group="stops" onRetry={() => positionsQuery.refetch()} />
          </>
        ) : (
          <>
            {exits.length > 0 && (() => {
              const { shown, overflow } = capped(exits);
              return (
                <div data-testid="today-group-exits" className="space-y-1">
                  <GroupHeader name={GROUP_NAMES.exits} count={exits.length} />
                  <p className={`text-sm ${MUTED}`}>
                    These positions meet a strategy exit condition (§8). Nothing is exited automatically.
                  </p>
                  <ul className="space-y-1">
                    {shown.map(({ position, condition }) => (
                      <li
                        key={position.id}
                        data-testid={`today-item-exits-${position.ticker}`}
                        className="flex items-center gap-3 text-sm"
                      >
                        <span className={`font-semibold ${TEXT}`}>{position.ticker}</span>
                        {condition.riskOff ? (
                          <span
                            className="inline-flex items-center text-xs px-1.5 py-0.5 rounded-full text-white font-medium"
                            style={{ backgroundColor: "#1E40AF" }}
                          >
                            RISK OFF
                          </span>
                        ) : (
                          <span
                            className="inline-flex items-center text-xs px-1.5 py-0.5 rounded-full text-white font-medium"
                            style={{ backgroundColor: "#EA580C" }}
                          >
                            STOP REACHED
                          </span>
                        )}
                        <Link
                          to={`/Positions?exit=${encodeURIComponent(position.id)}`}
                          aria-label={`Review exit for ${position.ticker}`}
                          className={`ml-auto ${LINK}`}
                        >
                          Review exit
                        </Link>
                      </li>
                    ))}
                  </ul>
                  <Overflow group="exits" count={overflow} to="/Positions" />
                </div>
              );
            })()}
            {grace.length > 0 && (
              <PositionLinkGroup
                group="grace"
                items={grace}
                text={() => "Grace ends today — the trailing stop applies from the next session"}
              />
            )}
            {stops.length > 0 && <PositionLinkGroup group="stops" items={stops} text={stopMovedText} />}
          </>
        )}

        {/* 5. New signals: GET /signals, API order, no rank shown */}
        {signalsQuery.isLoading ? (
          <SkeletonGroup group="signals" />
        ) : signalsQuery.isError ? (
          <ErrorGroup group="signals" onRetry={() => signalsQuery.refetch()} />
        ) : signals.length > 0 && (() => {
          const { shown, overflow } = capped(signals);
          return (
            <div data-testid="today-group-signals" className="space-y-1">
              <GroupHeader name={GROUP_NAMES.signals} count={signals.length} />
              <ul className="space-y-1">
                {shown.map((s, i) => (
                  <li
                    key={s.id ?? `${s.ticker}-${i}`}
                    data-testid={`today-item-signals-${s.ticker}`}
                    className="flex items-center gap-3 text-sm"
                  >
                    <span className={`font-semibold ${TEXT}`}>{s.ticker}</span>
                    <span className={MUTED}>{s.market}</span>
                    <Link
                      to={`/research/${encodeURIComponent(s.ticker)}`}
                      aria-label={`Research ${s.ticker}`}
                      className={`ml-auto ${LINK}`}
                    >
                      Research
                    </Link>
                  </li>
                ))}
              </ul>
              <Overflow group="signals" count={overflow} to="/Signals" />
            </div>
          );
        })()}
      </div>
    );
  }

  return (
    <section
      data-testid="today-list"
      aria-labelledby="today-list-title"
      className="rounded-2xl bg-white dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/50 p-6"
    >
      <h2 id="today-list-title" className={`text-sm font-semibold mb-3 ${TEXT}`}>
        Due today
      </h2>
      {body}
      {/* Accessible descriptions for UNKNOWN regime badges (dashboard.md v3.10 Card 4 rule, kept in §1B) */}
      {regimes
        .filter(({ status }) => status === REGIME_UNKNOWN)
        .map(({ market }) => (
          <span key={market.key} id={descriptionIds[market.key]} className="sr-only">
            {unknownRegimeExplanation(market.key)}
          </span>
        ))}
    </section>
  );
}
