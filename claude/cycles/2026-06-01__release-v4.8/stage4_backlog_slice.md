**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.8
**Cycle:** 2026-06-01__release-v4.8
**Last Updated:** 2026-06-01

---

# Backlog Slice — v4.8

**Theme:** Governance Hardening, Ops/Security Debt & SI-05 Phase 1

---

## EPIC-01 — Governance & Compliance Hardening

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Estimated effort:** ~1.5 dev-days
**Risk IDs:** RISK-03

### ST-01 — §13 register completion (BLG-GOV-69)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Close the governance integrity gap identified in AUD-2026-05-30-001 — 7 governance prompts missing from §13 ARTEFACT_STATUS entries in OPERATIONAL_GUIDE.md §14.

**Acceptance Criteria:**

| AC-ID | Criterion | Evidence method |
|-------|-----------|----------------|
| AC-01 | OPERATIONAL_GUIDE.md §14 contains §13 ARTEFACT_STATUS entries for all 7 missing prompts: sprint_planning_prompt.md, execution_prompt.md, post_ship_closure.md, design_gate_prompt.md, roadmap_management_prompt.md, backlog_management_prompt.md, ideas_housekeeping_prompt.md | Code review: grep §14 table for each filename |
| AC-02 | Each new §14 entry follows existing format: version, last_updated, authority fields present | Code review |
| AC-03 | OPERATIONAL_GUIDE.md version bumped; prompt_change_log.md entry appended (per CLAUDE.md §6 governance edit checklist) | Code review |
| AC-04 | AUD-2026-05-30-001 gap confirmed closed — Head of Specs Team sign-off | DoQ sign-off block |

**Dependencies:** None
**Notes:** Complements AUD-2026-05-30 Tier 1 patches already applied in prompt_change_log.md (OPERATIONAL_GUIDE.md v4.20 added 7 missing rows but may not have bumped version again — verify current version and apply if needed).

---

### ST-02 — Agent charter header compliance remediation (BLG-GOV-70)

**Owner:** Director of HR; Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Fix non-compliant header formats in 2 agent charter files identified in AUD-2026-05-30 Stage 3.

**Acceptance Criteria:**

| AC-ID | Criterion | Evidence method |
|-------|-----------|----------------|
| AC-01 | `api_contracts_documentation_owner.md`: `## Role:` header changed to `**Role:**` | Code review |
| AC-02 | `backend_engineering_patterns_owner.md`: `**Owner:**` header changed to `**Role:**` | Code review |
| AC-03 | All other agent files in `claude/agents/` verified to have compliant `**Role:**` header format | Code review: `grep -rn "^## Role\|^\*\*Owner:\*\*" claude/agents/` confirms only the 2 files were non-compliant |
| AC-04 | No governance engine role-validation failures after fix (verified by Head of Specs Team manual review) | DoQ sign-off block |

**Dependencies:** None

---

### ST-03 — AUD-2026-05-30-006 gap resolution verification (BLG-GOV-72)

**Owner:** PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Confirm whether the 3 deferred patches from v4.4 lessons_learnt_closure.md (without BLG IDs) were resolved in v4.5–v4.7 or remain outstanding.

**Acceptance Criteria:**

| AC-ID | Criterion | Evidence method |
|-------|-----------|----------------|
| AC-01 | v4.4 `claude/cycles/2026-05-29__release-v4.4/lessons_learnt_closure.md` loaded and the 3 patches identified by description | Code review |
| AC-02 | For each patch: resolution status confirmed (resolved in v4.5–v4.7 sprint records, or not yet resolved) | Code review: check relevant sprint sprint_close.md or lessons_learnt.md files |
| AC-03 | Resolved patches documented with cycle reference; unresolved patches filed as new BLG-GOV items with stable IDs | If unresolved: new BLG items present in backlog.md |
| AC-04 | AUD-2026-05-30-006 gap closed or formally escalated | PMO Lead sign-off in DoQ block |

**Dependencies:** None

---

## EPIC-02 — Operations, Security & QA Debt

**Maps to:** S2-02
**Owner:** Infrastructure & Operations Owner; Head of Specs Team
**Estimated effort:** ~3–4 dev-days
**Risk IDs:** RISK-02

### ST-04 — Build minutes monitoring policy (BLG-OPS-46)

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Establish monitoring policy for Render CI build minutes to prevent recurrence of the 2026-05-31 exhaustion event.

**Acceptance Criteria:**

| AC-ID | Criterion | Evidence method |
|-------|-----------|----------------|
| AC-01 | Monthly Render build minute allocation documented (current plan limit) | Documentation produced |
| AC-02 | Actual consumption from v4.6–v4.7 cycles documented (minutes used per sprint) | Documentation produced |
| AC-03 | Early-warning threshold defined at 80% monthly utilisation | Document contains threshold definition |
| AC-04 | Billing cycle reset date documented in ops runbook or equivalent | Documentation produced |
| AC-05 | Assessment of whether double-capacity sprint cadence requires plan upgrade documented | FinOps & Resource Architect assessment documented |
| AC-06 | FinOps & Resource Architect sign-off recorded | DoQ sign-off block |

**Dependencies:** None

---

### ST-05 — Dependency audit post-v4.7 (BLG-OPS-47)

**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Run dependency vulnerability audit (Python + npm) — last CVE remediation was starlette v4.0 (2026-05-25); v4.1–v4.7 had no audits.

**Acceptance Criteria:**

| AC-ID | Criterion | Evidence method |
|-------|-----------|----------------|
| AC-01 | `pip-audit` run against `requirements.txt`; output documented | Audit output documented |
| AC-02 | `npm audit` run against frontend `package.json`; output documented | Audit output documented |
| AC-03 | HIGH or CRITICAL findings addressed (fix applied or filed as P0/P1 backlog item within this sprint) | If findings: BLG-OPS items present in backlog.md, or fix committed |
| AC-04 | Anthropic SDK version checked; patch upgrade applied if available | Code review or documentation |
| AC-05 | Audit findings documented in security register (`docs/security/security_register.md`) or equivalent | Documentation produced |
| AC-06 | Cybersecurity & Trust Lead sign-off recorded | DoQ sign-off block |

**Dependencies:** None
**Notes:** If HIGH/CRITICAL CVEs found, file as P0/P1 backlog items. If CRITICAL found, escalate to Head of Engineering for immediate remediation. Sprint scope expansion for CVE fix is permitted without amendment (RISK-02 disposition).

---

### ST-06 — Coverage matrix update and v4.7 contract verification (BLG-QA-39)

**Owner:** QA Lead; API Contracts & Documentation Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Update QA coverage matrix with v4.7 compliance_summary field; verify GET /reports/monthly-pnl v0.6 contract.

**Acceptance Criteria:**

| AC-ID | Criterion | Evidence method |
|-------|-----------|----------------|
| AC-01 | QA coverage matrix (or equivalent test coverage reference) includes `compliance_summary` field from v4.7 ST-03 as an observable regression point | Code review |
| AC-02 | `compliance_summary` field has a regression test reference (Playwright scenario or unit test) | Code review: test exists |
| AC-03 | `docs/specs/api_contracts/` contains an entry confirming v0.6 schema for `GET /reports/monthly-pnl` | Code review |
| AC-04 | Any contract gaps found filed as BLG-SPEC items | If gaps: new BLG-SPEC items in backlog.md |
| AC-05 | QA Lead sign-off recorded | DoQ sign-off block |

**Dependencies:** None

---

### ST-07 — SI-04 strategy version comparison endpoint contract (BLG-SPEC-43) [CONDITIONAL]

**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** S–M (~1–2 days)
**Delegation class:** autonomous
**Staging-only ACs:** None
**Conditional on:** PO confirming SI-04 in next release planning cycle. If not confirmed: defer to v4.9.

**Objective:** Pre-author the `GET /analytics/strategy-version-comparison` API contract before SI-04 sprint, preventing same-sprint spec debt (pattern from SI-03, SI-01).

**Acceptance Criteria:**

| AC-ID | Criterion | Evidence method |
|-------|-----------|----------------|
| AC-01 | API contract document created at `docs/specs/api_contracts/strategy_version_comparison_contract.md` | File present |
| AC-02 | Contract defines response schema: version_comparison fields (current strategy version vs historical, trade count per version, win_rate, avg_R, performance_delta) | Code review |
| AC-03 | Contract defines query parameters: version_from, version_to, date_range | Code review |
| AC-04 | Contract defines error cases: version_not_found (404), insufficient_data (422) | Code review |
| AC-05 | Placeholder entry added to `docs/reference/openapi.yaml` (implementation not required) | Code review: openapi.yaml updated |
| AC-06 | SI-04 §13 binding conditions owner (Strategy Rules & System Intent Owner) sign-off on draft contract recorded | DoQ sign-off block |
| AC-07 | Head of Specs Team sign-off recorded | DoQ sign-off block |

**Dependencies:** None (SI-04 §13 PASS already recorded v4.7 — 6 binding conditions)
**Notes:** BLG-SPEC-43 gate condition: "SI-04 confirmed for next release planning cycle." Since v4.8 is not implementing SI-04 itself, the gate is interpreted as: PO acknowledges SI-04 is on the medium-term roadmap and pre-authoring is warranted. PO to confirm at sprint planning.

---

## EPIC-03 — SI-05 Phase 1 — Weekly Strategy Integrity Digest [CONDITIONAL]

**Maps to:** S2-03
**Owner:** Head of Specs Team
**Estimated effort:** ~2–3 dev-days (conditional)
**Risk IDs:** RISK-01
**Gate condition:** SI-01 + SI-03 live ≥ 30 days — clears 2026-06-21

**Gate check rule:** Sprint planning engine must check gate status before sealing. If today ≥ 2026-06-21: gate MET, include ST-08. If today < 2026-06-21: gate NOT MET, defer EPIC-03 to v4.9.

### ST-08 — SI-05 Phase 1 implementation (BLG-GOV-67)

**Owner:** Head of Specs Team; Head of Backend Engineering
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous
**Staging-only ACs:** AC-05 (Telegram delivery requires live Telegram bot in staging)
**Gate condition:** SI-01 + SI-03 live ≥ 30 days (2026-06-21)

**Objective:** Implement SI-05 Phase 1 — weekly strategy integrity digest via existing Telegram notification infrastructure. Phase 1 scope: SI-01 + SI-03 data only (validation_pass_rate, override_count, red_flag_frequency_trend). No SI-02 dependency.

**Acceptance Criteria:**

| AC-ID | Criterion | Evidence method |
|-------|-----------|----------------|
| AC-01 | Backend service computes weekly digest: validation_pass_rate (trailing 7 days), override_count (trailing 7 days), red_flag_frequency_trend (7d vs prior 7d) | Unit tests |
| AC-02 | `POST /portfolio/si05-weekly-digest` endpoint (or equivalent trigger) produces digest payload | Unit tests |
| AC-03 | Digest payload routed through existing Telegram notification infrastructure (weekly_digest_service.py or equivalent) — same pattern as v2.4 weekly digest | Code review |
| AC-04 | Digest message format: concise, human-readable; includes all 3 Phase 1 metrics | Code review |
| AC-05 | Telegram delivery verified on staging with live Telegram bot [staging-only evidence] | Human staging run; date recorded in DoQ sign-off |
| AC-06 | Endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml` per CLAUDE.md §2 | Code review |
| AC-07 | API contract document created in `docs/specs/api_contracts/` per CLAUDE.md §2 | Code review: contract file present |
| AC-08 | No SI-02 dependency in Phase 1 (verified by code review — no import of drift detection service) | Code review |
| AC-09 | Phase 1 scope explicitly documented (not SI-02, future Phase 2) in code comment or spec reference | Code review |
| AC-10 | Head of Backend Engineering sign-off; Head of Specs Team sign-off | DoQ sign-off block |

**Dependencies:** None (Telegram infrastructure shipped v2.4)
**Notes:** Gate check mandatory at sprint planning. v2.4 weekly digest already sends to Telegram via `weekly_digest_service.py` — Phase 1 extends that service with Arc 5 compliance metrics. No new UI component required.

---

## Backlog Slice Summary

| Story | EPIC | Effort | Firm/Conditional |
|-------|------|--------|-----------------|
| ST-01 — §13 register completion | EPIC-01 | S | Firm |
| ST-02 — Agent charter header compliance | EPIC-01 | S | Firm |
| ST-03 — AUD gap resolution verification | EPIC-01 | S | Firm |
| ST-04 — Build minutes monitoring policy | EPIC-02 | S | Firm |
| ST-05 — Dependency audit | EPIC-02 | S | Firm |
| ST-06 — Coverage matrix + v4.7 contract | EPIC-02 | S | Firm |
| ST-07 — SI-04 endpoint contract | EPIC-02 | S–M | Conditional (PO confirmation) |
| ST-08 — SI-05 Phase 1 implementation | EPIC-03 | M | Conditional (gate 2026-06-21) |

**Firm stories:** 6 | **Conditional stories:** 2 | **Total:** 8
