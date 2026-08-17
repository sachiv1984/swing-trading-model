**Owner:** QA & Testing Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-16
**Cycle:** 2026-08-14__release-v8.8 (ST-21 — BLG-QA-146)

---

# `backend/routers/test.py` Completeness Re-Audit

## Purpose

Re-audit of `docs/ops/endpoint_test_coverage_audit_2026-07-29.md` (ST-11, BLG-QA-133, v7.10) — confirm zero drift has crept into `backend/routers/test.py`'s `test_cases` coverage since that audit introduced the gate, and since `scripts/check_router_test_registration.py` (ST-10, BLG-QA-125, v7.9) started enforcing new-route registration on every commit.

## Method

Re-derived the full route inventory independently from the July audit (not trusted verbatim): regex-extracted every `@router.(get|post|put|delete|patch)(...)` decorator across all 23 `backend/routers/*.py` files (excluding `test.py` itself) plus each file's `APIRouter(prefix=...)`, resolved to full paths, and cross-referenced against `test_cases`'s 112 registered `(method, path)` entries with path-parameter normalisation (`{param}` / UUID / literal test values collapsed to a wildcard for comparison).

**Scope note:** unlike the July 29 audit, this re-audit does not re-derive `backend/main.py`'s own `@app.*`-decorated routes — the story's own AC names `@router.*` decorators specifically, and `main.py`'s routes are a separate, unchanged surface not touched since the last audit.

## Findings

**84 `@router.*` routes found** (up from an initial 80 on first pass — see §3, a tooling bug in the extraction itself, not a route-count discrepancy). **8 have no direct `test_cases` entry.**

### 7 of 8 — already correctly documented, re-confirmed (not new findings)

All 7 match the "deliberately NOT added" disposition comment already present above `test_cases`'s closing bracket in `test.py` (real-data-mutating endpoints on the live single-portfolio production system): `POST /alerts/rules`, `PATCH /alerts/rules/{rule_id}`, `DELETE /alerts/rules/{rule_id}`, `POST /alerts/evaluate`, `POST /notifications/mark-all-read`, `PATCH /notifications/{notification_id}`, `PATCH /watchlist/{entry_id}`.

### 1 of 8 — genuine undocumented gap, fixed

**`PATCH /notifications/preferences`** (`backend/routers/alerts.py`) — mutates real user notification-preference state (same exclusion class as the 7 above), but was **not** listed in the disposition comment, unlike its siblings. Git history confirms this endpoint has existed since March 2026 (`[EPIC-02][ST-05]`) — it predates the July 29 audit that introduced the comment block, and was missed by that audit rather than newly drifted in since. Fixed by adding it to the documented-exclusion list in `test.py` (not to the active `test_cases` — it remains correctly untested, same as its siblings, for the same mutation-safety reason). No count change to `test_cases` itself, so no cascading update needed to `SystemStatus.js`'s fallback count or `system-status.spec.js`'s `SC-SS-01b` (CLAUDE.md §2's cascade only applies when the active list's element count changes).

## 3. Tooling Bug Found in the Enforcement Script Itself

While re-deriving the route inventory, the same regex used in `scripts/check_router_test_registration.py` (the CI/pre-commit gate that enforces `test.py` registration for *new* routes going forward) was found to have **two compounding bugs**, both fixed in this story:

1. **`ROUTE_DECORATOR_RE`'s path-capture group was `+` (one-or-more), not `*` (zero-or-more)** — silently failed to match a bare `@router.get("")`/`@router.post("")` decorator (an empty-string path, resolving to the router's own prefix root — e.g. `ticker_universe.py`'s `GET`/`POST "/ticker-universe"`). A *newly added* route registered this way would never even be recognised as "a new route" by the gate — not flagged, not warned, silently invisible. (First noticed as an 80-vs-84 discrepancy against a raw `grep -c` count during this audit's own re-derivation.)
2. **Compounding bug, only reachable once #1 is fixed:** `extract_new_routes()`'s prefix-join logic (`prefix.rstrip("/") + "/" + path.lstrip("/")`) produces a **trailing slash** for an empty-string path (e.g. `"/ticker-universe/"`) that `path_pattern()`'s exact `^...$`-anchored match would never match against a `test.py` entry written without the trailing slash — meaning even after fixing bug #1, a genuinely-registered empty-path route would still be **false-positive flagged as unregistered**.

Both fixed in `scripts/check_router_test_registration.py` (regex `+` → `*`; trailing-slash strip after the join). Two new regression tests added to `tests/test_router_test_registration_check.py` (`test_empty_string_path_decorator_is_matched`, `test_empty_string_path_route_extraction_resolves_to_prefix_root`) — both fail against the pre-fix code, pass against the fix. Full script test suite: 12/12 pass (was 10/10 before this story's 2 additions).

This is a meaningfully different class of finding than a `test.py` content gap: the gate meant to catch *future* drift had a blind spot in its own extraction logic for one specific route-declaration style. No evidence any route was actually missed *going forward* by this gate (the one real content gap found, §2, predates the gate's introduction) — but the blind spot was live and would have silently passed a new empty-path route with no warning.

## 4. Disposition

- 1 documentation gap fixed directly (`test.py` comment).
- 2 tooling bugs fixed directly in the enforcement script, with regression test coverage.
- 7 pre-existing exclusions re-confirmed correct, not re-litigated.
- No backlog item filed — both fixes were low-risk, small, and within this story's own S-effort scope (matching the July 29 audit's own precedent of fixing-not-filing for exactly this class of finding).

## 5. Sign-off

- [x] Full route inventory re-derived independently (not trusted from the July 29 audit's numbers)
- [x] Every uncovered route individually assessed (documented-exclusion match vs genuine gap)
- [x] Enforcement-script bug found via a raw-count sanity check against the regex-based extraction, not assumed correct
- [x] Both fixes covered by new regression tests, full script suite re-run green
- Signed off by: PENDING — see agent-mediated review
- Date: PENDING
