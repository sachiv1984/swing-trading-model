/**
 * WeeklyDigest — ST-09 (BLG-FEAT-14 FE component, v2.4); rewritten as a
 * readable weekly summary in v9.18 (ST-15, BLG-UX-15) with onward links
 * (ST-16, BLG-UX-12).
 *
 * GET /digest/weekly as a list of plain-language figures, each linked to the
 * page where it is reviewed, with a freshness caption. Raw figures only, no
 * narrative or advice. Row building lives in src/lib/weeklyDigest.js.
 *
 * Spec: docs/specs/frontend/pages/weekly_digest.md v0.5;
 *       docs/specs/api_contracts/digest_endpoints.md v0.7
 */
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { RefreshCw, Printer } from "lucide-react";
import { apiFetch } from "../api/base44Client";
import PageHeader from "../components/ui/PageHeader";
import { PAGE_LABELS } from "../lib/pageLabels";
import DataState from "../components/ui/DataState";
import { Button } from "../components/ui/button";
import { digestFigures, freshnessCaption } from "../lib/weeklyDigest";

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

export default function WeeklyDigest() {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["weeklyDigest"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE_URL}/digest/weekly`);
      const json = await res.json();
      if (json?.status !== "ok") throw new Error(json?.message || "Digest unavailable");
      return json.data;
    },
    retry: 1,
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title={PAGE_LABELS.WeeklyDigest}
        description="Your last 7 days in figures. Most figures link to the page where you review them."
        actions={<DigestActions canPrint={!isLoading && !isError} onRefresh={refetch} />}
      />

      <DataState
        loading={isLoading}
        error={isError}
        onRetry={refetch}
        className="min-h-[300px]"
      >
        {data && <DigestFigures data={data} />}
      </DataState>
    </div>
  );
}
