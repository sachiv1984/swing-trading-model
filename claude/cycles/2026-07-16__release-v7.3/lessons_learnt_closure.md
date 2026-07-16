Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-16__release-v7.3
Release: v7.3
Last Updated: 2026-07-16
Authority: Post-Ship Closure Engine v2.17

---

# Lessons Learnt — Closure Summary: v7.3

Reviewed by: PMO Lead
Date filed: 2026-07-16
Prior cycle checked: claude/cycles/2026-07-15__release-v7.2/lessons_learnt_closure.md

## Classification Summary

| Count | Category |
|-------|----------|
| 1 | Immediate |
| 3 | Deferred (carried forward as Outstanding Action) |
| 0 | Escalated (new) |

---

## Action Classification Detail

### Immediate (1)

| ID | Source | Summary | File | Version | Prompt change log entry |
|----|--------|---------|------|---------|------------------------|
| Phase 4 Friction Item | lessons_learnt_cycle.md `## Phase 4` | `qa_evidence_EPIC-01.md` ST-02's evidence table tabulated AC-01/AC-02 only and silently dropped AC-03, rather than consolidating it with an explicit "Covers AC-03" note per the existing OA-3/ST-03 advisory. The AC was functionally addressed (confirmed via narrative + regression check) so it did not rise to a deviation, but the omission was silent rather than explicit. Applied now: `qa_evidence_template.md` OA-3/ST-03 Consolidation Block note elevated from advisory to a hard requirement — every AC in the backlog slice must now appear in the evidence table, either as its own row or explicitly named in a consolidated row's Evidence column. Delivery Verification's own write scope excludes `claude/system/templates/`, so this could not be applied at Phase 4 — applied here per the non-deferrable immediate-action rule. | `claude/system/templates/qa_evidence_template.md` | v1.6→v1.7 | Yes — appended to `claude/system/prompt_change_log.md` (2 rows: qa_evidence_template.md, OPERATIONAL_GUIDE.md v4.99→v4.100) |

### Deferred (3 — carried to next cycle or next relevant engine invocation)

| ID | Source | Summary | Owner | Target |
|----|--------|---------|-------|--------|
| Release Planning Friction Item 1 / Carry-Forward #1 | Release Planning lessons_learnt.md | `roadmap_prompt.md` STEP 8.1's Empty Now Horizon Gate condition 1 does not fire when the Now horizon holds committed items carried forward without a version label (as happened at `2026-07-15__release-v7.2` post-ship closure) — leaving no governed engine able to formally version-label the section. Resolved out-of-band this cycle under Head of Specs Team standing authority (DL-068); the structural gap itself is filed as `BLG-GOV-240` (P2) with two named remediation options, not yet actioned. | Head of Specs Team | Next available governance-hardening slot — next `roadmap_prompt.md` STEP 11 invocation, per the item's own backlog entry |
| Release Planning Carry-Forward #2 | Release Planning lessons_learnt.md | Capacity check landed at 13.25d midpoint / 15.5d pessimistic — a thinner buffer than v7.2's 10.5d/15.5d, with the same absolute pessimistic ceiling. This is the 3rd consecutive release-planning cycle to land close to the top of the capacity band (following the v7.1/v7.2 zero-buffer pattern already codified as LP-14 in `sprint_planning_prompt.md` v3.13). | Sprint Planning Engine | Next `plan sprint` invocation — treat any `### Phasing Recommendation` in `release_plan.md` as a live option early per the existing LP-14 requirement, rather than waiting for a formal capacity WARN that this PASS-band outcome would not trigger |
| Phase 3 Friction Item (4th recurrence of LL-v2.0-P3-5, new variant) | lessons_learnt_cycle.md `## Phase 3` | EPIC-02/03/04/05 branches were all cut from `main` before EPIC-01 (or each other) merged, since the merge gate halts on Product Owner acceptance — an always-human step. As each PR merged out-of-band between sessions, every later-cut sibling branch accumulated a conflict against `execution_state.json` (and twice against `base44_prompt_template_library.md`). All conflicts were resolved cleanly per `CLAUDE.md §8` with no work lost, but discovery was reactive — the user had to report a failed merge attempt before the engine acted. Two candidate fixes named (Head of Specs Team to evaluate): (a) CI-side sibling-PR "rebase recommended" comment on merge, or (b) a pre-PR-open STEP 3.2.B rebase check; recommend (a) as higher-leverage given this cycle's failure shape (all 4 PRs opened before any merged, so (b) alone would not have prevented it). | Head of Specs Team | Next `run sprint` invocation (any cycle) |

### Escalated (0 new)

None newly escalated this cycle. No deferred patch from this cycle has been carried 2+ cycles without a `prompt_change_log.md` entry — all three deferred items above are first-cycle carries or (for the Phase 3 item) a variant of a recurring pattern already tracked via its own named LL-ID rather than requiring a fresh escalation.

---

## Closure-Phase Observations

- Both `docs/product/scope/scope--2026-07-16__release-v7.3-dashboard-trade-plan-navigation-ux-continuation.md` and `docs/product/decisions/decisions--2026-07-16__release-v7.3.md` were cleanly located and marked Superseded — no "not found" flag needed this cycle.
- Backlog reconciliation (STEP 3): all 7 shipped ST items marked ✅ COMPLETE in `backlog.md` against their `execution_state.json` `merged` records (`BLG-FE-109` ST-01, `BLG-FE-110` ST-02, `BLG-FE-111` ST-03, `BLG-SPEC-91` ST-04, `BLG-SPEC-92` ST-05, `BLG-SPEC-93` ST-06, `BLG-SPEC-94` ST-07). Zero stale parked items (IMP-15 check) — matches `verification_report.md §5`'s own finding of zero `parked`-status items in the authoritative backlog slice. Zero Phase 4 additions required — `verification_report.md §2` confirmed 0 backlog entries added this run.
- Deviation compliance (STEP 5): N/A this cycle — `sprint_close.md` confirms zero deviations filed across all 7 stories.
- Specs Index (`docs/specs/Specs_Index.md`) STEP 7.3 TSG reconciliation resolved 3 stale "Open" entries found unrelated to this cycle's shipped scope but confirmed COMPLETE in `backlog_archive.md`: `TSG-v22-01`/`BLG-QA-01` (retired 2026-03-16), `TSG-V25-02`/`BLG-QA-07` (shipped v2.6), `TSG-v40-03`/`BLG-QA-29` (retired 2026-05-29, shipped v4.3) — all updated from "Open" to "RESOLVED". `TEST-GAP-EPIC-03-v33` (§19.3) left unchanged — no traceable standalone `BLG-`-prefixed backlog item exists for it, so the "if BLG item remains open, leave unchanged" fallback applies. §6.6 (`BLG-SPEC-72`) remains open, unchanged, out of scope. No new spec gaps surfaced (`verification_report.md §6` confirmed all EPIC-02–05 short-circuited to `not_applicable`, EPIC-01 fully covered).
- Endpoint coverage drift check (STEP 6): no drift — `api_performance_baseline.md` (102 measured endpoint rows) already covers more than `openapi.yaml`'s 88 method+path combinations; no new backend routes were added this cycle (confirmed in `sprint_close.md` Process Notes — EPIC-02 through EPIC-05 are documentation/spec-only, EPIC-01 is frontend-only plus one internal backend parameter change to an existing function, not a new route). No new top-level path prefix introduced, so `SystemStatus.js` `categorizeEndpoint()` requires no follow-up.
- Roadmap (STEP 2): v7.3 marked ✅ Complete for all 7 shipped items; the 4 named-but-unbuilt implementation items (`BLG-FE-115/116/117/118`) were annotated with their shipped-readiness-pass status and "ready for v7.4 scoping" note rather than left showing stale "named as anchor scope" language, since all 4 corresponding readiness passes (`BLG-SPEC-91/92/93/94`) shipped this same cycle, both §13 pre-checks (RISK-03, RISK-04) PASSED. `Next planned release` header reset to `[TBD]` — no formal v7.4 roadmap section exists yet (correctly deferred to next `plan release`, per Release Planning Friction Item 1 above, the exact structural gap this closure's own `Next planned release` write must not attempt to route around out-of-band a second time).
- Cross-EPIC merge conflicts across all 4 later-merging EPICs (PRs #1007, #1008, #1009) were resolved cleanly per `CLAUDE.md §8` with no work lost — see Phase 3 deferred item above for the reactive-discovery friction this produced.
- Release Planning Friction Item 2 (Type C, EPIC-grouping judgment call for the 3 ready UI items vs. the 4 readiness passes) was reviewed and confirmed advisory-only, consistent with v7.2's own disposition on the same friction type — no action filed, not treated as an outstanding item.

---

## Recurrence Escalations

None. The Phase 3 friction item is a 4th occurrence of the underlying LL-v2.0-P3-5 pattern (prior: v3.9, v6.8, v7.0) but is recorded as a distinct trigger-shape variant per its own Recurrence Notes (all branches cut and opened before any merge, rather than sequential single-session merges) — flagged for Head of Specs Team disposition on whether the existing LL-v2.0-P3-5 note needs a second clause, not an automatic escalation, since no prior-cycle outstanding action was left unresolved by this occurrence (v7.2's Phase 3 record had zero friction items). No deferred patch from this or the prior cycle has been carried 2+ cycles without a `prompt_change_log.md` entry.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-GOV-240` (STEP 8.1 empty-horizon gate structural gap) is filed and traceable but not yet resolved — a second occurrence of a non-empty-but-unversioned Now horizon would again have no governed write path. | Head of Specs Team to disposition at the next `roadmap_prompt.md` STEP 11 invocation — Apply now or Defer with owner + date. | Roadmap |
| 2 | Capacity check has landed close to the top of the band for 3 consecutive release-planning cycles (v7.1, v7.2, v7.3) despite the existing LP-14 Phasing Recommendation requirement. | Sprint Planning should treat this as a live, expected pattern rather than a one-off — confirm the Phasing Recommendation is being actively adopted/declined, not just acknowledged, at each planning cycle until the pattern breaks. | Sprint Planning |
| 3 | Cross-EPIC merge conflicts on shared files are still discovered reactively (via a failed human merge attempt reported back to the engine) whenever 2+ EPIC branches in a cycle are all opened as PRs before any has merged — 4th confirmed occurrence of this pattern, no work lost in any instance. | Until a CI-side sibling-PR notification or pre-PR-open rebase check lands (see deferred item above), expect a reactive round-trip per affected EPIC pair whenever a cycle has 2+ EPICs sharing `execution_state.json` or a common spec file. | Sprint Execution |

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-16__release-v7.3",
  "phase": "Post-Ship Closure",
  "status": "present",
  "generated_utc": "2026-07-16T22:45:00Z"
}
```
