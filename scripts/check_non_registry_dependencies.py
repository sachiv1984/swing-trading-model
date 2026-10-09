#!/usr/bin/env python3
"""
CI guard rejecting non-registry dependency specifiers (ST-29, BLG-SEC-38, EPIC-07,
v9.7; hardened ST-19, BLG-SEC-39, EPIC-04, v9.8; hardened again ST-06, BLG-SEC-40,
EPIC-02, v9.9 -- bare `-e .`/`-e ..` pip installs, and an npm-workspace-local
`file:` lockfile entry false positive).

A dependency pinned to a VCS ref (`git+ssh://`, `git+https://`, `git+http://`,
`git://`, `hg+...`, `svn+...`, `bzr+...`), a local/relative path, a direct tarball
URL, or an npm GitHub shorthand bypasses the package registry entirely -- no
published, versioned, checksummed artefact exists for it, so a supply-chain review
(`pip-audit`, `npm audit`, the dependency-vuln-rescan cadence) cannot see it, and the
exact code that ships is whatever the referenced ref/path/URL happened to contain at
install time, not a reproducible, auditable release.

Scans:
- backend/requirements.txt and backend/requirements-dev.txt (pip) -- also flags `-r`/`--requirement` includes, since
  they pull in a second file this guard does not itself scan.
- package.json (npm)
- package-lock.json (npm) -- flags any resolved package whose "resolved" URL is not
  served from the npm registry (catches a lockfile that was regenerated against a
  non-registry source even if package.json's own version range looks clean).

Usage: python3 scripts/check_non_registry_dependencies.py
Exit code 0 = no violations, 1 = violations found (prints each one).
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REQUIREMENTS_TXT = REPO_ROOT / "backend" / "requirements.txt"
# ST-43 (BLG-OPS-178, EPIC-06, v9.11): test-only packages moved here; same rules.
REQUIREMENTS_DEV_TXT = REPO_ROOT / "backend" / "requirements-dev.txt"
PACKAGE_JSON = REPO_ROOT / "package.json"
PACKAGE_LOCK_JSON = REPO_ROOT / "package-lock.json"

_NPM_REGISTRY_PREFIX = "https://registry.npmjs.org/"

# pip: VCS-ref specifiers -- `git+ssh://`, `git+https://`, `git+http://`, `hg+https://`,
# `svn+ssh://`, `bzr+http://`, etc. (any of the 4 VCS pip supports, any transport).
# Case-insensitive so `GIT+SSH://` is also caught.
_PIP_VCS_RE = re.compile(r"\b(git|hg|svn|bzr)\+[a-z0-9.+-]+://", re.IGNORECASE)

# pip: bare VCS scheme with no explicit transport (`git://`, `hg://`, ...).
_PIP_BARE_VCS_RE = re.compile(r"\b(git|hg|svn|bzr)://", re.IGNORECASE)

# pip: local file scheme.
_PIP_FILE_RE = re.compile(r"\bfile:", re.IGNORECASE)

# pip: PEP 508 direct URL reference (`name @ https://...`) or a bare URL requirement
# line (`https://example.com/pkg.whl`), including plain `http://` (not just `https://`).
_PIP_DIRECT_URL_RE = re.compile(r"(@\s*|^)(https?|ftp)://", re.IGNORECASE)

# pip: local/relative path install (`./pkg`, `../pkg`, `/abs/pkg`, `~/pkg`), with or
# without a leading `-e` editable-install flag.
_PIP_LOCAL_PATH_RE = re.compile(r"^(-e\s+)?(\.{1,2}/|/|~/)")

# pip: bare `.`/`..` with no trailing slash (`-e .`, `-e ..`, or no `-e` at all) --
# installs the current/parent directory as the package itself. Not matched by
# _PIP_LOCAL_PATH_RE above, which requires a trailing `/` after the dot(s).
_PIP_BARE_DOT_PATH_RE = re.compile(r"^(-e\s+)?\.{1,2}$")

# pip: `-r other.txt` / `--requirement other.txt` include -- pulls in a second file
# this guard does not itself scan, so treat the include as a violation to catch.
_PIP_INCLUDE_RE = re.compile(r"^(-r\b|--requirement\b)")

# npm: package.json dependency *values* using a non-registry protocol or shorthand.
# `github:user/repo`, `git+ssh|git+https|git+http|git+git|git://|file:|link:`
# (case-insensitive for upper-case schemes).
_NPM_NON_REGISTRY_RE = re.compile(
    r"^(git\+ssh|git\+https|git\+http|git\+git|git://|github:|file:|link:)",
    re.IGNORECASE,
)

# npm: direct tarball/HTTP(S) URL as the dependency value.
_NPM_URL_RE = re.compile(r"^https?://", re.IGNORECASE)

# npm: bare GitHub shorthand (`user/repo`, optionally `#ref`) with no scheme prefix.
# Deliberately narrow (word chars/dots/dashes either side of exactly one slash, plus
# an optional `#ref`) so it does not false-positive on semver ranges, which never
# contain a bare `/` of this shape.
_NPM_SHORTHAND_RE = re.compile(r"^[A-Za-z0-9][\w.-]*/[\w.-]+(#[\w.-]+)?$")


def _strip_pip_comment(line: str) -> str:
    """Drop a trailing `# ...` comment so comment text (e.g. a note that mentions
    `git+ssh` in prose) is never matched as a violation. Safe for VCS `#egg=` ref
    fragments too, since the VCS scheme always appears before the first `#`."""
    return line.split("#", 1)[0].strip()


def check_requirements_txt(text: str, label: str = "backend/requirements.txt") -> list:
    violations = []
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        matchable = _strip_pip_comment(stripped)
        if not matchable:
            continue
        if _PIP_INCLUDE_RE.search(matchable):
            violations.append(
                f"{label}:{lineno}: -r/--requirement include bypasses "
                f"this guard's scan of the referenced file: {stripped!r}"
            )
            continue
        if (
            _PIP_VCS_RE.search(matchable)
            or _PIP_BARE_VCS_RE.search(matchable)
            or _PIP_FILE_RE.search(matchable)
            or _PIP_DIRECT_URL_RE.search(matchable)
            or _PIP_LOCAL_PATH_RE.search(matchable)
            or _PIP_BARE_DOT_PATH_RE.search(matchable)
        ):
            violations.append(
                f"{label}:{lineno}: non-registry dependency specifier: {stripped!r}"
            )
    return violations


def check_package_json(text: str) -> list:
    violations = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return [f"package.json: could not parse as JSON ({e}) -- cannot check for non-registry specifiers"]
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        for name, spec in data.get(section, {}).items():
            if not isinstance(spec, str):
                continue
            if (
                _NPM_NON_REGISTRY_RE.match(spec)
                or _NPM_URL_RE.match(spec)
                or _NPM_SHORTHAND_RE.match(spec)
            ):
                violations.append(
                    f"package.json: {section}.{name} uses a non-registry specifier: {spec!r}"
                )
    return violations


def _file_url_is_within_repo(resolved: str) -> bool:
    """A `file:` resolved value is workspace-local (and therefore safe) only if it
    stays within the repository once resolved -- an absolute path, a `~`-relative
    path, or a path that `..`s its way out of the repo is a genuine non-workspace
    local dependency, not an npm workspace member."""
    # Strip the `file:` scheme and at most 2 slashes (the `//[host]` authority
    # separator) -- a 3rd leading slash, if present, is the path's own absolute-path
    # marker and must survive so `file:///abs/path` is still recognised as absolute.
    path_part = re.sub(r"^file:/{0,2}", "", resolved, flags=re.IGNORECASE)
    if not path_part or path_part.startswith("/") or path_part.startswith("~"):
        return False
    try:
        candidate = (REPO_ROOT / path_part).resolve()
        candidate.relative_to(REPO_ROOT.resolve())
        return True
    except ValueError:
        return False


def check_package_lock_json(text: str) -> list:
    violations = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return [f"package-lock.json: could not parse as JSON ({e}) -- cannot check for non-registry specifiers"]
    for pkg_path, entry in data.get("packages", {}).items():
        if not isinstance(entry, dict):
            continue
        resolved = entry.get("resolved")
        if not resolved or entry.get("link"):
            continue
        if resolved.lower().startswith("file:"):
            if _file_url_is_within_repo(resolved):
                continue  # npm-workspace-local reference -- safe, not a violation
            violations.append(
                f"package-lock.json: {pkg_path or '(root)'} resolves from a non-registry, "
                f"non-workspace local path: {resolved!r}"
            )
            continue
        if not resolved.startswith(_NPM_REGISTRY_PREFIX):
            violations.append(
                f"package-lock.json: {pkg_path or '(root)'} resolves from a non-registry source: {resolved!r}"
            )
    return violations


def main() -> int:
    violations = []
    if REQUIREMENTS_TXT.exists():
        violations += check_requirements_txt(REQUIREMENTS_TXT.read_text())
    if REQUIREMENTS_DEV_TXT.exists():
        violations += check_requirements_txt(REQUIREMENTS_DEV_TXT.read_text(), "backend/requirements-dev.txt")
    if PACKAGE_JSON.exists():
        violations += check_package_json(PACKAGE_JSON.read_text())
    if PACKAGE_LOCK_JSON.exists():
        violations += check_package_lock_json(PACKAGE_LOCK_JSON.read_text())

    if violations:
        for v in violations:
            print(v)
        print(f"\n{len(violations)} violation(s) found.")
        return 1
    print("Non-registry dependency check: PASSED — no git/file/link/URL-scheme dependency specifiers found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
