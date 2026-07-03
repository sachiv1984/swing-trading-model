Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-03
Cycle: 2026-07-02__release-v6.5

---

# Lessons Learnt — 2026-07-02__release-v6.5

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-02__release-v6.5
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-03
**Reviewed by:** PMO Lead

### What went well

- All 8 stories delivered across all 3 EPICs — zero items returned to backlog, zero delegation records needed (`delegation_log.md` was never created this sprint; every item was, or was reclassified to, `autonomous`).
- `deviations_filed` and `qa_signed_off` atomic-write discipline held throughout — both flags were set at story/EPIC completion time, no batch correction required at sprint close (continuing the pattern established in v6.4).
- Three ST items (ST-01/AC-01/AC-02, ST-02, ST-03) were verified pre-met on `main` from prior v6.4/roadmap-rebalance commits via direct file read rather than re-implemented — the pre-met verification path (LL-v2.4-P4-02) worked cleanly, each with its own qa_evidence entry documenting the verification method.
- `ESC-EXEC-20260703-01` (EPIC-02/ST-04, missing working `X-API-Key`) was raised, surfaced to the correct owning authority, and resolved same-day without blocking the other EPIC-02 items — the escalation/continue-other-items mechanism worked as designed.
- Agent-mediated sign-off resolved across three distinct domain-authority combinations (Infrastructure & Operations Owner; Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner + Financial Reporting & Records Owner) with zero escalations to a human authority.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| STEP 4's "on session resume — merge gate state sync" had no branch check of its own — this session resumed on `exec/2026-07-02__release-v6.5/EPIC-03` with all three PRs (#908, #910, #909) already `MERGED` on GitHub but `execution_state.json` on `main` still showing EPIC-02/EPIC-03 as `status: done`/`pr_status: open`. This is the exact v6.4 Phase 3 friction item 1 recurrence pattern (deferred, target v6.5) | Phase 3 | C | action-now | Applied — `execution_prompt.md` v3.50→v3.51: STEP 4's resume-sync sub-step now requires `git branch --show-current` (and `git checkout main && git pull` if not on `main`) before the sync write, mirroring STEP 5's branch-ordering gate. This session itself switched to `main` before writing (no orphaned write occurred), but the underlying prompt gap is now closed. See `claude/system/prompt_change_log.md` 2026-07-03 entries and `OPERATIONAL_GUIDE.md` v4.72→v4.73 | Head of Specs Team | — |
| v6.4 Phase 3 friction item 2 (`/commit-check` should diff `git add`'s target list against the intended file set before multi-file governance commits, target v6.5) remains unapplied — `.claude/skills/commit-check/SKILL.md` was checked this session and contains no such diff-verification step | Phase 3 | D | defer | Not applied this cycle — `.claude/skills/` is outside `run sprint`'s declared write scope (Section 7 permits `claude/system/`, `claude/charter/`, `claude/agents/` governance edits, not `.claude/skills/`). This is the 1st missed target since the v6.4 defer; needs a routine with skill-file write authority (or explicit Head of Specs Team-directed edit) to apply. If unapplied by the next cycle this becomes a 2-cycle carry-forward and an automatic escalation per `lessons_learnt_prompt.md` §3.7 | Head of Specs Team | 2026-07-02__release-v6.6 (next cycle) |
| `ESC-EXEC-20260703-01`: the engine initially could not distinguish the app's `X-API-Key` auth token from Render's separate *management*-API token — both were assumed to live under a single `RENDER_API_KEY` value in `~/.api_keys`, and the 401 from `api.render.com` (management API) was read as "no valid key available" rather than "wrong API queried" | Phase 3 | B | action-now | Resolved in-session by the reporting user (2026-07-03) — clarified `RENDER_API_KEY` is in fact the app's `X-API-Key`; the correct target host is the trading-assistant app, not `api.render.com`. No prompt change filed — this was a one-time credential-identity ambiguity in the runtime environment, not a repeatable governance gap; the escalation mechanism itself worked correctly (raised, scoped to non-blocking, resolved, unblocked same day) | Infrastructure & Operations Owner | — |

**Recurrence Notes:**
- v6.4 Phase 3 friction item 1 (STEP 4 resume-sync missing a branch check, target v6.5): **Recurred as predicted, and resolved this cycle.** The exact scenario materialised on this session's resume; the engine avoided the specific defect (orphaned write on a stale branch) by manually switching to `main` first, and the underlying prompt gap was closed action-now this cycle at its own named target — see Friction Log row 1.
- v6.4 Phase 3 friction item 2 (`/commit-check` pathspec diff reinforcement, target v6.5): **Not resolved — carried forward.** See Friction Log row 2. First missed target; not yet a 2-cycle carry-forward, so not an automatic escalation under §3.7, but flagged for priority attention next cycle.
- v6.4 Phase 3 friction item 3 (ST-11 sign-off section-citation errors, action-now, resolved same session): **Not a recurrence.** No section-citation errors occurred in this cycle's sign-off reviews.
- New friction item (ESC-EXEC-20260703-01 credential identity) is a first-time capture — no prior-cycle match found in `claude/cycles/2026-07-02__release-v6.4/lessons_learnt_cycle.md` `## Phase 3`.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-07-02__release-v6.5
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-03
**Reviewed by:** PMO Lead

### What went well

- All 8 stories verified in a single run — 0 traceability gaps, 0 QA Fail results, 0 P0/P1/P2 deviations. Verification reached `Verified` status directly, no re-run required.
- All three EPICs' QA evidence sign-off blocks used a fully compliant signer format this cycle — no Tier 2 flags fired at STEP -1.3. The v6.3 Phase 4 deferred patch (explicit signer-format validation note in `qa_evidence_template.md`) that carried an open 2-cycle recurrence-escalation warning into v6.5 was in fact already applied at v6.4 post-ship closure (v1.5→v1.6, 2026-07-02) — ahead of its own target, so no escalation triggers here.
- Zero test scenario gaps this cycle — EPIC-02 and EPIC-03 both had populated `test_scenarios` fully confirmed run in their QA evidence logs, and EPIC-01's empty `test_scenarios` correctly short-circuited to `not_applicable` (governance/documentation/config-only, no frontend-visible AC).
- `deferred_execution_blockers = []` and zero parked items in the backlog slice meant STEP 4 required no corrective writes — a genuinely clean sprint close, consistent with v6.4's pattern.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `backlog.md` entry headers for `BLG-GOV-157` and `BLG-GOV-159` are swapped relative to their actual titles (confirmed by direct read at STEP 4: `BLG-GOV-157`'s header reads ST-03's title, `BLG-GOV-159`'s header reads ST-01's title). This was already flagged non-blocking at Sprint Planning (`sprint_backlog.md` Outstanding Actions) but was not corrected during execution, so it reached Delivery Verification still unresolved | Phase 4 | A | defer | Not corrected this run — outside Delivery Verification's write scope for `backlog.md` (append-only, outstanding items and test scenario gaps only; a header-text correction is a content edit, not an append). Requires a `groom backlog` run or a Head of Specs Team-directed edit to swap the two entry headers back to their correct titles | Head of Specs Team | Next `groom backlog` run |

**Recurrence Notes:**
- v6.4 Phase 4 friction item 1 (`qa_evidence_template.md` signer-format validation note, deferred v6.3→v6.4, carried a 2-cycle-recurrence-escalation warning into v6.5 if unapplied): **Resolved — not a recurrence.** Confirmed applied at v6.4 post-ship closure (`prompt_change_log.md` 2026-07-02, v1.5→v1.6), ahead of its v6.5 target. No escalation triggered.
- v6.4 Phase 4 friction item 2 (`System_status_report.md` sprint section not written correctly at sprint close, resolved v6.4): No recurrence — the v6.5 sprint section was present, complete, and accurate at STEP 6 this cycle (only the same routine status-line correction was needed, consistent with both v6.4 and v6.3's pattern).
- v6.4 Phase 4 friction item 3 (EPIC-03 `test_scenarios` pending pattern, resolved v6.4): No recurrence — EPIC-03's `test_scenarios` was fully populated (`tests/e2e/trade-plan.spec.js`) at sprint close this cycle, with the corresponding Outstanding Action in `sprint_backlog.md` (LL-v2.0-P4-2) already dispositioned before this verification run began.
- New friction item (BLG-ID cross-reference defect in `backlog.md`) is a first-time capture at Delivery Verification — no prior-cycle match found in `claude/cycles/2026-07-02__release-v6.4/lessons_learnt_cycle.md` `## Phase 4`. Note it was already visible at Sprint Planning (`sprint_backlog.md` Outstanding Actions) but had not previously been logged as a Phase 4 friction item.

---
