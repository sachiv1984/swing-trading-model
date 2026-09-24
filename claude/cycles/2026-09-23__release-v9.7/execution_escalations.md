Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-24

# Sprint Execution Escalations — 2026-09-23__release-v9.7

## ESC-EXEC-20260924-01

- **Raised at:** 2026-09-24T07:07:54Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-23__release-v9.7
- **Step:** STEP 0 / 3.1.D
- **ST/EPIC item:** ST-01 / EPIC-01
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-01 (PO-05 Lightweight Replay Mode) is classified `delegated_backend`-eligible in principle (backend replay mechanics is the core blocking layer), but per the backend delegation note (execution_prompt.md §5.1) a canonical spec must be locked before delegation. The only frontend artefact, `docs/specs/frontend/pages/replay_mode.md` v0.1, is explicitly "Design Only, Implementation Pending" and the design gate record (`claude/cycles/2026-09-23__release-v9.7/design_gate.md`) states the exact wire contract is deferred to this item's own scope-confirmation sub-story (Binding Condition 6 of `docs/product/decisions/po05_section13_preassessment.md`). No lockable backend spec exists yet, so the item is reclassified `delegated_decision` rather than `delegated_backend` per §5.1's explicit fallback rule.
- **Owning authority:** Head of Specs Team
- **Unblock criteria:** Head of Specs Team runs the scope-confirmation sub-story (binding conditions from the §13 pre-assessment), locks the backend wire contract (API shape for the replay run endpoint, request/response schema, determinism guarantees), and publishes it as a canonical spec (e.g. `docs/specs/api_contracts/replay_endpoints.md` or an addendum to `replay_mode.md`). Once locked, ST-01 may be reclassified `delegated_backend` and handed to Head of Engineering with a full §3.1.B delegation record.
- **SLA due-by:** 2026-09-25T07:07:54Z
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**
