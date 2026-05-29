Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-29
Cycle: 2026-05-29__release-v4.3

---

# Lessons Learnt — 2026-05-29__release-v4.3

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-05-29__release-v4.3
**Section anchor:** `## Phase 3`
**Filed:** 2026-05-29
**Reviewed by:** PMO Lead
**Prior cycle Phase 3 checked:** claude/cycles/2026-05-27__release-v4.2/lessons_learnt_cycle.md — found.

**Prior cycle deferred items check:**
- v4.2 deferred item 1 — qa_signed_off stale state: **RESOLVED** in v4.3 ST-01. execution_prompt.md v3.31 added advisory to STEP 3.2.A: set `qa_signed_off: true` immediately after DoQ sign-off in the same commit as the QA evidence file.
- v4.2 deferred item 2 — branch safety at sprint close: **RESOLVED** in v4.3 ST-02. execution_prompt.md v3.32 added hard gate to STEP 8: halt if not on main. Advisory added to STEP 5.3. HoST decision: gate (halt if not on main).
- v4.2 Phase 4 deferred item — AC 1:1 mapping advisory: **RESOLVED** in v4.3 ST-03. qa_evidence_template.md v1.3 adds advisory that evidence table rows should map 1:1 to backlog slice ACs.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Wrong staging URL for ST-13/ST-14 initial checks: all health checks and timing measurements initially ran against the frontend SPA URL (`trading-assistant-staging.onrender.com`) rather than the backend API URL (`trading-assistant-api-staging.onrender.com`). Frontend SPA returns HTTP 200 for all routes (catch-all). ST-13 AC-02/03 and ST-14 timing results (55ms, invalid) were collected against the SPA. Discovery required re-run of all checks against backend API URL; corrected results were p50=2,541ms. Artefacts updated: parity report v1.0→v1.1, api_performance_baseline.md v1.8→v2.0. | Phase 3 | B | defer | Add a "Staging URL disambiguation" section to the staging parity report template (or OPERATIONAL_GUIDE.md §7 staging guidance) explicitly noting that Render deploys two separate services — frontend SPA and backend API — with different hostnames. Health checks and performance baselines must target the backend API URL, not the frontend. BLG-OPS-43. | Infrastructure & Operations Owner | v4.4 |
| All 3 EPIC-04 stories (ST-16/17/18) were sprint-planned as delegated_frontend but reclassified to autonomous at execution start per LL-v2.3-CL-01. This is the third consecutive sprint where all frontend items of this type (prop pass-through, variable rename, new UI section against locked spec) proved fully autonomous. Sprint planning is defaulting to delegated_frontend for any frontend work, even when the engine has demonstrated capability for this class of change. | Phase 3 | E | defer | Update sprint_planning_prompt.md classification guidance: add a "frontend classification fast-path" — if the story involves (a) a bug fix in prop/state threading, (b) a variable rename in React code, or (c) a new section/component against a locked spec with Playwright feasibility confirmed, default to autonomous unless the story involves new design decisions. Reduces unnecessary delegated_frontend planning overhead and avoids false delegation records. | Head of Specs Team | v4.4 |
| deviations_filed=False for staging delegation stories (ST-13/14/06/07/08) at sprint close: 5 stories with zero spec deviations had deviations_filed=False. The STEP 5.1 enforcement rule correctly auto-corrected these at sprint close. However, the correction required a Python script batch-fix rather than being applied individually at each story's sign-off step. Minor coordination friction. | Phase 3 | A | defer | Add reminder to execution_prompt.md delegation sign-off substep: when recording sign_off_record.status = "cleared" for a delegated story, also set deviations_filed = true if no deviation record was filed. This prevents accumulation of false-False flags that require batch correction at sprint close. | Head of Specs Team | v4.4 |
| All 3 v4.2 deferred items (qa_signed_off advisory, branch safety gate, AC 1:1 mapping) resolved cleanly in this sprint via ST-01/02/03. Governance patch mechanism working reliably — OA-to-story-to-patch pipeline completed within one cycle of filing. | Phase 3 | E | action-now | Positive: OA carry-forward resolution rate 100% for v4.3 (3/3 deferred items resolved). No process change needed. | Sprint Execution Engine | — |
| ANTHROPIC_API_KEY staging policy change: prior policy of "production-only" for ANTHROPIC_API_KEY had no technical basis and created recurring ST-06 staging friction. Changed permanently in v4.3: ANTHROPIC_API_KEY and REACT_APP_ANTHROPIC_API_KEY=true now configured on staging. Removes this blocker from all future QA cycles involving AI feature staging tests. | Phase 3 | E | action-now | Positive: infrastructure policy updated proactively. Security register and parity report updated to reflect new staging configuration. No further action needed. | Sprint Execution Engine | — |

**Recurrence Notes:**
- **Wrong staging URL:** New item this cycle. Not a recurrence. Discovery resolved and documented; defer to staging guidance update (BLG-OPS-43) in v4.4.
- **delegated_frontend reclassification:** Third consecutive cycle (v4.1, v4.2, v4.3 EPIC-04). Escalating from observation to classification guidance change in sprint_planning_prompt.md.
- **deviations_filed flag:** New in this form; minor process friction. Defer to execution_prompt.md update.
- **v4.2 deferred items resolved:** All 3 resolved within one cycle — no recurrence escalation.
