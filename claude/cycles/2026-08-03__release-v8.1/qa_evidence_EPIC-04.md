Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03

# QA Evidence Log — EPIC-04

**EPIC:** EPIC-04 — QA Process & Debt Closure
**Cycle:** 2026-08-03__release-v8.1
**Sprint goal:** Ship v8.1's operational-safety, governance-process, QA-debt, spec-debt, and backend-hardening scope — including the cross-EPIC execution-state structural fix and the release's one ready user-facing accessibility fix.
**Test scenarios used:** N/A for ST-11/12/13 (audit/review-shaped stories, verified by script output / documented review, not a Playwright suite); ST-10 is itself a staging-only human verification task, no CI-reproducible equivalent.

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-10 | N/A (`spec_reference_not_applicable: true`) | Nothing built — this item IS the staging verification task itself | Human staging run performed; alert deactivates + notification + Telegram delivery confirmed; dated in `qa_evidence_EPIC-02.md` (v7.5) DoQ sign-off block | **Blocked — awaiting human staging run** | None (staging-only AC, no CI-reproducible equivalent, per `BLG-QA-115`) |
| ST-11 | `scripts/audit_endpoint_test_coverage.py`, `sprint_planning_prompt.md#STEP -1` | Full-repo endpoint test coverage audit script, wired into sprint planning preflight as a recurring pre-sprint-planning check | Recurring audit added; run once against current state with results recorded | Pass — 78 routes scanned, 8 documented `KNOWN_GAPS`, 0 undocumented gaps | None |
| ST-12 | `docs/governance/deviation_consolidation_review_2026-08-03.md`, `post_ship_closure.md#STEP 5.1` | First cross-cycle DEV-* consolidation review; found and fixed a resolution-status drift (`DEV-ST14-01`); wired as a recurring STEP 5.1 in post-ship closure | Periodic review added; first review performed; Director of Quality sign-off | Pass | None (the drift found was a documentation-consistency gap, corrected same commit — not a new spec deviation) |
| ST-13 | `docs/ops/ci_pipeline_baseline.md#7` | Post-parallelization Playwright shard balance audit (5-run sample) | Shard runtimes audited; confirmed balanced or rebalanced if skewed; QA Lead sign-off | Pass — balanced within ~13% peak-to-peak spread, no rebalancing needed | None |

**QA test coverage:**
- Scenarios run: N/A (audit/review-shaped EPIC); ST-11's script and ST-13's measurement method are both independently reproducible (`python3 scripts/audit_endpoint_test_coverage.py`; `gh run view <id> --json jobs`)
- Regression areas checked: N/A — no code behaviour changed by ST-11/12/13; ST-10 has no engine-side work
- Known deviations filed: None

**ST-10 delegation detail:** This backlog item (`BLG-QA-115`) IS the staging verification task itself — no implementation work exists to complete. Per its own AC, when a human performs the live staging run (create a price alert with a crossed threshold, trigger `POST /alerts/evaluate` on staging, confirm deactivation + notification row + Telegram delivery), the result must be dated in the **prior cycle's** `claude/cycles/2026-07-17__release-v7.5/qa_evidence_EPIC-02.md` DoQ sign-off block (where the original staging-only deferral was filed, per `BLG-QA-115`) — not a new file. This EPIC's own qa_evidence log (this file) tracks ST-10 as blocked pending that human action; it does not duplicate the target sign-off block.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec (ST-11/12/13 only — ST-10 is blocked, see below)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend components in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-03
- Comments: ST-11, ST-12, and ST-13 are Pass with no deviations — each independently verifiable by script output or documented measurement (agent-mediated sign-off appropriate per §5.3, all three are process/audit-shaped with no observable UI behaviour or live-system interaction). ST-10 remains `blocked_qa`, correctly excluded from this EPIC's completion — it is delegated to Director of Quality for a live staging run, tracked via its own delegation entry, not resolved by this sign-off. EPIC-04 cannot reach `merged` status until ST-10 either completes or is returned to backlog at sprint close.
