Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03

---

## ESC-CLOSE-20260731-01

- **Raised at:** 2026-07-31T14:00:00Z
- **Routine:** Post-Ship Closure
- **Cycle ID:** 2026-07-30__release-v8.0
- **Step:** STEP 8 — Lessons Learnt Review and Application
- **ST/EPIC item:** N/A (governance prompt reconciliation, surfaced by Phase 4 friction item)
- **Trigger type:** Other (governance prompt disagreement)
- **Blocking statement:** `execution_prompt.md`'s EPIC-level sign-off consolidation step and `delivery_verification_prompt.md` STEP -1.3's recognised-format list disagree on what a compliant EPIC-level `Signed off by:` string looks like for `delegated_backend`/`delegated_decision`-heavy EPICs. At this cycle's delivery verification, `qa_evidence_EPIC-04.md` and `qa_evidence_EPIC-06.md` both recorded a named domain-authority signer (`Infrastructure & Operations Owner`; `Head of Engineering ... with Head of Specs Team concurrence`) rather than one of STEP -1.3's three recognised literal formats, requiring a one-time Director of Quality counter-sign remediation before verification could proceed. This is not blocking closure of this cycle (already remediated), but the underlying prompt disagreement remains open and will recur at the next EPIC dominated by delegated (non-autonomous-class) stories.
- **Owning authority:** Head of Specs Team
- **Unblock criteria:** Select one of two remediation paths and apply it as a governance prompt patch (with full CLAUDE.md §6 edit checklist): (a) extend `delivery_verification_prompt.md` STEP -1.3's recognised-format list with a fourth pattern for named domain-authority EPIC-level sign-off (e.g. `<Role> (human, <email>)` or `<Role> (agent-mediated)`), applicable only when the EPIC contains no `autonomous`-class stories requiring the DoQ/engine-signer paths; or (b) require `execution_prompt.md`'s EPIC sign-off consolidation step to always additionally record a literal `Director of Quality` line, even when the substantive review was performed by a named domain role.
- **SLA due-by:** 2026-08-03T14:00:00Z (72 hours from raise time, per `post_ship_closure.md` STEP 8's decision_required disposition rule)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** Option (a) selected and applied by Head of Specs Team (2026-08-03, within SLA). `delivery_verification_prompt.md` v3.5→v3.6: STEP -1.3 Tier 2 gains a fourth recognised sign-off format — a signer naming a specific human or agent-mediated domain-authority role (e.g. `Infrastructure & Operations Owner`, `Head of Engineering`, compound `<Role A> ... with <Role B> concurrence` forms, or execution_prompt.md §5.3's Infrastructure co-sign format) is accepted as compliant provided the EPIC contains no `autonomous`-class story; autonomous-class stories still require the literal DoQ/engine-signer paths. Full CLAUDE.md §6 edit checklist applied: version bumped, `delivery_verification_changelog.md` entry added, OPERATIONAL_GUIDE.md §9 header + §14 table + §14 change log all updated, `prompt_change_log.md` appended (2 rows). No DoQ counter-sign will be required for future EPIC-04/EPIC-06-shaped sign-offs unless the EPIC contains an autonomous-class story.
