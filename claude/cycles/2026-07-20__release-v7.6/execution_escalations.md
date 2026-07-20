Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-20

# Execution Escalations — 2026-07-20__release-v7.6

## ESC-EXEC-20260720-01

- **Raised at:** 2026-07-20T21:00:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-07-20__release-v7.6
- **Step:** STEP 3 (Execution Loop) — EPIC-07 / ST-07
- **ST/EPIC item:** ST-07 (EPIC-07, BLG-FEAT-77) — Add consolidated Gemini + Claude monthly cost summary
- **Trigger type:** Quality
- **Blocking statement:** ST-07's approved UX spec (`docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md`, Product Owner-approved 2026-07-20) and its AC ("combined total matches the sum of the two existing per-provider sources") both premise the feature on Gemini and Claude being two genuinely separate AI providers with independently-metered costs, sourced from `gemini_audit_log` and a Claude equivalent respectively. Tracing the actual data model during implementation found this premise is factually incorrect: `backend/services/gemini_service.py` — despite its filename — calls only the Anthropic Claude API (`_call_claude()`, `MODEL_VERSION = "claude-haiku-4-5"`, `import anthropic`). A repo-wide search for any genuine Gemini usage (`GEMINI_API_KEY`, `google.generativeai`, `google-generativeai` in `requirements.txt`, any `genai` import) found zero results — there is no Gemini API integration anywhere in this codebase. Every thesis-generation call to Claude writes to **both** `gemini_audit_log` (via `create_gemini_audit_entry`) **and** `claude_audit_log` (via `create_claude_audit_entry`) in the same `_log_audit()` function (`gemini_service.py` lines ~113–125) — these are two differently-named tables logging the *same* Claude spend event, not two providers' independent spend. This is independently confirmed by `docs/ops/gemini_cost_tracking.md`'s own H1 heading, which reads "Claude API Cost Tracking" (not Gemini), and by `docs/ops/claude_cost_review_2026-05.md §1`, which states `gemini_audit_log` "is the authoritative source for pre-v4.2 Claude API calls." Implementing ST-07 literally as specified — a "Gemini" row and a "Claude" row summed into a "Combined total" — would double-count one real cost stream as if it were two, producing a materially misleading AI-spend figure in production. This is a correctness/quality defect the engine cannot resolve by guessing at the right fix, since two different corrections are both plausible and have different product implications (see Unblock criteria).
- **Owning authority:** FinOps & Resource Architect (ST-07 story owner); Product Owner (approved the now-invalidated UX spec premise)
- **Unblock criteria:** A decision on one of the following (or another option the owning authority proposes), recorded either as a comment/decision record or as a re-issued UX spec addendum:
  - **(a) Single-provider reframe:** Since there is genuinely one AI provider (Claude) and one real cost stream, rename the section/AC to a single "Claude API Usage & Costs" figure (no "Gemini" row, no "combined total" of two sources — just the one real total, sourced from whichever table is designated authoritative going forward). Cheapest, most honest option; requires a UX spec addendum and an AC wording correction, but ships this sprint.
  - **(b) Defer pending provider-naming cleanup:** Treat the `gemini_audit_log`/`gemini_service.py` naming as its own tracked debt (rename to reflect Claude, decide whether the dual-table write is still needed) before shipping any user-facing "cost by provider" view, since shipping now under any framing risks needing rework once the naming is fixed. Defer ST-07 to a future cycle.
  - **(c) Ship as originally specified anyway:** Explicitly accept that the two rows will show the same underlying spend under different labels (Product Owner call only — this is knowingly shipping a misleading figure, which is why this is filed as a Quality escalation rather than assumed).
- **SLA due-by:** 2026-07-20T21:00:00Z + before execution (Quality trigger type — per `shared_standards.md §4`, before this item's execution proceeds; may not be marked Accepted Risk)
- **Blocks execution:** No — blocks ST-07/EPIC-07 only; other EPICs in this sprint are unaffected and continue independently (per `execution_prompt.md` §3.1.D: escalate, park, continue other items)
- **Disposition:** Open
- **Resolution summary:** _(complete when closing; include evidence links)_
