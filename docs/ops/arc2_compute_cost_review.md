**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-30 (ST-38, BLG-OPS-21, EPIC-06, v9.14 — created)
**Cycle:** 2026-10-29__release-v9.14 (ST-38)

---

# Arc 2 Compute Cost Review

## 1. Purpose

Arc 2 added screener batch processing, research endpoints and AI-assisted trade plan features. No compute cost review had been done since Arc 1 (BLG-OPS-21). This review compares the cost of those three feature groups against a baseline, names the top 3 cost drivers, and files recommendations for the infrastructure the Arc 3 work, and everything after it, runs on.

**Gate (verified at Release Planning, `run_manifest.md`, 2026-10-29):** PT-04 (Setup Quality Score) shipped in v6.1, and the 30-day cost baseline item `BLG-OPS-18` shipped in v9.13 (`data_pipeline_cost_baseline.md`).

**On "Arc 3":** the roadmap's Arc 3 (In-Trade Risk Management, v3.3–v3.5) has long shipped. The recommendations in §6 apply to the shared production infrastructure that the Arc 3 features and every later arc run on, which is what an Arc 3 infrastructure decision means today.

## 2. Baseline Used

**No Arc 1 cost baseline exists.** Arc 1 (Stock Discovery & Screening) shipped in v2.9–v3.1. The repository's earliest cost records are later: `claude_cost_review_2026-05.md` (v4.1, 2026-05-28) and `arc5_hosting_cost_projection.md` (2026-05-30). No document records Render, database or market-data cost for the Arc 1 period, and production hosting is dashboard-managed, so none can be reconstructed from git history (`cloud_infra_spend_by_epic.md` §Known limitation).

This review therefore uses the **v9.13 baseline**, `data_pipeline_cost_baseline.md` (2026-10-27), together with the latest recorded figure for each other cost line:

| Cost line | Baseline | Source |
|-----------|----------|--------|
| Market data (Alpaca data, news, paper; Yahoo Finance) | $0.00 per week; every source is free at current use. Weekly call volume still pending | `data_pipeline_cost_baseline.md` §2, §4 |
| Render production API | Starter tier, one instance, flat; no plan change in the reviewed window. Dollar amount not recorded in the repository | `render_hosting_cost_trend_dashboard_2026-08-21.md` §4; `arc5_hosting_cost_projection.md` §2.1 |
| Supabase production database | Free plan (confirmed 2026-07-31); 16 MB on 2026-08-08 | `database_backup_disaster_recovery_runbook.md` §2; `cloud_infra_spend_by_epic.md` |
| Claude API | ~$0.0013 per call (Haiku 4.5); ~$0.05–$0.15 per month last confirmed (v5.6) | `anthropic_api_cost_trend_2026.md` §5.3; `ai_cost_threshold_review_2026-09-08.md` |
| GitHub Actions (schedulers, CI) | $0: the repository is public and Actions minutes are not billed | `ci_usage_reports/2026-08.md` |

## 3. Arc 2 Feature Groups

| Feature group | What runs | Where the compute happens | Variable cost |
|---------------|-----------|---------------------------|---------------|
| Screener batch | `POST /screener/run`, weeknights 22:00 UTC (`screener-refresh.yml`); fetches bars for each active ticker (Alpaca for US, Yahoo for UK and as US fallback) | Render dyno, one batch per weeknight; Supabase writes of results | Market-data calls: $0, but the largest call volume (`data_pipeline_cost_baseline.md` §4 expected shape) |
| Research endpoints | `GET /research/{ticker}`: one on-demand aggregation (signal, correlation, regime, sector, earnings, news, heat) | Render dyno, on demand | Market-data calls per view: $0 |
| AI-assisted plan features | `POST /trade-plans/generate-plan`, `POST /trade-plans/{plan_id}/generate-thesis` | Anthropic (Claude Haiku 4.5); the dyno waits on the call | Claude tokens, ~$0.0013 per call; logged per call in `claude_audit_log` |

## 4. Comparison Against the Baseline

| Cost line | Arc 2's share now | Change from baseline |
|-----------|-------------------|----------------------|
| Render dyno | All three groups run inline on the one Starter instance. The heaviest is the screener batch: `screener-refresh.yml` took 37s mean, 54s median and 80s maximum over 30 successful runs from 2026-09-18 to 2026-10-30 (workflow wall time, including runner start-up; the request is capped by `curl --max-time 120`). Research and plan generation are single on-demand requests (`GET /research/{ticker}` p95 target 3s, `api_performance_baseline.md`). | None. No tier change; nothing Arc 2 added needs an always-on process, a worker or a paid cron (the schedulers are GitHub Actions). |
| Market data | Screener batch dominates call volume; research adds per-view calls. | $0 throughout. Volume baseline still pending; quota (Alpaca 200 requests/minute) and Yahoo throttling, not price, are the limits. |
| Supabase | Arc 2 tables (trade plans, screener results, research session rows in `api_call_log`) are a small part of 16 MB. | No paid plan. Growth since 2026-08-08 unmeasured (BLG-OPS-208). |
| Claude API | Plan and thesis generation, per user action, gated by low trade volume. | Within the last confirmed ~$0.05–$0.15/month for all AI features. No fresh production reading from this environment. |

**Result:** Arc 2 added no new paid cost line. Its compute runs on the fixed-price Starter dyno, and its only variable dollar cost is Claude tokens for plan and thesis generation, at negligible volume.

## 5. Top 3 Cost Drivers

1. **The Render production dyno (fixed).** The only recurring paid line Arc 2 compute runs on. Every feature shares it, so its cost is fixed regardless of Arc 2 use, but it is the line any growth would eventually move (a tier upgrade). Its dollar amount is not recorded anywhere in the repository.
2. **The nightly screener batch (compute time and market-data volume).** The largest single job on the dyno, and the largest source of market-data calls. It costs $0 today, but it scales with the ticker universe, and both its server-side duration and its weekly call volume are unmeasured.
3. **Claude API calls from plan and thesis generation (variable).** The only per-use dollar cost Arc 2 adds. About $0.0013 per call; the $5/month model-tier review threshold would need about 3,800 calls a month (`anthropic_api_cost_trend_2026.md` §6.1).

## 6. Recommendations Filed

| # | Recommendation | Backlog item |
|--:|----------------|--------------|
| 1 | Record the production Render invoice each month, so the dyno, driver 1, has a dollar trend and ST-39's cost-by-feature-area report can allocate a real figure | BLG-OPS-207 |
| 2 | Re-run the production database storage snapshot quarterly: on Supabase's Free plan, storage is the database's limit, and there is one reading (16 MB, 2026-08-08) | BLG-OPS-208 |
| 3 | Log the nightly screener run's server-side duration and ticker count, so driver 2's dyno headroom can be tracked as the universe grows | BLG-OPS-209 |

Also standing, already filed: the weekly market-data volume baseline (delegated, `data_pipeline_cost_baseline.md` §4) and its automated 2× advisory (`BLG-OPS-195`).

**Infrastructure guidance (no item needed):** keep new scheduled or background work on the existing pattern, a GitHub Actions schedule calling an API route on the Starter dyno, as every scheduler in `scheduled_workflows_inventory.md` does. A feature that needs an always-on process, a worker or a paid cron is a hosting cost decision and should be priced at design time.

## 7. Sign-Off

- [x] Arc 2 compute cost comparison for screener batch, research endpoints and AI-assisted plan features (§3, §4)
- [x] No Arc 1 baseline exists; stated, and the v9.13 baseline used instead (§2)
- [x] Top 3 cost drivers named (§5)
- [x] Recommendations filed as backlog items (§6: BLG-OPS-207, BLG-OPS-208, BLG-OPS-209)
- [x] Gate verified at Release Planning (`run_manifest.md`, 2026-10-29)
- Prepared by: Sprint Execution Engine (ST-38)
- Date: 2026-10-30
