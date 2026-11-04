// ST-04 (BLG-FE-243, EPIC-01, v9.15): a calendar date as YYYY-MM-DD in the
// browser's local timezone. `toISOString().split("T")[0]` gives the UTC date,
// which is the previous day between midnight and 01:00 BST (and earlier
// still further east), so it must not be used for a date the user means as
// "today" or a day they picked.
export function localDateString(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

export function todayLocal() {
  return localDateString(new Date());
}
