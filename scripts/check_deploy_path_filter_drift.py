#!/usr/bin/env python3
"""
Staging/production deploy path-filter drift detector.

ST-14 (BLG-OPS-90, EPIC-03, v9.0). Covers both confirmed incident shapes:

1. Missing-deploy (BLG-OPS-82): a runtime-read file changes but isn't
   covered by a deploy path filter, so the change silently doesn't
   trigger a redeploy.
2. Dashboard-only build-path filter drift (this item's own gate-clearing
   incident, commit e9c73f58): the *production* filter lives exclusively
   in the Render dashboard (render.yaml's own comment: "Production
   services are managed separately in the Render dashboard"), invisible
   to a repo-only search — so a human reviewer has no way to know it
   exists, let alone whether it still covers everything the app reads.

Design (see docs/ops/render_build_deploy_path_filter_audit.md for the
full narrative this formalises):

- KNOWN_RUNTIME_READ_FILES is a human-curated inventory of every non-.py
  file the running application actually reads at runtime (not build-time
  tooling inputs like package.json/requirements.txt, not CLI-only
  scripts). Mirrors the audit doc's own Runtime File-Read Inventory —
  kept in sync with it deliberately, not re-derived by static analysis
  every run, because indirect file-path construction (e.g.
  ticker_universe_service.py's `_CSV_PATH = os.path.join(...)` variable,
  rather than a literal path inline at the open() call) makes a fully
  automatic AST-based inventory unreliable — a naive scan both misses
  indirect reads and can flag build-time-only tooling as false positives.
  Each entry here is checked against BOTH filters below; any file not
  covered by AT LEAST ONE is a hard failure (addresses incident shape 1).

- Staging's filter is parsed live from
  .github/workflows/staging-deploy.yml's own `on.push.paths` list — this
  one genuinely can be read automatically, since it's a real repo file,
  so this script always reflects its current state rather than a stale
  copy.

- Production's filter is NOT live-queryable (dashboard-only, incident
  shape 2) — this script reads the checked-in snapshot at
  docs/ops/render_production_build_filter_snapshot.json instead, which a
  human with Render dashboard access maintains. This turns a previously
  prose-only audit-doc fact into a structured, script-comparable
  artifact — the actual fix for incident shape 2's "invisible to a
  repo-only search" root cause: the filter's *last confirmed value* is
  now a real, diffable repo file. It does not, and cannot, detect a
  *live* dashboard change nobody has recorded here — that residual gap
  is inherent to dashboard-only configuration and is disclosed, not
  silently assumed away (see the script's own final warning below).

- Best-effort static scan (`_static_scan_candidates`) additionally greps
  backend/**/*.py for common non-.py file-read patterns not already in
  KNOWN_RUNTIME_READ_FILES, as a soft, non-blocking prompt to keep the
  known inventory current — printed as a warning, never a failure,
  since a heuristic grep has real false-positive/false-negative risk
  (as this script's own module docstring above documents finding) and
  must not gate CI on an unreliable signal.

Exit code: 0 if all known runtime-read files are covered by at least one
filter; 1 if any is not (hard failure — same convention as
scripts/check_api_performance_baseline_drift.py).
"""
import fnmatch
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Mirrors docs/ops/render_build_deploy_path_filter_audit.md's Runtime
# File-Read Inventory. `optional: True` entries are checked only if the
# file actually exists (e.g. feature_flags.json, a hypothetical file the
# audit doc flags as a gap-in-waiting, not yet added to the repo).
KNOWN_RUNTIME_READ_FILES = [
    {"path": "docs/product/changelog.md", "optional": False},
    {"path": "backend/tickers_full_list.csv", "optional": False},
    {"path": "feature_flags.json", "optional": True},
]

STAGING_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "staging-deploy.yml"
PRODUCTION_SNAPSHOT = REPO_ROOT / "docs" / "ops" / "render_production_build_filter_snapshot.json"


def _parse_staging_filter_paths() -> list:
    """Extract the on.push.paths list from staging-deploy.yml without a
    full YAML parse (avoids a PyYAML dependency for a 6-line list) —
    reads the literal `- 'pattern'` / `- "pattern"` lines between the
    `paths:` key and the next non-list line."""
    text = STAGING_WORKFLOW.read_text()
    lines = text.splitlines()
    paths = []
    in_paths_block = False
    for line in lines:
        stripped = line.strip()
        if stripped == "paths:":
            in_paths_block = True
            continue
        if in_paths_block:
            m = re.match(r"^-\s+['\"]?([^'\"#]+)['\"]?", stripped)
            if m:
                paths.append(m.group(1).strip())
                continue
            if stripped and not stripped.startswith("#"):
                break  # left the paths: list
    return paths


def _covered_by_staging(file_path: str, staging_paths: list) -> bool:
    for pattern in staging_paths:
        if fnmatch.fnmatch(file_path, pattern):
            return True
        # fnmatch's `**` doesn't recurse across `/` the way gitignore-style
        # globs do (e.g. `backend/**` should match `backend/foo/bar.csv`,
        # not just `backend/bar.csv`) — handle the `<prefix>/**` shape
        # explicitly, matching GitHub Actions' own path-filter semantics.
        if pattern.endswith("/**") and file_path.startswith(pattern[:-2]):
            return True
    return False


def _covered_by_production(file_path: str, snapshot: dict) -> bool:
    root_dir = snapshot.get("root_directory")
    if root_dir and snapshot.get("root_directory_is_implicit_default_scope"):
        if file_path == root_dir or file_path.startswith(root_dir.rstrip("/") + "/"):
            return True
    for included in snapshot.get("included_paths", []):
        if file_path == included or fnmatch.fnmatch(file_path, included):
            return True
    return False


def _static_scan_candidates() -> list:
    """Best-effort, soft-only signal — see module docstring. Greps
    backend/**/*.py for common non-.py runtime file-read call shapes and
    returns any literal path found that isn't already in
    KNOWN_RUNTIME_READ_FILES."""
    known_paths = {e["path"] for e in KNOWN_RUNTIME_READ_FILES}
    pattern = re.compile(r"""(?:open|read_text|read_csv)\([^)]*['"]([^'"]+\.(?:json|csv|md|yaml|yml))['"]""")
    candidates = set()
    for py_file in (REPO_ROOT / "backend").rglob("*.py"):
        if ".venv" in py_file.parts or "__pycache__" in py_file.parts or "test_data" in py_file.parts:
            continue
        try:
            text = py_file.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for m in pattern.finditer(text):
            candidate = m.group(1)
            if candidate not in known_paths and not candidate.startswith(("http://", "https://")):
                candidates.add(candidate)
    return sorted(candidates)


def main() -> int:
    staging_paths = _parse_staging_filter_paths()
    if not staging_paths:
        print(f"::error::Could not parse any paths: entries from {STAGING_WORKFLOW} — check the file wasn't restructured.")
        return 1

    if not PRODUCTION_SNAPSHOT.exists():
        print(f"::error::{PRODUCTION_SNAPSHOT} is missing — cannot check production filter coverage.")
        return 1
    snapshot = json.loads(PRODUCTION_SNAPSHOT.read_text())

    failures = []
    for entry in KNOWN_RUNTIME_READ_FILES:
        file_path = entry["path"]
        if entry["optional"] and not (REPO_ROOT / file_path).exists():
            continue  # e.g. feature_flags.json, not yet added — nothing to check yet

        covered_staging = _covered_by_staging(file_path, staging_paths)
        covered_production = _covered_by_production(file_path, snapshot)

        if not covered_staging and not covered_production:
            failures.append(
                f"'{file_path}' is a known runtime-read file but is covered by NEITHER "
                f"the staging filter ({STAGING_WORKFLOW.relative_to(REPO_ROOT)}) NOR the "
                f"production filter snapshot ({PRODUCTION_SNAPSHOT.relative_to(REPO_ROOT)}). "
                f"A change to it would silently fail to trigger a redeploy on at least one "
                f"environment (BLG-OPS-82/BLG-OPS-90 drift class)."
            )

    if failures:
        print("::error::Deploy path-filter drift detected:")
        for f in failures:
            print(f"  - {f}")
        print(
            "\nFix: add the missing path to staging-deploy.yml's paths: list, and/or update "
            "docs/ops/render_production_build_filter_snapshot.json after confirming (or "
            "correcting) the production Render dashboard's Build Filters."
        )
        return 1

    print(f"OK — all {len(KNOWN_RUNTIME_READ_FILES)} known runtime-read file(s) covered by at least one deploy path filter.")

    candidates = _static_scan_candidates()
    if candidates:
        print(
            "\n::warning::Best-effort static scan found non-.py file read(s) not yet in "
            "KNOWN_RUNTIME_READ_FILES (scripts/check_deploy_path_filter_drift.py) — review "
            "whether any of these are genuine runtime reads that should be added to the "
            "known inventory (and both filters checked). Not a failure: this scan has real "
            "false-positive/false-negative risk (e.g. it cannot resolve a path built via a "
            "variable rather than a literal at the call site) and is a prompt, not a verdict."
        )
        for c in candidates:
            print(f"  - {c}")

    print(
        "\nNote: production's filter is dashboard-only and not live-queryable from this "
        "script — the snapshot above reflects its last human-confirmed value "
        f"({snapshot.get('confirmed_utc', 'unknown date')}). A live dashboard change made "
        "without updating the snapshot would not be caught here; periodic re-confirmation "
        "(same cadence as docs/ops/render_build_deploy_path_filter_audit.md's own refresh "
        "passes) remains necessary."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
