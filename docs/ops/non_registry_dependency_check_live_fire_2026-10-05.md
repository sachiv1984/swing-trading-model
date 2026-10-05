**Owner:** Infrastructure & Operations Owner; Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Complete
**Last Updated:** 2026-10-05 (ST-17, BLG-QA-193, EPIC-03, v9.9 — initial record)
**Source:** ST-17 (BLG-QA-193, EPIC-03, cycle `2026-09-30__release-v9.9`)

---

# Non-Registry Dependency Check — Live-Fire Confirmation

## Why

The `Non-Registry Dependency Check (ST-29)` workflow (`.github/workflows/non-registry-dependency-check.yml`, running `scripts/check_non_registry_dependencies.py`) was unit-tested, but nobody had seen it fail on a real pull request. It had also not been confirmed whether a failing run blocks a merge to `main`.

## Live-fire run

- **Throwaway PR:** #1887 (draft, `throwaway/st17-non-registry-livefire` → `main`), adding one line to `backend/requirements.txt`:
  `nonexistent-st17-livefire @ git+ssh://git@github.com/sachiv1984/nonexistent-st17-livefire.git`
- **Result: failed, as intended.** Run: https://github.com/sachiv1984/swing-trading-model/actions/runs/37282917791/job/111674945804
  - Log: `backend/requirements.txt:17: non-registry dependency specifier: 'nonexistent-st17-livefire @ git+ssh://…'` → `1 violation(s) found.` → `Process completed with exit code 1.`
  - The failure is the guard's own detection, not an infrastructure error.
- PR #1887 was closed unmerged and its branch deleted on 2026-10-05. Nothing reached `main`.
- Side effect, as expected: `Pytest Phase A` also failed on that PR, because `pip install -r requirements.txt` cannot resolve the fake dependency. A real PR adding such a dependency would therefore fail Phase A as well — but that is incidental, not a control.

## Required-status-check state on `main` (recorded 2026-10-05)

From `gh api repos/sachiv1984/swing-trading-model/branches/main` (`protection.required_status_checks`; enforcement level `non_admins`):

| Required check |
|---|
| `verify_governance` |
| `Pytest Phase A (clean tests — no DB required)` |
| `Endpoint Coverage Report (ST-16)` |
| `OpenAPI Drift Detection (ST-08)` |

**`Non-Registry Dependency Check (ST-29)` is not a required status check.** A failing run of it does not by itself block a merge. Today, a `requirements.txt` non-registry entry is still blocked indirectly, through the required `Pytest Phase A` check failing at install. That indirect block does not cover `package.json`/`package-lock.json` entries, which the guard also checks.

No repository rulesets apply to `main` (`gh api …/rules/branches/main` returns `[]`). The full classic protection settings could not be read (`GET …/branches/main/protection` returns 403 for the session's token), so the table above is the read-only protection summary.

## Follow-up

Making the check required is a repository-settings change that needs admin access. It is raised to the Infrastructure & Operations Owner as `BLG-OPS-177`.
