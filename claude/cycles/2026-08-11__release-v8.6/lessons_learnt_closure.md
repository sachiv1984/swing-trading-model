Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-12
Cycle: 2026-08-11__release-v8.6

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Post-ship closure of v8.6 — User Features, Data-Integrity Foundation & Correctness Carryover (26/26 stories shipped, Verified_with_deviations, 1 P3 deviation accepted, 1 retroactive P1 resolved, 1 pre-existing P2 closed)
Run: 2026-08-11__release-v8.6
Reviewed by: PMO Lead
Date filed: 2026-08-12
Prior cycle checked: 2026-08-08__release-v8.5 (`lessons_learnt_closure.md`)

---

## What worked well

- STEP 3 (Backlog Reconciliation) was mechanically simple: all 26 shipped items located and marked `✅ COMPLETE` on the first pass via the v8.6 Release Slice table's exact EPIC→backlog-ID mapping, cross-confirmed against `execution_state.json`'s `completed_items` array — no missing-entry gaps, 0 Phase 4 additions required.
- STEP 5's Canonical Spec Deviation Compliance Check earned its keep this cycle: both `RESOLVED`-status deviation entries (`DEV-NAV-ST06-01`, `DEV-EPIC02-ST03-01`) were missing an explicit `Target resolution release` field (and `DEV-NAV-ST06-01` also lacked an explicit `Canonical requirement` field) despite otherwise being well-documented — caught and corrected in-session rather than silently passed as "good enough because it's already resolved."
- The prior cycle's (`v8.5`) `lessons_learnt_closure.md` Escalations — `BLG-GOV-292` (72h decision on gate-detection pattern) and `DEV-EPIC02-ST03-01`'s stale re-triage deadline — were both independently confirmed resolved before this closure began (`BLG-GOV-292` closed 2026-08-11 by direct Head of Specs Team action; `DEV-EPIC02-ST03-01` closed this cycle by EPIC-03/ST-10). Neither required action from this closure — confirmed only.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** No (related to, but not a repeat of, `2026-08-08__release-v8.5` Friction Item 1 — see note below)

**What happened:** `post_ship_closure.md` STEP 7.3's full-document `TSG-*`/`Status: Open` scan (the mechanism itself, fixed at `v8.5` in place of a hardcoded stale section-number reference) correctly found 0 new gaps this cycle, but a full sweep of the *entire* document — not just the entries a prior cycle's own reconciliation note happened to already be tracking — surfaced 2 long-stale `Status: Open` `TSG-*` entries that had gone unreconciled for many cycles: `TSG-v33-03` (Open since `v3.3`, 2026-05-13 — the underlying scenarios were confirmed present in `tests/e2e/pre-trade-research.spec.js` this session) and `TSG-v6.8-01` (Open since `v6.8`, 2026-07-08, last checked-and-left-open at `v7.8`'s own closure — the underlying backlog item `BLG-QA-86` had in fact shipped `v8.3`, 5 closures ago, with no closure in between re-running the check against it).

**Where in the routine:** STEP 7.3 — TSG backlog reconciliation.

**Root cause:** document staleness — prior closures' own STEP 7.3 reconciliation notes each only re-checked the specific entries that closure's own note-writer already knew about (typically the single most-recently-flagged one), rather than re-scanning the full document every time. The `v8.5` fix corrected the *section-number-drift* half of this bug class but did not itself guarantee a full re-scan on every subsequent run — it depends on the executing session actually reading "scan the full document" literally rather than only the entries named in the immediately preceding closure's own note.

**Blast radius analysis:**
- What would have propagated: `Specs_Index.md` accumulating an unbounded set of falsely-Open TSG entries that misrepresent real test-coverage status to any future roadmap-engine gap-check or audit reading this file at face value.
- When it would have surfaced: only at the next session that happened to do a full-document read rather than trusting the prior closure's own reconciliation note — as this cycle did.
- Recovery cost if uncaught: low per entry (single-line status correction) but compounding — 2 entries found stale across roughly 15 and 5 intervening cycles respectively, with no natural trigger forcing a full re-scan absent this observation.

**Process patch:**

→ Immediate patch applied this run:
  - File: `docs/specs/Specs_Index.md`
  - Section: §19.3 (`TSG-v33-03`), §36 (`TSG-v6.8-01`), new §39 (v8.6 Test Coverage Gaps + full-sweep reconciliation note)
  - Change: Marked both stale entries `✅ RESOLVED` with resolution evidence (live test file confirmation for `TSG-v33-03`; shipped-changelog cross-reference for `TSG-v6.8-01`); added a §39 section documenting this cycle's 0-new-gaps result and the full-sweep finding, explicitly noting the risk that reconciliation-by-note-inheritance (rather than full re-scan) allowed the drift.
  - Version: N/A — `Specs_Index.md` is a Class 6 index document versioned only via its `Last Updated` header, not a numbered governance prompt; header bumped 2026-08-07 → 2026-08-12.
  - Confirmed by: Head of Specs Team (post-ship closure STEP 7.3, this run)
  - Prompt change log entry: Not applicable — `Specs_Index.md` is not a governance prompt (Class 6); no `prompt_change_log.md` entry required.

---

### Friction Item 2

**Classification:** Type E — Authority Gap

**Recurrence:** Yes — appeared in `2026-08-07__release-v8.4` (Friction Item 1 / Outstanding deferred patch) and `2026-08-08__release-v8.5` (Recurrence Escalation, Carry-Forward #1)

**What happened:** `scripts/check_api_performance_baseline_drift.py`'s substring-based `find_missing_endpoints()` still produces false negatives for endpoints documented only in prose without an adjacent measurement row or dedicated heading (originally found: `GET /trade-plans/tags`). This cycle's own Release Planning `lessons_learnt.md` Carry-Forward #1 explicitly directed "the next Post-Ship Closure ... should consider applying [this] directly as immediate action rather than deferring a 3rd time." On investigation this run, the fix genuinely cannot be applied directly by this routine: `post_ship_closure.md §5` Write Scope Restriction permits edits only to a named list of governance/planning documents plus "templates and prompt files" — a bare Python script under `scripts/` is neither. Three consecutive closures (`v8.4`, `v8.5`, `v8.6`) have now carried this patch forward on the assumption that "the next Post-Ship Closure" is the correct venue to apply it directly; this run is the first to actually check that assumption against the write-scope rule and find it false.

**Where in the routine:** STEP 8 — Lessons Learnt Review and Application (reviewing Release Planning's Carry-Forward #1).

**Root cause:** authority ambiguity — the deferred-patch carry-forward mechanism (`lessons_learnt_prompt.md §3.7`) does not distinguish "fixes this routine can apply directly" (prompt/template files, within `post_ship_closure.md §5`'s write scope) from "fixes requiring a proper sprint story" (application code, scripts, anything outside that scope). A `scripts/*.py` fix was carried using language ("the next Post-Ship Closure should ... apply directly") that only actually holds for prompt/template-file fixes.

**Blast radius analysis:**
- What would have propagated: a 4th, 5th, ... consecutive closure re-deferring the same patch indefinitely, since no closure in this chain can actually apply it — the carry-forward mechanism silently degrades into a permanent no-op for this class of fix rather than surfacing that a different remediation path (a sprint story) is needed.
- When it would have surfaced: only when someone actually checked the write-scope rule against the deferred file's type, as this session did — otherwise indefinitely.
- Recovery cost if uncaught: low (the underlying script bug itself is low-severity — a false negative on drift detection, not a data-integrity issue) but the process-mechanism gap (indefinite silent re-deferral) is a structural issue worth correcting on its own terms.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `scripts/check_api_performance_baseline_drift.py`
  - Section: `find_missing_endpoints()`
  - Change required: Require table-row or dedicated-heading context (not bare whole-document substring match) for an endpoint to count as "documented" in `api_performance_baseline.md`. A working table-row-OR-heading-line heuristic was prototyped and verified this session (0 false positives against `POST /ai/check-daily-cost` and `POST /test/endpoints`, which are documented via dedicated `### METHOD /path` headings rather than table rows; 3 genuine gaps correctly surfaced: `GET /portfolio/pre-entry-validation`, `GET /trade-plans/tags`, `PATCH /notifications/preferences`) — full working regex available in this session's transcript for whoever picks up the story. Applying the fix will also require grandfathering those 3 newly-surfaced genuine gaps into `KNOWN_GAPS` (with a tracking comment, mirroring the original `BLG-OPS-61` precedent) so the stricter check does not immediately fail the next PR's CI run.
  - Owner: Infrastructure & Operations Owner
  - Target: Next sprint that can accept a proper `BLG-OPS-*` story for this script fix — **not** a future Post-Ship Closure's own STEP 8 (out of write scope; see root cause above). Recommend the PMO Lead file a `BLG-OPS-*` backlog item at the next `groom backlog` or `run roadmap` session with this friction item's file/section/change-required content copied verbatim, rather than continuing the closure-to-closure carry-forward for this specific item.

---

### Friction Item 3

**Classification:** Type A — Governance Drift

**Recurrence:** Not checkable in the strict sense (this is a finding *about* a recurrence-check, not a recurrence itself)

**What happened:** `2026-08-08__release-v8.5`'s own `lessons_learnt_closure.md` Recurrence Escalations table asserted the `execution_prompt.md` `test_scenarios` EPIC-level roll-up patch (`LL-v8.4-P4-01`) was "unapplied after 2 consecutive cycles." This cycle's Sprint Execution Phase 4 lessons-learnt record (`lessons_learnt_cycle.md`, filed 2026-08-12) independently found this claim was factually wrong at the time it was written: the patch had already shipped `2026-08-08` (`execution_prompt.md` v3.65→v3.66, the *same day* as `v8.5`'s own closure that later — on 2026-08-10 — filed the "still unapplied" claim), and confirmed via `prompt_change_log.md`. This closure cross-checked and confirms that finding: the patch is genuinely, verifiably applied; no further action is needed on the roll-up itself.

**Where in the routine:** STEP 8 — Lessons Learnt Review and Application (reviewing Release Planning's Carry-Forward #1, which had inherited the stale claim).

**Root cause:** `lessons_learnt_prompt.md §3.7`'s recurrence-check instruction ("confirm whether the corresponding prompt change was subsequently applied") does not specify *how* to search `prompt_change_log.md` — a date-range or filename-only search can miss an entry, producing a false-positive "still unapplied" recurrence claim that then propagates forward (this cycle's own Release Planning `lessons_learnt.md` Carry-Forward #1 inherited the stale claim from `v8.5`, one cycle removed from the original error).

**Blast radius analysis:**
- What would have propagated: continued false-positive recurrence claims for already-resolved patches, diluting the signal value of genuine recurrence escalations and wasting review effort re-confirming already-closed items.
- When it would have surfaced: this cycle, via the Sprint Execution Phase 4 lessons-learnt record's own independent cross-check — not systematically guaranteed to be caught every time.
- Recovery cost if uncaught: low (no functional harm — the underlying fix was genuinely applied) but a real process-integrity cost to trusting future recurrence-escalation claims at face value.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/lessons_learnt_prompt.md`
  - Section: §3.7 Cross-Cycle Recurrence Check
  - Change required: Specify searching `prompt_change_log.md` by the friction item's own patch-ID tag (e.g. `LL-v8.4-P4-01`), not by date range or filename alone, so a genuinely-applied patch is not re-flagged as an unresolved recurrence in a later cycle's record.
  - Owner: Head of Specs Team
  - Target: Next `lessons_learnt_prompt.md` revision touching §3.7 (already recorded as an outstanding deferred patch in this cycle's own `lessons_learnt_cycle.md` Phase 4 section — not duplicated as a new item, cross-referenced here for closure-level visibility).

---

### Friction Item 4

**Classification:** Type B — Semantic Mismatch

**Recurrence:** No

**What happened:** `delivery_verification_prompt.md §7` Deviation Severity Policy states P0–P3 hard-block/acceptance-recording requirements without an explicit carve-out for a deviation record filed with `Status: Resolved` — i.e. a retroactive record of an already-fixed defect, filed for traceability rather than to flag a current gap. This cycle's own delivery verification (`DEV-NAV-ST06-01`, a retroactively-filed P1 record for an already-shipped `v8.5` fix) had to infer, rather than read directly, that "Resolved" status exempts a P1 record from the hard-block requirement — flagged explicitly as a friction item in this cycle's `lessons_learnt_cycle.md` Phase 4 section.

**Where in the routine:** STEP 8 — Lessons Learnt Review and Application (reviewing Delivery Verification Phase 4 friction item 3).

**Root cause:** template omission — the severity policy table was written for the general case (an open deviation blocking the current sprint's merge) without an explicit carve-out for the already-resolved-retroactive-filing case, which this cycle demonstrated is a real, recurring shape of deviation record (this is the second cycle to file one — `v8.5`'s own `DEV-REPORTS-ST01-02` resolution pattern, and now `v8.6`'s `DEV-NAV-ST06-01`).

**Blast radius analysis:**
- What would have propagated: a differently-scoped verifying agent could reasonably read the table literally and treat a `Resolved`-status P1 record as an unresolved hard block, incorrectly halting verification or requiring a spurious PO+DoQ acceptance recording for a defect that was never actually open during this sprint.
- When it would have surfaced: the next cycle to file a retroactive `Resolved`-status deviation record of P0/P1/P2 priority, if a different (less experienced or less thorough) verifying pass took the table literally.
- Recovery cost if uncaught: low (a one-time process confusion, correctable in-session) but avoidable entirely with an explicit clause.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/delivery_verification_prompt.md`
  - Section: §7 Deviation Severity Policy
  - Change: Added an explicit Resolved-deviation carve-out — a deviation record filed with `Status: Resolved` is entered in the Deviation Register for traceability but does not trigger the P0–P3 hard-block/PO+DoQ acceptance-recording requirement, conditioned on the canonical spec's own Known Deviations entry actually stating `RESOLVED` with a resolution narrative (a bare P1 label with no resolution evidence still hard-blocks).
  - Version: 3.7 → 3.8
  - Confirmed by: Head of Specs Team (post-ship closure STEP 8 immediate-action rule)
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|----------------|---------------------------|--------------|
| `scripts/check_api_performance_baseline_drift.py`'s substring-based endpoint matching produces false negatives for endpoints mentioned in prose without adjacent measurement data or a dedicated heading. | `2026-08-07__release-v8.4` closure (Friction Item 1) | Require table-row/heading context, not bare substring match — deferred a 3rd consecutive time. This run additionally found the deferred-patch mechanism's own assumption (that a future Post-Ship Closure can apply this directly) is false for this file type — see Friction Item 2's full account. | Infrastructure & Operations Owner (fix) / Head of Specs Team (process-mechanism gap) |

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `docs/specs/Specs_Index.md` | §19.3, §36, new §39 | 2 stale `Status: Open` TSG entries reconciled to `RESOLVED`; full-sweep reconciliation note added | Header date only (not a numbered prompt) | Not applicable |
| `claude/system/delivery_verification_prompt.md` | §7 Deviation Severity Policy | Resolved-deviation carve-out added — a `Status: Resolved` deviation record no longer triggers the hard-block/acceptance-recording requirement | 3.7 → 3.8 | Yes |
| `docs/specs/frontend/pages/navigation.md` | `DEV-NAV-ST06-01` Known Deviations entry | Added missing `Canonical requirement` and `Target resolution release` fields (STEP 5 compliance fix, not a lessons-learnt action) | 1.6 (unchanged — deviation-note field completion, not a version-triggering content change) | Not applicable |
| `docs/specs/frontend/pages/analytics.md` | `DEV-EPIC02-ST03-01` Known Deviations entry | Added missing `Target resolution release` field (STEP 5 compliance fix, not a lessons-learnt action) | 2.1 (unchanged — deviation-note field completion) | Not applicable |

---

## New files created this run

- `claude/cycles/2026-08-11__release-v8.6/closure_state.json`
- `claude/cycles/2026-08-11__release-v8.6/lessons_learnt_closure.md` (this file)
- `claude/cycles/2026-08-11__release-v8.6/closure_record.md` (STEP 9, filed immediately after this record per the documented sequencing note)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `scripts/check_api_performance_baseline_drift.py` | `find_missing_endpoints()` | Require table-row/heading context, not bare substring match — see Friction Item 2 for a working prototype heuristic and the 3 genuine gaps it surfaces. | Infrastructure & Operations Owner | Next sprint accepting a `BLG-OPS-*` story for this script (not a future Post-Ship Closure — out of write scope) |
| `claude/system/lessons_learnt_prompt.md` | §3.7 Cross-Cycle Recurrence Check | Match deferred patches in `prompt_change_log.md` by patch-ID tag, not date/filename alone — see Friction Item 3. | Head of Specs Team | Next `lessons_learnt_prompt.md` revision touching §3.7 |
| `claude/system/execution_prompt.md` | §3.2.A | `test_scenarios` roll-up backstop should re-trigger when a story's `spec_references` is edited during in-EPIC remediation, not only once at initial EPIC seal (carried from this cycle's own `lessons_learnt_cycle.md` Phase 4 friction item 1a — cross-referenced, not duplicated). | Head of Specs Team | Next `execution_prompt.md` revision touching §3.2.A |
| `claude/system/execution_prompt.md` §5.3 or `qa_evidence_template.md` | DoQ sign-off protocol | Require explicit restatement of the final CI-green confirmation (run ID / `head_sha` match) when a story's PR needed a post-open CI-triggered fix — 2nd carry-forward from `v8.5` (carried from this cycle's own `lessons_learnt_cycle.md` Phase 4 friction item 2 — cross-referenced, not duplicated). | Head of Specs Team | Next `execution_prompt.md` §5.3 or `qa_evidence_template.md` revision |
| `claude/system/execution_prompt.md` §5.3 | Agent-Mediated Sign-Off protocol | A mandatory second, differently-scoped review pass (or an evidenced-not-just-asserted "I re-verified X" requirement) for any story making a quantitative/"already verified" claim — 3-occurrence-in-1-sprint pattern this cycle (ST-03, ST-11+ST-12, ST-24), carried from this cycle's own `lessons_learnt_cycle.md` Phase 3 friction item 2 (cross-referenced, not duplicated). | Head of Specs Team | Next `execution_prompt.md` revision touching §5.3 |

---

## Escalations

None. (The one candidate — the write-scope conflict on `scripts/check_api_performance_baseline_drift.py`, Friction Item 2 — has a clear owner and a concrete target (next sprint story) rather than an unresolved authority ambiguity, so it is recorded as a Recurrence Escalation / deferred patch, not an open Escalation requiring a 72-hour decision.)

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `scripts/check_api_performance_baseline_drift.py`'s substring-matching false-negative fix has now carried forward 3 consecutive cycles (`v8.4`→`v8.5`→`v8.6`) with no closure able to apply it directly (out of `post_ship_closure.md §5`'s write scope). | Do not carry this into a 4th Post-Ship Closure cycle unchanged — the PMO Lead should file a `BLG-OPS-*` sprint story for it directly (content in Friction Item 2 above) rather than relying on the closure-to-closure deferred-patch mechanism, which cannot resolve a script-level fix. | Release Planning / Roadmap |
| 2 | `reports.md`'s cross-cycle deviation register concentration signal is unchanged (still 2 of the register's records reference `reports.md`); the 3rd deviation consolidation review (STEP 5.1) is not yet due (2 of 3 cycles since the last run, `2026-08-08`). | No action needed next cycle either — re-check due at the 3rd cycle. | Delivery Verification / Post-Ship |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-08-11__release-v8.6",
  "phase": "Post-Ship",
  "filed_utc": "2026-08-12T14:15:00Z",
  "friction_item_count": 4,
  "action_now_count": 2,
  "deferred_count": 5,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
