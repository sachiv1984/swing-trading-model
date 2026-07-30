**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-31
**Story:** ST-16 (BLG-OPS-124, EPIC-04, v8.0)

---

# Render Build/Deploy Path Filter Audit

## Purpose

Render's dashboard-configured build/deploy path filters (Settings → Build & Deploy → Build Filters, for the production service) are invisible to a repo-only search — a change to a file outside the configured watch paths can silently fail to trigger a redeploy with no signal visible in-repo. This is a confirmed **recurring drift class** (first occurrence: `BLG-OPS-82`; second occurrence: commit `e9c73f58`, "Fix stale What's New panel — trigger staging redeploy on changelog.md changes" — see `claude/backlog/backlog.md` BLG-OPS-90 gate-status update).

This document is the in-repo side of the audit: a complete inventory of every non-code file the running application actually reads at runtime, so it can be diffed against the two live path-filter configurations (staging's, which is repo-visible; production's, which is dashboard-only) by anyone with the relevant access. The dashboard remains the source of truth for production's filter — this document does not replace it, it makes the comparison possible.

---

## Two Distinct Path-Filter Mechanisms (do not conflate)

1. **Staging — repo-visible.** `.github/workflows/staging-deploy.yml`'s own `paths:` trigger filter, which calls a Render deploy hook. Current filter: `src/**`, `backend/**`, `public/**`, `package.json`, `package-lock.json`, `requirements.txt`, `docs/product/changelog.md`.
2. **Production — dashboard-only, not in this repo.** Per `render.yaml` (line 3: "Production services are managed separately in the Render dashboard — this file only defines staging"), production's build/deploy path filter lives exclusively in Render's dashboard (Settings → Build & Deploy → Build Filters) for the production service. `render.yaml` itself contains no `buildFilter` or equivalent key for either service it does define (staging API, staging frontend) — confirmed by full read, 64 lines total.

**This audit's runtime-read inventory below must be checked against *both* filters, but only the staging one (#1) can be verified by reading the repo. The production filter (#2) requires a human with Render dashboard access — see disposition below.**

---

## Runtime File-Read Inventory

Every non-code file (markdown, CSV, JSON, config) that the running application actually reads — not build-time tooling inputs (`package.json`, `requirements.txt` — read only by `npm`/`pip` at build time, confirmed no runtime exception), and not test fixtures.

| File | Read by | Timing | Covered by staging filter? |
|------|---------|--------|----------------------------|
| `docs/product/changelog.md` | `backend/services/changelog_service.py` (`get_latest_changelog_entry`) via `GET /changelog/latest` | Request-time | Yes — explicit exception in `staging-deploy.yml` |
| `docs/product/changelog.md` | `backend/services/ai_spend_trend_service.py` (`get_ai_spend_trend`) via `GET /ai/spend-trend` | Request-time (second, independent reader of the same file) | Yes — same exception covers it |
| `docs/product/changelog.md` | `backend/services/changelog_digest_service.py` (`send_changelog_digest`) via `scripts/send_changelog_digest.py` | CLI/manual (Post-Ship Closure step), not part of the always-on request path | Yes |
| `backend/tickers_full_list.csv` | `backend/services/ticker_universe_service.py` (`_load_company_names`, `_load_csv_tickers`) — startup seed (`seed_default_tickers()`, invoked at app startup) and inline during the ticker-add flow | Startup + request-time | Yes — covered by the `backend/**` filter |
| `feature_flags.json` (repo root — **does not currently exist**) | `backend/utils/feature_flags.py` (`_load_flags`), invoked at app startup | Startup, if the file is ever added | **No** — repo-root, not under `src/**`/`backend/**`/`public/**`, and not the changelog exception. Flagged below. |

**Not runtime-read by the live app** (confirmed, excluded): `docs/reference/openapi.yaml` and `docs/System_status_report.md` are referenced only in code comments as "source of truth" prose, never parsed by running code. `current_portfolio.json` (referenced by `backend/position_manager.py`/`portfolio_setup.py`) is only touched by standalone CLI scripts (`if __name__ == "__main__":` guarded), never imported into the live app. No FastAPI `StaticFiles` mount or `FileResponse` exists anywhere in `backend/main.py`/`backend/routers/*.py`.

---

## Finding: `feature_flags.json` gap

`backend/utils/feature_flags.py` optionally reads a repo-root `feature_flags.json` at startup (`os.path.isfile` guard — silently absent today, the file does not exist in this repo). If this file is ever added, it would sit at repo root, outside every current path-filter pattern (staging's `src/**`/`backend/**`/`public/**`/build-file list, and presumably production's dashboard filter too, since production's filter has historically mirrored a similar narrow scope per the `BLG-OPS-82`/`e9c73f58` precedent). Adding this file without also updating both path filters would silently reproduce the exact same drift class this audit exists to catch.

**Recommendation:** if `feature_flags.json` is added in a future story, add it to `staging-deploy.yml`'s `paths:` list in the same commit, and flag the production dashboard filter for the same update.

---

## Disposition

- **Staging filter (repo-visible):** Audited above — currently correctly covers every runtime-read file except the not-yet-existing `feature_flags.json` (flagged, no action needed until that file is actually added).
- **Production filter (dashboard-only):** Cannot be audited from the repo. **Delegated** to FinOps & Resource Architect: read the production service's Build Filters configuration directly from `dashboard.render.com` and confirm it covers the same runtime-read file set in the table above (particularly `docs/product/changelog.md`, given this exact file already caused a staging drift once). Record the production filter's current configuration in this document (§Production Filter Configuration, below) once confirmed.

### Production Filter Configuration

*Pending — to be completed by FinOps & Resource Architect with live Render dashboard access (see `delegation_log.md` DEL-20260731-04).*

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| FinOps & Resource Architect | *Pending — production filter confirmation required before sign-off* | — |
