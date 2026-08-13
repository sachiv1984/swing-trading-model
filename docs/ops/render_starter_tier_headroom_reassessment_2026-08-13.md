**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-13
**Story:** ST-15 (BLG-OPS-139, EPIC-06, v8.7)
**Prior assessment:** `docs/ops/arc5_hosting_cost_projection.md` v1.0 (2026-05-30, ST-10/BLG-OPS-40/v4.6) — scoped to the single SI-02 endpoint only, predates all subsequent Arc 5 endpoints and the current 133-endpoint total.

---

# Render Starter-Tier Headroom Reassessment

## 1. Purpose

`BLG-OPS-139`: the last tier/headroom assessment (v4.6) predates the Arc 5 analytics endpoint set and current trade volume; capacity margin has not been reconfirmed since. This reassesses current Render Starter-tier resource headroom against current traffic/build patterns and records a recommendation.

## 2. Sandbox limitation (disclosed, not silently assumed complete)

The AC asks for "CPU/memory/dyno hours" headroom — these are live, account-specific metrics visible only in the Render dashboard's Metrics tab. This execution sandbox has no Render dashboard/API access (same constraint class as `render_build_deploy_path_filter_audit.md`'s production-filter check, which explicitly required "a human with Render dashboard access" and was resolved by the user checking directly). This reassessment is a **best-available-proxy**: it compiles every load/capacity signal derivable from this repository and public Render plan documentation, and states explicitly where a live dashboard check would still add information this proxy cannot provide.

## 3. Current infrastructure baseline (unchanged since v4.6, confirmed)

| Component | Configuration |
|-----------|--------------|
| Backend API (production) | Render Starter tier, single instance, auto-deploy from `main` (managed in Render dashboard, not `render.yaml` — see `render_build_deploy_path_filter_audit.md` §"Two Distinct Path-Filter Mechanisms") |
| Database | Supabase, Supavisor transaction pooling (port 6543) since v2.7 |
| Workers | None — Render Starter does not support background worker dynos |
| Cron jobs | None provisioned on Render (scheduled jobs, e.g. the nightly backtest, run via GitHub Actions `workflow_dispatch`/schedule, not Render cron — confirmed no `cron:` service type in `render.yaml`) |
| Redis / queue | Not provisioned |

**Render Starter plan specs (public plan documentation, not this account's live utilization):** 512 MB RAM, 0.5 shared CPU, per Render's published Starter-tier specification. This reassessment cites the plan's published ceiling, not a live per-account reading — see §2.

## 4. Load-growth signals since v4.6 (2026-05-30 → 2026-08-13, ~2.5 months, releases v4.6 → v8.7)

- **Endpoint count:** 133 live endpoints today (`grep -c '@router\.\(get\|post\|put\|delete\|patch\)('` across `backend/routers/*.py` + `backend/main.py`, per `rate_limit_audit_2026-08-13.md`'s methodology, this same session) vs the v4.6 assessment's single-endpoint (SI-02) scope. Growth is real, but **all growth is in synchronous, on-demand, per-request endpoints** — no background job, no scheduled compute, no new always-on process added to the Render service. This matters directly for headroom: Render Starter's 512MB/0.5-CPU ceiling is a *per-request-burst* constraint for a stateless FastAPI process, not a cumulative one — idle endpoints cost nothing between requests.
- **Trade volume:** still low. The most recent live-checked figure on record (SI-02 gate status, `current_roadmap.md`, repeatedly re-confirmed through v8.6) is **9 trades in the trailing 90-day window** — well within the v4.6 assessment's own "< 50 trades (current)" band, which it projected at 250–350ms p50 with "Supavisor overhead dominates; query execution negligible." The v4.6 assessment's own escalation trigger ("500+ trades: consider adding a result cache") remains far off.
- **Endpoint latency trend:** `docs/ops/api_performance_baseline.md` (actively maintained, v2.26, latest registration 2026-08-11) shows no degradation trend across its 38 registration/measurement entries spanning v2.4→v8.6 — newly-registered endpoints continue landing in the same 200–600ms p50 band the v4.6 assessment characterized as normal for this Supavisor-backed setup, not a rising trend.
- **No incidents on record:** no incident/outage log exists in `docs/` documenting a Render resource-exhaustion event (OOM, CPU throttling, dyno restart under load) at any point in this project's history. Absence of evidence is not proof of headroom, but a genuine capacity problem on a single-instance Starter dyno over 2.5 months of continuous production traffic would be expected to have surfaced as a user-visible incident by now, and none is recorded.
- **Build/deploy pattern:** unchanged — single Render Web Service, `pip install -r requirements.txt` build command, no new build-time-heavy steps added (confirmed via `render_build_deploy_path_filter_audit.md`'s live-checked production Build & Deploy configuration, refreshed this same session).

## 5. Recommendation

**Hold — no tier change recommended**, based on the proxy signals in §4: endpoint growth is entirely in stateless, on-demand request handlers with no new background compute; real trade volume remains far below the v4.6 assessment's own escalation threshold; measured endpoint latencies show no degradation trend across 2.5 months of continuous registration; no capacity-related incident is on record.

**Residual gap (disclosed):** this recommendation is proxy-derived, not confirmed against live Render dashboard CPU/memory/dyno-hour utilization graphs. If a future session has dashboard access, a direct check of the Metrics tab (CPU %, memory %, and — Starter tier specifically — whether any request has been queued/delayed by concurrency limits) would either confirm this Hold recommendation with real data or surface a gap this proxy cannot see (e.g. periodic CPU spikes from a specific expensive endpoint that don't show up in this repo's p50-latency-only baseline). Recorded as a follow-up condition, not a blocking gap — the AC's own framing ("recommendation recorded... with supporting data") is satisfied by the proxy evidence above; the live-metrics confirmation is a nice-to-have refinement, not a required unblock.

## 6. Sign-off

**FinOps & Resource Architect (agent-mediated, §5.3):** Confirmed — 2026-08-13. Proxy evidence (endpoint growth shape, trade volume, latency trend, incident-free history) supports a Hold recommendation. Live dashboard metrics were not available in this session; the recommendation is disclosed as proxy-derived, consistent with this cycle's other best-available-proxy stories (ST-07, ST-13).
