**Owner:** Head of Backend Engineering
**Class:** Assessment Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-28
**Cycle:** 2026-05-27__release-v4.2 — ST-10 (BLG-BE-22)

---

# Claude API Prompt Caching — Feasibility Assessment

## Executive Summary

**Recommendation: DEFER — revisit at or before SI-05 Phase 2 sprint planning.**

Prompt caching is technically applicable to both AI thesis generation use cases, but current call volume is too low for caching to yield measurable cost savings. The implementation adds operational complexity (cache TTL management, cache-aware audit logging) that is not justified at this stage. Reassess when call volume is better understood from `claude_audit_log` data (available post-v4.2).

---

## 1. Background

Anthropic's prompt caching feature allows a prefix of the prompt to be cached server-side for up to 5 minutes (TTL). Subsequent calls that use the same cached prefix incur a lower input token cost (`cache_read_input_tokens`) in exchange for a one-time cache creation cost (`cache_creation_input_tokens`).

Pricing (Claude Haiku 4.5):
- Standard input: $1.00 / 1M tokens
- Cache creation: $1.25 / 1M tokens (25% surcharge on first write)
- Cache read: $0.10 / 1M tokens (90% discount vs standard)

Break-even: a cached prefix must be read at least **1.25 times** within the 5-minute TTL window to recoup the creation surcharge.

---

## 2. Current Prompt Architecture

### 2.1 Thesis generation (`generate_setup_thesis`, `generate_full_plan`)

Prompt structure in `_THESIS_PROMPT_TEMPLATE` and `_FULL_PLAN_PROMPT`:

```
[SYSTEM-STYLE PREFIX — static, ~80 tokens]
"You are a systematic swing trader. Generate a concise setup thesis..."

[DYNAMIC BODY — variable, ~60–120 tokens]
"Ticker: {ticker}\nMarket: {market}\nSetup type: {setup_type}\n..."
```

The static prefix ("You are a systematic swing trader...") is the only cacheable segment. It is approximately 80 tokens.

### 2.2 Journal summary (`summarise_journal_notes`)

Prompt structure in `ai_service.py`:

```
[STATIC PREFIX — ~60 tokens]
"You are reviewing a trader's journal entries. Summarise the key themes..."

[DYNAMIC BODY — variable, 50–2000+ tokens]
"Journal entries:\n- {note1}\n- {note2}..."
```

Similar pattern — static prefix (~60 tokens) followed by fully dynamic journal entries.

---

## 3. Cache Hit Rate Estimate

For caching to activate, the **same static prefix** must be called at least twice within the 5-minute TTL window.

| Use case | Typical call frequency | Within 5-minute window | Cache viable? |
|----------|----------------------|----------------------|---------------|
| Thesis generation | Ad-hoc, 1–5 calls/day | Near-zero likelihood of 2+ calls within 5 min | No |
| Journal summary | Ad-hoc, 0–3 calls/day | Near-zero likelihood of 2+ calls within 5 min | No |

**Estimated cache hit rate: < 1% at current volume.**

The application does not have a batch or scheduled AI call pattern that would produce burst-frequency calls. Each AI call is user-initiated and isolated.

---

## 4. Cacheable Prompt Segments

For Anthropic prompt caching to apply, the `cache_control: {"type": "ephemeral"}` breakpoint must be inserted at a static prefix boundary:

| Prompt | Cacheable prefix | Prefix tokens | Notes |
|--------|-----------------|---------------|-------|
| `_THESIS_PROMPT_TEMPLATE` | System instruction + context framing | ~80 | Cacheable, but TTL mismatch means near-zero hit rate |
| `_FULL_PLAN_PROMPT` | System instruction | ~75 | Same issue |
| Journal summary prompt | System instruction | ~65 | Same issue |

Minimum eligible prefix for caching is 1,024 tokens (Anthropic requirement as of 2026). The static prefix in all current prompts is well below this threshold (~65–80 tokens). This means **prompt caching is currently ineligible** for all three AI features — the cacheable prefix is too short to meet the minimum requirement.

---

## 5. Implementation Complexity

If caching becomes viable in future (higher volume, longer prompts), implementation would require:

1. Insert `cache_control: {"type": "ephemeral"}` at the end of the static system prefix in each prompt template.
2. Modify `_call_claude()` to pass the `system` parameter as a list of blocks rather than a single string.
3. Update `_log_audit()` to capture `usage.cache_creation_input_tokens` and `usage.cache_read_input_tokens` alongside existing usage fields.
4. Add `cache_creation_input_tokens` and `cache_read_input_tokens` columns to `claude_audit_log`.
5. Update cost calculation to use tiered rates (creation vs. read vs. standard).

Estimated effort: 1–2 days including testing and audit log schema migration.

---

## 6. Recommendation

**DEFER — not applicable at current call volume and prompt length.**

Two gates block immediate implementation:

1. **Minimum prefix length unmet:** All current prompts have static prefixes of ~65–80 tokens, below Anthropic's 1,024-token minimum for prompt caching eligibility.
2. **Call frequency insufficient:** Ad-hoc user-initiated calls will rarely repeat within the 5-minute TTL window, yielding an estimated cache hit rate < 1%.

**Reassessment trigger:** When `claude_audit_log` data (available post-v4.2) shows ≥ 10 calls per day AND a use case emerges with a static prompt prefix ≥ 1,024 tokens, re-open BLG-BE-22 for implementation scoping.

---

## 7. References

- Anthropic prompt caching docs: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- Current prompt implementations: `backend/services/gemini_service.py`, `backend/services/ai_service.py`
- Audit log: `GET /ai/claude-audit-log` (available post-v4.2 ST-07)
- Cost rates: `docs/ops/gemini_cost_tracking.md`
