"""
Pinned Claude model IDs — the one place backend code names a model
(ST-09, BLG-BE-142, EPIC-01, v9.11).

Every AI call site imports its model from here. A floating alias such as
`claude-haiku-4-5` can move to a newer snapshot without a code change, so
the debrief and trade-plan generation features could change model silently.
Each constant below is a complete, pinned model ID:

- Claude Haiku 4.5: `claude-haiku-4-5` is an alias; the pinned snapshot ID
  is `claude-haiku-4-5-20251001`.
- Claude Sonnet 4.6: `claude-sonnet-4-6` is itself the complete ID. Models
  from the 4.6 generation on have no dated snapshot form.

tests/test_ai_model_ids_pinned.py fails if a `claude-` model literal appears
anywhere else in backend/, or if a constant here is a known floating alias.
Changing a model is a deliberate edit to this file.
"""

# Post-trade debrief focus area, AI journal summary, trade-plan generation
# (generate-plan, generate-thesis).
CLAUDE_HAIKU_4_5 = "claude-haiku-4-5-20251001"

# Daily briefing and chat.
CLAUDE_SONNET_4_6 = "claude-sonnet-4-6"

# Model IDs that are complete as written, with no dated snapshot form.
DATELESS_COMPLETE_IDS = frozenset({CLAUDE_SONNET_4_6})

# Floating aliases that must never be used as a model ID in production code.
FLOATING_ALIASES = frozenset({"claude-haiku-4-5"})

ALL_MODEL_IDS = frozenset({CLAUDE_HAIKU_4_5, CLAUDE_SONNET_4_6})
