**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 3.3
**Last Updated:** 2026-09-23 (ideas_housekeeping — post-ship closure 2026-09-21__release-v9.6 — 42 rows archived: 41 Promoted-Backlog + 1 Rejected-not-strong (`IDEA-ai-compliance-20260919-02`, confirmed absent from `rejected_but_strong.md`); 3 rows kept — `IDEA-challenger-20260809-02` (Rejected, present in `rejected_but_strong.md`), `IDEA-data-model-20260919-02` and `IDEA-director-of-hr-20260919-02` (Parked-cycle-1)); prior — 2026-09-19 (roadmap rebalance `2026-09-19__scheduled` STEP 4.2 — `IW-20260919-01` dispositions applied: 41 Promoted-Backlog (filed as 36 backlog items after 4 consolidations), 2 Parked-cycle-1, 1 Rejected (already implemented)); prior — 2026-09-19 (idea intake window IW-20260919-01 — invoked inline as STEP -1.6 of `run roadmap --reason scheduled` (register held 0 open ideas); 44 rows appended, all Submitted, 22 agents × 2 net-new); prior history retained — see prior entries in version control (§16.14 header-history retention rule — current entry plus at most 2 prior entries retained).
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Ideas Register

Migrated from per-file model (44 submissions from IW-20260304-01) on 2026-03-17 per ST-19 (EPIC-06).
Schema: per `shared_standards.md §16.5`

| Idea ID | Title | Submitter | Window | Submitted At | Status | Park Count | Park Rationale | Step 4 | Step 5 |
|---------|-------|-----------|--------|--------------|--------|------------|----------------|--------|--------|
| IDEA-challenger-20260809-02 | Challenge: is the SI-02 ≥20-linked-trades gate threshold calibrated for this system's actual trade cadence? (9+ consecutive NOT MET readings) | Challenger | IW-20260809-01 | 2026-08-09 | Rejected | — | — | Reject — strong (already answered by BLG-GOV-237, v8.3, "still appropriate"; see rejected_but_strong.md) | N/A |
| IDEA-data-model-20260919-02 | Column provenance annotations in data_model.md (user-entered / derived / system-stamped) so analytics know which fields are safe to recompute | Data Model & Domain Schema Owner | IW-20260919-01 | 2026-09-19 | Parked-cycle-1 | 1 | Depends on BLG-SPEC-150 (4 orphaned, always-NULL columns on live `positions`) resolving which columns survive — annotating provenance before that triage would document columns about to be dropped. Revisit at the next scheduled rebalance once BLG-SPEC-150's disposition is known. | Park — specific blocker named; Facilitator challenge answered (STEP 4.1) | — |
| IDEA-director-of-hr-20260919-02 | Sign-off single-point-of-failure matrix: per governance gate, which roles can sign, flagging gates where one agent-mediated role is the sole signer | Director of HR | IW-20260919-01 | 2026-09-19 | Parked-cycle-1 | 1 | Depends on the just-closed BLG-GOV-335/337 rulings (2026-09-19): whether the new `execution_prompt.md` §7 exception and the Director-of-Quality review change signer topology is not yet observable, so a matrix drawn now would be redrawn. Revisit at the next scheduled rebalance. | Park — specific blocker named; Facilitator challenge answered (STEP 4.1) | — |
