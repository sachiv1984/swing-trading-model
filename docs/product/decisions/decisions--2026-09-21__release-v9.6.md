Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.6
Cycle: 2026-09-21__release-v9.6
Last Updated: 2026-09-23 (ST-23, EPIC-06, BLG-SPEC-160 — added the PO-05 §13 pre-assessment determination + exact gate-line replacement text); prior — 2026-09-21 (initial publication at Release Planning)

## Planning Decisions — v9.6 Build-and-Ship Pull-Forward & Full-Capacity Debt Clearance

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Selected a 32-item / 28.00-day subset from the 76-item / 61.75-day ready pool via §1.4c: all ready P2 items first (0 ready P1), then category-balanced round-robin oldest-first for the remaining P3/P4 | Explicit "use full capacity" instruction; 28.00d is the top of the confirmed ~24–28 day band | Release Planning Engine (Head of Specs Team, agent-mediated) | 2026-09-21 |
| No Product Owner override of §1.4c was applied, although strict application leaves 12 of 16 `Provisional-Target: v9.6` items (4.80 days) unselected | An override requires an explicit Product Owner instruction for the specific cycle; none was given. Flagged as Friction Item 2 for a Product Owner / Head of Specs Team decision | Release Planning Engine | 2026-09-21 |
| `BLG-FEAT-96` and `BLG-FEAT-97` seated (ST-01, ST-03) and EPIC-01 placed first in the EPIC table | The 2026-09-19 rebalance's mandatory ≥2 build-and-ship pull-forward (Skill-Silo Alert 98.8%, 5th consecutive worsening reading); this cycle's execution-heavy rotation slot | Product Owner (rebalance `2026-09-19__scheduled`, STEP 7.1); carried out by Release Planning Engine | 2026-09-21 |
| `BLG-GOV-90` and `BLG-GOV-188` cleared into the ready pool and selected | Lapsed-date gates verified individually: `BLG-GOV-74`'s first quarterly review is filed (`ai_feature_usage_quarterly_review_2026-09-07.md`); `BLG-GOV-188`'s gate line states "None — … Met 2026-07-08" | Release Planning Engine | 2026-09-21 |
| `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FEAT-63`, `BLG-FE-84` **not** cleared | Lapsed date is not proof the gate is met — each item's AC requires named-owner verification before sprint planning, none is recorded, and the evidence is due at the 2026-09-24 AI review. Classified conditional (§1.4b) | Release Planning Engine | 2026-09-21 |
| `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` excluded from the ready pool | Each states in its own body text that it may not enter sprint planning yet, despite no formal `Gate` field | Release Planning Engine | 2026-09-21 |
| `BLG-GOV-335`, `BLG-GOV-336`, `BLG-GOV-337` (✅ COMPLETE 2026-09-19) and `BLG-GOV-326` (satisfied by v9.5 ST-38's recorded merge decision) excluded | Not open work; a first-pass selection had seated two of them | Release Planning Engine | 2026-09-21 |
| Effort-to-days conversion stated explicitly (explicit day figure/range → midpoint; hours or bare `XS` → 0.15d; bare `S`/`M`/`L` → canonical table) | v9.5's published total could not be reproduced under either simple rule; sensitivity band-only total is 27.90d | Release Planning Engine | 2026-09-21 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Within EPIC-01, sequence ST-01 (`BLG-FEAT-96`) → ST-02 (`BLG-FE-180`) → … → ST-06 (`BLG-FE-182`) last | ST-01 and ST-02 both edit `TradePlans.js`; ST-06 touches Positions, TradeHistory and TradePlans and must rebase onto ST-01/ST-02 | Release Planning Engine | 2026-09-21 |
| Within EPIC-02, sequence ST-07 (`BLG-FR-04`) before ST-08 (`BLG-FR-05`) | The net/gross basis must be documented before month-end snapshots freeze figures computed on it | Release Planning Engine | 2026-09-21 |
| Within EPIC-03, sequence ST-09 (`BLG-BE-119`) first, ahead of ST-13 (`BLG-BE-122`) | ST-09 is a decision on live-capital trailing-stop behaviour; ST-13 also touches the nightly stop-update path | Release Planning Engine | 2026-09-21 |
| Within EPIC-07, sequence ST-27 (`BLG-GOV-345`) before ST-30 (`BLG-GOV-325`) | Both edit governed prompts and bump `OPERATIONAL_GUIDE.md`; sequential landing avoids a silent same-version collision (CLAUDE.md §8 step 2a) | Release Planning Engine | 2026-09-21 |
| EPIC-01 and EPIC-02 flagged design-gate-triggering; `run design-gate` must pass before `plan sprint` can seal | 8 of 32 items carry an observable UI acceptance criterion or UI-shipping Scope text | Release Planning Engine | 2026-09-21 |
| Cross-EPIC: EPIC-03 ST-09 and EPIC-06 ST-22 depend on human/delegated access (Strategy Rules Owner sign-off; live-DB write access) | Disclose rather than fabricate if unavailable — same honest-disclosure precedent as `ESC-EXEC-20260910-01` | Release Planning Engine | 2026-09-21 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations raised during this release-planning session | — | — |

### ST-23 execution-time determination — PO-05 §13 pre-assessment (2026-09-23)

**Context:** `BLG-SPEC-160`/ST-23 (EPIC-06) requires a dated §13 determinism pre-clearance determination for PO-05 (Lightweight Replay Mode), and updating `BLG-FEAT-74`'s gate line to reflect the outcome.

**Determination:** **PASS.** Full four-criterion assessment (Determinism, Own-Data Only, Non-Predictive Output, Decision-Support Only — the same template already used for PS-03/IT-06) recorded in `docs/product/decisions/po05_section13_preassessment.md`, agent-mediated per `execution_prompt.md` §5.3 (Strategy Rules & System Intent Owner role). PO-05's determinism case is stronger than PS-03's own: it replays already-known historical data through the already-fixed current rule set, with no pseudo-random sampling involved at all. 6 binding conditions carried forward for `BLG-FEAT-74`'s eventual implementation sprint (see that document's own §13 Conditions section) — most importantly, this PASS covers *replay under the current rule set only*; any future hypothetical/user-editable rule-set variation is a different feature requiring its own review.

**Exact replacement text** (for whichever human/role applies it — `execution_prompt.md` §7 does not permit this engine to edit `backlog.md` directly; see Outstanding Actions):

- `BLG-FEAT-74` — replace `**Provisional-Target:** Unscheduled (gated — §13 determinism pre-clearance not yet run)` with:
  `**Provisional-Target:** Unscheduled — §13 pre-clearance PASS 2026-09-23 (see docs/product/decisions/po05_section13_preassessment.md), 6 binding conditions carry forward to implementation; gated only by normal Release Planning prioritisation given its VH (>2 weeks) effort size, not by §13`

**Also needed (outside this engine's write scope — governance folder):** `claude/strategy/strategy_rules.md` §13.5's roster table should gain a new row for PO-05 (`docs/product/decisions/po05_section13_preassessment.md`, cleared v9.6), per that section's own maintenance rule that new clearances add themselves to the roster in the same commit. `claude/strategy/` is a governance folder `execution_prompt.md` §7/CLAUDE.md §2 does not permit this engine to write to — flagged for Head of Specs Team / Strategy Rules & System Intent Owner to apply alongside the `backlog.md` edit above.

**Made by:** Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3; §13 determination itself is complete and actionable — only the two write-scope-restricted follow-up edits above require a human/differently-scoped role to apply).
**Date:** 2026-09-23

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-09-21__release-v9.6
