**Owner:** Head of UX & Design
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-05
**Cycle:** 2026-05-05__release-v3.2
**Approved by:** Product Owner — 2026-05-05
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Backlog source:** BLG-FE-22

---

# UX Spec — Screener-to-Research Navigation & Morning Routine Workflow (ST-04 / BLG-FE-22)

## Purpose

This document defines the UX workflow for navigating from screener results and watchlist entries to the Pre-Trade Research View. It answers the BLG-FE-22 questions: how users navigate from screener discovery to research, what context carries between screens, and how the morning routine flows across Arc 1→Arc 2 surfaces.

It is the authoritative design source for the navigation integration changes in `docs/specs/frontend/pages/screener_results.md` and `docs/specs/frontend/pages/watchlist.md`.

---

## Morning Routine Workflow

The standard Arc 1→Arc 2 morning workflow:

```
1. Screener Results (/screener)
   → Review tickers passing strategy gates
   → Option A: "Add to Watchlist" (existing DS-07 flow)
   → Option B: "Research" → Research View for direct inspection

2. Research View (/research/{ticker})
   → Inspect momentum, ATR, price, news
   → Check prospective heat at entry
   → Review or create trade plan

3. Watchlist (/watchlist)
   → Monitor shortlisted candidates
   → "Research" → Research View for deeper review before entry
   → "Add to Position" (existing flow)
```

---

## Navigation Integration Design

### Screener Results: Research Entry Point (ST-04)

Add a **"Research"** action per ticker row in the screener results table.

| Attribute | Specification |
|-----------|---------------|
| Label | "Research" |
| Type | Text link or secondary button (consistent with existing "Add to Watchlist" treatment) |
| Placement | Actions column per row, adjacent to "Add to Watchlist" |
| Target | `/research/{ticker}` where `{ticker}` is the row's ticker symbol |
| Context carry | None — the research view fetches its own data from the API; no state is passed in the URL beyond the ticker |

**Back navigation:** User clicking `← Back` in the research view returns to `/screener` via browser back. No custom scroll-position restoration required; acceptable UX at current volume (screener results are short lists).

### Watchlist: Research Entry Point (ST-04)

Add a **"Research"** action per ticker entry in the watchlist table.

| Attribute | Specification |
|-----------|---------------|
| Label | "Research" |
| Type | Text link or secondary button (consistent with existing "Add to Position" treatment) |
| Placement | Actions column per row, adjacent to "Add to Position" |
| Target | `/research/{ticker}` where `{ticker}` is the watchlist entry's ticker symbol |
| Context carry | None |

**Back navigation:** User clicking `← Back` in the research view returns to `/watchlist` via browser back.

---

## Information Carry Decisions

| Information | Carry to research view? | Rationale |
|------------|------------------------|-----------|
| Ticker symbol | Yes (in URL path) | Required to fetch research data |
| Market (UK/US) | No | Research API returns market in response |
| Signal score | No | Research API returns current signal status |
| Screener entry price | No | Research API returns current price |
| Watchlist target entry | No | Research view is for current research, not pre-set targets |

**Decision rationale:** The research view fetches fresh data from `GET /research/{ticker}`. Passing stale screener prices would create inconsistency. The ticker in the URL is sufficient context.

---

## URL Model

- Research view URL: `/research/{ticker}` (e.g. `/research/AAPL`, `/research/BARC.L`)
- Ticker is in the path (not query param) — shareable and bookmarkable
- UK tickers use the `.L` suffix in the path (matches backend ticker format)

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| "Research" alongside "Add to Watchlist" on screener | Both are discovery→next-step actions; placing together creates a clear action set per candidate |
| No context state passed to research view | Research view is self-sufficient; avoids stale data from screener run |
| Browser back for return navigation | Simple and reliable at current list sizes; avoids scroll-position complexity |
| "Research" alongside "Add to Position" on watchlist | Natural progression: watchlist is the candidate holding area before research or entry |

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-05 | Initial design gate artefact for v3.2 ST-04, fulfilling BLG-FE-22. Approved by Product Owner 2026-05-05. |
