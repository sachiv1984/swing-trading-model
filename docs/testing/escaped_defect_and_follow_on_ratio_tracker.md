**Owner:** Director of Quality; PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-29 (ST-13, BLG-QA-182, EPIC-03, v9.8 — initial creation, v9.5 baseline computed)
**Source:** ST-13 (BLG-QA-182, EPIC-03, v9.8 sprint execution)

---

# Escaped-Defect and Follow-On-Ratio Tracking

## Purpose

v9.5 filed 21 follow-on backlog items during execution and two PR review rounds (~0.49 per shipped story), several found only by review — but nothing separated a genuine **escaped defect** (a bug in already-merged work, first observed after that merge) from **planned debt** (a follow-on item that documents a deliberately deferred scope, spec gap, or improvement, not a defect in what shipped). Both categories currently land in the same "Phase 4 follow-on items" count at post-ship closure, so a rising follow-on count could mean either "quality is slipping" or "the team is disclosing scope decisions well" — this tracker makes the two visible separately, cycle over cycle.

## Definitions

- **Shipped stories:** count of `ST-xx` items with `status: done` (or `merged`) in the cycle's `execution_state.json` at closure.
- **Follow-on items filed:** count of new `BLG-*` backlog items whose `**Source:**` line traces to the cycle, filed during execution or PR review (per `execution_prompt.md` §7's out-of-scope-finding exception) — regardless of whether they document a defect or planned debt. Read from the cycle's `closure_record.md` STEP 3 backlog-reconciliation row.
- **Follow-on ratio:** Follow-on items filed ÷ Shipped stories.
- **Escaped defects:** the subset of follow-on items (or separately-filed `DEV-*` deviation records) that describe a **defect in already-merged code** — i.e. the shipped implementation does not do what its own acceptance criteria said — first observed after that story's PR merged, as opposed to a scope gap, spec-debt item, or deliberately deferred enhancement. Sourced from the cycle's `closure_record.md` Deviation Register (`DEV-*` records) plus any follow-on item whose text is itself a defect report against a specific already-merged `ST-xx`.

A follow-on item is **not** automatically an escaped defect — most of v9.5's 21 were spec-debt/scope items (e.g. `BLG-SPEC-148`–`151`, `BLG-QA-180`/`181` documenting a *missing test*, not a *wrong behaviour*). Only classify as an escaped defect when the follow-on's own text asserts that shipped behaviour is wrong against its own AC.

## Per-Cycle Table

| Cycle | Shipped Stories | Follow-on Items Filed | Follow-on Ratio | Escaped Defects | Notes |
|-------|-----------------|------------------------|------------------|------------------|-------|
| `2026-09-15__release-v9.5` | 43 | 21 | 0.49 | 0 | **Baseline.** 0 formal `DEV-*` deviations filed this cycle (`closure_record.md` row 5: "0 formal DEV-* deviations filed this cycle — nothing to check"). All 21 follow-ons (`BLG-BE-118/119`, `BLG-SPEC-148`–`151`/`152`/`153`/`154`, `BLG-FE-178/179`, `BLG-QA-180/181`, `BLG-OPS-163/164`, `BLG-SPEC-155/156`, `BLG-GOV-335/336/337`) are spec-debt, missing-test-coverage, or governance-process items disclosed during execution/review — none asserts a merged story's shipped behaviour contradicts its own AC. Escaped-defect count for v9.5 is therefore 0, not because nothing was found, but because what was found was correctly classified as debt/coverage-gap rather than defect. |

## Update Procedure (Director of Quality / PMO Lead, at each post-ship closure)

1. Read the closing cycle's `claude/cycles/<cycle_id>/execution_state.json` — count stories with `status: done`/`merged` → **Shipped Stories**.
2. Read `claude/cycles/<cycle_id>/closure_record.md` STEP 3's backlog-reconciliation row → **Follow-on Items Filed** (the count already computed there).
3. Compute **Follow-on Ratio** = Follow-on Items Filed ÷ Shipped Stories (2 d.p.).
4. Read `closure_record.md`'s Deviation Register plus the follow-on items' own text (per the Definitions above) → **Escaped Defects** count, with a one-line Notes justification distinguishing defect from debt for any non-zero count.
5. Append one new row to the Per-Cycle Table above. Do not edit prior rows.
6. Update this document's `**Last Updated:**` header per `shared_standards.md` §16.14 (current entry + 2 prior, chain closed with "prior history retained — see prior entries in version control").

This document is not itself a governance prompt (`claude/system/`) — it is a QA operational record `docs/testing/` maintains going forward per its own update procedure, cross-referenced (not duplicated) from `post_ship_closure.md`'s own closure checklist by whoever next revises that prompt.
