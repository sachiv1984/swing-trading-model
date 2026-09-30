**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 3.5
**Last Updated:** 2026-09-30 (roadmap rebalance `2026-09-30__scheduled` STEP 4.2 — `IW-20260930-01` dispositions applied: 4 submissions consolidated and Promoted-Backlog (2 → BLG-FE-193, 2 → BLG-BE-135); `IDEA-director-of-hr-20260919-02` reached 3-cycle park hard cap, resolved Promoted-Backlog → BLG-GOV-357; 0 ideas remain open); prior — 2026-09-30 (idea intake window `IW-20260930-01` — 4 submissions added: 2 Head of UX & Design, 2 Head of Engineering, open-position stop-loss transparency review); prior — 2026-09-30 (ideas_housekeeping — post-ship closure 2026-09-28__release-v9.8 — 7 rows archived: 7 Promoted-Backlog, window IW-20260928-01, including the re-evaluated `IDEA-data-model-20260919-02`; 2 rows kept, unchanged); prior history retained — see prior entries in version control (§16.14 header-history retention rule — current entry plus at most 2 prior entries retained).
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Ideas Register

Migrated from per-file model (44 submissions from IW-20260304-01) on 2026-03-17 per ST-19 (EPIC-06).
Schema: per `shared_standards.md §16.5`

| Idea ID | Title | Submitter | Window | Submitted At | Status | Park Count | Park Rationale | Step 4 | Step 5 |
|---------|-------|-----------|--------|--------------|--------|------------|----------------|--------|--------|
| IDEA-challenger-20260809-02 | Challenge: is the SI-02 ≥20-linked-trades gate threshold calibrated for this system's actual trade cadence? (9+ consecutive NOT MET readings) | Challenger | IW-20260809-01 | 2026-08-09 | Rejected | — | — | Reject — strong (already answered by BLG-GOV-237, v8.3, "still appropriate"; see rejected_but_strong.md) | N/A |
| IDEA-head-of-ux-20260930-01 | Show ATR value, stop multiplier, and recalculation source inline on every open-position stop-loss cell | Head of UX & Design | IW-20260930-01 | 2026-09-30 | Promoted-Backlog | — | — | Backlog (ungated, consolidated) — filed as BLG-FE-193 (with IDEA-head-of-ux-20260930-02), gate-conditional on BLG-BE-135 | N/A |
| IDEA-head-of-ux-20260930-02 | Replace the static "ATR recalculated daily" explainer tooltip with copy sourced from the position's actual last-recalculation event | Head of UX & Design | IW-20260930-01 | 2026-09-30 | Promoted-Backlog | — | — | Backlog (ungated, consolidated) — filed as BLG-FE-193 (with IDEA-head-of-ux-20260930-01), gate-conditional on BLG-BE-135 | N/A |
| IDEA-head-of-engineering-20260930-01 | Consolidate the 4 duplicate ATR calculation implementations into one canonical source; remove the dead `position_manager.py` script | Head of Engineering | IW-20260930-01 | 2026-09-30 | Promoted-Backlog | — | — | Backlog (ungated, consolidated) — filed as BLG-BE-135 (with IDEA-head-of-engineering-20260930-02) | N/A |
| IDEA-head-of-engineering-20260930-02 | Persist stop/ATR recalculation timestamp, expose `atr`/multiplier/timestamp on `GET /positions`, and reconcile `strategy_rules.md` §7.1 "recalculated daily" wording against the actual on-load recompute cadence | Head of Engineering | IW-20260930-01 | 2026-09-30 | Promoted-Backlog | — | — | Backlog (ungated, consolidated) — filed as BLG-BE-135 (with IDEA-head-of-engineering-20260930-01) | N/A |
| IDEA-director-of-hr-20260919-02 | Sign-off single-point-of-failure matrix: per governance gate, which roles can sign, flagging gates where one agent-mediated role is the sole signer | Director of HR | IW-20260919-01 | 2026-09-19 | Promoted-Backlog | 2 | 3-cycle park hard cap reached 2026-09-30 (§4.5) — re-parking not permitted; resolved to Backlog (ungated), filed as BLG-GOV-357 | Backlog (ungated) — 3-cycle hard cap reached (§4.5), filed as BLG-GOV-357 | N/A |
