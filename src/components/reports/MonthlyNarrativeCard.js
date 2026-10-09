/**
 * AI summary card for the Monthly P&L report — ST-25 (EPIC-04, v9.11, BLG-FEAT-59).
 *
 * Spec: docs/specs/frontend/pages/reports.md §AI Summary (Monthly P&L Narrative), v0.21
 * Design: docs/design/2026-10-08__release-v9.11/monthly-pnl-ai-narrative/decision_record.md
 * §13: docs/product/decisions/decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md
 *
 * Optional (nothing is generated until Generate is pressed), dismissible
 * (Hide/Show, remembered per browser), advisory-labelled, and kept apart from
 * the financial record: it is a separate card and never feeds a figure or an
 * export. The only actions are Generate/Regenerate and Hide/Show (§13
 * Condition 7).
 */
import { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { formatDistanceToNow } from "date-fns";
import { X } from "lucide-react";
import { base44, apiFetch } from "../../api/base44Client";
import { Button } from "../ui/button";
import { Skeleton } from "../ui/skeleton";
import AiDisclaimer from "../shared/AiDisclaimer";

const HIDDEN_KEY = "reports.monthlyNarrative.hidden";
const CAPTION = "Describes your recorded figures only. Not a forecast, recommendation or tax advice.";
const FAILURE_MESSAGE = "Could not write the summary. Try again shortly.";

function readHidden() {
  try {
    return window.localStorage.getItem(HIDDEN_KEY) === "true";
  } catch {
    return false; // blocked or throwing storage: visible
  }
}

function writeHidden(value) {
  try {
    window.localStorage.setItem(HIDDEN_KEY, value ? "true" : "false");
  } catch {
    // storage unavailable: the choice lasts for this page view only
  }
}

// Accept a response only if it is a narrative payload for the requested
// year. This drops a late response for a previously selected year, and any
// payload that is not a narrative at all.
function narrativeFor(body, year) {
  const data = body && body.data;
  if (!data || Array.isArray(data) || data.year !== year) return null;
  return data;
}

export default function MonthlyNarrativeCard({ year }) {
  const [hidden, setHidden] = useState(readHidden);
  const [generated, setGenerated] = useState(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState(null);
  const yearRef = useRef(year);

  useEffect(() => {
    yearRef.current = year;
    setGenerated(null);
    setPending(false);
    setError(null);
  }, [year]);

  const { data: stored } = useQuery({
    queryKey: ["monthlyPnlNarrative", year],
    queryFn: () =>
      apiFetch(`${base44.baseUrl}/reports/monthly-pnl/narrative?year=${year}`)
        .then((r) => (r.ok ? r.json() : null))
        .catch(() => null),
    retry: false,
  });

  const storedForYear = narrativeFor(stored, year);
  const current =
    generated && generated.year === year
      ? generated
      : storedForYear && storedForYear.narrative
        ? storedForYear
        : null;

  const handleGenerate = async () => {
    const requestedYear = year;
    setPending(true);
    setError(null);
    try {
      const res = await apiFetch(`${base44.baseUrl}/reports/monthly-pnl/narrative`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ year: requestedYear, regenerate: Boolean(current) }),
      });
      const body = await res.json().catch(() => null);
      if (yearRef.current !== requestedYear) return; // the year changed while waiting
      if (!res.ok) {
        setError(res.status === 429 && body && body.message ? body.message : FAILURE_MESSAGE);
        return;
      }
      const data = narrativeFor(body, requestedYear);
      if (!data || !data.narrative) {
        setError(FAILURE_MESSAGE);
        return;
      }
      setGenerated(data);
    } catch {
      if (yearRef.current === requestedYear) setError(FAILURE_MESSAGE);
    } finally {
      if (yearRef.current === requestedYear) setPending(false);
    }
  };

  const hide = () => {
    setHidden(true);
    writeHidden(true);
  };
  const show = () => {
    setHidden(false);
    writeHidden(false);
  };

  if (hidden) {
    return (
      <div>
        <Button
          variant="ghost"
          size="sm"
          onClick={show}
          data-testid="monthly-narrative-show"
          className="text-slate-600 dark:text-slate-400"
        >
          Show AI summary
        </Button>
      </div>
    );
  }

  const generatedAt = current && current.generated_at ? new Date(current.generated_at) : null;
  const generatedAtValid = generatedAt && !Number.isNaN(generatedAt.getTime());

  return (
    <div
      data-testid="monthly-narrative-card"
      className="rounded-xl border border-slate-300 dark:border-slate-600/50 bg-white dark:bg-slate-800/30 p-5"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300">AI summary</h3>
          <AiDisclaimer
            variant="badge"
            caption={CAPTION}
            testId="monthly-narrative-caption"
            badgeTestId="monthly-narrative-badge"
          />
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={hide}
          aria-label="Hide AI summary"
          data-testid="monthly-narrative-hide"
          className="text-slate-600 dark:text-slate-400 shrink-0"
        >
          <X className="w-4 h-4" aria-hidden="true" />
        </Button>
      </div>

      {pending && !current ? (
        <div className="flex flex-col gap-2" aria-hidden="true" data-testid="monthly-narrative-skeleton">
          <Skeleton className="h-4 w-3/5 bg-slate-300/60 dark:bg-slate-700/60" />
          <Skeleton className="h-3 w-full bg-slate-300/60 dark:bg-slate-700/60" />
          <Skeleton className="h-3 w-4/5 bg-slate-300/60 dark:bg-slate-700/60" />
        </div>
      ) : current ? (
        <div className="space-y-2">
          {current.source === "fallback" && (
            <p data-testid="monthly-narrative-fallback-note" className="text-xs text-slate-600 dark:text-slate-400">
              The AI summary couldn't be checked against your figures, so a standard summary is shown.
            </p>
          )}
          <p
            data-testid="monthly-narrative-text"
            className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-line"
          >
            {current.narrative}
          </p>
        </div>
      ) : (
        <p className="text-sm text-slate-600 dark:text-slate-400">Get a short written summary of these months.</p>
      )}

      <div className="flex items-center justify-between gap-3 mt-4">
        {current && generatedAtValid ? (
          <span
            data-testid="monthly-narrative-generated-at"
            title={generatedAt.toLocaleString()}
            className="text-xs text-slate-600 dark:text-slate-400"
          >
            Generated {formatDistanceToNow(generatedAt, { addSuffix: true })}
          </span>
        ) : (
          <span />
        )}
        <Button
          variant="outline"
          size="sm"
          onClick={handleGenerate}
          disabled={pending}
          data-testid="monthly-narrative-generate"
          className="text-xs"
        >
          {current
            ? pending ? "Regenerating…" : "Regenerate"
            : pending ? "Generating…" : "Generate summary"}
        </Button>
      </div>

      {error && (
        <p data-testid="monthly-narrative-error" role="status" className="text-xs text-rose-700 dark:text-rose-400 mt-2">
          {error}
        </p>
      )}
    </div>
  );
}
