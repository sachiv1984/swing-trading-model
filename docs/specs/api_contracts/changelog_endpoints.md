# changelog_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-07-26
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Story:** ST-01 (BLG-FE-128, EPIC-01, v7.8)

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
    "version": "v7.8",
    "changes": [
      "In-app what's new panel",
      "Telegram changelog digest"
    ]
  }
}
```

If `docs/product/changelog.md` is missing, has no parseable version heading, or the most recent version has no `### Changes shipped` table:

```json
{
  "status": "ok",
  "data": null
}
```

#### Field notes

- `version`: the bare version number of the most recent changelog heading (e.g. `"v7.8"`) — the title/date portion of the heading is not surfaced, per the UX spec's `"What's New — v{X.Y}"` title format.
- `changes`: the `Description` column of the most recent version's `### Changes shipped` table, in table order, one entry per row. Does not include the `EPIC` or `Spec sections updated` columns — those are internal governance references, not user-facing copy.
- `data: null` signals the frontend to render the `DataState` empty branch ("Nothing to show" / "Check back after the next release.").

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
| 1.0 | 2026-07-26 | Initial spec. ST-01 (BLG-FE-128, EPIC-01, v7.8): `GET /changelog/latest` added, backing the in-app "What's New" panel. Authority: API Contracts & Documentation Owner. |
