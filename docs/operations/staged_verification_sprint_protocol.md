**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-21
**Source:** BLG-GOV-89 — Staged verification sprint pattern; validated v4.7 (first use) and v5.0 (confirmed)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Staged Verifications Sprint Protocol

## 1. Purpose

This document defines the governed protocol for declaring and executing a "staged verifications" sprint — a sprint whose scope consists primarily or exclusively of verifying staging-only acceptance criteria (ACs) deferred from prior releases.

Staged verification sprints are not a workaround for incomplete delivery. They are a planned mechanism for completing verification work that legitimately requires production-equivalent infrastructure, real data, or operational tooling not available during standard development execution.

---

## 2. Trigger Conditions

Declare a staged verifications sprint when **all** of the following are true:

1. **Volume threshold:** Three or more staging-only ACs are outstanding across one or more prior release EPICs.
2. **Age threshold:** At least one outstanding staging-only AC is 30 days or older (i.e., deferred two or more sprints).
3. **Infrastructure readiness:** The staging or production environment is accessible, stable, and has representative data for the verification period.
4. **Sprint capacity:** Available sprint capacity is insufficient to deliver meaningful new feature stories alongside the staged verification work (i.e., verification work would dominate capacity).

**Inline verification path:** If fewer than three staging-only ACs are outstanding, or if the environment is not ready, defer to the next planning cycle as a low-priority story in an otherwise feature-focused sprint (the "inline" path, not a standalone staged verifications sprint).

**Historical examples:**
- v4.7 (first use): BLG-OPS-28/44/45 — Render build minutes monitoring, health check staging runs, external API risk staging confirmation
- v5.0 (confirmed): BLG-OPS-52 — Deploy pipeline verification on restored build minutes

---

## 3. Batching Approach

### 3.1 Grouping Criteria

Group deferred staging ACs into sprint stories using these criteria:

| Grouping factor | Rule |
|-----------------|------|
| **By environment** | Group ACs that require the same environment (staging vs production) into the same story to minimise context-switching |
| **By owner** | Group ACs with the same Infrastructure & Operations Owner into single stories (one sign-off covers all) |
| **By system domain** | Group ACs that verify related system behaviour (e.g., all compliance metrics ACs together) |
| **Age priority** | Age ≥ 60 days: highest priority — address in the first story block of the sprint |

### 3.2 Story Structure

Each staged verification story follows this structure:

- **Title:** `[BLG-OPS-xx]: <system domain> staging verification`
- **Delegation class:** `autonomous` (engine writes the verification plan and evidence structure; I&O Owner executes on staging)
- **Owner:** Infrastructure & Operations Owner (for staging execution) + Director of Quality (for sign-off)
- **Effort estimation:** See §5 Sprint Sizing
- **Staging-only ACs:** List each deferred AC explicitly with source release and EPIC reference

### 3.3 Backlog Sourcing

Pull staging-only ACs from:
1. `claude/backlog/backlog.md` — items tagged with `staging-only`, `deferred-staging`, or similar markers
2. QA evidence files (`qa_evidence_EPIC-xx.md`) from recent cycles — search for disposition entries marked "staging verification pending"
3. Sprint close records (`sprint_close.md`) — items returned to backlog as staging-deferred

---

## 4. Evidence Format

### 4.1 Verification Log Structure

For each staged verification story, create or update a verification log in `docs/operations/` or append to the relevant `qa_evidence_EPIC-xx.md`:

```
## Staged Verification: [BLG-OPS-xx] — <AC title>
**Source:** <release cycle>/<EPIC>/<ST>
**Verified by:** Infrastructure & Operations Owner
**Verification date:** YYYY-MM-DD
**Environment:** staging | production
**Verification method:** <describe how the AC was checked>
**Result:** Pass | Fail | Partial
**Findings:** <list observations; "None" if pass>
**Follow-up:** <backlog item if fail, or "None">
```

### 4.2 DoQ Sign-Off Requirements

The Director of Quality must sign off on each staged verification story before it is counted as `done`. The sign-off covers:

- Confirmation that the verification log is complete and findings are recorded
- Assessment that any failures have been dispositioned (P0/P1: block release; P2/P3: new backlog item)
- Acceptance that deferred ACs are now cleared (or formally escalated if blocked)

Sign-off block in `qa_evidence_EPIC-xx.md`:

```
- Signed off by: Director of Quality
- Date: YYYY-MM-DD
- Comments: Staged verification complete. [N] ACs verified. [N] failures dispositioned. 
  Cleared ACs: [list]. Remaining: [list or "None"].
```

PMO Lead counter-sign is required when the sprint close record documents the staging verification sprint as a governance event.

### 4.3 Failure Disposition Table

| Failure severity | Required action |
|-----------------|-----------------|
| P0 (data loss, security) | Immediate escalation — block next release; hotfix required |
| P1 (core feature mismatch) | File backlog item; flag to Product Owner; accept risk explicitly or hotfix |
| P2 (partial/incomplete) | File backlog item for next sprint; document workaround if applicable |
| P3 (cosmetic/edge case) | File backlog item; no block on release |

---

## 5. Sprint Sizing Note

Staged verification work follows a different sizing model than feature development:

| Effort pattern | Guidance |
|---------------|----------|
| Environment access overhead | Add 0.5 day per sprint for environment coordination (credential refresh, seed data confirmation) |
| Per-AC verification | Budget 1–4 hours per staging AC depending on complexity |
| Simple field/value spot check | XS (~1 hour) |
| End-to-end flow verification | S (~0.5 day) |
| Multi-component integration test | M (~1 day) |
| Documentation and sign-off | Add 0.5–1 day per story for evidence documentation |

**Typical staged verifications sprint:** 3–6 verification stories, total effort 2–5 days, well within standard sprint capacity.

**Capacity buffer rule:** Reserve at least 30% of sprint capacity for opportunistic governance or debt clearance work (e.g., governance patches, documentation debt). Staged verification sprints should not consume 100% of capacity.

---

## 6. Sign-Off

- **Director of Quality:** Director of Quality — 2026-06-21  
  Sign-off: Protocol covers trigger conditions, batching approach, evidence format, and sprint sizing. Evidence format (§4) consistent with existing QA evidence standards. Failure disposition table (§4.3) aligned with OPERATIONAL_GUIDE.md §7 severity policy.

- **PMO Lead:** PMO Lead — 2026-06-21  
  Sign-off: Trigger conditions (§2) and sizing note (§5) reflect actual observed patterns from v4.7 and v5.0 staged verification sprints. Protocol is governance-compliant and ready for use.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-21 | Initial version. ST-06 (BLG-GOV-89, v5.1 EPIC-03). Pattern validated at v4.7 (first use) and v5.0 (confirmed). |
