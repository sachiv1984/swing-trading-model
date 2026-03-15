**Owner:** Backend Engineering Patterns Owner
**Class:** Planning Document (Class 4)
**Status:** Parked-cycle-2
**Submitted by:** Backend Engineering Patterns Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-backend-engineering-20260304-02

---

# Idea: Database Migration Governance Standard

## 1. Problem Statement

There is no documented process for how database schema migrations are created, reviewed, applied, and rolled back. The current practice is undocumented: a developer writes a migration, applies it to the database, and moves on. There is no version tracking of applied migrations, no review step, and no rollback procedure. In a system where the database holds live trading positions with real financial consequences, a bad migration applied to production without a rollback procedure is a critical operational risk.

## 2. Strategic Alignment

Section reference: Backend Engineering Patterns §4 — Adding a New Endpoint ("Step 1: confirm the canonical spec is locked — never implement without a committed, locked contract")

Alignment rationale: The same discipline that requires a locked spec before implementation is required before a database schema change. A migration that does not have a reviewed rollback procedure is equivalent to an endpoint implemented without a locked spec — it is moving forward without a safety net. The migration governance standard extends the existing engineering discipline to the database layer.

## 3. Proposed Solution

Create `docs/team_skills/engineering/database_migration_governance.md` — a Class 1 canonical document defining: (1) migration naming convention (e.g., `YYYYMMDD_HHMMSS_description.sql`), (2) required fields in a migration file (description, reversibility assessment, rollback SQL), (3) review requirements (at least one review by a second engineer, schema owner sign-off for structural changes), (4) application procedure for production (applied in a transaction where possible, tested against a staging copy first), and (5) incident procedure if a migration fails mid-apply.

## 4. Expected Value

Reduces the risk of a database incident caused by an unreviewed or un-rollbackable migration. Provides a documented audit trail for every schema change. Expected to prevent the class of incident where a migration partially applies and leaves the database in an inconsistent state with no documented recovery path.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires input from the Head of Engineering on whether a migration tool (e.g., Alembic) should be adopted. The governance standard can be defined independently of tool choice.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: A governance document can be revised; it does not change existing database schema.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Every undocumented schema change applied to the production database is a governance gap. Given that v1.7 may have involved schema changes, now is the right time to formalise before the next release.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | 🅿 Parked |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | N/A — not advanced to STEP 5 debate |
| Outcome date | N/A |
| Notes | |
