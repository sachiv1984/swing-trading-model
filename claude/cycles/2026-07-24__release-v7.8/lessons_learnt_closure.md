Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Filed
Report Date: 2026-07-27
Cycle: 2026-07-24__release-v7.8

# Lessons Learnt — Post-Ship Closure — v7.8

Feature / Trigger: Ship all 12 v7.8 EPICs — the release/spend-visibility feature set and the engineering-hardening set
Run: 2026-07-24__release-v7.8
Reviewed by: PMO Lead
Date filed: 2026-07-27
Prior cycle checked: 2026-07-21__release-v7.7 (`lessons_learnt_closure.md`)

---

## What worked well

- STEP 4.1's "any flagged gap must have a `backlog.md` entry before the verification report is sealed" rule worked exactly as designed this cycle — the 3 documentation-completeness gaps ST-11 surfaced during pilot contract-test authoring were filed as `BLG-SPEC-102`/`103`/`104` before `verification_report.md` sealed, so this closure run found zero outstanding traceability gaps to reconcile at STEP 3.
- Backlog/roadmap/velocity reconciliation across all 12 shipped items completed cleanly on the first pass — no missing `backlog.md` entries, zero stale parked items, and `docs/System_status_report.md`'s v7.8 section required no correction beyond the routine status-line update already applied at Phase 4.
- Release Planning's own `lessons_learnt.md` Friction Item 1 (a real defect: `release_planning_prompt.md` STEP 9 literally instructed writing a `.claude_current_state.json.status` value that does not exist in `lifecycle_schema.json`'s canonical enum) was reviewed and fixed this run rather than left to accumulate — the fix was unambiguous once the friction item's own diagnosis was read carefully, closing a defect that could have stranded a future cycle at Design Gate's Lifecycle Guard.

---

## Friction Log

### Friction Item 1

**Classification:** Type C — Dependency Stall

**Recurrence:** Not checkable (no prior file) — this is STEP 1.5's first invocation since it shipped this same cycle (ST-02, EPIC-02, `BLG-FEAT-84`).

**What happened:** STEP 1.5 (Telegram Changelog Digest) could not execute in this sandbox. `python3 scripts/send_changelog_digest.py --version "v7.8"` (and the project-venv equivalent, `backend/.venv/bin/python3`) both failed at import time: `changelog_digest_service.py`'s import chain pulls in `backend/services/__init__.py`, which imports `position_service.py`, which imports `database.py`, which raises `ValueError: DATABASE_URL environment variable not set`. The script itself needs no database access — it only reads and regex-parses `docs/product/changelog.md` — but the package-level import graph forces a DB connection attempt regardless.

**Where in the routine:** STEP 1.5 (Telegram Changelog Digest).

**Root cause:** process gap / missing artefact — no `DATABASE_URL` is configured in this sandbox (consistent with other v7.8 findings noting "no production API credentials available in this checkout"), and the script's import path was not designed to be independent of the full `backend.services` package.

**Blast radius analysis:**
- What would have propagated: none directly — the hard rule in STEP 1.5 explicitly makes a failed send non-blocking, so closure proceeded correctly regardless.
- When it would have surfaced: only as a silent "PMO Lead expected a Telegram notification and never received one" if this sandbox's lack of `DATABASE_URL` turns out to be the norm rather than an isolated gap.
- Recovery cost if uncaught: low (single-file import-chain fix).

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `backend/services/changelog_digest_service.py` (and/or `scripts/send_changelog_digest.py`)
  - Section: import chain
  - Change required: decouple `changelog_digest_service.py`'s import path from `backend/services/__init__.py`'s full package import (which transitively requires a live `DATABASE_URL` via `position_service.py`/`database.py`) so the script can run standalone in a DB-less environment, since it performs no database access itself.
  - Owner: Head of Engineering
  - Target: next run of Sprint Execution touching `backend/services/changelog_digest_service.py`

---

### Friction Item 2

**Classification:** Type D — Cognitive Fatigue

**Recurrence:** Not checkable (no prior file records this level of STEP 6 methodology detail to compare against).

**What happened:** STEP 6's Endpoint Coverage Drift Check initially appeared to surface 30 (then, after normalising the two documents' differing path-parameter placeholder names, 15) endpoints present in `openapi.yaml` but absent from `docs/ops/api_performance_baseline.md`. Manual spot-checking showed these were not new drift at all — they are pre-existing gaps already tracked by the still-open `BLG-OPS-111` (filed at `2026-07-15__release-v7.2` post-ship closure), and the apparent gap count was inflated by `openapi.yaml` using specific parameter names (e.g. `{position_id}`, `{rule_id}`) while `api_performance_baseline.md` uses a generic `{id}` placeholder for the same routes.

**Where in the routine:** STEP 6 (Advisory — Endpoint Coverage Drift Check).

**Root cause:** template omission — the advisory's instructions say to count and compare `path:` entries but do not specify how to reconcile differing path-parameter placeholder naming between the two documents, which is exactly what produces false-positive gaps under a naive literal diff.

**Blast radius analysis:**
- What would have propagated: a duplicate/near-duplicate backlog item (e.g. a fresh "N endpoints missing" item) shadowing `BLG-OPS-111`, fragmenting tracking of the same underlying gap across two open items.
- When it would have surfaced: at a future backlog grooming pass reconciling overlapping `BLG-OPS-*` scope.
- Recovery cost if uncaught: low (a groom-backlog dedup pass would eventually catch it) but avoidable.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 6 — Advisory — Endpoint Coverage Drift Check
  - Change: added an explicit path-parameter-normalisation instruction before diffing the two endpoint lists, and a check for an existing open `BLG-OPS-*` tracking item covering the same gap class before filing a new one.
  - Version: 2.19 → 2.20
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

### Friction Item 3

**Classification:** Type A — Governance Drift (Release Planning `lessons_learnt.md` Friction Item 1, reviewed and closed at this closure run)

**Recurrence:** No — first occurrence of this specific STEP 9 status-value defect being reviewed and fixed (the underlying drift itself dates to whenever `lifecycle_schema.json` introduced the `Release_Planning_Complete` state without a corresponding `release_planning_prompt.md` STEP 9 update).

**What happened:** `release_planning_prompt.md` v2.42 STEP 9 instructed writing `.claude_current_state.json.status = Published` — a value absent from `lifecycle_schema.json`'s canonical state enum, which instead names the terminal state `Release_Planning_Complete`. Following the prompt literally at a future cycle would have stranded that cycle at Design Gate's next Lifecycle Guard check (unrecognised status → self-halt to `Blocked`). This cycle's own Release Planning session (`lessons_learnt.md` Friction Item 1) had already diagnosed the issue and worked around it correctly in-session (per `shared_standards.md` §10.6, `lifecycle_schema.json` prevails), flagging it `action-now` for "the next governance prompt maintenance pass."

**Where in the routine:** Release Planning STEP 9 (not this routine's own steps) — reviewed and actioned here per STEP 8's lessons-learnt review requirement.

**Root cause:** document staleness — `release_planning_prompt.md` STEP 9's literal status-value language was never updated when `lifecycle_schema.json` formalised `Release_Planning_Complete` as the canonical terminal-state name.

**Blast radius analysis:**
- What would have propagated: any future cycle that followed STEP 9 literally (rather than the in-session workaround this cycle applied) would have written an invalid `.claude_current_state.json.status`.
- When it would have surfaced: at Design Gate's next Lifecycle Guard check for that cycle.
- Recovery cost if uncaught: medium (cycle rework — manual status correction plus investigation of why Design Gate self-halted).

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/release_planning_prompt.md`
  - Section: STEP 9 — Global State Synchronization
  - Change: corrected the terminal `.claude_current_state.json` write from `status: Published` to `status: Release_Planning_Complete`, and added an explanatory note distinguishing this field from the unrelated cycle-level `state.json.status = Published` value.
  - Version: 2.42 → 2.43
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

## Recurrence Escalations

Carried forward unchanged from Sprint Execution's Phase 3 review (`lessons_learnt_cycle.md` `## Phase 3`, this cycle) — both are 2nd-consecutive-cycle recurrences with unresolved prior outstanding actions, already correctly escalated at source and not re-recorded as new friction items here per the mandatory rule:

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| `execution_state.json` cross-EPIC conflict pattern — every EPIC branch cut before sprint execution progresses on `main` accumulates an independently-diverging full copy of the shared state file, requiring a manual per-branch resolve pass at merge time (11/12 branches affected this cycle, up from 10/11 at v7.7) | 2026-07-21__release-v7.7 | Add an explicit "post-first-merge rebase" step at STEP 2 (Branch Preflight) or STEP 4 resolving this conflict class proactively per-branch instead of leaving it to a scramble at merge-gate time. Owner: Head of Specs Team. Target: next run of this routine (this cycle) — not applied. | Head of Specs Team |
| Endpoint-count (or any AST-derivable hardcoded constant) fallback collision across concurrently-open sibling PRs — independently-cut branches derive the same wrong value against different baselines, and `git merge` cannot detect the resulting semantic conflict when the literal text happens to match (recurred in the identical shape this cycle, EPIC-01/EPIC-06) | 2026-07-21__release-v7.7 | Flag any story hardcoding a value also derivable via an AST/script check, requiring re-derivation (not assumption) of that value at rebase time. Owner: Head of Engineering. Target: next run of this routine (this cycle) — not applied. | Head of Engineering |

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/release_planning_prompt.md` | STEP 9 | Corrected terminal `.claude_current_state.json` status write from `Published` to `Release_Planning_Complete`; added distinguishing note vs. cycle-level `state.json.status = Published` | 2.42 → 2.43 | Yes |
| `claude/system/post_ship_closure.md` | STEP 6 — Advisory — Endpoint Coverage Drift Check | Added path-parameter normalisation instruction and existing-tracking-item check before filing a new `BLG-OPS-*` drift item | 2.19 → 2.20 | Yes |
| `claude/backlog/backlog.md` (`BLG-FE-123`) | Item body | Extended scope to also cover the new `/changelog` `categorizeEndpoint()` gap (`src/pages/SystemStatus.js`) introduced this cycle by `GET /changelog/latest` (`BLG-FE-128`) | n/a (backlog item, not a governance prompt) | Not applicable |
| `docs/specs/Specs_Index.md` | §38 (new); document header | Added v7.8 Test Coverage Gaps section (1 row, `not_applicable`); bumped `Last Updated` | n/a (not a governance prompt) | Not applicable |

---

## New files created this run

None (`closure_state.json`, `closure_record.md`, and this file are standard STEP 0/STEP 9/STEP 8.5 outputs, not "improvement" artefacts).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `backend/services/changelog_digest_service.py` (and/or `scripts/send_changelog_digest.py`) | Import chain | Decouple from `backend/services/__init__.py`'s full package import (transitively requires live `DATABASE_URL`) so the digest script can run standalone in a DB-less sandbox | Head of Engineering | next run of Sprint Execution touching this file |
| `.claude_current_state.json` schema / owning-engine documentation | `next_release` field | Confirm which engine's prompt owns `next_release` maintenance (candidates: Release Planning STEP 9, or `sync gh`'s own read of it per CLAUDE.md §4) and make that ownership explicit in the owning prompt — field was found 4 releases stale (stamped `v7.4`) at the start of this cycle's Release Planning session, with no engine explicitly owning its upkeep | Head of Specs Team | next governance prompt maintenance pass |
| `claude/system/execution_prompt.md` | §3.2.B (LL-v7.6-P3-01) | Convert the API performance baseline pre-PR check from prose advisory to an enforced pre-commit/pre-PR-open script step — the advisory has now failed to prevent this exact class of miss twice (v7.6/EPIC-07, v7.8/EPIC-06) | Head of Specs Team | next run of this routine (Sprint Execution) |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `execution_state.json` cross-EPIC conflict pattern (recurrence, 2nd consecutive cycle) | Recurrence | Head of Specs Team | Prior cycle's deferred structural fix (proactive per-branch rebase step at STEP 2/4) was never applied; the friction recurred at greater scale this cycle (11/12 branches vs 10/11 at v7.7). Decision needed: apply the deferred structural fix, or explicitly accept the manual-resolve cost as a standing cost of this sprint's multi-EPIC-parallel-branch model. 72-hour deadline: 2026-07-30. |
| Endpoint-count/hardcoded-constant fallback collision (recurrence, 2nd consecutive cycle) | Recurrence | Head of Engineering | Prior cycle's deferred structural fix (flag AST-derivable hardcoded values for mandatory re-derivation at rebase time) was never applied; the friction recurred in the identical shape this cycle. Decision needed: apply the deferred fix, or accept the recurring risk. 72-hour deadline: 2026-07-30. |
| Whether agent-mediated "acting as Product Owner"/"acting as Director of Quality" PR review comments should be disallowed entirely, and if permitted, under what labeling convention | Authority ambiguity (carried forward, unruled — 2nd cycle) | Head of Specs Team | v7.7's Phase 3 friction item raised this and was never formally ruled on; this cycle worked around the specific risk via an explicit owner-confirmed labeling convention (agent-mediated, sign-off fields left blank for human completion) rather than a codified rule. Decision needed: codify this session-level practice as a formal rule, or reject it. 72-hour deadline: 2026-07-30. |

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Two consecutive cycles (v7.7, v7.8) have now hit the same `execution_state.json` cross-EPIC conflict pattern with no structural fix applied between them — the cost scaled up (11/12 branches this cycle vs 10/11 last cycle) rather than down. | Sprint Execution should not proceed past a third occurrence of this exact recurrence without either applying the deferred STEP 2/4 fix or explicitly re-confirming with Head of Specs Team that the manual-resolve cost is accepted as a standing cost of this sprint's multi-EPIC-parallel-branch model. | Sprint Execution |
| 2 | This cycle's largest real defects (WhatsNewCard double-unwrap bug, EPIC-06's test-isolation bug, the endpoint-count collision, the missing API performance baseline registration) were all caught by *actually executing* tests/CI rather than by reading code or trusting "written but not yet run" disclaimers. | Sprint Execution should continue treating "get real test execution working, even under a constrained sandbox" as higher-value than accepting untested-but-plausible sign-off language. | Sprint Execution |
| 3 | This closure run's own STEP 6 advisory check (endpoint coverage drift) had a latent false-positive risk (path-parameter naming mismatch) that has presumably affected every prior cycle's STEP 6 run silently — this is the first time it was caught and fixed, only because the apparent gap count (30, then 15) was large enough to prompt manual verification rather than being accepted at face value. | Post-Ship Closure should treat any STEP 6 gap count as a hypothesis to verify (spot-check a sample against the actual document text) before filing a backlog item, not just a number to act on directly. | Post-Ship Closure |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-07-24__release-v7.8",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-07-27T13:15:00Z",
  "friction_item_count": 3,
  "action_now_count": 2,
  "deferred_count": 3,
  "escalation_count": 3,
  "carry_forward_count": 3,
  "status": "Complete"
}
```
