---
**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Frontend Specification (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-11
**Story:** ST-15 (BLG-FE-09, v2.6 EPIC-04)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
---

# Frontend Performance Budget

---

## 1. Purpose

This document defines maximum acceptable performance targets for the frontend application. It exists to give the Director of Quality a concrete reference when evaluating frontend PRs and to ensure that successive feature additions do not silently erode page load time or bundle size.

These targets are documentation only. No automated instrumentation or CI enforcement is in scope for this version. Measurement is performed manually using the methods described in §4.

---

## 2. Relationship to API Latency Baseline (BLG-OPS-05)

The frontend performance budget must account for the known backend latency floor established in `docs/ops/api_performance_baseline.md` (v1.1, BLG-OPS-05). Key observed figures from the staging baseline:

| Endpoint category | Observed p95 (staging) |
|-------------------|------------------------|
| Fast (GET /, unauthenticated) | ~450ms |
| Standard data endpoints (trades, signals, settings) | 1,300–2,800ms |
| Heavy endpoints (portfolio, positions) | 4,600–6,200ms |

**Implication for frontend budgets:** Total time-to-interactive on data-dependent pages must budget for 1–6 seconds of backend response time before any frontend rendering overhead. Frontend targets below are stated as _rendering overhead budgets_ — the frontend's share of total load time, not including network and API latency.

---

## 3. Performance Targets

### 3.1 Initial Page Load (First Contentful Paint — FCP)

Measured on a locally-served production build (`npm run build` + `serve -s build`), on a modern desktop browser, with no throttling.

| Target | Value |
|--------|-------|
| FCP (first contentful paint) | ≤ 1,500ms |
| LCP (largest contentful paint) | ≤ 2,500ms |
| Time to interactive (TTI) | ≤ 3,000ms |

These are the frontend-only targets. On staging, the actual user-experienced load time will be higher by the API latency floor (see §2).

### 3.2 Route Transitions (Client-Side Navigation)

After initial load, switching between pages (e.g. Dashboard → Trade History → Signals) is client-side only. Targets:

| Target | Value |
|--------|-------|
| Route transition (skeleton visible) | ≤ 200ms |
| Route transition (data loaded — dependent on API) | API latency floor + ≤ 200ms frontend overhead |

### 3.3 JavaScript Bundle Size

Measured from the `build/static/js/` output of `npm run build`.

| Bundle | Maximum size (gzipped) |
|--------|----------------------|
| Main bundle (`main.*.js`) | ≤ 200 KB |
| Per code-split chunk | ≤ 80 KB |
| Total JS (all chunks, gzipped) | ≤ 500 KB |

**Current baseline (v2.6, approximate — establish at first measurement):** TBD. The DoQ should record the baseline reading at the first measurement after v2.6 ships and track any growth per release.

### 3.4 Regression Threshold

A PR that increases total gzipped JS by more than **10 KB** relative to main must include a brief note in the PR description explaining the size increase. This is a documentation requirement only — it does not block merge.

---

## 4. Measurement Methodology

### 4.1 Bundle Size

```bash
npm run build
# After build completes:
ls -lh build/static/js/
# Or for gzip sizes:
for f in build/static/js/*.js; do
  echo -n "$f: "; gzip -c "$f" | wc -c; done
```

Record the gzipped sizes of each chunk. Sum for total.

### 4.2 Load Performance (Lighthouse)

1. Run a production build locally: `npm run build && npx serve -s build -l 3000`
2. Open Chrome DevTools → Lighthouse tab
3. Select "Performance" category only
4. Set device to "Desktop"
5. Run — note FCP, LCP, and TTI scores

Alternatively, use the Lighthouse CLI:

```bash
npx lighthouse http://localhost:3000 --only-categories=performance --output=json --output-path=lighthouse_report.json
```

### 4.3 When to Measure

- **Before and after any EPIC that adds a new page or major component** (compare bundle size delta)
- **At the start of each release cycle** (establish baseline for that cycle)
- **Whenever DoQ needs to sign off on a PR with significant new frontend code**

No automated measurement is required. Manual measurement on demand is sufficient at this stage.

---

## 5. Scope Limitations

- These targets apply to the React frontend served from `src/`.
- No backend or API performance targets are defined here — those are in `docs/ops/api_performance_baseline.md`.
- No mobile performance targets are defined in this version (the app targets desktop trading use).
- No CI enforcement of these targets is in scope for this document. A future backlog item may add Lighthouse CI or bundle size CI gates.

---

## 6. Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-11 | Initial version — ST-15 (BLG-FE-09, v2.6 EPIC-04). Page load targets (FCP ≤ 1,500ms, LCP ≤ 2,500ms, TTI ≤ 3,000ms), bundle size targets (main ≤ 200KB gzip, total ≤ 500KB gzip), route transition overhead ≤ 200ms. Aligned to BLG-OPS-05 API latency baseline (staging p95 1,300–6,200ms floor documented). |
