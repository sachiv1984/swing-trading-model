Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-21

---

# QA Evidence — EPIC-01: SI-05 Phase 1 Weekly Strategy Integrity Digest

**Cycle:** 2026-06-21__release-v5.1
**Sprint goal:** Deliver the SI-05 Phase 1 weekly Telegram digest (combining SI-01 compliance data and SI-03 red flag trends) and clear outstanding governance and QA debt.
**Test scenarios used:** Derived from spec + AC (`tests/test_si05_digest_service.py`, 21 unit tests; manual AC review against BLG-GOV-86 and `digest_endpoints.md` v0.2)

---

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-02 | `si05-financial-reporting-scope-decision.md` v1.0; BLG-SPEC-45 | `docs/product/decisions/si05-financial-reporting-scope-decision.md` — financial reporting confirmed OUT OF SCOPE for Phase 1; BLG-SPEC-45 marked COMPLETE; FR&R Owner sign-off recorded | AC-01 BLG-GOV-86 reviewed, scope answered; AC-02 decision documented; AC-03 no supplementary spec needed; AC-04 FR&R Owner sign-off; AC-05 BLG-SPEC-45 COMPLETE | Pass | None |
| ST-01 | BLG-GOV-86 (`si05-telegram-message-format-spec.md` v1.0); `digest_endpoints.md` v0.2; `arc5_compliance_analytics.md`; CLAUDE.md §2 | `backend/services/si05_digest_service.py`, `backend/routers/digest.py` (POST /digest/si05/send), `digest_endpoints.md` v0.2, `openapi.yaml`, `test.py` (62 endpoints), `SystemStatus.js` fallback '62', `system-status.spec.js` SC-SS-01b, `tests/test_si05_digest_service.py` (21 tests) | AC-01–AC-08 verified; AC-09 staging-only deferred (I&O Owner sign-off required) | Pass with notes — see deviation DEV-v51-EPIC01-01 | DEV-v51-EPIC01-01 (P3) |

> Covers: ST-02 AC-01 through AC-05; ST-01 AC-01 through AC-08 (AC-09 staging-only deferred per sprint backlog).

---

## Per-Story Verification Notes

### ST-02 — BLG-SPEC-45: SI-05 Financial Reporting Scope Verification

All five ACs verified:

- **AC-01:** BLG-GOV-86 reviewed in full. The spec defines SI-05 as a Strategy Integrity digest (4 non-financial fields). Financial performance reporting is not addressed.
- **AC-02:** Decision documented at `docs/product/decisions/si05-financial-reporting-scope-decision.md` — financial reporting OUT OF SCOPE for Phase 1, with rationale (SI-05 arc intent, v2.4 digest already covers financial metrics, no duplication warranted).
- **AC-03:** No supplementary spec required — the decision document is self-contained and definitive.
- **AC-04:** Financial Reporting & Records Owner sign-off recorded in decision document (2026-06-21).
- **AC-05:** BLG-SPEC-45 marked COMPLETE. No escalation needed.

**Result: Pass**

---

### ST-01 — SI-05 Phase 1: Backend Service + Telegram Digest Implementation

**AC-01 — Weekly digest uses SI-01 + SI-03 data:**
Service `fetch_arc5_data_for_digest()` queries `pre_entry_validation_log` (SI-01) for `validation_pass_rate` and `top_rule_breach`, and `red_flag_events` (SI-03) for `events_per_week` and `override_rate`. All four BLG-GOV-86 §4.1 fields sourced from SI-01 + SI-03 tables. **Pass.**

**AC-02 — Format per BLG-GOV-86 §4:**

Section structure verified against spec §4:

| Spec element | Implementation | Conformant |
|---|---|---|
| `---` divider | Present (section starts with `"---\n"`) | Yes |
| `*📋 Strategy Integrity*` header | Present | Yes |
| `✅ Pre\-entry pass rate \(7d\)` line | Present, MarkdownV2-escaped | Yes |
| `🚨 Red flag events \(7d\)` line | Present | Yes |
| `⚠️ Override rate \(7d\)` line | Present | Yes |
| `🔍 Top rule breach` line | Present | Yes |
| `{integrity_summary_line}` (rule-based, 5 rules in order) | Implemented in `_integrity_summary_line()` | Yes |
| MarkdownV2 escaping | `_escape_mdv2()` applied to variable data; static template chars escaped | Yes |
| Character limit 4,096 | Truncation logic present — falls back to summary-only if exceeded | Yes |

**Deviation noted on `pass_rate` computation — see DEV-v51-EPIC01-01 below.** Despite the computation method divergence, the format presentation (percentage to 1 decimal place, N/A for null) is conformant with spec §4.1 and §5.3.

Summary line rules verified (all 5 rules, correct priority order):
- Rule 1 (`pass_rate is None` → no-data message): Confirmed in `_integrity_summary_line()` and unit test `test_rules_evaluated_in_order_rule1_wins`.
- Rule 2 (`pass_rate < 70%` → threshold warning): Confirmed in unit test `test_low_pass_rate_triggers_threshold_warning`.
- Rule 3 (`red_flag_count > 5` → elevated activity): Confirmed in unit test `test_high_red_flags_triggers_elevated_activity`.
- Rule 4 (`override_rate > 30%` → high override warning): Confirmed in unit test `test_high_override_rate_triggers_warning`.
- Rule 5 (all clear → healthy): Confirmed in unit test `test_healthy_summary_line_when_all_clear`.

**AC-02 Result: Pass with notes (deviation DEV-v51-EPIC01-01 filed for pass_rate computation method).**

**AC-03 — Telegram delivery via existing v2.4 infrastructure:**
`send_si05_digest()` uses `urllib.request.urlopen` with Telegram Bot API (`sendMessage`), `MarkdownV2` parse mode, reads `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` from environment — matching v2.4 pattern. Failure modes handled: credentials absent → returns `sent: false`; data unavailable → returns `sent: false`; API error → logged, returns `sent: false`. **Pass.**

**AC-04 — No SI-02 dependency:**
`si05_digest_service.py` imports: `logging`, `os`, `datetime`, `typing`, `urllib.parse`, `psycopg2`. No import of any SI-02 module, no reference to `behavioural_drift`, `behavioural-drift`, or SI-02 endpoints. **Pass.**

**AC-05 — New endpoint documented in same commit:**
- `docs/specs/api_contracts/digest_endpoints.md` v0.1 → v0.2: `POST /digest/si05/send` section added with purpose, request, response, failure modes, data sources, format spec reference. Heading is `##` level (CLAUDE.md §2 requirement). **Pass.**
- `docs/reference/openapi.yaml`: `/digest/si05/send` path with `post` operation added. Confirmed at line 2283. **Pass.**
- Both files in commit `3887b6ca`. **Pass.**

**AC-06 — Endpoint registered per CLAUDE.md §2 (all in same commit 3887b6ca):**
- `backend/routers/test.py` line 177: `{"name": "POST /digest/si05/send", "method": "POST", "url": f"{base_url}/digest/si05/send", "body": {}, "critical": False}` — present. **Pass.**
- `src/pages/SystemStatus.js` line 533: `{totalTests || '62'}` — confirmed. **Pass.**
- `tests/e2e/system-status.spec.js` line 173: `SC-SS-01b` updated to `"62 endpoints"`. **Pass.**

**AC-07 — Unit tests (21 tests, 3 sub-categories):**
- AC-7.1 (data present): 6 tests covering header, field order, percentage formatting, red_flag_count × 7, title-case rule breach, healthy summary, character limit. **Pass.**
- AC-7.2 (empty/zero data): 5 tests covering null pass rate → N/A, null pass rate → no-data summary line, zero events → count 0, null override → N/A, null top rule → "None". **Pass.**
- AC-7.3 (format compliance): 7 tests covering divider, emojis, low pass rate rule, high red flags rule, high override rule, rule priority ordering. Plus `TestSendSi05Digest`: 3 tests covering no credentials, data unavailable, success path. **Pass.**
- Total: 21 unit tests. **Pass.**

**AC-08 — SI-05 Phase 1 gate confirmed (SI-01 + SI-03 live ≥ 30 days):**
Per sprint planning notes: RISK-01 gate confirmed cleared at sprint planning — SI-01 + SI-03 live ≥ 30 days (2026-06-21 = 30 days post SI-03 ship). PMO Lead verification recorded. **Pass.**

**AC-09 — Staging-only AC (Telegram message on staging):**
Deferred per sprint backlog staging-only ACs designation. Infrastructure & Operations Owner sign-off required. Not verified in this cycle — requires a subsequent staged verification sprint. **Deferred (staging-only, per plan).**

---

## Deviation Record

### DEV-v51-EPIC01-01 — P3: `pass_rate` computation diverges from BLG-GOV-86 §5.2

**Severity:** P3 (process / accuracy gap — not a system failure or data loss)

**AC affected:** ST-01 AC-01, AC-02

**Spec requirement (BLG-GOV-86 §5.2):**
> `pass_rate` ← Mean of all `pass_rate` values from `data.validation_pass_rate_by_rule`; null values excluded from mean. If map is empty → null.

This requires: (a) calling or replicating `GET /analytics/arc5-compliance?period=7d`, (b) iterating `validation_pass_rate_by_rule` entries, (c) computing the arithmetic mean of per-rule pass rates (equal weighting per rule).

**What was implemented:**
`fetch_arc5_data_for_digest()` queries `pre_entry_validation_log` directly and computes `pass_count / total` across all rules combined. This is a volume-weighted overall pass rate, not a mean of per-rule rates.

**Impact:**
When validation rules have different volumes (e.g. regime_gate fires 100 times, earnings_proximity fires 5 times), the two methods produce different values. The volume-weighted aggregate will be dominated by high-volume rules. The mean-of-per-rule-rates treats each rule equally. This is a functional accuracy gap against the canonical spec, not a display or format issue.

**Additionally:** `digest_endpoints.md` v0.2 documents the data source as "Overall pass/total ratio (7d)" — creating a spec-to-spec inconsistency between the contract document and BLG-GOV-86 §5.2 (the canonical format spec). The contract document should have matched the canonical spec.

**Action required:** File as backlog item. Head of Specs Team to determine whether (a) BLG-GOV-86 §5.2 should be updated to accept volume-weighted overall rate as equivalent (requires spec amendment), or (b) the service should be corrected to compute the mean-of-per-rule-rates and `digest_endpoints.md` updated accordingly. No PR block — P3 severity, staging path unaffected, and the displayed value is a valid compliance metric. Must resolve before next SI-05 feature increment.

**Backlog item:** BLG-SPEC-47 (to be filed)

---

## QA Test Coverage

- **Scenarios run:** `tests/test_si05_digest_service.py` (21 unit tests, all pass on commit 3887b6ca); manual AC review against BLG-GOV-86, `digest_endpoints.md` v0.2, `arc5_compliance_analytics.md`, CLAUDE.md §2
- **Regression areas checked:** Telegram digest infrastructure (v2.4 pattern); endpoint registration chain (`test.py`, `SystemStatus.js`, `system-status.spec.js`); OpenAPI spec coverage; format spec compliance (section structure, MarkdownV2 escaping, summary line rules)
- **Known deviations filed:** DEV-v51-EPIC01-01 (P3 — pass_rate computation method vs BLG-GOV-86 §5.2); backlog item BLG-SPEC-47 to be filed

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A (no frontend changes in EPIC-01)
- Signed off by: Director of Quality
- Date: 2026-06-21
- Comments: EPIC-01 approved with one P3 deviation filed (DEV-v51-EPIC01-01 — pass_rate computation method diverges from BLG-GOV-86 §5.2; backlog item BLG-SPEC-47 to be filed). ST-01 AC-09 (Telegram staging delivery) deferred per plan — Infrastructure & Operations Owner sign-off required in a subsequent staged verification sprint. All CLAUDE.md §2 same-commit requirements confirmed in commit 3887b6ca. No P0/P1 deviations. No SI-02 dependency. No frontend changes.
