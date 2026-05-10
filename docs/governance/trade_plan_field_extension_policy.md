**Owner:** Data Model Domain & Schema Owner
**Class:** Governance Document (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-10
**Story:** ST-12 (EPIC-03, v3.3) — BLG-GOV-20
**Sign-off:** Data Model Domain & Schema Owner: Accepted — 2026-05-10 (agent-mediated, v3.3 design gate)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Trade Plan Field Extension Policy

This policy governs how new fields are added to the `trade_plans` schema. Referenced by any story that proposes extending the trade plan data model.

---

## 1. Field Addition Decision Criteria

### 1.1 Add to `trade_plans` table when:

- The field is intrinsic to the trade plan concept (pre-trade reasoning, entry parameters, risk settings)
- The field is authored once per plan and updated in-place (upsert pattern)
- The field is needed in every trade plan context (list, detail, form)
- The field has a clear 1:1 cardinality with a trade plan

### 1.2 Create a separate table when:

- The field has 1:N cardinality (multiple records per trade plan)
- The field is independently versioned or audited (e.g. state history)
- The field is accessed independently and at high frequency (performance benefit from separate query)
- The field is added by a different owner role and should be governed separately

**Examples requiring separate table:** trade plan comments, trade plan revision history, per-plan alert rules.

---

## 2. Migration Strategy

### 2.1 When a migration script is required

A SQL migration script documented in `docs/specs/data_model.md` is **required** for:
- Any new column in `trade_plans` (regardless of nullability)
- Any schema constraint change (new CHECK, UNIQUE, NOT NULL)
- Any index addition

### 2.2 Nullable add (no back-fill required)

A nullable column with no default value may be added with a simple `ALTER TABLE ... ADD COLUMN ... NULL` migration. No back-fill is required. The migration is safe to apply without downtime.

### 2.3 NOT NULL with default

A `NOT NULL DEFAULT <value>` column is safe to apply in PostgreSQL 11+ as an instant operation (no table rewrite for constant defaults). The migration must include:
- The `NOT NULL DEFAULT` clause
- A verification query confirming all rows have the default value

### 2.4 NOT NULL without default (destructive)

Adding a NOT NULL column without a default requires a coordinated back-fill:
1. Add column as nullable
2. Back-fill all existing rows
3. Alter column to NOT NULL
This must be executed as three separate migration steps within one transaction or in a planned maintenance window.

---

## 3. Backwards Compatibility Rules

1. **Never remove a column without a deprecation period.** Columns must be marked deprecated in the data model spec for at least one release cycle before removal.
2. **Never change a column type in a destructive way** (e.g. VARCHAR(20) → INTEGER). Type widening (VARCHAR(20) → VARCHAR(50)) is safe.
3. **Never tighten a nullable column to NOT NULL** in a single migration without ensuring all existing rows have non-null values first.
4. **API responses may add new fields freely** (additive). Removing a field from an API response requires a versioning review.
5. **JSONB field schema changes** (e.g. `checklist_items` array shape) must be backwards compatible — existing items using the old shape must continue to deserialise correctly.

---

## 4. Authority

| Decision | Authority |
|---------|-----------|
| Add nullable column to `trade_plans` | Data Model owner approval required |
| Add NOT NULL column | Data Model owner + Product Owner approval required |
| Add separate table linked to trade plans | Data Model owner + Head of Specs Team approval |
| Remove/rename column | Data Model owner + Product Owner approval + deprecation notice filed |
| Change JSONB field structure | Data Model owner approval + backwards compatibility confirmed |

---

## 5. Changelog Format

When a trade plan schema change is made, a new DS-XX entry must be added to `docs/specs/data_model.md` following the DS-04/DS-05 pattern:

```markdown
## DS-XX — {Description} (v{n.m}, {YYYY-MM-DD})

**Story:** ST-xx (EPIC-xx, v{release})

{Purpose description}

### Up Migration

{SQL}

### Down Migration

{SQL}

**Sign-off:**
- Data Model Domain & Schema Owner: Accepted — {YYYY-MM-DD}
```

The version counter in the document header (`**Version:** n.m`) must be incremented.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-10 | Initial creation — ST-12 (EPIC-03, v3.3). Field addition criteria, migration strategy, backwards compatibility, authority matrix, changelog format. |
