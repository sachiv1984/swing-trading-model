Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-06-25
Cycle: 2026-06-24__release-v6.2

---

# Lessons Learnt — 2026-06-24__release-v6.2

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-06-24__release-v6.2
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-06-25
**Reviewed by:** PMO Lead

### What went well

- BLG-GOV-135 (autonomous class hard gate) and BLG-GOV-136 (test_scenarios path validation) both delivered cleanly as ST-10/ST-11 in EPIC-03 — two outstanding v6.1 Phase 4 actions cleared in the same sprint that surfaced them, with zero process friction.
- BLG-QA-62 (Playwright spec auto-registration via glob) delivered as ST-13 — eliminates the manual spec registration step that produced carry-forward friction in v6.0 and v6.1. BLG-QA-64 filed proactively for 12 pre-existing dark specs surfaced by the glob change.
- §13 SRB-v1.7 PASS gate for AI features was cleared pre-sprint (2026-06-24) — Sprint 2 began with no decision blockers, and `advisory: true` enforcement in both endpoints satisfied the compliance requirement cleanly.
- Multi-story same-commit format `[EPIC-02][ST-06][ST-08]` used for batched backend stories — governance_sync.yml auto-closed both GitHub issues correctly on push.
- All 13 stories delivered — zero items returned to backlog; both Sprint 1 and Sprint 2 goals fully met.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Playwright strict mode violation recurrence — SC-AB-02 and SC-AB-04 in EPIC-02 spec (`epic02-v62-ai-briefing-chat.spec.js`) failed CI on first push; getByText() assertions without exact scoping matched unintended elements; required fix commit `de068bbd` | Phase 3 | D | defer | Add Playwright strict mode advisory to frontend delegation spec template (Base44 prompt draft §6 Expected outcome): explicitly require `{exact: true}` or `data-testid` scoping on all text-based assertions when component co-renders with other panels; template version bump v6.3 | Director of Quality | v6.3 |
| Staging-only ACs cleared by code review without backlog item — ST-07/AC-04 (advisory label wording/styling) and ST-09/AC-03 (advisory footer + non-executability) designated staging-only at sprint planning but cleared by thorough code review in DoQ sign-off; CLAUDE.md §2 frontend testing gate requires backlog item if "code review only" for deferred-to-staging ACs; the DoQ determination was that code inspection of static JSX is sufficient for wording/non-dismissibility verification — protocol ambiguity exists on whether code review substitutes for staging for pure wording/styling ACs | Phase 3 | B | defer | Clarify frontend testing gate in CLAUDE.md §2 (or advisory in qa_evidence_template.md): define when code review of static JSX is an accepted substitute for staging sign-off for pure wording/non-dismissibility ACs (vs visual rendering/colour ACs that always require staging or Playwright); consider adding "code review accepted — static JSX verified" as a third sign-off path for wording-only ACs | Head of Specs Team | v6.3 |

**Recurrence Notes:**
- Friction item 1 (Playwright strict mode violation) is a **Recurrence** from v6.1 Phase 3 item 1. Prior action from v6.1: "no template change needed — pattern documented here. Spec author checklist: always scope page-wide getByText() with exact:true or testid scoping." That documentation-only action was insufficient — the pattern recurred in EPIC-02 tests authored this sprint. Escalation: this must now be encoded as a hard advisory in the delegation spec template (Base44 prompt draft), not just conversation history. Head of Specs Team to confirm template change scope at v6.3 planning.
- Friction item 2: first occurrence this cycle.
