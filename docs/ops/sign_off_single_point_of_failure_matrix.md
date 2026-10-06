**Owner:** Head of Specs Team; PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-06 (matrix created)
**Source:** ST-21 (`BLG-GOV-357`), EPIC-04, cycle `2026-10-06__release-v9.10`

# Sign-off Single-Point-of-Failure Matrix

## 1. Purpose

This matrix maps each sign-off gate in the six governed phases to the role or roles authorised to clear it, and flags every gate that has a single point of failure. A gate is a single point of failure when one named role's unavailability stalls the cycle and the governance stack names no alternate signer. Phases covered: roadmap rebalance, release planning (including the design gate, which runs between release planning and sprint planning), sprint planning, sprint execution, delivery verification and post-ship closure.

It is a reference for planning human availability and for future decisions on deputies. It changes no gate; the prompts listed in the Source column remain canonical.

## 2. Method

- Each gate was read from its phase prompt in `claude/system/`, at the versions in `OPERATIONAL_GUIDE.md` §14 on 2026-10-06. The Source column cites the section.
- **Signer type:**
  - **Sole:** exactly one role may clear the gate.
  - **Joint:** two or more roles must **all** sign. Each of them is a single point of failure for that gate.
  - **Any-of:** any one of the listed roles may clear it.
- **Agent-mediable** (`execution_prompt.md` §5.3): whether an agent may sign in that role when the human is unavailable. "Always human" gates (§5.3 Always-human gates) cannot be agent-mediated. For agent-mediable gates, the engine runs the named role's agent sign-off itself, so the human role is a SPOF only for the ruling or acceptance content, not for routine spec review.
- **SPOF flag:** ⚠ marks a gate where at least one required role has no alternate and the gate is not agent-mediable. △ marks a gate that is Sole or Joint but agent-mediable under §5.3, a softer dependency.

## 3. Matrix

### 3.1 Roadmap rebalance (`roadmap_prompt.md`)

| Gate | Authorised signer(s) | Type | Agent-mediable | SPOF | Source |
|------|---------------------|------|----------------|------|--------|
| Advance decision on a scored item | Product Owner | Sole | No (scope decision) | ⚠ | STEP 5 Debate |
| Score-5 §13 veto check on an advancing item | Strategy Rules & System Intent Owner | Sole | Yes, with user direction (precedent: v9.6 ESC-EXEC-20260921-05) | △ | STEP 5 Score-5 veto check |
| Proof of Gate (PoG) issuance for a hard-gated item | The gate's clearing authority (varies by gate) | Sole per gate | Depends on the role | △ | STEP 5.3 |
| §7.3 mandatory review when the gap grows 3+ releases | Product Owner + Head of Specs Team | Joint | Head of Specs Team yes; Product Owner no | ⚠ (Product Owner) | STEP 7.3 trigger |
| STEP 11 action-now governance patches | Head of Specs Team | Sole | Yes | △ | §4 Write Scope |

### 3.2 Release planning (`release_planning_prompt.md`) and design gate (`design_gate_prompt.md`)

| Gate | Authorised signer(s) | Type | Agent-mediable | SPOF | Source |
|------|---------------------|------|----------------|------|--------|
| Release scope and publish (Published, sealed) | Product Owner | Sole | No (scope) | ⚠ | §2, §12 Published |
| Domain blocks (Quality, Strategy) during planning | Director of Quality; Strategy Rules & System Intent Owner, each in its domain | Sole per domain | Yes, with user direction | △ | §2 Delegated Authority |
| Stale backlog lock removal | PMO Lead | Sole | No (manual file action) | ⚠ | -1.8 lock recovery |
| §-1.2 Option (b) rebalance-equivalence ruling | Head of Specs Team | Sole | Yes | △ | §-1.2 (ESC-CLOSE-20260928-02 ruling) |
| Design gate: decision record approval per Design Required item | Head of UX & Design + Product Owner | Joint | Head of UX & Design yes; Product Owner no | ⚠ (Product Owner) | `design_gate_prompt.md` approval block |
| Design gate: downgrade of a Design Required item | Head of UX & Design | Sole | Yes | △ | `design_gate_prompt.md` classification |

### 3.3 Sprint planning (`sprint_planning_prompt.md`)

| Gate | Authorised signer(s) | Type | Agent-mediable | SPOF | Source |
|------|---------------------|------|----------------|------|--------|
| Sprint goal confirmation | Product Owner | Sole | No (always human, `execution_prompt.md` §5.3) | ⚠ | STEP 6.2 Sign-Off Gate |
| Sprint backlog seal | Product Owner | Sole | No (always human) | ⚠ | STEP 6.2, STEP 7 |
| Capacity buffer-floor / WARN acceptance | Product Owner (FinOps & Resource Architect supplies the number) | Sole | No | ⚠ | §1.5 buffer floor, STEP 3.2 Capacity Gate |
| Director of Quality AC readiness check | Director of Quality | Sole | Yes (agent-mediated in practice every cycle) | △ | STEP 4.3 |

### 3.4 Sprint execution (`execution_prompt.md`)

| Gate | Authorised signer(s) | Type | Agent-mediable | SPOF | Source |
|------|---------------------|------|----------------|------|--------|
| Merge gate: QA sign-off on the PR | Director of Quality | Sole | **No (always human)** | ⚠ | §5.3 Always-human gates; STEP 4 |
| Merge gate: Product Owner acceptance on the PR | Product Owner | Sole | **No (always human)** | ⚠ | §5.3 Always-human gates; STEP 4 |
| EPIC DoQ sign-off block (`qa_evidence_EPIC-xx.md`) | Director of Quality, or the autonomous class (BLG-GOV-19 criteria), or a named domain role / Infrastructure + DoQ co-sign | Any-of | Yes | none | §3.2.A |
| Spec sign-offs named in a story's seal condition | The named spec role (Head of Specs Team, API Contracts & Documentation Owner, Data Model & Domain Schema Owner) | Sole per story | Yes | △ | §5.3 |
| `delegated_decision` strategy rulings | Strategy Rules & System Intent Owner | Sole | Only with explicit user direction (precedent v9.6, v9.9) | ⚠ (in practice) | §3.1.D |
| Live-environment actions (migrations, production reads, Render/GitHub control) | Data Model & Domain Schema Owner / Infrastructure & Operations Owner, acting as a human with live access | Sole per action | **No.** The sandbox has no write access, so this cannot be agent-mediated | ⚠ | §3.1.B; LL-v8.0-P3-01 |
| Sprint close acceptance | Product Owner | Sole | **No (always human)** | ⚠ | §5.3 Always-human gates; STEP 5 |

### 3.5 Delivery verification (`delivery_verification_prompt.md`)

| Gate | Authorised signer(s) | Type | Agent-mediable | SPOF | Source |
|------|---------------------|------|----------------|------|--------|
| Director of Quality sign-off (verification report §9) | Director of Quality | Sole | Yes (Tier 2 accepts agent-mediated) | △ | §9 Sign-off Block; -1.3 |
| Product Owner acceptance (verification report §9) | Product Owner | Sole | No | ⚠ | §9 Sign-off Block |
| P1 deviation acceptance | Product Owner **and** Director of Quality | Joint | Product Owner no; Director of Quality yes | ⚠ (Product Owner) | §7 Deviation Severity Policy |
| Scope ambiguity / Known Deviations rulings | Head of Specs Team | Sole | Yes | △ | STEP 3 rulings |

### 3.6 Post-ship closure (`post_ship_closure.md`)

| Gate | Authorised signer(s) | Type | Agent-mediable | SPOF | Source |
|------|---------------------|------|----------------|------|--------|
| Changelog entry (needs the Product Owner sign-off date) | Product Owner (date carried from verification) | Sole | No | ⚠ | STEP 1 |
| Closure-escalation rulings on governance prompts | Head of Specs Team | Sole | Yes | △ | STEP 8 / §3.7 recurrence escalations |
| Outstanding-action closure decisions | The action's owner role (varies) | Sole per action | Depends on the role | △ | STEP 3 / outstanding actions |

## 4. Gates Flagged as Sole-Signer Single Points of Failure (⚠)

**Product Owner** is the single point of failure for the most gates: 12 of the 16 ⚠ gates across all six phases. These are release publish, the advance decision, sprint goal, sprint seal, capacity acceptance, PR acceptance, sprint close, verification acceptance, P1 deviation acceptance, design-record approval, the changelog date and the §7.3 mandatory review. Most are "always human" by design (`execution_prompt.md` §5.3), so this dependency is intended, not accidental. It does mean a Product Owner absence stalls every phase boundary.

The remaining ⚠ gates:
- **Director of Quality, PR QA sign-off** (always human): the only Director of Quality gate that cannot be agent-mediated.
- **PMO Lead, stale backlog lock removal**: a manual file action with no alternate named.
- **Live-environment human with production access** (acting as Data Model & Domain Schema Owner or Infrastructure & Operations Owner): every migration, production read and live-fire check depends on one human with credentials. This was the most frequent cause of `blocked_backend` items over v9.6–v9.10 (DS-22, DS-23, DS-24, DS-25; ESC-EXEC-20260921-02/03/04).
- **Strategy Rules & System Intent Owner, strategy rulings**: agent-mediable only with explicit user direction, so in practice a human dependency for every `delegated_decision` ruling.

## 5. Observations (no change made)

- No gate in the governance stack names a deputy or alternate signer. Where a phase has stalled on a missing signer, it was resolved by the user acting in the role or authorising agent mediation, not by a defined alternate.
- The △ gates are mitigated by §5.3 agent mediation. The ⚠ gates are deliberately human-only, or depend on access the sandbox lacks. Any decision to add deputies is a governance change, outside this matrix's scope, for the Head of Specs Team and Product Owner.

## 6. Maintenance

Re-check this matrix when any phase prompt's sign-off, seal or "always human" rule changes (CLAUDE.md §6 governance edits), and at each lifecycle audit (`run audit`).
