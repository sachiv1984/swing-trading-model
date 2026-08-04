Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-04
Cycle: 2026-08-04__release-v8.2
Release: v8.2

# Backlog Slice — v8.2

<!-- release-plan-marker: RP:v8.2:2026-08-04__release-v8.2 -->

25 stories across 5 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution).

---

## EPIC-01 — User-Facing Features & UX

**Maps to:** S2-01
**Owner:** Financial Reporting & Records Owner; Head of UX & Design; Metrics Definitions & Analytics Canonical Owner

**Staging-only ACs:** ST-02, ST-03, ST-04 each carry an observable UI acceptance criterion — see RISK-01; Design Gate PASS or Playwright coverage/staging sign-off required before these ACs may be considered met (per CLAUDE.md §2). ST-01's reconciliation report is also observable UI (new view) and falls under the same gate.

### ST-01 — P&L / tax record reconciliation report (system totals vs individual trade export)
**Source:** BLG-FEAT-88
**Effort:** M
**Acceptance Criteria:**
- Reconciliation report/view added comparing system-computed P&L totals against a sum of the individual trade export
- Confirmed to match on current data
- Financial Reporting & Records Owner sign-off
- Playwright coverage or a recorded staging sign-off confirms the view renders correctly

### ST-02 — Compliance Recheck Modal all-pass empty-state design
**Source:** BLG-FE-105
**Effort:** S
**Acceptance Criteria:**
- All-rules-pass empty state confirmed or specified for `ComplianceRecheckModal.js`
- Implemented if a gap is found
- Playwright coverage or a recorded staging sign-off confirms the empty state renders correctly
- Head of UX & Design sign-off

### ST-03 — RFJ event type colour palette refinement
**Source:** BLG-FE-67
**Effort:** XS
**Acceptance Criteria:**
- Red Flag Journal event-type colours revised so `checklist_skipped` no longer blends with risk-event colours and `drawdown_prompt_dismissed` is perceptually distinct from `stop_prompt_dismissed`, including under the `light-daltonized` theme
- Playwright coverage or a recorded staging sign-off confirms the new palette
- Head of UX & Design sign-off

### ST-04 — Trade Plan native form fields use a weaker focus indicator than the rest of the codebase
**Source:** BLG-FE-138
**Effort:** S
**Acceptance Criteria:**
- All native form fields on the Trade Plan page use the same `focus-visible:ring-*` pattern as the shared UI primitives (`src/components/ui/{input,select,button,dialog}.js`)
- No visual regression to unfocused-state styling
- Playwright coverage or a recorded staging sign-off confirms the fix
- Head of UX & Design sign-off

### ST-05 — Drift-detection metric for the behavioural-drift endpoint's `insufficient_data` streak
**Source:** BLG-FEAT-86
**Effort:** S
**Acceptance Criteria:**
- Streak-length metric added (consecutive `insufficient_data` readings, trade-count trend) surfaced alongside the existing SI-02 gate note
- Metric defined and documented
- Metrics Definitions & Analytics Canonical Owner sign-off

---

## EPIC-02 — Staging/Production Security Hardening

**Maps to:** S2-02
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner

### ST-06 — Provision a distinct API key for the staging environment
**Source:** BLG-SEC-27
**Effort:** S
**Acceptance Criteria:**
- Staging and production authenticate with two different, independently-revocable API key values
- Confirmed live: the old shared key no longer works against production after rotation
- Cybersecurity & Trust Lead sign-off

### ST-07 — Detect silent staging deploy staleness (GitHub↔Render auto-deploy webhook can fail silently)
**Source:** BLG-OPS-128
**Effort:** S
**Acceptance Criteria:**
- Root cause of the webhook failure identified and fixed (or documented if unresolvable)
- Recurring drift-detection check added comparing staging's deployed commit SHA against `origin/main`'s HEAD, alerting if they drift beyond a threshold
- Confirmed firing correctly on a deliberately-stale test
- Infrastructure & Operations Owner sign-off

---

## EPIC-03 — Governance Process Integrity Cluster

**Maps to:** S2-03
**Owner:** Product Owner; Infrastructure & Operations Owner; Metrics Definitions & Analytics Canonical Owner; Head of Specs Team; AI Compliance & Governance Officer; PMO Lead; Strategy Rules & System Intent Owner; Head of Engineering

### ST-08 — File SI-05 Phase 1 30-day effectiveness review record
**Source:** BLG-GOV-160
**Effort:** XS
**Acceptance Criteria:**
- Formal review record filed with all three criteria assessed (PASS/FAIL for each)
- `si05_digest_log` evidence for the relevant send windows recorded
- PO self-assessments for Criteria 1 and 2 attested in the record
- Phase 2 activation decision (PROCEED / ITERATE / PAUSE) recorded by Product Owner
- Director of Quality sign-off on evidence completeness

### ST-09 — `velocity_metrics.md` row-count audit against cycle folder count
**Source:** BLG-GOV-213
**Effort:** S
**Acceptance Criteria:**
- One-time audit comparing `velocity_metrics.md` row count against completed release cycles in `claude/cycles/`
- Audit confirms parity, or missing rows are backfilled

### ST-10 — Confirm Arc 5 composite formula accounts for v6.9 recheck events
**Source:** BLG-GOV-214
**Effort:** S
**Acceptance Criteria:**
- `metrics_definitions.md` v1.11 Arc 5 composite compliance formula reviewed against v6.9's on-demand compliance-recheck event type
- Formula updated if a gap exists, or confirmed already correct
- Metrics Definitions & Analytics Canonical Owner sign-off

### ST-11 — Rebalance-skip advisory should verify next release is actually scoped
**Source:** BLG-GOV-218
**Effort:** S
**Acceptance Criteria:**
- `post_ship_closure.md` STEP 0's Rebalance Cadence Check reads `current_roadmap.md` §1 before recommending skip
- A cycle closing with an odd `completed_cycle_count` but a `[TBD]`/already-consumed next release produces a corrected warning, not the unconditional skip advisory
- A cycle closing with a genuinely fresh, unconsumed Option(b)/Option(a) scoping decision still gets the skip advisory as before (no regression)
- Standard governance file edit checklist applied (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry)

### ST-12 — AI vendor Terms-of-Service & data-processing review (Gemini/Claude, financial data handling)
**Source:** BLG-GOV-265
**Effort:** S
**Acceptance Criteria:**
- Both vendors' current ToS/DPA terms reviewed against the system's financial-data handling (retention, training-data use, sub-processor disclosure)
- Findings documented; any gap flagged with a remediation item
- AI Compliance & Governance Officer sign-off

### ST-13 — Direct-write / governance-bypass pattern tracker (roadmap & amendment gate bypasses)
**Source:** BLG-GOV-269
**Effort:** M
**Acceptance Criteria:**
- Structured, append-only log created of every direct-write bypass of a governed routine (date, file, reason given, routine bypassed)
- Backfilled with the known historical instances (v7.4 AMD, v7.5, v7.6 DL-073, v7.7 DL-074, and others)
- PMO Lead sign-off

### ST-14 — Idea-intake backlog-overlap check effectiveness retrospective (v2.8, post-N-windows)
**Source:** BLG-GOV-278
**Effort:** S
**Acceptance Criteria:**
- Retrospective performed on whether the v2.8 mandatory backlog-overlap check materially reduced downstream STEP 4 rejection rates
- Recommendation recorded (keep/adjust/retire the check)
- PMO Lead sign-off

### ST-15 — SI-02 production credential provisioning decision (formalise fallback vs acquire)
**Source:** BLG-GOV-279
**Effort:** S
**Acceptance Criteria:**
- Decision recorded: (a) persist the credential into checked-in-but-gitignored environment config, or (b) formally accept the fallback-citation pattern as standing behaviour
- If (a): implemented
- If (b): `roadmap_prompt.md` STEP 2.3 updated to remove the "should attempt genuine live re-check" framing as an open gap
- Product Owner sign-off

### ST-16 — Mandatory §13 boundary pre-check at design gate for new AI-calling feature proposals
**Source:** BLG-GOV-281
**Effort:** S
**Acceptance Criteria:**
- Mandatory §13 boundary pre-check step added to `design_gate_prompt.md` for proposals that call an AI provider
- Standard governance file edit checklist applied
- Strategy Rules & System Intent Owner sign-off

### ST-17 — Codify a `Last Updated` header-history retention convention
**Source:** BLG-GOV-283
**Effort:** S
**Acceptance Criteria:**
- Formal retention rule documented in `shared_standards.md` with an explicit depth/age threshold
- `roadmap_prompt.md` STEP 9 (and `idea_intake_prompt.md`'s equivalent for `ideas_register.md`) updated to apply it automatically, per the standard governance file edit checklist
- Head of Specs Team sign-off

### ST-18 — governance_sync.yml auto-close regex cannot distinguish delegation-record commits from completion commits
**Source:** BLG-GOV-285
**Effort:** S
**Acceptance Criteria:**
- A delegation-record-only commit referencing `[ST-xx]` no longer closes that story's GitHub issue
- A genuine completion commit still closes the issue as today
- Convention documented in `shared_standards.md` §8
- Head of Engineering sign-off

---

## EPIC-04 — Operations & CI Hardening

**Maps to:** S2-04
**Owner:** Head of Engineering; Infrastructure & Operations Owner

### ST-19 — Quarterly dependency-upgrade cadence for backend/requirements.txt
**Source:** BLG-OPS-116
**Effort:** S
**Acceptance Criteria:**
- Quarterly review cadence for `backend/requirements.txt` dependency versions documented
- First review scheduled

### ST-20 — CI cache tuning to reduce Playwright suite runtime
**Source:** BLG-OPS-118
**Effort:** S
**Acceptance Criteria:**
- CI caching (dependency install, browser binaries) reviewed and tuned for the Playwright job
- Measurable CI runtime reduction on the Playwright job
- No test reliability regression

### ST-21 — Automated commit-message format lint (pre-commit hook for [EPIC-xx][ST-xx] convention)
**Source:** BLG-OPS-125
**Effort:** S
**Acceptance Criteria:**
- Pre-commit hook added that lints the commit message format on `exec/**` branches
- Confirmed to reject a deliberately malformed commit message
- Head of Engineering sign-off

---

## EPIC-05 — QA & Spec Debt Cleanup

**Maps to:** S2-05
**Owner:** QA & Testing Owner; Head of Specs Team; Head of Engineering; Head of UX & Design

### ST-22 — Snapshot test for `SystemStatus.js` hardcoded fallback counts
**Source:** BLG-QA-126
**Effort:** S
**Acceptance Criteria:**
- Snapshot/assertion test added comparing the hardcoded fallback value against an AST-derived count of registered endpoint tests
- Test fails on a deliberately-stale fallback value
- QA & Testing Owner sign-off

### ST-23 — Reconstruct 13 undocumented versions in sprint_planning_changelog.md (v3.1–v3.13)
**Source:** BLG-SPEC-110
**Effort:** M
**Acceptance Criteria:**
- All 13 missing rows (3.1–3.13) added to `sprint_planning_changelog.md` in newest-first order, consistent with the surrounding rows, using `git log -p` as the reconstruction source
- Head of Specs Team sign-off

### ST-24 — Remove dead-code duplicate POST /test/endpoints handler in backend/main.py
**Source:** BLG-BE-81
**Effort:** XS
**Acceptance Criteria:**
- Duplicate `POST /test/endpoints` handler removed from `backend/main.py`
- `backend/routers/test.py`'s route remains the sole handler for this path
- Full backend regression suite passes with no change in behaviour

### ST-25 — Design-gate checklist addendum for motion/timing-sensitive chart interactions
**Source:** BLG-FE-131
**Effort:** S
**Acceptance Criteria:**
- Explicit motion/timing-sensitive interaction checklist item added to the design gate classification table in `design_gate_prompt.md`
- Head of UX & Design sign-off

---

## Capacity Summary (see `release_plan.md §Capacity Check` for full detail)

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days |
| Total estimated effort (in-scope) | ~24.7 days |
| Utilisation | ~88-103% |
| Over-allocation | No |
