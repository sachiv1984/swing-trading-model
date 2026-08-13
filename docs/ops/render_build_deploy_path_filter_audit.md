**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-08-13 (ST-16, EPIC-06, v8.7, BLG-OPS-140 — onboarding note added, runtime-read inventory re-verified current); prior — 2026-07-31 (ST-16, EPIC-04, v8.0, BLG-OPS-124 — production filter conclusively confirmed via deploy trigger-source label)
**Story:** ST-16 (BLG-OPS-140, EPIC-06, v8.7); originated ST-16 (BLG-OPS-124, EPIC-04, v8.0)

---

# Render Build/Deploy Path Filter Audit

## ⚠️ Read this before assuming a deploy will pick up a non-code file change

**If you are adding or changing a file the running app reads at runtime that is *not* `.py`/`.js` source (a markdown file, CSV, JSON config, etc.) — stop and check this document's Runtime File-Read Inventory below, and confirm the file is covered by *both* deploy-trigger mechanisms, before assuming a normal push will redeploy it.** This has silently bitten this project twice already (`BLG-OPS-82`, then `BLG-OPS-90`/commit `e9c73f58`) — a docs-only change to a file the app reads at request time didn't trigger a redeploy, and the staleness wasn't visible anywhere in the repo. See "Two Distinct Path-Filter Mechanisms" immediately below for why a repo-only search cannot catch this on its own.

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
- **Production filter (dashboard-only):** Configuration read live 2026-07-31 (see §Production Filter Configuration below). **No gap found — conclusively confirmed** via the deploy trigger-source label (see below), resolving the ambiguity the FinOps & Resource Architect review correctly flagged.

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

**Follow-up check performed (resolves the ambiguity):** the `95b2e6bf` deploy's detail view in the Render dashboard was checked directly — it reads:

> "Deploy started for 95b2e6b: Merge pull request #1160 from sachiv1984/exec/2026-07-30__release-v8.0/EPIC-01 [EPIC-01] Data Model & Spec Integrity — **New commit via Auto-Deploy** — July 30, 2026 at 11:09 AM"

The explicit **"New commit via Auto-Deploy"** label confirms this was a genuine automatic push-triggered deploy, not a manual dashboard click. This directly rules out possibility 2 (manual trigger) from the review finding above. Possibility 1 is therefore confirmed: Render's push-triggered auto-deploy fired automatically for a `backend/**`-only commit that did not touch `docs/product/changelog.md`, under the Root-Directory-as-default-scope model.

**Coverage check against the Runtime File-Read Inventory (above) — repo-side claims independently re-verified, both hold:**
- `docs/product/changelog.md` reads confirmed in all 3 named services (`changelog_service.py`, `ai_spend_trend_service.py`, `changelog_digest_service.py`).
- `feature_flags.json` confirmed absent from the repo (`ls feature_flags.json` → no such file).
- `backend/tickers_full_list.csv` and all `backend/**` runtime-read paths — now conclusively confirmed covered by the Root Directory default, per the trigger-source label above.
- `docs/product/changelog.md` — confirmed covered by the explicit Included Paths entry (this was never in dispute; only the `backend/**` default-scope side needed the stronger check).

**Result: no gap found, conclusively confirmed.** Production's filter correctly covers every currently-existing runtime-read file: `backend/**` via the Root Directory default (proven by the Auto-Deploy label on a real backend-only commit), and `docs/product/changelog.md` via the explicit Included Paths supplement. The `BLG-OPS-82`/`e9c73f58` fix is correctly configured. No dashboard change needed.

---

## Refresh (2026-08-13, ST-16/EPIC-06/v8.7, `BLG-OPS-140`)

Re-ran the Runtime File-Read Inventory scan against the current codebase (`json.load(`/`.read_text()`/`open(` calls on non-`.py` files across `backend/`) to confirm no new runtime-read file has been added since the 2026-07-31 audit that would need a path-filter check:

- `feature_flags.json` — confirmed still absent from the repo (`ls feature_flags.json` → no such file). The flagged gap remains purely hypothetical, unchanged.
- `docs/product/changelog.md` readers — same 3 services as before (`changelog_service.py`, `ai_spend_trend_service.py`, `changelog_digest_service.py`), no new reader added.
- `backend/tickers_full_list.csv` — same reader (`ticker_universe_service.py`), unchanged.
- `current_portfolio.json` readers (`position_manager.py::load_portfolio()`, `portfolio_setup.py`, `live_trading_assistant.py`) — re-confirmed the specific functions that read the file remain CLI-only (`if __name__ == "__main__":` guarded), not part of the live app's request path. **Precision correction to the prior audit's phrasing:** `position_manager.py` *as a module* is in fact imported live (`routers/portfolio_risk.py` and `routers/pre_entry_validation.py` both do `from position_manager import check_market_regime`) — but `check_market_regime()` is a distinct function from `load_portfolio()`/`save_portfolio()` and never touches `current_portfolio.json`. The file-read itself is still CLI-only; only the "never imported into the live app" framing was too broad at the module level.

**No new gap found.** Both filters (staging's repo-visible `paths:` list, production's dashboard Included Paths + Root Directory default) remain correctly configured for every file the running app actually reads.

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| FinOps & Resource Architect | **BLOCKED** (initial pass) — the "no gap found" conclusion rested on one deploy event that could not distinguish an automatic push-triggered deploy from a manual dashboard click. Required the deploy trigger-source label as a conclusive check. | 2026-07-31 |
| FinOps & Resource Architect | **APPROVED** — the required trigger-source label was checked directly: the `95b2e6bf` deploy is confirmed "New commit via Auto-Deploy," ruling out the manual-trigger alternative and confirming Render's push-triggered auto-deploy correctly fires for `backend/**` changes under the Root-Directory-as-default-scope model. No gap found; no dashboard change needed. | 2026-07-31 |
