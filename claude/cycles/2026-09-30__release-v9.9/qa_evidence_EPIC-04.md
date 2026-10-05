Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-05

# QA Evidence Log — EPIC-04

**EPIC:** EPIC-04 — Governance Process & Strategy Boundary
**Cycle:** 2026-09-30__release-v9.9
**Sprint goal:** Ship a single canonical ATR/stop-recalculation implementation with timestamp visibility on `GET /positions` (`BLG-BE-135`), while clearing the queued backend, security, QA, governance, spec, and frontend debt items that make up the rest of v9.9's full-capacity scope.
**Test scenarios used:** `tests/test_state_execution_path_consistency.py`, `tests/test_scan_backlog_gate_conditions_date_disambiguation.py`, `tests/test_compute_rebalance_diagnostics.py`

## Process Deviation — Merged to main via EPIC-02's PR without its own merge gate

This EPIC's story commits were never merged through an EPIC-04 PR. They were made on a single linear branch history that EPIC-02's branch was later cut on top of, so PR #1886 (`[EPIC-02] Operational Reliability & Security Hardening`, merged as `362ff619`) carried them into `main` together with EPIC-05's commits. PR #1886's body and `qa_evidence_EPIC-02.md` named only ST-06–ST-09, so none of this EPIC's work received a Director of Quality review or Product Owner acceptance before reaching `main`.

- **Commits affected (this EPIC):** `018f5c1c` (ST-27), `d260e98b` (ST-23), `002a2dc5`/`1ef2ae8d` (ST-24 escalation), `94de0a0b` (ST-21), `ae17d5de` (ST-22), `57de1411` (ST-25), `53842d71` (ST-19/ST-20/ST-26 escalations), plus their `execution_state.json` record commits.
- **Rule breached:** CLAUDE.md §2 — story commits must land on the branch matching their EPIC prefix; never merge a PR without QA sign-off and Product Owner acceptance (Section 13 / STEP 4 merge gate).
- **Disposition (user direction, 2026-10-05):** retroactive merge gate. The code stays on `main`; this log is written after the fact, and the sign-off block below is left blank for the Director of Quality. Product Owner acceptance must also be recorded before this EPIC is treated as `merged`. Also recorded in `qa_evidence_EPIC-02.md` and `qa_evidence_EPIC-05.md`.
- **Retroactive re-verification (2026-10-05):** all three test files above re-run on `main` at `6accd183` — passing. `roadmap_prompt.md` core re-measured at ~16k tokens (63,937 chars), within ST-21's ≤25,000-token AC.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-19 | — | Not built. Escalated: live production data needed for the 90-day AI usage review; no production credential in this sandbox (RISK-03). | Dated review artefact; disposition for all 8 gated items | Pending — blocked_decision | ESC-EXEC-20261001-02 |
| ST-20 | — | Not built. Escalated: the §13 boundary determination needs named-authority judgement. | Dated determination recorded; conditions/remediation filed if needed | Pending — blocked_decision | ESC-EXEC-20261001-03 |
| ST-21 | `claude/system/roadmap_prompt.md`, `claude/system/roadmap_prompt_appendix.md` | Split `roadmap_prompt.md` into a core plus `roadmap_prompt_appendix.md`; CLAUDE.md §6 checklist applied in the same commit (version bump, `OPERATIONAL_GUIDE.md` §14 + source-prompt header, `prompt_change_log.md`, changelog). | Covers AC-01 (core ≤25,000 tokens), AC-02 (no procedural step lost, diff-verified), AC-03 (CLAUDE.md §6 checklist complete) | Pass | None |
| ST-22 | `docs/governance/strategy_parameter_change_ledger.md`, `claude/strategy/strategy_rules.md#12.3` | New parameter-change ledger backfilled from `strategy_rules.md`'s change log (v1.0–v1.12; none of §11's 4 parameters has changed since v1.0). §12.3 now cross-references it (`strategy_rules.md` v1.12→v1.13), with an agent-mediated Strategy Rules & System Intent Owner sign-off (§5.3) before the write. | Covers AC-01 (ledger backfilled), AC-02 (§12.3 references it) | Pass | None |
| ST-23 | `scripts/scan_backlog_gate_conditions.py` | Date-disambiguation fix: a `gate_condition` with an early future date and a later past date is now flagged correctly rather than resolved wrong. | Covers AC-01 (mixed-date case flagged), AC-02 (test file passes — `tests/test_scan_backlog_gate_conditions_date_disambiguation.py`) | Pass | None |
| ST-24 | — | Not built. Escalated: the AC needs edits to `claude/roadmap/*` and to existing `backlog.md` item content, both outside Sprint Execution's write scope. | Single canonical statement; all 5 items reference it | Pending — blocked_decision | ESC-EXEC-20261001-01 |
| ST-25 | `scripts/compute_rebalance_diagnostics.py`, `claude/system/roadmap_prompt.md#STEP 2.4`, `#7.1` | New script computes the STEP 2.4/7.1 tallies; `roadmap_prompt.md` cites it as an optional acceleration. STEP 2.4 reproduced exactly (U=16/G=41/D=109/P=4 of 170 → 0.094). STEP 7.1's cited 83.7% comes out as 84.0% from the same v9.6–v9.8 window. This is disclosed as a probable hand-calculation drift in the cited figure, not a script defect (intent-check advisory LL-v3.4-P3-03). | Covers AC-01 (reproduces cited STEP 2.4/7.1 figures), AC-02 (optional, not hard dependency) | Pass with notes — STEP 7.1 off by 0.3pp vs the hand-computed figure (see execution_state notes) | None (notes-only, no canonical value overridden) |
| ST-26 | — | Not built. Escalated: creating a new `claude/roadmap/*` file is outside write scope (RISK-02). | File exists, seeded; §7.2 reads from it | Pending — blocked_decision | ESC-EXEC-20261001-04 |
| ST-27 | `claude/schemas/state_field_owners.json#execution_state_path` | Corrected `.claude_current_state.json`'s stale `execution_state_path`, corrected the field's ownership record, and added a consistency test so it can't drift silently again. | Covers AC-01 (path matches active cycle), AC-02 (root cause identified and guarded — `tests/test_state_execution_path_consistency.py`) | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_state_execution_path_consistency.py` (ST-27), `tests/test_scan_backlog_gate_conditions_date_disambiguation.py` (ST-23), `tests/test_compute_rebalance_diagnostics.py` (ST-25). Re-run retroactively 2026-10-05 together with EPIC-05's `tests/test_check_data_model_drift.py`: 22 passed.
- Regression areas checked: governance prompts (`roadmap_prompt.md` split + appendix), `strategy_rules.md` §12.3, backlog gate-scan tooling, state-pointer consistency
- Known deviations: None found — all 5 done stories' deviation checks completed with nothing to file. Process deviation above (merge-gate bypass) recorded separately; it is not a spec deviation.

---

## Standard Sign-Off Block

> Autonomous class (BLG-GOV-19) not applicable: Criterion 1 is unmet (ST-19/ST-20/ST-24/ST-26 are `delegated_decision`), and the merge-gate bypass above needs human review in any case. The EPIC is also not yet `done` — 4 stories are still blocked on open escalations.

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- Signed off by:
- Date:
- Comments: Retroactive merge gate. Director of Quality to review the 5 done stories already on `main` (via PR #1886) and complete this block. Product Owner acceptance still needs recording separately.
