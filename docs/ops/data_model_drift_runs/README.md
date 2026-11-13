**Owner:** QA & Testing Owner; Data Model & Domain Schema Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-13 (created, ST-20, EPIC-07, v9.17, BLG-QA-223)
**Source:** ST-20 (BLG-QA-223, EPIC-07, v9.17 sprint execution)

# Data Model Drift Detector Runs

This folder keeps the `--json` output of every `scripts/check_data_model_drift.py` run that a triage relies on.

## How to save a run

1. Run the detector read-only against the target database, with the owner's permission:
   `python3 scripts/check_data_model_drift.py docs/specs/data_model.md --json > docs/ops/data_model_drift_runs/<YYYY-MM-DD>_<environment>.json`
2. Commit the file in the same commit as the triage that uses it.
3. In the triage, cite the file path and the `data_model.md` revision the run used.

## Why

The first run (v9.9, 2026-10-01) kept no output. When its findings were triaged at v9.12, 3 of the 11 index and CHECK names it reported could not be identified (`data_model.md` §Drift Detector Triage).
