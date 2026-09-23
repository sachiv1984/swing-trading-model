Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.6
Cycle: 2026-09-21__release-v9.6
Last Updated: 2026-09-23 (ST-27, EPIC-07, BLG-GOV-345 — added the execution-time determination + exact gate-line replacement text for the 4 lapsed AI-adoption-window items); prior — 2026-09-21 (initial publication at Release Planning)

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

### ST-27 execution-time determination — lapsed AI-adoption-window gates (2026-09-23)

**Context:** `BLG-GOV-345`/ST-27 (EPIC-07) requires each of `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FEAT-63`, `BLG-FE-84` be individually verified and either cleared or re-gated with a new dated condition. The 2026-09-24 AI review named at Release Planning (see the "not cleared" row above) has not yet run as of this determination — it is scheduled for tomorrow, one day after this sprint-execution session. There is therefore still no new evidence to clear these gates on today; re-gating with a concrete forward date (rather than leaving the stale "~2026-07-25" text) is the correct disposition, not clearing.

**Determination:** Re-gate all 4 items — replace each item's `**Gate criteria:**` line with the text below, which anchors to the already-scheduled 2026-09-24 AI review instead of the lapsed 2026-07-25 date, and states explicitly that a lapsed date is not itself a clearance (closing the exact gap `BLG-GOV-345` was filed over, so the next scan of these same items doesn't reproduce it).

**Exact replacement text** (for whichever human/role applies it — `execution_prompt.md` §7 does not permit this engine to edit `backlog.md` directly; see Outstanding Actions):

- `BLG-FEAT-59` — replace `**Gate criteria:** AI adoption window clears ~2026-07-25 (same constraint as BLG-FEAT-55/56 — too early to layer additional AI-generated content onto financial reporting).` with:
  `**Gate criteria:** AI adoption window verification due at the 2026-09-24 AI feature usage review (BLG-GOV-74 cadence) — Financial Reporting & Records Owner to confirm usage patterns have stabilised before this clears. A lapsed date alone (the prior ~2026-07-25 estimate) is not a clearance; re-verify against the 2026-09-24 review's actual finding.`
- `BLG-FEAT-60` — replace `**Gate criteria:** AI adoption window clears ~2026-07-25 — usage patterns remain unestablished at current usage duration; metric definition would be premature.` with:
  `**Gate criteria:** AI adoption window verification due at the 2026-09-24 AI feature usage review (BLG-GOV-74 cadence) — Metrics Definitions & Analytics Owner to confirm usage patterns have stabilised before this clears. A lapsed date alone (the prior ~2026-07-25 estimate) is not a clearance; re-verify against the 2026-09-24 review's actual finding.`
- `BLG-FEAT-63` — replace `**Gate criteria:** Same AI-adoption gate as BLG-FEAT-59 (AI-assisted monthly P&L narrative) — clears ~2026-07-25.` with:
  `**Gate criteria:** Same AI-adoption gate as BLG-FEAT-59 — verification due at the 2026-09-24 AI feature usage review (BLG-GOV-74 cadence). A lapsed date alone (the prior ~2026-07-25 estimate) is not a clearance; track disposition on BLG-FEAT-59.`
- `BLG-FE-84` — replace `**Gate criteria:** AI adoption window clears ~2026-07-25 — usage patterns must stabilise before a research protocol targeting them is designed.` with:
  `**Gate criteria:** AI adoption window verification due at the 2026-09-24 AI feature usage review (BLG-GOV-74 cadence) — Head of UX & Design to confirm usage patterns have stabilised before this clears. A lapsed date alone (the prior ~2026-07-25 estimate) is not a clearance; re-verify against the 2026-09-24 review's actual finding.`

**Additional finding (not in this story's named 6, disclosed for awareness only):** re-running the extended scan (this story's own `scripts/scan_backlog_gate_conditions.py` change) at `--as-of 2026-09-23` surfaces 12 date-lapsed gated items, not 6 — `BLG-FEAT-55`, `BLG-OPS-53`, `BLG-GOV-121`, `BLG-SPEC-65`, `BLG-FEAT-62`, `BLG-FEAT-92` are also date-lapsed but were not named in `BLG-GOV-345`'s original 2026-09-19 finding. `BLG-FEAT-55` shares the identical AI-adoption-window gate as the 4 items above (same clears-~2026-07-25 text) and would benefit from the same replacement text if the Head of Specs Team wants to fold it in; the remaining 5 are unrelated gates and are left for a future `groom backlog` pass to individually verify, not decided here.

**Made by:** Sprint Execution Engine (documented determination only — the four gate-line edits above require Head of Specs Team / Product Owner application, per the write-scope constraint recorded in `sprint_backlog.md`'s Outstanding Actions table).
**Date:** 2026-09-23

### ST-28 — §13 boundary review cadence for ATR parameter calibration: drafted options (2026-09-23, decision NOT made by the engine)

**Context:** `BLG-GOV-329`/ST-28 requires deciding whether to schedule the ATR-parameter-calibration §13 review now, or formally defer with a concrete trigger — the 2 `rejected_but_strong.md` entries this blocks (`IDEA-strategy-owner-20260304-02` "ATR Parameter Sensitivity Analysis", `IDEA-challenger-20260304-01` "Force Explicit Evidence Review for ATR Parameter Selection") have sat "§13 ATR review-gated"/"Unmet" since 2026-03-04, with no standing cadence forcing a re-check. Per this story's own sprint-backlog note, **the engine may draft options but must not choose for the owner** — the determination below is explicitly not final.

**What would actually be reviewed:** `strategy_rules.md` §12.2 already lists "ATR multipliers" and "ATR lookback period" as parameters that may change, subject to §12.3's change-control requirements (documented, versioned, stated rationale/impact, applied consistently). The 2 rejected ideas ask for (a) a sensitivity analysis of the current ATR multiplier values, and (b) a governance gate requiring evidence review before any future ATR parameter change — i.e. a §13.2 boundary review confirming that *analysing or changing* these specific numerical constants doesn't cross into "adaptive rule system" territory, since §13.2 already treats the strategy as "a single, explicit, human-designed strategy" with parameters, not a tunable/adaptive one.

**A concrete trigger already exists and appears not yet met.** §12.2 itself (added ST-39, EPIC-04, v9.2, `BLG-GOV-262`) already defines a data-volume trigger: *"A review of these elements' calibration is triggered once 100 closed trades have accumulated since the last time any element in this list was reviewed."* The most recent closed-trade counts found anywhere in this repo's live-checked documents (SI-02 gate re-checks, `current_roadmap.md`) are all well under 100 — single digits to low twenties as of the most recent live confirmations (2026-06-09 through 2026-07-28) — so this trigger has very likely not yet fired, though this engine has no live-DB access this session to confirm the exact current count.

**Option A — Schedule the §13 ATR review now**, independent of the §12.2 trade-count trigger, since a *review of whether the current parameters are well-calibrated* is a smaller and different question than *changing* them, and doesn't necessarily need the same evidentiary bar as a change itself. Pro: closes a 6+-month-old open item; the review itself is scoped as small (per `BLG-GOV-329`'s own `S` effort estimate). Con: with a small trade sample, any sensitivity-analysis output is itself low-confidence — the review might conclude "insufficient data to say anything," which is arguably not worth scheduling yet.

**Option B — Defer, with the trigger set explicitly to §12.2's existing 100-closed-trades threshold** (rather than a new, separately-invented date or condition). This directly satisfies the AC's "if deferred again, the new trigger must be more concrete than the prior one" requirement — the revival condition becomes "closed-trade count crosses 100 since 2026-09-23" (or since the last §12.2-triggered review, if run first), a single unambiguous number rather than an open-ended "when §13 review is opened." Con: could sit for a long time yet if trade cadence stays low; the two ideas remain formally un-actioned in the interim (though `rejected_but_strong.md` already tracks them, so nothing is lost).

**Engine's lean, not a decision:** Option B — it reuses a trigger this codebase has already deliberately chosen for exactly this class of question (ATR/grace-period parameter recalibration reviews generally), rather than inventing a bespoke ATR-specific date, and directly produces the "more concrete than the prior one" trigger the AC requires without guessing at a closed-trade count this session cannot verify live.

**Standing-cadence question (BLG-GOV-329's second scope bullet):** whichever option is chosen above, a standing cadence beyond per-item expiry flagging is a separate, larger governance decision (would need its own scope/effort) — not drafted here as a concrete option, since `BLG-GOV-329`'s own AC treats it as "consider," not "decide."

**Status: Proposed, awaiting Strategy Rules & System Intent Owner confirmation** — not recorded as the sprint's final disposition. `ESC-EXEC-20260921-06` left `Open` pending that confirmation.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-09-21__release-v9.6
