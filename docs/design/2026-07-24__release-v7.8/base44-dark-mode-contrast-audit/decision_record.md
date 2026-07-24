**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-24__release-v7.8
**Backlog source:** BLG-FE-125
**Maps to:** EPIC-04, ST-04

---

# Decision Record — Consolidated Dark-Mode Contrast Audit Across Base44-Generated Pages

## 1. Scope

Like EPIC-03 (`notification-accessibility-audit`), this is an audit-and-fix story. The design gate's role is to fix the **standard**, **scope**, and **filing method** so the audit can run during sprint execution without a further design round-trip.

**In scope:** every currently-shipped Base44-generated page under `docs/specs/frontend/pages/` (dark theme only — this audit does not re-check light theme, which has its own remediation history: `secondary-text-contrast` v6.7, `heading-light-theme-contrast` v7.0). Reference list at audit time: `analytics.md`, `dashboard.md`, `navigation.md`, `notifications.md`, `positions.md`, `pre_trade_research.md`, `red_flag_journal.md`, `reflections.md`, `reports.md`, `research_view.md`, `risk_dashboard.md`, `screener_morning_routine.md`, `screener_results.md`, `settings.md`, `signals.md`, `strategy_benchmark.md`, `system_status.md`, `ticker_universe.md`, `trade_history.md`, `trade_plan.md`, `trade_reflection.md`, `watchlist.md`, `weekly_digest.md` — i.e. all pages in `docs/specs/frontend/pages/`.

**Out of scope:** any page or component already covered by a dedicated, still-current dark-mode contrast fix this cycle or a prior one whose remediation is unchanged (e.g. dashboard's `heading-light-theme-contrast` v2.8 fix was dark-mode-safe already per that decision record — no re-audit needed for that specific element).

## 2. Standard Applied

Same WCAG 2.1 AA thresholds as EPIC-03 — no new contrast ratio invented for this story:
- Text/background contrast ≥4.5:1 (normal text), ≥3:1 (large text ≥18pt/24px or ≥14pt/18.66px bold), dark theme only
- Focus-indicator contrast ≥3:1 against adjacent colour (per `design_system.md` §Hover & Focus States v1.4, added this cycle for EPIC-03 — reused here rather than redefined)
- Icon-only controls checked per WCAG 1.4.11, consistent with the existing exemption note in `design_system.md` §Color Usage

This audit specifically checks for the **defect class already documented twice in this codebase** (`design_system.md` §Card Hierarchy: "this project has twice shipped a dark-only-token-on-light-theme contrast defect, `BLG-FE-87/88`, `BLG-FE-95`") — i.e. it is the dark-mode-equivalent sweep: any token that is light-theme-safe but has no (or an insufficient) `dark:` pairing.

## 3. Method

Head of UX & Design (or delegate) performs a systematic per-page pass across all pages listed in §1, dark theme only, checking every text/background and focus-indicator pairing against §2's thresholds. This is a manual review, consolidated into a single pass — not per-page ad hoc spot checks, per the story's own AC.

## 4. Filing Method (satisfies AC "one filing, not one per page")

All findings across all pages are collected into a **single consolidated backlog filing** (one `/backlog-add` covering the full findings list, grouped by page) rather than one item per page or per finding. Trivial findings (single class-token swap, no layout change) may still be fixed directly during sprint execution per the story's AC; the consolidated filing covers only the non-trivial remainder.

Audit method and per-page coverage (pass/fail/fixed) recorded in QA evidence for ST-04, per AC.

## 5. Compliance Check

No conflict with `strategy_rules.md §13` — purely visual/accessibility, no automated-decision or trading-parameter surface.

## 6. Sign-off

- **Head of UX & Design:** Approved — 2026-07-24 (standard, scope, method per §1–§3)
- **Product Owner:** Approved — 2026-07-24 (consolidated single-filing approach accepted, per §4)
