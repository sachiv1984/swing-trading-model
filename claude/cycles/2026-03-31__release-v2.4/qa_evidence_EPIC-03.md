---
**Owner:** QA Lead
**Class:** Working Document (Class 3)
**Status:** Complete — both stories done
**Cycle:** 2026-03-31__release-v2.4
**EPIC:** EPIC-03 — Data Model Schema Reconciliation
**Last Updated:** 2026-04-02
---

# QA Evidence — EPIC-03

## Delivery of Quality (DoQ) Sign-Off Log

### ST-06 — Reconcile portfolios table schema in data_model.md

**Story:** Align `docs/specs/data_model.md` portfolios CREATE TABLE with deployed staging DB schema.

**Status:** Done — 2026-04-02

**Evidence method:** Actual Supabase DB schema provided by Product Owner 2026-04-02 (direct DB confirmation). Initial code-inference pass (v2.1) was incorrect — DB confirmation supersedes.

**Commits:**
- `79b68f1` — initial (incorrect code-inference pass — superseded)
- `pending` — corrected against actual DB schema

**Actual DB schema (confirmed 2026-04-02):**
```sql
CREATE TABLE public.portfolios (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  cash numeric(12, 2) NOT NULL DEFAULT 20000.00,
  created_date DATE NOT NULL DEFAULT CURRENT_DATE,
  last_updated TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
  CONSTRAINT portfolios_pkey PRIMARY KEY (id)
);
```

**Divergences found and corrected:**

| Column | Spec (before) | Actual DB | Fix |
|--------|--------------|-----------|-----|
| `initial_cash` | Present (deprecated) | **Does not exist** | Removed from spec |
| `created_at` TIMESTAMP | In spec | **Does not exist** | Removed from spec |
| `created_date` DATE | Not in spec | **Exists, NOT NULL** | Added to spec |
| `cash` DEFAULT | `DEFAULT 0` | `DEFAULT 20000.00` | Corrected |
| `last_updated` | Nullable | **NOT NULL** | Corrected |

**Side effect fixed:** `scripts/reset_staging_db.sql` inserted `initial_cash` (line 54) which would fail against actual DB. Removed `initial_cash` from INSERT.

**Acceptance Criteria:**

| AC | Description | Evidence | Result |
|----|-------------|----------|--------|
| AC-1 | `data_model.md` portfolios CREATE TABLE matches `\d portfolios` on staging | Direct DB schema provided by PO 2026-04-02 — spec updated to match exactly | ✅ Pass |
| AC-2 | `initial_cash` either removed from spec or present in DB | `initial_cash` absent from DB — removed from spec and reset script | ✅ Pass |
| AC-3 | `created_date` vs `created_at` discrepancy resolved | DB has `created_date DATE` — spec corrected from `created_at TIMESTAMP` | ✅ Pass |
| AC-4 | `data_model.md` version bumped | `data_model.md` v2.0 → v2.2; `reset_staging_db.sql` fixed | ✅ Pass |

**DoQ sign-off:** ✅ Head of Engineering — 2026-04-02

---

### ST-07 — Reconcile trade_history table schema in data_model.md

**Story:** Align `docs/specs/data_model.md` trade_history CREATE TABLE, `database.py`, and seed SQL with confirmed staging DB schema.

**Status:** Done — 2026-04-02

**Evidence method:** Actual Supabase DB schema provided by Product Owner 2026-04-02 (direct DB confirmation).

**Commit:** `pending-ST-07` — `[EPIC-03][ST-07] Reconcile trade_history schema against actual Supabase DB`

**Divergences found and corrected:**

| Column/detail | Spec (before) | Actual DB | Fix |
|---------------|--------------|-----------|-----|
| `exit_proceeds` | Present, NOT NULL | **Does not exist** | Removed from spec |
| `gross_proceeds` | Not in spec | Present, nullable | Added |
| `net_proceeds` | Not in spec | Present, nullable | Added |
| `entry_fees` | Not in spec | Present, nullable | Added |
| `exit_fees` | Not in spec | Present, nullable | Added |
| `portfolio_id` nullability | NOT NULL | NULL | Fixed |
| `market` nullability | NOT NULL | NULL | Fixed |
| `total_cost` nullability | NOT NULL | NULL | Fixed |
| `pnl` / `pnl_pct` nullability | NOT NULL | NULL | Fixed |
| `holding_days` nullability | NOT NULL | NULL | Fixed |
| `exit_reason` length | VARCHAR(50) | VARCHAR(100) | Fixed |
| `entry/exit_fx_rate` type | DECIMAL(10,6) | NUMERIC(10,4) | Fixed |
| `created_at` nullability | NOT NULL (implied) | NULL DEFAULT now() | Fixed |
| `position_id` column order | Near top | Last column | Fixed |
| FK `portfolio_id` | No cascade | ON DELETE CASCADE | Fixed |
| Index `idx_trade_history_exit_date` | In spec | **Not in DB** | Removed |
| Index `idx_trade_history_position_id` | Not in spec | Present | Added |

**`fill_price` — confirmed present (2026-04-02):**
`fill_price` was not visible in the base DDL (added via ALTER TABLE by the v1.9→v2.0 migration). Confirmed present in Supabase DB via `information_schema.columns` query — column exists. Spec updated to include `fill_price` in the main CREATE TABLE definition. No action required.

**Acceptance Criteria:**

| AC | Description | Evidence | Result |
|----|-------------|----------|--------|
| AC-1 | `data_model.md` trade_history CREATE TABLE matches `\d trade_history` on staging | Direct DB schema provided by PO 2026-04-02 — spec updated to match exactly | ✅ Pass |
| AC-2 | `database.py:create_trade_history()` column list matches confirmed schema | All columns match (`gross_proceeds`/`net_proceeds`/`entry_fees`/`exit_fees`); `fill_price` retained as migration-dependent — no code change | ✅ Pass (with `fill_price` migration flag) |
| AC-3 | `seed_portfolio_trades.sql` INSERT uses confirmed column names | Seed already uses `gross_proceeds`/`net_proceeds`/`entry_fees`/`exit_fees`; no `exit_proceeds`; no `fill_price`. No change required. | ✅ Pass |
| AC-4 | `data_model.md` version bumped | `data_model.md` v2.2 → v2.3 | ✅ Pass |

**DoQ sign-off:** ✅ Head of Engineering — 2026-04-02

---

## Consolidation

| Story | Status | Commit | Notes |
|-------|--------|--------|-------|
| ST-06 | Done | 79b68f1 | HoE schema audit 2026-04-02 — code evidence definitive, no DB access required. All 4 AC Pass. |
| ST-07 | Done | pending-ST-07 | HoE schema audit 2026-04-02 — direct DB confirmation. 8 divergences corrected. fill_price migration flag raised. |

**EPIC-03 DoQ:** Both stories complete. fill_price migration status flagged for PO follow-up (confirm v1.9→v2.0 migration applied to Supabase prod). Ready for PR and merge.

**Director of Quality sign-off:** [x] 2026-04-03
DoQ review note: ST-06 and ST-07 verified against direct Supabase DB schema provided by Product Owner 2026-04-02. Head of Engineering sign-off on both stories accepted as the domain authority for schema correctness (direct DB access required). All AC confirmed Pass by DB evidence. fill_price migration flag is a post-merge tracking item (not a deviation). DoQ sign-off appended 2026-04-03 at delivery verification preflight — HoE sign-off was the primary authority for schema reconciliation stories; DoQ review confirms evidence quality and AC coverage are sufficient.
