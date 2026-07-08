/**
 * WeeklyDigest — ST-09 (BLG-FEAT-14 FE component, v2.4)
 *
 * Renders GET /digest/weekly response as a structured data table.
 * All displayed values are raw numeric — no narrative or interpretation.
 *
 * Spec: docs/specs/api_contracts/digest_endpoints.md v0.1
 */
import { useQuery } from "@tanstack/react-query";
import { CalendarDays, RefreshCw } from "lucide-react";
import { apiFetch } from "../api/base44Client";
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
          <Button
            variant="ghost"
            size="sm"
            onClick={() => refetch()}
            className="text-slate-400 hover:text-white hover:bg-slate-800"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
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
            {FIELD_LABELS.map(({ field, label, unit }) => (
              <TableRow key={field}>
                <TableCell className="font-medium text-slate-200">{label}</TableCell>
                <TableCell className="text-slate-400 text-sm">{unit}</TableCell>
                <TableCell className="text-right font-mono text-slate-300">
                  {data ? formatValue(field, data[field]) : "—"}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </DataTable>
      </DataState>
    </div>
  );
}
