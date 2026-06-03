**Owner:** Head of Specs Team
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-06-21
**Cycle:** 2026-06-03__release-v5.0
**Story:** ST-10 (EPIC-04, v5.0)
**Backlog ref:** BLG-GOV-86
**Depends on:** BLG-FE-60 — confirmed Telegram channel (2026-06-03)

---

# SI-05 Phase 1 — Telegram Message Format Specification

**Feature:** SI-05 — Weekly Strategy Integrity Digest
**Delivery channel:** Telegram (existing v2.4 infrastructure)
**Frequency:** Weekly (same schedule as v2.4 performance digest)
**Gate condition:** BLG-FE-60 confirmed Telegram ✅ (2026-06-03)

---

## 1. Purpose

This document specifies the exact format of the SI-05 weekly strategy integrity digest delivered via Telegram. It defines: section structure, character budget allocation, data field bindings from SI-01/SI-03 endpoints, failure mode handling, and the implementation constraint that SI-05 may either extend the v2.4 weekly digest or deliver as a separate message.

---

## 2. Telegram Constraints

| Constraint | Value | Impact |
|-----------|-------|--------|
| Max message length | 4,096 characters (Markdown) | Generous for 3-metric summary |
| Markup style | `MarkdownV2` (Telegram API) | Bold: `*text*`, italic: `_text_`, code: `` `text` ``, links: `[label](url)` |
| No HTML | Not permitted in `MarkdownV2` | — |
| No tables | Not rendered in Telegram | Use indented bullets for tabular data |
| No interactive elements | No buttons, menus, checkboxes | Digest is read-only |
| No file attachments | Photos/files require separate `sendDocument` | Phase 1 is text-only |
| Escape requirement | Special chars must be escaped: `_`, `*`, `[`, `]`, `(`, `)`, `~`, `` ` ``, `>`, `#`, `+`, `-`, `=`, `|`, `{`, `}`, `.`, `!` | Templates must escape all literal occurrences |

---

## 3. Message Delivery Strategy

SI-05 Phase 1 delivers the strategy integrity digest as an **extension to the v2.4 weekly digest message** — a new "Strategy Integrity" section appended after the existing performance summary. This avoids a second weekly message and preserves the single-channel digest habit.

**Alternative (separate message):** If extending the v2.4 message would exceed the 4,096-character budget (measured at implementation time against real data), SI-05 may deliver a separate second Telegram message in the same weekly job. Implementation must check total length before deciding; default to extension.

---

## 4. Section Structure

The SI-05 section appended to the v2.4 digest:

```
---
*📋 Strategy Integrity*

✅ Pre\-entry pass rate \(7d\): {pass_rate}
🚨 Red flag events \(7d\): {red_flag_count}
⚠️ Override rate \(7d\): {override_rate}
🔍 Top rule breach: {top_rule_breach}

{integrity_summary_line}
```

### 4.1 Section fields

| Field | Telegram text | Data source |
|-------|--------------|-------------|
| `pass_rate` | Percentage, 1 decimal place, e.g. `85.0%` or `N/A` | `GET /analytics/arc5-compliance` → aggregate of `validation_pass_rate_by_rule` values (mean across rules); `null` → `N/A` |
| `red_flag_count` | Integer count, e.g. `3` | `events_per_week × 7`, rounded to nearest integer; `0.0` → `0` |
| `override_rate` | Percentage, 1 decimal place, e.g. `10.0%` or `N/A` | `override_rate × 100`; `null` → `N/A` |
| `top_rule_breach` | Rule name, title-cased, e.g. `Regime Gate` or `None` | `top_rule_breach`; `null` → `None` |
| `integrity_summary_line` | One-line plain-text summary (see §4.2) | Derived from field values (rule-based, no AI generation) |

### 4.2 Integrity summary line rules

The summary line is **rule-based** — no generated text, no AI. Apply in order:

1. If `pass_rate` is `N/A` (no validation data): `_No pre\-entry validation data available this week\._`
2. If `pass_rate` < 70%: `_Pass rate below threshold — review pre\-entry rule compliance\._`
3. If `red_flag_count` > 5: `_Elevated red flag activity this week — check the journal\._`
4. If `override_rate` > 30%: `_High override rate — consider reviewing override decisions\._`
5. Otherwise (all clear): `_Strategy integrity healthy this week\._`

Only the first matching rule fires. Rules are evaluated in order 1–5.

---

## 5. Data Field Definitions

### 5.1 Source endpoint

```
GET /analytics/arc5-compliance?period=7d
```

See: `docs/specs/api_contracts/arc5_compliance_analytics.md`

### 5.2 Field binding table

| Telegram field | API field | Transformation |
|---------------|----------|---------------|
| `pass_rate` | `data.validation_pass_rate_by_rule` | Mean of all `pass_rate` values; `null` values excluded from mean. If map is empty → `null` |
| `red_flag_count` | `data.events_per_week` | `round(events_per_week * 7)`. `0.0` → `0` |
| `override_rate` | `data.override_rate` | `override_rate * 100`, formatted as `{:.1f}%`. `null` → `N/A` |
| `top_rule_breach` | `data.top_rule_breach` | Title-case the snake_case value (e.g. `regime_gate` → `Regime Gate`). `null` → `None` |

### 5.3 Percentage formatting

- `pass_rate`: `f"{value:.1f}%"` where value ∈ [0, 100]. If source is 0.0–1.0 scale: multiply by 100 first.
- `override_rate`: same pattern.

---

## 6. Character Budget

Estimated character count for a populated SI-05 section:

| Element | Estimated chars |
|---------|----------------|
| Section divider + header | ~25 |
| 4 metric lines (avg 45 chars each) | ~180 |
| Summary line (avg 60 chars) | ~60 |
| **SI-05 section total** | **~265 chars** |

v2.4 digest section estimated at ~400–600 chars. Combined message well within the 4,096-char limit. No truncation risk for Phase 1 scope.

---

## 7. Failure Modes

| Scenario | Behaviour |
|----------|-----------|
| `/analytics/arc5-compliance` returns non-200 or times out | Omit the SI-05 section entirely from the digest; do not fail the weekly job. Log the error. |
| All `validation_pass_rate_by_rule` values are null | `pass_rate` displays as `N/A`; summary line rule 1 fires |
| `events_per_week` is 0.0 | `red_flag_count` displays as `0` |
| `override_rate` is null | Displays as `N/A` |
| `top_rule_breach` is null | Displays as `None` |
| Message total length > 4,096 chars | Truncate SI-05 section to summary line only; log truncation |

---

## 8. Weekly Schedule

SI-05 digest is generated and delivered in the same weekly scheduled job as the v2.4 performance digest. No separate scheduling is required for Phase 1.

**Timing:** Implementation inherits v2.4 schedule. If the v2.4 job runs on a configurable schedule, SI-05 data is fetched and appended in the same execution.

---

## 9. Implementation Notes

- The SI-05 section is appended **after** the v2.4 performance content and **before** any closing footer.
- All literal special characters in the template (dashes, dots, parentheses) must be escaped for `MarkdownV2`.
- Field values that are already formatted strings must escape any special characters before interpolation.
- Implementation must call `/analytics/arc5-compliance?period=7d` — not `period=30d` — for the weekly digest window.
- No AI-generated text. All copy is template-driven with rule-based conditional lines.

---

## 10. Sign-Off

**Product Owner:** Product Owner — 2026-06-03

Rationale: Format is proportionate for Phase 1 (3 metrics, rule-based summary). No AI generation. Failure modes are safe (omit on error, never fail the job). Character budget verified.

**Head of Specs Team:** Head of Specs Team — 2026-06-03

Spec review: section structure, field bindings, escape requirements, failure modes all conformant with Telegram MarkdownV2 constraints and the `docs/specs/api_contracts/arc5_compliance_analytics.md` response schema. No deviations.

---

## Known Deviations

### DEV-v51-EPIC01-01 — P3: `pass_rate` computation method diverges from §5.2

**Severity:** P3 (accuracy gap — not a system failure or data loss)
**Sprint:** 2026-06-21__release-v5.1 (ST-01)
**Canonical requirement (§5.2):** `pass_rate` ← Mean of all `pass_rate` values from `data.validation_pass_rate_by_rule`; null values excluded from mean. If map is empty → null. Requires calling or replicating `GET /analytics/arc5-compliance?period=7d` and iterating `validation_pass_rate_by_rule` entries for equal-weighted arithmetic mean.
**What was implemented:** `fetch_arc5_data_for_digest()` queries `pre_entry_validation_log` directly and computes `pass_count / total` across all rules combined — a volume-weighted overall pass rate, not a mean of per-rule rates.
**Secondary inconsistency:** `docs/specs/api_contracts/digest_endpoints.md` v0.2 documents the data source as "Overall pass/total ratio (7d)", which is inconsistent with this spec's §5.2. The contract document should reference the per-rule mean method.
**Impact:** When validation rules have different volumes, the two methods produce different values. Volume-weighted aggregate is dominated by high-volume rules; mean-of-per-rule-rates treats each rule equally.
**Target resolution:** v5.1+ (before next SI-05 feature increment) — Head of Specs Team to determine whether (a) §5.2 is updated to accept volume-weighted overall rate, or (b) the service is corrected to compute mean-of-per-rule-rates and `digest_endpoints.md` updated accordingly.
**Owner:** Head of Specs Team
**Backlog reference:** BLG-SPEC-47
