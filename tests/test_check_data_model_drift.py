"""Tests for scripts/check_data_model_drift.py (ST-28, EPIC-05, v9.9, BLG-SPEC-157)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_data_model_drift import (  # noqa: E402
    default_mismatches,
    normalize_default,
    parse_check_constraint_names,
    parse_documented_defaults,
    parse_index_names,
    parse_table_sections,
)

FIXTURE = """\
## 1. Widgets Table

```sql
CREATE TABLE widgets (
    id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    note TEXT
);

CREATE INDEX idx_widgets_name ON widgets(name);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| name | VARCHAR(50) | NO | Widget name |
| note | TEXT | YES | Optional note |

### Constraints

- None

---

## 2. Gadgets Table

```sql
CREATE TABLE gadgets (
    id UUID PRIMARY KEY,
    widget_id UUID NOT NULL REFERENCES widgets(id),
    label VARCHAR(50)
);

ALTER TABLE gadgets ADD CONSTRAINT gadgets_label_check CHECK (label IN ('a', 'b'));
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |
| widget_id | UUID | NO | FK to widgets |
| label | VARCHAR(50) | YES | Category label |

---

## Migration History

### DS-01 — some unrelated migration (v1.1)

| Column | Type | Nullable |
|--------|------|----------|
| unrelated_field | TEXT | YES |
"""


def test_parse_table_sections_stops_at_next_heading():
    tables = parse_table_sections(FIXTURE)
    assert set(tables.keys()) == {"widgets", "gadgets"}
    assert tables["widgets"] == {"id": False, "name": False, "note": True}
    assert tables["gadgets"] == {"id": False, "widget_id": False, "label": True}
    # Migration History's unrelated_field must not leak into gadgets (last real section)
    assert "unrelated_field" not in tables["gadgets"]


def test_parse_index_names():
    assert parse_index_names(FIXTURE) == ["idx_widgets_name"]


def test_parse_check_constraint_names():
    assert parse_check_constraint_names(FIXTURE) == ["gadgets_label_check"]


def test_diff_logic_matches_expected_shape():
    """Exercise the same diff computation run_live_checks performs, against a
    synthetic 'live' snapshot, without requiring a real DB connection."""
    tables = parse_table_sections(FIXTURE)
    live_widgets = {"id": False, "name": False, "extra_col": True}  # missing 'note', has 'extra_col'

    documented = tables["widgets"]
    undocumented = sorted(set(live_widgets) - set(documented))
    missing = sorted(set(documented) - set(live_widgets))
    mismatches = [c for c in set(documented) & set(live_widgets) if documented[c] != live_widgets[c]]

    assert undocumented == ["extra_col"]
    assert missing == ["note"]
    assert mismatches == []


def test_real_data_model_md_parses_without_error():
    """Regression check: the real file must parse without throwing, and must
    find at least the known 'positions' and 'notifications' tables."""
    data_model = Path(__file__).resolve().parent.parent / "docs" / "specs" / "data_model.md"
    text = data_model.read_text()
    tables = parse_table_sections(text)
    assert "positions" in tables
    assert "notifications" in tables
    # The 4 known-orphaned columns must not appear as documented fields on positions
    for orphan in ("atr_value", "stop_price", "fees", "pnl_percent"):
        assert orphan not in tables["positions"]


# --- Column defaults (ST-37, EPIC-06, v9.13, BLG-SPEC-184) ---------------

DEFAULTS_FIXTURE = """\
## 1. Ledgers Table

```sql
CREATE TABLE ledgers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fees_paid DECIMAL(10, 2) DEFAULT 0,          -- documented, none live
    rebate DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'closed')),
    history JSONB NOT NULL DEFAULT '[]'::JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ledgers_fees_check CHECK (fees_paid >= 0)
);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | NO | Primary key |

## 2. Counters Table

```sql
CREATE TABLE counters (
    id SERIAL PRIMARY KEY,
    hits INTEGER DEFAULT (0)
);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | SERIAL | NO | Primary key |
"""


def test_parse_documented_defaults_reads_create_table_block():
    d = parse_documented_defaults(DEFAULTS_FIXTURE)
    assert d["ledgers"] == {
        "id": "gen_random_uuid()",
        "fees_paid": "0",
        "rebate": None,
        "status": "'open'",
        "history": "'[]'::JSONB",
        "created_at": "CURRENT_TIMESTAMP",
    }
    assert "CONSTRAINT" not in d["ledgers"]
    assert d["counters"] == {"id": "nextval()", "hits": "(0)"}


def test_documented_default_with_none_live_is_a_mismatch():
    documented = parse_documented_defaults(DEFAULTS_FIXTURE)["ledgers"]
    live = {"id": "gen_random_uuid()", "fees_paid": None, "rebate": None, "status": "'open'::character varying",
            "history": "'[]'::jsonb", "created_at": "CURRENT_TIMESTAMP"}
    assert default_mismatches(documented, live) == [
        {"column": "fees_paid", "documented_default": "0", "live_default": None}
    ]


def test_live_default_with_none_documented_is_a_mismatch():
    documented = parse_documented_defaults(DEFAULTS_FIXTURE)["ledgers"]
    live = {"id": "gen_random_uuid()", "fees_paid": "0", "rebate": "0::numeric", "status": "'open'::character varying",
            "history": "'[]'::jsonb", "created_at": "now()"}
    assert default_mismatches(documented, live) == [
        {"column": "rebate", "documented_default": None, "live_default": "0::numeric"}
    ]


def test_equivalent_forms_do_not_mismatch():
    pairs = [
        ("0", "0::numeric"),
        ("0", "'0'::numeric"),
        ("0.00", "0"),
        ("20000.00", "20000.00::numeric(12,2)"),
        ("'[]'::JSONB", "'[]'::jsonb"),
        ("'[]'", "'[]'::jsonb"),
        ("'open'", "'open'::character varying"),
        ("NOW()", "now()"),
        ("CURRENT_TIMESTAMP", "now()"),
        ("TRUE", "true"),
        ("(0)", "0"),
        ("-1", "'-1'::integer"),
        ("nextval()", "nextval('counters_id_seq'::regclass)"),
        ("timezone('utc', now())", "timezone('utc'::text, now())"),
        (None, None),
        ("NULL", None),
    ]
    for documented, live in pairs:
        assert normalize_default(documented) == normalize_default(live), (documented, live)


def test_different_defaults_mismatch():
    for documented, live in [("0", "1"), ("'open'", "'closed'::character varying"), ("'[]'", "'{}'::jsonb"),
                             ("gen_random_uuid()", "uuid_generate_v4()"), ("'GBP'", "'gbp'::bpchar")]:
        assert normalize_default(documented) != normalize_default(live), (documented, live)


def test_column_absent_from_create_table_is_not_compared():
    documented = parse_documented_defaults(DEFAULTS_FIXTURE)["ledgers"]
    assert default_mismatches(documented, {"added_later": "false"}) == []


def test_real_data_model_md_documents_no_fees_paid_default():
    """The v9.9 hand-found drift: fees_paid must show no default (DS-23 correction)."""
    data_model = Path(__file__).resolve().parent.parent / "docs" / "specs" / "data_model.md"
    d = parse_documented_defaults(data_model.read_text())
    assert d["positions"]["fees_paid"] is None
    assert normalize_default(d["positions"]["state_history"]) == normalize_default("'[]'::jsonb")


def test_tool_issues_only_select_statements():
    src = (Path(__file__).resolve().parent.parent / "scripts" / "check_data_model_drift.py").read_text()
    executed = re.findall(r'cur\.execute\(\s*"(\w+)', src)
    assert executed and all(stmt.upper() == "SELECT" for stmt in executed)
