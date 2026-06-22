**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-22
**Window:** IW-20260622-01

# Idea Intake Summary — IW-20260622-01

## Window Status: Closed

Opened: 2026-06-22 00:30 UTC
Closed: 2026-06-22 00:45 UTC
Mode: Standard
Trigger: Inline — roadmap STEP -1.6 (8 open ideas in register < threshold 20)
Context: 3-day gap since IW-20260619-01; v6.0 shipped 2026-06-22; focus on v6.1 readiness

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|-----------------|--------------------|-------|
| Product Owner | 2 | 0 | 2 |
| Head of Specs Team | 2 | 0 | 2 |
| PMO Lead | 2 | 0 | 2 |
| Director of Quality | 2 | 0 | 2 |
| Strategy Rules & System Intent Owner | 2 | 0 | 2 |
| FinOps & Resource Architect | 2 | 0 | 2 |
| Infrastructure & Operations Owner | 2 | 0 | 2 |
| Facilitator | 0 | 0 | 0 |
| Challenger | 2 | 0 | 2 |
| **Total** | **16** | **0** | **16** |

## Agents Without Minimum Submissions

Facilitator — 0 submissions. Charter constraint: Facilitator role is structurally excluded from idea generation. Standard mode — noted, no halt. Consistent with IW-20260619-01 and prior window treatment.

## Ideas Available for Roadmap STEP 4

| Idea ID | Agent | Title | STEP 4 Outcome | Notes |
|---------|-------|-------|----------------|-------|
| IDEA-product-owner-20260622-01 | Product Owner | Trade gate proximity indicator on dashboard | Promoted-Backlog → BLG-FE-78 | U-story; small effort; addresses gate awareness gap; confirmed active need post-v6.0 |
| IDEA-product-owner-20260622-02 | Product Owner | Morning briefing section configurability | Parked-C1 | Hard-coded sections appropriate for v6.0 initial delivery; revisit v6.2 |
| IDEA-head-of-specs-20260622-01 | Head of Specs Team | Inline CI OpenAPI changelog validation | Promoted-Backlog → BLG-GOV-134 | P2 governance tooling; prevents BLG-OPS-73 class at root; S effort |
| IDEA-head-of-specs-20260622-02 | Head of Specs Team | Governance artefact completeness gate at STEP 0 | Parked-C1 | STEP 0 already includes artefact checks; formal gate complexity overhead not justified now |
| IDEA-pmo-lead-20260622-01 | PMO Lead | Governance health score persistence | Parked-C1 | GHS framework still maturing; persistence premature; revisit after 3+ consistent audits |
| IDEA-pmo-lead-20260622-02 | PMO Lead | Backlog item age tracking | Parked-C1 | backlog_management_prompt.md v1.9 ghost detection covers key risk; park v6.2 |
| IDEA-director-of-quality-20260622-01 | Director of Quality | Playwright spec glob registration in playwright.yml | Promoted-Backlog → BLG-QA-62 | Root-cause fix for BLG-QA-60 class; S effort; complements BLG-QA-60 firm scope |
| IDEA-director-of-quality-20260622-02 | Director of Quality | API endpoint test coverage gap report in CI | Parked-C1 | BLG-GOV-134 covers OpenAPI drift; separate endpoint test coverage report is complementary; park C1 |
| IDEA-strategy-owner-20260622-01 | Strategy Rules & System Intent Owner | PT-04/SI-02 gate proximity pre-alert in morning briefing | Parked-C1 | Dependent on PT-04 conditional scope activating; natural extension if gate clears in v6.1 |
| IDEA-strategy-owner-20260622-02 | Strategy Rules & System Intent Owner | v6.0 SI-05 effectiveness review at +30 days | Parked-C1 | Informal review appropriate at this stage; raise at v6.1 post-ship closure |
| IDEA-finops-20260622-01 | FinOps & Resource Architect | Anthropic API cost-per-briefing logging | Promoted-Backlog → BLG-OPS-74 | P3 ops item; S effort; directly tracks v6.0 morning briefing cost envelope |
| IDEA-finops-20260622-02 | FinOps & Resource Architect | Release cost estimation at release planning | Parked-C1 | Requires BLG-OPS-74 cost logging as prerequisite; revisit after BLG-OPS-74 ships |
| IDEA-infra-ops-20260622-01 | Infrastructure & Operations Owner | Background scheduler health monitoring endpoint | Parked-C1 | Background jobs minimal at current scale; park for Arc 3+ infrastructure phase |
| IDEA-infra-ops-20260622-02 | Infrastructure & Operations Owner | Deployment health dashboard widget | Parked-C1 | System status page adequate; deployment version display low urgency at current scale |
| IDEA-challenger-20260622-01 | Challenger | Hard cap on G/D/P stories until user_value_ratio ≥ 0.35 | Parked-C1 | Covered by BLG-GOV-131 (governance overhead ceiling metric — already v6.1 firm scope); hard cap rule rejected; BLG-FE-78 added to Now horizon as firm U-story to address Challenger PVC; see DL-054 |
| IDEA-challenger-20260622-02 | Challenger | Challenge PT-04 20-trade gate threshold validity | Parked-C1 | Gate reassessment debated in STEP 5; PO confirmed count-based gate retained; time-based alternative noted but not adopted; revisit post v6.1 retrospective |

## Parked Ideas Carried Forward (Not Resubmitted)

8 ideas from IW-20260619-01 incremented to Parked-cycle-2 in ideas_register.md. No resubmissions.

## STEP 4 Outcomes

- Promoted-Backlog (immediate): 4 ideas → BLG-FE-78, BLG-GOV-134, BLG-QA-62, BLG-OPS-74
- Parked-C1 (new, this window): 12 ideas
- Rejected: 0
- Note: IDEA-challenger-20260622-01 (hard cap rule) → Parked-C1; covered by BLG-GOV-131; Challenger PVC outcome recorded in DL-054

## Total Register State Post-Classification

- Parked-C2 (from IW-20260619-01): 8
- Parked-C1 (from IW-20260622-01): 11 (12 less IDEA-challenger per reclassification — 11 after IDEA-challenger remains as Parked-C1 see register)
- Total open ideas: 19

## Idea Summaries

**IDEA-product-owner-20260622-01 — Trade gate proximity indicator on dashboard**
Problem: The PT-04/SI-02 gate requires 20 closed trades. At v6.0 ship date, there are ~13 closed trades. The operator has no visible counter showing current count vs threshold without running SQL queries.
Solution: A small badge or counter on the dashboard or system status page showing `[N]/20 trades (PT-04/SI-02 gate)`. Read from existing GET /portfolio/gate-metrics endpoint (shipped v5.5, BLG-BE-34). Display-only.
Strategic alignment: Governance transparency; supports PT-04 conditional scope activation awareness.
Effort: S (~0.5 day — frontend only; endpoint already exists).
Recommendation: Promoted-Backlog → BLG-FE-78.

**IDEA-head-of-specs-20260622-01 — Inline CI OpenAPI changelog validation**
Problem: BLG-OPS-73 (PATCH /trades/{trade_id}/costs missing from api_performance_baseline.md) surfaced because there's no CI step verifying that openapi.yaml additions have corresponding entries in api_performance_baseline.md. The execution_prompt.md v3.47 advisory is a reminder, not enforcement.
Solution: Add a CI step (GitHub Actions workflow) that diffs openapi.yaml endpoints against api_performance_baseline.md endpoints and outputs a warning list. Non-blocking (advisory gate) — not a hard fail. Prevents accumulation of BLG-OPS-73 class gaps.
Strategic alignment: P2 governance tooling; OpenAPI drift detection enhancement.
Effort: S (~0.5 day).
Recommendation: Promoted-Backlog → BLG-GOV-134.

**IDEA-director-of-quality-20260622-01 — Playwright spec glob registration in playwright.yml**
Problem: BLG-QA-60 (morning-briefing.spec.js and screener-quality.spec.js not registered in playwright.yml) exists because spec registration is manual. The root cause is the explicit file list in playwright.yml — each new spec file requires a conscious registration step that is easy to miss.
Solution: Replace the explicit file list in playwright.yml with a glob pattern (e.g., `tests/e2e/**/*.spec.js`). CI picks up all spec files automatically. Eliminates the BLG-QA-60 class at root. May be implemented in same sprint as or after BLG-QA-60.
Strategic alignment: P2 QA automation; addresses systemic CI coverage gap.
Effort: S (<0.5 day).
Recommendation: Promoted-Backlog → BLG-QA-62. Note: does not replace BLG-QA-60 (which files the specific two missing specs); BLG-QA-62 is the structural fix; BLG-QA-60 is the immediate fix.

**IDEA-finops-20260622-01 — Anthropic API cost-per-briefing logging**
Problem: The morning briefing (BLG-FEAT-46, shipped v6.0) calls the Claude API each run. Token usage and estimated cost per call are not tracked anywhere. As usage scales (more frequent runs, longer briefings), cost visibility is needed.
Solution: Log token usage (prompt_tokens, completion_tokens) and estimated cost per morning briefing generation call to a log file or database table. Surface aggregate in /system-status or existing claude_audit_log. Adds to existing gemini_audit_log pattern (v3.8).
Strategic alignment: FinOps mandate; tracks cost envelope for v6.0's primary new AI feature.
Effort: S (<0.5 day — follows established claude_audit_log pattern).
Recommendation: Promoted-Backlog → BLG-OPS-74.
