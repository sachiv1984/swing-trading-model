"""Tests for scripts/compute_rebalance_diagnostics.py (ST-25, EPIC-04, v9.9, BLG-GOV-352)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from compute_rebalance_diagnostics import parse_cycles, pvr_diagnostic, skill_silo_diagnostic, skill_silo_history  # noqa: E402

FIXTURE = """\
## v3.0 — Fixture Cycle C — 2026-01-03
Cycle: 2026-01-01__release-v3.0

### Tech backlog items shipped
- [ST-01] [U] Feature A
- [ST-02] [G] Governance A
- [ST-03] [D] Debt A
- [ST-04] [D] Debt B

---

## v2.0 — Fixture Cycle B — 2026-01-02
Cycle: 2025-12-15__release-v2.0

### Tech backlog items shipped
- [ST-01] [U] Feature B
- [ST-02] [U] Feature C
- [ST-03] [G] Governance B

---

## v1.0 — Fixture Cycle A — 2026-01-01
Cycle: 2025-12-01__release-v1.0

### Tech backlog items shipped
- [ST-01] [P] Pre-work A
- [ST-02] [D] Debt C
"""


def test_parse_cycles_newest_first():
    cycles = parse_cycles(FIXTURE)
    assert [c["cycle"] for c in cycles] == [
        "2026-01-01__release-v3.0",
        "2025-12-15__release-v2.0",
        "2025-12-01__release-v1.0",
    ]


def test_pvr_diagnostic_matches_known_total():
    cycles = parse_cycles(FIXTURE)
    result = pvr_diagnostic(cycles, window=3)
    # U=1(C)+2(B)+0(A)=3, total=4+3+2=9
    assert result["U"] == 3
    assert result["total"] == 9
    assert result["user_value_ratio"] == round(3 / 9, 3)
    assert result["tier"] == "Advisory"


def test_pvr_diagnostic_alert_tier():
    cycles = parse_cycles(FIXTURE)
    result = pvr_diagnostic(cycles, window=1)  # only cycle C: U=1, total=4
    assert result["user_value_ratio"] == 0.25
    assert result["tier"] == "Product Value Alert"


def test_skill_silo_diagnostic_matches_known_total():
    cycles = parse_cycles(FIXTURE)
    result = skill_silo_diagnostic(cycles, window=2)  # cycles C + B
    # governance = G+D+P: C has G=1,D=2 -> 3; B has G=1 -> 1; total governance=4, total stories=4+3=7
    assert result["total"] == 7
    assert result["governance_pct"] == round(100 * 4 / 7, 1)
    assert result["skill_silo_alert"] is True


def test_real_changelog_reproduces_cited_pvr_figure():
    """Regression check against the actual cited figure in .claude_current_state.json:
    U=16/G=41/D=109/P=4 of 170, window v9.4-v9.8 -> user_value_ratio = 0.094."""
    changelog = Path(__file__).resolve().parent.parent / "docs" / "product" / "changelog.md"
    cycles = parse_cycles(changelog.read_text())
    # Pin the window to the cited v9.4-v9.8 range: the live changelog gains a new
    # newest cycle at every post-ship closure, which would otherwise shift window=5.
    start = next(i for i, c in enumerate(cycles) if c["cycle"].endswith("release-v9.8"))
    result = pvr_diagnostic(cycles[start:], window=5)
    assert result["window_cycles"][-1].endswith("release-v9.4")
    assert (result["U"], result["G"], result["D"], result["P"], result["total"]) == (16, 41, 109, 4, 170)
    assert result["user_value_ratio"] == 0.094


def test_skill_silo_uses_pooled_method_not_plain_mean():
    """ST-42 (BLG-GOV-367): roadmap_prompt.md §7.1 names the pooled method.
    Cycles C (4 stories, 3 governance = 75%) and B (3 stories, 1 governance =
    33.3%) pool to 4/7 = 57.1%, whereas the plain mean would be 54.2%."""
    result = skill_silo_diagnostic(parse_cycles(FIXTURE), window=2)
    assert result["method"] == "pooled"
    assert result["governance_pct"] == 57.1
    assert result["governance_pct"] != round((75.0 + 100 / 3) / 2, 1)


def test_real_changelog_restated_skill_silo_readings_are_pooled():
    """ST-42: the four readings restated in roadmap_prompt.md §7.1's method-break
    note (v9.3-v9.5 97/98, v9.5-v9.7 90/103, v9.6-v9.8 84/99, v9.7-v9.9 93/102)."""
    changelog = Path(__file__).resolve().parent.parent / "docs" / "product" / "changelog.md"
    cycles = parse_cycles(changelog.read_text())
    start = next(i for i, c in enumerate(cycles) if c["cycle"].endswith("release-v9.9"))
    history = skill_silo_history(cycles[start:], window=3, readings=5)
    by_newest = {h["window_cycles"][0].split("release-")[1]: h for h in history}
    expected = {"v9.9": (93, 102, 91.2), "v9.8": (84, 99, 84.8), "v9.7": (90, 103, 87.4), "v9.5": (97, 98, 99.0)}
    for newest, (gov, total, pct) in expected.items():
        h = by_newest[newest]
        assert (h["G"] + h["D"] + h["P"], h["total"], h["governance_pct"]) == (gov, total, pct), newest
