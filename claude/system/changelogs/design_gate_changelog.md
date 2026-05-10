**Owner:** Head of Specs Team
**Status:** Active

# Change Log — Design Gate Engine

This file contains the historical change log for `claude/system/design_gate_prompt.md`.
The prompt itself contains only the current version — full history is here.

---

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-03-07 | **Dry-run behaviour made explicit throughout.** §2 invocation rule: dry-run output scope defined (classification table + gap list only; no gate record, no state, no commit). §5 write scope: dry-run write scope stated as nothing. STEP -1.1: dry-run preflight note added. STEP 1: dry-run exit point added. STEP 7: explicit skip instruction for dry-run added. §7 completion condition: dry-run completion condition added. §8 governance invariants: dry-run invariant updated with exit point. **`design_gate_status` state lifecycle documented.** STEP -1.1: preflight now checks existing `design_gate_status` value and defines behaviour for each state (`not_started`, `Passed`, `Blocked`). STEP 6: state lifecycle table added (`not_started` → `Blocked` / `Passed`); note that `not_started` is set by Release Planning Engine at STEP 0. **State write scope tightened.** §5 write scope note: additive write only. STEP 6 instruction: additive write only; must not overwrite unrelated fields. §8 governance invariants: additive write invariant added. |
| 1.0 | 2026-03-04 | Initial version. |
