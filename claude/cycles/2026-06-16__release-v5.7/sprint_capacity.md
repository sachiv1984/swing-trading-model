**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-16
**Cycle:** 2026-06-16__release-v5.7

---

# Sprint Capacity — v5.7

---

## 1. Capacity Inputs

```
Sprint duration:    Continuous (solo-dev; no fixed day timebox)
Available FTE:      1 (solo-dev — engine + human for delegated items)
Total capacity:     Solo-dev sprint; stories sized XS–S
Skill constraints:  Production environment access required for EPIC-01 staging items
                    Mobile device + Telegram access required for ST-05
```

Source: `release_plan.md ## Capacity Check` — verdict PASS.

---

## 2. Item Effort Mapping

### Sprint 1

#### EPIC-01 — Staging Verification & QA Coverage

| Story | Title | Effort Band | Effort Hours (est.) |
|-------|-------|------------|---------------------|
| ST-01 | Staging verification — concentration-status p95 | XS | <1 hr |
| ST-02 | Staging verification — red-flag-journal p95 | XS | <1 hr |
| ST-03 | Staging verification — behavioural-drift p95 + cache | XS | <1 hr |
| ST-04 | Staging verification — research view p95 + cache | S | ~2–3 hrs |
| ST-05 | Staging verification — SI-05 deep links mobile Telegram | XS | <1 hr |
| ST-06 | SI-01 all-pass state Playwright scenario | XS | <1 hr |
| ST-07 | SI-03 Red Flag Journal pagination Playwright | XS | <1 hr |
| ST-08 | Arc 5 compliance score trend Playwright | XS | <1 hr |
| **EPIC-01 subtotal** | | | **~5–9 hrs** |

#### EPIC-02 — Governance & Engineering Patches

| Story | Title | Effort Band | Effort Hours (est.) |
|-------|-------|------------|---------------------|
| ST-09 | BLG-FE-64 RFJ design review pre-brief [CONDITIONAL] | XS | ~1 hr |
| ST-10 | Lazy-import pattern documentation | S | ~1–2 hrs |
| ST-11 | Confirm dual sign-off pattern in execution_prompt | S | ~0.5–1 hr |
| **EPIC-02 subtotal** | | | **~2.5–4 hrs** |

**Sprint 1 total: ~7.5–13 hrs. Well within solo-dev sprint capacity.**

### Sprint 2 (Conditional — gate 2026-07-04)

#### EPIC-03 — SI-05 Effectiveness Review & Post-Deploy Metrics

| Story | Title | Effort Band | Effort Hours (est.) |
|-------|-------|------------|---------------------|
| ST-12 | SI-05 digest weekly cadence review | S | ~0.5 day |
| ST-13 | SI-05 actionability metric definition | S | ~0.5 day |
| ST-14 | SI-05 service production p99 latency baseline review | S | ~0.5 day |
| **EPIC-03 subtotal** | | | **~3–4.5 hrs** |

---

## 3. Total Effort vs Capacity

| Sprint | Stories | Est. Effort | Capacity Verdict |
|--------|---------|------------|-----------------|
| Sprint 1 | 11 (10 firm + 1 conditional) | ~7.5–13 hrs | PASS |
| Sprint 2 | 3 (all conditional) | ~3–4.5 hrs | PASS (if gate clears) |

No over-allocation. Capacity verdict: **PASS**.

---

## 4. Conditional (Deferred) Items

| EPIC | Story | Effort Band | Gate Condition |
|------|-------|------------|----------------|
| EPIC-02 | ST-09 | XS | SI-03 Red Flag Journal live ≥30 days; gate clears 2026-06-21 |
| EPIC-03 | ST-12 | S | SI-05 effectiveness review complete; gate 2026-07-04 |
| EPIC-03 | ST-13 | S | SI-05 effectiveness review complete; gate 2026-07-04 |
| EPIC-03 | ST-14 | S | ≥4 weeks production operation; gate 2026-07-04 |

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-16__release-v5.7 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

*Note: ST-09 and EPIC-03 items are already in scope and marked conditional. Gate re-invocation is only required if new out-of-slice items need to be added. ST-09's gate clearing on 2026-06-21 does not require an amendment — the story is already in the sealed backlog as conditional and becomes ready on that date.*
