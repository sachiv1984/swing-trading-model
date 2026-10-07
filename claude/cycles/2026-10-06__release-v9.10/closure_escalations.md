Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-07 (ESC-CLOSE-20261007-01 filed at post-ship closure STEP 8)
Cycle: 2026-10-06__release-v9.10

---

# Closure Escalations — 2026-10-06__release-v9.10

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20261007-01

| Field | Value |
|-------|-------|
| Issue | `lessons_learnt.md` (Release Planning) Friction Item 2 (`2026-10-06__release-v9.10`). `release_planning_prompt.md` §1.3a tells Release Planning to clear or re-gate a date-lapsed backlog item's gate text in place once read. `ESC-CLOSE-20261006-01`'s resolution and the `BLG-GOV-362` ruling (`execution_prompt.md` v3.83 §7, `sprint_planning_prompt.md` v3.20/v3.21) cover in-sprint writes authorised by a sealed AC only. The `ESC-CLOSE-20261006-01` resolution summary states that "Release Planning §1.3a in-place gate edits are not covered". So v9.10 Release Planning read 8 date-lapsed items and recorded dispositions in `run_manifest.md` without editing. Two false-positive lapses (`BLG-FEAT-62`, `BLG-OPS-53`: the gate date is a counting start date, not a clearance date) will reappear on every scan until their gate text is edited. |
| Type | Decision required — write-scope authority gap (`post_ship_closure.md` STEP 8 `decision_required`) |
| Escalated to | Head of Specs Team (with Product Owner, as backlog owner) |
| Reason | The decision is whether, and how far, Release Planning may edit an existing `backlog.md` item's `Gate criteria` field under §1.3a. Options: (a) authorise §1.3a gate-text edits directly, limited to the Gate field and recorded in `run_manifest.md`; (b) route them to `groom backlog`'s own write scope; (c) keep the read-only practice, and have `scan_backlog_gate_conditions.py` read a known-false-positive allow-list (`BLG-GOV-373`). This is a write-scope authority call, so the closure engine cannot make it. |
| Tracking | SLA 2026-10-10T12:00:00Z (72h from filing). Related: `BLG-GOV-373`, `BLG-GOV-362` (resolved). Non-blocking: the next `plan release` can proceed with the read-only practice. |
| Disposition | Open |
| Filed | 2026-10-07T11:19:46Z |
