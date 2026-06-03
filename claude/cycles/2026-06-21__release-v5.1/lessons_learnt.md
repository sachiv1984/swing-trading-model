**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-06-21__release-v5.1
**Phase:** Release Planning
**Published:** 2026-06-21

---

# Lessons Learnt — Release Planning — v5.1

## Observations

### LL-RP-v5.1-01 — STEP 8.1 Option(b) creates §-1.2 ambiguity

**Type:** Process  
**Severity:** Advisory  
**Pattern:** When the roadmap rebalance uses STEP 8.1 Option(b) ("defer with written rationale"), the roadmap does not contain a formal `## vX.Y` section. The release planning engine's §-1.2 hard gate checks for a "planned release section." This creates a literal-vs-intent gap: the PO intent is unambiguous (roadmap metadata explicitly states "plan release v5.1 is next step") but the §-1.2 gate fires.  
**Disposition:** Proceeded under advisory — PO STEP 8.1 decision recorded in roadmap metadata is the authorizing document; release planning added the formal v5.1 section at STEP 5. No escalation required.  
**Action:** Consider whether §-1.2 should explicitly accommodate STEP 8.1 Option(b) decisions (e.g., "OR documented in roadmap metadata as a STEP 8.1 PO decision") to prevent this advisory recurring.  
**Action classification:** Deferred — not urgent; process works correctly with the current interpretation; may be addressed at next prompt review cycle.

### LL-RP-v5.1-02 — SI-05 Phase 1 gate aligns exactly with release date

**Type:** Observation  
**Severity:** Advisory  
**Pattern:** The SI-05 Phase 1 gate (SI-01 + SI-03 live ≥ 30 days) clears on exactly the same date as the `--date` parameter (2026-06-21). This means the gate cannot be confirmed until the same day release planning runs. Sprint planning should verify gate confirmation explicitly (PMO Lead production check) rather than relying on the date calculation alone.  
**Disposition:** Risk noted (RISK-01); ST-01 AC-08 requires PMO Lead gate confirmation at sprint planning.  
**Action:** None — correct handling already in place via AC-08.

## Carry-Forward Items

| # | Observation | Action | Engine | Target |
|---|-------------|--------|--------|--------|
| 1 | BLG-FE-61 recurrence pattern (3 consecutive sprints) resolved by promoting to firm scope | Monitor for recurrence — if Playwright coverage gaps recur again in v5.2, consider sprint planning hard gate | Sprint Planning | v5.2 monitor |
| 2 | STEP 8.1 Option(b) §-1.2 advisory (LL-RP-v5.1-01) — consider formal §-1.2 accommodation | Head of Specs Team to assess at next prompt review | Release Planning | v5.2+ prompt review |

```json
// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-06-21__release-v5.1",
  "release": "v5.1",
  "lessons_count": 2,
  "carry_forward_count": 2,
  "action_now_count": 0,
  "deferred_count": 1,
  "published_utc": "2026-06-21T00:14:00Z"
}
```
