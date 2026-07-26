"""
Changelog Digest Service (ST-02, EPIC-02, v7.8, BLG-FEAT-84)

Sends a Telegram digest of a shipped release's "### Changes shipped"
changelog entries as part of Post-Ship Closure. Reuses the existing
Telegram notification infrastructure (POST+JSON with exponential-backoff
retry, shipped v2.4/v5.1 for the SI-05 weekly digest) rather than
introducing a new send path.

Failure to send (e.g. Telegram API error, missing credentials) must NEVER
raise out of send_changelog_digest — Post-Ship Closure must not be
blocked by a Telegram outage, per this story's own acceptance criteria.
"""

import logging
import os
import re
from pathlib import Path
from typing import Optional

from services.si05_digest_service import _send_telegram_request, MAX_MESSAGE_LENGTH

logger = logging.getLogger(__name__)

CHANGELOG_PATH = Path(__file__).resolve().parent.parent.parent / "docs" / "product" / "changelog.md"

_VERSION_HEADING_RE = re.compile(r"^## (v\S+ — .+)$", re.MULTILINE)
_CHANGES_SHIPPED_RE = re.compile(r"^### Changes shipped\s*\n(.*?)(?=\n##|\Z)", re.MULTILINE | re.DOTALL)
_TABLE_ROW_RE = re.compile(r"^\|\s*(EPIC-\d+)\s*\|\s*(.+?)\s*\|.*\|$", re.MULTILINE)

_MDV2_SPECIAL_CHARS = r"_*[]()~`>#+-=|{}.!"


def _escape_mdv2(text: str) -> str:
    """Escape MarkdownV2 special characters per Telegram's Bot API spec."""
    return "".join(f"\\{c}" if c in _MDV2_SPECIAL_CHARS else c for c in text)


def extract_changes_shipped(changelog_text: str, version: Optional[str] = None) -> Optional[dict]:
    """
    Parse changelog.md content and return the "### Changes shipped" table
    rows for the given version section, or the FIRST (most recent) version
    section if `version` is None.

    Returns {"heading": str, "rows": [(epic_id, description), ...]} or None
    if no matching version section (or no "### Changes shipped" table
    within it) is found.
    """
    headings = list(_VERSION_HEADING_RE.finditer(changelog_text))
    if not headings:
        return None

    target = None
    if version is None:
        target = headings[0]
    else:
        for h in headings:
            if h.group(1).startswith(version + " ") or h.group(1) == version:
                target = h
                break
    if target is None:
        return None

    start = target.end()
    idx = headings.index(target)
    end = headings[idx + 1].start() if idx + 1 < len(headings) else len(changelog_text)
    section_text = changelog_text[start:end]

    changes_match = _CHANGES_SHIPPED_RE.search(section_text)
    if not changes_match:
        return None

    rows = [(m.group(1), m.group(2)) for m in _TABLE_ROW_RE.finditer(changes_match.group(1))]
    # Drop the markdown separator row ("|------|-------------|...") if matched.
    rows = [(epic, desc) for epic, desc in rows if not set(epic) <= {"-"} and not set(desc) <= {"-"}]
    if not rows:
        return None

    return {"heading": target.group(1), "rows": rows}


def format_changelog_digest(heading: str, rows: list) -> str:
    """Format the changes-shipped rows as a Telegram MarkdownV2 message."""
    lines = [f"*Release shipped: {_escape_mdv2(heading)}*", ""]
    for epic_id, description in rows:
        lines.append(f"• *{_escape_mdv2(epic_id)}*: {_escape_mdv2(description)}")
    message = "\n".join(lines)
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[: MAX_MESSAGE_LENGTH - 20] + "\n\\.\\.\\. \\(truncated\\)"
    return message


def send_changelog_digest(version: Optional[str] = None, *, _sleep_fn=None) -> dict:
    """
    Read docs/product/changelog.md, extract the target version's "### Changes
    shipped" entries (most recent version if `version` is omitted), format
    as a Telegram MarkdownV2 message, and send.

    Never raises — always returns a result dict. Callers (Post-Ship Closure)
    must treat a failed send as non-fatal: log and continue.
    """
    try:
        if not CHANGELOG_PATH.exists():
            logger.warning("Changelog digest: %s not found", CHANGELOG_PATH)
            return {"sent": False, "error": f"changelog not found: {CHANGELOG_PATH}"}

        changelog_text = CHANGELOG_PATH.read_text()
        extracted = extract_changes_shipped(changelog_text, version=version)
        if extracted is None:
            logger.warning("Changelog digest: no '### Changes shipped' section found for version=%s", version)
            return {"sent": False, "error": "no matching changes-shipped section found"}

        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        if not telegram_token or not telegram_chat_id:
            logger.warning("Changelog digest: Telegram credentials not configured — skipping send")
            return {"sent": False, "error": "Telegram credentials not configured"}

        message = format_changelog_digest(extracted["heading"], extracted["rows"])
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "MarkdownV2",
        }
        _send_telegram_request(url, payload, sleep_fn=_sleep_fn)
        return {"sent": True, "heading": extracted["heading"], "entry_count": len(extracted["rows"])}
    except Exception as exc:
        # Post-Ship Closure must never be blocked by a digest-send failure.
        logger.error("Changelog digest send failed: %s", exc)
        return {"sent": False, "error": str(exc)}
