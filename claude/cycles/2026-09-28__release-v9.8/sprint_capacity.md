Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-28
Cycle: 2026-09-28__release-v9.8

# Sprint Capacity — 2026-09-28__release-v9.8

## 1.1 Capacity Inputs

```
Sprint duration:    ~1–2 calendar days between sprint starts (workforce_capacity.md, Effective 2026-07-17); band expressed in working-day-equivalent units
Available FTE:      Full-capacity band, ~24–28 working-day-equivalent units (reconfirmed unchanged 2026-09-23, ESC-EXEC-20260921-07)
Total capacity:     ~24–28 days
Skill constraints:  None flagged this cycle — all 6 EPIC owner roles (Head of UX & Design / Frontend Specifications & UX Documentation Owner; Head of Engineering / Financial Reporting & Records Owner; Director of Quality; Infrastructure & Operations Owner / Cybersecurity & Trust Lead; Head of Specs Team / Data Model & Domain Schema Owner; PMO Lead / Head of Specs Team) are available roles with no scarcity flag in workforce_capacity.md
```

## 1.2 Item Effort Mapping

All 39 items carry an explicit `**Effort:**` day-range or band in `stage4_backlog_slice.md` (release plan STEP 4 estimates — `scored_initiatives.md` holds 0 active roadmap initiatives, so no pre-assigned Effort Bands apply; all figures are inline estimates per `workforce_capacity.md`'s effort-to-days precedence rule). No `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Items | Estimated effort (days) |
|------|-------|--------------------------|
| EPIC-01 — Frontend & UX Debt Clearance | ST-01–ST-06 (6) | 3–5 (ST-01, L) + 1–2 (ST-02, M) + 0.5 (ST-03, S) + <1h (ST-04, XS) + 0.5–1 (ST-05, S) + 0.5 (ST-06, S) |
| EPIC-02 — Backend Reliability & Financial Correctness | ST-07–ST-08 (2) | 1 (ST-07, S) + 1 (ST-08, S) |
| EPIC-03 — QA & Test Coverage | ST-09–ST-16 (8) | 0.5–1 + <1h + 0.5 + 0.5 + 0.5–1 + 0.5 + 2 + <1h |
| EPIC-04 — Operations & Security Hardening | ST-17–ST-19 (3) | 0.5 + 0.5 + 0.5 |
| EPIC-05 — Spec & API Contract Debt | ST-20–ST-29 (10) | 0.5–1 ×2 + 1–2 + 0.5 + <1h ×3 + 0.5 (×2) + <1h |
| EPIC-06 — Governance & Process Debt | ST-30–ST-39 (10) | 0.5 + 1.5–2 + 1 + 0.5–1 + 0.5–1 + <1h + <1h + 0.5 + 1 + 0.5 |

**Total estimated effort: 28.00 days** (matches `release_plan.md ## Capacity Check` published figure — reconciled against the same item set, no drift).

## 1.3 Total Effort vs Capacity

28.00 days vs confirmed ~24–28 day band = **100.0% of the band's top edge**. Within band (at its ceiling). `capacity_feasible: pass` (per `release_plan.md`/`state.json`) — not a `warn` outcome, so no Phasing Recommendation subsection exists this cycle and no formal over-allocation resolution is required at STEP 3.2.

## 1.4 Gate-Conditional Deferred Items

None. `execution_state.json` for this cycle does not yet exist (fresh cycle) and no items in `stage4_backlog_slice.md` carry a `status: deferred_at_planning` marker — all 39 sliced items enter the sprint backlog as `include`.

## 1.5 Minimum Capacity Buffer Floor (Advisory)

`scope_effort ÷ confirmed_capacity` = 28.00 / 28.00 = **1.00 (100%)** — exceeds the 95% buffer-floor recommendation (§1.5). This is distinct from and less severe than the >100%-of-capacity WARN threshold (not triggered here — scope sits exactly at, not above, the top edge).

**Product Owner acknowledgement (buffer floor exceeded):** Proceed at full capacity. Rationale: this cycle's scope was explicitly constructed to the top of the confirmed band per the Product Owner's own "full capacity" instruction recorded at release planning (`cycle_summary.md`, `release_plan.md ## Capacity Check`) — the 0% buffer is a deliberate, already-acknowledged choice at the release-planning stage, not a new risk surfacing for the first time here. No scope trim requested. `capacity_warn_acknowledged` is not applicable (outcome is `pass`, not `warn`) — this buffer-floor acknowledgement is recorded as a distinct, non-blocking advisory per §1.5's own terms.
