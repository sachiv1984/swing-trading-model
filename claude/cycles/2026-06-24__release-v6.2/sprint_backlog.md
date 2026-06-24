**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-24
**Cycle:** 2026-06-24__release-v6.2
**Release:** v6.2
**Sprint Goal:** See sprint_goal.md — Sprint 1: Strategy parity cluster; Sprint 2 (conditional): AI intelligence layer
**Backlog Slice Source:** stage4_backlog_slice.md (original — no amendment)

---

# Sprint Backlog — 2026-06-24__release-v6.2

---

## Merge Order

**Sprint 1 EPIC merge sequence: EPIC-03 → EPIC-01**

- EPIC-03 is autonomous-class (governance patches only) and will complete first; merge before EPIC-01 PR to keep main clean
- EPIC-01 must rebase onto main after EPIC-03 merges
- **execution_state.json owner: EPIC-01** — EPIC-01 initialises this file; EPIC-03 appends its section when found
- Sprint 1 shared files: no overlap between EPIC-01 (backend/frontend/API) and EPIC-03 (governance documents only)

**Sprint 2 EPIC merge sequence: EPIC-02** (after Sprint 1 fully merged and verified)

- EPIC-02 branch must rebase onto main after EPIC-01 + EPIC-03 merge before finalising implementation
- Shared files (Sprint 2 rebase advisory): `docs/reference/openapi.yaml`, `docs/specs/api_contracts/` — EPIC-02 must include EPIC-01's additions before adding its own entries

---

## Sprint Scope

---

### Sprint 1

---

#### EPIC-01 — Strategy Parity: Core Engine Alignment

**Maps to:** S2-01, S2-02, S2-03, S2-04 (BLG-FEAT-46, BLG-FEAT-47, BLG-FEAT-48, BLG-FEAT-49)
**Owner:** Head of Engineering
**Estimated effort:** ~7 days
**Risk IDs:** RISK-03 (inv-vol sizing regression — mitigated by AC-04/05 of ST-04)
**Execution sequence:** 2 (after EPIC-03 merges; runs Sprint 1)
**Branch:** `exec/2026-06-24__release-v6.2/EPIC-01`
**execution_state.json:** Owner — initialise on first EPIC-01 commit

---

##### ST-01 — Nightly trailing stop computation — backend service

**Owner:** Head of Engineering
**Estimated effort:** ~2 days
**Delegation class:** delegated_backend
**Dependencies:** None
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Staging-only ACs:** None

**Notes:** This story establishes the `current_trailing_stop` field on the positions response. ST-02 cannot begin until ST-01 is complete and verified. Logic must match `production_strategy.py` parameters exactly: `INITIAL_ATR_MULT=5`, `PROFIT_ATR_MULT=2`, `ATR_PERIOD=14`.

---

##### ST-02 — Trailing stop display and breach badge — frontend

**Owner:** Head of Engineering
**Estimated effort:** ~1 day
**Delegation class:** delegated_frontend
**Dependencies:** ST-01 (current_trailing_stop field required)
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Staging-only ACs:** AC-03 (breach badge visual distinctiveness — colour/icon confirmation requires human staging sign-off; badge presence and breach logic covered by Playwright)

**Notes:** Design spec: `docs/design/2026-06-24__release-v6.2/trailing-stop-display/ux_spec.md`; Frontend spec: `docs/specs/frontend/pages/positions.md` v1.8. Table column density advisory from design gate: if layout testing reveals excessive horizontal scroll (~15 columns), Initial Stop + Trail Stop may be combined into a two-line cell without spec amendment — implementation-level layout decision.

---

##### ST-03 — Month-end rebalance exit signal generation

**Owner:** Head of Engineering
**Estimated effort:** ~1.5 days
**Delegation class:** delegated_backend
**Dependencies:** None
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Staging-only ACs:** AC-05 (styling — `exit_rebalance` visual distinctiveness from stop exits requires human staging sign-off; `exit_rebalance` label presence in GET /signals covered by Playwright)

**Notes:** Design spec: `docs/design/2026-06-24__release-v6.2/rebalance-exit-signal-style/ux_spec.md`; Frontend spec: `docs/specs/frontend/pages/signals.md` v0.4. Pre-check: confirm `stop_exit` is a live API value in GET /signals before applying red badge styling — if not live, defer that badge variant to the sprint that introduces `stop_exit` (no spec amendment needed for deferral).

---

##### ST-04 — Inverse-volatility position sizing for signal-driven entries

**Owner:** Head of Engineering
**Estimated effort:** ~2 days
**Delegation class:** delegated_backend
**Dependencies:** None
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Staging-only ACs:** None

**Notes:** RISK-03 — this story replaces the core sizing path for signal-driven entries. Regression test required (AC-04): manual position sizing path must remain unchanged. Existing sizing unit tests must pass alongside new inv-vol tests. High regression risk — treat as highest-priority test coverage item in EPIC-01.

---

##### ST-05 — Risk-off exit alerts for existing positions

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_backend
**Dependencies:** None
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Staging-only ACs:** AC-02 (risk_off_exit alert styling — visual distinctiveness from trailing stop breach and exit_rebalance requires human staging sign-off; alert presence covered by Playwright)

**Notes:** Design spec: `docs/design/2026-06-24__release-v6.2/risk-off-exit-alert/ux_spec.md`; Frontend spec: `docs/specs/frontend/pages/positions.md` v1.8. ST-06 (Sprint 2) depends on risk_off_exit alerts being live — verify AC-01/03/04 before Sprint 1 close.

---

#### EPIC-03 — Governance & QA Debt

**Maps to:** S2-07, S2-08, S2-09, S2-10 (BLG-GOV-135, BLG-GOV-136, BLG-OPS-75, BLG-QA-62)
**Owner:** Head of Specs Team (ST-10, ST-11); Infrastructure & Operations Owner (ST-12); Director of Quality + Head of Frontend Engineering (ST-13)
**Estimated effort:** ~1.5 days
**Risk IDs:** None (RISK-02 is release-level, mitigated by 2-sprint phasing)
**Execution sequence:** 1 (first to merge; autonomous items complete fastest)
**Branch:** `exec/2026-06-24__release-v6.2/EPIC-03`
**execution_state.json:** Append EPIC-03 section to EPIC-01-owned file (check for file existence before creating)

---

##### ST-10 — execution_prompt autonomous class hard gate (BLG-GOV-135)

**Owner:** Head of Specs Team
**Estimated effort:** < 0.25 day
**Delegation class:** autonomous
**Dependencies:** None (may batch with ST-11)
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Staging-only ACs:** None

**Notes:** Governance document patch only — no backend/frontend changes. Batching with ST-11 in a single commit is explicitly supported (backlog slice: "may batch with ST-10"). When batching: commit message must include both `[ST-10][ST-11]`. CLAUDE.md §6 checklist applies: bump execution_prompt.md version, update OPERATIONAL_GUIDE §14 and §8 source prompt header, append prompt_change_log.md row for each file changed.

---

##### ST-11 — execution_prompt test_scenarios path validation (BLG-GOV-136)

**Owner:** Head of Specs Team
**Estimated effort:** < 0.25 day
**Delegation class:** autonomous
**Dependencies:** None (may batch with ST-10)
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Staging-only ACs:** None

**Notes:** Governance document patch — companion to ST-10. May be committed in the same commit as ST-10 (include `[ST-10][ST-11]` in commit message). CLAUDE.md §6 checklist applies.

---

##### ST-12 — api_performance_baseline.md — 2 new v6.1 endpoint measurements (BLG-OPS-75)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** < 0.25 day
**Delegation class:** autonomous
**Dependencies:** None
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Staging-only ACs:** AC-03 (measurement values — must come from Render internal logs or live endpoint test on staging; cannot be computed from code)

**Notes:** Measurements for `GET /portfolio/sector-weights` and `GET /trade-plans/setup-quality-score` (both shipped v6.1). Values (p50, p95) must be sourced from Render logs or a direct staging endpoint test — values cannot be fabricated. If logs are unavailable, defer this story and file a new BLG-OPS item targeting the next sprint when logs are accessible.

---

##### ST-13 — Playwright spec auto-registration via glob pattern (BLG-QA-62)

**Owner:** Director of Quality; Head of Frontend Engineering
**Estimated effort:** ~0.75 day
**Delegation class:** delegated_qa
**Dependencies:** None
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Staging-only ACs:** None

**Notes:** CI/CD change — replaces explicit spec file list in `playwright.yml` with a glob (`tests/e2e/**/*.spec.js`). Must confirm all existing specs still run (AC-02) before merging. Priority carry-forward from v6.1 closure (recommendation: "within next 2 sprints"). This story closes that obligation.

---

### Sprint 2 (Conditional — §13 review required before execution begins)

**Pre-condition gate:** Strategy Rules & System Intent Owner §13 review for BLG-FEAT-50 and BLG-FEAT-51 must be recorded in `docs/product/decisions/decisions--2026-06-24__release-v6.2.md` before Sprint 2 execution begins. EPIC-02 stories must not enter `in_progress` until this gate is confirmed.

**Data pre-condition:** All EPIC-01 stories (ST-01, ST-03, ST-05) must be verified and live before ST-06 execution begins — daily briefing context assembly requires `current_trailing_stop`, `exit_rebalance` signals, and `risk_off_exit` alerts to be available from the live backend.

---

#### EPIC-02 — AI Intelligence Layer

**Maps to:** S2-05, S2-06 (BLG-FEAT-50, BLG-FEAT-51)
**Owner:** Head of Engineering
**Estimated effort:** ~4 days
**Risk IDs:** RISK-01 (§13 review required — see Outstanding Actions)
**Execution sequence:** 3 (Sprint 2 — after Sprint 1 fully merged and verified)
**Branch:** `exec/2026-06-24__release-v6.2/EPIC-02`
**execution_state.json:** Append EPIC-02 section; rebase onto main after EPIC-01 + EPIC-03 merge

---

##### ST-06 — AI daily briefing — backend endpoint

**Owner:** Head of Engineering
**Estimated effort:** ~2 days
**Delegation class:** delegated_backend
**Dependencies:** ST-01, ST-03, ST-05 (trailing stop data, rebalance signals, risk-off alerts must be live); ST-06 is the context assembly foundation for ST-07 and ST-08
**Status at sprint open: conditional — §13 review + EPIC-01 completion required**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Staging-only ACs:** None

**Notes:** Uses `claude-sonnet-4-6` model. Token usage must be logged to `claude_audit_log` per established pattern (AC-05). AI advisory metadata field `advisory: true` required in response (AC-06). New endpoint `POST /ai/daily-briefing` must be added to `docs/reference/openapi.yaml` and a corresponding `## POST /ai/daily-briefing` entry in a file in `docs/specs/api_contracts/` in the same commit (CLAUDE.md §2). Backend route must be registered in `backend/routers/test.py` and `src/pages/SystemStatus.js` fallback count updated in the same commit.

---

##### ST-07 — AI Daily Briefing card — frontend

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_frontend
**Dependencies:** ST-06
**Status at sprint open: conditional — §13 review + EPIC-01 completion required**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Staging-only ACs:** AC-04 (AI advisory label — "AI Advisory — all actions require your confirmation" wording and styling requires human staging sign-off; card presence, content structure, and Regenerate button covered by Playwright)

**Notes:** Design spec: `docs/design/2026-06-24__release-v6.2/ai-daily-briefing-card/ux_spec.md`; Frontend spec: `docs/specs/frontend/pages/dashboard.md` v2.3. "Today's Briefing" card on Dashboard page.

---

##### ST-08 — Conversational AI trade advisor — backend endpoint

**Owner:** Head of Engineering
**Estimated effort:** ~1 day
**Delegation class:** delegated_backend
**Dependencies:** ST-06 (shared context assembly pattern)
**Status at sprint open: conditional — §13 review + EPIC-01 completion required**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Staging-only ACs:** None

**Notes:** Uses `claude-sonnet-4-6` model. Stateless per request — no session memory across calls (AC-05). New endpoint `POST /ai/chat` must follow the same commit rules as ST-06: openapi.yaml entry, api_contracts/ entry, test.py registration, SystemStatus.js fallback count update.

---

##### ST-09 — AI chat widget — frontend

**Owner:** Head of Engineering
**Estimated effort:** ~0.5 day
**Delegation class:** delegated_frontend
**Dependencies:** ST-08
**Status at sprint open: conditional — §13 review + EPIC-01 completion required**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Staging-only ACs:** AC-03 (AI advisory label and non-executability of trade actions requires human staging sign-off; widget presence, submit/response flow, loading state, and error state covered by Playwright)

**Notes:** Design spec: `docs/design/2026-06-24__release-v6.2/ai-chat-widget/ux_spec.md`; Frontend spec: `docs/specs/frontend/pages/positions.md` v1.8. Canonical placement: **Positions page**. Signals page placement is a capacity-dependent stretch goal — do not treat as in-scope without explicit capacity confirmation at execution; file a follow-on backlog item if deferred.

---

## Capacity Summary

| Metric | Sprint 1 | Sprint 2 | Overall |
|--------|---------|---------|---------|
| Confirmed capacity | ~12–14 days | ~12–14 days | ~24–28 days |
| Estimated effort (in-scope) | ~8.5 days | ~4 days | ~12.5 days |
| Utilisation | ~61–71% | ~29–33% | ~45–52% |
| Over-allocation | No | No | No |

Capacity WARN from release planning resolved by 2-sprint phasing (see sprint_capacity.md and sprint_planning_notes.md).

---

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | No items deferred from the authoritative backlog slice |

---

## Deferred Execution Blockers Accepted

*(Section not applicable — `deferred_execution_blockers` was empty in state.json)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| §13 compliance review for BLG-FEAT-50 (AI daily briefing) and BLG-FEAT-51 (AI chat advisor) — confirm advisory-only, no automated execution; record in decisions document | Strategy Rules & System Intent Owner | **Yes** |
| Sprint goal sign-off (Sprint 1 + Sprint 2 goals) | Product Owner | **Yes** |
| Capacity WARN acknowledgement (2-sprint plan confirmed) | Product Owner | **Yes** |
| pip-audit run before sprint execution begins | Head of Engineering | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — Sprint 1 (strategy parity cluster) and Sprint 2 conditional (AI intelligence layer)
**Scope confirmed:** Confirmed — Sprint 1: 9 stories (EPIC-01 ST-01–05 + EPIC-03 ST-10–13); Sprint 2 conditional: 4 stories (EPIC-02 ST-06–09)
**Capacity confirmed (2-sprint plan acknowledged):** Confirmed — WARN from release planning resolved by 2-sprint phasing; per-sprint effort within 12–14 day baseline
**Deferred execution blockers accepted:** N/A
**Signed off by:** Product Owner
**Date:** 2026-06-24
