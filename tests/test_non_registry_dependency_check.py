"""
Non-registry dependency specifier guard — ST-29 (EPIC-07, v9.7, BLG-SEC-38);
hardened ST-19 (EPIC-04, v9.8, BLG-SEC-39).

Unit tests for scripts/check_non_registry_dependencies.py's detection logic, plus a
regression guard confirming the real backend/requirements.txt, package.json and
package-lock.json have zero violations today. Mirrors the existing
test_flaky_quarantine_format.py / test_playwright_skip_only_check.py convention for
this class of grep-based CI lint.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import check_non_registry_dependencies as guard  # noqa: E402
from check_non_registry_dependencies import (  # noqa: E402
    check_package_json,
    check_package_lock_json,
    check_requirements_txt,
    main,
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


# --- BLG-SEC-39 hardening: previously-missed pip forms ------------------------------


def test_pip_git_http_specifier_is_flagged():
    """git+http (no trailing 's') was not matched by the original git+https-only regex."""
    text = "some-package @ git+http://example.com/example/repo.git\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1
    assert "git+http" in violations[0]


def test_pip_hg_and_svn_and_bzr_specifiers_are_flagged():
    text = (
        "hg-package @ hg+https://example.com/example/repo\n"
        "svn-package @ svn+ssh://example.com/example/repo\n"
        "bzr-package @ bzr+http://example.com/example/repo\n"
    )
    violations = check_requirements_txt(text)
    assert len(violations) == 3


def test_pip_bare_vcs_scheme_is_flagged():
    text = "some-package @ git://example.com/example/repo.git\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1


def test_pip_direct_url_reference_is_flagged():
    """PEP 508 direct URL reference (`name @ https://...`) bypasses the registry
    even with no VCS scheme involved."""
    text = "some-package @ https://example.com/dist/some-package-1.0.0.whl\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1


def test_pip_bare_url_line_is_flagged():
    text = "https://example.com/dist/some-package-1.0.0.tar.gz\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1


def test_pip_relative_and_absolute_local_paths_are_flagged():
    text = "./local-package\n-e ../local-package\n/abs/path/local-package\n~/local-package\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 4


def test_pip_upper_case_scheme_is_flagged():
    text = "some-package @ GIT+SSH://git@github.com/example/repo.git\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 1


def test_pip_bare_dot_editable_install_is_flagged():
    """ST-06 (EPIC-02, v9.9, BLG-SEC-40): `-e .`/`-e ..` with no trailing slash was
    not matched by _PIP_LOCAL_PATH_RE, which requires a trailing `/` after the dot(s)."""
    text = "-e .\n-e ..\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 2


def test_pip_requirement_include_is_flagged():
    text = "-r other-requirements.txt\n--requirement more.txt\n"
    violations = check_requirements_txt(text)
    assert len(violations) == 2
    assert "include" in violations[0]


def test_pip_pinned_version_with_trailing_comment_mentioning_git_is_not_flagged():
    """The false positive this story exists to fix: a clean version pin whose
    trailing comment happens to mention `git+ssh` in prose must not be rejected."""
    text = "fastapi==0.135.1  # pinned, not git+ssh\n"
    assert check_requirements_txt(text) == []


# --- BLG-SEC-39 hardening: previously-missed npm forms -------------------------------


def test_npm_github_shorthand_with_prefix_is_flagged():
    pkg = json.dumps({"dependencies": {"some-lib": "github:example/repo"}})
    violations = check_package_json(pkg)
    assert len(violations) == 1


def test_npm_bare_github_shorthand_is_flagged():
    pkg = json.dumps({"dependencies": {"some-lib": "example/repo"}})
    violations = check_package_json(pkg)
    assert len(violations) == 1


def test_npm_bare_github_shorthand_with_ref_is_flagged():
    pkg = json.dumps({"dependencies": {"some-lib": "example/repo#v1.0.0"}})
    violations = check_package_json(pkg)
    assert len(violations) == 1


def test_npm_tarball_url_is_flagged():
    pkg = json.dumps({"dependencies": {"some-lib": "https://example.com/some-lib-1.0.0.tgz"}})
    violations = check_package_json(pkg)
    assert len(violations) == 1


def test_npm_semver_ranges_with_carets_and_tildes_are_not_flagged():
    """Regression guard for the shorthand regex: must not false-positive on ordinary
    semver ranges, which never contain a bare `owner/repo`-shaped slash."""
    pkg = json.dumps(
        {
            "dependencies": {
                "@radix-ui/react-dialog": "^1.1.15",
                "react": ">=18.0.0 <20.0.0",
                "serve": "14.2.6",
            }
        }
    )
    assert check_package_json(pkg) == []


# --- BLG-SEC-39 hardening: package-lock.json was not scanned at all before -----------


def test_package_lock_non_registry_resolved_url_is_flagged():
    lock = json.dumps(
        {
            "packages": {
                "": {},
                "node_modules/some-lib": {
                    "resolved": "git+ssh://git@github.com/example/some-lib.git",
                },
            }
        }
    )
    violations = check_package_lock_json(lock)
    assert len(violations) == 1
    assert "some-lib" in violations[0]


def test_package_lock_registry_resolved_url_is_not_flagged():
    lock = json.dumps(
        {
            "packages": {
                "": {},
                "node_modules/some-lib": {
                    "resolved": "https://registry.npmjs.org/some-lib/-/some-lib-1.0.0.tgz",
                },
            }
        }
    )
    assert check_package_lock_json(lock) == []


def test_package_lock_link_entry_without_resolved_is_not_flagged():
    """A workspace/local link entry has no `resolved` URL and is not itself an
    external dependency fetch -- must not be treated as a violation."""
    lock = json.dumps({"packages": {"": {}, "node_modules/workspace-pkg": {"link": True}}})
    assert check_package_lock_json(lock) == []


def test_package_lock_npm_workspace_local_file_entry_is_not_flagged():
    """ST-06 (EPIC-02, v9.9, BLG-SEC-40): a `resolved: "file:..."` entry that stays
    within the repo (an npm workspace member) must not be flagged, even without a
    `link` key -- distinct from the already-covered `link`-only case above."""
    lock = json.dumps(
        {
            "packages": {
                "": {},
                "node_modules/workspace-pkg": {"resolved": "file:packages/workspace-pkg"},
            }
        }
    )
    assert check_package_lock_json(lock) == []


def test_package_lock_non_workspace_file_entry_is_still_flagged():
    """The other half of ST-06's AC: a genuine non-workspace `file:` resolved path
    (escaping the repo via `..` or an absolute path) must still be flagged."""
    lock = json.dumps(
        {
            "packages": {
                "": {},
                "node_modules/escaped-pkg": {"resolved": "file:../../outside-the-repo-package"},
                "node_modules/abs-pkg": {"resolved": "file:///home/user/local-package"},
            }
        }
    )
    violations = check_package_lock_json(lock)
    assert len(violations) == 2


def test_package_lock_non_workspace_git_entry_is_still_flagged():
    """Non-`file:` non-workspace resolutions (e.g. a git URL) are unaffected by the
    workspace-local exemption, which only applies to `file:` resolved values."""
    lock = json.dumps(
        {
            "packages": {
                "": {},
                "node_modules/some-lib": {"resolved": "git+ssh://git@github.com/example/some-lib.git"},
            }
        }
    )
    violations = check_package_lock_json(lock)
    assert len(violations) == 1


def test_real_package_lock_json_has_no_violations_today():
    package_lock_json = REPO_ROOT / "package-lock.json"
    assert check_package_lock_json(package_lock_json.read_text()) == []


# --- BLG-SEC-39 hardening: main()'s exit code was previously untested ----------------


def test_main_exits_zero_on_the_current_clean_repo_tree(monkeypatch):
    assert main() == 0


def test_main_exits_non_zero_on_a_violation(tmp_path, monkeypatch, capsys):
    dirty_requirements = tmp_path / "requirements.txt"
    dirty_requirements.write_text("some-package @ git+ssh://git@github.com/example/repo.git\n")
    clean_package_json = tmp_path / "package.json"
    clean_package_json.write_text(json.dumps({"dependencies": {}}))
    clean_package_lock = tmp_path / "package-lock.json"
    clean_package_lock.write_text(json.dumps({"packages": {"": {}}}))

    monkeypatch.setattr(guard, "REQUIREMENTS_TXT", dirty_requirements)
    monkeypatch.setattr(guard, "PACKAGE_JSON", clean_package_json)
    monkeypatch.setattr(guard, "PACKAGE_LOCK_JSON", clean_package_lock)

    exit_code = main()
    out = capsys.readouterr().out

    assert exit_code == 1
    assert "git+ssh" in out
