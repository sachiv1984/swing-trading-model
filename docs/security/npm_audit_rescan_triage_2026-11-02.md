**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Record (Class 3)
**Status:** Draft
**Last Updated:** 2026-11-02 (triage record created, Cybersecurity & Trust Lead sign-off pending)
**Source:** GitHub issue #2136 (`dependency-vuln-rescan.yml`, 2026-11-01 scheduled run) — `[GOVERNANCE]` hotfix, out-of-cycle (`2026-10-29__release-v9.14` Verified, post-ship closure not yet run)

# Monthly Rescan npm audit Findings — Triage (November 2026)

## 1. Purpose

The 2026-11-01 scheduled re-scan (`shared_standards.md` §20, Tier 3) filed issue #2136 with 3 packages carrying 15 advisory IDs absent from `docs/security/dependency_vuln_baseline.json`. pip-audit reported 0 findings. A fresh `npm audit` at triage time (2026-11-02) reported the same 3 packages. This record dispositions all 3, following the method of `npm_audit_rescan_triage_2026-10-06.md`.

## 2. Method

For each package: (a) direct `package.json` dependency or transitive; (b) imported anywhere in `src/` or build/dev-toolchain only; (c) non-breaking fix available. Verification re-ran `scripts/check_dependency_vuln_rescan.py` (the workflow's own analysis script) against a post-fix `npm audit --json`.

## 3. Findings and Disposition

### 3.1 Fixed (3 packages)

| Package | Version change | New advisories | Pulled in by |
|---------|----------------|----------------|--------------|
| `body-parser` | 1.20.8 → 1.20.9 | `GHSA-27r3-jxmh-p828` | `react-scripts` → `webpack-dev-server` → `express` |
| `follow-redirects` | 1.16.0 → 1.16.2 | `GHSA-8r9p-f939-6h3c`, `GHSA-mrwp-f3q8-3g9p`, `GHSA-q3jh-wrc6-jgq8` | `react-scripts` → `webpack-dev-server` → `http-proxy-middleware` → `http-proxy` |
| `node-forge` | 1.4.0 → 1.4.2 | `GHSA-4487-j8r4-4g2f`, `GHSA-4642-5mcj-2rqw`, `GHSA-525v-9gp9-w22h`, `GHSA-5cwg-6vw7-rj6p`, `GHSA-5x38-2vff-x55p`, `GHSA-6wvx-3r32-xmcg`, `GHSA-7wch-p9px-956x`, `GHSA-8hrf-8g6f-7xwp`, `GHSA-h6cr-wjv9-3cpp`, `GHSA-hqq3-7jhf-c5jx`, `GHSA-jc66-7q78-782g` | `react-scripts` → `webpack-dev-server` → `selfsigned` |

All three are transitive and none is imported by any file in `src/`. The fix is a lockfile-only bump (`npm audit fix --legacy-peer-deps`) with no `package.json` change. `npm audit fix --dry-run` reports no changes for this lockfile, so it should not be used to judge whether a fix exists.

The same bump changes five further transitive packages: `fast-uri` 3.1.8 → 3.1.9, `filelist` 1.0.4 → 1.0.6, `postcss-selector-parser` 6.1.4 → 6.1.5, `qs` 6.16.0 → 6.16.2 and `serialize-javascript` 7.0.5 → 7.1.4. `serialize-javascript` is the only minor-version change and runs at build time.

Net `npm audit` change: high 8 → 5, moderate 44 → 41, low 13 → 10, total 65 → 56, critical 0 → 0.

Verified: `npm ci --legacy-peer-deps` succeeds; `CI=false PUBLIC_URL=/ npm run build` succeeds with the ESLint plugin enabled, which CI's Playwright build does not exercise; `npx serve -s` serves the bundle (root, main JS bundle and a client-side route all return 200). Playwright E2E runs in CI on the PR.

### 3.2 Closed Out From the October Accept-Risk List

| Package | Advisory | Outcome |
|---------|----------|---------|
| `node-forge` | `GHSA-86w9-cpqp-85rv` | Fixed by 1.4.2. The October record held this as accept-risk because no patched release existed; its sign-off condition (2) requires a patched release to be applied at the next monthly triage, and this record does that. |
| `braces` | `GHSA-vfj7-8cjw-p6xm` | No longer reported by `npm audit`, before or after this fix. `braces` remains at 3.0.3, so this is an advisory-data change rather than a code fix. |

### 3.3 Unchanged Accept-Risk

`postcss`, `svgo`, `webpack-dev-server` and `webpack-dev-middleware` remain HIGH and keep their existing accept-risk records (`npm_audit_baseline_review_2026-08-16.md`, `npm_audit_rescan_triage_2026-10-06.md`), review-by 2027-02-16. Each is fixable only through BLG-TECH-21 (CRA → Vite). `@svgr/plugin-svgo` is also reported HIGH but has no advisory of its own; it inherits from `svgo`.

## 4. Baseline File Update

`docs/security/dependency_vuln_baseline.json` updated in the same commit: `GHSA-86w9-cpqp-85rv` and `GHSA-vfj7-8cjw-p6xm` removed (so any regression re-surfaces as new), `high_critical_count` set to 4, `note` updated. None of the 15 new IDs is added, because all are fixed rather than accepted.

## 5. Escalation Condition Check

The October sign-off's condition (3) asks for a prioritisation concern to be raised with the Head of Engineering if a third consecutive rescan triage is dominated by `react-scripts`-pinned findings without BLG-TECH-21 scheduled. All 3 new packages in this triage were fixable without the migration, so this record's proposed reading is that the condition is not met. BLG-TECH-21's Provisional-Target remains v10.0. The Cybersecurity & Trust Lead confirms or overrides this reading at sign-off.

## 6. Sign-off

- [x] All 3 newly-reported packages individually assessed
- [x] 3 fixed by a lockfile bump, verified via install, build and serve
- [x] Rescan analysis script reports `new_finding_count=0` post-fix
- [ ] Full PR CI passes, including Playwright E2E
- [ ] Escalation condition reading in §5 confirmed
- Signed off by: **Pending — Cybersecurity & Trust Lead**
- Date: Pending
