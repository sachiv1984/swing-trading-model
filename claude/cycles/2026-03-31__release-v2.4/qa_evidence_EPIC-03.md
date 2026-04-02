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

**Evidence method:** HoE schema audit via code evidence (no direct DB access required).

**Commit:** `79b68f1` — `[EPIC-03][ST-06] Reconcile portfolios table schema in data_model.md`

**Schema audit findings (Head of Engineering — 2026-04-02):**

`initial_cash` — **confirmed present in DB.** Evidence: `scripts/reset_staging_db.sql` line 54 (`INSERT INTO portfolios (cash, initial_cash, last_updated)`) actively inserts it; data migration v1.2→v1.3 reads `SELECT initial_cash, created_at::date FROM portfolios`. If the column were absent, the staging reset script would fail. Column is retained (deprecated, not dropped).

`created_at` vs `created_date` — **no discrepancy.** `created_at` is the SQL column name; all SQL migrations and `database.py` use `created_at`. The string `"created_date"` appears only in `backend/portfolio_setup.py` which is the legacy file-based JSON system — it has no bearing on the SQL schema.

**Direct DB access assessment:** Not required. Code evidence is definitive — `reset_staging_db.sql` and the v1.2→v1.3 migration together constitute authoritative proof of both column names.

**Acceptance Criteria:**

| AC | Description | Evidence | Result |
|----|-------------|----------|--------|
| AC-1 | `data_model.md` portfolios CREATE TABLE matches deployed schema | Verified via code evidence — no divergence found | ✅ Pass |
| AC-2 | `initial_cash` either removed from spec or confirmed present in DB | Confirmed present — `reset_staging_db.sql` L54 inserts it | ✅ Pass |
| AC-3 | `created_date` vs `created_at` discrepancy resolved | `created_at` confirmed correct; `created_date` is legacy JSON only | ✅ Pass |
| AC-4 | `data_model.md` version bumped; notes updated | `data_model.md` v2.0 → v2.1; clarifying notes added to §1 | ✅ Pass |

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
