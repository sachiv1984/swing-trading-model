Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# QA Evidence Log — EPIC-02: CI Quality Gates

**EPIC:** EPIC-02 — CI Quality Gates
**Cycle:** 2026-03-04__release-v1.8
**Sprint goal:** Establish automated correctness gates (golden output CI, vulnerability scanning, OpenAPI drift detection) to protect calculation integrity and dependency security on every PR.
**Test scenarios used:** Derived from spec + acceptance criteria (no separate scenario document exists for EPIC-02)

---

## Per-Story Evidence

---

### ST-05 — Golden Output Regression Baseline

**Spec references:** `claude/strategy/strategy_rules.md` (canonical stop-loss and position sizing formulas)

**Status:** COMPLETE — Engine implemented; commit 8101423.

**Commit SHA:** 8101423

**What was built:** `tests/golden_outputs.json` containing 5 position-sizing (PS) vectors and 7 stop-loss (SL) vectors, all independently derived from `strategy_rules.md` canonical formulas (not reverse-engineered from the running implementation). Precision tolerance: 4 decimal places for share counts, 2 for prices; documented in the JSON file. CI workflow step added — 30 tests pass. CI step confirmed to fail correctly on a known-bad input (synthetic divergence tested).

**Acceptance criteria verification:**

| Criterion | Result |
|-----------|--------|
| `tests/golden_outputs.json` exists with ≥4dp share count, ≥2dp price precision | Pass |
| Golden values spec-derived (not implementation-derived) | Pass |
| CI step fails on any numeric deviation | Pass — confirmed with synthetic divergence |
| CI step added to workflow on every PR | Pass |

**Deviation check:** No deviations from acceptance criteria.

---

### ST-06 — Backtest vs Live Stop Reconciliation

**Spec references:** `claude/strategy/strategy_rules.md` §11 (stop-loss formula parameters)

**Status:** COMPLETE — Engine implemented; commit 5bc22ee.

**Commit SHA:** 5bc22ee

**What was built:** Automated CI check comparing backtest stop calculations vs live system stop calculations for all 7 golden SL inputs from ST-05. `position_manager.PARAMS` verified against `strategy_rules.md §11`. Stop formula reconciled against all 7 golden SL inputs. Synthetic divergence detection confirmed sensitive — CI check fails on any deviation between backtest and live stop values.

**Acceptance criteria verification:**

| Criterion | Result |
|-----------|--------|
| CI check compares backtest vs live stops for all golden inputs | Pass |
| Any divergence fails the check | Pass |
| Integrated into CI pipeline | Pass |
| Confirmed to fail on synthetic divergence | Pass — tested with deliberately introduced divergence |

**Deviation check:** No deviations from acceptance criteria.

---

### ST-07 — Dependency Vulnerability Scanning

**Spec references:** None (infrastructure CI story; no canonical spec governs tool selection)

**Status:** COMPLETE — Engine implemented; commit feb84ec. Pending: Cybersecurity & Trust Lead acknowledgement.

**Commit SHA:** feb84ec

**What was built:** `pip-audit` CI workflow step added to `.github/workflows/`. High and critical CVEs block merge; severity threshold documented in workflow file. Tool choice rationale: `pip-audit` selected over `safety` — maintained by Python Packaging Authority, no API key required, output format machine-readable. Scan runs on every PR. Confirmed scan produces output and severity threshold is applied correctly.

**Acceptance criteria verification:**

| Criterion | Result |
|-----------|--------|
| CI step scans Python dependencies for known CVEs on every PR | Pass |
| Tool selected and documented in workflow file | Pass — `pip-audit` |
| High/critical CVEs block merge | Pass — threshold documented and enforced |
| Cybersecurity & Trust Lead acknowledges approach and severity threshold | **PENDING** — see QA sign-off block |
| Director of Quality confirms CI integration | Pending DoQ review |

**Deviation check:** No deviations from technical acceptance criteria. Cybersecurity & Trust Lead acknowledgement is a verification-dimension requirement — not yet obtained.

---

### ST-08 — Automated OpenAPI Drift Detection

**Spec references:** `docs/reference/openapi.yaml`

**Status:** COMPLETE — Engine implemented; commit d9ff7a6.

**Commit SHA:** d9ff7a6

**What was built:** Regex-based drift detection CI step comparing `docs/reference/openapi.yaml` against markdown API contract files. Approach: diff-based (not generation-based) — documented in workflow. `KNOWN_GAPS` config supports managed transitions during spec updates. Confirmed to detect real drift: 2 gaps + a YAML error present in the pre-v1.9.0 state were detected. Fully clean after EPIC-03 (ST-09, ST-10) merged to main. Merge blocked on detected drift.

**Acceptance criteria verification:**

| Criterion | Result |
|-----------|--------|
| CI step detects drift between openapi.yaml and markdown contracts | Pass |
| Approach documented in workflow (generation vs diff) | Pass — diff-based, documented |
| Merge blocked on detected drift | Pass |
| Passes on clean state after ST-10 (openapi.yaml v1.9.0) | Pass — confirmed clean after EPIC-03 merge |
| Confirmed to fail on synthetic drift | Pass — 2 real gaps + YAML error detected in pre-v1.9.0 state |

**Deviation check:** No deviations from acceptance criteria.

---

## EPIC-Level Consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-05 | `strategy_rules.md` | `tests/golden_outputs.json`: 5 PS + 7 SL vectors, spec-derived; CI step (30 tests, fails on deviation) | Golden values spec-derived; CI fails on deviation; DoQ confirms coverage | Pass | None |
| ST-06 | `strategy_rules.md §11` | CI check: backtest vs live stop for all 7 golden SL inputs; confirmed sensitive to synthetic divergence | CI runs, divergence detected, integrated into pipeline | Pass | None |
| ST-07 | N/A | `pip-audit` CI step; high/critical CVEs block merge; tool choice documented | CI runs; threshold applied; CyberSec & Trust Lead ack | Pass (technical) / **Pending** (CyberSec ack) | None |
| ST-08 | `openapi.yaml` | Drift detection CI; diff-based; KNOWN_GAPS config; detects real drift; clean after EPIC-03 | CI runs, passes clean, blocks on drift | Pass | None |

**QA test coverage:**
- Scenarios run: Derived from acceptance criteria (no separate scenario document for EPIC-02)
- Regression areas checked: CI workflow integrity, golden value derivation, vulnerability scan integration, drift detection sensitivity
- Known deviations filed: None

**Outstanding pre-merge requirement (ST-07):**
The ST-07 security dimension acceptance criterion requires explicit acknowledgement from the Cybersecurity & Trust Lead of the `pip-audit` tool choice and the high/critical severity threshold. This has not yet been obtained. The Director of Quality should confirm CI integration; the Cybersecurity & Trust Lead must separately acknowledge the security control design before the merge gate for EPIC-02 can pass.

**Cybersecurity & Trust Lead acknowledgement (ST-07):**
- [x] Tool acknowledged: `pip-audit` (PyPA-maintained, OSV + PyPI Advisory Database, no credentials required) — APPROVED for CI use
- [x] Severity threshold acknowledged: all findings treated as high/critical blocking (conservative, appropriate for v1.8; CVSS tiering recommended for v1.9)
- [x] Scope acknowledged: `backend/requirements.txt` only; frontend npm out of scope for v1.8 (acceptable)
- [x] Block mechanism confirmed: `exit 1` on any finding; PR comment with package-level detail
- Acknowledged by: Cybersecurity & Trust Lead
- Date: 2026-03-05
- Notes: v1.9 recommendations — (1) CVSS severity tiering via OSV service flag; (2) add `npm audit` for frontend dependencies.

**QA sign-off block:** (Director of Quality completes this)
- [x] All acceptance criteria verified against canonical spec — ST-05: 30 golden tests pass, spec-derived values confirmed; ST-06: backtest vs live reconciliation confirmed sensitive; ST-07: pip-audit CI integration confirmed, CyberSec acknowledged; ST-08: drift detection confirmed clean post-EPIC-03, fails on synthetic drift. All AC met.
- [x] No unresolved P0 or P1 deviations — no deviations identified across ST-05 through ST-08
- [x] Regression areas checked — CI pipeline integrity verified: golden output gate, reconciliation gate, vulnerability scan, drift detection all confirmed operational
- [x] Cybersecurity & Trust Lead acknowledgement obtained for ST-07 (pip-audit tool, high/critical threshold) — confirmed above 2026-03-05
- Signed off by: Director of Quality
- Date: 2026-03-05
- Comments: All four EPIC-02 CI gates operational and confirmed. ST-07 CyberSec acknowledgement in place. No deviations. EPIC-02 cleared for merge.
