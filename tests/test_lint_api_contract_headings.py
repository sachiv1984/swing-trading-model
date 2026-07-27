"""
Unit tests for the API contract heading-level compliance lint (ST-12,
EPIC-12, v7.8, BLG-OPS-117) — scripts/lint_api_contract_headings.py.

Includes the negative test required by the story's own AC: "Lint step
confirmed to catch a deliberately-miscoded test heading (negative test)
before merge."
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lint_api_contract_headings import find_heading_level_violations, lint_directory  # noqa: E402


def test_correctly_leveled_heading_produces_no_violation():
    text = "## GET /positions\n\nSome contract body.\n"
    assert find_heading_level_violations(text) == []


def test_deliberately_miscoded_heading_is_caught():
    # Negative test (AC requirement): a heading one level too deep — the
    # exact silent-fail case documented in CLAUDE.md §2 — must be flagged.
    text = "### GET /positions\n\nSome contract body.\n"
    violations = find_heading_level_violations(text)
    assert len(violations) == 1
    assert "level 3" in violations[0]
    assert "GET /positions" in violations[0]


def test_heading_one_level_too_shallow_is_also_caught():
    text = "# POST /trades\n\nSome contract body.\n"
    violations = find_heading_level_violations(text)
    assert len(violations) == 1
    assert "level 1" in violations[0]


def test_multiple_violations_all_reported():
    text = (
        "### GET /positions\n\nBody.\n\n"
        "## POST /trades\n\nCorrectly leveled, no violation.\n\n"
        "#### DELETE /watchlist/{id}\n\nBody.\n"
    )
    violations = find_heading_level_violations(text)
    assert len(violations) == 2


def test_non_endpoint_headings_are_ignored():
    # Regular section headings (no HTTP method + path) must not be flagged,
    # regardless of depth.
    text = "## Overview\n\n### Notes\n\n#### Deeply Nested Section\n"
    assert find_heading_level_violations(text) == []


def test_correctly_leveled_headings_across_multiple_methods():
    text = (
        "## GET /positions\n\nBody.\n\n"
        "## POST /positions\n\nBody.\n\n"
        "## PATCH /positions/{id}\n\nBody.\n\n"
        "## DELETE /positions/{id}\n\nBody.\n"
    )
    assert find_heading_level_violations(text) == []


def test_real_contracts_directory_has_zero_violations():
    """
    Regression guard: the actual docs/specs/api_contracts/ directory must
    lint clean today. If this starts failing, either a real heading-level
    defect was introduced (fix the contract) or a new legitimately-nested
    non-canonical file was added (add it to NON_CANONICAL_FILES with a
    documented reason, per the one existing exemption).
    """
    contracts_dir = Path(__file__).parent.parent / "docs" / "specs" / "api_contracts"
    assert lint_directory(contracts_dir) == 0
