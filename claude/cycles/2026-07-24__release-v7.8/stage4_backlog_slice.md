**Owner:** Head of Specs Team
**Status:** Active
**Release:** v7.8
**Cycle:** 2026-07-24__release-v7.8
**Last Updated:** 2026-07-24

---

# Stage 4 Backlog Slice — v7.8

<!-- release-plan-marker: RP:v7.8:2026-07-24__release-v7.8 -->

EPIC-01, EPIC-03, EPIC-04, EPIC-05, EPIC-06 are **conditional**, not firm — see `release_plan.md` RISK-01. Sprint Planning may not seal these stories until `run design-gate --cycle 2026-07-24__release-v7.8` PASSes (all 5 carry observable UI acceptance criteria). EPIC-02, EPIC-07 through EPIC-12 have no Design Gate dependency — no observable UI acceptance criteria.

`BLG-FEAT-73` and `BLG-FEAT-74` are **not** included in this slice — PO disposition Option (b), removed from the Now-horizon per the STEP 1.4a Perennial-Return Check (see `release_plan.md` §Scope, `run_manifest.md`).

## EPIC-01 — In-app "what's new" panel for most recent release
**Maps to:** S2-01
**Backlog source:** `BLG-FE-128`
**Sequencing:** Conditional on Design Gate PASS (RISK-01); no blocking dependency

### ST-01 — Build in-app "what's new" panel sourced from changelog.md
**Acceptance Criteria:**
- Panel (Dashboard section or dedicated "What's New" entry) shows the most recent release's `### Changes shipped` entries from `docs/product/changelog.md`
- Panel updates automatically on the next release without manual wiring (parses the changelog's most recent version block, not a hardcoded copy)
- Empty/loading states follow the existing `DataState` pattern (`design_system.md`)

---

## EPIC-02 — Automated Telegram changelog digest after each release
**Maps to:** S2-02
**Backlog source:** `BLG-FEAT-84`
**Sequencing:** No dependency; no Design Gate requirement (no UI surface)

### ST-02 — Send Telegram digest of shipped items on post-ship closure
**Acceptance Criteria:**
- Digest sent automatically as part of Post-Ship Closure, reusing existing Telegram notification infrastructure (shipped v2.4)
- Digest content matches the release's `### Changes shipped` entries in `docs/product/changelog.md`
- Failure to send (e.g. Telegram API error) does not block Post-Ship Closure — logged, not fatal

---

## EPIC-03 — Accessibility pass on v7.7 notification UX components
**Maps to:** S2-03
**Backlog source:** `BLG-FE-127`
**Sequencing:** Conditional on Design Gate PASS (RISK-01); standalone, no dependencies

### ST-03 — Contrast/focus-state accessibility pass on v7.7 notification UX
**Acceptance Criteria:**
- Contrast and focus-state accessibility review performed specifically on the v7.7 notification/digest surface consolidation (`BLG-FE-114`) and shared standing-alert component (`BLG-FE-120`)
- Any findings fixed directly if trivial, or filed as follow-up backlog items (per `/backlog-add`) if not
- Result recorded (pass / fixed / follow-up filed) in QA evidence

---

## EPIC-04 — Dark-mode contrast audit across Base44-generated pages
**Maps to:** S2-04
**Backlog source:** `BLG-FE-125`
**Sequencing:** Conditional on Design Gate PASS (RISK-01); standalone, no dependencies

### ST-04 — Consolidated dark-mode contrast audit across shipped pages
**Acceptance Criteria:**
- Dark-mode contrast audit run across all shipped Base44-generated pages (not per-page ad hoc)
- Findings filed as a consolidated batch of follow-up items (one filing, not one per page) or fixed directly if trivial
- Audit method and coverage recorded in QA evidence

---

## EPIC-05 — Monthly realized P&L CSV export
**Maps to:** S2-05
**Backlog source:** `BLG-FEAT-81`
**Sequencing:** Conditional on Design Gate PASS (RISK-01); reuses existing tax-year export reconciliation logic (v7.6, `BLG-FEAT-79`)

### ST-05 — Add monthly CSV export option alongside existing tax-year export
**Acceptance Criteria:**
- Monthly realized P&L CSV export available as an option alongside the existing tax-year export
- Monthly figures reconcile against the existing tax-year export for the same period (no double-counting or drift)
- Export trigger UI follows existing export-control patterns on the page it's added to

---

## EPIC-06 — AI usage spend trend dashboard (Gemini/Claude, per release cycle)
**Maps to:** S2-06
**Backlog source:** `BLG-FEAT-82`
**Sequencing:** Conditional on Design Gate PASS (RISK-01); extends the existing v7.6 AI Usage & Costs settings view (`BLG-FEAT-77`)

### ST-06 — Add per-cycle AI spend trend chart to AI Usage & Costs view
**Acceptance Criteria:**
- Trend chart added to the existing AI Usage & Costs settings view, showing at least the last 6 release cycles' spend
- Data sourced from existing `gemini_audit_log` / Claude cost tracking — no new data collection required
- Chart follows existing chart styling conventions on the page

---

## EPIC-07 — Scheduled rotation-and-audit cadence for third-party API keys
**Maps to:** S2-07
**Backlog source:** `BLG-SEC-20`
**Sequencing:** No dependency; no Design Gate requirement (documentation/process only)

### ST-07 — Define rotation-and-audit schedule for all external API keys
**Acceptance Criteria:**
- Rotation-and-audit schedule documented for all 5 external key types (Yahoo Finance, Alpaca, Gemini, Claude, Telegram), building on the existing `alpaca_key_rotation_policy.md` pattern
- First rotation date set per key
- Cybersecurity & Trust Lead sign-off

---

## EPIC-08 — Rate-limiting review of public-facing endpoints
**Maps to:** S2-08
**Backlog source:** `BLG-SEC-21`
**Sequencing:** No dependency; no Design Gate requirement (backend/policy only)

### ST-08 — Identify and remediate endpoints with no documented rate limit
**Acceptance Criteria:**
- List of endpoints with zero documented rate limit produced (extends `BLG-SEC-18`'s general audit, prioritising undocumented-limit endpoints specifically)
- Each listed endpoint either given a documented limit or explicitly accepted as low-risk (recorded, not silently skipped) — see RISK-04
- Cybersecurity & Trust Lead sign-off

---

## EPIC-09 — Shared retry/backoff decorator for external data calls
**Maps to:** S2-09
**Backlog source:** `BLG-BE-71`
**Sequencing:** No dependency; no Design Gate requirement (backend only) — see RISK-02 (scope bounded to proof-of-pattern)

### ST-09 — Extract shared retry/backoff decorator and migrate highest-traffic call site
**Acceptance Criteria:**
- Shared retry/backoff decorator or helper added with unit tests
- At least the highest-traffic external call site (Yahoo Finance or Alpaca, whichever is higher-traffic) migrated to the shared helper as proof of pattern
- No full retrofit required this cycle — remaining call sites migrate incrementally in future cycles

---

## EPIC-10 — Flaky-test quarantine process for the Playwright suite
**Maps to:** S2-10
**Backlog source:** `BLG-QA-117`
**Sequencing:** No dependency; no Design Gate requirement (process only)

### ST-10 — Define and apply flaky-test quarantine mechanism
**Acceptance Criteria:**
- Quarantine tag/process defined (e.g. `test.fixme` with a tracked follow-up item) and documented
- Process applied to any currently-known flaky test in the Playwright suite, if one exists at implementation time
- Director of Quality sign-off

---

## EPIC-11 — Contract tests for highest-traffic frontend/backend endpoints
**Maps to:** S2-11
**Backlog source:** `BLG-QA-119`
**Sequencing:** No dependency; no Design Gate requirement (backend/test tooling only) — see RISK-03 (pilot endpoint selection to be confirmed by Head of Engineering before implementation)

### ST-11 — Add pilot contract tests for 3 highest-traffic endpoints
**Acceptance Criteria:**
- Lightweight contract tests added for the 3 highest-traffic endpoints as a pilot (candidates: positions, trades, dashboard — Head of Engineering to confirm selection per RISK-03 before implementation)
- Contract tests added and passing in CI for all 3 pilot endpoints
- Approach documented for extending to additional endpoints in future cycles

---

## EPIC-12 — Automated lint check for API contract `##` heading level
**Maps to:** S2-12
**Backlog source:** `BLG-OPS-117`
**Sequencing:** No dependency; no Design Gate requirement (CI tooling only)

### ST-12 — Add CI lint step for API contract heading-level compliance
**Acceptance Criteria:**
- Lightweight CI lint step added scanning `docs/specs/api_contracts/*.md` for `## METHOD /path` heading-level compliance (catches the documented `###`-level silent-fail case from `CLAUDE.md` §2)
- Lint step confirmed to catch a deliberately-miscoded test heading (negative test) before merge
- Lint step runs ahead of / alongside the existing OpenAPI Drift Detection gate

---

```yaml
artifacts.stage4_backlog_slice: pass
attributes.backlog_committed: true
status: Committed
```
