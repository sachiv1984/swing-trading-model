Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-17
Cycle: 2026-07-17__release-v7.4

---

# Lessons Learnt — Post-Ship Closure

## Closure-Phase Observations

- No document gaps surfaced during closure. Scope document, decisions record, `System_status_report.md`, and `docs/specs/Specs_Index.md` were all found accurate and current on first read — only the routine scope/decisions Superseded flip and roadmap/backlog reconciliation writes were needed.
- No deviation compliance corrections were required (STEP 5 N/A — zero deviations filed this cycle; confirmed independently across `sprint_close.md`, `qa_evidence_EPIC-01.md`, and the governing spec document's own "Known Deviations: None" section).
- No new Specs Index gaps identified from this cycle's delivery (STEP 7) — `verification_report.md §6` recorded no test coverage gaps (short-circuited `not_applicable`, no frontend-visible change), and no canonical spec compliance issues were surfaced by ST-01's readiness-pass work.
- STEP 7.3 TSG reconciliation: no open §27 (or later) Test Coverage Gap entries reference this cycle's shipped scope; nothing to flip Open → RESOLVED this run.
- Endpoint Coverage Drift advisory (STEP 6): re-verified openapi.yaml vs. `api_performance_baseline.md` — pre-existing gap (tracked under `BLG-OPS-111`, filed v7.2 closure) is unchanged; v7.4 shipped zero new backend endpoints (readiness-pass-only cycle — `package.json`/`package-lock.json` and documentation changes only), so no new drift was introduced and no new backlog item was filed.

## Consolidated Action Summary (STEP 8)

**Immediate actions applied: 5** (all confirmations/closures — no template or prompt document required editing this run)

1. `lessons_learnt.md` (Release Planning) Friction Item 2 — user-invocation-named-shipped-release catch: confirmed no prompt change needed; the session-level pre-execution state check that caught it is sufficient and requires no `release_planning_prompt.md` edit.
2. `lessons_learnt.md` (Release Planning) Carry-Forward item 1 (RISK-05, `BLG-GOV-250`) — confirmed resolved: `design_gate.md` records both `BLG-FE-115` and `BLG-FE-118` §13 pre-checks as PASS. Carry-forward item is closed; no further action.
3. `lessons_learnt_cycle.md` Amendment Item A (`AMD-20260717-01` scope reduction) — action-now item; confirmed already fully applied (the amendment itself). No further action.
4. `lessons_learnt_cycle.md` Phase 3 friction log item — "clean execution, continue pattern" (type A, monitor). Confirmed pattern held this cycle; no action required.
5. `lessons_learnt_cycle.md` Phase 4 friction log item — "clean verification pass, continue pattern" (type A, monitor). Confirmed pattern held this cycle; no action required.

**Deferred to next cycle: 3**

1. `lessons_learnt.md` Friction Item 1 — governance-input items filed with an "ahead of next invocation" deadline should be tracked with a due-date reminder, not just a `Provisional-Target` field. Owner: Head of Specs Team. Target cycle: opportunistic — next cycle a similarly-dated governance-input item is filed; no concrete mechanism yet specified, needs further definition before it can be applied as a template edit.
2. `lessons_learnt_cycle.md` Amendment Item B — when `BLG-FE-116` (custom price alerts) is re-scoped into a future release, the Product Owner must explicitly assign Head of UX & Design artefact production rather than assuming it is covered by a readiness-pass story (this release had zero design-artefact production scheduled for it anywhere in the plan). Owner: Product Owner. Target cycle: next release scoping `BLG-FE-116`.
3. `lessons_learnt_cycle.md` Amendment Item C — consider a Release Planning STEP check that flags, at release-planning time (not first discovered at Design Gate), any case where a Design Required item's UX-spec production is scheduled inside another item's acceptance criteria rather than as a pre-sprint deliverable. Owner: Head of Specs Team. Target: unscheduled — candidate backlog item (not filed this run; write scope for `backlog.md` at post-ship closure is limited to shipped-item completion and Phase 4 additions).

**Escalated for decision: 0**

## Process Improvements Applied Immediately

None — no action item this run required a template, prompt, or process document edit (all immediate-class items were confirmations of already-resolved conditions).

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Governance-input items filed with an "ahead of next invocation" deadline are not tracked with a due-date reminder mechanism, only a `Provisional-Target` field — a repeat of the `BLG-GOV-248` gap could recur for any future dated governance-input item. | Head of Specs Team should define a concrete tracking mechanism (or confirm none is warranted) before the next such item is filed. | Roadmap Rebalance / Release Planning |
| 2 | `BLG-FE-116` (custom price alerts) has no design-artefact production scheduled anywhere in the current plan for any future release it re-enters. | Product Owner must explicitly assign Head of UX & Design artefact production when `BLG-FE-116` is next scoped — do not assume a readiness-pass story covers it. | Release Planning |
| 3 | No structural cross-check exists between Release Planning and Design Gate to catch a Design-Required item's UX-spec production being scheduled as in-sprint work of another item (the exact pattern `AMD-20260717-01` had to correct for `BLG-FE-115/116/117/118`). | Consider a Release Planning STEP check flagging this pattern explicitly at planning time. Candidate backlog item — not yet filed. | Release Planning / Design Gate |
