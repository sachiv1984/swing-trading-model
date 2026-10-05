**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-01 (ST-21, EPIC-04, v9.9, BLG-GOV-343 — created as part of splitting `roadmap_prompt.md` into a core + this appendix so the core fits a single read)
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
