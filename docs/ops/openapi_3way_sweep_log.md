**Owner:** API Contracts & Documentation Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-06
**Cycle:** 2026-08-05__release-v8.3 (ST-17 — BLG-QA-94)

---

# OpenAPI 3-Way Drift Sweep — Procedure and Run Log

## Purpose

`BLG-QA-94`'s problem statement: the `## METHOD /path` heading-level rule enforced by the existing OpenAPI Drift Detection CI gate (`.github/workflows/openapi-drift.yml`) has already caused one silent contract-drift gap (fixed, per that workflow's own header comment history). No periodic audit confirmed non-recurrence, and — more fundamentally — the existing gate is only a **2-way** check (canonical markdown contracts ↔ `docs/reference/openapi.yaml`). It cannot detect a route that exists in the actual backend code but was never documented in *either* of the other two artefacts, because it never reads the code at all.

This sweep adds the missing third leg: backend router decorators (`backend/routers/*.py`'s `@router.<method>(...)` and `backend/main.py`'s `@app.<method>(...)`).

## Procedure

**Tool:** `scripts/openapi_3way_drift_sweep.py`

**What it does:** parses all three artefacts independently (router/`@app` decorators, `## METHOD /path` contract headings, `openapi.yaml` path blocks) into three `METHOD /path` sets, then reports every pairwise gap (6 directions total — each pair, both ways) not already listed in the script's `KNOWN_GAPS` set.

**Cadence:** quarterly. This is a manually-run sweep, not a CI gate — running it on every PR would be redundant with the existing 2-way CI gate for the two legs it already covers, and router-decorator parsing has a higher false-positive rate (path-parameter naming style, external third-party API contracts accidentally in scope) that warrants human review of each finding rather than blocking merges automatically.

**Next scheduled run:** 2026-11-06 (quarterly from this first run).

**How to run:**
```
python3 scripts/openapi_3way_drift_sweep.py
```
Exit code 0 = clean. Exit code 1 = drift found (printed to stdout, grouped by direction).

**Disposition of a finding:**
1. If it's a genuine undocumented (or over-documented) endpoint: file a follow-up `BLG-SPEC-*` item and fix directly if trivial, matching the "fixed directly if trivial" convention already used elsewhere in this codebase's dark-mode-token defect class (`design_system.md` §Accessibility).
2. If it's a false positive of a known, deliberate, already-explained kind (see below): add the `METHOD /path` string(s) to `KNOWN_GAPS` in the script, with a comment explaining why.

## First Run — 2026-08-06

**Result:** 131 router/`@app` endpoints, 130 contract endpoints, 130 `openapi.yaml` endpoints scanned. **0 unresolved drift** after investigation — 1 genuine gap filed as a follow-up item, all other initial findings were false positives of the categories below (added to `KNOWN_GAPS`).

### Investigation

| Finding | Disposition |
|---|---|
| `GET /` | False positive — trivial infra root/health-check route (`{"status": "ok", ...}`), same exemption category as `/health` per `conventions.md` §11/§13.3. Added to `KNOWN_GAPS`. |
| `GET /v2/stocks/{symbol}/bars`, `GET /v1beta1/news` | False positive — these are `alpaca_integration_contract.md`'s documentation of a **third-party** API (Alpaca Markets) this backend calls, not routes of this backend's own routers. Added to `KNOWN_GAPS`. |
| `DELETE /price-alerts/{alert_id}` vs `{id}`, `DELETE /saved-filters/{filter_id}` vs `{id}`, `DELETE`/`GET`/`PUT /trade-plans/{plan_id}` vs `{id}`, `PATCH /notifications/{notification_id}` vs `{id}` | False positive — path-parameter **naming style** only, not an undocumented endpoint. Contract headings use a generic `{id}` placeholder; the implementation uses a more descriptive param name. Each router function's own docstring already cross-references its contract by the `{id}` form (e.g. `alerts.py`'s `PATCH /notifications/{notification_id}` handler docstring reads "Contract: alerts_endpoints.md §PATCH /notifications/{id}") — this is a deliberate, already-self-documented convention, not drift. Both string forms added to `KNOWN_GAPS` so the pairwise diff is suppressed in both directions. |
| `GET /test/quick-health`, `POST /test/rate-limit-scenarios` | **Genuine gap.** Internal test-harness endpoints in `backend/routers/test.py`, same category as the already-documented `POST /test/endpoints`, but never added when that entry was written. Filed as `BLG-SPEC-111` (P3). Not added to `KNOWN_GAPS` — this is a real, if minor, documentation debt, not a false positive; the sweep should keep flagging it until `BLG-SPEC-111` resolves it (fixing the doc gap, or extending the `conventions.md` test-endpoint exemption to name both explicitly). |

### Zero-drift confirmation

After `BLG-SPEC-111`'s resolution (either path), a re-run of `scripts/openapi_3way_drift_sweep.py` is expected to exit 0. As of this sweep (pre-`BLG-SPEC-111`), the only outstanding finding is that one filed gap — no other drift exists across any of the three pairwise comparisons.

## Known Deviations

None. This is a net-new artefact — no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-08-06 | 1.0 | Initial procedure + first run log (ST-17, EPIC-04, v8.3, BLG-QA-94) |
