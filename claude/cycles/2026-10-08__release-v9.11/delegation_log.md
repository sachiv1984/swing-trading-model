Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-08

# Delegation Log — 2026-10-08__release-v9.11

## DEL-20261008-01

- **ST Item:** ST-02 — Verify all six AI features after the PR #1921 import fix, and file the escaped-defect note
- **EPIC:** EPIC-01
- **Classification:** delegated_qa (sub-step: staging run, Human-Delegation, RISK-02)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1926
- **Branch:** exec/2026-10-08__release-v9.11/EPIC-01
- **Delegated at:** 2026-10-08T11:01:30Z
- **What is needed:** On the staging deploy, with a working Anthropic key, run each of the six AI features once from the UI: post-trade debrief (Trade History → a closed trade → Regenerate), journal summary, daily briefing, chat (one question), generate-plan and generate-thesis. For each, record the date and whether it returned generated content, the generic "unavailable" message or an error. Then opt in to AI-output sampling in Settings, trigger one feature again, and confirm a sampled row was written (or paste the sampling-path log line). The debrief may instead cite the 2026-10-07 production verification.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. This is a manual UI run on staging, so no GitHub Actions run is involved.
- **Spec reference:** `stage4_backlog_slice.md#ST-02` AC 1 and AC 2; `docs/specs/api_contracts/ai_endpoints.md`
- **Unblock criteria:** A dated six-row result table and the sampling evidence, recorded in `qa_evidence_EPIC-01.md` under ST-02. Any feature returning an error or the generic message is a defect and is filed before ST-02 closes.
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-10-08__release-v9.11/EPIC-01`
- **Status:** Pending

## DEL-20261008-02

- **ST Item:** ST-42 — Make the Non-Registry Dependency Check a required status check on main
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (repository admin action, Human-Delegation, RISK-08)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1966
- **Branch:** exec/2026-10-08__release-v9.11/EPIC-06
- **Delegated at:** 2026-10-08T11:01:30Z
- **What is needed:** Add the status check context `Non-Registry Dependency Check (ST-29)` to `main`'s branch protection `required_status_checks`, keeping the four existing contexts (`verify_governance`, `Pytest Phase A (clean tests — no DB required)`, `Endpoint Coverage Report (ST-16)`, `OpenAPI Drift Detection (ST-08)`). Via the GitHub UI (Settings → Branches → main → Require status checks), or with repository admin rights: `gh api -X POST repos/sachiv1984/swing-trading-model/branches/main/protection/required_status_checks/contexts -f 'contexts[]=Non-Registry Dependency Check (ST-29)'`. Then paste the output of `gh api repos/sachiv1984/swing-trading-model/branches/main --jq .protection.required_status_checks`.
- **Workflow viability (LL-v9.10-P3-01):** `non-registry-dependency-check.yml`, most recent success run 37764573094 (2026-10-08T10:36:23Z); 5 of the last 5 runs succeeded. The workflow triggers on every `pull_request` to `main` with no `paths:` filter, so a PR that does not touch dependency files still gets a run and is not left waiting on the check (AC 2).
- **Spec reference:** `.github/workflows/non-registry-dependency-check.yml`; `stage4_backlog_slice.md#ST-42`
- **Unblock criteria:** The `gh api` read lists the new context under `protection.required_status_checks`, and one later PR that does not touch dependency files shows the check completing. Both recorded in `qa_evidence_EPIC-06.md` under ST-42.
- **Commit format required:** `[EPIC-06][ST-42] <description>` pushed to `exec/2026-10-08__release-v9.11/EPIC-06`
- **Status:** Pending
