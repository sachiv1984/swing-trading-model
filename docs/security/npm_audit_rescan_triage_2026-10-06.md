**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-06
**Source:** GitHub issue #1885 (`dependency-vuln-rescan.yml`, 2026-10-01 scheduled run) — `[GOVERNANCE]` hotfix, out-of-cycle (`2026-09-30__release-v9.9` Closed)

# Monthly Rescan npm audit Findings — Triage (October 2026)

## 1. Purpose

The 2026-10-01 scheduled re-scan (`shared_standards.md` §20, Tier 3) filed issue #1885 with 6 packages carrying HIGH advisory IDs absent from `docs/security/dependency_vuln_baseline.json`. A fresh `npm audit` at triage time (2026-10-06) found 6 further newly-disclosed packages (12 in total) — advisories published between the scheduled run and triage, equally present on `main`. This record dispositions all 12, following the method of `npm_audit_baseline_review_2026-08-16.md` (ST-24, BLG-SEC-18).

## 2. Method

For each package: (a) direct `package.json` dependency or transitive; (b) imported anywhere in `src/` (ships in the production bundle) or build/dev-toolchain only; (c) non-breaking fix available. Verification re-ran `scripts/check_dependency_vuln_rescan.py` (the workflow's own analysis script) against a post-fix `npm audit --json`, so the result matches what the next scheduled run will report.

## 3. Findings and Disposition

### 3.1 Fixed (7 packages)

| Package | Advisories | Fix |
|---------|-----------|-----|
| `brace-expansion` | 6 GHSA IDs | Lockfile-only bump (`npm audit fix --legacy-peer-deps`) |
| `fast-uri` | 8 GHSA IDs | Lockfile-only bump |
| `js-yaml` | 4 GHSA IDs | Lockfile-only bump — 4.x paths patched; the remaining 3.x copy (under `svgo`) is now MODERATE only, below the rescan's HIGH/CRITICAL threshold |
| `http-proxy-middleware` | `GHSA-64mm-vxmg-q3vj` | Lockfile-only bump |
| `proxy-addr` | `GHSA-jqcg-44mw-7w3h` (critical) | Lockfile-only bump |
| `source-map-js` | `GHSA-68fv-2mgg-jv7q` | Lockfile-only bump |
| `compression` | `GHSA-vc2v-76pw-4v95` | `package.json` override `"compression": ">=1.8.2"` — `serve` 14.2.6 pins 1.8.1 exactly; 1.8.2 is a patch release |

The same lockfile bump also cleared previously-baselined accept-risk findings (`shell-quote`, `websocket-driver`, `ws`, `form-data`, `nanoid`, `tar` and others — 23 IDs). Net `npm audit` change: critical 3 → 0, high 64 → 55.

Verified: `npm ci --legacy-peer-deps` succeeds; `CI=false PUBLIC_URL=/ npm run build` succeeds (the Playwright `webServer` build command); `npx serve -s build` serves the bundle with gzip `Content-Encoding` under `compression` 1.8.2. Playwright E2E runs in CI on the PR.

### 3.2 Accept-risk (5 packages — build/dev toolchain, no production exposure, no fix)

| Package | Advisories | Pulled in by | Why not fixed |
|---------|-----------|--------------|---------------|
| `svgo` 1.3.2 | `GHSA-4vpr-x523-8j87`, `GHSA-w27v-7q3p-w38r` (+ `GHSA-2p49-hgcm-8545`, already accept-risk) | `react-scripts` → `@svgr/webpack` | Fix is `svgo` 2.8.4+; only via a `react-scripts` major bump (none exists — CRA unmaintained) |
| `webpack-dev-server` 4.15.2 | `GHSA-4v9v-hfq4-rm2v`, `GHSA-79cf-xcqc-c78w`, `GHSA-9jgg-88mc-972h`, `GHSA-f5vj-f2hx-8m93`, `GHSA-m28w-2pqf-7qgj`, `GHSA-mx8g-39q3-5c79` | `react-scripts` | Fix is the 5.x major; incompatible with `react-scripts` 5 |
| `webpack-dev-middleware` 5.3.4 | `GHSA-g84c-rxfj-3j2c` | `webpack-dev-server` | Fix is the 7.x major |
| `node-forge` 1.4.0 | `GHSA-86w9-cpqp-85rv` | `webpack-dev-server` → `selfsigned` | No patched release published (1.4.0 is latest) |
| `braces` 3.0.3 | `GHSA-vfj7-8cjw-p6xm` | `tailwindcss`/`react-scripts` → `chokidar`/`micromatch` | No patched release published (3.0.3 is latest) |

Repo-wide grep confirms none of the five is imported by any file in `src/`.

**Accept-risk decision:**
- **Owner:** Cybersecurity & Trust Lead
- **Rationale:** All five run only on the developer/CI machine. `webpack-dev-server`, `webpack-dev-middleware` and `node-forge` (its self-signed HTTPS cert helper) run only under `npm start`; their advisories (source-code exposure to a malicious site visited while the dev server runs, path traversal, CSRF on dev endpoints, signature-verification laxity) require a live local dev server and are not reachable in any deployed environment — production is a static `build/` bundle on GitHub Pages / Render. `svgo` and `braces` run only during `npm run build`/`npm start` against repo-controlled input (our own SVGs and glob patterns), so the sanitisation and ReDoS/stack-exhaustion advisories have no untrusted-input path. The `svgo` `removeScripts` advisories would matter only for user-uploaded SVGs, which this app does not accept.
- **Developer guidance (residual risk):** avoid browsing untrusted sites in the same browser while `npm start` is running — the practical mitigation for the `webpack-dev-server` advisories until the toolchain migration ships.
- **Review-by date:** 2027-02-16 — aligned with the 2026-08-16 review so all build-toolchain accept-risk findings are re-reviewed together. Re-assess sooner if `braces` or `node-forge` publish a patched release (both would then be fixable via a lockfile bump or override), or if any advisory gains an exploit path not requiring a running local dev server.
- **Durable fix path:** the CRA → Vite migration scoped in `docs/ops/cra_migration_scoping_2026-09-08.md` (BLG-TECH-11). The migration itself is now filed as a backlog item (see §5) — this rescan is the second consecutive triage dominated by `react-scripts`-pinned findings.

## 4. Baseline File Update

`docs/security/dependency_vuln_baseline.json` updated in the same commit: the 23 IDs no longer reported at HIGH/CRITICAL removed (so any regression re-surfaces as new), the 11 accept-risk IDs in §3.2 added, `high_critical_count` set to 6 (distinct packages carrying their own advisory), `note` updated. Post-update, `scripts/check_dependency_vuln_rescan.py` reports `new_finding_count=0`.

## 5. Backlog Items Filed

- CRA (`react-scripts` v5) → Vite migration — execution item, following BLG-TECH-11's completed scoping

## 6. Sign-off

- [x] All 12 newly-reported packages individually assessed
- [x] 7 fixed (lockfile bump + one patch-level override), verified via install, build and serve
- [x] 5 accept-risk with owner, rationale and review-by date recorded
- [x] Durable fix path filed as a backlog item
- Signed off by: PENDING — Cybersecurity & Trust Lead review on PR
- Date: PENDING
