---
**Owner:** QA Lead
**Class:** Working Document (Class 3)
**Status:** Draft — Blocked (delegation pending)
**Cycle:** 2026-03-31__release-v2.4
**EPIC:** EPIC-03 — Data Model Schema Reconciliation
**Last Updated:** 2026-04-01
---

# QA Evidence — EPIC-03

## Delivery of Quality (DoQ) Sign-Off Log

### ST-06 — Reconcile portfolios table schema in data_model.md

**Story:** Align `docs/specs/data_model.md` portfolios CREATE TABLE with deployed staging DB schema.

**Status:** Delegated — blocked_backend (DEL-20260401-01)

**Delegation details:**
- **Assigned to:** Head of Engineering
- **Delegation log entry:** DEL-20260401-01
- **Branch:** `exec/2026-03-31__release-v2.4/EPIC-03`
- **Required commit:** `[EPIC-03][ST-06] Reconcile portfolios table schema in data_model.md`
- **GitHub issue:** #165

**Blocking reason:** Requires `\d portfolios` output from staging database to confirm `initial_cash` / `created_date` discrepancy. Engine cannot access staging DB directly.

**Acceptance Criteria (pending completion):**

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | `data_model.md` portfolios CREATE TABLE matches `\d portfolios` on staging | Pending |
| AC-2 | `initial_cash` either removed from spec or confirmed present in DB | Pending |
| AC-3 | `created_date` vs `created_at` discrepancy resolved | Pending |
| AC-4 | `data_model.md` version bumped; §6 checklist applied | Pending |

**DoQ sign-off:** Pending delegation completion — Head of Engineering to commit and sign off.

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
| ST-06 | Delegated — blocked_backend | — | DEL-20260401-01: Head of Engineering, GitHub #165 |
| ST-07 | Delegated — blocked_backend | — | DEL-20260401-02: Head of Engineering + API Contracts Owner, GitHub #166 |

**EPIC-03 DoQ:** Both stories delegated. EPIC-03 PR opened to establish branch and record delegation. Merge gate requires both ACs met (delegatee commits) before EPIC-03 can merge.
