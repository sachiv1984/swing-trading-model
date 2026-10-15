Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-15 (ESC-CLOSE-20261015-01 disposition set to Resolved — Head of Specs Team ruling, option (a), BLG-GOV-390 filed)
Cycle: 2026-10-12__release-v9.12

---

# Closure Escalations — 2026-10-12__release-v9.12

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20261015-01

| Field | Value |
|-------|-------|
| Issue | A deferred patch has been carried for 3 cycles with no change applied and no tracking item that covers it. v9.10 Release Planning Friction Item 1 asked `scripts/scan_backlog_gate_conditions.py` to treat a literal `Gate criteria: None`/`N/A` as ungated, then to confirm each affected P3 item still deserves a slot. The v9.10 and v9.11 closures both named `BLG-GOV-373` as its vehicle. Read directly at this closure, `BLG-GOV-373`'s scope is only a known-false-positive allow-list for date-lapse matches (`BLG-OPS-53`, `BLG-FEAT-92`). It does not mention `None`/`N/A` gate values, so the "folded" vehicle does not cover the patch. The script still has no `None`/`N/A` handling. |
| Type | Recurrence — `lessons_learnt_prompt.md` §3.7: a deferred patch carried two or more cycles without being applied is a recurrence escalation |
| Escalated to | Head of Specs Team (with Head of Engineering, as script owner) |
| Reason | The closure engine cannot write `scripts/` or add a non-Phase-4 backlog item. The fix needs a decision on its vehicle: (a) file a dedicated backlog item for `None`/`N/A` gate handling with a sprint target; (b) widen `BLG-GOV-373`'s scope and ACs to include it; or (c) withdraw the patch with a stated reason. |
| Tracking | SLA 2026-10-18T15:01:43Z (72h from filing). Related: `BLG-GOV-373`, v9.11 `closure_record.md` §6 row 5. Non-blocking: the next `plan release` can proceed by reading `None`/`N/A` gates by hand. |
| Disposition | Resolved — 2026-10-15T16:02:47Z |
| Resolved by | Head of Specs Team (agent-mediated per `execution_prompt.md` §5.3, on explicit user direction 2026-10-15; role ownership checked per the CLAUDE.md §2 role-ownership rule: the escalation's owner is the Head of Specs Team) |
| Resolution | **Option (a): dedicated backlog item `BLG-GOV-390`** (P2, Provisional-Target v9.13, owners Head of Engineering and Head of Specs Team). The defect is live: a re-run of the scan at ruling time showed 17 active items with a literal `Gate criteria: None` reported as gated (`BLG-GOV-178`–`201` series, `BLG-SPEC-77`, `BLG-OPS-105`, `BLG-QA-93`), so they are silently dropped from every Release Planning ready pool. P2 rather than P3 for that reason. Option (b), widening `BLG-GOV-373`, was rejected: that item fixes a different problem (date-lapse false positives) and merging the two would blur both ACs. Option (c), withdrawal, was rejected because the defect is still live. `BLG-GOV-373` keeps its own scope. The deferred patch now has a covering vehicle, so it leaves the closure's carried deferred-patch list. |
| Filed | 2026-10-15T15:01:43Z |
