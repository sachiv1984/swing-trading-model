Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-17

# Delegation Log — 2026-08-17__release-v8.9

Append-only. Do not edit previous entries.

---

## DEL-20260817-01

- **ST Item:** ST-01 — Fix nightly trailing-stop ratchet to apply breakeven floor for profitable positions
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Backend Engineering Patterns Owner
- **GitHub Issue:** #1429
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-01
- **Delegated at:** 2026-08-17T17:15:00Z
- **What is needed:** Confirm which trailing-stop calculation path runs in production for the nightly job and any on-demand recompute (BLG-BE-102 scope item 1); consolidate on `backend/utils/calculations.py::calculate_trailing_stop` (has the breakeven floor) if a second, unfloored path is found live; add a regression test covering the breakeven-floor case using BLG-BE-102's own WDC worked example.
- **Spec reference:** `backend/utils/calculations.py#calculate_trailing_stop` (pre-existing canonical implementation; no prior dedicated spec doc — bug/correctness investigation per execution_prompt.md STEP 3.1.A Case E pattern, closed with a regression test as the traceable artefact instead)
- **Unblock criteria:** Code-path audit complete and documented; regression test added and passing; Backend Engineering Patterns Owner sign-off.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-01`
- **Status:** Unblocked — in-session credential/action provisioning not applicable (no external credential needed); engine completed the investigation and regression test directly within this session per execution_prompt.md §5.2 (engine may write and commit code where the spec/AC is unambiguous). Agent-mediated Backend Engineering Patterns Owner sign-off (§5.3) cleared Approved 2026-08-17; regression test suite (7/7) passing. No multi-session parking occurred (LL-v8.2-P3-04 in-session completion pattern).

---

## DEL-20260817-02

- **ST Item:** ST-02 — Fix currency basis of current_trailing_stop/stop_price for US-market positions
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
- **GitHub Issue:** #1430
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-01
- **Delegated at:** 2026-08-17T17:15:00Z
- **What is needed:** `initial_stop`, `current_trailing_stop`, and `stop_price` must be in a consistent currency basis for a given position, or unambiguously suffixed with the frontend consuming the correct one. Add `current_trailing_stop_native` to `GET /positions` (backend/services/position_service.py::get_positions_with_prices) and update PositionCard.js/Positions.js to render it instead of the GBP-converted `current_trailing_stop`. Add a regression test case for a US-market profitable position showing a single consistent stop value across Init and live-stop tiles.
- **Spec reference:** `docs/specs/api_contracts/position_endpoints.md#Field notes`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`
- **Unblock criteria:** Backend field added; frontend consumers updated on both Card and Table views; regression tests (pytest + Playwright) added and passing; pre-existing e2e fixtures re-verified against the corrected field; Backend Engineering Patterns Owner and Frontend Specifications & UX Documentation Owner sign-off.
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-01`
- **Status:** Unblocked — same in-session completion pattern as DEL-20260817-01. Agent-mediated Backend Engineering Patterns Owner and Frontend Specifications & UX Documentation Owner sign-offs (§5.3) both cleared Approved 2026-08-17; regression suite (pytest 2/2, Playwright 2/2) passing, pre-existing e2e fixtures re-verified.

---

## DEL-20260818-03

- **ST Item:** ST-16 — Local dev venv version-pin enforcement; confirm PUBLIC_URL parity on production
- **EPIC:** EPIC-05
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1444
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-05
- **Delegated at:** 2026-08-18T10:10:00Z
- **What is needed:** (a) Document a mechanism for local backend dev environments to actually honour the existing `backend/.python-version` pin (3.11.0) — a `pyenv install/local` step in a local-setup doc, since plain `python3 -m venv` silently ignores it; (b) confirm production `PUBLIC_URL` status and document it.
- **Spec reference:** `docs/ops/test_environment_parity_check_2026-08-16.md#§2.1, §2.4` (source audit)
- **Unblock criteria:** README.md local-setup instructions added, correctly using pyenv to honour the pin; `.env.production` template parity fix (or documented reason it's unneeded) for `PUBLIC_URL`; Infrastructure & Operations Owner sign-off. (Full production dashboard confirmation of AC-2 is staging-only per sprint_backlog.md — not required for this item's completion, matching the audit's own advisory, not-a-confirmed-defect disposition.)
- **Commit format required:** `[EPIC-05][ST-16] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-05`
- **Status:** Unblocked — same in-session completion pattern as DEL-20260817-01/02. Agent-mediated Infrastructure & Operations Owner sign-off (§5.3) cleared Approved 2026-08-18; confirmed pyenv command correctness, confirmed the `.env.production` disclosure does not overclaim dashboard confirmation it doesn't have. No multi-session parking occurred.
