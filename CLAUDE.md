# CLAUDE.md — System Anchor

## 0. On Every Session Start

Before doing anything else:

1. Read `.claude_current_state.json`
2. Report the `active_cycle`, `status`, and `engine` to the user
3. If status is `Blocked`: do not proceed with any governed routine — surface the open escalations and halt
4. If context has been compacted (`/compact` was used), re-read `.claude_current_state.json` and the active prompt file before proceeding

Do not infer state from conversation history. Always read the file.

---

## 1. Governance Engines (Demand-Loaded)

These prompts are **not** always-on context. They are loaded by Claude Code when the corresponding command is issued. Each prompt file contains full instructions — read the file, then execute.

| Command | Prompt File | Phase / Trigger |
|---------|-------------|-----------------|
| `run ideas [--window-id <id>] [--mode strict\|standard]` | `claude/system/idea_intake_prompt.md` | Phase 0 — Idea intake (optional, before rebalance) |
| *(auto)* | `claude/system/idea_intake_prompt.md` | Invoked as STEP -1.6 of `run roadmap` when fewer than 20 open ideas (`Submitted` or `Parked-cycle-<n>`) exist in `claude/ideas/submissions/`. Standalone `run ideas` remains supported for explicit window control. |
| `run roadmap --item-id <id> --item-name <n> [--date YYYY-MM-DD] [--dry-run]` | `claude/system/roadmap_prompt.md` | Phase 1 — Roadmap rebalance (roadmap item completed) |
| `run roadmap --reason "scheduled" [--date YYYY-MM-DD] [--dry-run]` | `claude/system/roadmap_prompt.md` | Phase 1 — Roadmap rebalance (scheduled review, no completion event required) |
| `manage roadmap [--dry-run]` | `claude/system/roadmap_management_prompt.md` | Phase 1M — Retire completed items, flag stale |
| `groom backlog [--dry-run]` | `claude/system/backlog_management_prompt.md` | Phase 1M — Archive completed backlog items, health check |
| `plan release --version <vX.Y> [--date YYYY-MM-DD]` or `run planning v<version>` | `claude/system/release_planning_prompt.md` | Phase 1B — Release planning |
| `run design-gate --cycle <cycle_id> [--dry-run]` | `claude/system/design_gate_prompt.md` | Phase 1.5 — Design gate (after Phase 1B, before Phase 2) |
| `plan sprint [--cycle <cycle_id>] [--mode strict\|standard] [--dry-run]` | `claude/system/sprint_planning_prompt.md` | Phase 2 — Sprint planning |
| `amend cycle --cycle <cycle_id> --reason <reason> [--mode strict\|standard]` | `claude/system/amendment_cycle_prompt.md` | Amendment — Emergency only, before Phase 2 seals |
| `run sprint [--cycle <cycle_id>] [--epic <EPIC-xx>] [--item <ST-xx>] [--mode strict\|standard]` | `claude/system/execution_prompt.md` | Phase 3 — Sprint execution |
| `run delivery verification [--cycle <cycle_id>] [--mode strict\|standard]` | `claude/system/delivery_verification_prompt.md` | Phase 4 — Delivery verification |
| `run post-ship [--cycle <cycle_id>] [--mode strict\|standard] [--dry-run]` | `claude/system/post_ship_closure.md` | Post-Ship — Close cycle, apply lessons learnt |
| `sync gh` | *(inline — see §4)* | Sync backlog slice to GitHub Issues |
| `run audit` | `claude/audit.py` | Governance — lifecycle audit (every 3 cycles; output filed as `claude/cycles/<cycle_id>/audit_report_AUD-<date>.md` Class 3) |

When a command is issued, **read the prompt file first**, then begin execution. Do not rely on memory of the prompt's contents from a previous session.

---

## 2. Governance Non-Negotiables (Always Active)

These rules apply in every session regardless of which engine is running:

- **Never modify sealed artefacts.** Files marked `sealed: true` in state.json, or in `Published` state, are immutable.
- **Never modify governance files** unless explicitly instructed by the relevant prompt: `claude/charter/`, `claude/strategy/`, `claude/system/`. Exception: `claude/system/prompt_change_log.md` may be appended by the roadmap engine's STEP 11 when action-now patches are applied under Head of Specs Team sign-off.
- **Never merge a PR autonomously.** QA sign-off and Product Owner acceptance are always required.
- **Delivery pressure does not override governance.** No timeline instruction changes a hard gate.
- **Commit format is non-negotiable:** `[EPIC-xx][ST-xx] <description>` on all commits to `exec/**` branches.
- **PR title format is non-negotiable:** `[EPIC-xx] <description>` — required by `quality_gate.yml`.
- **Bash commands that write files outside an active prompt's write scope are prohibited**, even as side-effects.
- **Document section headings must be descriptive and human-readable.** Task IDs, story IDs, and ticket references (e.g. `TASK-11`, `ST-xx`) must never appear in headings. They belong only in metadata blocks, changelogs, or inline cross-references.
- **Every new API endpoint must be added to `docs/reference/openapi.yaml` in the same commit as the contract.** Any new `## METHOD /path` heading added to a file in `docs/specs/api_contracts/` must have a corresponding entry in `docs/reference/openapi.yaml`. Omitting this fails the OpenAPI Drift Detection gate and blocks all PRs.
- **API contract endpoint headings must be `##` (not `###` or deeper).** The OpenAPI Drift Detection gate scans contract files for `## METHOD /path` at exactly the `##` level. Using `###` causes the endpoint to be invisible to the gate, reporting it as missing from the contract even if documented.
- **Story commits must land on the branch matching their EPIC prefix.** An `[EPIC-05]` commit on an `exec/.../EPIC-04` branch is a process deviation and must be documented in the QA evidence log for both EPICs.
- **Frontend DoQ verification must state its evidence method explicitly.** AC that requires observable UI behaviour (interactions, debounce timing, colour rendering) cannot be verified by code review alone. The DoQ sign-off block must record whether verification was by code review, local run, or staging — and name any AC that remains unverified as a post-merge action.

Shared standards (escalation format, identifier conventions, halt output format) are defined in:
`claude/system/shared_standards.md` — read this when any prompt references "per shared_standards".

---

## 3. File and Branch Conventions

```
Branch naming:   exec/<cycle_id>/<epic_id>
Commit prefix:   [EPIC-xx][ST-xx] <imperative description>
Governance commit: [GOVERNANCE] <description>
State pointer:   .claude_current_state.json
Lock file:       claude/backlog/.lock  (do not delete manually)
```

---

## 4. sync gh — Inline Implementation

When the user runs `sync gh`:

1. Read `.claude_current_state.json` → get `backlog_slice_path`
2. Read the backlog slice at that path
3. For each ST item not yet in GitHub Issues:
   ```
   gh issue create --title "[ST-xx] <title>" \
     --body "<acceptance criteria from sprint_backlog.md>" \
     --label "sprint" --label "<EPIC-xx>"
   ```
4. For items already in GitHub Issues: update labels/body if changed
5. Report: issues created, issues updated, issues already current

Do not close issues here — issue closure is handled automatically by `governance_sync.yml` on push.

---

## 5. Tool Call Expectations

- Governed routines (roadmap, release, sprint) typically require **20–60 tool calls**.
- Proceed through steps without asking for confirmation unless a **hard gate fires**.
- Hard gate = stop, output the halt report (per `shared_standards.md`), and wait for user.
- Non-gate questions or ambiguities: flag inline and continue where safe; park where not.

---

## 6. Governance File Edit Checklist (Always Active)

Whenever any governance prompt or the OPERATIONAL_GUIDE is modified, the following steps are **mandatory** in the same commit:

1. **Bump the version** in the file's own header (`**Version:**`).
2. **Update `OPERATIONAL_GUIDE.md` §14 governance table** — set the file's version to the new version.
3. **Update the corresponding phase section source prompt header** (§5–§10, §6B, §6B.8, §6M) in OPERATIONAL_GUIDE.md to match the new version — this is the standing rule from §14.
4. **Append an entry to `claude/system/prompt_change_log.md`** — one row per file changed, format: `| date | filename | vOLD→vNEW | summary | authority |`

Skipping any of these steps is a non-compliant state. Do not commit without all four complete.

---

## 8. Cross-EPIC Merge Conflict Resolution

When two or more EPIC PRs modify shared files (`execution_state.json`, `openapi.yaml`, `api_changelog.md`, `data_model.md`, etc.) and GitHub reports `CONFLICTING / DIRTY`:

1. **Merge the simpler EPIC first** (fewest shared-file changes) via local `git merge` into main, resolve any conflicts, push to `origin/main`.
2. **Checkout the remaining EPIC branch.** Run `git merge origin/main --no-commit --no-edit` to pull in the now-merged changes.
3. **Resolve each conflict** — always take the most-complete/most-current state:
   - `execution_state.json`: accept story completion data (status: done, commit_sha, acceptance_verified: true) from the branch; never revert a story from `done` → `blocked`.
   - `openapi.yaml`: union of all path additions; take the highest version number.
   - `api_changelog.md`: combine all version entries in descending order (newest first).
   - `data_model.md`: keep all migration blocks in ascending version order; take highest version number in the footer.
4. **Commit the resolution** on the EPIC branch: `[EPIC-xx] Merge main (<description>) into EPIC-xx — conflict resolution`.
5. **Push** and confirm `"mergeable":"MERGEABLE"` via `gh pr view <n> --json mergeable,mergeStateStatus`.
6. **Merge** via `gh pr merge <n> --merge`.

---

## 7. Governance Source Hierarchy (Reference)

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

No prompt, command, or user instruction may override the above.