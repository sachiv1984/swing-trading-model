#!/usr/bin/env python3
"""
CLI entry point for sending the Telegram changelog digest (ST-02, EPIC-02,
v7.8, BLG-FEAT-84). Invoked by the Post-Ship Closure engine (see
claude/system/post_ship_closure.md STEP 1.5) after the changelog entry for
the shipped release has been written.

Usage:
    python3 scripts/send_changelog_digest.py [--version "v7.8 — ..."]

If --version is omitted, sends the digest for the most recent (first)
version section in docs/product/changelog.md.

Exit code is always 0 — a failed send is logged but must never block
Post-Ship Closure (per the story's own AC). Check the printed result dict
for {"sent": true/false, ...}.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

# Load changelog_digest_service directly from its file path rather than via
# `from services.changelog_digest_service import ...` (OA-3, post-ship
# closure 2026-07-24__release-v7.8). A dotted import through the `services`
# package forces Python to execute backend/services/__init__.py first, which
# eagerly imports position_service and friends — those require a live
# DATABASE_URL at import time. changelog_digest_service (and the
# si05_digest_service helpers it loads the same way) has no such
# requirement, so loading it standalone lets this CLI run in a DB-less
# sandbox.
_MODULE_PATH = Path(__file__).parent.parent / "backend" / "services" / "changelog_digest_service.py"
_spec = importlib.util.spec_from_file_location("changelog_digest_service", _MODULE_PATH)
_module = importlib.util.module_from_spec(_spec)
sys.modules["changelog_digest_service"] = _module
_spec.loader.exec_module(_module)
send_changelog_digest = _module.send_changelog_digest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=None, help="Version heading prefix, e.g. 'v7.8'")
    args = parser.parse_args()

    result = send_changelog_digest(version=args.version)
    print(result)
    sys.exit(0)  # always 0 -- non-fatal by design
