# changelog_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-08-16 (ST-13, BLG-FE-161, EPIC-03, v8.8 — sourcing switched to `User Impact`); prior — 2026-07-26 (initial spec)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Story:** ST-01 (BLG-FE-128, EPIC-01, v7.8); ST-13 (BLG-FE-161, EPIC-03, v8.8)

## Overview

This document defines the **Changelog** endpoint, backing the in-app "What's New" panel (`docs/specs/frontend/pages/dashboard.md` §6A).

---

## Endpoints

- [GET /changelog/latest](#get-changeloglatest)

---

## GET /changelog/latest

**Purpose**

Return the most recent release's version label and changes-shipped descriptions, parsed server-side from `docs/product/changelog.md`'s most recent `## vX.Y — <title> — <date>` block. Parsed on each request — no hardcoded copy in the frontend build, so a new release is picked up automatically with no manual wiring.

**Method & Path**

- `GET /changelog/latest`

**Idempotency**

- Safe to refresh (read-only).

### Request

No parameters.

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "version": "v8.8",
    "changes": [
      "Trade plans now let you record what would invalidate your thesis right when you write it."
    ]
  }
}
```

If `docs/product/changelog.md` is missing, has no parseable version heading, the most recent version has no `### Changes shipped` table, or that table has no row with a populated `User Impact` cell:

```json
{
  "status": "ok",
  "data": null
}
```

#### Field notes

- `version`: the bare version number of the most recent changelog heading (e.g. `"v8.8"`) — the title/date portion of the heading is not surfaced, per the UX spec's `"What's New — v{X.Y}"` title format.
- `changes`: the `User Impact` column of the most recent version's `### Changes shipped` table, in table order, one entry per row with a non-empty cell (BLG-FE-161, v8.8 — see `docs/product/changelog.md`'s authoring convention note). Rows with a blank/`—` `User Impact` cell are excluded — this is the mechanism satisfying "an EPIC with no user-facing change does not appear in the What's New feed." Does not include the `EPIC`, `Description`, or `Spec sections updated` columns — `Description` is the engineering record and internal governance references, not user-facing copy.
- `data: null` signals the frontend to render the `DataState` empty branch ("Nothing to show" / "Check back after the next release."). This also occurs for a release whose `### Changes shipped` table predates the `User Impact` column (pre-v8.8) or where every row's `User Impact` cell is blank/`—`.

### Notes

- This endpoint never raises on a malformed or missing changelog — it returns `data: null` rather than a 500, since a missing/malformed changelog is not itself an application error condition worth surfacing as one.
- The frontend truncates `changes` to the first 8 entries with a non-interactive "+N more" trailer if longer — truncation is a display concern, not enforced server-side, so this endpoint always returns the full list.

---

## Known Deviations

None.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-08-16 | ST-13 (BLG-FE-161, EPIC-03, v8.8): sourcing switched from the `Description` column to a new `User Impact` column (curated, user-facing copy); rows with a blank/`—` `User Impact` cell are excluded from `changes` entirely. `Description` is unaffected and remains the engineering record. Design source: `docs/design/2026-08-14__release-v8.8/whats-new-user-benefit-copy/decision_record.md`. Authority: API Contracts & Documentation Owner. |
| 1.0 | 2026-07-26 | Initial spec. ST-01 (BLG-FE-128, EPIC-01, v7.8): `GET /changelog/latest` added, backing the in-app "What's New" panel. Authority: API Contracts & Documentation Owner. |
