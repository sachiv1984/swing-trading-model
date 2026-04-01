**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-01
**Cycle:** 2026-03-31__release-v2.4

---

# Delegation Log — v2.4 Correctness, Insight & Governance Hardening

This log records all delegated items (delegated_backend, delegated_frontend, delegated_decision) for this sprint cycle. Append-only.

---

## DEL-20260401-01

**ID:** DEL-20260401-01
**Date:** 2026-04-01
**Story:** ST-06 — Reconcile portfolios table schema in data_model.md
**EPIC:** EPIC-03
**Classification:** delegated_backend
**Assigned to:** Head of Engineering
**Status:** Pending

**Spec reference:** `docs/specs/data_model.md` — portfolios table (CREATE TABLE portfolios, line ~27)

**Context:**
`data_model.md` documents the `portfolios` table with columns: `id, cash, initial_cash, created_at, last_updated`. The deployed database has `id, cash, created_date, last_updated` — `initial_cash` does not exist and `created_at` is named `created_date`. This divergence must be resolved.

**Change required:**
1. Run `\d portfolios` on staging database to confirm the exact column set
2. Update `data_model.md` portfolios CREATE TABLE to match the staging DB schema exactly
3. Bump `data_model.md` version; apply §6 checklist if data_model.md has a version header
4. If `initial_cash` exists in DB: retain in spec; if absent: remove from spec

**Branch:** `exec/2026-03-31__release-v2.4/EPIC-03`
**Required commit format:** `[EPIC-03][ST-06] Reconcile portfolios table schema in data_model.md`
**GitHub issue:** #165
**Unblock criteria:** Commit `[EPIC-03][ST-06]` pushed to branch with `data_model.md` portfolios section matching staging DB output

**Acceptance criteria (from sprint backlog):**
- `data_model.md` portfolios CREATE TABLE matches `\d portfolios` output on staging
- `initial_cash` either removed from spec or present in DB — no divergence
- `created_date` vs `created_at` discrepancy resolved
- `data_model.md` version bumped; §6 checklist applied

---

## DEL-20260401-02

**ID:** DEL-20260401-02
**Date:** 2026-04-01
**Story:** ST-07 — Reconcile trade_history table schema in data_model.md
**EPIC:** EPIC-03
**Classification:** delegated_backend
**Assigned to:** Head of Engineering + API Contracts & Documentation Owner
**Status:** Pending

**Spec reference:** `docs/specs/data_model.md` — trade_history table (CREATE TABLE trade_history, line ~139)

**Context:**
`data_model.md` documents `trade_history` with column `exit_proceeds`. `database.py:create_trade_history()` uses `gross_proceeds, net_proceeds, entry_fees, exit_fees`. The canonical column set must be determined from the staging DB and the spec and code must align.

**Change required:**
1. Run `\d trade_history` on staging database to confirm the exact column set
2. Update `data_model.md` trade_history CREATE TABLE to match staging DB
3. Update `database.py:create_trade_history()` column list to match the confirmed schema
4. Update `seed_portfolio_trades.sql` trade_history INSERT to use confirmed column names
5. Bump `data_model.md` version; apply §6 checklist

**Branch:** `exec/2026-03-31__release-v2.4/EPIC-03`
**Required commit format:** `[EPIC-03][ST-07] Reconcile trade_history table schema in data_model.md`
**GitHub issue:** #166
**Unblock criteria:** Commit `[EPIC-03][ST-07]` pushed to branch with `data_model.md`, `database.py`, and `seed_portfolio_trades.sql` all using confirmed column names

**Acceptance criteria (from sprint backlog):**
- `data_model.md` trade_history CREATE TABLE matches `\d trade_history` on staging
- `database.py:create_trade_history()` column list matches the spec
- `seed_portfolio_trades.sql` trade_history INSERT uses confirmed column names and succeeds
- `data_model.md` version bumped; §6 checklist applied

**Layer(s) required:** Database schema spec (data_model.md) + database layer (database.py) + seed data (SQL)

---
