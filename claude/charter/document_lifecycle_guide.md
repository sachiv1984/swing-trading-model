# Documentation Lifecycle Guide

**Owner:** Head of Specs Team  
**Scope:** All governed documentation across the entire product  
**Status:** Canonical  
**Version:** 2.6
**Last Updated:** 2026-03-07  

---

## Change Log

| Version | Change |
|--------:|--------|
| 2.6 | Added Class 4 sub-type 3 — Release Plan (`release_plan.md`). The Release Planning Engine now consolidates all intermediate reasoning artefacts (readiness, scope, execution plan, capacity check, integrity validation) into a single `release_plan.md` per cycle. Final outputs (scope document, decisions record, backlog slice) remain separate. |
| 2.5 | Added Class 8 — Proof of Gate. New document class for hard gate clearance evidence. Immutable once issued; status field only may change to Superseded; permanent governance record stored in `claude/evidence/gates/`. Required when any governed routine records a hard gate condition that must be cleared before an item advances. Added Class 8 to Section 2, Section 3 (lifecycle states), Section 4 (universal header block), and Section 5 (versioning — Class 8 does not use version numbers). |
| 2.4 | Added Release Planning Engine governance alignment. Clarified that multiple governed routines may exist (e.g., Roadmap Rebalance, Release Planning), all invoked via Class 6 Governance Prompts. Explicitly recognised `claude/roadmap/` and `claude/backlog/` as valid planning-document locations for governed routines. |
| 2.3 | Clarified lifecycle enforcement roles to explicitly include Facilitator and Challenger as non-decision governance roles. No changes to document classes or lifecycle semantics. |
| 2.2 | Added Section 9 — Known Deviation Documentation Standard. When any deviation from canonical behaviour is documented in a spec, it must be assigned a priority tier, a target resolution release, and a named owner at the time of documentation. P0 deviations must be resolved within one release cycle. |
| 2.1 | Class 4 (Planning Document): added canonical location `docs/product/scope/` for scope documents, naming convention, and scope document as a distinct sub-type with its own supersession rule. |
| 2.0 | Expanded scope to cover all document classes. Added Operational Record, Planning Document, Role Charter, and Governance Prompt as formal classes. Added universal header block standard and enforcement mechanisms. |
| 1.0 | Initial version. |

---

## 1. Purpose

This guide defines how all product documentation is:

- Classified
- Created
- Maintained
- Reviewed
- Versioned
- Deprecated or archived
- Enforced for compliance

Its goal is to prevent:

- Silent drift between documents and reality
- Conflicting sources of truth
- Undocumented behavioural change
- Documents that influence decisions without a named owner

This guide applies to every document in the repository — not only specs. All roles that own documentation are bound by it.

---

## 2. Document Classes

Every governed document belongs to exactly one class. The class determines which header fields are required, which lifecycle states are valid, and how compliance is checked.

---

### Class 1 — Canonical

**What it is:** The authoritative source of truth for a product domain. When this document and any other document disagree, this document prevails.

**Who creates it:** A named domain owner.

**Lifecycle states available:** Draft → Canonical → Deprecated → Archived

**Required header fields:**
```
Owner:        [Role name]
Status:       Canonical
Version:      [x.y]
Last Updated: [date]
```

**Rules:**
- Must be listed in the Specs Index
- Must not be contradicted by any Supporting document
- Changes that alter meaning, behaviour, or consumer interpretation require a version increment
- Deprecation requires an explicit successor declaration and effective date

**Examples:** `strategy_rules.md`, `data_model.md`, `metrics_definitions.md`, `api_contracts/*_endpoints.md`, `frontend/pages/*.md`, `document_lifecycle_guide.md` (this document)

---

### Class 2 — Supporting

**What it is:** A document that represents or summarises canonical truth. It adds no new rules. It must never contradict a Canonical document.

**Who creates it:** The domain owner of the canonical document it supports, or a designated maintainer.

**Lifecycle states available:** Current → Deprecated → Archived (no "Canonical" status — it derives authority from its source)

**Required header fields:**
```
Owner:            [Role name]
Status:           Supporting
Canonical Source: [path to canonical document]
Last Updated:     [date]
```

**Rules:**
- Must be reviewed inline with its canonical source whenever the canonical source changes
- Must declare which canonical document it represents
- A Supporting document becoming inconsistent with its canonical source is a system bug

**Examples:** `docs/reference/openapi.yaml`, diagrams, generated references

---

### Class 3 — Operational Record

**What it is:** A point-in-time record of observed system state. It records facts — it does not define rules or intended behaviour.

**Who creates it:** Infrastructure & Operations Documentation Owner (governs and files); engineering team (generates the underlying data).

**Lifecycle states available:** Filed (permanent — Operational Records are never deprecated or superseded)

**Required header fields:**
```
Owner:              Infrastructure & Operations Documentation Owner
Status:             Operational Record
Deployment Version: [version]
Report Date:        [date]
Environment:        [e.g. Production]
Generated By:       [system or person]
Filed:              [date filed]
```

**Rules:**
- Body content is immutable after filing — it records observed state at a fixed moment
- A newer record does not supersede an older one — both remain permanent artefacts
- Deviations from canonical specs observed in a record must be raised to the relevant domain owner; they are not resolved by annotating the record
- Naming convention: `System_status_report_v{version}_{YYYY-MM-DD}.md`
- Location: `docs/operations/status_reports/`

**Examples:** `System_status_report_v1.4_2026-02-14.md`

---

### Class 4 — Planning Document

**What it is:** A working document capturing product decisions, feature intent, prioritisation, and backlog thinking. It is pre-canonical.

Planning Documents include three distinct sub-types:

1. **Roadmap, backlog, and decisions documents** — ongoing planning artefacts that evolve over time
2. **Scope documents** — implementation briefs written at the end of pre-alignment
3. **Release plan** (`release_plan.md`) — consolidated intermediate planning record produced by the Release Planning Engine. Contains all intermediate reasoning (readiness, scope, execution plan, capacity check, integrity validation). Retained in `claude/cycles/<cycle_id>/release_plan.md`. Final outputs (scope document, decisions record, backlog slice) are retained separately.

**Who creates it:** Product Owner.
**Lifecycle states:** Draft → Active → Superseded → Archived

**Required header fields:**

```
Owner:        Product Owner
Class:        Planning Document (Class 4)
Status:       Draft | Active | Superseded
Last Updated: [date]
```

**Rules:**

- Planning documents may exist in governed planning workspaces used by governance prompts (e.g., `claude/roadmap/`, `claude/backlog/`) as well as in `docs/product/`.
- When a governed routine is in effect (e.g., Roadmap Rebalance Engine or Release Planning Engine), the prompt-defined write scope is authoritative for where Class 4 documents are created or updated.
- Planning documents must never be cited as canonical intent.

---

### Class 5 — Role Charter

**What it is:** A document defining the scope, responsibilities, and operating standards of a named role in the documentation or engineering system.

**Who creates it:** Head of Specs Team (for Specs Team roles) or the role's functional lead (for Engineering roles). All charters are stored in `docs/documentation_team/specs/`.

**Lifecycle states available:** Draft → Canonical → Deprecated

**Required header fields:**
```
Owner:        Head of Specs Team [or functional lead]
Status:       Canonical
Version:      [x.y]
Last Updated: [date]
```

**Rules:**
- Every role that owns documents must have a charter
- Every charter must include a "Lifecycle & Versioning Compliance" section explicitly stating that the role owner is accountable for compliance of all documents they own
- Every charter must declare who the role reports to
- Charters are versioned when role scope or reporting line changes
- A role without a charter may not be treated as authoritative — their documents are Draft until a charter exists

**Examples:** `Head_of_Specs_Team.md`, `API_Contracts_&_Documentation_Owner.md`, `Infrastructure_and_Operations_Owner.md`

---

### Class 6 — Governance Prompt

**What it is:** An instruction set used to invoke automated, governed routines that enforce this lifecycle guide.
**Who creates it:** Head of Specs Team.
**Lifecycle states:** Draft → Active → Deprecated

**Required header fields:**

```
Owner:        Head of Specs Team
Status:       Active
Version:      [x.y]
Last Updated: [date]
```

**Rules:**

- Multiple governed routines may coexist (e.g., Roadmap Rebalance, Release Planning).
- Each governed routine must have exactly one Class 6 governance prompt stored under `claude/system/`.
- The prompt defines:
  - invocation syntax
  - allowed write scope
  - enabled vs disabled governance steps
- Governance prompts are governance infrastructure, not product documentation.

---

### Class 8 — Proof of Gate

**What it is:** An immutable evidence record confirming that a specific hard gate condition has been cleared. A hard gate is not considered cleared until a Class 8 document exists in `claude/evidence/gates/` referencing the specific initiative, gate condition, and the versioned document whose content the clearance was based on.

**Who creates it:** The authority role responsible for clearing the gate (e.g. Strategy Rules & System Intent Owner for §13 boundary gates; Head of Specs Team for lifecycle compliance gates; Director of Quality for quality gates).

**Lifecycle states available:** Active → Superseded

> Superseded is the only permitted state transition. A PoG document may never be edited, deleted, or archived. If the gate must be re-cleared (e.g. because the referenced document was incremented), a new PoG is issued and the prior one is marked Superseded with a reference to its successor. Both documents remain as permanent audit records.

**Required header fields:**
```
Owner:                        [Clearing authority role]
Class:                        Proof of Gate (Class 8)
Status:                       Active | Superseded
Gate ID:                      POG-<YYYYMMDD>-<nn>
Issued:                       [date]
Cycle:                        [cycle_id]
Initiative:                   [initiative name]
Gate cleared:                 [one sentence — what condition is now satisfied]
Versioned document referenced:[file path] v[version]
Decision:                     [exact decision text — specific enough to stand alone]
Confirmed by:                 [role name]
Checksum note:                [document version at time of signing, e.g. "strategy_rules.md v2.3 as of 2026-03-04"]
```

If Status is Superseded, add:
```
Superseded by:                [Gate ID of successor PoG]
Superseded date:              [date]
```

**Rules:**
- Body content is immutable after issuance — only the Status, Superseded by, and Superseded date fields may be added or changed
- A PoG is automatically stale (and must be re-issued) when the versioned document it references is incremented after the PoG was issued
- Stale PoG documents do not clear their gate — the gate is treated as open until a fresh PoG is issued against the current document version
- The `claude/evidence/gates/` folder is append-only; no PoG document may be deleted
- PoG documents are not subject to the planning document grooming lifecycle — they are permanent governance records
- One PoG per gate condition per initiative per cycle — if the same gate must be cleared twice in one cycle (e.g. after a document increment), the second PoG supersedes the first
- Location: `claude/evidence/gates/<gate-slug>_<YYYYMMDD>.md`

**When required:** A Class 8 PoG is required whenever a governed routine (roadmap rebalance, design gate, or any other engine) records a hard gate condition in a stage artefact. Items carrying an uncleared hard gate may not advance to the next stage.

**Not required for:** Items with no recorded hard gate conditions. The absence of a PoG is not a compliance violation for items where no hard gate was raised.

---

## 3. Lifecycle States

### Universal states (available to all classes unless restricted above)

| State | Meaning | Who sets it |
|-------|---------|-------------|
| **Draft** | In progress, not authoritative | Document owner |
| **Canonical** | Authoritative source of truth | Document owner, confirmed by Head of Specs Team |
| **Active** | In use and current (for non-canonical classes) | Document owner |
| **Filed** | Permanently recorded (Operational Records only) | Ops Documentation Owner |
| **Superseded** | Replaced by canonical documents (Planning only); or prior gate clearance replaced by new PoG (Class 8) | Product Owner (Class 4); Clearing authority (Class 8) |
| **Deprecated** | No longer authoritative; successor declared | Document owner |
| **Archived** | Historical only; no longer referenced | Head of Specs Team |

**Rules that apply to all classes:**
- Every governed document must be in exactly one state at all times
- State must be declared explicitly in the document header
- No document may move from Deprecated or Archived back to an active state — a new document must be created instead
- Deprecation requires: what supersedes it, and from what date
- **Class 8 exception:** PoG documents may only transition Active → Superseded. They may never be Deprecated, Archived, or deleted. Supersession does not remove the document from the record.

---

## 4. Universal Header Block

Every governed document must carry a header block. The exact fields depend on document class (see Section 2), but the following fields are **required for all classes** except Operational Record (which has its own fixed set) and Class 8 (which has its own fixed set):

- **Owner** — the named role accountable for this document
- **Status** — one of the lifecycle states defined in Section 3
- **Last Updated** — the date the document was last meaningfully changed

Canonical documents and Role Charters additionally require:
- **Version** — incremented according to the versioning rules in Section 5

Class 8 (Proof of Gate) documents use their own fixed header set (see Section 2 — Class 8). They do not carry a Version field. Gate IDs serve as the unique identifier.

A document without a complete header block is non-compliant and must not be treated as authoritative regardless of its content.

---

## 5. Versioning Rules

Versioning applies to Canonical documents, Role Charters, and Governance Prompts.

**Class 8 (Proof of Gate) documents do not use version numbers.** Gate IDs (`POG-<YYYYMMDD>-<nn>`) serve as the unique identifier. When a PoG must be re-issued, a new Gate ID is issued and the prior PoG is marked Superseded — no version increment is involved.

**A version increment is required when:**
- Meaning changes
- Behaviour or rules change
- A consumer reading the document would act differently as a result

**A version increment is not required for:**
- Typo corrections
- Formatting changes
- Pure clarification that adds no new meaning

**Version format:** `x.y` where `x` (major) increments on breaking or significant behavioural changes, and `y` (minor) increments on additive or clarifying changes.

---

## 6. Mandatory Inline Review for Supporting Artifacts

When a change affects a Canonical document:

- Any Supporting document that represents that domain must be reviewed inline in the same change
- Approval must only be granted once alignment is confirmed

This applies explicitly to:
- API contracts ↔ `docs/reference/openapi.yaml`

If a change is explicitly declared "no contract change" and affects only internal implementation, Supporting artifact review is not required. Disputes are escalated to the Head of Specs Team.

---

## 7. Ownership & Accountability

**Every document must have a named owner.** A document without an owner is non-compliant.

**Domain owners are responsible for:**
- Accuracy of their documents
- Keeping documents current when the system they describe changes
- Ensuring Supporting documents remain aligned with their Canonical sources
- Initiating deprecation when a document is superseded

**The Head of Specs Team is responsible for:**
- Enforcing lifecycle compliance across all document classes
- Blocking changes when lifecycle rules are violated
- Resolving ambiguity about document class or ownership
- Maintaining and updating this guide
- Conducting or triggering compliance audits

**The Head of Specs Team has authority to audit any document in the repository** regardless of which function its owner reports into. Lifecycle compliance is a cross-functional standard, not a Specs Team internal rule.

---

## 8. Enforcement Mechanism

### When compliance is checked

Governance review must be triggered at the following points:

| Trigger | What is reviewed | Who triggers it |
|---------|-----------------|-----------------|
| New document created | Header completeness, correct class assignment, owner named | Document owner (self-check), Head of Specs Team (on merge) |
| Existing document updated | Version increment if required, header currency | Document owner (self-check), Head of Specs Team (on merge) |
| Feature shipped | Planning documents for that feature updated to Superseded; canonical specs confirmed as filed | Head of Specs Team |
| New role created | Charter exists and is compliant before role is treated as authoritative | Head of Specs Team |
| Periodic audit | All documents checked for compliance | Head of Specs Team (quarterly recommended) |
| Governance guide updated | Governance reviewer prompt updated in same change | Head of Specs Team |
| PoG referenced document incremented | All PoG documents referencing that document checked for staleness | Head of Specs Team / PMO Lead |

### How compliance is checked

The governance reviewer prompt (`docs/documentation_team/prompts/governance_reviewer.md`) is the primary compliance tool. It must be invoked using the prompt as a system instruction with the document(s) under review provided as context.

Automated review assists but does not replace owner accountability.

### What happens when compliance fails

| Severity | Condition | Consequence |
|----------|-----------|-------------|
| **Blocking** | Missing owner, missing status, Canonical document with no version | Document must not be merged or treated as authoritative until remediated |
| **Required** | Incorrect lifecycle state, version not incremented when required, Supporting artifact not reviewed inline | Must be remediated before the change is considered complete |
| **Advisory** | Minor header formatting inconsistency, Last Updated date stale | Should be remediated; does not block |
| **Blocking (Class 8)** | PoG references a document version that has been incremented — gate is stale | Gate treated as uncleared; item may not advance until PoG re-issued |

### Enforcement Roles

**Head of Specs Team**
- Owns lifecycle standards
- Blocks non‑compliant documents
- Resolves classification ambiguity
- Conducts audits
- Triggers PoG staleness checks when a referenced document is incremented

**Facilitator (Process Role)**
- Enforces lifecycle compliance during governed routines
- May halt execution if lifecycle rules are violated
- Has no authority to waive requirements or approve non-compliance
- Must verify PoG validity before allowing a gated item to advance

**Challenger (Process Role)**
- Surfaces documentation risk or ambiguity during decision routines
- May delay advancement until documentation integrity is clarified
- Does not assess, approve, or override lifecycle compliance

---

## 9. Known Deviation Documentation Standard

### Purpose

When a canonical spec owner identifies that the system's actual behaviour deviates from the canonical specification — whether discovered during implementation, code review, testing, or audit — they must document the deviation. However, documentation without triage is insufficient. An undated, unprioritised deviation note in a spec can sit unresolved indefinitely, as demonstrated by BLG-TECH-01 (Sharpe variance and capital efficiency errors sat in `analytics_endpoints.md` known limitations and `metrics_definitions.md` Appendix E through the full v1.5 lifecycle without a forced resolution path).

This section defines the mandatory standard for all such documentation.

### Required fields when documenting a deviation

Every deviation documented in a canonical spec — whether in a "Known Limitations", "Backlog Items", "Deviations", or equivalent section — must include at the time of writing:

| Field | Description |
|-------|-------------|
| **Deviation description** | What the current behaviour is and how it differs from canonical |
| **Canonical requirement** | What the spec says should happen |
| **Priority** | P0 / P1 / P2 / P3 using the standard backlog priority definitions |
| **Target resolution release** | The specific version by which this must be resolved (not "TBD") |
| **Owner** | The named role responsible for the fix |
| **Backlog reference** | The backlog item ID (e.g. BLG-TECH-01) — must be created at the time the deviation is documented |

### Priority-based resolution rules

| Priority | Required action |
|----------|----------------|
| **P0** | Must be resolved before the next release ships. May not be deferred. The release is a quality gate for this item. |
| **P1** | Must be assigned a specific target release within the current or next release cycle. May not remain open-ended. |
| **P2** | Target release must be named. May be deferred one release cycle with explicit Product Owner acknowledgement. |
| **P3** | Target release may be "backlog" but must be reviewed at the next quarterly audit. |

### Enforcement

- The Head of Specs Team is responsible for ensuring deviations are documented with all required fields
- A deviation documented without a priority, target release, or owner is non-compliant and must be remediated before the document is merged
- At each governance review trigger point (§8), any deviation notes in canonical specs are checked for compliance with this standard

### Roles outside the Specs Team

This standard applies to all canonical documents, regardless of which function their owner reports into. Engineering-owned operational documentation that records deviations from canonical behaviour must follow the same standard and escalate to the relevant canonical spec owner.

---

## 10. Roles Outside the Specs Team

This guide applies to **all roles that own documents**, including those outside the Specs Team. Specifically:

- **Product Owner** — Planning Documents must follow Class 4 rules
- **Engineering Lead** — any documentation owned by the engineering function must follow this guide
- **Infrastructure & Operations Documentation Owner** — Operational Records and Operational Guides must follow Class 3 and Class 1 rules respectively
- **QA & Testing Owner** — testing documentation must follow this guide

The Head of Specs Team sets these standards. Roles outside the Specs Team follow them. This is a standards relationship, not a management relationship — the Head of Specs Team does not manage those roles but does have authority to flag non-compliance to their functional lead.

---

## 11. Non-Negotiable Rule

> If a document influences decisions,
> it must be owned, reviewed, and aligned at the point of change.