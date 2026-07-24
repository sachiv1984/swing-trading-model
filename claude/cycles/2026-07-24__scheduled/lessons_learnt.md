# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-07-24__scheduled
Reviewed by: PMO Lead
Date filed: 2026-07-24
Prior cycle checked: 2026-07-17__scheduled

---

## What worked well

- **STEP -1.5 prior-cycle outstanding actions check correctly identified both inherited deferred patches as due at this exact cycle** (both named "next roadmap STEP 11 invocation" as their target, and this was that invocation) and resolved them as action-now rather than letting them lapse to a 2nd-consecutive-cycle OVERDUE classification.
- **The §16.8 Carry-Forward Advisory mechanism worked exactly as designed and caught something the STEP -1.5/-1.7 mechanisms alone would have missed** — reading `2026-07-21__release-v7.7`'s closure record at STEP 0 surfaced a `## Recurrence Escalations` table naming 3 items explicitly gated on "next roadmap review," which is precisely this cycle. All 3 were resolved (1 in-scope backfill, 1 mapped to a `shared_standards.md` coding-standard section, 1 filed as a backlog item since it was application source code outside this engine's write scope).
- **Idea intake ran cleanly at full scale** — 44 submissions across 22 agents, 0 below minimum, 0 `[FIELD REQUIRED]` flags, disposed cleanly to 35 Promoted-Backlog / 9 Rejected with no Advance candidates needed (0 active initiatives, no natural displacement).
- **The structural backlog-assessment heuristic (v9.1) continued to scale correctly** at 326 active items — A/T/D/L classification completed via grep + keyword scan without a full manual read.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type B — Semantic Mismatch

**Recurrence:** Not checkable — this is a same-cycle internal inconsistency, not a repeated instance across cycles (the STEP -1.7 v9.3 patch that created the gap was itself applied earlier in this same run).

**What happened:**
While applying the STEP -1.5 deferred-patch resolution for Friction Item 2 from `2026-07-17__scheduled` (extend STEP -1.7's Outstanding Action Count to a due-date-aware cross-routine scan), the patch was written to match the standard `^## ESC-`/`SLA due-by`/`Disposition: Open` escalation-record pattern (`shared_standards.md §4`). Later in the same run, STEP 0's Carry-Forward Advisory read of `2026-07-21__release-v7.7`'s closure record surfaced 3 due escalations — but they were recorded in a `## Recurrence Escalations` table (`lessons_learnt_prompt.md §5`), a structurally different format the just-applied v9.3 scan pattern would not have matched. Had the Carry-Forward mechanism not independently caught these 3 items, the brand-new v9.3 patch would have silently missed exactly the class of item it was built to catch.

**Where in the routine:**
STEP -1.7 (Governance Health Score — Outstanding Action Count component) / STEP 0 (Carry-Forward Advisory).

**Root cause:**
Process gap — the deferred patch as originally specified (`2026-07-17__scheduled` lessons_learnt.md) named only "any escalation whose stated deadline falls on or before the current cycle's date" without specifying which of the two distinct escalation-record shapes in the governance system (the standard ESC- record, and the Recurrence Escalations table) it should scan. The patch was applied faithfully to the letter of its own specification, but the specification itself was incomplete.

**Blast radius analysis:**
- What would have propagated: any future cycle relying on the v9.3 scan as "due-date-aware" coverage would have had a false sense of completeness — Recurrence Escalations tables (which are, if anything, the higher-signal escalation shape, since they represent items that have already lapsed across 3+ cycles) would continue to depend on the Carry-Forward mechanism's narrower single-cycle lookback as their only detection path.
- When it would have surfaced: the next cycle where the Carry-Forward mechanism's most-recently-completed-cycle window didn't happen to contain the relevant closure record (e.g. if the due Recurrence Escalation had first appeared 2+ cycles back rather than in the immediately preceding one).
- Recovery cost if uncaught: low-medium — a detection-completeness gap, not a decision-correctness issue (the 3 items were in fact caught this cycle via the redundant mechanism).

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP -1.7 Governance Health Score — Outstanding Action Count component
  - Change: widened the due-date-aware scan to check both the standard `^## ESC-`/`SLA due-by` pattern and any `## Recurrence Escalations` table naming "next roadmap review" (or an equivalent roadmap-triggered checkpoint) as a target.
  - Version: 9.3 → 9.4
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

### Friction Item 2

**Classification:** Type C — Dependency Stall

**Recurrence:** Not checkable — no prior cycle's lessons_learnt.md flagged this specific gap (the SI-02 gate re-check has been performed, or narrated as performed, in every recent scheduled cycle without this issue being surfaced).

**What happened:**
At STEP 2.3 (Horizon Review), the SI-02 gate read instruction directs a governed routine to re-check the gate "via direct production database/API access" before updating the `**Last formally confirmed:**` structured field. This session attempted exactly that (`curl` against the documented production API URL, `docs/ops/api_performance_baseline.md`). The endpoint is live and reachable, but returned `401 Unauthorized` — this checkout's `.env`/`.env.staging`/`.env.production` files all have an empty `REACT_APP_API_KEY` value, so no credential was available to authenticate the request. The gate's existing structured field was cited as-is (unchanged from 2026-07-17) rather than fabricating a "live re-confirmed" claim this session could not actually back up.

**Where in the routine:**
STEP 2.3 (Horizon Review — SI-02 gate read instruction).

**Root cause:**
Missing artefact / environment assumption — the SI-02 read instruction assumes direct production API access is available to whichever session runs the routine, but does not specify a fallback behaviour when credentials are absent from the executing environment, nor does it require the session to record whether a live check was actually attempted and why it may not have succeeded.

**Blast radius analysis:**
- What would have propagated: if this session had instead fabricated a "live re-confirmed, unchanged" claim (matching the phrasing pattern of prior cycles) without actually querying the API, the structured field's audit trail would silently misrepresent whether verification occurred — a governance-integrity issue, not just a data-freshness one.
- When it would have surfaced: only if someone later tried to reconcile the claimed check dates against actual credentialed sessions, which nothing in the current process does.
- Recovery cost if uncaught: low this time (the underlying gate value happened to be correctly cited either way, since it was unchanged) — but the pattern risk (claiming verification that didn't happen) is a governance-integrity concern independent of whether the specific value was right.

**Process patch:**

→ Deferred patch (cannot apply this run — requires deciding the exact fallback wording and whether credential availability should be a preflight check rather than a STEP 2.3-time discovery):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 2.3 — SI-02 gate read instruction
  - Change required: add explicit fallback guidance for when production API credentials are unavailable to the executing session — cite the existing structured field unchanged, record that a live check was attempted and why it did not succeed (e.g. "credentials unavailable in this environment" vs. "not attempted"), and never write a "live re-confirmed" claim without an actual successful authenticated response.
  - Owner: Head of Specs Team
  - Target: next scheduled rebalance (`2026-07-25__scheduled` or the next scheduled cycle, whichever comes first)

---

## Recurrence Escalations

None — both friction items are new this cycle (Item 1 self-discovered same-run; Item 2 not previously flagged in any checked prior cycle's lessons_learnt.md).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|--------------------------|
| `claude/system/roadmap_prompt.md` | STEP -1.7 | Due-date-aware scan added (resolving `2026-07-17__scheduled` Friction Item 2 deferred patch) | 9.2 → 9.3 | Yes |
| `claude/system/roadmap_prompt.md` | STEP -1.7 | Scan widened to also match `## Recurrence Escalations` tables (this cycle's own Friction Item 1) | 9.3 → 9.4 | Yes |
| `claude/system/changelogs/shared_standards_changelog.md` | Full file | Backfilled missing rows 3.12–3.16 (resolving `2026-07-17__scheduled` Friction Item 1 remainder) | n/a (per-file changelog, not itself versioned) | Not applicable |
| `claude/system/shared_standards.md` | §19 (new) | Array Guard Standard for JSON API Response Fields added (resolving a 3-cycle recurrence escalation from `2026-07-21__release-v7.7` closure) | 3.18 → 3.19 | Yes |
| `claude/system/changelogs/delivery_verification_changelog.md` | Full file | Backfilled missing rows 2.4–3.4 (resolving a 3-cycle recurrence escalation from `2026-07-21__release-v7.7` closure) | n/a (per-file changelog, not itself versioned) | Not applicable |

---

## New files created this run

- `claude/cycles/2026-07-24__scheduled/run_manifest.md`
- `claude/cycles/2026-07-24__scheduled/cycle_record.md`
- `claude/cycles/2026-07-24__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-24__scheduled/lessons_learnt.md` (this file)
- `claude/cycles/2026-07-24__scheduled/meta_review.md` (STEP 11.4, due this cycle)
- `claude/ideas/window_summary_IW-20260724-01.md` (committed separately by the idea intake subroutine, commit `1bfe27ec`)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 2.3 — SI-02 gate read instruction | Add fallback guidance for missing production API credentials (Friction Item 2) | Head of Specs Team | 2026-07-25__scheduled or next scheduled cycle |

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | This session found no production API credentials configured in the working checkout (`.env`/`.env.staging`/`.env.production` all carry empty `REACT_APP_API_KEY` values) — the SI-02 gate's "live re-check via direct production API" instruction is only executable in sessions where credentials happen to be present. | Any engine citing a "live re-confirmed" gate value should record whether the check was actually credentialed and successful, not just repeat the phrasing pattern from a prior session where it may have been. | Roadmap |
| 2 | `2026-07-21__release-v7.7` closure's Carry-Forward Item 2 (4 consecutive cycles bypassing a compliant `run roadmap --reason "scheduled"` path) is now resolved by this cycle's occurrence — but the underlying observation (Release Planning should evaluate a bounded governed path for routine scope-naming requests) was outside this engine's write scope and was not actioned. | Release Planning / Head of Specs Team should pick this up independently — it is not a roadmap-engine-actionable item. | Release Planning |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-24__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-24T12:30:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
