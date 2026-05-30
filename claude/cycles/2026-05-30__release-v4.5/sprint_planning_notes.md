**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.5

---

# Sprint Planning Notes — 2026-05-30__release-v4.5

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-30__release-v4.5/stage4_backlog_slice.md`

No amendment slice present (`amended_backlog_slice_path` = "").

---

## Carry-Forward Items

Carry-forward items reviewed: 2 items from cycle `2026-05-29__release-v4.4`

| # | Observation | Implication | Resolution in v4.5 |
|---|-------------|-------------|---------------------|
| 1 | Empty spec_references for doc-creation stories has recurred 3+ times (v4.3 Phase 4, v4.4 Phase 3, v4.4 Phase 4) | At sprint planning: confirm BLG-GOV-70 is in scope (or escalate) | ✓ BLG-GOV-70 = ST-04 in EPIC-01 Sprint 1 — addressed |
| 2 | BLG-GOV-19 criterion 1 gap surfaced for first time in a pre-planning sprint (v4.4 EPIC-02/03) | At sprint execution: confirm execution_prompt.md has verification-class sub-criterion before scheduling delegated pre-planning stories | ✓ BLG-GOV-77 = ST-03 in EPIC-01 Sprint 1 — addressed |

---

## Capacity WARN Acknowledgement

Capacity check verdict: WARN (inherited from release plan stage4_5_capacity_check).

**WARN reason:** Sprint 2 conditional uncertainty — if SI-02 gate not met, Sprint 2 has no firm stories and the cycle closes with Sprint 1 only (5 stories). Sprint 1 effort (~4.5 hrs / ~0.6 days) is well within capacity. Sprint 2 conditional effort (~20–28 hrs / ~2.5–3.5 days) is within capacity if gate is met.

**Product Owner acknowledgement:** Confirmed 2026-05-30. Sprint 1 proceeds. Sprint 2 gate decision (SI-02 20-closed-trades confirmation) to be resolved before Sprint 2 seal.

---

## Pre-Sprint Vulnerability Scan

pip-audit -r backend/requirements.txt: **0 vulnerabilities** — clean.

---

## Dependency Map

### Sprint 1

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | None | — | No dependency |
| ST-02 | None | — | No dependency |
| ST-03 | None | — | No dependency |
| ST-04 | None | — | No dependency |
| ST-05 | None | — | No dependency |

No cross-item dependencies within Sprint 1. EPIC-01 stories (ST-01–04) all modify execution_prompt.md and must be applied in the same EPIC-01 commit to minimize version bump overhead (per release plan EPIC-01 notes). This is a packaging decision, not a dependency.

### Sprint 2 (Conditional)

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-06 | PO gate confirmation | External (gate) | Unresolved at Sprint 1 seal |
| ST-07 | ST-06 (§13 PASS) | Internal | Blocked until ST-06 completes with PASS |
| ST-08 | ST-07 (metric definition) | Internal | Informed by (not hard-blocked) — can proceed in parallel after ST-06 PASS but benefits from ST-07 metric context |

---

## Execution Sequence

### Sprint 1 (Firm)

1. **EPIC-02** (ST-05) — Agent file header standardization
   - First in merge order: no governance file edits, no version bumps
   - `execution_state.json` owner: EPIC-02 (first EPIC to merge)
   - All content autonomous; Head of Specs Team

2. **EPIC-01** (ST-01, ST-02, ST-03, ST-04) — Execution prompt hardening
   - Second in merge order: all §6 governance file edit checklist steps applied
   - EPIC-01 branch must rebase onto main after EPIC-02 merges before finalizing
   - All 4 stories packaged in a single EPIC-01 commit to minimize version bump overhead
   - All content autonomous; Head of Specs Team

### Sprint 2 (Conditional — gate required)

3. **EPIC-03** (ST-06 → ST-07 → ST-08) — SI-02 Spec Pre-Sprint Completion
   - Gate: PO explicit confirmation that SI-02 sprint planning is imminent
   - ST-06 (§13 boundary review) → ST-07 (drift score metric) → ST-08 (data schema)
   - All items `delegated_decision` — Sprint 2 seal requires PO gate confirmation first
   - If gate not confirmed by Sprint 2 seal: EPIC-03 deferred; cycle closes with Sprint 1 only

---

## Multi-EPIC Execution Notes

Sprint 1 has 2 EPICs. Ownership and sequencing:

- **execution_state.json owner:** EPIC-02 (first in merge order — EPIC-02 → EPIC-01)
- **Shared files across EPICs:** None — EPIC-01 modifies `claude/system/execution_prompt.md`, `OPERATIONAL_GUIDE.md`, `claude/system/prompt_change_log.md`; EPIC-02 modifies 5 agent files in `claude/agents/`. No file overlap.
- **Rebase requirement:** EPIC-01 branch must rebase onto `main` after EPIC-02 merges before finalizing its PR

---

## Planning-Deferred Item Traceability

Per AUD-2026-05-21-002, the following ST items from `stage4_backlog_slice.md` are NOT included in the sealed sprint backlog and must be recorded as `deferred_at_planning` in `execution_state.json` at Phase 3 initialisation:

```yaml
epics:
  EPIC-03:
    stories:
      ST-06:
        status: deferred_at_planning
        gate_condition: "PO confirmation that SI-02 sprint planning is imminent not confirmed at Sprint 1 planning seal"
      ST-07:
        status: deferred_at_planning
        gate_condition: "PO confirmation that SI-02 sprint planning is imminent not confirmed at Sprint 1 planning seal; depends on ST-06 §13 PASS"
      ST-08:
        status: deferred_at_planning
        gate_condition: "PO confirmation that SI-02 sprint planning is imminent not confirmed at Sprint 1 planning seal; informed by ST-07 metric definition"
```

**Execution engine instruction:** Include these entries when initialising `execution_state.json` in Phase 3 STEP 1. This ensures Phase 4 delivery verification STEP 1 can account for all 8 slice items without a traceability gap.

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — 4 stories packaged in single EPIC-01 commit; §6 checklist applied once; OPERATIONAL_GUIDE §14 updated in final commit |
| RISK-02 | EPIC-02 | Valid — single story, single commit, cosmetic-only agent file edits; no version bumps required |
| RISK-03 | EPIC-03 | Accepted — EPIC-03 conditional; gate not confirmed at Sprint 1 seal; no blocking dependency on Sprint 1 |

---

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-06 | EPIC-03 | Gate condition: PO confirmation that SI-02 sprint planning is imminent — not confirmed at Sprint 1 planning seal | Yes (Sprint 2 — conditional) |
| ST-07 | EPIC-03 | Gate condition: same as ST-06; additionally depends on ST-06 §13 PASS | Yes (Sprint 2 — conditional) |
| ST-08 | EPIC-03 | Gate condition: same as ST-06; informed by ST-07 metric definition | Yes (Sprint 2 — conditional) |

All deferred items remain in `claude/backlog/backlog.md` at their current status. No backlog modifications made during sprint planning.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Confirm SI-02 20-closed-trades gate status; provide explicit PO go/no-go for EPIC-03 before Sprint 2 planning seals | Product Owner | No (before Sprint 2 seal, not Sprint 1 seal) |

No outstanding actions block Sprint 1 seal.

---

## Delegation Classification Notes

All Sprint 1 stories are classified `autonomous`:

- **ST-01 (autonomous):** Governance prompt edit; document inspection verification; no UX change; no human sign-off required mid-task.
- **ST-02 (autonomous):** Governance prompt edit; document inspection verification; same classification rationale as ST-01.
- **ST-03 (autonomous):** Governance prompt edit; document inspection verification; same classification rationale as ST-01.
- **ST-04 (autonomous):** Governance prompt edit; document inspection verification; same classification rationale as ST-01.
- **ST-05 (autonomous):** Agent file header edits; cosmetic only; document inspection verification; no design decisions required. Fast-path per BLG-GOV-72.

Sprint 2 stories (ST-06, ST-07, ST-08) are all `delegated_decision` — require human domain owners. This is recorded in the sprint backlog for the amendment cycle if EPIC-03 is activated.
