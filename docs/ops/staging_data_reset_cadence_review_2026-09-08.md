**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-55, EPIC-05, v9.2, BLG-OPS-141 — cadence defined and documented)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Staging Environment Data-Reset Cadence

## 1. Current Mechanism

`.github/workflows/reset-and-seed-staging.yml` (`workflow_dispatch` only — no scheduled trigger exists today) resets `STAGING_DATABASE_URL` to a clean baseline, applies pending schema migrations, and optionally seeds QA fixture data (`scripts/reset_staging_db.sh`, `scripts/seeds/seed_all.sh`). Its own header comment states the intended trigger: **"run before any QA session against staging."** No cadence beyond that has ever been formally defined — this story's gap.

## 2. Cadence Definition

**Primary trigger (unchanged, confirmed as correct): manual, before each QA session against staging.** This remains the right default — a reset mid-session would destroy in-progress test state, so triggering only ever needs to be human-initiated at a session boundary, not on a fixed clock. No change recommended here.

**New: a documented staleness ceiling, not an automated schedule.** Between QA sessions, if none occurs for an extended period, staging data can silently accumulate drift (partial test runs, manually-poked records, schema migrations applied but never re-baselined against). Define:

- **Staleness ceiling: 30 days.** If staging has not been reset within the last 30 days *and* a new QA session is about to start, reset before that session rather than reusing possibly-stale data — this is a strengthening of the existing "before any QA session" trigger (makes explicit that "before" means "reset if last reset > 30 days old", not merely "reset if you remember to").
- **No calendar-scheduled automated reset is added.** Deliberately not adding a `schedule:` cron trigger to `reset-and-seed-staging.yml` — an unattended destructive reset firing while a QA session happens to be in progress would destroy that session's test state with no human in the loop to catch it, and this app's QA cadence (roughly once per sprint) is infrequent enough that a 30-day staleness ceiling checked at session-start already achieves the goal without that risk. If QA session frequency increases materially in the future, revisit whether a scheduled trigger becomes worth the added risk.
- **Where to check "last reset" date:** the workflow run history (Actions tab) is the source of truth; no separate tracking file is introduced by this story to avoid a second, potentially-drifting record of the same fact.

## 3. Sign-Off

**Infrastructure & Operations Owner:** Confirmed — cadence defined (manual, session-triggered, with an explicit 30-day staleness ceiling), documented; no change made to the existing `workflow_dispatch`-only trigger mechanism, deliberately, per the rationale above. 2026-09-08.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-08 | 1.0 | Cadence defined and documented (ST-55, EPIC-05, v9.2, BLG-OPS-141). |
