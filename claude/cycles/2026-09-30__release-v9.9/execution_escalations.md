Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-05

# Execution Escalations — 2026-09-30__release-v9.9

## ESC-EXEC-20261001-01

- **Raised at:** 2026-10-01T13:05:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-30__release-v9.9
- **Step:** STEP 3.1 (EPIC-04 execution loop)
- **ST/EPIC item:** ST-24 / EPIC-04
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-24's AC requires (a) defining a canonical "AI adoption window" gate reference, with the backlog item's own scope suggesting it live in `current_roadmap.md` §6 or as "a shared backlog convention," and (b) updating the 5 affected items' `**Gate criteria:**` fields in `claude/backlog/backlog.md` to cite that reference instead of restating it. Both `claude/roadmap/*` (beyond the narrow `workforce_capacity.md` exception) and editing existing `backlog.md` item content are explicitly outside Sprint Execution's declared write scope (CLAUDE.md §2 / `execution_prompt.md` §7) — this is a judgment call about where governance convention text should live, not a mechanical fix the engine can apply within its own write scope.
- **Owning authority:** Head of Specs Team (backlog.md's own Owner, and this item's listed Owner)
- **Unblock criteria:** Head of Specs Team decides where the canonical gate statement should live (new `current_roadmap.md` §6 entry, a shared backlog convention section, or another Class-1/Class-4 home) and either makes the edit directly or explicitly authorises this engine to do so (citing this escalation ID in the commit message, per the `workforce_capacity.md`/BLG-GOV-337 precedent format).
- **SLA due-by:** 2026-10-02T13:05:00Z (24h — Lifecycle/Process Integrity)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolved at:** 2026-10-05
- **Resolved by:** Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3), on the user's explicit direction ("act as relevant agents and resolve issues", 2026-10-05). SLA (2026-10-02T13:05:00Z) exceeded by ~3 days.
- **Resolution summary:** Head of Specs Team, 2026-10-05: Approved as a one-off write-scope authorisation (execution_prompt.md §7 not amended). Canonical home is a new unnumbered `## Shared Gate References` section in `claude/backlog/backlog.md` (not `current_roadmap.md` §6, which tracks roadmap-feature gates and is read by no backlog gate scanner). Engine authorised to insert that section and replace only the `**Gate criteria:**` line of BLG-FEAT-59/60/63, BLG-FE-84 and BLG-OPS-88; replacement lines keep a `due 2026-09-24` token so `scan_backlog_gate_conditions.py` and post-ship STEP 12.6 still detect them (verified: 130 gated / 14 lapsed unchanged; 4 items now report the correct 2026-09-24 lapse date instead of 2026-07-25). BLG-SPEC-65's stale sixth variant filed as BLG-GOV-361; standing-rule recommendation filed as BLG-GOV-362. Ownership correction: `backlog.md` is owned by the Product Owner — PO acknowledgement in PR review recommended, not blocking (content signed off at the planning seal).

## ESC-EXEC-20261001-02

- **Raised at:** 2026-10-01T15:10:44Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-30__release-v9.9
- **Step:** STEP 3.1.D (EPIC-04 execution loop)
- **ST/EPIC item:** ST-19 / EPIC-04
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-19 requires conducting the overdue 90-day AI feature usage review (BLG-GOV-74/140/141/142 cluster) — AC-1 requires assessing production AI feature adoption rate, cost per use, and continued-investment justification. This sandboxed environment has no production credential (same structural gap as `ESC-EXEC-20260921-02/03/04`, `ESC-EXEC-20260910-01`) — the review cannot be genuinely conducted against live production data from within this session.
- **Owning authority:** Head of Specs Team; PMO Lead
- **Unblock criteria:** A human with production access conducts (or directly supplies the data for) the review — a dated review artefact assessing adoption rate, cost per use, and continued-investment justification, with all 8 downstream gated items in the source cluster given an explicit disposition. Per CLAUDE.md §2's frontend-testing-gate pattern applied by analogy here (deferred-to-post-merge evidence requires a filed backlog item before the PR opens): if this is deferred past this EPIC's PR, a backlog item must be filed for the pending review before the PR opens.
- **SLA due-by:** 2026-10-04T15:10:44Z (72h — Human-Delegation)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:** —

## ESC-EXEC-20261001-03

- **Raised at:** 2026-10-01T15:10:44Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-30__release-v9.9
- **Step:** STEP 3.1.D (EPIC-04 execution loop)
- **ST/EPIC item:** ST-20 / EPIC-04
- **Trigger type:** Strategy
- **Blocking statement:** `gap_risk_service.py` (BLG-FEAT-65) shipped without a recorded §13 review or §13.5 roster row. Determining whether this was a genuine gap (and, if so, whether it is CONDITIONAL/COMPLIANT and what binding conditions apply) requires Strategy Rules & System Intent Owner / Head of Specs Team judgement against §13's actual boundary criteria — not a mechanical check. Per `execution_prompt.md` §5.3, this class of determination is eligible for agent-mediated sign-off in principle, but given its precedent-setting nature (a retroactive §13 finding against an already-shipped production feature) and this session having no standing user authorisation to rule on §13 boundary questions on the Strategy Rules & System Intent Owner's behalf for this specific item, it is surfaced rather than agent-mediated.
- **Owning authority:** Head of Specs Team; Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated determination recorded (new `docs/product/decisions/` file, or a `strategy_rules.md` §13.3/§13.5 wording update, as appropriate to the outcome). If CONDITIONAL or a genuine gap is found, binding conditions or a remediation item must be filed in the same determination.
- **SLA due-by:** 2026-10-04T15:10:44Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolved at:** 2026-10-05
- **Resolved by:** Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner jointly with Head of Specs Team — §5.3), on the user's explicit direction ("act as relevant agents and resolve issues", 2026-10-05). SLA (2026-10-04T15:10:44Z) exceeded by ~1 day.
- **Resolution summary:** CONDITIONAL. Decision record `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` (2026-10-05). The earnings-triggered flag is outside §13.3's exclusion (display-only, on request, position-specific dated event the user can act on within the daily cadence, consistent with §4.2.3); the standalone weekend-hold trigger (flags every open position all day every Friday) falls within §13.3's noise rationale — a genuine gap. Premise correction: a §13 sign-off was recorded at v6.9 (`claude/cycles/2026-07-10__release-v6.9/qa_evidence_EPIC-02.md`) but its AC tested §13.2 only. 9 binding conditions recorded; remediation filed as BLG-BE-136 (weekend-hold disposition by 2027-02-06), BLG-SPEC-179, BLG-GOV-359, BLG-GOV-360 (strategy_rules.md §13.3/§13.5 wording — outside Sprint Execution's write scope, exact text in the record's appendix).

## ESC-EXEC-20261001-04

- **Raised at:** 2026-10-01T15:10:44Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-30__release-v9.9
- **Step:** STEP 3.1.D (EPIC-04 execution loop)
- **ST/EPIC item:** ST-26 / EPIC-04
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-26's AC requires creating `claude/roadmap/role_share_history.md` (seeded with the 3-cycle backfill already computed by `scripts/compute_role_share_history.py`) so `roadmap_prompt.md` §7.2 can read from it instead of re-deriving the tally by hand. RISK-02 (per `sprint_backlog.md`'s own note): `claude/roadmap/*` is outside this routine's declared write scope (`execution_prompt.md` §7) beyond the narrow `workforce_capacity.md` exception — creating a new file there requires the same kind of explicit, plan-authorised routing/authority decision as that exception, not an engine-side default. This is also the same underlying write-scope gap already disclosed as deferred twice (`BLG-GOV-353` at v9.7 and v9.8 — see `docs/specs/metrics_definitions.md`'s Ready-Pool Runway Forecast section, which cites `claude/cycles/2026-09-28__release-v9.8/role_share_history.md`'s own interim-location precedent for the same constraint).
- **Owning authority:** Head of Specs Team (write-scope/routing authority for `claude/roadmap/*`)
- **Unblock criteria:** Head of Specs Team decides the canonical home for `role_share_history.md` (a `claude/roadmap/*` write-scope exception in the `workforce_capacity.md`/BLG-GOV-337 format, or a different canonical location) and either makes the edit directly or explicitly authorises this engine to do so, citing this escalation ID in the commit message.
- **SLA due-by:** 2026-10-02T15:10:44Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolved at:** 2026-10-05
- **Resolved by:** Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3), on the user's explicit direction ("act as relevant agents and resolve issues", 2026-10-05). SLA (2026-10-02T15:10:44Z) exceeded by ~3 days.
- **Resolution summary:** Head of Specs Team, 2026-10-05: Approved as a one-off write-scope authorisation (execution_prompt.md §7 not amended). Engine authorised to create `claude/roadmap/role_share_history.md` (PMO Lead, Class 3) — interim v9.8-cycle copy migrated, v9.8 row computed by `scripts/compute_role_share_history.py` (39 stories, Head of Specs Team 12 = 30.8%; v9.6–v9.8 rolling 18/102 = 17.6%, cross-checked against `2026-09-30__scheduled/cycle_record.md` §7.2) — and to edit `roadmap_prompt.md` §4 and §7.2 with the full CLAUDE.md §6 checklist (v9.29→v9.30; OPERATIONAL_GUIDE.md v4.217→v4.218). Interim file left as a dated historical snapshot. BLG-GOV-353 bullet-3 finding: `product_value_ratio_history.md` (v8.5 ST-22, `ad102c50`) had no write-scope authorisation on record and was absent from `roadmap_prompt.md` §4 — ratified retroactively by adding it to §4. One drafted edit not applied: adding story/backlog IDs to the §7.2 `####` heading, which CLAUDE.md §2 forbids — provenance recorded in the step text and changelog instead.

## ESC-EXEC-20261001-05

- **Raised at:** 2026-10-01T15:17:20Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-30__release-v9.9
- **Step:** STEP 3.1 (EPIC-05 execution loop)
- **ST/EPIC item:** ST-31 / EPIC-05
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-31's AC requires editing `claude/roadmap/current_roadmap.md`'s SI-02 field to cross-reference `docs/specs/metrics/si02_drift_score.md` §2.4's canonical "linked trade plan" definition (completing ST-23/v9.7's own already-decided cross-reference, which that cycle's `si02_drift_score.md` entry explicitly recorded as "deferred, outside Sprint Execution's write scope"). Sprint Planning classified this `autonomous`, but `claude/roadmap/*` (including `current_roadmap.md` by name) is explicitly listed as **not permitted** under `execution_prompt.md` §7's write-scope restriction, beyond the narrow `workforce_capacity.md` exception — the same gap already identified this session for ST-26 (`ESC-EXEC-20261001-04`), and the same gap `si02_drift_score.md` itself already disclosed at v9.7.
- **Owning authority:** Head of Specs Team (write-scope/routing authority for `claude/roadmap/*`)
- **Unblock criteria:** Head of Specs Team either makes the `current_roadmap.md` edit directly, or explicitly authorises this engine to do so (citing this escalation ID in the commit message, per the `workforce_capacity.md`/BLG-GOV-337 precedent format). The content itself is not in question — only the write-scope authorisation — since ST-23/v9.7 already decided what the cross-reference should say; this escalation and `ESC-EXEC-20261001-04` (ST-26) may be resolved together if Head of Specs Team grants a single `claude/roadmap/*` write-scope ruling covering both.
- **SLA due-by:** 2026-10-02T15:17:20Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:** —
