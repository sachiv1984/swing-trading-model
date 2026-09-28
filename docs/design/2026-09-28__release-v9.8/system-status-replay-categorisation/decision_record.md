**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-28__release-v9.8
**Story:** ST-04 (EPIC-01, BLG-FE-191)

# Decision Record — System Status Endpoint Category for `/replay` Routes

## 1. Problem

`SystemStatus.js`'s `categorizeEndpoint()` has no pattern matching `/replay`, so `POST /replay/run` falls through to the catch-all `'Other'` category on the endpoint test grid, alongside anything else the function doesn't recognise — not a meaningful grouping for a user checking system health.

## 2. Decision

Add a new **Replay** category, following the page's existing one-category-per-domain-area pattern (Alerts, Notifications, Digest, Cash Management, etc. each get their own icon/colour rather than being folded into a nearby category):

| Category | Match | Icon | Colour |
|----------|-------|------|--------|
| Replay | `endpointName.includes('/replay')` | `RefreshCw` (already imported; thematically fits "replay") | `text-pink-400` / `bg-pink-500/10` / `border-pink-500/30` (first unused colour in the existing palette) |

Checked before the `/health`/`/changelog` "Core" catch-all (consistent with the function's existing most-specific-first ordering) and after all other specific patterns, so it cannot shadow or be shadowed by an existing category. No other endpoint's categorization changes — the new `if` branch only matches `/replay`.

## 3. §13 Compliance

Not applicable — a dashboard label, no AI call.

## 4. Frontend Spec Impact

`system_status.md` gains a new §Endpoint Test Category Labels subsection documenting the categorisation scheme (this is the first time the endpoint-test-grid feature's categories are recorded in this spec at all — the existing spec predates that feature and only covers the top-level service-health cards). Scope is limited to recording the current scheme plus the new Replay row; reconciling the rest of this stale Class 1 spec with the shipped endpoint-test-grid feature is a pre-existing gap, out of this story's scope, and not blocking.

## 5. Testability (CLAUDE.md §2)

The AC ("categorized under a meaningful label, not 'Other'") is a code-level assertion checkable via the existing `SystemStatus` test suite's category-grouping test (add a `/replay` case) rather than a new Playwright visual test — no new rendering behaviour is introduced beyond an existing category-card pattern with a new label.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-28.
Product Owner: confirmed, 2026-09-28.
