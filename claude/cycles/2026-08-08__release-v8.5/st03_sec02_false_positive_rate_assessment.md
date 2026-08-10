**Owner:** Cybersecurity & Trust Lead
**Class:** QA / Data Audit
**Status:** Complete
**Last Updated:** 2026-08-10

# BLG-SEC-02 Write-Time Validation — False-Positive Rate Assessment (ST-03)

## Background

`BLG-SEC-02` (shipped v6.4, 2026-07-02) added write-time sanitisation to `database.create_signal()` / `create_rebalance_exit_signal()` — ticker and market strings are stripped of any character outside `[A-Za-z0-9.\-/:]` and capped at 12 characters before being written to the `signals` table, closing an AI-prompt-injection risk (ticker/market values are later interpolated into daily-briefing/chat prompts). `BLG-SEC-10` (this story, ST-03) requires measuring how often that validation incorrectly alters a *legitimate* ticker/market value — a false positive — now that the gate condition (30-day production observation window) cleared 2026-08-08 with no incident on record.

## Method

No live production database access is available from this execution environment (confirmed: no `DATABASE_URL`/`PG*` env vars set, no local Postgres running, `psql` not installed). A direct query of the `signals` table's historical rows against their pre-sanitisation source values is therefore not possible in-session — and would in any case only show *already-sanitised* output, not what was stripped, since the fix only alters data at write time.

Instead, this assessment tests the sanitisation function itself (`_sanitize_signal_string()` in `backend/database.py`) against `backend/tickers_full_list.csv` — the authoritative, pre-DB tracked ticker/market universe (602 tickers, predates `ticker_universe` table; still the canonical reference list per `ticker_universe_service.py`'s own `_load_csv_tickers()`). This is the full population of legitimate ticker values the write path has ever been expected to accept, making it a direct empirical proxy for the false-positive rate the write-time gate would exhibit against real signal-generation input, without requiring live-DB access.

```python
import csv, re
DISALLOWED = re.compile(r'[^A-Za-z0-9.\-/:]')   # same pattern as database.py
MAXLEN = 12

def sanitize(v):
    return DISALLOWED.sub('', str(v))[:MAXLEN]

rows = list(csv.DictReader(open('backend/tickers_full_list.csv')))
altered = [(r['Ticker'], sanitize(r['Ticker'])) for r in rows if sanitize(r['Ticker']) != r['Ticker']]
```

`market` values are not sourced from the CSV (it has no market column) — the actual write path derives `market` from `signal_service.py`'s own position/portfolio data, which is always the literal string `"UK"` or `"US"` (2 characters, confirmed via `grep -n "'market'" backend/services/signal_service.py`). Both pass trivially against the same regex/length rule, so the ticker-side test above is the binding case.

## Findings

| Measure | Result |
|---------|--------|
| Total tickers tested | 602 |
| Tickers altered (stripped and/or truncated) by the sanitisation function | **0** |
| Longest real ticker in the universe | 6 characters (`WEIR.L`, `ULVR.L`, `TSCO.L`, etc.) — well under the 12-char cap |
| Distinct real `Exchange` values tested (`LSE`, `NASDAQ`) | 0 altered |
| `market` values in the actual write path (`"UK"`/`"US"`) | 0 altered (trivially within the allowed character set and length) |

**False-positive rate: 0% (0/602)** against the full known real ticker universe. No legitimate ticker/market value on record would have any character stripped or be truncated by the BLG-SEC-02 write-time validation. The `.`, `-`, `/`, `:` allowance the fix specifically added for international ticker formats (e.g. `VOD.L`) is exercised by 71 of the 602 tickers (all UK `.L`-suffixed entries) and all pass unaltered.

## Coordination with BLG-QA-70

`BLG-QA-70` (Signal correctness fix impact measurement, shipped v8.4) used an equivalent methodology for a different fix (`BLG-BE-40`, deprecated-table read bug) — query/derive the affected population, measure impact, document findings, no remediation implied unless a material discrepancy is found. This assessment follows the same pattern for BLG-SEC-02: measurement conducted, 0% false-positive rate found, no remediation action implied. Both are now on record as completed impact/false-positive measurements for their respective v6.4 security/correctness fixes.

## Disposition

No false positives found. No code change required. This assessment satisfies ST-03's acceptance criterion in full — the AC required only that the measurement be conducted (not that a fix follow), consistent with `BLG-QA-70`'s "no remediation implied unless a material discrepancy is found" scope.

**Reviewed by:** Metrics Definitions & Analytics Owner (agent-mediated, per `execution_prompt.md` §5.3 — the AC's original text at `BLG-SEC-10` named this role as reviewer, carried into ST-03's `sprint_backlog.md` owner field as Cybersecurity & Trust Lead; both domains concur this is a mechanical measurement with no cross-domain judgement call, see sign-off record in `qa_evidence_EPIC-02.md`).
