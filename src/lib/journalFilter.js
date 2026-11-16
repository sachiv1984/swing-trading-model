// Shared ticker filter for the Journal page (journal.md v1.1 §3; ST-05,
// BLG-FE-258, EPIC-02, v9.17).
//
// Reflections and Position notes filter in the browser: case-insensitive
// partial match, ignoring a UK ".L" suffix on both sides ("AA" matches "AAPL";
// "LGEN" and "LGEN.L" both match "LGEN.L"). Red flags is filtered by the
// server on the exact ticker, so it gets the input as typed, upper-cased.

export const JOURNAL_SECTIONS = ["reflections", "red-flags", "notes"];
export const DEFAULT_JOURNAL_SECTION = "reflections";

export function journalSection(value) {
  return JOURNAL_SECTIONS.includes(value) ? value : DEFAULT_JOURNAL_SECTION;
}

function baseTicker(value) {
  return String(value ?? "").trim().toUpperCase().replace(/\.L$/, "");
}

export function tickerMatches(itemTicker, filter) {
  const wanted = baseTicker(filter);
  if (!wanted) return true;
  return baseTicker(itemTicker).includes(wanted);
}

export function redFlagTicker(filter) {
  return String(filter ?? "").trim().toUpperCase();
}
