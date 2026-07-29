# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-07-29 (session — 1 new item(s) added: BLG-SEC-25, corrected to 16 sites during sign-off review); prior — 2026-07-29 (session — 1 new item(s) added: BLG-SEC-24); prior — 2026-07-28 (roadmap rebalance 2026-07-28__scheduled — DL-077: 42 new items filed from IW-20260728-01, BLG-OPS-90 gate status updated to cleared, BLG-GOV-283 filed documenting the Last-Updated header-retention convention applied to current_roadmap.md/workforce_capacity.md/initiative_register.md this session); prior — 2026-07-28 (session — user-directed priority escalation + duplicate consolidation: 11 items priority-escalated P3→P1 [Arc 5 pre-entry/compliance-gateway UX cluster: BLG-FEAT-44, BLG-FE-45, BLG-FE-54, BLG-FE-58, BLG-FE-59, BLG-FE-62, BLG-FE-63, BLG-FE-68, BLG-FE-69, BLG-FE-70, BLG-FE-71] — rationale: this cluster is the shared UX surface that already-P1 SI-02/SI-05 frontend work (BLG-FEAT-73, BLG-FE-43) depends on (BLG-FE-59 is explicitly scoped as an "extension spec for SI-02/SI-04"; BLG-FE-68/69/70/71 are the SI-05 digest/compliance-score surfacing widgets), so leaving it at P3 was blocking already-committed P1 scope; escalation is a value-judgment override, not a gate-clearance — each item's own gate criteria (where present) are unchanged and still govern sprint entry; + 9 duplicate-consolidation merges (ad hoc, not a formal `groom backlog` run — that engine's own charter forbids content/scope changes), 13 items closed as ❌ Killed — duplicate and archived to `backlog_archive.md`: BLG-QA-93 absorbed BLG-QA-99 (conftest.py AST-scan glob coverage confirmation, re-proposed without cross-reference); BLG-QA-42 absorbed BLG-QA-55 (SI-02 Playwright scaffold + its own readiness-assessment follow-up, same gate); BLG-QA-97 absorbed BLG-QA-101 (retroactive Playwright §18 anti-pattern sweep — route.fallback() ordering + networkidle usage, same mechanism); BLG-QA-81 absorbed BLG-QA-118 (visual-regression baseline snapshots — contrast-sensitive + chart-heavy components, same Playwright tooling; priority raised P3→P2 to match cluster max); BLG-GOV-144 absorbed BLG-GOV-182, BLG-GOV-199, BLG-GOV-236 (agent role charter freshness review, re-proposed 3x across separate idea-intake cycles without cross-reference); BLG-GOV-178 absorbed BLG-GOV-197, BLG-GOV-251 (quarterly AI output §13 sampling review, re-proposed 2x); BLG-GOV-95 absorbed BLG-GOV-122, BLG-GOV-187 (strategy_rules.md §11 annual parameter review, re-proposed 2x; merged gate condition now "whichever comes first" across all three original triggers — 30 ATR-stop trades, 12 months elapsed, or annual cadence — so no single absorbed item's condition was silently dropped); BLG-GOV-221 absorbed BLG-GOV-234 (cross-provider AI disclaimer consistency check — GOV-234's scope was a strict superset, adding a kill-switch drill); BLG-GOV-90 absorbed BLG-GOV-239 (Claude model deprecation monitoring/calendar); deliberately NOT merged on closer full-text review: BLG-QA-63/BLG-QA-83 (backlog's own text already documents these as an intentional gated/ungated phased pair) and BLG-QA-77/BLG-QA-92 (Playwright vs backend runtime-baseline tracking — differing gate posture, gated vs ungated, made this a real distinction rather than a duplicate; left unmerged despite being flagged as a candidate in the initial session review)); prior — 2026-07-28 (session — 1 new item(s) added: BLG-QA-127); prior — 2026-07-28 (groom backlog post-ship closure 2026-07-27__release-v7.9 — 15 items archived: BLG-FEAT-66, BLG-FEAT-67, BLG-SPEC-105, BLG-FEAT-85, BLG-FEAT-87, BLG-BE-73, BLG-BE-74, BLG-OPS-121, BLG-QA-124, BLG-QA-125, BLG-FE-130, BLG-OPS-120, BLG-FE-129, BLG-GOV-258, BLG-QA-123; ephemeral Release Slice v7.9 section removed; Gate Field Normalisation: 0 in backlog.md (2 pre-existing archive occurrences out of scope); Effort Day-Range Validation: 1 pre-existing flag (BLG-QA-115), 0 new; ID uniqueness PASS (5 known legacy duplicates unchanged, no new); 0 orphans, 0 stale blockers, 0 promotion candidates; health=PASS; report: claude/backlog/backlog_health_20260728.md); prior — 2026-07-28 (post-ship closure 2026-07-27__release-v7.9 — 15 items marked ✅ COMPLETE: BLG-FEAT-66 (ST-01), BLG-FEAT-67 (ST-02), BLG-SPEC-105 (ST-03), BLG-FEAT-85 (ST-04), BLG-FEAT-87 (ST-05), BLG-BE-73 (ST-06), BLG-BE-74 (ST-07), BLG-OPS-121 (ST-08), BLG-QA-124 (ST-09), BLG-QA-125 (ST-10), BLG-FE-130 (ST-11), BLG-OPS-120 (ST-12), BLG-FE-129 (ST-13), BLG-GOV-258 (ST-14), BLG-QA-123 (ST-15); no stale parked items (zero parked-status items in `backlog.md`, matches authoritative backlog slice); no Phase 4 additions required — BLG-GOV-264 already present pre-closure per `verification_report.md §5(a)`, 0 test scenario gaps or returned items per §5/§6); prior — 2026-07-27 (session — direct governance fix, user-directed: BLG-GOV-190 resolved and archived to `backlog_archive.md` — `design_gate_prompt.md` v1.4→v1.5, root state pointer sync gap closed per option (a); see `prompt_change_log.md` and `changelogs/design_gate_changelog.md` for full detail); prior — 2026-07-27 (release planning 2026-07-27__release-v7.9 — Release Slice v7.9 added, 15 items: BLG-FEAT-66, BLG-FEAT-67 (2 ready P1 anchors) + BLG-SPEC-105, BLG-FEAT-85, BLG-FEAT-87, BLG-BE-73, BLG-BE-74, BLG-OPS-121, BLG-QA-124, BLG-QA-125, BLG-FE-130 (9 P2 capacity-fill items) + BLG-OPS-120, BLG-FE-129, BLG-GOV-258, BLG-QA-123 (4 P3 capacity-fill items) — `Provisional-Target` updated TBD/Unscheduled → v7.9 on all 15, per explicit user instruction to use the full confirmed ~24-28 day capacity band (~26.5 days midpoint, ~95-110% utilisation); `BLG-FEAT-56` excluded (gate date sub-condition elapsed but usage-validation sub-condition unconfirmable this session); `BLG-FEAT-73`/`BLG-FEAT-74` excluded (SI-02 NOT MET / §13 pre-clearance not run, consistent with the already-executed PO perennial-return disposition); EPIC-01/02/05 (3 items) conditional pending Design Gate PASS (observable UI ACs); see `decisions--2026-07-27__release-v7.9.md`); prior — 2026-07-27 (roadmap rebalance 2026-07-27__scheduled — 21 new items added via idea intake IW-20260727-01 disposition: BLG-FE-129/130/131, BLG-GOV-258/259/260/261/262, BLG-SPEC-105, BLG-FEAT-85/86/87, BLG-BE-73/74, BLG-OPS-120/121/122, BLG-QA-123/124/125/126 (21 standalone; 23 Rejected — not strong, the large majority duplicates of existing open backlog items surfaced by the STEP 4.0/§2.0.5 overlap check, 0 Advance, 0 Parked); STEP 8.1 fired (condition 1a — Now horizon fully empty) — Option (b): defer, PO rationale: no newly-cleared gate or fast-track anchor this cycle, next `plan release` is the natural scoping moment; STEP 8.0 fast-track 0 qualifying P0/P1 items; Product Value Ratio 0.42 (U=15/G=1/D=18/P=2 of 36, v7.4–v7.8 window) — Advisory; DL-076; STEP -1.5: 1 deferred patch from `2026-07-24__scheduled` resolved (roadmap_prompt.md v9.5→v9.6 STEP 2.3 SI-02 credential-fallback guidance); STEP -1.7 cross-routine scan found and filed 1 previously-missed outstanding action (BLG-GOV-263, cross-EPIC execution_state.json structural fix, first surfaced `2026-07-17__release-v7.5` closure); Backlog Accessibility Warning not triggered (A≈40.8% of 341 items pre-addition, structural heuristic)); prior — 2026-07-27 (session — priority escalation, user-directed: 5 items raised to P1 following a session top-5 user-facing feature review (BLG-FEAT-74 P2→P1, BLG-FE-43 P2→P1, BLG-FEAT-66 P3→P1, BLG-FEAT-67 P3→P1, BLG-FEAT-56 P3→P1; BLG-FEAT-73 already P1, unchanged); escalation is a value-judgment override, not a gate-clearance — each item's own gate criteria (where present) are unchanged and still govern sprint entry; not a formal `groom backlog` priority-revalidation pass); prior — 2026-07-27 (session — duplicate consolidation, ad hoc user-directed backlog cleanup (not a formal `groom backlog` run): 5 near-duplicate clusters merged into their most-complete survivor item, 13 duplicate items closed as ❌ Killed — duplicate and archived to `backlog_archive.md`; BLG-OPS-25 absorbed BLG-OPS-100/102/107/119 (staging smoke test on deploy/merge/cadence — gate cleared, BLG-OPS-27 shipped v4.0); BLG-BE-47 absorbed BLG-BE-53/64/72 (canonical list-endpoint pagination pattern, priority raised P3→P2 to match cluster max); BLG-FEAT-30 absorbed BLG-FEAT-27/28 (screener-to-trade attribution pipeline + its retrospective/hit-rate reporting views); BLG-QA-75 absorbed BLG-QA-80/87 (Playwright flake tracking — quarantine-list scope ungated, CI-pipeline-integration scope kept gated per original BLG-QA-75 rationale); BLG-SEC-15 absorbed BLG-OPS-93/BLG-SEC-19 (recurring dependency CVE re-scan cadence); no other backlog content changed); prior — 2026-07-27 (groom backlog post-ship closure 2026-07-24__release-v7.8 — 12 items archived: BLG-FE-128, BLG-FEAT-84, BLG-FE-127, BLG-FE-125, BLG-FEAT-81, BLG-FEAT-82, BLG-SEC-20, BLG-SEC-21, BLG-BE-71, BLG-QA-117, BLG-QA-119, BLG-OPS-117; ephemeral Release Slice v7.8 section removed; Gate Field Normalisation: 0 in backlog.md (2 pre-existing archive occurrences out of scope); Effort Day-Range Validation: 1 pre-existing flag (BLG-QA-115), 0 new; ID uniqueness PASS (5 known legacy duplicates unchanged, no new); 0 orphans, 0 stale blockers, 0 promotion candidates; health=PASS; report: claude/backlog/backlog_health_20260727.md); prior — 2026-07-27 (post-ship closure 2026-07-24__release-v7.8 — 12 items marked ✅ COMPLETE: BLG-FE-128 (ST-01), BLG-FEAT-84 (ST-02), BLG-FE-127 (ST-03), BLG-FE-125 (ST-04), BLG-FEAT-81 (ST-05), BLG-FEAT-82 (ST-06), BLG-SEC-20 (ST-07), BLG-SEC-21 (ST-08), BLG-BE-71 (ST-09), BLG-QA-117 (ST-10), BLG-QA-119 (ST-11), BLG-OPS-117 (ST-12); no stale parked items (zero parked-status items in `backlog.md`, matches authoritative backlog slice); no Phase 4 additions required — BLG-SPEC-102/103/104 already present pre-closure per `verification_report.md §2`, 0 test scenario gaps or returned items per §5/§6); prior — 2026-07-27 (delivery verification `2026-07-24__release-v7.8` — 3 new item(s) added: BLG-SPEC-102, BLG-SPEC-103, BLG-SPEC-104 — doc-completeness gaps surfaced during EPIC-11/ST-11 pilot contract test authoring, per `verification_report.md §6`); prior — 2026-07-26 (session — 2 new item(s) added: BLG-GOV-256, BLG-GOV-257); prior history retained — see prior entries in version control (last full entry retained here: 2026-07-26 session note; chain truncated 2026-07-28 per BLG-GOV-283, header-history retention convention).
**Last rebalance:** 2026-07-12 (cycle 2026-07-12__scheduled — DL-064; 36 new backlog items added (BLG-GOV-203–217, BLG-QA-94–99/101–103, BLG-BE-57/58, BLG-FE-103–105, BLG-SEC-17, BLG-SPEC-78–82, BLG-OPS-106/107) via idea intake IW-20260712-01 (44 submissions, 22 agents) disposition: 36 Promoted-Backlog, 7 Rejected (all resolved by direct action), 1 Promoted-Added (process patch), 2 Parked; 0 active initiatives, CPS=N/A; STEP 2.4 Product Value Ratio 0.21 (U=8 G=9 D=21 P=0, window v6.5–v6.9) — 🔴 3rd consecutive Product Value Alert, improved from prior 0.18 but still below 0.30 floor; mandatory pull-forward named BLG-FE-102 as anchor candidate for next `plan release`, BLG-FE-97 secondary; SI-02 gate live re-checked via production API — NOT MET (0/11 linked trade plans; behavioural-drift endpoint self-reports insufficient_data); STEP 7.1 Skill-Silo rolling-3-cycle avg 76.9% (v6.7/v6.8/v6.9) — Alert persists but improved from 78.2%; STEP 8.1 empty horizon gate: Option (b) — defer, scoping deferred to next `plan release`; Backlog Accessibility Warning RE-TRIGGERED (A=19.9%, down from 38.8%); prior — 2026-07-10 (cycle 2026-07-10__scheduled — DL-063; 39 new backlog items added (BLG-GOV-191–202, BLG-QA-87–93, BLG-OPS-101–105, BLG-SEC-14–16, BLG-BE-53–56, BLG-SPEC-74–77, BLG-FE-99–101, BLG-FEAT-72) via idea intake IW-20260710-01 (44 submissions, 22 agents) disposition: 39 Promoted-Backlog, 3 Parked-cycle-1, 2 Rejected; 0 active initiatives, CPS=N/A; STEP 2.4 Product Value Ratio 0.18 (U=9 G=16 D=24 P=0, window v6.4–v6.8) — 🔴 2nd consecutive Product Value Alert, worse than prior 0.26; mandatory pull-forward named BLG-FEAT-64 as anchor candidate for `plan release v6.9`; STEP 7.1 Skill-Silo rolling-3-cycle avg 78.2% (v6.6/v6.7/v6.8) — Alert persists, single-reading worsening after 2 consecutive improvements; STEP 8.1 empty horizon gate: Option (b) — defer, v6.9 scoping deferred to `plan release v6.9`; prior — 2026-07-02 (cycle 2026-07-02__scheduled — DL-059; 24 new backlog items added (BLG-FEAT-55–60, BLG-FE-81–84, BLG-BE-41/42, BLG-GOV-154/156, BLG-QA-69/70/71, BLG-SEC-09, BLG-SPEC-62/63/65/66, BLG-OPS-84/85) via idea intake IW-20260702-01 (44 submissions) + 19 carried ideas at 3-cycle hard cap; STEP 8.0: 0 fast-track items this cycle; STEP 3.1 Actionable Backlog Assessment: A=35/28%, T=7/6%, D=27/22%, L=55/44% of 124 baseline items — Backlog Accessibility Warning triggered (A% below 30% floor); PVR=0.344 Advisory; Skill-Silo rolling-3-cycle avg=64.8% Alert, worse than prior 53.2% (pull-forward candidate BLG-FE-46)))

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

> 📋 Placement Rule
> New items must be appended to the correct existing type section (§1–§8). Do not create new numbered session sections. The backlog is organised by type, not by session date.
> **Ephemeral sections** (Release Slice tables, Test Scenario Gap sections, and "Returned to Backlog" sections appended by governance engines) are temporary. They must be removed during the next `groom backlog` run after the cycle closes. Any still-open items within them must be promoted to the appropriate §1–§8 type section before the ephemeral section is removed.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

### BLG-GOV-240 — No governed write path exists to formally version-label a non-empty, unversioned Now-horizon carry-forward
**Priority:** P2 (Medium) | **Type:** Governance Process | **Owner:** Head of Specs Team; Product Owner | **Source:** DL-068, current_roadmap.md v7.3 formalization session — 2026-07-16 | **Effort:** S (~0.5-1 day) | **Provisional-Target:** TBD

**Problem**
`roadmap_prompt.md` STEP 8.1 (Empty Now Horizon Gate) is the only mechanism that lets the roadmap engine formally write a "## vX.Y" Now-horizon section name via its Option (a)/(b) PO decision — but it only fires when condition 1 (Now horizon contains no committed items) is true. When a prior cycle's post-ship closure leaves unblocked items carried forward in the Now horizon *without* a version label (as happened at `2026-07-15__release-v7.2` post-ship closure, which explicitly re-added `BLG-FE-109/110/111` as "an un-versioned Now-horizon carry-forward entry"), STEP 8.1 never fires again for that horizon, because it is no longer empty. Separately, `release_planning_prompt.md`'s write scope (§7) only permits annotating an *existing* release section on the roadmap — it cannot create a new one. Confirmed live at `2026-07-16__scheduled` (DL-067: "STEP 8.1 empty horizon gate: not triggered (Now horizon non-empty — 3 items already carried)") despite the PO having already named a formal v7.3 anchor scope that same cycle, deferred as advisory-only to "the next `plan release` invocation" — which then had no compliant path to write it either. Resolved this session via an out-of-band write under Head of Specs Team authority (DL-068), by analogy to the `shared_standards.md` §17 pattern (standing authority for files/scenarios no engine's Write Scope covers).

**Scope**
- Extend `shared_standards.md` §17 with a narrow standing-authority provision for `current_roadmap.md` §1/§3 version-labeling in this specific scenario, OR
- Amend `roadmap_prompt.md` STEP 8.1 condition 1 to also fire when the Now horizon is non-empty but contains no version-labeled section (i.e. "no committed items" OR "committed items present but none under a versioned heading")

**Acceptance Criteria**
- One of the two remediation paths is selected and implemented via the standard governance file edit checklist (version bump, `OPERATIONAL_GUIDE.md` §14 update, `prompt_change_log.md` entry)
- A non-empty, unversioned Now-horizon carry-forward no longer requires an out-of-band write to receive a formal version label

---

### BLG-GOV-241 — Automated PII scan gate for new backend endpoints
**Priority:** P2 (Medium) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260717-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** New backend endpoints are reviewed for auth/security (per `BLG-SEC-*` patterns) but there is no CI-level check that a new response schema doesn't inadvertently expose PII-shaped fields (e.g. raw email, unredacted account identifiers).
**Scope:** Add a lightweight CI check that scans new/changed response schemas in `docs/reference/openapi.yaml` for common PII field-name patterns and flags them for manual review.
**Acceptance Criteria:** CI check added and confirmed to fire on a deliberately-introduced PII-shaped field in a test PR.

---

### BLG-GOV-242 — Quarterly model/prompt-drift compliance attestation log
**Priority:** P3 (Low) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260717-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-GOV-239` tracks the model deprecation calendar, but there is no recurring attestation record confirming the pinned model/prompt behaviour hasn't silently drifted between quarters.
**Scope:** Add a lightweight quarterly attestation log (pinned model version, last prompt-template review date, any observed drift) as a companion to `BLG-GOV-239`'s deprecation calendar.
**Acceptance Criteria:** Attestation log document created; first entry filed.

---

### BLG-GOV-243 — OpenAPI contract linter in CI for heading-level drift
**Priority:** P2 (Medium) | **Type:** Governance / Process Tooling | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260717-01 | **Effort:** M | **Provisional-Target:** v7.10
**Problem:** `CLAUDE.md §2` requires API contract endpoint headings to be exactly `##` (not `###`+) or the OpenAPI Drift Detection gate silently misses them — this is currently caught only by the gate failing after the fact, not by a lint step naming the specific violation clearly.
**Scope:** Extend the existing OpenAPI Drift Detection CI job to emit a specific, actionable error message when a `docs/specs/api_contracts/` heading is found at the wrong level, rather than a generic "endpoint missing from contract" failure.
**Acceptance Criteria:** CI job produces a distinct, correctly-worded error for the heading-level case versus the missing-entry case; confirmed via a test PR with a deliberately mis-leveled heading.

---

### BLG-GOV-244 — Deprecation header convention for retiring API endpoints
**Priority:** P3 (Low) | **Type:** Governance / API Process | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260717-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The system has never formally retired a shipped API endpoint, so there is no documented convention for how a deprecation should be communicated in `openapi.yaml`/contract docs before removal.
**Scope:** Document a lightweight deprecation-header convention (e.g. `**Deprecated:** vX.Y, removal target vX.Z`) for future use in `docs/specs/api_contracts/`.
**Acceptance Criteria:** Convention documented; referenced from `shared_standards.md` or an equivalent canonical location.

---

### BLG-GOV-245 — Formal expiry review for §13-adjacent initiatives open more than 2 cycles
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** Challenger; Strategy Rules & System Intent Owner | **Source:** IDEA-challenger-20260717-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `roadmap_prompt.md` STEP 2.1 requires Score-4/5 initiatives to get heightened Challenger scrutiny at debate time, but there is no recurring check that a Score-4/5 item still open after 2+ cycles gets re-reviewed rather than just re-carried.
**Scope:** Add an advisory check to STEP 2 that flags any Score-4/5 initiative open more than 2 consecutive cycles for explicit Challenger re-review, rather than silent carry-forward.
**Acceptance Criteria:** Check specified; would have fired correctly against at least one historical example if run retroactively (or confirmed no qualifying example exists).

---

### BLG-GOV-246 — Skill-Silo mitigation: rotate execution-heavy story assignment pattern
**Priority:** P2 (Medium) | **Type:** Governance / Workforce | **Owner:** Director of HR; FinOps & Resource Architect | **Source:** IDEA-director-of-hr-20260717-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** The Skill-Silo Alert (`roadmap_prompt.md §7.1`) has worsened for 2 consecutive readings (66.7% → ~81%, v7.0–v7.3 windows) despite prior single-item U-pull-forwards; there is no structural mechanism encouraging execution-heavy (build-and-ship) story selection independent of a single-cycle PO override.
**Scope:** Define a lightweight rotation guideline for release planning — e.g. a soft target that at least 1 in 3 release cycles leads with execution-heavy scope by default, reviewed at each `plan release` invocation.
**Acceptance Criteria:** Guideline documented in `release_planning_prompt.md` or a referenced companion doc; explicitly tied to the STEP 7.1 alert as its trigger condition.

---

### BLG-GOV-247 — Formalise condensed-tier trigger thresholds beyond the "no new FTE required" test
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260717-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `roadmap_prompt.md` STEP 0.C's Lightweight-tier workforce economics condensing rule ("Condensed if no new FTE required") has never actually fired in this backlog-driven, solo-developer context (0 active initiatives, no FTE concept in practice) — the criterion may not be a meaningful discriminator here.
**Scope:** Review whether STEP 0.C's condensed-tier language should be reworded for a solo-developer/story-count context, analogous to how `roadmap_prompt.md §7.1` already substitutes story-count for FTE-hours.
**Acceptance Criteria:** Review completed; either a specific prompt change proposed, or an explicit decision recorded that the existing language is fine as-is.

---

### BLG-GOV-256 — design_gate_prompt.md does not sync .claude_current_state.json root pointer on gate pass
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** `plan sprint 2026-07-24__release-v7.8` session — 2026-07-26
**Effort:** S (~0.5-1 day)
**Provisional-Target:** v7.10

**Problem**
`design_gate_prompt.md` v1.4's write scope (§5) only permits writes to `claude/cycles/<cycle_id>/design_gate.md` and the cycle-level `state.json` — it never touches `.claude_current_state.json`. When the design gate passes, the cycle-level `state.json` correctly records `design_gate_status = Passed`, but the root pointer file's `status` field stays at `Release_Planning_Complete` and its `design_gate_status`/`design_gate_record`/`design_gate_completed_utc` fields stay stale (`not_started`/empty). This causes `sprint_planning_prompt.md`'s STEP -1.3 bypass audit (IMP-04) to fire on every cycle with a required design gate, mechanically treating a genuinely-passed gate as "skipped entirely" since it only reads the literal `.claude_current_state.json` status string. Discovered and worked around (treated as a documented process deviation rather than an actual bypass, per Product Owner decision) during `plan sprint` for `2026-07-24__release-v7.8` — see `claude/cycles/2026-07-24__release-v7.8/sprint_planning_notes.md` "Design Gate / Lifecycle Note".

**Scope**
- Add a step to `design_gate_prompt.md` STEP 5 that also writes `status = Design_Gate_Passed` (and `design_gate_status`/`design_gate_record`/`design_gate_completed_utc`) to `.claude_current_state.json` atomically with the existing cycle-level `state.json` write
- Update `sprint_planning_prompt.md` STEP -1.3's bypass-audit condition to check the cycle-level `state.json`'s `design_gate_status` directly as a first-class pass condition, not only the root status enum

**Acceptance Criteria**
- `run design-gate` updates `.claude_current_state.json` to `Design_Gate_Passed` (or equivalent) in the same run as a Passed gate, with no separate manual sync step required
- `plan sprint`'s bypass audit no longer fires for a cycle where the cycle-level `state.json` already shows `design_gate_status = Passed`
- Governance file edit checklist (CLAUDE.md §6) applied in full for both prompt edits

---

### BLG-GOV-257 — prompt_change_log.md mixed prepend/append ordering breaks grep|head -1 gap detection
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** `plan sprint 2026-07-24__release-v7.8` session — 2026-07-26
**Effort:** M (~1-2 days)
**Provisional-Target:** TBD

**Problem**
`prompt_change_log.md`'s header states "Append-only," but a contiguous block (~lines 53-213, dated 2026-06-16 through 2026-07-02) was written prepended newest-first per the v3.9→v3.10 `sprint_planning_prompt.md` fix (`c86b02c5`). Below that block sits an older historical backfill in ascending chronological order that runs to the end of the file, and that backfill's last rows (e.g. a `sprint_planning_prompt.md` v3.12→v3.13 row dated 2026-07-14, at line 572) are chronologically newer than every row in the "prepended" block above them. `sprint_planning_prompt.md` STEP -1.7's hygiene check (`grep "<filename>" prompt_change_log.md | head -1`) therefore returns a stale row as "the latest" for any file whose true latest entry landed in the old append-ordered tail rather than the newer prepend-ordered head. Discovered during `plan sprint` for `2026-07-24__release-v7.8` as a false-positive "prompt change log gap" advisory for `sprint_planning_prompt.md` (v3.13 current; check reported last-logged v3.12 when v3.13 was in fact already logged at line 572).

**Scope**
- Either (a) do a one-time full re-sort of `prompt_change_log.md` into strict newest-first order and keep it that way going forward, or (b) change the STEP -1.7 check in `sprint_planning_prompt.md` (and any equivalent check elsewhere) to scan the full file for the row with the latest Date column per filename rather than relying on file position
- Option (b) is more robust against any future ordering drift and does not require rewriting a large historical governance record

**Acceptance Criteria**
- The chosen fix is implemented and the false-positive case above no longer reproduces (re-running the STEP -1.7 check against `sprint_planning_prompt.md` correctly finds the line 572 entry as current)
- If option (a) is chosen: the full file is verified newest-first top-to-bottom after the resort
- If option (b) is chosen: the check's new logic is documented in `shared_standards.md` alongside the existing STEP -1.7 description

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-26 — ATR position-sizing retrospective analysis
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped and live for ≥ 30 days; sufficient attributed closed trades to support retrospective.

**Problem**
There is no retrospective view of whether ATR-based position sizing (risked R per trade) was consistent over time, or whether deviation from the ATR sizing formula correlated with outcome. Understanding sizing discipline and its P&L impact requires a dedicated analytics view built on historical trade data.

**Scope**
- Retrospective dashboard: actual position size vs ATR-recommended size per trade
- Correlation view: sizing deviation vs R-multiple outcome
- Summary metric: sizing discipline score over rolling window

**Acceptance Criteria**
- ATR-sizing deviation visible per trade and in aggregate
- Correlation between sizing deviation and R-multiple summarised
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-29 — Regime distribution metric over screener history
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days.

**Problem**
No view exists showing how market regime distribution (bull/bear/neutral/volatile) has evolved across screener runs over time. Understanding regime frequency and drift helps contextualise screener output quality and strategy performance in different market conditions.

**Scope**
- Aggregate view: regime distribution over screener history (rolling 30d/60d/all)
- Displayable as percentage breakdown or time-series chart

**Acceptance Criteria**
- Regime distribution over screener history computable and displayable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-30 — Screener-to-trade attribution pipeline & retrospective analytics (consolidated)
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-05 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032); consolidates BLG-FEAT-27 (retrospective quality/win-rate analysis) and BLG-FEAT-28 (hit-rate metric) — both are reporting views over the same attribution linkage this item builds; filed together in the same 2026-04-21 idea batch but scoped as if independently buildable, when in practice all three need the same underlying instrumentation — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days AND ≥ 60 closed trades with screener attribution (the more demanding of the original gate conditions — the merged retrospective/quality-correlation scope needs both).

**Problem**
The full pipeline from screener hit → watchlist add → research → trade plan → execution → close is not yet instrumented end-to-end. Attribution gaps prevent retrospective analysis of conversion rates at each stage, make it impossible to evaluate whether the screener generates genuinely high-quality candidates vs high-volume noise, and leave no aggregate hit-rate metric available — all needs originally filed as three separate items requiring the same underlying linkage.

**Scope**
- Full attribution model: screener_run_id linkage through to trade close
- Conversion funnel: screener → watchlist → plan → closed
- Aggregate hit-rate metric: screener_candidates_total, advanced_to_watchlist, advanced_to_trade_plan, advanced_to_closed_trade — displayable in governance/operations reporting view
- Retrospective metric: screener hit rate and win rate of attributed trades vs baseline, filterable by screener run date range
- Exportable for offline analysis

**Acceptance Criteria**
- Full attribution pipeline implemented; conversion funnel metrics computable
- Hit-rate metric computed and displayable
- Screener hit rate and attributed-trade win rate reportable, filterable by date range
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-31 — Research-to-trade conversion rate metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-06 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-02 (Research View) live ≥ 30 days AND ≥ 30 research sessions with attribution.

**Problem**
No metric tracks how often a research session (opening the research view for a ticker) results in a trade plan creation. This conversion rate is an indicator of research quality and operator decision confidence. Requires 30 days of research session history with attribution.

**Scope**
- Metric: research_sessions_total, sessions_leading_to_plan, sessions_leading_to_closed_trade
- Attribution requires `session_id` or equivalent linkage from research view to trade plan

**Acceptance Criteria**
- Research-to-trade conversion rate computable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-32 — Trade plan completion rate tracking
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-07 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped.

**Problem**
No metric tracks what proportion of created trade plans are completed (i.e., result in a closed trade) vs abandoned. The completion rate is a key indicator of plan quality, operator follow-through, and whether PT-04 quality scores correlate with plan execution. Requires PT-04 to create the quality score baseline for correlation.

**Scope**
- Metric: plans_created, plans_completed (closed trade), plans_abandoned, completion_rate
- Optional: completion rate segmented by setup quality score tier

**Acceptance Criteria**
- Trade plan completion rate computable and displayable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-33 — Trade plan approval workflow
**Priority:** P3 (Low)
**Type:** Product Feature / Workflow
**Owner:** Product Owner; Head of UX & Design
**Source:** IDEA-trade-plan-20260508-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-05 (Trade Plan feature set) live ≥ 3 months with ≥ 20 plans created; operator confirms approval workflow adds value.

**Problem**
Trade plans are currently created and immediately actionable without a formal review or approval step. As plan complexity grows (multi-day setup, multi-leg risk), an explicit approval checkpoint may improve discipline — but the value of an approval workflow vs friction cost is not yet established. Gate ensures sufficient usage history before committing implementation effort.

**Scope**
- Approval state: Draft → Pending Approval → Approved / Rejected
- Approval action: operator-controlled (self-approval supported for solo use)
- Approved plans visible separately from drafts

**Acceptance Criteria**
- Approval workflow implemented and functional
- Plan state transitions correct and persisted
- Gate condition and usage volume verified by Product Owner before sprint planning

---

### BLG-FEAT-34 — Trade plan P&L attribution
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner; Financial Reporting & Records Owner
**Source:** IDEA-trade-plan-20260508-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** `plan_id` linkage live on closed trades (PT-05 shipped and plans actively used).

**Problem**
Closed trade P&L cannot currently be attributed back to the trade plan that governed the entry. Without `plan_id` on position records, it is impossible to compare planned R-risk vs realised R-multiple or evaluate whether adhering to a plan improved outcomes vs discretionary deviation.

**Scope**
- Link `plan_id` from trade plan to position/trade close record
- Attribution report: planned_risk_R vs realised_R per attributed trade
- Aggregate: plan-adhered trades vs plan-deviated trades outcome comparison

**Acceptance Criteria**
- `plan_id` linkage implemented on closed trades
- Attribution report computable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-35 — Entry zone discipline reporting
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-trade-plan-20260508-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 20 closed trades with linked trade plans AND `entry_delta_pct` field captured on closed trades.

**Problem**
No metric tracks whether entries were executed within the planned entry zone. `entry_delta_pct` (actual entry vs planned entry midpoint) is a candidate field but is not yet captured at trade close. Without this data, it is impossible to assess entry zone discipline or its correlation with trade outcome.

**Scope**
- Capture `entry_delta_pct` on trade close: actual_entry_price vs planned_entry_zone midpoint
- Discipline metric: % of trades entering within planned zone
- Correlation: entry discipline vs R-multiple outcome

**Acceptance Criteria**
- `entry_delta_pct` captured on trade close where plan linkage exists
- Entry discipline metric computable and displayable
- Gate condition verified by Product Owner before sprint planning

---

---

### BLG-FEAT-44 — Arc 5 compliance score utility advisory at low trade volume
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Product Feature / UX Advisory
**Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design
**Source:** IDEA-metrics-analytics-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc5ComplianceSection live 3+ months post-v4.1 ship (~Aug 2026). Minimum usage period needed to assess whether low-volume score values are misinterpreted in practice.

**Problem**
The Arc 5 composite compliance score (shipped v4.1) is computed from fewer than 20 closed trades. At low sample volumes, the score may represent statistical noise rather than actionable signal. Without a "minimum data" advisory in the UI, users may over-interpret early values.

**Scope**
- Assess whether compliance scores at <20 trades are statistically meaningful
- If noise at low volume: add a "Minimum trade history required (< 20 trades)" advisory near the score display
- Gate condition verification by Metrics Definitions & Analytics Owner before sprint planning

**Acceptance Criteria**
- Assessment document produced (advisory or advisory-not-needed conclusion)
- If advisory warranted: UI advisory added to Arc5ComplianceSection for sub-20-trade states
- Gate condition verified before sprint planning

---

### BLG-FEAT-45 — Monthly P&L report format review — 3-month usage retrospective
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥ 2026-08-05 (3+ months since Monthly P&L shipped 2026-05-05)

**Problem**
Monthly P&L shipped 2026-05-05 with a fixed column/section layout. After 3 months of real usage, the format may benefit from minor adjustments (column order, section grouping, display precision). A lightweight retrospective assessment at 3 months is appropriate before any format changes are considered.

**Scope**
- Review current Monthly P&L format against 3+ months of usage experience
- Identify any column, section, or display precision improvements
- Produce a brief recommendations document; if no changes warranted, record "no change" decision
- Product Owner sign-off

**Acceptance Criteria**
- Format review conducted with 3+ months of data available
- Recommendations document produced (or "no change" decision recorded)
- Any format changes flow into the next appropriate sprint as separate stories
- Gate condition verified: ≥ 2026-08-05

---

---

### BLG-FEAT-55 — AI chat conversation history persistence across sessions
**Priority:** P3 (Low)
**Type:** Product Feature / AI
**Owner:** Product Owner; Data Model & Domain Schema Owner
**Source:** IDEA-product-owner-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥30 days of AI chat usage (v6.2 shipped 2026-06-25; clears ~2026-07-25) AND a §13 review opened and passed for persistence design (chat is currently stateless per SRB-v1.7).

**Problem**
POST /ai/chat (shipped v6.2) is stateless — no conversation history persists across sessions. Users who want to continue a prior chat thread cannot. Persisting history is a genuine schema and §13 boundary question (stored AI conversation content) that should not be designed ahead of both an established usage pattern and a formal boundary review.

**Scope**
- §13 review: does persisting chat history change SRB-v1.7's stateless-advisory classification?
- Schema design: chat session/message data model (companion to BLG-SPEC-65/66)
- Frontend: session list, resume-conversation UX

**Acceptance Criteria**
- §13 review passed before design begins
- Chat session schema designed and reviewed by Data Model & Domain Schema Owner
- Gate condition (30 days usage) verified by Product Owner before sprint planning

---

### BLG-FEAT-56 — AI-assisted setup thesis digest at order placement
**Priority:** P1 (High) — escalated from P3, 2026-07-27, session product review (see note below)
> ⚠️ **Priority escalation (2026-07-27):** Raised P3→P1 during a session backlog review — flagged as high-value user-facing decision support (surfaces existing AI thesis infra at the order-placement moment). Escalation reflects value judgment only; the gate criteria below are unchanged and still govern when this may enter sprint planning.
**Type:** Product Feature / AI
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 AND existing AI touchpoints (daily briefing, chat) show established, validated usage patterns.

**Problem**
The AI thesis generation button (v4.0) populates `setup_thesis` on demand. Adding a further AI touchpoint — an automatic digest surfaced at order placement — before existing AI features are validated risks layering unvalidated AI surface area on top of unvalidated AI surface area.

**Scope**
- Digest content: setup thesis + key risk factors summarised at the order-placement step
- Reuses existing Claude thesis generation infrastructure (v4.0)
- Gated behind confirmed adoption of the existing AI touchpoints

**Acceptance Criteria**
- Digest renders at order placement using existing thesis generation service
- Gate condition (adoption validated) verified by Product Owner before sprint planning

---

### BLG-FEAT-57 — Strategy parameter sensitivity analysis framework
**Priority:** P3 (Low)
**Type:** Product Feature / Strategy Analytics
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥20 closed trades (currently ~15–17) AND Arc 5/6 tooling prerequisite in place.

**Problem**
There is no systematic pre-process to evaluate the effect of a §11 strategy parameter change (e.g. ATR multiplier) against historical trade data before committing to a version bump. Building this ahead of sufficient trade density or the Arc 5/6 analytical foundation would produce statistically unreliable output.

**Scope**
- Sensitivity analysis: apply candidate parameter values against historical trade set, compare outcome deltas
- Feeds into SI-04 (Strategy Version Comparison) as a pre-change evaluation step

**Acceptance Criteria**
- Framework produces before/after outcome comparison for a candidate parameter change
- Gate condition (≥20 closed trades) verified by Strategy Rules & System Intent Owner before sprint planning

---

### BLG-FEAT-58 — Trade annotation model
**Priority:** P3 (Low)
**Type:** Product Feature / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Arc 4 PO-02 (Journal Pattern Recognition) data model established (~2026-10-20, 6+ months AI-summarised journal data).

**Problem**
No schema exists for user-authored free-text annotations on individual trades, distinct from the AI-summarised journal entry. Designing this ahead of PO-02's data model risks a schema that conflicts with or duplicates the eventual journal-pattern data structure.

**Scope**
- `trade_annotations` schema: trade_id, annotation_text, created_at, tags (optional, see BLG-FEAT-52)
- Co-designed with PO-02 data model once that gate clears

**Acceptance Criteria**
- Schema co-designed with PO-02 data model, not ahead of it
- Gate condition (PO-02 data model established) verified before sprint planning

---

### BLG-FEAT-59 — AI-assisted monthly P&L narrative
**Priority:** P3 (Low)
**Type:** Product Feature / AI
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 (same constraint as BLG-FEAT-55/56 — too early to layer additional AI-generated content onto financial reporting).

**Problem**
Monthly P&L (shipped v2.x) is a fixed-format report. An optional AI-generated narrative commentary could add interpretive value, but adding it before existing AI features (daily briefing, chat) are validated risks compounding unvalidated AI surface area onto a financial-reporting document specifically.

**Scope**
- Optional AI narrative section appended to Monthly P&L using existing Claude infrastructure
- Advisory-only framing consistent with §13 SRB-v1.7

**Acceptance Criteria**
- Narrative section renders as optional/dismissible
- Gate condition (AI adoption window) verified by Financial Reporting & Records Owner before sprint planning

---

### BLG-FEAT-60 — AI chat engagement metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 — usage patterns remain unestablished at current usage duration; metric definition would be premature.

**Problem**
No metric tracks AI chat engagement (sessions per week, questions per session, response acceptance rate). Defining the metric before usage patterns stabilise risks needing early revision.

**Scope**
- Define engagement metric set: sessions/week, questions/session, response-acceptance rate
- Document in `metrics_definitions.md`

**Acceptance Criteria**
- Metric set defined and documented
- Gate condition (AI adoption window) verified before sprint planning

---

---

### BLG-FEAT-73 — SI-02 Behavioural Drift Detection — frontend build
**Priority:** P1 (High)
**Type:** Product Feature / Frontend, gate-conditional
**Owner:** Head of Engineering; Head of UX & Design
**Source:** Feature-gap review (current_roadmap.md Arc 5 status table cross-referenced with BLG-GOV-107, BLG-BE-46, BLG-BE-52) — 2026-07-10
**Effort:** M (~2 days)
**Provisional-Target:** v7.7 — named as v7.7 anchor scope 2026-07-21 (DL-074); `[gate status unverified/unmet]` — BLG-GOV-107 gate conditions last confirmed NOT MET 2026-07-17, not re-verified this session; may not enter sprint planning until independently reconfirmed met
**Depends on:** BLG-FE-56, BLG-FE-57, BLG-FE-58, BLG-FE-59 (UI extension specs); BLG-BE-27, BLG-BE-29 (perf baseline, index review) — all currently gate-conditional on this item entering sprint planning

**Problem**
The behavioural drift detection backend service shipped in v4.6 and computes drift scores from `trade_history`/`trade_plans` window functions, but no frontend was ever built to surface it — there is no UI showing drift scores, trend, or explanation anywhere in the app. This is Arc 5's flagship "tell me when I'm deviating from my own rules" feature, and it is currently invisible to the user despite the backend existing and running.

**Scope**
- Drift score display card(s) in `Arc5ComplianceSection`, per the existing extension-point spec (BLG-FE-59)
- Historical trend view for drift score over time
- Plain-language explanatory copy for what a drift score means and what action it implies

**Acceptance Criteria**
- User can view current drift score(s) in the Arc 5 compliance UI
- User can see a historical trend of drift score over time
- Each score is accompanied by plain-language explanation of contributing factors
- Feature does not enter sprint planning until all 3 BLG-GOV-107 gate conditions are independently reconfirmed met: (1) ≥20 closed trades with **linked** trade_plans (`trade_plans.position_id` populated) — note this gate can only clear via new trade_plans created going forward, since BLG-BE-52 declined to backfill the 11 pre-existing unlinked rows; (2) `GET /analytics/behavioural-drift` p99 < 2s stable over a 7-day window; (3) drift scores show non-trivial variance across trades (not all 0 or 1.0)

---

### BLG-FEAT-74 — PO-05 Lightweight Replay Mode
**Priority:** P1 (High) — escalated from P2, 2026-07-27, session product review (see note below)
> ⚠️ **Priority escalation (2026-07-27):** Raised P2→P1 during a session backlog review — the roadmap itself names this "the highest-value long-term validation feature" in Arc 4. Escalation reflects value judgment only; the §13 pre-clearance and effort-phasing conditions in this item's own scope note still apply before sprint entry.
**Type:** Product Feature / Backend + Frontend, gated
**Owner:** Head of Engineering; Product Owner
**Source:** Feature-gap review (current_roadmap.md §5 Arc 4, PO-05 — flagged as unbacklogged) — 2026-07-10
**Effort:** VH (>2 weeks)
**Provisional-Target:** v7.7 — named as v7.7 anchor scope 2026-07-21 (DL-074); `[gate status unverified/unmet]` — §13 determinism pre-clearance not yet run; effort (VH) exceeds typical single-cycle sizing, Release Planning to confirm phasing
**Depends on:** IT-06 Alpaca Paper Trading Integration (shipped v3.5) — foundational infrastructure this feature reuses

**Problem**
The roadmap names this "the highest-value long-term validation feature" in Arc 4, but no backlog item exists for it at all. There is currently no way for the user to test how a candidate strategy-rule change would have performed historically, or to replay a specific past setup/period against the paper-trading infrastructure that already exists and is otherwise unused for this purpose.

**Scope**
- §13 compliance pre-clearance: confirm the feature is a deterministic replay of the user's own historical data, not a predictive simulation (precedent: PS-03 Monte Carlo's determinism framing; IT-06's four binding conditions as a template for the review)
- Backend: replay a historical window of the user's own trade/candidate history through the existing paper-trading mechanics under the *current* rule set
- Frontend: date range or trade-set selector, and a clearly-labelled retrospective/deterministic output view
- Exact scope (single trade replay vs. full historical window, output format) to be confirmed by canonical spec before implementation, per the roadmap's Standing Notice

**Acceptance Criteria**
- User can select a historical date range or trade set and run it through paper-trading mechanics under current strategy rules
- Output is clearly labelled as retrospective/deterministic, not predictive
- §13 pre-clearance review completed and documented before sprint planning begins

---


### BLG-FEAT-76 — SI-05 Weekly Strategy Integrity Digest — Phase 2 (full digest)
**Priority:** P3 (Low)
**Type:** Product Feature / Backend + Frontend, gate-conditional
**Owner:** Head of Engineering; Head of UX & Design
**Source:** Feature-gap review (current_roadmap.md Arc 5 status table cross-referenced with BLG-FE-69, BLG-FE-71, BLG-GOV-121 — prep-only, no primary Phase 2 item existed) — 2026-07-10
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled (gated)
**Depends on:** BLG-FEAT-73 (SI-02 frontend) and BLG-FEAT-75 (SI-04) — hard-blocked on both shipping first; BLG-FE-69, BLG-FE-71, BLG-GOV-121 are prep items for this build

**Problem**
Only Phase 1 shipped (v5.0/v5.1) — a lightweight Telegram-only digest. The full-scope digest, incorporating SI-02 drift scores and SI-04 version comparison data, has prep items filed but no primary "build Phase 2" item ties them together, so this content will not exist even once its dependencies ship unless the digest itself is scoped and built.

**Scope**
- Extend the existing Telegram digest (or add an in-app channel, pending the Phase 2 channel decision referenced by BLG-FE-69/71) to include SI-02 drift score summaries and SI-04 version comparison highlights
- Sequenced explicitly last of the 5 items in this batch — must not enter sprint planning before SI-02 and SI-04 ship

**Acceptance Criteria**
- Weekly digest includes a drift score summary line
- Weekly digest includes a brief before/after comparison note when a strategy version change occurred in the reporting period
- Phase 2 channel decision (Telegram-only vs. added in-app view) resolved before frontend work begins

---


## 3. Frontend & UX Backlog

---

### BLG-FE-27 — Nav bar redesign exploration
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** v3.2 delivery verification — user feedback 2026-05-06
**Effort:** M (~1–2 days design + spec)
**Provisional-Target:** Arc 3 (design exploration — not urgent; no current blocking workflow)

**Problem**
The current nav bar occupies a fixed portion of the visible screen area. As the application grows in Arc 2 and beyond, the navigation structure may benefit from a redesign to reclaim vertical space. Options to evaluate: Sticky/Fixed Header (current pattern, optimised), mega menu (grouped sections), or breadcrumb navigation (context-sensitive, minimal footprint).

**Scope**
- Head of UX & Design to evaluate the three navigation patterns in the context of current and Arc 2 page inventory
- Produce a design recommendation with rationale (no implementation required at this stage)
- If redesign is recommended, produce a UX spec and create a follow-on implementation backlog item

**Acceptance Criteria**
- Design recommendation document produced (one of: maintain current, redesign to pattern X)
- Rationale covers: screen real-estate impact, mobile responsiveness, Arc 2 page count
- If redesign: UX spec produced and implementation backlog item filed

---

### BLG-FE-39 — Arc 2 user journey map
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** IDEA-ux-design-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped.

**Problem**
No end-to-end user journey map exists covering the full Arc 2 flow: Screener → Watchlist → Research View → Trade Plan → Execution. As Arc 2 ships its final features, a journey map would surface UX gaps, confirm feature sequencing, and establish the baseline for Arc 3 UX planning. Requires PT-04 to be shipped so the full flow is complete before mapping.

**Scope**
- User journey map covering screener discovery → trade plan creation → execution
- Identify friction points and hand-off gaps between views
- Produce design recommendation: maintain current or file targeted UX improvement items

**Acceptance Criteria**
- Journey map document produced
- Friction points enumerated; any actionable items filed as backlog entries
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FE-43 — SI-05 Weekly Digest frontend component spec
**Priority:** P1 (High) — escalated from P2, 2026-07-27, session product review (see note below)
> ⚠️ **Priority escalation (2026-07-27):** Raised P2→P1 during a session backlog review as the highest-priority Frontend/UX item. Note this item is a component spec (pre-work), not a shippable feature — its own gate criteria (SI-05 sprint planning imminent) still govern entry.
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend
**Source:** IDEA-base44-frontend-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-05 (Weekly Strategy Integrity Digest) sprint planning imminent.

**Problem**
SI-05 will deliver the Weekly Strategy Integrity Digest via Telegram notification and potentially an in-app view. No frontend component spec or UX spec exists for the digest display. Authoring this spec before sprint planning ensures frontend scope is clearly defined and sized — preventing mid-sprint ambiguity on rendering requirements.

**Scope**
- UX spec: digest layout, content sections (drift signal, red flag summary, compliance score trend), notification vs in-app view decision
- Component requirements document: data inputs, update frequency, display states (no data, loading, populated)
- Review against Telegram notification format constraints (v2.4 weekly digest pattern)

**Acceptance Criteria**
- Frontend component spec and UX spec produced and filed
- Component requirements document covers all SI-05 data inputs
- Spec reviewed by Product Owner and Head of UX & Design before sprint planning
- Gate condition verified before sprint planning

---

### BLG-FE-45 — Arc5ComplianceSection layout expandability review
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / UX
**Owner:** Base44 Frontend; Head of UX & Design
**Source:** IDEA-base44-frontend-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** v4.1 sprint planning complete — layout expandability review requires knowing which Arc 6 compliance data points will be added to the PerformanceAnalytics page.

**Problem**
Arc5ComplianceSection.js (shipped v4.0) displays 5 compliance metrics. Arc 6 will add performance science metrics to the same analytics surface. Without an expandability review, the component layout may require significant rework when additional data sections are added. A pre-sprint review ensures the component is structurally extensible.

**Scope**
- Review Arc5ComplianceSection layout for extensibility: grid, card count, responsive breakpoints
- Identify layout constraints that would prevent additional section additions
- Produce short design note with recommendations (retain, refactor, or modularise)

**Acceptance Criteria**
- Design note produced and reviewed by Product Owner
- Gate condition verified before sprint planning

---

---

### BLG-FE-54 — Arc 5 unified pre-entry gateway
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / UX Exploration
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260522-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 5 fully complete (SI-02, SI-04, SI-05 all shipped).

**Problem**
SI-01 (pre-entry validation panel) and PT-05 (entry checklist) are separate views requiring multi-view navigation before trade finalisation. A unified pre-entry gateway combining all required checks into a single screen could reduce friction and navigation complexity. Gate ensures design is informed by the complete Arc 5 feature set.

**Scope**
- Explore combining SI-01 and PT-05 into a single pre-entry gateway screen
- Map decision points and information needs for the combined flow
- Propose structural changes; not a committed sprint item until gate clears

**Acceptance Criteria**
- UX exploration document produced
- Combined flow mapped with clear decision points
- Gate condition (Arc 5 fully complete) verified before commencing

---

### BLG-FE-58 — Pre-entry panel: check grouping for Arc 5 expansion
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / UX Improvement
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** docs/product/ux/pre_entry_panel_ux_assessment.md — candidate P4 — cycle 2026-05-31__release-v4.7 (ST-09)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 or SI-04 sprint planning initiated (Arc 5 expansion imminent).

**Problem**
PreEntryValidationPanel currently displays 5 checks in a flat list. As SI-02 drift detection and SI-04 strategy version comparison add compliance context to the pre-entry flow, check count may grow to 8–10+ items. A flat list at that scale is dense and unscannable.

**Scope**
- Group checks into labelled sections: "Compliance" (Arc 5 checks), "Risk" (cash, sizing), "Technical" (regime, earnings)
- Section headers use small separator labels; no collapsible sub-groups required
- Prepare component structure for Arc 5 check additions before SI-02/SI-04 ship

**Acceptance Criteria**
- Checks grouped into at minimum 2 sections (Compliance and Risk/Technical)
- Grouping does not break existing override acknowledgement behaviour
- Gate condition (SI-02 or SI-04 sprint planning) verified before commencing

---

### BLG-FE-59 — Arc5ComplianceSection extension spec for SI-02/SI-04
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend
**Source:** IDEA-frontend-ux-20260527-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 disposition)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend + SI-04 sprint planning imminent (both Arc 5 features approaching their sprint entry).

**Problem**
Arc5ComplianceSection.js (shipped v4.0) displays 5 compliance metrics. SI-02 drift detection frontend and SI-04 strategy version comparison will each add new display cards to this section. Without extension point specifications defined in advance, each addition will require layout redesign rather than slotting into a prepared contract. Pre-specifying card layout contracts prevents rework.

**Scope**
- Update BLG-FE-48 spec (if exists) or author new: extension point specifications for SI-02 drift score card and SI-04 version comparison card
- Define card layout contract: minimum data fields, display states (loading, populated, gate-not-met), responsive breakpoints
- Ensure additions require no Arc5ComplianceSection.js layout redesign

**Acceptance Criteria**
- Extension spec document produced covering SI-02 and SI-04 card requirements
- Card layout contract defines all required display states
- Gate conditions (both SI-02 frontend + SI-04 sprint planning imminent) verified before commencing

---

### BLG-FE-62 — Pre-entry panel combined component specification (BLG-FE-56/57/58)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-87 shipped v5.0)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-FE-56/57/58 sprint planning imminent; SI-02 frontend activation triggered (20+ closed trades confirmed). BLG-GOV-87 re-entry criteria shipped v5.0 — functional activation gate still pending.

**Problem**
BLG-FE-56 (warn/fail override separation), BLG-FE-57 (count badge when collapsed), and BLG-FE-58 (check grouping for Arc 5) are three interdependent PreEntryValidationPanel improvements. Specifying them individually risks fragmented UX implementation. A combined specification aligns all three changes before sprint planning seals.

**Scope**
- Combined component spec covering all three BLG-FE-56/57/58 improvements as a coherent design
- Map interaction dependencies (e.g., grouping in BLG-FE-58 affects badge count in BLG-FE-57)
- Input to sprint planning when gate triggers; replaces need for three separate spec documents

**Acceptance Criteria**
- Combined component spec produced and reviewed by Head of UX & Design
- All three BLG-FE-56/57/58 scopes covered in a single document
- Gate condition verified before sprint planning

---

### BLG-FE-63 — Arc 5 completion visual consistency pre-review
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 binding conditions shipped v5.0; SI-04 is in Later horizon — gate triggers when SI-04 enters sprint planning.

**Problem**
SI-04 (strategy version comparison) and SI-05 (weekly digest display) will introduce new panels to the Arc 5 UI surface. No review of the existing Arc 5 design vocabulary (Pre-Entry panel, Red Flag Journal, Arc5ComplianceSection) has been done to ensure consistency before these additions begin. A pre-review before SI-04 implementation prevents retroactive consistency fixes.

**Scope**
- Review existing Arc 5 panel design patterns (colour, typography, layout, empty states)
- Identify consistency vocabulary: what patterns to carry forward to SI-04/SI-05 panels
- Produce short design vocabulary note; no implementation required

**Acceptance Criteria**
- Design vocabulary note produced covering existing Arc 5 panels
- Consistency patterns identified; input to SI-04/SI-05 sprint planning
- Gate condition verified before sprint planning

---

### BLG-FE-65 — User journey map: SI-05 Telegram digest to app action
**Priority:** P3 (Low)
**Type:** Frontend / UX Research
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-FE-55 (mobile responsiveness baseline, P3, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 1 introduces a new workflow pattern: the user receives a Telegram notification (weekly digest) and then takes an action in the app (review Red Flag Journal, check compliance score, adjust behaviour). This is the first push notification → app action flow in the system. Friction mapping this journey surfaces improvements before SI-05 Phase 2 scope is defined.

**Scope**
- Map the user journey from receiving the SI-05 digest to completing an in-app action
- Identify: entry points (what links are in the digest), navigation steps to the relevant app screen, any friction encountered
- Produce a brief journey map document with friction findings; file follow-up backlog items if significant friction discovered

**Acceptance Criteria**
- User journey map document produced
- Entry points and navigation steps documented
- Friction findings enumerated; any significant friction filed as a separate backlog item
- Head of UX & Design sign-off

---

### BLG-FE-66 — RFJ date-range filter (date-to field)
**Priority:** P3 (Low)
**Type:** Frontend / UX Refinement
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Source:** ST-07 RFJ visual design review — filed 2026-06-22 (cycle 2026-06-19__release-v6.0)
**Effort:** XS
**Provisional-Target:** Unscheduled
**Gate criteria:** Event volume makes date-from-only filtering insufficient for review workflows.

**Problem**
The Red Flag Journal filter panel supports a "From date" input only. A growing journal has no upper date bound — a user reviewing "last month's" events cannot scope the view to a period. At current low event volume this is acceptable, but will become limiting as the journal grows.

**Scope**
- Add a "To date" input to the RFJ filter panel
- Update `GET /portfolio/red-flag-journal` to accept an optional `until` parameter
- Convert current date-from-only filter to a date range (from + to)

**Acceptance Criteria**
- "To date" filter input present in filter panel
- Results are scoped to [date-from, date-to] when both are set
- "Clear filters" clears both date inputs
- Existing "From date" behaviour unchanged when "To date" is not set

---

### BLG-FE-67 — RFJ event type colour palette refinement
**Priority:** P3 (Low)
**Type:** Frontend / Cosmetic / Accessibility
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Source:** ST-07 RFJ visual design review — filed 2026-06-22 (cycle 2026-06-19__release-v6.0)
**Effort:** XS
**Provisional-Target:** Unscheduled

**Problem**
The Red Flag Journal uses four warm-spectrum colours (amber-400, orange-400, red-400, rose-400) that are semantically arbitrary and difficult to distinguish under the `light-daltonized` theme. The colour for `checklist_skipped` (orange-400) blends with risk-event colours, and `drawdown_prompt_dismissed` (rose-400) is perceptually similar to `stop_prompt_dismissed` (red-400).

**Scope**
- Update `EVENT_TYPE_CONFIG` in `src/pages/RedFlagJournal.js`:
  - `checklist_skipped`: `orange-400` → `sky-400` (administrative miss, not a risk event)
  - `drawdown_prompt_dismissed`: `rose-400` → `red-500` (deeper risk signal, distinguishable from red-400)
- No other changes required (icons, layout, data model unchanged)

**Acceptance Criteria**
- `checklist_skipped` renders with `sky-400` colour indicator
- `drawdown_prompt_dismissed` renders with `red-500` colour indicator
- Other two event types (amber-400, red-400) unchanged
- Colours visible and semantically distinct under `light-daltonized` theme

---

### BLG-FE-68 — Arc 5 compliance score sparkline trend chart (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Analytics Display
**Owner:** Metrics Definitions & Analytics Owner; Base44 Frontend Prompt Owner
**Source:** IDEA-metrics-analytics-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-FE-45 (Arc5ComplianceSection layout expandability review) complete

**Problem**
The Arc 5 compliance score is displayed as a single value on the compliance section. A sparkline trend chart showing the score's trajectory over recent weeks would help identify improving or degrading compliance at a glance. The gate is BLG-FE-45 — adding widgets to Arc5ComplianceSection before the layout expandability review is premature.

**Scope**
- Add sparkline trend chart to Arc5ComplianceSection (or equivalent compliance view)
- Data source: existing compliance score history endpoint or new rolling-window endpoint
- Chart shows last 8–12 weeks of compliance scores
- BLG-FE-45 must be complete before this enters sprint planning

**Acceptance Criteria**
- Sparkline chart renders in compliance section
- Data sourced from a defined endpoint (not mocked)
- Gate condition (BLG-FE-45) verified before sprint planning
- Playwright: chart renders with data; empty state handled

---

### BLG-FE-69 — SI-05 in-app digest panel — read-only last-sent view (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Notification Display
**Owner:** Base44 Frontend Prompt Owner; Frontend Specs & UX Documentation Owner
**Source:** IDEA-base44-frontend-20260607-01 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Phase 2 channel decision (BLG-GOV-92 SI-05 Phase 2 activation criteria) — if Telegram remains the sole channel, this item is not required

**Problem**
SI-05 weekly digest is delivered via Telegram (v5.1). Users who miss a Telegram message have no way to retrieve the last digest content from within the app. An in-app read-only panel showing the last-sent digest content would provide a fallback reference point. However, this is premature until the Phase 2 channel decision confirms an in-app component is warranted.

**Scope**
- Read-only digest panel in Settings or a new SI-05 section
- Shows last digest sent: date, content summary, link counts
- No composition or editing — display only
- Phase 2 channel decision must be made before sprint planning

**Acceptance Criteria**
- Panel renders last-sent digest content
- Date and delivery status visible
- Gate condition (BLG-GOV-92 Phase 2 decision) verified before sprint planning

---

### BLG-FE-70 — Compliance score trend widget on dashboard homepage (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Dashboard
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Source:** IDEA-base44-frontend-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-FE-45 (Arc5ComplianceSection layout expandability review) complete

**Problem**
Dashboard homepage shows key portfolio metrics but not the Arc 5 compliance score trend. A small trend widget on the homepage would surface compliance trajectory without requiring navigation to the full compliance section. Gate is BLG-FE-45 — homepage widget additions should follow the expandability assessment.

**Scope**
- Small compliance score trend widget on dashboard homepage
- Shows current score + trend arrow (up/down/flat vs prior week)
- Links to full Arc5ComplianceSection
- BLG-FE-45 must be complete before this enters sprint planning

**Acceptance Criteria**
- Widget renders on dashboard with current score and trend indicator
- Links correctly to full compliance section
- Gate condition (BLG-FE-45) verified before sprint planning

---

### BLG-FE-71 — SI-05 in-app digest UX spec — Phase 2 potential (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend Spec / UX
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Phase 2 channel decision (BLG-GOV-92) — if in-app delivery is confirmed for Phase 2, this spec should precede implementation

**Problem**
If SI-05 Phase 2 includes an in-app delivery channel, a UX spec will be required before frontend implementation begins. Authoring the spec before the Phase 2 channel decision is premature — the spec scope depends entirely on which channel(s) Phase 2 targets.

**Scope**
- Interaction pattern for SI-05 digest delivery in-app (read, dismiss, archive)
- Visual design: notification panel, badge indicators, read/unread states
- Produced only if Phase 2 channel decision confirms in-app component
- Must be completed before BLG-FE-69 sprint planning

**Acceptance Criteria**
- UX spec produced covering interaction patterns and visual design
- Reviewed by Head of UX & Design and Frontend Specs & UX Documentation Owner
- Gate condition (BLG-GOV-92) verified before authoring

---

### BLG-FE-81 — AI disclaimer component extraction
**Priority:** P3 (Low)
**Type:** Frontend / Refactor
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260702-02 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** TBD
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
BLG-UX-01 and BLG-UX-02 (both shipped v6.4) independently fixed disclaimer contrast on the AI daily briefing and AI chat widget respectively, each editing its own component's Tailwind classes. Without a shared component, a future third AI surface risks repeating the same contrast mistake.

**Scope**
- Extract a single `AiDisclaimer` component with the now-corrected WCAG-AA-passing slate values
- Replace the two existing inline disclaimer implementations with the shared component
- No visual change — refactor only

**Acceptance Criteria**
- Single shared disclaimer component used by both AI daily briefing and AI chat widget
- No visual regression (same rendered contrast as post-v6.4 fix)
- Playwright: existing disclaimer visibility assertions still pass

---

### BLG-FE-83 — Frontend bundle size optimization assessment
**Priority:** P3 (Low)
**Type:** Frontend / Performance
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A user-reported performance issue OR profiling data indicates bundle-size impact.

**Problem**
No formal assessment of current React bundle size or heavy dependencies has been performed. No user-reported issue currently motivates this — the gate exists specifically to avoid speculative optimisation work.

**Scope**
- Bundle analysis (e.g. source-map-explorer or equivalent) to identify heaviest dependencies
- Recommendations report; no implementation required at this stage

**Acceptance Criteria**
- Bundle analysis report produced
- Gate condition (reported issue or profiling signal) verified before commencing

---

### BLG-FE-84 — AI chat UI interaction study protocol
**Priority:** P3 (Low)
**Type:** Frontend / UX Research
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 — usage patterns must stabilise before a research protocol targeting them is designed.

**Problem**
No structured protocol exists to study how the AI chat advisor is actually used. Designing one before interaction patterns stabilise risks studying patterns that later shift.

**Scope**
- 5-question interaction study protocol targeting chat advisor usage
- Applied once gate clears

**Acceptance Criteria**
- Protocol document produced
- Gate condition (AI adoption window) verified before use

---


### BLG-FE-98 — WatchlistModal.js fails ESLint (24 problems) — same patterns fixed in Watchlist.js
**Priority:** P3 (Low)
**Type:** Frontend / Tech Debt
**Owner:** Head of Engineering
**Source:** ST-14 (BLG-FE-77), EPIC-03, v6.8 — Head of Engineering sign-off review — 2026-07-09
**Effort:** M (~1 day)
**Provisional-Target:** v6.9

**Problem**
`src/components/watchlist/WatchlistModal.js` (rendered directly by the just-refactored `Watchlist.js`) fails `npx eslint` with 24 problems (8 errors, 16 warnings): `process` referenced directly instead of importing `API_BASE_URL` from `base44Client.js` (same `no-undef` pattern fixed in Watchlist.js this sprint), the component function is 209 lines (max 50), a magic number (`409`), 5 forbidden-comment violations, and missing PropTypes on most props. Was out of scope for ST-14 (AC-01 was scoped to `Watchlist.js` only) but is the natural next file to bring into compliance given it shares the same defect patterns and is directly coupled to the file just fixed.

**Scope**
- Import `API_BASE_URL` from `base44Client.js` instead of reading `process.env` directly
- Decompose the 209-line component into smaller sub-components/hooks (mirroring the `useWatchlistData`/`useWatchlistModal` pattern from ST-14)
- Add PropTypes, remove comments, extract the magic number to a named constant

**Acceptance Criteria**
- `npx eslint src/components/watchlist/WatchlistModal.js` exits 0 with zero warnings/errors
- No functional or visual behaviour change

---


### BLG-FE-106 — Consolidate StrategyBenchmark.js page header onto shared PageHeader component
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of Engineering
**Source:** 2026-07-12__release-v7.0 design gate (ST-08, BLG-FE-95) — spec/implementation deviation observed while reviewing strategy_benchmark.md §2 Page Header — 2026-07-12
**Effort:** XS (<1h)
**Provisional-Target:** v7.10

**Problem**
`strategy_benchmark.md` §2 Page Header specifies the shared `PageHeader` component (`src/components/ui/PageHeader.js`) for the "Strategy Benchmark" page title, but the shipped `src/pages/StrategyBenchmark.js:497` hand-rolls its own header (icon + bare `<h1>` + `<p>`) instead. This is a pre-existing spec/implementation deviation, out of scope for the ST-08 light-theme contrast fix applied directly to the current markup this cycle. Left unresolved, this header will keep diverging from the shared component (e.g. future PageHeader-wide styling changes won't propagate here) and continues to violate the documented spec.

**Scope**
- Replace the hand-rolled header block in `StrategyBenchmark.js` (icon + h1 + p) with the shared `PageHeader` component (`title="Strategy Benchmark"`, `description="Compare live trading vs backtest"`)
- Preserve the `BarChart2` icon and "Benchmark data as of DD Mon YYYY" last-updated line via `PageHeader`'s available props or an adjacent element
- No visual regression beyond the intended consolidation

**Acceptance Criteria**
- `StrategyBenchmark.js` page header renders via the shared `PageHeader` component, matching `strategy_benchmark.md` §2
- Page title displays correctly in both light and dark themes (PageHeader's existing gradient treatment applies)
- `BarChart2` icon and last-updated line remain present and correctly placed
- No other page layout/behaviour changes

---




### BLG-FE-121 — Extract a shared modal-confirmation component to de-dupe bulk-actions/alerts patterns
**Priority:** P3 (Low) | **Type:** Frontend / Code Health | **Owner:** Head of Engineering | **Source:** IDEA-head-of-engineering-20260717-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-FE-117` (bulk actions) will need a confirmation-modal pattern with an undo window; a similar pattern will likely recur for `BLG-FE-116` (custom price alerts, deletion/edit confirmation) — risk of two near-duplicate modal implementations shipping in the same release.
**Scope:** Extract a single reusable confirmation-modal component (configurable message, optional undo-window countdown) ahead of `BLG-FE-116`/`BLG-FE-117` implementation.
**Acceptance Criteria:** Shared component exists and is referenced by both items' Base44 prompt templates before their sprint execution begins.

---

### BLG-FE-122 — Rewrite calendar.js against the react-day-picker v9+ API before EPIC-05 implementation
**Priority:** P2 (Medium) | **Type:** Frontend / Technical Debt | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** v7.4 readiness pass, `docs/specs/blg_spec_95_v7_4_ui_readiness_pass.md` §2 (AC-01), ST-01/BLG-SPEC-95 — 2026-07-17 | **Effort:** S | **Provisional-Target:** v7.10 (ahead of whichever release re-introduces `BLG-FE-118`)
**Depends on:** BLG-FE-118 (saved filter views and calendar view — parent feature)
**Problem:** `src/components/ui/calendar.js` wraps `react-day-picker` using the legacy v8 API (`classNames` keys `nav_button_previous`/`day_range_start`/`day_outside`/`day_range_middle`, plus a `components={{ IconLeft, IconRight }}` override). `package.json` now declares `react-day-picker ^10.0.1` (v9+ line), which replaced that entire API surface (`Chevron` replaces `IconLeft`/`IconRight`; `classNames` keys renamed, e.g. `range_start`/`outside`/`selected`/`today`/`disabled`/`hidden`). `calendar.js` has zero current consumers (dead code, pre-staged for EPIC-05), so nothing breaks today — but none of its style overrides will match once a page renders it, since the prop names it passes no longer correspond to anything the installed version reads.
**Scope:** Rewrite `calendar.js`'s `classNames` map and icon override against the `react-day-picker` v9+ API, preserving the existing visual output (component is otherwise a thin styling wrapper, no behavioural logic to change).
**Acceptance Criteria:** `calendar.js` renders correctly (spot-checked or covered by the `saved-filters-calendar.spec.js` Playwright baseline scoped in `blg_spec_95_v7_4_ui_readiness_pass.md` §5 AC-04) against the `react-day-picker` version pinned in `package.json` at the time EPIC-05 begins implementation; no `day_`-prefixed or `IconLeft`/`IconRight` v8-era keys remain in the file.

---

### BLG-FE-123 — `SystemStatus.js` `categorizeEndpoint()` missing `/price-alerts`, `/saved-filters`, and `/changelog` branches
**Priority:** P3 (Low) | **Type:** Frontend / Technical Debt | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** Recurrence escalation, `2026-07-17__release-v7.5` closure, carried across 3 Post-Ship Closure cycles (v7.5→v7.6→v7.7) pending "next roadmap review"; filed as a backlog item by roadmap rebalance `2026-07-24__scheduled` STEP 0 since the fix is application source code outside the Roadmap Engine's write scope; extended at post-ship closure `2026-07-24__release-v7.8` STEP 6 (a new `/changelog` top-level prefix was introduced this cycle by `GET /changelog/latest`, BLG-FE-128, and is not handled by any existing `includes()` branch either) | **Effort:** XS | **Provisional-Target:** v7.10

**Problem**
`src/pages/SystemStatus.js`'s `categorizeEndpoint()` function has no `includes()` branch for the `/price-alerts`, `/saved-filters`, or `/changelog` endpoint paths (shipped v7.5, v7.4, and v7.8 respectively). All three currently degrade gracefully to the `'Other'` category rather than their correct functional grouping — not a correctness bug (no wrong data shown, nothing broken), but a categorisation gap that has now persisted across 4 releases and grown by one more prefix.

**Scope**
Add `/price-alerts`, `/saved-filters`, and `/changelog` `includes()` branches to `categorizeEndpoint()`, grouping each under the appropriate existing category (or a new one if none fits) consistent with the function's existing pattern.

**Acceptance Criteria:**
- `categorizeEndpoint('/price-alerts')`, `categorizeEndpoint('/saved-filters')`, and `categorizeEndpoint('/changelog')` (and their sub-paths) each return a category other than `'Other'`
- No regression to existing endpoint categorisation

---

## 4. Backend & Data Backlog

---

### BLG-BE-13 — Screener result history table
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** IDEA-backend-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days (sufficient history to make a queryable history table valuable).

**Problem**
Each screener run overwrites or appends to the current results without a queryable historical table. After 60 days, trend analysis (how screener output has evolved over time) becomes valuable but requires a properly structured history table with per-run metadata (run_timestamp, run_id, ticker count, pass count, regime distribution). Without this, historical comparison is not possible.

**Scope**
- `screener_run_history` table: run_id, run_timestamp, total_tickers, pass_count, regime_distribution JSON
- `GET /screener/history` endpoint returning run history with pagination
- Backfill not required; populate from next run forward

**Acceptance Criteria**
- History table created and populated on each screener run
- `GET /screener/history` returns paginated run history
- Gate condition verified by Product Owner before sprint planning

---

### BLG-BE-14 — Trade plan schema versioning
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering; Head of Specs Team
**Source:** IDEA-backend-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 3 new fields added to trade plan schema after v3.4 baseline (indicating schema churn warrants versioning overhead).

**Problem**
Trade plan schema has grown incrementally. If the schema continues to change at pace (new fields, deprecated fields), reading old plans stored under prior schema versions becomes an issue. Schema versioning adds a `schema_version` field to each trade plan record, enabling readers to apply the correct transformation for older records. Gate ensures the overhead is warranted before introducing this complexity.

**Scope**
- Add `schema_version` field to trade plan records (default: current version)
- Transformation layer: when reading plans, apply version-appropriate defaults for missing fields
- Migration: backfill existing plans with baseline schema_version

**Acceptance Criteria**
- `schema_version` field present on all trade plan records
- Read path applies correct field defaults for legacy records
- Gate condition (≥3 new fields post v3.4) verified by Product Owner before sprint planning

---

### BLG-BE-21 — Arc 5 analytics endpoint versioning strategy
**Priority:** P3 (Low)
**Type:** Backend / API Design
**Owner:** Head of Backend Engineering; API Contracts Documentation Owner
**Source:** IDEA-backend-engineering-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 6 planning trigger — analytics endpoint versioning strategy needed when Arc 6 analytics endpoints are being designed alongside existing Arc 5 endpoints.

**Problem**
GET /analytics/arc5-compliance (shipped v4.0) and future Arc 6 analytics endpoints will coexist on the same service. Without an explicit versioning and naming convention, Arc 6 additions may collide with or shadow Arc 5 endpoints. A versioning strategy (path prefix, query param, or response envelope version) must be decided before Arc 6 sprint planning.

**Scope**
- Define endpoint versioning convention for analytics namespace
- Assess whether current /analytics/ prefix is extensible or requires refactoring
- Input to Arc 6 analytics endpoint design

**Acceptance Criteria**
- Versioning strategy documented in API design notes or openapi.yaml preamble
- Reviewed by API Contracts Documentation Owner and Head of Specs Team
- Gate condition (Arc 6 planning trigger) verified before commencing

---

### BLG-BE-24 — Red flag events retention policy
**Priority:** P2 (Medium)
**Type:** Backend / Data Lifecycle
**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner
**Source:** IDEA-backend-engineering-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** red_flag_events table 6+ months old (post 2026-11-22).

**Problem**
The red_flag_events table has no defined data retention policy. As override events accumulate over months, query performance may degrade without indexes and archiving strategy. Defining a retention policy before the table requires unplanned maintenance is standard operational hygiene.

**Scope**
- Define minimum required event fields for retention
- Define archiving cadence (e.g. events older than 12 months archived to cold storage)
- Define query performance thresholds that trigger archiving review
- Document policy in ops notes

**Acceptance Criteria**
- Retention policy document produced
- Archiving cadence defined
- Gate condition (table 6+ months old) verified before commencing

### BLG-BE-27 — SI-02 drift service query performance baseline
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Performance
**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Source:** IDEA-backend-engineering-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed (BLG-GOV-87 re-entry criteria shipped v5.0 — functional activation still pending trade count gate).

**Problem**
The SI-02 drift service (shipped v4.6) uses window functions over trade_history and trade_plans. With only 6 closed trades, current query volume is too low to surface meaningful index gaps. A performance baseline at activation volume (20+ trades) establishes the query cost before concurrent frontend load is introduced.

**Scope**
- Run drift score queries against staging at 20+ trade volume
- Record p50/p95 query latency per metric (early_entry_rate, momentum_override_rate, losing_streak_sizing, regime_deviation_rate)
- Identify indexes required to maintain sub-200ms response at projected load

**Acceptance Criteria**
- Performance baseline document produced for all 4 drift metric queries
- Indexes identified and filed as implementation items if needed
- Gate condition verified before sprint planning

---

### BLG-BE-28 — Arc 4 PO-03 behavioral pattern storage pre-design
**Priority:** P3 (Low)
**Type:** Backend Engineering / Data Model
**Owner:** Backend Engineering Patterns Owner; Data Model, Domain & Schema Owner
**Source:** IDEA-backend-engineering-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 gate met (6+ months AI journal entries ~Oct 2026) + Arc 4 sprint planning triggered.

**Problem**
PO-03 (Behavioural Error Taxonomy) requires a new classification table and error_type enum. Pre-designing the schema before Arc 4 sprint planning prevents same-sprint data model debt (pattern observed in v3.3 IT-01/02/03 backend split).

**Scope**
- Define error_type enum values (entry_too_early, sized_incorrectly, ignored_regime, held_too_long, etc.)
- Define behavioral_errors table schema (id, trade_id, journal_entry_id, error_type, notes, detected_at)
- Pre-design migration strategy; no implementation until Arc 4 sprint

**Acceptance Criteria**
- Schema pre-design document produced
- error_type enum values defined and reviewed by Metrics Definitions & Analytics Owner
- Gate condition verified before sprint planning

---

### BLG-BE-29 — Database index review for SI-02 drift queries
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Performance
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Source:** IDEA-head-of-engineering-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. To be completed alongside or immediately after BLG-BE-27.

**Problem**
SI-02 drift service queries trade_plans and trade_history with window functions and date-range filters. Appropriate indexes must be confirmed before frontend activation adds concurrent load. BLG-BE-27 establishes the baseline; this item implements any gaps found.

**Scope**
- Review current indexes on trade_plans (signal_id, entry_date, exit_date) and trade_history (trade_id, close_date)
- Add indexes identified as missing from BLG-BE-27 performance baseline
- Verify drift score queries benefit from new indexes via EXPLAIN ANALYZE

**Acceptance Criteria**
- Index gaps identified and addressed
- EXPLAIN ANALYZE output confirms index usage for all drift metric queries
- Gate condition verified before sprint planning

---

### BLG-BE-30 — SI-04 schema requirements pre-design
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Source:** IDEA-data-model-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 binding conditions shipped v5.0 — next gate is active sprint planning for SI-04 (Later horizon).

**Problem**
SI-04 strategy version comparison requires linking trade_plans to historical strategy_rules.md versions. Whether this is a new strategy_versions table, a foreign key, or a snapshot field must be decided before SI-04 sprint to avoid same-sprint data model debt. BLG-SPEC-43 (API contract) exists; data model pre-design is the remaining gap.

**Scope**
- Evaluate three schema options: new table (strategy_versions), FK on trade_plans (strategy_version), snapshot field (strategy_snapshot JSON)
- Recommend approach with rationale (versioning overhead vs query simplicity)
- Define migration path for existing trade_plans (backfill strategy)

**Acceptance Criteria**
- Schema pre-design document produced with recommended approach
- Reviewed by Data Model, Domain & Schema Owner and Strategy Rules & System Intent Owner
- Gate condition verified before sprint planning

---

### BLG-BE-31 — Arc 4 PO-04 reflection-outcome correlation data prerequisites
**Priority:** P3 (Low)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Source:** IDEA-data-model-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 gate met + Arc 4 sprint planning triggered (~Oct-Dec 2026).

**Problem**
PO-04 (Reflection ↔ Outcome Correlation) requires journal entries with quantified reflection depth scores linked to trade outcomes. Neither reflection depth scoring nor the linkage from journal_entries to trade outcomes is currently captured. A data prerequisites assessment determines whether new fields are needed before Arc 4 sprint planning.

**Scope**
- Assess current journal_entries and trade_history data models for PO-04 readiness
- Identify new fields required: reflection_depth_score, journal_entry_id on trade_history, etc.
- Document prerequisites; no implementation until Arc 4 sprint

**Acceptance Criteria**
- Data prerequisites assessment document produced
- New fields required for PO-04 identified and estimated
- Gate condition verified before sprint planning

---

### BLG-QA-21 — Arc 2 end-to-end QA protocol
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** IDEA-qa-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 feature set complete.

**Problem**
No consolidated end-to-end QA protocol covers the full Arc 2 feature set (Screener, Research View, Trade Plan, Setup Quality Score). Individual EPICs have per-story DoQ sign-offs, but there is no arc-level protocol that exercises the full workflow from screener discovery to closed trade with a quality score. Such a protocol is most valuable once Arc 2 is complete.

**Scope**
- Arc-level E2E test protocol document covering full Arc 2 flow
- Playwright automation for the core arc-level happy path
- Manual checklist for Arc 2 edge cases not covered by Playwright

**Acceptance Criteria**
- Arc 2 E2E protocol document produced and filed in `docs/qa/`
- Core happy path covered by Playwright
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-22 — Arc 2 DoQ standards review
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** QA Lead; Head of Specs Team
**Source:** IDEA-qa-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 feature set complete.

**Problem**
DoQ standards (shared_standards.md §DoQ) were established in Arc 1 and have evolved incrementally. Arc 2 introduced new feature types (research views, AI-assisted UX, trade plans) that may expose gaps in the existing DoQ rubric. A targeted review of DoQ standards against Arc 2 artefacts will ensure the standards remain fit for Arc 3 and beyond.

**Scope**
- Review DoQ standards against Arc 2 EPIC QA evidence files
- Identify any rubric gaps introduced by Arc 2 feature types
- Propose amendments to `shared_standards.md` DoQ section if warranted

**Acceptance Criteria**
- DoQ standards reviewed; gaps (if any) documented
- If amendments warranted: `shared_standards.md` updated per §6 governance checklist
- Gate condition verified before sprint planning

---

### BLG-QA-23 — Trade plan lifecycle end-to-end test
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** IDEA-qa-20260421-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped.

**Problem**
No Playwright test covers the full trade plan lifecycle: create → edit → link to position → close → view in plan-vs-reality. Individual story tests cover creation and display, but lifecycle continuity (plan survives position link, quality score visible at creation, plan-vs-reality renders post-close) is not tested end-to-end. PT-04 must be shipped to make the quality-score step part of the lifecycle.

**Scope**
- Playwright E2E test: create plan with quality score visible → link to position → close position → verify plan-vs-reality
- Cover: plan state transitions, quality score persistence, plan-vs-reality accuracy

**Acceptance Criteria**
- Full lifecycle Playwright test authored and passing in CI
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-26 — Arc 5 QA protocol
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 5 fully complete per BLG-QA-45 criteria (docs/qa/arc5_qa_completion_criteria.md): SI-01 ✅, SI-02 backend ✅, SI-03 ✅, SI-05 Phase 1 ✅, BLG-QA-49 coverage assessment ✅. SI-02 frontend, SI-04, and SI-05 Phase 2 explicitly excluded from trigger. Updated 2026-06-16 (ST-09 v5.6).

**Problem**
SI-01 through SI-03 shipped across v3.8 and v3.9. Each sprint produced per-story DoQ sign-offs but no arc-level QA protocol exists covering the full Arc 5 feature set end-to-end. Once all five features ship, an arc-level protocol analogous to BLG-QA-21 (Arc 2 E2E QA protocol) will ensure the complete Strategy Integrity workflow is tested holistically.

**Scope**
- Arc-level E2E test protocol document covering full Arc 5 flow: validation gate → override event → red flag journal → drift detection review → strategy version comparison → weekly digest
- Playwright automation for the arc-level happy path
- Manual checklist for Arc 5 edge cases not covered by Playwright
- Filed in `docs/qa/arc5_qa_protocol.md`

**Acceptance Criteria**
- Arc 5 E2E protocol document produced and filed
- Core happy path covered by Playwright
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-42 — SI-02 E2E Playwright test strategy and scaffold (consolidated)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038); consolidates BLG-QA-55 — a readiness-assessment follow-up on this item's own scaffold, gated on the same 20+ closed-trades condition — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. BLG-QA-37 (Playwright mock strategy for drift features, shipped v4.2) defines the approach — this item implements it.

**Problem**
SI-02 drift service (35 unit tests, shipped v4.6) has no E2E Playwright coverage. When the frontend ships (~2027-Q1), test coverage must be ready immediately. Pre-building the scaffold 1–2 cycles before activation avoids rushed test creation under sprint pressure.

**Scope**
- Define E2E test strategy for GET /analytics/behavioural-drift (per BLG-QA-37 Playwright mock strategy)
- Scaffold Playwright test file with scenarios: drift scores render, gate-not-met state, all 4 metric cards display
- Confirm mock data approach (per BLG-QA-37 mock strategy)
- Once the 20+ closed-trades gate clears and SI-02 frontend enters sprint planning: re-review this scaffold against the final drift service implementation (which may have evolved since authoring) and confirm the mock strategy is still valid before sprint entry

**Acceptance Criteria**
- E2E test strategy document produced
- Playwright test scaffold created and passing against mock data
- All 4 drift metric display scenarios covered
- Gate condition verified before sprint planning
- Pre-sprint-entry readiness confirmation recorded: "proceed with scaffold as-is" or a revision document produced, with Director of Quality sign-off

---

### BLG-QA-44 — SI-04 test planning requirements definition
**Priority:** P2 (Medium)
**Type:** QA / Test Planning
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 binding conditions shipped v5.0 — functional activation gate is SI-04 entering sprint planning (Later horizon).

**Problem**
SI-04 (strategy version comparison) requires test coverage across: unit tests (version comparison logic), integration tests (trade_plans version linkage), and Playwright (version diff display). Defining test requirements before sprint planning ensures test scope is clear and prevents test debt analogous to BLG-QA-24 (Yahoo Finance backoff).

**Scope**
- Define unit test requirements: version comparison logic, version not found case
- Define integration test requirements: trade_plans version linkage correctness
- Define Playwright scenario requirements: version diff display, empty state, gate-not-met
- Estimate test effort; input to sprint sizing

**Acceptance Criteria**
- Test requirements document produced covering all three test tiers
- Playwright scenario outlines defined
- Gate condition verified before sprint planning

---

### BLG-BE-41 — Deprecated table read-path audit
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Integrity
**Owner:** Head of Backend Engineering
**Source:** IDEA-backend-engineering-20260702-02 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** v7.10
**Effort:** S (~1 day)

**Problem**
BLG-BE-40 (v6.4) fixed a P1 correctness bug where signal generation read the deprecated `tickers` table instead of `ticker_universe`. No systematic check has been done to confirm this was the only deprecated-table read remaining in the codebase.

**Scope**
- Grep/audit all `database.py` read functions for references to tables superseded by a documented migration
- Cross-check against `data_model.md` migration history for tables marked deprecated
- File follow-up correctness items for any additional instances found

**Acceptance Criteria**
- Audit completed across all `database.py` read functions
- Findings documented; any additional deprecated-table reads filed as P0/P1 correctness items per severity
- Head of Backend Engineering sign-off

---

### BLG-BE-42 — Backend request tracing
**Priority:** P3 (Low)
**Type:** Backend Engineering / Observability
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A demonstrated multi-service call failure requiring cross-service tracing to diagnose.

**Problem**
No per-request trace ID propagation exists across routers/services. No incident has yet demonstrated a need for this level of observability — the gate exists to avoid speculative infrastructure investment.

**Scope**
- Trace ID generation at request entry; propagation through service-layer calls
- Surfaced in structured logs

**Acceptance Criteria**
- Trace ID present in logs across a multi-service call path
- Gate condition (demonstrated failure requiring tracing) verified before commencing

---

### BLG-BE-66 — Index review pass for trade_plan queries as row count grows
**Priority:** P3 (Low) | **Type:** Backend / Data Model | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260717-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `trade_plans` row count is currently small (11 rows per live check 2026-07-17) so no index pressure exists yet, but several endpoints join or filter on `position_id`/`ticker`/`status` without a confirmed index review.
**Scope:** A lightweight index audit against current query patterns, to be actioned proactively rather than reactively once row count grows materially.
**Acceptance Criteria:** Audit completed; any missing indexes identified (implementation deferred if no current performance impact, per gate below).
**Gate criteria:** Revisit when `trade_plans` row count exceeds ~500 or any query is observed exceeding baseline latency — not urgent at current scale.

---

### BLG-BE-67 — Canonical enum registry for position_state values shared frontend/backend
**Priority:** P3 (Low) | **Type:** Backend / Data Model | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260717-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Position lifecycle states (per `strategy_rules.md §9`) are referenced independently in backend enums and frontend badge-rendering logic, with no single canonical source confirmed for the value list.
**Scope:** Consolidate position-state values into one canonical registry (e.g. a shared constants file or OpenAPI enum) referenced by both layers.
**Acceptance Criteria:** Canonical registry exists; both backend and frontend confirmed to derive from it (or a documented reconciliation shows they were already consistent).

---

### BLG-BE-68 — Fix errors masked as HTTP 200 in portfolio_risk.py
**Priority:** P2 (Medium) | **Type:** Backend / API Consistency | **Owner:** Backend Engineering Patterns Owner | **Source:** BLG-BE-65 audit (ST-04, EPIC-04, v7.6) | **Effort:** S (~0.5d) | **Provisional-Target:** v7.10

**Problem**
`portfolio_risk.py`'s four endpoints (`/drawdown-status`, `/concentration-status`, `/sector-weights`, `/gate-metrics`) catch all exceptions and return `{"status": "ok", "data": {..., "error": str(e)}}` (first three) or `{"status": "error", "error": str(e)}` (last one) as a bare dict — implicit HTTP 200 in all four cases. This violates `conventions.md` §13.3 ("error responses must not use HTTP 200 with an error body") and is a correctness/observability issue, not just cosmetic inconsistency: a frontend caller checking only `response.status === "ok"` would treat these backend failures as success. Identified during the `docs/specs/api_contracts/backend_engineering_patterns.md` §Error-response envelope conformance audit (v1.3).

**Scope**
- Convert all four catch blocks to return `JSONResponse(status_code=500, content={"status": "error", "message": str(e)})` per the canonical envelope (`conventions.md` §13), matching the `research.py` reference pattern.

**Acceptance Criteria**
- All four endpoints return HTTP 500 with the canonical `{status, message}` envelope on internal error
- Existing 200-path success shapes unchanged
- Regression test confirms the error path no longer returns HTTP 200

---

### BLG-BE-69 — Conform remaining routers to canonical error envelope + status codes
**Priority:** P3 (Low) | **Type:** Backend / API Consistency | **Owner:** Backend Engineering Patterns Owner | **Source:** BLG-BE-65 audit (ST-04, EPIC-04, v7.6) | **Effort:** M (~1–2d) | **Provisional-Target:** TBD

**Problem**
Across `alerts.py`, `analytics.py`, `digest.py` (401 case + `/weekly` wrong-status-code case), `ai.py` (422 case), `paper_trading.py`, `plan_vs_reality.py`, `portfolio_size.py`, `red_flag_journal.py`, `saved_filters.py`, `screener.py` (400/404/409 cases), `strategy_benchmark.py`, `ticker_universe.py`, `trade_plans.py` (404 case), `trades_export.py`, `validation.py` (500 case), `watchlist.py`, `earnings.py`, `news.py` — error responses use FastAPI's default `{"detail": "..."}` envelope (via bare `raise HTTPException`, no global exception handler exists) instead of the canonical `{"status": "error", "message": "..."}` envelope from `conventions.md` §13. `digest.py`'s `/weekly` catch-all additionally returns the correct shape but at the wrong HTTP status (200 instead of 500). Identified during the `docs/specs/api_contracts/backend_engineering_patterns.md` §Error-response envelope conformance audit (v1.3).

**Scope**
- Migrate each listed endpoint's error paths to `JSONResponse(status_code=X, content={"status": "error", "message": ...})` per the `research.py` reference pattern.
- Large mechanical change across ~17 files — apply incrementally, not as one PR, to keep review scope manageable.

**Acceptance Criteria**
- All listed router error paths return the canonical `{status, message}` envelope at the correct HTTP status code
- No change to success-path shapes
- No change to existing frontend error-handling behaviour without a corresponding frontend check (per BLG-BE-65's original Security AC)

---

### BLG-QA-115 — Staging sign-off needed: custom price alert live delivery firing (ST-02, EPIC-02, v7.5)
**Priority:** P2 (Medium) | **Type:** QA / Test Coverage | **Owner:** Director of Quality | **Source:** ST-02 (EPIC-02, v7.5, BLG-FE-116) sprint execution, CLAUDE.md §2 frontend testing gate — 2026-07-17 | **Effort:** XS
**Provisional-Target:** v7.5

> ⚠️ **Stale target notice (groom backlog 2026-07-20):** `v7.5` shipped 2026-07-20 (cycle `2026-07-17__release-v7.5`) without this item's staging sign-off being recorded — the item's own acceptance criteria require a live staging run distinct from the shipped code, so this is expected (the code shipped; the sign-off follow-up remains open). Provisional-Target should be updated to reflect the next scheduled staging window, or the item closed once the sign-off is recorded.

> ⚠️ **Missing Effort Day-Range (groom backlog 2026-07-20):** `Provisional-Target: v7.5` names a specific release but `Effort: XS` carries no day range in parentheses — flagged per §16.12, not backfilled (owner judgment required).

**Problem:** ST-02's "Alert fires via the existing notification delivery channel when its condition is met" acceptance criterion requires a live price crossing a live threshold and a real Telegram delivery — CI cannot reproduce this (same class as the canonical `shared_standards.md §16.11` staging-only example). The other two ACs (create alert from UI; view/edit/delete active alerts) are fully covered by Playwright (`tests/e2e/custom-price-alerts.spec.js`, 11 scenarios) and the evaluation/trigger logic is unit-tested with mocked pricing (`tests/test_price_alerts_service.py`, 21 scenarios), but end-to-end delivery firing has no automated coverage.
**Scope:** Perform a human staging run: create a price alert with a threshold already crossed by the live market price, trigger `POST /alerts/evaluate` on staging, and confirm (a) the alert deactivates (`active=false`, `triggered_at` set), (b) a `notifications` row is created with `alert_type='custom_price_alert'`, and (c) the Telegram delivery is received.
**Acceptance Criteria:**
- Staging run performed and dated in the ST-02 DoQ sign-off block (`qa_evidence_EPIC-02.md`)
- All three delivery-firing checks above confirmed pass
- This backlog item closed/archived once the staging run is recorded

---

### BLG-QA-116 — Backfill regression baseline with 24 undocumented Playwright spec files (v6.0-v7.3)
**Priority:** P3 (Low) | **Type:** QA / Test Automation | **Owner:** Director of Quality | **Source:** ST-02 (EPIC-02, v7.6, BLG-QA-112) sprint execution — 2026-07-20 | **Effort:** M (~1–2d) | **Provisional-Target:** TBD

**Problem**
`docs/qa/regression_test_suite_baseline.md` Part 2 (Playwright End-to-End Test Suite) was last comprehensively refreshed at v5.9 (2026-06-17) and, prior to this cycle, listed 41 spec files. `tests/e2e/` actually contains 70 spec files as of v7.6 — 24 files added between v6.0 and v7.3 (separate from ST-02's own 5 v7.4–v7.6 additions, which brought the documented total to 46) are not catalogued: no scenario count, feature/area mapping, or Arc coverage entry. This was out of ST-02's scope (which only required entries for `BLG-FE-115` through `BLG-FE-119`) but is a real and growing documentation gap noted during that item's execution.

**Scope**
- Enumerate all spec files in `tests/e2e/` not currently listed in Part 2 of `regression_test_suite_baseline.md`
- Add a row for each: scenario count (via `test(` grep), feature/area name, introduced version (where determinable from git history or the file's own header comment)
- Update Part 3 Arc coverage mapping and Part 4 Full Regression totals to match

**Acceptance Criteria**
- Part 2 table lists all spec files present in `tests/e2e/` at time of this item's execution
- Total spec files / Total scenarios counts match the table exactly
- Part 3 Arc coverage table references every newly-added file
- Director of Quality sign-off recorded

---

### BLG-QA-127 — Serve production build for Playwright E2E webServer instead of CRA dev server
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA Lead
**Source:** User-directed CI runtime review (acting as QA & Testing Owner / QA Lead / Director of Quality) — 2026-07-28
**Effort:** M (~1-2 days)
**Provisional-Target:** v7.10

**Problem**
The `playwright-e2e` CI job boots the app via `npm start` (`react-scripts` dev server, unminified, webpack dev-middleware) rather than a production build. All 382 `page.goto()` navigations across the 677-test suite pay dev-server compile/serve overhead on every run. This was identified alongside REC-CI-01 (workers/shard parallelization, actioned 2026-07-28 — see `docs/ops/ci_pipeline_baseline.md` v1.1) but deferred: it requires adding a new dependency (`serve` or `http-server`, neither currently installed) and restructuring how `REACT_APP_API_URL` / `REACT_APP_DEV_FAKE_AUTH` / `REACT_APP_ANTHROPIC_API_KEY` are injected, since CRA bakes `REACT_APP_*` vars into the bundle at build time, not serve time — the current workflow sets them as runtime env vars against the dev server.

**Scope**
- Add a build step (`npm run build`) before Playwright runs in CI, with `REACT_APP_*` vars present at build time
- Add and pin a static-serve dependency (`serve` or `http-server`) to serve the build output on port 3000
- Update `playwright.config.js` `webServer.command` to be CI-conditional (production serve in CI, `npm start` for local dev/live-reload)

**Acceptance Criteria**
- CI E2E job builds and serves a production bundle instead of the dev server
- All existing `REACT_APP_*`-gated behaviour (dev fake auth, API base URL, "Improve with AI" button gate) still functions correctly under the production build
- Local `npx playwright test` (non-CI) continues to use `npm start` / live reload, unaffected
- Re-measured CI runtime shows improvement over the workers+shard baseline (REC-CI-01) alone
- QA Lead sign-off recorded

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0/v3.4/v3.9/v4.6 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints); v3.4 post-ship closure 2026-05-14 (2 additional endpoints); v3.5 post-ship closure 2026-05-15 (2 additional endpoints); v3.9 post-ship closure 2026-05-22 (1 additional endpoint: GET /portfolio/red-flag-journal); v4.6 post-ship closure 2026-05-31 (1 additional endpoint: GET /analytics/behavioural-drift)
**Effort:** M (~2 days — 24 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Twenty-two endpoints shipped in v2.8/v2.9/v3.0/v3.1/v3.4/v3.5 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-05-31):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- v3.1 endpoints (10): `POST /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`, `GET /trade-plans/by-ticker/{ticker}`, `GET /research/{ticker}`, `GET /earnings/{ticker}`, `GET /reports/monthly-pnl`, plus any additional v3.1 routes
- v3.4 endpoints (2): `GET /portfolio/drawdown-status`, `GET /portfolio/concentration-status`
- v3.5 endpoints (2): `GET /portfolio/paper-positions`, `GET /trades/{trade_id}/plan-vs-reality`
- v3.9 endpoints (1): `GET /portfolio/red-flag-journal`
- v4.6 endpoints (1): `GET /analytics/behavioural-drift`
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 24 endpoints have p50 and p95 latency entries in the baseline document
- Entries consistent with existing baseline measurement methodology

---

### BLG-OPS-17 — Alpaca API cost monitoring
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days (sufficient history to establish a meaningful cost baseline).

**Problem**
Alpaca API call volume (paper-positions, orders, account data) is not tracked. After 60 days of screener and research operations, a cost-per-run baseline can be established. Without a baseline, it is impossible to detect cost regressions when new features or higher screener frequency are introduced.

**Scope**
- Instrument Alpaca API call count per endpoint per day
- Log to `api_cost_log` or equivalent structured log
- Daily/weekly aggregate report

**Acceptance Criteria**
- Alpaca API call count logged per endpoint per run
- Aggregate report computable
- Gate condition verified by Infrastructure & Operations Owner before sprint planning

---

### BLG-OPS-18 — Data pipeline cost baseline
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-17 complete (Alpaca cost monitoring instrumented).

**Problem**
No aggregate data pipeline cost baseline exists covering Alpaca, Yahoo Finance, and news API calls together. Once Alpaca is instrumented (BLG-OPS-17), a combined baseline across all external data dependencies can be produced. Without this, cost anomalies across the pipeline are invisible.

**Scope**
- Aggregate cost baseline: Alpaca + YF + news API per week
- Baseline document filed in `docs/ops/`
- Alert threshold definition: >2× baseline triggers advisory

**Acceptance Criteria**
- Combined pipeline cost baseline document produced
- Alert threshold defined
- Gate condition (BLG-OPS-17 complete) verified before sprint planning

---

### BLG-OPS-19 — External API cost attribution per feature
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-17 complete (Alpaca cost monitoring instrumented).

**Problem**
External API calls are not attributed to the feature or workflow that triggered them. After BLG-OPS-17 instruments Alpaca, the next step is attributing each API call to the triggering feature (screener run, research view load, trade plan creation). This enables per-feature cost analysis and informs future optimisation decisions.

**Scope**
- Call attribution: tag each outbound API call with the triggering endpoint/feature
- Attribution report: cost breakdown by feature
- Identify top 3 cost contributors

**Acceptance Criteria**
- Each external API call tagged with triggering feature
- Attribution report computable
- Gate condition (BLG-OPS-17 complete) verified before sprint planning

---

### BLG-OPS-20 — Research endpoint cost monitoring
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-02 (Research View) live ≥ 30 days.

**Problem**
Research view loads trigger multiple downstream API calls (Yahoo Finance OHLCV, earnings, news). The per-session API cost of the research endpoint is not tracked. After 30 days of research view usage, a cost-per-session baseline can be established and anomalies detected.

**Scope**
- Instrument research endpoint: log external API calls triggered per request
- Cost-per-session aggregate (weekly baseline)
- Anomaly detection: sessions with >2× baseline API call count

**Acceptance Criteria**
- Research endpoint API call count logged per session
- Weekly baseline computable
- Gate condition verified by Infrastructure & Operations Owner before sprint planning

---

### BLG-OPS-21 — Arc 2 compute cost review
**Priority:** P3 (Low)
**Type:** Operations / Cost Review
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-05 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped AND 30-day cost baseline exists (BLG-OPS-17 or BLG-OPS-18 complete).

**Problem**
Arc 2 adds screener batch processing, research endpoints, and AI-assisted trade plan features. No compute cost review has been conducted since Arc 1. Once Arc 2 is complete and a 30-day cost baseline is available, a targeted review of Arc 2 compute overhead (CPU, memory, external API cost) should be conducted to inform Arc 3 infrastructure decisions.

**Scope**
- Review compute cost across Arc 2 features against Arc 1 baseline
- Identify top 3 cost drivers
- Produce recommendations for Arc 3 infrastructure planning

**Acceptance Criteria**
- Arc 2 vs Arc 1 compute cost comparison produced
- Recommendations filed
- Gate condition verified before sprint planning

---

### BLG-OPS-23 — Screener performance benchmark
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-07 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-13 (performance baseline) complete.

**Problem**
Screener batch runs involve 500+ ticker OHLCV fetches. No formal latency benchmark exists for screener run duration (p50/p95 end-to-end). BLG-OPS-13 establishes the API endpoint baseline; this item extends that to the full screener batch run. Without a benchmark, regressions introduced by new screener features (e.g., quality scoring) cannot be detected.

**Scope**
- Benchmark: full screener run duration (p50/p95) against full ticker universe
- Filed in `docs/ops/api_performance_baseline.md`
- Regression alert threshold: >1.5× baseline duration

**Acceptance Criteria**
- Screener run p50/p95 benchmark measured and filed
- Regression threshold defined
- Gate condition (BLG-OPS-13 complete) verified before sprint planning

---

### BLG-OPS-24 — Research endpoint performance benchmark
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-08 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-13 (performance baseline) complete AND research endpoint shows regression risk (p95 latency trending up over 30d).

**Problem**
BLG-OPS-13 adds research endpoints to the API performance baseline, but ongoing p95 trending is not monitored. If the research endpoint p95 latency trends upward over 30 days (indicating regression from data volume growth or upstream API changes), a targeted benchmark re-run and root cause investigation is warranted.

**Scope**
- Monthly p95 latency tracking for research endpoint
- Trend report: 30d rolling p95 chart
- Root cause investigation trigger at >1.5× baseline

**Acceptance Criteria**
- Monthly p95 tracking implemented
- Trend report computable
- Gate condition (BLG-OPS-13 + regression trend) verified before sprint planning

---

### BLG-OPS-25 — Automated staging smoke test on deploy/merge (consolidated)
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Director of Quality; Infrastructure & Operations Owner
**Source:** IDEA-director-of-quality-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033); consolidates BLG-OPS-100, BLG-OPS-102, BLG-OPS-107, BLG-OPS-119 — the same capability was independently re-proposed across four idea-intake cycles (2026-07-08 through 2026-07-24) without cross-reference to this existing item or each other — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** None — BLG-OPS-27 (automated staging re-deployment on main merge) shipped v4.0 (2026-05-25); the deploy hook mechanism this item depends on already exists.

**Problem**
Every delivery verification run begins with manual staging health checks, and staging deploys have no automated smoke test — deployment regressions (broken environment, missing env vars, cold-start failures) are caught manually or not until the next deliberate check.

**Scope**
- Smoke test suite: 3–5 critical endpoint health checks (backend health, screener availability, positions endpoint)
- Triggered automatically on both staging deploy and merge to main (the BLG-OPS-27 deploy hook fires on merge, so these are the same trigger in practice)
- Also runs on a scheduled cadence (e.g. weekly), independent of deploy/merge events, to catch environment drift between deploys
- Failure: deploy pipeline reports failure; delivery verification engine advised; alert on scheduled-run failure
- Output: smoke test pass/fail result stored in CI artefacts

**Acceptance Criteria**
- Smoke test suite authored and triggered on staging deploy / merge to main
- Suite covers minimum 3 critical endpoints
- Failure prevents "staging ready" signal from being issued
- Suite also runs on a scheduled cadence and alerts on failure independent of deploy events
- Confirmed to fail correctly on a deliberately-broken staging deploy (dry run)

---

### BLG-OPS-41 — Red flag events table archiving strategy
**Priority:** P2 (Medium)
**Type:** Operations / Data Lifecycle
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** red_flag_events table 6+ months old (post 2026-11-22).

**Problem**
The red_flag_events table has no defined retention or archiving strategy. As override events accumulate, the table will grow. Without an archiving policy, the table may require unplanned manual intervention. Defining the strategy before the table reaches significant size is operationally prudent.

**Scope**
- Define: retention window (e.g., keep 12 months active; archive older rows to cold storage)
- Define: archiving trigger (size-based vs age-based) and procedure
- Document strategy in ops notes; complement BLG-BE-24 retention policy

**Acceptance Criteria**
- Archiving strategy document produced
- Retention window and trigger defined
- Gate condition (table 6+ months old) verified before commencing

---

### BLG-OPS-48 — ANTHROPIC_API_KEY 6-month scope audit
**Priority:** P2 (Medium)
**Type:** Operations / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** ~v4.9 (date-gated: no earlier than 2026-11-01)
**Provisional-Target:** Gate date: 2026-11-01 (~6 months after BLG-OPS-36 scope review in v4.2, 2026-05-28)

**Problem**
BLG-OPS-36 (ANTHROPIC_API_KEY scope review) was completed in v4.2 (2026-05-28). Security policy (BLG-OPS-38) requires periodic key scope reviews. 6-month follow-up due ~November 2026 to verify key scope remains minimal and no scope creep has occurred in the API key permissions.

**Scope**
- Review ANTHROPIC_API_KEY permissions against current usage patterns
- Confirm key is not used outside the documented endpoints (generate-thesis, check-daily-cost)
- Verify key rotation has occurred per BLG-OPS-38 policy
- Document review findings

**Acceptance Criteria**
- ANTHROPIC_API_KEY scope confirmed minimal (only documented endpoints)
- Key rotation confirmed per BLG-OPS-38 schedule
- Review findings documented

---

### BLG-SPEC-35 — PO-02 §13 boundary review for AI cross-journal analysis
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning imminent.

**Problem**
PO-02 (Journal Pattern Recognition) will use AI to analyse cross-journal entries for recurring themes, emotional patterns, and setup types. This is an AI-assisted analysis of trading behaviour — the §13 boundary review must confirm this constitutes display/insight only and does not constitute signal generation or automated advisory. §13 PASS is required before PO-02 sprint planning seals.

**Scope**
- Run §13 checklist against PO-02 story set before sprint planning seals
- Confirm AI analysis output is: display-only, human-reviewed, no automated position recommendations
- Document binding conditions (if any) analogous to IT-06 §13 PASS conditions
- Sign-off recorded in sprint planning artefact

**Acceptance Criteria**
- §13 review completed; PASS or FAIL determination documented
- Binding conditions (if any) recorded
- Gate condition verified before PO-02 sprint planning seals

---

### BLG-SPEC-36 — PO-02 AI output audit schema
**Priority:** P2 (Medium)
**Type:** Spec / Governance
**Owner:** AI Compliance & Governance Officer; Head of Specs Team
**Source:** IDEA-ai-compliance-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning imminent.

**Problem**
PO-02 will generate AI output (pattern summaries, theme classifications) using an LLM. Governance policy requires AI-generated content to be traceable to model version, prompt version, and input at time of generation. Designing the audit log schema before sprint planning ensures it is built in from day 1, avoiding retroactive compliance debt.

**Scope**
- Design audit log schema: pattern_id, model_version, prompt_version, journal_ids_included, output_hash, generated_at
- Storage mechanism: append-only table or structured log file
- Retention policy: minimum 90 days
- Schema reviewed by AI Compliance & Governance Officer and Head of Specs Team

**Acceptance Criteria**
- Audit log schema designed and documented
- Storage mechanism defined
- Retention policy specified
- Gate condition verified before sprint planning

---

### BLG-SPEC-44 — SI-02 drift threshold calibration specification
**Priority:** P2 (Medium)
**Type:** Specification / Metrics Definition
**Owner:** Metrics Definitions & Analytics Owner; Head of Specs Team
**Source:** IDEA-metrics-analytics-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-87 shipped v5.0)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. BLG-GOV-87 re-entry criteria document shipped v5.0 — functional activation gate still pending.

**Problem**
SI-02 backend (shipped v4.6) defines 4 drift metrics (early_entry_rate, momentum_override_rate, losing_streak_sizing, regime_deviation_rate) but does not specify meaningful alert thresholds. Without calibrated thresholds, the frontend display may surface false positives (alert fatigue) or miss genuine drift. Thresholds should be defined before frontend activation.

**Scope**
- Define alert thresholds for each of the 4 drift metrics (e.g., early_entry_rate > 40% = amber, > 60% = red)
- Provide rationale for each threshold (e.g., based on your own historical compliance data, statistical percentiles)
- Define score interpretation guidance for the user-facing display
- Add threshold definitions to metrics_definitions.md (per §12 of that document)

**Acceptance Criteria**
- Threshold calibration specification document produced
- All 4 drift metrics have defined alert levels with rationale
- metrics_definitions.md updated with drift threshold definitions
- Gate condition verified before sprint planning

---

### BLG-SPEC-46 — Arc 4 API contract pre-planning surface area
**Priority:** P3 (Low)
**Type:** Specification / API Contracts
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-SPEC-35 (PO-02 §13 boundary review) complete. Arc 4 API contract surface area is premature before §13 determines whether PO-02/PO-03 constitute "adaptive logic" or "structured pattern extraction."

**Problem**
PO-02 (journal pattern recognition) and PO-03 (behavioural error taxonomy) will each require new API endpoints. Pre-defining the endpoint surface area (GET /analytics/journal-patterns, classification endpoints) before Arc 4 sprint prevents same-sprint API spec debt analogous to the Arc 5 retroactive contracts filed in v4.1/v4.2.

**Scope**
- Define candidate endpoint names and response shapes for PO-02 and PO-03
- Produce lightweight endpoint surface area document (not full contracts — just paths, methods, response envelopes)
- Input to Arc 4 release planning; pre-authorise contract authoring for named endpoints

**Acceptance Criteria**
- Endpoint surface area document produced for PO-02 and PO-03 APIs
- Reviewed by API Contracts & Documentation Owner and Head of Specs Team
- Gate condition (BLG-SPEC-35 complete) verified before commencing

---

### BLG-SPEC-55 — Arc 4 API contract pre-planning surface area advancement check (gate-conditional)
**Priority:** P3 (Low)
**Type:** Specification / API Contracts
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning confirmed imminent — when PO confirms ≥6 months AI-summarised journal entries gate is cleared and PO-02 is entering sprint planning

**Problem**
BLG-SPEC-46 (Arc 4 API surface area) is a gate-conditional spec planning item that was parked until PO-02 sprint planning is imminent (~Oct 2026). When that gate clears, an advancement check should confirm BLG-SPEC-46's scope still reflects the final Arc 4 API surface — the surface may have evolved since BLG-SPEC-46 was authored. This item tracks that confirmation step.

**Scope**
- Review BLG-SPEC-46 against current api_contracts/ documents and openapi.yaml
- Confirm Arc 4 API surface is still accurately captured or produce a revision scope
- Produce brief readiness note: "BLG-SPEC-46 proceed as-is" or list required updates
- Gate: PO-02 sprint planning imminent confirmation by PMO Lead

**Acceptance Criteria**
- BLG-SPEC-46 scope reviewed against current API surface
- Readiness note produced with clear proceed/update decision
- API Contracts & Documentation Owner sign-off
- Gate condition verified

---

### BLG-GOV-26 — Arc velocity tracking dashboard
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead
**Source:** IDEA-governance-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 velocity history complete.

**Problem**
No arc-level velocity tracking exists. Cycle velocity is tracked per-cycle (cycle_velocity in run_manifest.md), but no aggregate view shows velocity trends across an entire arc. Once Arc 2 is complete (PT-04 shipped), an Arc 2 velocity retrospective would establish baseline expectations for Arc 3 planning.

**Scope**
- Arc velocity report: stories/cycle, epic completion rate, arc-level rolling velocity
- Filed in governance reporting; updated at arc close
- Input to release planning engine for arc-boundary cycles

**Acceptance Criteria**
- Arc 2 velocity report produced at arc close
- Report format reusable for Arc 3+
- Gate condition verified by PMO Lead before sprint planning

---

### BLG-GOV-27 — Cross-arc dependency map
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-governance-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 3 arcs running concurrently (Arc 3, Arc 4, Arc 5 or later all in active/planned state simultaneously).

**Problem**
Current arcs (Arc 2, Arc 3, Arc 4) have informal dependency tracking (noted in roadmap annotations). If 3 or more arcs are in concurrent active or planned state, cross-arc dependency conflicts become a risk: feature data dependencies, shared backend schema changes, and governance sequencing conflicts all require explicit mapping. Gate ensures effort is only incurred when the complexity warrants it.

**Scope**
- Cross-arc dependency map: for each arc, list upstream arcs (data dependencies) and downstream arcs (consumes output)
- Conflict detection: identify stories across arcs that modify shared resources
- Filed in `claude/strategy/`

**Acceptance Criteria**
- Cross-arc dependency map produced
- Conflicts (if any) documented and escalation plan filed
- Gate condition (≥3 concurrent arcs) verified by PMO Lead before sprint planning

---


### BLG-GOV-29 — Trade plan AI summary audit log
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; QA Lead
**Source:** IDEA-governance-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** AI trade plan analysis feature scoped and scheduled (i.e., a story exists in the backlog that adds AI-generated trade plan summaries or analysis).

**Problem**
If an AI-assisted trade plan analysis feature is scoped (generating text summaries, recommendations, or signals using an LLM), an audit log is required per governance policy (AI-generated content must be traceable to the model version, prompt version, and input at time of generation). Without a pre-designed audit log schema, retrofitting this after feature delivery creates governance debt.

**Scope**
- Audit log schema: plan_id, model_version, prompt_version, input_hash, output_hash, generated_at
- Storage: append-only table or log file
- Retention policy: minimum 90 days

**Acceptance Criteria**
- Audit log schema designed and documented
- Storage mechanism implemented
- Gate condition (AI trade plan analysis feature scoped) verified by Head of Specs Team before sprint planning

---

### BLG-GOV-68 — Backlog item inter-dependency tracking
**Priority:** P2 (Medium)
**Type:** Governance / Process Enhancement
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260522-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** 20+ concurrent implementation items in a single sprint causing dependency-blocking.

**Problem**
Backlog items have no explicit Blocks/Blocked-by fields. Cross-item dependencies are currently documented via prose in backlog entries (e.g. "Gate: BLG-OPS-36 complete"). As the backlog grows, undiscovered dependencies become sprint-time blockers. A formal inter-dependency field would surface critical path items at sprint planning.

**Scope**
- Add Blocks/Blocked-by field to backlog item format (optional; populated when dependency is known)
- Update sprint planning engine to surface Blocks/Blocked-by chains
- Back-fill critical known dependencies (BLG-OPS-36 → BLG-OPS-37, etc.)

**Acceptance Criteria**
- Field format defined and documented in backlog header conventions
- Sprint planning engine updated to surface dependency chains
- Gate condition (20+ concurrent items with dependency-blocking evidence) verified before commencing

---

### BLG-GOV-71 — Governance engine complexity assessment (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Director of HR; PMO Lead
**Source:** IDEA-director-of-hr-20260525-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036; terminal 3-cycle disposition)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Audit overall score drops below 70 OR a step-skip event is formally documented in an audit report.

**Problem**
Governance engine prompts have grown complex over 33 cycles. Without periodic complexity assessment, latent process friction accumulates invisibly. This assessment would identify steps that rarely trigger, candidates for simplification, and produce a governance simplification roadmap for meta-review.

**Scope**
- For each governance engine prompt: count steps, hard gates, and write operations
- Identify steps with documented "never triggered" patterns from lessons_learnt.md history
- Propose candidates for simplification, consolidation, or removal

**Acceptance Criteria**
- Per-engine complexity metrics documented
- Simplification candidates enumerated with rationale
- Gate condition verified before commencing

---

### BLG-GOV-73 — Scheduled rebalance cadence review
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260601-02 + IDEA-challenger-20260601-02 (merged) — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Advance at next meta-review cycle (rebalance_cycles_since_meta_review ≥ 3).

**Problem**
10+ scheduled rebalances since 2026-03-24. CPS stable at 1.15. Multiple consecutive scheduled rebalances have had empty Now horizons with no items advancing. The Challenger raised the concern that running full governance process when no strategic decision is pending may produce overhead without proportional value.

**Scope**
- Review scheduled rebalances since last meta-review for value produced (items advanced, horizon movements, CPS changes)
- Assess whether a lightweight mode for no-change-expected cycles could reduce overhead
- Produce recommendation: maintain cadence or propose modification; present at next meta-review

**Acceptance Criteria**
- Value analysis of recent scheduled rebalances documented
- Recommendation produced and presented at next meta-review
- Gate condition (cycles_since_meta_review ≥ 3) verified before commencing

---

### BLG-GOV-74 — AI feature usage quarterly review (BLG-GOV-63 mandate)
**Priority:** P2 (Medium)
**Type:** Governance / Compliance
**Owner:** AI Compliance & Governance Officer; PMO Lead
**Source:** IDEA-ai-compliance-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036; fulfills BLG-GOV-63 mandate)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.10 or first cycle after 2026-08-29
**Gate date:** First review due 2026-08-29 (3 months after v4.0 AI feature ship 2026-05-29)

**Problem**
BLG-GOV-63 (shipped v4.2) requires a quarterly review of the claude_audit_log. First quarterly review due 2026-08-29. Without a backlog item it will be missed.

**Scope**
- Review claude_audit_log for the preceding quarter (v4.0–v4.8 window)
- Assess: total thesis generation requests, model version used, override_rate, cost per use
- Flag anomalies; document findings; file BLG items for any anomalies

**Acceptance Criteria**
- Quarterly audit log review completed; findings documented
- Anomalies (if any) filed as BLG items
- Next review date recorded (2026-11-29)

---

### BLG-OPS-51 — Add GET /analytics/strategy-version-comparison to api_performance_baseline.md (when implemented)
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner; API Contracts & Documentation Owner
**Source:** Post-ship closure 2026-06-01__release-v4.8 — endpoint coverage drift advisory (STEP 6)
**Effort:** S (~0.5 day)
**Provisional-Target:** SI-04 sprint (whenever GET /analytics/strategy-version-comparison is implemented)

**Problem**
v4.8 ST-07 added a placeholder entry for GET /analytics/strategy-version-comparison to openapi.yaml (pre-authored contract; not yet implemented). Once implemented, this endpoint will need p50/p95 latency measurement and an entry in docs/ops/api_performance_baseline.md.

**Scope**
- After SI-04 sprint implements the endpoint: run performance baseline measurement (p50/p95)
- Add measurement to docs/ops/api_performance_baseline.md

**Acceptance Criteria**
- GET /analytics/strategy-version-comparison present in api_performance_baseline.md with p50/p95 values
- Measurement conducted with ≥5 staging samples

---

### BLG-OPS-53 — Application log retention policy expansion (Supabase + claude_audit_log)
**Priority:** P3 (Low)
**Type:** Operations / Data Lifecycle
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** claude_audit_log table 6+ months old (~Nov 2026, since v4.0 ship 2026-05-22). BLG-OPS-31 (Render log retention policy) shipped v4.7; this extends scope to Supabase query logs and claude_audit_log.

**Problem**
BLG-OPS-31 defined Render log retention. claude_audit_log (shipped v4.0) and Supabase query logs have no defined retention policy. As audit log volume grows, query performance and storage cost may degrade without archiving strategy.

**Scope**
- Define retention period for claude_audit_log (e.g., 12 months rolling)
- Define Supabase query log retention consistent with data privacy obligations
- Define archiving trigger (log volume threshold or time-based)
- Document policy in docs/operations/

**Acceptance Criteria**
- Retention policy document produced covering claude_audit_log and Supabase query logs
- Archiving cadence defined
- Gate condition (6+ months of audit log data) verified before sprint planning

---

### BLG-OPS-54 — Add POST /digest/si05/send to api_performance_baseline.md
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner; PMO Lead
**Source:** Post-ship closure 2026-06-21__release-v5.1 — endpoint drift check (STEP 6)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** Unscheduled (pending live environment access)
**Scope revision (I&O Owner, 2026-06-22):** Standard external HTTP measurement is not viable for this endpoint — it blocks on the Telegram Bot API and timed out at 45s in the §19 baseline run. Revised approach: (1) Render internal log duration (server-side p50/p95), (2) weekly delivery success rate from `si05_digest_log`, (3) Telegram API timeout flag if request duration > 30s. See ST-11 staging evidence (docs/testing/staging_latency_review_ST-11.md).

**Problem**
`POST /digest/si05/send` was added to `docs/reference/openapi.yaml` in v5.1 (ST-01, EPIC-01). This endpoint is not present in `docs/ops/api_performance_baseline.md`. Standard external HTTP measurement is not viable (Telegram API timeout — excluded from §19 standard run). A Render internal log-based measurement approach is required.

**Scope**
- Add `POST /digest/si05/send` to `docs/ops/api_performance_baseline.md` using Render internal log duration (server-side), not external HTTP timing
- Extract p50/p95 from Render production logs for the dispatch endpoint
- Record weekly delivery success rate from `si05_digest_log` as the primary health metric

**Acceptance Criteria**
- POST /digest/si05/send present in api_performance_baseline.md with Render internal log-based measurements recorded
- Measurement methodology note added explaining why standard external HTTP timing does not apply

---

### BLG-GOV-84 — Arc 6 gate revision and threshold assessment
**Priority:** P3 (Low)
**Type:** Governance / Product Planning
**Owner:** Product Owner; Challenger; Strategy Rules & System Intent Owner
**Source:** IDEA-product-owner-20260527-02 + IDEA-challenger-20260527-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 combined disposition)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 50 closed trades (trajectory approaching) — at current ~1–2 trades/month, this is approximately 2026-Q4/2027.

**Problem**
PS-01 (Edge Analysis Dashboard) gate requires 100+ trades with plans and lifecycle data. At current trade frequency (1–2 trades/month), this gate takes 5–8 years to clear. The Challenger has raised (twice) that a meaningful edge analysis may be achievable with 20–30 closed trades with explicit statistical caveats. The Product Owner's Arc 6 minimum viable entry assessment (also raised twice) asks whether the gate calibration is appropriate. Both ideas address the same question: is the 100-trade threshold right? A formal assessment when trade count approaches 50 is the appropriate trigger.

**Scope**
- Formal assessment: at ≥50 closed trades, evaluate whether PS-01 can yield meaningful signal with available history (20–30 qualifying trades as a subset)
- Assess: what statistical confidence is achievable at 30 vs 50 vs 100 trades? Are explicit caveats sufficient to communicate limited confidence?
- Challenge the threshold: if PO decides 30–50 trades is sufficient with caveats, recommend gate revision; document decision in decision_log.md
- §13 check: any gate revision must remain within the "deterministic historical analysis" framework; no predictive claims

**Acceptance Criteria**
- Assessment document produced when ≥50 closed trades confirmed
- Threshold recommendation made (maintain 100-trade gate OR revise with documented caveats)
- PO + Challenger + Strategy Rules Owner sign-off on recommendation
- If gate revised: decision_log.md updated; PS-01 roadmap section updated
- Gate condition (≥50 closed trades approaching) verified before commencing

---

### BLG-GOV-85 — Arc 6 §13 pre-assessment boundary document
**Priority:** P3 (Low)
**Type:** Governance / §13 Compliance Pre-work
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260527-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 disposition)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 6 release planning trigger (first sprint planning cycle that includes a PS-01 through PS-05 story).

**Problem**
Arc 6 features (PS-01 through PS-05) are roadmapped with informal §13 compliance notes ("deterministic simulation, §13 COMPLIANT"; "statistical observation, not prediction"). Before Arc 6 sprint planning seals, a formal §13 pre-assessment must consolidate binding conditions for each feature — as was done for SI-01 (8 conditions), IT-06 (4 conditions), SI-04 (6 conditions). PS-03 already has a formal §13 PASS assessment (10 conditions, v4.6). PS-01, PS-02, PS-04, PS-05 need similar pre-assessment documents.

**Scope**
- Formal §13 pre-assessment for PS-01, PS-02, PS-04, PS-05 (PS-03 already complete)
- Each assessment confirms: deterministic calculation only, display-only output, no automated recommendations, no ML/prediction components
- Binding conditions documented per the SI-01/IT-06 pattern
- Strategy Rules & System Intent Owner sign-off required on each assessment

**Acceptance Criteria**
- §13 assessment documents produced for PS-01, PS-02, PS-04, PS-05
- Binding conditions documented for each PASS determination
- Gate condition (Arc 6 release planning trigger) verified before commencing

---

### BLG-GOV-90 — Claude model deprecation monitoring procedure (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038); consolidates BLG-GOV-239 — same "track Claude model deprecation on a defined schedule" capability, independently re-proposed as a standalone calendar at the 2026-07-16 idea-intake cycle without cross-reference to this existing item — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-GOV-74 first quarterly AI feature review completes (due 2026-08-29). Consolidate this procedure definition with the BLG-GOV-74 review action.

**Problem**
BLG-GOV-64 pins the model to claude-3-5-sonnet. Anthropic publishes model deprecation notices. No formal procedure exists for checking deprecation notices on a schedule and triggering a governed sprint story to update the pinned model. BLG-GOV-74 (quarterly AI review, first due 2026-08-29) is the natural integration point for a standard procedure.

**Scope**
- Define quarterly deprecation check procedure: check Anthropic model lifecycle page, compare against pinned model in BLG-GOV-64 policy
- Define trigger: if deprecation notice issued → file P1 sprint story to update pinned model
- Document procedure in docs/governance/ai_model_policy.md or equivalent

**Acceptance Criteria**
- Deprecation monitoring procedure defined and documented
- Procedure integrated with BLG-GOV-74 quarterly review cadence
- Gate condition (BLG-GOV-74 first review complete) verified before sprint planning

---

### BLG-GOV-91 — SI-04 strategy history access security review
**Priority:** P2 (Medium)
**Type:** Governance / Security Review
**Owner:** Cybersecurity & Trust Lead; Strategy Rules & System Intent Owner
**Source:** IDEA-cybersecurity-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 (binding conditions doc) shipped v5.0 — SI-04 remains in Later horizon; gate triggers when SI-04 enters sprint planning.

**Problem**
SI-04 (strategy version comparison) will access historical strategy_rules.md content and link it to trade data. This creates a data access pattern not present in SI-01 through SI-03: querying historical document versions alongside personal trade records. A security pre-assessment confirms whether this pattern introduces any data pattern or access control concerns before sprint planning.

**Scope**
- Assess data access pattern: historical strategy content + trade data linkage
- Determine if any additional access controls or audit logging are required
- Document as security review record per BLG-GOV-31 (security review pattern)
- Cybersecurity & Trust Lead sign-off

**Acceptance Criteria**
- Security review record produced covering SI-04 data access pattern
- PASS or REQUIRES_MITIGATIONS determination with evidence
- Cybersecurity & Trust Lead sign-off recorded
- Gate condition verified before sprint planning

---

### BLG-GOV-95 — strategy_rules.md annual parameter review schedule (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039); consolidates BLG-GOV-122, BLG-GOV-187 — the same "§11 production parameter review against live trading data" capability was independently re-proposed across two later idea-intake cycles (2026-06-10 and 2026-07-08) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-29 (trade plan AI audit log, P3, gate-conditional) deprioritised.

**Gate criteria:** Whichever comes first: ≥ 30 closed trades with ATR-based stop exits in production (sufficient data density to assess parameter appropriateness), OR 12 months elapsed since parameters were last reviewed, OR the annual review cadence date if neither condition has fired sooner.

**Problem**
strategy_rules.md §11 defines production parameters (5× initial ATR, 2× profitable ATR, 10-day grace period, regime gate thresholds). These have never been reviewed against live trading performance data — the system has run on its original parameter settings since inception (last validated at v5.3, BLG-GOV-104, not against realised outcomes). §12.3 requires documented rationale for any parameter change, but there is no scheduled review mechanism to surface whether changes are warranted.

**Scope**
- Define annual parameter review process: PMO Lead adds review to the next roadmap rebalance after the gate clears
- Review actual trading behaviour over the review window against each parameter's assumptions; identify any divergence between documented parameters and actual practice
- Review scope: compare actual trade outcomes against parameter-predicted outcomes for each parameter (does 5× ATR give sufficient breathing room? does 2× ATR lock in enough gain on average?)
- Output: parameter review report; PO + Strategy Rules owner decision: maintain, adjust (with §12.3 rationale), or schedule future review
- If parameters adjusted: follow §12.3 change control (version increment, rationale, consistency across backtests)

**Acceptance Criteria**
- Parameter review process document produced
- Gate condition (≥30 closed trades with stops) verified before review commences
- Product Owner and Strategy Rules & System Intent Owner sign-off on review findings
- If parameters adjusted: strategy_rules.md version increment with §12.3-compliant rationale

---

### BLG-GOV-102 — Arc completion velocity scorecard (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Product Planning Reference
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-product-owner-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-85 (Arc 6 §13 boundary document, P3, gate-conditional) deprioritised.

**Gate criteria:** Arc 5 fully complete (all five Arc 5 features: SI-01 ✅, SI-03 ✅, SI-05 Phase 1 ✅, SI-02 frontend, SI-04 — all shipped).

**Problem**
With 6 arcs spanning v2.9–v4.0+, there is no single reference document showing arc-level completion status: which arcs are done, which are in progress, which features remain, and what gate conditions are outstanding. As the project moves from Arc 5 toward Arc 6, assembling this picture from multiple sections of current_roadmap.md is time-consuming at each release planning session.

**Scope**
- One-page arc completion scorecard: for each of the 6 arcs, list (a) arc status (Complete/In Progress/Planned), (b) features shipped, (c) features remaining, (d) gate conditions outstanding, (e) earliest realistic activation date
- Filed in docs/product/ or claude/roadmap/
- Updated at each major arc milestone; not a living document requiring cycle-by-cycle updates

**Acceptance Criteria**
- Arc completion scorecard document produced covering all 6 arcs
- Gate condition (Arc 5 fully complete) verified before authoring (ensures Arc 5 data is final)
- Product Owner sign-off

---

### BLG-GOV-103 — Staged verification sprint tracking worksheet (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Process Tool
**Owner:** Director of Quality; PMO Lead
**Source:** IDEA-pmo-lead-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1 hour)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-90 (Claude model deprecation monitoring procedure, P2, gate-conditional) deprioritised.

**Gate criteria:** BLG-GOV-89 (staged verification sprint protocol, shipped v5.1) used 2+ times in practice. First use: v5.1 staged ACs; second use: this staged verification sprint (SI-05 Phase 1 deferred ACs). Gate clears after the v5.1 staged verification sprint is completed.

**Problem**
BLG-GOV-89 (staged verification sprint protocol) defines the pattern. After 2+ uses, a companion tracking worksheet — a simple checklist capturing: which releases have deferred ACs, which ACs per release, their status (pending/verified/signed-off) — would reduce coordination overhead when multiple staged ACs accumulate across releases.

**Scope**
- Produce a single-page tracking worksheet template (Markdown table) for staged verification sprints: columns = Release, AC ID, Description, Status, Evidence, Sign-off Date
- Template filed in docs/operations/ alongside BLG-GOV-89 protocol
- Reviewed by Director of Quality and PMO Lead

**Acceptance Criteria**
- Worksheet template produced and filed
- Gate condition (BLG-GOV-89 used 2+ times) verified before authoring
- Director of Quality and PMO Lead sign-off

---

### BLG-GOV-105 — Arc 6 PS-03 Monte Carlo §13 threshold pre-assessment — ✅ CLOSED (confirmed duplicate, 2026-07-12)
**Priority:** P2 (Medium)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (before Arc 6 moves from Later to Next)
**Displacement:** BLG-GOV-111 (v5.3 design gate pre-assessment, lower-P) deprioritised.

**Problem**
Arc 6 PS-03 (Monte Carlo simulation) requires a §13 review before sprint planning. The core §13 question — "is Monte Carlo simulation deterministic or predictive?" — can be answered definitively now without knowing implementation details. A pre-assessment scoped to this threshold question de-risks Arc 6 sprint planning entry.

**Scope**
- Assess whether Monte Carlo simulation as described in current_roadmap.md §5 (PS-03 notes) is deterministic (replaying own trade distribution) or predictive (forecasting future outcomes)
- Determine: does PS-03 engage the §13 boundary "Not an ML-based prediction system"?
- Produce a one-page §13 threshold assessment; if PASS (deterministic), note that binding conditions will be defined at full §13 review when Arc 6 moves to Next
- Note: scope is threshold question only — NOT a full §13 review with binding conditions

**Acceptance Criteria**
- §13 threshold assessment produced for PS-03 (deterministic vs predictive question answered)
- PASS/FAIL on the threshold question documented
- Strategy Rules & System Intent Owner sign-off

**Possible duplicate — flagged 2026-07-10 (backlog consistency audit, not yet dispositioned):** This item's threshold question — "is Monte Carlo simulation deterministic or predictive, does PS-03 engage the §13 boundary" — appears to already be answered by `BLG-GOV-45` ("Arc 6 Monte Carlo §13 pre-assessment"), which shipped in v4.6 (2026-05-31, ST-18): PASS, 10 binding conditions, decision doc filed at `docs/product/decisions/arc6_ps03_section13_preassessment.md` (confirmed on disk). This item may have been filed without visibility into that prior work. Not closed here — requires Strategy Rules & System Intent Owner confirmation that BLG-GOV-45 fully supersedes this item before disposition as duplicate/pre-met.

**Confirmed and closed 2026-07-12 (roadmap rebalance 2026-07-12__scheduled, Strategy Rules & System Intent Owner):** Verified `docs/product/decisions/arc6_ps03_section13_preassessment.md` directly — it answers this item's exact threshold question (deterministic vs predictive) for the same feature (PS-03), with a full PASS determination and 10 binding conditions, superseding this item's narrower scope entirely. `BLG-GOV-45` fully supersedes this item. Closed as confirmed duplicate/pre-met — resolves `IDEA-head-of-specs-20260712-01` and `BLG-GOV-202` (see below).

---

### BLG-GOV-119 — Arc 5 delivered value retrospective (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Strategic Review
**Owner:** Product Owner; Strategy Rules & System Intent Owner
**Source:** IDEA-challenger-20260610-01 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** SI-04 (strategy version comparison) AND SI-05 Phase 2 both shipped

**Problem**
Arc 5 is functionally near-complete (SI-01/02/03 shipped; SI-04 pre-planned; SI-05 Phase 1 live). Before committing to Arc 6, a retrospective against the original Arc 5 end-state intent would confirm whether the arc is delivering its stated purpose: "making every deviation visible, deliberate, and recorded."

**Scope**
- Review Arc 5 end-state description against delivered features
- Assess whether SI-01/02/03/05 collectively achieve the stated purpose
- Produce a 1-page retrospective document; note gaps or intent drift

**Acceptance Criteria**
- Retrospective document produced and filed
- Gap list (if any) filed as backlog items
- Product Owner + Strategy Rules & System Intent Owner sign-off
- Gate: SI-04 + SI-05 Phase 2 both shipped

---

### BLG-GOV-121 — SI-05 Phase 2 §13 pre-clearance document (gate-conditional)
**Priority:** P2 (Medium)
**Type:** Governance / Strategy Compliance
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260610-02 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** 2026-07-04 SI-05 effectiveness review output (BLG-GOV-113) complete AND Phase 2 activation decision made

**Problem**
SI-05 Phase 2 integrates drift signals (SI-02) with the Telegram digest. Before Phase 2 activates, a targeted §13 review should confirm that incorporating drift signals into an automated notification remains compliant with the "not an automated trading system" and "human-in-the-loop" principles. Phase 1 cleared §13 (notification of compliance scores + red flags). Phase 2 adds drift-signal interpretation — this boundary warrants formal pre-clearance.

**Scope**
- Extend the SI-05 Phase 1 §13 review framework to Phase 2 scope
- Confirm: drift signal summary in digest is informational, not prescriptive; no automated action triggered
- Document binding conditions for Phase 2 operation (analogous to IT-06 §13 conditions)

**Acceptance Criteria**
- §13 pre-clearance document produced and filed
- Strategy Rules & System Intent Owner sign-off
- Gate condition verified before Phase 2 sprint planning

---

### BLG-GOV-124 — SC-02: Remove RESUME PRECHECK mutation detection block from release_planning_prompt.md
**Priority:** P3 (Low)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-02
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled (governance sprint)

**Scope**
The RESUME PRECHECK mutation detection block in `release_planning_prompt.md` (~80 lines, lines 417–510) handles interrupted multi-session runs and assumption invalidation. This path has never been exercised in 100% of recorded v4.x–v5.x cycles. The lightweight state.json resume rule (7 lines) provides sufficient resumability for the observed failure mode. Remove the invalidation map and efficiency policy block; retain the state.json check. Requires dry-run validation pass.

**Implementation constraint (Head of Specs Team sign-off GCA-2026-06-17):** The Terminal State Guard ("Published Is Immutable") and State File Immutability Rule hard gates within the RESUME PRECHECK block must be extracted and retained outside the block before the mutation detection/invalidation map machinery is removed. The implementing story must explicitly scope the deletion and confirm these two gates survive.

**Acceptance Criteria**
- RESUME PRECHECK mutation detection/invalidation map block removed (mutation-detection portion only)
- Terminal State Guard and State File Immutability Rule hard gates extracted and retained in the prompt body
- State.json resume rule retained
- Dry-run validation pass confirming no functional regression
- Version bump + changelog entry
- Head of Specs Team sign-off

---

### BLG-FE-72 — Arc 4 PO-02 journal pattern UX spec (gate-conditional)
**Priority:** P3 (Low)
**Type:** Frontend & UX / Specification
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260608-02 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-043)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning confirmed imminent — PMO Lead confirmation required before commissioning this work

**Problem**
PO-02 (Journal Pattern Recognition) requires displaying cross-entry AI analysis results: recurring themes, emotional patterns, setup types, conditions present at winning vs losing entries. No UX specification exists for how this data should be presented. Before PO-02 enters sprint planning (gate: 6+ months AI journals, ~Oct 2026), a UX spec should be prepared to enable accurate scope definition at sprint planning.

**Scope**
- Define the display patterns for journal theme analysis (list view? heatmap? timeline?)
- Specify how patterns are surfaced: by entry count, by theme frequency, by outcome correlation
- Define empty state and gate-not-met state (< 6 months of journals)
- Produce a canonical frontend spec for the Journal Pattern Recognition UI component

**Acceptance Criteria**
- Frontend spec document produced: data display patterns, empty states, component architecture
- Spec reviewed and signed off by Head of UX & Design and Frontend Specs & UX Documentation Owner
- Gate: PMO Lead confirms PO-02 sprint planning is imminent before this story begins

---

---

---

### BLG-SPEC-56 — Arc 4 API contract pre-authoring (PO-02/03/04)
**Priority:** P3 (Low)
**Type:** Spec / Pre-authoring
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
PO-02 (journal pattern recognition), PO-03 (behavioural error taxonomy), and PO-04 (reflection/outcome correlation) are currently gate-blocked (~2026-10). However, the API contract surface for these features can be pre-authored now, reducing execution risk and spec bottlenecks when the gate clears. Pre-authoring allows the Specs team to identify ambiguities, surface §13 questions, and establish endpoint naming conventions before sprint planning pressure exists.

**Scope**
- Draft API contract stub files for PO-02, PO-03, PO-04 feature endpoints in `docs/specs/api_contracts/`
- Flag any §13 boundary questions for BLG-SPEC-35 (§13 pre-assessment, P1, active)
- No implementation; contract stubs only

**Acceptance Criteria**
- Stub contract files exist for PO-02, PO-03, PO-04 endpoint groups in `docs/specs/api_contracts/`
- Each stub includes at minimum: endpoint path, HTTP method, brief description, key request/response fields
- BLG-SPEC-35 §13 pre-assessment reviewed or updated if new boundary questions arise

---

### BLG-SPEC-57 — Data model v3 pre-definition for Arc 4 journal intelligence
**Priority:** P3 (Low)
**Type:** Spec / Pre-authoring
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260619-02 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
Arc 4 journal intelligence (PO-02/03/04) will require data model changes. Pre-defining the schema additions now (while the architecture is in working memory post-Arc 3 delivery) reduces execution risk and produces a migration plan that can be reviewed before sprint planning pressure exists.

**Scope**
- Define data model additions for PO-02/03/04 features (new tables or columns for pattern recognition, error taxonomy, outcome correlation)
- Document as a pre-definition document in `docs/specs/` or `docs/data_models/`
- No migration SQL; schema design only

**Acceptance Criteria**
- Data model pre-definition document produced covering Arc 4 schema additions
- BLG-SPEC-56 Arc 4 API contracts reference the pre-defined model where applicable
- Reviewed by Head of Specs Team and Infrastructure & Operations Owner

---

---

---

---

---

### BLG-QA-59 — Arc 4 E2E test strategy pre-design (PO-02/03/04)
**Priority:** P3 (Low)
**Type:** Quality Assurance / Pre-design
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
Arc 4 AI-driven features (PO-02/03/04) introduce Playwright test challenges not present in current arcs: AI response non-determinism, journal pattern recognition latency, cost implications of running AI calls in CI. Pre-designing the test strategy before sprint planning avoids last-minute patching of the CI pipeline during delivery.

**Scope**
- Define Playwright test strategy for Arc 4 features: which ACs require Playwright vs unit tests vs staging-only verification
- Define mocking approach for AI API calls in CI (extend existing mock harness)
- Document in `docs/specs/qa/` or `docs/operations/`

**Acceptance Criteria**
- Arc 4 E2E test strategy document produced
- Mocking approach for PO-02/03/04 AI calls defined and consistent with existing BLG-QA-37 Playwright mock strategy
- Reviewed by Director of Quality

---

---

### BLG-OPS-72 — AI API cost model for Arc 4 journal intelligence features
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled (before Arc 4 sprint planning)

**Problem**
PO-02 (journal pattern recognition) and PO-03/04 will call the Anthropic or Gemini API for AI summarisation and pattern analysis. Current AI cost modelling (BLG-OPS-65, completed v5.6) covers the thesis generation feature only. Arc 4 AI features will process trade journal entries in volume — potentially 1 AI call per journal entry per user per week. Without a cost model, Arc 4 budget impact is unknown and could exceed the current $0.05–$0.15/month baseline significantly.

**Scope**
- Estimate API call volume for PO-02/03/04 features based on expected usage patterns
- Model monthly cost at current Anthropic/Gemini pricing tiers
- Identify cost controls (caching, batching, user limits) and their estimated savings
- Document as `docs/operations/arc4_ai_cost_model.md`

**Acceptance Criteria**
- Cost model document produced with estimated monthly AI API cost for Arc 4 features
- Cost controls identified and quantified
- Reviewed by FinOps & Resource Architect

---

### BLG-BE-37 — Database index audit for Arc 4 cross-table queries
**Priority:** P3 (Low)
**Type:** Backend Engineering / Performance
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled (before Arc 4 sprint planning)

**Problem**
Arc 4 (PO-02/03/04) will introduce cross-table queries joining trade_plans, red_flag_events, arc5_compliance_scores, and potentially new journal tables. The current index strategy was designed for Arc 1–3 query patterns. Without an audit, Arc 4 sprint delivery may encounter unexpected latency regressions on production Supabase once real data volumes are involved.

**Scope**
- Review current index coverage on trade_plans, red_flag_events, arc5_compliance_scores, ai_journal_summaries tables
- Model likely Arc 4 query patterns based on BLG-SPEC-56 pre-authored contracts
- Identify missing indexes; file BLG-OPS or BLG-BE items for each gap discovered
- Document in `docs/operations/` or `docs/data_models/`

**Acceptance Criteria**
- Index audit document produced covering Arc 4 query patterns
- Any missing indexes produce separate BLG items before sign-off
- Reviewed by Infrastructure & Operations Owner

---

---

### BLG-GOV-137 — API contract version tagging for all api_contracts documents
**Priority:** P3 (Low)
**Type:** Governance Process / Spec Quality
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Source:** IDEA-head-of-specs-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Tooling assessment confirming version tagging adds drift detection value not already covered by `quality_gate.yml` OpenAPI validation.

**Problem**
API contract documents in `docs/specs/api_contracts/` do not carry a version field. When a contract is amended (endpoint added, field type changed), there is no audit trail of which version was in force when a sprint was planned. Version tagging creates a lightweight reference that enables contract consumers to identify changes.

**Scope**
- Add `version:` field to each api_contracts document (start at v1.0 for all existing docs)
- Define version bump rules: patch for additive changes, minor for breaking changes
- Update checklist for new endpoint authoring to include version bump step

**Acceptance Criteria**
- All api_contracts documents carry a `version:` field
- Version bump rules documented
- Gate condition verified before sprint planning

---

### BLG-GOV-138 — Sprint velocity trend alert in run_manifest (rolling 3-cycle drop)
**Priority:** P3 (Low)
**Type:** Governance Process / Metrics
**Owner:** PMO Lead; Infrastructure & Operations Owner
**Source:** IDEA-pmo-lead-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** velocity_metrics.md path discrepancy resolved (file currently at `claude/cycles/velocity_metrics.md` instead of `claude/roadmap/velocity_metrics.md` — see DL-057 friction items).

**Problem**
The roadmap_prompt.md reads velocity_metrics.md but does not auto-surface a warning when the rolling 3-cycle velocity falls below 0.90. PMO must manually compare values and raise the concern. An explicit alert rule in the run_manifest generation step ensures degrading velocity is visible without manual tracking.

**Scope**
- Add rule to roadmap_prompt.md STEP 1.1: if rolling 3-cycle average velocity < 0.90, surface "Velocity Trend Advisory" in run_manifest header
- Rule documents the threshold, current value, and whether the advisory is advisory or hard gate

**Acceptance Criteria**
- Rule added to roadmap_prompt.md per §6 governance checklist (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry)
- Gate condition (velocity_metrics.md path resolved) verified before sprint planning

---

### BLG-GOV-139 — Regression impact analysis at sprint planning
**Priority:** P3 (Low)
**Type:** Governance Process / Quality
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Tooling approach identified — cross-reference methodology between changed files and Playwright coverage map assessed (automated script vs manual checklist approach).

**Problem**
When sprint planning seals scope, there is no step to cross-reference the changed files against existing Playwright coverage. A regression could be introduced in a file that has Playwright coverage but whose coverage is not triggered by the specific code path being changed. A lightweight impact analysis would surface this risk at planning time.

**Scope**
- Define methodology: compare sprint story file scope against `tests/e2e/` coverage map
- Produce a "coverage gap report" template: stories × files × test coverage status
- Integrate as an advisory step in sprint_planning_prompt.md STEP 3 or STEP 4

**Acceptance Criteria**
- Methodology document produced; approach decision (automated vs manual) recorded
- Gate condition verified before sprint planning entry
- If integrated into sprint_planning_prompt.md: all §6 governance checklist steps completed

---

### BLG-GOV-140 — AI chat advisory §13 quarterly self-audit checklist
**Priority:** P2 (Medium)
**Type:** Governance Process / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner; AI Compliance & Governance Officer
**Source:** IDEA-strategy-owner-20260626-02 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Gate criteria:** First review due 2026-09-24 (90 days post-v6.2 ship 2026-06-25). Quarterly cadence thereafter.

**Problem**
v6.2 AI chat advisor and daily briefing are now live. §13 requires AI advisory outputs to remain advisory-only and not cross into automated decision-making. Periodic self-audit confirms this boundary is maintained as prompts and response handling evolve. Without a scheduled review, §13 compliance depends on individual vigilance rather than a governed cadence.

**Scope**
- Author §13 self-audit checklist document covering: output advisory language confirmation, no-automated-action verification, disclaimer visibility check, prompt injection risk review
- Schedule first review 2026-09-24; quarterly cadence thereafter
- Owner: Strategy Rules & System Intent Owner; co-reviewer: AI Compliance & Governance Officer

**Acceptance Criteria**
- Checklist document produced and filed
- First review date scheduled (2026-09-24)
- Product Owner and Strategy Rules owner sign-off

---

### BLG-GOV-141 — AI model output logging completeness audit
**Priority:** P2 (Medium)
**Type:** Governance Process / §13 Compliance
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Gate criteria:** Schedule within 90 days of v6.2 ship (by 2026-09-24).

**Problem**
v6.2 AI features (briefing, chat) should be logging all AI responses with model ID, prompt hash, and response length per AI governance policy. A completeness audit verifies the logging is in place and complete. Without this audit, log completeness is assumed rather than verified.

**Scope**
- Review claude_audit_log (or equivalent) for completeness: all POST /ai/daily-briefing and POST /ai/chat responses logged
- Verify fields: model_id, prompt_hash, response_length, timestamp
- If gaps found: file remediation items
- Schedule review by 2026-09-24

**Acceptance Criteria**
- Audit completed before 2026-09-24
- Logging completeness confirmed or gaps filed as remediation backlog items
- AI Compliance Officer sign-off

---

### BLG-GOV-142 — AI feature ROI assessment at 3-month post-ship mark
**Priority:** P2 (Medium)
**Type:** Governance Process / Value Assessment
**Owner:** Challenger; FinOps & Resource Architect; Product Owner
**Source:** IDEA-challenger-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** 2026-09-24 (90 days post-v6.2 ship). Assess: adoption rate of AI briefing and chat features, cost per use (Anthropic API cost / sessions), and whether usage data justifies continued investment.

**Problem**
v6.2 AI features have a per-use cost (Anthropic API call for each briefing and chat interaction). Without a formal ROI assessment at 3 months, there is no trigger to reconsider the feature investment if adoption is low or costs are disproportionate. The assessment is a formal governance checkpoint, not a presumption of cancellation.

**Scope**
- Assess: AI briefing usage rate (sessions/week), AI chat usage rate (questions/week), cost-per-session
- Compare against: value hypothesis from v6.2 release planning (trader intelligence value)
- Output: continue / sunset / modify recommendation with rationale
- Product Owner decision authority

**Acceptance Criteria**
- Assessment document produced by 2026-09-24
- Recommendation with rationale produced
- Product Owner decision recorded

---

### BLG-GOV-143 — OpenAPI completeness validation in CI (endpoint count reconciliation)
**Priority:** P3 (Low)
**Type:** Governance Process / CI
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Coverage methodology assessment confirming this complements (not duplicates) the existing OpenAPI drift detection in `quality_gate.yml`.

**Problem**
The existing `quality_gate.yml` drift detection checks `openapi.yaml` for new endpoints mentioned in contract files. BLG-GOV-134 adds advisory CI annotation. This item proposes a complementary check: validate that `openapi.yaml` covers 100% of routes in `backend/routers/`. These are distinct checks (forward vs backward coverage). Gate: confirm no duplication before implementing.

**Scope**
- Assess current coverage gap between quality_gate.yml (contract → openapi) and a hypothetical route scan (routes → openapi)
- If gap confirmed: author CI step to scan `backend/routers/` for `@router.[get|post|put|delete]` and cross-reference against openapi.yaml paths
- Gate condition assessment first; CI implementation only if gap confirmed

**Acceptance Criteria**
- Coverage gap assessment document produced
- If gap confirmed: CI step implemented as advisory (non-blocking, analogous to BLG-GOV-134)
- Gate condition verified before implementation

---

### BLG-GOV-144 — Agent role charter annual review schedule (consolidated)
**Priority:** P3 (Low)
**Type:** Governance Process / HR
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057); consolidates BLG-GOV-182, BLG-GOV-199, BLG-GOV-236 — the same "periodic role-charter freshness review" capability was independently re-proposed across three later idea-intake cycles (2026-07-08 through 2026-07-15) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Time-gated — first review due 2027-06-26 (annual cadence from first filing). A lighter-weight spot-check may also be run at any 10-cycle interval in the interim (per the absorbed BLG-GOV-236 proposal), without waiting for the full annual date.

**Problem**
Agent role charter files (`claude/agents/*.md`) define role responsibilities and decision authorities. As the governance system evolves, role definitions may become stale — including drift against current tooling and practice (e.g. `gh` CLI usage, current write-scope conventions). Without a scheduled review cadence, charter drift accumulates silently. An annual review, with a lighter interim spot-check, ensures each role definition remains current.

**Scope**
- Author an annual review procedure for all `claude/agents/*.md` charter files
- Schedule first review: 2027-06-26
- Procedure: review each charter for accuracy and continued relevance to current tooling/practice; propose amendments through Head of Specs Team; record in prompt_change_log.md
- Optional lighter interim spot-check every 10 cycles, flagging any staleness found as a follow-up ahead of the next full annual review

**Acceptance Criteria**
- Annual review procedure documented
- First review date: 2027-06-26 recorded
- Director of HR sign-off

---

### BLG-GOV-145 — Database connection pool sizing review for AI endpoints
**Priority:** P3 (Low)
**Type:** Governance Process / Operations Assessment
**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Source:** IDEA-head-of-engineering-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** 30+ days AI endpoint usage observation post-v6.2 ship (by 2026-07-25). v6.2 AI endpoints make additional DB reads; pool sizing should be reviewed under real load.

**Problem**
v6.2 added POST /ai/daily-briefing and POST /ai/chat, both of which read from the database (portfolio state, trade history for context). Supavisor connection pool configuration was set before AI endpoints existed. Under sustained AI endpoint load, the pool may be undersized. A review at 30 days confirms the pool is sized correctly or identifies adjustment needed.

**Scope**
- Review current Supavisor pool configuration (connection count, timeout settings)
- Cross-reference with AI endpoint DB query volume (from logs or monitoring)
- Identify whether pool size adjustment is warranted
- Document findings; file implementation item if adjustment needed

**Acceptance Criteria**
- Pool configuration review document produced
- Findings: "no change needed" or specific adjustment filed as a separate item
- Gate condition (30+ days usage) verified before review commences

---

### BLG-GOV-149 — AI response caching evaluation for morning briefing
**Priority:** P3 (Low)
**Type:** Governance Process / Architecture Assessment
**Owner:** Backend Engineering Patterns Owner; FinOps & Resource Architect
**Source:** IDEA-backend-engineering-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
POST /ai/daily-briefing makes an Anthropic API call on every request. If the same briefing is requested multiple times in the same trading day, each call incurs API cost and latency. A caching evaluation assesses whether same-day caching is technically feasible and whether the staleness risk (briefing should reflect the day's market data) outweighs the cost benefit.

**Scope**
- Evaluate caching feasibility: cache key options (date, user, market open/close state), cache invalidation triggers
- Assess staleness risk: how often does market data change in a way that would materially change the briefing during a trading day?
- Produce evaluation document: recommend cache (with approach) or no-cache (with rationale)
- No implementation commitment; evaluation output only

**Acceptance Criteria**
- Evaluation document produced covering cache key design, staleness risk, and cost-benefit analysis
- Recommendation: cache / no-cache with rationale
- Backend Engineering Owner and FinOps sign-off

---

---

---

### BLG-QA-63 — Automated accessibility testing (axe-core) in Playwright CI
**Priority:** P3 (Low)
**Type:** QA / Accessibility
**Owner:** Director of Quality; Head of Frontend Engineering
**Source:** IDEA-director-of-quality-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate criteria:** Arc 5 fully complete (all SI features shipped) — accessibility testing added after frontend feature set stabilises

**Problem**
The Playwright E2E suite provides functional coverage but no accessibility validation. axe-core (via @axe-core/playwright) can be added to the existing Playwright setup to surface WCAG 2.1 AA violations in CI without blocking test runs.

**Scope**
- Install @axe-core/playwright
- Add a dedicated accessibility spec (tests/e2e/accessibility.spec.js) that visits each major page (Dashboard, Positions, Signals, Screener, Watchlist, Risk, Research, Reports, SystemStatus) and runs axe analysis
- Report violations as CI warnings (non-blocking initially); convert to hard failure after a clean baseline is established

**Acceptance Criteria**
- AC-01: axe-core runs on all major pages in CI (advisory, non-blocking)
- AC-02: Zero critical (level A) violations on any page at time of implementation
- AC-03: Violation report surfaced as CI annotation on PRs

---

---

---

### BLG-OPS-76 — Enhanced health check with external dependency verification
**Priority:** P3 (Low)
**Type:** Operations / Observability
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate criteria:** BLG-OPS-25 (automated staging smoke test) complete AND ≥3 external dependency failures observed in production logs

**Problem**
GET /health returns only internal service health (database connectivity, scheduler status). External dependency status (Alpaca API reachability, Anthropic API reachability, Yahoo Finance fallback) is not surfaced in the health check, making degraded-run detection reactive rather than proactive.

**Scope**
- Add optional `?extended=true` query param to GET /health
- Extended check: attempt lightweight connectivity test for each external dependency (Alpaca: GET /v2/clock; Anthropic: no-op; Yahoo Finance: HEAD check)
- Return dependency status map in health response
- No latency regression on default (non-extended) health check

**Acceptance Criteria**
- AC-01: GET /health?extended=true returns a `dependencies` object with status for each external dependency
- AC-02: GET /health (no param) remains unchanged in response shape and latency
- AC-03: Degraded dependency status visible in `/system-status` page

---

### BLG-OPS-77 — Data provider diversity risk assessment and failover strategy
**Priority:** P3 (Low)
**Type:** Operations / Risk
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** IDEA-challenger-20260619-01 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate criteria:** BLG-OPS-71 (system threat model) complete — data provider risk will be enumerated in the threat model

**Problem**
All market data (OHLCV, signals, news) is sourced exclusively from Alpaca and Yahoo Finance. No documented failover strategy exists for a scenario where either provider becomes unavailable for an extended period. The risk has been accepted at current scale but has not been formally assessed.

**Scope**
- Produce a data provider risk assessment document (docs/operations/data_provider_risk_assessment.md): enumerate current dependencies, failure modes, estimated impact per provider loss, and mitigation options
- Identify any quick-win failover paths (e.g. Yahoo Finance as sole fallback if Alpaca unavailable)
- Document accepted risk and conditions under which a more robust failover should be re-evaluated

**Acceptance Criteria**
- AC-01: data_provider_risk_assessment.md produced covering all active external data providers
- AC-02: Failure modes and impact documented per provider
- AC-03: Accepted risk statement signed off by Infrastructure & Operations Owner and FinOps & Resource Architect

---

---

---

---


### BLG-GOV-154 — API contract deprecation marker convention
**Priority:** P3 (Low)
**Type:** Governance / API Design
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260702-02 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** TBD
**Effort:** S (~0.5 day)

**Problem**
No formal process exists for marking an API contract's endpoint as deprecated once its backing implementation is retired. BLG-BE-40 (v6.4) removed a deprecated-table read path but the affected contract sections were updated ad hoc rather than via a defined convention.

**Scope**
- Define a `**Deprecated:**` marker convention for `## METHOD /path` headings in `docs/specs/api_contracts/`
- Document in the API contracts style guide / openapi.yaml preamble

**Acceptance Criteria**
- Deprecation marker convention documented
- Reviewed by Head of Specs Team

---

### BLG-GOV-156 — Base44 prompt template versioning
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥3 Base44 prompt draft revisions within a single release cycle (current iteration frequency does not warrant versioning overhead).

**Problem**
No versioning exists to track which version of the Base44 generation prompt produced each delivered component. At current low iteration frequency this is not yet a problem, but the gate defines a concrete trigger for when it would become one.

**Scope**
- Lightweight per-revision log (date, summary of change) appended to the Base44 prompt draft file
- No tooling required — a changelog section within the existing prompt file

**Acceptance Criteria**
- Changelog section added once gate condition is met
- Gate condition (≥3 revisions/cycle) verified before commencing

---

### BLG-GOV-160 — File SI-05 Phase 1 30-day effectiveness review record
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Product Owner; Infrastructure & Operations Owner; Director of Quality
**Source:** Scheduled 30-day SI-05 effectiveness review routine (BLG-GOV-96 / BLG-GOV-113) — 2026-07-04
**Effort:** XS (<1 hour)
**Provisional-Target:** Unscheduled

**Problem**
The SI-05 Phase 1 effectiveness review was due 2026-07-01 per BLG-GOV-113 protocol but has not been formally conducted or recorded. Criteria 1 (PO reads ≥4 of last 5 digests) and Criterion 2 (≥1 digest-triggered app action) require PO self-assessment; Criterion 3 (service delivered ≥4 of last 5 scheduled sends) requires a `si05_digest_log` query to confirm the June 22 and June 29 delivery windows. The formal review record must be filed before the Phase 2 revised review date of 2026-08-04.

**Scope**
- PO provides self-assessment for Criterion 1: number of last 5 digests reviewed
- PO provides self-assessment for Criterion 2: describes any digest-triggered app action in the 30-day period
- I&O Owner runs `si05_digest_log` health check (Option A) for June 22 and June 29 send windows
- PMO Lead records overall verdict (PROCEED / ITERATE / PAUSE) and Phase 2 activation decision
- Review record filed per BLG-GOV-113 §4 format in `claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md`

**Acceptance Criteria**
- Formal review record filed with all three criteria assessed (PASS / FAIL for each)
- `si05_digest_log` evidence for June 22 and June 29 sends recorded
- PO self-assessments for Criteria 1 and 2 attested in the record
- Phase 2 activation decision (PROCEED / ITERATE / PAUSE) recorded by Product Owner
- Director of Quality sign-off on evidence completeness recorded

---


### BLG-QA-70 — Signal correctness fix impact measurement
**Priority:** P3 (Low)
**Type:** QA / Data Audit
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-20260702-01 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** TBD
**Effort:** S (~0.5–1 day)

**Problem**
BLG-BE-40 (v6.4) fixed signal generation reading the deprecated `tickers` table instead of `ticker_universe`. No retrospective measurement exists of how many historical `suggested_shares` values were affected by the bug before the fix.

**Scope**
- Query historical signals generated before the BLG-BE-40 fix; identify count and magnitude of affected `suggested_shares` values
- Document findings — informational, no remediation implied unless a material discrepancy is found

**Acceptance Criteria**
- Impact measurement query run and findings documented
- Reviewed by Metrics Definitions & Analytics Owner and Product Owner

---

### BLG-QA-71 — Playwright fixture isolation tooling
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** First empirical Playwright fixture-isolation failure observed in CI (no such failure has occurred to date).

**Problem**
No test data fixtures or state-reset mechanism exists between Playwright runs. No empirical fixture-isolation failure has occurred — the gate exists to avoid building tooling for a problem not yet demonstrated.

**Scope**
- Fixture reset mechanism between Playwright test runs
- Applied once a real isolation failure is observed

**Acceptance Criteria**
- Fixture isolation tooling implemented once gate condition met
- Gate condition (demonstrated failure) verified before commencing

---

### BLG-SEC-09 — AI rate-limit bypass test
**Priority:** P2 (Medium)
**Type:** Security / Verification
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260702-02 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** v7.10
**Effort:** S (~1 day)

**Problem**
BLG-OPS-81 (v6.3) added per-endpoint AI rate limiting (10 req/min/IP daily-briefing; 30 req/min/IP chat). No verification has been done that these limits cannot be bypassed via IP rotation or header spoofing in the current deployment.

**Scope**
- Test rate-limit enforcement against IP-rotation and X-Forwarded-For header spoofing attempts
- Document findings; file a security fix item if a bypass is confirmed

**Acceptance Criteria**
- Bypass test performed against both rate-limited AI endpoints
- Findings documented; any confirmed bypass filed as a P1/P0 security item
- Cybersecurity & Trust Lead sign-off

---

### BLG-SPEC-62 — Open Positions panel spec backfill
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260702-01 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** TBD
**Effort:** S (~0.5 day)

**Problem**
BLG-FEAT-54 (Open Positions panel, v6.4) shipped with a UX spec (`docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md`) but no corresponding entry was backfilled into the canonical `docs/specs/frontend/pages/strategy_benchmark.md` page spec, leaving the page spec incomplete relative to what shipped.

**Scope**
- Backfill Panel 0 (Open Positions) into `docs/specs/frontend/pages/strategy_benchmark.md`
- Cross-reference the existing UX spec and API contract

**Acceptance Criteria**
- `strategy_benchmark.md` page spec includes Panel 0 documentation
- Reviewed by Frontend Specifications & UX Documentation Owner

---

### BLG-SPEC-63 — Spec coverage gap detection script design
**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Head of Specs Team completes a script-design scoping decision (static route diff vs frontend spec inventory approach).

**Problem**
No automated check compares frontend page specs against deployed routes to detect coverage gaps. The scoping approach (static diff vs inventory-based) has not yet been decided.

**Scope**
- Scope and select an implementation approach
- Build a lightweight script to flag routes with no corresponding spec file (or vice versa)

**Acceptance Criteria**
- Scoping decision recorded
- Script implemented and run at least once with findings documented

---

### BLG-SPEC-65 — AI interaction history data model
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same gate as BLG-FEAT-55 — §13 review opened and passed for chat persistence AND AI adoption window clears ~2026-07-25.

**Problem**
Companion spec item to BLG-FEAT-55 (chat persistence). §13-compliant schema design for persisting user chat sessions must not precede the boundary review itself.

**Scope**
- §13-compliant schema design, co-developed with BLG-FEAT-55
- No implementation ahead of the §13 review passing

**Acceptance Criteria**
- Schema spec produced only after §13 review passes
- Gate condition verified before commencing

---

### BLG-SPEC-66 — AI chat conversation persistence spec
**Priority:** P3 (Low)
**Type:** Spec Debt / Frontend Spec
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same §13 review gate as BLG-FEAT-55/BLG-SPEC-65.

**Problem**
Companion frontend spec item to BLG-FEAT-55/BLG-SPEC-65 — persisting and displaying chat session history. Authoring this spec ahead of the §13 boundary decision risks rework or discard.

**Scope**
- Frontend spec for session list and resume-conversation UX, authored only once the §13 gate clears

**Acceptance Criteria**
- Spec produced only after §13 review passes
- Gate condition verified before commencing

---

### BLG-OPS-84 — Annual data provider cost comparison review
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Annual cadence — first review due ≥2027-06-25.

**Problem**
No scheduled review compares current data provider (Yahoo Finance, Alpaca) costs against alternatives. Annual cadence is appropriate; the gate simply establishes when the first review is due.

**Scope**
- Cost/feature comparison of current vs alternative data providers
- Recommendation: retain or switch

**Acceptance Criteria**
- Review conducted and documented at gate date
- FinOps & Resource Architect sign-off

---

### BLG-OPS-85 — Compute cost trending by feature area
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-OPS-74 (Anthropic API cost logging) ships.

**Problem**
No view partitions Render dyno compute cost by feature area. Meaningful cost trending depends on the per-call cost logging BLG-OPS-74 will provide — building this ahead of that data source would have nothing to trend.

**Scope**
- Partition compute cost by feature area (AI endpoints, screener, core CRUD) once BLG-OPS-74 data is available

**Acceptance Criteria**
- Cost trending view implemented and populated
- Gate condition (BLG-OPS-74 shipped) verified before sprint planning

---

### BLG-FEAT-61 — Screener-to-watchlist promotion friction audit
**Priority:** P3 (Low)
**Type:** Product Feature / UX Research
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A user-reported friction signal on the DS-07 promotion flow, or an observed drop in promotion-to-watchlist conversion rate.

**Problem**
DS-07 (screener → watchlist promotion) has been unchanged since v3.0 with no reported usage issue. Auditing it now would be speculative.

**Scope**
- Review promotion flow usage once a friction signal exists
- Recommend UX changes if warranted

**Acceptance Criteria**
- Audit conducted and documented only after gate signal observed

---

### BLG-FEAT-62 — Trade plan template presets by setup type
**Priority:** P3 (Low)
**Type:** Product Feature
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥20 closed trades captured post-PT-04 (2026-06-23) with sufficient `setup_type` diversity to justify presets (at least 3 distinct setup types with ≥3 trades each).

**Problem**
PT-04 (Setup Quality Score) is live, but trade volume since its gate clearance is too low to know which setup-type presets would actually be useful.

**Scope**
- Analyse `setup_type` distribution once gate clears
- Design preset templates for the most common setup types

**Acceptance Criteria**
- Preset design only commences after gate condition confirmed

---

### BLG-GOV-171 — Spec staleness scan across owning code paths
**Priority:** P3 (Low)
**Type:** Governance / Spec Debt
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A staleness-threshold definition (e.g. "spec unedited N releases while its code path changed") is authored first — this item is the scan itself, not the threshold definition.

**Problem**
No demonstrated spec-drift incident motivates this yet, and no threshold exists to define "stale."

**Scope**
- Author a staleness threshold, then run a one-off scan of specs against their owning code paths

**Acceptance Criteria**
- Threshold defined before scan is run
- Scan report produced identifying any specs exceeding the threshold

---

### BLG-GOV-172 — Governance prompt cross-reference integrity check
**Priority:** P3 (Low)
**Type:** Governance
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — run at the next scheduled lifecycle audit (`run audit`, every 3 cycles) or upon discovery of a broken cross-reference, whichever comes first.

**Problem**
No evidence yet of a broken cross-reference between governance prompts, but none has been checked systematically either.

**Scope**
- Scan all `claude/system/*.md` cross-references for validity, bundled into the next scheduled `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-GOV-173 — Escalation SLA dashboard
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Open escalation volume grows to ≥3 concurrent open escalations (current baseline: 0) — below that, existing manual tracking is sufficient.

**Problem**
Escalation volume is currently zero; a dashboard has no data to justify its build cost yet.

**Scope**
- Build a simple SLA-tracking view once escalation volume justifies it

**Acceptance Criteria**
- Dashboard built only after gate condition confirmed

---

### BLG-QA-75 — Playwright flake-rate tracking (consolidated)
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled; consolidates BLG-QA-80 (flaky Playwright test tracker) and BLG-QA-87 (Playwright flake tracking log) — the same underlying capability was re-proposed across the 2026-07-08 and 2026-07-10 idea-intake cycles without cross-reference to this existing item — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** S (~1 day) for the lightweight quarantine list; CI-pipeline-integrated flake-rate tracking (gated, see below) is a larger follow-on effort
**Provisional-Target:** Unscheduled
**Gate criteria:** A lightweight quarantine list/log has no gate and can be built now (per BLG-QA-80/87's original proposal). Full CI-pipeline-integrated flake-rate tracking remains gated on the first demonstrated flaky-test incident (a test that fails intermittently without a code change) — building that fuller tooling ahead of any observed flakiness would be premature.

**Problem**
Occasionally-flaky Playwright tests are re-run ad hoc with no tracking of which tests flake, how often, or why. Intermittent CI failures are currently indistinguishable from confirmed defects in QA evidence logs, and there is no visibility into whether flake rate is worsening.

**Scope**
- Maintain a quarantine list / flake log now: test name, first-flagged date, flake count, whether a re-run passed, re-enable criteria
- Once a first flaky-test incident is confirmed: add flake-rate tracking to the CI pipeline itself (gated follow-on)

**Acceptance Criteria**
- Quarantine list / log created; any currently-known flaky test logged
- CI-pipeline flake-rate tracking built only after the gate condition (first flaky-test incident) is confirmed

---

### BLG-QA-76 — QA evidence cross-link audit
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — bundle into the next scheduled lifecycle audit, or run on discovery of a dangling DoQ claim.

**Problem**
No evidence yet of a dangling (unlinked/broken) DoQ sign-off claim, but none has been checked systematically.

**Scope**
- Scan `qa_evidence_*.md` files for DoQ claims lacking a valid evidence link, bundled with the next `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-OPS-88 — Render dyno right-sizing review
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Bundle with the existing scheduled 90-day AI cost review (due 2026-09-24) — no standalone signal yet indicates the current dyno tier is mismatched.

**Problem**
The 2 AI endpoints are only 8 days live as of this idea's submission; no cost/performance signal yet indicates a right-sizing need.

**Scope**
- Review dyno tier alongside the 2026-09-24 AI cost review

**Acceptance Criteria**
- Review conducted at or after the 2026-09-24 gate date

---

### BLG-OPS-89 — Anthropic API budget alert threshold calibration
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** The existing `POST /ai/check-daily-cost` alert (shipped v4.1) produces a first false positive or false negative.

**Problem**
The existing cost alert has not misfired since shipping; recalibrating its threshold now would be speculative.

**Scope**
- Recalibrate the alert threshold once a false positive/negative is observed

**Acceptance Criteria**
- Recalibration only performed after gate condition confirmed

---

### BLG-OPS-90 — Staging environment drift detector
**Priority:** P2 (Medium) — escalated from P3, 2026-07-28, roadmap rebalance `2026-07-28__scheduled` (gate cleared, see below)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** TBD
**Gate criteria:** ~~A second occurrence of a staging/production configuration drift incident (first occurrence: BLG-OPS-82, a one-off missing-deploy issue).~~ **Gate cleared 2026-07-28** — commit `e9c73f58` ("[GOVERNANCE] Fix stale What's New panel — trigger staging redeploy on changelog.md changes") is a confirmed second occurrence of the same drift class: a runtime-read file changed in the repo without triggering a staging redeploy (Render dashboard-only build-path filter invisible to repo grep), producing stale served content exactly as BLG-OPS-82 did. Identified via `IDEA-infra-ops-20260728-01` (IW-20260728-01); disposition: idea resolved directly by this gate-status update rather than filed as a separate backlog row (register Status → Promoted-Added).

**Problem**
BLG-OPS-82 was originally treated as a single one-off incident. A second, independently-caused instance of the same underlying pattern (deploy-path filters that are invisible to a repo-level search, so a runtime-read file's change doesn't trigger the redeploy a reviewer would expect) has now occurred, confirming this is a recurring drift class rather than a one-off.

**Scope**
- Build automated drift detection between staging and production config/build-path coverage, informed by both incidents (BLG-OPS-82: missing-deploy; this one: dashboard-only path filter)

**Acceptance Criteria**
- Tooling built and covers both confirmed incident shapes; Infrastructure & Operations Owner sign-off

---

### BLG-OPS-91 — Deploy rollback runbook dry-run
**Priority:** P3 (Low)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** After the next real production deploy that uses the BLG-OPS-80 rollback runbook.

**Problem**
The rollback runbook (BLG-OPS-80) is authored but has not yet been exercised against a real production deploy.

**Scope**
- Perform a dry-run (or live use) of the runbook at the next production deploy

**Acceptance Criteria**
- Dry-run performed and runbook gaps (if any) documented after the next deploy

---

### BLG-GOV-174 — Skill-Silo Alert historical trend chart
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** PMO Lead
**Source:** IDEA-challenger-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Adoption of a second Skill-Silo escalation tier (BLG-GOV-176a / companion idea IDEA-challenger-20260702-01, Advanced this cycle — see `cycle_record.md` STEP 5) — if a second tier is adopted, this chart becomes part of its supporting dashboard; if not adopted, defer indefinitely.

**Problem**
The underlying data already exists across `workforce_capacity.md` and `decision_log.md` cycle entries; a chart is a presentation nice-to-have, not new capability, and its value depends on whether a second escalation tier is adopted.

**Scope**
- Build a historical trend chart of the rolling Skill-Silo percentage, contingent on the companion escalation-tier decision

**Acceptance Criteria**
- Built only if the companion decision (STEP 5, this cycle) adopts a second tier

---

### BLG-SPEC-67 — OpenAPI example-response completeness sweep
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic documentation debt — bundle with the next scheduled lifecycle audit.

**Problem**
No evidence gaps in `openapi.yaml` example responses have caused an actual integration problem; this is opportunistic hygiene, not urgent.

**Scope**
- Sweep `docs/reference/openapi.yaml` for endpoints missing example responses, bundled with the next `run audit` pass

**Acceptance Criteria**
- Sweep performed alongside next lifecycle audit; gaps (if any) filed as backlog items

---

### BLG-GOV-175 — Base44 prompt draft changelog
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Base44 prompt draft revision frequency increases to a point where informal tracking becomes error-prone (e.g. ≥3 revisions to the same prompt draft within a single sprint).

**Problem**
Prompt revision frequency remains low; a formal changelog/versioning process is not yet warranted.

**Scope**
- Introduce a lightweight changelog for Base44 prompt drafts once revision frequency justifies it

**Acceptance Criteria**
- Changelog introduced only after gate condition confirmed

---

### BLG-BE-43 — Trade plan field usage audit
**Priority:** P3 (Low)
**Type:** Backend / Data
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Arc 4 PO-02 (Journal Pattern Recognition) design phase begins (gated to ~2026-10-20, 6+ months AI-summarised journal data).

**Problem**
This audit would directly inform Arc 4 PO-02/PO-03 design, but running it ahead of that design phase risks auditing fields that later change.

**Scope**
- Audit actual usage of trade plan fields once PO-02 design phase begins

**Acceptance Criteria**
- Audit conducted only after gate condition (PO-02 design phase start) confirmed

---

### BLG-BE-44 — Signal write-path schema consolidation
**Priority:** P3 (Low)
**Type:** Backend / Refactor
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-SEC-02's 3-path sanitisation fix (shipped v6.4) has run in production for ≥30 days with no incident (clears ~2026-08-01).

**Problem**
BLG-SEC-02 just shipped a 3-path sanitisation fix to the signal write path; consolidating that code now, before it has stabilised in production, risks compounding an unproven change with a refactor.

**Scope**
- Consolidate the 3 signal write paths into a single validated path once the sanitisation fix has proven stable

**Acceptance Criteria**
- Refactor only commences after gate condition (30-day stability window) confirmed

---

### BLG-GOV-176 — Facilitator workload note
**Priority:** P3 (Low)
**Type:** Governance / HR
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Facilitator workload is reported as a bottleneck in any cycle's lessons learnt or escalation record.

**Problem**
No signal currently indicates Facilitator workload is a bottleneck; formal tracking is not yet warranted.

**Scope**
- Produce a workload note/assessment once a bottleneck signal is reported

**Acceptance Criteria**
- Assessment produced only after gate condition confirmed

---

### BLG-FEAT-63 — P&L report AI narrative cost estimate
**Priority:** P3 (Low)
**Type:** Product Feature / FinOps
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same AI-adoption gate as BLG-FEAT-59 (AI-assisted monthly P&L narrative) — clears ~2026-07-25.

**Problem**
This cost estimate directly feeds BLG-FEAT-59, which is itself gated on the AI-adoption window; estimating cost ahead of that gate is premature.

**Scope**
- Produce a cost estimate for AI-generated P&L narrative once the adoption window clears

**Acceptance Criteria**
- Estimate produced only after gate condition confirmed

---

### BLG-BE-45 — Trade cost field completeness check
**Priority:** P3 (Low)
**Type:** Backend / Data Quality
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — bundle with the next scheduled lifecycle audit.

**Problem**
No evidence yet of missing `trade_costs` values; this is a data-quality hygiene check, not an urgent fix.

**Scope**
- Check completeness of `trade_costs` fields across closed trades, bundled with the next `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; gaps (if any) filed as backlog items

---

### BLG-QA-77 — Playwright suite runtime trend
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** CI suite runtime is reported as a bottleneck (e.g. blocking rapid iteration or exceeding a defined CI time budget).

**Problem**
CI suite runtime has not been reported as a bottleneck at the current spec-file count; trend tracking now would be premature.

**Scope**
- Add runtime trend tracking to CI once runtime is reported as a bottleneck

**Acceptance Criteria**
- Tracking added only after gate condition confirmed

---

### BLG-OPS-92 — Dependency update review
**Priority:** P2 (Medium)
**Type:** Operations / Security Hygiene
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A new CVE or deprecation warning surfaces on a project dependency, OR the next quarterly hygiene cadence (~2026-10-06, 3 months post v4.0 starlette remediation).

**Problem**
No known CVE or deprecation warning is currently outstanding since the v4.0 starlette remediation; a full review now would be opportunistic rather than urgent.

**Scope**
- Full dependency update review triggered by either a new CVE/deprecation signal or the quarterly cadence, whichever comes first

**Acceptance Criteria**
- Review conducted at or after the gate condition (signal or cadence date)

---

### BLG-FE-90 — Open Positions panel visual consistency check
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A visual inconsistency in the Open Positions panel (BLG-FEAT-54, shipped v6.4) is reported.

**Problem**
BLG-FEAT-54 shipped with Head of UX & Design input already incorporated at design-gate time; no visual inconsistency has been reported since.

**Scope**
- Review and correct any reported visual inconsistency once one surfaces

**Acceptance Criteria**
- Review conducted only after a specific inconsistency is reported

---

### BLG-SEC-10 — Security fix false-positive rate assessment
**Priority:** P2 (Medium)
**Type:** Security / QA
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A production observation window of ≥30 days post-BLG-SEC-02 ship (shipped v6.4, 2026-07-02; clears ~2026-08-01). Revisit alongside BLG-QA-70.

**Problem**
BLG-SEC-02's write-time validation just shipped; a false-positive rate cannot be meaningfully measured without a production observation window.

**Scope**
- Measure false-positive rate of BLG-SEC-02 validation once the observation window elapses, alongside BLG-QA-70

**Acceptance Criteria**
- Measurement conducted only after gate condition (30-day window) confirmed

---

### BLG-GOV-177 — DoQ sign-off audit spot-check
**Priority:** P3 (Low)
**Type:** Governance / QA
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A non-compliant DoQ sign-off is found, OR bundle with the next scheduled lifecycle audit.

**Problem**
Every recent cycle has shipped Verified with zero deviations; no evidence yet of a non-compliant DoQ sign-off.

**Scope**
- Spot-check DoQ sign-off compliance, bundled with the next `run audit` pass

**Acceptance Criteria**
- Spot-check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-QA-78 — Test data fixture staleness check
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A test failure is attributed to a stale test fixture.

**Problem**
No test failures have been attributed to stale fixtures since v6.4's signal/security changes; a staleness check now would be speculative.

**Scope**
- Check test data fixtures for staleness once a failure is attributed to one

**Acceptance Criteria**
- Check conducted only after gate condition confirmed

---

---

### BLG-BE-47 — Standardise pagination pattern across list endpoints (consolidated)
**Priority:** P2 (Medium)
**Type:** Backend / Code Quality
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled; consolidates BLG-BE-53, BLG-BE-64, BLG-BE-72 — the same capability was independently re-proposed across three idea-intake cycles (2026-07-10 through 2026-07-24) without cross-reference to this existing item or each other — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
List endpoints (trades, trade-plans, positions, signals, watchlist, journal, red-flag-journal) currently use at least 3 divergent pagination styles (offset/limit, cursor-based, page-number based) depending on when each was built, with no documented convention — increasing maintenance cost and inconsistent frontend handling.

**Scope**
- Audit all paginated endpoints (including trades, trade-plans, positions, signals, watchlist, journal, red-flag-journal); document current styles
- Define one canonical cursor-based pagination pattern in `backend_engineering_patterns.md`
- Extract a shared pagination helper/dependency for FastAPI routers
- Migrate endpoints opportunistically as they are touched — not a forced mass-migration or single big-bang migration

**Acceptance Criteria**
- Canonical pattern documented in `backend_engineering_patterns.md`
- Shared pagination helper exists, documented, with at least one existing endpoint migrated as a reference example
- At least the next 2 new/modified list endpoints follow the canonical pattern
- Not required to retrofit all existing endpoints in one pass

---

### BLG-BE-48 — Structured logging correlation-ID propagation across FastAPI request lifecycle
**Priority:** P3 (Low)
**Type:** Backend / Observability
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Log lines from a single request cannot currently be correlated across service boundaries (e.g. a signal-generation request that also calls the AI service) — debugging multi-step requests requires manual timestamp correlation.

**Scope**
- Add a request-scoped correlation ID (middleware-generated or accepted via header), included in all log lines emitted during that request

**Acceptance Criteria**
- Correlation ID present in logs for at least 2 representative multi-step endpoints
- Documented in `backend_engineering_patterns.md`

---

### BLG-BE-49 — Down-migration rollback verification tests
**Priority:** P3 (Low)
**Type:** Backend / Data Integrity
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Schema migrations are tested forward (apply) but not backward (rollback) — a bad migration in production has no verified rollback path.

**Scope**
- Add rollback tests for the 5 most recent schema migrations, confirming `down()` (or equivalent) restores the prior schema state cleanly

**Acceptance Criteria**
- 5 migrations have passing rollback tests
- Pattern documented for future migrations

---

### BLG-GOV-178 — Quarterly AI output sampling audit (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** IDEA-ai-compliance-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled; consolidates BLG-GOV-197, BLG-GOV-251 — the same "recurring sampled review of AI output against the §13 boundary" capability was independently re-proposed across two later idea-intake cycles (2026-07-10 and 2026-07-24) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day per quarter)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
AI output (thesis generation, chat, daily briefing) has no recurring compliance sampling — only ad hoc review during feature work. As prompts and models evolve over time, outputs could drift from §13's determinism/no-prediction boundary without a scheduled check to catch it.

**Scope**
- Sample 10 random AI outputs per quarter; check against §13.2 boundary language (no autonomous-sounding directives, advisory framing preserved) and for determinism/no-prediction drift as prompts/models evolve

**Acceptance Criteria**
- First quarterly sample conducted and findings (if any) filed as backlog items

---

### BLG-GOV-179 — Local pre-commit lint for OpenAPI contract completeness
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The `openapi.yaml` completeness check currently only fires at PR/CI time — a local pre-commit lint would catch omissions before push, reducing CI churn.

**Scope**
- Pre-commit hook scanning `docs/specs/api_contracts/*.md` for new `## METHOD /path` headings without a matching `openapi.yaml` entry, mirroring the existing CI gate's logic

**Acceptance Criteria**
- Hook catches at least the same class of omission as the CI gate, locally, before commit

---

### BLG-SPEC-68 — Deprecation lifecycle policy for removed/renamed endpoints
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
No documented policy exists for how an endpoint is deprecated (sunset header, changelog entry, removal timeline) — the current process is ad hoc.

**Scope**
- Author a short policy doc: sunset-header convention, minimum deprecation window, changelog entry format

**Acceptance Criteria**
- Policy doc authored and referenced from `api_contracts` documentation index

---

### BLG-GOV-180 — Base44 prompt versioning changelog
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Base44 frontend scaffold prompts change over time with no changelog — regressions from a prompt change are hard to trace.

**Scope**
- Create a changelog file tracking Base44 prompt versions and what changed

**Acceptance Criteria**
- Changelog created; first entry backfilled from the most recent known prompt change

---

### BLG-GOV-181 — Base44 component regeneration diff review checklist
**Priority:** P3 (Low)
**Type:** Governance / QA
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
When a Base44-generated component is regenerated, there's no checklist to catch silent regressions (e.g. dropped props, changed class names) before merge.

**Scope**
- Short checklist: diff review points to check when a Base44 component is regenerated

**Acceptance Criteria**
- Checklist authored and referenced from the Base44 frontend prompt owner's charter

---

### BLG-SEC-11 — API key rotation drill
**Priority:** P3 (Low)
**Type:** Security / Operations
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The API key rotation runbook has never been exercised end-to-end — its first real use would be during an actual incident, the worst time to discover a gap.

**Scope**
- Exercise the rotation runbook for one non-critical key; document any gaps found

**Acceptance Criteria**
- Drill completed; runbook corrected if any step failed

---

### BLG-SEC-12 — CSP allows 'unsafe-inline' for script-src and style-src
**Priority:** P3 (Low)
**Type:** Security / Frontend
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Source:** ST-17 (BLG-OPS-71), EPIC-03, v6.8 system threat model review — 2026-07-09
**Effort:** M (~1-2 days — requires nonce/hash-based CSP migration and testing across all inline scripts/styles)
**Provisional-Target:** Unscheduled

**Problem**
`public/index.html`'s Content-Security-Policy permits `'unsafe-inline'` for both `script-src` and `style-src`. This significantly weakens the CSP's XSS mitigation value — an attacker who achieves any injection point (e.g. via a compromised dependency or a future reflected-XSS bug) can execute inline script/style despite the CSP being present, since `'unsafe-inline'` is a blanket allowance.

**Scope**
- Audit all inline `<script>`/`<style>` usage in the built SPA (CRA's default build may inject some)
- Migrate to nonce-based or hash-based CSP directives where feasible, removing `'unsafe-inline'`
- If full removal isn't feasible (e.g. due to a build-tool constraint), document the specific residual need and narrow the exception as much as possible

**Acceptance Criteria**
- CSP no longer includes a blanket `'unsafe-inline'` for `script-src`; `style-src` narrowed or justified explicitly if any exception remains
- No functional regression (app loads and renders correctly under the tightened CSP)

---

### BLG-SEC-13 — Raw exception text returned in API error responses
**Priority:** P3 (Low)
**Type:** Security / Backend
**Owner:** Head of Engineering
**Source:** ST-17 (BLG-OPS-71), EPIC-03, v6.8 system threat model review — 2026-07-09
**Effort:** M (~1-2 days — touches 44 call sites in backend/main.py)
**Provisional-Target:** v7.10

**Problem**
44 call sites in `backend/main.py` construct `HTTPException` responses with `detail=str(e)`, returning the raw Python exception message directly to the API caller. This risks incidental disclosure of internal file paths, database schema hints, or library version details to anyone holding the API key. Impact is bounded (the API is already key-gated and this is a single-user system), but it is a defense-in-depth gap — if the key is ever compromised, verbose errors give an attacker more reconnaissance than a generic message would.

**Scope**
- Replace `detail=str(e)` with a generic client-facing message for 500-class errors; log the full exception server-side (already partially done via `traceback.print_exc()` at some sites)
- Preserve specific, safe detail messages for expected 4xx errors (e.g. validation failures) where the detail is not derived from a raw exception object

**Acceptance Criteria**
- 500-class error responses no longer include raw exception text in the client-facing `detail` field
- Full exception detail still logged server-side for debugging
- No change to intentional, safe 4xx error messages

---

### BLG-OPS-94 — Data retention policy for AI audit log tables
**Priority:** P3 (Low)
**Type:** Operations / Data Management
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`gemini_audit_log` and the Claude audit log table grow without a retention policy — unbounded growth over a multi-year horizon.

**Scope**
- Define a retention window (e.g. 12–24 months) and an archival/deletion procedure

**Acceptance Criteria**
- Policy documented; first cleanup pass (if any rows exceed the window) executed or explicitly deferred with rationale

---

### BLG-GOV-183 — Onboarding template for new agent role charters
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Adding a new agent role charter currently means copying and adapting an existing one with no explicit template — inconsistent header/section coverage risk.

**Scope**
- Author a template charter file with required sections annotated

**Acceptance Criteria**
- Template authored and referenced from `claude/agents/` documentation

---


### BLG-QA-81 — Visual regression baseline snapshots (consolidated: contrast-sensitive + chart-heavy components)
**Priority:** P2 (Medium)
**Type:** QA / Visual Testing
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled; consolidates BLG-QA-118 — same capability (Playwright visual-regression baseline snapshots), independently re-proposed for a second component class at the 2026-07-24__scheduled rebalance without cross-reference to this existing item — merged 2026-07-28, session duplicate-consolidation cleanup; priority raised P3→P2 to match cluster max
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None — Arc 5/contrast remediation work (v6.6/v6.7) now stable; a good time to baseline before further drift accumulates.

**Problem**
No visual regression baseline exists for the components remediated in v6.6/v6.7's contrast work, nor for chart-heavy components (Performance Analytics, Strategy Benchmark) — a future change could silently reintroduce a contrast regression or a chart layout/rendering regression with no automated catch.

**Scope**
- Capture baseline screenshots for the highest-risk contrast-sensitive components; wire into CI visual diff (if tooling supports it) or a manual comparison checklist
- Capture baseline snapshots for the highest-value chart-heavy components (Performance Analytics, Strategy Benchmark) using existing Playwright visual-regression tooling

**Acceptance Criteria**
- Baselines captured for at least the components touched by `BLG-FE-87/88/89`
- Baselines captured for at least one chart-heavy component end-to-end as proof of pattern

---


### BLG-OPS-95 — Render hosting cost trend dashboard
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Render hosting cost is reviewed monthly ad hoc with no trend visualisation — harder to spot a cost trajectory shift early.

**Scope**
- Simple monthly cost-vs-request-volume trend chart, sourced from existing monthly review data

**Acceptance Criteria**
- Trend chart built with at least 3 months of historical data points

---

### BLG-OPS-96 — Anthropic API cost per-feature attribution
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Anthropic API cost is tracked in aggregate — no breakdown by feature (thesis generation vs. chat vs. daily briefing), making it hard to identify which feature drives cost.

**Scope**
- Tag cost-tracking records by feature/endpoint; produce a per-feature monthly breakdown

**Acceptance Criteria**
- Monthly cost breakdown available by feature for at least 1 reporting cycle

---

### BLG-FE-91 — Design token audit: v6.7 contrast fix consistency
**Priority:** P3 (Low)
**Type:** Frontend / Design System
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`BLG-FE-89` locked a canonical secondary-text design token into `design_system.md`, but no audit has confirmed every component actually uses the token rather than a hardcoded equivalent class.

**Scope**
- Spot-check a sample of components across the app for token usage vs. hardcoded classes

**Acceptance Criteria**
- Audit conducted; any drift found filed as a follow-up backlog item

---

### BLG-FE-92 — Empty-state illustration/microcopy consistency pass
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Empty states across pages (e.g. no trades, no watchlist items, no journal entries) use inconsistent copy tone and layout — no shared pattern.

**Scope**
- Audit existing empty states; define one shared pattern; apply to the most visible pages

**Acceptance Criteria**
- Shared pattern documented; applied to at least 3 pages

---

### BLG-OPS-97 — CI pipeline build-time reduction via parallelized test jobs
**Priority:** P3 (Low)
**Type:** Operations / CI
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Backend and frontend test suites currently run sequentially in CI, extending PR feedback time as the suites grow.

**Scope**
- Parallelize independent CI test jobs (backend/frontend at minimum)

**Acceptance Criteria**
- Measured CI wall-clock time reduced for a representative PR

---

### BLG-OPS-98 — Quarterly dependency minor-version upgrade cadence policy
**Priority:** P3 (Low)
**Type:** Operations / Engineering
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day per quarter)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Dependency minor-version upgrades happen reactively (security patch, feature need) rather than on a cadence — small upgrades accumulate into larger, riskier jumps.

**Scope**
- Define a quarterly minor-version upgrade window; first pass applies safe minor bumps across `requirements.txt`/`package.json`

**Acceptance Criteria**
- Policy documented; first quarterly pass completed

---

### BLG-SPEC-69 — Spec debt dashboard
**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
All `BLG-SPEC-*` items must currently be found by grepping `backlog.md` — no single view shows spec debt volume or age.

**Scope**
- Generate a single-page summary of all open `BLG-SPEC-*` items with age since filing

**Acceptance Criteria**
- Dashboard produced; refreshable at future `groom backlog` runs

---

### BLG-SPEC-70 — Canonical spec cross-reference linter
**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
A canonical spec document can become orphaned (no backlog item or code references it) with no automated way to detect this.

**Scope**
- Script scanning `docs/specs/**` for files not referenced by any backlog item or codebase comment

**Acceptance Criteria**
- Linter run once; any orphaned specs found are triaged (kept, merged, or archived)

---

### BLG-FE-93 — Confirm theme-toggle persistence across sessions
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The dark/light theme toggle is assumed to persist via localStorage, but this has not been explicitly verified across all entry points (e.g. a fresh session after a long gap, or after a browser storage-clearing event).

**Scope**
- Verify theme persistence behaviour across session boundaries; fix if any gap found

**Acceptance Criteria**
- Verification conducted; any gap found fixed or filed as a follow-up

---

### BLG-FE-94 — Mobile responsive audit for PerformanceAnalytics page
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
PerformanceAnalytics is one of the densest pages (multiple charts, tables) and has not had a dedicated mobile responsive audit.

**Scope**
- Audit page at common mobile breakpoints; document/fix any overflow, truncation, or unusable-control issues

**Acceptance Criteria**
- Audit conducted; critical issues (if any) fixed or filed

---

---

### BLG-GOV-184 — Canonical "win rate" definition consistency confirmation
**Priority:** P3 (Low)
**Type:** Governance / Metrics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
"Win rate" is surfaced in at least 4 places (dashboard, P&L report, drift analytics, journal) with no confirmation they all use the same calculation.

**Scope**
- Confirm calculation consistency across all 4 surfaces against `metrics_definitions.md`

**Acceptance Criteria**
- Consistency confirmed, or discrepancy filed as a correctness backlog item

---

### BLG-GOV-185 — Changelog section in metrics_definitions.md
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`metrics_definitions.md` has no changelog — formula version bumps are not tracked, making it hard to know when a metric's calculation last changed.

**Scope**
- Add a changelog section; backfill known recent formula changes

**Acceptance Criteria**
- Changelog section added with at least the most recent known change recorded

---

### BLG-GOV-186 — §13 boundary illustrative examples appendix
**Priority:** P3 (Low)
**Type:** Governance / Documentation
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Score-4/5 debates require citing specific §13 clauses, but §13 itself has no worked examples — every debate re-derives what "engaging a boundary" looks like in practice.

**Scope**
- Add an appendix to `strategy_rules.md` (or a companion doc) with 1–2 concrete right/wrong examples per §13 sub-clause

**Acceptance Criteria**
- Appendix authored, reviewed by Strategy Rules & System Intent Owner

---

### BLG-GOV-188 — Sprint Velocity Trend Chart
**Priority:** P3 (Low)
**Type:** Governance / Process Visibility
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260708-01 (IW-20260708-01), resubmission of IDEA-pmo-lead-20260619-02 (originally rejected at `2026-06-24__scheduled`, 3-cycle hard cap) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None — revival condition (velocity_metrics.md populated ≥5 cycles/2 rebalances) confirmed Met 2026-07-08 (49 rows across 8 rebalance-tracked cycles)

**Problem**
Sprint velocity trend (delivered stories per sprint, U/G/D/P breakdown, delivery rate) requires manual changelog/velocity_metrics.md analysis to see at rebalance time — no visualisation exists.

**Scope**
- Chart of velocity trend across the last 10 rebalance-tracked cycles, sourced from `velocity_metrics.md`

**Acceptance Criteria**
- Chart built, showing at least delivered-story-count and U/G/D/P split per cycle over the available history

---

### BLG-QA-82 — Consolidate 3 overlapping SignalCard Playwright specs
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
3 Playwright spec files cover overlapping SignalCard scenarios, accumulated incrementally across features (allocation_insufficient, badge colours, etc.) — redundant coverage slows the suite without adding confidence.

**Scope**
- Audit the 3 spec files; consolidate into 1 with no coverage loss

**Acceptance Criteria**
- Consolidated into 1 spec file; full scenario coverage confirmed retained; suite runtime reduced

---

### BLG-QA-83 — Standalone axe-core accessibility CI scan
**Priority:** P3 (Low)
**Type:** QA / Accessibility
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None — independent of `BLG-QA-63`'s "Arc 5 fully complete" gate; an automated axe-core scan doesn't require the full frontend feature set to stabilise first, unlike the fuller accessibility-testing programme `BLG-QA-63` describes.

**Problem**
No automated accessibility scanning exists in CI at all — `BLG-QA-63` gates a fuller programme behind Arc 5 completion, but a basic axe-core pass could run today at low cost.

**Scope**
- Add axe-core to the existing Playwright CI run for the highest-traffic pages; fail (or warn, initially) on critical violations

**Acceptance Criteria**
- axe-core scan running in CI for at least 3 pages; results visible in CI output

---

### BLG-QA-84 — Publish backend test coverage report to PR comments
**Priority:** P3 (Low)
**Type:** QA / CI
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Backend test coverage is only visible by running pytest locally with coverage flags — no visibility in the PR review flow, so coverage regressions can slip through unnoticed.

**Scope**
- Add a CI step posting a coverage summary (and delta vs. base branch, if feasible) as a PR comment

**Acceptance Criteria**
- Coverage summary posted automatically on the next PR after this ships

---

### BLG-QA-85 — Contract test suite: openapi.yaml vs. actual route behaviour
**Priority:** P3 (Low)
**Type:** QA / API Contracts
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The existing OpenAPI drift gate only checks that a `## METHOD /path` heading has a matching `openapi.yaml` entry (presence check) — it does not verify the entry's schema (request/response shape) actually matches route behaviour.

**Scope**
- Contract tests for a representative sample of endpoints, asserting actual response shape matches the documented `openapi.yaml` schema

**Acceptance Criteria**
- Contract tests passing for at least 5 representative endpoints; documented pattern for extending coverage

---

### BLG-QA-86 — Add baseline Playwright coverage for Watchlist.js
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality
**Source:** ST-14 (BLG-FE-77), EPIC-03, v6.8 — QA evidence consolidation frontend testing gate — 2026-07-09
**Effort:** S (~0.5-1 day)
**Provisional-Target:** v6.9

**Problem**
`src/pages/Watchlist.js` has no pre-existing Playwright spec file (confirmed via repo search during ST-14's refactor to ESLint compliance). ST-14's own AC-02 (no functional/visual behaviour change) was verified via agent-mediated diff review and a manual smoke script rather than an automated spec, since none exists to run as a regression baseline. This is a pre-existing coverage gap on an actively-used page, not something ST-14 introduced.

**Scope**
- Add `tests/e2e/watchlist.spec.js` covering: entries render with ticker/market/signal data; news-toggle expand/collapse for US-market entries; Add Ticker modal opens; edit/delete flows

**Acceptance Criteria**
- New spec file passes in CI
- Covers at minimum: entry rendering, news toggle, Add Ticker modal open

---

### BLG-GOV-189 — Governance overhead audit (PMO/spec time per shipped story)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Challenger; PMO Lead
**Source:** IDEA-challenger-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The Product Value Ratio and Skill-Silo alerts both measure governance overhead indirectly (via story classification) — no direct measurement exists of actual PMO/spec time cost per shipped user story, which would ground future governance-cadence decisions (e.g. `IDEA-pmo-lead-20260708-02`, debated this cycle) in harder evidence.

**Scope**
- Retrospective estimate of PMO/spec/governance effort vs. shipped-story count over the last 10 cycles, using available run_manifest/cycle_record artefacts as a proxy

**Acceptance Criteria**
- Estimate produced; findings inform the next cycle-cadence discussion if one recurs

---

### BLG-SPEC-72 — Revisit SI-02 Gate Status Condition 2/3 threshold definitions once real adherence data exists
**Priority:** P2 (Medium)
**Type:** Spec Debt
**Owner:** Product Owner / Head of UX & Design
**Source:** ST-06 (BLG-FEAT-71, v6.8) Product Owner PR review — 2026-07-09
**Effort:** S (~0.5 day — product decision + spec update, no new engineering)
**Provisional-Target:** Unscheduled
**Depends on:** Sufficient real trade-plan-linkage volume in production to make a data-informed threshold call (soft — could also be resolved by product judgment alone)

**Problem**
The locked ux_spec (`docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md`) named Gate Condition 1 ("20-trade threshold") and Condition 3's topic ("trade plan adherence") but left Condition 2 unlabeled and gave no numeric MET threshold for Condition 3. At implementation, the engine filled the gap with Condition 2 = "linked closed trades ≥ 20" and Condition 3 = `trade_plan_adherence_rate > 0` — both spec-conformant (confirmed by agent-mediated Director of Quality review) but never explicitly reviewed as a *product* decision. `adherence > 0` in particular is a very low bar — a single linked trade among hundreds would read as MET — and risks becoming a permanent, unexamined default if not revisited.

**Scope**
- Product Owner + Head of UX & Design review the current Condition 2/3 definitions against real production adherence data once available
- Decide whether the thresholds should change (e.g. a percentage-based adherence bar rather than `> 0`)
- Update `docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md` (or its successor) and `docs/specs/frontend/pages/reports.md` to formally codify the decision, replacing the engine's placeholder language

**Acceptance Criteria**
- AC-01: Gate Condition 2 and 3 definitions are explicitly product-reviewed and documented in the canonical spec, no longer marked as an engine-filled gap
- AC-02: If thresholds change, `src/pages/Reports.js`'s `SI02GateStatusSection` is updated to match, with Playwright coverage for the new thresholds

---

### BLG-GOV-191 — Spec debt aging report
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-specs-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
There is no standing report surfacing which `BLG-SPEC-*` items are approaching the 2-cycle-without-story-assignment advisory threshold defined in `release_planning_prompt.md` STEP 1.1 — it currently only fires reactively when a release plan happens to scan for it.

**Proposed solution**
Add a lightweight scan (reusable at `groom backlog` or release planning time) that lists spec-debt items by cycles-aged, surfaced proactively rather than only at the moment a release plan checks.

---

### BLG-GOV-192 — Governance prompt cross-reference sweep cadence
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-specs-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
§14 OPERATIONAL_GUIDE.md version drift is currently only caught opportunistically (e.g. by the `governance-drift` skill when invoked, or when a friction item happens to surface it) rather than on a fixed cadence.

**Proposed solution**
Schedule a periodic (e.g. every-3-cycle, alongside the meta-review) explicit governance-drift check rather than relying on incidental discovery.

---

### BLG-GOV-193 — Escalation SLA breach dry-run test
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead
**Source:** Idea intake IW-20260710-01 (IDEA-pmo-lead-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The `BLOCKED_SLA_BREACH` 72-hour notice path (`shared_standards.md` §4) has never been exercised end-to-end in this repository's history — it is untested governance machinery.

**Proposed solution**
Construct a deliberate dry-run (e.g. a synthetic escalation with a backdated timestamp) to confirm the breach notice actually fires and halts as designed.

---

### BLG-QA-88 — DoQ sign-off template freshness check
**Priority:** P3 (Low)
**Type:** QA / Process
**Owner:** Director of Quality
**Source:** Idea intake IW-20260710-01 (IDEA-director-of-quality-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The `record-visual-qa` skill's evidence format was defined against a staging practice that may have since evolved; no periodic check confirms the template still matches actual practice.

**Proposed solution**
Periodically (e.g. every few releases) confirm the DoQ sign-off template and the skill that populates it still reflect current staging sign-off practice.

---

### BLG-GOV-194 — §13 boundary language clarity pass — AI journal summarisation
**Priority:** P3 (Low)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** Idea intake IW-20260710-01 (IDEA-strategy-owner-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`strategy_rules.md` §13's "deterministic scoring" boundary language pre-dates the AI journal summarisation feature; it has not been explicitly re-read against that feature to confirm the language still functions as an unambiguous boundary.

**Proposed solution**
Strategy Rules & System Intent Owner re-reads §13 against the AI journal summarisation feature specifically and confirms (or clarifies) the boundary language remains unambiguous.

---

### BLG-GOV-195 — Strategic exclusions review cadence
**Priority:** P3 (Low)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** Idea intake IW-20260710-01 (IDEA-strategy-owner-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The 4 product-scope exclusions in `current_roadmap.md` §2 (broker API integration, real-time streaming, social features, options/futures) have not been explicitly re-confirmed since they were first recorded — they could be stale rather than deliberate.

**Proposed solution**
Add a periodic (e.g. every-N-cycle) explicit re-confirmation that each exclusion remains a deliberate choice, not simply an un-revisited default.

---

### BLG-OPS-101 — Render hosting tier review
**Priority:** P3 (Low)
**Type:** Operations
**Owner:** FinOps & Resource Architect
**Source:** Idea intake IW-20260710-01 (IDEA-finops-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The current Render service tier was set early in the project's life and has not been reviewed against actual usage since v6.8's added traffic (SI-02 indicator, trade tagging).

**Proposed solution**
Compare current Render tier cost/limits against actual measured usage and confirm the tier still fits, or right-size it.

---

### BLG-OPS-103 — Production database backup/restore drill
**Priority:** P2 (Medium)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner
**Source:** Idea intake IW-20260710-01 (IDEA-infra-ops-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
No governed routine has ever exercised a full backup/restore drill against the production database; the recovery procedure's correctness is currently unverified.

**Proposed solution**
Document the current backup mechanism (if any) and perform one full restore drill against a non-production target to confirm the procedure actually works.

---

### BLG-GOV-196 — Sunset review for Priority 3 — Deferred initiatives
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Product Owner
**Source:** Idea intake IW-20260710-01 (IDEA-challenger-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The 7-item `initiative_register.md` Priority 3 — Deferred list (Position Correlation Analysis, Backtesting Module, Multi-Portfolio Support, Mobile App, Full Compliance Scoring, Prometheus, Customisable Dashboard Layout) has not been explicitly re-confirmed since first recorded; some entries may now be stale rather than deliberately deferred.

**Proposed solution**
Product Owner reviews each Priority 3 item and confirms it is still deliberately deferred (not simply forgotten), recording the confirmation date.

---

### BLG-SEC-14 — AI journal generation audit trail
**Priority:** P3 (Low)
**Type:** Security / Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** Idea intake IW-20260710-01 (IDEA-ai-compliance-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Generated AI journal entries do not currently log which model/version produced them, limiting compliance traceability if AI output quality or behaviour is later questioned.

**Proposed solution**
Log model identifier and version alongside each AI-generated journal entry at generation time.

---

### BLG-SPEC-74 — OpenAPI response examples for Arc 5 endpoints
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** Idea intake IW-20260710-01 (IDEA-api-contracts-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`docs/reference/openapi.yaml` lacks example response payloads for Arc 5 endpoints, slowing frontend integration since developers must infer shapes from the schema alone.

**Proposed solution**
Add representative example payloads to the Arc 5 endpoint definitions in `openapi.yaml`.

---

### BLG-OPS-104 — Contract drift dashboard
**Priority:** P3 (Low)
**Type:** Operations / Governance
**Owner:** API Contracts & Documentation Owner
**Source:** Idea intake IW-20260710-01 (IDEA-api-contracts-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Routes missing a `docs/specs/api_contracts` entry are currently only caught when the CI OpenAPI Drift Detection gate fires on a PR — there is no proactive, pre-PR way to see the gap.

**Proposed solution**
Add a simple script/report surfacing any `backend/routers/` endpoint lacking a matching contract entry, runnable ahead of opening a PR.

---

### BLG-BE-54 — Database connection pool tuning review
**Priority:** P3 (Low)
**Type:** Backend / Operations
**Owner:** Backend Engineering Patterns Owner
**Source:** Idea intake IW-20260710-01 (IDEA-backend-engineering-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The database connection pool size has not been reviewed against actual concurrent load since v6.8's added traffic; it may be mis-sized in either direction.

**Proposed solution**
Measure current concurrent connection usage and compare against the configured pool size; adjust if warranted.

---

### BLG-FE-99 — Reusable empty-state component spec for Base44 prompts
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** Idea intake IW-20260710-01 (IDEA-base44-frontend-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Each page's empty-state currently gets a bespoke Base44 prompt, producing visual/copy drift across pages with no shared source of truth.

**Proposed solution**
Define one reusable empty-state component spec that future Base44 prompts reference instead of reinventing per page.

---

### BLG-GOV-198 — Base44 prompt versioning convention
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** Idea intake IW-20260710-01 (IDEA-base44-frontend-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
There is no convention tracking which Base44 prompt draft shipped with which ST-id, making future regression triage ("which prompt produced this component") harder than necessary.

**Proposed solution**
Adopt a lightweight convention (e.g. a comment header or delegation log field) recording the ST-id alongside each Base44 prompt draft.

---

### BLG-SEC-15 — Recurring dependency vulnerability re-scan cadence (consolidated)
**Priority:** P2 (Medium)
**Type:** Security
**Owner:** Cybersecurity & Trust Lead
**Source:** Idea intake IW-20260710-01 (IDEA-cybersecurity-20260710-01), roadmap rebalance 2026-07-10__scheduled; consolidates BLG-OPS-93 (automate monthly dependency vulnerability re-scan) and BLG-SEC-19 (formalise npm audit + pip-audit sweep cadence) — the same underlying capability was re-proposed across the 2026-07-08 and 2026-07-17 idea-intake cycles without cross-reference to this existing item — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** S (~0.5–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`pip-audit` runs at sprint planning (`sprint_planning_notes.md` §Pre-Sprint Vulnerability Scan) and `npm audit`/`pip audit` are otherwise run ad hoc rather than on a fixed schedule, with no documented recurring cadence independent of sprint planning or any single backlog item — new CVEs in existing dependencies could go unnoticed between ad hoc scans.

**Scope**
- Add a scheduled CI job (e.g. monthly) running both `pip-audit` and `npm audit`, independent of sprint planning
- File a backlog item for any new HIGH/CRITICAL finding
- Document the combined cadence (sprint planning + scheduled interval) explicitly in `sprint_planning_prompt.md` or `shared_standards.md`

**Acceptance Criteria**
- Scheduled job runs successfully at least once and reports results for both `pip-audit` and `npm audit`
- Combined cadence documented
- New HIGH/CRITICAL findings result in a filed backlog item

---

### BLG-SEC-16 — API key rotation runbook
**Priority:** P2 (Medium)
**Type:** Security
**Owner:** Cybersecurity & Trust Lead
**Source:** Idea intake IW-20260710-01 (IDEA-cybersecurity-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The application `X-API-Key` was formally registered in v6.8 (BLG-OPS-99) but no rotation procedure has been documented — if the key were ever compromised, there is no defined runbook for rotating it.

**Proposed solution**
Document a rotation runbook: steps, owner, and verification checklist for rotating the registered API key.

---

### BLG-BE-55 — trade_plans.position_id historical backfill design
**Priority:** P2 (Medium)
**Type:** Backend / Data
**Owner:** Data Model & Domain Schema Owner
**Source:** Idea intake IW-20260710-01 (IDEA-data-model-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-BE-46 forward-fixed new `trade_plans` rows to populate `position_id`, but the 11 historically-affected rows remain permanently unlinked per BLG-BE-52's "no backfill" resolution — a backfill design was never actually scoped, only declined.

**Proposed solution**
Data Model Owner scopes what a backfill would require (if ever revisited) so the "no backfill" decision is a recorded trade-off, not a gap.

---

### BLG-SPEC-75 — Migration block consolidation review
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Data Model & Domain Schema Owner
**Source:** Idea intake IW-20260710-01 (IDEA-data-model-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`data_model.md`'s migration block history has not been reviewed for consistency since before v6.8's schema changes.

**Proposed solution**
Review all migration blocks in ascending version order for consistency and confirm the footer version matches the highest block.

---

### BLG-QA-89 — R-multiple calculation regression test
**Priority:** P2 (Medium)
**Type:** QA / Backend
**Owner:** Financial Reporting & Records Owner
**Source:** Idea intake IW-20260710-01 (IDEA-financial-reporting-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The v6.8 R-multiple FX spec has no automated regression test locking its behaviour against known trade fixtures — a future change could silently alter R-multiple calculations.

**Proposed solution**
Add an automated test asserting R-multiple output against a small set of known trade fixtures.

---

### BLG-SPEC-76 — Trade tagging taxonomy documentation
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Financial Reporting & Records Owner
**Source:** Idea intake IW-20260710-01 (IDEA-financial-reporting-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-FEAT-52 (trade tagging) shipped without a canonical list of allowed tags, risking inconsistent tag usage that would undermine tag-based reporting.

**Proposed solution**
Document a canonical allowed-tag taxonomy for trade tagging, referenced by both the UI and reporting logic.

---

### BLG-FE-100 — Dark/light theme contrast audit follow-up
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Idea intake IW-20260710-01 (IDEA-frontend-specs-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-FE-87/88/89 fixed the known secondary-text contrast gaps, but no follow-up audit has confirmed no further gaps exist outside that specific defect class.

**Proposed solution**
Run a targeted follow-up contrast audit scoped to confirm no other secondary-text (or similar) contrast gaps remain.

---

### BLG-SPEC-77 — Gate-status indicator reusable component pattern documentation
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Idea intake IW-20260710-01 (IDEA-frontend-specs-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-FEAT-71's SI-02 gate visibility indicator is a one-off implementation; the pattern is not documented for reuse by future gated features.

**Proposed solution**
Document the SI-02 indicator as a reusable gate-status component pattern in the relevant frontend spec, for future gated-feature reuse.

---

### BLG-OPS-105 — CI pipeline runtime audit
**Priority:** P3 (Low)
**Type:** Operations / QA
**Owner:** Head of Engineering
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-engineering-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Full CI suite runtime has been creeping up without a recent audit identifying which test files are slowest.

**Proposed solution**
Profile CI runtime by file and identify the slowest contributors as candidates for optimisation or parallelisation.

---

### BLG-BE-56 — Backend service-layer boundary review
**Priority:** P3 (Low)
**Type:** Backend
**Owner:** Head of Engineering
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-engineering-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Recent `BLG-BE-*` items have touched router/service/database layers; no recent review confirms the layering boundary still holds cleanly after these changes.

**Proposed solution**
Review recent backend changes for layering-boundary drift (e.g. business logic leaking into routers) and correct any found.

---

### BLG-FE-101 — Reports page information hierarchy review
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-ux-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The Reports page gained the SI-02 gate visibility indicator (BLG-FEAT-71) in v6.8; no follow-up review has confirmed the page's information hierarchy still reads cleanly with the addition.

**Proposed solution**
Head of UX & Design reviews the Reports page for visual clutter or hierarchy issues introduced by the new indicator.

---

### BLG-QA-90 — Watchlist.js post-refactor visual QA
**Priority:** P3 (Low)
**Type:** QA / Frontend
**Owner:** Head of UX & Design
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-ux-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The v6.8 Watchlist.js ESLint refactor (BLG-OPS-61) was a code-quality change; no explicit visual QA pass has confirmed it introduced no visual regressions.

**Proposed solution**
Perform a visual QA pass on the Watchlist page to confirm the ESLint refactor did not change rendered behaviour.

---

### BLG-FEAT-72 — Product Value Ratio historical trend chart
**Priority:** P3 (Low)
**Type:** Product Feature / Governance Tooling
**Owner:** Metrics Definitions & Analytics Owner
**Source:** Idea intake IW-20260710-01 (IDEA-metrics-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
STEP 2.4's U/G/D/P ratio is currently re-read from decision-log prose each rebalance rather than visualised as a trend, making it harder to spot the trajectory at a glance.

**Proposed solution**
Build a small chart/table visualising the ratio across cycles, sourced from a structured record rather than re-derived prose each time.

---

### BLG-GOV-200 — Skill-Silo rolling-average automation
**Priority:** P3 (Low)
**Type:** Governance Tooling
**Owner:** Metrics Definitions & Analytics Owner
**Source:** Idea intake IW-20260710-01 (IDEA-metrics-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The STEP 7.1 Skill-Silo rolling-3-cycle average is currently computed manually each rebalance by reading the prior 2 cycles' recorded percentages from decision-log prose.

**Proposed solution**
Compute the rolling average from a structured source (e.g. a small per-cycle metrics file) instead of manual re-derivation each rebalance.

---

### BLG-QA-91 — Cross-browser Playwright matrix evaluation
**Priority:** P3 (Low)
**Type:** QA
**Owner:** QA Lead
**Source:** Idea intake IW-20260710-01 (IDEA-qa-lead-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Playwright coverage currently runs Chromium-only; critical-path behaviour on Firefox/WebKit is unverified.

**Proposed solution**
Evaluate the cost/benefit of adding Firefox/WebKit to the CI matrix for a small set of critical-path specs.

---

### BLG-GOV-201 — QA evidence log template consolidation
**Priority:** P3 (Low)
**Type:** Governance / QA Process
**Owner:** QA Lead
**Source:** Idea intake IW-20260710-01 (IDEA-qa-lead-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Per-EPIC `qa_evidence_EPIC-*.md` files currently duplicate a substantial amount of boilerplate header/structure across files.

**Proposed solution**
Consolidate shared boilerplate into a referenced template section, reducing duplication across EPIC evidence files.

---

### BLG-QA-92 — Backend test suite runtime baseline
**Priority:** P3 (Low)
**Type:** QA / Backend
**Owner:** QA & Testing Owner
**Source:** Idea intake IW-20260710-01 (IDEA-qa-testing-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
No current baseline records pytest suite runtime, making future runtime regressions hard to detect early.

**Proposed solution**
Record current `backend/.venv/bin/python3 -m pytest` runtime as a baseline for future comparison.

---

### BLG-QA-93 — conftest.py AST-scan coverage confirmation (consolidated)
**Priority:** P3 (Low)
**Type:** QA / Backend
**Owner:** QA & Testing Owner
**Source:** Idea intake IW-20260710-01 (IDEA-qa-testing-20260710-02), roadmap rebalance 2026-07-10__scheduled; consolidates BLG-QA-99 — the same capability was independently re-proposed at the 2026-07-12__scheduled idea-intake cycle without cross-reference to this existing item — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-QA-73 replaced the manual `_DB_STUB_FUNCTIONS` list with an AST-scan derivation; no confirmation has been recorded that the scan's glob/traversal logic still covers all `backend/` modules and subpackages added since v6.8.

**Proposed solution**
Re-verify the AST scan's module coverage and glob/traversal logic against the current `backend/` tree; extend if a subpackage was missed; record confirmation.

---



### BLG-QA-105 — Fix unrestored sys.modules stubbing in test_alerts_service.py (cross-file test pollution)
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Session investigation into signal-generation data integrity — 2026-07-13
**Effort:** S (~0.5-2 days)
**Provisional-Target:** v7.1
**Gate criteria:** None

**Problem**
`tests/test_alerts_service.py` (~line 89-100) unconditionally overwrites `sys.modules["utils.formatting"]`, `sys.modules["utils.pricing"]`, `sys.modules["utils.calculations"]`, and `sys.modules["config"]` with stub modules/MagicMocks at import time, with no teardown. Because `sys.modules` is process-global, every test file collected afterward in the same pytest session that imports `utils.formatting` (etc.) silently receives the fake passthrough stub instead of the real module. Confirmed directly: a new regression test (tests/test_formatting.py, added in PR #971) passed in isolation but failed under the full suite until rewritten to load the real module from its file path, bypassing the pollution. This is a plausible reason the numpy/psycopg2 signal-write bug (PR #971) was never caught by any test exercising `signal_service.py` — its `decimal_to_float` import could have been silently neutered the same way. `tests/test_trade_service.py` has an equivalent stub but already guards it (`if not hasattr(...)`) so it doesn't clobber a real module; `test_alerts_service.py` does not.

**Proposed solution**
Give test_alerts_service.py's module stubbing proper scoping/teardown (e.g. a pytest fixture restoring the prior `sys.modules` entries after that file's tests complete), matching the safer guarded pattern already used in test_trade_service.py.

---

---
*Release Slice v4.6 removed — cycle 2026-05-30__release-v4.6 closed 2026-05-31. Archived canonical home: claude/cycles/2026-05-30__release-v4.6/stage4_backlog_slice.md*

---

*Release Slice v4.8 removed — cycle 2026-06-01__release-v4.8 closed 2026-06-02. Archived canonical home: claude/cycles/2026-06-01__release-v4.8/stage4_backlog_slice.md*

---

*Release Slice v4.9 removed — cycle 2026-06-02__release-v4.9 closed 2026-06-02. Archived canonical home: claude/cycles/2026-06-02__release-v4.9/stage4_backlog_slice.md*

---

*Release Slice v5.0 removed — cycle 2026-06-03__release-v5.0 closed 2026-06-03. Archived canonical home: claude/cycles/2026-06-03__release-v5.0/stage4_backlog_slice.md*

---
*Release Slice v5.2 removed — cycle 2026-06-08__release-v5.2 closed 2026-06-08. Archived canonical home: claude/cycles/2026-06-08__release-v5.2/stage4_backlog_slice.md*

---

*Release Slice v5.3 removed — cycle 2026-06-08__release-v5.3 closed 2026-06-09. Archived canonical home: claude/cycles/2026-06-08__release-v5.3/stage4_backlog_slice.md*

---

*Release Slice v5.4 removed — cycle 2026-06-09__release-v5.4 closed 2026-06-10. Archived canonical home: claude/cycles/2026-06-09__release-v5.4/stage4_backlog_slice.md*

---

*Release Slice v5.5 removed — cycle 2026-06-10__release-v5.5 closed 2026-06-16. Archived canonical home: claude/cycles/2026-06-10__release-v5.5/stage4_backlog_slice.md*

---

*Release Slice v5.6 removed — cycle 2026-06-16__release-v5.6 closed 2026-06-16. Archived canonical home: claude/cycles/2026-06-16__release-v5.6/stage4_backlog_slice.md*

---

*Release Slice v5.8 removed — cycle 2026-06-17__release-v5.8 closed 2026-06-17. Archived canonical home: claude/cycles/2026-06-17__release-v5.8/stage4_backlog_slice.md*

*Release Slice v5.7 removed — cycle 2026-06-16__release-v5.7 closed 2026-06-17. Archived canonical home: claude/cycles/2026-06-16__release-v5.7/stage4_backlog_slice.md*

---

---

*Release Slice v5.9 removed — cycle 2026-06-17__release-v5.9 closed 2026-06-18. Archived canonical home: claude/cycles/2026-06-17__release-v5.9/stage4_backlog_slice.md*

*Release Slice v6.0 removed — cycle 2026-06-19__release-v6.0 closed 2026-06-22. Archived canonical home: claude/cycles/2026-06-19__release-v6.0/stage4_backlog_slice.md*

---

*Release Slice v6.1 removed — cycle 2026-06-22__release-v6.1 closed 2026-06-23. Archived canonical home: claude/cycles/2026-06-22__release-v6.1/stage4_backlog_slice.md*

---

*Release Slice v6.2 removed — cycle 2026-06-24__release-v6.2 closed 2026-06-25. Archived canonical home: claude/cycles/2026-06-24__release-v6.2/stage4_backlog_slice.md*

---

*Release Slice v6.3 removed — cycle 2026-06-26__release-v6.3 closed 2026-06-30. Archived canonical home: claude/cycles/2026-06-26__release-v6.3/stage4_backlog_slice.md*

---

*Release Slice v6.4 removed — cycle 2026-07-02__release-v6.4 closed 2026-07-02. Archived canonical home: claude/cycles/2026-07-02__release-v6.4/stage4_backlog_slice.md*

---

*Release Slice v6.5 removed — cycle 2026-07-02__release-v6.5 closed 2026-07-03. Archived canonical home: claude/cycles/2026-07-02__release-v6.5/stage4_backlog_slice.md*

---

*Release Slice v6.6 removed — cycle 2026-07-04__release-v6.6 closed 2026-07-06. Archived canonical home: claude/cycles/2026-07-04__release-v6.6/stage4_backlog_slice.md*

---

*Release Slice v6.7 removed — cycle 2026-07-06__release-v6.7 closed 2026-07-08. Archived canonical home: claude/cycles/2026-07-06__release-v6.7/stage4_backlog_slice.md*

---

*Release Slice v6.8 removed — cycle 2026-07-08__release-v6.8 closed 2026-07-09. Archived canonical home: claude/cycles/2026-07-08__release-v6.8/stage4_backlog_slice.md*

---

*Release Slice v6.9 removed — cycle 2026-07-10__release-v6.9 closed 2026-07-10. Archived canonical home: claude/cycles/2026-07-10__release-v6.9/stage4_backlog_slice.md*

---

*Release Slice v7.0 removed — cycle 2026-07-12__release-v7.0 closed 2026-07-13. Archived canonical home: claude/cycles/2026-07-12__release-v7.0/stage4_backlog_slice.md*

---

## Release Slice v7.10

<!-- release-plan-marker: RP:v7.10:2026-07-28__release-v7.10 -->

**Ephemeral section — removed at next `groom backlog` run after this cycle closes.** Canonical home: `claude/cycles/2026-07-28__release-v7.10/stage4_backlog_slice.md`.

23 items across 6 grouped EPICs, sized to the full confirmed ~24-28 day capacity band (~26.15 days midpoint), per explicit user "use full capacity" instruction:

| Item | Epic | Story |
|------|------|-------|
| BLG-BE-68 | EPIC-01 | ST-01 |
| BLG-BE-75 | EPIC-01 | ST-02 |
| BLG-BE-76 | EPIC-01 | ST-03 |
| BLG-BE-41 | EPIC-01 | ST-04 |
| BLG-SEC-22 | EPIC-02 | ST-05 |
| BLG-SEC-09 | EPIC-02 | ST-06 |
| BLG-SEC-18 | EPIC-02 | ST-07 |
| BLG-SEC-13 | EPIC-02 | ST-08 |
| BLG-QA-127 | EPIC-03 | ST-09 |
| BLG-QA-96 | EPIC-03 | ST-10 |
| BLG-QA-133 | EPIC-03 | ST-11 |
| BLG-QA-128 | EPIC-03 | ST-12 |
| BLG-SPEC-102 | EPIC-04 | ST-13 |
| BLG-SPEC-103 | EPIC-04 | ST-14 |
| BLG-SPEC-104 | EPIC-04 | ST-15 |
| BLG-GOV-243 | EPIC-04 | ST-16 |
| BLG-FE-122 | EPIC-05 | ST-17 |
| BLG-FE-123 | EPIC-05 | ST-18 |
| BLG-FE-106 | EPIC-05 | ST-19 |
| BLG-FE-134 | EPIC-05 | ST-20 |
| BLG-GOV-256 | EPIC-06 | ST-21 |
| BLG-GOV-216 | EPIC-06 | ST-22 |
| BLG-GOV-207 | EPIC-06 | ST-23 |

`Provisional-Target` updated `TBD`/`Unscheduled`/stale `v7.7` → `v7.10` on all 23 items (see each item's own entry above). `BLG-FEAT-73`/`BLG-FEAT-74` and the Arc 5 pre-entry/compliance-gateway UX cluster (12 items) + `BLG-SPEC-35` excluded — all carry unmet gate criteria, consistent with the standing PO perennial-return disposition. See `decisions--2026-07-28__release-v7.10.md`.

---

### BLG-SEC-18 — Rate-limit audit on public-facing endpoints ahead of any future auth changes
**Priority:** P2 (Medium) | **Type:** Security | **Owner:** Cybersecurity & Trust Lead | **Source:** IDEA-cybersecurity-20260717-01 | **Effort:** M | **Provisional-Target:** v7.10
**Problem:** No confirmed rate-limiting audit has been performed against the current `X-API-Key`-gated endpoint set (registered `BLG-OPS-99`) — a gap that becomes more consequential once/if any auth model change is considered.
**Scope:** Audit current rate-limiting posture (Render platform-level and application-level) against all public-facing endpoints; document findings.
**Acceptance Criteria:** Audit complete; any gaps filed as follow-up `BLG-SEC-*` items; no implementation required unless a P0/P1 gap is found.

---

### BLG-QA-113 — Recurring pre-sprint-planning endpoint test coverage audit
**Priority:** P2 (Medium) | **Type:** QA / Process | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260717-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `CLAUDE.md §2` requires every new backend route to have a corresponding entry in `backend/routers/test.py` in the same commit, but this is currently caught per-PR by review discipline rather than by a recurring audit that would catch any historical drift.
**Scope:** Add a recurring (pre-sprint-planning) audit comparing all `@router.get/post/put/delete` decorators against `test.py` entries, catching any gap missed by per-commit review.
**Acceptance Criteria:** Audit script/checklist added; run once against current state with results recorded (pass, or gaps filed).

---

### BLG-OPS-113 — Consolidate window_summary_IW-*.md files older than 90 days into a dated archive folder
**Priority:** P3 (Low) | **Type:** Operations / Housekeeping | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260717-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `claude/ideas/` now holds 20+ `window_summary_IW-*.md` files accumulated since 2026-03-21 with no archival pass — a directory-hygiene gap analogous to the pattern `ideas_housekeeping_prompt.md` already solves for register rows.
**Scope:** Move `window_summary_IW-*.md` files older than 90 days into a dated archive subfolder (e.g. `claude/ideas/window_summaries_archive/`), leaving the most recent 90 days in place for easy reference.
**Acceptance Criteria:** Archive folder created; files older than 90 days moved; no content lost (move, not delete).

---

### BLG-OPS-114 — Render service health-check alerting to Telegram on 5xx spike
**Priority:** P2 (Medium) | **Type:** Operations / Reliability | **Owner:** Infrastructure & Operations Owner | **Source:** IDEA-infra-ops-20260717-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** The existing Telegram integration (weekly digest, per `strategy_rules.md §` digest references) has no wiring to Render service health — a sustained 5xx spike on the production backend would currently only be discovered manually.
**Scope:** Add a lightweight health-check poll (or Render webhook, if available on current plan tier) that posts a Telegram alert on a sustained 5xx spike.
**Acceptance Criteria:** Alert wired and confirmed to fire on a simulated 5xx spike (staging) or a documented dry-run test.

---

### BLG-OPS-115 — Configure TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID as GitHub Actions repo secrets for nightly backtest job alerting
**Priority:** P2 (Medium) | **Type:** Operations / Reliability | **Owner:** Infrastructure & Operations Owner | **Source:** ST-10 (EPIC-10, v7.7) execution | **Effort:** XS | **Provisional-Target:** TBD
**Problem:** `backtest.yml`'s new failure/anomaly alert step (ST-10, EPIC-10, v7.7) POSTs to Telegram via `secrets.TELEGRAM_BOT_TOKEN`/`secrets.TELEGRAM_CHAT_ID`, but these are currently only configured as Render backend env vars (`backend/config.py`), not as GitHub Actions repo secrets. Until added, the alert step degrades gracefully (logs a `::warning::` annotation instead of sending) rather than failing the job — but the alert will not actually reach anyone until configured.
**Scope:** Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as GitHub Actions repo secrets (same values as the existing Render env vars) under repo Settings → Secrets and variables → Actions.
**Acceptance Criteria:** Secrets present in repo Actions settings; a manual `workflow_dispatch` re-run against a deliberately-broken endpoint confirms a Telegram message is actually received (not just the `::warning::` fallback).

---

## Roadmap Rebalance 2026-07-12__scheduled — New Items (IW-20260712-01 disposition)

*37 items added via idea intake IW-20260712-01 STEP 4 disposition (Backlog/gate-conditional-or-actionable-now). Source ideas and full rationale: `claude/ideas/ideas_register.md` (2026-07-12 rows), `claude/ideas/window_summary_IW-20260712-01.md`. DL-064.*

### BLG-GOV-203 — Gemini AI usage audit-trail retention policy
**Priority:** P3 (Low) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `gemini_audit_log` (v4.0) has no retention/archival policy; unbounded growth complicates compliance review.
**Scope:** Define a retention window and archival job for the audit log table.
**Acceptance Criteria:** Retention policy documented; archival mechanism specified; AI Compliance Officer sign-off.

### BLG-GOV-204 — Formal §13 boundary re-attestation cadence
**Priority:** P3 (Low) | **Type:** Governance / §13 Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260712-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Individual features get one-time §13 PASS reviews; no recurring re-attestation exists as the system accretes AI/automation-adjacent features, so cumulative drift risk goes undetected between reviews.
**Scope:** Propose a semi-annual boundary re-attestation cadence across all shipped AI/automation-adjacent features (IT-06, SI-01, Gemini thesis generation, etc.).
**Acceptance Criteria:** Cadence proposal documented; first review date set; Strategy Rules & System Intent Owner sign-off.

### BLG-QA-94 — OpenAPI drift gate false-negative sweep
**Priority:** P3 (Low) | **Type:** QA / Process Tooling | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The `## METHOD /path` heading-level rule has already caused one silent contract-drift gap (fixed). No periodic audit confirms non-recurrence.
**Scope:** Add a quarterly 3-way sweep comparing router decorators, contract file headings, and `openapi.yaml` paths.
**Acceptance Criteria:** Sweep procedure documented; first run scheduled; zero drift confirmed or gaps filed.

### BLG-GOV-205 — Standardise `api_changelog.md` entry template
**Priority:** P3 (Low) | **Type:** Governance / Documentation | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Inconsistent version-footer formatting across releases makes `CLAUDE.md` §8 cross-EPIC merge-conflict resolution harder than necessary.
**Scope:** Define one canonical `api_changelog.md` entry template and apply retroactively where low-cost.
**Acceptance Criteria:** Template documented; existing entries conform or a migration note is filed.

### BLG-BE-57 — Alpaca API rate-limit backoff audit
**Priority:** P3 (Low) | **Type:** Backend / Reliability | **Owner:** Backend Engineering Patterns Owner | **Source:** IDEA-backend-engineering-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** DS-05/IT-06 depend on the Alpaca API; no documented backoff/retry audit has been performed since integration shipped (v2.9/v3.5).
**Scope:** Audit current retry/backoff logic against Alpaca's documented rate limits; document the effective SLA.
**Acceptance Criteria:** Audit findings documented; any gaps filed as follow-up items.

### BLG-FE-103 — Shared modal shell for compliance/checklist components
**Priority:** P3 (Low) | **Type:** Frontend / Refactor | **Owner:** Base44 Frontend Prompt Owner | **Source:** IDEA-base44-frontend-20260712-02 | **Effort:** M | **Provisional-Target:** Unscheduled
**Problem:** `ComplianceRecheckModal.js` (v6.9) and the PT-05 checklist modal implement a similar pattern divergently, risking UX drift between them over time.
**Scope:** Extract a shared modal shell component; migrate both consumers.
**Acceptance Criteria:** Shared component exists; both modals migrated with no visual/behavioural regression (Playwright coverage confirms).

### BLG-GOV-207 — Same-day scheduled-rebalance cycle_id collision handling
**Priority:** P2 (Medium) | **Type:** Governance / Process Integrity | **Owner:** Head of Specs Team | **Source:** IDEA-challenger-20260712-01 | **Effort:** S | **Provisional-Target:** v7.10
**Problem:** `run roadmap --reason "scheduled"` invoked twice on the same calendar date produces an identical `cycle_id` (`YYYY-MM-DD__scheduled`), risking a silent overwrite of a completed Class 3 record. Confirmed in practice this cycle (`2026-07-10__scheduled` ran twice in one session as the sandbox clock advanced from 07-10 to 07-12 mid-session; resolved ad hoc via user-confirmed date resolution rather than a built-in rule).
**Scope:** Add an explicit STEP 0 rule to `roadmap_prompt.md` — detect an existing cycle folder for the computed `cycle_id` and auto-suffix (`-2`, `-3`, …) rather than requiring ad hoc user escalation.
**Acceptance Criteria:** STEP 0 rule added and versioned per `CLAUDE.md` §6; a second same-day scheduled invocation no longer requires manual disambiguation.

### BLG-QA-96 — Red Flag Journal auth regression test
**Priority:** P2 (Medium) | **Type:** QA / Security | **Owner:** Cybersecurity & Trust Lead | **Source:** IDEA-cybersecurity-20260712-01 | **Effort:** S | **Provisional-Target:** v7.10
**Problem:** `GET /portfolio/red-flag-journal` had a security review at v4.0 shipping, but no regression test confirms auth stays enforced after later, unrelated endpoint changes.
**Scope:** Add an auth-required regression test (401/403 on missing/invalid `X-API-Key`) to the backend test suite.
**Acceptance Criteria:** Test added to `backend/routers/test.py`; passes in CI; fails if auth check is removed (verified by temporarily removing it locally).

### BLG-SEC-17 — Gemini API key rotation runbook
**Priority:** P3 (Low) | **Type:** Security / Operations | **Owner:** Cybersecurity & Trust Lead | **Source:** IDEA-cybersecurity-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Gemini Flash thesis-generation wiring shipped v4.0 with no documented key-rotation runbook.
**Scope:** Document rotation steps and a recommended cadence in the security register.
**Acceptance Criteria:** Runbook added to `docs/security/api_key_security_register.md`.

### BLG-SPEC-78 — `strategy_version_at_entry` field on trade/trade_plan
**Priority:** P2 (Medium) | **Type:** Data Model / Pre-work | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260712-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** SI-04 (Strategy Version Comparison) requires version-tagged trade history, but no schema field currently captures `strategy_rules.md` version at entry time.
**Scope:** Add a `strategy_version_at_entry` field to the trade/trade_plan schema (forward-only, no backfill) ahead of SI-04 sprint planning, avoiding a later painful migration.
**Acceptance Criteria:** Migration added; field populated on new trade plans at entry; `data_model.md` updated.

### BLG-BE-58 — Position lifecycle state-transition history table
**Priority:** P3 (Low) | **Type:** Data Model / Pre-work | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260712-02 | **Effort:** M | **Provisional-Target:** Unscheduled
**Problem:** `position_lifecycle_service` tracks current state only; no historical transition log exists for post-hoc analysis.
**Scope:** Add an append-only `position_state_history` table, written on each lifecycle transition, to support future PS-04 (Strategy Decay Detection) state-conditional analysis.
**Acceptance Criteria:** Table + migration added; transitions logged; no behavioural change to current lifecycle logic.

### BLG-GOV-208 — Minimum-interval guideline between scheduled rebalances
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** 55+ completed cycles at high governance intensity, including a same-day double-run this cycle, risk operator fatigue even in a solo-plus-AI-delegation context.
**Scope:** Propose a policy guideline against same-day double scheduled-rebalance runs absent explicit cause (complements `BLG-GOV-207`'s technical fix).
**Acceptance Criteria:** Guideline documented in `claude/charter/team_charter.md` or `CLAUDE.md` §5; Director of HR + Head of Specs Team sign-off.

### BLG-GOV-209 — Frame Skill-Silo Alert as workload-composition, not just product-mix
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `roadmap_prompt.md` STEP 7.1's >40% governance ceiling is treated purely as a product-value problem; it is equally an HR/workload-composition signal for the one human operator.
**Scope:** Add an HR-perspective note to STEP 7.1's output alongside the existing PO pull-forward mechanism.
**Acceptance Criteria:** `roadmap_prompt.md` STEP 7.1 patched (versioned per `CLAUDE.md` §6); Director of HR sign-off.

### BLG-QA-97 — Retroactive Playwright §18 anti-pattern sweep (route.fallback() ordering + networkidle usage) (consolidated)
**Priority:** P2 (Medium) | **Type:** QA / Process Tooling | **Owner:** Director of Quality; QA Lead | **Source:** IDEA-director-of-quality-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Consolidates:** BLG-QA-101 — same "retroactively sweep pre-existing Playwright specs for a shared_standards.md §18 anti-pattern never audited before it was codified" mechanism, filed for a second §18 anti-pattern the same rebalance cycle (2026-07-12__scheduled) — merged 2026-07-28, session duplicate-consolidation cleanup
**Problem:** `shared_standards.md` §18 (v6.8) documents two Playwright anti-pattern fixes for new tests only — `route.fallback()` vs `route.continue()` ordering, and a ban on `waitForLoadState('networkidle')` — but existing pre-v6.8 suites were never retroactively audited for either latent pattern.
**Scope:** One-time grep-and-fix sweep of all existing spec files for (a) generic catch-all handlers using `route.continue()` ahead of a more specific handler, and (b) any remaining `networkidle` usage, replacing with an element-specific wait.
**Acceptance Criteria:** Sweep complete for both patterns; any found instances fixed; zero remaining instances of either confirmed via grep in CI or a one-time report.

### BLG-QA-98 — DoQ sign-off staleness pre-merge lint
**Priority:** P3 (Low) | **Type:** QA / Process Tooling | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Parallel-EPIC merges (per `CLAUDE.md` §8) can leave a `qa_evidence_EPIC-*.md` sign-off block at "Pending" post-merge with nothing flagging it.
**Scope:** Add a pre-merge lint/CI check that fails on residual "Pending" rows in a merged `qa_evidence_EPIC-*.md`.
**Acceptance Criteria:** Lint check added to `quality_gate.yml`; fails on a synthetic Pending-row test case.

### BLG-OPS-106 — AI cost-threshold alert value review
**Priority:** P3 (Low) | **Type:** Operations / FinOps | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `POST /ai/check-daily-cost` (v4.0) alerts on a fixed cost threshold; no review has confirmed it's still appropriate given growing SI-04-adjacent AI usage.
**Scope:** Review 90 days of actual AI spend against the current threshold; adjust if warranted.
**Acceptance Criteria:** Review documented; threshold confirmed or adjusted with rationale.

### BLG-SPEC-79 — FX handling review post-DS-05 US market source change
**Priority:** P2 (Medium) | **Type:** Spec Debt | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `strategy_rules.md` §4.1.5 currency/FX canonical rules predate DS-05's switch to Alpaca for US-market OHLCV data; no confirmation FX handling was revisited when the US data source changed.
**Scope:** Spec review confirming no silent position-sizing miscalculation for GBP-denominated accounts trading US tickers under the current data pipeline.
**Acceptance Criteria:** Review documented; §4.1.5 confirmed accurate or an amendment filed.

### BLG-GOV-210 — Governance-cycle wall-clock cost logging
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No estimate exists of session/compute time consumed per scheduled rebalance cycle, relevant given the recent same-day double-run.
**Scope:** Log start/end timestamp and step count per cycle in `run_manifest.md` (partially already present); roll up into `velocity_metrics.md`.
**Acceptance Criteria:** Logging convention documented; applied from the next cycle onward.

### BLG-GOV-211 — Effort-band accuracy retrospective
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `scored_initiatives.md` assigns S/M/L/XS effort bands at promotion time but nothing checks these against actual sprint-planning delivered effort afterward.
**Scope:** Quarterly retrospective comparing assigned effort band vs actual sprint capacity consumed for shipped initiatives.
**Acceptance Criteria:** First retrospective produced; process documented for repeat.

### BLG-SPEC-81 — Research view `signal_type` filter spec
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260712-02 | **Effort:** S | **Provisional-Target:** Unscheduled
**Gate criteria:** ≥5 distinct `signal_type` values observed in practice (currently fewer; re-check at next backlog grooming).
**Problem:** v4.1 added `signal_type` (Setup Type) to the research view with no filter/sort spec as the field accumulates distinct values.
**Scope:** Spec a filter control once the gate condition is met.
**Acceptance Criteria:** Filter spec written; gate condition re-verified before implementation.

### BLG-GOV-212 — Dry-run the cross-EPIC merge conflict runbook
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Head of Engineering | **Source:** IDEA-head-of-engineering-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `CLAUDE.md` §8's conflict-resolution convention has not been exercised in a real parallel-branch sprint in recent cycle history reviewed this session — an untested runbook risk.
**Scope:** Intentionally sequence one real 2-EPIC-parallel sprint to validate the runbook before it's needed under time pressure.
**Acceptance Criteria:** One sprint executed with genuinely parallel EPIC branches; runbook followed; gaps found are filed as follow-ups.

### BLG-FE-105 — Compliance Recheck Modal all-pass empty-state design
**Priority:** P3 (Low) | **Type:** UX / Design | **Owner:** Head of UX & Design | **Source:** IDEA-head-of-ux-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `ComplianceRecheckModal.js` (v6.9) has a documented happy-path and override-acknowledgement path per QA evidence, but no confirmed design for the all-rules-pass case.
**Scope:** Confirm/spec the all-pass empty state explicitly.
**Acceptance Criteria:** Empty-state design confirmed or specified; implemented if a gap is found.

### BLG-GOV-213 — `velocity_metrics.md` row-count audit against cycle folder count
**Priority:** P2 (Medium) | **Type:** Governance / Process Integrity | **Owner:** Infrastructure & Operations Owner | **Source:** IDEA-infra-ops-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** With the recent same-day/multi-cycle cadence, confirm `velocity_metrics.md`'s update cadence hasn't fallen behind the actual `claude/cycles/` count, which would silently corrupt STEP 1.1's rolling average.
**Scope:** One-time audit comparing `velocity_metrics.md` row count against completed release cycles in `claude/cycles/`.
**Acceptance Criteria:** Audit confirms parity or missing rows are backfilled.

### BLG-GOV-214 — Confirm Arc 5 composite formula accounts for v6.9 recheck events
**Priority:** P2 (Medium) | **Type:** Governance / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `metrics_definitions.md` v1.11's Arc 5 composite compliance formula predates v6.9's on-demand compliance-recheck event type; unclear whether recheck outcomes feed `override_rate`/`validation_pass_rate` or are invisible to them.
**Scope:** Review the v1.11 formula against v6.9's new event type; update if a gap exists.
**Acceptance Criteria:** Review documented; formula updated or confirmed already correct; Metrics Owner sign-off.

### BLG-GOV-215 — Product Value Ratio historical trend row in `velocity_metrics.md`
**Priority:** P3 (Low) | **Type:** Governance / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 2.4's Product Value Ratio is recomputed from scratch each cycle (0.26 → 0.18 → 0.21) with no first-class trend record, making the multi-cycle alert pattern harder to see at a glance.
**Scope:** Add a Product Value Ratio row to `velocity_metrics.md`, appended each time STEP 2.4 runs.
**Acceptance Criteria:** Row added retroactively for the last 3 readings; convention documented for future cycles.

### BLG-GOV-216 — Recent-rebalance recency advisory at roadmap STEP -1
**Priority:** P2 (Medium) | **Type:** Governance / Process Integrity | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260712-01 | **Effort:** S | **Provisional-Target:** v7.10
**Problem:** STEP -1.5 doesn't check inter-run recency; an accidental double-invocation of `run roadmap --reason scheduled` isn't caught until cycle-folder creation (as happened this cycle — complements `BLG-GOV-207`'s auto-suffix fix with an earlier, cheaper warning).
**Scope:** Surface a confirmation advisory at STEP -1 if `last_scheduled_rebalance_utc` is <24h old.
**Acceptance Criteria:** `roadmap_prompt.md` patched (versioned per `CLAUDE.md` §6); advisory fires correctly on a same-day re-invocation.

### BLG-GOV-217 — Surface meta-review countdown in every `run_manifest.md`
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 11.4's meta-review triggers every 3rd cycle but nothing surfaces the countdown until it fires; PMO currently computes it manually each time.
**Scope:** Surface `rebalance_cycles_since_meta_review` in every cycle's run manifest header, regardless of due status.
**Acceptance Criteria:** `roadmap_prompt.md` STEP 1.1 patched (versioned per `CLAUDE.md` §6) to include the field.

### BLG-GOV-218 — Rebalance-skip advisory should verify next release is actually scoped
**Priority:** P2 (Medium) | **Type:** Governance / Process Integrity | **Owner:** Head of Specs Team | **Source:** Post-ship closure session, cycle 2026-07-12__release-v7.0 — 2026-07-13 | **Effort:** S (~0.5 day) | **Provisional-Target:** TBD
**Problem:** `post_ship_closure.md` STEP 0's Rebalance Cadence Check recommends skipping roadmap rebalance purely on `completed_cycle_count` odd/even parity, without checking whether `current_roadmap.md` actually has a next release scoped. At the close of cycle `2026-07-12__release-v7.0` this produced a misleading advisory ("proceed directly to plan release ... no rebalance required") even though `current_roadmap.md` §1 "Next planned release" was `[TBD]` and the only STEP 8.1 Option(b) decision on record (from the `2026-07-12__scheduled` rebalance) had already been consumed by v7.0's own release planning — not a decision about what comes after v7.0. Following the advisory as given would have caused `plan release` to hit its STEP -1.2 hard gate (`release_planning_prompt.md`) with either a hard halt or a misleading mechanical pass on a stale, already-spent Option(b) record.
**Scope:**
- In `post_ship_closure.md` STEP 0's Rebalance Cadence Check, before emitting the skip advisory: check whether `current_roadmap.md` §1 "Next planned release" is populated with a real version + theme (not `[TBD]`)
- If relying on a STEP 8.1 Option(b) record instead, check whether that record postdates the release cycle just being closed (i.e. hasn't already been consumed by the cycle's own release planning)
- If neither condition holds, replace the skip advisory with a corrected warning, e.g.: "⚠ Next release not yet scoped — even though cadence suggests skipping rebalance, roadmap has no named next release and the last Option(b) decision was already consumed by this cycle's own release planning. Run `run roadmap` or record a fresh Option(a)/Option(b) scoping decision before `plan release`."
- Apply the CLAUDE.md §6 governance file edit checklist (version bump, OPERATIONAL_GUIDE.md §14 sync, prompt_change_log.md entry) to the `post_ship_closure.md` edit
**Acceptance Criteria:**
- Rebalance Cadence Check advisory logic reads `current_roadmap.md` §1 before recommending skip
- A cycle closing with an odd `completed_cycle_count` but a `[TBD]`/already-consumed next release produces the corrected warning, not the unconditional skip advisory
- A cycle closing with a genuinely fresh, unconsumed Option(b)/Option(a) scoping decision still gets the skip advisory as before (no regression)

### BLG-QA-103 — pip-audit trend log across sprint-planning runs
**Priority:** P3 (Low) | **Type:** QA / Security | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `sprint_planning_notes.md`'s Pre-Sprint Vulnerability Scan runs `pip-audit` each sprint but results aren't tracked over time to see whether the same finding recurs or is repeatedly deferred.
**Scope:** Append a running pip-audit summary log (date, findings count, resolution status) alongside `sprint_planning_notes.md`.
**Acceptance Criteria:** Log convention documented and applied from the next sprint planning onward.

### BLG-SPEC-82 — Explicit §13 continuity note for v6.9 on-demand recheck
**Priority:** P2 (Medium) | **Type:** Spec Debt / §13 Compliance | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** v6.9's on-demand compliance recheck (`BLG-FEAT-64`) re-applies SI-01's 5 rule checks on demand but has no explicit §13 PASS record of its own (unlike SI-01's original v3.8 gate) — it inherits cleared status implicitly rather than by explicit record.
**Scope:** Add a short explicit §13 continuity note confirming the on-demand recheck doesn't introduce new automation/prediction surface beyond SI-01's existing gate.
**Acceptance Criteria:** Continuity note added to `strategy_rules.md` or a linked decision doc; Strategy Rules & System Intent Owner sign-off.

---

### BLG-QA-108 — Spot-check Tier 1/Tier 2 DoQ severity-labeling consistency
**Priority:** P3 (Low) | **Type:** QA / Process | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** DoQ severity tiering (Tier 1/Tier 2) is applied per verification report without a periodic cross-report consistency check — risk of drift in how similar findings are labelled across cycles.
**Scope:** Sample the last 5 `verification_report.md` files; confirm comparable findings received comparable tier labels; document any drift found.
**Acceptance Criteria:** Spot-check completed and documented; any labelling drift found is either corrected going forward or explicitly justified.

### BLG-SPEC-85 — `trailing_stop_action_rate` spec entry with validation tolerances
**Priority:** P3 (Low) | **Type:** Spec Debt / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** v7.0's `trailing_stop_action_rate` metric instrumentation (EPIC-02 ST-07, `BLG-BE-50`) shipped without a formal `metrics_definitions.md` entry defining acceptable validation tolerances (e.g. expected range, what a stale/anomalous reading looks like).
**Scope:** Add a formal spec entry mirroring the format of other Arc 3/5 metrics already documented, including explicit validation tolerance bounds.
**Acceptance Criteria:** Entry added to `metrics_definitions.md`; tolerances stated numerically, not qualitatively.

### BLG-SPEC-86 — Formally define SI-02 condition-3 "sufficient data" threshold
**Priority:** P2 (Medium) | **Type:** Spec Debt / §13 | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260713-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** SI-02's condition (3) ("drift scores confirmed meaningful") has been re-verified live at every recent roadmap rebalance via `GET /analytics/behavioural-drift`, which self-reports `"status": "insufficient_data"` below an internal threshold — but that threshold (currently observed: still insufficient at 9 trades in a 90-day window) is not formally documented anywhere in `strategy_rules.md`. Every governed routine currently cites the API's own opaque self-report rather than a documented, independently-checkable number.
**Scope:** Document the exact trade-count/window threshold the `behavioural-drift` endpoint uses internally to move off `insufficient_data`, in `strategy_rules.md` §5 (Arc 5) or a linked spec, so future gate re-checks can compare against a stated number rather than an opaque service response.
**Acceptance Criteria:** Threshold value and window documented in a canonical spec; cross-referenced from `current_roadmap.md`'s SI-02 structured field.

### BLG-SPEC-87 — Reports.js unrealised P&L is a nightly snapshot, not live — diverges from Positions page live figure
**Priority:** P3 (Low) | **Type:** Spec Debt / Data Integrity | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** 2026-07-14__release-v7.1 EPIC-03 ST-06 (BLG-SPEC-83) reconciliation verification, deviation DEV-REPORTS-ST06-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `GET /reports/monthly-pnl` and `GET /reports/tax-year`'s `estimated_unrealised_pnl` field (`get_estimated_unrealised_pnl()`, `backend/services/reports_service.py`) sums `positions.pnl` via a raw `database.get_positions()` read — a column written once per night by `run_nightly_trailing_stop_update()`, not recomputed live. The Positions page (`GET /positions` → `get_positions_with_prices()`) computes `pnl` fresh against the current live price on every request. The two pages can show different unrealised P&L figures for the same position at the same moment, with no in-app indication that one is a snapshot. Verified in production 2026-07-14: Reports showed −£126.25 vs the Positions page's live −£115.06 for the same single open position at the same time (£11.19 gap).
**Scope:** Decide and implement one of: (a) switch `get_estimated_unrealised_pnl()` to live-compute via `get_positions_with_prices()` instead of the raw nightly-snapshot read, or (b) keep the snapshot for performance/cost reasons but add an explicit "as of last nightly update" caveat to `unrealised_note`.
**Acceptance Criteria:** Chosen direction implemented; if (a), Reports and Positions page unrealised figures match at the same moment (verified); if (b), `unrealised_note` text updated and reviewed by Head of UX & Design.

### BLG-FE-108 — GAP RISK / RISK OFF combined badge usability check
**Priority:** P3 (Low) | **Type:** Frontend / UX | **Owner:** Head of UX & Design | **Source:** IDEA-head-of-ux-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The v6.9/v7.0 combined-badge differentiation work (hue separation, `BLG-FE-104`) confirmed the two badges are *technically* visually distinguishable, but no check has confirmed users actually *understand* what each badge means at a glance (comprehension, not just contrast).
**Scope:** Run a lightweight usability check (e.g. a short comprehension-style review) on whether the GAP RISK vs RISK OFF badges are understood correctly without reading the legend.
**Acceptance Criteria:** Usability check completed and documented; any comprehension gap found is filed as a follow-up.

### BLG-OPS-109 — Confirm Render rollback runbook has real execution history
**Priority:** P2 (Medium) | **Type:** Operations / Infrastructure | **Owner:** Infrastructure & Operations Owner | **Source:** IDEA-infra-ops-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The deploy-rollback runbook has (per available records) only ever been dry-run, never executed against a real incident — its actual reliability under a live rollback is unverified. Distinct from `BLG-GOV-212` (cross-EPIC merge runbook dry-run), which covers a different artefact.
**Scope:** Either confirm a real prior rollback execution exists in history, or schedule a deliberate rollback drill against a non-production/staging deploy to validate the runbook end-to-end.
**Acceptance Criteria:** Either historical execution evidence is found and documented, or a drill is run and its outcome documented.

### BLG-GOV-219 — 3-month usage check-in for new v7.0 financial-reporting features
**Priority:** P3 (Low) | **Type:** Governance / Product Review | **Owner:** Product Owner | **Source:** IDEA-product-owner-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Gate criteria:** 3 months elapsed since v7.0 ship (2026-07-13) — clears ~2026-10-13.
**Problem:** Tax-year CSV export and realized/unrealized P&L split are newly shipped; no review is scheduled to confirm they are actually used before further investment in the same surface area.
**Scope:** After the gate clears, review usage (export download counts if available, or qualitative user check-in) and record whether further investment in this surface is warranted.
**Acceptance Criteria:** Review completed after gate date; outcome recorded (continue / deprioritise / iterate).

### BLG-GOV-220 — AI feature sunset/retirement decision criteria after negative ROI
**Priority:** P2 (Medium) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260713-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-GOV-142`'s AI feature ROI-assessment mandate defines how to evaluate an AI feature's value, but not what happens if that assessment comes back negative — there is no defined sunset/retirement decision path.
**Scope:** Extend `BLG-GOV-142`'s scope (or file as a linked companion) to define explicit retirement criteria and process for an AI feature that fails its ROI assessment.
**Acceptance Criteria:** Retirement criteria documented; explicitly linked from `BLG-GOV-142`.

### BLG-GOV-221 — AI governance operational checks: disclaimer consistency + kill-switch drill (consolidated)
**Priority:** P3 (Low) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Consolidates:** BLG-GOV-234 — GOV-234's scope ("disclaimer audit + kill-switch drill") is a superset of this item's disclaimer-only check, filed 2 days later without cross-reference — merged 2026-07-28, session duplicate-consolidation cleanup
**Problem:** Gemini thesis generation and Claude chat/briefing surfaces may carry inconsistent AI-generated-content disclaimers between the two providers. Separately, no periodic re-check exists that the AI feature global kill-switch still fully suppresses all AI calls app-wide.
**Scope:** Audit both surfaces' user-facing disclaimer language for consistency; align wording where they diverge without a documented reason. Add a kill-switch drill confirming the global AI kill-switch still fully suppresses all AI calls app-wide. Run both checks as a combined periodic review item.
**Acceptance Criteria:** Disclaimer audit completed; disclaimers aligned or divergence explicitly justified. Kill-switch drill performed at least once with findings documented; any gap filed as a follow-up.

### BLG-GOV-222 — Is the 0.30 Product Value Ratio floor durable, or a one-cycle artefact?
**Priority:** P3 (Low) | **Type:** Governance / Process Review | **Owner:** Head of Specs Team | **Source:** IDEA-challenger-20260713-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** After 3 consecutive Product Value Alerts (0.26→0.18→0.21), this cycle's ratio moved to 0.33 (Advisory), driven heavily by one unusually U-heavy release (v7.0, 8/15 stories). Whether the 0.30 floor is a durable, achievable target or was cleared by one favourable release composition is untested.
**Scope:** Revisit at the next 1-2 cycles' readings; if the ratio drops back below 0.30 immediately, treat this as evidence the floor needs a different calculation basis (e.g. a rolling average rather than a 5-cycle window) rather than a genuine behavioural shift.
**Acceptance Criteria:** Tracked explicitly at the next 2 roadmap rebalances; a written verdict recorded either way.

### BLG-GOV-223 — Is Arc 6 realistically reachable at current trade volume?
**Priority:** P3 (Low) | **Type:** Governance / Roadmap Review | **Owner:** Head of Specs Team | **Source:** IDEA-challenger-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Arc 6 (Performance Science) features gate on 50-100+ trades and 12-18+ months of history. At the current observed rate (~1-2 trades/month, 20 closed trades total), several Arc 6 gates are multiple years away. Adjacent to `BLG-GOV-196` (sunset review for Priority 3 — Deferred initiatives) but argues for an explicit reachability verdict on Arc 6 specifically rather than a general sunset process.
**Scope:** Compute a realistic ETA for each Arc 6 gate at current trade velocity; if any exceed ~3 years, flag explicitly to Product Owner for a named decision (keep as aspirational vs. formally deprioritise).
**Acceptance Criteria:** ETA computed per Arc 6 feature; PO decision recorded for any exceeding 3 years.

### BLG-GOV-224 — Skill-Silo Alert: structured cross-role review-rotation pilot
**Priority:** P3 (Low) | **Type:** Governance / HR Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260713-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** The Skill-Silo Alert (>40% governance/debt story share) has fired for many consecutive cycles; the only structural remedy exercised so far is single-item U-story pull-forward, which the engine's own documentation notes is not reliably sufficient.
**Scope:** Design a lightweight pilot where a subset of governance/debt-shaped backlog items are deliberately reviewed or scoped by a role outside their usual owner, to test whether cross-role rotation reduces the governance-story share over time.
**Acceptance Criteria:** Pilot design documented; if run, outcome recorded against the next 3-cycle Skill-Silo rolling average.

### BLG-GOV-225 — Role succession/handoff checklist
**Priority:** P3 (Low) | **Type:** Governance / HR Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-GOV-183`'s onboarding template covers bringing a new role in, but not the reverse case — a structured handoff when a role's responsibilities transfer.
**Scope:** Author a succession/handoff checklist complementing the existing onboarding template.
**Acceptance Criteria:** Checklist authored; explicitly cross-referenced from `BLG-GOV-183`.

### BLG-GOV-226 — Enforce P2 deviation target-release commitments at sprint planning
**Priority:** P2 (Medium) | **Type:** Governance / Process Integrity | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260713-01, IDEA-head-of-engineering-20260713-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Accepted P2 deviations (e.g. `DEV-EPIC01-ST05-01`, target v7.1) name a target release but nothing in `sprint_planning_prompt.md` currently checks, at the next sprint planning gate, whether a deviation whose named target release has arrived is actually being scheduled. Two complementary gaps: (a) DoQ-side — no gate enforcement at sprint planning; (b) engineering-side — no checklist item at sprint planning intake surfacing carried-forward deviations for scheduling.
**Scope:** Add both: (a) a DoQ-owned gate check in `sprint_planning_prompt.md` cross-referencing open deviations against the release being planned; (b) an engineering-side intake checklist item surfacing the same list for scoping.
**Acceptance Criteria:** `sprint_planning_prompt.md` patched (versioned per `CLAUDE.md` §6) with both the gate check and checklist item; a deviation with an arrived target release is either scheduled or explicitly re-targeted with rationale, not silently dropped.

### BLG-GOV-227 — Governance overhead trend-over-time across all 56 completed cycles
**Priority:** P3 (Low) | **Type:** Governance / Process Analytics | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260713-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Individual cycles' governance overhead (tool calls, session time, artefact count) is implicitly visible per-cycle but no trend view exists across the full 56-cycle history to show whether overhead is growing, shrinking, or stable as the governance stack has grown.
**Scope:** Compile a lightweight trend summary (e.g. artefact count per cycle, prompt version-bump frequency) across available cycle records.
**Acceptance Criteria:** Trend summary produced; any notable trend (e.g. accelerating governance file growth) flagged to Head of Specs Team.

### BLG-GOV-228 — Periodic engineering-owned architecture health review
**Priority:** P3 (Low) | **Type:** Governance / Engineering Process | **Owner:** Head of Engineering | **Source:** IDEA-head-of-engineering-20260713-02 | **Effort:** M | **Provisional-Target:** TBD
**Gate criteria:** Annual cadence (first due 2027-07-13), same pattern as `BLG-GOV-144`.
**Problem:** `backend/services/`, `backend/routers/`, and `database.py` have grown substantially across 56 cycles with no periodic engineering-owned review of structural health (module size, coupling, duplicated patterns).
**Scope:** Define and schedule an annual architecture health review, first due 2027-07-13.
**Acceptance Criteria:** Review cadence documented; first review scheduled.

### BLG-GOV-229 — Consolidate spec-freshness checks into one dashboard artefact
**Priority:** P3 (Low) | **Type:** Governance / Process Tooling | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260713-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** `BLG-GOV-171`, `BLG-GOV-191`, and `BLG-GOV-192` each independently track a spec-freshness concern; no single artefact shows their combined status.
**Scope:** Consolidate the three items' tracking into one dashboard-style artefact; the three underlying backlog items remain but gain a shared status view.
**Acceptance Criteria:** Consolidated artefact created; cross-referenced from all three source items.

### BLG-GOV-230 — Quarterly spec-vs-shipped-code reconciliation sweep
**Priority:** P3 (Low) | **Type:** Governance / Process Tooling | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260713-02 | **Effort:** M | **Provisional-Target:** TBD
**Gate criteria:** Quarterly cadence (first due ~2026-10-13).
**Problem:** Individual spec-drift gaps are caught reactively (e.g. this cycle's `BLG-SPEC-83`/`84`/`85`) rather than via a scheduled proactive sweep.
**Scope:** Define and schedule a quarterly sweep comparing frontend specs against shipped `src/pages/` behaviour.
**Acceptance Criteria:** Sweep procedure documented; first run scheduled.

### BLG-GOV-231 — Track empty-Now-horizon streak counter
**Priority:** P3 (Low) | **Type:** Governance / Process Tooling | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260713-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The Product Value Alert streak is tracked explicitly cycle-to-cycle; the empty-Now-horizon pattern (resolved this cycle after 2+ consecutive occurrences) has no equivalent explicit counter, relying on manual prose review of prior cycles.
**Scope:** Add an explicit streak counter for consecutive empty-Now-horizon cycles alongside the existing Product Value Alert tracking, in `roadmap_prompt.md`'s STEP -1.7 Governance Health Score or STEP 8.1.
**Acceptance Criteria:** `roadmap_prompt.md` patched (versioned per `CLAUDE.md` §6) to track and surface the counter each run.

### BLG-GOV-232 — Track idea register open-row depth trend across cycles
**Priority:** P3 (Low) | **Type:** Governance / Process Tooling | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The open (Submitted/Parked-cycle-n) row count in `ideas_register.md` is checked as a threshold gate (STEP -1.6, <20) each cycle but no trend view shows whether it's growing or shrinking over time.
**Scope:** Add a lightweight trend note (open-row count per cycle) alongside the existing housekeeping/rebalance outcome logging.
**Acceptance Criteria:** Trend note added and populated retroactively where cycle records allow.

### BLG-GOV-233 — Governance overhead cost tracking per scheduled rebalance
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260710-01 (mandatory Parked-cycle-3 disposition, §4.5) | **Effort:** S | **Provisional-Target:** TBD
**Gate criteria:** 3 consecutive scheduled-rebalance cycles' recorded cost/effort data — evaluated directly, independent of whether `roadmap_prompt.md` STEP 0.C's abbreviated-manifest exception ever lands (that dependency proved unreliable as a trigger across 4+ carried cycles, 2026-07-08 through 2026-07-13).
**Problem:** No per-cycle cost/effort tracking exists for scheduled roadmap rebalances specifically (as distinct from completion-triggered runs), despite this being the highest-frequency governed routine.
**Scope:** Record a lightweight cost/effort note (e.g. tool-call count, session duration if available) at the close of each scheduled rebalance for 3 consecutive cycles, then assess whether a permanent tracking mechanism is warranted.
**Acceptance Criteria:** 3 consecutive scheduled cycles' data recorded; a written yes/no decision on permanent tracking follows.

---

### BLG-SPEC-88 — OpenAPI response-example drift spot-check
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260715-01 | **Effort:** S (~0.5-1 day) | **Provisional-Target:** TBD
**Problem:** The CI OpenAPI Drift Detection gate checks structural presence of endpoints but not whether documented example payloads in `openapi.yaml` still match live response shapes.
**Scope:** Spot-check a sample of documented examples against live responses; file individual `BLG-SPEC-*` items for any drift found.
**Acceptance Criteria:** Sample check performed and documented; drift (if any) filed as follow-up items.

### BLG-GOV-235 — Idea-intake minimum-submission flex condition
**Priority:** P3 (Low) | **Type:** Governance | **Owner:** Head of Specs Team | **Source:** IDEA-director-of-hr-20260715-01 | **Effort:** S | **Provisional-Target:** TBD
**Gate criteria:** Recurs at 3+ consecutive scheduled cycles where the Now horizon is already populated with 3+ ad-hoc (non-governed-cycle) P1 items at window-open — not yet met (this is the 1st such occurrence).
**Problem:** `idea_intake_prompt.md`'s standing 2-net-new-ideas-per-agent minimum does not flex when the Now horizon is already saturated with ad-hoc additions, potentially generating submissions redundant with just-added scope.
**Scope:** If the gate condition recurs, evaluate whether the minimum should reduce or the window should skip agents whose domain is already covered by the ad-hoc additions.
**Acceptance Criteria:** Gate re-checked each scheduled cycle; a written decision follows once met.

### BLG-QA-109 — DoQ sign-off template alignment check (FI-P3-02 wording-only exception)
**Priority:** P3 (Low) | **Type:** QA / Governance | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260715-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No recent confirmation that the DoQ sign-off block template still correctly reflects CLAUDE.md's FI-P3-02 wording-only exception (code review may substitute for staging sign-off only for non-visual, wording-only ACs).
**Scope:** Compare current DoQ sign-off block template/practice against the CLAUDE.md FI-P3-02 clause; correct if drifted.
**Acceptance Criteria:** Comparison performed; template confirmed current or corrected.

### BLG-QA-110 — Recurring CSV export content regression check
**Priority:** P3 (Low) | **Type:** QA | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260715-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-SPEC-84`/`BLG-QA-106` (v7.1) hardened CSV export content validation, but no recurring check exists to catch regressions as new fields are added to the export over time.
**Scope:** Add a lightweight recurring (e.g. quarterly) regression check that CSV export content stays correct.
**Acceptance Criteria:** Recurring check scoped and scheduled; first instance run clean or findings filed.

### BLG-GOV-237 — SI-02 trade-count gate threshold calibration review
**Priority:** P3 (Low) | **Type:** Governance / Strategy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260715-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** SI-02's 11-linked-trade-plan gate threshold has sat at 0/11 for a near-full quarter (unchanged 2026-07-06 through 2026-07-15 across 5 live re-checks); no review has confirmed the threshold itself is still the right calibration point versus the linkage-UX root cause `BLG-FE-109` now targets.
**Scope:** Review whether the 11-trade-plan threshold remains appropriate once `BLG-FE-109` ships and linkage friction is removed, or whether the threshold should be reconsidered independently.
**Acceptance Criteria:** Review performed after `BLG-FE-109` ships (or at next scheduled rebalance if not shipped within 2 cycles); written conclusion recorded.

### BLG-GOV-238 — Governed-vs-ad-hoc backlog scope visibility
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** PMO Lead; FinOps & Resource Architect | **Source:** IDEA-challenger-20260715-02, IDEA-pmo-lead-20260715-01, IDEA-finops-20260715-02 (3-idea consolidation per STEP 4.2 Idea Consolidation convention) | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Three independent submissions this window flagged the same underlying pattern from different angles: 5 P1 items were added to `backlog.md` outside a governed cycle in the session immediately preceding this rebalance (a 2nd occurrence of ad-hoc additions bypassing governed release scoping, per the Challenger's framing), with no lightweight tracking of governed-cycle-added vs. ad-hoc session-added items per release, nor visibility into whether ad-hoc additions are displacing gated/scored capacity.
**Scope:** Add a lightweight running tally (e.g. a count/tag in each cycle's `run_manifest.md` or `cycle_summary.md`) distinguishing governed-cycle additions from ad-hoc session additions per release, to give FinOps/PMO Lead visibility into the trend.
**Acceptance Criteria:** Tally mechanism scoped; first data point recorded retroactively for v7.1/this cycle where determinable.

### BLG-OPS-111 — Reconcile 21 endpoints missing from api_performance_baseline.md (post-ship closure 2026-07-15 drift check)
**Priority:** P3 (Low) | **Type:** Operations / Performance Baseline | **Owner:** Infrastructure & Operations Owner | **Source:** post-ship closure 2026-07-15__release-v7.2 STEP 6 Endpoint Coverage Drift Check | **Effort:** M (~2-3 days — 21 endpoints) | **Provisional-Target:** Before next performance baseline review
**Problem:** `docs/reference/openapi.yaml` has 100 registered path+method combinations; `docs/ops/api_performance_baseline.md` has measurement rows for 91 (after normalising path-param name differences), leaving 21 endpoints with no recorded p50/p95 baseline: `GET /analytics/market-correlation`, `GET /analytics/metrics`, `GET /analytics/strategy-version-comparison`, `GET /analytics/tag-performance`, `GET /portfolio/pre-entry-validation`, `GET /positions/analyze`, `GET /positions/grace-period-alerts`, `GET /positions/tags`, `GET /positions/{id}`, `GET /positions/{id}/stop-trail`, `GET /trade-plans/tags`, `GET /v1beta1/news`, `GET /v2/stocks/{symbol}/bars`, `POST /ai/check-daily-cost`, `POST /positions/nightly-stop-update`, `POST /positions/risk-off-alerts`, `POST /positions/{id}/refresh-state`, `POST /signals/rebalance-exit`, `POST /strategy/benchmark/import`, `POST /test/endpoints`, `POST /trade-plans/generate-plan`. None of these were introduced by v7.2 (zero backend routes shipped this cycle — all 5 deliverables were doc/spec artefacts) — this is accumulated drift from prior cycles. `BLG-OPS-13` is a pre-existing rolling tracking item for this same pattern but its own scope list (v2.8–v4.6 endpoints) is stale against the current gap — several of its listed endpoints are now present in the baseline while the 21 above are not yet reflected in it.
**Scope:** Run each of the 21 endpoints against staging/production to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`; reconcile/supersede `BLG-OPS-13`'s stale endpoint list in the same pass rather than maintaining two parallel tracking items.
**Acceptance Criteria:** All 21 endpoints have p50/p95 latency entries in the baseline document, consistent with existing measurement methodology; `BLG-OPS-13` disposition (close as superseded, or merge remaining-still-missing items from its list into this one) recorded.

---

### BLG-OPS-112 — AI endpoint (daily-briefing/chat) cost & latency drift monitoring
**Priority:** P3 (Low) | **Type:** Operations / AI Governance | **Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner | **Source:** IDEA-ai-compliance-20260716-01 | **Effort:** S (~1 day) | **Provisional-Target:** TBD
**Problem:** `POST /ai/daily-briefing` and `POST /ai/chat` have per-call cost tracking (`gemini_audit_log`/Anthropic usage logging) but no rolling anomaly check — a latency or cost regression would only surface via manual review, not an alert.
**Scope:** Extend existing cost-tracking infrastructure with a rolling anomaly check (e.g. week-over-week cost/latency delta threshold) for the two AI endpoints.
**Acceptance Criteria:** Anomaly check scoped and added; confirmed to fire on a simulated cost/latency spike.

---

### BLG-FEAT-78 — Trade-tag/trigger-source column on tax-year P&L CSV export
**Priority:** P3 (Low) | **Type:** Product Feature / Reporting, gate-conditional | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260716-01 | **Effort:** S (~1 day) | **Provisional-Target:** TBD
**Gate criteria:** `BLG-FE-116` (custom price alerts) ships — no trigger-source data exists to export until an alert-triggered trade path exists.
**Problem:** The tax-year P&L CSV export (shipped v7.0, hardened v7.1) has no column distinguishing trades opened via a system-surfaced trigger (e.g. a future price alert) from manually-initiated trades, which will become a reporting gap once `BLG-FE-116` ships.
**Scope:** Add a trigger-source column to the CSV export once alert-triggered trades exist to populate it.
**Acceptance Criteria:** CSV export includes a trigger-source column; column populated correctly for both alert-triggered and manual trades.

---

## Roadmap Rebalance 2026-07-24__scheduled — New Items (IW-20260724-01 disposition)

*34 items added via idea intake IW-20260724-01 STEP 4 disposition (Backlog). Source ideas and full rationale: `claude/ideas/ideas_register.md` (2026-07-24 rows), `claude/ideas/window_summary_IW-20260724-01.md`. DL-075.*

### BLG-BE-70 — Log AI model+version provenance on stored thesis/summary text
**Priority:** P3 (Low) | **Type:** Backend / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260724-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Stored AI-generated thesis/summary text has no field recording which model+version produced it, complicating retroactive audit if model behaviour is later questioned.
**Scope:** Add a model/version provenance field to the relevant storage table(s), populated at write time.
**Acceptance Criteria:** New field present and populated on all newly-created AI-generated records; existing records unaffected (no backfill required).

---

### BLG-SPEC-96 — API endpoint deprecation-window policy
**Priority:** P3 (Low) | **Type:** Spec Debt / API Governance | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260724-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No documented policy exists for how long a deprecated endpoint remains available before removal, leaving each removal decision ad hoc.
**Scope:** Author a deprecation-window policy section in API contract documentation standards.
**Acceptance Criteria:** Policy section added; Head of Specs Team sign-off.

---

### BLG-FE-124 — Reusable Base44 prompt fragment library for common layouts
**Priority:** P2 (Medium) | **Type:** Frontend / Technical Debt | **Owner:** Base44 Frontend Prompt Owner | **Source:** IDEA-base44-frontend-20260724-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Common card/empty-state/loading-skeleton layout prompts are re-authored per page rather than drawing from a shared fragment library, contributing to visual drift across pages.
**Scope:** Extract the most-repeated layout prompt fragments into `base44_prompt_template_library.md`.
**Acceptance Criteria:** Library extended with at least 3 new reusable fragments; referenced by at least one new story going forward.

---

### BLG-SPEC-97 — Formal schema-versioning doc for trade_plan/position tables
**Priority:** P3 (Low) | **Type:** Spec Debt / Data Model | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260724-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** `trade_plan`/`position` table migration history is reconstructable from git history but not documented as a single canonical versioning reference.
**Scope:** Author a schema-versioning doc covering migration history and field deprecation for these two tables.
**Acceptance Criteria:** Doc created; Data Model Owner sign-off.

---

### BLG-GOV-252 — Data-retention policy for closed-trade and journal records
**Priority:** P3 (Low) | **Type:** Governance / Data Model | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260724-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No retention policy exists for closed-trade and journal records; at current trade volume this is low-urgency but undefined.
**Scope:** Define archival-vs-deletion policy ahead of long-term data growth.
**Acceptance Criteria:** Policy documented; no implementation required until data volume warrants action.

---

### BLG-GOV-253 — Onboarding checklist for new governance agent roles
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260724-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Each new governance agent role (`claude/agents/*.md`) is created ad hoc with no standard checklist of required charter fields, write-scope declarations, or review cadence.
**Scope:** Document a standard onboarding checklist for new agent role creation.
**Acceptance Criteria:** Checklist added to `claude/charter/` or `claude/system/`; Head of Specs Team sign-off.

---

### BLG-GOV-254 — Minimum capacity buffer floor recommendation for sprint planning
**Priority:** P2 (Medium) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260724-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Sprint planning has landed at the top of the capacity band with zero buffer at least once (v7.1, per `2026-07-14__release-v7.1` closure carry-forward), with no documented minimum-buffer recommendation to guard against recurrence.
**Scope:** Propose a minimum capacity buffer floor (e.g. a percentage of confirmed capacity) for `sprint_planning_prompt.md` STEP 4.5 to reference.
**Acceptance Criteria:** Recommendation documented; FinOps & Resource Architect + PMO Lead sign-off.

---

### BLG-SPEC-98 — Consolidate duplicate empty-state pattern specs
**Priority:** P3 (Low) | **Type:** Spec Debt / Frontend | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260724-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Empty-state pattern definitions (the `DataState` pattern formalised in `design_system.md` v1.1, per v7.2) are restated with minor variation across multiple page specs rather than referencing one canonical definition.
**Scope:** Consolidate empty-state pattern definitions into `design_system.md`; update page specs to reference rather than restate.
**Acceptance Criteria:** Duplicate definitions removed from at least 3 page specs; `design_system.md` remains the single source.

---

### BLG-SPEC-99 — Keyboard-navigation requirements section for table-based page specs
**Priority:** P3 (Low) | **Type:** Spec Debt / Accessibility | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260724-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Table-based page specs (Positions, Trades, Red Flag Journal) have no documented keyboard-navigation requirements, leaving the expected behaviour implicit.
**Scope:** Add a keyboard-navigation requirements section to the relevant page specs.
**Acceptance Criteria:** Section added to at least Positions, Trades, and Red Flag Journal specs.

---

### BLG-OPS-116 — Quarterly dependency-upgrade cadence for backend/requirements.txt
**Priority:** P2 (Medium) | **Type:** Operations / Technical Debt | **Owner:** Head of Engineering | **Source:** IDEA-head-of-engineering-20260724-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Backend dependency upgrades currently happen reactively (e.g. the starlette CVE remediation, v4.0) rather than on a defined cadence, risking CVE backlog accumulation.
**Scope:** Define a quarterly review cadence for `backend/requirements.txt` dependency versions.
**Acceptance Criteria:** Cadence documented; first review scheduled.

---

### BLG-FE-126 — Unified loading-skeleton pattern for async-loading cards
**Priority:** P3 (Low) | **Type:** Frontend / Design System | **Owner:** Head of UX & Design | **Source:** IDEA-head-of-ux-20260724-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Async-loading cards use inconsistent spinner/blank-state treatments across pages rather than one shared loading-skeleton pattern.
**Scope:** Define a unified loading-skeleton pattern in `design_system.md`; apply to new cards going forward.
**Acceptance Criteria:** Pattern documented; not required to retrofit all existing cards in one pass.

---

### BLG-OPS-118 — CI cache tuning to reduce Playwright suite runtime
**Priority:** P2 (Medium) | **Type:** Operations / CI | **Owner:** Infrastructure & Operations Owner | **Source:** IDEA-infra-ops-20260724-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The Playwright suite has grown with each release's added test scenarios (70+ spec files as of v7.6, per `BLG-QA-116`); CI runtime has grown correspondingly with no caching optimisation pass.
**Scope:** Review and tune CI caching (dependency install, browser binaries) for the Playwright job.
**Acceptance Criteria:** Measurable CI runtime reduction on the Playwright job; no test reliability regression.

---

### BLG-SPEC-100 — Canonical "win rate" vs "hit rate" definitions doc
**Priority:** P3 (Low) | **Type:** Spec Debt / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260724-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** "Win rate" and "hit rate" terminology is used inconsistently across specs (`metrics_definitions.md` and page specs) without a single canonical distinction.
**Scope:** Add canonical definitions for both terms to `metrics_definitions.md`; audit existing specs for inconsistent usage.
**Acceptance Criteria:** Canonical definitions added; at least the highest-traffic specs (Performance Analytics, Reports) reconciled to use them consistently.

---

### BLG-FEAT-83 — Cohort-based (setup/signal type) performance metric
**Priority:** P3 (Low) | **Type:** Product Feature / Analytics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260724-02 | **Effort:** M | **Provisional-Target:** TBD
**Gate criteria:** Sufficient `setup_type`/signal-type diversity in closed-trade history to produce a meaningful cohort split (same data-density concern as `BLG-FEAT-62`).
**Problem:** Performance Analytics has no cohort-based (grouped by setup/signal type) performance metric, despite the underlying `signal_type` field being captured since the Research view shipped it (v4.1).
**Scope:** Add a cohort-based performance metric to Performance Analytics, building on the existing Arc 5 compliance analytics layer.
**Acceptance Criteria:** Metric available once gate clears; at least 3 distinct cohorts represented.

---

### BLG-QA-120 — Test-tagging convention (smoke/regression/critical) for selective CI runs
**Priority:** P2 (Medium) | **Type:** QA / Process | **Owner:** QA Lead | **Source:** IDEA-qa-lead-20260724-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** The Playwright suite always runs in full; no tagging convention exists to allow selective (e.g. smoke-only) runs for faster feedback on lower-risk changes.
**Scope:** Define and apply a tagging convention (smoke/regression/critical) to the existing suite; wire selective-run capability into CI where useful.
**Acceptance Criteria:** Tagging convention documented; applied to at least the smoke-tier subset.

---

### BLG-QA-121 — Synthetic trade-history data generator for gated-feature testing
**Priority:** P2 (Medium) | **Type:** QA / Test Tooling | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260724-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Gated features (Setup Quality Score, SI-02 frontend) can only be tested end-to-end once real trade volume clears their gates, slowing test development for features that are otherwise implementation-ready.
**Scope:** Build a synthetic trade-history generator producing realistic (non-production) data satisfying gate thresholds, for use in test environments only.
**Acceptance Criteria:** Generator produces data satisfying at least the SI-02 and Setup Quality Score gate thresholds; clearly scoped/labelled as test-only, never usable against production.

---

### BLG-GOV-255 — Periodic §13 boundary review cadence tied to SI-02's gate history
**Priority:** P3 (Low) | **Type:** Governance / Strategy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260724-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** SI-02's gate has now returned NOT MET across 9+ consecutive re-checks; while this is a data-density issue rather than a §13 issue, no periodic review formally confirms that distinction continues to hold as the system evolves.
**Scope:** Define a periodic (e.g. every 10th consecutive identical gate reading) §13 boundary review checkpoint tied to SI-02's gate history specifically.
**Acceptance Criteria:** Review cadence documented; Strategy Rules & System Intent Owner sign-off.

---

### BLG-SPEC-101 — Worked example of the ATR-based sizing edge case in strategy_rules.md
**Priority:** P3 (Low) | **Type:** Spec Debt / Strategy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260724-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Several backlog items reference an ATR-based sizing edge case informally without a canonical worked example in `strategy_rules.md` itself.
**Scope:** Add a worked numerical example of the edge case to `strategy_rules.md`.
**Acceptance Criteria:** Worked example added; Strategy Rules & System Intent Owner sign-off; no functional/behavioural change (documentation only).

---

### BLG-QA-122 — Broker statement reconciliation (blocked — no broker import mechanism)
**Priority:** P3 (Low) | **Type:** QA / Financial Reporting, gate-conditional | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260724-02 | **Effort:** M | **Provisional-Target:** TBD
**Gate criteria:** A broker statement import mechanism exists. Per `current_roadmap.md` §2 Product Scope Exclusions, "Broker API integration (execution)" is currently a deferred (not strategically excluded) exclusion — no import path exists today for this item to reconcile against.
**Problem:** Idea proposed a reconciliation check between journal/trade entries and broker statement data, but no broker statement import mechanism currently exists to reconcile against.
**Scope:** Deferred until broker integration (or a manual statement upload path) exists.
**Acceptance Criteria:** N/A until gate clears.

---

---

## Delivery Verification 2026-07-24__release-v7.8 — New Items

*Doc-completeness findings surfaced while authoring `tests/test_pilot_contract_schemas.py` (EPIC-11/ST-11), recorded but not fixed in that story per its own scope boundary (adding contract tests, not auditing existing contract docs) — see `qa_evidence_EPIC-11.md`. None are P0/P1; no caller-relied-upon field is missing from any real response.*

### BLG-SPEC-102 — `position_endpoints.md` envelope claim doesn't match live `GET /positions` behaviour
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** API Contracts & Documentation Owner | **Source:** `2026-07-24__release-v7.8` EPIC-11 ST-11 pilot contract test authoring (`qa_evidence_EPIC-11.md`) | **Effort:** XS | **Provisional-Target:** v7.10
**Problem:** `docs/specs/api_contracts/position_endpoints.md` documents `GET /positions` as returning the standard `{status, data}` envelope, but the live endpoint returns a raw list (confirmed via `tests/test_api_contracts.py::test_get_positions_returns_ok`'s own comment and re-confirmed by `tests/test_pilot_contract_schemas.py`). Doc/reality mismatch only — the pilot contract test asserts the real (unenveloped) behaviour, not the doc's claim.
**Scope:** Update `position_endpoints.md` to document the actual (unenveloped) response shape for `GET /positions`.
**Acceptance Criteria:** `position_endpoints.md` corrected to match live behaviour; API Contracts & Documentation Owner sign-off; no functional change.

---

### BLG-SPEC-103 — `GET /positions` undocumented lifecycle fields (`position_state`, `state_entered_at`, `days_in_state`)
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** API Contracts & Documentation Owner | **Source:** `2026-07-24__release-v7.8` EPIC-11 ST-11 pilot contract test authoring (`qa_evidence_EPIC-11.md`) | **Effort:** XS | **Provisional-Target:** v7.10
**Problem:** `GET /positions` merges in 3 fields via `get_lifecycle_fields_for_position()` (`position_state`, `state_entered_at`, `days_in_state`) that are absent from `docs/specs/api_contracts/position_endpoints.md`'s documented response shape.
**Scope:** Add the 3 fields to `position_endpoints.md`'s response schema with type/description.
**Acceptance Criteria:** All 3 fields documented; API Contracts & Documentation Owner sign-off; no functional change.

---

### BLG-SPEC-104 — `trade_endpoints.md` JSON example omits documented fields (`commission_gbp`, `spread_cost_gbp`, `net_r_multiple`)
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** API Contracts & Documentation Owner | **Source:** `2026-07-24__release-v7.8` EPIC-11 ST-11 pilot contract test authoring (`qa_evidence_EPIC-11.md`) | **Effort:** XS | **Provisional-Target:** v7.10
**Problem:** `docs/specs/api_contracts/trade_endpoints.md`'s JSON example for `GET /trades` omits `commission_gbp`, `spread_cost_gbp`, `net_r_multiple` — fields documented in the same file's Field notes table and always returned by the live service. Example-completeness gap only, not a schema gap.
**Scope:** Update the JSON example to include all 3 fields.
**Acceptance Criteria:** Example updated to include all 3 fields; API Contracts & Documentation Owner sign-off; no functional change.

---

## Roadmap Rebalance 2026-07-27__scheduled — New Items (IW-20260727-01 disposition)

*21 items added from `IW-20260727-01`'s 44 submissions (22 agents × 2 ideas). 23 submissions rejected — not strong, the large majority as duplicates of existing open backlog items surfaced by the mandatory STEP 4.0/§2.0.5 backlog-overlap check (this backlog has run 20+ idea-intake cycles and is now heavily saturated for "obvious" governance/process-improvement topics — see `lessons_learnt.md` for the resulting process observation). Full disposition: `claude/ideas/ideas_register.md` (2026-07-27 rows).*

### BLG-GOV-259 — Quarterly retrospective: estimated vs. actual effort bands (§16.7)
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260727-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `scored_initiatives.md` Effort Band (§16.7) and `backlog.md` Effort day-ranges (§16.12) are assigned at promotion time but never checked back against actual delivery time — no feedback loop exists to calibrate future estimates.
**Scope:** Add a quarterly (or every-N-cycle) retrospective comparing estimated effort bands to actual sprint-close data.
**Acceptance Criteria:** Retrospective cadence documented; FinOps & Resource Architect sign-off.

---

### BLG-GOV-260 — Retire stale `RA:` roadmap-annotation markers older than 3 releases
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `current_roadmap.md` §3 accumulates `RA:` retirement markers indefinitely (18+ visible as of this cycle, back to v5.0) with no defined pruning rule — each is a one-line pointer to `roadmap_archive.md`, so retaining very old ones adds document length without adding information not already in the archive.
**Scope:** Define a rule (e.g. `manage roadmap` STEP N) to prune `RA:` markers older than 3 releases, since the archive itself remains the permanent record.
**Acceptance Criteria:** Rule documented in `roadmap_management_prompt.md`; Head of Specs Team sign-off.

---

### BLG-FE-131 — Design-gate checklist addendum for motion/timing-sensitive chart interactions
**Priority:** P3 (Low) | **Type:** Frontend / Design | **Owner:** Head of UX & Design | **Source:** IDEA-head-of-ux-20260727-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `design_gate_prompt.md`'s classification checklist has no explicit item for motion/timing-sensitive interactions (e.g. chart transition animations, tooltip delay timing), which fall through the cracks between "visual rendering" and "interaction" categories.
**Scope:** Add an explicit motion/timing-sensitive interaction checklist item to the design gate classification table.
**Acceptance Criteria:** Checklist item added; Head of UX & Design sign-off.

---

### BLG-OPS-122 — CI runner cache warm-up for `backend/.venv` to cut pytest job time
**Priority:** P3 (Low) | **Type:** Ops / CI | **Owner:** Infrastructure & Operations Owner | **Source:** IDEA-infra-ops-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** CI installs `backend/requirements.txt` fresh into each runner on every workflow invocation (per `CLAUDE.md` §9's own description of current CI behaviour) — no dependency cache is used, adding avoidable install time to every run.
**Scope:** Add a cache step (keyed on `requirements.txt` hash) for `backend/.venv` in the relevant GitHub Actions workflows.
**Acceptance Criteria:** Cache step added; measured CI job time reduction; Infrastructure & Operations Owner sign-off.

---

### BLG-FEAT-86 — Drift-detection metric for the behavioural-drift endpoint's `insufficient_data` streak
**Priority:** P3 (Low) | **Type:** Feature / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `GET /analytics/behavioural-drift` has returned `insufficient_data` across 9+ consecutive live re-checks (per the SI-02 gate note in `current_roadmap.md` §5) with no metric tracking how long the streak has persisted or when it's likely to clear.
**Scope:** Add a simple streak-length metric (consecutive `insufficient_data` readings, trade-count trend) surfaced alongside the existing gate note.
**Acceptance Criteria:** Metric defined and documented; Metrics Definitions & Analytics Canonical Owner sign-off.

---

### BLG-GOV-261 — Lightweight due-date index for outstanding deferred-patch reminders across cycles
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Deferred patches are tracked individually within each cycle's `lessons_learnt.md`, requiring STEP -1.5 to re-read the immediately prior cycle's file each time — there is no single cross-cycle index of "what's due when," which is exactly the class of gap that let a v7.6-sourced Recurrence Escalation go unresolved for 2 further cycles (see this cycle's STEP -1.7 finding).
**Scope:** Add a lightweight append-only index file listing every open deferred patch, its target, and owner, updated whenever one is filed or resolved.
**Acceptance Criteria:** Index file created and documented; PMO Lead sign-off.

---

### BLG-QA-126 — Snapshot test for `SystemStatus.js` hardcoded fallback counts
**Priority:** P3 (Low) | **Type:** QA Process / Tooling | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `CLAUDE.md` §2 requires `SystemStatus.js`'s hardcoded `Tests {totalTests || 'N'} endpoints` fallback (and `SC-SS-01b` in `tests/e2e/system-status.spec.js`) to be updated whenever the endpoint test count changes — currently manual, with no automated check that the hardcoded value still matches the derivable total.
**Scope:** Add a snapshot/assertion test comparing the hardcoded fallback value against an AST-derived count of registered endpoint tests.
**Acceptance Criteria:** Test added; fails on a deliberately-stale fallback value; QA & Testing Owner sign-off.

---

### BLG-GOV-262 — Formalise a data-volume threshold trigger for the §12.2 "elements that may change" review
**Priority:** P3 (Low) | **Type:** Governance / Strategy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `strategy_rules.md` §12.2 lists elements that may change as trade-history volume grows, but does not name a specific volume threshold that should trigger a formal review — review timing is currently ad hoc.
**Scope:** Define an explicit trade-count (or time-based) threshold that triggers a §12.2 review.
**Acceptance Criteria:** Threshold documented in §12.2; Strategy Rules & System Intent Owner sign-off.

---

### BLG-GOV-263 — Structural fix for recurring cross-EPIC `execution_state.json` merge-conflict pattern
**Priority:** P2 (Medium) | **Type:** Governance / Engineering | **Owner:** Head of Engineering | **Source:** STEP -1.7 Governance Health Score cross-routine scan, roadmap rebalance `2026-07-27__scheduled` (item first surfaced `2026-07-17__release-v7.5` closure, escalated again at `2026-07-20__release-v7.6` and `2026-07-21__release-v7.7` closures, target "next roadmap review" missed at `2026-07-24__scheduled` due to the Carry-Forward mechanism's single-cycle lookback — see `lessons_learnt.md` for the full detection-gap account) | **Effort:** L (~3-5 days) | **Provisional-Target:** TBD
**Problem:** Every EPIC branch cut before sprint execution progresses on `main` accumulates an independently-diverging copy of `execution_state.json`, requiring a manual per-branch conflict resolve at merge time. The existing mitigation (`shared_standards.md` §12, merge sequencing + reactive conflict resolution) does not prevent the conflict, only resolves it after the fact — and the cost has scaled up across 3 consecutive multi-EPIC cycles (v7.6, v7.7, v7.8; 10/11 branches affected at v7.7, 11/12 at v7.8) rather than down.
**Scope:** A structural fix removing the recurring merge-conflict surface itself — e.g. per-EPIC append-only manifest files aggregated at build/CI time instead of every branch writing to the same shared state file independently.
**Acceptance Criteria:** Structural fix designed and implemented; next multi-EPIC sprint shows a measured reduction in per-branch `execution_state.json` conflicts; Head of Engineering sign-off; `shared_standards.md` §12 updated to reference the new mechanism.

---

## Delivery Verification 2026-07-27__release-v7.9 — New Items

*Open escalation carried forward at sprint close with no prior backlog.md tracking entry — filed per `delivery_verification_prompt.md` STEP 4.1.*

### BLG-GOV-264 — Physically place the Displacement Debt Register and wire it into `roadmap_prompt.md` STEP 8
**Priority:** P3 (Low) | **Type:** Governance | **Owner:** Roadmap Rebalance Engine / Head of Specs Team | **Source:** `ESC-EXEC-20260727-02` (`claude/cycles/2026-07-27__release-v7.9/execution_escalations.md`), raised during EPIC-14/ST-14 (`2026-07-27__release-v7.9`) | **Effort:** XS | **Provisional-Target:** TBD
**Problem:** ST-14 designed the Displacement Debt Register (format + reconstructed seed content) in full, but `claude/roadmap/*` and `claude/system/roadmap_prompt.md` are outside Sprint Execution's write scope, so the design was handed off rather than applied. Two actions are needed together: (1) create `claude/roadmap/displacement_debt_register.md` using the format/seed content in `claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md#Displacement Debt Register — Design`; (2) edit `roadmap_prompt.md` STEP 8's "Displacement candidate flag" instruction to also update this register going forward. Landing only one half leaves either a stale instruction (no file) or an unmaintained file (no forcing function).
**Scope:** Both actions above, in the same session, per CLAUDE.md §6 Governance File Edit Checklist for the `roadmap_prompt.md` edit (version bump, `OPERATIONAL_GUIDE.md` §14 table update, `prompt_change_log.md` entry).
**Acceptance Criteria:** `claude/roadmap/displacement_debt_register.md` created with the seeded content; `roadmap_prompt.md` STEP 8 updated to reference it; `ESC-EXEC-20260727-02` closed.

---

## Roadmap Rebalance 2026-07-28__scheduled — New Items (IW-20260728-01 disposition)

*42 items filed from a 44-submission window (1 idea resolved directly — see BLG-OPS-90 gate-status update above; 2 ideas consolidated into one item — see BLG-GOV-269). All ungated unless a Gate criteria line is present.*

### BLG-GOV-265 — AI vendor Terms-of-Service & data-processing review (Gemini/Claude, financial data handling)
**Priority:** P2 (Medium) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No formal review exists confirming Gemini's and Claude's vendor ToS/data-processing terms are compatible with handling this system's financial trade data (retention, training-data use, sub-processor disclosure).
**Scope:** Review both vendors' current ToS/DPA terms against the system's financial-data handling; document findings and any required mitigations.
**Acceptance Criteria:** Review documented; any gap flagged with a remediation item; AI Compliance & Governance Officer sign-off.

---

### BLG-GOV-266 — Canonical AI feature touchpoint register with per-feature §13 classification
**Priority:** P3 (Low) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260728-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** AI-touching features (thesis generation, daily briefing, chat advisor, cost alerts) have each had individual §13 reviews over time, but no single register lists every AI touchpoint and its current §13 classification in one place.
**Scope:** Build a register listing each AI-calling feature, its §13 classification, and a link to its review record.
**Acceptance Criteria:** Register created and covers all currently-shipped AI touchpoints; AI Compliance & Governance Officer sign-off.

---

### BLG-SPEC-106 — OpenAPI security-scheme & auth-header documentation completeness check
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `openapi.yaml` documents endpoint paths and schemas but has not been audited to confirm every authenticated endpoint's security scheme and required auth header are correctly and completely documented.
**Scope:** Audit all authenticated endpoints in `openapi.yaml` against actual backend auth enforcement; correct any gaps.
**Acceptance Criteria:** Audit complete; any documentation gap fixed; API Contracts & Documentation Owner sign-off.

---

### BLG-QA-128 — Consumer-driven contract check: frontend API calls vs documented contracts
**Priority:** P2 (Medium) | **Type:** QA / Contract Testing | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260728-02 | **Effort:** M | **Provisional-Target:** v7.10
**Problem:** `openapi.yaml` and `docs/specs/api_contracts/` describe the backend's own contract, but nothing checks that frontend call sites actually match the documented request/response shape they depend on.
**Scope:** Add a lightweight consumer-driven contract check comparing frontend API call sites against the documented contract fields they consume.
**Acceptance Criteria:** Check implemented (CI or scripted); first run's findings triaged; API Contracts & Documentation Owner sign-off.

---

### BLG-BE-75 — Extend Alpaca backoff audit (BLG-BE-57) to Yahoo Finance, Gemini, and Claude call sites
**Priority:** P2 (Medium) | **Type:** Backend / Resilience | **Owner:** Backend Engineering Patterns Owner | **Source:** IDEA-backend-engineering-20260728-01 (relationship note: extends `BLG-BE-57`'s Alpaca-only scope to 3 additional providers) | **Effort:** M | **Provisional-Target:** v7.10
**Problem:** `BLG-BE-57` audited retry/backoff behaviour for Alpaca call sites only; Yahoo Finance, Gemini, and Claude external calls have not had the same review, despite being equally capable of rate-limiting or transient failure.
**Scope:** Apply the same retry/backoff audit methodology from `BLG-BE-57` to the three remaining external providers.
**Acceptance Criteria:** All 4 providers' call sites confirmed to use the shared retry/backoff decorator (`BLG-BE-71`) or have a documented exception; Backend Engineering Patterns Owner sign-off.

---

### BLG-BE-76 — Idempotency key pattern for state-mutating POST endpoints
**Priority:** P2 (Medium) | **Type:** Backend / Correctness | **Owner:** Backend Engineering Patterns Owner | **Source:** IDEA-backend-engineering-20260728-02 | **Effort:** M | **Provisional-Target:** v7.10
**Problem:** State-mutating POST endpoints (trade entry, trade plan creation, alert rules) have no idempotency-key mechanism, so a retried request (e.g. after a timeout) risks creating a duplicate record.
**Scope:** Define and apply an idempotency-key pattern (client-supplied key + short-lived server-side dedup check) for the highest-risk state-mutating endpoints.
**Acceptance Criteria:** Pattern documented in `backend_engineering_patterns.md`; applied to at least the trade-entry and trade-plan-creation endpoints; Backend Engineering Patterns Owner sign-off.

---

### BLG-GOV-267 — Base44 generation failure-mode log (recurring manual-correction patterns)
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Base44 Frontend Prompt Owner | **Source:** IDEA-base44-frontend-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Base44-generated components occasionally need manual correction (e.g. missed dark-mode class pairs, contrast issues) but no log tracks which failure modes recur, so prompt-template improvements are made ad hoc rather than targeting the most frequent gaps.
**Scope:** Add a lightweight log of Base44 generation failure modes requiring manual correction, reviewed periodically to prioritise prompt-template fixes.
**Acceptance Criteria:** Log created; at least the known recurring modes (dark-mode class pairs, contrast) backfilled; Base44 Frontend Prompt Owner sign-off.

---

### BLG-FE-132 — Standard Base44 prompt section for dark/light theme compliance
**Priority:** P3 (Low) | **Type:** Frontend / Process | **Owner:** Base44 Frontend Prompt Owner | **Source:** IDEA-base44-frontend-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Dark/light theme compliance issues have recurred across multiple Base44-generated components (BLG-FE-113, BLG-FE-125, BLG-FE-129 checklist), suggesting the prompt template itself lacks a standard theme-compliance section rather than each case being caught after the fact.
**Scope:** Add a standard theme-compliance section to the core Base44 prompt template (distinct from the BLG-FE-129 dark-mode AC checklist, which is a review-time check, not a generation-time prompt instruction).
**Acceptance Criteria:** Standard section added to `base44_prompt_template_library.md`; Base44 Frontend Prompt Owner sign-off.

---

### BLG-GOV-268 — Escalation path for Product Value Ratio's persistent Advisory tier
**Priority:** P2 (Medium) | **Type:** Governance / Process | **Owner:** Challenger | **Source:** IDEA-challenger-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The Product Value Ratio has sat in the 0.30–0.49 Advisory band for numerous consecutive cycles (0.31→0.42→0.39→0.42→0.38 across the last several windows) without ever reaching the ≥0.50 Healthy threshold or dropping into the <0.30 Alert threshold that would force mandatory action — an Advisory reading currently has no equivalent "sustained non-improvement" escalation clause the way Skill-Silo does (STEP 7.1's 3-consecutive-worsening mandatory clause).
**Scope:** Define a sustained-Advisory escalation clause for STEP 2.4 (e.g. N consecutive cycles in Advisory band without reaching Healthy triggers a strengthened response), mirroring the Skill-Silo precedent.
**Acceptance Criteria:** Clause drafted and reviewed with Head of Specs Team; if adopted, `roadmap_prompt.md` STEP 2.4 updated per the standard governance file edit checklist.

---

### BLG-GOV-269 — Direct-write / governance-bypass pattern tracker (roadmap & amendment gate bypasses)
**Priority:** P2 (Medium) | **Type:** Governance / Process | **Owner:** PMO Lead | **Source:** IDEA-challenger-20260728-02, IDEA-pmo-lead-20260728-02 (consolidated — both submissions converge on the same recurring pattern: direct writes to `current_roadmap.md`/`decision_log.md` bypassing a compliant `run roadmap`/amendment-cycle path) | **Effort:** M | **Provisional-Target:** TBD
**Problem:** `current_roadmap.md`'s own history shows a repeated pattern (v7.4 AMD, v7.5, v7.6 DL-073, v7.7 DL-074, and others) of "out-of-band" direct writes to formalise release sections or add capacity, each time noting that a fully compliant `run roadmap --reason scheduled` path existed but was bypassed by explicit session direction. This was already flagged as a Carry-Forward observation at `2026-07-21__release-v7.7` closure (Item 2) but has no dedicated tracking artefact — each new bypass is only visible by reading roadmap prose history, not a structured log.
**Scope:** Add a structured, append-only log of every direct-write bypass of a governed routine (date, file, reason given, routine bypassed), so the recurrence pattern is visible without re-deriving it from `current_roadmap.md` prose each time.
**Acceptance Criteria:** Log created; backfilled with the known historical instances named above; PMO Lead sign-off.

---

### BLG-SEC-22 — Secrets-scanning pre-commit/CI gate (gitleaks/trufflehog)
**Priority:** P2 (Medium) | **Type:** Security / CI | **Owner:** Cybersecurity & Trust Lead | **Source:** IDEA-cybersecurity-20260728-01 | **Effort:** S | **Provisional-Target:** v7.10
**Problem:** CI has a secret-scanning gate at the pipeline level (per `v5.3`'s `BLG-OPS-58`), but no pre-commit local check exists, so a secret can be committed locally before CI ever runs.
**Scope:** Add a local pre-commit hook running a secrets scanner (gitleaks or trufflehog), complementing the existing CI-level gate.
**Acceptance Criteria:** Hook added to `.githooks/pre-commit`; confirmed to catch a deliberately-planted test secret; Cybersecurity & Trust Lead sign-off.

---

### BLG-SEC-23 — Mandatory security review checklist for new AI-calling endpoints
**Priority:** P2 (Medium) | **Type:** Security / Process | **Owner:** Cybersecurity & Trust Lead | **Source:** IDEA-cybersecurity-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** New AI-calling endpoints have each had ad hoc security consideration (rate limiting, cost gating, prompt-injection awareness) but no standard checklist ensures every new one covers the same baseline before shipping.
**Scope:** Define a short mandatory security review checklist specific to AI-calling endpoints (distinct from the general API security review), referenced at design-gate time.
**Acceptance Criteria:** Checklist documented; referenced from the design gate process; Cybersecurity & Trust Lead sign-off.

---

### BLG-BE-77 — Mutation/audit-trail log for trade plan edits post-entry
**Priority:** P3 (Low) | **Type:** Backend / Data Integrity | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260728-01 (distinct from `BLG-BE-73`, shipped v7.9, which covers manual *position* edits — this covers *trade plan* edits after the position is opened) | **Effort:** M | **Provisional-Target:** TBD
**Problem:** `BLG-BE-73` added an audit trail for manual position edits, but trade plan records can also be edited after entry (e.g. thesis or R-target revision) with no equivalent who/when/before-after log.
**Scope:** Extend the audit-trail pattern established by `BLG-BE-73` to trade plan mutations post-entry.
**Acceptance Criteria:** Audit log covers trade plan edits; Data Model & Domain Schema Owner sign-off.

---

### BLG-BE-78 — Auto-generated data dictionary from live schema
**Priority:** P3 (Low) | **Type:** Backend / Documentation | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260728-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** `data_model.md` is hand-maintained; as migrations accumulate (v2.17 and counting) there is growing risk of the documented schema drifting from the live one.
**Scope:** Add a script generating a data dictionary directly from the live schema, for comparison against `data_model.md` at review time.
**Acceptance Criteria:** Script added; first run's diff against `data_model.md` triaged; Data Model & Domain Schema Owner sign-off.

---

### BLG-GOV-270 — Cross-role workload balance check (avoid single-role bottleneck across consecutive cycles)
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No check currently confirms that story/EPIC ownership is balanced across roles over consecutive cycles — a role could be silently overloaded for several cycles running without it being visible in any single cycle's own artefacts.
**Scope:** Add a lightweight cross-cycle check tallying story ownership per role over a rolling window, surfaced at roadmap rebalance.
**Acceptance Criteria:** Check defined and documented; Director of HR sign-off.

---

### BLG-GOV-271 — Agent onboarding runbook for adding a new governance role
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Adding a new agent role (most recently done for several roles across the project's history) has no documented runbook — each addition has been done ad hoc (charter file, idea-intake slug mapping, required-roles lists across multiple prompt files).
**Scope:** Document the full checklist of files/lists that must be updated when adding a new governance role.
**Acceptance Criteria:** Runbook created; Director of HR sign-off.

---

### BLG-QA-129 — Cross-EPIC deviation (DEV-*) consolidation review across cycles
**Priority:** P2 (Medium) | **Type:** QA / Process | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** DEV-* deviation records are filed and resolved per-cycle, but no periodic review looks across cycles for recurring deviation types that might indicate a systemic (not one-off) gap.
**Scope:** Add a periodic review consolidating DEV-* records across recent cycles to surface recurring patterns.
**Acceptance Criteria:** First consolidation review performed; Director of Quality sign-off.

---

### BLG-QA-130 — Quality trend index aggregating DEV-* records over time
**Priority:** P3 (Low) | **Type:** QA / Metrics | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260728-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** There is no single trend view of deviation volume/severity over time — each cycle's deviation count is only visible in that cycle's own `sprint_close.md`.
**Scope:** Build a simple trend index (deviation count/severity per cycle, plotted or tabulated over time).
**Acceptance Criteria:** Index created and backfilled from available cycle history; Director of Quality sign-off.

---

### BLG-SPEC-107 — FX conversion audit trail completeness check (§4.1.5 effective-rate logging)
**Priority:** P2 (Medium) | **Type:** Spec Debt / Financial Records | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `data_model.md` §4.1.5 documents effective-rate logging for FX conversions, but no audit has confirmed every conversion path actually writes a complete audit trail entry.
**Scope:** Audit all FX conversion code paths against the §4.1.5 logging requirement; fix any gap found.
**Acceptance Criteria:** Audit complete; any gap fixed; Financial Reporting & Records Owner sign-off.

---

### BLG-FEAT-88 — P&L / tax record reconciliation report (system totals vs individual trade export)
**Priority:** P3 (Low) | **Type:** Product Feature / Financial Reporting | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260728-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** The Monthly P&L CSV export and individual trade records are both user-facing, but nothing confirms (or lets the user confirm) that the two reconcile to the same totals — a silent discrepancy would currently go unnoticed.
**Scope:** Add a reconciliation report/view comparing system-computed P&L totals against a sum of the individual trade export.
**Acceptance Criteria:** Reconciliation report added; confirmed to match on current data; Financial Reporting & Records Owner sign-off.

---

### BLG-OPS-123 — Database storage growth cost trend tracking (Postgres/Supabase)
**Priority:** P3 (Low) | **Type:** FinOps / Operations | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Cloud spend is cost-tagged per EPIC (`BLG-OPS-120`), but database storage growth over time has no dedicated trend tracking, despite being a cost driver that scales with trade/journal history volume.
**Scope:** Add a simple storage-growth trend view (size over time) alongside the existing cost-tag reporting.
**Acceptance Criteria:** Trend tracking added; FinOps & Resource Architect sign-off.

---

### BLG-OPS-124 — Render dashboard-only build/deploy path filter audit (invisible to repo grep)
**Priority:** P2 (Medium) | **Type:** Operations / Infrastructure | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260728-02 (submitter recommendation: Now) | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Render's dashboard-configured build/deploy path filters are not represented anywhere in the repo, so a change to a file outside the configured watch paths (e.g. `changelog.md`, per commit `e9c73f58` this same day) can silently fail to trigger a redeploy with no signal visible to a repo-only search. This is now a confirmed second occurrence of the same class as `BLG-OPS-82` (see `BLG-OPS-90` gate-status update, this cycle).
**Scope:** Audit the full current Render dashboard build/deploy path-filter configuration against the set of files the running app actually reads at runtime; document any other file outside the watched paths.
**Acceptance Criteria:** Audit complete; configuration documented in-repo (even though the source of truth remains the dashboard) so future searches can find it; FinOps & Resource Architect sign-off.

---

### BLG-SPEC-108 — Canonical form validation error-message pattern spec
**Priority:** P3 (Low) | **Type:** Frontend Spec | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Form validation error messages across the app (trade plan form, alert rules, saved filters) have been built independently without a canonical spec for tone/format, risking inconsistency.
**Scope:** Define a canonical error-message pattern spec (tone, placement, wording conventions) in `design_system.md`.
**Acceptance Criteria:** Spec added; Frontend Specifications & UX Documentation Owner sign-off.

---

### BLG-GOV-272 — Recurring spec-debt backlog review cadence
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** BLG-SPEC-* items accumulate over time (105+ so far) with no defined periodic review cadence dedicated specifically to spec debt, distinct from general backlog grooming.
**Scope:** Define a periodic review cadence specifically for BLG-SPEC-* items.
**Acceptance Criteria:** Cadence defined and documented in `backlog_management_prompt.md`; Head of Specs Team confirmation.

---

### BLG-GOV-273 — Technical debt registry (consolidated cross-cycle view)
**Priority:** P2 (Medium) | **Type:** Governance / Process | **Owner:** Head of Engineering | **Source:** IDEA-head-of-engineering-20260728-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Technical debt items are scattered across BLG-BE-*, BLG-FE-*, BLG-OPS-* with no consolidated cross-category view of total outstanding technical debt.
**Scope:** Build a consolidated registry pulling technical-debt-classified items from across backlog categories into one view.
**Acceptance Criteria:** Registry created; Head of Engineering sign-off.

---

### BLG-OPS-125 — Automated commit-message format lint (pre-commit hook for [EPIC-xx][ST-xx] convention)
**Priority:** P2 (Medium) | **Type:** Ops / CI | **Owner:** Head of Engineering | **Source:** IDEA-head-of-engineering-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `CLAUDE.md` §2's commit format (`[EPIC-xx][ST-xx] <description>`) is enforced only by human/agent discipline and caught after the fact by `governance_sync.yml`, not checked at commit time.
**Scope:** Add a pre-commit hook (alongside the existing route-registration hook, `BLG-QA-125`) that lints the commit message format on `exec/**` branches.
**Acceptance Criteria:** Hook added; confirmed to reject a deliberately malformed commit message; Head of Engineering sign-off.

---

### BLG-GOV-274 — Automated Specs_Index.md freshness check against live spec files
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `Specs_Index.md`'s maintenance has previously lapsed silently for 5 consecutive cycles before being caught (per `2026-07-21__release-v7.7` closure Carry-Forward Item 3) — the check for staleness is currently manual.
**Scope:** Add an automated check comparing `Specs_Index.md` entries against the live `docs/specs/` tree for additions/removals it doesn't yet reflect.
**Acceptance Criteria:** Check added; Head of Specs Team sign-off.

---

### BLG-GOV-275 — Searchable index of STEP 11.4 meta-review findings across cycles
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 11.4 meta-reviews produce `meta_review.md` files per triggering cycle, but there is no searchable cross-cycle index of what patterns each meta-review found or what it changed.
**Scope:** Add a lightweight index summarising each meta-review's key findings and resulting prompt changes.
**Acceptance Criteria:** Index created and backfilled from existing `meta_review.md` files; Head of Specs Team sign-off.

---

### BLG-FE-133 — Ad hoc component inventory: candidates for shared design-system extraction
**Priority:** P3 (Low) | **Type:** Frontend / Design System | **Owner:** Head of UX & Design | **Source:** IDEA-head-of-ux-20260728-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Several shared-component extractions have happened reactively (e.g. `BLG-FE-120` standing alert, `BLG-FE-121` modal confirmation) after duplication was noticed; no proactive inventory tracks which ad hoc components are current extraction candidates.
**Scope:** Build an inventory of ad hoc/duplicated component patterns across the app, ranked by duplication count, as a standing extraction candidate list.
**Acceptance Criteria:** Inventory created; Head of UX & Design sign-off.

---

### BLG-FE-134 — Keyboard navigation & focus-order audit (distinct from colour-contrast a11y work)
**Priority:** P2 (Medium) | **Type:** Frontend / Accessibility | **Owner:** Head of UX & Design | **Source:** IDEA-head-of-ux-20260728-02 | **Effort:** M | **Provisional-Target:** v7.10
**Problem:** Accessibility work to date (`BLG-FE-82`, `BLG-FE-87/88/89`, dark-mode contrast audits) has focused on colour/contrast; keyboard navigation and focus order have not had an equivalent dedicated audit.
**Scope:** Audit keyboard navigation and focus order across the app's primary flows (trade entry, trade plan, command palette).
**Acceptance Criteria:** Audit complete; findings filed as follow-up items where gaps are found; Head of UX & Design sign-off.

---

### BLG-OPS-126 — Backup & disaster recovery runbook for production database
**Priority:** P2 (Medium) | **Type:** Operations / Infrastructure | **Owner:** Infrastructure & Operations Owner | **Source:** IDEA-infra-ops-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No documented runbook exists for production database backup verification or disaster recovery — a real incident would rely on ad hoc knowledge rather than a tested procedure.
**Scope:** Document backup frequency/retention (as currently configured on the hosting provider) and a step-by-step recovery runbook.
**Acceptance Criteria:** Runbook documented; recovery steps confirmed against actual hosting provider capability; Infrastructure & Operations Owner sign-off.

---

### BLG-GOV-276 — Formalise Product Value Ratio rolling-window boundary-trade handling in metrics_definitions.md
**Priority:** P3 (Low) | **Type:** Governance / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 2.4's Product Value Ratio is computed over "the last 5 completed cycles," but `metrics_definitions.md` does not formally specify how a cycle at the exact window boundary should be handled (e.g. a cycle completing mid-window), leaving this to ad hoc judgment each time the ratio is computed.
**Scope:** Add a formal boundary-handling rule to `metrics_definitions.md`.
**Acceptance Criteria:** Rule documented; Metrics Definitions & Analytics Canonical Owner sign-off.

---

### BLG-GOV-277 — Document exact skill-category taxonomy used for Skill-Silo classification
**Priority:** P3 (Low) | **Type:** Governance / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 7.1's Skill-Silo classification (Governance-heavy vs Execution-heavy) is applied consistently in practice but the exact taxonomy (which roles/story-shapes fall into which bucket) is not written down in one canonical place — it's reconstructed from precedent each cycle.
**Scope:** Document the exact classification taxonomy in `metrics_definitions.md`, consistent with how STEP 2.4's U/G/D/P taxonomy is already documented.
**Acceptance Criteria:** Taxonomy documented; Metrics Definitions & Analytics Canonical Owner sign-off.

---

### BLG-GOV-278 — Idea-intake backlog-overlap check effectiveness retrospective (v2.8, post-N-windows)
**Priority:** P2 (Medium) | **Type:** Governance / Process | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The mandatory backlog-overlap check (`idea_intake_prompt.md` v2.8) was added at `2026-07-27__scheduled` in response to a 52% duplicate-submission rate; this window (`IW-20260728-01`) shows the check catching real overlaps (20 of the initial topic-slots dropped/reframed), but there has been no formal retrospective confirming the check is working as intended versus just adding process overhead.
**Scope:** After a few more windows have run under v2.8, review whether the check materially reduced downstream STEP 4 rejection rates and whether the check's own overhead is proportionate.
**Acceptance Criteria:** Retrospective performed; recommendation recorded (keep/adjust/retire the check); PMO Lead sign-off.

---

### BLG-GOV-279 — SI-02 production credential provisioning decision (formalise fallback vs acquire)
**Priority:** P2 (Medium) | **Type:** Governance / Process | **Owner:** Product Owner | **Source:** IDEA-product-owner-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-OPS-121` provisioned a working credential this cycle, but it was supplied ad hoc into that session's environment and did not persist into this new session's `.env` files (confirmed absent again at this rebalance) — the underlying "credential persistence" gap identified in `2026-07-27__release-v7.9` closure Carry-Forward Item 2 remains open despite the credential itself existing and working.
**Scope:** Decide and document whether the fix is (a) persisting the credential into checked-in-but-gitignored environment config that governed routines can rely on, or (b) formally accepting the fallback-citation pattern (`roadmap_prompt.md` v9.6 STEP 2.3) as the standing behaviour and stop treating each occurrence as a fresh gap.
**Acceptance Criteria:** Decision recorded; if (a), implemented; if (b), `roadmap_prompt.md` STEP 2.3 updated to remove the "should attempt genuine live re-check" framing as an open gap; Product Owner sign-off.

---

### BLG-GOV-280 — Formal sunset criteria for perennially-returning gated backlog items
**Priority:** P2 (Medium) | **Type:** Governance / Process | **Owner:** Product Owner | **Source:** IDEA-product-owner-20260728-02 (submitter recommendation: Now) | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-FEAT-73`/`BLG-FEAT-74` have now cycled through Now-horizon inclusion and removal multiple times (named as v7.7 anchor scope, then removed at `2026-07-24__release-v7.8` post-ship per a "perennial-return" PO disposition) without a formal, written sunset test for when a perennially-returning gated item should be killed outright versus kept indefinitely parked. Each disposition has been a fresh ad hoc judgment call.
**Scope:** Define explicit sunset criteria (e.g. N consecutive perennial-return cycles with no gate progress triggers a formal Kill decision, not just another un-scheduled parking) for items that repeatedly enter and exit the Now horizon without shipping.
**Acceptance Criteria:** Criteria documented in `roadmap_prompt.md` or `shared_standards.md` (per the standing governance file edit checklist if adopted); applied retroactively to assess `BLG-FEAT-73`/`BLG-FEAT-74`'s current status; Product Owner sign-off.

---

### BLG-QA-131 — Post-parallelization Playwright shard balance audit (REC-CI-01 follow-up)
**Priority:** P2 (Medium) | **Type:** QA / CI | **Owner:** QA Lead | **Source:** IDEA-qa-lead-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `REC-CI-01` parallelized Playwright E2E CI with workers + shard matrix, but no follow-up has confirmed the shards are actually balanced (similar runtime per shard) rather than one shard becoming a new bottleneck.
**Scope:** Audit shard runtimes post-parallelization; rebalance shard assignment if skewed.
**Acceptance Criteria:** Audit performed; shard runtimes confirmed balanced or rebalanced; QA Lead sign-off.

---

### BLG-QA-132 — Staging sign-off backlog tracker (FI-P3-02 wording-only AC exceptions)
**Priority:** P3 (Low) | **Type:** QA / Process | **Owner:** QA Lead | **Source:** IDEA-qa-lead-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The `FI-P3-02` exception (wording-only ACs may substitute code review for staging sign-off) is applied per-story with no consolidated tracker of how often it's invoked, making it hard to spot if the exception is being over-relied upon.
**Scope:** Add a tracker logging each `FI-P3-02` invocation across cycles.
**Acceptance Criteria:** Tracker created and backfilled where findable; QA Lead sign-off.

---

### BLG-QA-133 — Endpoint test suite coverage audit against all backend/routers/ files
**Priority:** P2 (Medium) | **Type:** QA / Backend | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260728-01 | **Effort:** M | **Provisional-Target:** v7.10
**Problem:** `CLAUDE.md` §2 requires every new route to be registered in `backend/routers/test.py`, but no periodic audit confirms all *existing* routes across every router file are actually covered, only that new ones are added going forward.
**Scope:** Audit `backend/routers/test.py` coverage against every `@router.*` decorator across all router files.
**Acceptance Criteria:** Audit complete; any coverage gap found is filed or fixed; QA & Testing Owner sign-off.

---

### BLG-QA-134 — Regression suite runtime budget & reporting
**Priority:** P3 (Low) | **Type:** QA / CI | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The regression suite has grown substantially (baseline updates at `BLG-QA-112`, `BLG-QA-114`) with no defined runtime budget or reporting on whether it's trending toward becoming a CI bottleneck.
**Scope:** Define a runtime budget and add simple reporting on regression suite duration over time.
**Acceptance Criteria:** Budget defined; reporting added; QA & Testing Owner sign-off.

---

### BLG-GOV-281 — Mandatory §13 boundary pre-check at design gate for new AI-calling feature proposals
**Priority:** P2 (Medium) | **Type:** Governance / Strategy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** §13 reviews for AI-calling features have so far each been requested individually (e.g. retroactive PT-04 review, `BLG-GOV-28`) rather than being a standing, mandatory step at design-gate time for any *new* AI-calling proposal.
**Scope:** Add a mandatory §13 boundary pre-check step to `design_gate_prompt.md` specifically for proposals that call an AI provider.
**Acceptance Criteria:** Step added to `design_gate_prompt.md` per the standing governance file edit checklist; Strategy Rules & System Intent Owner sign-off.

---

### BLG-GOV-282 — strategy_rules.md version cross-reference consistency check in dependent docs
**Priority:** P3 (Low) | **Type:** Governance / Spec Debt | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Several documents cite a specific `strategy_rules.md` version (e.g. §13 review records, compliance score formulas); when `strategy_rules.md` is incremented, nothing checks whether those cross-references have gone stale.
**Scope:** Add a check comparing cited `strategy_rules.md` versions in dependent docs against the current version.
**Acceptance Criteria:** Check added; first run's findings triaged; Strategy Rules & System Intent Owner sign-off.

---

### BLG-GOV-283 — Codify a `**Last Updated:**` header-history retention convention (stop unbounded chain growth)
**Priority:** P2 (Medium) | **Type:** Governance / Process | **Owner:** Head of Specs Team | **Source:** User observation, session 2026-07-28 (raised while reviewing the output of roadmap rebalance `2026-07-28__scheduled`) | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `claude/roadmap/current_roadmap.md`, `claude/roadmap/workforce_capacity.md`, and `claude/roadmap/initiative_register.md` each carry a `**Last Updated:**` header field that accumulates a `prior — <date> (...)` chain every time the file is touched, with no rule anywhere requiring it to be trimmed. `current_roadmap.md`'s chain had grown to ~11.5KB in a single header line (unbroken growth since at least 2026-07-08) before being manually truncated this session. `claude/ideas/ideas_register.md` has cut its own chain once before, using the phrase "prior history retained — see prior entries in version control," but that was an undocumented, one-off act by whichever session did it, not a convention any governance prompt actually invokes. No backlog item previously tracked this gap, so it would have kept recurring indefinitely.
**Scope:** Define a formal, named retention rule (e.g. "keep the current entry plus the last N prior entries or M days, whichever is longer, then cut with the standard `prior history retained — see prior entries in version control (last full entry retained: <ref>)` sentence") in `claude/system/shared_standards.md`, and reference it from the STEP 9 write instructions of `roadmap_prompt.md` (and any other engine that writes one of these three files, or `ideas_register.md`) so trimming happens as a routine part of the write, not an ad hoc manual cleanup. Apply retroactively: `current_roadmap.md`, `workforce_capacity.md`, and `initiative_register.md` were all manually truncated to this pattern on 2026-07-28 as an interim fix, ahead of the rule being formally codified.
**Acceptance Criteria:** Retention rule documented in `shared_standards.md` with an explicit depth/age threshold; `roadmap_prompt.md` STEP 9 (and `ideas_register.md`'s STEP 9 equivalent in `idea_intake_prompt.md`, if applicable) updated to apply it automatically per the standard governance file edit checklist (version bump, `OPERATIONAL_GUIDE.md` §14 update, `prompt_change_log.md` entry); Head of Specs Team sign-off.

---

### BLG-SEC-24 — Verify request.client.host reflects true client IP behind Render's proxy; configure trusted-proxy headers if not
**Priority:** P1 (High) | **Type:** Security / Infrastructure | **Owner:** Cybersecurity & Trust Lead | **Source:** BLG-SEC-09 AI rate-limit bypass audit finding (ST-06, EPIC-02, v7.10) — 2026-07-29 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `backend/routers/ai.py`'s per-IP AI rate limiter (`_ai_limiter`) keys purely on `request.client.host`. `render.yaml`'s start command (`uvicorn main:app --host 0.0.0.0 --port $PORT`) has no `--proxy-headers`/`--forwarded-allow-ips` flag. Render terminates connections at its own edge/proxy layer, so without trusting a specific forwarded-IP header from that known upstream, `request.client.host` at the ASGI layer likely reflects Render's internal proxy connection, not the real client IP, for every request in production. If confirmed, every user's traffic collapses onto the same rate-limit key — the documented "10/min/IP" and "30/min/IP" limits would actually be a single shared global budget, meaning one user (malicious or not) could exhaust the entire app's AI quota and deny service to everyone else with as few as 10 rapid requests. This undermines the cost/DoS control the limiter was built for (`BLG-SEC-21`/v7.8).
**Scope:** Verify against the live Render deployment whether `request.client.host` reflects the real client IP or Render's proxy IP (e.g. log it for a live request from a known external IP). If confirmed to be the proxy IP: configure uvicorn to trust Render's forwarding (`--proxy-headers --forwarded-allow-ips=...` scoped correctly, not a blanket wildcard, per Render's documented `X-Forwarded-For` behaviour) so the limiter keys on the true client IP.
**Acceptance Criteria:** Live verification documented; if the proxy-IP collapse is confirmed, uvicorn configured to trust the correct forwarded-IP header from Render's known edge; re-verified live that distinct real clients now get independent rate-limit buckets; Cybersecurity & Trust Lead sign-off.

---

### BLG-SEC-25 — Raw exception text leaked in 16 implicit-HTTP-200 error paths in backend/main.py
**Priority:** P2 (Medium) | **Type:** Security / Backend | **Owner:** Head of Engineering | **Source:** BLG-SEC-13 raw-exception-text remediation finding (ST-08, EPIC-02, v7.10) — 2026-07-29 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** ST-08 (BLG-SEC-13) fixed all 27 explicit 500-class `HTTPException`/`JSONResponse` call sites in `backend/main.py` that leaked raw exception text via `detail=str(e)`. During that work, 16 additional call sites were found returning a bare `{"status": "error", "message": ...}` dict with **no explicit status code** — FastAPI serialises this as an implicit HTTP 200, so these are simultaneously an instance of the "errors masked as HTTP 200" bug class (`BLG-BE-68`'s pattern, fixed for `portfolio_risk.py` in this same cycle) AND a raw-exception-text leak, in the same 16 places (15 direct `str(e)` interpolations plus 1 f-string variant, `f"Failed to fetch market status: {str(e)}"`). Out of scope for ST-08 (whose AC is explicitly scoped to "500-class error responses") and out of scope for `BLG-BE-68` (scoped to `portfolio_risk.py` only) — neither existing item covers `main.py`'s own 16 instances of this combined bug. Note: some of these 16 sites already log server-side (`traceback.print_exc()`) pre-existing this cycle's work; others do not — logging coverage is itself inconsistent across the 16 and should be normalised as part of the fix, not just the client-facing message.
**Scope:** For each of the 16 call sites: (a) correct the status code to 500 with the canonical `{status, message}` envelope (matching the `BLG-BE-68`/ST-01 remediation pattern), and (b) substitute a generic message for the raw exception text, ensuring full exception detail is logged server-side (adding `traceback.print_exc()` wherever it's currently missing).
**Acceptance Criteria:** All 16 call sites return HTTP 500 (not implicit 200) with a generic client-facing message; full exception detail logged server-side on every one of the 16 (not just those that already had it); existing 200-path success shapes unchanged; regression test added; Head of Engineering sign-off.

---
