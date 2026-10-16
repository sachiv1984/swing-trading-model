Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-16

# Delegation Log — 2026-10-16__release-v9.13

## DEL-20261016-01

- **ST Item:** ST-02 — Define the allowed exit reasons and map each to one of §8's three exit conditions
- **EPIC:** EPIC-01
- **Classification:** delegated_backend (live backfill and CHECK constraint, Human-Delegation — `sprint_backlog.md` ST-02 Notes / Staging-only AC 2, live half; RISK-01, DS-23 pattern)
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #2032
- **Branch:** exec/2026-10-16__release-v9.13/EPIC-01
- **Delegated at:** 2026-10-16T11:05:32Z
- **What is needed:** The engine has written AC 1 and the documentation half of AC 2 (`aded4d63`): the allowed values and their §8 condition in `data_model.md` §3 and `metrics_definitions.md` §Exit Condition Category, `backend/exit_reasons.py`, the 400 on an unlisted value at `POST /positions/{position_id}/exit`, and DS-34. The sandbox `DATABASE_URL` is staging and this engine has no authorisation to write to it, so the live steps remain. On **staging, then production**, in the Supabase SQL editor: (1) run DS-34's **Pre-check** and paste the output. Every `allowed = false` row must be a legacy alias from DS-34's table or blank; if any other value appears, stop and report it, because the Up Migration would roll back. (2) Run the **Up Migration** (one transaction: backfill, then both constraints). (3) Run the **Verification** query and re-run the Pre-check, and paste both outputs. Expected: 2 constraint rows (`chk_positions_exit_reason`, `chk_trade_history_exit_reason`), and every Pre-check row `allowed = true`.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Manual SQL in the Supabase SQL editor; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/data_model.md#DS-34 — Allowed exit_reason values with CHECK constraints on positions and trade_history (v2.63, 2026-10-16)`; `docs/specs/data_model.md#Exit Reason Values`; `stage4_backlog_slice.md#ST-02` AC 2
- **Unblock criteria:** each environment's Pre-check counts and Verification output, recorded in DS-34's Live Confirmation (status changed from PENDING to CONFIRMED APPLIED) and in `qa_evidence_EPIC-01.md` under ST-02.
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-10-16__release-v9.13/EPIC-01` (or a `[GOVERNANCE]` commit on `main` if EPIC-01 has merged)
- **Status:** Pending
