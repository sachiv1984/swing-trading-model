# QA Evidence Log — EPIC-05
# Cycle: 2026-03-24__release-v2.3
# Branch: exec/2026-03-24__release-v2.3/EPIC-05

---

## ST-15 — BLG-QA-03: Canonical Test Execution Report Template

**Status:** Done
**Completed:** 2026-03-25
**Implemented by:** Director of Quality (acting as QA Lead — engine-mediated)

### Acceptance Criteria Verification

| AC | Criterion | Verification | Result |
|----|-----------|-------------|--------|
| AC-1 | Template document present and usable | Code review — `docs/testing/test_execution_report_template.md` created at this commit. File is complete: header block, instructions, all required sections, DoQ sign-off block present and annotated. | PASS |
| AC-2 | Template includes all mandatory fields (scenario list, pass/fail, deviation notes, DoQ block) | Code review — §2.2 Scenario Results table (scenario list); §2.3 Pass/Fail Summary (pass/fail counts); §6 Deviation Notes (deviation notes with DEV-ID cross-reference); §7 Director of Quality Sign-Off block with full pre-sign-off checklist. All mandatory fields present. | PASS |
| AC-3 | Template is usable for both manual and automated test runs | Code review — §2.1 Run Configuration explicitly covers automated runs (test runner, spec files, run command, CI workflow, seed data, environment URL, artifact link); instructions note "Manual execution — no automated runner" as valid bypass for §2.1. §2.2 Type column values include `automated`, `manual`, `manual (visual)`, `hybrid`. Template is structurally valid for both modalities. | PASS |
| AC-4 | Template referenced in QA governance documentation | Code review — `docs/team_skills/quality/defect_lifecycle.md` updated to v1.1: §10 added with explicit cross-reference to `docs/testing/test_execution_report_template.md` as the canonical record format for Phase 5 verification reports. | PASS |

### Notes

- Template is a Class 6 Governance Template per `claude/charter/document_lifecycle_guide.md`.
- Template §7 (DoQ sign-off block) includes the verification method note required by CLAUDE.md §2 for observable UI behaviour AC.
- `defect_lifecycle.md` version incremented 1.0 → 1.1. No process rules changed — addition of §10 cross-reference only. Version increment trigger (process/severity/sign-off change) was not met; version bump applied as a documentation hygiene standard for any canonical document update.
- Template enables consistent DoQ sign-off evidence from Sprint 2 onwards per sprint backlog notes.

### DoQ Sign-Off

**Method:** Code review — this commit
**Signed off by:** Director of Quality
**Date:** 2026-03-25
**Verdict:** ✅ PASS — Full sign-off granted

**Findings:**
- All 4 acceptance criteria satisfied by code review. No observable UI behaviour involved — this story produces documentation artefacts only.
- Template is structurally complete and internally consistent with `defect_lifecycle.md` severity classification (§3.1 defect summary table mirrors `defect_lifecycle.md §9`), observation format (OBS-{NNN}, `defect_lifecycle.md §8`), and DoQ sign-off criteria (`defect_lifecycle.md §6`).
- Template's §7 pre-sign-off checklist directly encodes all criteria from `defect_lifecycle.md §6.2` — any DoQ using the template will be guided to the correct sign-off gate.
- `defect_lifecycle.md §10` cross-reference is precise: states the template is mandatory for Phase 5 verification reports submitted for DoQ sign-off.

**No deviations filed.**

---

## ST-16 — BLG-QA-04: Integration Test Coverage Report

**Status:** Done
**Completed:** 2026-03-25
**Implemented by:** QA & Testing Owner + Infrastructure & Operations Owner (engine-mediated, Director of Quality oversight)

### Acceptance Criteria Verification

| AC | Criterion | Verification | Result |
|----|-----------|-------------|--------|
| AC-1 | CI produces an endpoint coverage report on every PR | Code review — `.github/workflows/endpoint-coverage.yml` triggers on `pull_request` (branches: main, develop) and `push` (exec/**, main, develop). Runs `endpoint-coverage` job which executes the Python scanner and generates `coverage_report.md`. | PASS |
| AC-2 | Report shows each endpoint with covered / not-covered status | Code review — Coverage Detail table in generated report has one row per `METHOD /path` from openapi.yaml. Status column is one of: ✅ Covered, ⚠️ E2E only, ❌ Not covered. Current scan result: 3 covered (integration), 6 E2E-only, 38 not covered of 47 total endpoints. | PASS |
| AC-3 | Coverage gaps are visible to DoQ during sign-off | Code review — on `pull_request` events, the report is posted as a PR comment (upserted via `actions/github-script@v7`). On `push` events, the full report is printed to CI log via `cat coverage_report.md`. The Coverage Gap Summary section explicitly lists uncovered endpoints by METHOD+PATH. DoQ can see gap detail in both PR comment and CI log. | PASS |
| AC-4 | Report format machine-readable or human-readable (either acceptable) | Code review — report is human-readable markdown (table + summary). Also: the Python script writes `coverage_report.md` as a file artifact; GITHUB_OUTPUT exports `covered`, `not_covered`, `e2e_only`, `total` as machine-readable integer key-value pairs. Both formats produced. | PASS |

### Notes

- Detection engine: Python 3.11, no external dependencies (stdlib only). Same parse approach as `openapi-drift.yml` for openapi.yaml extraction.
- Pytest detection: regex `CLIENT.(get|post|put|patch|delete)("/path")` against all `tests/**/*.py`. Path normalization strips query strings and replaces f-string variables with `PARAM` for OpenAPI parameter wildcard matching.
- Playwright detection: two patterns — template literals (`` `${API_BASE}/path` ``) and regex literals (`/\/path/`). Matched against all `tests/e2e/*.spec.js`.
- Validated locally before commit: 3 pytest-covered, 6 Playwright-only, 38 not-covered, 47 total. Results are consistent with `test_automation_readiness.md` coverage baseline.
- **Advisory only** — workflow never blocks merge. Gaps are surfaced for DoQ visibility.
- No new endpoints added — no openapi.yaml update required.

### DoQ Sign-Off

**Method:** Code review + local validation run of detection script — this commit
**Signed off by:** Director of Quality
**Date:** 2026-03-25
**Verdict:** ✅ PASS — Full sign-off granted

**Findings:**
- All 4 acceptance criteria satisfied.
- CI trigger covers both PR and push events — DoQ will see the report on every PR raised against main or develop.
- Coverage gap summary section is explicit and formatted for DoQ review: lists each uncovered `METHOD /path` with no ambiguity.
- Detection script validated against live repo data before commit — numbers confirm known baseline from `test_automation_readiness.md`.
- Advisory-only design is correct: forcing this to block merge would penalise features for pre-existing test debt. The gaps are visible; closure is a separate backlog action.
- Script has no external dependencies beyond Python 3.11 stdlib — no pip install step required; CI startup time minimised.

**No deviations filed.**

---
