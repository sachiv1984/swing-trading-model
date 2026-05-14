**Owner:** PMO Lead
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-14

---

# Shared Write Recovery Procedure

Applies to any shared resource with a lock + transaction pattern.

## Parameters (caller must supply)
- `{resource}`: `backlog` or `roadmap`
- `{lock_file}`: e.g. `claude/backlog/.lock`
- `{marker_value}`: e.g. `RP:<release>:<cycle_id>` or `RA:<release>:<cycle_id>`
- `{marker_key}`: e.g. `release-plan-marker` or `roadmap-annotation-marker`
- `{txn_file}`: e.g. `claude/cycles/<cycle_id>/backlog_txn.json`
- `{artifact_key}`: state.json artifact key for this lock (e.g. `backlog_lock`, `roadmap_lock`)
- `{resume_step}`: step to resume at if marker absent (e.g. STEP 4 for backlog, STEP 4.95/5 for roadmap)

## Procedure

Trigger: `{lock_file}` exists OR `artifacts.{artifact_key}` in state.json is `acquired`.

1. Read `{lock_file}` → get `owner_cycle_id`.
2. If `owner_cycle_id != <cycle_id>`: record ⛔ Blocker (Lifecycle/Process Integrity; owner: PMO Lead). HALT (no override, no auto-delete).
3. If `owner_cycle_id == <cycle_id>`: proceed with recovery below.

**Recovery:**
A) Check file/content for marker: `<!-- {marker_key}: {marker_value} -->`
B) If marker present:
   - Ensure `{txn_file}` exists and committed (create/upgrade if needed).
   - Update state.json: `artifacts.{artifact_key}_txn = committed`, `locks.{artifact_key}.txn_state = committed`.
   - Remove `{lock_file}`. Update state.json: `artifacts.{artifact_key} = released`, `locks.{artifact_key}.status = released`, `locks.{artifact_key}.owned = false`.
   - Continue.
C) If marker absent:
   - Treat step as incomplete. Set `artifacts.{artifact_key} = not_started`, `artifacts.{artifact_key}_txn = prepared` (create txn file if missing), `locks.{artifact_key}.txn_state = prepared`.
   - Resume at `{resume_step}`.

If lock removal fails: record blocker and HALT.
