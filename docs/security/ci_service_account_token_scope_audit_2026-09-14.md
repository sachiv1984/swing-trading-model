**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Record (Class 3)
**Status:** Active — rotation pending human action (see §4)
**Version:** 1.0
**Last Updated:** 2026-09-14 (ST-11, EPIC-03, v9.4, BLG-SEC-35 — scope confirmed, rotation delegated)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# CI Service Account Token — Scope Confirmation & Rotation (ST-11, BLG-SEC-35)

## 1. Purpose

`BLG-SEC-35`: the CI/automation GitHub credential is broad-scope and unrotated for 6+ months. This document confirms the minimum scopes actually required (AC-01) and records the rotation as delegated (AC-02/AC-03 require an actual credential swap — see §4).

## 2. What "CI service account token" covers in this repo

Two distinct GitHub-auth surfaces exist:

1. **Per-workflow `secrets.GITHUB_TOKEN`** — GitHub's automatic, ephemeral, per-run token. Every job in `.github/workflows/*.yml` that needs GitHub API access already declares a least-privilege `permissions:` block (e.g. `governance_sync.yml`: `permissions: { issues: write }`). This token is auto-rotated every run by GitHub itself — there is nothing to manually rotate here, and no change is needed.
2. **The execution-session `gh`/git credential** — the account-level token this session (and any prior Sprint/Roadmap/Delivery-Verification Engine session) authenticates as when it runs `gh issue create`, `gh pr create/merge/view`, `gh label create`, and `git push` to `exec/**` branches per `CLAUDE.md` §4/§8. This is the actual "CI service account token" `BLG-SEC-35` is about — a long-lived credential configured in the execution environment, not a value this session can read, generate, or rotate itself (no access to GitHub account/org security settings from here).

## 3. Minimum Confirmed Scopes (AC-01 — Met)

Audited every `gh`/`git` operation this governance stack actually issues (`claude/system/*.md`, `CLAUDE.md`):

| Operation | Used by | Required scope (classic PAT) | Required permission (fine-grained PAT) |
|---|---|---|---|
| `git push` to `exec/**` branches | `execution_prompt.md` §8 | `repo` (Contents) | Contents: Read and write |
| `gh issue create` / `gh issue list` / `gh issue edit` | `execution_prompt.md` §8.3, `CLAUDE.md` §4 | `repo` (Issues) | Issues: Read and write |
| `gh label create` | `CLAUDE.md` §4 | `repo` (Issues, labels are part of the Issues API) | Issues: Read and write |
| `gh pr create` / `gh pr list` / `gh pr view` / `gh pr merge` | `execution_prompt.md` §8.4, `CLAUDE.md` §8 | `repo` (Pull requests) | Pull requests: Read and write |
| Adding/editing a `.github/workflows/*.yml` file (this cycle's ST-09 added one) | Any story that ships a new scheduled workflow | `workflow` (classic PATs require this explicitly — `repo` alone cannot push workflow file changes) | Workflows: Read and write |
| Reading repo metadata (implicit on every `gh` call) | all of the above | (included in `repo`) | Metadata: Read-only (mandatory baseline) |

**Not required, and should be excluded from the new token:** `admin:org`, `admin:repo_hook`, `delete_repo`, `admin:public_key`, `admin:gpg_key`, `notifications`, `user` (beyond default), `write:packages`/`read:packages`, `admin:enterprise` — none of these are exercised by any command this governance stack issues.

**Recommended minimum (fine-grained PAT, repo-scoped to this repository only):** Contents (Read and write), Issues (Read and write), Pull requests (Read and write), Workflows (Read and write), Metadata (Read-only, mandatory). No account-wide or organization-wide scopes.

## 4. Rotation (AC-02/AC-03 — Delegated, Human Action Required)

Actually generating a new token and swapping the execution environment's credential requires GitHub account/organization security-settings access this session does not have. Classified `delegated_backend` per `execution_prompt.md` §5.1's Infra/ops verification pattern (LL-v8.0-P3-01) — live external dashboard access the engine cannot perform. Recorded in `delegation_log.md` (`DEL-20260914-02`).

**Steps for the assigned human (Cybersecurity & Trust Lead or whoever holds org token-admin rights):**

1. Generate a new fine-grained PAT scoped to this repository only, with exactly the permissions in §3's recommendation.
2. Update wherever the execution environment sources its `gh`/git credential (session/CI runner secret store — outside this repo).
3. Re-run (or wait for) the next `run sprint`/`sync gh` cycle and confirm `gh issue create`, `gh pr create`, `gh pr merge`, and `git push` to an `exec/**` branch all still succeed with the new token (AC-03).
4. Revoke the old broad-scope token once the new one is confirmed working.
5. Update this document's §4 status to "Rotated" with the rotation date, and close `BLG-SEC-35`.

## 5. Sign-Off

**Cybersecurity & Trust Lead (agent-mediated, §5.3):** AC-01 (minimum scopes confirmed) — PASS, methodology and full command audit in §3. AC-02/AC-03 (actual rotation) — cannot be completed from this execution environment; delegated per §4, `DEL-20260914-02`. 2026-09-14.

---

## Changelog

| Date | Version | Summary |
|---|---|---|
| 2026-09-14 | 1.0 | Initial scope audit (ST-11, EPIC-03, v9.4, BLG-SEC-35). Minimum scopes confirmed; actual token rotation delegated to a human with GitHub account/org security-settings access. |
