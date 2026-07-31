**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.1
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
- **Production filter (dashboard-only):** Configuration read live 2026-07-31 (see §Production Filter Configuration below). **Status: provisionally under review, not yet cleared** — see FinOps & Resource Architect finding below. An initial hypothesis about how this configuration behaves was tested against one data point and found consistent with "no gap," but that single data point cannot rule out an equally plausible alternative explanation. A cheap, conclusive follow-up check is identified and pending.

### Production Filter Configuration

Read live via Render dashboard (Settings → Build & Deploy, production API service), 2026-07-31:

- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Build Filters → Included Paths:** `docs/product/changelog.md` (no other entries)

**Initial hypothesis and its test:** the concern was that a bare Included Paths list acts as an exhaustive allow-list — i.e. that setting it to just `docs/product/changelog.md` would mean *only* changelog-only commits auto-deploy, and all `backend/**` changes would be silently ignored (a severe, easily-missed production risk). This was checked against real deploy history: the production service's most recent deploy is live for commit `95b2e6bf` (`[EPIC-01] Data Model & Spec Integrity`), which touched only `backend/database.py`, `backend/main.py`, `backend/routers/*.py`, `backend/services/position_service.py`, `backend/strategy_version_registry.py` — zero changes to `docs/product/changelog.md`. It deployed anyway.

**FinOps & Resource Architect review finding (2026-07-31): this single observation is NOT conclusive.** It cannot distinguish between two possibilities that would produce the identical "most recent deploy is live for 95b2e6bf" observation:
1. Render's push-triggered auto-deploy fired automatically, under a model where Root Directory contents (`backend/**`) form an implicit default trigger scope and Included Paths only adds extra paths outside it (which would mean the current config is correct).
2. A human manually clicked "Deploy latest commit" in the Render dashboard after merging PR #1160 — an entirely ordinary post-merge action — which would say nothing about whether push-triggered auto-deploy actually respects `backend/**` changes, and the severe-risk hypothesis (Included Paths as an exhaustive allow-list, silently blocking all future backend auto-deploys) would remain live.

Two official Render documentation pages, checked independently during the review, gave framings that are not obviously consistent with each other on this exact interaction (Root Directory set *and* Included Paths simultaneously non-empty, pointing outside it) — so this cannot be resolved by re-reading documentation either.

**Required follow-up (identified by the reviewer, cheap and conclusive):**
- Open the `95b2e6bf` deploy's detail view in the Render dashboard and check its trigger-source label (Render typically labels each deploy as e.g. "Deploy triggered by push to main" vs. "Manual deploy"). This directly resolves the ambiguity with no further inference.
- If that label is unavailable or ambiguous: push a trivial, harmless backend-only commit (e.g. a comment, not touching `changelog.md`) and confirm autodeploy fires with zero manual dashboard interaction — the same live-fire rigor already applied to ST-13/ST-14 this cycle.

**Coverage check against the Runtime File-Read Inventory (above) — repo-side claims independently re-verified, both hold:**
- `docs/product/changelog.md` reads confirmed in all 3 named services (`changelog_service.py`, `ai_spend_trend_service.py`, `changelog_digest_service.py`).
- `feature_flags.json` confirmed absent from the repo (`ls feature_flags.json` → no such file).
- Whether the *filter mechanism* itself actually covers `backend/tickers_full_list.csv` and `docs/product/changelog.md` in production remains the open question above — the file-existence/reader facts are solid, the deploy-trigger mechanism is not yet proven.

**Result: not yet resolved — do not close on the current evidence.** Proceeding to sign off "no gap found" on a single ambiguous data point would risk exactly the kind of silent, undetected drift this audit exists to catch, given the failure mode (all future backend changes silently failing to auto-deploy) is severe.

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| FinOps & Resource Architect | **BLOCKED** — the "no gap found" conclusion rested on one deploy event that cannot distinguish an automatic push-triggered deploy from a manual dashboard click, and Render's own documentation is not clearly consistent with the proposed Root-Directory-as-default-scope mechanism. Given the failure mode is silent non-deployment of all future backend changes, sign-off must wait on the cheap, conclusive check identified above (deploy trigger-source label, or a trivial backend-only live-fire push test). | 2026-07-31 |
