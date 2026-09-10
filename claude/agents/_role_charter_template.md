# <Role Name>

<!--
  Onboarding Template for New Agent Role Charters — ST-26 (BLG-GOV-183, EPIC-05, v9.3)

  Copy this file to claude/agents/<role_name_lowercase_with_underscores>.md and
  fill in every section below. Delete this comment block and all inline
  <angle-bracket> placeholders and guidance notes before filing the new
  charter — a real charter must read as a finished document, not a
  half-completed template.

  Required sections (per the existing 23 charters in claude/agents/, cross-
  checked for the pattern this template annotates): the header field block,
  §1 Purpose, §2 Core Responsibility, §N Responsibilities (numbered/detailed),
  §N Explicit Non-Responsibilities, §N Definition of Success. Everything
  else below is common but not universal — include what genuinely applies
  to this role, per the guidance notes at each section.
-->

**Role:** <Role Name — exact string used elsewhere to refer to this role, e.g. in sign-off blocks and delegation records>
**Reports to:** <the role or body this role is accountable to — e.g. "Head of Engineering", "Executive Leadership">
**Governance alignment:** <optional — other roles this one must stay consistent with on cross-cutting concerns, e.g. "Head of Specs Team (documentation lifecycle, document classes, headers, naming conventions)". Omit this field if the role has no such cross-cutting alignment requirement; not every charter has one (see qa_lead.md for an example without it).>
**Scope:** <one sentence — the domain this role owns, e.g. "Test execution leadership, automation oversight, and operational quality delivery">
**Status:** Canonical
**Version:** 1.0
**Last Updated:** <YYYY-MM-DD — the date this charter is filed>

### Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | <YYYY-MM-DD> | Initial canonical version. |

<!-- Every subsequent charter edit adds a new row here, newest first, per this codebase's universal Last-Updated/Changelog convention (see CLAUDE.md §2's `**Last Updated:**` header field rule). -->

---

## 1. Purpose

<!--
  1-3 sentences (or a short bulleted list, per existing charters' varying
  style) stating why this role exists — what gap it closes, what
  responsibility would otherwise have no clear owner. Answer: "This role
  exists to ensure that..." — see qa_lead.md §1 or base44_frontend_prompt_
  owner.md §1 for the pattern.
-->

This role exists to ensure that:
- <first thing this role guarantees>
- <second thing this role guarantees>

---

## 2. Core Responsibility

<!--
  A short paragraph (2-4 sentences) — the single-sentence-summarizable
  "what this role actually does day to day." More concrete and narrower
  than §1's Purpose; §4 (Responsibilities) then breaks this down into detail.
-->

---

## 3. Authority Model & Role Boundaries (Non-Negotiable)

<!--
  Optional but common for roles with cross-cutting or gate-holding
  authority (e.g. cybersecurity_trust_lead.md §3, qa_lead.md §3). State
  what this role has final say over, what it must escalate rather than
  decide unilaterally, and how it relates structurally to adjacent roles
  (independent oversight vs. reporting line vs. peer collaboration). Omit
  this section entirely for a role with no special authority/independence
  concerns — most charters do include some version of it, but not all.
-->

---

## 4. Responsibilities

<!--
  The detailed breakdown of §2's Core Responsibility, typically as
  numbered §4.1/§4.2/... subsections, each covering one distinct area of
  the role's work. This is normally the longest section in a charter — be
  concrete (name the actual artefacts, processes, or gates this role
  produces or holds), not aspirational.
-->

### 4.1 <Area of responsibility>

### 4.2 <Area of responsibility>

---

## 5. Explicit Non-Responsibilities

<!--
  What this role does NOT own, especially anything a reader might
  reasonably assume it does given its title or adjacent scope. This
  section exists specifically to prevent authority creep and duplicate/
  conflicting ownership between roles — name the role that actually owns
  each excluded item where relevant.
-->

---

## 6. Definition of Success

<!--
  What "this role is working well" looks like, in concrete/observable
  terms — not a restatement of §1/§2, but the evidence a reviewer would
  look for (e.g. "no P0 incident traced to a decision this role owned",
  "every gate this role holds has a documented, evidenced clearance").
-->

---

## 7. Guiding Principle(s)

<!--
  Optional — a short closing statement (one sentence to a short paragraph)
  capturing the role's operating philosophy in a memorable way, if one
  exists that isn't already fully captured by §1/§2. Many charters include
  this (e.g. qa_lead.md §7, base44_frontend_prompt_owner.md's "Guiding
  Principle"); some don't. Omit if it would just restate §1.
-->

<!--
  Additional sections seen in some existing charters, include only if genuinely
  applicable to this role:
    - Reporting & Interfaces (Reports to / Governed by / Works closely with,
      as a dedicated section rather than just header fields — see
      base44_frontend_prompt_owner.md §8)
    - Lifecycle & Versioning Compliance (if this role's own outputs are
      governed documents subject to the document_lifecycle_guide.md)
    - Delegation Requirements (if this role is ever the target of a
      delegated_backend/delegated_frontend/delegated_decision item in
      execution_prompt.md §5.1 — state the mandatory fields any delegation
      record to this role must include)
-->

---

## Acceptance

- Filed by: <who authored this charter>
- Reviewed by: <Head of Specs Team — role charters fall under its governance alignment per team_charter.md §4>
- Date: <YYYY-MM-DD>
