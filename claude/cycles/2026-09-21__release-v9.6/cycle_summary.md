Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-09-21 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-09-21__release-v9.6

**Release:** v9.6 — Build-and-Ship Pull-Forward & Full-Capacity Debt Clearance

**Run type:** Backlog-driven (no formal roadmap section — STEP -1.2 Option (b) equivalence from the `2026-09-19__scheduled` rebalance, extending the v8.5–v9.5 pattern, now 14 consecutive release cycles).

**Anchor scope:** `BLG-FEAT-96` ("Clone as new plan") and `BLG-FEAT-97` (CSV export for Screener and Watchlist) — the two build-and-ship U-items the Product Owner committed at the 2026-09-19 rebalance to satisfy the Skill-Silo Alert's mandatory ≥2 pull-forward (alert at 98.8%, 5th consecutive worsening reading). Both are seated in the leading EPIC-01, alongside `BLG-FEAT-98`.

**Capacity decision (explicit user instruction, this invocation): "use full capacity".** Applied as: all 8 ready P2 items first (the ready pool holds 0 P1), then category-balanced round-robin oldest-first across 7 themes, reaching **28.00 estimated days — exactly the top of the confirmed ~24–28 day band** (27.90 days under a band-letter-only reading).

**Scope:** 32 stories across 7 EPICs:
- EPIC-01 — Product Features & Frontend Build-and-Ship (6 items: `BLG-FEAT-96`, `BLG-FE-180`, `BLG-FEAT-97`, `BLG-FEAT-98`, `BLG-FE-181`, `BLG-FE-182`)
- EPIC-02 — Financial Reporting & Records Integrity (2 items: `BLG-FR-04`, `BLG-FR-05`)
- EPIC-03 — Backend & Platform Engineering Debt (5 items: `BLG-BE-119`, `BLG-BE-118`, `BLG-BE-120`, `BLG-BE-121`, `BLG-BE-122`)
- EPIC-04 — Operations & Security Debt (4 items: `BLG-OPS-166`, `BLG-OPS-163`, `BLG-OPS-164`, `BLG-OPS-165`)
- EPIC-05 — QA & Test Coverage Debt (4 items: `BLG-QA-171`, `BLG-QA-172`, `BLG-QA-173`, `BLG-QA-178`)
- EPIC-06 — Spec & Documentation Debt (5 items: `BLG-SPEC-148`, `BLG-SPEC-160`, `BLG-SPEC-144`, `BLG-SPEC-145`, `BLG-SPEC-146`)
- EPIC-07 — Governance Process Debt (6 items: `BLG-GOV-345`, `BLG-GOV-329`, `BLG-GOV-328`, `BLG-GOV-325`, `BLG-GOV-90`, `BLG-GOV-188`)

**Capacity:** 28.00 estimated days vs confirmed ~24–28 day band — PASS, at the top of the band, matching the explicit "use full capacity" instruction. The §1.5 95% buffer floor is exceeded (100.0%); acknowledgement is due at Sprint Planning.

**Scope-selection method:** Gate-detection procedure run against the current 212-item active backlog (`scripts/scan_backlog_gate_conditions.py`): 131 gated, 4 data-quality warnings. Six date-lapsed gates read individually (2 cleared and selected, 4 not cleared — owner verification due at the 2026-09-24 AI review). 7 further items excluded as not open work or substantively gate-blocked. Result: a 76-item / 61.75-day ready pool → 32 items / 28.00 days via `release_planning_prompt.md` §1.4c.

**Deferred:** `BLG-FEAT-73`/`74`/`76` (substantively gate-blocked); `BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`, `BLG-GOV-140`/`141`/`142`, `BLG-OPS-88` (within-sprint date gate 2026-09-24, classified conditional — re-eligible at v9.7); `BLG-GOV-335`/`336`/`337`/`326` (already complete/satisfied — archive at next groom); 121 further gated items; 44 further ready items (~33.75 days), including **12 items tagged `Provisional-Target: v9.6` (4.80 days)** — see Decisions Needed below.

**Escalations:** None raised during this release-planning session.

**Design Gate:** **Required.** All 6 EPIC-01 items and both EPIC-02 items carry an observable UI acceptance criterion — `BLG-FEAT-96` (Clone action), `BLG-FEAT-97` (export control), `BLG-FEAT-98` (in-app reminder), `BLG-FE-180` (stale marker), `BLG-FE-181` (next-action links), `BLG-FE-182` (shared formatter across three tables), `BLG-FR-04` (NULL-fee count in Monthly P&L), `BLG-FR-05` (restatement diff). **Do not invoke `plan sprint` until `run design-gate --cycle "2026-09-21__release-v9.6"` has passed** — `sprint_planning_pre_condition` blocks the seal otherwise.

## Decisions Needed (not blocking publication)

1. **Provisional-Target v9.6 items left behind (Product Owner / Head of Specs Team).** Strict §1.4c seated 4 of the 16 ready items tagged `v9.6` and left 12 (4.80 days) — follow-ups filed against v9.5's own shipped work: `BLG-SPEC-149`–`155`, `BLG-FE-178`/`179`, `BLG-QA-179`/`180`/`181`. No override was applied because none was instructed. Cheapest to decide before Sprint Planning starts: after that, a scope change means `amend cycle`, which CLAUDE.md §1 scopes as emergency-only.
2. **`BLG-BE-119` (ST-09) needs a Strategy Rules & System Intent Owner decision on live trailing-stop behaviour** before its code can proceed (RISK-03, High) — resolved in-sprint by the story; flagged here so it is scheduled early.
3. **Human-access dependencies:** `ST-16` (`BLG-OPS-164`, Actions-write token + Telegram receipt) and `ST-22` (`BLG-SPEC-148`, live-DB write access) cannot be completed autonomously.

**Publish Gate:** All conditions met — `open_escalations` empty, no blocking deferred escalations, `stage4_5_capacity_check` = pass, `stage5_5_cross_stage_integrity` = pass, `stage5_7` = not_applicable (no escalations raised this cycle), `stage1_readiness`/`stage3_5_model_integrity` = pass, `plan_structured`/`plan_executable`/`backlog_committed` = true. `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` acquired, committed, and released cleanly. `roadmap_lock` acquired, committed, and released cleanly.
