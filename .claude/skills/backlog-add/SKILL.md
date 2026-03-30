---
name: backlog-add
description: Add one or more items to the product backlog (claude/backlog/backlog.md) with correct IDs, formatting, and section placement. Use this skill whenever the user says "add to the backlog", "file this for later", "track this", "we should backlog this", or any time bugs, gaps, ideas, or improvement actions surface during a session that aren't being actioned immediately. Also use proactively after delivery verification or sprint closure when deviations or observations produce follow-up items.
---

# Backlog Add

Adds one or more correctly-formatted, correctly-IDed items to `claude/backlog/backlog.md`.

## Step 0 — Load lessons

Read `.claude/skills/lessons_learnt.md` before doing anything else. Look for entries tagged `[backlog-add]` and apply them now. If the file doesn't exist, continue.

## Step 1 — Scan existing IDs

Read `claude/backlog/backlog.md` in full. For every ID namespace, record the highest number currently in use (search both active items AND the Closed Items table — archived items still consume their ID):

| Namespace | Covers | Example |
|-----------|--------|---------|
| BLG-GOV-xx | Governance process items | BLG-GOV-09 |
| BLG-FE-xx | Frontend component, page, UX interaction | BLG-FE-07 |
| BLG-UX-xx | UX / navigation / layout (no functional component change) | BLG-UX-02 |
| BLG-QA-xx | QA and test automation | BLG-QA-06 |
| BLG-OPS-xx | Operational / infrastructure | BLG-OPS-09 |
| BLG-SPEC-Dxx | Spec debt (sequential, not padded) | BLG-SPEC-D15 |
| BLG-TECH-xx | Platform / technical debt | BLG-TECH-05 |
| BLG-BE-xx | Backend engineering | BLG-BE-04 |
| BLG-FEAT-xx | User-facing product features | BLG-FEAT-11 |
| BLG-UX-xx | UX / interaction design | BLG-UX-01 |
| TEST-GAP-xxx | Test coverage gaps | TEST-GAP-EPIC-05-SLIP |

Assign each new item ID = highest in its namespace + 1. Never reuse an ID even if the prior holder was archived.

## Step 2 — Determine namespace for each item

Use this guide:
- Governance process, prompt changes, workflow policy → **BLG-GOV**
- Frontend component, page, or interaction (button, form, modal, data display) → **BLG-FE**
- Navigation structure, sidebar layout, information architecture, viewport behaviour with no new functional component → **BLG-UX**
- QA infrastructure, test automation, test tooling → **BLG-QA**
- Operational runbook, CI/CD, infrastructure, monitoring → **BLG-OPS**
- Spec debt — missing, wrong, or outdated documentation → **BLG-SPEC-D**
- Platform / third-party / non-feature technical debt → **BLG-TECH**
- Backend endpoint, service, data model → **BLG-BE**
- Net-new user-facing product feature → **BLG-FEAT**
- Test scenario coverage gap → **TEST-GAP**

**BLG-FE vs BLG-UX:** Use BLG-FE when a component needs to be built or changed. Use BLG-UX when the work is primarily about layout, navigation grouping, or information architecture — i.e. how things are arranged rather than what they do.

When in doubt, ask the user which namespace fits best.

## Step 3 — Gather item details

For each item, collect the following. Infer as much as possible from the user's description; only ask about fields you genuinely cannot determine:

| Field | Required | Guidance |
|-------|----------|---------|
| Title | Yes | Short imperative phrase — "Add X", "Fix Y", "Define Z" |
| Priority | Yes | P0 Critical / P1 High / P2 Medium / P3 Low |
| Type | Yes | e.g. "Governance Process", "Frontend / UX", "Spec Debt", "QA / Test Automation" |
| Owner | Yes | One or more role names from `claude/agents/` |
| Source | Yes | Where it came from: session date, deviation ID, user request, etc. |
| Effort | Yes | XS (<1h) / S (~0.5d) / M (~1–2d) / L (~3–5d) / H (>5d) |
| Provisional-Target | Yes | vX.Y — use the next release after current if unsure |
| Problem | Yes | 2–4 sentences: what is broken or missing, and why it matters |
| Scope | Yes | Bullet list of what will actually be done |
| Acceptance Criteria | Yes | Bullet list of verifiable, observable outcomes |
| Depends on | No | Other BLG-xxx items; only include if a hard dependency exists |

Draft the full item and show it to the user for confirmation before writing to the file. If adding multiple items, show all drafts together.

## Step 4 — Find the insertion point

The backlog is organised into numbered domain sections. New items go into a **session section** appended at the bottom of the active items area (before the first `<!-- release-plan-marker -->` comment) — do not insert items directly into a domain section.

The domain sections and their namespaces are:

| Section | Title | Namespaces |
|---------|-------|------------|
| §1 | Platform & Validation Governance | BLG-TECH |
| §2 | Product Feature Backlog (User-Facing) | BLG-FEAT |
| §3 | Frontend & UX | BLG-FE, BLG-UX |
| §4 | Backend & Data | BLG-BE |
| §5 | QA & Test Automation | BLG-QA, TEST-GAP |
| §6 | Operations & Infrastructure | BLG-OPS |
| §7 | Spec Debt | BLG-SPEC-D |
| §8 | Governance | BLG-GOV |

These sections are for reference (so you can orient the user and correctly categorise items). All new items are still appended to a session section — not inserted mid-file into a domain section.

- If a session section already exists for today's date (e.g. `## N. New Backlog Items — Session 2026-03-25`), append to it.
- If no session section exists for today, create a new one. Number it sequentially (next integer after the highest section number currently in the file):

```markdown
## {N}. New Backlog Items — Session {YYYY-MM-DD}

*User-raised items from session review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---
```

Never insert items inside a release slice section, a closed items table, or before existing active sections.

## Step 5 — Write the item

Use this exact template for every item:

```
### {ID} — {Title}
**Priority:** {P0|P1|P2|P3} ({Critical|High|Medium|Low})
**Type:** {type}
**Owner:** {owner role(s)}
**Source:** {source description} — {YYYY-MM-DD}
**Effort:** {XS|S|M|L|H} ({human-readable estimate})
**Provisional-Target:** {vX.Y}
[**Depends on:** {BLG-xxx (description)} — only if applicable]

**Problem**
{2–4 sentences describing the gap or pain point and why it matters}

**Scope**
- {what will be done}
- {what will be done}

**Acceptance Criteria**
- {verifiable outcome}
- {verifiable outcome}

---
```

## Step 6 — Update the header

Update the `**Last Updated:**` line at the top of `backlog.md` to:
```
**Last Updated:** {YYYY-MM-DD} (session — {N} new item(s) added: {comma-separated IDs})
```

## Step 7 — Confirm

Tell the user:
- IDs assigned and titles
- Section they were added to
- That the Last Updated header was updated

## Error handling and lessons learnt

If anything goes wrong — wrong ID assigned, wrong section chosen, format rejected by user, duplicate ID detected — do the following immediately:

1. Fix the mistake in the file.
2. Append an entry to `.claude/skills/lessons_learnt.md`:

```
| {YYYY-MM-DD} | backlog-add | {what went wrong — be specific} | {what the correct approach is} |
```

Apply the fix in the same session. The goal is that this class of mistake never happens again.