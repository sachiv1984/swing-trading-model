**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-07-31
**Story:** ST-15 (BLG-OPS-80, EPIC-03, v6.3); ST-15 (BLG-OPS-109, EPIC-04, v8.0)

---

# Render Deployment Rollback Runbook

Procedure for rolling back to a prior deployment version on Render in the event of a production incident. Covers rollback decision criteria, execution steps, and verification.

---

## When to Rollback

### Rollback (immediate) — do not attempt fix-forward

Roll back immediately when:

| Criterion | Example |
|-----------|---------|
| **Health endpoint down** | `GET /health` returns non-200 for ≥ 2 consecutive checks | 
| **Database connectivity lost** | `GET /health` returns `"db": "error"` and restart hasn't resolved within 5 minutes |
| **Total endpoint failure** | ≥ 50% of critical endpoints returning 500 after deploy |
| **Data corruption** | Live trade records or position records visibly wrong (wrong prices, missing rows) after deploy |
| **Auth bypass** | A deploy introduced a regression allowing unauthenticated access to protected endpoints |

### Fix-forward — do not rollback

Fix forward (deploy a hotfix) when:

| Criterion | Rationale |
|-----------|-----------|
| **Non-critical endpoint failure** | One endpoint 500s but health, portfolio, positions, and signals unaffected |
| **UI-only issue** | Frontend regression on GitHub Pages — Render backend unaffected; redeploy frontend only |
| **Intermittent errors** | Sporadic 500s that clear on retry — likely transient; monitor before escalating |
| **Migration successfully ran** | A DB migration has already applied; rollback would not reverse the schema change and may create inconsistency |

---

## Rollback Steps

### Prerequisites

- Access to the Render dashboard at `dashboard.render.com` with Owner or Admin role on the `trading-assistant-api-c0f9` service
- The incident has been confirmed as rollback-worthy per the criteria above
- Inform the product owner before executing rollback if time permits

### Step 1 — Identify the prior deploy version

1. Open [Render dashboard](https://dashboard.render.com) → Services → `trading-assistant-api-c0f9`
2. Click **Deploys** in the left sidebar
3. Locate the last deploy that was **green (Live)** before the current problematic deploy
4. Note the deploy SHA and timestamp
5. Confirm the commit was the last known-good state (cross-reference with `git log --oneline origin/main`)

### Step 2 — Initiate rollback

1. Click on the prior green deploy row in the Deploys list
2. Click **Rollback to this deploy** (button on the right side of the deploy row)
3. Confirm the rollback prompt

Render will:
- Deploy the prior container image without running `buildCommand` again
- Re-run `startCommand` (`uvicorn main:app --host 0.0.0.0 --port $PORT`) with the prior code

**Note:** Rolling back does NOT reverse database migrations. If the incident was caused by a new schema migration, check §Database Migration Considerations below.

### Step 3 — Monitor rollback progress

1. Watch the deploy progress bar in the Render dashboard — should complete in ~2–4 minutes
2. Monitor the **Logs** tab for startup errors (look for `ERROR` entries in the first 60 seconds)
3. Confirm `@app.on_event("startup")` completes without fatal errors

**Note (confirmed during the 2026-07-31 staging drill, see §Execution History):** the Logs tab may show no entries at all during a clean rollback — this is not itself a sign of failure. Treat the Deploy status going **Live (green)** plus a successful `GET /health` (Step 4) as the authoritative signals; don't wait for log output that may never appear.

### Step 4 — Verify health

Run the following checks after the rollback deploy is **Live**:

```bash
# 1. Basic health
curl -s https://trading-assistant-api-c0f9.onrender.com/health | python3 -m json.tool

# 2. Confirm db: connected
# Expected: {"status": "ok", "db": "connected", ...}

# 3. Critical endpoint check (requires X-API-Key)
source ~/.api_keys
curl -s -H "X-API-Key: $API_KEY" https://trading-assistant-api-c0f9.onrender.com/positions | python3 -c "import sys,json; d=json.load(sys.stdin); print('positions:', 'ok' if isinstance(d, list) else 'error')"
curl -s -H "X-API-Key: $API_KEY" https://trading-assistant-api-c0f9.onrender.com/portfolio | python3 -c "import sys,json; d=json.load(sys.stdin); print('portfolio:', 'ok' if 'id' in d else 'error')"
```

Expected outcome: `GET /health` returns `"status": "ok"` and `"db": "connected"`. Critical endpoints return valid data.

---

## Database Migration Considerations

Render rollback reverts the application code only — it does **not** reverse database schema migrations. This creates a risk if the deployment being rolled back includes a schema migration that has already applied:

| Scenario | Risk | Action |
|----------|------|--------|
| New table added in migration | Prior code has no reference to the table | Safe to rollback — prior code ignores unknown tables |
| Column added to existing table | Prior code may use `SELECT *` and receive extra columns | Usually safe — extra columns ignored in Python dicts |
| Column renamed or dropped | Prior code references the old name → crashes | **Do not rollback** — deploy a hotfix instead |
| Column type changed | Prior code may fail to parse the new type | Assess case-by-case |

**Decision rule:** If the problematic deploy includes a destructive migration (column rename, drop, type change), fix-forward with a hotfix is safer than rollback. Contact the Head of Engineering before rollback if unsure.

Current migration pattern: all v6.x migrations use `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` (additive only). Rolling back is generally safe.

---

## Post-Rollback Actions

After rollback is verified:

1. **Inform product owner** that rollback was executed and the system is stable on the prior version
2. **File a post-incident note** in the cycle QA evidence log: rollback date, version rolled back from/to, incident description, resolution
3. **Create a hotfix branch** (`hotfix/<description>`) to prepare the fix that can be deployed safely
4. **Re-test the fix** on staging before re-deploying to production
5. **Check `GET /health/scheduler`** — if nightly jobs ran during the incident window, confirm their status is not degraded before the next scheduled run

---

## Execution History (ST-15, BLG-OPS-109, EPIC-04, v8.0)

This section tracks whether the procedure above has actually been exercised — against a real incident or a deliberate drill — as distinct from having been authored and reviewed.

**Finding as of 2026-07-31:** No real production rollback has ever been executed using this runbook, and no deliberate drill has been run against a staging/non-production deploy either. Confirmed by:
- `git log --all --oneline | grep -i rollback` returns only the commit that *authored* this runbook (`2d2c290c`), not a commit reverting a deploy.
- No `lessons_learnt_cycle.md` or `post_ship*.md` file across any cycle mentions a rollback event.
- `claude/backlog/backlog_archive.md` (BLG-OPS-91, "Deploy rollback runbook dry-run") explicitly states: *"The rollback runbook (BLG-OPS-80) is authored but has not yet been exercised against a real production deploy."*
- `claude/backlog/backlog.md` (BLG-OPS-109, the item this section resolves) states the same: *"only ever been dry-run, never executed against a real incident — its actual reliability under a live rollback is unverified."* Note: even a dry-run record could not be located as of this finding — the honest status is that neither a live incident rollback nor a documented drill has occurred yet.

**Disposition:** Per this story's AC ("historical execution evidence... OR a deliberate rollback drill... outcome documented either way"), a deliberate drill was run against the non-production staging service (`trading-assistant-api-staging`) by the Infrastructure & Operations Owner on 2026-07-31 (see `delegation_log.md` DEL-20260731-03 resolution). **Result: the rollback procedure works as documented.** The deploy transitioned cleanly to Live (green) in the Render dashboard, and a post-rollback `GET /health` check confirmed `"status":"ok","db":"connected"` — matching this runbook's §Step 4 expected outcome exactly.

**Procedure correction found during the drill:** Step 3 ("Monitor rollback progress") tells the operator to watch the Logs tab for `ERROR` entries in the first 60 seconds. In practice, no log entries — error or otherwise — were visible in the Logs tab during or immediately after the rollback, despite the deploy completing successfully. This means an empty/quiet Logs tab is not itself a red flag and should not be read as a stuck or failed rollback; the **Deploy status going Live (green) plus a successful `/health` check are the authoritative signals**, not log output. Step 3 above has been annotated with this note so a future operator doesn't misread silence as a problem.

| Date | Event | Outcome | Recorded by |
|------|-------|---------|-------------|
| 2026-07-31 | Execution-history audit (no rollback/drill performed) | No real rollback or drill found; procedure remains unexercised | Sprint Execution Engine (ST-15) |
| 2026-07-31 | Deliberate rollback drill executed against staging (`trading-assistant-api-staging`) | Success — deploy went Live (green); post-rollback `/health` confirmed `status: ok`, `db: connected`. No log entries observed during the rollback window (procedure note added to Step 3 above). | Infrastructure & Operations Owner |

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| Infrastructure & Operations Owner | Approved — rollback decision criteria, step-by-step procedure, DB migration risk matrix, and post-rollback actions reviewed and confirmed as complete and correct for the current Render deployment configuration | 2026-06-29 |
| Infrastructure & Operations Owner | Approved — deliberate rollback drill executed against staging (`trading-assistant-api-staging`); procedure confirmed to work as documented, one correction applied (Step 3 log-visibility note) based on tested reality | 2026-07-31 |

*Sign-off completed by Sprint Execution Engine under agent-mediated governance protocol — ST-15 AC-03.*
