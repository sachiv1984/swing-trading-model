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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.changelog_digest_service import send_changelog_digest  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=None, help="Version heading prefix, e.g. 'v7.8'")
    args = parser.parse_args()

    result = send_changelog_digest(version=args.version)
    print(result)
    sys.exit(0)  # always 0 -- non-fatal by design
