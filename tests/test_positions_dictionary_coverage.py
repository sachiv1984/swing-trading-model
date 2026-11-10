"""
ST-22 (BLG-SPEC-200, EPIC-05, v9.16): the positions data dictionary lists every
column in data_model.md §2's Fields table, with the same SQL type and Nullable
value, and lists no other column except an explicitly marked historical row.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SPECS = ROOT / "docs" / "specs"


def _data_model_fields():
    text = (SPECS / "data_model.md").read_text(encoding="utf-8")
    section = text.split("## 2. Positions Table", 1)[1].split("\n## 3", 1)[0]
    fields = section.split("### Fields", 1)[1].split("**Provenance", 1)[0]
    rows = re.findall(r"^\| ([a-z_]+) \| ([^|]+?) \| ([^|]+?) \|", fields, re.M)
    return {name: (sql_type, nullable) for name, sql_type, nullable in rows}


def _dictionary_rows():
    text = (SPECS / "data_model_positions_dictionary.md").read_text(encoding="utf-8")
    section = text.split("## 3. Field Dictionary", 1)[1].split("\n## 4.", 1)[0]
    rows = re.findall(r"^\| `([a-z_]+)` \| ([^|]+?) \| ([^|]+?) \| (.*)\|$", section, re.M)
    return {name: (sql_type, nullable, desc) for name, sql_type, nullable, desc in rows}


def test_every_data_model_column_has_a_matching_dictionary_row():
    dm, dd = _data_model_fields(), _dictionary_rows()
    assert len(dm) > 30  # the parse found the table
    missing = sorted(set(dm) - set(dd))
    assert not missing, f"no dictionary row for: {missing}"
    for name, (sql_type, nullable) in dm.items():
        assert dd[name][:2] == (sql_type, nullable), name


def test_any_extra_dictionary_row_is_marked_historical():
    dm, dd = _data_model_fields(), _dictionary_rows()
    extra = {name: row for name, row in dd.items() if name not in dm}
    for name, (_, _, desc) in extra.items():
        assert desc.startswith("**Historical row"), name
