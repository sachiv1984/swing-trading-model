Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-17__release-v7.5

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-17__release-v7.5
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-20
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| All four EPICs registered new endpoints in the same set of shared files (`backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js`, `docs/specs/data_model.md`, `docs/ops/api_performance_baseline.md`, `docs/reference/openapi.yaml`) — every EPIC after the first hit a guaranteed cross-EPIC merge conflict against main, requiring two full CLAUDE.md §8 resolution passes this sprint (EPIC-03 vs EPIC-02, then EPIC-04 vs EPIC-02+EPIC-03) | Phase 3 | C | defer | Process worked as designed (CLAUDE.md §8 resolved both conflicts cleanly with no data loss), but the underlying pattern is now recurrent across cycles (also seen in 2026-07-10__release-v6.9's sprint_close.md). Consider a structural fix — e.g. splitting the endpoint test registry and performance baseline into per-EPIC append-only manifest files aggregated at build/CI time — to remove the shared-file collision surface entirely, rather than continuing to resolve it manually each multi-EPIC sprint. | Head of Engineering | next roadmap review |
| A real regression was caught during EPIC-04's own DoQ verification pass: pre-existing `tests/e2e/net-r-trade-history.spec.js` crashed because the newly-mounted components called `.map()` on `json.data \|\| []`, which does not guard against a non-array truthy `data` value returned by the test suite's generic catch-all mock. The same weak-guard pattern (`json.data \|\| []` instead of `Array.isArray(json.data) ? json.data : []`) was independently reused across at least two of this sprint's four EPICs before being fixed in EPIC-04 | Phase 3 | D | defer | Not fixed as a repo-wide sweep this sprint (out of scope — only the two call sites causing the actual failure were patched). Recommend a coding-standard note (or lint rule) requiring `Array.isArray(...)` guards on any `.map()`/`.filter()` call over a JSON API response field, to catch this class of bug before Playwright does. | Head of Engineering | next roadmap review |

**Recurrence Notes:**
The shared-registration-file conflict pattern (friction item 1) recurred from the 2026-07-10__release-v6.9 cycle, where the same file set (endpoint test registry, performance baseline, data model) produced an analogous EPIC-02-vs-EPIC-01 conflict, resolved the same way. This is the second consecutive multi-EPIC sprint to hit it — worth escalating from "resolve each time" to "consider removing the collision surface," per the action column above.

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-07-17__release-v7.5
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-20
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-07-17__release-v7.4 (`lessons_learnt_cycle.md` `## Phase 4`) — clean pass, `monitor` classification, no outstanding action carried. No recurrence.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `qa_evidence_EPIC-02.md`'s Result column used a third disposition value, "Deferred to staging", for ST-02's live-delivery-firing AC — but `delivery_verification_prompt.md` STEP 2.1 only names `Pass` / `Pass with notes` / `Fail` as valid Result values. The verifying pass had to reason by cross-reference (CLAUDE.md §2, `shared_standards.md §16.11`, the confirmed pre-PR `BLG-QA-115` filing) that this is a recognised, separately-governed disposition and not equivalent to a blocking `Fail`, rather than the prompt text itself confirming this. | Phase 4 | A | defer | Add "Staging-deferred (per CLAUDE.md §2 / `shared_standards.md §16.11`)" as an explicitly accepted STEP 2.1 Result value, alongside `Pass`/`Pass with notes`/`Fail`, conditioned on a confirmed pre-PR backlog item — not a verification blocker when that condition holds. | Head of Specs Team | next roadmap review |
| All four `qa_evidence_EPIC-xx.md` Standard Sign-Off Blocks this cycle used the literal, STEP -1.3-compliant text `Signed off by: Director of Quality` — but the actual signer was Claude acting in the Director of Quality role under explicit user direction (per `sprint_close.md`'s own record and `docs/System_status_report.md`'s "agent-mediated Director of Quality" annotation), not a human sign-off. `execution_prompt.md §5.3` already defines a compliant agent-mediated naming pattern (`"Sprint Execution Engine (agent-mediated, <Role Name> role — §X.Y)"`) for exactly this situation, but it was not used in the `Signed off by:` field itself — so the STEP -1.3 structural signer check passed at face value without the sign-off field disclosing true provenance; only cross-referencing `sprint_close.md` and the system status report surfaced it. | Phase 4 | A | defer | When Director of Quality sign-off on a `qa_evidence_EPIC-xx.md` is performed by the engine in an agent-mediated capacity, the `Signed off by:` field itself should use the existing `execution_prompt.md §5.3` agent-mediated naming pattern rather than the literal `"Director of Quality"` string, so the STEP -1.3 check reflects true signer provenance directly rather than relying on prose elsewhere in the cycle to disclose it. | Head of Specs Team | next `run sprint` cycle producing agent-mediated DoQ sign-off |

**Recurrence Notes:**
None. Both friction items above are new this cycle — neither appeared in v7.4's Phase 4 record (which was a single-EPIC, autonomous-class cycle with no agent-mediated DoQ sign-off and no staging-deferred ACs, so neither condition was present to surface it there).

---

## Recurrence Escalations

None.

## Process improvements actioned this run

None applied this run — both Phase 4 friction items are `defer` classification (delivery_verification_prompt.md is outside this routine's write scope per §5 Write Scope Restriction; execution_prompt.md/qa_evidence_template.md changes require Head of Specs Team confirmation not available this run).

## New files created this run

`claude/cycles/2026-07-17__release-v7.5/verification_report.md` (this Phase 4 append and the `docs/System_status_report.md` status-line update are the only other artefacts touched).

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/delivery_verification_prompt.md` | STEP 2.1 | Add "Staging-deferred" as an explicitly accepted Result value (conditioned on a confirmed pre-PR backlog item) alongside Pass/Pass with notes/Fail | Head of Specs Team | next roadmap review |
| `claude/system/qa_evidence_template.md` (Standard Sign-Off Block) | `Signed off by:` field | Require the `execution_prompt.md §5.3` agent-mediated naming pattern when Director of Quality sign-off is performed by the engine in an agent-mediated capacity, instead of the literal "Director of Quality" string | Head of Specs Team | next `run sprint` cycle producing agent-mediated DoQ sign-off |

## Escalations

None.

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | This cycle's DoQ sign-off (both the 4 QA evidence logs and the verification_report.md §9 block) was agent-mediated end-to-end under explicit user direction, but none of the sign-off fields used the compliant agent-mediated naming pattern already defined in `execution_prompt.md §5.3` — the true provenance was only recoverable by cross-referencing `sprint_close.md` prose. | Future verification/execution runs performing agent-mediated sign-off should use the §5.3 naming pattern directly in the `Signed off by:`/`Accepted by:` fields, not just record it in surrounding commentary. | All |
