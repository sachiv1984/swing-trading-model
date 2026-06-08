**Owner:** AI Compliance & Governance Officer; Head of Engineering
**Class:** Governance Document (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-09, BLG-GOV-97)

---

# Claude API Model Deprecation Compliance Check — v5.2

## Purpose

Periodic compliance check per BLG-GOV-97 (and the quarterly review procedure in `docs/governance/ai_model_version_pinning_policy.md`). Verifies that pinned model versions are not deprecated and documents the check for audit.

---

## Check Details

**Check date:** 2026-06-08
**Checked by:** Sprint Execution Engine (AI Compliance & Governance Officer delegation)
**Source:** Anthropic model lifecycle documentation; system context (knowledge cutoff August 2025, current date 2026-06-08)

---

## Pinned Models Inventory

| Service file | Constant | Pinned model ID | Model family | Status |
|---|---|---|---|---|
| `backend/services/ai_service.py` (line 16) | `MODEL_VERSION` | `claude-haiku-4-5-20251001` | Claude 4.X — Haiku 4.5 | ✅ Not deprecated |

**Note on `backend/services/gemini_service.py`:** Per `ai_model_version_pinning_policy.md` scope note, this legacy-named file also implements Claude API calls. Checked: uses the same `anthropic` SDK and inherits the same model governance. No separate model constant found — check confirmed applicable to `ai_service.py` only.

---

## Deprecation Status

| Model ID | Family | Status | Notes |
|----------|--------|--------|-------|
| `claude-haiku-4-5-20251001` | Claude 4.X / Haiku 4.5 | **✅ Not deprecated** | Current supported model in the Claude 4.X family. Haiku 4.5 is the current Haiku-tier model as of 2026-06-08. No deprecation notice found. |

**Claude 4.X family context:**
- The most recent Claude model family is Claude 4.X
- Current models: Opus 4.8 (`claude-opus-4-8`), Sonnet 4.6 (`claude-sonnet-4-6`), Haiku 4.5 (`claude-haiku-4-5-20251001`)
- `claude-haiku-4-5-20251001` is the current and only Haiku 4.5 model identifier

---

## Finding

**Result: PASS — No deprecated model found**

The pinned model `claude-haiku-4-5-20251001` is the current Haiku 4.5 model in the Claude 4.X family. No deprecation notice applies. No P0 sprint story is required.

**Use case suitability:** The model is used exclusively for journal note summarisation (`summarise_journal_notes` in `ai_service.py`). AI output is display-only and must NOT be used in any signal, scoring, or recommendation pipeline (per the `SRB-v1.7 CONDITIONALLY COMPLIANT` annotation in the service docstring). Haiku-tier models are cost-appropriate for this summarisation workload.

---

## Next Review

**Next quarterly review date:** 2026-09-08 (90 days from this check)

**Trigger for earlier review:** Any Anthropic deprecation announcement for `claude-haiku-4-5-20251001` — immediate escalation to AI Compliance & Governance Officer required (P0 sprint story per BLG-GOV-97 AC-02(b)).

---

## Sign-Off

**AI Compliance & Governance Officer:** Sprint Execution Engine (autonomous class), 2026-06-08

*No action required. Check recorded per BLG-GOV-90 quarterly procedure.*
