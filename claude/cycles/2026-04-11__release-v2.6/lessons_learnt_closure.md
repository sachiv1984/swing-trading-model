**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-04-13
**Cycle:** 2026-04-11__release-v2.6
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Lessons Learnt — Post-Ship Closure — v2.6

---

## Summary

This record covers the post-ship closure run for cycle `2026-04-11__release-v2.6` (v2.6). It consolidates lessons from all three source records: Release Planning (`lessons_learnt.md`), Sprint Execution and Delivery Verification (`lessons_learnt_cycle.md` Phases 3 and 4). Immediate actions applied: 0. Deferred actions carried forward: 5.

---

## Immediate Prompt / Template Fixes Applied

None applied this run.

All action items from the cycle lessons records were explicitly classified `defer` by the originating engine at time of filing. No item meets the "unambiguous, no-authority-decision-required" threshold for immediate prompt change. Prompt changes for BLG-GOV-17, BLG-GOV-18, and BLG-GOV-19 are deferred pending named authority involvement (Head of Specs Team, Director of Quality).

---

## Prompt Changes Applied

None.

If none: "None applied this run."

---

## New files created this run

- `claude/cycles/2026-04-11__release-v2.6/closure_state.json` — closure tracking state (created at STEP 0)
- `claude/cycles/2026-04-11__release-v2.6/closure_record.md` — post-ship closure record (created at STEP 9)
- `claude/cycles/2026-04-11__release-v2.6/lessons_learnt_closure.md` — this file

---

## Document Closure Friction

| Document | Friction | Resolution |
|----------|---------|------------|
| `claude/backlog/backlog.md` | Duplicate BLG-QA-11 ID — System Status spec (line 363) and Playwright intercept failure (line 933) share the same ID. Pre-existing conflict not introduced this cycle. | Flagged in closure record §6 Outstanding Actions. PMO Lead to resolve ID conflict at backlog groom. |
| `docs/product/scope/scope--v2.6...md` | None | Superseded normally |
| `docs/product/decisions/decisions--2026-04-11__release-v2.6.md` | None | Superseded normally |

---

## Lessons Learnt Action Application Rate

| Source | Total items | Immediate | Deferred | Escalated | Backlog items filed |
|--------|------------|-----------|----------|-----------|---------------------|
| lessons_learnt.md (Release Planning) | 1 | 0 | 1 | 0 | 0 |
| lessons_learnt_cycle.md Phase 3 | 4 | 0 | 4 | 0 | 4 (BLG-GOV-17, BLG-GOV-18, BLG-GOV-19, BLG-QA-11) |
| lessons_learnt_cycle.md Phase 4 | 3 | 0 | 3 | 0 | 0 (same items, already filed Phase 3) |
| **Total** | **8** | **0** | **5 unique** | **0** | **4** |

Application rate for `immediate` class: N/A — 0 items were classified immediate.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `execution_prompt.md` | §3.2.B (Open PR step) | Gate PR creation on non-blank DoQ sign-off Date in `qa_evidence_EPIC-xx.md` | Director of Quality | v2.7 (BLG-GOV-18) |
| `execution_prompt.md` | Sprint close trigger | Implement mechanism to prevent STEP 5 being skipped when PRs are merged outside engine session | Head of Specs Team | Before v2.7 planning (BLG-GOV-17 — P1, escalated) |
| `execution_prompt.md` | §3.2.A | Define autonomous DoQ sign-off class for code-review-only EPICs | Director of Quality | v2.7 (BLG-GOV-19) |
| `delivery_verification_prompt.md` | STEP -1.3 Tier 2 check | Recognise autonomous DoQ class as compliant sign-off | Director of Quality | v2.7 (BLG-GOV-19) |

---

## Escalations

None.

BLG-GOV-17 was escalated to Head of Specs Team during delivery verification (third recurrence — per `lessons_learnt_prompt.md §3.7`). That escalation is recorded in `lessons_learnt_cycle.md` Phase 4. No new escalation required at closure.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Sprint Close STEP 5 has now been skipped three consecutive cycles when PRs are merged on GitHub outside the engine session. BLG-GOV-17 is P1 and requires Head of Specs Team implementation before v2.7 planning. | Check at Sprint Planning STEP -1 whether BLG-GOV-17 has been resolved; if not, flag as open risk before accepting sprint seal. | Sprint Planning |
| 2 | BLG-QA-11 (Playwright page.route() intercept failure) has now affected SC-REP-01–04, SC-SIG-CB-01–02, SC-FEE-01–04 across v2.5 and v2.6. Resolution unblocks multiple existing structurally-correct specs. | At Sprint Planning, check if BLG-QA-11 is scoped into v2.7; if not, flag the growing test coverage debt to the Product Owner. | Sprint Planning |
