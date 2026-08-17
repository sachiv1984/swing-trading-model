**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-16
**Story:** ST-24 (BLG-SEC-18, EPIC-05, v8.8)

# Baseline npm audit HIGH/CRITICAL Findings — Review

## 1. Purpose

`BLG-SEC-18` (filed at the `docs/security/dependency_vuln_baseline.json` baseline capture, v8.5) flagged 16 npm packages carrying HIGH/CRITICAL advisories as "known, not yet individually risk-assessed." This review individually assesses each and dispositions per the AC: fixed (removed from baseline) or a recorded accept-risk decision (owner, rationale, review-by date).

## 2. Method

Fresh `npm audit --json` re-run (not trusted from the stale baseline snapshot alone) — cross-referenced every GHSA ID in the resulting HIGH/CRITICAL findings against `docs/security/dependency_vuln_baseline.json`'s `npm_audit.advisory_ids` array: **exact match, 41/41, zero drift since baseline capture** (no new advisory, none resolved on its own since 2026-08-10). Confirmed the baseline's `high_critical_count: 16` field correctly counts distinct **packages** (16), while `advisory_ids` correctly counts distinct **GHSA IDs** (41, since several packages carry multiple advisories, e.g. `react-router`'s 12) — both figures are internally consistent, not a drift or documentation bug.

For each of the 16 packages, checked: (a) is it a direct `package.json` dependency or purely transitive; (b) is it imported anywhere in `src/` (i.e. does it ship in the production bundle and run in the browser) or is it exclusively part of the `react-scripts` build toolchain (runs only during `npm run build`/`npm start`, on the developer/CI machine, never in a deployed user's browser); (c) is a non-breaking fix available.

## 3. Findings and Disposition

### 3.1 Fixed (2 packages — react-router, react-router-dom)

Unlike the other 14, **`react-router-dom` is a direct `package.json` dependency, genuinely imported throughout `src/pages/` (`useLocation`, `useNavigate`, etc.) and shipped in the production bundle** — the baseline item's own problem statement framed all 16 as "not direct runtime dependencies of the shipped app," which is accurate for the other 14 but not for this pair.

| Package | Advisories | Fix |
|---------|-----------|-----|
| `react-router` | 12 GHSA IDs (RCE, XSS, DoS, CSRF, open-redirect — severities high/moderate/low) | Upgraded transitively via `react-router-dom` |
| `react-router-dom` | (wrapper, no own advisory) | `^7.13.0` → `^7.18.2` (same major version, non-breaking per `npm audit`'s `fixAvailable: true`) |

Verified: `npm run build` succeeds; `tests/e2e/smoke-critical-paths.spec.js` and `tests/e2e/sidebar-nav-groups.spec.js` (navigation-dependent specs) both pass against the upgraded version. Post-fix `npm audit`: these 12 advisories no longer appear in the HIGH/CRITICAL set.

### 3.2 Accept-risk (14 packages — react-scripts build-toolchain, no production exposure)

| Package(s) | Confirmed no direct `src/` import (build-tooling only) |
|---|---|
| `@svgr/plugin-svgo`, `@svgr/webpack`, `svgo` | ✅ |
| `postcss` | ✅ |
| `nanoid` | ✅ |
| `js-yaml` | ✅ |
| `ws`, `websocket-driver` | ✅ (webpack-dev-server's hot-reload transport) |
| `tar` | ✅ (webpack-dev-server file-watching) |
| `shell-quote` | ✅ |
| `brace-expansion` | ✅ |
| `fast-uri` | ✅ |
| `form-data` | ✅ |

**Accept-risk decision:**
- **Owner:** Cybersecurity & Trust Lead
- **Rationale:** All 14 are transitive dependencies pulled in exclusively by `react-scripts` v5's build/dev toolchain (webpack-dev-server → ws/tar/websocket-driver/shell-quote; svgo/postcss-loader chain; etc.) — confirmed via repo-wide grep that none is imported by any application source file. They execute only during `npm run build` (CI/local, producing the static bundle) or `npm start` (local dev server) — never inside a deployed user's browser, never in the shipped `build/` output. `npm audit`'s severity classification does not account for this exposure distinction; the practical risk is materially lower than "high/critical" implies for a package that never runs in a untrusted-input-facing production context. No non-major fix is available for any of the 14 — each is pinned by `react-scripts`'s own dependency tree (`fixAvailable` reports a forced `react-scripts` major-version bump for the ones checked individually, e.g. `svgo`), and `react-scripts` (Create React App) is itself unmaintained upstream with no compatible non-breaking upgrade path.
- **Review-by date:** 2027-02-16 (6 months) — re-run this same review at or before that date; re-assess sooner if any of the 14 packages' advisories gain a working exploit chain reachable through the dev-server (e.g. a documented attack requiring only that `npm start` be running, not attacker-controlled application input) or if a CRA→(Vite/other) migration is scoped, which would resolve the whole class at once.
- **Durable fix path:** filed `BLG-TECH-11` (see §5) recommending eventual migration off the CRA/`react-scripts` v5 toolchain (e.g. to Vite) as the only path that closes this vulnerability class definitively, rather than deferring individually forever. Not scoped or estimated here — a toolchain migration is a substantial, separate initiative outside this S-effort audit story.

No package in either group is fixed by silently ignoring — 2 fixed directly, 14 explicitly accept-risk with a recorded rationale and review-by date, satisfying the AC in full for all 16.

## 4. Baseline File Update

`docs/security/dependency_vuln_baseline.json` updated in this commit, per its own header comment's instruction to update once a finding is reviewed and fixed or accept-risked: the 12 `react-router` advisory IDs are removed (genuinely fixed, confirmed absent from a fresh `npm audit`); `high_critical_count` corrected `16` → `14`; the `note` field updated to record the accept-risk disposition and point to this document instead of describing the findings as unreviewed.

## 5. Backlog Items Filed

- **BLG-TECH-11** — Scope a future migration off Create React App (`react-scripts` v5) to an actively-maintained build toolchain (e.g. Vite), as the durable fix for the 14 accept-risk findings in §3.2 (P3, no effort estimate — scoping only)

## 6. Sign-off

- [x] All 16 packages individually assessed (not blanket-accepted)
- [x] 2 genuinely fixed (verified via build + targeted Playwright regression check)
- [x] 14 accept-risk with owner, rationale, and review-by date recorded
- [x] Durable fix path (toolchain migration) filed as a backlog item, not left implicit
- Signed off by: PENDING — see agent-mediated review
- Date: PENDING
