Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# Execution Escalations — 2026-03-04__release-v1.8

---

## ESC-EXEC-20260305-01

- **Raised at:** 2026-03-05T02:00:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-03-04__release-v1.8
- **Step:** STEP 3.1.A — Post-commit issue auto-close verification
- **ST/EPIC item:** EPIC-03 (ST-09, ST-10), EPIC-04 (ST-11, ST-12)
- **Trigger type:** GitHub
- **Blocking statement:** The `governance_sync.yml` Governance Sync Loop workflow fails on all exec/** branch pushes because the "Update State and Close Issue" step passes the story ID string (e.g. "ST-10") as the issue identifier to `gh issue close`, rather than the numeric GitHub issue number. The `gh issue close` command requires an integer issue number or URL; a string label fails with `invalid issue format`. As a result, GitHub issues for all completed autonomous ST items in EPIC-03 and EPIC-04 were not auto-closed on push, and the `sync_state` CI check appears as FAILED on PR #29 and PR #30. This blocks the "all checks green" merge gate condition even though the actual code quality checks (verify_governance, Analytics Validation Gate) passed.
- **Owning authority:** Infrastructure & Operations Owner
- **Unblock criteria:** (a) `governance_sync.yml` corrected to look up the numeric issue number from the ST ID before calling `gh issue close`; (b) PR checks re-run and sync_state passes green on both PR #29 and PR #30; OR (c) Product Owner and Director of Quality explicitly acknowledge this as a workflow infrastructure defect and grant merge authorisation for PR #29 and PR #30 despite the sync_state failure, recording their decision on each PR.
- **SLA due-by:** 2026-03-06T00:00:00Z (24 hours — Lifecycle/GitHub integrity)
- **Blocks execution:** Yes — blocks merge gate for EPIC-03 and EPIC-04
- **Disposition:** Open — Infrastructure & Operations Owner assigned
- **Resolution summary:** Fix required in `.github/workflows/governance_sync.yml` line 36: replace `"${{ steps.parse.outputs.st_id }}"` with a `gh issue list` lookup returning the numeric issue number for that ST ID. Infrastructure & Operations Owner owns this. All completed ST issues from v1.8 sprint to be closed manually by I&O Owner once fix is confirmed. SLA: 2026-03-06.

**Interim mitigation applied:** GitHub issues #25 (ST-09), #26 (ST-10), #27 (ST-11), #28 (ST-12) manually closed by engine at 2026-03-05T02:00:00Z with comments referencing this escalation ID and the commit SHAs. Issue closure is correct; the only remaining gap is the sync_state CI check on the open PRs.

**Workflow bug location:** `.github/workflows/governance_sync.yml`, line 36:

---

## ESC-EXEC-20260305-02

- **Raised at:** 2026-03-05T02:15:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-03-04__release-v1.8
- **Step:** STEP 3.1.B — Block re-evaluation for ST-03 (delegated_frontend)
- **ST/EPIC item:** EPIC-01 / ST-03 — Frontend: Risk Dashboard Page Implementation
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-03 frontend implementation was committed directly to `main` by the user (commits `0d319b4`, `b1bb3d2`, `2182b9d`, `ccbd645`, `ba6131c`, `b034d29`, `3e4d143`, `7b08fa7`, 2026-03-05 10:10–11:05 UTC) bypassing the EPIC branch (`exec/2026-03-04__release-v1.8/EPIC-01`) and not using the `[EPIC-01][ST-03]` commit format required by governance. No PR was opened. Code is now live on `main`. Two deviations were identified in the implementation vs the canonical spec: (1) P2 — Entity store fallback (`base44.entities.Position` / `base44.entities.Portfolio`) masks API failure states, preventing QA from verifying the "each component renders its own error state independently" acceptance criterion; (2) P3 — GracePeriodPanel shows the empty state ("No positions in grace period") on API failure — indistinguishable from a valid empty state. Engine cannot retroactively enforce branch governance or undo the merge. Product Owner acceptance required.
- **Owning authority:** Product Owner
- **Unblock criteria:** Product Owner records acceptance of the ST-03 implementation as meeting ST-03 acceptance criteria (with deviations noted); confirms the P2 entity fallback deviation is either accepted (with backlog item raised) or removed before QA sign-off is sought; confirms the P3 GracePeriodPanel error state gap is accepted or addressed. ST-03 will then be marked `done` and ST-04 will proceed.
- **SLA due-by:** 2026-03-06T02:15:00Z (24 hours — Lifecycle / Process Integrity)
- **Blocks execution:** No — ST-04 QA scenario authoring may begin in parallel; QA execution against the implementation can begin; merge of EPIC-03 and EPIC-04 is unaffected. However, ST-03 cannot be formally marked `done` and EPIC-01 cannot proceed to merge gate without Product Owner acceptance.
- **Disposition:** Resolved
- **Resolution summary:** Product Owner accepted ST-03 implementation on 2026-03-05. All 8 deviations (DEV-ST03-01 through DEV-ST03-08) accepted for v1.8; documented in `docs/specs/frontend/pages/risk_dashboard.md §11` v0.1.1. Backlog items to be assigned before cycle close (DEV-ST03-01 through DEV-ST03-07). DEV-ST03-08 (drawdown data source) flagged to Head of Specs Team for spec update. Governance breach acknowledged — future sprints must use EPIC branches and compliant commit format without exception. ST-03 marked `done`. ST-04 now active.

**Deviations for documentation in canonical spec (`docs/specs/frontend/pages/risk_dashboard.md`) once Product Owner accepts:**

| Ref | Priority | Description | Canonical requirement | Actual behaviour | Target resolution |
|-----|----------|-------------|----------------------|------------------|-------------------|
| DEV-ST03-01 | P2 | Entity store fallback masks API error states | Each component renders its own error state independently on `GET /portfolio` failure | Fallback to `base44.entities.Position` / `base44.entities.Portfolio` hides the failure; error states not shown when entity data exists | v1.9 — remove fallback or make it explicit opt-in post-error-display |
| DEV-ST03-02 | P3 | GracePeriodPanel error vs empty state indistinguishable | GracePeriodPanel renders its own error state on API failure | On API failure, `positions` is `[]`; "No positions in grace period" shown — cannot be distinguished from valid empty state | v1.9 — surface error card if `portfolioError` is set |
```yaml
gh issue close --comment "Resolved via Claude Code commit: ${{ steps.parse.outputs.st_id }}" "${{ steps.parse.outputs.st_id }}"
```
The last argument `"${{ steps.parse.outputs.st_id }}"` must be replaced with the numeric issue number obtained by querying `gh issue list --search "[ST-xx]"`.
