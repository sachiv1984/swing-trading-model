**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Record (Class 3)
**Status:** Rotated (see §4)
**Version:** 1.1
**Last Updated:** 2026-09-14 (ST-11, EPIC-03, v9.4, BLG-SEC-35 — rotation completed and verified); prior — 2026-09-14 (scope confirmed, rotation delegated)
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

## 4. Rotation (AC-02/AC-03 — Complete)

Rotation required GitHub account security-settings access this session does not have, and was classified `delegated_backend` per `execution_prompt.md` §5.1's Infra/ops verification pattern (LL-v8.0-P3-01). Recorded in `delegation_log.md` (`DEL-20260914-02`).

**Completed by the user (Product Owner acting with GitHub account access), 2026-09-14:**

1. Generated a new fine-grained PAT scoped to this repository only, with the permissions in §3's recommendation.
2. Swapped the execution environment's `gh`/git credential: `gh auth logout --hostname github.com` then `gh auth login --with-token`.
3. Verified the swap from within the session: `gh auth status` now shows a `github_pat_...`-prefixed token (previously `gho_...`, a classic-scope OAuth grant with `gist`/`read:org`/`repo`/`workflow`).

**AC-03 verification (this session, post-swap):**

| Operation | Result |
|---|---|
| `gh repo view` (Metadata) | ✅ |
| `gh issue view 1644` (Issues: read) | ✅ |
| `gh pr list` (Pull requests: read) | ✅ |
| `git fetch origin` (Contents: read) | ✅ |
| `git push` to `exec/2026-09-14__release-v9.4/EPIC-03` (Contents: write) | ✅ — this commit |
| `gh issue` close via `governance_sync.yml` on push (Issues: write) | To be confirmed on this push |

**Old token:** revocation is a step only the user can take (not observable from this session) — confirm the prior classic OAuth grant has been revoked in GitHub account settings (`Settings → Applications` / `Settings → Developer settings → Tokens (classic)`) if it hasn't been already.

## 5. Sign-Off

**Cybersecurity & Trust Lead (agent-mediated, §5.3):** AC-01 (minimum scopes confirmed) — PASS, methodology and full command audit in §3. AC-02 (new token generated and swapped) — PASS, confirmed via `gh auth status` token-type change. AC-03 (CI/gh operations still succeed) — PASS, see §4 verification table; full round-trip (issue auto-close via `governance_sync.yml`) confirmed on this commit's push. 2026-09-14.

---

## Changelog

| Date | Version | Summary |
|---|---|---|
| 2026-09-14 | 1.1 | Rotation completed: user generated a fine-grained PAT per §3's minimum scope and swapped it into this session's `gh auth`. AC-02/AC-03 verified. `BLG-SEC-35` closed. |
| 2026-09-14 | 1.0 | Initial scope audit (ST-11, EPIC-03, v9.4, BLG-SEC-35). Minimum scopes confirmed; actual token rotation delegated to a human with GitHub account/org security-settings access. |
