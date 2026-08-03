Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03

# QA Evidence Log — EPIC-03

**EPIC:** EPIC-03 — Governance Process Hardening
**Cycle:** 2026-08-03__release-v8.1
**Sprint goal:** Ship v8.1's operational-safety, governance-process, QA-debt, spec-debt, and backend-hardening scope — including the cross-EPIC execution-state structural fix and the release's one ready user-facing accessibility fix.
**Test scenarios used:** N/A — all stories are governance/process documentation changes plus one CI script (ST-08), verified by code review and (for ST-08) a local fire-test. No Playwright/runnable test suite applies to this EPIC's scope.

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-03 | `release_planning_prompt.md#1.4a.1` | New Sunset Criteria sub-section: 4 consecutive Option-(a) Perennial-Return dispositions escalate to mandatory Option (b) unless a materially new gate path is documented; applied retroactively to `BLG-FEAT-73`/`BLG-FEAT-74` (both 2 of 4, below trigger) | Explicit sunset criteria defined; applied retroactively to BLG-FEAT-73/74; Product Owner sign-off | Pass | None |
| ST-04 | `roadmap_prompt.md#2.4` | New mandatory-pull-forward clause for sustained PVR Advisory-tier readings (3+ consecutive), mirroring §7.1's Skill-Silo clause | Escalation clause drafted; reviewed with Head of Specs Team; roadmap_prompt.md updated if adopted | Pass | None |
| ST-05 | `sprint_planning_prompt.md#1.5` | New Minimum Capacity Buffer Floor advisory (95% of confirmed capacity), referenced by STEP 3.2's Capacity Gate | Minimum buffer floor proposed; FinOps & Resource Architect + PMO Lead sign-off | Pass | None |
| ST-06 | `claude/backlog/technical_debt_registry.md` | New consolidated registry of BLG-BE/FE/OPS items Type-tagged Tech/Technical Debt (2 currently qualify), with a mechanically re-derivable inclusion rule | Consolidated registry built; Head of Engineering sign-off | Pass | None |
| ST-07 | `release_planning_prompt.md#STEP 3` | New Skill-Silo mitigation advisory: soft 1-in-3-release-cycles rotation target toward execution-heavy scope, tied to §7.1's Skill-Silo Alert as trigger | Rotation guideline documented; tied to STEP 7.1 alert; documented in release_planning_prompt.md | Pass | None |
| ST-08 | `scripts/check_pii_field_patterns.py`, `.github/workflows/quality_gate.yml` | New CI job scanning added/changed `openapi.yaml` lines for common PII field-name patterns, flags for manual review | Lightweight CI check added; confirmed to fire on a deliberately-introduced PII-shaped field | Pass | None |
| ST-09 | `shared_standards.md#17` | New §17 companion provision: Head of Specs Team standing authority to relabel a resolved un-versioned Now-horizon carry-forward heading with its confirmed version, without a full `run roadmap` invocation; cross-referenced from `roadmap_prompt.md` STEP 8.1 | One remediation path selected and implemented via the standard governance file edit checklist; carry-forward no longer requires an out-of-band write | Pass | None |

**QA test coverage:**
- Scenarios run: N/A (no runnable test suite applies); ST-08's CI script fire-tested locally (deliberate PII field injection → exit 1 with field named; clean baseline → exit 0; file restored)
- Regression areas checked: governance-file-edit checklist consistency (version headers, `OPERATIONAL_GUIDE.md` §14, `prompt_change_log.md`) verified across all 4 touched prompt files (`release_planning_prompt.md`, `roadmap_prompt.md`, `sprint_planning_prompt.md`, `shared_standards.md`) after a mid-EPIC process gap (see Process Note below)
- Known deviations filed: None

**Process note:** The CLAUDE.md §6 governance-file-edit checklist (version bump + `OPERATIONAL_GUIDE.md` §14 + `prompt_change_log.md`, all in the same commit) was not completed in the same commits as the ST-03/ST-04/ST-05/ST-07 prompt edits. This was caught before the PR opened and closed in commit `0bd1d586` (ST-09), which completes all four files' checklist entries together. No governance file was left inconsistent at PR-open time.

**Two additional backlog items filed during this EPIC's execution** (both are process/documentation gaps discovered incidentally, not part of this EPIC's own scope): `BLG-GOV-285` (governance_sync.yml auto-close false positive on delegation commits, found during EPIC-02) and `BLG-SPEC-110` (13 undocumented versions in `sprint_planning_changelog.md`, found during ST-05's own checklist pre-check).

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (ST-08's "fire test" is a script/CI check, not a UI or staging verification)
- Criterion 3: No frontend-visible change — no story in this EPIC creates or modifies any file under `src/components/**` or `src/pages/**` — ✓
- Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-03
- Comments: Autonomous class sign-off — all four qualifying criteria met. **EPIC-level consolidation note (BLG-GOV-14):** several stories in this EPIC name their own story-level domain-authority sign-off in the AC (Product Owner — ST-03/ST-09; Head of Specs Team — ST-04; FinOps & Resource Architect + PMO Lead — ST-05; Head of Engineering — ST-06; Director of HR — ST-07). Each was cleared via agent-mediated review (§5.3) and is recorded per-story in `execution_state/EPIC-03.json` `sign_off_record`. This EPIC-level autonomous-class block is the required DoQ consolidation and does not substitute for, nor is substituted by, those story-level sign-offs — both are present. ST-08 (AI Compliance & Governance Officer) was self-verified per its own AC via the local fire-test described above; no separate sign-off record was created since the AC explicitly framed it as engine-self-verifiable.
