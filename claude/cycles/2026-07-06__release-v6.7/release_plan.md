Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Published
Release: v6.7
Cycle: 2026-07-06__release-v6.7
Last Updated: 2026-07-06

---

# Release Plan — v6.7

## Readiness

**Prior cycle:** `2026-06-26__release-v6.3` (`.claude_current_state.json` `prior_cycle` field — stale pointer, several releases old). Most recently closed release: `2026-07-04__release-v6.6` (Verified, Closed_with_actions, post_ship_complete=true).

**Roadmap status:** `current_roadmap.md` §3 (Now horizon) remains empty — Arc 1/Arc 2 fully complete; Arc 3 fully complete; Arc 4–6 remainder (PO-02/PO-04, SI-02/SI-04/SI-05, all Arc 6) remain data-density-gated. v6.7 exists on the roadmap via the documented STEP 8.1 Option (b) deferral from `2026-07-06__scheduled` (see `run_manifest.md` §-1.2).

**Readiness determination: READY.** Scope is drawn from (a) the now-**mandatory** (not advisory) Skill-Silo pull-forward clause (`roadmap_prompt.md` §7.1 v8.3 — requires ≥2 build-and-ship-shaped U-items; candidates `BLG-FE-87`/`BLG-FE-88` named directly by the `2026-07-06__scheduled` rebalance) and (b) the 4-item Lifecycle Audit AUD-2026-07-06 improvement backlog (`BLG-GOV-167`–`170`, all filed 2026-07-06, all `Provisional-Target: v6.7`). Full rationale at `run_manifest.md`.

**SI-02 re-verification attempt (carry-forward priority action):** This session attempted the production trade-count re-check flagged by the `2026-07-06__scheduled` rebalance's `lessons_learnt.md` as a priority action for the next data-access-capable engine. `~/.api_keys` contains only `RENDER_API_KEY` (platform management), no application `X-API-Key`; a direct request to the production backend (`https://trading-assistant-api-c0f9.onrender.com/`) returned `HTTP 401`. **Verification remains blocked** — same outcome as the rebalance session. Not a release-planning blocker: SI-02 is not a v6.7 scope candidate regardless of trade count, as gate conditions (2) p99 latency and (3) drift-score meaningfulness are independently unverified. Recorded for PMO Lead to re-attempt with proper credentials.

### 1.1 Backlog Age Advisory
No spec/documentation debt item found flagged with an explicit multi-cycle non-assignment marker in `backlog.md` (searched "consecutive cycles" / "cycles without" / carry-forward aging language — none matched for scope candidates). No advisory triggered.

### 1.2 Provisional-Target Advisory
7 items carry `Provisional-Target: v6.7` or an equivalent firm elevation: `BLG-FE-87` (Target: v6.7, firm — elevated by PO comment on PR #918), `BLG-FE-88`, `BLG-FE-89`, `BLG-GOV-167`, `BLG-GOV-168`, `BLG-GOV-169`, `BLG-GOV-170` (all Provisional-Target: v6.7). All 7 are horizon-planned for this release and form the full scope candidate list — no items with `Provisional-Target: v6.7` were excluded.

### 1.3 Design-Gate Language Scan
No scope candidate contains the literal phrases "design decision required" / "pending design" / "requires UX decision". However `BLG-FE-87`/`BLG-FE-88` carry explicit observable-UI acceptance criteria (WCAG-AA contrast pass, Playwright/staging sign-off) independently driving `delegated_frontend` classification at STEP 4.1 (same pattern as v6.6's `BLG-FE-40`). `BLG-FE-89` documents a design-system convention but its AC is documentation-only (no rendering claim) — classified as spec/documentation debt, not itself design-gate-triggering. `BLG-GOV-167`–`170` are governance/process items with no UI surface.

### 1.4a Perennial-Return Check
None of the 7 candidates appear in `2026-07-04__release-v6.6`'s `stage4_backlog_slice.md` with `returned_to_backlog`/`deferred` status — all were filed 2026-07-06 (post-v6.6 audit and post-v6.6 UX contrast sweep), entering release-planning scope for the first time. No perennial-return disposition required.

### 1.4b Within-Sprint Date Gate Classification
No scope candidate carries a calendar-date gate condition. `BLG-FE-88`/`BLG-FE-89` carry a **sequencing dependency** (must follow `BLG-FE-87`), not a date gate — §1.4b does not apply to ordering dependencies. No item requires mandatory-conditional classification under this rule.

### 1.4 Gate-Condition Proximity Scan

| Item | Gate condition | Current trajectory | Projected clear date |
|------|-----------------|---------------------|------------------------|
| SI-02 (Behavioural Drift Detection) | ≥20 closed trades with linked trade_plans (+ p99 latency + drift-score meaningfulness) | Last formally confirmed: 15 (2026-06-23). Unverified self-report: 20 (2026-07-03, user). This session's re-verification attempt blocked (no application API key — see Readiness above) | Condition (1) potentially cleared but unconfirmed; conditions (2)/(3) trajectory unknown |
| PO-02 (Journal Pattern Recognition) | 6+ months of AI-summarised journal entries | trajectory unknown — not queried this session | data not available — Product Owner to surface at readiness review |
| PO-04 (Reflection ↔ Outcome Correlation) | 50+ trades with plans | long-horizon at ~1–2 trades/month pace per prior rebalance estimates | ≈2026-Q4/2027 (indicative only) |

**Do not halt.** Advisory only. None of the 3 gated items above are v6.7 scope candidates.

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass
```

---

## Scope

No backlog items were newly filed this session for v6.7 scope — all 7 items (`BLG-FE-87/88/89`, `BLG-GOV-167/168/169/170`) already existed in `backlog.md`, filed 2026-07-06 by prior sessions (ST-01 contrast audit follow-up; Lifecycle Audit AUD-2026-07-06 improvement backlog). No scope change or reprioritisation was made to the global backlog beyond the release slice itself.

### Items in scope

| S2-ID | Backlog item | Description | Priority | Effort |
|-------|--------------|-------------|----------|--------|
| S2-01 | BLG-FE-87 | Dark-theme secondary-text contrast fix (`text-slate-500`, ~262 instances/~90 files) | P1 (firm) | L (~2–3 days) |
| S2-02 | BLG-FE-88 | Light-theme secondary-text contrast fix (missing `dark:`/light: variants, 764 instances/102 files) — sequenced after S2-01 | P2 | L (~3–4 days) |
| S2-03 | BLG-FE-89 | Shared secondary-text design token/component to prevent recurrence | P3 | M (~1–2 days) |
| S2-04 | BLG-GOV-167 | Grant `.claude/skills/` write-scope authority; apply carried commit-check diff-verification patch | P1 | M (~1–2 days) |
| S2-05 | BLG-GOV-168 | Structural guard (count-before/after) for 4 append-only governance logs, applied at each engine's write step | P2 | M (~1–2 days) |
| S2-06 | BLG-GOV-169 | `audit.py` SLA — require same-session commit of audit reports | P2 | XS (<1 hour) |
| S2-07 | BLG-GOV-170 | Document sprint-status-line update at Delivery Verification STEP 6 | P3 | XS (<1 hour) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| SI-02 (Behavioural Drift Detection) | Trade-count condition unresolved (15 confirmed vs. 20 self-reported); p99 latency and drift-score conditions independently unverified; this session's re-verification attempt blocked by missing API credentials | Re-check at next release/roadmap cycle once PMO Lead formally re-verifies via production query with proper credentials |
| PO-02/PO-04 (Arc 4 remainder) | Data-density gates not met | Re-check at next release planning readiness scan |
| BLG-SPEC-35 (PO-02 §13 boundary review) | Gate: PO-02 sprint planning imminent — not met (PO-02 itself gated on 6-month journal data density) | Re-review when PO-02 sprint planning becomes imminent |
| BLG-FE-90, BLG-BE-43/44/45, BLG-QA-75–78, BLG-OPS-88–92, BLG-SPEC-67, BLG-FEAT-61/62/63, BLG-GOV-171–177, BLG-SEC-10 (all filed by `2026-07-06__scheduled` rebalance) | All explicitly gate-conditional (design-phase trigger, stability window, signal-triggered, or audit-bundle) per `workforce_capacity.md` §Rebalance 2026-07-06 — none carry `Provisional-Target: v6.7` | Re-evaluate as respective gates clear |

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-03 | Base44 Frontend Prompt Owner / Head of UX & Design | RISK-01, RISK-02 | S2-02 must land after S2-01 merges; S2-03 recommended last (documents the final canonical treatment) |
| EPIC-02 | S2-04, S2-05, S2-06, S2-07 | Head of Specs Team | RISK-03, RISK-04 | None — independent of EPIC-01; S2-06/S2-07 (XS) may run in parallel with S2-04/S2-05 |

**EPIC-01 (UX & Accessibility Contrast Remediation):** Both S2-01 and S2-02 fix the same defect class (ad hoc secondary-text colour choice) across dark and light theme respectively — the audit that found them (BLG-FE-82, v6.6 ST-01) explicitly recommends sequencing to avoid rework. S2-03 generalises the fix into a shared token so the defect class does not recur a third time. This EPIC satisfies the mandatory Skill-Silo pull-forward clause (`roadmap_prompt.md` §7.1 v8.3): S2-01/S2-02 are both build-and-ship-shaped, ungated U-items.

**EPIC-02 (Governance Process Hardening):** All 4 items originate from Lifecycle Audit AUD-2026-07-06 (overall score 81, all 17 prior findings resolved) as its improvement backlog. S2-04 directly resolves the 3-cycle-carried `/commit-check` write-scope escalation (`ESC-CLOSE-20260706-01`, v6.6 carry-forward item 1) — do not let a 4th cycle pass unresolved. S2-05/06/07 are documentation/process hardening items with no code-path dependency on S2-04.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | S2-01/S2-02 together touch ~1,026 text-colour instances across ~190 files (largest contrast remediation attempted to date; prior fixes BLG-UX-01/02 touched 1 file each) — scale increases regression risk if reviewed only by code inspection | High | Both items' own ACs require Playwright coverage or recorded staging sign-off per CLAUDE.md's frontend-visible-change rule; phase by page traffic/visibility per each item's Scope section; per-surface contrast spot-checks recorded | null |
| RISK-02 | EPIC-01 | S2-02 (light theme) landing before or interleaved with S2-01 (dark theme) risks a `dark:` variant being added against a base colour that S2-01 is simultaneously changing, causing rework or a merge conflict | Medium | Explicit sequencing constraint (S2-02's own `**Depends on:**` field); enforce S2-01 merge-to-main before S2-02 branch work begins | null |
| RISK-03 | EPIC-02 | S2-04 grants standing write-scope authority outside any governed routine's declared scope for the first time in this repository — a precedent-setting change to `shared_standards.md` | High | Scope narrowly to the `.claude/skills/` path only, naming Head of Specs Team explicitly (not open-ended); apply only the already-drafted commit-check diff-verification patch under that authority, nothing broader | null |
| RISK-04 | EPIC-02 | S2-05's structural guard touches 4 separate engines' write steps (`release_planning_prompt.md`, `execution_prompt.md`, `delivery_verification_prompt.md`, plus the `delegation_log.md`-owning engine); partial application would repeat the exact "documentation-only, zero adoption" failure that created this backlog item | Medium | Item's own AC requires direct read-verification of each of the 4 engines' actual write steps post-change, not documentation alone | null |

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Verified: all 7 backlog items referenced by S2-01 through S2-07 (`BLG-FE-87`, `BLG-FE-88`, `BLG-FE-89`, `BLG-GOV-167`, `BLG-GOV-168`, `BLG-GOV-169`, `BLG-GOV-170`) exist exactly once each in `claude/backlog/backlog.md` (confirmed via direct grep). Every S2-ID maps to exactly one EPIC-ID (EPIC-01: S2-01/S2-02/S2-03; EPIC-02: S2-04/S2-05/S2-06/S2-07) and every EPIC declares its scope-item set consistently between the Scope and Execution Plan sections. Every RISK-ID (RISK-01/02/03/04) declared in the Execution Plan EPIC table appears as a row in the Risk Register Summary with `Relates to` pointing to a valid EPIC-ID. No orphaned references found. PASS.

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## STEP 4 — Backlog Slice (Committed)

`stage4_backlog_slice.md` written (7 stories, ST-01 through ST-07, across EPIC-01/EPIC-02, all Firm). Backlog lock `RP:v6.7:2026-07-06__release-v6.7` acquired, transaction `BLTX-20260706-01` prepared → committed, release-slice section written to `claude/backlog/backlog.md` with the required marker, lock released. `stage4_issue_manifest.json` written (7 entries; `--issues` defaults to `none` so no GitHub/import artefact generated at this stage — deferred to STEP 10).

### STEP 4.1 — Design Gate Classification

⚠ **DESIGN GATE REQUIRED before plan sprint — 2 items classified as UI-facing** (ST-01 `BLG-FE-87`, ST-02 `BLG-FE-88` — both `delegated_frontend` with observable UI acceptance criteria: WCAG-AA contrast pass verified per-surface). ST-03 (`BLG-FE-89`) is documentation-only (no rendering claim) and does not independently trigger the gate. Run: `run design-gate --cycle 2026-07-06__release-v6.7`

```yaml
# state.json update (STEP 4 outcome):
artifacts.stage4_backlog_slice: pass
artifacts.stage4_issue_manifest: pass
attributes.backlog_committed: true
attributes.design_gate_required: true
status: Committed
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No matching row in `scored_initiatives.md` for any of EPIC-01/02 (confirmed at STEP 0 — file's most recent entries predate 2026-06-07; all 7 backlog IDs in this cycle's scope were filed 2026-07-06). Per the three-tier resolution rule, this falls to tier 3: use STEP 4 inline estimates; no advisory required.

| EPIC | Stories | Estimated effort (mid-point) |
|------|---------|-------------------|
| EPIC-01 | ST-01, ST-02, ST-03 | ~2.5 + 3.5 + 1.5 ≈ 7.5 days |
| EPIC-02 | ST-04, ST-05, ST-06, ST-07 | ~1.5 + 1.5 + 0.1 + 0.1 ≈ 3.2 days |
| **Total** | 7 stories | **≈ 10.7 days** |

**Assumptions:** `--timebox` and `--capacity` were not specified at invocation (both default to empty per `state.json.assumptions`). No explicit capacity figure exists to check against.

**Outcome:** ≈10.7 days sits within the historical range of firm-scope sprints delivered since v5.0 (typically 5–15 days of story effort; v6.6 was an outlier-light 3.5 days), but toward its upper half. This is a **PASS**, not a WARN — no phasing recommendation is mandated. However, the EPIC-01 internal sequencing constraint (S2-02 after S2-01) means Sprint Planning should weigh whether both fit in a single sprint or should phase across two: EPIC-02 (3.2 days, no dependency) can run fully in parallel with EPIC-01's sequential chain, so a natural single-sprint fit exists if capacity allows; if not, EPIC-02 + S2-01 in Sprint 1, S2-02 + S2-03 in Sprint 2 is the recommended split. This sequencing note is advisory to Sprint Planning, not a mandatory Phasing Recommendation (reserved for WARN outcomes).

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Roadmap Annotation

No formal `## v6.7` roadmap section exists (Option (b)-deferred release). Per §5 fallback rule, annotated the `**Next planned release:**` line in `current_roadmap.md` §1 instead. Lock `RA:v6.7:2026-07-06__release-v6.7` acquired, `roadmap_txn.json` prepared → committed, annotation written with marker, lock released.

```yaml
# state.json update (STEP 5):
artifacts.roadmap_txn: committed
locks.roadmap_lock.status: released
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 7 S2 IDs (S2-01 through S2-07) map to exactly one of EPIC-01/02; EPIC IDs in `stage4_backlog_slice.md` (EPIC-01, EPIC-02) match the Execution Plan's EPIC table exactly; all 4 RISK IDs (RISK-01, RISK-02, RISK-03, RISK-04) referenced in the EPIC table appear as rows in the Risk Register Summary; no orphaned references. No Stage 2/3/4 artefact has changed since the STEP 3.5 pass. PASS.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations were raised this cycle). `not_applicable`.

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Publish Gate

All engine-specific conditions verified: `open_escalations` empty; `deferred_execution_blockers` empty; `stage4_5_capacity_check = pass`; `stage5_5_cross_stage_integrity = pass`; `stage5_7_decision_record_integrity = not_applicable`; `stage1_readiness`/`stage3_5_model_integrity = pass`; `plan_structured`/`plan_executable`/`backlog_committed = true`. Gate PASSES. `docs/product/scope/scope--2026-07-06__release-v6.7-contrast-and-governance-hardening.md` and `docs/product/decisions/decisions--2026-07-06__release-v6.7.md` exist; both locks released. Completion conditions met.

```yaml
# state.json terminal update:
status: Validated → Published (on STEP 9 global sync)
publish_eligible: true
sealed.sealed_utc: 2026-07-06T15:00:00Z
```

---

**Design Gate:** REQUIRED — 2 UI-facing stories (ST-01, ST-02). Run `run design-gate --cycle 2026-07-06__release-v6.7` before invoking `plan sprint`.
