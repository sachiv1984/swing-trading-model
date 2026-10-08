"""
ST-09 (BLG-BE-142, EPIC-01, v9.11) — every Claude model ID is pinned in one
backend module, backend/ai_models.py.

1. No `claude-<family>` model literal appears in backend/ outside that
   module (string literals, comments and docstrings all count).
2. No constant in the module is a floating alias, and each is either a
   dated snapshot ID or listed as complete without a date.
3. Every AI call site's model constant comes from the module.
"""
import re
import sys
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parent.parent / "backend"
MODULE = BACKEND / "ai_models.py"
EXCLUDED_DIRS = {".venv", "venv", "site-packages", "__pycache__", "node_modules"}

# A model ID literal: claude-<family>... (not e.g. "claude-audit-log").
MODEL_LITERAL_RE = re.compile(r"claude-(?:haiku|sonnet|opus|fable|mythos|instant|\d)[\w.-]*")
DATED_RE = re.compile(r"-\d{8}$")


def _model_literals_outside_module(root: Path):
    hits = []
    for path in sorted(root.rglob("*.py")):
        if EXCLUDED_DIRS.intersection(path.relative_to(root).parts) or path.name == MODULE.name:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in MODEL_LITERAL_RE.finditer(line):
                hits.append(f"{path.relative_to(root.parent)}:{lineno}: {m.group(0)}")
    return hits


def test_no_model_literal_outside_the_pinned_module():
    hits = _model_literals_outside_module(BACKEND)
    assert not hits, "Claude model IDs must come from backend/ai_models.py:\n" + "\n".join(hits)


def test_reintroduced_literal_is_detected(tmp_path):
    root = tmp_path / "backend"
    (root / "services").mkdir(parents=True)
    (root / "services" / "x.py").write_text('MODEL = "claude-haiku-4-5"\n')
    assert _model_literals_outside_module(root) == ["backend/services/x.py:1: claude-haiku-4-5"]


def test_audit_log_endpoint_name_is_not_a_model_literal():
    assert not MODEL_LITERAL_RE.search("GET /ai/claude-audit-log")


def _module():
    sys.path.insert(0, str(BACKEND))
    import ai_models
    return ai_models


def test_no_floating_alias_and_every_id_pinned():
    m = _module()
    for model_id in m.ALL_MODEL_IDS:
        assert model_id not in m.FLOATING_ALIASES, f"{model_id} is a floating alias"
        assert DATED_RE.search(model_id) or model_id in m.DATELESS_COMPLETE_IDS, (
            f"{model_id} is neither a dated snapshot nor listed as complete without a date"
        )


def test_every_constant_is_registered():
    m = _module()
    constants = {v for k, v in vars(m).items() if k.startswith("CLAUDE_")}
    assert constants == set(m.ALL_MODEL_IDS)


@pytest.mark.parametrize("module_name,attr", [
    ("services.ai_service", "MODEL_VERSION"),
    ("services.ai_service", "MODEL_BRIEFING"),
    ("services.debrief_service", "MODEL_VERSION"),
    ("services.gemini_service", "MODEL_VERSION"),
])
def test_call_sites_use_pinned_ids(module_name, attr):
    import importlib
    value = getattr(importlib.import_module(module_name), attr)
    assert value in _module().ALL_MODEL_IDS
