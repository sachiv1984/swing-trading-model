---
**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Date:** 2026-04-02
**Story:** ST-10 (BLG-OPS-10) — Render hosting tier review and decision record
**Cycle:** 2026-03-31__release-v2.4
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
---

# Render Hosting Tier Review — v2.4 Decision Record

---

## 1. Review Scope

This document records the FinOps & Resource Architect assessment of the Render hosting
tier against the scheduling and compute workload of the application as of v2.4. Triggered
by BLG-OPS-10: one full sprint cycle (v2.3) of alert scheduling has elapsed with no
documented capacity review.

---

## 2. Current Hosting Configuration

### 2.1 Render Services

| Service | Type | Tier | Notes |
|---------|------|------|-------|
| `trading-assistant-api-staging` | Web Service | **Free** | Defined in `render.yaml` |
| `trading-assistant-staging` (frontend) | Static Site | **Free** | Defined in `render.yaml` |
| Production API | Web Service | **Unknown — managed in Render dashboard** | Not in `render.yaml`; requires dashboard confirmation |
| Production Frontend | Static Site | Unknown | Not in `render.yaml` |
| Render Cron | Cron Job | **Not used** | See §3 |

> **Action for Infrastructure & Operations Owner:** Confirm production Render web service
> tier in the Render dashboard. If on a paid tier, record the tier name and monthly cost
> below. If on free tier, this review's conclusion applies to production as well.
>
> Production tier confirmed: _________________ Cost: _________________

### 2.2 Render Free Tier Limits (Web Service)

| Limit | Free Tier Value |
|-------|----------------|
| RAM | 512 MB |
| CPU | 0.1 CPU (shared) |
| Spin-down after inactivity | 15 minutes |
| Cold start delay | ~50–60 seconds |
| Bandwidth | 100 GB/month |
| Build minutes | 500/month |

---

## 3. Scheduling Workload Assessment

### 3.1 Alert Evaluation Cron

The delegation record (DEL-20260401-03) assumed Render cron would be required for the
alert evaluation workload. **This assumption is incorrect.**

`render.yaml` §"Alert Evaluation Cron" explicitly documents:

> *"Render cron requires paid tier. Trigger mechanism: GitHub Actions scheduled workflow.
> See `.github/workflows/alert-evaluation.yml` — runs 21:30 UTC Mon–Fri."*

**The alert evaluation cron runs entirely on GitHub Actions, not Render.** Architecture
decision was made at BLG-OPS-04 implementation time (v2.2). Render has zero scheduling
workload from this feature.

**GitHub Actions usage for alert evaluation:**

| Parameter | Value |
|-----------|-------|
| Schedule | 21:30 UTC Mon–Fri (weekdays only) |
| Runs per month | ~21 |
| Execution time per run | ~30 seconds (curl to POST /alerts/evaluate) |
| GitHub Actions minutes consumed | ~11 minutes/month |
| Free tier allowance (private repo) | 2,000 minutes/month |
| Utilisation | **< 1%** |

**Verdict: No Render cron cost or capacity concern. GitHub Actions free tier is
consuming < 1% of its monthly allowance for alert evaluation.**

### 3.2 Weekly Digest (ST-08)

`GET /digest/weekly` is a **synchronous, on-demand endpoint**. It is called by the
frontend when the user navigates to the Weekly Digest page. There is no scheduled
or background component. Zero scheduling burden on Render or GitHub Actions.

### 3.3 Render Web Service — Cold Start Impact on Cron

One operational observation (not a cost concern, flagged for InfraOps):

The GitHub Actions workflow calls `POST /alerts/evaluate` at 21:30 UTC. If the Render
web service has been idle and spun down, this call triggers a ~50–60s cold start before
the request is served. The `curl` command in the workflow has no explicit `--max-time`
flag — a cold start will not cause a timeout failure (curl default is no timeout), but
the job will appear to hang for ~60s before completing.

**Operational risk:** Low. The alert evaluation endpoint itself is lightweight. The cold
start is a latency issue only, not a reliability issue. Alert evaluation will complete
successfully after warm-up.

**Recommendation:** Add `--max-time 120` to the curl command in
`.github/workflows/alert-evaluation.yml` to make the timeout explicit. File as a
low-priority backlog item (P4) rather than blocking v2.4.

---

## 4. Decision

**Decision: Free tier is sufficient. No paid tier warranted.**

**Rationale:**

1. Scheduling workload is on GitHub Actions, not Render — Render has zero cron load.
2. The weekly digest feature adds no scheduled compute — it is purely on-demand.
3. GitHub Actions alert evaluation consumes < 1% of the free tier minute allowance.
4. Render web service free tier (512MB RAM, 0.1 CPU) is adequate for current single-user
   workload. Cold starts are an accepted latency trade-off, not a reliability failure.
5. No evidence of CPU, memory, or bandwidth pressure from v2.3 sprint cycle.

**Monitor criteria (review at v2.5 sprint planning):**

- If production Render tier is confirmed paid: record actual cost and assess value
- If alert rule complexity increases and evaluation time exceeds 90s: reassess cold start risk
- If daily active users expand beyond single-user: reassess 512MB RAM ceiling
- If GitHub Actions private repo minutes approach 1,000/month: evaluate cron frequency

**Follow-up backlog item filed:** None required at this time. The cold start curl timeout
observation is a P4 operational improvement — not a cost concern and not blocking release.
It will be raised as a standard backlog addition if the InfraOps Owner agrees.

---

## 5. Sign-Off

```
FinOps & Resource Architect
Date: 2026-04-02
Finding: Free tier sufficient. No paid tier warranted.
Rationale summary: Render cron is not in use — scheduling runs on GitHub Actions free
tier at < 1% utilisation. Weekly digest is on-demand. No cost pressure observed.

Signed: [x] FinOps & Resource Architect — 2026-04-02
```

```
Infrastructure & Operations Owner
Date: ___________
Production tier confirmed: ___________
Cold start impact on alert eval acknowledged: [ ] Yes
Decision concurrence: [ ] Agree — free tier sufficient
                      [ ] Disagree — see attached rationale

Signed: [ ] Infrastructure & Operations Owner — ___________
```

---

## 6. Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-04-02 | FinOps & Resource Architect | Initial decision record |
