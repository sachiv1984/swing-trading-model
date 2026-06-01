**Owner:** FinOps & Resource Architect
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-01
**Cycle:** 2026-06-01__release-v4.8 (ST-04 — BLG-OPS-46)

---

# Render Build Minutes Monitoring Policy

## 1. Background

On 2026-05-31, Render CI build minutes were exhausted mid-sprint during v4.6/v4.7 double-capacity cycles, blocking all deploys until the billing cycle reset. This policy establishes monitoring thresholds and operational controls to prevent recurrence.

---

## 2. Monthly Allocation

| Plan | Monthly Allocation | Billing Cycle Reset |
|------|-------------------|---------------------|
| Render Starter (current) | 400 minutes/month | 1st of each calendar month |

**Note:** The exact plan and allocation should be verified against the Render dashboard at `dashboard.render.com` → Account → Billing. The 400-minute figure is the Render Starter plan default as of 2026. If the team has upgraded to a higher plan, update this table accordingly.

---

## 3. Historical Consumption (v4.6–v4.7)

| Cycle | Sprint dates | Estimated build minutes consumed | Notes |
|-------|-------------|----------------------------------|-------|
| v4.6 (2026-05-30–31) | 2026-05-30 to 2026-05-31 | ~180–220 min (estimated) | Double-capacity sprint; 4 EPICs; 22 stories merged |
| v4.7 (2026-05-31) | 2026-05-31 | ~40–60 min (estimated) | 8 stories; 4 EPICs; minutes exhausted during this cycle |
| **Combined v4.6+v4.7** | 2026-05-30 to 2026-05-31 | **~400+ min** | Exhaustion event occurred on 2026-05-31 |

**Root cause:** Two consecutive release cycles (v4.6 + v4.7) were executed within a single billing month. v4.6 was a double-capacity sprint (22 stories, 4 EPICs). Combined builds exhausted the monthly 400-minute allocation.

---

## 4. Early-Warning Threshold

**80% threshold:** When cumulative build minutes in the current billing month reach **320 minutes** (80% of 400-minute allocation), the following actions are triggered:

| Action | Owner | SLA |
|--------|-------|-----|
| Alert FinOps & Resource Architect | Infrastructure & Operations Owner | Same day |
| Review remaining sprint activity and estimated build count | FinOps & Resource Architect | 24 hours |
| Consider plan upgrade if mid-sprint exhaustion risk is HIGH | FinOps & Resource Architect + Product Owner | 24 hours |

**Monitoring method:** Check Render dashboard → Account → Billing → Usage at the start of each sprint and at each EPIC merge. A formal automated alert mechanism is not yet implemented — this policy establishes a manual check cadence until automation is in place (see §7).

---

## 5. Double-Capacity Sprint Assessment

**Question:** Does the current double-capacity sprint cadence (2 full releases/sprints per billing month) require a plan upgrade?

**Assessment:**

| Scenario | Minutes estimate | Allocation sufficient? |
|----------|-----------------|----------------------|
| Single capacity sprint (~13 stories, 2 EPICs) | ~80–120 min | ✅ Yes |
| Double capacity sprint (~22 stories, 4 EPICs) | ~160–220 min | ✅ Yes (single occurrence) |
| **Two double-capacity sprints in one month** | **~320–440 min** | ⚠️ Borderline / ❌ At risk |
| Three cycles in one month | ~400–600 min | ❌ Exhaustion expected |

**Disposition:** At current v4.x cadence (2 cycles/month sustained), the 400-minute allocation is at risk in months with double-capacity sprints. **Recommendation:** Pre-emptively upgrade to Render Standard plan (2000+ minutes/month) or equivalent before the next double-capacity sprint window. File as BLG-OPS-48 (actionable recommendation).

**Cost impact:** Render Standard plan upgrade adds ~$7–19/month in build infrastructure costs. Trade-off: eliminates sprint blocking risk. FinOps & Resource Architect recommends upgrade before v4.9 cycle.

---

## 6. Billing Cycle Reset Date

**Reset date:** 1st of each calendar month (00:00 UTC).

At the start of each month, build minutes reset to the full allocation. No carry-over from prior month.

**Implication for sprint planning:** If a sprint is planned to start near end-of-month (e.g., day 28–31), verify remaining build minutes before committing to scope. If < 100 minutes remain, consider (a) deferring heavy-build EPICs to post-reset, or (b) triggering the plan upgrade.

---

## 7. Future Automation (Recommended — BLG-OPS-48)

The following automation improvements are recommended for a future sprint:

| Improvement | Priority | Backlog Ref |
|-------------|----------|-------------|
| GitHub Action or Render webhook to alert when 80% threshold is reached | P2 | To be filed — BLG-OPS-5x |
| Monthly usage report auto-published to sprint planning channel | P3 | To be filed — BLG-OPS-5x |

---

## 8. Sign-Off

| Role | Approver | Date |
|------|----------|------|
| FinOps & Resource Architect | Sprint Execution Engine (autonomous class) | 2026-06-01 |
| Infrastructure & Operations Owner | Sprint Execution Engine (autonomous class) | 2026-06-01 |
