Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Filed
Report Date: 2026-07-28
Cycle: 2026-07-27__release-v7.9

# Lessons Learnt — Post-Ship Closure — v7.9

Feature / Trigger: Ship all 15 v7.9 EPICs — the two P1 UX anchors and the 13 capacity-fill engineering-hardening items
Run: 2026-07-27__release-v7.9
Reviewed by: PMO Lead
Date filed: 2026-07-28
Prior cycle checked: 2026-07-24__release-v7.8 (`lessons_learnt_closure.md`)

---

## What worked well

- STEP 3 backlog reconciliation completed cleanly on the first pass across all 15 shipped items — no missing `backlog.md` entries, zero stale parked items, and the one Phase 4 addition (`BLG-GOV-264`) was already present pre-closure per `verification_report.md §5(a)`, requiring no new filing.
- Release Planning's own `lessons_learnt.md` Friction Item 1 (the `BLG-FE-128` stale pull-forward-candidate reference) was reviewed and actioned this run rather than left deferred a further cycle — `roadmap_prompt.md` gained an explicit candidate live-status cross-check, closing the gap before it could recur at a future rebalance.
- All three deferred patches and all three formal escalations recorded in `2026-07-24__release-v7.8`'s own `lessons_learnt_closure.md` were confirmed resolved (via `prompt_change_log.md` entries 4.111–4.114, all dated within that same closure session, well inside their 2026-07-30 deadlines) — cross-cycle recurrence check found nothing outstanding to escalate this cycle.
- STEP 6's Endpoint Coverage Drift Check followed v7.8's own Carry-Forward guidance ("treat any STEP 6 gap count as a hypothesis to verify") — the diff was computed programmatically with path-parameter normalisation and cross-checked against `backlog.md` for an existing open tracking item before considering any new filing, surfacing a genuine (if minor) staleness gap rather than either a false positive or a silent miss.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** No (first occurrence of this specific sub-pattern; a different Endpoint Coverage Drift Check gap — path-parameter normalisation — was found and fixed at `2026-07-24__release-v7.8`, but this is a distinct issue about the referenced tracking item's own list going stale over time, not the normalisation logic itself).

**What happened:** STEP 6's Endpoint Coverage Drift Check found 25 method+path combinations in `openapi.yaml` (after path-parameter normalisation) with no corresponding row in `docs/ops/api_performance_baseline.md` — up from the 21 endpoints originally named when `BLG-OPS-111` was filed at `2026-07-15__release-v7.2` post-ship closure. Four endpoints have accumulated since then that are not reflected in `BLG-OPS-111`'s own endpoint list: `PATCH /watchlist/{entry_id}` (new this cycle, EPIC-01), `PATCH /notifications/preferences`, `POST /alerts/rules`, `POST /settings`. The existing-tracking-item check (added at v7.8, v2.20) correctly found and referenced `BLG-OPS-111` rather than filing a duplicate, but had no instruction to flag that the item's own list had drifted stale relative to the current gap.

**Where in the routine:** STEP 6 — Advisory Endpoint Coverage Drift Check.

**Root cause:** template omission — the "reference the existing item" instruction (v2.20) checks for an existing open tracking item but does not instruct recording whether new drift has accumulated since that item was filed, so the tracking item silently understates the true gap over successive cycles.

**Blast radius analysis:**
- What would have propagated: `BLG-OPS-111`'s acceptance criteria ("all 21 endpoints have p50/p95 latency entries") would eventually be satisfied and the item closed without covering the 4 endpoints that accumulated afterward — a false sense of completeness.
- When it would have surfaced: whenever `BLG-OPS-111` is eventually actioned and someone re-diffs against the then-current `openapi.yaml`.
- Recovery cost if uncaught: low (a future STEP 6 run would eventually re-surface the residual gap) but avoidable.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 6 — Advisory — Endpoint Coverage Drift Check
  - Change: when referencing an existing open tracking item instead of filing a duplicate, and the current gap has grown beyond that item's own recorded list, record the delta explicitly in the closure record and Advisory Summary rather than silently reusing the reference.
  - Version: 2.20 → 2.21
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

## Recurrence Escalations

None. Cross-cycle check against `2026-07-24__release-v7.8`'s `lessons_learnt_closure.md` (3 deferred patches, 3 escalations, all with a 2026-07-30 deadline) found all six items already resolved and logged (`prompt_change_log.md` entries 4.111, 4.112, 4.113, 4.114 — all dated 2026-07-27, within that same closure session, before their deadlines). No item required re-escalation this cycle.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/roadmap_prompt.md` | Candidate gate verification block (after LP-05) | Added a "Candidate live-status cross-check" — before naming a pull-forward candidate, confirm it is still open in `backlog.md` (not archived/shipped in the same session's own `groom backlog`/post-ship-closure output). Resolves Release Planning `lessons_learnt.md` (`2026-07-27__release-v7.9`) Friction Item 1. | 9.6 → 9.7 | Yes |
| `claude/system/post_ship_closure.md` | STEP 6 — Advisory — Endpoint Coverage Drift Check | Added a stale-tracking-item delta note — see Friction Item 1 above. | 2.20 → 2.21 | Yes |

---

## New files created this run

None (`closure_state.json`, `closure_record.md`, and this file are standard STEP 0/STEP 9/STEP 8.5 outputs, not "improvement" artefacts).

---

## Outstanding deferred patches

None.

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-OPS-111` (endpoint coverage drift tracking item, filed v7.2) now covers 21 of the 25 endpoints currently missing from `api_performance_baseline.md` — a 4-endpoint delta has accumulated across v7.3–v7.9 with no update to the item's own list. | Whichever engine next actions `BLG-OPS-111` (or a future STEP 6 run) should reconcile its endpoint list against the then-current `openapi.yaml` gap before treating it as complete, not just against its originally-filed list. | Post-Ship Closure |
| 2 | `BLG-FEAT-73`/`BLG-FEAT-74` remain parked (perennial-return, Option (b)) with the SI-02 live-gate re-check still blocked on credential availability; `BLG-OPS-121` (this cycle's own scope — staging credential provisioning) resolved the underlying credential gap on 2026-07-28 (`ESC-EXEC-20260727-01`). | The next `plan release`/roadmap rebalance should attempt a genuine live SI-02 re-check using the newly-provisioned credential rather than citing the unchanged 2026-07-17 structured field a further time. | Roadmap Rebalance |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-07-27__release-v7.9",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-07-28T15:35:00Z",
  "friction_item_count": 1,
  "action_now_count": 2,
  "deferred_count": 0,
  "escalation_count": 0,
  "carry_forward_count": 2,
  "status": "Complete"
}
```
