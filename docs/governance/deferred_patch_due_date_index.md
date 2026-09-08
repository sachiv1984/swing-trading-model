**Owner:** PMO Lead
**Class:** Governance Register (Class 4)
**Status:** Active
**Last Updated:** 2026-09-08 (ST-31, EPIC-04, v9.2, BLG-GOV-261 — index created)

---

# Deferred-Patch Due-Date Index

## 1. Purpose

Deferred governance-prompt patches — findings from `lessons_learnt_closure.md`, meta-reviews (`meta_review.md`), or audits, deliberately deferred rather than applied immediately — are currently tracked only inside the individual cycle document that deferred them (scattered across `claude/cycles/<cycle_id>/lessons_learnt*.md` and `meta_review.md` files). There is no single place to check "what's still outstanding and when is it due," which is why deferred patches have historically been re-discovered late (e.g. the `.claude/skills/commit-check/SKILL.md` patch carried 3 cycles, v6.4→v6.6, before `shared_standards.md` §17 gave it a governed write path).

This index is a lightweight, manually-maintained cross-reference — not a new source of truth. The deferring document remains authoritative; this index exists purely so a session can answer "is anything overdue?" in one read instead of scanning every cycle folder.

## 2. Schema

| Patch ID | Originating Cycle | Target File | Target (owner + date/trigger) | Status | Last Checked |
|----------|-------------------|--------------|-------------------------------|--------|--------------|
| Six-Arc model reconciliation | (carried across multiple scheduled rebalances, most recently referenced 2026-08-11) | `claude/roadmap/current_roadmap.md` (Six-Arc model section) | Head of Specs Team — next STEP 11.4 meta-review | Open — not yet OVERDUE per last rebalance's STEP -1.5 re-check | 2026-08-11 |
| LL-P5-03 | `2026-06-17__scheduled` meta_review.md | `roadmap_prompt.md` (per-patch release-shipped check) | Head of Specs Team — next scheduled rebalance | Deferred, no forcing recurrence observed since | 2026-06-17 |
| STEP 3.1 methodology standardisation | `2026-07-15__scheduled` meta_review.md | `roadmap_prompt.md` STEP 3.1 | Head of Specs Team — next STEP 11.4 meta-review, conditional on recurrence | Deferred, condition not yet re-triggered as of last check | 2026-07-15 |

## 3. Maintenance Convention

Update this index whenever:
- A new deferred patch is created (add a row at the point of deferral, in the same session that defers it).
- An existing deferred patch is applied, superseded, or explicitly re-deferred (update Status and Last Checked).
- A STEP 11.4 meta-review runs (cross-check every `Open`/`Deferred` row against that meta-review's own findings — a meta-review is the natural checkpoint for re-evaluating carried patches).

This index does not gate any governed routine — it is advisory, read-only reference material. Failing to update it is not itself a hard-gate violation, but a stale index defeats its own purpose, so update it opportunistically whenever a deferred-patch status changes.

## 4. Sign-Off

**PMO Lead:** Approved. This closes a real visibility gap — the three rows above were reconstructed from separate cycle documents that would otherwise require a multi-file scan to assemble; a single index is the right lightweight fix. Sprint Execution Engine (agent-mediated, PMO Lead role — §5.3), 2026-09-08.
