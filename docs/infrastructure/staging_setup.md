**Owner:** Infrastructure & Operations Owner
**Class:** Reference Document (Class 3)
**Status:** Active
**Last Updated:** 2026-03-16
**Cycle:** 2026-03-15__release-v1.10 (ST-01)

---

# Staging Environment Setup Runbook

## Architecture Decision

**Approach:** Render (API Web Service + Static Site) + Supabase (separate project)

| Component | Production | Staging |
|-----------|-----------|---------|
| Frontend | GitHub Pages (`sachiv1984.github.io/swing-trading-model`) | Render Static Site (`trading-assistant-staging.onrender.com`) |
| API | Render Web Service (`trading-assistant-api-c0f9.onrender.com`) | Render Web Service (`trading-assistant-api-staging.onrender.com`) |
| Database | Supabase (production project) | Supabase (staging project — separate) |

**Rationale:** Same platform as production (no new vendors). React app uses `HashRouter` so no path-routing config needed on Render Static Site. Free tier sufficient for staging load.

**Note on service names:** Render service names are globally unique. If `trading-assistant-api-staging` or `trading-assistant-staging` are taken, choose alternative names and update:
- `backend/config.py` `ALLOWED_ORIGINS` (line with staging frontend URL)
- `render.yaml` service names and `fromService` reference

---

## Section 1 — Supabase: Create Staging Project

**These steps must be completed FIRST. The staging DATABASE_URL is required before creating the Render services.**

### 1.1 Create the project

1. Go to [supabase.com](https://supabase.com) → Dashboard → **New project**
2. Name it: `trading-assistant-staging`
3. Set a strong database password (save it — needed for connection string)
4. Choose the same region as production (to minimise latency for comparison testing)
5. Click **Create new project** and wait for provisioning (~2 minutes)

### 1.2 Copy schema from production

The staging database must have the same schema as production. Use `pg_dump` to export the schema only (no data):

```bash
# Get your production DATABASE_URL from Render dashboard (Environment tab of the API service)
# It looks like: postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

pg_dump "$PROD_DATABASE_URL" \
  --schema-only \
  --no-owner \
  --no-acl \
  --no-comments \
  -f staging_schema.sql
```

Then apply to staging:

```bash
# Get the staging DATABASE_URL from the Supabase staging project:
# Project Settings → Database → Connection string → URI (use the "Transaction" pooler URI for port 6543)

psql "$STAGING_DATABASE_URL" -f staging_schema.sql
```

**Alternative (Supabase UI):**
If `pg_dump` is not available locally, use the Supabase SQL Editor to recreate tables. The required tables are:

| Table | Key columns |
|-------|-------------|
| `portfolios` | id (uuid PK), cash (numeric), last_updated (timestamp) |
| `positions` | id, portfolio_id (FK), ticker, market, entry_date, entry_price, fill_price, fill_currency, fx_rate, shares, total_cost, fees_paid, fee_type, initial_stop, current_stop, current_price, atr, holding_days, pnl, pnl_pct, status, entry_note, tags (text[]), updated_at, exit_date |
| `trade_history` | id, portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, gross_proceeds, net_proceeds, entry_fees, exit_fees, pnl, pnl_pct, holding_days, exit_reason, entry_fx_rate, exit_fx_rate, entry_note, exit_note, tags (text[]) |
| `settings` | id (uuid PK), created_at, updated_at, + all settings columns (replicate from production) |
| `cash_transactions` | id, portfolio_id, type, amount (numeric), date, note, created_at |
| `portfolio_history` | id, portfolio_id, snapshot_date, total_value, cash_balance, positions_value, total_pnl, position_count, created_at; UNIQUE(portfolio_id, snapshot_date) |
| `signals` | id, portfolio_id, ticker, market, signal_date, rank, momentum_percent, current_price, price_gbp, atr_value, volatility, initial_stop, suggested_shares, allocation_gbp, total_cost, status, updated_at, created_at; UNIQUE(portfolio_id, ticker, signal_date) |
| `tickers` | id, ticker |
| `trade_reflections` | id, trade_id (FK → trade_history, UNIQUE), trade_rationale, what_worked, what_didnt_work, discipline_assessment, key_takeaway, created_at, updated_at |

**Strongly recommend `pg_dump` approach** — it guarantees schema parity.

### 1.3 Seed a portfolio record

The API requires at least one portfolio record to function:

```sql
INSERT INTO portfolios (id, cash, last_updated)
VALUES (gen_random_uuid(), 10000.00, NOW());
```

Run this in the Supabase SQL Editor for the staging project.

### 1.4 Get the staging DATABASE_URL

1. Supabase staging project → **Project Settings** → **Database**
2. Under **Connection string**, select **URI**
3. Use the **Transaction** pooler URI (port `6543`) — this is what Render needs
4. Copy the full string: `postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres`
5. **Save this securely** — you will set it as a Render environment variable in Section 3.

---

## Section 2 — Render: Deploy Staging Services via Blueprint

The `render.yaml` file in the repo root defines both staging services. Use the Render Blueprint feature to deploy them.

### 2.1 Create services via Blueprint

1. Go to [render.com](https://render.com) → Dashboard → **New** → **Blueprint**
2. Connect to the `sachiv1984/swing-trading-model` GitHub repository
3. Render will detect `render.yaml` and show 2 services:
   - `trading-assistant-api-staging` (Web Service)
   - `trading-assistant-staging` (Static Site)
4. Review and click **Apply** (do NOT set `DATABASE_URL` yet — do it in the next section)

> **If service names are taken:** Rename to e.g. `trading-assistant-api-stg` and `trading-assistant-stg`. Update `backend/config.py` `ALLOWED_ORIGINS` to match the new frontend URL, and update `render.yaml` accordingly before deploying.

### 2.2 Confirm auto-deploy settings

After Blueprint deploys, verify each service:

**trading-assistant-api-staging (Web Service):**
- Settings → **Branch:** `main`
- Settings → **Auto-Deploy:** Yes (deploys on every push to `main`)

**trading-assistant-staging (Static Site):**
- Settings → **Branch:** `main`
- Settings → **Auto-Deploy:** Yes

---

## Section 3 — Render: Set DATABASE_URL Secret

The `DATABASE_URL` is marked `sync: false` in `render.yaml` — it must be set manually to avoid committing the secret to the repo.

1. Render Dashboard → `trading-assistant-api-staging` → **Environment**
2. Click **Add Environment Variable**
3. Key: `DATABASE_URL`
4. Value: the staging Supabase connection string from Section 1.4
5. Click **Save Changes**
6. Render will automatically redeploy the API service

---

## Section 4 — Verify Deployment

### 4.1 Verify staging API

```bash
curl https://trading-assistant-api-staging.onrender.com/health
# Expected: {"status": "ok", ...}

curl https://trading-assistant-api-staging.onrender.com/health/detailed
# Expected: database connectivity confirmed, no errors
```

### 4.2 Verify staging frontend

1. Visit `https://trading-assistant-staging.onrender.com` in a browser
2. Confirm the app loads and connects to the staging API (not production)
3. Check browser network tab: API calls should go to `trading-assistant-api-staging.onrender.com`

### 4.3 Verify isolation

Confirm staging and production are fully isolated:
- Action in staging (e.g. add a test position) must NOT appear in production
- Production database must be unaffected by staging activity

---

## Section 5 — CORS: Update if Service Names Changed

If you used different Render service names than those in `render.yaml`:

1. Open `backend/config.py`
2. Replace `https://trading-assistant-staging.onrender.com` with the actual staging frontend URL
3. Commit: `[EPIC-01][ST-01] Update CORS for actual staging frontend URL`
4. Push to `exec/2026-03-15__release-v1.10/EPIC-01`

If the service names match as planned, this step is already done (CORS was updated in the ST-01 commit).

---

## Section 6 — Render Free Tier Considerations

- **API (Web Service):** Free tier spins down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds. Acceptable for QA use; not suitable for production load testing.
- **Static Site:** Always on, no spin-down.
- **Auto-deploy on push to main:** Both services will redeploy. API redeploy takes ~2–3 minutes.

---

## Section 7 — Access for Director of Quality

The staging URLs are public (no authentication on the Render services themselves). Share with Director of Quality:

- **Staging frontend:** `https://trading-assistant-staging.onrender.com`
- **Staging API health:** `https://trading-assistant-api-staging.onrender.com/health`
- **Note:** API may take 30–60 seconds to respond on first access (free tier spin-up). Refresh once if the frontend shows a loading error.

---

## Acceptance Criteria Checklist

- [ ] Staging frontend accessible at a stable URL (≠ production URL)
- [ ] Staging API accessible and returns healthy status
- [ ] Frontend and backend both running — app loads and functions end-to-end
- [ ] Database uses seeded data set (staging Supabase project with portfolio record)
- [ ] Staging database is isolated from production (separate Supabase project)
- [ ] Director of Quality can access staging URL
- [ ] Hosting approach documented (this file — same-platform Render + Supabase approach)
