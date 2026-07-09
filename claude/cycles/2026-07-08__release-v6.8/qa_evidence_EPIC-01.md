Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-09

# QA Evidence — EPIC-01 (2026-07-08__release-v6.8)

## Consolidation Block

**EPIC:** EPIC-01 — Production Correctness, Security & Infrastructure
**Cycle:** 2026-07-08__release-v6.8
**Sprint goal:** Fix the SI-02-blocking trade-plan linkage bug and close the two accompanying security gaps, ship both mandatory Product Value Alert pull-forwards (trade tagging and the SI-02 gate visibility indicator), and clear the accumulated spec, QA, and governance debt cluster.
**Test scenarios used:** `tests/test_position_trade_plan_link.py` (new, 4 scenarios), `tests/test_signal_write_sanitization.py` (extended, 4 new scenarios; 10 pre-existing)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01 (BLG-BE-46) | none — bug fix, no prior canonical spec | Backend-only auto-link: `add_position()` now looks up the most recent unlinked draft trade plan matching ticker+market and sets `position_id`/`status=active` on it. No UI change (preserves the pre-approved "no UI change" design gate). | AC-01 root cause documented (workflow gap — TradePlan.js and TradeEntry.js are disconnected pages with no hand-off); AC-02 fix implemented and verified via regression tests + production API read; AC-03 decision recorded (forward-fix only, no historical backfill of 11 pre-existing unlinked plans); AC-04 roadmap update out of this engine's write scope, handed off to Roadmap Rebalance Engine | Pass with notes | None — AC-04 is a cross-engine handoff (`claude/roadmap/*` is outside execution_prompt.md §7 write scope), not a spec deviation; documented in `execution_state.json` notes |
| ST-02 (BLG-SEC-08) | none — bug fix, no prior canonical spec | `SIGNAL_UPDATABLE_COLUMNS` allowlist added in `database.py`; `update_signal()` rejects any dict key outside it before building SQL; `PATCH /signals/{id}` pre-validates the same allowlist for a proper 400 response. | AC-01 dict keys validated against allowlist before use; AC-02 regression test confirms rejection of unrecognised key | Pass | None |
| ST-03 (BLG-SEC-07) | `docs/security/signal_anomaly_review_2026-07-09.md` | Manual review of all 300 production `signals` records for anomalous ticker/market values, via direct production API read (ST-04 key). | AC-01 existing signal records reviewed; findings documented; anomalies filed as follow-up BLG items | Pass | None — 0 anomalies found, so no follow-up items were required |
| ST-04 (BLG-OPS-99) | `docs/security/api_key_security_register.md#6-application-x-api-key` | Documented the previously-undocumented application `X-API-Key` (register entry #6, resolving LP-08). Used the key live against `GET /trades` and `GET /trade-plans` to confirm the SI-02 gate condition directly. | AC-01 key provisioned and documented; AC-02 a governed routine directly confirms a gate condition without self-report | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_position_trade_plan_link.py` (4/4 pass), `tests/test_signal_write_sanitization.py` (14/14 pass, includes 4 new BLG-SEC-08 tests), full backend suite (`backend/.venv/bin/python3 -m pytest tests/ --ignore=tests/e2e`) — 576 passed, 2 skipped, no regressions
- CI: `CI Pytest Suite` (Phase A + Phase B against real Postgres) and `Critical-Path Smoke Tests (Playwright)` both green on the final commit (`1242e388`) pushed to `exec/2026-07-08__release-v6.8/EPIC-01`
- Regression areas checked: position entry flow (`add_position`), signal write path (both `create_signal` and `update_signal`), no frontend changes in this EPIC
- Known deviations filed: None (see Deviations column above for ST-01's documented cross-engine handoff, which is not a spec deviation)

---

## Sign-Off Block

**Frontend-visible-change check:** No story in this EPIC creates or modifies any file under `src/pages/**` or `src/components/**` — confirmed via `git diff --name-only origin/main...HEAD` on this branch (only `backend/`, `tests/`, `docs/` paths touched). The CLAUDE.md frontend testing gate does not apply to this EPIC.

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required, and no live system interaction — ✗ (ST-04 AC-02 required a live production API call to confirm the SI-02 gate condition directly — this is a live system interaction by design, not a code-review-only verification)
- Criterion 3: No frontend-visible change — ✓
- Criterion 4: N/A (criterion 2 fails)

Autonomous class does not apply (criterion 2 unmet) — sign-off proceeds via agent-mediated Director of Quality review per §5.3.

- [x] All acceptance criteria verified against canonical spec (or, where no prior spec existed, against the story's stated AC in `stage4_backlog_slice.md`)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (full backend suite green, CI green on final commit)
- [x] No frontend components in this EPIC — URL-base-variable check not applicable
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-09
- Comments: Agent-mediated Director of Quality review — **APPROVED, no blocking findings**. Independently verified (not by re-reading this log): (1) `git diff main...exec/2026-07-08__release-v6.8/EPIC-01 --stat` confirms only `backend/`, `tests/`, `docs/` paths touched — no `src/pages/**`/`src/components/**` changes, so the ST-01 "no UI change" design-gate claim holds. (2) ST-01's auto-link creates the position and updates cash *before* the try/except wrapping the plan lookup/link — lookup and update failures are both caught and cannot block position creation (confirmed via `test_link_lookup_failure_does_not_block_position_creation` / `test_link_update_failure_does_not_block_position_creation`); `update_trade_plan()` already has its own field allowlist so the new call site can't be abused. (3) `SIGNAL_UPDATABLE_COLUMNS` was diffed against the actual `INSERT INTO signals (...)` column list in `create_signal()` — exact match; `update_signal()` has exactly one production caller (`main.py` PATCH endpoint via `signal_service.update_signal_status`), and the endpoint pre-validates the same allowlist for a proper 400. (4) Re-ran both new test files independently: `tests/test_position_trade_plan_link.py tests/test_signal_write_sanitization.py` → 18 passed, 0 failures; the rejection test uses a SQL-injection-shaped bad key and asserts the DB cursor was never called, which would catch a reverted fix. (5) ST-03/ST-04 docs reviewed for completeness — sound.
