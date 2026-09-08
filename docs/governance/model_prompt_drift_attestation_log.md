**Owner:** Head of Specs Team
**Class:** Governance Register (Class 4)
**Status:** Active
**Last Updated:** 2026-09-08 (ST-17, EPIC-04, v9.2, BLG-GOV-242 — log created, first entry filed)

---

# Quarterly Model / Prompt-Drift Compliance Attestation Log

## 1. Purpose

This log records a quarterly attestation that the governance prompt stack (`claude/system/*_prompt.md`, `OPERATIONAL_GUIDE.md`) and the assistant model powering it (per `CLAUDE.md`'s Environment section) have not silently drifted apart — i.e. that a model upgrade has not changed how a governed routine behaves in a way the prompts do not account for, and that the prompt stack itself has not accumulated undocumented behavioural drift relative to what `OPERATIONAL_GUIDE.md` §14 declares as current.

This is distinct from:
- `governance-drift` skill (checks §14 table vs. individual prompt headers — structural version sync, not behavioural drift)
- Lifecycle audits (`claude/audit.py`, every 3 cycles — checks artefact compliance, not model/prompt behavioural consistency)

## 2. Attestation Method

Each quarter (calendar quarter, first scheduled rebalance or sprint execution session on or after the quarter boundary):

1. Record the model ID currently in use (per session environment banner).
2. Compare against the model ID recorded at the prior attestation. If changed: note the change and confirm — by spot-checking 2–3 recently completed governed routine outputs (e.g. a `run sprint` execution_state.json write, a `run roadmap` STEP 8 decision) — that output structure, field names, and hard-gate enforcement remain consistent with what the prompts specify.
3. Confirm `governance-drift` skill's Step 1b self-consistency check has been run at least once since the prior attestation (cross-reference `prompt_change_log.md` for evidence of a drift-check pass, or run it now if no evidence exists).
4. Record: any drift found, corrective action taken, or "No drift found."

## 3. Attestation Register

| Date | Quarter | Model ID | Model Changed Since Prior? | Drift Found | Corrective Action | Attested By |
|------|---------|----------|----------------------------|-------------|--------------------|-------------|
| 2026-09-08 | Q3 2026 | claude-sonnet-5 | First entry — no prior attestation to compare against | No drift found. `governance-drift` skill checks have run repeatedly within this quarter per `prompt_change_log.md`'s self-drift-correction entries (e.g. AUD-2026-08-21 series); no undocumented behavioural divergence observed in recently completed governed routines (`run sprint` EPIC-01/02/03 this cycle, `run roadmap` outcomes recorded in `.claude_current_state.json`) — hard-gate halts, commit format enforcement, and execution_state.json schema all matched prompt specification. | N/A | Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-17, 2026-09-08) |

## 4. Next Attestation Due

Q4 2026 (on or after 2026-10-01), at the first scheduled rebalance or sprint execution session falling in that window.
