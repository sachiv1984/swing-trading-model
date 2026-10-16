**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-10-16 (Head of Specs Team action-now patch, user-directed, roadmap rebalance `2026-10-16__scheduled` STEP -1.5 — Part B gains "Core wording moved at v9.35 (verbatim)", holding the v9.34 core paragraphs shortened in `roadmap_prompt.md` v9.35); prior — 2026-10-01 (ST-21, EPIC-04, v9.9, BLG-GOV-343 — created as part of splitting `roadmap_prompt.md` into a core + this appendix so the core fits a single read)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Roadmap Rebalance Engine — Appendix

This file has two parts:

- **Part A — STEP 9 onward.** The direct continuation of the mandatory process defined in `claude/system/roadmap_prompt.md` (the core). The core covers Sections 1–8 through STEP 8.5 (preflight through the verified write plan) in one single read; this part covers STEP 9 (Canonical Write) through STEP 12 (Stage, Commit & Global State Update), plus the closing Invariants and Completion Condition sections. Read Part A immediately after completing STEP 8.5 in the core — it is not optional or supplementary, it is the rest of the same routine, split out purely so the core fits a single read (a split already anticipated by the core's own STEP 8.5.E Extended-tier advisory: "a new session executes STEP 9 by reading `cycle_record.md §8.5.B` directly without re-running STEPS 2–8").
- **Part B — Detailed rationale and history.** For decisions in the core (Sections 1–8.5) whose **actionable rule** is stated compactly in the core with a pointer here. Nothing in Part B changes what the core instructs — it holds the full "why" (specific past cycles, confirmed incidents, decisions already made and closed) so the core can state the rule itself without re-deriving its history inline. Read Part B when you need that history, not to execute the routine.

---

# Part A — STEP 9 Onward (Continuation of the Mandatory Process)

### STEP 9 — Canonical Write
Authorities: Head of Specs Team + PMO Lead (process), Product Owner (planning owner)

**Precondition:** Verified write plan exists and passed STEP 8.5. STEP 9 may only modify files in that plan.

#### STEP 9.0 — Net-Zero Displacement Verification (Hard Gate — IMP-13)

Count:
- **Additions:** items classified ✅ Advance in STEP 8 (to be added to roadmap)
- **Confirmed Kills:** items classified ❌ Rejected (permanent stop) — not merely parked or deferred

**Net-zero rule:** additions > kills → halt. Output halt report per `shared_standards.md §5` (gate: Net-Zero Displacement Gap, step: STEP 9.0). Resolution: PO names additional displacements or downgrades advancing items; then re-invoke STEP 8. Mode-independent.

If additions ≤ kills: record net displacement count; proceed.

Update (create-if-missing) with lifecycle-compliant headers:
- `claude/roadmap/current_roadmap.md`
- `claude/roadmap/initiative_register.md` (include displacement candidate flags from STEP 8)
- `claude/roadmap/workforce_capacity.md`
- `claude/roadmap/decision_log.md`
- `claude/backlog/backlog.md` (reconcile to reflect decisions)

Rules:
- No drafts — write as current authoritative planning state.
- No backfilling history.
- Reflect STEP 8 decisions exactly.
- Decision log: append-only per Section 7 invariant.
- When adding a newly promoted item to `backlog.md`: include `**Provisional-Target:**` field derived from horizon placement per `shared_standards.md §16.6`. Write `TBD` if mapping is ambiguous.
- **Effort day-range requirement (§16.12):** if the item's `Provisional-Target` names a specific release (not `TBD`/`Unscheduled`), the `**Effort:**` field must include a day range in parentheses (e.g. `M (~2-3 days)`), not a bare letter alone. Applies here and at STEP 4.2.
- **Hard gate marking:** any gate marked "complete" in `current_roadmap.md` must reference the PoG/evidence artefact that cleared it. No artefact → gate stays "pending."
- **Header formatting:** all Class 4 headers written/updated in STEP 9 use bold labels: `**Owner:**`, `**Status:**`, `**Class:**`, `**Last Updated:**`.
- **Last Updated header-history retention (ST-17, EPIC-03, v8.2, BLG-GOV-283):** when appending a new entry to a chained `**Last Updated:**` field (e.g. `current_roadmap.md`), apply `shared_standards.md §16.14`'s retention rule — retain the current entry plus at most 2 prior entries (3 total); if the new entry would exceed this depth, drop older entries and close the chain with `prior history retained — see prior entries in version control`.

**Decision log append-only enforcement (structural):**
- Before writing: count existing entries (N). After writing: re-read; confirm count = N + entries added this run. Count decreased → halt. Any existing entry text changed → halt. Both checks must pass before STEP 9 commit.

**Post-write park count verification:**
After completing all `ideas_register.md` park count updates, grep for rows still containing the prior cycle's park count value in `Parked-cycle-N | N` format and confirm zero rows remain with outdated counts. This prevents context-compaction truncation artifacts from leaving stale park counts in the register.

---

### STEP 10 — Publish Delta Summary
Authority: Facilitator

Write `claude/cycles/<cycle_id>/cycle_summary.md` covering:
- Run type; capacity freed (or "N/A — scheduled")
- Initiatives added/stopped; net roadmap change
- Key risks reduced; key skills reallocated
- Backlog reconciliation counts (moved/promoted/killed)
- Stale ideas closed this cycle
- Prior cycle outstanding actions: resolved count / carried forward count

---

### STEP 11 — Lessons Learnt
Authority: PMO Lead (process), Head of Specs Team (prompt change sign-off)

Purpose: capture process friction and produce governed prompt changes. Not a retrospective; must not re-litigate decisions.

#### 11.1 Invoke Lessons Learnt Prompt

Invoke `claude/system/lessons_learnt_prompt.md` (§3.1 Roadmap Rebalance inputs). Missing → halt; do not fall back to a minimal structure.

Output: `claude/cycles/<cycle_id>/lessons_learnt.md` — following the structure in `lessons_learnt_prompt.md §5` exactly. Every friction item: classification (Type A–E), blast radius analysis, process patch (immediate or deferred). Deferred patch without named owner + target date → escalate to Head of Specs Team under Escalations.

Terminal block (machine-readable, at end of file):
```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "<cycle_id>",
  "phase": "Roadmap",
  "filed_utc": "<ISO-8601 UTC>",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```

#### 11.2 Prompt Change Classification

Every process patch classified as:
- **Action-now:** Head of Specs Team explicit confirmation required → apply patch → version bump → update `Last Updated` → record in `prompt_change_log.md`.
- **Defer:** must name exact file path, exact section, exact one-sentence change, named owner (role), target date. Vague defers → escalations. **Target date must be a cycle_id or an absolute date — not a bare release version alone** (a release can ship before or after any given rebalance independent of cycle cadence). If a release version is the natural reference, also record a concrete date estimate alongside it (e.g., "v6.3 (target ships ~2026-06-28, revisit by 2026-07-01__scheduled)") so STEP -1.5's stale-release-target check has a deterministic fallback.

#### 11.3 Prompt Change Log (Append-Only)

Record every action-now patch in `claude/system/prompt_change_log.md` (create as Class 6 if missing) with: heading `## <date> — <file path> v<old> → v<new>`, then Triggering friction item, Cycle, Change applied (one sentence), Confirmed by. Exact template: §STEP 11.3 below.

#### 11.4 Meta-Review Trigger (Every Third Cycle)

Count completed rebalance cycles since `last_meta_review_cycle` in `.claude_current_state.json`. If ≥ 3:

1. Load lessons learnt from all cycles since last review.
2. Aggregate friction items by Type A–E.
3. Identify: type appearing ≥ 2 cycles; deferred patch carried forward > once; §9 invariant triggered > once.
4. For each pattern: one candidate prompt change (specific file, section, improvement).
5. Present to Head of Specs Team: Apply now or Defer with owner + date.
6. Record in `claude/cycles/<cycle_id>/meta_review.md` (Class 3, Owner: PMO Lead).
7. Update `.claude_current_state.json` key `last_meta_review_cycle` to this cycle_id.

Not due: record "Meta-review not due — <n> cycles since last review" in `cycle_summary.md`.

If `last_meta_review_cycle` absent: initialise counter; meta-review triggers after third completed cycle.

---

### STEP 12 — Stage, Commit & Global State Update

**Preconditions (all must be true):** STEP 8.5 passed; STEP 10 complete; no outstanding halts; all writes match verified write plan.

#### 12.1 Global State Update

**Artefact existence precondition (hard gate):** Before updating `last_rebalance_cycle` in `.claude_current_state.json`, verify the following files exist in `claude/cycles/<cycle_id>/`: `run_manifest.md`, `cycle_record.md`, `cycle_summary.md`, `lessons_learnt.md`. If any is absent, complete the missing artefact before updating the state file. Do not update state to reference a cycle with incomplete artefacts.

Update `.claude_current_state.json` (rebalance keys only — do not overwrite `active_cycle`, `status`, or `backlog_slice_path`):

```json
{
  "last_rebalance_cycle": "<cycle_id>",
  "last_rebalance_utc": "<ISO-8601 UTC>",
  "last_rebalance_outcome": "<No-change | Add | Replace | Defer | Kill — brief summary>",
  "last_rebalance_pvr": "<STEP 2.4's computed user_value_ratio, as a bare number, e.g. 0.42 — null if STEP 2.4 did not run/compute a value this cycle>",
  "last_skill_silo_rolling_avg": "<STEP 7.1's rolling 3-cycle Skill-Silo Governance story % / 100, as a bare number, e.g. 0.548 — null if STEP 7.1 did not run/compute a value this cycle>",
  "last_meta_review_cycle": "<cycle_id | unchanged if not due>",
  "last_sync_utc": "<ISO-8601 UTC>"
}
```

**Structured PVR/Skill-Silo fields (ST-40, EPIC-05, v9.1, BLG-GOV-307):** `last_rebalance_pvr` and `last_skill_silo_rolling_avg` are additive — they make STEP 2.4's/STEP 7.1's already-computed values queryable as top-level numeric state fields; `last_rebalance_outcome`'s own prose summary is unchanged. Both new fields are `null` on any rebalance where the corresponding STEP's diagnostic did not produce a value — never fabricate a number to avoid a `null`.

**Advisory — next_release after DL decision (OA-02/ST-22, v4.6):** After the DL decision at STEP 8 sets the next planned release label, update `next_release` in `.claude_current_state.json` to the projected version label if determinable. Advisory only — `release_planning_prompt.md` STEP 9 remains the authoritative source and overwrites this unconditionally at its own seal. Leave unchanged if not determinable from the DL decision.

If `.claude_current_state.json` does not exist: create it with rebalance keys only.

**Scheduled-run recency marker (v9.8, BLG-GOV-216):** If this run's `--reason` is `"scheduled"`, also set `last_scheduled_rebalance_utc` = this run's `last_rebalance_utc` value in the same write. This field is read by STEP -1.5.5's recency advisory and by the Extended-tier "> 90 days since `last_scheduled_rebalance_utc`" check (§2.4) — without this write, both checks would read a stale or never-set value. Do not set this field for `--item-id` completion-triggered runs (it is scoped to scheduled invocations only).

**Session end (UTC) (ST-32, EPIC-05, v9.5, BLG-GOV-316):** Immediately before STEP 12.2's commit, capture `Session end (UTC)` in `run_manifest.md` via a real shell timestamp command, and record the computed elapsed duration against `Session start (UTC)` from STEP 1.1. Per `shared_standards.md §22`. If this session halts at a hard gate before reaching STEP 12: record the halt point's timestamp as Session end instead, noted `(halted, not completed)`.

#### 12.2 Commit

Stage only files within Section 4 write scope that were modified in this run. Commit message: `Roadmap rebalance <cycle_id>`.

**Governance file edit check (ST-13 / CF-2):** Before committing, if any §6-governed file (per OPERATIONAL_GUIDE.md §14) was modified: confirm version bump applied, OPERATIONAL_GUIDE §14 updated, and `prompt_change_log.md` entry appended. All three must complete before commit.

Precondition fails → do not stage; do not commit; report reason; halt.

If git unavailable: output exact file list to stage and exact commit message; mark "Ready to commit."

---

## 9. Invariants

→ Apply `claude/system/shared/governance_preamble.md §Invariants` (system-wide) and `claude/system/invariants.md`. Violation → halt.

---

## 10. Completion Condition

The run is complete when the STEP 12 commit succeeds with no outstanding halts. If blocked: report the exact failing step and rule.

---

# Part B — Detailed Rationale and History (for Core Sections 1–8.5)

---

## STEP 0.C — Condensed-tier trigger threshold review (full rationale)

**Trigger (ST-38, EPIC-04, v9.2, BLG-GOV-247):** reviewed whether "Condensed if no new FTE required" is sufficient on its own, or whether it should be formalised into a multi-condition threshold set (e.g. additionally requiring the Skill-Silo Alert and PVR readings both be outside their Alert tiers, or initiative count below some N).

**Decision: retain the single "no new FTE required" test as-is — no additional thresholds added.**

**Rationale:** The Condensed row only applies within the **Lightweight** tier, whose own entry conditions (Step 0.C) already require zero Submitted ideas, no ⚠/❌ initiatives, and a completion-triggered run — i.e. by the time a session reaches the point of asking whether STEP 7 can condense, the surrounding context is already tightly scoped to a low-impact session. Adding further conditions specifically to the Condensed test itself would duplicate constraints the Lightweight-tier gate already enforces one level up, rather than closing a real gap. If a future cycle finds a Lightweight-tier session where "no new FTE required" alone produced an under-scrutinised workforce decision despite Lightweight's other conditions holding, that would be new evidence for revisiting this decision — none has been observed as of this review.

**Authority:** Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-38, 2026-09-08).

---

## STEP 2.3 — Credential-fallback guidance (full rationale and history)

**Context (v9.6, resolves `2026-07-24__scheduled` Friction Item 2):** Before attempting a live re-check, confirm production API credentials are actually available in the executing checkout (e.g. a non-empty `REACT_APP_API_KEY` in `.env`/`.env.staging`/`.env.production`). If credentials are absent or the live call returns an auth failure (e.g. `401 Unauthorized`):
- Do not write a "live re-confirmed" claim — this would misrepresent whether verification occurred.
- Cite the existing `**Last formally confirmed:**` structured field unchanged.
- Record explicitly in `run_manifest.md` that a live check was attempted and why it did not succeed (e.g. "credentials unavailable in this environment" vs. "not attempted") — distinguish this from a session that never attempted the check at all.
- This is advisory bookkeeping only; it does not change the gate's MET/NOT MET status, which is governed solely by the structured field's own recorded value.
- **Read-only staging credential (v9.25, `2026-09-19__scheduled` Friction Item 3):** a `DATABASE_URL` pointing at the read-only *staging* database (provisioned for governed sessions by `BLG-OPS-121`) may be used opportunistically for a single aggregate read (`default_transaction_read_only=on`, counts only, URL never printed) as **context**. Confirm which environment the URL targets (host keyword or database name) before citing any value, and cite it explicitly as *staging*: its data (e.g. 14 closed trades / 1 trade plan at `2026-09-19`, against production's last formally confirmed 20 / 11) is not the production database's, so it is **not** a production confirmation and `**Last formally confirmed:**` must not be updated from it. Record the attempt and its target environment in `run_manifest.md`.

**Standing-behaviour decision (ST-15, EPIC-03, v8.2, BLG-GOV-279 — closes the recurring "should attempt genuine live re-check" carry-forward pattern):** Product Owner formally decided (2026-08-04) to accept the fallback-citation pattern above as **permanent, intended behaviour** — not an open gap awaiting a future credential-provisioning fix. Rationale: a production API key was never persisted into the gitignored `.env.production`/`.env.staging` files across every session checked from `2026-07-17__scheduled` through this decision (confirmed empty again at `2026-08-04`, 3+ consecutive months); repeated per-cycle carry-forward notes asking "the next rebalance should attempt a genuine live re-check" have not changed this, since no governed routine has write access to provision a real secret into version control by design (secrets are correctly excluded from git). The fallback-citation pattern itself is not a degraded workaround — it is fully transparent (distinguishes `**Last formally confirmed:**` from `**Unverified report:**`, never misrepresents an unattempted check as a confirmed one) and has already proven reliable across 6+ consecutive cycles. **Future rebalance/release-planning sessions must not file a new carry-forward item asking for "a genuine live re-check next cycle"** — that framing is retired. A live re-check remains welcome opportunistically (e.g. if a human supplies credentials mid-session, as occurred once at `2026-07-27__release-v7.9` EPIC-08/ST-08), but is no longer tracked as outstanding governance debt.

## STEP 2.3 — Six-Arc model vs. backlog-driven delivery (full rationale and history)

**Standing operating-mode note (v9.20, STEP 11.4 meta-review, `2026-09-14__scheduled`, resolves a deferred patch carried since `2026-07-28__scheduled`):** When the Now/Next horizons have been empty across multiple consecutive scheduled cycles *and* every Later/Gated item's own pre-condition remains independently unmet (i.e. Horizon Review finds "no movements warranted" for a genuine data/gate reason, not neglect), this is not itself a process failure requiring a fresh friction item each cycle — it is the expected shape of this project's current operating mode: backlog-driven debt clearance while the Arc-gated data-density thresholds (SI-02 linked-trade count, Arc 6 trade-count minimums, etc.) mature. Confirmed at `2026-09-14__scheduled`'s STEP 11.4: 12 consecutive 0-active-initiative cycles, 11+ consecutive cycles with an empty Now horizon, and 5 consecutive releases (`v8.9`–`v9.3`) shipped entirely backlog-driven with no formal Arc-scoped roadmap section created — each individually re-diagnosed as correct at the time, never as a defect. Record the operating mode explicitly in this cycle's `run_manifest.md`/`cycle_record.md` (e.g. "Horizon Review: no movements warranted — operating mode note applies") instead of re-opening a "Six-Arc model vs backlog-driven delivery" deferred patch each time the same underlying condition (gates unmet) recurs. This does **not** retire the Horizon Review itself — every cycle must still actually check each gate/pre-condition against current data (a gate clearing is real news and must promote normally) — it retires only the redundant *meta*-observation that the divergence exists, once that divergence's cause (unmet data gates, not neglect) has been confirmed stable across multiple cycles. Should the underlying cause ever change (e.g. a gate clears and the roadmap is *still* not updated to reflect it), that is a genuine process gap and must be raised fresh, not suppressed by this note.

---

## STEP 7.1 — Skill-Silo Alert (full rationale and history)

**Workload-composition framing (ST-24, EPIC-04, v9.2, BLG-GOV-209 — clarifies, does not replace, the core formula):** the "Governance story %" formula uses STEP 2.4's U/G/D/P tags as its input, but U/G/D/P is a **product-value** lens (why a story matters — user-facing vs governance vs debt vs process) computed at ship time, not a **workload-composition** lens (who/what skill actually did the work). The two usually correlate but can diverge — e.g. a `D`-classified (debt) story executed primarily by Backend Engineering Owner is execution-heavy by workload even though it is debt-shaped by product value. When classifying an initiative as Governance-heavy/Execution-heavy for this alert, prefer the role-based bucketing in `docs/specs/metrics_definitions.md` Appendix D's Skill-Category Taxonomy (ST-35, same cycle) — driven by the story's actual `**Owner:**` field, the same field §7.2 already tallies — over the U/G/D/P proxy where the two disagree. The U/G/D/P-based formula remains the default when no per-story Owner breakdown is readily available (e.g. very early cycles before the taxonomy existed).

**> 40% Ceiling, correction-persistence note:** A single U-item pull-forward is not guaranteed to bring the rolling average back under the ceiling — a heavy governance/debt cycle can outweigh one prior cycle's correction (observed: bundling one U-story at v6.4 raised the 3-cycle average from 53.2% to 64.8% rather than lowering it, since the two remaining cycles in the window were both debt-heavy). If the alert has fired for 2+ consecutive cycles despite a prior pull-forward, the PO should consider prioritising more than one user-facing item at the next release rather than repeating a single-item correction.

**Candidate gate verification (LP-05, v8.2 — fixes silent naming of gated candidates):** This closes the gap where `2026-07-03__scheduled` named BLG-FEAT-52 as a candidate without checking its own PO-02 gate, which release planning then had to catch and reject.

**Candidate live-status cross-check (v9.7 — fixes same-session stale naming):** This closes the gap where `2026-07-27__scheduled` named `BLG-FE-128` as an advisory pull-forward candidate after that same day's earlier `groom backlog` run had already archived it as shipped v7.8 scope; the error was only caught downstream at `plan release v7.9`, via an appended `[CORRECTION ...]` annotation (see `lessons_learnt.md` Friction Item 1, `2026-07-27__release-v7.9`).

**Mandatory pull-forward on sustained failure (v8.3 — closes the story-shape gap identified at `2026-07-04__release-v6.6` closure and confirmed a 2nd time at `2026-07-06__scheduled`):** This closes the gap where v6.5 and v6.6 each bundled 2 nominal U-items but only 1 resolved to genuine `U` at ship in both cases (the other was audit-shaped and correctly reclassified `D`), so the "2-item correction" was never actually tested as designed.

**Cross-role pairing rotation note (ST-37, EPIC-05, v9.5, BLG-GOV-322):** `claude/roadmap/workforce_capacity.md`'s "Cross-Role Pairing Rotation Note" section is informed by the accumulated §7.1/§7.2 historical pattern.

---

## STEP 7.2 — Cross-Role Workload Balance Check (full rationale and history)

**Formal threshold review (ST-37, EPIC-04, v9.2, BLG-GOV-300):** the 40% ceiling was reviewed against the alternative of mirroring §7.1's mandatory-pull-forward escalation (a hard scope requirement after 3+ consecutive over-ceiling readings).

**Decision: retain advisory-only, no mandatory escalation added.**

**Rationale:** §7.1's Skill-Silo Alert measures *story shape* against a product-value lens where a sustained imbalance genuinely signals under-delivery of user-facing value — a condition the Product Owner should be forced to correct. §7.2 measures *role concentration*, which can legitimately and durably reflect a release's genuine thematic focus (e.g. a multi-cycle governance-debt-clearance arc naturally and correctly concentrates on Head of Specs Team) without indicating a problem needing correction. Forcing a mandatory rebalance based on role concentration alone risks displacing genuinely load-bearing work with artificial role-diversification stories that don't serve product goals. The 40% ceiling is confirmed as-is; no threshold value change, no escalation tier added.

**Sign-off:** Director of HR (this check's definition, not each individual reading — readings are advisory and self-surfacing at each rebalance). Formal threshold review (ST-37) also sign-off cleared: Director of HR — Approved. Confirms the advisory-only design was a deliberate choice examined here, not an oversight, and correctly distinguishes this check's role-concentration lens from §7.1's product-value lens rather than mechanically copying that section's escalation tier. Sprint Execution Engine (agent-mediated, Director of HR role — §5.3), 2026-09-08.

---

## STEP 7.3 — Ready-Pool Capacity Gap Trend (full rationale and history)

**Origin:** post-ship closure `2026-09-14__release-v9.4`, `LL-v9.4-Release-Carry-03`, resolving Outstanding Action #1 — this check tracks whether the ungated/ready backlog pool is growing faster than sprint capacity can consume it, a trend first flagged as a standing watch-item at `2026-09-14__release-v9.4` release planning (ready pool more than doubled in one cycle, 61→74 items / 41.0→65.05 days, purely from one idea-intake window landing almost entirely ungated).

**Runway projection (ST-32, EPIC-06, v9.8, BLG-GOV-340):** `docs/specs/metrics_definitions.md` Appendix F's "Ready-Pool Runway Forecast" metric projects a "cycles until empty" figure from the same leftover-pool figures, using a rolling-3-cycle trailing net-change average.

**Historical reading (recorded at `2026-09-14__release-v9.4` post-ship closure, resolving that cycle's own Outstanding Action #1):** 2 consecutive releases of widening gap (v9.3: 34 items/~13.1 days unselected; v9.4: 46 items/~37.5 days unselected) — below the 3-consecutive threshold. **Decision (Head of Specs Team + PMO Lead, 2026-09-15, per explicit user direction resolving the outstanding action):** no capacity-band or sub-tiering change made at that time — one more consecutive widening reading would cross the mandatory-review threshold this section defines. This is deliberately a lower bar than §7.1's Skill-Silo mandatory-pull-forward (which requires 3 consecutive *unresolved* readings before forcing a decision) because a ready-pool gap that keeps widening for 3 straight releases is a purely mechanical trend, not a judgment call the Product Owner might reasonably resolve without new information — codifying the trigger avoided re-deriving this threshold ad hoc at whichever future rebalance happened to notice a 3rd widening reading.

**Sign-off:** Head of Specs Team + PMO Lead — Approved. Sprint Execution Engine (agent-mediated, per explicit user direction resolving post-ship closure `2026-09-14__release-v9.4`'s Outstanding Action #1), 2026-09-15.

---

## STEP 8.1.5 — §13-Adjacent Initiative Expiry Review (retroactive validation detail)

**Retroactive validation (required by ST-19/BLG-GOV-245's own AC):** this check was run against `claude/ideas/rejected_but_strong.md`'s existing revival-tracking entries. As of the `run ideas housekeeping` outcome recorded in `.claude_current_state.json` at the time this check was written, `IDEA-strategy-owner-20260304-02` and `IDEA-challenger-20260304-01` were both recorded "§13 ATR review-gated" and "Unmet — no §13 ATR review opened," first flagged 2026-03-04 — well over 2 rebalance cycles at that point. This confirmed the check would have fired correctly against this real historical example at any rebalance from approximately mid-2026 onward, had it existed — satisfying the AC without requiring a fabricated example, since a genuine, currently-still-open qualifying case already existed in the live idea register.

**Sign-off:** Strategy Rules & System Intent Owner — Approved. The check correctly stays soft-gate/advisory (a §13 review's timing is a genuine strategy judgement call, not something a mechanical cycle-count should force), while still ensuring a multi-month-open gate can no longer go unmentioned cycle after cycle purely because no one re-opened the idea register. Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3), 2026-09-08.

---

## STEP 8.2 — Now Horizon Item Verification (why this is distinct from STEP 8.0.5)

STEP 8.0.5 pre-cleans the *formal candidate list compiled at STEP 3*. STEP 8.2 catches items introduced at STEP 8 scope composition time via prose references — run_manifest entries, sprint history text, or prior-cycle conditional cluster notes — that did not go through the STEP 3 candidate list. Root cause: `2026-06-19__scheduled` included BLG-GOV-113 (archived since v5.3) in the v6.0 Now conditional scope because it was cited in a context-window run_manifest entry; the error propagated to `cycle_summary.md` and `DL-048` before correction at STEP 9 write verification. This step prevents that class of error. (Added v7.6, deferred patch from `2026-06-19__scheduled` lessons_learnt, Head of Specs Team sign-off.)

---

## STEP 8.0.5 — Candidate List Pre-Clean (why this is mandatory, not advisory)

Presenting complete items to the PO wastes debate time and inflates apparent scope. Two consecutive cycles (v5.4 LL-RP-01; v5.5 LL-RP-02) saw complete items appear in candidate lists despite STEP 8.0.5 existing. Root cause: candidate lists were compiled without running the grep. Compile-time execution (STEP 3) is the permanent fix. (Added AUD-2026-06-10-003 v5.4; strengthened to Mandatory at STEP 3 + STEP 8.1 v7.1 LL-RP-02.)

---

## STEP 8 — Displacement Debt Register seed content and design

If `claude/roadmap/displacement_debt_register.md` does not yet exist, create it using the format, purpose statement, and seed content documented at `claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md#Displacement Debt Register — Design` (this instruction was originally added by `execution_prompt.md`'s Sprint Execution Engine at ST-21, which — per its own §7 write-scope hard gate — could edit this prompt but could not itself create files under `claude/roadmap/`; physical creation was deferred to this routine's own next live invocation, which does hold that write scope).

---

## STEP 5.3 — Proof of Gate (PoG) exact field template

```
**Owner:** <role>
**Class:** Proof of Gate (Class 8)
**Status:** Active
**Gate ID:** POG-<YYYYMMDD>-<nn>
**Issued:** <date>
**Cycle:** <cycle_id>
**Initiative:** <name>
**Gate cleared:** <one sentence>
**Versioned document referenced:** <file path> v<version>
**Decision:** <exact decision text>
**Confirmed by:** <role name>
**Checksum note:** <document version at time of signing>
```

---

## STEP 11.3 — Prompt Change Log exact entry template

```markdown
## <date> — <file path> v<old> → v<new>

- **Triggering friction item:** <description from lessons_learnt.md>
- **Cycle:** <cycle_id>
- **Change applied:** <one sentence>
- **Confirmed by:** Head of Specs Team
```

---

## Core wording moved at v9.35 (verbatim)

On 2026-10-16 (roadmap rebalance `2026-10-16__scheduled` STEP -1.5, Head of Specs Team action-now patch, user-directed), these paragraphs were shortened in `roadmap_prompt.md` so the core fits under 24k tokens. The core keeps each actionable rule. The v9.34 wording is kept here unchanged for its rationale, history and worked figures. Where the two differ, the core governs.

### STEP 6 — Same-day collision check

**Same-day collision check (v8.7, 2026-07-12):** Before creating `claude/cycles/<cycle_id>/`, check whether that path already exists. If it does (a prior scheduled or completion-triggered run already used this exact `cycle_id` today): do not write into it. Append `-2`, `-3`, … (lowest unused integer) to form the new `cycle_id`, and record the collision and resolved `cycle_id` in `run_manifest.md`. Non-blocking, automatic — no user confirmation required.

### STEP -1.5 — Out-of-scope OVERDUE resolution

- **Out-of-scope OVERDUE resolution (v8.7, 2026-07-12):** If an OVERDUE patch's target file is outside this engine's Write Scope §4 (e.g. `CLAUDE.md`), "outside scope" is not itself a valid carry-forward reason once a named authority holds a standing out-of-band write privilege for that file (e.g. `shared_standards.md` §17). The escalation to Head of Specs Team must then instruct applying the patch directly under that standing authority this session, rather than carrying it forward again. Full history: `roadmap_prompt_appendix.md` §STEP -1.5.

### STEP -1.5 — Condition-gated defer exemption

- **Condition-gated defer exemption (v8.8, 2026-07-13):** A deferred patch whose Target field names a recurrence condition (not a cycle_id or absolute date) is **not** subject to the "second consecutive cycle → OVERDUE" rule. Instead, apply a **Stale Condition-Gated Defer** advisory (non-blocking) once such a defer has been carried for **6 or more consecutive cycles** without its condition recurring: escalate to Head of Specs Team to assess whether the condition is realistic, and consider rewriting it as an unconditional action-now patch or retiring it. Full history: `roadmap_prompt_appendix.md` §STEP -1.5.

### STEP -1.6 — Standalone pre-run exception

**Standalone pre-run exception (v9.27, `2026-09-30__scheduled`):** If a `run ideas` window was already opened and closed standalone within the same session-chain immediately prior to this invocation — its submissions still `Submitted`, not yet processed by STEP 4 — do not open a second inline window merely because the open-idea count is still < 20; proceed directly to STEP 4 with those submissions. Does not apply when the open rows are all `Parked-cycle-<n>` carries with no fresh `Submitted` rows — that case still triggers a fresh inline window. Record which path was taken in `run_manifest.md`. Full rationale: `roadmap_prompt_appendix.md` §STEP -1.6. **Reduced-roster bound (ST-43, BLG-GOV-364, v9.12):** the exception applies only if that standalone window complied with `idea_intake_prompt.md` §4.1. An inline window opened by this step is full roster unless §4.1 conditions 1–4 are met and recorded in `run_manifest.md`.

### STEP -1.7 — Outstanding Action Count

3. **Outstanding Action Count** — from `open_escalations` (state file + execution_state.json) + prior `lessons_learnt.md`, **plus a due-date-aware scan (v9.3, widened v9.4)**: read the last 3 completed cycles' `lessons_learnt_closure.md`/`lessons_learnt.md` files across all five routines, and surface any escalation whose stated deadline falls on or before the current cycle's date, regardless of named owner. Check both the standard `^## ESC-`/`SLA due-by`/`Disposition: Open` pattern and any `## Recurrence Escalations` table (per `lessons_learnt_prompt.md §5`) naming "next roadmap review" or an equivalent checkpoint. List each by ID (or description) and owning routine.

### STEP 0.C — Condensed-tier trigger threshold

**Condensed-tier trigger threshold (ST-38, EPIC-04, v9.2, BLG-GOV-247):** reviewed and decided — retain the single "no new FTE required" test as-is; no additional thresholds added (the Lightweight tier's own entry conditions already tightly scope this). Full rationale: `roadmap_prompt_appendix.md` §STEP 0.C.

### STEP 1.1 — Meta-Review Countdown

- **Meta-Review Countdown (ST-27, EPIC-04, v9.2, BLG-GOV-217):** read `last_meta_review_cycle` from `.claude_current_state.json` and count completed rebalance cycles since. Record as `"<n> of 3 cycles since <last_meta_review_cycle> — not due"` or `"DUE this cycle — see §11.4"` when `n >= 3`. This is the same count §11.4 itself computes at STEP 11.4 — surfacing it here at STEP 1.1 makes the countdown visible from the very first artefact of the session instead of only appearing once STEP 11.4 runs near the end.

### STEP 2.3 — SI-02 gate read instruction

**SI-02 gate read instruction (v8.4, LP-09):** When citing the SI-02 trade-count gate, read the structured `**Last formally confirmed:**` / `**Unverified report:**` sub-fields directly below the SI-02 row in `current_roadmap.md` §5 (Arc 5 Later horizon table) rather than re-deriving the distinction from prose. Cite `**Last formally confirmed:**` as the authoritative value for gate-clearance decisions; note `**Unverified report:**` as context only. Only a governed routine with direct production database/API access may update `**Last formally confirmed:**`.

### STEP 2.3 — Credential-fallback guidance

**Credential-fallback guidance (v9.6):** Before attempting a live re-check, confirm production API credentials are actually available in the executing checkout. If absent or the live call fails auth: do not write a "live re-confirmed" claim; cite the existing `**Last formally confirmed:**` field unchanged; record in `run_manifest.md` that a live check was attempted and why it did not succeed. A read-only *staging* `DATABASE_URL` (per `BLG-OPS-121`) may be cited opportunistically as context only — never updates `**Last formally confirmed:**`. **Standing-behaviour decision (ST-15, EPIC-03, v8.2, BLG-GOV-279):** Product Owner formally decided (2026-08-04) this fallback-citation pattern is permanent, intended behaviour — future sessions must not file a new carry-forward item requesting "a genuine live re-check next cycle." Full rationale and history: `roadmap_prompt_appendix.md` §STEP 2.3.

### STEP 2.3 — Six-Arc model vs. backlog-driven delivery

**Six-Arc model vs. backlog-driven delivery — standing operating-mode note (v9.20):** Empty Now/Next horizons with every Later/Gated pre-condition genuinely unmet is expected operating-mode behaviour, not a process failure needing a fresh friction item each cycle. Record the operating mode in `run_manifest.md`/`cycle_record.md`. Does **not** retire the Horizon Review — still check each gate/pre-condition against current data every cycle. Full rationale: `roadmap_prompt_appendix.md` §STEP 2.3.

### STEP 2.4 — Read the tag

**Read the tag, don't re-derive it, when one exists:** from `post_ship_closure.md` v2.17 onward, each `Tech backlog items shipped` line carries an inline `[U|G|D|P]` tag assigned at ship time — use it directly. Only fall back to judgment-based classification for cycles shipped before this tagging convention existed (pre-v6.6) or if a line is missing its tag. (Removes reconstruction-variance risk — see `2026-07-02__scheduled`/`2026-07-03__scheduled` lessons learnt.)

### STEP 2.4 — Optional acceleration

**Optional acceleration (ST-25, EPIC-04, v9.9, BLG-GOV-352):** `python3 scripts/compute_rebalance_diagnostics.py docs/product/changelog.md` reproduces this computation mechanically from the changelog's own `[U|G|D|P]` tags. It is an acceleration, not a hard dependency — this STEP's own manual procedure above remains authoritative if the two ever disagree (e.g. a cycle shipped before the tagging convention existed, pre-v6.6, which the script silently skips).

### STEP 2.4 — Structured history

**Structured history (ST-22, BLG-FEAT-72, v8.5):** In the same commit, append one row to `claude/roadmap/product_value_ratio_history.md`'s History table (cycle_id, date, ratio, tier, U/G/D/P, total, window, this cycle's `decision_log.md` `DL-xxx` reference) and refresh its sparkline. This is the durable, structured trend record — read it (not `decision_log.md` prose) when checking the sustained-tier consecutive-readings rules below. `decision_log.md`'s own prose sentence is still written as before (unchanged) — this is an addition, not a replacement.

### STEP 2.4 — Effort-weighted reading

**Effort-weighted reading (ST-34, EPIC-06, v9.11, BLG-GOV-355 / BLG-GOV-339):** In the same History row, also fill the `Effort-weighted Ratio` column, to three decimals: effort-days of U stories ÷ effort-days of U+G+D+P stories over the same 5-cycle window, using the same U/G/D/P tags as the story-count ratio. Weight each story by the `**Estimated effort:**` line under its `#### ST-xx` block in its own cycle's `sprint_backlog.md`, converted to days with the normalisation table in `docs/specs/metrics_definitions.md` Appendix F (PVR Measurement Package, "1. Effort-weighted PVR"). Exclude from both numerator and denominator any story with no matching `#### ST-xx` block, no `**Estimated effort:**` line, or a value the table does not cover — never assign it an assumed weight. Record the coverage (weighted stories / total stories, e.g. `153/155`) and the excluded `ST-xx` IDs in `run_manifest.md`. If no story in the window can be weighted, write `—` in the column and give the reason in `run_manifest.md`. Record both readings in `run_manifest.md`'s `## Product Value Ratio Diagnostic` section. `scripts/compute_effort_weighted_pvr.py` implements the same method, but its windows are hard-coded and `scripts/` is outside §4 write scope: run it only if its `WINDOWS` map already contains this rebalance's window, and do not edit it during a rebalance — otherwise compute by hand; this manual procedure is authoritative if the two disagree. The effort-weighted reading is diagnostic only and carries no tier: the tier table above, the Product Value Alert and the sustained-Advisory rule below all continue to use the story-count `user_value_ratio`, even when the two readings fall in different bands.

### STEP 2.4 — Sustained Advisory tier

**Mandatory pull-forward on sustained Advisory tier (added v9.9 — ST-04, BLG-GOV-268, mirrors the Skill-Silo sustained-failure clause in §7.1):** Read the last several rows of `claude/roadmap/product_value_ratio_history.md` (not `decision_log.md` prose) to determine the consecutive-readings count. If the ratio has remained in the **Advisory band (0.30–0.49)** for **3 or more consecutive readings** (neither Healthy ≥0.50 nor Alert <0.30), the "Facilitator surfaces in STEP 8" action becomes a **mandatory scope requirement**: the Product Owner must commit **at least 1 build-and-ship-shaped U-item** at the next release, using the same content-based test as §7.1. Full rationale: `roadmap_prompt_appendix.md` §STEP 2.4.

### STEP 3.1 — Scale-appropriate methodology

**Scale-appropriate methodology (v9.1, 2026-07-16 — closes the deferred patch from `2026-07-15__scheduled` Friction Item 2, confirmed on its 2nd occurrence at `2026-07-16__scheduled`):** A full manual per-item read is the default method while the active backlog is below ~150 items. At or above ~150 active items, apply this structural heuristic instead:

### STEP 3.1 — Date-lapse re-check

**Date-lapse re-check (v9.25, closes `2026-09-19__scheduled` Friction Item 1):** the structural heuristic's step 2 classifies by keyword only, so an item whose gate date has passed stays counted gated indefinitely unless re-checked. After the A/T/D/L split, for every gated item whose `**Gate criteria:**` text names an ISO date or `~YYYY-MM-DD`, compare the **latest** such date with the run date; also check any gate naming a completed prior item against the archive. If the date is ≤ the run date, or the named event has occurred, re-classify the item **A (date-lapsed — verify)**, list it by ID in `run_manifest.md` with any *remaining* non-date conditions, and carry the list into the cycle summary's capacity outlook. A lapsed date is **not** proof the gate is met — it flags that nothing is currently checking it. Full history: `roadmap_prompt_appendix.md` §STEP 3.1.

### STEP 6 — Overwrite verification

**Overwrite verification (v8.6, resolves `2026-07-08__scheduled` Friction Item 1):** Before writing, if the file already exists, read it first and confirm the write fully replaces its content rather than appending. After writing, re-read the file and confirm it contains no section dated to a prior cycle — if it does, this is non-compliant drift, not intentional history; overwrite fully rather than append.

### STEP 7.1 — Workload-composition framing

**Workload-composition framing (ST-24, EPIC-04, v9.2, BLG-GOV-209):** the "Governance story %" formula uses STEP 2.4's U/G/D/P tags (a product-value lens), which can diverge from a workload-composition lens (who/what skill did the work). Prefer the role-based bucketing in `docs/specs/metrics_definitions.md` Appendix D's Skill-Category Taxonomy — driven by the story's `**Owner:**` field — over the U/G/D/P proxy where the two disagree; the U/G/D/P formula remains the default otherwise. Full rationale: `roadmap_prompt_appendix.md` §STEP 7.1.

### STEP 7.1 — Aggregation method (method-break note with restated readings)

**Aggregation method: pooled, and only pooled (ST-42, BLG-GOV-367, v9.12).** The rolling 3-cycle figure is the pooled ratio: the sum of G + D + P stories across the 3 cycles divided by the sum of all their stories, × 100. It is **not** the plain mean of the three per-cycle percentages. The two differ whenever cycle sizes differ. `scripts/compute_rebalance_diagnostics.py` computes the pooled form and labels it `method: pooled`, and `--silo-history N` prints the last N rolling readings by the same method. Every reading recorded in `## STEP 8` and every "improving / worsening / unresolved" judgement in this section (including the sustained-failure clause below) must compare pooled readings only. **Method-break note:** `claude/roadmap/decision_log.md` recorded plain means up to the v9.6–v9.8 reading and switched to pooled at DL-084 (v9.7–v9.9). Restated under the pooled method, the last 4 recorded readings are v9.3–v9.5 **99.0%** (97/98; recorded 98.8%), v9.5–v9.7 **87.4%** (90/103; recorded 85.7%), v9.6–v9.8 **84.8%** (84/99; recorded 83.7%) and v9.7–v9.9 **91.2%** (93/102; recorded as pooled). The trend directions are unchanged by the restatement: improving, improving, worsening. When judging trend direction, the next rebalance compares against these restated figures, not the recorded plain means.

### STEP 7.1 — > 40% Ceiling

**> 40% Ceiling:** Skill-Silo Alert. Scan backlog for highest-priority user-facing item (U-classified, no blockers, within available capacity) — present as pull-forward candidate. PO decides. Check is mandatory; result recorded in `## STEP 8`. A single U-item pull-forward is not guaranteed to bring the rolling average back under the ceiling — if the alert has fired for 2+ consecutive cycles despite a prior pull-forward, the PO should consider prioritising more than one user-facing item. Full rationale: `roadmap_prompt_appendix.md` §STEP 7.1.

### STEP 7.1 — Candidate gate verification

**Candidate gate verification (LP-05, v8.2):** Before naming any item as a pull-forward candidate, read that item's own backlog entry (`claude/backlog/backlog.md`) for a `**Gate criteria:**` line. If a gate exists, confirm it is met or near-term-clearing. If unmet with no confirmed near-term clearance: do not name it as a candidate — select the next-highest-priority ungated U-item instead, or name it explicitly marked `[gate status unverified/unmet — release planning to confirm before accepting into scope]`.

### STEP 7.1 — Candidate live-status cross-check

**Candidate live-status cross-check (v9.7):** Before naming any item as a pull-forward candidate, confirm it is still present and open in `claude/backlog/backlog.md` (not archived, not already `✅ COMPLETE`) — including any `groom backlog`/post-ship-closure action taken earlier in this same session. If archived or shipped within this same session: do not name it — select the next-highest-priority ungated U-item instead.

### STEP 7.1 — Mandatory pull-forward on sustained failure

**Mandatory pull-forward on sustained failure (v8.3):** If the rolling 3-cycle Skill-Silo average has worsened or remained unresolved for 3 or more consecutive readings, the pull-forward recommendation becomes mandatory: the Product Owner must commit **at least 2 build-and-ship-shaped U-items** at the next release (acceptance criteria require a shipped, user-visible change; an audit/investigation-shaped story does not count even if nominally labelled user-facing — classify using the same content-based test as STEP 2.4). Full rationale and history for all four rules above: `roadmap_prompt_appendix.md` §STEP 7.1.

### STEP 7.1 — Optional acceleration

**Optional acceleration (ST-25, EPIC-04, v9.9, BLG-GOV-352):** `python3 scripts/compute_rebalance_diagnostics.py docs/product/changelog.md` also reproduces the default U/G/D/P-proxy form of this STEP's "Governance story %" figure. It is an acceleration, not a hard dependency, and does **not** implement the workload-composition (Owner-field) refinement two paragraphs above — when that refinement is in use for a given cycle (Owner data available and it diverges from the U/G/D/P proxy), the manual procedure remains authoritative and the script's output should be treated as the proxy baseline only.

### STEP 7.2 — Method step 1

1. Read `claude/roadmap/role_share_history.md` — the structured per-cycle role-share record (raw-tally method: each ST item's `**Owner:**` string tallied verbatim, compound multi-role strings as their own bucket). If the most recently shipped cycle has no row yet, first run `python3 scripts/compute_role_share_history.py claude/cycles/<that cycle_id>/sprint_backlog.md` and append its History row and Full Per-Role Breakdown section to the file (same table formats; update the rolling-aggregate line) in this run's commit. Then take the last 3 shipped cycles (same rolling window as §7.1, for consistency) from the file — do not re-parse `sprint_backlog.md` Owner fields by hand for cycles already recorded there. **Fallback:** if the file is missing or unreadable, tally each cycle's `sprint_backlog.md` `**Owner:**` fields directly (the pre-v9.30 method) and record the fallback in `run_manifest.md`. (Structured history source added ST-26, BLG-GOV-353, EPIC-04, v9.9.)

### STEP 7.2 — Advisory-only rationale

4. This check is **advisory only** — it does not gate release scope and has no mandatory-pull-forward escalation (unlike §7.1's sustained-failure clause). Its purpose is visibility for the Product Owner and Director of HR to consider when scoping future releases (e.g. deliberately routing more stories to underrepresented roles' domains), not a hard rebalancing rule — role-story-count concentration can legitimately reflect the release's actual thematic focus (e.g. a governance-heavy debt-clearance cycle naturally skews toward Head of Specs Team) rather than a genuine bottleneck.

### STEP 7.2 — Formal threshold review

**Formal threshold review (ST-37, EPIC-04, v9.2, BLG-GOV-300):** reviewed against mirroring §7.1's mandatory-pull-forward escalation. **Decision: retain advisory-only, no mandatory escalation added** — role concentration can legitimately reflect a release's genuine thematic focus, unlike §7.1's product-value lens. Full rationale and sign-off: `roadmap_prompt_appendix.md` §STEP 7.2.

### STEP 7.3 — full section as it read at v9.34

#### 7.3 Ready-Pool Capacity Gap Trend (added — post-ship closure `2026-09-14__release-v9.4`, `LL-v9.4-Release-Carry-03`)

Distinct from §7.1/§7.2 (story *shape* and *role concentration*) — tracks whether the ungated/ready backlog pool is growing faster than sprint capacity can consume it. Full origin and history: `roadmap_prompt_appendix.md` §STEP 7.3.

**Method:**
1. At each rebalance, read the most recent Release Planning `run_manifest.md`'s recorded ready-pool size (items/days) and the confirmed capacity band's upper bound (days) — the newest `claude/cycles/*__release-v*/run_manifest.md`, `**Result:**` line under Scope Construction. Do not record "not re-measured" without naming the manifest checked (v9.31).
2. Compute the gap: ready-pool days minus capacity-band upper bound. A positive, growing gap across consecutive releases indicates the ready pool is outpacing what any single release can select.
3. **Mandatory review trigger:** if the gap has grown (not merely stayed positive, but increased release-over-release) for **3 or more consecutive releases**, this is no longer an advisory watch-item — it becomes a mandatory decision point: the Product Owner and Head of Specs Team must jointly decide, at that rebalance, between (a) raising the confirmed capacity band, or (b) introducing a secondary prioritisation pass within the P3 tier (sub-tiering), or (c) an explicit documented decision that the growing gap is acceptable and no action is needed. Record the decision and rationale in `decision_log.md`.
4. Below the 3-consecutive-release threshold: advisory only — note the gap and trend in `## STEP 8` output, no mandatory action.

**Runway projection (ST-32, EPIC-06, v9.8, BLG-GOV-340):** in addition to the gap-vs-ceiling check above, `docs/specs/metrics_definitions.md` Appendix F's "Ready-Pool Runway Forecast" metric projects a "cycles until empty" figure from the same leftover-pool figures, using a rolling-3-cycle trailing net-change average. When that figure is finite (the trailing trend is net-shrinking), cite it in this STEP's output alongside the gap reading; when it reads "N/A — pool growing", state that instead. If Appendix F lags the latest release, compute the reading from the run-manifest figures and record it here and in `workforce_capacity.md` — Appendix F is outside §4 write scope and is updated by its owner (`BLG-GOV-374`) (v9.31).

**Sign-off:** Head of Specs Team + PMO Lead — Approved, 2026-09-15. Full reading history and sign-off detail: `roadmap_prompt_appendix.md` §STEP 7.3.

### STEP 8 — Displacement Debt Register update

**Displacement Debt Register update (ST-21, BLG-GOV-264, v8.9):** Also update `claude/roadmap/displacement_debt_register.md` (create first if missing — seed content per `roadmap_prompt_appendix.md` §STEP 8). If the candidate has no row: add one (`Candidate`, `Rationale as flagged`, `First flagged` = this cycle's DL ID/date, `Times re-flagged` = 0, `Disposition` = "Named, not yet displaced"). If it has a row: increment `Times re-flagged` by 1 (unless added this cycle). If THIS step's Kill/Replace decision resolves a prior "Named, not yet displaced" row: set `Disposition` = "Displaced" with this cycle's DL ID/date.

### STEP 8.0.5 — call-site note

For each `BLG-<ID>` in the candidate list, run the Candidate/Item Backlog-Status Verification Subroutine above. Record removed items in `run_manifest.md` as "Already shipped — excluded from candidates." (Since these candidates were compiled directly from the active backlog at STEP 3, subroutine step 1's active-backlog check will always pass for them at this call site — the effective behaviour here is unchanged from the pre-extraction grep-and-marker-check.)

### STEP 8.0.5 — not advisory

This is **not advisory** — presenting complete items to the PO wastes debate time and inflates apparent scope. Full root cause and history: `roadmap_prompt_appendix.md` §STEP 8.0.5.

### STEP 8.1 — Version-labeling a resolved condition-1b carry-forward

**Version-labeling a resolved condition-1b carry-forward (v9.10 — ST-09, BLG-GOV-240):** Once condition 1b's un-versioned carry-forward heading has been adopted into a firm release, it no longer needs a full `run roadmap` invocation just to relabel it. `shared_standards.md` §17 grants Head of Specs Team standing authority to apply that narrow relabeling edit directly (heading label + adjacent metadata only — item content changes still require `run roadmap`/`plan release`).

### STEP 8.1.5 — non-blocking note

- This is **non-blocking** (soft gate, like STEP 8.1) — it does not force the §13 review to open, but it does force the finding to be surfaced rather than silently re-carried cycle after cycle. Strategy Rules & System Intent Owner is the role who can either schedule the review or record an explicit "still not ready, re-check next cycle" note; either response clears this cycle's surfacing (the item remains tracked and re-checked next cycle regardless).

### STEP 8.1.5 — sign-off

**Sign-off:** Strategy Rules & System Intent Owner — Approved, 2026-09-08 (agent-mediated, §5.3). Retroactive validation against real `rejected_but_strong.md` entries and full sign-off rationale: `roadmap_prompt_appendix.md` §STEP 8.1.5.

### STEP 8.5.B — BLG-ID collision advisory

5. **BLG-ID collision advisory (non-blocking):** Before assigning new BLG-IDs in STEP 5 debate summaries or STEP 8 decision records, grep **both** `backlog.md` **and** `backlog_archive.md` for the highest existing ID in each series (e.g. `grep -o 'BLG-GOV-[0-9]*' claude/backlog/backlog.md claude/backlog/backlog_archive.md | sort -t'-' -k3,3n | tail -1`). Assign IDs starting from highest+1 across both files — prevents both a same-day collision and reissuing an archived-only ID invisible to a `backlog.md`-only grep. Advisory only — does not halt. Full history: `roadmap_prompt_appendix.md` §STEP 8.5.B.

### STEP 8.5 — Extended-tier advisory

> **Extended-tier advisory:** For Extended-tier scheduled runs (40+ ideas), STEP 9 write volume (~13 files) may require a new session. Confirm the STEP 8.5.B write plan is complete and recorded in `cycle_record.md` before closing. The write plan is the resumption artefact — a new session executes STEP 9 by reading `cycle_record.md §8.5.B` directly without re-running STEPS 2–8.

### Continuation note

This core file covers Sections 1–8 through STEP 8.5 (preflight through the verified write plan). **STEP 9 (Canonical Write) through STEP 12 (Stage, Commit & Global State Update), plus the closing Invariants and Completion Condition sections, continue in `claude/system/roadmap_prompt_appendix.md` Part A.** This is not optional or supplementary material — it is the direct continuation of this same mandatory process, split out only so this core file fits a single read. Read Part A immediately after completing STEP 8.5 below.
