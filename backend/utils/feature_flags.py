"""
Feature flag evaluation utility.

Flags can be defined in two ways (checked in order):
  1. Environment variable: FEATURE_FLAGS=flag1:true,flag2:false
  2. Config file: feature_flags.json in the project root

Usage:
  from utils.feature_flags import is_flag_enabled
  if is_flag_enabled("arc3_lifecycle_display"):
      ...

§13 compliance: feature flags control feature visibility only — they never
substitute for human decision steps or bypass governance gates.

ST-16 (BLG-OPS-140, EPIC-06, v8.7): `feature_flags.json` does not exist in
this repo today (confirmed absent as of this note) but is a currently-flagged
gap in docs/ops/render_build_deploy_path_filter_audit.md -- if it is ever
added, add it to `.github/workflows/staging-deploy.yml`'s `paths:` list and
production's Render dashboard Build Filters in the same commit, or a deploy
may silently skip picking up changes to it. Read that doc before adding the
file.
"""

import os
import json
import logging

_log = logging.getLogger(__name__)

_CACHE: dict | None = None


def _load_flags() -> dict:
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    flags: dict = {}

    # 1. Environment variable
    raw = os.environ.get("FEATURE_FLAGS", "")
    if raw:
        for item in raw.split(","):
            item = item.strip()
            if ":" in item:
                name, val = item.split(":", 1)
                flags[name.strip()] = val.strip().lower() == "true"

    # 2. Config file (merges on top of env var, file wins on conflict)
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "feature_flags.json")
    config_path = os.path.normpath(config_path)
    if os.path.isfile(config_path):
        try:
            with open(config_path) as f:
                file_flags = json.load(f)
            if isinstance(file_flags, dict):
                flags.update({k: bool(v) for k, v in file_flags.items()})
        except Exception as e:
            _log.warning("feature_flags.json could not be parsed: %s", e)

    _CACHE = flags
    return flags


def is_flag_enabled(flag_name: str) -> bool:
    """Return True if the named feature flag is enabled, False otherwise."""
    return _load_flags().get(flag_name, False)


def log_flag_states() -> None:
    """Log all known flag states at INFO level (called at app startup)."""
    flags = _load_flags()
    if flags:
        for name, enabled in sorted(flags.items()):
            _log.info("Feature flags: %s=%s", name, enabled)
    else:
        _log.info("Feature flags: none configured")
