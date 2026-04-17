**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.8
**Cycle:** 2026-04-17__release-v2.8
**Last Updated:** 2026-04-17

---

# Release Plan — v2.8 Frontend Completion, Test Quality & AI Journal Feature

---

## Readiness

**Lifecycle guard:** prior cycle `2026-04-13__release-v2.7` status = `Closed` ✓

### Source Inputs
- Roadmap: `claude/roadmap/current_roadmap.md` — v2.8 listed as "Next planned release" ✓
- Backlog: `claude/backlog/backlog.md` — 7 items with Provisional-Target: v2.8
- Initiative Register: AI-SUM in Priority 2 (Next Phase) — BLG-FEAT-16 filed

### Backlog Candidates (Provisional-Target: v2.8)

| ID | Item | Priority | Effort | Design dep? |
|----|------|----------|--------|-------------|
| BLG-FE-14 | Market Correlation frontend view | P3 | M | No |
| BLG-GOV-08 | Engine prompt compression | P3 | L | No |
| BLG-GOV-11 | Cycle artefact inventory | P3 | M | No |
| BLG-FEAT-13 | Feature flag rollout capability | P3 | M | No |
| BLG-GOV-13 | Backlog archive deduplication | P3 | S | No — PO confirmation needed |
| BLG-FEAT-16 | AI Journal Summarisation | P3 | M | No — SRB-v1.7 (conditional) |
| BLG-QA-13 | Test scenario coverage gap (v2.7) | P3 | M | No |

### 1.1 Backlog Age Advisory
No spec/documentation debt items aged 2+ cycles without story assignment were identified in the v2.8 candidate list. All 7 items are backlog items (not spec debt). Advisories: none.

### 1.2 Provisional-Target Advisory
7 items carry `Provisional-Target: v2.8` — all horizon-planned for this release.
0 items have no matching Provisional-Target signal in the candidate pool.

### 1.3 Design-Gate Language Scan
Scanned 7 candidate items for design-gate language ("Product Owner to decide", "design decision required", "pending design", "requires UX decision"):
- BLG-FE-14: "Head of UX to confirm page placement — Analytics or Portfolio page" — **design dependency detected**
- All other items: no design-gate language found.

**Design dependency scan: 1 item flagged** (BLG-FE-14 — UX page placement decision required).
Recorded as outstanding action in run manifest. Non-blocking.

**Readiness verdict:** PASS — all preconditions met; proceed to scope extraction.

---

## Scope

### Release Scope Selection (Product Owner)

**In scope for v2.8 (6 items):**

| S2-ID | Epic | Item | Effort | Rationale |
|-------|------|------|--------|-----------|
| S2-01 | EPIC-01 | BLG-FE-14 — Market Correlation frontend view | M | Completes v2.7 deferred AC-6; backend live and spec'd; carry-forward obligation |
| S2-02 | EPIC-02 | BLG-QA-13 — Test scenario coverage (SC-CORR/SC-SIG-IND) | M | Fills known v2.7 test gap; QA maturity requirement |
| S2-03 | EPIC-03 | CF-1: DoQ Date field reminder (execution_prompt.md §3.2.A) | S | Carry-forward 1 from v2.7; governance hardening |
| S2-04 | EPIC-03 | CF-2: Sprint close terminology patch (sprint_close.md) | S | Carry-forward 2 from v2.7; governance hardening |
| S2-05 | EPIC-03 | BLG-GOV-13 — Backlog archive deduplication | S | Quick win; fixes ongoing ID uniqueness FAIL |
| S2-06 | EPIC-04 | BLG-FEAT-16 — AI Journal Summarisation | M | Gate-cleared initiative (SRB-v1.7); first AI feature; Priority 2 |

**Explicitly deferred:**

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-08 — Engine prompt compression | L effort; 4 consecutive deferrals (v2.4–v2.7); PO decision: defer to v2.9 with retirement review at v2.9 planning if not actioned | v2.9 (final deferral) |
| BLG-GOV-11 — Cycle artefact inventory | M effort; lower urgency given other governance items in scope | v2.9 |
| BLG-FEAT-13 — Feature flag rollout | M effort; not needed at current single-user scale; low strategic urgency | v2.9+ |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Frontend Specs & UX Owner | RISK-01 (UX placement TBD) | After design decision on page placement; no backend dependency |
| EPIC-02 | S2-02 | QA & Testing Owner | RISK-02 (spec version alignment) | Independent; after v2.7 canonical spec confirmed |
| EPIC-03 | S2-03, S2-04, S2-05 | Head of Specs Team + PMO Lead | RISK-03 (governance file versioning) | Governance file edit checklist mandatory; runs in Sprint 1 |
| EPIC-04 | S2-06 | Head of Engineering + Frontend Specs & UX Owner | RISK-04 (external LLM API; §13 sign-off gate) | Strategy Rules owner sign-off required before merge; external API key required |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | UX page placement not yet confirmed by Head of UX & Design (Analytics vs Portfolio page) | Medium | Head of UX & Design to decide at sprint planning pre-decisions; fallback: Analytics page per BLG-FE-14 spec | null |
| RISK-02 | EPIC-02 | SC-CORR/SC-SIG-IND scenarios must reference analytics_endpoints.md v2.1.0 and signal_endpoints.md v1.1 exactly; version drift would invalidate scenarios | Low | QA owner to verify spec versions before authoring; both specs confirmed live from v2.7 delivery | null |
| RISK-03 | EPIC-03 | Governance prompt patches require CLAUDE.md §6 checklist (version bump, OPERATIONAL_GUIDE update, change log entry) — omission creates non-compliant state | Medium | Must-do checklist in AC for each ST story touching governed prompts | null |
| RISK-04 | EPIC-04 | (a) External LLM API adds operational cost and potential latency; (b) Strategy Rules owner sign-off required before any merge of AI output integration | High | (a) API key via env var; timeout/fallback on API unavailability; (b) Strategy Rules owner sign-off is an explicit AC — must be in-sprint action, not deferred to post-ship | null |

RISK-04 is **High priority** with mandatory Strategy Rules owner sign-off before merge — this must be resolved in-sprint. Flagging for Pre-sprint Required Decisions checklist.

---

## Integrity Validation — 3.5 Local Model Integrity

**Checks:**

1. **All S2 IDs have a defined scope item:** S2-01 through S2-06 — all defined ✓
2. **Every EPIC-ID declared in scope table maps to S2 items:** EPIC-01→S2-01, EPIC-02→S2-02, EPIC-03→S2-03/S2-04/S2-05, EPIC-04→S2-06 ✓
3. **Every RISK-ID in execution plan has a Risk Register row:** RISK-01 through RISK-04 — all rows present ✓
4. **No circular sequencing dependencies:** EPIC-01 depends on design decision; EPIC-02 independent; EPIC-03 independent; EPIC-04 depends on Strategy Rules sign-off in-sprint. No circularity ✓
5. **All deferred items explicitly listed:** BLG-GOV-08, BLG-GOV-11, BLG-FEAT-13 — all listed ✓
6. **Plan structured:** all required sections present ✓

**Model integrity:** PASS — plan_structured = true; plan_executable = true.

---

## Capacity Check

### Effort Estimates (inline — no scored_initiatives.md matches)

| EPIC | Stories | Inline Effort | Est. Hours (mid) |
|------|---------|---------------|-----------------|
| EPIC-01 | 1 (ST-01) | M (~1–2 days) | 12 hrs |
| EPIC-02 | 2 (ST-02, ST-03) | M (~1–2 days each) | 16 hrs |
| EPIC-03 | 3 (ST-04, ST-05, ST-06) | S + S + S | 8 hrs |
| EPIC-04 | 2 (ST-07, ST-08) | M + M (~1–2 days each) | 16 hrs |
| **Total** | **8 stories** | | **~52 hrs** |

### Capacity Assessment
- Solo dev, evenings — estimated capacity: ~3–4 hrs/evening, 5 evenings/week = ~15–20 hrs/week
- 52 hrs total ÷ 17.5 hrs/week avg = ~3 weeks = 2 sprints of 1.5 weeks each
- Velocity: 0.99 (last 6 cycles) — no reason to discount

**Capacity verdict: PASS** — 52 hrs across 2 sprints is achievable at current velocity.

### Sprint Phasing Recommendation

**Sprint 1 (higher urgency / independence):**
- EPIC-02 (test scenarios) — 16 hrs — independent, quality foundation
- EPIC-03 (governance patches + deduplication) — 8 hrs — quick wins, carry-forward obligations
Total Sprint 1: ~24 hrs ✓

**Sprint 2 (frontend + AI feature):**
- EPIC-01 (market correlation frontend) — 12 hrs — depends on UX design decision in pre-sprint
- EPIC-04 (AI journal summarisation) — 16 hrs — depends on external API setup + strategy sign-off in-sprint
Total Sprint 2: ~28 hrs ✓

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**Checks:**

1. **Every S2-ID appears in exactly one EPIC:** S2-01→EPIC-01, S2-02→EPIC-02, S2-03/04/05→EPIC-03, S2-06→EPIC-04 ✓
2. **Every EPIC-ID in execution plan has a corresponding stage4_backlog_slice entry:** (confirmed at STEP 4) ✓
3. **RISK-IDs in execution plan each have an escalation_ref field:** all set to null (no escalations raised) ✓
4. **No scope items in backlog slice that are not in stage2 scope:** (confirmed at STEP 4) ✓
5. **Deferred items not present in backlog slice:** BLG-GOV-08, BLG-GOV-11, BLG-FEAT-13 not in slice ✓
6. **Assumption timebox/capacity matches state.json:** none specified (default) ✓

**Cross-stage integrity:** PASS

---

## Integrity Validation — 5.7 Decision Record Integrity

**Trigger check:** Are there any Accepted Risk escalations in this cycle?
- accepted_risk_escalations = [] — no AR records
- No SRB records required

**Decision record check:**
- `docs/product/decisions/decisions--2026-04-17__release-v2.8.md` — present ✓
- Scope decisions table populated ✓
- Sequencing decisions table populated ✓
- Accepted risks: None ✓

**Decision record integrity:** PASS (not_applicable for AR/SRB since none raised)
