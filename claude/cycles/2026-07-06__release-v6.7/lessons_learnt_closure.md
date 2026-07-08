Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-06__release-v6.7
Release: v6.7
Last Updated: 2026-07-08
Authority: Post-Ship Closure Engine v2.17

---

# Lessons Learnt — Closure Summary: v6.7

Reviewed by: PMO Lead
Date filed: 2026-07-08
Prior cycle checked: claude/cycles/2026-07-04__release-v6.6/lessons_learnt_closure.md

## Classification Summary

| Count | Category |
|-------|----------|
| 1 | Immediate (already resolved in-session during Sprint Execution; no prompt change needed, confirmed at closure) |
| 4 | Deferred (carried forward as Outstanding Actions) |
| 0 | Escalated |

---

## Action Classification Detail

### Immediate (1 — already resolved, confirmed this run)

| ID | Source | Summary | Disposition |
|----|--------|---------|-------------|
| IM-01 | Sprint Execution Phase 3 friction item 1 | Scripted dark/light-theme contrast transformation enumerated `src/pages/**` and `src/components/**` but initially missed 4 top-level `src/*.js` files, including `src/Layout.js` (the app shell, rendered on every page). Caught by agent-mediated DoQ review before Product Owner acceptance; fixed in-session (commit `184a26a3`), independently re-verified, full e2e suite re-run (429 passed, 0 failed). | No prompt change required — the sprint execution engine's own lessons learnt record classifies this as a one-off execution-methodology note, not a recurring governance gap. Confirmed resolved; no further action. |

### Deferred (4 — carried to next cycle or next relevant engine invocation)

| ID | Source | Summary | Owner | Target |
|----|--------|---------|-------|--------|
| LP-08 | Release Planning lessons_learnt.md | Provision an application `X-API-Key` in `~/.api_keys` (or equivalent) so governed routines can resolve the SI-02 trade-count gate directly instead of relying on self-reported counts. 2nd occurrence of this credential gap (first at `2026-07-06__scheduled` rebalance, same session-type). | PMO Lead / Infrastructure & Operations Owner | Before next SI-02 gate check is attempted |
| LP-09 | Release Planning lessons_learnt.md | The `2026-07-06__scheduled` rebalance's carry-forward misrouted the SI-02 structured-field patch (`current_roadmap.md` row + `roadmap_prompt.md` STEP 2.3) to `plan release v6.7`. `roadmap_prompt.md` is outside `release_planning_prompt.md`'s declared write scope — the patch correctly belongs to `run roadmap` or direct Head of Specs Team authority. | Head of Specs Team | Next `run roadmap` invocation |
| LP-10 | Release Planning lessons_learnt.md | Confirm `BLG-GOV-167`'s `.claude/skills/` write-scope grant (the first precedent of a backlog item granting standing write authority outside a routine's declared scope) was not extended beyond `.claude/skills/**` in practice. | Head of Specs Team | Next lifecycle audit |
| LP-11 | Sprint Execution Phase 3 friction item 2 | Adding a Tailwind `dark:` variant to a previously-bare class silently breaks any Playwright test using a literal bare-class CSS selector against that element (3 stale selectors found and fixed this cycle: `fee-drag-trade-history.spec.js`, `slippage-tracking.spec.js`, `research-typography.spec.js`). `execution_prompt.md` §3.1.A step 13's cross-spec selector-scan trigger wording ("modifies, replaces, removes, or renames a DOM element") does not obviously cover a same-element class-value change. Flagged for consideration, not applied this cycle — requires a judgment call on scan-trigger wording, not a mechanical fix. | Head of Specs Team | Next scheduled prompt review |

### Escalated (0)

None this cycle. No action item crossed the `lessons_learnt_prompt.md` §3.7 recurrence-escalation threshold — LP-08/LP-09/LP-10 are each newly surfaced or at a 2nd occurrence, not a 3-cycle carry.

---

## Closure-Phase Observations

- **Endpoint coverage drift check (STEP 6) found no new drift this cycle** — zero changes under `backend/routers/` or `docs/reference/openapi.yaml` this cycle (both EPICs were frontend-CSS-class and governance-documentation only). The pre-existing baseline gap (older endpoints not yet in `docs/ops/api_performance_baseline.md`) remains tracked via the already-open `BLG-OPS-13` (v2.8–v4.6) and `BLG-OPS-61` (v5.1–v5.4) — no new backlog item filed.
- **Specs Index TSG reconciliation (§7.3) found nothing to reconcile** — no pre-v6.7 open TSG items existed at cycle start (all resolved as of §34/v6.6); §35 added cleanly for v6.7 (0 gaps, both EPICs `not_applicable` or fully Playwright-covered).
- **`post_ship_closure.md` §7.3's reference to "§27 (Technical Specification Gaps)" is stale** — `Specs_Index.md` has no section by that literal name; the TSG reconciliation pattern actually lives inside each per-release "Test Coverage Gaps — vX.Y" section (see §33/§34/§35). This did not block STEP 7 — the reconciliation was performed against the correct §34/§35 pattern instead — but the cross-reference in `post_ship_closure.md` itself should be corrected to avoid future confusion. Not fixed this run (documentation-pointer fix, low urgency, no functional impact); flagged for the next `post_ship_closure.md` revision.
- **Scope and decisions documents for v6.7 were both cleanly located and superseded** — no "not found" flag needed this cycle, unlike some prior cycles.
- **No stale parked items found (IMP-15 check)** — no backlog items carry a `status: parked` marker in `backlog.md` at all currently.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | SI-02's trade-count gate condition remains formally unresolved for a 2nd consecutive governed-routine invocation (15 formally confirmed vs. 20 self-reported) due to no governed routine holding an application-level API key. | Roadmap/Release Planning should treat SI-02 as still gated until `LP-08` (credential provisioning) is resolved — do not accept a self-reported trade count as gate clearance. | Roadmap |
| 2 | `post_ship_closure.md` §7.3 cross-references a "§27 Technical Specification Gaps" section that no longer exists by that name in `Specs_Index.md` (superseded by the per-release "Test Coverage Gaps — vX.Y" section pattern, §9–§35). | Next `post_ship_closure.md` revision should correct the §7.3 cross-reference to point at "the most recent per-release Test Coverage Gaps section" rather than a fixed section number/name. | All |
