**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-30 (ST-39, BLG-OPS-85, EPIC-06, v9.14 — created: method, allocation rule and generator; monthly figures pending, BLG-OPS-201)
**Cycle:** 2026-10-29__release-v9.14 (ST-39)

---

# Cost by Feature Area

## 1. Purpose

No view partitioned the system's cost by feature area (BLG-OPS-85). This report does, monthly, for three areas: **AI endpoints**, the **screener** and **core CRUD**. It reads the per-call data `claude_audit_log` (BLG-OPS-74, v6.8) and `api_call_log` (BLG-OPS-19, v9.13) now provide, and states how the shared Render dyno's cost is allocated.

**Gate (verified at Release Planning, `run_manifest.md`, 2026-10-29):** `BLG-OPS-74` shipped in v6.8.

## 2. Feature Areas

`api_call_log.feature` holds the `<METHOD> <route template>` of the request that made each market-data call. `scripts/cost_by_feature_area.py` maps it to an area:

| Area | Routes | Notes |
|------|--------|-------|
| AI endpoints | `/ai/*`; `POST /trade-plans/generate-plan`; `POST /trade-plans/{plan_id}/generate-thesis`; `/reports/monthly-pnl/narrative`; `POST /trades/{trade_id}/debrief` | Every `claude_audit_log` row is in this area. Market-data calls these routes make (e.g. the daily briefing's prices) count here too. |
| Screener | `/screener/*`; `/ticker-universe/*` | Mostly the weeknight `POST /screener/run` batch. |
| Core CRUD | Every other route | Positions, portfolio, signals, trade plans, reports, settings, market, research, ops. |
| Unattributed | `feature = 'unattributed'` | Calls made outside a request (start-up, threads that did not copy the request context). Shown separately rather than guessed. |

## 3. Cost Sources

| Cost | Source | How it is split |
|------|--------|-----------------|
| Claude API | `claude_audit_log.cost_usd`, one row per call | Directly: all AI endpoints |
| Market-data providers | `api_call_log` rows × `UNIT_COST_USD` (`backend/utils/api_attribution.py`), one row per HTTP attempt | Directly, by the route's area. Every unit cost is $0 today (`data_pipeline_cost_baseline.md` §2), so this column shows volume until a provider charges. |
| Render production dyno | The month's invoice (Render reports no per-route usage) | Allocated (§4) |
| Supabase, GitHub Actions | — | Not allocated: Supabase is on the Free plan and Actions minutes are not billed for this public repository. Add a row if either starts charging. |

## 4. How the Shared Render Dyno Cost Is Allocated

The dyno is a fixed monthly charge: one Starter instance serves every feature, and using a feature less does not lower the bill. Allocating it is for visibility, to show which area the fixed spend mainly serves, not a marginal cost.

**Rule:** each area's share of the month's dyno charge equals its share of **work units**, where one work unit is one Claude call (`claude_audit_log` row) or one market-data call (`api_call_log` row).

**Why this proxy:** the dyno's work is mostly waiting on and processing outbound calls. Screener runs are bar fetches per ticker; AI requests wait on Claude; research views fan out to providers. Request counts and server time per route are not recorded anywhere, so these two per-call tables are the only per-feature measure of dyno work.

**What it misses:** routes that only read the database (most core CRUD reads) make no outbound call and get no share, so core CRUD is under-allocated. A Claude call and a market-data call weigh the same, though a Claude call holds the request open longer (`claude_audit_log.latency_ms` is reported alongside so the difference can be seen). If per-route request timing is ever recorded (BLG-OPS-209 adds it for the screener), switch the key to server time.

## 5. Producing the Monthly Table

Run against production (read-only; a single `SET TRANSACTION READ ONLY` session), with the dyno charge from that month's Render invoice (BLG-OPS-207):

```bash
DATABASE_URL=<production URL> python3 scripts/cost_by_feature_area.py --month 2026-11 --render-monthly-usd <invoice amount>
```

Paste the printed table into §6 under its month, with the date it was read. Months are UTC calendar months, and only complete months are recorded. `tests/test_cost_by_feature_area.py` covers the area mapping, the month bounds and the allocation.

## 6. Monthly Figures

**Pending.** The first complete month of production data is recorded under BLG-OPS-201 (post-merge: the production tables cannot be reached from CI or the governed environment). The table will take this form:

| Feature area | Claude calls | Claude cost | Market-data calls (failed) | Market-data cost | Work-unit share | Render dyno share | Total |
|--------------|-------------:|------------:|---------------------------:|-----------------:|----------------:|------------------:|------:|
| AI endpoints | — | — | — | — | — | — | — |
| Screener | — | — | — | — | — | — | — |
| Core CRUD | — | — | — | — | — | — | — |
| Unattributed (outside a request) | — | — | — | — | — | — | — |

## 7. Sign-Off

- [x] Report partitions cost by feature area (AI endpoints, screener, core CRUD) from `claude_audit_log` and the API-call attribution data (§2, §3, §5)
- [x] Shared Render dyno allocation stated (§4)
- [ ] Populated for at least one complete month of production data: post-merge, BLG-OPS-201
- Prepared by: Sprint Execution Engine (ST-39)
- Date: 2026-10-30
