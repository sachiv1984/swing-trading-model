// ST-03 (EPIC-01, v9.6, BLG-FEAT-97): client-side CSV generation for Screener results and
// Watchlist. Design: docs/design/2026-09-21__release-v9.6/screener-watchlist-csv-export/decision_record.md
//
// Columns are `{ header, value(row, ctx) }` arrays defined once per table and consumed by both
// the table header renderer and buildCsv, so the exported header row cannot drift from the
// rendered one. Format: UTF-8, RFC 4180 quoting, \r\n terminators, no BOM.

const FORMULA_TRIGGERS = ["=", "+", "-", "@"];

// Spreadsheet-formula-injection guard (§2.4): a STRING cell beginning with = + - @ is prefixed
// with a single quote. Numeric cells (incl. negatives) are written as numbers and untouched.
export function guardFormulaInjection(value) {
  return typeof value === "string" && value.length > 0 && FORMULA_TRIGGERS.includes(value[0])
    ? `'${value}`
    : value;
}

export function toCsvField(value) {
  if (value == null) return "";
  if (typeof value === "number") return Number.isFinite(value) ? String(value) : "";
  const s = String(guardFormulaInjection(value));
  return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export function buildCsv(columns, rows, ctx) {
  const lines = [columns.map((c) => toCsvField(c.header)).join(",")];
  rows.forEach((row) => {
    lines.push(columns.map((c) => toCsvField(c.value(row, ctx))).join(","));
  });
  return lines.join("\r\n") + "\r\n";
}

export function csvFilename(prefix, date = new Date()) {
  const pad = (n) => String(n).padStart(2, "0");
  return `${prefix}-${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}.csv`;
}

export function downloadCsv(filename, csv) {
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  try {
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  } finally {
    URL.revokeObjectURL(url);
  }
}
