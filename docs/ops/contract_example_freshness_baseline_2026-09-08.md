**Owner:** API Contracts & Documentation Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-44, EPIC-05, v9.2, BLG-SPEC-120 — first baseline run recorded)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Contract Example-Payload Freshness — Baseline Run

## 1. Purpose

Records the first run of `scripts/check_contract_example_freshness.py` (added this story) and the disposition of its findings, per the scheduled-check cadence documented in that script's own docstring.

## 2. Run Summary (2026-09-08)

- 126 contract response examples checked across `docs/specs/api_contracts/*.md` against `docs/reference/openapi.yaml`.
- 37 examples flagged POSSIBLE DRIFT (an example key not found in the resolved `openapi.yaml` schema for that method+path).
- 3 examples SKIPPED (no confident method+path match against `openapi.yaml` — `POST /screener/run`, `POST /trade-plans`, `DELETE /trade-plans/{id}`; these paths' operations were not found under an exact or template match during this run and need a manual look, not necessarily real drift).

Full output: see the script's own stdout — not re-pasted here in full (46 lines); re-run `python3 scripts/check_contract_example_freshness.py` for the current list.

## 3. Known Limitation Affecting This Baseline (Read Before Triaging)

This is the tool's **first run**. The script's own docstring already frames it as a structural drift *detector* requiring human judgment per finding (same posture as `check_specs_index_freshness.py`), and that judgment has not yet been applied here. In particular, spot-checking `GET /portfolio` against its `PortfolioOverview`/`PositionSummary` schemas confirmed the schema *does* declare fields the script initially flagged — the false positives traced to the script comparing prefixed (`data.foo`) schema keys against the contract files' convention of showing the *unwrapped* contents of `data` directly; that specific mismatch is now corrected in the script (§ comparison logic compares both forms). The remaining 37 findings above are post-correction and more likely to contain genuine drift, but a per-nested-array-depth resolution limit in the script (defaults to 3 levels) means some remaining flags — particularly the deeply-nested array cases (e.g. `GET /positions/analyze`'s `actions[].*`, `GET /health`'s `external_apis.*.*`) — may still be resolver artifacts rather than real contract/schema mismatches.

## 4. Disposition

Given the volume (37 findings) and that most cluster in a handful of files, a full per-finding triage is out of scope for this story's 0.5-day effort — the AC is "check added/scheduled", not "all findings resolved". Filed as a follow-up:

- **BLG-SPEC-139** (filed from this story, per §7 write-scope exception in `execution_prompt.md`): API Contracts & Documentation Owner to triage the 37 POSSIBLE DRIFT + 3 SKIPPED findings above, either fixing genuine example/schema drift or noting each as a script-resolver limitation.

## 5. Scheduled Cadence

Per the script's own docstring: run manually before any `openapi.yaml` version bump touching an endpoint with a contract example, and at every `run audit` cycle (alongside `check_specs_index_freshness.py`). Not a CI hard gate this cycle.

## 6. Sign-Off

**API Contracts & Documentation Owner:** Confirmed — check added and run once to establish this baseline; scheduled cadence documented; triage follow-up filed (BLG-SPEC-139) rather than deferred silently. 2026-09-08.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-08 | 1.0 | Baseline run recorded (ST-44, EPIC-05, v9.2, BLG-SPEC-120). |
