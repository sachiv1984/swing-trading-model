**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-27 (assessment created)
**Source:** ST-34 (`BLG-TECH-23`), EPIC-05, cycle `2026-10-16__release-v9.13`

# Major Dependency Upgrade Assessment — October 2026

## 1. Purpose

The October 2026 quarterly review (`docs/security/dependency_update_review_2026-10-06.md` §6) found 8 direct dependencies a major version, or a breaking minor series, behind. This document assesses each one: what breaks for this codebase, the effort, and an upgrade-or-hold decision. Approved upgrades are filed as separate backlog items (§5). Nothing is upgraded here.

tailwindcss 4 and `react-scripts` are out of scope and stay with `BLG-TECH-21` (CRA → Vite).

## 2. Method

Assessed 2026-10-27.

- **Latest versions:** PyPI JSON API and `npm view`, 2026-10-27.
- **Breaking changes:** each package's own changelog, release notes or migration guide (anthropic `CHANGELOG.md`, `MIGRATION.md` and the API version `2026-10-21` migration guide; uvicorn release notes; reportlab `CHANGES.md` from the 5.1.0 sdist; motion `CHANGELOG.md`; lucide 1.0.1 release notes and the 1.62.0 package's exports and icon builder; ESLint's "Migrate to v10.x" guide).
- **Usage in this codebase:** `grep` of `backend/`, `scripts/`, `src/` and `tests/` for each package's imports, the APIs they call and test selectors that depend on them.
- **Runtime pins:** every candidate was checked against the pinned runtimes, Python 3.11.0 (`backend/.python-version`, CI, `render.yaml`) and Node 22 (CI), because the numpy 2.5 bump failed for that reason (`BLG-TECH-24`).
- **Vulnerabilities:** OSV (`api.osv.dev`) for each package at its current version.

## 3. Summary

| Package | Current | Latest | Known vulnerability | Effort | Decision | Backlog item |
|---------|---------|--------|---------------------|--------|----------|--------------|
| anthropic (Python) | 0.105.2 | 2.3.0 | None | S | Upgrade, straight to 2.x | `BLG-TECH-25` |
| SQLAlchemy | 2.0.52 | 2.1.6 | None | XS | Remove: never imported | `BLG-TECH-26` |
| reportlab | 4.2.5 | 5.1.0 | None in OSV; 4.4.8 – 5.0.3 ship security fixes | S | Upgrade | `BLG-TECH-27` |
| uvicorn[standard] | 0.24.0 | 0.54.0 | None | XS | Upgrade | `BLG-TECH-28` |
| framer-motion | 12.29.0 (lock 12.43.0) | 14.7.1 | None | S | Upgrade, with a design check | `BLG-TECH-29` |
| lucide-react | 0.563.0 | 1.62.0 | None | S | Upgrade, with a design check | `BLG-TECH-30` |
| eslint | 9.39.5 | 10.13.0 | None | M | Hold | — |
| moment | 2.30.1 (lock 2.31.0) | 2.31.0 | GHSA-4p3w-j4w9-5jqw below 2.31.0; lock already has the fix | XS | Replace with `date-fns` and remove | `BLG-TECH-31` |

Seven upgrades approved, one held.

## 4. Package Assessments

### anthropic (Python SDK)

**Used by:** `services/ai_service.py`, `services/gemini_service.py`, `services/debrief_service.py`, `services/monthly_pnl_narrative_service.py` (`anthropic.Anthropic(api_key=..., timeout=...)` and `client.messages.create(...)` only), and `utils/upstream_call.py` (retries on `APITimeoutError`, `APIConnectionError`, `RateLimitError`, `InternalServerError`). Models in `backend/ai_models.py`: `claude-haiku-4-5`, `claude-sonnet-4-6`.

**Breaking changes that apply:**
- **1.0 (2026-08-20):** the HTTP layer moved from `httpx` to `httpx2`. Error objects now carry `httpx2` requests and responses. `tests/test_upstream_call_helper.py` and `tests/test_gemini_claude_retry_backoff.py` build `anthropic.RateLimitError` from `httpx.Request`/`httpx.Response`; they must build them from `httpx2`. `routers/test.py` uses `httpx` itself and keeps it.
- **1.0:** `temperature`, `top_p` and `top_k` were removed from `messages.create()`. None of the four services passes them (checked).
- **2.0 (2026-10-21):** requests use API version `2026-10-21`. Its Messages-API breaks (documents in assistant messages, citations in user messages, sampling parameters) are not used here. The key is sent as `Authorization: Bearer` instead of `X-Api-Key`; nothing here reads that header. `MessageParam` is now a union; the services pass dict literals, which need no change. A client holds one credential; each service passes only `api_key`.

**Not affected:** Python ≥ 3.10 required; the backend runs 3.11.0.

**Effort:** S (~0.5d). Bump the pin, add `httpx2` if it is not pulled in transitively, port the two tests to `httpx2`, then run one live call per AI feature on staging.

**Decision: upgrade, straight to 2.x.** Skipping 1.x avoids two migrations. The 0.x line no longer gets fixes, and staying on API version `2023-06-01` leaves the backend on an old contract as new models arrive.

### SQLAlchemy

**Used by:** nothing. No file in `backend/`, `scripts/` or `tests/` imports it; database access is `psycopg2` throughout. It was added to `backend/requirements.txt` in `3579d2ff` (2026-02-16) and never used.

**Breaking changes that apply:** none, because nothing calls it.

**Effort:** XS. Delete the line, then run the full pytest suite and a Render staging build.

**Decision: remove, do not upgrade.** An unused dependency still costs install time and adds to the audit surface.

### reportlab

**Used by:** `services/reports_service.py::build_tax_year_pdf` only (the tax-year PDF export). It uses `SimpleDocTemplate`, `Paragraph`, `Table`, `TableStyle`, `Spacer`, `getSampleStyleSheet`, `colors`, `landscape(A4)`, `mm` and the built-in `Helvetica-Bold` font. It loads no images or remote URLs.

**Breaking changes that apply:**
- **5.0.0a1:** `trustedHosts=None` now means no host is trusted in `open_for_read`. This only affects images or files fetched by URL; the export fetches none.
- **5.0.4:** started replacing Times with a new base font in the default styles. `getSampleStyleSheet()` title and body styles may render in a different face, so the PDF needs a visual check.
- **5.1.0a1:** Python ≥ 3.10 required; the backend runs 3.11.0.

**Security:** OSV lists no advisory for 4.2.5, but 4.4.8, 4.4.10, 5.0.1, 5.0.2 and 5.0.3a1 each record a security fix (a callback hole, `trustedHosts` on redirects, issues reported by external researchers). Those mostly concern untrusted input, which the export does not take, but staying on 4.2 means missing them.

**Effort:** S (~0.5d). Bump the pin, add a pytest that builds a PDF from a fixed report and checks it parses (no test covers `build_tax_year_pdf` today), and compare one exported PDF before and after.

**Decision: upgrade.**

### uvicorn[standard]

**Used by:** `render.yaml` start command `uvicorn main:app --host 0.0.0.0 --port $PORT`, `validate-analytics.yml` (same form), and `main.py`'s `uvicorn.run(...)` dev entry point. `main.py`'s logging setup names the `uvicorn`, `uvicorn.error` and `uvicorn.access` loggers. The app has no WebSocket routes.

**Breaking changes that apply:** none found across 0.25 – 0.54. Changes in the range: Python 3.8 and 3.9 dropped (0.34, 0.40); `--reload` WatchGod removed (0.33; not used); `colorama` dropped from `standard` (0.51); `--ws auto` now picks `websockets-sansio` (0.50; no WebSockets here); proxy-header handling refined and IPv6 loopback trusted by default in `FORWARDED_ALLOW_IPS` (0.53). The three logger names are unchanged.

**Effort:** XS (~0.25d). Bump the pin, then check the Render staging deploy starts and access logs still appear in the same format.

**Decision: upgrade.**

### framer-motion

**Used by:** 28 files in `src/`, all `import { motion }` or `import { motion, AnimatePresence }`.

**Breaking changes that apply:**
- **13.0.0:** the optional `@emotion/is-prop-valid` dependency was removed in favour of `<MotionConfig isValidProp>`. It is not installed here, so prop filtering does not change.
- **14.0.0:** removed internal APIs kept for 13.0 – 13.4 compatibility. Nothing here uses internals.
- Peer dependency React 18 or 19; the app runs React 19.

The two majors break almost nothing for this app's usage. The risk is in behaviour fixes between 12.43 and 14.7 (`AnimatePresence` exit ordering, value resolution before first render, spring changes), which can change how an animation looks without failing any test.

**Effort:** S (~0.5d). Bump, run the Playwright suite, and have the Head of UX & Design look at the animated surfaces (modals, panels, page transitions) on staging.

**Decision: upgrade, with a design check before merge.**

### lucide-react

**Used by:** 127 files in `src/`, importing 105 distinct icons. Playwright selects icons by class in four specs (`svg.lucide-triangle-alert`, `svg.lucide-chevron-right`, `svg.lucide-clock`, `svg[class*="lucide-pen"]`/`lucide-edit`), and one asserts `aria-hidden="true"`.

**Breaking changes that apply:**
- **Renamed icons:** the October review expected the 1.x rename to break imports. Checked against the 1.62.0 package: all 105 names used here are still exported, including the 18 old names (`AlertTriangle`, `AlertCircle`, `CheckCircle2`, `Loader2`, `BarChart3`, `Trash2`, `XCircle` and 11 others), and none is marked deprecated. No import changes are needed.
- **Classes:** 1.x still puts `lucide-<name>` and `lucide-<alias>` classes on each `<svg>`, so the four Playwright selectors keep working.
- **`aria-hidden="true"` by default:** the one spec that checks it already expects `true`.
- **Brand icons removed:** none used.
- **Icon artwork:** 1.x redraws some icons, so the same name can look different.

**Effort:** S (~0.5d). Bump, run the Playwright suite, and have the Head of UX & Design check the most-used icons on staging. Moving to the new names (e.g. `TriangleAlert`) is optional and can follow later.

**Decision: upgrade, with a design check before merge.**

### eslint

**Used by:** `eslint.config.mjs` (flat config) with `@eslint/js`, `globals`, `eslint-plugin-react`, `eslint-plugin-react-hooks`, `eslint-plugin-playwright`, `eslint-plugin-no-comments` and `eslint-plugin-better-max-params`. The file is protected: changing it needs Product Owner sign-off, and a PreToolUse hook blocks automated edits. `react-scripts` bundles its own ESLint for the build and is unaffected.

**Breaking changes that apply:**
- **Plugin blocker:** `eslint-plugin-react` 7.37.5, the latest release (last published 2025-04-03), declares peer `eslint` up to `^9.7` only. ESLint 10 also removes deprecated `context` members and `SourceCode` methods that older plugins call. Installing ESLint 10 fails the peer check, or needs `--legacy-peer-deps` with a plugin that may crash.
- `eslint:recommended` gains `no-unassigned-vars`, `no-useless-assignment` and `preserve-caught-error`, so new violations would need triage.
- `@eslint/js` 10 must move in step with ESLint.
- Node ^20.19 or ^22.13 is required; CI runs Node 22.

The other plugins already accept ESLint 10.

**Effort:** M while the React plugin lags; S once it supports ESLint 10.

**Decision: hold.** Re-evaluate when `eslint-plugin-react` publishes a release with ESLint 10 in its peer range, or as part of `BLG-TECH-21` if the Vite migration changes the lint setup first.

### moment

**Used by:** `src/pages/SystemStatus.js` only, in two places: `moment(data.as_of).format('HH:mm, D MMM YYYY')` and `moment(healthData.timestamp).fromNow()`. `date-fns` 4.4.0 is already a dependency and is used in 19 files.

**Breaking changes that apply:** not an upgrade. moment is deprecated (maintenance mode), so the question is replacing it.

**Security:** GHSA-4p3w-j4w9-5jqw (moderate, published 2026-09-29) is a path traversal in `moment.locale()` with a crafted non-string locale, fixed in 2.31.0. It affects server-side use only. This app calls moment in the browser and never calls `moment.locale()`. The lockfile already resolves 2.31.0.

**Effort:** XS (~0.25d). Use `format(date, 'HH:mm, d MMM yyyy')` and `formatDistanceToNow(date, { addSuffix: true })`, then remove `moment`. `fromNow()` and `formatDistanceToNow` word short intervals differently ("a few seconds ago" against "less than a minute ago"). The System Status Playwright spec only checks `/^As of /`, so no assertion breaks.

**Decision: replace with `date-fns` and remove `moment`.**

## 5. Backlog Items Filed

One item per approved upgrade, each to land in its own PR with a full CI run. Each item checks the pinned runtime before the bump lands (`BLG-TECH-24`).

- `BLG-TECH-25`: anthropic 0.105 → 2.x
- `BLG-TECH-26`: remove the unused SQLAlchemy pin
- `BLG-TECH-27`: reportlab 4.2 → 5.x, with a PDF build test
- `BLG-TECH-28`: uvicorn 0.24 → 0.54
- `BLG-TECH-29`: framer-motion 12 → 14, with a design check
- `BLG-TECH-30`: lucide-react 0.563 → 1.x, with a design check
- `BLG-TECH-31`: replace moment with date-fns
- eslint 10: held, no item. Re-evaluation condition in §4.
- tailwindcss 4 and `react-scripts`: unchanged, with `BLG-TECH-21`.

## 6. Sign-off

- [x] All 8 packages assessed: breaking changes for this codebase, effort and an upgrade-or-hold decision
- [x] Every approved upgrade has its own backlog item; eslint is held with a re-evaluation condition
- [x] tailwindcss 4 left with `BLG-TECH-21`
- Prepared by: Sprint Execution Engine (autonomous; ST-34)
- Date: 2026-10-27
