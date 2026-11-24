"""Tests for scripts/check_prompt_size_budget.py --staged (ST-23, BLG-GOV-421, EPIC-04, v9.18).

Each test builds a throwaway git repo with a copy of the script, one over-cap
prompt and its baseline, so the staged and working-tree sizes can differ.
"""
import json
import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = 68_500


# No GIT_DIR/GIT_INDEX_FILE/GIT_WORK_TREE from a calling hook, and no user git
# config (commit signing), so the throwaway repo never touches the real one.
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"})


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=ENV)


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "claude" / "system").mkdir(parents=True)
    shutil.copy(os.path.join(ROOT, "scripts", "check_prompt_size_budget.py"), tmp_path / "scripts")
    (tmp_path / "claude" / "system" / "big_prompt.md").write_text("a" * (CAP + 1000))
    (tmp_path / "claude" / "system" / "small_prompt.md").write_text("b" * 100)
    (tmp_path / "scripts" / "prompt_size_baseline.json").write_text(json.dumps({"claude/system/big_prompt.md": CAP + 1000}))
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "seed")
    return tmp_path


def check(repo, *args):
    p = subprocess.run([sys.executable, str(repo / "scripts" / "check_prompt_size_budget.py"), *args],
                       capture_output=True, text=True, env=ENV)
    return p.returncode, p.stdout


def test_staged_growth_past_baseline_fails(repo):
    (repo / "claude/system/big_prompt.md").write_text("a" * (CAP + 1001))
    git(repo, "add", "claude/system/big_prompt.md")
    code, out = check(repo, "--staged")
    assert code == 1
    assert "exceeded (staged)" in out and "big_prompt.md: 69501 bytes > limit 69500 (baseline)" in out


def test_staged_mode_ignores_unstaged_growth(repo):
    (repo / "claude/system/big_prompt.md").write_text("a" * (CAP + 5000))
    assert check(repo, "--staged")[0] == 0
    assert check(repo)[0] == 1  # the working-tree mode still sees it


def test_staged_small_prompt_crossing_the_cap_fails(repo):
    (repo / "claude/system/small_prompt.md").write_text("b" * (CAP + 1))
    git(repo, "add", "claude/system/small_prompt.md")
    code, out = check(repo, "--staged")
    assert code == 1 and "(cap)" in out


def test_staged_baseline_raise_in_the_same_commit_passes(repo):
    (repo / "claude/system/big_prompt.md").write_text("a" * (CAP + 2000))
    (repo / "scripts/prompt_size_baseline.json").write_text(json.dumps({"claude/system/big_prompt.md": CAP + 2000}))
    git(repo, "add", "-A")
    assert check(repo, "--staged")[0] == 0


def test_staged_mode_checks_top_level_files_only(repo):
    (repo / "claude/system/templates").mkdir()
    (repo / "claude/system/templates/nested_prompt.md").write_text("c" * (CAP + 10))
    git(repo, "add", "-A")
    assert check(repo, "--staged")[0] == 0
    assert check(repo)[0] == 0  # both modes agree


def test_staged_mode_reports_an_unmerged_prompt_instead_of_crashing(repo):
    git(repo, "checkout", "-q", "-b", "side")
    (repo / "claude/system/small_prompt.md").write_text("side")
    git(repo, "commit", "-q", "-am", "side")
    git(repo, "checkout", "-q", "-")
    (repo / "claude/system/small_prompt.md").write_text("main")
    git(repo, "commit", "-q", "-am", "main")
    subprocess.run(["git", "-C", str(repo), "merge", "side"], capture_output=True, env=ENV)  # conflicts
    code, out = check(repo, "--staged")
    assert code == 0
    assert "Skipped claude/system/small_prompt.md: unresolved merge conflict" in out


def test_hook_triggers_on_the_script_itself():
    hook = open(os.path.join(ROOT, ".githooks", "pre-commit")).read()
    assert "^scripts/check_prompt_size_budget\\.py$" in hook


def test_workflow_runs_on_push_to_main():
    text = open(os.path.join(ROOT, ".github", "workflows", "prompt-size-budget.yml")).read()
    on_block = text.split("\non:\n", 1)[1].split("\njobs:", 1)[0]
    assert "\n  push:\n    branches:\n      - main\n" in on_block


def test_pre_commit_hook_runs_the_staged_check():
    hook = open(os.path.join(ROOT, ".githooks", "pre-commit")).read()
    assert "python3 scripts/check_prompt_size_budget.py --staged" in hook
