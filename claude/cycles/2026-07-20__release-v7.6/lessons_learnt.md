Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-20__release-v7.6
Release: v7.6
Last Updated: 2026-07-20

---

# Lessons Learnt — Release Planning v7.6

## What worked well

1. **STEP -1.2's Empty Now Horizon Gate held correctly and was surfaced to the user rather than silently bypassed.** Unlike the v7.3/v7.5 precedents (which discovered the gap organically mid-routine), this session halted cleanly at preflight, presented the full evidence, and let the user (as Product Owner) make an informed choice between the compliant `run roadmap` path and the direct-write bypass pattern — with the tradeoff stated explicitly, not assumed.
2. **The gate-conditional item BLG-QA-112 (regression baseline update, gated on any of BLG-FE-115–119 entering scope) was caught and its firing surfaced to the user before STEP 4 commit**, rather than being missed and discovered later at delivery verification or post-ship. This is the first release-planning cycle to catch a companion gate fire proactively during scope selection rather than after the fact.
3. **The live SI-02 re-check (STEP 1.4 Arc 4 sub-check) surfaced a genuinely new data point** (8th consecutive unchanged reading, spanning 2026-07-12 through 2026-07-20) despite this release having no Arc 5 scope — keeping the standing advisory current rather than letting it go stale between cycles that don't touch it.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governed-Process Gap (structural, recurrence of a known limitation)

**Recurrence:** Yes — third occurrence of the STEP -1.2 roadmap-formalization gap (v7.3 → DL-068, v7.5 → DL-071, this cycle → DL-072), but the first occurrence where the Now horizon was genuinely **empty** rather than non-empty-but-unversioned.

**What happened:** `roadmap_prompt.md` v9.2's STEP 8.1 condition 1b (added to close `BLG-GOV-240`) only fires on a non-empty-but-unversioned Now horizon — it does not by itself preclude the older, simpler "fully empty Now horizon" case from also needing a `run roadmap` invocation. At this cycle's invocation, the Now horizon was fully empty (RA:v7.5 retired in full, no carry-forward), which is squarely condition 1's *original* target case, so a compliant `run roadmap --reason "scheduled"` path did exist and was recommended. The direct-write bypass chosen instead required a materially larger judgment call than the v7.3/v7.5 precedents: selecting which backlog item to anchor, not just relabelling an existing carried-forward set. This is a bigger authority step than the DL-068/DL-071 precedents established, and DL-072 documents that distinction explicitly rather than treating it as equivalent.

**Where in the routine:** STEP -1.2 (Verify Release Exists on the Roadmap).

**Root cause:** The direct-write bypass pattern (per `shared_standards.md` §17-style standing authority) was established for a narrower case (relabelling) and has now been exercised for a broader case (scope selection) without a distinct governance track for the two. Nothing in the pattern currently distinguishes "formalize a label" from "formalize a label and pick the anchor scope" — both route through the same DL-0xx mechanism.

**Suggested fix:** Consider whether the direct-write bypass pattern should require an explicit, separate confirmation step when the Now horizon is empty at invocation (scope-selection case) versus non-empty-but-unversioned (pure relabel case) — the current session handled this via an extra `AskUserQuestion` round, but that was a judgment call, not a prompted requirement.

**Target:** Advisory — no backlog item filed; the underlying `BLG-GOV-240` gap is closed and this is a usage-pattern observation, not a fresh structural defect. Head of Specs Team to consider at next governance-hardening opportunity if the pattern recurs a second time with an empty horizon.

---

### Friction Item 2

**Classification:** Type A — Governed-Process Gap (structural, first occurrence)

**Recurrence:** No — first time a user has requested scope expansion on an already-Published release plan within the same session, with zero downstream consumption.

**What happened:** After this cycle published (2 EPICs), the user asked to add more scope to push sprint capacity. No governed engine accepted the request: the Amendment Cycle Engine's `--reason` values (`emergency-fix`/`hard-blocker`) explicitly exclude "more capacity is wanted" (`amendment_cycle_prompt.md` §11: "routine scope changes... do not qualify"), and its own lifecycle guard additionally didn't match the current state (`sprint_sealed` was still `true`, stale from v7.5; `status` was `Published`, not `Sprint_Planning_Complete` — v7.6 Sprint Planning had not run). Re-invoking `plan release --version "v7.6"` is unconditionally blocked by Release Planning's RESUME PRECHECK Terminal State Guard on any `Published` cycle, regardless of how recently it published or whether anything downstream has consumed it. Sprint Planning's STEP 3.1 also has no mechanism to pull items beyond the release-planning-confirmed slice. The only way to fulfil the request was a manually-executed, explicitly-flagged PO-directed bypass (DL-073) reopening the Published cycle's own artefacts directly.

**Where in the routine:** Post-STEP 9 (Global State Synchronization) — i.e., entirely outside any governed engine's normal operating window.

**Root cause:** No governed engine's design accounts for the "I just published this and immediately want to change it, before anything downstream has touched it" case. The Amendment Cycle Engine is deliberately narrow (emergency-only) by design; Release Planning's Published-immutability guard is deliberately unconditional (no "grace window" or "nothing has consumed this yet" exception). This is very likely intentional governance design (immutability should not have a timing loophole), but it means routine same-session scope-sizing corrections have no governed path at all — the user must either accept the original scope, wait for the next release cycle, or invoke a PO-authority bypass.

**Suggested fix:** Consider whether `release_planning_prompt.md`'s RESUME PRECHECK Terminal State Guard should distinguish "Published with zero downstream artefacts" (no `design_gate.md`, no `sprint_goal.md`/`sprint_backlog.md` for this cycle) from "Published and consumed" — the former could plausibly permit a bounded, PO-ratified reopen through a governed step rather than requiring an ad hoc bypass every time. Alternatively, extend the Amendment Cycle Engine's `--reason` enum with a narrowly-scoped `scope-expansion` option restricted to cycles with zero downstream consumption, distinct from its emergency-only design intent.

**Target:** Advisory — no backlog item filed this session (the user directed the bypass rather than asking for a prompt change). Head of Specs Team to consider filing a `BLG-GOV` item if this pattern recurs.

## Monitoring Carried Forward

- Design Gate required for ST-01 (EPIC-01, `BLG-FE-119`) — run `run design-gate --cycle 2026-07-20__release-v7.6` before `plan sprint`. ST-02 (EPIC-02, `BLG-QA-112`) has no Design Gate dependency (documentation-only).
- SI-02 gate: 8th consecutive unchanged reading (2026-07-12 through 2026-07-20) — still NOT MET on all three conditions. Not relevant to v7.6 scope; carried forward as a standing cross-cycle watch item, consistent with prior cycles' practice.
- `BLG-QA-112`'s inclusion mid-cycle (after initial scope was set to `BLG-FE-119` only) is the first time a gate-conditional companion item was added to a release's scope after the anchor item was already confirmed by the PO, rather than being part of the original scope proposal. Sprint Planning should confirm both EPIC-01 and EPIC-02 are correctly represented in `sprint_backlog.md`.

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-20__release-v7.6",
  "phase": "Release",
  "filed_utc": "2026-07-20T16:50:00Z",
  "amended_utc": "2026-07-20T17:25:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
