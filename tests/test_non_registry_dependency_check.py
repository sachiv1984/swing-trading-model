"""
Non-registry dependency specifier guard — ST-29 (EPIC-07, v9.7, BLG-SEC-38).

Unit tests for scripts/check_non_registry_dependencies.py's detection logic, plus a
regression guard confirming the real backend/requirements.txt and package.json have
zero violations today. Mirrors the existing test_flaky_quarantine_format.py /
test_playwright_skip_only_check.py convention for this class of grep-based CI lint.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_non_registry_dependencies import (  # noqa: E402
    check_package_json,
    check_requirements_txt,
)

REPO_ROOT = Path(__file__).parent.parent


def test_pip_git_ssh_specifier_is_flagged():
    """The exact scenario this story exists to catch: a deliberately-introduced PR
    adding a git+ssh dependency."""
    text = "fastapi==0.135.1\nsome-package @ git+ssh://git@github.com/example/repo.git@main\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1
    assert "git+ssh" in violations[0]


def test_pip_git_https_specifier_is_flagged():
    text = "some-package @ git+https://github.com/example/repo.git\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1
    assert "git+https" in violations[0]


def test_pip_file_specifier_is_flagged():
    text = "some-package @ file:///home/user/local-package\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1
    assert "file:" in violations[0]


def test_pip_editable_git_install_is_flagged():
    text = "-e git+ssh://git@github.com/example/repo.git#egg=some_package\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1


def test_pip_pinned_registry_version_is_not_flagged():
    text = "fastapi==0.135.1\nnumpy==2.4.6\n"
    assert check_requirements_txt(text) == []


def test_pip_comments_and_blank_lines_are_ignored():
    text = "# a comment mentioning git+ssh://example for illustration\n\nfastapi==0.135.1\n"
    assert check_requirements_txt(text) == []


def test_npm_git_ssh_dependency_is_flagged():
    pkg = json.dumps({"dependencies": {"some-lib": "git+ssh://git@github.com/example/repo.git"}})
    violations = check_package_json(pkg)
    assert len(violations) == 1
    assert "some-lib" in violations[0]


def test_npm_file_dependency_is_flagged():
    pkg = json.dumps({"devDependencies": {"local-tool": "file:../local-tool"}})
    violations = check_package_json(pkg)
    assert len(violations) == 1
    assert "local-tool" in violations[0]


def test_npm_registry_semver_range_is_not_flagged():
    pkg = json.dumps({"dependencies": {"react": "^19.0.0"}, "devDependencies": {"vite": "~7.1.0"}})
    assert check_package_json(pkg) == []


def test_npm_malformed_json_reports_a_violation_not_a_crash():
    assert len(check_package_json("{not valid json")) == 1


def test_real_requirements_txt_has_no_violations_today():
    requirements_txt = REPO_ROOT / "backend" / "requirements.txt"
    assert check_requirements_txt(requirements_txt.read_text()) == []


def test_real_package_json_has_no_violations_today():
    package_json = REPO_ROOT / "package.json"
    assert check_package_json(package_json.read_text()) == []
