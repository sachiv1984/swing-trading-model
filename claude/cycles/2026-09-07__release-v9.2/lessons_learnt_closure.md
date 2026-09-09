Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-09 (Addendum — all 7 outstanding deferred patches resolved same-session, user-directed follow-up); prior: 2026-09-09 (initial filing)
Cycle: 2026-09-07__release-v9.2

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Ship v9.2: close all 56 backlog-driven items in scope — Arc 5 low-volume compliance advisory (the sole ungated build-adjacent item), frontend accessibility & spec compliance (4 items), QA & CI reliability debt (11 items), governance process debt (26 items), and spec/tech/ops debt (14 items).
Run: 2026-09-07__release-v9.2
Reviewed by: PMO Lead
Date filed: 2026-09-09
Prior cycle checked: 2026-09-03__release-v9.1 (`lessons_learnt_closure.md`)

---

## What worked well

- STEP 0's parallel reads of `verification_report.md`, `execution_state.json`, and `sprint_close.md` again produced a single, internally consistent picture of the cycle (56/56 stories done, 0 new `DEV-*` deviations filed, 2 P3 register entries — `BLG-FE-172` resolved same-story, `BLG-OPS-152` confirmed — 0 delegations/blocked items outstanding at closure time) with no contradictions across the three sealed sources.
- The Release Slice table in `backlog.md` (ST → BLG source mapping, `RP:v9.2:...` marker) made STEP 3 Backlog Reconciliation for all 56 items fully mechanical via a single scripted pass — every `BLG-*` heading matched, every `**Provisional-Target:**` field located and updated in one run, 0 not-found, 0 already-complete false positives.
- `2026-09-03__release-v9.1` closure's own Carry-Forward item 2 (formalise the "apply an unambiguous Phase 3/4 friction-item fix at the immediately-following closure's own STEP 8" pattern, rather than relying on precedent alone) was applied this run — `post_ship_closure.md` STEP 8 now states this explicitly (v2.31→v2.32). Its sibling Carry-Forward item 1 (re-verify prior-cycle "carried" claims against current `prompt_change_log.md` state, `LL-v9.1-Closure-01`) was independently confirmed working this cycle: this cycle's own Phase 4 section (`lessons_learnt_cycle.md`) explicitly re-ran the check and confirmed all 3 carried-forward deferred patches from `2026-09-03__release-v9.1`/`2026-08-21__release-v9.0` were already applied — no stale "still open" claim propagated forward.
- The endpoint coverage drift check (STEP 6 advisory) found an apparent 80-endpoint gap on a naive parse of `api_performance_baseline.md` before the table's actual (non-backtick, plain `METHOD /path`) row format was identified; re-parsing correctly against that format reduced the gap to 0 genuine misses (remaining apparent gaps were query-string-suffixed rows and path-parameter-name differences, both already-known formatting quirks, not real coverage gaps) — worth noting in case a future closure hits the same false-positive shape.

---

## Friction Log

### Friction Item 1

**Classification:**
Type D — Minor Process Friction (documentation/tooling ambiguity, no functional or governance gap)

**Recurrence:** New this cycle — not carried from `2026-09-03__release-v9.1`.

**What happened:**
STEP 6's Endpoint Coverage Drift Check advisory does not specify the exact row format of `docs/ops/api_performance_baseline.md`'s endpoint table, and this table's actual format (plain `| GET /path | ... |` rows, no backticks around the method+path) differs from the backtick-wrapped format assumed by a first-pass regex parse, which produced a false 80-endpoint gap before the correct format was identified and re-parsed (0 genuine gaps). No incorrect `BLG-OPS-*` item was filed as a result — the false positive was caught before any write — but a future closure re-deriving this check from the prompt text alone, without this session's context, could plausibly repeat the same mis-parse and file a spurious tracking item.

**Where in the routine:**
STEP 6, Endpoint Coverage Drift Check (Advisory).

**Root cause:**
The advisory's instructions describe *what* to compare (normalised method+path sets from both documents) but not the concrete row format of either source document — reasonable, since format is presentation detail, not governance logic, but the two documents in this repo happen to use different embedded-code-span conventions (`openapi.yaml` is structured YAML with no ambiguity; `api_performance_baseline.md` is free-form Markdown prose+tables that vary in whether the endpoint identifier is backtick-wrapped).

**Blast radius analysis:**
- What would have propagated: a spurious `BLG-OPS-*` backlog item claiming ~80 missing endpoint registrations, when the real number is 0 — would have cost the item's eventual reviewer significant re-investigation time before finding the same parsing gap this session found directly.
- When it would have surfaced: at the next attempt to actually action the filed item (re-run the perf baseline), or at the next closure's own STEP 6 re-derivation, whichever came first.
- Recovery cost if uncaught: moderate — a large, wrong-count backlog item is more disruptive to correct later than a same-session parsing fix, since by the time it's actioned the original parsing context is gone.

**Process patch:**
→ Deferred patch (cannot apply this run — a one-line format note is low-risk, but the underlying `api_performance_baseline.md` table format is itself not owned by this closure engine, and generalising the note to be robust to a *future* format change, not just this cycle's observed one, needs a moment's more thought than fits this run's own scope):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 6, Endpoint Coverage Drift Check (Advisory)
  - Change required: add a brief parsing note — normalise both documents' endpoint identifiers to a canonical `METHOD /path` string regardless of surrounding Markdown formatting (backticks, query-string suffixes, inline prose) before diffing, and treat a query-string-suffixed row (e.g. `GET /analytics/metrics?period=all_time`) as the same endpoint as its bare-path form.
  - Owner: Head of Specs Team
  - Target: next `post_ship_closure.md` revision touching STEP 6

---

## Recurrence Escalations

None raised this cycle. `lessons_learnt_cycle.md`'s own Phase 3/Phase 4 sections report 0 active recurrence escalations — all 4 friction items there (2 Phase 3, 2 Phase 4) are first occurrences per the formal §3.7 check, and all 3 deferred patches carried in from `2026-09-03__release-v9.1`/`2026-08-21__release-v9.0` were independently re-confirmed already applied this run (see Phase 3/Phase 4 "Prior cycle checked" notes).

`2026-09-03__release-v9.1`'s own Carry-Forward item 1 (re-verify prior-cycle "carried" claims against current state) is confirmed applied and working as designed this cycle (see "What worked well" above). Carry-Forward item 2 (formalise the same-cycle-application pattern) is resolved by this closure's own STEP 8 immediate action (`post_ship_closure.md` v2.32).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/post_ship_closure.md` | STEP 8 | New "Same-cycle application pattern" paragraph, formalising when to apply vs. defer a Phase 3/4 friction-item fix at Post-Ship Closure (resolves `2026-09-03__release-v9.1` Carry-Forward item 2) | 2.31 → 2.32 | Yes — `prompt_change_log.md` 2026-09-09 |
| `claude/system/OPERATIONAL_GUIDE.md` | §10, §14 (×2), document header | Source-prompt header and governance table synced for the bump above; document-level `**Version:**`/`**Last Updated:**` header also corrected from a stale 4.180 to 4.183, having fallen 2 rows behind the table's own already-current entries (4.181/4.182, both landed 2026-09-08 without a header bump) | 4.180 → 4.183 | Yes — `prompt_change_log.md` 2026-09-09 |
| `docs/specs/Specs_Index.md` | §42 (new) | Test Coverage Gaps — v9.2 section added (0 new gaps); endpoint coverage drift check cross-referenced (0 genuine gaps after correct parsing); full-document TSG sweep explicitly reported (0 Open entries, 0 resolved) per `LL-v9.0-Closure-01`'s mandatory-reporting requirement | n/a (Changelog-table document, no header version field) | Not applicable |

---

## New files created this run

None — this closure's document changes were all updates to existing artefacts (changelog, roadmap, backlog, velocity metrics, Specs Index, scope/decisions supersession, governance prompts).

---

## Outstanding deferred patches

**All 7 below resolved same-session (2026-09-09, later the same day), acting per-role at explicit user direction ("act as the relevant agents and deal with the 7 outstanding actions") — see Addendum at the end of this file and `closure_record.md`'s own Addendum for full detail.**

| File | Section | Change required | Owner | Target | Carried since | Resolution |
|------|---------|----------------|-------|--------|---------------|------------|
| `claude/roadmap/backlog.md` (via `groom backlog`'s field-completeness scan design) | Field-completeness scan | Extend the scan to flag a backlog item whose exclusion depends on another item's gate but which itself carries no `**Gate criteria:**` field (Release Planning Friction Item 1, `BLG-FEAT-92`'s 4th-consecutive-cycle manual reconciliation) | Head of Specs Team / PMO Lead | Next `groom backlog`/`backlog_management_prompt.md` design review | v9.2 (new) | ✅ Resolved — Gate-Inheritance Field-Completeness Scan added, `backlog_management_prompt.md` v1.16→v1.17; applied immediately to `BLG-FEAT-92` |
| `claude/roadmap/workforce_capacity.md` or `claude/system/shared_standards.md` | New canonical band-to-days table | Add a canonical XS/S/M/L→days conversion table so Release/Sprint Planning stop re-deriving it from scattered per-item `**Effort:**` parentheticals each cycle (Release Planning Friction Item 2) | Head of Specs Team | Next `release_planning_prompt.md` or `shared_standards.md` revision | v9.2 (new) | ✅ Resolved — table added to `workforce_capacity.md` (chosen over `shared_standards.md`: lighter-weight, not a governance prompt) |
| `claude/system/execution_prompt.md` | STEP 4 (Merge Gate), step 3a | Add a same-step self-verification read-back (`gh pr view` + `execution_state.json` field re-read) after the persist-state-before-halt commit, mirroring `LL-v9.0-P3-01`'s fix for STEP 3.1.A step 10a | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 4 | v9.2 (new) | ✅ Resolved — `LL-v9.2-P3-01` added, v3.73→v3.74 |
| `claude/system/execution_prompt.md` | STEP 3.1.A, commit guidance | Extend the never-`amend`-a-pushed-commit guardrail (`LL-v9.1-P3-02`) to explicitly cover the failed-intermediate-commit trigger path, not only the amend-after-successful-push path | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 3.1.A | v9.2 (new) | ✅ Resolved — `LL-v9.2-P3-02` added, same v3.74 bump |
| `claude/system/delivery_verification_prompt.md` (+ `claude/system/templates/qa_evidence_template.md`) | §2.1 (QA Evidence Review — Per-Item Review) | Add `Pass_with_deviation` to the enumerated Result value set with defined semantics (AC partially unmet, disclosed transparently, requires a confirmed backlog item, defaults to P3 unless later assessed as core-behaviour-incomplete) | Head of Specs Team | Next `delivery_verification_prompt.md` revision touching §2.1 | v9.2 (new) | ✅ Resolved — `LL-v9.2-P4-01` added, v3.9→v3.10 + companion template v1.12→v1.13 |
| `claude/cycles/2026-09-07__release-v9.2/qa_evidence_EPIC-02.md`, `qa_evidence_EPIC-03.md` | Sign-Off Block comments | Strike or update the stale "STEP 4 merge-gate...remains outstanding before merge" sentence now that both PRs (#1597, #1598) are confirmed merged | Director of Quality | Next touch of either file | v9.2 (new) | ✅ Resolved — both files' stale sentences struck |
| `claude/system/post_ship_closure.md` | STEP 6, Endpoint Coverage Drift Check | Add a parsing note: normalise both documents' endpoint identifiers to canonical `METHOD /path` regardless of Markdown formatting (backticks, query-string suffixes) before diffing (this closure's own Friction Item 1) | Head of Specs Team | Next `post_ship_closure.md` revision touching STEP 6 | v9.2 (new) | ✅ Resolved — `LL-v9.2-P-Closure-01` added, v2.32→v2.33 (also backfilled a missing v2.32 row found omitted from the companion changelog during this same edit) |

0 deferred patches remain open from this closure as of this addendum.

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `2026-09-03__release-v9.1`'s own Carry-Forward items were both resolved or confirmed working this cycle (item 1 confirmed live in this cycle's own Phase 4 recurrence check; item 2 applied directly at this closure's STEP 8) — the closure-to-closure Carry-Forward mechanism itself is functioning as intended across a full cycle boundary. | No action needed; continue relying on the mechanism. | Post-Ship Closure |
| 2 | 6 deferred patches were open simultaneously across `execution_prompt.md` (2), `delivery_verification_prompt.md`/`qa_evidence_template.md` (1), `qa_evidence_EPIC-xx.md` (1), `groom backlog` design (1), and a canonical effort-band table (1) — a noticeably larger simultaneous backlog than the 1-3 typical of recent cycles, but all resolved same-day per the Addendum below rather than carried forward. | The 2-cycle escalation threshold was never tested this time (all resolved within hours), so this observation is now informational only — the "lighter-weight sweep" recommendation is moot for this specific batch, but the underlying pattern (a larger-than-typical outstanding-action count) is worth noting if it recurs and is *not* resolved same-day next time. | Post-Ship Closure |

## Addendum — 2026-09-09 (same-session follow-up, user-directed: "act as the relevant agents and deal with the 7 outstanding actions")

All 7 items in the Outstanding Deferred Patches table above were actioned later the same day, acting as Head of Specs Team (items 1–5, 7) and Director of Quality (item 6) per explicit user direction, following the role-ownership-verification rule. Summary here for this file's own tracking (full narrative in `closure_record.md`'s own Addendum):

- Item 1 (gate-inheritance scan): `backlog_management_prompt.md` v1.16→v1.17, applied immediately to `BLG-FEAT-92`.
- Item 2 (effort-band table): added to `workforce_capacity.md`.
- Items 3–4 (execution_prompt.md self-check + amend-guardrail extension): both landed in one `execution_prompt.md` v3.73→v3.74 bump.
- Item 5 (`Pass_with_deviation`): `delivery_verification_prompt.md` v3.9→v3.10 + `qa_evidence_template.md` v1.12→v1.13.
- Item 6 (stale caveat): both `qa_evidence_EPIC-xx.md` files struck.
- Item 7 (endpoint-drift parsing note): `post_ship_closure.md` v2.32→v2.33 — also caught and backfilled a missing v2.32 row in the companion changelog, found omitted during this same edit.

`OPERATIONAL_GUIDE.md` synced in one consolidated pass (v4.183→v4.184) for all 5 governance-prompt bumps.

0 deferred patches remain open from this closure as of this addendum.

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-09-07__release-v9.2",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-09-09T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 0,
  "resolved_same_day_count": 7,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Active"
}
```
