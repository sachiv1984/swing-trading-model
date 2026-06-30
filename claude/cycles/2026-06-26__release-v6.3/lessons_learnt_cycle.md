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
