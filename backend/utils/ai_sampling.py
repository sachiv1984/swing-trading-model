"""
Fail-safe wrapper around the AI-output sampling hook (ST-03, BLG-BE-151,
EPIC-01, v9.11).

`services.ai_output_sampling_service.maybe_sample_output()` already swallows
its own failures, but every AI endpoint imported it inside the same `try`
block that returns the endpoint's fallback message. A failure at import
time (the PR #1921 bare-import defect, v9.4-v9.10) therefore replaced a
successfully generated AI response with the generic "unavailable" message,
and nothing was logged.

`sample_ai_output()` moves the import inside its own guard. Any failure,
including at import, is logged with `exc_info` and never reaches the
caller, so the endpoint's response is the same whether sampling works or
not. This module imports only the standard library, so importing it
cannot fail the way the sampling service's own import did.
"""
import logging

logger = logging.getLogger(__name__)


def sample_ai_output(feature: str, output_text: str, model_version: str | None = None) -> bool:
    """Offer one generated output to the sampling hook. Returns the hook's
    own result, or False if the hook failed. Never raises."""
    try:
        from services.ai_output_sampling_service import maybe_sample_output
        return bool(maybe_sample_output(feature, output_text, model_version))
    except Exception:
        logger.warning("AI output sampling failed for %s; response unaffected", feature, exc_info=True)
        return False
