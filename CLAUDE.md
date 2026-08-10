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
| `run ideas housekeeping [--dry-run]` | `claude/system/ideas_housekeeping_prompt.md` | Phase 1M — Archive terminal ideas register rows, review rejected-but-strong revival conditions |
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
- **Commit format is non-negotiable:** `[EPIC-xx][ST-xx] <description>` on all commits to `exec/**` branches. **When two stories are implemented in the same commit, all story IDs must appear in the message:** `[EPIC-xx][ST-xx][ST-yy] <description>`. Omitting a story ID prevents `governance_sync.yml` from closing that story's GitHub issue automatically.
- **PR title format is non-negotiable:** `[EPIC-xx] <description>` — required by `quality_gate.yml`. For hotfixes or out-of-sprint work not attached to a current EPIC, use `[GOVERNANCE] <description>` instead. The gate accepts `[EPIC-xx]`, `[ST-xx]`, or a title starting with `[GOVERNANCE]`. Any other format will fail `verify_governance`.
- **Bash commands that write files outside an active prompt's write scope are prohibited**, even as side-effects.
- **Document section headings must be descriptive and human-readable.** Task IDs, story IDs, and ticket references (e.g. `TASK-11`, `ST-xx`) must never appear in headings. They belong only in metadata blocks, changelogs, or inline cross-references.
- **Every new API endpoint must be added to `docs/reference/openapi.yaml` in the same commit as the contract.** Any new `## METHOD /path` heading added to a file in `docs/specs/api_contracts/` must have a corresponding entry in `docs/reference/openapi.yaml`. Omitting this fails the OpenAPI Drift Detection gate and blocks all PRs.
- **API contract endpoint headings must be `##` (not `###` or deeper).** The OpenAPI Drift Detection gate scans contract files for `## METHOD /path` at exactly the `##` level. Using `###` causes the endpoint to be invisible to the gate, reporting it as missing from the contract even if documented.
- **Every new API endpoint added to `backend/routers/` must have a corresponding `## METHOD /path` entry in a file in `docs/specs/api_contracts/` in the same sprint.** This complements the same-commit `docs/reference/openapi.yaml` requirement. Endpoints shipped without a contract document constitute spec debt (BLG-SPEC-type backlog items) and must be resolved before the next sprint planning seals.
- **Story commits must land on the branch matching their EPIC prefix.** An `[EPIC-05]` commit on an `exec/.../EPIC-04` branch is a process deviation and must be documented in the QA evidence log for both EPICs.
- **Any story introducing frontend-visible changes requires Playwright automated test coverage or human staging sign-off.** For each observable AC (visible rendering, element presence/absence, colour, interaction, timing): either (a) a Playwright test covering that AC must exist and pass in CI, or (b) a human staging run must be performed with the date recorded in the DoQ sign-off block. Code review alone is not a valid evidence method for observable UI behaviour. **Exception (FI-P3-02):** for ACs that are wording-only (text content, no visual rendering/colour/layout claim), code review of the static JSX/text may substitute for staging sign-off. Any AC involving visual rendering, colour, layout, or interaction timing requires Playwright coverage or a recorded staging run regardless of how simple the change appears. Any observable AC without Playwright coverage that is deferred to post-merge staging must have a backlog item filed (via /backlog-add) before the PR opens — "code review only" without a filed backlog item is a hard gate that blocks the PR.
- **Verify role ownership before acting on outstanding actions or clearing gates.** When asked to act as a role to action an OA, clear a gated initiative, or review a governance item, always check the Owner field of that item first. If the invoked role does not match the owner, flag the mismatch explicitly and ask for confirmation before taking any action. Do not proceed in the wrong role.
- **Every new backend route must be registered in the endpoint test suite in the same commit.** Any new `@router.get`, `@router.post`, `@router.put`, or `@router.delete` decorator added to a file in `backend/routers/` must have a corresponding entry in `backend/routers/test.py`. For parameterised routes (e.g. `/{ticker}`), use a representative safe value (e.g. `AAPL`). The hardcoded fallback count in `src/pages/SystemStatus.js` (`Tests {totalTests || 'N'} endpoints`) must also be updated to reflect the new total. **Additionally, update `SC-SS-01b` in `tests/e2e/system-status.spec.js` to match the new fallback value in the same commit.** Omitting any of these steps is a process deviation.
- **Retired (BLG-QA-73, resolved v6.6):** the `_DB_STUB_FUNCTIONS` list in `tests/conftest.py` no longer requires manual sync. It is now derived automatically via an AST scan of `backend/` for `from database import (...)` statements at conftest load time (vendored/virtualenv paths excluded from the scan). Adding a new `database` import to any backend module — not just `position_service.py` — requires no `conftest.py` edit.
- **A `**Last Updated:**` header field is a summary, not a history.** It records what the most recent edit changed — one entry, plainly stated. It must never become a chained `<date> (<reason>); prior — <date> (<reason>); prior — ...` log: every write to any document carrying this field retains at most the current entry plus 2 prior entries (3 total), dropping older ones and closing the chain with `prior history retained — see prior entries in version control`. This applies to **every** document using the field, regardless of Class — full history is always recoverable via `git log -p -- <file>`, so the header owes the reader a quick-glance summary, not an archive. Documents with real change-history needs use a dedicated `## Changelog` table or companion `claude/system/changelogs/*.md` file instead (per `shared_standards.md` §11) — that is a different field, not an exemption for this one. See `shared_standards.md` §16.14 for full mechanics. (Originated as a Class 4-only convention, BLG-GOV-283/ST-17, v8.2; broadened to universal scope 2026-08-07 after `backlog.md`'s chain reached 56 chained entries/~32,000 characters despite the narrower rule.)

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
3. Read `claude/cycles/<cycle_id>/sprint_backlog.md` to determine the sprint number (1, 2, 3…) for each ST item — sprint assignment is defined by the Sprint section headers in that file
4. Ensure release and sprint-specific labels exist (create if absent):
   ```
   gh label create "<release>" --color "1d76db" --description "<release> items" 2>/dev/null || true
   gh label create "sprint-1" --color "0075ca" --description "Sprint 1 items" 2>/dev/null || true
   gh label create "sprint-2" --color "0052cc" --description "Sprint 2 items" 2>/dev/null || true
   gh label create "sprint-3" --color "003a8c" --description "Sprint 3 items" 2>/dev/null || true
   ```
   where `<release>` is the `next_release` value from `.claude_current_state.json` (e.g. `v2.3`).
5. For each ST item not yet in GitHub Issues:
   ```
   gh issue create --title "[ST-xx] <title>" \
     --body "<acceptance criteria from sprint_backlog.md>" \
     --label "<release>" --label "sprint-N" --label "<EPIC-xx>"
   ```
   where `<release>` is from step 4 and `sprint-N` is the sprint number from step 3.
6. For items already in GitHub Issues: update labels/body if changed
7. Report: issues created, issues updated, issues already current

Do not close issues here — issue closure is handled automatically by `governance_sync.yml` on push.

---

## 5. Tool Call Expectations

- Governed routines (roadmap, release, sprint) typically require **20–60 tool calls**.
- Proceed through steps without asking for confirmation unless a **hard gate fires**.
- Hard gate = stop, output the halt report (per `shared_standards.md`), and wait for user.
- Non-gate questions or ambiguities: flag inline and continue where safe; park where not.

---

## 6. Governance File Edit Checklist (Always Active)

Whenever any governance prompt or the OPERATIONAL_GUIDE is modified — **including changes made as part of sprint story execution** — the following steps are **mandatory** in the same commit:

1. **Before bumping, read the file's own Change Log table's top row (or full existing body) to confirm its header/content is not already ahead of — or behind — what the edit assumes** (per `shared_standards.md` §9.1). Then **bump the version** in the file's own header (`**Version:**`).
2. **Update `OPERATIONAL_GUIDE.md` §14 governance table** — set the file's version to the new version.
3. **Update the corresponding phase section source prompt header** (§5–§10, §6B, §6B.8, §6M) in OPERATIONAL_GUIDE.md to match the new version — this is the standing rule from §14.
4. **Append an entry to `claude/system/prompt_change_log.md`** — one row per file changed, format: `| date | filename | vOLD→vNEW | summary | authority |`

Skipping any of these steps is a non-compliant state. Do not commit without all four complete.

---

## 8. Cross-EPIC Merge Conflict Resolution

When two or more EPIC PRs modify shared files (`execution_state.json`, `openapi.yaml`, `api_changelog.md`, `data_model.md`, etc.) and GitHub reports `CONFLICTING / DIRTY`:

1. **Merge the simpler EPIC first** (fewest shared-file changes) via local `git merge` into main, resolve any conflicts, push to `origin/main`.
2. **Checkout the remaining EPIC branch.** Run `git merge origin/main --no-commit --no-edit` to pull in the now-merged changes.
2a. **Identical-text-masks-differing-semantics check (mandatory, before resolving any conflict below).** For any shared *governance prompt or Class 6 document* touched by both sides (not just the files explicitly named in step 3), check whether both branches independently bumped the same `**Version:**` header field to the same literal version number for two *different* changes. `git merge` sees no conflict when the version-line text is byte-identical on both sides — the collision is silent, and one branch's change can end up applied under a version number that no longer uniquely identifies it. Before accepting either side's version number as-is: confirm the two branches' *change descriptions* (their own `Change Log` entries or `prompt_change_log.md` rows) are actually the same change, not two coincidentally-matching version bumps. If they are different changes: renumber the later-merging branch's bump to the next free version (and its `Change Log`/`prompt_change_log.md`/`OPERATIONAL_GUIDE.md` §14 rows) *before* committing the merge resolution — do not let two different changes ship under one version number. Record any renumbering performed in the conflict-resolution commit message. (Real precedent for the numeric half of this pattern, `sprint_planning_prompt.md` v3.13/v3.14 both independently cut, is in `prompt_change_log.md`'s `2026-08-03__release-v8.1` entries — this check exists to make that renumbering step deliberate rather than incidental.)
3. **Resolve each conflict** — always take the most-complete/most-current state:
   - `execution_state.json`: accept story completion data (status: done, commit_sha, acceptance_verified: true) from the branch; never revert a story from `done` → `blocked`. For summary arrays (`completed_items`, `blocked_items`, `delegated_items`): take the union of completed items from both sides; take the branch's (not main's) blocked/delegated lists as those reflect the more current state. **Sibling-vs-sibling clause (ST-24, BLG-GOV-289, v8.5):** the "take the branch's list" rule above assumes a two-party merge where one side is `main` (the stale side). When the conflict is instead between two EPIC branches directly (neither side is `main` — e.g. resolving a branch merge before either has reached `main`), "the branch's list" is ambiguous: both sides may have independently diverged from a common ancestor and both may have added genuinely new, non-overlapping `blocked_items`/`delegated_items` entries. Neither side's list alone is correct in that case — take the **union** of `blocked_items`/`delegated_items` across both sides, the same treatment already specified for `completed_items`. Confirmed via a dry-run test merge between two EPIC branches (`docs/ops/cross_epic_merge_runbook_dry_run_2026-08-08.md`) that the single-branch rule does not resolve this case.
   - `openapi.yaml`: union of all path additions; take the highest version number.
   - `api_changelog.md`: combine all version entries in descending order (newest first).
   - `data_model.md`: keep all migration blocks in ascending version order; take highest version number in the footer.
   - `qa_evidence_EPIC-*.md` (`add/add` conflict): take the completed DoQ sign-off blocks from the branch over any pending placeholders from main. Retain the full header metadata block (Owner, Class, Status) from whichever side has it. Keep all ST sections — combine rather than choose. Update any consolidation block rows from "Pending" → "Pass" where the branch has sign-off evidence.
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

---

## 9. Running the Backend Test Suite

Always invoke pytest via the project virtualenv, not the system Python: `backend/.venv/bin/python3 -m pytest`. `backend/requirements.txt` (fastapi, yfinance, pandas, etc.) is installed there; system `python3`/`pip3` is not guaranteed to have these, and running with system Python produces spurious collection errors and cascading test failures that look like real bugs but aren't. CI is unaffected — every workflow in `.github/workflows/` installs `requirements.txt` fresh into its own runner.