Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-06-30
Cycle: 2026-06-26__release-v6.3

---

# Lessons Learnt — 2026-06-26__release-v6.3

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-06-26__release-v6.3
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-06-30
**Reviewed by:** PMO Lead

### What went well

- All 15 stories delivered — zero items returned to backlog. Sprint 1 (EPIC-01 + EPIC-02) and Sprint 2 (EPIC-03) goals both fully met; 29 new automated tests landed in CI.
- Three delegated_frontend items (ST-02, ST-11, ST-12) all completed cleanly by Base44 Frontend Prompt Owner with complete Playwright coverage — delegation record quality was sufficient; no back-and-forth.
- Multi-EPIC shared file merge sequence (EPIC-02 first → EPIC-01 rebase) followed without conflicts; `test.py` line counts reconciled correctly at merge.
- `services/__init__.py` missing exports surfaced and fixed within the same EPIC-03 story (ST-11) rather than requiring a follow-up story — self-contained fix pattern working as intended.
- Prior cycle (v6.2) Phase 3 deferred action (Playwright strict mode advisory for Base44 delegation spec template) was applied in-sprint for ST-12 — SC-PD-05 used `page.evaluate()` rather than `addInitScript`, correctly scoping localStorage injection to the test session.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| deviations_filed = false not set atomically after deviation check — 13 of 15 stories had deviations_filed = false at sprint close despite no spec deviations found; the LL-v3.7-EX-01 atomic write rule requires this flag to be set immediately after step 10 deviation check, not at sprint close | Phase 3 | D | defer | Reinforce LL-v3.7-EX-01 in execution_prompt.md STEP 3.1.A step 10a: add reminder note that deviations_filed must be written in the same session turn as the deviation check — not deferred to sprint close batch correction; consider adding a per-story checklist prompt in step 10a | Head of Specs Team | v6.4 |
| qa_signed_off = false on all three EPICs in execution_state.json at sprint close — QA evidence sign-off blocks were complete with non-blank dates, but the advisory OA-1/ST-01 to update qa_signed_off = true after committing qa_evidence was not followed atomically | Phase 3 | D | defer | Verify OA-1/ST-01 advisory in execution_prompt.md §3.2.A is prominently visible; consider elevating from advisory to hard requirement (STRUCTURAL) since delivery verification reads this flag at STEP 0A; both flags (deviations_filed and qa_signed_off) have the same root cause — atomic write discipline after each step | Head of Specs Team | v6.4 |
| Sprint close requires deviations_filed/qa_signed_off batch correction for stories completed in prior sessions — because atomic writes are missed, sprint close must iterate through all 15 stories to apply corrections; this consumes disproportionate sprint close time and risks stale state if stories are missed | Phase 3 | C | defer | Consider adding a STEP 4 pre-halt checklist that verifies deviations_filed and qa_signed_off are set before outputting the EPIC merge halt message; this would catch the gap at each EPIC completion rather than at sprint close | PMO Lead | v6.4 |

**Recurrence Notes:**
- Prior cycle (v6.2) Phase 3 deferred item 1 (Playwright strict mode violation — recurrence from v6.1): checked against v6.3 execution — NOT a recurrence. No Playwright strict mode failures in v6.3; SC-PD-05 localStorage injection pattern avoided the issue that caused v6.2 failures. Prior action (add advisory to Base44 delegation template) appears to have been applied effectively.
- Prior cycle (v6.2) Phase 3 deferred item 2 (staging-only ACs cleared by code review): NOT a clear recurrence in v6.3. ST-01 observable ACs accepted by code review, but sprint_backlog.md staging-only note explicitly allows this. Protocol ambiguity from v6.2 remains unresolved (Head of Specs Team / v6.3 target — not closed this sprint; deferred carry-forward applies).
- Friction item 1 (deviations_filed atomic write): first explicit capture as a Phase 3 lessons learnt item; underlying pattern has occurred across multiple cycles but not previously recorded as a structured friction item.
- Friction item 2 (qa_signed_off atomic write): same root cause as item 1; first explicit capture.
- Friction item 3 (sprint close batch correction overhead): downstream consequence of items 1 and 2; same root cause cluster.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-06-26__release-v6.3
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-06-30
**Reviewed by:** PMO Lead

### What went well

- All 15 stories delivered with zero spec deviations — no P0/P1/P2 items; traceability matrix clean with 0 gaps; verification reached `Verified` status in a single run.
- Tier 2 sign-off flags were resolved promptly via Director of Quality counter-sign within the same session; no multi-session delay in QA evidence remediation.
- Three delegated_frontend items all had complete Playwright evidence at verification time — no missing or deferred AC coverage for ST-02, ST-12, or any autonomous stories.
- Deferred execution blockers = 0, outstanding items = 0, open escalations = 0 — sprint close was genuinely clean; verification had nothing material to carry forward beyond the two TSG items.
- v6.2 Phase 4 recurrence item (Playwright strict mode) confirmed resolved — SC-PD-05 `page.evaluate()` localStorage pattern worked correctly; no Tier-2 or staging-only AC issues for ST-12.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| QA evidence sign-off blocks used "Sprint Execution Engine" without required format qualifier ("(autonomous class)" or "(agent-mediated, Director of Quality role — §5.3)") across all three EPICs — triggered Tier 2 flags at STEP -1.3 for every EPIC, requiring Director of Quality counter-sign before STEP 1 could proceed; same root cause as qa_signed_off atomic-write pattern identified in Phase 3 | Phase 4 | A | defer | Reinforce sign-off format requirement in qa_evidence_template.md: add a validation note in the DoQ sign-off block template that the signer value must be one of: "Director of Quality", "Sprint Execution Engine (autonomous class)", or "Sprint Execution Engine (agent-mediated, <Role Name> role — §X.Y)"; also add an advisory reminder in execution_prompt.md §3.2.A sign-off protocol section that omitting the qualifier will trigger a delivery verification Tier 2 halt | Head of Specs Team | v6.4 |
| System_status_report.md v6.3 sprint section not written at sprint close — sprint_close.md recorded "Sprint section added at STEP 5.3A" but the file was not updated (Last Updated remained 2026-06-25; v6.2 was still the top section at STEP 6 of delivery verification); required a STEP 6 correction write | Phase 4 | A | defer | Add a post-write verification step to execution_prompt.md STEP 5.3A: after writing the sprint section to docs/System_status_report.md, immediately confirm the section is present by checking the file's Last Updated field or section header; if absent, re-attempt write before proceeding to sprint close commit | Head of Specs Team | v6.4 |
| EPIC-03 test_scenarios pending at sprint end — intentionally deferred per LL-v2.0-P4-2 but creates a recurring pattern where major frontend features (Strategy Benchmark page, 3 panels, 3 endpoints) ship without any Playwright scenario file; TSG-v63-02 backlog item created but the underlying pattern is that frontend EPICs consistently leave test_scenarios at "pending" rather than authoring even a minimal scenario set during execution | Phase 4 | C | defer | Consider adding a minimum-scenario requirement in sprint_backlog.md: for any delegated_frontend story with AC count ≥ 5, the delegation spec must include at least one Playwright scenario stub (even if unimplemented) so that QA & Testing Owner has a concrete starting point rather than authoring from scratch at delivery verification; this could be a spec template advisory rather than a hard gate | QA & Testing Owner | v6.4 |

**Recurrence Notes:**
- v6.2 Phase 4 friction item 1 (CI/infrastructure stories leave spec_references = [], deferred to v6.3 with target: add convention to execution_prompt.md §3.1.A): **NOT a recurrence this cycle** — all v6.3 CI/test stories had non-empty spec_references naturally. However, the deferred patch was not applied (no prompt_change_log entry found). 1-cycle carryover. If not applied in v6.4, this will become a 2-cycle recurrence escalation per lessons_learnt_prompt.md §3.7. Action: Head of Specs Team to confirm patch was applied or to apply it in v6.4.
- v6.2 Phase 4 sign-off format issues: NOT formally captured as a Phase 4 item in v6.2. The Tier 2 flag pattern recurred in all three v6.3 EPICs despite the sign-off compliance requirements being stable since delivery_verification_prompt.md v3.0 (v5.1 sprint). **Root cause persists** — the qa_evidence_template.md does not make the exact format requirement sufficiently visible during execution. Friction item 1 above is the corrective action.
- Phase 3 deferred items 1/2/3 (deviations_filed/qa_signed_off atomic write, sprint close batch correction): These are Phase 3 friction items targeted at v6.4 by the Head of Specs Team. Confirmed not closed this cycle. Not yet at 2-cycle escalation threshold (first captured Phase 3, v6.3). Monitor at v6.4 Phase 3.
- System status report write gap (friction item 2): First occurrence at this severity level captured as structured friction. Not a prior-cycle recurrence.
