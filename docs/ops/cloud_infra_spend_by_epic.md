Owner: FinOps & Resource Architect
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-08
Story: ST-23 (BLG-OPS-123, EPIC-05, v8.4) — storage-growth trend view added; ST-12 (BLG-OPS-120, EPIC-12, v7.9) — original cost-tag report

# Cloud Infrastructure Spend Attribution by EPIC

> **This report covers $0/month staging resources only — it does not attribute actual (paid, production) spend to any EPIC.** Production runs on Render's Starter tier (paid) per `docs/ops/arc5_hosting_cost_projection.md`, but production services have no git history in this repo (dashboard-managed) and are therefore out of this report's scope — see § "Known limitation". Do not read this document as "cost attribution solved."

## Purpose

`roadmap_prompt.md` STEP 7.1's Skill-Silo workforce economics reasons about story counts only — no cloud infrastructure cost signal feeds into that same picture. This document is the per-EPIC spend attribution report this gap calls for.

## Finding: Render has no native resource-tagging or per-tag cost breakdown (AC-01 reframed)

Sprint planning's premise for this story ("`render.yaml` supports config-level tagging in-repo") does not hold. Verified against Render's own Blueprint spec documentation:

- The Blueprint YAML spec (`render.yaml`) has **no `tags` field** on services, databases, or environment groups — confirmed against the current Blueprint reference.
- Render's Blueprint spec does support a `projects:` / `environments:` grouping construct (services nested under `projects[].environments[]` instead of at the root level), but this is a **deploy-topology** construct — Render's own docs describe it purely in terms of organisational grouping and environment-specific access/traffic controls, not cost or billing visibility. Render's billing documentation does not mention cost breakdown by project, environment, or any custom label.
- **Restructuring `render.yaml` to nest services under `projects:` was considered and rejected here.** This project's services are currently defined at the root level; Render's own docs note that root-level services "keep their currently assigned environment" across syncs, meaning moving them into a `projects:` block is a live deploy-topology change, not a label-only edit. Taking on that risk for a P3 reporting nice-to-have is disproportionate — if this is worth doing later, it should be its own story with its own design-gate/deploy-verification pass, not folded into a cost-attribution report.

**AC-01 ("Cost tags applied") is therefore not achievable as literally specified — Render has no mechanism to apply cost tags to, whether via `render.yaml` or otherwise.** The closest available substitute, applied below, is a manually-maintained EPIC-attribution mapping derived from git history against `render.yaml` (the only cloud-resource definition tracked in this repository) — see § "Known limitation" for what this does not cover.

## Per-EPIC spend attribution (AC-02 — summary report)

### Resources defined in this repository (`render.yaml` — staging only)

| Resource | Type | Plan | Introduced by | Notable changes by EPIC |
|----------|------|------|----------------|---------------------------|
| `trading-assistant-api-staging` | Web Service (Python/FastAPI) | Free | EPIC-01 (`1bcd4897`, "Provision staging environment infrastructure") | EPIC-02: alert delivery iterated 3 times (Resend → Gmail SMTP → Brevo → Telegram) and a cron job added then replaced with a GitHub Actions scheduled workflow (`43d4adb1`, `66e0858a`) — no plan-tier change, same free-tier service throughout |
| `trading-assistant-staging` | Static Site (React) | Free (no `plan` field — confirmed not applicable to static sites, `c1b8830d`) | EPIC-01 (`1bcd4897`) | No further EPIC changes found in `render.yaml` history |

Both staging resources are on Render's free tier — **$0/month attributable spend** for everything this repository's `render.yaml` actually provisions.

### Resources not defined in this repository (production)

Per `render.yaml`'s own header comment: "Production services are managed separately in the Render dashboard — this file only defines staging." Production is where actual paid spend lives (`docs/ops/arc5_hosting_cost_projection.md` records the backend API on Render's **Starter** tier, a paid plan), but:

- Production services have no git history in this repository — there is no version-controlled record of which EPIC provisioned or resized them.
- Render's dashboard is the only source of truth for production plan tier and actual dollar spend; this document cannot reproduce that from repo state alone.

**Known limitation:** this report attributes spend for the two resources this repository actually defines and tracks (both $0/month). It does not — and cannot, from repo state alone — attribute the paid production spend to individual EPICs. If per-EPIC production cost attribution becomes a genuine planning need (not just a nice-to-have), the Infrastructure & Operations Owner or FinOps & Resource Architect would need to periodically cross-reference Render's dashboard/invoice against the deployment history (e.g. `docs/product/changelog.md` release entries), since Render itself provides no tag-based mechanism to automate this.

## Database Storage Growth Trend (ST-23, BLG-OPS-123, EPIC-05, v8.4)

**Purpose:** database storage is a cost driver that scales with trade/journal history volume, independent of the Render service-tier spend tracked above. This section adds a simple size-over-time trend view alongside the existing cost-tag reporting, per this story's scope.

**Method:** `pg_database_size(current_database())` and `pg_total_relation_size()` per table, queried directly against production via the `PROD_DATABASE_URL` secret — same auth pattern already established by `production-db-backup.yml` (`BLG-OPS-127`, v8.2). Reusable workflow: `.github/workflows/db-storage-size-snapshot.yml` (`workflow_dispatch`, read-only queries only — no writes, no relation to the backup workflow's dump/restore behaviour).

**First snapshot — 2026-08-08T09:28:57Z:**

| Metric | Value |
|--------|-------|
| Total database size | 16 MB (16,321,683 bytes) |

**Top 10 tables by size:**

| Table | Size |
|-------|------|
| `screener_results` | 440 kB |
| `backtest_trades` | 360 kB |
| `alert_evaluations` | 296 kB |
| `signals` | 256 kB |
| `ticker_universe` | 232 kB |
| `notifications` | 208 kB |
| `trade_history` | 192 kB |
| `tickers` | 184 kB |
| `pre_entry_validation_log` | 176 kB |
| `positions` | 168 kB |

**Row counts for the volume-scaling tables named in this story's problem statement:**

| Table | Rows |
|-------|------|
| `trade_history` | 21 |
| `signals` | 389 |
| `trade_plans` | 13 |

**Trend note:** this is the first recorded snapshot — a single point establishes the tracking mechanism and baseline, not yet a multi-point trend. The workflow is deliberately kept as a reusable, re-runnable tool (not a one-off) so that re-running it periodically (e.g. alongside a future backlog/grooming cycle, or on a schedule if growth monitoring becomes a higher priority) builds the actual trend over time from this baseline. At 16 MB total with the two fastest-growing tables (`trade_history` 21 rows, `signals` 389 rows) both well under any Supabase free-tier storage concern, there is no cost signal here warranting closer monitoring cadence today — noted for context, not as a recommendation to add scheduling now.

## Maintenance

Update the "Resources defined in this repository" table whenever `render.yaml` changes materially (new service, plan-tier change) — add a row or extend the "Notable changes by EPIC" column citing the commit and EPIC/ST ID, the same way `git log --follow -- render.yaml` was used to reconstruct the table above.

Re-run `.github/workflows/db-storage-size-snapshot.yml` periodically and append a new snapshot row/date to the "Database Storage Growth Trend" section above to extend the trend.

## Sign-Off — ST-23 (BLG-OPS-123)

```
AC-01: Simple storage-growth trend view (size over time) added alongside
       the existing cost-tag reporting. ✅ PASS — "Database Storage Growth
       Trend" section above, with a real first snapshot (16 MB total,
       queried directly against production) and a reusable workflow for
       future snapshots to extend the trend.
AC-02: FinOps & Resource Architect sign-off. ✅ this block.

Signed: [x] Infrastructure & Operations Owner (agent-mediated, §5.3) — 2026-08-08
Signed: [x] FinOps & Resource Architect (agent-mediated, §5.3) — 2026-08-08
```
