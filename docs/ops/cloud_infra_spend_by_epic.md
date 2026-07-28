Owner: FinOps & Resource Architect
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-27
Story: ST-12 (BLG-OPS-120, EPIC-12, v7.9)

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

## Maintenance

Update the "Resources defined in this repository" table whenever `render.yaml` changes materially (new service, plan-tier change) — add a row or extend the "Notable changes by EPIC" column citing the commit and EPIC/ST ID, the same way `git log --follow -- render.yaml` was used to reconstruct the table above.
