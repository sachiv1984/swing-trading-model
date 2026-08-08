Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-08

# QA Evidence Log — EPIC-07 (Governance Process Integrity)

**EPIC:** EPIC-07 — Governance Process Integrity
**Cycle:** 2026-08-07__release-v8.4
**Sprint goal:** Ship both available user-facing reporting enhancements while clearing a full-capacity slate of API contract & spec debt, backend hardening, frontend code health & security, operational reliability & cost monitoring, QA/test infrastructure, and governance-process integrity work across all 31 scoped stories.
**Test scenarios used:** Derived from spec + AC (governance-process items; no runnable test suite applies — verified by script execution and code review, see below)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-29 | `claude/system/release_planning_prompt.md` §1.3a | New canonical, scripted gate-detection procedure (`scripts/scan_backlog_gate_conditions.py`) run at Release Planning STEP 1 before §1.4a's Perennial-Return Check. Parses backlog items by heading boundary only (never `---`), checks `Gate criteria`/`Gate`/`Gate date` field variants, flags `Provisional-Target`-embedded gate language with no formal field as a data-quality warning. Standard governance file edit checklist applied (v2.47→v2.48, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry, `release_planning_changelog.md` entry). | Documents a specific, repeatable scan procedure (not prose guidance); explicitly covers the `Provisional-Target`-embedded case (2 of 3 recorded misses) and the missing-`---`-separator case (4th failure mode, self-caught this cycle); governance file edit checklist applied; Head of Specs Team sign-off | Pass | None |
| ST-30 | `docs/ops/cross_epic_merge_runbook_dry_run_2026-08-08.md` | Dry-ran `CLAUDE.md` §8 (Cross-EPIC Merge Conflict Resolution) against this cycle's genuinely-parallel EPIC branches via a live test merge (`exec/.../EPIC-05` → `exec/.../EPIC-06`, `--no-commit --no-ff`, aborted after inspection — no state changed). Runbook's core append-only-file union and `execution_state.json` story-status precedence held up correctly. 2 gaps found and filed as follow-up backlog items (`BLG-GOV-289` — sibling-vs-sibling `blocked_items`/`delegated_items` union rule missing; `BLG-GOV-290` — no rule for shared-JSON-field schema-shape drift mid-sprint). | One sprint executed with genuinely parallel EPIC branches; Runbook followed; Gaps found are filed as follow-ups | Pass | None — 2 follow-up items filed (`BLG-GOV-289`, `BLG-GOV-290`), not deviations from ST-30's own scope |

**QA test coverage:**
- Scenarios run: `python3 scripts/scan_backlog_gate_conditions.py` executed against the live `claude/backlog/backlog.md` (294 items scanned, 192 gated items correctly detected, 5 genuine data-quality warnings found — independently re-verified by agent-mediated review, see below); live dry-run merge test for ST-30 (aborted cleanly, no state changed, conflict shape matched `CLAUDE.md` §8's prediction exactly)
- Regression areas checked: `OPERATIONAL_GUIDE.md` 3-way self-consistency (header / §14 self-row / Change Log top row) — found and corrected a pre-existing, unrelated drift (§14 self-row was stuck at v4.144 while header/Change-Log were already at v4.145 from an earlier, unrelated session edit) in the same pass
- Known deviations filed: None

---

## Agent-Mediated Sign-Off (ST-29, on behalf of Head of Specs Team)

Per `execution_prompt.md` §5.3, a general-purpose subagent reviewed ST-29's changes against the Head of Specs Team charter before this consolidation sign-off. First pass returned `Blocked` — not on content (all substantive findings were confirmed sound: correct 4-failure-mode coverage, script structurally eliminates the missing-`---` case rather than merely detecting it, all 4 version-bump locations consistent) — but on process: the work was not yet committed and `qa_evidence_EPIC-07.md` did not yet exist. Both were completed in-session (commit `67243bed`, this file) immediately after, closing the process gap the review correctly caught.

- Signed off by: Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3)
- Date: 2026-08-08
- Comments: Content verified sound on first pass (script independently re-run, 294/192/5 figures matched exactly; version consistency across file header, §6B source-prompt header, §14 table row, and OPERATIONAL_GUIDE.md's 3-way self-consistency confirmed; 20-of-293 missing-separator claim independently re-verified). Process gap (uncommitted work, no qa evidence file) identified and closed same-session — see commit `67243bed` and this file.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-29, ST-30 both autonomous; no `delegated_*` items in EPIC-07)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (governance prompt text, a Python script, and an operational report — all reviewed as text/code)
- [x] Criterion 3: No frontend-visible change — confirm no React page or UI component was created or modified — ✓ (no `src/pages/` or `src/components/` files touched by either story)
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-08
- Comments: Autonomous class sign-off — all four qualifying criteria met. ST-29 additionally carries its own named agent-mediated Head of Specs Team review above (its AC specifically names that role), which is not superseded by this EPIC-level autonomous-class block — both are recorded per the EPIC-level consolidation note (`execution_prompt.md` §3.2.A, BLG-GOV-14).
