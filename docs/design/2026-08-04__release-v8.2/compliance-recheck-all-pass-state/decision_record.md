**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-08-04
**Cycle:** 2026-08-04__release-v8.2
**Backlog source:** BLG-FE-105
**Maps to:** EPIC-01, ST-02

---

# Decision Record — Compliance Recheck Modal All-Pass State

## 1. Problem

`ComplianceRecheckModal.js` (v6.9) has a confirmed design for Loading, Error, and the Warn/Fail path (checklist plus an override-acknowledgement checkbox, per `positions.md` §Compliance Recheck Panel (Modal)). There is no confirmed design for the all-rules-pass case — today the code simply renders the checklist with five green ✓ rows and nothing else, which happens to be adequate but was never a deliberate design decision (`hasWarnOrFail` gates the acknowledgement block; nothing fills the equivalent space when all rules pass).

## 2. Options Considered

1. **No change** — full checklist with pass icons is sufficient; the five green ✓ rows already communicate "all clear" without extra copy.
2. **Add an affirmation line** — a single line below the checklist, symmetrical to the warn/fail acknowledgement block's position, confirming the all-pass outcome explicitly rather than leaving the user to infer it from the absence of a warning.

## 3. Decision: Option 2

The warn/fail path gets an explicit, styled block (border-top divider + text) confirming what happened and what the user is acknowledging. The pass path currently gets nothing in that same visual slot — an asymmetry that reads as unfinished rather than intentional. A one-line affirmation closes that gap cheaply, reusing the existing pass colour token (no new colour introduced).

**Spec:**

- Shown only when `overall_status === "pass"` (mirrors the existing `hasWarnOrFail` gate's structure exactly, in the same position, as its positive-case complement)
- Same layout slot as the acknowledgement block: `mt-4 pt-3 border-t border-slate-700/50`
- Text: **"All 5 checks passed — no action needed."**
- Colour: `text-emerald-400` (the existing `OVERALL_BADGE.pass` / `STATUS_COLOR.pass` token — no new colour)
- No interactive element (nothing to acknowledge) — plain text, not a button or checkbox
- No icon change — the five per-row ✓ glyphs already carry the visual weight; this is a closing summary line, not a new graphic element

## 4. Compliance Check

No conflict with `strategy_rules.md §13` — this is a display-only text addition to an existing read-only recheck result; no new automation, scoring, or decision logic.

## 5. Sign-off

- **Head of UX & Design:** Approved — 2026-08-04 (reuses existing pass colour token; no new visual pattern)
- **Product Owner:** Approved — 2026-08-04 (confirms Option 2 over Option 1 — explicit affirmation preferred over relying on absence-of-warning as the signal)
