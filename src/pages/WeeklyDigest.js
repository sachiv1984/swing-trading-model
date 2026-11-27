/**
 * WeeklyDigest — ST-09 (BLG-FEAT-14 FE component, v2.4); rewritten as a
 * readable weekly summary in v9.18 (ST-15, BLG-UX-15) with onward links
 * (ST-16, BLG-UX-12).
 *
 * GET /digest/weekly as a list of plain-language figures, each linked to the
 * page where it is reviewed, with a freshness caption. Raw figures only, no
 * narrative or advice. Row building lives in src/lib/weeklyDigest.js.
 *
 * Spec: docs/specs/frontend/pages/weekly_digest.md v0.6;
 *       docs/specs/api_contracts/digest_endpoints.md v0.8
 */
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { RefreshCw, Printer, ArrowRight } from "lucide-react";
import { apiFetch } from "../api/base44Client";
import PageHeader from "../components/ui/PageHeader";
import { PAGE_LABELS } from "../lib/pageLabels";
import DataState from "../components/ui/DataState";
import { Button } from "../components/ui/button";
import { digestFigures, freshnessCaption, loopSteps, loopCaption } from "../lib/weeklyDigest";
import { recordLoopEvent } from "../api/loopEvents";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const LINK_CLASS =
  "text-cyan-700 dark:text-cyan-400 hover:text-cyan-800 dark:hover:text-cyan-300 underline underline-offset-2";

function FigureValue({ row }) {
  const text = row.muted ? (
    <span className="text-app-muted">{row.value}</span>
  ) : (
    row.value
  );
  if (!row.href) return text;
  return (
    <Link
      to={row.href}
      data-testid={`digest-link-${row.field}`}
      aria-label={`${row.label}: ${row.value}`}
      className={LINK_CLASS}
    >
      {row.value}
    </Link>
  );
}

function SecondLine({ row }) {
  const { text, href } = row.secondLine;
  return (
    <span className="block text-xs text-app-muted mt-0.5">
      {href ? (
        <Link to={href} data-testid={`digest-second-link-${row.field}`} className={LINK_CLASS}>
          {text}
        </Link>
      ) : (
        text
      )}
    </span>
  );
}

function LoopStep({ step }) {
  if (!step.href) {
    return (
      <span className={step.muted ? "text-app-muted" : "tabular-nums text-app-fg"} data-testid={`digest-loop-${step.key}`}>
        {step.label}: {step.value}
      </span>
    );
  }
  return (
    <Link
      to={step.href}
      data-testid={`digest-loop-${step.key}`}
      className={`tabular-nums ${LINK_CLASS}`}
    >
      {step.label}: {step.value}
    </Link>
  );
}

// This week's loop (ST-17, weekly_digest.md §2): counts only, no rates.
function WeeklyLoop({ loop }) {
  const caption = loopCaption(loop?.week_start);
  const steps = loopSteps(loop);
  return (
    <section data-testid="digest-loop" aria-labelledby="digest-loop-heading" className="space-y-2">
      <h2 id="digest-loop-heading" className="text-lg font-semibold text-app-fg">This week&apos;s loop</h2>
      {caption && <p data-testid="digest-loop-caption" className="text-xs text-app-muted">{caption}</p>}
      <ol className="flex flex-wrap items-center gap-x-2 gap-y-1">
        {steps.map((step, i) => (
          <li key={step.key} className="flex items-center gap-2">
            {i > 0 && <ArrowRight aria-hidden="true" data-testid="digest-loop-arrow" className="w-3.5 h-3.5 text-app-muted" />}
            <LoopStep step={step} />
          </li>
        ))}
      </ol>
    </section>
  );
}

function DigestFigures({ data }) {
  return (
    <div className="space-y-3">
      <dl
        data-testid="digest-figures"
        className="divide-y divide-app-line rounded-2xl border border-app-line bg-app-raised"
      >
        {digestFigures(data).map((row) => (
          <div
            key={row.field}
            data-testid={`digest-figure-${row.field}`}
            className="flex items-start justify-between gap-4 px-4 py-3"
          >
            <dt className="font-medium text-app-fg">{row.label}</dt>
            <dd className="text-right tabular-nums text-app-fg">
              <FigureValue row={row} />
              {row.secondLine && <SecondLine row={row} />}
            </dd>
          </div>
        ))}
      </dl>
      <p data-testid="digest-as-of" className="text-xs text-app-muted">
        {freshnessCaption(data)}
      </p>
      <WeeklyLoop loop={data.loop} />
    </div>
  );
}

function DigestActions({ canPrint, onRefresh }) {
  return (
    <div className="flex items-center gap-2">
      {canPrint && (
        <Button
          variant="outline"
          size="sm"
          data-testid="print-export-pdf-btn"
          onClick={() => window.print()}
          className="border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
        >
          <Printer className="w-4 h-4 mr-2" />
          Print / Export PDF
        </Button>
      )}
      <Button
        variant="ghost"
        size="sm"
        onClick={() => onRefresh()}
        className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800"
      >
        <RefreshCw className="w-4 h-4 mr-2" />
        Refresh
      </Button>
    </div>
  );
}

// One "Weekly Digest opened" event per page load (ST-17), not per refetch or
// Refresh. The digest query waits for it to settle (at most OPENED_EVENT_WAIT_MS)
// so this week's Reviews always include today's visit. React StrictMode runs
// the effect twice in development only; reviews count distinct UTC days, so a
// duplicate never inflates them.
const OPENED_EVENT_WAIT_MS = 1500;

function useOpenedEvent() {
  const [settled, setSettled] = useState(false);
  useEffect(() => {
    let active = true;
    const done = () => active && setSettled(true);
    const timer = setTimeout(done, OPENED_EVENT_WAIT_MS);
    recordLoopEvent("weekly_digest_opened").then(done);
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, []);
  return settled;
}

export default function WeeklyDigest() {
  const eventSettled = useOpenedEvent();

  // isPending, not isLoading: the query is disabled until the opened event
  // settles, and a disabled query with no data is pending but not loading.
  const { data, isPending, isError, refetch } = useQuery({
    queryKey: ["weeklyDigest"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE_URL}/digest/weekly`);
      const json = await res.json();
      if (json?.status !== "ok") throw new Error(json?.message || "Digest unavailable");
      return json.data;
    },
    retry: 1,
    enabled: eventSettled,
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title={PAGE_LABELS.WeeklyDigest}
        description="Your last 7 days in figures. Most figures link to the page where you review them."
        actions={<DigestActions canPrint={!isPending && !isError} onRefresh={refetch} />}
      />

      <DataState
        loading={isPending}
        error={isError}
        onRetry={refetch}
        className="min-h-[300px]"
      >
        {data && <DigestFigures data={data} />}
      </DataState>
    </div>
  );
}
