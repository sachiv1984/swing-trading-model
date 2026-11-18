**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-18__release-v9.18
**Stories:** ST-13 (BLG-FE-320) — EPIC-02

# Decision Record — Rules Followed / Rules Broken Filter

## 1. Scope of this record

ST-13 adds a computed "rules followed / rules broken" filter to Trade History. The metric definition belongs to the Metrics Definitions & Analytics Owner and is written in ST-13 before the build (slice sequencing). This record fixes the UI, the states and the data path the definition must fill.

Spec impact: `trade_history.md` v1.17 → v1.18 (new §Rules Filter). `metrics_definitions.md` and `trade_endpoints.md` are written in-story.

## 2. Data-source check

- `GET /trades` (`trade_endpoints.md`) returns `exit_reason` but **no rule-adherence field**. The pre-entry evidence is elsewhere:
  - `red_flag_events` (`event_type`, `ticker`, `position_id` nullable, `created_at`), which holds `pre_entry_override` events (proceeding over a WARN/FAIL; `strategy_rules.md` §4.2.6) and the other red-flag types.
  - `pre_entry_validation_log` (`ticker`, `market`, `rule_type`, `status`, `validated_at`) has **no position link**: it can only be joined by ticker and time.
  - `trade_history.position_id` links a closed trade to its position, so `red_flag_events.position_id` joins when it is set.
- **Decision:** the filter cannot be computed in the browser from `GET /trades`. ST-13 adds a server-computed field per trade to `GET /trades`: `rules_followed: true | false | null` and `rules_broken: string[]` (the reasons, e.g. `"pre_entry_override"`, `"manual_exit_before_stop"`, empty when followed). Contract, `openapi.yaml` and pytest in ST-13. The definition decides what counts; the UI only reads these two fields.
- **Third state is required.** Trades closed before the evidence existed (no `position_id`, or a `red_flag_events` row with null `position_id`, or pre-SI-01 dates) cannot be classified. They return `rules_followed: null` and show as "Not known", never as followed.

## 3. What the user sees

- **Filter control:** a segmented control in the Trade History filter bar, label "Rules", options "All" (default), "Followed", "Broken", "Not known". `data-testid="rules-filter"`. Combines with the existing ticker, tag, saved-filter and date filters (AND). Stored with saved filters like the other filters; not in the URL except as `?rules=followed|broken|unknown` when set.
- **Summary counts** above the table, for the trades the other filters leave: "{a} followed · {b} broken · {c} not known". Each number selects its option. `data-testid="rules-summary"`.
- **Row marker:** in the expanded row, a "Rules" line: "Followed" or "Broken: {reason labels}" or "Not known (no entry check recorded)". No colour-only signal; a broken trade's line uses `text-app-negative` with the word "Broken".
- **Journal red flags:** not changed in v9.18. The Journal Red flags tab already lists the events; adding the filter there adds nothing the tab does not show. Recorded as the "if useful" decision the scope asks for.
- **Empty filtered state:** "No trades match these filters." with "Clear filters" (the page's existing pattern).

## 4. Worked examples (fixture for the ST-13 Playwright test)

| Trade | Evidence | `rules_followed` | Shown under |
|-------|----------|------------------|-------------|
| A | position linked; checks passed; no red flags; stop exit | true | Followed |
| B | position linked; `pre_entry_override` event for its position | false | Broken |
| C | position linked; per definition, an exit the definition counts as off-rule | false | Broken |
| D | no `position_id` (legacy trade) | null | Not known |
| E | position linked; a red flag with `position_id` null for the same ticker the same day | per definition (ticker/time join or null); never silently "Followed" | as defined |

The definition's own worked examples (the metric owner's AC) cover row E and the exit reasons; this table fixes only that each state is reachable and filtered correctly.

## 5. §13

The field is a deterministic classification of recorded events, shown to the user about their own past trades. It makes no recommendation and changes no rule. No AI call. The labels "Followed"/"Broken" describe the record; they are not a score. No ranking.

## 6. Approvals

- Head of UX & Design: approved (agent-mediated, Design Gate Engine), 2026-11-18.
- Product Owner: approved (the user, in session, 2026-11-18).
- Metric definition: Metrics Definitions & Analytics Owner, in ST-13, before the build.
