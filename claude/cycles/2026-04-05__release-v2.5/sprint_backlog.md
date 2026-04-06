**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-06
**Cycle:** 2026-04-05__release-v2.5
**Release:** v2.5
**Sprint Goal:** Establish an operational baseline for v2.5 by sealing Sprint 1 governance debt (prompt patches, batch push fix, backlog placement rule) and System Status reliability, then completing backend integration documentation and targeted quick-win features in Sprint 2.
**Backlog Slice Source:** `claude/cycles/2026-04-05__release-v2.5/stage4_backlog_slice.md` (original — no amendment active)

---

# Sprint Backlog — v2.5

---

## Sprint Scope

---

### Sprint 1

---

#### EPIC-04 — Governance, Process & QA Hardening

**Maps to:** S2-10, S2-11, S2-12, S2-13
**Owner:** PMO Lead + Head of Specs Team + QA & Testing Owner
**Estimated effort:** ~1.5–2.5 days
**Risk IDs:** RISK-04
**Execution sequence:** 1 (first in Sprint 1 — governance patches must precede all other sprint execution)

##### ST-12 — Apply v2.4 deferred governance prompt patches

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | `execution_prompt.md` STEP 8 (or §6.1 sub-note) requires `prompt_change_log.md` append for any §6-governed file modified during sprint execution. `delivery_verification_prompt.md` STEP 8/9 pre-seal gate verifies §9 PO and DoQ Date fields are non-blank. Both files version-bumped. |
| Quality | Version bump confirmed; `OPERATIONAL_GUIDE.md` §14 and source prompt headers updated; `prompt_change_log.md` entries prepended for both changes in same commit. CF-2 carry-forward resolved. |
| Security | N/A — no security surface changed. |
| Verification | Director of Quality: code review of both prompt files confirming text matches AC. prompt_change_log.md entries present for both changes. |

**Dependencies:** None
**Notes:** Sequence first in Sprint 1. Per RISK-04: patches must govern remaining execution. Per CF-1: log entry for this edit must appear in prompt_change_log.md in the same session.

---

##### ST-10 — Fix governance_sync.yml batch push issue closure

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | `governance_sync.yml` uses `git log $BEFORE..$AFTER` to extract all commit messages in push range. Every referenced issue in push range closed (not just last commit). |
| Quality | Single-commit push behaviour unchanged (tested). Multi-commit push closes all referenced issues (verified with 2+ commit test on test branch per AC). |
| Security | N/A — CI workflow change; no user-facing security surface. |
| Verification | Director of Quality: code review of updated workflow. Confirm AC item "Tested with 2+ commit push on test branch" is evidenced in QA record. |

**Dependencies:** None
**Notes:** None.

---

##### ST-11 — Formalise backlog entry placement standard

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | `.claude/skills/lessons_learnt.md` has `backlog-add` entry recording placement rule. Placement rule note visible at top of `backlog.md` (below standing notice). |
| Quality | Confirm placement rule is in both locations; no regression to existing backlog content or structure. |
| Security | N/A — documentation change. |
| Verification | Director of Quality: code review confirming both files updated per AC. |

**Dependencies:** None
**Notes:** None.

---

##### ST-13 — Create test scenarios for EPIC-01 correctness fixes

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | SC-ATR-01, SC-DEDUP-01, SC-DEDUP-02, SC-STOP-01 all authored and filed in canonical test scenario library. |
| Quality | All 4 scenarios cross-referenced in QA evidence file. Scenarios cover: pence→GBP conversion correctness, dedup fires correctly, pipeline not suppressed by dedup, stop_price present on analytics response. |
| Security | N/A — test scenario authoring; no security surface. |
| Verification | Director of Quality: confirm all 4 scenario files exist in library with correct cross-references. |

**Dependencies:** ST-01 (advisory — scenarios benefit from referencing ST-01 implementation as test anchor)
**Notes:** Best sequenced after ST-01 merges. No hard dependency.

---

#### EPIC-01 — System Status Reliability

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Head of Engineering
**Estimated effort:** ~2–3 hours (3×XS)
**Risk IDs:** RISK-01
**Execution sequence:** 2 (after EPIC-04 — governance patches govern execution from here)

##### ST-01 — Fix auth forwarding in POST /test/endpoints

**Owner:** Head of Engineering
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | `test_all_endpoints()` accepts and forwards API key; `POST /test/endpoints` extracts `X-API-Key` from incoming request and passes through; implementation uses API key forwarding (not middleware bypass). |
| Quality | All correctly-implemented endpoints report "pass" when system is healthy. Success rate on System Status page reflects actual health (not 401 rejections). |
| Security | **API key forwarding only** — middleware bypass approach prohibited per RISK-01. API key is forwarded, not stored or logged. |
| Verification | Director of Quality: staging run confirming success rate improves from 1/17 to expected pass rate (all healthy endpoints passing). Code review confirming no middleware bypass pattern. |

**Dependencies:** None (dependency anchor for ST-02, ST-03, ST-13)
**Notes:** RISK-01 security constraint applies — see AC Security dimension.

---

##### ST-02 — Sync endpoint test list with openapi.yaml

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | All 10 missing parameterless GET endpoints added to health_service.py test list. Comment block references `docs/reference/openapi.yaml` as source of truth. System Status placeholder text updated to actual endpoint count. |
| Quality | No regression to existing endpoint tests. All added endpoints correctly included in test run. |
| Security | N/A — test list update; no security surface. |
| Verification | Director of Quality: code review confirming all 10 missing endpoints present; comment block present; placeholder text updated. |

**Dependencies:** ST-01 (sequencing — auth forwarding must work for results to be meaningful; execute after ST-01)
**Notes:** None.

---

##### ST-03 — Fix System Status endpoint categorisation for v2.3/v2.4 routes

**Owner:** Frontend Engineer
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | `categorizeEndpoint()` in SystemStatus.js updated to cover `/alerts`, `/notifications`, `/digest` routes. `categoryConfig` entries for "Alerts" and "Notifications" added with icons/colours. |
| Quality | Alert, notification, and digest endpoints appear in correct categories (not "Other") in Endpoint Tests panel. No endpoints in "Other" except `/` (root). No regression to other categories. |
| Security | N/A — frontend display-only change. |
| Verification | Director of Quality: code review confirming new category configs added. Staging run or screenshot evidence that categories render correctly. |

**Dependencies:** ST-01 (advisory — meaningful test results require auth fix, but categorisation itself is independent)
**Notes:** None.

---

### Sprint 2

---

#### EPIC-02 — Backend Integration & Performance

**Maps to:** S2-04, S2-05, S2-06
**Owner:** Head of Engineering
**Estimated effort:** ~4–6 days (3×M)
**Risk IDs:** RISK-02
**Execution sequence:** 3 (first in Sprint 2)

##### ST-04 — Review and document Reports page backend integration

**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | Review document exists mapping each Reports page section to its backend endpoint (or flagging missing connection). Filed at canonical or cycle-level path. Improvement proposals as prioritised list. |
| Quality | All integration gaps have either a follow-up backlog item filed or are addressed within scope. Document is actionable (no vague "TBD" entries). |
| Security | N/A — documentation review; no security surface. |
| Verification | Director of Quality: confirm review document exists at filed path; all gaps have disposition (backlog item or addressed); prioritised improvement list present. |

**Dependencies:** None (parallel with ST-05)
**Notes:** RISK-02 — review may surface gaps; these become backlog items, not in-scope fixes. No sprint overrun risk.

---

##### ST-05 — Review and document Signals page backend integration

**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | Review document exists mapping each Signals page section to its backend endpoint (or flagging missing connection). Filed at canonical or cycle-level path. Improvement proposals as prioritised list. |
| Quality | All integration gaps have follow-up backlog item filed or are addressed within scope. Document is actionable. |
| Security | N/A — documentation review; no security surface. |
| Verification | Director of Quality: confirm review document exists; all gaps dispositioned; improvement list present. |

**Dependencies:** None (parallel with ST-04)
**Notes:** Same scope constraint as ST-04 (RISK-02).

---

##### ST-06 — Investigate high external baseline latency on DB-backed endpoints

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | Root cause of `GET /portfolio` (p50=5,979ms) and `GET /notifications/preferences` (p50=4,631ms) outlier latency identified and documented. Either fix applied (outliers within 2× of peer endpoints) OR documented architectural constraint explaining why optimisation not feasible on free tier. Supabase connection pooling options evaluated. |
| Quality | Findings filed at `docs/ops/api_performance_baseline.md` (if changes made). Root cause documentation must be specific (not "slow query" — must identify exact bottleneck). |
| Security | N/A — performance investigation; no security surface changed. |
| Verification | Director of Quality: review findings document confirming root cause identified for both outliers; disposition documented (fix or constraint); pooling options evaluation present. |

**Dependencies:** ST-04, ST-05 (advisory — benefits from knowing integration state; no hard dependency)
**Notes:** Classified `delegated_backend` — potential fixes to connection pooling or query patterns require human evaluation and decision before applying. Human sign-off required before any performance change is committed.

---

#### EPIC-03 — Frontend & Operations Quick Wins

**Maps to:** S2-07, S2-08, S2-09
**Owner:** Frontend + Backend + Operations
**Estimated effort:** ~1–2 days (2×XS + 1×S)
**Risk IDs:** RISK-03
**Execution sequence:** 4 (Sprint 2, alongside or after EPIC-02)

##### ST-07 — Add --max-time to GitHub Actions curl calls

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | `--max-time 120` added to every `curl` call in `alert-evaluation.yml` and `daily-snapshot.yml`. Workflow step fails with non-zero exit code if service doesn't respond within 120s. |
| Quality | No regression to existing workflow logic. Both files updated. Failure mode confirmed (non-zero exit, not hanging). |
| Security | N/A — CI workflow change; no security surface. |
| Verification | Director of Quality: code review of both workflow files confirming `--max-time 120` present on all curl calls. |

**Dependencies:** None
**Notes:** None.

---

##### ST-08 — Fix Avg Slippage StatsCard gradient rendering

**Owner:** Frontend Engineer
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | Avg Slippage StatsCard renders with gradient background matching other StatsCard components. `docs/testing/slippage_scenarios.md §5` updated with DEV-ST14-01 resolution note. |
| Quality | No regression to slippage value display or colour coding. Gradient visually consistent with other StatsCards. |
| Security | N/A — cosmetic frontend fix. |
| Verification | Director of Quality: staging run or screenshot evidence that gradient renders correctly. Code review confirming slippage_scenarios.md updated with resolution. |

**Dependencies:** None
**Notes:** Clears DEV-ST14-01 deviation (P3 cosmetic, pre-accepted 2026-03-20).

---

##### ST-09 — Fee drag metric on Trade History

**Owner:** Metrics Definitions & Analytics Owner + Head of Engineering + Frontend Engineer
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Acceptance Criteria (structured — §7):**
| Dimension | Criteria |
|-----------|----------|
| Technical | `fee_drag_pct` per-trade field and `avg_fee_drag_pct` envelope field returned in GET /trades response. "Avg Fee Drag" StatsCard and "Fee Drag %" column in TradeHistoryTable. Spec updates to metrics_definitions.md, trade_history.md, trade_endpoints.md, openapi.yaml in same commit as implementation per CLAUDE.md. |
| Quality | StatsCard displays `avg_fee_drag_pct` as `+X.XX%`. Column always populated (no `—` for missing data). Metric never called "slippage". Formula: `exit_fees / gross_proceeds × 100`, rounded to 2dp. |
| Security | N/A — display-only analytics metric; SPS=1; does not affect signal ranking or trading decisions. |
| Verification | Director of Quality: staging run confirming StatsCard visible and correct, column present and populated. Code review confirming all 4 spec files updated in same commit. openapi.yaml drift detection gate must pass. |

**Dependencies:** None (RISK-03: EPIC-03 branch must branch from up-to-date main after EPIC-01 merges to avoid openapi.yaml conflicts)
**Notes:** Classified `delegated_frontend` — involves spec authoring + frontend rendering. HoST to co-author spec updates. Test scenario gap flagged in sprint_planning_notes.md: QA & Testing Owner to author visual/functional scenarios for ST-09 before delivery verification.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~6–10 effective days (2 sprints) |
| Total estimated effort (in-scope) | ~7.0 days |
| Utilisation | ~87% (mid-point) |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | No items deferred — all 13 in-scope |

## Deferred Execution Blockers Accepted

*(Section omitted — `deferred_execution_blockers` was empty in state.json)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Provide `design_gate_bypass_authority` and `design_gate_bypass_reason` → write to `.claude_current_state.json`; authority must be `"Head of UX & Design + Product Owner"` per IMP-30 | Head of UX & Design + Product Owner | **Yes** |
| Confirm sprint goal in `sprint_goal.md` | Product Owner | **Yes** |
| Confirm sprint scope (this document) | Product Owner | **Yes** |
| Backfill `prompt_change_log.md` version gaps (4 prompts) | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** [AWAITING SIGN-OFF]
**Scope confirmed:** [AWAITING SIGN-OFF]
**Capacity confirmed:** [AWAITING SIGN-OFF]
**Deferred execution blockers accepted:** N/A
**Signed off by:** Product Owner
**Date:** [AWAITING SIGN-OFF]
