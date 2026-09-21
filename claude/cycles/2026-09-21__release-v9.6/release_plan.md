Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-21
Cycle: 2026-09-21__release-v9.6
Release: v9.6

# Release Plan — v9.6

Invocation: `plan release --version "v9.6" --capacity "full capacity"`

---

## Readiness

Preflight (STEP -1) passed in full — see `run_manifest.md`. No formal `## v9.6` roadmap section exists; cleared via the STEP -1.2 Option(b)-equivalence rule against the `2026-09-19__scheduled` rebalance's documented "defer" decision (14th consecutive release cycle relying on this equivalence, extending the v8.5–v9.5 pattern). `post_ship_complete`/`next_cycle_unblocked` both `true` for prior cycle `2026-09-15__release-v9.5`. All required agent roles present. Write test passed. `open_escalations` empty; `ESC-EXEC-20260910-01` sits in `deferred_escalations` at disposition `Deferred`, not `Open` — the SLA-breach carry-forward gate does not fire.

Advisory checks (§1.1–§1.4, full detail in `run_manifest.md`):
- Gate-detection scan: 212 items, 131 gated, 4 data-quality warnings. Six date-lapsed gates read individually: `BLG-GOV-90` and `BLG-GOV-188` cleared and selected; `BLG-FEAT-59`/`60`/`63`/`BLG-FE-84` not cleared (owner verification due at the 2026-09-24 AI review) and classified conditional (§1.4b). 4 further items (`BLG-GOV-335`/`336`/`337` complete, `BLG-GOV-326` satisfied) excluded as not open work — a blind spot in the scan, recorded as a friction item.
- Backlog Age Advisory: no selected spec/documentation debt item aged 2+ cycles without story assignment.
- Provisional-Target Advisory: 4 selected items carry `v9.6`, 1 carries `v9.5`; 12 of the pool's 16 `v9.6`-tagged items (4.80 days) are not selected under strict §1.4c — no Product Owner override was given (Friction Item 2).
- Design-Gate Language Scan: all 6 EPIC-01 items and both EPIC-02 items carry an observable UI acceptance criterion → **`design_gate_required: true`**.
- Gate-Condition Proximity Scan: Arc 4 data-density metrics not re-queried (carried forward from the 2026-09-19 rebalance; SI-02/PO-02/PO-04 gates NOT MET). No selected item touches that gate family. Ready pool holds **0 P1**, 8 P2, 61 P3, 7 P4.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-09-21__release-v9.6-build-and-ship-pull-forward-and-debt-clearance.md`

| S2-ID | Scope theme | Items | Effort (days) |
|-------|-------------|-------|----------------|
| S2-01 | Product Features & Frontend Build-and-Ship | 6 | 6.75 |
| S2-02 | Financial Reporting & Records Integrity | 2 | 2.75 |
| S2-03 | Backend & Platform Engineering Debt | 5 | 4.55 |
| S2-04 | Operations & Security Debt | 4 | 1.90 |
| S2-05 | QA & Test Coverage Debt | 4 | 3.65 |
| S2-06 | Spec & Documentation Debt | 5 | 4.15 |
| S2-07 | Governance Process Debt | 6 | 4.25 |
| **Total** | | **32** | **28.00** |

**Items explicitly deferred (not entering v9.6 scope):**
- `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` — substantively gate-blocked by their own body text.
- `BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`, `BLG-GOV-140`/`141`/`142`, `BLG-OPS-88` — within-sprint date gate (2026-09-24), classified conditional per §1.4b; re-eligible at v9.7.
- `BLG-GOV-335`/`336`/`337`/`326` — already complete or satisfied; archive at next groom.
- 121 further formally gated items; 44 further ready items (~33.75 days) left unselected on capacity grounds only.

No scope reprioritisation performed beyond selection from the ungated pool — this routine does not alter strategy boundaries.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note (IMP-08):** full acceptance criteria live in `stage4_backlog_slice.md`; this section is the compact sequencing/risk view. EPIC-01 leads the table as this cycle's execution-heavy rotation slot (Skill-Silo Alert 98.8%, per the 2026-09-19 rebalance).

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Head of Engineering; Head of UX & Design; Product Owner; Frontend Specifications & UX Documentation Owner | RISK-01 | **Design-gate-triggering.** `ST-01` → `ST-02` (both edit `TradePlans.js`); `ST-06` (`BLG-FE-182`, touches 3 tables) last so it rebases onto them |
| EPIC-02 | S2-02 | Financial Reporting & Records Owner; Backend Engineering Patterns Owner; Metrics Definitions & Analytics Owner | RISK-02 | **Design-gate-triggering.** `ST-07` (net/gross basis) before `ST-08` (month-end snapshot) |
| EPIC-03 | S2-03 | Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; Financial Reporting & Records Owner | RISK-03 | `ST-09` (`BLG-BE-119`, live-capital decision) first; `ST-13` (`BLG-BE-122`) also touches the nightly stop-update path — after `ST-09` |
| EPIC-04 | S2-04 | Infrastructure & Operations Owner; FinOps & Resource Architect | RISK-04 | Independent of other EPICs |
| EPIC-05 | S2-05 | QA & Testing Owner; Director of Quality; QA Lead | RISK-05 | Independent of other EPICs |
| EPIC-06 | S2-06 | Data Model & Domain Schema Owner; Strategy Rules & System Intent Owner; Frontend Specifications & UX Documentation Owner; Head of Engineering; Metrics Definitions & Analytics Owner | RISK-06 | `ST-22` (`BLG-SPEC-148`) needs live-DB write access — human/delegated |
| EPIC-07 | S2-07 | Head of Specs Team; Product Owner; PMO Lead; FinOps & Resource Architect; AI Compliance & Governance Officer; Strategy Rules & System Intent Owner | RISK-07 | `ST-27` (`BLG-GOV-345`) before `ST-30` (`BLG-GOV-325`) — both bump governed prompts and `OPERATIONAL_GUIDE.md` |

**Design-gate-triggering EPICs this cycle:** EPIC-01 and EPIC-02 (8 items — double v9.5's 4 UI items, and the mix includes three new user-facing product features: `BLG-FEAT-96`/`97`/`98`).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Six frontend-visible stories across overlapping files (`TradePlans.js` is edited by 3 of them; `BLG-FE-181`/`182` span many pages/tables), each carrying a Playwright-covers-the-AC criterion — a merge-collision and CI-coverage load, with the design gate not yet run | Medium | Sequence per the table; one Playwright spec per observable AC (CLAUDE.md §2); `run design-gate` must pass before `plan sprint` seals; list remaining call sites for `BLG-FE-182` as follow-ups rather than widening scope | null |
| RISK-02 | EPIC-02 | `BLG-FR-05` (month-end snapshot + restatement diff) likely needs a new table/migration, a `data_model.md` entry and possibly a new endpoint (with its contract, `openapi.yaml` and `test.py` registration), but is sized `M (~2d)`; `BLG-FR-04`'s audit may find reported P&L is gross of fees — a correctness finding | Medium | `ST-07` first; if `ST-08` exceeds its estimate, deliver persistence with a disclosed partial and file the remainder rather than absorb it; file any discovered discrepancy as its own fix item — do not change reported figures inside these stories | null |
| RISK-03 | EPIC-03 | `BLG-BE-119` decides live-capital trailing-stop behaviour: removing the entry-price floor (option b) changes live trading; option (a) edits `claude/strategy/strategy_rules.md`, a governance file outside the engine's autonomous write scope; `BLG-BE-122` also modifies the nightly stop-update path | High | Decision-first: no change to `calculate_trailing_stop` without the Strategy Rules & System Intent Owner's explicit sign-off; add the golden-output case regardless; any `strategy_rules.md` edit goes through that owner's change route; `ST-13` lands after `ST-09` with timeout/retry-exhaustion tests. Resolved in-sprint by the story itself — not a sprint-planning-seal blocker | null |
| RISK-04 | EPIC-04 | `BLG-OPS-164` needs an Actions-write token and real Telegram receipt (the prior session's `gh workflow run` returned HTTP 403); `BLG-OPS-166` must prove a missed-run alert without disturbing live stops | Medium | Disclose any AC that cannot be closed rather than fabricate evidence (precedent: `ESC-EXEC-20260910-01`); test the dead-man's-switch against a simulated/non-production run marker; file a follow-up if live confirmation stays unavailable | null |
| RISK-05 | EPIC-05 | `BLG-QA-171` (bare `M`) requires a live staging environment and fresh seed; its "first quarterly run completed" AC cannot be verified in CI | Low | Sprint Planning tags that AC `[staging-only evidence]` and pre-files the deferral item if staging sign-off is post-merge (sprint-planning §7); document the procedure separately from the first-run evidence | null |
| RISK-06 | EPIC-06 | `BLG-SPEC-148` needs write access to the live database (available credential is read-only); its duplicate pre-check (0 groups at 2026-09-18) must be re-run immediately before applying | Medium | Human/delegated step; re-run the pre-check as the final safety net; disclose the "confirmed-applied" AC as not closeable rather than fabricating it if access is unavailable | null |
| RISK-07 | EPIC-07 | `ST-27`/`ST-30` edit governed prompts and bump `OPERATIONAL_GUIDE.md` — the same-version-collision class of CLAUDE.md §8 step 2a; `ST-29` writes `workforce_capacity.md`, permitted only where the sealed `sprint_backlog.md` names it (2026-09-19 write-scope ruling) | Medium | Sequence `ST-27` before `ST-30`; separate commit per bump with the full CLAUDE.md §6 checklist; Sprint Planning must name `workforce_capacity.md` in `ST-29`'s AC/sequencing note | null |
| RISK-08 | Release-level | Scope is exactly 100.0% of the 28-day ceiling (0% buffer; the §1.5 95% floor is exceeded) with two human-access dependencies (`ST-16`, `ST-22`), one decision gate on live behaviour (`ST-09`) and one sizing-uncertain item (`ST-08`) | Medium | Explicit Product Owner "use full capacity" instruction; Sprint Planning records the buffer-floor acknowledgement (sprint-planning §1.5); if slippage occurs, return items to the backlog in reverse selection order (last-selected first) — never silently | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Checked by script against the written files (not asserted): all 32 ST items in `stage4_backlog_slice.md` carry a `**Source:** BLG-xxx` reference resolving to an existing backlog entry in `claude/backlog/backlog.md` with no `✅ COMPLETE` banner (32/32; 32 unique sources, 32 unique ST IDs). ST headings in the slice equal the manifest's ST IDs in order. All 7 EPIC IDs are internally consistent between this file, the slice and the manifest. No `[ESTIMATE REQUIRED]`, `[AC REQUIRED]` or `[AWAITING SIGN-OFF]` placeholders in any story; every story has an effort field and at least one acceptance criterion.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` has 0 active initiatives — no pre-assigned Effort Bands. All 7 EPICs sized via inline estimate from each item's own `**Effort:**` field, converted per the rule stated in `run_manifest.md` (explicit day figure/range → midpoint; hours or bare `XS` → 0.15d; bare `S`/`M`/`L` → the canonical `workforce_capacity.md` table at 0.5 / 2.5 / 3.5d).

| EPIC | Items | Subtotal (days) |
|------|-------|-------------------|
| EPIC-01 — Product Features & Frontend Build-and-Ship | 6 | 6.75 |
| EPIC-02 — Financial Reporting & Records Integrity | 2 | 2.75 |
| EPIC-03 — Backend & Platform Engineering Debt | 5 | 4.55 |
| EPIC-04 — Operations & Security Debt | 4 | 1.90 |
| EPIC-05 — QA & Test Coverage Debt | 4 | 3.65 |
| EPIC-06 — Spec & Documentation Debt | 5 | 4.15 |
| EPIC-07 — Governance Process Debt | 6 | 4.25 |
| **Total** | **32** | **28.00** |

28.00 days vs the confirmed ~24–28 day band (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17) — within band, exactly at its upper bound (100.0% of the 28-day ceiling), matching the explicit "use full capacity" instruction. Sensitivity: 27.90 days under a band-letter-only reading of the same 32 items. **Capacity check outcome: pass, no WARN** (the WARN threshold is > 28 days), so no Phasing Recommendation is required. The §1.5 buffer floor (95% of capacity) is exceeded — a direct, disclosed consequence of the full-capacity instruction, to be acknowledged at Sprint Planning STEP 3.2.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 7 S2 IDs (S2-01..S2-07) map 1:1 to EPIC-01..EPIC-07. All 7 EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan table. All 8 RISK IDs (RISK-01..RISK-07 in the EPIC table, plus the release-level RISK-08) appear in the Risk Register Summary. No orphaned references found.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` for this cycle's own run (no escalation raised during this release-planning session). `decisions--2026-09-21__release-v9.6.md` is still produced per STEP 3's standing requirement (scope/sequencing decisions, not escalation-driven).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Change Log

| Date | Version | Change | Authority |
|------|---------|--------|-----------|
| 2026-09-21 | 1.0 | Initial publication — v9.6 release plan, 32 items / 7 EPICs / 28.00 days, full capacity; leads with an execution-heavy EPIC-01 seating the rebalance's mandatory build-and-ship pull-forward; design-gate-triggering (EPIC-01, EPIC-02) | Head of Specs Team (Release Planning Engine) |
