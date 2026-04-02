---
**Owner:** QA Lead
**Class:** Working Document (Class 3)
**Status:** Active — ST-06 complete, ST-07 pending
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

**Status:** Delegated — blocked_backend (DEL-20260401-02)

**Delegation details:**
- **Assigned to:** Head of Engineering + API Contracts & Documentation Owner
- **Delegation log entry:** DEL-20260401-02
- **Branch:** `exec/2026-03-31__release-v2.4/EPIC-03`
- **Required commit:** `[EPIC-03][ST-07] Reconcile trade_history table schema in data_model.md`
- **GitHub issue:** #166

**Blocking reason:** Requires `\d trade_history` output from staging database to confirm canonical column set (`exit_proceeds` vs `gross_proceeds`/`net_proceeds`/`entry_fees`/`exit_fees`).

**Acceptance Criteria (pending completion):**

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | `data_model.md` trade_history CREATE TABLE matches `\d trade_history` on staging | Pending |
| AC-2 | `database.py:create_trade_history()` column list matches confirmed schema | Pending |
| AC-3 | `seed_portfolio_trades.sql` trade_history INSERT uses confirmed column names and succeeds | Pending |
| AC-4 | `data_model.md` version bumped; §6 checklist applied | Pending |

**DoQ sign-off:** Pending delegation completion — Head of Engineering + API Contracts Owner to commit and sign off.

---

## Consolidation

| Story | Status | Commit | Notes |
|-------|--------|--------|-------|
| ST-06 | Done | 79b68f1 | HoE schema audit 2026-04-02 — code evidence definitive, no DB access required. All 4 AC Pass. |
| ST-07 | Delegated — blocked_backend | — | DEL-20260401-02: Head of Engineering + API Contracts Owner, GitHub #166 |

**EPIC-03 DoQ:** ST-06 complete. ST-07 still delegated — requires HoE action on trade_history schema. EPIC-03 merge gate holds until ST-07 committed.
