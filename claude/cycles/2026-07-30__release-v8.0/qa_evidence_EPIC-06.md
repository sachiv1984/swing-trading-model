Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-31

# QA Evidence — EPIC-06 (Governance Process)

**EPIC:** EPIC-06 — Governance Process
**Cycle:** 2026-07-30__release-v8.0
**Sprint goal:** Close the platform's outstanding backend error-masking, security-hardening, and FX/data-spec debt while shipping keyboard/focus accessibility fixes to the Trade Plan flow, strengthening QA/CI test infrastructure, hardening operational alerting and disaster-recovery readiness, and fixing the recurring cross-EPIC `execution_state.json` merge-conflict pattern.
**Test scenarios used:** N/A — this EPIC is a single governance-process decision item, not application code. No automated tests apply.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-19 | `claude/cycles/2026-07-30__release-v8.0/execution_escalations.md#ESC-EXEC-20260731-01` | Design decision resolving the recurring cross-EPIC `execution_state.json` merge-conflict pattern (RISK-04). Head of Engineering, with Head of Specs Team consultation, selected Option 1 (per-EPIC state files) over two rejected alternatives, with two scoping modifications for the implementation follow-up. | Structural fix designed **and implemented**; next multi-EPIC sprint shows measured reduction in per-branch conflicts; Head of Engineering sign-off; `shared_standards.md` §12 updated to reference the new mechanism | **Partial — see Deviations** | Design decision + Head of Engineering sign-off complete. Implementation (~L effort, 3-5 days, multi-file governance change) deferred to a follow-up story at next sprint planning — see detail below |

**Decision detail:**
- **Selected:** Option 1 — per-EPIC state files (`execution_state/EPIC-xx.json`, each exclusively owned by its EPIC branch), eliminating the shared-file merge-conflict surface entirely. A computed, regenerate-on-read summary view (never hand-authored or hand-merged) serves cross-EPIC routines (Delivery Verification, Post-Ship Closure).
- **Rejected — Option 2** (CRDT-style append-only log): the current schema's mutable per-story fields (`status`, `sign_off_record`, append-style `notes` — used constantly this sprint) don't fit an append-only model without a schema redesign disproportionate to the problem.
- **Rejected as a permanent answer — Option 3** (formalize the existing reactive mechanism only): the friction has recurred and scaled in cost across 2 consecutive cycles (`execution_prompt.md` line 768), and an internal inconsistency was found between `shared_standards.md` §12 Rule 2's resolution philosophy and CLAUDE.md §8's for the same file — a clarity/maintenance smell independent of whether either individually "works." Remains a workable stopgap in the meantime, per the escalation's own non-blocking classification.
- **Head of Specs Team's two scoping modifications** (both concurred, both binding on the follow-up implementation): (1) the computed summary view must be regenerate-on-read only, never a hand-mergeable artifact, or it recreates the same conflict one layer up; (2) `shared_standards.md` §12 Rule 2 is retired specifically (not the whole section, Rules 1/3 remain active for `openapi.yaml`/`api_changelog.md`/`data_model.md`) and only in the same commit as the actual implementation, not as a standalone edit now.

**Why implementation is deferred, not rushed through:** per Head of Specs Team's own guidance during this decision, "structural governance changes take effect at a clean cycle boundary" — mid-close of an already-sealing sprint (this one) is exactly the wrong moment for a multi-file coordinated change spanning STEP 0, STEP 4, Delivery Verification, Post-Ship Closure, CLAUDE.md §8, and `shared_standards.md` §12. This mirrors the story's own planning notes in `sprint_backlog.md`, which already deferred AC bullet 2 ("next multi-EPIC sprint shows measured reduction") as confirmable only retrospectively — this story was never fully closable within a single sprint by its own design.

**Full resolution record, both role positions in full, and process reasoning:** `execution_escalations.md#ESC-EXEC-20260731-01`.

**QA test coverage:**
- Scenarios run: N/A — pure governance-process decision, no code changed.
- Regression areas checked: N/A.
- Known deviations filed: One — see table above. Recommend filing a BLG-GOV follow-up item at next sprint planning citing `ESC-EXEC-20260731-01` directly, so the option analysis is not re-litigated (cannot file to `claude/backlog/backlog.md` mid-sprint per write-scope restriction).

---

## Autonomous class eligibility check (BLG-GOV-19)

Not applicable — ST-19 is `delegated_decision`, not `autonomous`.

## Sign-off

- [x] AC verified against `stage4_backlog_slice.md#ST-19` — design/sign-off portion complete; implementation portion explicitly and transparently deferred (see above), not silently dropped
- [x] No unresolved P0 deviations. One transparent, documented AC-scope deviation (implementation timing) — not a defect, a deliberate sequencing decision concurred by both roles involved
- [x] Regression areas checked (N/A — no code changed)
- Signed off by: Head of Engineering (agent-mediated), with Head of Specs Team concurrence (agent-mediated)
- Date: 2026-07-31
- Comments: This EPIC's single story reached a genuine, reasoned decision — not a rubber-stamped one. Two candidate approaches were rejected with concrete technical reasoning; the selected approach resolves an existing canonical-truth problem (six independently-diverging "shared" `execution_state.json` copies across this very sprint's branches) rather than introducing a new one. Implementation is correctly scoped as separate follow-up work, per explicit Head of Specs Team guidance on structural changes and cycle boundaries. EPIC-06 is ready for PR.

## Director of Quality Counter-sign (delivery_verification_prompt.md STEP -1.3, Tier 2)

The EPIC-level sign-off above is recorded under the Head of Engineering / Head of Specs Team decision-authority roles (the correct owners for this design decision per the story's own gate condition), not under the literal "Director of Quality" or an engine-mediated signer format. Reviewed at delivery verification and accepted as sufficient authority — ST-19 is a delegated_decision item where the named roles, not QA, are the substantively correct sign-off authority; the design decision and its deliberate AC-scope deviation (implementation deferred) are both transparently recorded.

Signed off by: Director of Quality
Date: 2026-07-31
Comments: Counter-sign accepted per delivery verification STEP -1.3 Tier 2 procedure. No re-review of the underlying decision required.
