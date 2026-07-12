**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Filed
**Report Date:** 2026-07-12

---

# Lessons Learnt — Roadmap Rebalance 2026-07-12__scheduled

Feature / Trigger: N/A — scheduled review
Run: 2026-07-12__scheduled
Reviewed by: PMO Lead
Date filed: 2026-07-12
Prior cycle checked: 2026-07-10__scheduled

---

## What worked well

- The SI-02 gate re-check moved from citing a 6-day-stale structured field to a genuine live re-verification via direct production API access (`GET /trades`, `GET /trade-plans`, `GET /analytics/behavioural-drift`), correctly distinguishing "condition (1) still fails, but now for a data-timing reason rather than the original `BLG-BE-46` bug" — this is exactly the distinction STEP 2.3's structured field exists to preserve.
- The LP-05 candidate gate-verification check caught a real near-miss: `BLG-FEAT-73` (SI-02 frontend, P1, highest-priority nominal Skill-Silo pull-forward candidate) would have been named as a candidate had its gate only been checked via the literal `**Gate criteria:**` field (absent on this item — the gate is embedded in its Acceptance Criteria instead). Reading the full item body instead of grepping one field pattern caught this before it could repeat the exact `2026-07-03__scheduled`/`BLG-FEAT-52` failure mode LP-05 was built to prevent.
- Two OVERDUE deferred patches were actually resolved this cycle rather than carried a further time — one confirmed already-applied via evidence (the tag convention), one applied directly under newly-granted standing authority (`CLAUDE.md` §6) rather than continuing to cite "outside write scope" as a reason to defer again.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** No (first occurrence of this specific gap; the same-day collision itself was a first-time event, not a repeat of a previously-identified friction)

**What happened:**
This engine's `cycle_id` convention (`YYYY-MM-DD__scheduled`) has no provision for a second scheduled invocation on the same calendar date. Partway into preflight, it was discovered that a scheduled rebalance had already run and been `Filed` earlier the same session (`2026-07-10__scheduled`, 16:00 UTC) — writing this run's artefacts into the same path would have silently overwritten a completed Class 3 record. There was no rule in `roadmap_prompt.md` STEP 0/6 covering this case; it required a user-confirmed ad hoc resolution (suffixed `cycle_id`) mid-run. A related complication: the sandbox clock advanced from 2026-07-10 to 2026-07-12 mid-session, which was also flagged to the user before being used to resolve the `cycle_id` question naturally (no suffix needed once the date genuinely differed).

**Where in the routine:**
STEP 0 — Load and Validate Inputs (Cycle ID definition, §6 Completion Event Definition).

**Root cause:**
Template omission — the `cycle_id` naming convention was designed assuming at most one scheduled run per calendar date, an assumption that held until this cycle.

**Blast radius analysis:**
- What would have propagated: a completed, `Filed` Class 3 operational record (`run_manifest.md`, `cycle_record.md`, `cycle_summary.md`, `lessons_learnt.md`, `meta_review.md`) for `2026-07-10__scheduled` would have been silently overwritten, destroying the audit trail for that cycle's decisions (including `DL-063` context).
- When it would have surfaced: likely never as an active alarm — the next reader of `2026-07-10__scheduled`'s artefacts would simply find this cycle's content instead, with no error raised.
- Recovery cost if uncaught: high — a completed governance record with its own decision-log entry and downstream references (`plan release v6.9` cited it at STEP -1.2) would be unrecoverable from the working tree (git history would still have it, but nothing in-repo would signal the loss).

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: §6 Completion Event Definition
  - Change: added a same-day collision check — before creating `claude/cycles/<cycle_id>/`, detect an existing folder for today's computed `cycle_id` and auto-suffix (`-2`, `-3`, …) rather than requiring ad hoc user escalation.
  - Version: 8.6 → 8.7
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

### Friction Item 2

**Classification:** Type A — Governance Drift

**Recurrence:** No (the underlying carried patch was known and tracked across prior cycles, but this specific observation — that STEP -1.5's own OVERDUE rule was never actually enforced against it despite the letter of the rule requiring escalation — was not flagged as a friction item in any prior cycle's lessons learnt)

**What happened:**
The `CLAUDE.md` §6 step 1 deferred patch was carried across 6 consecutive scheduled-rebalance cycles (2026-07-01 through 2026-07-10 first run). STEP -1.5's own rule states: "Absent and second consecutive cycle carrying this patch → classify OVERDUE; escalate to Head of Specs Team immediately. Run may not proceed past -1.5 with any OVERDUE patch." By the letter of this rule, the patch should have triggered an OVERDUE halt at the 2nd carry (around `2026-07-02__scheduled`) — it never did; every cycle simply re-recorded it as "carried forward, outside this engine's write scope." Today, `shared_standards.md` §17 was extended (via audit `AUD-2026-07-10-001`) to grant Head of Specs Team standing write authority over `CLAUDE.md` independent of any engine's per-run scope — but this session still had to notice the gap and act on it explicitly rather than the routine surfacing it as newly-actionable.

**Where in the routine:**
STEP -1.5 — Prior Cycle Outstanding Actions (Prompt patch confirmation sub-section).

**Root cause:**
Process gap — the OVERDUE rule's escalation language assumed the escalation itself would prompt resolution, but provided no explicit instruction for the case where the blocker (write scope) has since been removed by a separate governance change. Six cycles of "correctly identify as OVERDUE, then re-carry anyway because it's out of scope" is exactly the loop this exposes.

**Blast radius analysis:**
- What would have propagated: an indefinitely-recurring OVERDUE patch that gets correctly labelled every cycle but never resolved, silently normalising "OVERDUE" as a steady-state rather than a hard-gate trigger — eroding the practical meaning of the OVERDUE classification itself.
- When it would have surfaced: never as a hard failure (no downstream gate reads this classification), only as an accumulating governance-debt smell across `run_manifest.md` files.
- Recovery cost if uncaught: low-medium — the patch itself was small and low-risk, but the pattern (OVERDUE flagged, never enforced) generalises to any future out-of-scope patch, which is a more serious integrity risk.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP -1.5 Prior Cycle Outstanding Actions
  - Change: added an "out-of-scope OVERDUE resolution" clause — once a named authority holds a standing out-of-band write privilege for an OVERDUE patch's target file, "outside this engine's write scope" is no longer a valid reason to re-carry; the escalation must instruct direct application under that authority.
  - Version: 8.6 → 8.7 (same version bump as Friction Item 1 — both applied in one pass)
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

## Recurrence Escalations

None this cycle — both friction items above are newly-identified observations, not recurrences of previously-flagged-and-unresolved friction.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|--------------------------|
| `claude/system/roadmap_prompt.md` | §6 Completion Event Definition | Same-day `cycle_id` collision auto-suffix rule | 8.6→8.7 | Yes |
| `claude/system/roadmap_prompt.md` | STEP -1.5 | Out-of-scope OVERDUE resolution clause | 8.6→8.7 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §6/§13/§14 + Change Log | Version-reference sync for the above 2 patches; also corrected a pre-existing §13/§14 drift found this cycle (§13 row read v8.5 while §14 already read v8.6) | 4.91→4.92 | Yes |
| `CLAUDE.md` | §6 Governance File Edit Checklist, step 1 | Applied directly this session (outside this routine's own write scope, under Head of Specs Team's standing §17 authority) — require reading the file's own Change Log/state before bumping a version, mirroring `shared_standards.md` §9.1 | N/A (no version field) | N/A — not a Class 6 prompt in `prompt_change_log.md`'s scope list; recorded here and in `run_manifest.md` instead |

---

## New files created this run

- `claude/cycles/2026-07-12__scheduled/run_manifest.md`
- `claude/cycles/2026-07-12__scheduled/cycle_record.md`
- `claude/cycles/2026-07-12__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-12__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260712-01.md` (committed separately as part of the idea intake window close)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|------------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 0.C (Run Tier Determination) | Abbreviated-manifest exception for "0 active initiatives + no backlog/register change since prior scheduled run" (carried from `2026-07-08__scheduled`, still not recurred at `2026-07-10__scheduled` or this cycle) | Head of Specs Team | Next scheduled rebalance where the condition genuinely recurs |

---

## Escalations

None raised by this engine this cycle.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The Product Value Ratio has now alerted 3 consecutive times (0.26 → 0.18 → 0.21) — the improvement this cycle is real but the ratio remains well below the 0.30 floor, and the only lever available at 0 active roadmap initiatives is backlog-level pull-forward naming (this cycle: `BLG-FE-102`/`BLG-FE-97`). | The next `plan release` should treat these 2 items as the anchor scope decision, not merely available candidates — consistent with the pattern where rebalance-level naming has become the de facto release scope for 3 consecutive releases now. | Release Planning |
| 2 | `BLG-FEAT-73` (SI-02 frontend, P1) encodes its gate condition entirely in prose within its Acceptance Criteria rather than a `**Gate criteria:**` field — the LP-05 check caught this only because it reads the full item body, not just the structured field. Other backlog items may have the same pattern undetected. | The next `groom backlog` run should spot-check high-priority items lacking a `**Gate criteria:**` field for prose-embedded gates that should be normalised to the structured field (extends the `2026-07-08__scheduled` Gate Field Label Normalization precedent from label-synonym drift to missing-field-entirely drift). | Roadmap |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-12__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-12T21:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 3,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
