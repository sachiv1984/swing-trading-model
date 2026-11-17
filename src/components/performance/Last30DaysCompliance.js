import { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { base44, apiFetch } from "../../api/base44Client";
import { formatPercent } from "../../lib/format";
import { getCurrentUKTaxYear } from "./ReportViews";

// Performance → Compliance → "Last 30 days" (performance.md v1.1 §4, §5.1;
// ST-06, BLG-FE-259, EPIC-02, v9.17). The Reports Monthly "Strategy
// Compliance" block, moved: Validation Pass Rate, Override Count and Red Flag
// Events over the last 30 days. Most Frequent Breach is not shown here — its
// one home is Arc 5's Top Rule Breach (ruling 2026-11-16).
// Data: GET /reports/monthly-pnl `compliance_summary` (reports_endpoints.md),
// which covers the last 30 days whatever the year; read through the same
// ['monthlyPnl', year] query as the Monthly view, so the two share a cache.
// The monthly report is the whole tax year's computation, so it is fetched only
// once this block is near the viewport (review finding, ST-06), unless the
// Monthly view has already cached it.
function useNearViewport() {
  const ref = useRef(null);
  const [near, setNear] = useState(typeof IntersectionObserver === "undefined");
  useEffect(() => {
    if (near || !ref.current) return undefined;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setNear(true);
          observer.disconnect();
        }
      },
      { rootMargin: "400px 0px" }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, [near]);
  return [ref, near];
}

export default function Last30DaysCompliance() {
  const year = getCurrentUKTaxYear();
  const [ref, near] = useNearViewport();
  const { data: response, isLoading, isError } = useQuery({
    queryKey: ["monthlyPnl", year],
    queryFn: () =>
      apiFetch(`${base44.baseUrl}/reports/monthly-pnl?year=${year}`).then((r) => r.json()),
    enabled: near,
  });
  const compliance = response?.compliance_summary ?? null;

  return (
    <div
      ref={ref}
      data-testid="strategy-compliance-section"
      className="rounded-xl border border-app-line bg-app-raised overflow-hidden"
    >
      <div className="px-6 py-4 border-b border-app-line">
        <h3 className="text-sm font-semibold text-app-fg">Last 30 days</h3>
        <p className="text-xs text-app-muted mt-0.5">
          Pre-entry discipline counts — last {compliance?.period_days ?? 30} days.
        </p>
      </div>
      {!response && (!near || isLoading) ? (
        <div className="px-6 py-6 text-center text-app-muted text-sm">Loading…</div>
      ) : isError || compliance === null ? (
        <div className="px-6 py-6 text-center text-app-muted text-sm">Compliance data unavailable.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-px bg-app-line">
          <div data-testid="compliance-pass-rate" className="bg-app-raised px-5 py-4">
            <p className="text-xs text-app-muted uppercase tracking-wide mb-1">Validation Pass Rate</p>
            <p className="text-lg font-semibold text-app-fg">
              {formatPercent(compliance.validation_pass_rate != null ? compliance.validation_pass_rate * 100 : null)}
            </p>
          </div>
          <div data-testid="compliance-override-count" className="bg-app-raised px-5 py-4">
            <p className="text-xs text-app-muted uppercase tracking-wide mb-1">Override Count</p>
            <p className="text-lg font-semibold text-app-fg">{compliance.override_count ?? "—"}</p>
          </div>
          <div data-testid="compliance-red-flag-count" className="bg-app-raised px-5 py-4">
            <p className="text-xs text-app-muted uppercase tracking-wide mb-1">Red Flag Events</p>
            <p className="text-lg font-semibold text-app-fg">{compliance.red_flag_events_count ?? "—"}</p>
          </div>
        </div>
      )}
    </div>
  );
}
