// Release version label shared by the sidebar footer and the Dashboard What's
// New heading (navigation.md §Sidebar Footer and Height; dashboard.md §6A;
// ST-14, BLG-FE-266, v9.15). The changelog feed's version may arrive as "9.15"
// or "v9.15"; both display as "v9.15". A missing or blank version returns null,
// and callers then show no version text — never "undefined" or a hard-coded one.
export function formatReleaseVersion(version) {
  if (version === null || version === undefined) return null;
  const bare = String(version).trim().replace(/^v/i, "");
  return bare ? `v${bare}` : null;
}
