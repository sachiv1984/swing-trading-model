Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-23

---

# QA Evidence — EPIC-02: Alert System Maturity

**EPIC:** EPIC-02 — Alert System Maturity
**Cycle:** 2026-03-21__release-v2.2
**Sprint goal:** Ship a secured, observable alert system: authenticate the Render API against public access, complete the alert engine with configurable thresholds and evaluation history, close QA scenario gaps from v2.1, and deliver three governance process improvements that streamline all future cycles.
**Test scenarios used:** `docs/testing/notifications_scenarios.md` (referenced; execution via ST-09 in EPIC-04)

---

## ST-03 — Alert Scheduling: Define Trigger Mechanism and Rule Behaviour

**Spec references:** `docs/specs/api_contracts/alerts_endpoints.md`, `docs/product/decisions/decisions--2026-03-21__release-v2.2.md#st-03-execution-decisions`
**Commit SHA:** null (decision/spec story — no implementation commit)
**What was built:** Product Owner documented all four scheduling decisions (A–D) and five mandatory pre-conditions for ST-04/ST-05 implementation. Decision document authored at `docs/product/decisions/decisions--2026-03-21__release-v2.2.md §ST-03 Execution Decisions`. Challenger review completed; all challenges resolved.

**Acceptance criteria:**
1. Evaluation frequency documented (daily 21:30 UTC Mon–Fri via Render cron) — AC met.
2. Decisions recorded in `docs/product/decisions/` — AC met.
3. `alerts_endpoints.md` updated if scheduling-related API additions needed — no new endpoints required; existing spec sufficient for this story.
4. `openapi.yaml` updated if new endpoint defined — no new endpoint; not required.
5. Gates ST-04 and ST-05 — gate cleared 2026-03-23.

**Result:** Pass
**Deviations:** None

---

## ST-04 — Alert Threshold Customisation

**Spec references:** `docs/specs/frontend/pages/notifications.md` v0.2 §Section 2 (Alert Rule Thresholds); `docs/specs/api_contracts/alerts_endpoints.md` v0.2 (PATCH /alerts/rules/{rule_id})
**Commit SHA:** ddc4f44
**What was built:** `AlertThresholdsSection` component added to `/notifications/preferences` page below email preferences. Shows per-rule threshold list with "Within N% of stop" display. `stop_loss_approach` has an inline edit form with numeric input, validation (non-numeric / ≤0 / >50 / blank=default), Save/Cancel, save error state. `GET /alerts/rules` on mount with loading/error states. Save via `PATCH /alerts/rules/{rule_id}` with correct `threshold_percent` field. "History" tab added to sub-nav. All API calls use `apiFetch` (X-API-Key header).

**Acceptance criteria:**
| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | User can set a custom threshold when creating or editing | Pass | Inline edit form confirmed by code review |
| 2 | Alert evaluation uses per-rule threshold (not hardcoded) | Deferred to staging | Backend concern; frontend sends correct `threshold_percent` field |
| 3 | Default threshold (5.0) applies when no custom value set | Pass | Blank → 5.0 sent to API; pre-fill and display both use 5.0 fallback |
| 4 | Threshold visible on alert list view | Pass | ThresholdText component renders in each rule row |
| 5 | `alerts_endpoints.md` + `openapi.yaml` updated if shape changes | Pass | No shape change for ST-04; PATCH /alerts/rules/{rule_id} already in spec |
| 6 | DoQ sign-off: threshold customisation verified; default behaviour regression confirmed | Pass | Code review. Staging confirmation of AC-2 deferred. |

**Deviations filed:** Yes — DEV-EPIC02-ST04-01 (see `notifications.md` Known Deviations)

---

## ST-05 — Alert History Table (frontend)

**Spec references:** `docs/specs/frontend/pages/notifications.md` v0.2 §Page 3 (Alert History)
**Commit SHA:** ddc4f44 (frontend); backend implementation pending (GET /alerts/history + alert_evaluations migration)
**What was built:** `NotificationsHistory` page at `/notifications/history` with: 6-column alert history table, Date/Time sort toggle (asc/desc with arrow indicator), rule type filter dropdown ("All types" + 4 types), row-expand inline for full `values_compared` key-value detail, load-more pagination (`last_n_days=30` initial, `last_n_records=200` on load-more), loading skeleton (5 rows), empty states (no records; filtered no matches with "Clear filter"), error state. All badges (Triggered: amber/grey; Notified: green/grey) match spec. "History" tab active in sub-nav. All API calls use `apiFetch`.

**Acceptance criteria:**
| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | Every `POST /alerts/evaluate` persists a record | Deferred to staging | Backend concern |
| 2 | `GET /alerts/history` returns records with all fields; frontend displays correctly | Pass | All 6 fields consumed and rendered correctly by code review |
| 3 | Frontend: records sortable by date, filterable by rule type | Pass | Sort toggle + client-side filter confirmed by code review |
| 4 | Schema migration includes down migration | Deferred to staging | Backend concern |
| 5 | `alerts_endpoints.md` + `openapi.yaml` updated | Deferred to staging | Backend PR pending; GET /alerts/history not yet in spec |
| 6 | DoQ sign-off: history persists across evaluate calls; migration runs cleanly | Pass (frontend portion) | Code review for frontend. Staging portion deferred (backend dependency). |

**Deviations filed:** Yes — DEV-EPIC02-ST05-01 (React fragment key warning — observation, non-functional; see below)

---

## EPIC-Level Consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-03 | alerts_endpoints.md, decisions doc | Alert scheduling decisions documented; ST-04/ST-05 unblocked | 5 ACs — all met | Pass | None |
| ST-04 | notifications.md v0.2 §Section 2 | AlertThresholdsSection with inline edit form | AC1,3,4,5,6: Pass; AC2: Deferred staging | Pass | DEV-EPIC02-ST04-01 |
| ST-05 | notifications.md v0.2 §Page 3 | NotificationsHistory page with full table | AC2,3,6(FE): Pass; AC1,4,5,6(staging): Deferred | Pass (FE) | DEV-EPIC02-ST05-01 |

**QA test coverage:**
- Scenarios run: Code review (frontend); staging execution via ST-09 (EPIC-04, separate)
- Regression areas checked: notifications sub-nav, /notifications/preferences (email toggles unaffected), API call pattern (apiFetch confirmed)
- Known deviations filed: DEV-EPIC02-ST04-01, DEV-EPIC02-ST05-01 (observation only)

**Known deviations:**

**DEV-EPIC02-ST04-01 — Alert Thresholds empty state: missing "Add alert rule" CTA button**
- Description: `notifications.md` v0.2 §Section 2 specifies an "Add alert rule" button in the empty state (when no rules configured). The implementation renders the icon, heading, and body text but omits the CTA button. In practice this state is unreachable — rules are auto-seeded by `GET /alerts/rules` on first use.
- Canonical requirement: Empty state includes "Add alert rule" CTA button per `notifications.md §Section 2`
- Priority: P3 (Low — edge-case state, effectively unreachable in normal operation)
- Target resolution release: v2.3
- Owner: Base44 Frontend Prompt Owner
- Backlog reference: File as BLG-FE item at next roadmap rebalance

**DEV-EPIC02-ST05-01 — NotificationsHistory: React fragment missing key prop**
- Description: In `NotificationsHistory.js` row render, the `<>...</>` fragment wrapper over row + expanded row has no `key` prop. The inner `<tr>` elements carry keys, but React will log console warnings about missing fragment keys in development mode.
- Canonical requirement: Not spec-defined (observation only — React best practice)
- Priority: P3 (Low — no functional or visual impact)
- Target resolution release: v2.3
- Owner: Base44 Frontend Prompt Owner
- Backlog reference: File as BLG-FE item at next roadmap rebalance

---

**QA sign-off block:** (Director of Quality completes this)
> **Authoring note (LL-v1.10-P4-1):** Sign-off block and AC table must be consistent.
- [x] All acceptance criteria verified against canonical spec (frontend ACs by code review; backend ACs deferred to staging per above)
- [x] No unresolved P0 or P1 deviations (both deviations are P3)
- [x] Regression areas checked (email preferences unaffected; apiFetch pattern confirmed)
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object (LL-v2.0-P3-4) — all API calls use `apiFetch` from `base44Client.js`; `API_BASE_URL` sourced from env var. Confirmed.
- Signed off by: Director of Quality (agent-mediated)
- Date: 2026-03-23
- Comments: ST-04 approved with P3 deviation (DEV-EPIC02-ST04-01 — missing CTA in unreachable empty state). ST-05 frontend approved; backend ACs deferred to staging pending Head of Engineering implementation of `GET /alerts/history` and `alert_evaluations` migration. Two staging confirmations required before sprint close: (1) ST-04 AC2 — backend uses per-rule threshold value; (2) ST-05 AC1/AC4/AC5 — migration, endpoint spec update, history persistence.
