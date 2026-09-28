Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-28
Cycle: 2026-09-23__release-v9.7

---

# Post-Ship Closure Record — 2026-09-23__release-v9.7

## §1 — Closure Status

```
Status: Closed_with_actions
Release: v9.7 — PO-05 Replay Mode & Full-Capacity Debt Clearance
Ship date: 2026-09-25
Cycle: 2026-09-23__release-v9.7
Verification status: Verified_with_deviations
Backlog slice source: claude/cycles/2026-09-23__release-v9.7/stage4_backlog_slice.md (original — amended_backlog_slice_path absent/empty; cross-referenced against execution_state.json.backlog_slice_source, which agrees)
Closure run: 2026-09-28T00:00:00Z
```

## §2 — Documents Updated

| Step | Document | Action | Status |
|------|----------|--------|--------|
| 1 | docs/product/changelog.md | v9.7 entry written (7 EPICs, 2 P4 deviations, 28 tech backlog items classified U/G/D) | ✅ |
| 1.5 | Telegram changelog digest | Attempted via `scripts/send_changelog_digest.py --version v9.7`; `sent: false` (Telegram credentials not configured in this environment) — non-blocking per hard rule | ✅ (attempted) |
| 2 | claude/roadmap/current_roadmap.md | v9.7 marked ✅ Complete (shipped 2026-09-25); §1 headers updated (Current Version → v9.7, Next planned release → [TBD]); §8 release summary table row added | ✅ |
| 3 | claude/backlog/backlog.md | 29 items marked ✅ COMPLETE (31 ST entries via ST-01a/b/c phasing); 0 Phase 4 additions required (all already filed during execution/review); 0 stale parked items; 1 new item added (BLG-FE-191, STEP 6 finding) | ✅ |
| 4 | Scope document / Decisions record | Both superseded — `scope--2026-09-23__release-v9.7-replay-mode-and-capacity-clearance.md`, `decisions--2026-09-23__release-v9.7.md` | ✅ |
| 5 | Canonical specs (deviation compliance) | 2 P4 deviations checked (`DEV-v9.7-ST05-01`, `DEV-v9.7-ST04-01`), both fully field-compliant, no corrections needed; STEP 5.1 cross-cycle consolidation review (6th run, cadence-due) found and fixed 1 further compliance gap (`ai_endpoints.md` stale "None at v1.10" summary) | ✅ |
| 6 | Operational docs | System_status_report.md confirmed accurate (already reconciled at delivery verification); validation_system.md — no stale references found; velocity_metrics.md — v9.7 row appended (31/31, 1.00), rolling average advanced to v9.2–v9.7; endpoint coverage drift — 0 gap (147 normalised endpoints, new `POST /replay/run` already registered same-PR); `SystemStatus.js` `/replay` categorisation gap flagged, filed as `BLG-FE-191` | ✅ |
| 7 | Specs Index | §6/§7: 0 open items to resolve (all already Resolved), 0 new gaps to add (verification confirmed 0 genuine coverage gaps). §47 Test Coverage Gaps — v9.7 section added (0 new gaps requiring a backlog item). **STEP 7.3 full-document sweep: 26 Open TSG entries checked, 0 resolved** (all already carry a terminal disposition). | ✅ |
| 8 | Lessons Learnt Review | All records reviewed (Release Planning `lessons_learnt.md`, Phase 3+4 `lessons_learnt_cycle.md`). 1 immediate action applied (release_planning_prompt.md v2.55→v2.56); 3 deferred; 2 escalated (mandatory recurrence + governance-scope ruling) | ✅ |
| 8.5 | lessons_learnt_closure.md | Created | ✅ |

## §3 — Backlog Additions This Run

- `BLG-FE-191` — SystemStatus.js `categorizeEndpoint()` has no case for the new `/replay` prefix (P4). Filed at STEP 6 (Endpoint Coverage Drift Check advisory finding).

No Phase 4 (returned-items / P2-P3-deviation / test-scenario-gap) additions were required — `verification_report.md` §2 confirmed all relevant backlog references (`BLG-SPEC-164/165/166/167/169/170`, `BLG-QA-192/194/196`, `BLG-GOV-349`) were already filed during execution and independent review.

## §4 — Deviation Compliance Summary

2 deviations filed this sprint (both P4): `DEV-v9.7-ST05-01` (`notifications.md`), `DEV-v9.7-ST04-01` (`reports.md`). Both checked against the Known Deviation Standard's 6 required fields (Description, Canonical requirement, Priority, Target resolution release, Owner, Backlog reference) — all present and complete at filing; no corrections needed.

All now compliant: **Yes**.

Additionally (STEP 5.1, 6th cross-cycle consolidation review, cadence-due — 3rd invocation since the 5th run): 1 further, pre-existing compliance gap found and fixed in this closure — `docs/specs/api_contracts/ai_endpoints.md`'s `## Known Deviations` section read a stale "None at v1.10." despite an already-disclosed, already-dispositioned `BLG-BE-128` won't-fix deviation (documented only in the Changelog table and an inline note, from `2026-09-21__release-v9.6`). Corrected: added `DEV-v9.7-ST13-01` with full required fields. A second gap of the same class (`BLG-BE-127`, P2, fee-rounding, no canonical-spec Known Deviations entry at all) was identified but **not** remediated — the nearest candidate canonical spec (`claude/strategy/strategy_rules.md`) is sealed to this routine's write scope, and the correct owning spec was not confirmed within this closure's time budget. Recorded as an Outstanding Action (§6, row 3).

## §5 — Lessons Learnt Action Summary

All records reviewed: Release Planning (`lessons_learnt.md`, 4 friction items), Phase 3 + Phase 4 (`lessons_learnt_cycle.md`).

**Immediate (1):**
- Release Planning Friction Item 1 — `scripts/scan_backlog_gate_conditions.py` + `release_planning_prompt.md` §1.3a widened to detect an "already-resolved banner" (`**Resolution (...):**`/`**Resolved (...):**`) independent of gated status, closing the gap that let `BLG-FE-189` slip through this cycle's own release-planning selection. `release_planning_prompt.md` v2.55→v2.56; `OPERATIONAL_GUIDE.md` v4.206→v4.207; `prompt_change_log.md` and `changelogs/release_planning_changelog.md` both updated per the CLAUDE.md §6 checklist.

**Deferred (3):**
- Release Planning Friction Item 2 — `workforce_capacity.md` VH effort-band table row; not actionable until a 2nd real VH-effort item is scored. Owner: Head of Specs Team.
- `execution_prompt.md` STEP 3.1/§3.1.D — broaden the delegated-item-resolution write to also sync `open_escalations`/`completed_items`/`blocked_items` in the same commit. 1st carry (raised this cycle). Owner: Head of Specs Team.
- `execution_prompt.md` §3.2.A — mandate the fully-qualified agent-mediated signer label whenever the reviewer is not the literal human role-holder (EPIC-04/EPIC-07 signer-label ambiguity finding). 1st cycle. Owner: Head of Specs Team.

**Escalated for decision (2):**
- `execution_prompt.md` §3.2.A same-EPIC cross-story testing-gap disclosure consistency check — 3rd consecutive cycle carried unapplied, crosses the `lessons_learnt_prompt.md §3.7` mandatory 2-cycle recurrence-escalation threshold. `ESC-CLOSE-20260928-01`, Head of Specs Team, SLA 2026-10-01.
- Release Planning Friction Item 3 — `release_planning_prompt.md §-1.2` Option(b) rebalance-equivalence precedent-reuse ruling. `ESC-CLOSE-20260928-02`, Head of Specs Team, SLA 2026-10-01.

## §6 — Outstanding Actions

| # | Description | Owner | Deadline | Escalation path | Resolution |
|---|-------------|-------|----------|-----------------|------------|
| 1 | `execution_prompt.md §3.2.A` same-EPIC testing-gap consistency check — ruling needed (implement or retire). | Head of Specs Team | 2026-10-01 | `ESC-CLOSE-20260928-01` | *(open)* |
| 2 | `release_planning_prompt.md §-1.2` Option(b) precedent-reuse ruling. | Head of Specs Team | 2026-10-01 | `ESC-CLOSE-20260928-02` | *(open)* |
| 3 | `BLG-BE-127` (P2, fee-rounding float→Decimal deviation) has no canonical-spec Known Deviations entry — confirm the correct owning spec (candidate: a backend fee/calculations spec; `strategy_rules.md` is sealed to this routine) and add the entry. | Backend Engineering Patterns Owner | Before next release plan opens | — | *(open)* |
| 4 | `execution_prompt.md` STEP 3.1/§3.1.D `open_escalations`/`completed_items`/`blocked_items` sync gap — 1st carry, watch for a 2nd unresolved carry at `v9.8` (would cross the automatic-escalation threshold). | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 3.1/3.1.D | — | *(open)* |
| 5 | File a `BLG-GOV-*` item requiring every new `## Known Deviations` entry to carry a `DEV-<id>` from the point of filing (6th consolidation review Finding 1 — recommended at the 1st, 5th, and 6th review runs, still unfiled). | Head of Specs Team | Next `groom backlog` or Post-Ship Closure pass | — | *(open)* |
| 6 | `workforce_capacity.md` — add a `VH` effort-band row once a 2nd real `VH`-effort item is scored. | Head of Specs Team | Once a 2nd VH item is scored | — | *(open)* |
| 7 | `execution_prompt.md §3.2.A` — mandate the fully-qualified agent-mediated signer label format (EPIC-04/EPIC-07 signer-label ambiguity finding). | Head of Specs Team | Next `execution_prompt.md` revision touching §3.2.A | — | *(open)* |

## §7 — Closure Confirmation

```
Post-ship closure complete — 2026-09-23__release-v9.7 — 2026-09-28
Release: v9.7 — PO-05 Replay Mode & Full-Capacity Debt Clearance
Verification status: Verified_with_deviations
Lessons learnt applied: 1 immediate | 3 deferred | 2 escalated
Outstanding actions carried forward: 7 (see §6)
Next cycle may now open.
```
