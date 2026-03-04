**Owner:** Head of Engineering
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Head of Engineering
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-head-of-engineering-20260304-01

---

# Idea: Dependency Vulnerability Scanning in CI

## 1. Problem Statement

The Python backend has external dependencies (FastAPI, psycopg2, pydantic, and others) that accumulate known security vulnerabilities over time as CVEs are published. There is currently no automated check in the CI pipeline that identifies vulnerable dependencies before they reach production. A vulnerable dependency that was safe when pinned may become a security risk weeks later when a CVE is published — and without automated scanning, this would not be detected until a manual review or a security incident.

## 2. Strategic Alignment

Section reference: §13 — System boundaries ("a deterministic decision-support engine" that handles real financial data and user credentials)

Alignment rationale: A system handling live financial data has an obligation to maintain a defensible security posture. Dependency vulnerability scanning is a standard baseline for any production Python application. The absence of automated scanning means the Head of Engineering cannot assert that the system's dependencies are free of known vulnerabilities — which is a reliability and security gap in the engineering programme.

## 3. Proposed Solution

Add `pip-audit` (or `safety check`) to the CI pipeline. Run on every PR and on a scheduled weekly basis against the main branch. Report vulnerabilities as warnings for low/medium severity; block merges for high/critical severity CVEs. Configure an exception process for cases where a vulnerable dependency cannot be immediately upgraded (e.g., waiting for an upstream fix). Document the exception process in `docs/team_skills/engineering/dependency_management.md`.

## 4. Expected Value

Reduces time-to-detect for new dependency vulnerabilities from "after a security incident or manual review" to "at the next PR or weekly scan." Ensures the engineering team is informed of all high/critical CVEs in dependencies before they reach production. Target: zero high/critical CVEs in production dependencies at any point in time.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires adding `pip-audit` to the CI environment. May surface existing vulnerabilities that require immediate remediation — plan for a short remediation sprint if the first scan reveals critical issues.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: Removing a CI step is trivial; no architectural lock-in.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: This is a baseline engineering hygiene control with near-zero implementation cost. Every day without it is a day where a new CVE in a dependency goes undetected.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | |
| Classification date | |
| Classified by | Product Owner |
| STEP 5 outcome | |
| Outcome date | |
| Notes | |
