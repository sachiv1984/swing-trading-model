Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-04

# Execution Escalations — 2026-11-03__release-v9.15

## ESC-EXEC-20261104-01

- **Raised at:** 2026-11-04T10:56:15Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start per `sprint_backlog.md` ST-01 Notes and `stage4_backlog_slice_addendum.md` ST-01, RISK-07)
- **ST/EPIC item:** ST-01 / EPIC-01 (BLG-FE-244)
- **Trigger type:** Strategy
- **Blocking statement:** ST-01 AC 2 says that with a risk-off or unknown regime "save requires the acknowledgement". `strategy_rules.md` §4.2.6 (binding) says the advisory panel "must never prevent, gate, or auto-reject" a submission and that any hard submission gate needs a new §13 review. §4.2.1 (v1.20) says new entries in an unknown-regime market "are blocked". The Trade Plan path's acknowledgement does not disable Save today. A dated ruling is needed: **Branch A (acknowledge to proceed)** — Submit is disabled until a WARN/FAIL is acknowledged; the ruling states that a one-click, user-passable acknowledgement is not a "hard submission gate" under §4.2.6 (and, if needed, clarifies §4.2.1's "are blocked" wording), applied as a case (c) `strategy_rules.md` write confirmed at seal; or **Branch B (advisory only)** — Submit stays enabled as on the plan path, and AC 2 is met by the regime check showing FAIL/unknown with the acknowledgement offered. Both are designed in `docs/design/2026-11-03__release-v9.15/trade-entry-pre-entry-checks/decision_record.md` §2.3.
- **Engine recommendation (non-binding):** see the in-session question; this is a strategy call.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling, Branch A or Branch B, recorded in this escalation's resolution and in ST-01's QA evidence. Under Branch A with a text clarification, the engine applies the case (c) `strategy_rules.md` write with its Change Log row and `STRATEGY_VERSION_REGISTRY` entry in the same commit.
- **SLA due-by:** 2026-11-07T10:56:15Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T11:00:36Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **Branch A, acknowledge to proceed.** On Trade Entry, when any pre-entry check is WARN or FAIL (including a risk-off or unknown regime), Submit is disabled until the user ticks the acknowledgement. A one-click, user-passable acknowledgement is not a "hard submission gate" under §4.2.6, and §4.2.1's "are blocked" for an unknown regime means the entry cannot be saved until the FAIL is acknowledged (or the regime is measured). The engine recommended Branch A: it carries out v1.20's fail-closed intent while keeping the decision with the user, as §3 requires. Applied by ST-01 as a case (c) `strategy_rules.md` write (§4.2.1, §4.2.6) with a Change Log row and a `STRATEGY_VERSION_REGISTRY` entry. ST-01 reclassified `autonomous`.
