"""
ST-35 (BLG-OPS-205, EPIC-06, v9.18): no seed script inserts a market = 'UK'
ticker without the `.L` suffix.

Staging was seeded with `LGEN` and `BARC` (market UK). Price lookups route a UK
row by its `.L` symbol, so those rows came back `price_is_stale: true`. The app
stores UK tickers as Yahoo symbols (`BP.L`, `BT-A.L`;
`backend/services/ticker_universe_service.py`) in positions, trade_history and
signals (`signal_service.py` reads `.L` to tell UK from US), and every seed now
does too.

Exception, the watchlist: the app stores watchlist tickers bare. Adding an item
accepts letters and digits only, and the watchlist read joins `ticker_universe`
on `ticker || '.L'` for UK rows (`watchlist_service.py`). A `.L` watchlist seed
row would look up `LGEN.L.L` and lose its company name, so
`scripts/seeds/seed_watchlist.sql` stays bare, and a test below keeps it so.

Forms scanned (each has a failing sample below):
  - SQL values:     ('LGEN.L', 'UK', ...)   and   v_portfolio_id, 'AZN.L', 'UK'
  - Python dicts:   "ticker": "LGEN.L", "market": "UK"
  - Python dicts, market first: "market": "UK", "ticker": "LGEN.L"
  - Python tuples:  ("LGEN.L", "UK") and ("LGEN.L", "UK", 75)
Blind spots: a UK ticker built at run time (string formatting, a CSV read);
a dict with other keys between "ticker" and "market";
a symbol in a row with no market column (alert_evaluations, notification JSON);
and SQL embedded in workflow files (`.github/workflows/seed-preview.yml`, whose
alert_evaluations symbols were moved to `.L` by hand in ST-35).
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
WATCHLIST_SEED = ROOT / "scripts" / "seeds" / "seed_watchlist.sql"
SEED_FILES = sorted(p for p in (
    list((ROOT / "scripts" / "seeds").glob("*.sql"))
    + list((ROOT / "scripts" / "seeds").glob("*.py"))
    + list((ROOT / "backend" / "test_data").glob("*.sql"))
    + list((ROOT / "backend" / "test_data").glob("*.py"))
) if p != WATCHLIST_SEED)

_T = r"([A-Za-z][A-Za-z0-9.\-]*)"
_PATTERNS = (
    re.compile(r"'" + _T + r"'\s*,\s*'UK'"),
    re.compile(r'"ticker"\s*:\s*"' + _T + r'"\s*,\s*"market"\s*:\s*"UK"'),
    re.compile(r'"market"\s*:\s*"UK"\s*,\s*"ticker"\s*:\s*"' + _T + r'"'),
    re.compile(r'\(\s*"' + _T + r'"\s*,\s*"UK"\s*[,)]'),
)


def uk_tickers_without_suffix(text):
    """Every UK ticker in `text` that does not end in `.L`."""
    found = []
    for pattern in _PATTERNS:
        found += [m.group(1) for m in pattern.finditer(text) if not m.group(1).endswith(".L")]
    return found


def test_seed_files_exist():
    assert len(SEED_FILES) >= 8


def test_watchlist_seed_keeps_the_apps_bare_uk_tickers():
    text = WATCHLIST_SEED.read_text()
    assert "('LGEN', 'UK'" in text and "('BARC', 'UK'" in text
    assert not any(m.group(1).endswith(".L") for m in _PATTERNS[0].finditer(text))


@pytest.mark.parametrize("path", SEED_FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_no_uk_ticker_without_dot_l(path):
    assert uk_tickers_without_suffix(path.read_text()) == []


@pytest.mark.parametrize("bad, expected", [
    ("    ('LGEN', 'UK', '2026-03-01', 2.45),", ["LGEN"]),
    ("VALUES (v_portfolio_id, 'BP.', 'UK', '2026-01-09')", ["BP."]),
    ('{"ticker": "AZN", "market": "UK", "entry": 1}', ["AZN"]),
    ('UK_TICKERS = [("BT.A", "UK"), ("VOD.L", "UK")]', ["BT.A"]),
    ('POOL = [("VOD", "UK", 75)]', ["VOD"]),
    ('{"market": "UK", "ticker": "AZN"}', ["AZN"]),
])
def test_scanner_catches_each_form(bad, expected):
    assert uk_tickers_without_suffix(bad) == expected


@pytest.mark.parametrize("good", [
    "    ('LGEN.L', 'UK', '2026-03-01', 2.45),",
    "    ('AAPL', 'US', '2026-03-01', 2.45),",
    '{"ticker": "BT-A.L", "market": "UK"}',
    '("NG.L", "UK")',
])
def test_scanner_passes_good_rows(good):
    assert uk_tickers_without_suffix(good) == []
