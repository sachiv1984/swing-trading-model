Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-06

---

# Lessons Learnt — Release Planning 2026-11-06__release-v9.16

## Friction Items

**Friction Item 1: §1.4c step 0 holds later phases but does not seat the current one.** `ESC-CLOSE-20261106-02`'s ruling (v2.72) worked as intended on first use. It held the 8 Phase 3 items, including P2 `BLG-FE-260`, with no Product Owner override. But the current phase's P3 items get no tier. The release was named "Site Structure & Usability, Phase 2", yet the oldest-first round-robin would not have reached `BLG-FE-251`, `252` and `253`, all filed 2026-11-03. Phase 2 would then have finished in v9.17 alongside Phase 3. The Product Owner seated them by override. The same will recur at v9.17 for Phase 3's six P3 items. Recommendation: when the release being planned is the provisional release of a DL-recorded programme phase, seat that phase's ready P3/P4 items as a tier after P1/P2. This mirrors step 0, which holds later phases out. Deferred to the Head of Specs Team (`release_planning_prompt.md` §1.4c) with the Product Owner.

**Friction Item 2: in-place gate clears surface the oldest items first, with scope written for an older app.** v9.15 ST-37 taught the gate scan to read roadmap feature IDs. Its first run here listed 5 items gated only on PT-04, which shipped at v6.1, 21 releases ago. Cleared in place, they are the oldest-filed items in the pool (2026-05-21), so oldest-first ordering seated all five ahead of everything else (7.50d). Each AC asked for the gate to be "verified before sprint planning", and each scope was written against the v6.1 app. The slice restates those ACs as a confirmation at the seal, and RISK-06 sequences the tests after EPIC-02. Observation: a one-off backlog of long-cleared feature gates, not a recurring pattern. The next `groom backlog` should check the 14 remaining feature-ID gates for the same staleness. No prompt change is proposed.

**Friction Item 3: `Provisional-Target` text can contradict a cleared gate.** `BLG-OPS-48`'s gate was cleared at v9.15, but its `Provisional-Target` still reads "~v4.9 (date-gated)", so the scan lists it as a data-quality warning. §1.3a's edit bounds (bound 2) allow only the Gate field and its note, so Release Planning cannot fix it. Recommendation: when §1.3a clears a gate, the same dated note should be allowed to replace gate language in `Provisional-Target` with "TBD". Alternatively, `groom backlog` corrects it. Deferred to the PMO Lead (`groom backlog`), since the item itself should be bannered under ST-28.

## Prompt Change Classification

No action-now patches. Friction Item 1 is a deferred patch. Friction Item 2 is an observation for `groom backlog`. Friction Item 3 is a deferred patch, with `groom backlog` as the interim fix.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-11-06__release-v9.16",
  "phase": "Release",
  "filed_utc": "2026-11-06T17:17:27Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 2,
  "status": "Active"
}
```
