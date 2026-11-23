"""Tests for scripts/check_e2e_locator_collisions.py (ST-21, BLG-QA-268, EPIC-04, v9.18).

The two v9.17 cases are replayed from fixtures (tests/fixtures/e2e_locator_collisions),
since CI checks out a shallow clone. The rest are small synthetic diffs, one per
form the script claims to handle or to ignore.
"""
import os
import subprocess
import sys
import textwrap

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "check_e2e_locator_collisions.py")
FIX = os.path.join(ROOT, "tests", "fixtures", "e2e_locator_collisions")


def run(diff_file, src_root, tests_dir):
    p = subprocess.run(
        [sys.executable, SCRIPT, "--diff-file", diff_file, "--src-root", src_root, "--tests-dir", tests_dir],
        capture_output=True, text=True,
    )
    return p.returncode, p.stdout


# ------------------------------------------------------------ v9.17 replays

def test_v917_st01_flags_sc_comp_02_03_07():
    code, out = run(f"{FIX}/b2d93f6d/diff.txt", f"{FIX}/b2d93f6d/src", f"{FIX}/b2d93f6d/tests")
    assert code == 1
    assert "compliance-panel.spec.js:169 [SC-COMP-03]" in out
    assert 'matches text this diff adds: "Sorted by what needs attention first"' in out
    assert "compliance-panel.spec.js:260 [SC-COMP-07]" in out
    assert "matches an attribute this diff adds: \"aria-expanded={…}\"" in out
    assert "[SC-COMP-02]" in out  # the same locator, fixed in the same commit


def test_v917_st01_fixed_locators_are_clean():
    code, out = run(f"{FIX}/b2d93f6d/diff.txt", f"{FIX}/b2d93f6d/src", f"{FIX}/b2d93f6d/tests-fixed")
    assert code == 0, out


def test_v917_st03_flags_sc_lbg_03_as_moved_text():
    code, out = run(f"{FIX}/99f16e6d/diff.txt", f"{FIX}/99f16e6d/src", f"{FIX}/99f16e6d/tests")
    assert code == 1
    assert "lifecycle-badge-grace-calendar-days.spec.js:118 [SC-LBG-03]" in out
    assert "moves, hides or re-parents" in out
    assert "<GracePeriodAlertContent>" in out


# --------------------------------------------------------------- synthetic

def make_case(tmp_path, added, removed=(), spec="", component_file=None):
    """A one-file diff of src/pages/Page.js, a spec file and the post-change source."""
    lines = [f"-{l}" for l in removed] + [f"+{l}" for l in added]
    diff = "diff --git a/src/pages/Page.js b/src/pages/Page.js\n--- a/src/pages/Page.js\n+++ b/src/pages/Page.js\n@@ -1 +1 @@\n" + "\n".join(lines) + "\n"
    (tmp_path / "diff.txt").write_text(diff)
    src = tmp_path / "src" / "src" / "pages"
    src.mkdir(parents=True)
    (src / "Page.js").write_text(component_file or "\n".join(added) + "\n")
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "page.spec.js").write_text(textwrap.dedent(spec))
    return run(str(tmp_path / "diff.txt"), str(tmp_path / "src"), str(tests))


SPEC_HEAD = "test('SC-X-01: a case', async ({ page }) => {\n"


@pytest.mark.parametrize("added,locator,flagged", [
    # JSX text on its own line, non-exact substring, case-insensitive
    (["        Review your open trades"], "page.getByText('open trades')", True),
    # exact: true needs the whole string
    (["        Review your open trades"], "page.getByText('open trades', { exact: true })", False),
    # JSX text between tags on one line
    (['<p className="text-xs">Grace ends today</p>'], "page.getByText(/grace ends/i)", True),
    # a template literal, with a sample value for ${n}
    (["const s = `Next ends in ${n} days`;"], "page.getByText(/ends in 2 days/)", True),
    # a regex matching only the sample value is not a collision
    (["const s = `Item ${n}`;"], "page.getByRole('button', { name: /1|news/i })", False),
    # a two-letter overlap is not a collision
    (['const label = "GBP";'], "page.getByText('BP')", False),
    # a class list is not visible text
    (['<div className="text-app-muted font-medium">'], "page.getByText('font-medium')", False),
    # getByRole with a name
    (['<button aria-label="Toggle theme">'], "page.getByRole('button', { name: 'Toggle theme' })", True),
    # a scoped locator is skipped: scoping is the fix
    (["        Review your open trades"], "page.getByTestId('panel').getByText('open trades')", False),
    # comparison code is not JSX text
    (["{price > 0 && stop < price && <Badge />}"], "page.getByText(/0 && stop/)", False),
    # an attribute presence selector
    (["<button aria-expanded={open}>"], "page.locator('main button[aria-expanded]')", True),
    # a dynamic value never matches a value selector
    (["<button title={label}>"], "page.locator('button[title=\"Zoom in\"]')", False),
    # a literal value matches its own value selector
    (['<button title="Zoom in">'], "page.locator('button[title=\"Zoom in\"]')", True),
    # data-testid is the scoped form, never a collision
    (['<div data-testid="grace-view">'], "page.locator('[data-testid=\"grace-view\"]')", False),
    # data-title is not title
    (['<div data-title="Zoom in">'], "page.locator('button[title=\"Zoom in\"]')", False),
    # snake_case keys are not visible text (PR #2311 DoQ review: 'Price' vs current_price)
    (["const v = row['current_price'];"], "page.getByText('Price')", False),
    (["const k = 'open_positions';"], "page.getByRole('columnheader', { name: 'Positions' })", False),
    # a Tailwind arbitrary-variant class list is not visible text
    (['<SelectTrigger className="[&>span]:line-clamp-1 flex h-9 w-full">'], "page.getByText(/line-clamp/)", False),
])
def test_synthetic_forms(tmp_path, added, locator, flagged):
    code, out = make_case(tmp_path, added, spec=SPEC_HEAD + f"  await expect({locator}).toBeVisible();\n}});\n")
    assert (code == 1) is flagged, out


def test_text_unchanged_on_both_sides_is_not_flagged(tmp_path):
    # A class sweep rewrites the line, not the text (PR #2311 DoQ review: 249 hits on 071a43f3).
    code, out = make_case(tmp_path, added=['<p className="text-app-muted">Unable to load heat data</p>'],
                          removed=['<p className="text-slate-400">Unable to load heat data</p>'],
                          spec=SPEC_HEAD + "  await expect(page.getByText('Unable to load heat data')).toBeVisible();\n});\n")
    assert code == 0, out


def test_removed_text_is_flagged(tmp_path):
    code, out = make_case(tmp_path, added=["<p>New copy</p>"], removed=["        Old banner copy here"],
                          spec=SPEC_HEAD + "  await expect(page.getByText('Old banner copy')).toBeVisible();\n});\n")
    assert code == 1 and "matches text this diff removes" in out


def test_moved_component_text_is_flagged(tmp_path):
    component = textwrap.dedent("""\
        function Banner() {
          return <p>Your grace period ends soon</p>;
        }

        export default function Page() {
          return <Collapsed><Banner /></Collapsed>;
        }
        """)
    code, out = make_case(tmp_path, added=["  return <Collapsed><Banner /></Collapsed>;"],
                          removed=["  return <Banner />;"], component_file=component,
                          spec=SPEC_HEAD + "  await expect(page.getByText(/grace period ends/i)).toBeVisible();\n});\n")
    assert code == 1 and "<Banner>" in out


@pytest.mark.parametrize("path", ["src/lib/positionUrgency.test.js", "src/test-utils/knownFailing.js", "src/lib/__tests__/x.js", "src/setupTests.js"])
def test_unit_test_files_are_not_rendered_source(tmp_path, path):
    diff = f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -1 +1 @@\n+        Review your open trades\n"
    (tmp_path / "diff.txt").write_text(diff)
    (tmp_path / "src").mkdir()
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "a.spec.js").write_text("test('SC-X-01: a', async ({ page }) => {\n  await page.getByText('open trades');\n});\n")
    code, out = run(str(tmp_path / "diff.txt"), str(tmp_path / "src"), str(tests))
    assert code == 0 and "not needed" in out


def test_no_src_change_exits_zero(tmp_path):
    (tmp_path / "diff.txt").write_text("diff --git a/README.md b/README.md\n+++ b/README.md\n+hello\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    code, out = run(str(tmp_path / "diff.txt"), str(tmp_path / "src"), str(tmp_path / "tests"))
    assert code == 0 and "not needed" in out
