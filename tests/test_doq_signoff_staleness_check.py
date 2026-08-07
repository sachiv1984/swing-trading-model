"""
Tests for scripts/check_doq_signoff_staleness.py — ST-18 (EPIC-04, v8.3, BLG-QA-98).

Exercises the pure detection function directly against synthetic fixture
text, including the deliberately-stale case required by the story's own
AC ("fails on a synthetic Pending-row test case").
"""

import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_doq_signoff_staleness.py"
spec = importlib.util.spec_from_file_location("check_doq_signoff_staleness", SCRIPT_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules["check_doq_signoff_staleness"] = mod
spec.loader.exec_module(mod)


CLEAN_QA_EVIDENCE = """\
| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | some_spec.md | did the thing | AC met | Pass | None |
| ST-02 | some_spec.md | did another thing | AC met | Pass with notes | None |

- Signed off by: Director of Quality
- Date: 2026-08-06
"""

SYNTHETIC_PENDING_ROW = """\
| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | some_spec.md | did the thing | AC met | Pass | None |
| ST-02 | some_spec.md | did another thing | AC met | Pending DoQ | None |

- Signed off by: Director of Quality
- Date: 2026-08-06
"""

SYNTHETIC_AWAITING_QA_ROW = """\
| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | some_spec.md | did the thing | AC met | Awaiting QA | None |

- Signed off by: Director of Quality
- Date: 2026-08-06
"""


def test_clean_evidence_has_no_findings():
    assert mod.find_stale_placeholders(CLEAN_QA_EVIDENCE) == []


def test_synthetic_pending_row_is_flagged():
    """AC: fails on a synthetic Pending-row test case."""
    findings = mod.find_stale_placeholders(SYNTHETIC_PENDING_ROW)
    assert len(findings) == 1
    line_no, line_text = findings[0]
    assert "Pending DoQ" in line_text
    assert line_no == 4


def test_synthetic_awaiting_qa_row_is_flagged():
    findings = mod.find_stale_placeholders(SYNTHETIC_AWAITING_QA_ROW)
    assert len(findings) == 1
    assert "Awaiting QA" in findings[0][1]


def test_multiple_stale_rows_all_flagged():
    text = SYNTHETIC_PENDING_ROW + "\n" + SYNTHETIC_AWAITING_QA_ROW
    findings = mod.find_stale_placeholders(text)
    assert len(findings) == 2


def test_pass_with_notes_is_not_flagged():
    """'Pass with notes' must not false-positive-match on substring overlap."""
    text = "| ST-09 | spec.md | thing | AC | Pass with notes | None |"
    assert mod.find_stale_placeholders(text) == []


def test_prose_quoting_placeholder_strings_is_not_flagged():
    """A row that merely *describes* the placeholder strings by name (e.g.
    this script's own ST-18 evidence row) must not be flagged — only a
    placeholder occupying its own standalone table cell counts. Regression
    test for the self-referential false positive found on PR #1260 (ST-18's
    own qa_evidence_EPIC-04.md row quotes 'Pending DoQ'/'Awaiting QA' in its
    'What was built' prose)."""
    text = (
        '| ST-18 | scripts/check_doq_signoff_staleness.py | Pre-merge lint '
        'catching residual "Pending DoQ"/"Awaiting QA" placeholders in the '
        'active cycle\'s qa_evidence files | Lint check added | Pass | None |'
    )
    assert mod.find_stale_placeholders(text) == []
