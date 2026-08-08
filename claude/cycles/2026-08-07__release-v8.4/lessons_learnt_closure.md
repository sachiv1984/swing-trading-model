Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-08
Cycle: 2026-08-07__release-v8.4

# Lessons Learnt — Post-Ship Closure — v8.4

Feature / Trigger: Ship v8.4's user-facing reporting enhancements (Monthly P&L average-per-trade column; tax-year CSV trigger-source column) alongside a full-capacity slate of API contract & spec debt, backend hardening, frontend code health & security, operational reliability & cost monitoring, QA/test infrastructure, and governance-process integrity work across all 31 scoped stories.
Run: 2026-08-07__release-v8.4
Reviewed by: PMO Lead
Date filed: 2026-08-08
Prior cycle checked: 2026-08-05__release-v8.3

---

## What worked well

- All 31 shipped items reconciled cleanly against `execution_state.json` on the first pass — 0 returned items, 0 test scenario gaps, 0 stale parked items, 0 missing Phase 4 backlog references. STEP 3 (Backlog Reconciliation), STEP 4 (Scope/Decisions), and STEP 7 (Specs Index Review) all required no exception handling.
- STEP 8's lessons learnt review found two well-specified, unambiguous action items across the two source records (`lessons_learnt.md` Carry-Forward + `lessons_learnt_cycle.md` Phase 3/Phase 4 friction items) and both were applied immediately in a single bundled `execution_prompt.md` v3.65→v3.66 version bump, rather than deferred — the immediate-action rule worked as designed.
- The Carry-Forward item from Release Planning's own `lessons_learnt.md` (confirm `BLG-GOV-286`'s 4th gate-detection failure mode is genuinely covered before ST-29 is marked complete) was already independently resolved within-cycle by Sprint Execution — closure only needed to verify the resolution, not chase an open item.
- STEP 5.1's cadence-triggered Cross-Cycle Deviation Consolidation Review (3rd invocation since the last run, per its 3-cycle cadence) executed cleanly and, applying its own first run's Recommendation 2 (target-release-elapsed check) for the first time, surfaced one genuinely stale open deviation (`DEV-EPIC02-ST03-01`, target `v1.10` vs current `v8.4`) for Head of Specs Team re-triage — the recommendation from the first run proved directly actionable on its first application.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift (a canonical script's own methodology under-detects a real gap it was built to catch)

**Recurrence:** No — first observed this cycle; the script (`scripts/check_api_performance_baseline_drift.py`) has existed since v3.60/OA-2 (2026-07-24__release-v7.8) without this specific false-negative being caught before.

**What happened:** STEP 6's Endpoint Coverage Drift Check was run twice this session: first via an ad hoc path-normalised diff (produced 8 false positives — endpoints actually documented under query-string variants or distinct table rows the naive regex missed), then via the canonical `scripts/check_api_performance_baseline_drift.py` for a corrected result, which reported "PASSED — no new drift detected." Manual verification against the raw baseline document text found this to be a false negative: `GET /trade-plans/tags` is defined in `openapi.yaml` but has no actual measurement row (p50/p95/max) in `api_performance_baseline.md` — it is only *mentioned* once, in a prose cross-reference comparing it to its sibling `GET /watchlist/tags` ("...consistent with `GET /trade-plans/tags` (§ existing pattern)"). The script's matching logic (`e not in baseline_text`) is a bare substring check against the whole document — it treats any textual mention, including a passing comparative remark with no adjacent latency data, as equivalent to a genuine registration. Filed as `BLG-OPS-135`.

**Where in the routine:** STEP 6 — Operational Documents Reconciliation, Endpoint Coverage Drift Check (Advisory).

**Root cause:** Process gap — the canonical script's substring-based matching was designed to eliminate manual regex false positives (its own stated purpose, v3.60) but does not distinguish "endpoint string appears anywhere in the document" from "endpoint has an actual measurement row." A cross-reference sentence naming a sibling endpoint is enough to silence the check for that endpoint indefinitely.

**Blast radius analysis:**
- What would have propagated: `GET /trade-plans/tags` would remain permanently unmeasured and untracked — the canonical script reporting PASSED gives no future closure run a reason to look again, since the false negative is stable (the same cross-reference sentence will always satisfy the substring check).
- When it would have surfaced: never, absent a future session manually re-verifying the script's PASSED result against the raw document rather than trusting it — exactly what happened this run, but only because the STEP 6 advisory prescribes normalisation-aware comparison as a named step, prompting a second look.
- Recovery cost if uncaught: low (single endpoint, already filed as `BLG-OPS-135`) but the underlying methodology gap could silently mask a larger future gap the same way (any endpoint mentioned once in prose without a real table row).

**Process patch:**
→ Deferred patch (cannot apply this run — script logic, not this engine's governance-prompt write scope):
  - File: `scripts/check_api_performance_baseline_drift.py`
  - Section: `find_missing_endpoints()`
  - Change required: Require the endpoint string to appear specifically within a table-row context (e.g. line starts with `| <method> <path>` followed by numeric latency columns) rather than a bare substring match anywhere in the document text — closing the "mentioned in prose, not actually measured" false-negative class this run found.
  - Owner: Infrastructure & Operations Owner
  - Target: Next revision of `scripts/check_api_performance_baseline_drift.py`

---

### Friction Item 2

**Classification:** Type A — Governance Drift (this closure engine's own prompt cites a section reference that no longer matches the target document's structure)

**Recurrence:** Not checkable — `post_ship_closure.md` STEP 7.3 (AUD-2026-06-22-005) has not previously been flagged for this specific staleness in a reviewable lessons-learnt record.

**What happened:** STEP 7.3 instructs reconciling "each entry in §27 (Technical Specification Gaps) with status 'Open'" against backlog item completion. `docs/specs/Specs_Index.md`'s actual §27 is "Test Coverage Gaps — v5.0" (already fully Resolved) — no section in the current document is titled "Technical Specification Gaps." The document's numbering has grown by appending dated "Test Coverage Gaps — vX.Y" sections chronologically (§9, §19–§29+), so any earlier fixed section-number reference in `post_ship_closure.md` drifts stale as new sections are appended over time. The one genuinely `Open` TSG entry found this run (§19.3, `TSG-v33-03`) is tracked under a prose backlog reference (`TEST-GAP-EPIC-03-v33`) rather than a discrete `BLG-*` ID, so even locating it did not yield an actionable lookup per STEP 7.3's own instruction ("look up the corresponding BLG item ID").

**Where in the routine:** STEP 7 — Specs Index Review, sub-step 7.3 (TSG backlog reconciliation).

**Root cause:** Document staleness — a hardcoded section-number reference in a governance prompt, pointed at a target document whose section numbering is append-only and grows every cycle a new Test Coverage Gap section is filed.

**Blast radius analysis:**
- What would have propagated: STEP 7.3 silently finds nothing to reconcile every cycle (since §27 as currently numbered is already Resolved), giving a false impression the sub-step ran meaningfully when it in fact checked the wrong section.
- When it would have surfaced: only if a future reviewer manually diffs the prompt's instruction against the actual document structure, as happened this run.
- Recovery cost if uncaught: low-to-moderate — genuinely open TSG entries elsewhere in the document (like `TSG-v33-03`) continue to go unreconciled indefinitely, since no step in the routine currently searches the whole document for `Status: Open` TSG entries.

**Process patch:**
→ Deferred patch (cannot apply this run — modifying this engine's own governing prompt mid-execution is deferred to a future session for review, not self-patched in place):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 7.3
  - Change required: Replace the hardcoded "§27" reference with an instruction to scan the entire `Specs_Index.md` document for `Status: Open` (or equivalent) entries under any `TSG-*`-prefixed heading, and require each such entry to carry a discrete `BLG-*` backlog ID (flagging any that use a prose-only reference like `TEST-GAP-*` for Head of Specs Team to formalise) rather than naming a fixed section number.
  - Owner: Head of Specs Team
  - Target: Next `post_ship_closure.md` revision touching STEP 7

---

## Recurrence Escalations

None this cycle — Sprint Execution's own Phase 3 record confirms the prior cycle's 3rd-consecutive-recurrence escalation (backlog write-scope tension) was resolved this cycle (`execution_prompt.md` §7 + `CLAUDE.md` §2 sanctioned write path, v3.63/v3.64), and no new item in either source record met the 2+ cycle deferred-without-changelog-entry threshold.

---

## Process improvements actioned this run

- `claude/system/execution_prompt.md` v3.65→v3.66 — two immediate lessons-learnt actions applied in one bundled edit: (1) commit-SHA-write reminder added to the in-session credential/action provisioning sub-path (LL-v8.4-P3-01); (2) EPIC-level `test_scenarios` roll-up backstop added to STEP 3.1.A step 12 (LL-v8.4-P4-01). See STEP 8 consolidated action summary below and `claude/system/prompt_change_log.md`/`OPERATIONAL_GUIDE.md` §14 for the full governance-checklist trail.
- `docs/governance/deviation_consolidation_review_2026-08-08.md` produced (STEP 5.1, cadence-triggered) — second run of the cross-cycle `DEV-*` consolidation review, applying the first run's own Recommendation 2 (target-release-elapsed check) for the first time.

---

## New files created this run

- `claude/cycles/2026-08-07__release-v8.4/closure_state.json`
- `claude/cycles/2026-08-07__release-v8.4/lessons_learnt_closure.md` (this file)
- `claude/cycles/2026-08-07__release-v8.4/closure_record.md` (STEP 9, filed immediately after this record per the documented sequencing note)
- `docs/governance/deviation_consolidation_review_2026-08-08.md`

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `scripts/check_api_performance_baseline_drift.py` | `find_missing_endpoints()` | Require table-row context, not bare substring match, for an endpoint to count as "documented" — see Friction Item 1 | Infrastructure & Operations Owner | Next revision of the script |
| `claude/system/post_ship_closure.md` | STEP 7.3 | Replace hardcoded "§27" reference with a full-document scan for `Status: Open` TSG-prefixed entries — see Friction Item 2 | Head of Specs Team | Next `post_ship_closure.md` revision touching STEP 7 |
| `docs/specs/frontend/pages/analytics.md` | `DEV-EPIC02-ST03-01` entry | Re-triage the stale-target (`v1.10` vs current `v8.4`) Open deviation — accept client-side cohort computation as canonical (update §15's hard rule) or schedule the backend-migration fix — see `docs/governance/deviation_consolidation_review_2026-08-08.md` Finding 2 | Head of Specs Team | Before next `plan release` |
| `docs/specs/frontend/design_system.md` / `claude/system/execution_prompt.md` | Frontend-testing-gate | Carried from `v8.3` closure — close the environment-parity gap between sandboxed pre-merge review and real-CI Playwright execution for focus/interaction-timing ACs. No EPIC this cycle exercised a focus-restoration AC to test the `v8.3`-added sub-clause against, so recurrence remains unconfirmed either way | Base44 Frontend Prompt Owner | Next EPIC shipping a focus-restoration AC |

---

## Escalations

None this cycle.

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `scripts/check_api_performance_baseline_drift.py`'s substring-based matching produces a false negative for endpoints mentioned in prose without an actual measurement row (found this cycle: `GET /trade-plans/tags`). | The script's methodology should be hardened before it is trusted as sole authority for a future closure's STEP 6 advisory — see Friction Item 1. | Post-Ship Closure / Infrastructure & Operations Owner |
| 2 | `post_ship_closure.md` STEP 7.3's hardcoded "§27" reference has drifted from `Specs_Index.md`'s actual (append-only, chronologically-numbered) section structure. | The next `post_ship_closure.md` revision should replace the fixed reference with a full-document scan — see Friction Item 2. | Post-Ship Closure / Head of Specs Team |
| 3 | `DEV-EPIC02-ST03-01` is now confirmed, via the deviation consolidation review's new target-release-elapsed check, to be a genuinely neglected Open deviation (target `v1.10`, ~60+ releases stale). | Head of Specs Team should re-triage before the next `plan release` — see Outstanding deferred patches. | Release Planning / Head of Specs Team |
| 4 | `reports.md` now carries 2 of the 10-record cross-cycle deviation register (`DEV-REPORTS-ST06-01`, `DEV-REPORTS-ST01-02`) — a first light concentration signal on a single spec file, below the 3+ threshold that would warrant a dedicated audit. | The next (3rd) deviation consolidation review run should watch whether a 3rd `reports.md` deviation is filed before escalating to a dedicated audit. | Post-Ship Closure (next cadence-triggered run) |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-08-07__release-v8.4",
  "phase": "Post-Ship",
  "filed_utc": "2026-08-08T14:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 2,
  "deferred_count": 4,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
