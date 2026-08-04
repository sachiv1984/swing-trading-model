Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-04

# QA Evidence — EPIC-03 (Governance Process Integrity Cluster)

**EPIC:** EPIC-03 — Governance Process Integrity Cluster
**Cycle:** 2026-08-04__release-v8.2
**Sprint goal:** Ship v8.2's curated full-capacity scope — five ready user-facing/UX improvements leading the release, staging/production security hardening, an 11-item governance-process integrity cluster, CI/operations hardening, and QA/spec debt cleanup — advancing the release's explicit "user features first" priority within the confirmed capacity band.
**Test scenarios used:** No runnable test files apply — this EPIC is a governance-process integrity cluster (11 process-audit, documentation, and CI-workflow stories); verification is by code/document review against each story's canonical spec or protocol, per the BLG-GOV-19 autonomous class criteria below.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|-----------------|------------------|-----------------------|--------|------------|
| ST-08 | `claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md#30-Day Review — 2026-08-04` | Filed the overdue SI-05 Phase 1 30-day effectiveness review record — all 3 criteria FAIL (PO attests no digest since 2026-06-17), Phase 2 activation PAUSEd, re-evaluation 2026-10-03, 2 follow-up backlog items filed | Formal review record filed with all 3 criteria PASS/FAIL; evidence recorded; PO self-assessment attested; Phase 2 decision recorded; DoQ sign-off on evidence completeness | Pass | None |
| ST-09 | `claude/cycles/velocity_metrics.md#Row-Count Audit` | Audited velocity_metrics.md row count against completed release cycles; found and backfilled 3 missing rows (v1.7, v1.8, v2.0) | One-time audit comparing row count against completed cycles; parity confirmed or missing rows backfilled | Pass | None |
| ST-10 | `docs/specs/metrics_definitions.md#v6.9 On-Demand Compliance Recheck — Confirmed No Formula Gap` | Reviewed Arc 5 composite formula against v6.9's on-demand compliance-recheck event type; traced write paths, confirmed no gap exists (recheck feature is non-persisted) | Formula reviewed against v6.9 event type; updated if gap exists or confirmed correct; sign-off | Pass | None |
| ST-11 | `claude/system/post_ship_closure.md#Rebalance Cadence Check` | Corrected the Rebalance Cadence Check to read current_roadmap.md §1 before recommending skip, avoiding stale advisory for a [TBD]/already-consumed next release | STEP 0 reads current_roadmap.md §1 before skip advisory; corrected warning for TBD/consumed case; unchanged advisory for fresh case; governance edit checklist applied | Pass | None |
| ST-12 | `docs/specs/security/ai_vendor_tos_dpa_review.md` | Reviewed AI vendor ToS/DPA — scope-corrected to Anthropic only (Gemini has no live integration, verified via code inspection); no gaps found in Anthropic Commercial API terms | Both vendors' current ToS/DPA reviewed; findings documented; gaps flagged with remediation; sign-off | Pass | None |
| ST-13 | `claude/roadmap/governance_bypass_log.md` | New structured, append-only governance bypass tracker; backfilled with 8 historical instances found by scanning decision_log.md and amendment folders | Structured append-only log created; backfilled with known historical instances; sign-off | Pass | None |
| ST-14 | `docs/governance/idea_intake_overlap_check_retrospective_2026-08-04.md` | Retrospective on v2.8 backlog-overlap check effectiveness — 52.3% pre-fix vs 0% post-fix rejection rate; recommendation: keep unchanged | Retrospective performed on whether check reduced rejection rates; recommendation recorded; sign-off | Pass | None |
| ST-15 | `claude/system/roadmap_prompt.md#STEP 2.3 — Standing-behaviour decision` | Product Owner formally accepted the SI-02 credential fallback-citation pattern as permanent behaviour; closed the recurring "should attempt genuine live re-check" carry-forward pattern | Decision recorded (option a or b); if (b), STEP 2.3 updated to remove open-gap framing; sign-off | Pass | None |
| ST-16 | `claude/system/design_gate_prompt.md#STEP 1 — Classify Each Item` | Added mandatory §13 boundary pre-check for AI-calling proposals at design gate classification time | §13 boundary pre-check step added for AI-calling proposals; governance edit checklist applied; sign-off | Pass | None |
| ST-17 | `claude/system/shared_standards.md#§16.14 Last Updated Header-History Retention Convention` | New retention rule (current + 2 prior entries, 3 total); applied at roadmap_prompt.md STEP 9 and ideas_housekeeping_prompt.md §1.4; applied retroactively to ideas_register.md | Formal retention rule with depth/age threshold; applied automatically at both write sites; sign-off | Pass | None |
| ST-18 | `.github/workflows/governance_sync.yml`; `claude/system/shared_standards.md#GitHub CLI Commands` | governance_sync.yml now cross-checks execution_state status before auto-closing issues, fixing a false-positive that recurred twice (v8.0 EPIC-02/ST-08, v8.1 EPIC-02/ST-02) | Delegation-record commit no longer closes issue; genuine completion commit still closes; convention documented; sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: N/A (no runnable test files for this EPIC's scope — governance process/documentation/CI-workflow work). ST-18's fix to `.github/workflows/governance_sync.yml` was unit-tested locally by extracting and running its `is_story_done()` bash logic against 4 fixture scenarios (per-EPIC done/blocked, legacy-format done/not_started) with `jq 1.8.1`, all passing — documented in the story-level sign-off.
- Regression areas checked: `claude/system/OPERATIONAL_GUIDE.md` §14 governance table 3-way self-consistency (header/§14 self-row/changelog top row) verified after every edit in this EPIC (7 separate version bumps across `post_ship_closure.md`, `design_gate_prompt.md`, `roadmap_prompt.md` ×2, `shared_standards.md` ×2, `ideas_housekeeping_prompt.md`) — full governance-drift scan run before the final commit, zero mismatches found.
- Known deviations filed: None

**Frontend testing gate (CLAUDE.md §2):** Not applicable — zero files under `src/pages/` or `src/components/` were touched by any story in this EPIC (confirmed via `git diff origin/main..HEAD --stat`).

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All 11 stories in this EPIC have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/components/**` or `src/pages/**` was created or modified — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-04
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable, no frontend changes, engine signer populated).

**EPIC-level consolidation note (BLG-GOV-14):** Per BLG-GOV-14, a domain-authority sign-off at story level does not by itself substitute for this EPIC-level block — both are required. The following story-level domain-authority sign-offs (all agent-mediated, §5.3) are confirmed cleared as of this EPIC-level sign-off:

| Story | Domain Authority | Status |
|-------|-------------------|--------|
| ST-08 | Director of Quality | Cleared |
| ST-09 | PMO Lead | Cleared |
| ST-10 | Metrics Definitions & Analytics Canonical Owner | Cleared |
| ST-11 | Head of Specs Team | Cleared |
| ST-12 | AI Compliance & Governance Officer | Cleared |
| ST-13 | PMO Lead | Cleared |
| ST-14 | PMO Lead | Cleared (one blocking finding fixed in-session before clearing — see ST-14's own sign-off notes) |
| ST-15 | Product Owner | Cleared |
| ST-16 | Strategy Rules & System Intent Owner | Cleared |
| ST-17 | Head of Specs Team | Cleared |
| ST-18 | Head of Engineering | Cleared (one hardening finding fixed in-session before clearing — see ST-18's own sign-off notes) |

Both story-level review agents (ST-14, ST-18) independently caught real issues — a fabricated citation and a shell-scripting edge case respectively — that were fixed before sign-off cleared, consistent with the multi-layer review process this EPIC's own subject matter (governance process integrity) is about.
