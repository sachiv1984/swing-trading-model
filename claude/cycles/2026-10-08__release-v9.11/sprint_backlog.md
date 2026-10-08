**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-10-08
**Cycle:** 2026-10-08__release-v9.11
**Release:** v9.11
**Sprint Goal:** Make the post-trade debrief state R achieved and the stop at exit so it stops misreading correct trades, confirm every AI feature works after the v9.4–v9.10 import defect, and make the Risk Dashboard and Positions page show real prices, GBP entry values, true stop distance and calendar-day grace (BLG-BE-152, BLG-BE-150, BLG-BE-154, BLG-FE-206), while shipping the AI monthly P&L narrative and clearing v9.11's records, spec and governance hygiene items.
**Backlog Slice Source:** Original — `claude/cycles/2026-10-08__release-v9.11/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (ST-25 ordering)

# Sprint Backlog — 2026-10-08__release-v9.11

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-06 → EPIC-04 → EPIC-05. The P1 fast-track EPIC goes first. EPIC-06 merges before EPIC-04 so ST-35's §13 citation rule and ST-36's DoQ line reach `main` early. EPIC-05 merges last because ST-30 annotates columns added by EPIC-01 and EPIC-03.

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch must check whether the file exists before creating its own. If it exists, the branch appends its own section and does not overwrite.

**Sequencing note (ST-28 / `BLG-GOV-366`):** the engagement metric (ST-24) is defined before the first new AI feature (ST-25) ships, so its effect can be measured against the 2026-10-05 review baseline.

**Shared files across EPICs:**
- `openapi.yaml` (EPIC-02 ST-10/13; EPIC-03 ST-19; EPIC-04 ST-25; EPIC-05 ST-31/32): EPIC-02 owns it. Take the union of additions and the highest version.
- Route-registration chain: `routers/test.py`, `SystemStatus.js` fallback count, `SC-SS-01b` (EPIC-03 ST-19; EPIC-04 ST-25). EPIC-03 owns it. EPIC-04 recomputes the count after rebasing.
- `data_model.md` (EPIC-01 ST-06; EPIC-03 ST-17/20; EPIC-04 ST-26; EPIC-05 ST-30): EPIC-01 owns it. Keep migration blocks in ascending order.
- `ai_service.py` and prompt modules (EPIC-01 ST-01/07/08/09; EPIC-02 ST-12; EPIC-04 ST-25): EPIC-01 owns them.
- `reports.md` (EPIC-04 ST-25; EPIC-05 ST-29): EPIC-04 owns it.
- `accessibility-axe-scan.spec.js` (EPIC-01 ST-05; EPIC-06 ST-37): combine scan targets.
- `OPERATIONAL_GUIDE.md` and `prompt_change_log.md` (EPIC-06 only): CLAUDE.md §6 checklist and §8 step 2a per file.
- `backlog.md`: new items only, appended via `/backlog-add`. Re-check new IDs after rebasing.

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — Post-Trade Debrief & AI Reliability

**Maps to:** S2-01–S2-09
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer; QA & Testing Owner
**Estimated effort:** 6.75 days
**Risk IDs:** RISK-01, RISK-02, RISK-03
**Execution sequence:** 1

#### ST-01 — Give the post-trade debrief R achieved, the stop at exit and entry slippage

**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer
**Estimated effort:** 1.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (ST-05 and ST-09 depend on it)

**Notes:** RISK-01. P1 Correctness Fast-Track (DL-084). The AI Compliance & Governance Officer's Condition 2 sign-off is the first sub-step, before the prompt change; raise it at sprint start. `PROMPT_VERSION` bump. UI effect is wording only (FI-P3-02), so fixture tests suffice.

**Staging-only ACs:** AC 1 (the summary text produced for the three 2026-10-07 production examples is live model output; CI can assert the prompt inputs, not the generated wording).

**Status at sprint open: ready**

---

#### ST-02 — Verify all six AI features after the PR #1921 import fix, and file the escaped-defect note

**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-03, ST-04 (the escaped-defect note cites them)

**Notes:** RISK-02. Raise the staging Human-Delegation at sprint start. The 2026-10-07 production debrief verification may be cited for the debrief. The note's follow-ups map to ST-03, ST-04 and `BLG-QA-218`.

**Staging-only ACs:** AC 1 (dated staging run of all six AI features with a working Anthropic key). AC 2 (sampled output after opt-in, or another recorded live check).

**Status at sprint open: ready**

---

#### ST-03 — Keep the AI-output sampling hook from breaking or hiding errors in AI responses

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Pairs with ST-04. Fallback paths log with `exc_info`.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-04 — Test that every backend module imports with only backend/ on the path

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-03

**Notes:** Runs in CI Phase A.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-05 — Make the debrief Regenerate button recognisable, and show failures and the generated time

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-01 (same debrief component)

**Notes:** BLG-GOV-72 fast-path (c), `trade_history.md` v1.15 and the `debrief-regenerate-feedback` decision record. No shared relative-time formatter exists; the story may move one into `src/lib/format` (design gate note). Shares `accessibility-axe-scan.spec.js` with ST-37.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-06 — claude_audit_log: add prompt_hash and response_length, and log failed model calls

**Owner:** AI Compliance & Governance Officer; Data Model & Domain Schema Owner
**Estimated effort:** 1.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** RISK-03. Code, tests, `data_model.md` and `claude_api_log_hygiene_policy.md` proceed first; the live migration is Human-Delegation (DS-17 precedent, `ESC-EXEC-20260921-04`). ST-30 annotates the new columns later.

**Staging-only ACs:** AC 3 (migration applied live on staging and production, with verification output).

**Status at sprint open: ready**

---

#### ST-07 — State in the daily-briefing system prompt that output is advisory and cannot execute trades

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** One `prompt_version` bump, golden fixtures updated. Self-audit checklist A1 for chat and briefing.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-08 — AI briefing and chat state when a quoted stop was last recalculated

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-07 (same prompt module)

**Notes:** Its own `prompt_version` bump after ST-07's.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-09 — Pin every Claude model ID in one backend module

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** ST-01, ST-07, ST-08 (same call sites)

**Notes:** ST-25 (EPIC-04) must use this module once EPIC-01 merges.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

### EPIC-02 — Risk & Position Display Correctness (build-and-ship)

**Maps to:** S2-10–S2-15
**Owner:** Head of Engineering; Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 4.775 days
**Risk IDs:** RISK-04
**Execution sequence:** 2

#### ST-10 — Remove the hard-coded ×1.38 US price fallback from GET /portfolio, and flag stale prices

**Owner:** Head of Engineering; API Contracts & Documentation Owner
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None (ST-11, ST-12 and ST-13 depend on it)

**Notes:** RISK-04: lands first. `portfolio_endpoints.md` and `openapi.yaml` in the same commit. Design gate: the Dashboard Card 2 stale notice is a Playwright assertion beyond the AC. Add it, or file a backlog item before the PR opens. Qualifies for ST-36's DoQ strategy-values line.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-11 — Position Risk table: GBP entry prices, and grace-period stops shown as not enforced

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 0.875
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** ST-10

**Notes:** `risk-price-integrity` decision record. Confirm `risk_dashboard.md` §6 text (pre-written by the design gate) against what ships. Qualifies for ST-36's DoQ line (grace stops).

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-12 — GET /portfolio computes holding_days live from entry_date

**Owner:** Head of Engineering
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** ST-10 (same service function)

**Notes:** The other stored-`holding_days` readers (`alerts_service.py`, `compliance_service.py`, `ai_service.py`) are fixed, or filed as new backlog items. Do not edit an existing item. Qualifies for ST-36's DoQ line.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-13 — Stop Dist % computed in native currency for US positions

**Owner:** Head of Engineering; API Contracts & Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** ST-10, ST-11

**Notes:** `risk_dashboard.md` §6, `portfolio_endpoints.md` and `openapi.yaml` together. Qualifies for ST-36's DoQ line.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-14 — Grace alert filter and "Day N of 10" label use calendar days since entry

**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** `grace-alert-calendar-days` decision record and `positions.md` v2.15. The endpoint selects on `grace_days_remaining ≤ 2`; the `days_in_state` fallback and the `GRACE_SUPPRESSION_DAYS_IN_STATE` suppression move to the same predicate. Design gate: the "Day 10 of 10" ended state is a Playwright assertion beyond the AC. Add it, or file a backlog item before the PR opens. Qualifies for ST-36's DoQ line.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-15 — Recent Trades glyph treats a P&L that rounds to £0.00 as break-even

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Uses the existing `design_system.md` rule (no new decision record).

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

### EPIC-03 — Strategy, Records & Alert Integrity

**Maps to:** S2-16–S2-22
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner; Infrastructure & Operations Owner
**Estimated effort:** 4.55 days
**Risk IDs:** RISK-03, RISK-05
**Execution sequence:** 3

#### ST-16 — Rule on and test stop recalculation during grace

**Owner:** Strategy Rules & System Intent Owner; Head of Engineering
**Estimated effort:** 0.75
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None (ST-17 depends on it)

**Notes:** RISK-05. The ruling is the first sub-step; raise it at sprint start. Any `strategy_rules.md` §6.3 edit is under the Strategy Rules & System Intent Owner's explicit authority. Qualifies for ST-36's DoQ line.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-17 — Snapshot the strategy parameters in force onto each closed trade

**Owner:** Financial Reporting & Records Owner; Data Model & Domain Schema Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** ST-16

**Notes:** RISK-03 if new `trade_history` columns are needed; the live migration is Human-Delegation. ST-30 annotates the new columns later. Qualifies for ST-36's DoQ line.

**Staging-only ACs:** AC 2 (new columns applied live with verification output).

**Status at sprint open: ready**

---

#### ST-18 — Post-deploy synthetic check for post-grace stops and §11 multipliers

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Gate met (`BLG-BE-138` shipped in v9.10, ruling (a)). The AC is met by a fixture plus the existing Telegram send path; a live Telegram receipt is not named. Qualifies for ST-36's DoQ line.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-19 — Read-only market-regime source, so viewing regime no longer runs the stop-writing analyze call

**Owner:** Head of Engineering; API Contracts & Documentation Owner
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** RISK-05. New endpoint: `##` contract heading, `openapi.yaml`, `routers/test.py`, `SystemStatus.js` fallback count and `SC-SS-01b`, all in the same commit. EPIC-03 owns the fallback count; EPIC-04 (ST-25) recomputes it after rebasing.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-20 — DB-level unique constraint for active price alerts

**Owner:** Data Model & Domain Schema Owner; Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** RISK-03 live migration (Human-Delegation). Code and `data_model.md` first.

**Staging-only ACs:** AC 2 (constraint applied live with verification output). AC 1's genuinely concurrent double-submit can be shown in CI against a test DB only if the constraint exists there; otherwise it is evidenced on staging.

**Status at sprint open: ready**

---

#### ST-21 — Make the anomaly-check fingerprint-clear path respect send_alert, or document why not

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Either outcome is acceptable; the test asserts the chosen one.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-22 — Guard POST /trade-plans against a double-submitted duplicate plan

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** The default disposition is the client-side submit guard. An accepted-risk disposition needs a Product Owner line in QA evidence.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

### EPIC-06 — Governance, QA & Ops Hygiene

**Maps to:** S2-33–S2-43
**Owner:** Head of Specs Team; QA & Testing Owner; Infrastructure & Operations Owner; Director of Quality
**Estimated effort:** 5.20 days
**Risk IDs:** RISK-07, RISK-08
**Execution sequence:** 4

#### ST-33 — Write-time check that sprint_backlog.md Owner values use canonical role names

**Owner:** Head of Specs Team
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** None

**Notes:** Edits `idea_intake_prompt.md`: CLAUDE.md §6 checklist and the §8 step 2a per-file version-collision check (RISK-07). Replaces the §16.11 by-inspection rule that Sprint Planning applies today.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-34 — Give the effort-weighted PVR column its home in product_value_ratio_history.md

**Owner:** Head of Specs Team; Metrics Definitions & Analytics Owner
**Estimated effort:** 0.75
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None

**Notes:** RISK-07. Named-file write: `claude/roadmap/product_value_ratio_history.md` `## History` table, authorised under the execution_prompt.md §7 named-file rule. The `roadmap_prompt.md` STEP 2.4 change waits for `BLG-GOV-339`'s Head of Specs Team + Product Owner sign-off (raise at sprint start), with the CLAUDE.md §6 checklist.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-35 — §13 sign-off ACs must cite every §13 clause that names the feature's subject

**Owner:** Head of Specs Team; Strategy Rules & System Intent Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None

**Notes:** Governance prompt edit, CLAUDE.md §6 checklist (RISK-07). Push before ST-25's §13 determination if possible, so ST-25 is the rule's first user.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-36 — DoQ sign-off line for stories touching stop, grace, ATR or exit logic

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** None

**Notes:** First in EPIC-06, so qualifying EPIC-02/EPIC-03 stories (ST-10–ST-14, ST-16–ST-18) and ST-39 can complete the new DoQ line. CLAUDE.md §6 checklist if the template is a governance file.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-37 — Extend the axe accessibility scan to the Replay page

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** None

**Notes:** Shares `accessibility-axe-scan.spec.js` with ST-05 (EPIC-01): combine scan targets.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-38 — Fix SC-REP-04a's signed "+£0.00" expectation

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-39 — Mutation-test the US-market and batch-sizing paths

**Owner:** QA & Testing Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** ST-41 (same pilot test file)

**Notes:** Sizing paths: qualifies for ST-36's DoQ line if it touches stop or ATR values.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-40 — Make the ceiling/count regression tests read the source they claim to verify

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`

**Dependencies:** None

**Notes:** The scratch-branch regression edit is evidence only and must not be merged.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-41 — Reset the pilot test file's shared database mocks between tests

**Owner:** QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-41`

**Dependencies:** None (ST-39 depends on it)

**Notes:** —

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-42 — Make the Non-Registry Dependency Check a required status check on main

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-42`

**Dependencies:** None

**Notes:** RISK-08. Repository admin access via Human-Delegation; raise at sprint start.

**Staging-only ACs:** AC 1 (live `gh api` branch-protection read). AC 2 (a live PR not touching dependency files is not left blocked).

**Status at sprint open: ready**

---

#### ST-43 — Move test-only Python packages out of the production build

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-43`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** AC 1 (the production Render build installs no test-only package: confirmed from the deploy build log, or by CI if the Render build command installs only the production requirements file).

**Status at sprint open: ready**

---

### EPIC-04 — AI Narrative & Engagement Measurement (build-and-ship)

**Maps to:** S2-23–S2-28
**Owner:** Financial Reporting & Records Owner; Metrics Definitions & Analytics Owner; Head of UX & Design
**Estimated effort:** 4.90 days
**Risk IDs:** RISK-06, RISK-04
**Execution sequence:** 5

#### ST-23 — Cost estimate for the AI monthly P&L narrative

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None (ST-25 depends on it)

**Notes:** The cost-gating input to ST-25's AI endpoint security checklist.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-24 — Define the AI chat engagement metric set

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None (ST-25 depends on it)

**Notes:** Engagement metric before the first new AI feature (ST-28 sequencing note).

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-25 — AI-assisted monthly P&L narrative

**Owner:** Financial Reporting & Records Owner; Strategy Rules & System Intent Owner; Head of UX & Design
**Estimated effort:** 1.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** ST-23, ST-24; ST-35 (advisory)

**Notes:** RISK-06 resolved at planning 2026-10-08: confirmation route. Addendum order: (1) the Strategy Rules & System Intent Owner records a PASS / CONDITIONAL / FAIL §13 determination citing every §13 clause naming AI output or financial reporting; (2) the AI endpoint security checklist (ST-23's estimate is the cost input); (3) the design decision record under `docs/design/2026-10-08__release-v9.11/monthly-pnl-ai-narrative/` with Product Owner approval, plus the `reports.md` §Monthly P&L Report update. No implementation commit before (1)–(3) are recorded in `execution_state.json`. FAIL or a full-review finding stops ST-25 and ST-26 and goes to `amend cycle`. New AI endpoint: the CLAUDE.md §2 registration chain applies (shared with ST-19, RISK-04). Uses ST-09's model-ID module.

**Staging-only ACs:** None. Playwright with a mocked narrative covers AC 1; AC 2 is the recorded determination and prompt framing.

**Status at sprint open: ready**

---

#### ST-26 — Usage counter for the AI monthly P&L narrative

**Owner:** Metrics Definitions & Analytics Owner; Data Model & Domain Schema Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** ST-25

**Notes:** If the count needs a new table rather than existing audit rows, the live migration follows RISK-03 and is recorded as a delegation then.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-27 — AI chat UI interaction study protocol

**Owner:** Head of UX & Design
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** Protocol document only; no study is run in-sprint.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-28 — Track the 2027-01-03 AI feature usage review

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** Files a new gated backlog item via `/backlog-add`; does not edit `BLG-FEAT-60`. The sequencing note (ST-24 before ST-25) is recorded in this backlog's Merge Order.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

### EPIC-05 — Spec & Contract Hygiene

**Maps to:** S2-29–S2-32
**Owner:** API Contracts & Documentation Owner; Data Model & Domain Schema Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.80 days
**Risk IDs:** RISK-04
**Execution sequence:** 6

#### ST-29 — Reconcile the Monthly Restatement Marker spec with GET /reports/monthly-pnl

**Owner:** Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** Aged 2+ cycles. DEV-v9.7-ST04-01 is marked resolved in `reports.md` (canonical spec). Shares `reports.md` with ST-25: rebase after EPIC-04 merges.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-30 — Column provenance annotations in data_model.md

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** ST-06 (EPIC-01), ST-17 and ST-20 (EPIC-03)

**Notes:** Cross-EPIC: annotate after those columns are on `main`.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-31 — Correct the TradePlan status enum in openapi.yaml

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None

**Notes:** RISK-04: coordinate the `openapi.yaml` edit (rebase after EPIC-02/03/04).

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-32 — Fix the 5 error-response examples that diverge from the canonical envelope

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** —

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days (top edge 28.00) |
| Total estimated effort (in-scope) | 27.975 days (43 stories) |
| Utilisation | 99.9% (above the §1.5 95% buffer floor; Product Owner: proceed at ceiling, 2026-10-08) |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | None. All 43 slice items are in scope. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-06 §13 route for ST-25 | Strategy Rules & System Intent Owner | No — Done 2026-10-08 (confirmation route) |
| Condition 2 sign-off for ST-01, raised at sprint start | AI Compliance & Governance Officer | No |
| In-grace ruling for ST-16 and §13 determination for ST-25, raised at sprint start | Strategy Rules & System Intent Owner | No |
| `BLG-GOV-339` sign-off for ST-34's STEP 2.4 change | Head of Specs Team; Product Owner | No |
| Human-Delegation: ST-02 staging AI run; ST-06, ST-20 (and ST-17 if needed) live migrations; ST-42 branch protection | Infrastructure & Operations Owner; Data Model & Domain Schema Owner | No |
| Playwright for the ST-10 Dashboard Card 2 stale notice and the ST-14 "Day 10 of 10" ended state, or backlog items filed before the PR opens | QA & Testing Owner | No |

---

## Product Owner Sign-Off

Sprint goal: Confirmed (as drafted), 2026-10-08
Buffer floor (99.9%): Proceed at ceiling, 2026-10-08
Sprint split (RISK-09): Single sprint, 2026-10-08
Deferred execution blockers accepted: N/A (none)
RISK-06 pre-sprint decision: Confirmation route, ruled by the Strategy Rules & System Intent Owner, 2026-10-08

### Named-file writes

- Named-file write: `claude/roadmap/product_value_ratio_history.md` `## History` table (ST-34) — authorised under execution_prompt.md §7 named-file rule. A `claude/roadmap/*` write, listed for information; no separate confirmation needed.
- No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

Sprint backlog: Confirmed, 2026-10-08
Signed off by: Product Owner
