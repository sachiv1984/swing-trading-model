Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-24
Cycle: 2026-07-21__release-v7.7

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v7.7 Strategy Intelligence Surfacing & Notification UX
Run: 2026-07-21__release-v7.7
Reviewed by: PMO Lead
Date filed: 2026-07-24
Prior cycle checked: 2026-07-20__release-v7.6 (`lessons_learnt_closure.md`)

---

## What worked well

- Backlog reconciliation (STEP 3) and scope/decisions supersession (STEP 4) both located every target artefact on the first lookup — no missing documents this cycle; `scope--2026-07-21__release-v7.7-strategy-intelligence-notification-ux.md`'s 11 in-scope items matched `execution_state.json`'s 11 completed stories exactly.
- STEP 6 endpoint coverage drift check found the gap already fully tracked by an existing open rolling item (`BLG-OPS-111`, filed at v7.2), avoiding a duplicate filing — including EPIC-01's new `GET /analytics/strategy-version-comparison` endpoint, which was already anticipated in that item's own gap list.
- Zero deviations filed this sprint (confirmed in `sprint_close.md` and `verification_report.md §4`) meant STEP 5's canonical spec deviation compliance check was a clean pass-through with no field-completeness corrections required.
- All 11 QA evidence logs and the verification report's sign-off block were complete and non-blank on first read — no Tier 1/Tier 2 signer issues carried into closure.

---

## Friction Log

### Friction Item 1

**Classification:** Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced

**Recurrence:** Yes — appeared in `2026-07-20__release-v7.6` closure (Recurrence Escalation: cross-EPIC merge-conflict pattern; Outstanding Deferred Patches: 3 items targeting "next roadmap review"; Carry-Forward item 2: empty-Now-horizon scope-selection reopen)

**What happened:** `current_roadmap.md`'s v7.7 section was formalized via the same direct-write/PO-bypass pattern used at v7.4 (AMD), v7.5, and v7.6 (DL-073) — this is the 4th consecutive cycle a compliant `run roadmap --reason "scheduled"` path existed and was bypassed by explicit PO/session direction (per the roadmap's own header, DL-074). This is also the **second** exercise of the scope-selection sub-case specifically (choosing new anchor items from an empty Now horizon, not just relabelling a carry-forward set) — the exact trigger condition v7.6's own `lessons_learnt_closure.md` Carry-Forward item 2 flagged for Head of Specs Team review. As a direct consequence, the 3 deferred patches filed at v7.5's closure and re-carried at v7.6's closure — `delivery_verification_changelog.md` historical backfill, an `Array.isArray()` coding-standard lint rule, and `SystemStatus.js` `categorizeEndpoint()`'s two missing `includes()` branches — all target "next roadmap review", which still has not arrived (no `run roadmap` invocation since `2026-07-17__scheduled`; `last_manage_roadmap_utc` only reflects STEP 11 subroutine runs within post-ship closures, not a scheduled rebalance).

**Where in the routine:** STEP 8 — Lessons Learnt Review and Application, cross-referencing the prior cycle's Outstanding Deferred Patches table against `.claude_current_state.json.last_rebalance_cycle` / `last_manage_roadmap_utc`.

**Root cause:** authority ambiguity — no governed engine currently accepts a "PO wants to formalize/reopen scope now, without a full rebalance" request (already recorded as v7.6's own Carry-Forward item 1); this absence is what forces the bypass pattern each time, which in turn stalls every deferred patch gated on "next roadmap review" ever actually running.

**Blast radius analysis:**
- What would have propagated: the 3 already-deferred patches continue accumulating indefinitely as long as `run roadmap` keeps being bypassed for scope-naming purposes.
- When it would have surfaced: next `run roadmap` invocation (whenever it actually occurs) — or a future audit cross-referencing deferred-patch age.
- Recovery cost if uncaught: low-medium (each individual patch is small) but compounding governance-trust erosion the longer resolution is deferred without a structural fix.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/roadmap_prompt.md` (or a new bounded "scope reopen" engine)
  - Section: New section required — a governed, bounded "reopen with zero downstream consumption" path for PO-directed scope naming outside a full rebalance
  - Change required: Add an explicit lightweight path so the next occurrence of this pattern (near-certain, given 4 consecutive cycles) does not require an ungoverned PO bypass
  - Owner: Head of Specs Team
  - Target: next `run roadmap` invocation

---

### Friction Item 2

**Classification:** Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** Not checkable via the standard §3.7 prior-cycle check (this is a multi-cycle historical gap discovered by direct inspection, not a single prior-cycle friction item)

**What happened:** `docs/specs/Specs_Index.md`'s `Last Updated` header had not been touched since `2026-07-14` (v7.1's post-ship closure) despite five subsequent Post-Ship Closure runs (v7.2 through v7.6) completing in between. STEP 7 requires appending a "Test Coverage Gaps — v<X.Y>" section each cycle (per the established §9–§36 series) and updating `Last Updated` "if any changes were made" — the TSG section series stopped at §36 (v6.8) and never resumed for v6.9 through v7.6, even though each of those cycles' own `verification_report.md §6` contained TSG rows that should have been transcribed. Also discovered: the section CLAUDE.md/AUD-2026-06-22-005 reference as "§27 (Technical Specification Gaps)" for the STEP 7.3 reconciliation rule is now actually "§27. Test Coverage Gaps — v5.0" — the numbered-section reference has drifted as new sections were appended, making the rule's own citation stale.

**Where in the routine:** STEP 7 — Specs Index Review, while performing the STEP 7.3 TSG backlog reconciliation.

**Root cause:** process gap / document staleness — five consecutive Post-Ship Closure runs appear to have treated "no §6/§7 items to resolve" as "nothing to do" for STEP 7 and skipped both the TSG section append and the `Last Updated` bump, even on cycles with populated TSG rows in their own verification report.

**Blast radius analysis:**
- What would have propagated: `Specs_Index.md` silently understated as a source of truth for 6 cycles' worth of test-coverage-gap history; a future audit or `run roadmap` STEP 0 gap-check reading this file would not see v6.9–v7.6 TSG data at all.
- When it would have surfaced: next `run audit` (Coverage Inventory refresh) or a future roadmap STEP 0 gap-check.
- Recovery cost if uncaught: medium if left much longer (reconstructing 6 cycles of historical TSG data from old `verification_report.md` files becomes progressively harder to justify as genuinely load-bearing vs. speculative backfill).

**Process patch:**

→ Immediate patch applied this run:
  - File: `docs/specs/Specs_Index.md`
  - Section: New §37 "Test Coverage Gaps — v7.7"; document header `Last Updated`
  - Change: Added this cycle's 5-row TSG register (all `not_applicable`, transcribed from `verification_report.md §6`) and bumped `Last Updated` to `2026-07-24`. Historical backfill for v6.9–v7.6 was **not** attempted — reconstructing 6 cycles retroactively is out of this routine's write scope (no scope revision of already-closed cycles) and was judged not clearly load-bearing enough to justify the effort/risk of introducing fabricated-looking historical entries.
  - Version: n/a (`Specs_Index.md` is not a versioned Class 6 governance prompt)
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Not applicable (not a Class 6 governance prompt)

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| `claude/system/changelogs/delivery_verification_changelog.md` — backfill missing 2.4–3.4 historical version rows | `2026-07-17__release-v7.5` closure | Owner: Head of Specs Team; Target: next roadmap review (still not arrived after 2 further cycles) | Head of Specs Team |
| Coding standard / lint rule — require `Array.isArray(...)` guards on `.map()`/`.filter()` over JSON API response fields | `2026-07-17__release-v7.5` closure | Owner: Head of Engineering; Target: next roadmap review (still not arrived after 2 further cycles) | Head of Specs Team |
| `src/pages/SystemStatus.js` `categorizeEndpoint()` — add `/price-alerts` and `/saved-filters` `includes()` branches | `2026-07-17__release-v7.5` closure | Owner: Frontend engineer; Target: before next System Status review (still not arrived after 2 further cycles; both endpoints degrade gracefully to `'Other'`, not urgent) | Head of Specs Team |

Per `lessons_learnt_prompt.md` §3.7: each of these three items has now carried across 3 consecutive Post-Ship Closure runs (v7.5 → v7.6 → v7.7) without resolution, gated on a "next roadmap review" target that has not occurred (no `run roadmap` invocation since `2026-07-17__scheduled`; v7.6 and v7.7 both used direct-write bypass patterns instead — see Friction Item 1 above, same root cause). Recorded as recurrence escalations rather than re-deferred a further cycle.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `docs/specs/Specs_Index.md` | §37 (new); document header | Added v7.7 Test Coverage Gaps section (5 rows, all `not_applicable`); bumped `Last Updated` | n/a (not a governance prompt) | Not applicable |

---

## New files created this run

None (`closure_state.json`, `closure_record.md`, and this file are standard STEP 0/STEP 9/STEP 8.5 outputs, not "improvement" artefacts).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | STEP 2 (Branch Preflight) or STEP 4 | Add an explicit "post-first-merge rebase" step resolving the `execution_state.json` cross-EPIC `add/add` conflict class proactively per-branch, rather than leaving it to be caught in a scramble at merge-gate time (Phase 3 friction, `lessons_learnt_cycle.md` `## Phase 3`) | Head of Specs Team | next run of this routine (Sprint Execution) |
| `claude/system/execution_prompt.md` | STEP 3.1.A | Flag any story hardcoding a value also derivable via a script (e.g. the EPIC-11 AST endpoint-count scan) and require re-deriving — not assuming — that value at rebase time when a sibling EPIC branch may have independently changed the same constant (Phase 3 friction, `lessons_learnt_cycle.md` `## Phase 3`) | Head of Engineering | next run of this routine (Sprint Execution) |
| `claude/system/roadmap_prompt.md` (or new bounded engine) | New section required | Governed, bounded "reopen with zero downstream consumption" path for PO-directed scope naming outside a full rebalance (Friction Item 1 above) | Head of Specs Team | next `run roadmap` invocation |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| Should agent-mediated "acting as Product Owner" PR comments be disallowed entirely (reserving that authority strictly for genuine human comments), or is the current explicit self-disclaiming disclosure sufficient safeguard? A prior session's proxy comments on 10 open PRs were visually similar enough to genuine human PO acceptance that this session had to carefully distinguish them before evaluating the merge gate (Phase 3 friction, `lessons_learnt_cycle.md` `## Phase 3`, classification: decision). | Authority ambiguity | Head of Specs Team (owns §5.3's always-human-gate definition) | Needs a ruling from the role that owns the always-human-gate boundary definition; 72-hour deadline: 2026-07-27. |

Recurrence escalations are recorded separately above (3 items).

---

## Carry-Forward
Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The empty-Now-horizon direct-write scope-selection pattern (choosing new anchor items, not just relabelling a carry-forward set) has now been exercised twice (v7.6, v7.7) with no distinct governance track from a pure relabel — the exact "second time" condition v7.6's own closure flagged for review. | Head of Specs Team should decide whether an empty-Now-horizon scope-selection reopen needs its own confirmation step before a third occurrence. | Roadmap |
| 2 | Four consecutive cycles (v7.4 AMD, v7.5, v7.6 DL-073, v7.7 DL-074) have bypassed a compliant `run roadmap --reason "scheduled"` path for routine, non-emergency scope-naming — and this is the structural blocker keeping 3 deferred patches from ever resolving (see Recurrence Escalations). | Release Planning / Roadmap engine should evaluate a bounded governed path for this recurring request class before a 5th bypass occurs. | Release Planning |
| 3 | `Specs_Index.md`'s STEP 7 maintenance (TSG section append + `Last Updated` bump) silently lapsed for 5 consecutive Post-Ship Closure cycles (v6.9–v7.6) before being caught this run. | Post-Ship Closure's own STEP 7 should make the "append a TSG section every cycle, even with zero gaps" expectation unambiguous rather than implicitly skippable when there is nothing to resolve in §6/§7. | All |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-07-21__release-v7.7",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-07-24T11:45:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 3,
  "escalation_count": 4,
  "carry_forward_count": 3,
  "status": "Complete"
}
```
