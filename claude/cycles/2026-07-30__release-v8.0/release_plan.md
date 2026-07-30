Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-30
Cycle: 2026-07-30__release-v8.0
Release: v8.0

# Release Plan — v8.0

## Readiness

Preflight (STEP -1) passed all hard gates. Prior cycle `2026-07-28__release-v7.10` is `Closed` with `post_ship_complete = true` and `next_cycle_unblocked = true`. No `## v8.0` roadmap section exists; this release is scoped via the STEP -1.2 Option (b) equivalence rule, citing the `2026-07-28__scheduled` rebalance's documented STEP 8.1 Option (b) decision (Now horizon fully empty, deferred again, no newly-ready anchor content that cycle). See `run_manifest.md` for full STEP -1 detail and the STEP 1.1/1.2/1.3/1.4/1.4a/1.4b advisory outputs, including a self-caught scope correction (`BLG-OPS-48` removed — see run_manifest.md).

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

No scope changes to strategy or roadmap boundaries. This section extracts a backlog-driven scope slice (no formal roadmap release section exists yet for v8.0 — see Readiness above). No explicit user grouping/capacity instruction was given this session; items are grouped into a small set of thematic EPICs, consistent with the pattern established at v7.8/v7.9/v7.10.

### Items in scope

| S2-ID | Epic | Item | Description |
|-------|------|------|-------------|
| S2-01 | EPIC-01 | BLG-SPEC-78 | `strategy_version_at_entry` field on trade/trade_plan |
| S2-02 | EPIC-01 | BLG-SPEC-79 | FX handling review post-DS-05 US market source change |
| S2-03 | EPIC-01 | BLG-SPEC-107 | FX conversion audit trail completeness check (§4.1.5 effective-rate logging) |
| S2-04 | EPIC-02 | BLG-SEC-25 | Raw exception text leaked in 16 implicit-HTTP-200 error paths in backend/main.py |
| S2-05 | EPIC-02 | BLG-SEC-23 | Mandatory security review checklist for new AI-calling endpoints |
| S2-06 | EPIC-02 | BLG-FE-135 | Trade Plan pre-entry checklist items unreachable by keyboard |
| S2-07 | EPIC-02 | BLG-FE-136 | Trade Plan "Abandon" modal has no focus trap or restoration |
| S2-08 | EPIC-02 | BLG-SEC-24 | Verify `request.client.host` reflects true client IP behind Render's proxy |
| S2-09 | EPIC-02 | BLG-SEC-26 | `.gitleaks.toml` global `[[allowlists]]` blocks use an invalid schema |
| S2-10 | EPIC-03 | BLG-QA-97 | Retroactive Playwright §18 anti-pattern sweep (consolidated) |
| S2-11 | EPIC-03 | BLG-QA-120 | Test-tagging convention (smoke/regression/critical) for selective CI runs |
| S2-12 | EPIC-03 | BLG-QA-121 | Synthetic trade-history data generator for gated-feature testing |
| S2-13 | EPIC-04 | BLG-OPS-114 | Render service health-check alerting to Telegram on 5xx spike |
| S2-14 | EPIC-04 | BLG-OPS-115 | Configure TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID as GitHub Actions repo secrets |
| S2-15 | EPIC-04 | BLG-OPS-109 | Confirm Render rollback runbook has real execution history |
| S2-16 | EPIC-04 | BLG-OPS-124 | Render dashboard-only build/deploy path filter audit (invisible to repo grep) |
| S2-17 | EPIC-04 | BLG-OPS-126 | Backup & disaster recovery runbook for production database |
| S2-18 | EPIC-05 | BLG-FE-124 | Reusable Base44 prompt fragment library for common layouts |
| S2-19 | EPIC-06 | BLG-GOV-263 | Structural fix for recurring cross-EPIC `execution_state.json` merge-conflict pattern |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-OPS-48 | Real future-dated gate (`Gate date: 2026-11-01`), ~3 months past this cycle's date — self-caught during scope write-up, see `run_manifest.md` | ~v4.9 candidate pool, no earlier than 2026-11-01 |
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate NOT MET / §13 determinism pre-clearance not run; standing PO perennial-return disposition (Option (b), unchanged since `manage roadmap` 2026-07-30) | Unscheduled, pending gate clearance |
| Arc 5 pre-entry/compliance-gateway UX cluster (BLG-FEAT-44/56, BLG-FE-43/45/54/58/59/62/63/68/69/70/71) + BLG-SPEC-35 | Escalated to P1 as a value-judgment priority override 2026-07-27/28, but every item's own gate criteria remain unmet | Unscheduled, pending respective gate clearance |
| Remaining ~145 ungated P2/P3 candidates not selected this cycle (e.g. remaining BLG-GOV-*/BLG-SPEC-*/BLG-OPS-* process/spec items) | Capacity — full band reached by the 19 items above | v8.1 candidate pool |

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** compact table per IMP-08; full acceptance criteria live in `stage4_backlog_slice.md`.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01, S2-02, S2-03 | Data Model & Domain Schema Owner; Financial Reporting & Records Owner | — | None |
| EPIC-02 | S2-04, S2-05, S2-06, S2-07, S2-08, S2-09 | Cybersecurity & Trust Lead; Head of Engineering; Head of UX & Design | RISK-01, RISK-02, RISK-03 | None |
| EPIC-03 | S2-10, S2-11, S2-12 | Director of Quality; QA Lead; QA & Testing Owner | — | None |
| EPIC-04 | S2-13, S2-14, S2-15, S2-16, S2-17 | Infrastructure & Operations Owner; FinOps & Resource Architect | — | S2-14 (Telegram secrets) should land before/alongside S2-13 (5xx alerting) — both depend on the same credential pair |
| EPIC-05 | S2-18 | Base44 Frontend Prompt Owner | — | None |
| EPIC-06 | S2-19 | Head of Engineering | RISK-04 | None |

EPIC-02: carries at least two observable UI acceptance criteria (BLG-FE-135 keyboard operability/`aria-checked`; BLG-FE-136 focus trap/restoration/Escape) — classified `design_gate_required = true` at STEP 4.1 below.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-02 | BLG-FE-135/BLG-FE-136 carry observable UI interaction acceptance criteria (keyboard operability, focus trap/restoration) and require Design Gate PASS before Sprint Planning may seal | Medium | Run `run design-gate --cycle 2026-07-30__release-v8.0` promptly after this plan publishes; per CLAUDE.md, Playwright coverage or recorded staging sign-off required for each observable AC | null |
| RISK-02 | EPIC-02 | BLG-SEC-24 requires live verification against the production Render deployment and a possible uvicorn trusted-proxy config change (`--proxy-headers`/`--forwarded-allow-ips`); an over-broad forwarded-IP trust config could let a spoofed header override the real client IP, while an under-scoped one leaves the rate-limit collapse unfixed | Medium | Scope `--forwarded-allow-ips` narrowly to Render's documented edge range only (never a blanket wildcard); re-verify live post-change that distinct real clients get independent rate-limit buckets | null |
| RISK-03 | EPIC-02 | BLG-SEC-26's `.gitleaks.toml` rewrite touches secret-suppression rules; an over-broad rewritten allowlist rule could silently suppress a genuine future secret leak | Low-Medium | Explicit `condition = "AND"` and `regexTarget = "match"` on every rewritten block; verify each block's suppression via an actual local `gitleaks detect` run against its target file, not just TOML syntax validity | null |
| RISK-04 | EPIC-06 | BLG-GOV-263 is an L-effort (~3-5 day) structural fix to the recurring cross-EPIC `execution_state.json` merge-conflict pattern, touching `execution_prompt.md` and/or CI tooling that every future multi-EPIC sprint depends on; a flawed implementation could introduce a new failure mode across the next sprint's branches | Medium | Head of Engineering sign-off required before the mechanism is used live; validate on the very next multi-EPIC sprint with the existing reactive-resolution mechanism (`shared_standards.md` §12) kept as a documented fallback if the new mechanism misbehaves | null |
| RISK-05 | Release-level | Scope sized to ~26.25 days midpoint against the confirmed ~24-28 day capacity band (~94-109% utilisation depending on denominator), leaving limited slack for in-sprint surprises — consistent with the top-of-band pattern used at v7.8/v7.9/v7.10, applied by default here since no contrary user instruction was given this session | Medium | STEP 4.5 Capacity Check below confirms no over-allocation against the ceiling; EPIC-06 (single item, most divisible) is the natural trim candidate if early sprint velocity signals overrun | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All EPIC-ID / S2-ID / RISK-ID cross-references above resolve internally (19 S2-IDs ↔ 6 EPIC-IDs, grouped; 4 RISK-IDs reference EPIC-IDs present in the Scope table plus 1 Release-level RISK-ID). No orphaned references found.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14, `shared_standards.md` §16.7):** 0 of the 19 in-scope items have a matching row in `claude/scoring/scored_initiatives.md` (all are backlog-driven items, not roadmap initiatives; the `2026-07-27__scheduled` rebalance's scored_initiatives.md scored 0 items — Debate Queue empty). Tier 3 applies uniformly: STEP 4 inline estimate used for all 19, no advisory required.

### Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None scarce this cycle — 6 EPICs span 8 distinct owner roles, no concurrent scarce-skill collision identified
```

### Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) |
|------|------|-------------|------------------|
| EPIC-01 | BLG-SPEC-78 | M | 2.0 |
| EPIC-01 | BLG-SPEC-79 | S | 1.0 |
| EPIC-01 | BLG-SPEC-107 | S | 1.0 |
| EPIC-02 | BLG-SEC-25 | S | 1.0 |
| EPIC-02 | BLG-SEC-23 | S | 1.0 |
| EPIC-02 | BLG-FE-135 | S | 1.0 |
| EPIC-02 | BLG-FE-136 | S | 1.0 |
| EPIC-02 | BLG-SEC-24 | S | 1.0 |
| EPIC-02 | BLG-SEC-26 | S | 1.0 |
| EPIC-03 | BLG-QA-97 | S | 1.0 |
| EPIC-03 | BLG-QA-120 | M | 2.0 |
| EPIC-03 | BLG-QA-121 | M | 2.0 |
| EPIC-04 | BLG-OPS-114 | M | 2.0 |
| EPIC-04 | BLG-OPS-115 | XS | 0.25 |
| EPIC-04 | BLG-OPS-109 | S | 1.0 |
| EPIC-04 | BLG-OPS-124 | S | 1.0 |
| EPIC-04 | BLG-OPS-126 | S | 1.0 |
| EPIC-05 | BLG-FE-124 | M | 2.0 |
| EPIC-06 | BLG-GOV-263 | L (~3-5 days) | 4.0 |

All 19 items carry an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

### Total Effort vs Capacity

```
Total estimated effort:  ~26.25 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~94-109% (depending on which end of the band is used as denominator)
Outcome:                 pass (does not exceed the ~28-day ceiling)
```

No over-allocation against the confirmed ceiling. STEP 3/STEP 4 scope selection includes all 19 items across 6 grouped EPICs — a top-of-band fill by default, not a phasing scenario, so no `### Phasing Recommendation` subsection is required (that subsection is required only on a `warn` outcome; this is `pass`).

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

Verified: all 19 S2-IDs map to EPIC-IDs in both `## Scope` and `## Execution Plan` (grouped, 3/6/3/5/1/1 per EPIC); all 6 EPIC-IDs in `stage4_backlog_slice.md` match the Execution Plan table exactly; all 4 RISK-IDs referenced in the Execution Plan table appear in the Risk Register Summary (plus RISK-05, Release-level); no orphaned S2/EPIC/RISK references found. `stage4_issue_manifest.json` contains exactly 19 entries (ST-01 through ST-19), one per story, labels consistent with `cycle:2026-07-30__release-v8.0`.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations were raised this cycle; capacity outcome was `pass`, not `warn`/`fail`, so the escalation subroutine never triggered).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
