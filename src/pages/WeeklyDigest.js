/**
 * WeeklyDigest — ST-09 (BLG-FEAT-14 FE component, v2.4)
 *
 * Renders GET /digest/weekly response as a structured data table.
 * All displayed values are raw numeric — no narrative or interpretation.
 *
 * Spec: docs/specs/api_contracts/digest_endpoints.md v0.1
 */
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { CalendarDays, RefreshCw, Printer } from "lucide-react";
import { apiFetch } from "../api/base44Client";
import { createPageUrl } from "../utils";
import PageHeader from "../components/ui/PageHeader";
import DataState from "../components/ui/DataState";
import { Button } from "../components/ui/button";
import {
  DataTable,
  TableHeader,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
} from "../components/ui/DataTable";

// Alert-count deep-links (v0.2, ST-02/EPIC-02/v7.7) — both source from the
// `notifications` table (same table backing the Notification Feed), so both
// deep-link into the Feed with a filter query, not Alert History.
const ALERT_COUNT_LINKS = {
  alerts_fired_7d: `${createPageUrl("notifications")}?since_days=7`,
  alerts_dismissed_7d: `${createPageUrl("notifications")}?since_days=7&read=true`,
};

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function formatValue(field, value) {
  if (value === null || value === undefined) return "—";
  switch (field) {
    case "realised_pnl_7d":
      return `£${value.toFixed(2)}`;
    case "unrealised_pnl_delta_7d":
      return `£${value.toFixed(2)}`;
    case "compliance_score_current":
    case "compliance_score_7d_ago":
      return `${value.toFixed(1)}%`;
    case "staleness_hours":
      return `${value.toFixed(1)} h`;
    case "as_of_utc":
      return value;
    default:
      return String(value);
  }
}

const FIELD_LABELS = [
  { field: "realised_pnl_7d",           label: "Realised P&L (7d)",            unit: "GBP" },
  { field: "unrealised_pnl_delta_7d",    label: "Unrealised P&L Delta (7d)",     unit: "GBP" },
  { field: "alerts_fired_7d",            label: "Alerts Fired (7d)",             unit: "count" },
  { field: "alerts_dismissed_7d",        label: "Alerts Dismissed (7d)",         unit: "count" },
  { field: "compliance_score_current",   label: "Compliance Score (current)",    unit: "%" },
  { field: "compliance_score_7d_ago",    label: "Compliance Score (7d ago)",     unit: "%" },
  { field: "staleness_hours",            label: "Data Staleness",                unit: "hours" },
  { field: "as_of_utc",                  label: "As of (UTC)",                   unit: "timestamp" },
];

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
        title="Weekly Digest"
        description="7-day trading summary"
        actions={
          <div className="flex items-center gap-2">
            {!isLoading && !isError && (
              <Button
                variant="outline"
                size="sm"
                data-testid="print-export-pdf-btn"
                onClick={() => window.print()}
                className="border-slate-700 text-slate-300 hover:bg-slate-800"
              >
                <Printer className="w-4 h-4 mr-2" />
                Print / Export PDF
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => refetch()}
              className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>
          </div>
        }
      />

      <DataState
        loading={isLoading}
        error={isError}
        onRetry={refetch}
        className="min-h-[300px]"
      >
        <DataTable>
          <TableHeader>
            <TableHead>Field</TableHead>
            <TableHead>Unit</TableHead>
            <TableHead className="text-right">Value</TableHead>
          </TableHeader>
          <TableBody>
            {FIELD_LABELS.map(({ field, label, unit }) => {
              const value = data ? formatValue(field, data[field]) : "—";
              const linkTo = ALERT_COUNT_LINKS[field];
              const isLinkable = linkTo && value !== "—";
              return (
                <TableRow key={field}>
                  <TableCell className="font-medium text-slate-200">{label}</TableCell>
                  <TableCell className="text-slate-600 dark:text-slate-400 text-sm">{unit}</TableCell>
                  <TableCell className="text-right font-mono text-slate-300">
                    {isLinkable ? (
                      <Link
                        to={linkTo}
                        data-testid={`digest-link-${field}`}
                        className="text-cyan-400 hover:text-cyan-300 underline underline-offset-2"
                      >
                        {value}
                      </Link>
                    ) : (
                      value
                    )}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </DataTable>
      </DataState>
    </div>
  );
}
