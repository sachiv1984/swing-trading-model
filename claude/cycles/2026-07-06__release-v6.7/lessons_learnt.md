**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-06__release-v6.7
**Release:** v6.7
**Last Updated:** 2026-07-06

---

# Lessons Learnt — Release Planning v6.7

## What worked well

1. **The mandatory Skill-Silo pull-forward clause (`roadmap_prompt.md` §7.1 v8.3) resolved cleanly on its first binding invocation.** The rebalance had already named `BLG-FE-87`/`BLG-FE-88` as candidates and confirmed both were ungated and build-and-ship-shaped; release planning only had to confirm and include them, with no gate mismatch to catch this time (unlike v6.6's `BLG-FEAT-52` finding).
2. **Bundling the full Lifecycle Audit AUD-2026-07-06 improvement backlog (`BLG-GOV-167`–`170`) as a single EPIC worked well** — all 4 items share a source, an owner (Head of Specs Team), and no cross-dependency, making a clean second EPIC alongside the frontend contrast work.
3. **`BLG-GOV-167`'s inclusion directly resolves LP-07 (v6.6 carry-forward)** — the `/commit-check` write-scope escalation is now addressed via a governed scope item rather than remaining an unowned 4th-cycle carry.

---

## Friction Log

### Friction Item 1

**Classification:** Type C — Dependency Stall (data-access constraint)

**Recurrence:** 2nd occurrence — first surfaced at `2026-07-06__scheduled` rebalance, same session-type gap (no application `X-API-Key` available).

**What happened:** This session attempted the production trade-count re-verification flagged by the rebalance as a priority action for the next data-access-capable engine invocation (per `~/.api_keys` and the memory record). `~/.api_keys` still contains only `RENDER_API_KEY` (platform management), no application-level key; a direct request to the production backend returned HTTP 401. The SI-02 gate's trade-count condition remains unresolved (15 formally confirmed vs. 20 self-reported) for a 2nd consecutive governed-routine invocation.

**Where in the routine:** STEP 1 (Readiness) / STEP 1.4 (Gate-Condition Proximity Scan).

**Root cause:** No governed routine currently has access to an application-level API key — `~/.api_keys` has only ever contained `RENDER_API_KEY`. This is an environment/credential provisioning gap, not a routine logic gap.

**Suggested fix:** PMO Lead or Infrastructure & Operations Owner to provision an application `X-API-Key` into `~/.api_keys` (or an equivalent secrets location readable by governed routines) so future release/roadmap/sprint planning invocations can resolve data-density gate conditions directly instead of carrying the same unresolved prose forward indefinitely.

**Target:** PMO Lead / Infrastructure & Operations Owner, before next SI-02 gate check is attempted.

---

### Friction Item 2

**Classification:** Type B — Write-Scope Boundary (correctly identified, not applied)

**Recurrence:** First identified this cycle.

**What happened:** The `2026-07-06__scheduled` rebalance's carry-forward named this cycle (`plan release v6.7`) as the target for applying a structured `**Last formally confirmed:**` / `**Unverified report:**` field patch to `current_roadmap.md`'s SI-02 row and `roadmap_prompt.md` STEP 2.3. On review, this patch requires editing `roadmap_prompt.md` — a reserved governance file explicitly outside `release_planning_prompt.md`'s write scope (§7) — and a `current_roadmap.md` change beyond the execution-notes-only annotation permitted at STEP 5. The engine correctly declined to make an out-of-scope edit rather than silently exceeding its declared write boundary.

**Where in the routine:** §7 Write Scope Restriction (implicit check during Readiness).

**Root cause:** The rebalance's carry-forward named the wrong engine as the target — the patch's own file list (`roadmap_prompt.md`) makes clear it belongs to a `run roadmap` invocation (or direct Head of Specs Team authority, same pattern as `BLG-GOV-167`), not `plan release`.

**Suggested fix:** When a rebalance carry-forward item names a target engine for a deferred patch, cross-check that the patch's own file list falls within that engine's declared write scope before naming it as the target — otherwise the patch will bounce to a second engine that also cannot apply it, costing a cycle.

**Target:** Head of Specs Team, next `roadmap_prompt.md`/`shared_standards.md` revision (or apply directly, same authority pattern as `BLG-GOV-167`, at the next `run roadmap` invocation).

---

## Monitoring Carried Forward

- **RISK-01/RISK-02 (EPIC-01 contrast remediation scale):** Largest contrast remediation attempted to date (~1,026 instances, ~190 files). Sprint execution and delivery verification should confirm the Playwright/staging evidence is genuinely representative, not sampled thin given the scale.
- **RISK-03 (BLG-GOV-167 write-scope precedent):** First time a backlog item grants standing write authority outside a routine's declared scope. Next lifecycle audit should confirm this precedent was not extended beyond `.claude/skills/` in practice.
- **Friction Item 1 (SI-02 credential gap):** Now a 2-cycle-old unresolved data-access constraint. If unresolved by the next SI-02 gate check, escalate per `lessons_learnt_prompt.md` §3.7 recurrence rules.

---

## Action Items (to be completed at Post-Ship Closure)

| ID | Source | Summary | Classification | Owner | Target |
|----|--------|---------|----------------|-------|--------|
| LP-08 | Release Planning | Provision an application `X-API-Key` for governed routines to resolve data-density gates directly | environment-gap | PMO Lead / Infrastructure & Operations Owner | Before next SI-02 gate check |
| LP-09 | Release Planning | SI-02 structured-field patch misrouted to `plan release` by rebalance carry-forward — correct target is `run roadmap` / direct Head of Specs Team authority | prompt-gap | Head of Specs Team | Next `run roadmap` invocation |
| LP-10 | Release Planning | Confirm BLG-GOV-167's write-scope grant was not extended beyond `.claude/skills/` in practice | monitoring | Head of Specs Team | Next lifecycle audit |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle": "2026-07-06__release-v6.7",
  "release": "v6.7",
  "status": "seeded",
  "completed_at": ""
}
