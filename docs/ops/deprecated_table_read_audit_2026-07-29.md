**Owner:** Head of Backend Engineering
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-29
**Cycle:** 2026-07-28__release-v7.10 (ST-04 — BLG-BE-41)

---

# Deprecated-Table Read-Path Audit — `backend/database.py`

## Purpose

`BLG-BE-40` (v6.4) fixed a P1 correctness bug where `signal_service.py` read the deprecated `tickers` table instead of `ticker_universe`. No systematic check had been done to confirm this was the only deprecated-table read remaining anywhere in the codebase. ST-04 (BLG-BE-41) performs that systematic check, scoped to `backend/database.py`'s read functions per its acceptance criteria.

## Method

1. Confirmed the only table formally documented as deprecated is `tickers` (superseded by `ticker_universe`) — see `docs/specs/data_model.md` §Deprecated Tables (new section, added this story as a documentation backfill; previously this fact was only recoverable from `claude/backlog/backlog_archive.md`'s `BLG-BE-40` entry).
2. Enumerated all 39 `get_*`/`list_*` read functions in `backend/database.py` and grepped every `FROM <table>` reference in the file (`grep -noE "FROM [a-z_]+|INTO [a-z_]+|UPDATE [a-z_]+"`) to get the full set of tables the file actually reads/writes.
3. Cross-checked that table set against `data_model.md`'s documented schema sections and the new §Deprecated Tables entry.

## Findings

**1 deprecated-table read found:** `database.py::get_all_tickers()` (`SELECT ticker FROM tickers ORDER BY ticker`) — the exact same deprecated table `BLG-BE-40` fixed in `signal_service.py`, but in a separate, differently-scoped function that fix never touched.

**Severity assessment:** confirmed via `grep -rn "get_all_tickers"` across `backend/` that this specific function has **zero callers anywhere in the codebase**. Every actual call site (`signal_service.py`, `screener_batch_service.py`, `routers/ticker_universe.py`) imports a same-named but distinct `get_all_tickers` from `services.ticker_universe_service`, which correctly queries `ticker_universe`. This is dead code, not a live production bug — no user-facing or scheduled-job path is affected. Per this story's acceptance criteria ("any additional deprecated-table reads filed as P0/P1 correctness items per severity"), a P0/P1 filing is not warranted here since there is no live-impact severity to assign; the finding is remediated directly instead (see below) rather than filed, since leaving known-dead code that reads a deprecated table is itself a latent risk (a future accidental import would silently resurrect the bug class).

**All other 38 read functions** reference only non-deprecated tables — none reads `tickers` or any other table flagged as superseded. **Correction (found during Head of Engineering sign-off review):** not all of these tables are themselves documented in `data_model.md` — `backtest_trades`, `idempotency_keys`, `ai_journal_entries`, and `gemini_audit_log` are read by `database.py` functions but have no corresponding section in `data_model.md` §1–§11 or the DS-0x migration history. This is a separate, pre-existing spec-debt gap (undocumented tables, not deprecated ones) — it does not change this audit's deprecated-table conclusion, but it does mean the "cross-checked against documented tables" claim below should be read as "no table read was found to be deprecated," not "every table read is documented." Filed as a follow-up: `BLG-SPEC-109` (backfill missing `data_model.md` sections for these 4 tables).

## Remediation (this cycle)

- Removed `database.py::get_all_tickers()` (dead code, zero callers, read the deprecated `tickers` table) in the same commit as this audit.
- Added `docs/specs/data_model.md` §Deprecated Tables (v2.19) documenting the `tickers` → `ticker_universe` migration and its history, so this and future audits have a canonical reference instead of re-deriving the fact from backlog history each time.

## Disposition

Audit complete. 1 finding (dead code reading a deprecated table), remediated directly (removed) rather than filed as a follow-up, since severity assessment found zero live callers — no P0/P1 correctness item applies. No other `database.py` read function references a deprecated table.

## Sign-off

**Head of Backend Engineering:** Confirmed — audit complete across all 39 `database.py` read functions; 1 finding (dead code, zero callers, remediated by removal); `data_model.md` backfilled with the missing deprecation record. 2026-07-29.
