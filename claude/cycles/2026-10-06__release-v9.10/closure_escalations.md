Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-07 (ESC-CLOSE-20261007-01 disposition set to Resolved — Head of Specs Team ruling, release_planning_prompt.md v2.60)
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
| Disposition | Resolved — 2026-10-07 |
| Resolved by | Head of Specs Team (agent-mediated per `execution_prompt.md` §5.3, on explicit user direction 2026-10-07; role ownership checked per the CLAUDE.md §2 role-ownership rule) |
| Resolution | **Option (a), narrowed.** Root cause: `release_planning_prompt.md` §7 limited `backlog.md` writes to the "release slice only", while §1.3a instructed in-place clear/re-gate edits, so the two contradicted each other. §7 gains a named gate-field carve-out. §1.3a gains 6 bounds: (1) date-lapsed items read this run only; (2) the `**Gate criteria:**` field plus one dated note only, with no other field and no section move; (3) clearing must cite evidence, because a lapsed date is not evidence; (4) re-gating restates the *same* condition with a correct clearance date or threshold, which covers false-positive lapses such as `BLG-FEAT-62` and `BLG-OPS-53`; loosening, tightening or replacing a condition stays with Roadmap Rebalance and the PO; (5) ACs naming a cleared gate are listed in the note, not edited, and are restated in the slice when seated; (6) every edit is disclosed in `run_manifest.md` and the PO sign-off summary. Option (b), routing to `groom backlog`, was rejected: it would leave the lapse in place for the whole Release Planning run that reads it. Option (c), an allow-list only, was rejected as insufficient on its own: it hides false positives but never corrects the source text. `BLG-GOV-373` stays a complementary, optional fix. This ruling also settles v9.10 Release Planning Friction Item 3 (refresh ACs on gate clearance): ACs are not edited. Applied in `release_planning_prompt.md` v2.59→v2.60, `OPERATIONAL_GUIDE.md` v4.226→v4.227 and `prompt_change_log.md`. |
| Filed | 2026-10-07T11:19:46Z |
