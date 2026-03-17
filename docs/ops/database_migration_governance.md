**Owner:** Backend Engineering Patterns Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-03-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Database Migration Governance Standard

---

## 1. Purpose

This document defines the governance standard for all database schema migrations in the Momentum Trading Assistant backend. It ensures migrations are safe, reversible where possible, reviewed before application, and recoverable if they fail.

All schema changes — including `CREATE TABLE`, `ALTER TABLE`, `ADD COLUMN`, `DROP COLUMN`, `CREATE INDEX`, and constraint modifications — are subject to this standard.

---

## 2. When This Standard Applies

This standard applies to:
- Any change to the database schema (`schema.sql` or equivalent)
- Any Alembic migration script or raw SQL migration file
- Any data migration that modifies existing rows in a table used by the production API

It does **not** apply to:
- Read-only queries
- Application configuration changes with no schema effect
- Test database setup scripts (`tests/fixtures/`)

---

## 3. Migration File Naming Convention

```
YYYYMMDD_NNN_<short_description>.sql
```

| Component | Rule |
|-----------|------|
| `YYYYMMDD` | Date migration was authored (not applied) |
| `NNN` | Three-digit sequence number within that date (001, 002, ...) |
| `<short_description>` | Snake-case description of the change (max 50 chars) |

**Examples:**
- `20260317_001_add_entry_fx_rate_to_positions.sql`
- `20260317_002_create_user_notification_preferences.sql`

Migration files are stored in `backend/migrations/`.

---

## 4. Required Migration File Fields

Every migration file must include a header comment block with the following fields:

```sql
-- Migration: 20260317_001_add_entry_fx_rate_to_positions.sql
-- Description: Adds entry_fx_rate column to positions table for explicit FX rate tracking at entry
-- Author: <role or name>
-- Date: 2026-03-17
-- Reversible: Yes
-- Rollback SQL:
--   ALTER TABLE positions DROP COLUMN IF EXISTS entry_fx_rate;
-- Risk assessment: Low — additive column, nullable, no existing rows affected
-- Spec reference: docs/specs/api_contracts/reports_endpoints.md §entry_fx_rate
```

| Field | Required | Notes |
|-------|----------|-------|
| `Migration` | Yes | File name (self-referential) |
| `Description` | Yes | One sentence describing what changes and why |
| `Author` | Yes | Role or name |
| `Date` | Yes | Authoring date |
| `Reversible` | Yes | `Yes`, `No`, or `Conditional` |
| `Rollback SQL` | Yes if Reversible = Yes | Exact SQL to undo the migration |
| `Risk assessment` | Yes | Low / Medium / High with brief justification |
| `Spec reference` | Yes if applicable | Canonical spec section that requires this field |

If a migration is **not reversible** (e.g. `DROP COLUMN` with data loss), the `Risk assessment` must be `High` and the migration requires Head of Engineering + Data Model Domain & Schema Owner sign-off before application.

---

## 5. Review Requirements

| Migration type | Required reviewers |
|----------------|-------------------|
| Additive (ADD COLUMN, CREATE TABLE, CREATE INDEX) | Second engineer review |
| Structural (ALTER COLUMN type, RENAME) | Second engineer + Schema Owner |
| Destructive (DROP COLUMN, DROP TABLE, TRUNCATE) | Head of Engineering + Schema Owner |
| Data migration (UPDATE existing rows) | Head of Engineering + Director of Quality |

Review must be recorded as a pull request comment or sign-off commit before the migration is applied to staging or production.

---

## 6. Application Procedure

### 6.1 Pre-Application Checklist

Before applying any migration:

- [ ] Migration file follows naming convention (§3)
- [ ] All required header fields present (§4)
- [ ] Review completed and recorded (§5)
- [ ] Migration tested against a local or staging copy of the database
- [ ] Rollback SQL tested (for reversible migrations)
- [ ] Application is not currently under load (or a maintenance window is open)
- [ ] Current schema state backed up (or snapshot confirmed in staging)

### 6.2 Staging Application

1. Apply migration to staging database:
   ```bash
   psql $STAGING_DATABASE_URL -f backend/migrations/<migration_file>.sql
   ```
2. Run integration tests against staging:
   ```bash
   python -m pytest tests/ -v
   ```
3. Verify affected API endpoints return expected responses
4. Record result (pass/fail) in the migration's PR or deployment record

### 6.3 Production Application

Production migration may only proceed when:
- Staging application succeeded (§6.2)
- All integration tests pass on staging
- Director of Quality sign-off obtained (for Data migration type; recommended for Destructive type)

Apply to production:
```bash
psql $DATABASE_URL -f backend/migrations/<migration_file>.sql
```

Record the UTC timestamp of production application and the result (success/failure) in the migration file's PR or deployment log.

---

## 7. Incident Procedure (Migration Fails Mid-Apply)

If a migration fails partway through:

### 7.1 Immediate actions

1. **Do not retry** the migration without diagnosing the failure first
2. Capture the full error output
3. Check whether the migration was transactional:
   - If wrapped in `BEGIN; ... COMMIT;`: the database should have rolled back automatically — verify with `\d <table>` in psql
   - If not transactional: determine which statements applied and which did not

### 7.2 Rollback

If partial application is confirmed and a rollback SQL is available:
```bash
psql $DATABASE_URL -f rollback_<migration_file>.sql
```

If no rollback SQL exists (non-reversible migration):
- Escalate to Head of Engineering immediately
- Do not apply any further migrations until the failure is resolved
- Restore from backup if data integrity is at risk

### 7.3 Post-incident

- Document the failure, root cause, and resolution in the migration's PR
- Add a post-incident note to `docs/ops/` if the failure reveals a gap in this governance standard

---

## 8. Cross-References

- Database schema: `docs/specs/data_model.md`
- Backend implementation patterns: see engineering standards (no standalone `backend_engineering_patterns.md` exists at time of writing — this document is a peer standard)
- Spec-driven schema changes: changes required by API contracts should reference the relevant spec section (see §4 `Spec reference` field)
- Staging environment: `docs/ops/` (staging runbook, if present)

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-17 | Initial version. ST-16 — EPIC-05 (Documentation & Standards Pack). v2.0 sprint cycle 2026-03-17__release-v2.0. Backend Engineering Patterns Owner + Head of Engineering sign-off. |
