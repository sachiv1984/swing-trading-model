Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-23

---

## ESC-CLOSE-20260923-01

- **Raised at:** 2026-09-23T16:00:00Z
- **Routine:** Post-Ship Closure
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** STEP 8 — Lessons Learnt Review and Application
- **ST/EPIC item:** N/A (Release Planning lessons_learnt.md Friction Item 2)
- **Trigger type:** Strategy
- **Blocking statement:** `release_planning_prompt.md` §1.4c's oldest-filed-first round-robin ranks items with no explicit horizon tag above items self-declared `Provisional-Target: v<current release>`. At v9.6 this left 12 of 16 `v9.6`-tagged ready items (4.80 days) unselected, including follow-ups filed against v9.5's own shipped work. No Product Owner override was given for this cycle, so none was applied — the silence is unexplained to a future reader of the selection.
- **Owning authority:** Product Owner (with Head of Specs Team)
- **Unblock criteria:** A ruling on one of: (a) add an explicit horizon-tag tier to §1.4c (tagged-for-this-release items seated after P2, before round-robin), or (b) state explicitly that an unselected `v<current>` tag is expected to be cleared at post-ship groom instead.
- **SLA due-by:** 2026-09-26T16:00:00Z
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:** *(complete when resolved)*

---

## ESC-CLOSE-20260923-02

- **Raised at:** 2026-09-23T16:00:00Z
- **Routine:** Post-Ship Closure
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** STEP 8 — Lessons Learnt Review and Application
- **ST/EPIC item:** N/A (lessons_learnt_cycle.md Phase 4 friction item 2)
- **Trigger type:** Strategy
- **Blocking statement:** `delivery_verification_prompt.md §7`'s `LL-v9.1-P4-01` "or equivalent" evidence clause was written narrowly for *Resolved* deviations with no natural canonical-spec Known Deviations home. This cycle's verification report applied its reasoning by extension to three *open* P2/P3 deviations (`BLG-BE-127`, `BLG-BE-128`, `DEV-EPIC05-ST21-01`) — a defensible reading, but an interpretive extension beyond the clause's own literal scope, applied without a prior ruling.
- **Owning authority:** Head of Specs Team
- **Unblock criteria:** A ruling on whether `LL-v9.1-P4-01`'s "or equivalent" clause should be reworded to state explicitly that it covers open (not only resolved) deviations with no natural canonical-spec home, or whether open deviations of this shape require a different evidence standard.
- **SLA due-by:** 2026-09-26T16:00:00Z
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:** *(complete when resolved)*
