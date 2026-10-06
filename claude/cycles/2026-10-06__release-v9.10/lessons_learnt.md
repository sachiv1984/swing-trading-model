Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-06

---

# Lessons Learnt — Release Planning 2026-10-06__release-v9.10

## Friction Items

**Friction Item 1: the gate scan counts a literal `**Gate criteria:** None` as a gate.** `scripts/scan_backlog_gate_conditions.py` marks an item gated whenever a Gate field is present, whatever it says. 17 P3 items (`BLG-GOV-178`, `-184`, `-185`, `-186`, `-189`, `-191`–`-196`, `-198`, `-200`, `-201`, `BLG-SPEC-77`, `BLG-OPS-105`, `BLG-QA-93`) say `None` and have stayed out of every ready pool on that basis. Nobody ever decided they were gated. This cycle kept the exclusion so its pool stays comparable with earlier cycles. In practice it is a silent exclusion rule. **Recommendation:** treat `None`/`N/A` as ungated in the script (or require those items to say "Opportunistic"/"Cadence" with a date). `BLG-GOV-373` (known-false-positive allow-list) is the natural vehicle. After that, `groom backlog` should confirm each of the 17 still deserves a slot.

**Friction Item 2: §1.3a's "clear or re-gate in place" instruction collides with the open write-scope escalation.** §1.3a tells Release Planning to edit a date-lapsed item's gate text once it has been read. `ESC-CLOSE-20261006-01` is the pending ruling on whether governed routines may edit existing `backlog.md` item fields. This cycle read all 8 date-lapsed items and recorded dispositions in `run_manifest.md` instead of editing. Two of the six "still gated" items (`BLG-FEAT-62`, `BLG-OPS-53`) are false-positive lapses: the date in their gate text is a counting start date, not a clearance date. They will reappear on every scan until their text is edited. **Recommendation:** the escalation's ruling should cover §1.3a's edits explicitly.

**Friction Item 3: four source items carried ACs that could not be met as written.** `BLG-GOV-140`/`141` had a 2026-09-24 deadline (already passed), `BLG-FE-193` had a "wait for BLG-BE-135" AC (already satisfied), and `BLG-GOV-357` named a `claude/roadmap/` destination (the escalated boundary). Each was restated in the slice and marked *(restated)*. The pattern is that gate-cleared items keep pre-clearance ACs. **Recommendation:** when a gate is cleared (as ST-19 did at v9.9), the same edit should refresh any AC that names the gate's date.

## Prompt Change Classification

No process patches proposed this cycle. Friction Items 1 and 3 are backlog/tooling recommendations. Friction Item 2 needs the already-tracked `ESC-CLOSE-20261006-01` ruling.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-10-06__release-v9.10",
  "phase": "Release",
  "filed_utc": "2026-10-06T12:50:00Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 3,
  "status": "Active"
}
```
