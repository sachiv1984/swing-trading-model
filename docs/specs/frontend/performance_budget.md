---
**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Frontend Specification (Class 2)
**Status:** Active
**Version:** 2.0
**Last Updated:** 2026-11-19 (ST-06, EPIC-01, v9.18, BLG-QA-271 — Core Web Vitals targets on mobile and desktop, TTI dropped, Lighthouse CI and bundle-size check, web-vitals reporting, first baseline); prior — 2026-04-11 (ST-15, BLG-FE-09, v2.6 — initial version); prior history retained — see prior entries in version control
**Story:** ST-06 (BLG-QA-271, v9.18 EPIC-01); originally ST-15 (BLG-FE-09, v2.6 EPIC-04)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
---

# Frontend Performance Budget

---

## 1. Purpose

This document defines the frontend's performance targets, how they are measured, and the measured baseline. It gives the Director of Quality a concrete reference when evaluating frontend PRs, and it is the before-picture for Phase 4 stage 4's speed work (`BLG-FE-315`, `BLG-FE-316`, `BLG-FE-317`, v9.19).

Since v2.0 (ST-06, v9.18) the targets are Google's Core Web Vitals, measured in CI on every PR on a mobile and a desktop profile, and reported in the field by the app itself.

---

## 2. Relationship to API Latency Baseline (BLG-OPS-05)

The frontend performance budget must account for the known backend latency floor established in `docs/ops/api_performance_baseline.md` (v1.1, BLG-OPS-05). Key observed figures from the staging baseline:

| Endpoint category | Observed p95 (staging) |
|-------------------|------------------------|
| Fast (GET /, unauthenticated) | ~450ms |
| Standard data endpoints (trades, signals, settings) | 1,300–2,800ms |
| Heavy endpoints (portfolio, positions) | 4,600–6,200ms |

**Implication for frontend budgets:** the lab measurements in §4.2 answer the API instantly from a mock, so they measure the frontend's own cost (download, parse, render). Real users add the API latency floor above on data-dependent content. Field values (§4.3) include it.

---

## 3. Performance Targets

### 3.1 Core Web Vitals (v2.0)

Targets are the Core Web Vitals "good" thresholds. They are judged on the CI lab values (§4.1) on both profiles in §3.2. Field values (§4.3) are for inspecting one session in the browser; nothing collects them, so no field percentile is claimed.

| Metric | Target | Lab measurement (CI) | Field measurement |
|--------|--------|----------------------|-------------------|
| LCP (largest contentful paint) | ≤ 2,500 ms | Lighthouse LCP | `web-vitals` `onLCP` |
| INP (interaction to next paint) | ≤ 200 ms | Not measurable without interactions; **Total Blocking Time** is the lab proxy, against Lighthouse's own "good" TBT: ≤ 200 ms mobile, ≤ 150 ms desktop | `web-vitals` `onINP` |
| CLS (cumulative layout shift) | ≤ 0.1 | Lighthouse CLS | `web-vitals` `onCLS` |

FCP and Speed Index are reported for context, with no target. **TTI is dropped:** Lighthouse no longer reports it (v1.0's TTI ≤ 3,000 ms target is withdrawn).

### 3.2 Profiles

| Profile | Lighthouse setting | Represents |
|---------|-------------------|------------|
| Mobile | Lighthouse default: Moto G Power emulation, simulated slow 4G, 4× CPU slowdown | A phone on a typical connection |
| Desktop | `desktop-config.js`: 1350×940, simulated fast connection, no CPU slowdown | The primary trading-desk use |

v1.0 targeted an unthrottled desktop only; the mobile profile is new in v2.0.

### 3.3 JavaScript Bundle Size

Measured from `build/static/js/*.js`, gzip level 9, 1 KB = 1,024 bytes.

| Bundle | Maximum size (gzipped) |
|--------|----------------------|
| Main bundle (`main.*.js`) | ≤ 200 KB |
| Per code-split chunk | ≤ 80 KB |
| Total JS (all chunks, gzipped) | ≤ 500 KB |

Unchanged from v1.0. The baseline (§5) is a single, unsplit main bundle over both the main and the total budget.

### 3.4 Route Transitions (Client-Side Navigation)

Unchanged from v1.0: route transition to a visible skeleton ≤ 200 ms; with data, API latency floor + ≤ 200 ms frontend overhead. Not measured automatically.

### 3.5 Enforcement

**Report only.** CI reports every value on every PR (§4.1) and marks those over target, but does not fail the PR on a budget miss: the current bundle and several lab values are over target, and Phase 4 stage 4 is the planned fix. Once that work lands, the Director of Quality may turn on enforcement (`check_bundle_size.py --enforce`, and a Lighthouse threshold) in a later story.

**Regression note (from v1.0):** a PR that increases total gzipped JS by more than **10 KB** relative to `main` explains the increase in its PR description. Compare its bundle table with the latest `main` run.

---

## 4. Measurement Methodology

### 4.1 CI: Lighthouse and bundle size on every PR

Workflow: `.github/workflows/lighthouse-ci.yml` (job "Lighthouse (mobile + desktop) and bundle size"), on every pull request to `main` that changes anything the build or the measurement reads (`package*.json`, `src/**`, `public/**`, `scripts/perf/**`, the workflow), and on pushes to `exec/**` branches with the same paths. A push and its PR share one concurrency group, so a change runs once. A backend- or docs-only PR cannot move these values and does not run it.

1. Builds the app with `REACT_APP_API_URL=http://localhost:4173/api` and fake auth.
2. `scripts/perf/check_bundle_size.py` reports §3.3.
3. `scripts/perf/mock_api_server.js` serves the build and a populated mock API on one origin (the app's Content-Security-Policy allows `connect-src 'self'` and `https:` only, so a mock on another port would be blocked).
4. `scripts/perf/run_lighthouse.mjs` (Lighthouse 13.6.0) runs Dashboard (`/#/DashboardHome`), Positions (`/#/Positions`), Trade Plan (`/#/TradePlan`) and Performance (`/#/Performance`) on both profiles, 3 runs each, and reports the median of each metric.
5. Both tables go to the job summary of the run; the raw Lighthouse JSON is the `lighthouse-results-<run id>` artifact (14 days).

### 4.2 Locally

```bash
BUILD_PATH=build-perf CI=false PUBLIC_URL=/ REACT_APP_API_URL=http://localhost:4173/api \
  REACT_APP_DEV_FAKE_AUTH=true DISABLE_ESLINT_PLUGIN=true GENERATE_SOURCEMAP=false npm run build
python3 scripts/perf/check_bundle_size.py build-perf
node scripts/perf/mock_api_server.js --port 4173 --static build-perf &
# in a directory with `npm install lighthouse@13.6.0`, copy scripts/perf/run_lighthouse.mjs there, then:
node run_lighthouse.mjs --base http://localhost:4173 --runs 3
```

Local numbers vary with the machine; compare like with like, and use the CI run for the record.

### 4.3 Field reporting (`web-vitals`)

`src/lib/reportWebVitals.js` (called from `src/index.js`) uses `web-vitals` 6.2.3 to record LCP, INP, CLS, FCP and TTFB. Every change to each value is reported (`reportAllChanges`), and the latest value with its rating is kept on `window.__WEB_VITALS__`; in development each is also logged to the console (`[web-vitals] LCP 1235 ms (good)`). Nothing is sent over the network: there is no analytics endpoint, so these are per-session values for inspection, not a field dataset.

### 4.4 When to Measure

- Every PR (automatic, §4.1).
- Record a new baseline (§5) after any change meant to move these numbers, and at least once per release that changes the frontend substantially.

---

## 5. Baseline

*Pending: the first `lighthouse-ci.yml` run on the ST-06 commit records the baseline here (next revision of this section, same story).*

---

## 6. Scope Limitations

- These targets apply to the React frontend served from `src/`.
- No backend or API performance targets are defined here — those are in `docs/ops/api_performance_baseline.md`.
- Lab runs use a mock API with a fixed, small data set; pages with much more data (a long trade history) can be slower in real use.
- The bundle check sees JavaScript only, not CSS, images or fonts.

---

## 7. Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.0 | 2026-11-19 | ST-06 (BLG-QA-271, v9.18 EPIC-01). Targets become Core Web Vitals (LCP ≤ 2.5 s, INP ≤ 200 ms with TBT ≤ 200/150 ms mobile/desktop as the lab proxy, CLS ≤ 0.1) on a mobile and a desktop profile; TTI and the FCP target dropped. New CI workflow `lighthouse-ci.yml` runs Lighthouse (4 pages × 2 profiles) and the bundle-size check on every PR and reports the values (report only, §3.5). `web-vitals` field reporting added. Dated baseline in §5 from the first CI run, measured before ST-08 (BLG-QA-274). |
| 1.0 | 2026-04-11 | Initial version — ST-15 (BLG-FE-09, v2.6 EPIC-04). Page load targets (FCP ≤ 1,500ms, LCP ≤ 2,500ms, TTI ≤ 3,000ms), bundle size targets (main ≤ 200KB gzip, total ≤ 500KB gzip), route transition overhead ≤ 200ms. Aligned to BLG-OPS-05 API latency baseline (staging p95 1,300–6,200ms floor documented). |
