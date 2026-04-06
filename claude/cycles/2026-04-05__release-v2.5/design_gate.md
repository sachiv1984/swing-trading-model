**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-06
**Cycle:** 2026-04-05__release-v2.5

---

# Design Gate Record — 2026-04-05__release-v2.5

## Gate Status: PASSED

Completed: 2026-04-06
PMO Lead: confirmed
Head of UX & Design: confirmed

---

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Fix auth forwarding in POST /test/endpoints | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-02 | Sync endpoint test list with openapi.yaml | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-03 | Fix System Status endpoint categorisation | Design Pre-Approved | N/A (follows existing patterns) | `docs/specs/frontend/pages/system_status.md` v1.1 | ✅ Cleared |
| ST-04 | Review and document Reports page backend integration | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Review and document Signals page backend integration | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-06 | Investigate high external latency on DB-backed endpoints | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-07 | Add --max-time to GitHub Actions curl calls | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-08 | Fix Avg Slippage StatsCard gradient rendering | Design Pre-Approved | N/A (correcting DEV-ST14-01 — restoring approved gradient) | `docs/specs/frontend/pages/trade_history.md` v1.5 | ✅ Cleared |
| ST-09 | Fee drag metric on Trade History | Design Required | `docs/design/2026-04-05__release-v2.5/fee-drag/ux_spec.md` v1.0 | `docs/specs/frontend/pages/trade_history.md` v1.5 | ✅ Cleared |
| ST-10 | Fix governance_sync.yml batch push issue closure | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-11 | Formalise backlog entry placement standard | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-12 | Apply v2.4 deferred governance prompt patches | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-13 | Create test scenarios for EPIC-01 correctness fixes | Design Not Applicable | N/A | N/A | ✅ Cleared |

All 13 items classified. 0 blocked.

---

## Blocked Items

None — gate passed cleanly.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| ST-09 | UX Decision Record — Fee Drag Metric (Avg Fee Drag StatsCard + Fee Drag % column) | `docs/design/2026-04-05__release-v2.5/fee-drag/ux_spec.md` | Product Owner (2026-04-06) |

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version | Change |
|------|------|---------|--------|
| ST-03 | `docs/specs/frontend/pages/system_status.md` | v1.1 | No change required — existing spec covers categorisation patterns |
| ST-08 | `docs/specs/frontend/pages/trade_history.md` | v1.5 | Updated at design gate to include Fee Drag spec (ST-09 co-update) |
| ST-09 | `docs/specs/frontend/pages/trade_history.md` | v1.5 | Updated: Avg Fee Drag StatsCard (Summary Stats), Fee Drag % column (Table) |

---

## Notes

- Design gate run after Sprint Planning artefacts were produced (Sprint_Planning_In_Progress) — sprint was not sealed; sprint_sealed = false at gate entry. Consistent with design_gate_prompt.md §2 pre-condition (sprint_sealed = false).
- ST-08 (DEV-ST14-01 gradient fix): classified Design Pre-Approved since the gradient was part of the original approved design. Restoration of a known deviation requires no new design decision.
- ST-09 design decisions follow existing Trade History page patterns (StatsCard row, table column) with amber/neutral colour to distinguish fee drag from P&L direction colouring (green/red).
- With design_gate_status = Passed, the IMP-04 outstanding action in sprint_planning_notes.md is now resolved. `design_gate_bypass_authority` and `design_gate_bypass_reason` fields in .claude_current_state.json should be cleared (gate was run; no bypass occurred).
