"""scripts/check_staged_state_path.py (BLG-GOV-430 lesson, 2026-11-19).

Fails a commit that stages .claude_current_state.json pointing at an
execution_state.json the commit/branch does not contain, from Sprint Execution
on. Exercised against a real temporary git repo, so the index is real.
"""

import importlib.util
import json
import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "check_staged_state_path.py"
_spec = importlib.util.spec_from_file_location("check_staged_state_path", SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

CYCLE = "2026-11-18__release-v9.18"
PATH = f"claude/cycles/{CYCLE}/execution_state.json"


def state(status="Executing", path=PATH, cycle=CYCLE):
    return {"active_cycle": cycle, "status": status, "execution_state_path": path}


@pytest.fixture
def repo(tmp_path):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    run = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, env=env)  # noqa: E731
    run("init", "-q")
    (tmp_path / "README").write_text("x")
    run("add", "README")
    run("commit", "-q", "-m", "init")
    return tmp_path, run


def run_check(cwd):
    return subprocess.run(["python3", str(SCRIPT)], cwd=cwd, capture_output=True, text=True)


def test_executing_without_state_file_fails(repo):
    root, git = repo
    (root / ".claude_current_state.json").write_text(json.dumps(state()))
    git("add", ".claude_current_state.json")
    r = run_check(root)
    assert r.returncode == 1 and "not in this commit or the branch" in r.stderr


def test_executing_with_state_file_staged_in_same_commit_passes(repo):
    root, git = repo
    (root / ".claude_current_state.json").write_text(json.dumps(state()))
    (root / PATH).parent.mkdir(parents=True)
    (root / PATH).write_text("{}")
    git("add", ".claude_current_state.json", PATH)
    assert run_check(root).returncode == 0


def test_executing_with_state_file_already_committed_passes(repo):
    root, git = repo
    (root / PATH).parent.mkdir(parents=True)
    (root / PATH).write_text("{}")
    git("add", PATH)
    git("commit", "-q", "-m", "state")
    (root / ".claude_current_state.json").write_text(json.dumps(state()))
    git("add", ".claude_current_state.json")
    assert run_check(root).returncode == 0


def test_untracked_state_file_on_disk_does_not_count(repo):
    # The v9.18 case: the file existed in the working tree (EPIC branch) but not on main's index.
    root, git = repo
    (root / PATH).parent.mkdir(parents=True)
    (root / PATH).write_text("{}")
    (root / ".claude_current_state.json").write_text(json.dumps(state()))
    git("add", ".claude_current_state.json")
    assert run_check(root).returncode == 1


def test_pre_execution_status_does_not_need_the_file(repo):
    root, git = repo
    (root / ".claude_current_state.json").write_text(json.dumps(state(status="Sprint_Planning_Complete")))
    git("add", ".claude_current_state.json")
    assert run_check(root).returncode == 0


def test_wrong_path_for_active_cycle_fails(repo):
    root, git = repo
    (root / ".claude_current_state.json").write_text(json.dumps(state(status="Sprint_Planning_Complete", path="claude/cycles/old/execution_state.json")))
    git("add", ".claude_current_state.json")
    r = run_check(root)
    assert r.returncode == 1 and "active_cycle expects" in r.stderr


def test_state_file_not_staged_is_skipped(repo):
    root, _ = repo
    (root / ".claude_current_state.json").write_text(json.dumps(state()))  # on disk, not staged
    assert run_check(root).returncode == 0


def test_status_list_matches_the_ci_test():
    src = (Path(__file__).parent / "test_state_execution_path_consistency.py").read_text()
    for s in mod.PRE_EXECUTION_STATUSES:
        assert f'"{s}"' in src
