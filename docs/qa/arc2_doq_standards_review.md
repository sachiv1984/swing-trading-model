**Owner:** QA Lead; Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-10 (ST-25, EPIC-06, v9.16, BLG-QA-22 — initial review)
**Cycle:** 2026-11-06__release-v9.16 (ST-25 — BLG-QA-22)

---

# Arc 2 DoQ Standards Review

## 1. Purpose and Method

`BLG-QA-22` asks whether the Director of Quality (DoQ) sign-off standards are adequate for the kinds of feature Arc 2 introduced, and to amend `shared_standards.md` if not.

**Standards reviewed (current versions):** `claude/system/templates/qa_evidence_template.md` v1.18 (evidence table, result grades, Standard Sign-Off Block, addenda), `claude/system/execution_prompt.md` v3.93 §3.2.A (frontend testing gate, autonomous class, same-EPIC consistency check), CLAUDE.md §2 (Playwright-or-staging rule), and `shared_standards.md` v3.41 §18 (Playwright authoring standard).

**Evidence reviewed:** the QA evidence files of the EPICs that shipped Arc 2 features:

| Cycle | File | Arc 2 feature |
|-------|------|---------------|
| `2026-04-29__release-v3.1` | `qa_evidence_EPIC-01.md` | PT-01 Trade Plan object |
| `2026-04-29__release-v3.1` | `qa_evidence_EPIC-02.md` | PT-02 Research View (first slice) |
| `2026-05-05__release-v3.2` | `qa_evidence_EPIC-01.md` | PT-02 + PT-03 Research View, prospective heat |
| `2026-05-05__release-v3.2` | `qa_evidence_EPIC-02.md` | PT-05 Pre-trade entry checklist |
| `2026-05-09__release-v3.3` | `qa_evidence_EPIC-03.md` | Research View spec and QA closure |
| `2026-06-22__release-v6.1` | `qa_evidence_EPIC-04.md` | PT-04 Setup Quality Score |

**Cross-check:** the defects found this cycle by the first tests that run the whole Arc 2 flow (ST-24 `arc2-happy-path.spec.js`, ST-26 `trade-plan-lifecycle.spec.js`; see `docs/qa/arc2_e2e_qa_protocol.md` §6). A defect that reached `main` through a signed-off EPIC is evidence of what the rubric did not ask.

Gaps already closed by later standards are listed in §3 and not re-proposed.

---

## 2. Gaps Found

### Gap 1 — Cross-page hand-offs are verified one page at a time

**Arc 2 feature type:** a flow in which one page hands data to the next (URL parameters, router state, a write that a later page reads): Research → Trade Plan, Trade Plan → Trade Entry ("Start Trade from Plan"), Trade Entry → plan link, position exit → Plan vs Reality.

**Evidence:** every Arc 2 EPIC verified each story's ACs on its own page. v3.1 EPIC-01 ST-03 verified "Position linking: `?position_id=` param auto-sets position_id" by code review of the receiving page only. The Playwright files written for Arc 2 each mock a single page (`docs/qa/arc2_e2e_qa_protocol.md` §3). Nothing in the rubric asks whether the sending page sends what the receiving page needs.

**Defect that got through:** `BLG-FE-281`. Research View's "Create Trade Plan" sends only `ticker`; the Trade Plan defaults the missing market to US, so a UK ticker's plan is created as a US plan. Both pages pass their own tests.

**Proposed check:** when a story adds or changes a hand-off between pages, the evidence names one test (or recorded staging run) that starts on the sending page and asserts the value on the receiving page or in the resulting write.

### Gap 2 — Lifecycle transitions stated in a spec are not traced to code

**Arc 2 feature type:** a first-class object with a status lifecycle. PT-01 introduced `trade_plans.status`; `data_model.md` §Trade Plan Lifecycle draws `draft → … → active → closed`.

**Evidence:** v3.1 EPIC-01 verified that the `status` column and its CHECK constraint exist (ST-01 AC-1, ST-02). No row checks which code path performs each transition. The later status extension (DS-21, seven statuses) was documented from the live constraint, again without tracing the writers.

**Defect that got through:** `BLG-BE-211`. `data_model.md` says `active → closed` happens when the linked position closes, but no backend code writes `closed`. Every linked plan stays `active` after its trade closes, and the P&L reconciliation flags each one.

**Proposed check:** when a story adds or changes a status or lifecycle field, or the spec's lifecycle diagram, the evidence lists each transition the spec states with the code path that performs it and a test, or marks it not implemented and names the backlog item.

### Gap 3 — Data-gated features are signed off on the branch that can occur live

**Arc 2 feature type:** a feature whose main output exists only once real data passes a threshold. PT-04 Setup Quality Score returns a score only with ≥ 20 closed trades.

**Evidence:** v6.1 EPIC-04 ST-08 AC-03 records the gate-not-met response as "the primary testable state at implementation time (15 trades in production)". The score branch was verified by unit tests and a mocked panel only. That was a fair basis for sign-off, but nothing recorded that the score had never been seen on real data, and nothing tracks seeing it once the gate clears. The same pattern applies to Arc 5's SI-02 drift UI (`docs/qa/arc5_qa_protocol.md` Stage 4).

**Proposed check:** when a story ships a feature gated on a data threshold, the evidence states which branches were observed on real (staging or production) data and which only on mocks or fixtures, and names a backlog item to verify the unobserved branch on real data once the threshold is met.

### Observation (no rubric change) — Values derived from another record

`BLG-BE-212`: Plan vs Reality's entry delta takes the planned entry from the signal's price at exit, not from the plan. The existing line "All acceptance criteria verified against canonical spec" covers this when the spec names the source; here `data_model.md` described the field as not yet implemented, so the miss is spec drift, handled by the backlog item. No new rubric line.

---

## 3. Arc 2-Era Gaps Already Closed

| Gap seen in the Arc 2 evidence | Closed by |
|--------------------------------|-----------|
| Observable UI ACs passed on code review with "staging verification pending post-merge" and no tracking item (v3.1 EPIC-01 ST-03) | CLAUDE.md §2 frontend testing gate (Playwright or recorded staging run; deferred staging needs a backlog item before the PR) |
| Autonomous-class sign-off applied to an EPIC with frontend changes (v6.1 EPIC-04, retro counter-signed) | `execution_prompt.md` §3.2.A Criterion 3 detection rule (BLG-GOV-135) |
| Evidence tables that did not list every AC | `qa_evidence_template.md` v1.7 every-AC requirement |
| No grade for a partly met AC | `Pass_with_deviation` (template v1.13) |
| Sizing and stop values not checked against strategy rules | Strategy-values DoQ line (template v1.18, BLG-GOV-370) |

---

## 4. Amendment

Amendments are warranted for Gaps 1–3. They are added to `claude/system/shared_standards.md` as **§25 DoQ Checks for Flow, Lifecycle and Data-Gated Stories** (v3.41 → v3.42), under the CLAUDE.md §6 checklist, as conditional checks applied at DoQ sign-off (`execution_prompt.md` §3.2.A). Each check applies only when its trigger is met, so EPICs without that feature type are unaffected.

Wiring the three checks into the Standard Sign-Off Block of `qa_evidence_template.md` as checkbox lines is outside this story's sealed AC, which names `shared_standards.md` only. It is tracked by `BLG-GOV-418`. Until then §25 applies by reference from the sign-off reviewer.

---

## 5. Change Log

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-11-10 | Initial review (ST-25, BLG-QA-22) | QA Lead; Head of Specs Team (Sprint Execution Engine) |
