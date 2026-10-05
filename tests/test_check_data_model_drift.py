"""Tests for scripts/check_data_model_drift.py (ST-28, EPIC-05, v9.9, BLG-SPEC-157)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_data_model_drift import (  # noqa: E402
    parse_check_constraint_names,
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
