**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-19
**Cycle:** 2026-09-15__release-v9.5 (EPIC-04, BLG-GOV-335)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Director of Quality Review — EPIC-04 Autonomous-Class Sign-Off (v9.5)

## Why this exists

`qa_evidence_EPIC-04.md` signed EPIC-04 off as **autonomous class** (BLG-GOV-19), resolving its own Criterion 1 ambiguity in its own favour and stating the sign-off "should not be treated as final on this point." `BLG-GOV-335` was filed to rule on the ambiguity; the Head of Specs Team ruled 2026-09-19 (`execution_prompt.md` v3.79 §3.2.A) that the live-interaction bar is judged against the verification method **actually used**. This record is the Director of Quality review that ruling calls for. The cycle's artefacts (`qa_evidence_EPIC-04.md`, `verification_report.md`) are sealed and are **not edited**, per the `BLG-GOV-334` precedent; this record stands beside them.

## Eligibility determination

| Criterion | Claimed | Determination under v3.79 §3.2.A |
|-----------|---------|----------------------------------|
| 1 — all stories autonomous, or verification by document inspection only | Met via the Verification-class sub-criterion | **Unmet.** ST-22 (`delegated_decision`) and ST-29 verified against a live staging database, so verification was not by document inspection only. The evidence log's own wording — "document inspection only (a live schema query + a documentation note)" — describes both at once. |
| 2 — all AC verifiable by code review alone; no staging run; no live system interaction | Met | **Unmet** for ST-22 and ST-29, for the same reason. |
| 3 — no frontend-visible change | Met | Met (no file under `src/pages/**` or `src/components/**` touched). |
| 4 — signer field populated | Met | Met, but moot. |

EPIC-04 did **not** qualify for autonomous class. It required the standard Director of Quality sign-off block.

## Substance review (independent re-verification)

Method: read-only SELECTs against the staging database as `readonly_staging` (the ST-14 role; a read-only transaction; writes are rejected by the role). Run 2026-09-19, one day after the original 2026-09-18 queries.

| Finding (backlog item) | Claim in evidence | Re-verified |
|------------------------|-------------------|-------------|
| `BLG-SPEC-148` | DS-17 partial unique index absent; 5 pre-existing indexes; 0 duplicate open groups | Confirmed — 5 indexes, `idx_positions_open_ticker_entry_date_unique` absent, 0 duplicate `(portfolio_id, ticker, entry_date)` groups |
| `BLG-SPEC-149` | `positions.exit_note` does not exist; lives on `trade_history` | Confirmed |
| `BLG-SPEC-150` | 4 orphan columns (`atr_value`, `stop_price`, `fees`, `pnl_percent`) NULL on every row; counterparts populated | Confirmed — 2 rows, 0 non-null on each orphan; 2/2 non-null on `atr`, `current_stop`, `fees_paid`, `pnl_pct` |
| `BLG-SPEC-151` | `fees_paid` nullable though documented `NOT NULL` | Confirmed |
| `BLG-SPEC-154` | `trade_plans_status_check` has 7 values, spec documents 3 | Confirmed — exact 7-value list |

Every disclosed finding reproduces exactly. No fabrication or overstatement found; the follow-on filings are accurate and correctly prioritised.

## Disposition

- **Substance: Pass.** No AC narrowed or unmet; no `DEV-*` deviation; `verification_report.md`'s `Verified` status is unaffected (its own §1 already recorded this as a non-blocking advisory).
- **Class: reclassified** from autonomous class to **standard agent-mediated Director of Quality sign-off** — the same recognised format EPIC-01/02/03/06 used (`Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)`).
- **Blocking effect: none.** PR #1715 already merged; this corrects the record's classification, not the delivered work.

## Limits of this review (stated, not implied)

- It is **agent-mediated (§5.3)**. It cures the misclassification — the sign-off now sits in a class whose gate the work actually meets — but it is not a human review, and no rule in this framework requires one for the standard block.
- Only ST-29's `trade_plans` constraint claim (`BLG-SPEC-154`) was re-run live. ST-29's other content (the lifecycle state diagram) was not re-verified against live data here.
- Staging data was re-read one day after the original queries; agreement is strong evidence, not proof the original session saw identical state.
- The systemic question in the Phase 4 friction item — whether the framework should force a *human* decision point when both authoring and verifying steps are agent-mediated — is **not** answered by this review or by the §3.2.A ruling. It remains tracked as Carry-Forward item 1 in `lessons_learnt_closure.md`.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-19
- Comments: EPIC-04 substance verified independently and correct; autonomous-class eligibility unmet on Criteria 1 and 2 under `execution_prompt.md` v3.79 §3.2.A; reclassified to the standard agent-mediated block. `BLG-GOV-335` closed on this disposition.
