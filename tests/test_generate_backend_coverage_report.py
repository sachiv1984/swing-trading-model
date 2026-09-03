"""
Regression tests for scripts/generate_backend_coverage_report.py (ST-22,
BLG-QA-84, EPIC-04, v9.0).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import generate_backend_coverage_report as gen  # noqa: E402


def _coverage_data(files, covered_lines, num_statements):
    return {
        "files": files,
        "totals": {
            "covered_lines": covered_lines,
            "num_statements": num_statements,
            "percent_covered": round(covered_lines / num_statements * 100, 4),
        },
    }


def _file_entry(covered, statements):
    return {"summary": {"covered_lines": covered, "num_statements": statements}}


class TestModuleRows:
    def test_groups_by_top_level_backend_subpackage(self):
        data = _coverage_data(
            files={
                "backend/services/foo.py": _file_entry(10, 20),
                "backend/services/bar.py": _file_entry(5, 5),
                "backend/routers/baz.py": _file_entry(8, 10),
                "backend/database.py": _file_entry(3, 6),
            },
            covered_lines=26, num_statements=41,
        )
        rows = {group: (covered, statements, pct) for group, covered, statements, pct in gen._module_rows(data)}
        assert rows["services"] == (15, 25, 60.0)
        assert rows["routers"] == (8, 10, 80.0)
        assert rows["database.py"] == (3, 6, 50.0)


class TestGenerateReport:
    def test_report_without_base_shows_not_available(self):
        head = _coverage_data(files={"backend/services/foo.py": _file_entry(10, 20)}, covered_lines=10, num_statements=20)
        report = gen.generate_report(head, base_data=None)
        assert "Backend Test Coverage Report" in report
        assert "50.0%" in report
        assert "not available this run" in report

    def test_report_with_base_shows_positive_delta(self):
        head = _coverage_data(files={"backend/services/foo.py": _file_entry(15, 20)}, covered_lines=15, num_statements=20)
        base = _coverage_data(files={"backend/services/foo.py": _file_entry(10, 20)}, covered_lines=10, num_statements=20)
        report = gen.generate_report(head, base)
        assert "+25.0pp" in report
        assert "📈" in report

    def test_report_with_base_shows_negative_delta(self):
        head = _coverage_data(files={"backend/services/foo.py": _file_entry(5, 20)}, covered_lines=5, num_statements=20)
        base = _coverage_data(files={"backend/services/foo.py": _file_entry(10, 20)}, covered_lines=10, num_statements=20)
        report = gen.generate_report(head, base)
        assert "-25.0pp" in report
        assert "📉" in report

    def test_report_table_includes_all_groups(self):
        head = _coverage_data(
            files={
                "backend/services/foo.py": _file_entry(10, 10),
                "backend/models/bar.py": _file_entry(5, 5),
            },
            covered_lines=15, num_statements=15,
        )
        report = gen.generate_report(head, base_data=None)
        assert "backend/services" in report
        assert "backend/models" in report
