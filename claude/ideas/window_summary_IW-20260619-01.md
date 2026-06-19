**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-19
**Window:** IW-20260619-01

# Idea Intake Summary — IW-20260619-01

## Window Status: Closed

Opened: 2026-06-19 09:00 UTC
Closed: 2026-06-19 09:30 UTC
Mode: Standard
Trigger: Inline — roadmap STEP -1.6 (0 open ideas in register)

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|-----------------|--------------------|-------|
| Product Owner | 2 | 0 | 2 |
| Head of Specs Team | 2 | 0 | 2 |
| PMO Lead | 2 | 0 | 2 |
| Director of Quality | 2 | 0 | 2 |
| Strategy Rules & System Intent Owner | 2 | 0 | 2 |
| FinOps & Resource Architect | 2 | 0 | 2 |
| Infrastructure & Operations Owner | 2 | 0 | 2 |
| Facilitator | 0 | 0 | 0 |
| Challenger | 2 | 0 | 2 |
| **Total** | **16** | **0** | **16** |

## Agents Without Minimum Submissions

Facilitator — 0 submissions. Charter constraint: Facilitator role is structurally excluded from idea generation (non-decision process role). Standard mode — noted, no halt. Consistent with IW-20260610-01 treatment.

## Ideas Available for Roadmap STEP 4

| Idea ID | Agent | Title | Recommendation | Status |
|---------|-------|-------|----------------|--------|
| IDEA-product-owner-20260619-01 | Product Owner | Portfolio sector heat-map visualization | Now | Submitted |
| IDEA-product-owner-20260619-02 | Product Owner | Trade tagging and tag-based performance filtering | Soon | Submitted |
| IDEA-head-of-specs-20260619-01 | Head of Specs Team | Arc 4 API contract pre-authoring (PO-02/03/04) | Now | Submitted |
| IDEA-head-of-specs-20260619-02 | Head of Specs Team | Data model v3 pre-definition for Arc 4 journal intelligence | Now | Submitted |
| IDEA-pmo-lead-20260619-01 | PMO Lead | Automated governance health score computation script | Backlog | Submitted |
| IDEA-pmo-lead-20260619-02 | PMO Lead | Sprint velocity trend chart (last 10 cycles) | Backlog | Submitted |
| IDEA-director-of-quality-20260619-01 | Director of Quality | Arc 4 E2E test strategy pre-design (PO-02/03/04) | Now | Submitted |
| IDEA-director-of-quality-20260619-02 | Director of Quality | Automated accessibility testing (axe-core) in Playwright CI | Soon | Submitted |
| IDEA-strategy-owner-20260619-01 | Strategy Rules & System Intent Owner | §13 pre-assessment for Arc 4 AI features (PO-02/03) | Now | Submitted |
| IDEA-strategy-owner-20260619-02 | Strategy Rules & System Intent Owner | Formal strategy rules effectiveness review cadence | Soon | Submitted |
| IDEA-finops-20260619-01 | FinOps & Resource Architect | AI API cost model for Arc 4 journal intelligence features | Now | Submitted |
| IDEA-finops-20260619-02 | FinOps & Resource Architect | Alpaca API tier and cost optimization assessment | Backlog | Submitted |
| IDEA-infra-ops-20260619-01 | Infrastructure & Operations Owner | Database index audit for Arc 4 cross-table queries | Now | Submitted |
| IDEA-infra-ops-20260619-02 | Infrastructure & Operations Owner | Enhanced health check with external dependency verification | Soon | Submitted |
| IDEA-challenger-20260619-01 | Challenger | Data provider diversity risk assessment and failover strategy | Soon | Submitted |
| IDEA-challenger-20260619-02 | Challenger | Governance overhead ceiling metric and accountability mechanism | Soon | Submitted |

## Parked Ideas Carried Forward (Not Resubmitted)

None — register was empty at window open.

## Idea Summaries

**IDEA-product-owner-20260619-01 — Portfolio sector heat-map visualization**
Problem: The portfolio view shows positions as a list but gives no at-a-glance sense of sector concentration, lifecycle-state distribution, or heat distribution. A trader cannot quickly see "I'm overweight technology in GRACE state" without scanning each row.
Strategic alignment: §2 — captures momentum trends safely; a sector heat-map directly supports Arc 3 position concentration awareness and Arc 6 regime-conditional performance.
Solution: A visual grid (sector × lifecycle state) showing heat % per cell. Deterministic display of existing data — no new calculations required beyond DS-03 sector data and existing heat calculations. §13 COMPLIANT.
Expected value: Reduces time to identify concentration risk from minutes to seconds; supports IT-05 (concentration limits) with visual complement.
Effort: Medium (frontend only; backend data exists).
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Now.

**IDEA-product-owner-20260619-02 — Trade tagging and tag-based performance filtering**
Problem: The only categorization available for trades is setup_type (6 options). Traders often want to track their own situational labels (e.g., "earnings play", "sector rotation", "high conviction") and analyze win rates by those custom labels.
Strategic alignment: §2 intent 4 — "defend profits aggressively once momentum is confirmed" requires knowing which setups produce the most reliable momentum.
Solution: Optional tag field on trade entry/edit. Tag management page. Performance analytics breakdowns by tag group. §13 COMPLIANT — deterministic filter on user-defined labels, no prediction.
Expected value: Enables self-directed pattern discovery beyond the 6 pre-set setup types; enriches PO-02 Journal Pattern Recognition data foundation.
Effort: Medium.
Reversibility: Mostly reversible (tag data stays but feature can be disabled).
Stop: No view — leave to debate.
Recommendation: Soon.

**IDEA-head-of-specs-20260619-01 — Arc 4 API contract pre-authoring (PO-02/03/04)**
Problem: PO-02 (Journal Pattern Recognition), PO-03 (Behavioural Error Taxonomy), and PO-04 (Reflection ↔ Outcome Correlation) will reach gate clearance within ~3–6 months. When they enter sprint, there are currently zero API contracts for these features. Pre-authoring now reduces spec debt at implementation time.
Strategic alignment: §2 (strategy intent — plan vs reality foundation) + governance effectiveness (reducing BLG-SPEC debt at delivery).
Solution: Author v0.1.0 API contracts for 3 new endpoints: GET /analytics/journal-patterns, GET /trades/{id}/error-taxonomy, GET /analytics/reflection-outcome-correlation. Indicative only at this stage.
Expected value: Eliminates predictable spec debt at Arc 4 implementation; reduces sprint planning preparation time.
Effort: Small (documentation only).
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Now.

**IDEA-head-of-specs-20260619-02 — Data model v3 pre-definition for Arc 4 journal intelligence**
Problem: PO-02 and PO-03 require new database columns: pattern_tags[], error_taxonomy_label, error_taxonomy_confidence, reflection_depth_score. Without a pre-defined schema, implementation sprint will encounter schema design debates under delivery pressure.
Strategic alignment: §2 intent — data density for feedback loop; pre-planned schema reduces execution risk.
Solution: Extend arc4_data_requirements.md to include concrete column definitions, indexes, and migration stubs for PO-02/03. No code changes — documentation only.
Expected value: Reduces Arc 4 sprint planning time; prevents mid-sprint schema pivots.
Effort: Small.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Now.

**IDEA-pmo-lead-20260619-01 — Automated governance health score computation script**
Problem: The governance health score (OPERATIONAL_GUIDE §15) is computed manually at each roadmap rebalance. This involves checking header compliance, deferred patch counts, and open escalations across multiple files — toil that could be scripted.
Strategic alignment: §2 governance effectiveness (not directly strategy-bounded, but reduces governance cycle overhead).
Solution: Python script `claude/audit.py` extension (or standalone `claude/governance_health.py`) that reads the active cycle, counts compliant headers, checks deferred patch status, and outputs the three §15 metrics. Output format matching run_manifest.md §-1.7 section.
Expected value: Saves 5–10 minutes per rebalance; reduces risk of missed header compliance issues.
Effort: Small–Medium.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Backlog.

**IDEA-pmo-lead-20260619-02 — Sprint velocity trend chart (last 10 cycles)**
Problem: velocity_metrics.md exists but is a flat text file. There's no visual representation of velocity trends over time. A cycle-to-cycle velocity chart would help identify cadence acceleration or deceleration and inform sprint capacity planning.
Strategic alignment: §2 governance effectiveness; planning visibility.
Solution: Add a velocity trend section to the governance dashboard (if one exists) or generate a markdown table with sparkline-style ASCII trend in velocity_metrics.md. If UI investment is warranted, a lightweight chart component on a governance page.
Expected value: Makes sprint pacing visible at a glance; supports capacity planning at sprint planning.
Effort: Small.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Backlog.

**IDEA-director-of-quality-20260619-01 — Arc 4 E2E test strategy pre-design (PO-02/03/04)**
Problem: PO-01 Plan vs Reality has Playwright coverage. PO-02/03/04 have no test strategy defined. When these features reach implementation gate, test design under sprint pressure leads to coverage gaps and deferred Playwright scenarios (recurring pattern across v4.x–v5.x cycles).
Strategic alignment: §2 governance quality; DoQ charter — testing strategy must precede implementation.
Solution: Author a test strategy document for Arc 4 remaining features: define E2E scenarios (10–15 per feature), identify mock/real-data requirements, define coverage acceptance criteria. Output: arc4_test_strategy.md.
Expected value: Eliminates reactive test design during delivery; reduces post-ship QA deviations.
Effort: Small.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Now.

**IDEA-director-of-quality-20260619-02 — Automated accessibility testing (axe-core) in Playwright CI**
Problem: No accessibility testing exists in the CI pipeline. As the UI grows (RFJ redesign, Arc 4 views), WCAG violations may accumulate without visibility. The current QA coverage matrix has no accessibility dimension.
Strategic alignment: §2 product quality (broader strategic value than pure §strategy_rules.md reference, but aligns with quality mandate).
Solution: Integrate axe-core with existing Playwright test suite. Add 1–2 accessibility checks to key page entry points (dashboard, positions, screener, analytics). Fail CI on any critical axe violations. Document threshold.
Expected value: Catches WCAG violations before production; reduces risk of usability regression as UI complexity grows.
Effort: Small.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Soon.

**IDEA-strategy-owner-20260619-01 — §13 pre-assessment for Arc 4 AI features (PO-02/03)**
Problem: PO-02 (Journal Pattern Recognition) uses Claude API to analyze patterns across journal entries. PO-03 (Behavioural Error Taxonomy) auto-classifies journal entries. Both use AI analysis that may approach the §13 "prediction" boundary. No §13 review exists for these features yet.
Strategic alignment: §13 boundary compliance — deterministic system vs prediction system boundary. §3 human-in-the-loop mandate.
Solution: Conduct formal §13 pre-assessment for PO-02 and PO-03. Document binding conditions (similar to IT-06, SI-01, SI-04 assessments). Output: decisions document per established pattern.
Expected value: Prevents last-minute scope changes when features enter sprint; establishes binding conditions before implementation commits.
Effort: Small (documentation/assessment — no code).
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Now.

**IDEA-strategy-owner-20260619-02 — Formal strategy rules effectiveness review cadence**
Problem: strategy_rules.md v1.4 has been in force since 2026-05-20 (4 weeks). With ~13 closed trades, some data exists to assess whether the ATR multipliers, grace period lengths, and regime gate parameters are producing intended outcomes. No formal review cadence exists.
Strategic alignment: §2 strategy intent (non-negotiable) — the intent must remain stable, but parameter effectiveness should be assessable.
Solution: Define a formal cadence for strategy rules effectiveness review (e.g., every 6 months, or after 25/50 closed trades). Review scope: parameter effectiveness vs stated intent only — not changes to intent. Output: a review protocol document.
Expected value: Creates structured mechanism for evidence-based strategy parameter refinement; prevents strategy drift without governance.
Effort: Small.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Soon.

**IDEA-finops-20260619-01 — AI API cost model for Arc 4 journal intelligence features**
Problem: Current Claude API usage is $0.05–$0.15/month (largely AI thesis generation). PO-02 (Journal Pattern Recognition) will run cross-trade analysis across potentially 50–200 journal entries per call. The cost envelope is unknown and could be 10–50× higher than current usage.
Strategic alignment: §2 cost governance; FinOps mandate — cost envelopes must be modelled before feature activation.
Solution: Model projected token counts (input: journal entries + context, output: pattern summary) for PO-02 and PO-03 at 50/100/200 trade history depth. Set cost alert thresholds. Define max-per-call token budget. Output: Arc 4 AI cost envelope document.
Expected value: Prevents cost surprise at PO-02 activation; enables informed go/no-go decision.
Effort: Small.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Now.

**IDEA-finops-20260619-02 — Alpaca API tier and cost optimization assessment**
Problem: Alpaca Markets is used for US OHLCV data and paper trading. The current API tier was selected when Arc 1 was being built. With 6+ months of usage data, it's worth assessing whether the current tier matches actual usage or if a different tier (higher or lower) would be more cost-effective.
Strategic alignment: §2 infrastructure cost (FinOps mandate); §13 COMPLIANT — data provider assessment, no functional change.
Solution: Pull Alpaca API usage metrics (request count, data volume, API call distribution). Compare against tier limits. Assess cost vs alternative tiers or alternative US market data providers.
Expected value: Potential cost reduction or confirmation that current tier is appropriate.
Effort: Small.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Backlog.

**IDEA-infra-ops-20260619-01 — Database index audit for Arc 4 cross-table queries**
Problem: PO-02 (Journal Pattern Recognition) and PO-03 (Behavioural Error Taxonomy) will execute complex queries: JOIN across trade_history, trade_plans, and journal_entries with pattern aggregation. The existing api_performance_baseline.md covers v5.3 endpoints. No index analysis exists for the Arc 4 query patterns.
Strategic alignment: §2 technical quality; infrastructure mandate — performance baselines must be established before feature activation.
Solution: Analyse planned PO-02/03 query patterns. Assess existing indexes (current schema). Identify missing indexes needed for <2s p99 on 50/100 trade history depth. Output: arc4_db_index_assessment.md.
Expected value: Prevents performance regressions at Arc 4 activation; reduces risk of costly post-ship index migrations.
Effort: Small.
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Now.

**IDEA-infra-ops-20260619-02 — Enhanced health check with external dependency verification**
Problem: The current GET /health endpoint confirms the backend is running and the database is reachable. It does not verify external dependencies: Alpaca API reachability, Yahoo Finance connectivity, Telegram bot token validity, Claude API key status. Failures in these dependencies are invisible until a user experiences them.
Strategic alignment: §2 operational reliability; infrastructure mandate — external dependencies should be monitored.
Solution: Extend GET /health with an optional deep-check mode: `GET /health?deep=true` that tests each external API (ping only, no data fetch). Return per-dependency status. Add to System Status page as "External Dependencies" section.
Expected value: Surfaces external API failures before users encounter them; reduces MTTR for Alpaca/Yahoo/Telegram incidents.
Effort: Medium (backend + frontend).
Reversibility: Mostly reversible.
Stop: No view — leave to debate.
Recommendation: Soon.

**IDEA-challenger-20260619-01 — Data provider diversity risk assessment and failover strategy**
Problem: The system has two single points of failure: Yahoo Finance (UK stocks — crumb/401 issue in v3.9 demonstrated fragility) and Alpaca (US stocks and paper trading). No failover strategy exists. A Yahoo Finance API deprecation or Alpaca pricing change would break significant functionality.
Strategic alignment: §2 intent 2 — "avoid premature exits caused by early volatility" applies to data availability too. §13 boundary: data provider change is within bounds provided strategy rules are preserved.
Solution: Formal assessment of alternative data providers per market leg (UK: Refinitiv, EOD Historical Data, MarketStack; US: Polygon.io, IEX Cloud). Define failover decision criteria and the minimum viable switch path for each market. Not an immediate implementation — a risk document and contingency plan.
Expected value: Reduces operational risk from single provider dependency; informs future provider selection decisions.
Effort: Small (assessment only).
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Soon.

**IDEA-challenger-20260619-02 — Governance overhead ceiling metric and accountability mechanism**
Problem: STEP 2.4 Product Value Ratio Diagnostic now tracks U/G/D/P story ratios. The last 5 cycles show significant governance/debt load. However, there is no governance-level commitment to a ceiling — the STEP 7.1 Skill-Silo Alert (40% ceiling) fires but is advisory to the PO. A stronger accountability mechanism for governance overhead is needed.
Strategic alignment: §2 strategic effectiveness — governance overhead is not explicitly in strategy_rules.md, but the system's value delivery depends on product features reaching users. A non-binding ceiling without enforcement creates systematic governance inflation risk.
Solution: Define a "governance overhead budget": if G+D+P stories > 50% of total in any 3-cycle rolling window, require a written PO rationale explaining why product value delivery is being deferred, stored in claude/cycles/<cycle_id>/governance_budget_statement.md. This creates a documented record but does not block delivery.
Expected value: Creates accountability without halting governance work; makes governance overhead a first-class tracked metric.
Effort: Small (governance process only).
Reversibility: Fully reversible.
Stop: No view — leave to debate.
Recommendation: Soon.

## Notes

- Backlog scope advisory (STEP 2.0, step 5): All submissions checked against known backlog themes. IDEA-head-of-specs-20260619-01 may overlap with prior BLG-SPEC items; noted in submission. All others appear to be net-new scope not currently tracked. Non-blocking advisory only.
- STEP 4.3 Innovation debt: All 8 submitting agents met the 2-submission minimum. Facilitator structural exclusion recorded; no innovation debt for Facilitator specifically.
- 16 ideas advancing to STEP 4 of roadmap rebalance.
