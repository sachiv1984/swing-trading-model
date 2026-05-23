**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-23
**Cycle:** 2026-05-22__release-v4.0
**Release:** v4.0
**Sprint Goal:** Deliver Arc 5 compliance analytics metrics, harden ticker universe with symbol validation, establish Gemini AI compliance infrastructure, automate CI/CD staging deployment, and remediate the starlette authentication vulnerability.
**Backlog Slice Source:** amended: `claude/cycles/2026-05-22__release-v4.0/amendments/AMD-20260523-01/amended_backlog_slice.md`

---

# Sprint Backlog — 2026-05-22__release-v4.0

## Sprint Scope

### Merge Order (Sprint 1: EPIC-01 → EPIC-02; Sprint 2: EPIC-03)

- **Sprint 1 merge sequence:** EPIC-01 merges first → EPIC-02 rebases onto main and merges second
- **Sprint 2 merge sequence:** EPIC-03 (after Sprint 1 complete)
- **execution_state.json owner:** EPIC-01
- **Shared files:** `docs/reference/openapi.yaml`, `backend/routers/test.py`, `src/pages/SystemStatus.js` — EPIC-01 owns canonical; EPIC-02 and EPIC-03 must rebase onto main after EPIC-01 merges before finalising changes to these files

---

### EPIC-01 — Arc 5 Analytics Metrics

**Maps to:** S2-01, S2-02
**Owner:** Metrics & Analytics Owner; QA Lead
**Estimated effort:** ~5 days (M+S+S+S)
**Risk IDs:** RISK-02 (resolved — metric definition confirmed)
**Execution sequence:** 1

#### ST-01 — SI-01 pass/fail rate by rule — backend metric endpoint

**Owner:** Metrics & Analytics Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `amended_backlog_slice.md` → `stage4_backlog_slice.md#ST-01` (BLG-FEAT-36)

**Key AC summary:**
- `GET /analytics/arc5-compliance` or dedicated endpoint returns `validation_pass_rate_by_rule` per rule_type
- Canonical definition: pass_count / (pass_count + fail_count) per rule_type, rolling 7d (default) / 30d
- Backend analysis of pre-entry validation log schema completed; any required schema addition documented
- Metrics definition registered in `metrics_definitions.md`

**Dependencies:** None
**Notes:** RISK-02 resolved. Metric definition confirmed by Metrics & Analytics Owner 2026-05-23. Endpoint feeds analytics.md §19 `GET /analytics/arc5-compliance`. New endpoint must be registered in `backend/routers/test.py` and `docs/reference/openapi.yaml` per CLAUDE.md §2.
**Staging-only ACs:** None

---

#### ST-02 — Red flag event frequency metric — backend + frontend

**Owner:** Metrics & Analytics Owner
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-FEAT-37

**Key AC summary:**
- Three named metrics: `events_per_week`, `override_rate`, `event_type_distribution`
- Backend aggregate query on red_flag_events; metrics registered in metrics_definitions.md
- Frontend: displays in analytics.md §19 as "Red Flag Events/Week", "Override Rate", "Top Rule Breach" stat cards per approved UX spec `docs/design/2026-05-22__release-v4.0/arc5-analytics-metrics/ux_spec.md`

**Dependencies:** None (independent of ST-01; shares §19 section endpoint)
**Notes:** Frontend spec: analytics.md v1.8 §19. Design gate cleared. `delegated_frontend` — requires frontend implementation of §19 stat cards.
**Staging-only ACs:** None

---

#### ST-03 — E2E Playwright test — SI-01→SI-03 integration path

**Owner:** QA Lead
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-QA-25

**Key AC summary:**
- Full SI-01→SI-03 path: navigate to position → trigger pre-entry validation → acknowledge override → navigate to RFJ → verify event present with correct metadata
- Cover: filter by event type → verify filtered results contain override event
- Test passes in CI; integrated into existing Playwright suite

**Dependencies:** SI-01 (v3.8) ✅; SI-03 (v3.9) ✅
**Notes:** Sequence last in EPIC-01 to allow ST-01/ST-02 to land first.
**Staging-only ACs:** None

---

#### ST-04 — Trade plan adherence rate metric — backend + frontend

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-FEAT-39

**Key AC summary:**
- Named metric: `trade_plan_adherence_rate = trades_with_plan_id / total_closed_trades`
- Backend aggregate query on closed trades; registered in metrics_definitions.md
- Frontend: "Trade Plan Adherence" stat card in analytics.md §19 per UX spec

**Dependencies:** None (independent)
**Notes:** Frontend spec: analytics.md v1.8 §19. Design gate cleared. Gate condition (plan_id linkage actively captured) confirmed by PO.
**Staging-only ACs:** None

---

### EPIC-02 — Ticker Quality & Security

**Maps to:** S2-03, S2-04
**Owner:** Head of Backend Engineering; Cybersecurity Lead
**Estimated effort:** ~2 days (S+XS+XS)
**Risk IDs:** None
**Execution sequence:** 2

#### ST-05 — Validate ticker symbol on add

**Owner:** Head of Backend Engineering
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-BE-15

**Key AC summary:**
- `POST /ticker-universe` calls Yahoo Finance to validate ticker existence
- Invalid ticker → 400/422 with message "Ticker [SYMBOL] not found — please check the symbol and market"; ticker not saved
- Valid ticker → success; sector/industry optionally auto-populated
- Frontend displays error message inline below input field per ticker_universe.md v1.1 §8

**Dependencies:** None
**Notes:** Frontend spec: ticker_universe.md v1.1 §8. Design Pre-Approved. New endpoint test in `backend/routers/test.py` per CLAUDE.md §2.
**Staging-only ACs:** `[staging-only evidence]` AC — "invalid ticker returns error (not saved)": requires live Yahoo Finance lookup; cannot be verified in CI (network-dependent). If staging sign-off deferred to post-merge, backlog item must be filed before PR opens.

---

#### ST-06 — Red flag endpoint auth and PII review

**Owner:** Cybersecurity Lead
**Estimated effort:** XS (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-GOV-37

**Key AC summary:**
- API key auth confirmed active on `GET /portfolio/red-flag-journal`
- Response payload reviewed: PII-free, no sensitive strategy data
- Findings documented in `docs/security/`
- If gap found: remediation backlog item filed

**Dependencies:** None
**Notes:** Review task only; no code change unless gap found. Sequence after ST-05/ST-13 to allow those to land first.
**Staging-only ACs:** None

---

#### ST-13 — Starlette security upgrade to ≥1.0.1

**Owner:** Head of Backend Engineering
**Estimated effort:** XS (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:**
- `starlette>=1.0.1` present in `backend/requirements.txt`
- `pip-audit -r backend/requirements.txt` no longer reports PYSEC-2026-161
- Existing backend test suite passes with new starlette version
- No functional regressions in any endpoint

**Dependencies:** None — sequence first in EPIC-02 (security fix)
**Notes:** Added via AMD-20260523-01 (CVE PYSEC-2026-161). Purely a dependency version bump; no code changes expected. Pin to minimum version `starlette>=1.0.1` to maintain compatibility with FastAPI.
**Staging-only ACs:** None

---

### EPIC-03 — AI Governance & CI/CD

**Maps to:** S2-05, S2-06
**Owner:** AI Compliance Officer; FinOps; Infrastructure Owner
**Estimated effort:** ~6 days (S+M+S+M)
**Risk IDs:** RISK-03 (OPS-27 build-minute assessment — Sprint 2 pre-work)
**Execution sequence:** 3

#### ST-12 — Gemini Flash base wiring

**Owner:** Head of Backend Engineering
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-BE-19

**Key AC summary:**
- `google-generativeai` in `requirements.txt`; `GEMINI_API_KEY` in `.env.example`
- `backend/services/gemini_service.py`: `generate_setup_thesis(ticker, signal_data, plan_data) -> dict` using `gemini-1.5-flash`
- `POST /trade-plans/{plan_id}/generate-thesis` endpoint — returns `{thesis, model_version, prompt_version}` when key set; graceful error when key absent
- Frontend: "Generate Thesis" button on TradePlan page calls endpoint and populates `setup_thesis` textarea
- New endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml`

**Dependencies:** None (first story in EPIC-03; must complete before ST-07 and ST-08 begin)
**Notes:** Added via AMD-20260523-01. Hard prerequisite for ST-07 and ST-08. Frontend: TradePlan page button. `delegated_frontend` — requires frontend implementation.
**Staging-only ACs:** `[staging-only evidence]` — "returns thesis when GEMINI_API_KEY set": requires live Gemini API key; cannot verify in CI. "Returns graceful error when key absent" is testable in CI (mock absent key).

---

#### ST-07 — Gemini audit trail — log AI thesis generation calls

**Owner:** AI Compliance Officer; Head of Backend Engineering
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-GOV-35

**Key AC summary:**
- Audit log created for each Gemini thesis generation call
- Record fields: model_version, prompt_version, input_hash, output_hash, generated_at
- Retention policy enforced (90-day minimum)
- No performance impact on thesis generation response time

**Dependencies:** ST-12 must complete first
**Notes:** Append-only audit table or structured log. No user-facing change.
**Staging-only ACs:** None (audit log verifiable via integration test)

---

#### ST-08 — Gemini cost tracking — token usage and cost per call

**Owner:** FinOps & Resource Architect
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-OPS-26

**Key AC summary:**
- Gemini API call count logged per request
- Monthly aggregate computable
- Alert threshold defined and documented (>80% free-tier monthly limit)
- No change to user-facing behaviour

**Dependencies:** ST-12 must complete first
**Notes:** Backend instrumentation only. No UI change.
**Staging-only ACs:** None

---

#### ST-09 — CI/CD automated staging re-deploy on main merge

**Owner:** Infrastructure Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `amended_backlog_slice.md` → BLG-OPS-27

**Key AC summary:**
- Staging auto-deploys on main merge for code changes
- Documentation-only commits do not trigger a deploy
- Free-tier build minute impact assessed and documented
- BLG-OPS-25 dependency satisfied (deploy hook available)

**Dependencies:** None (independent)
**Notes:** RISK-03 — build-minute filter design must be confirmed before implementation begins (RISK-03 acceptance by PO required during Sprint 2). Add file-change path filter to GitHub Actions workflow.
**Staging-only ACs:** `[staging-only evidence]` — "staging auto-deploys on main merge": requires live Render environment; cannot verify in CI. If staging sign-off deferred to post-merge, backlog item must be filed before PR opens.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~10 days |
| Total estimated effort (in-scope) | ~13 days |
| Utilisation | ~130% |
| Over-allocation | Yes — accepted by PO (WARN acknowledged; BLG-BE-19 effort was implicit in prior estimates) |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-10 | EPIC-04 | PT-04 gate not met — <20 closed trades |
| ST-11 | EPIC-04 | PT-04 gate not met — same gate condition |

## Deferred Execution Blockers Accepted

*(section omitted — `deferred_execution_blockers` was empty in release plan)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-03: OPS-27 build-minute assessment | Infrastructure Owner | No (Sprint 2 pre-work) |
| BLG-SPEC-33 + BLG-SPEC-34 backlog archive | PMO Lead | No (next groom run) |
| Prompt change log verification (sprint_planning v3.6, execution v3.27) | Head of Specs Team | No (hygiene) |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed — 2026-05-23
**Scope confirmed:** confirmed — 2026-05-23
**Capacity confirmed:** confirmed — WARN acknowledged; over-allocation accepted
**Deferred execution blockers accepted:** N/A
**Signed off by:** Product Owner
**Date:** 2026-05-23
