**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-08-03
**Filed:** 2026-08-03
**Cycle:** 2026-08-03__release-v8.1 (ST-12, EPIC-04, BLG-QA-129)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — First Run

## Objective

`ST-12`'s acceptance criteria call for a periodic review that consolidates `DEV-*` deviation records across recent cycles into one place, to surface recurring patterns that a single-cycle view would miss. This is the first run of that review. Going forward, re-run this review periodically (recommended: alongside `groom backlog` or post-ship closure) and file a new dated copy (`deviation_consolidation_review_<date>.md`), cross-referencing the prior one.

## Method

Scanned every canonical spec file, QA evidence log, and verification report under `docs/` and `claude/cycles/` for `## DEV-*` / `### DEV-*` headings (the `Known Deviations` section convention, LL-v3.4-P3-04). 9 distinct deviation records found (one, `DEV-ST14-01`, has entries in two files — see Finding 3).

## Consolidated Register

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-EPIC02-ST04-01 | `frontend/pages/notifications.md` | P3 | Resolved (v2.3) | v2.3 |
| DEV-EPIC02-ST03-01 | `frontend/pages/analytics.md` | P2 | Open | v1.10 (stale — see Finding 2) |
| DEV-ST04-01 | `api_contracts/alerts_endpoints.md` | P2 | Accepted (PO + DoQ, 2026-03-20) | v2.2, pending paid infra |
| DEV-EPIC01-ST05-01 | `frontend/pages/positions.md` | P2 | Resolved (v7.1) | v7.1 |
| DEV-EPIC02-ST05-03 | `frontend/pages/positions.md` | P2 | Resolved (v2.4) | v2.4 |
| DEV-REPORTS-ST06-01 | `frontend/pages/reports.md` | P3 | Open | TBD — not yet scheduled |
| DEV-ST14-01 | `frontend/pages/trade_history.md` + `docs/testing/slippage_scenarios.md` | P3 | Resolved (v2.5) per testing doc; **canonical spec not updated** | v2.5 |
| DEV-EPIC04-ST09-01 | `api_contracts/ticker_universe_api_contract.md` | P3 | Resolved (same release) | v3.8 |
| DEV-v51-EPIC01-01 | `product/decisions/si05-telegram-message-format-spec.md` | P3 | Resolved (v5.2) | v5.2 |

## Findings

**Finding 1 — Priority skew:** 5 of 9 (56%) are P2; 4 of 9 (44%) are P3. No P0/P1 deviations found in the current register — consistent with the general pattern that behavioural deviations discovered post-ship tend to be lower-severity (P0/P1 gaps are more likely caught before merge by the merge-gate's "no unresolved P0 deviations" hard condition).

**Finding 2 — Stale target release, no re-derivation step exists:** `DEV-EPIC02-ST03-01` (Cohort Analysis client-side computation) still names `Target resolution release: v1.10` as its target, but the codebase is now at v8.1 — roughly 60 releases past its named target with no update. There is currently no periodic mechanism that re-checks whether an open deviation's `Target resolution release` has elapsed and flags it for re-triage (accept as permanent, re-target, or resolve). This review is itself evidence of the gap this recurring review is meant to close — **recommend this becomes a checked field in future runs of this review** (see Recommendations).

**Finding 3 — Spec/QA-doc resolution-status drift (the clearest recurring pattern found):** `DEV-ST14-01` is resolved according to `docs/testing/slippage_scenarios.md` (explicit `Status: RESOLVED — v2.5`, resolution detail, two follow-up commits named), but its sibling entry in the canonical spec `docs/specs/frontend/pages/trade_history.md` was never updated — it still reads `Target resolution release: v2.5 *(originally v2.2; not resolved in v2.2, v2.3, or v2.4...)*` with no resolution note at all, even though v2.5 has long since shipped. This is a real, confirmed instance of the class of gap `LL-v3.4-P3-04`'s "Known Deviations section" convention was meant to prevent — the deviation *was* tracked to resolution, but only in one of its two homes. **This is the recurring pattern this review surfaces**: a deviation resolved via a QA/testing artefact does not automatically propagate its resolved status back to the canonical spec's own Known Deviations entry, because no step in any governed routine currently re-visits a spec's existing DEV-* entries once filed — the STEP 3.1.A deviation-check flow only checks for *new* deviations against current work, not the resolution status of *pre-existing* ones in a spec being touched.

**Finding 4 — No recurring category concentration:** Deviations span frontend visual/copy (2), frontend column/layout (2), backend computation-layer (1), backend delivery-channel infrastructure-constraint (1), navigation/routing (1), analytics computation-method (1), and data-freshness/staleness framing (1) — no single spec file or component has 3+ deviations, so this run does not surface a "same file keeps deviating" hotspot. Re-run this review over a longer window (more cycles) before concluding this absence is stable.

## Recommendations

1. **Close Finding 3 directly:** Update `docs/specs/frontend/pages/trade_history.md`'s `DEV-ST14-01` entry to reflect the resolution already recorded in `docs/testing/slippage_scenarios.md` (done in the same commit as this review — see below).
2. **For the next run of this review:** add a "target-release-elapsed" check — for every `Open`/`Accepted` deviation, compare its named target release against the current release; flag any that are more than 2 releases stale for Head of Specs Team re-triage.
3. **Structural fix candidate (not implemented here — recommend filing as a backlog item):** when a deviation is resolved via a QA evidence log or test-scenario doc rather than directly in the canonical spec, the resolving commit should be required to also update the canonical spec's own `DEV-*` entry in the same commit — mirroring the existing `deviations_filed` atomic-write discipline (`execution_prompt.md` §3.1.A step 10a) but for *closing* a deviation, not just filing one.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-03
- Comments: First consolidation review performed per ST-12's AC. 9 deviation records catalogued; one confirmed resolution-status drift found and corrected in the same commit (Finding 3 / Recommendation 1). Recommendations 2–3 are scoped for the next review run and a follow-up backlog item respectively, not implemented in this pass.
