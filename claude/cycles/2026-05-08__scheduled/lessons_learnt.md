**Owner:** PMO Lead
**Class:** Governance Artefact (Class 3)
**Status:** Published
**Cycle:** 2026-05-08__scheduled

# Lessons Learnt — Roadmap Rebalance 2026-05-08__scheduled

## Outstanding Actions

None.

## Deferred Patches

None. Meta-review concluded no prompt patches warranted.

## Friction Items

### F-01 (Type C) — Register integrity: park counts not incremented for STEP 5 parked ideas

**Description:** Two ideas parked at STEP 5 in the 2026-05-05 cycle (IDEA-finops-20260421-01, IDEA-cybersecurity-20260421-02) had their park counts not incremented in ideas_register.md. This was identified at STEP 4 gate-condition re-check in this cycle when park counts appeared inconsistent with the STEP 5 debate record.

**Impact:** Minor — park counts were 1 cycle behind actual. Both ideas were correctly re-parked in the prior cycle; only the register counter was wrong. Corrected in this cycle.

**Root cause:** Context compression during the prior cycle's register write pass caused the STEP 5-parked idea rows to be omitted from the register update.

**Corrective action:** Register integrity corrections applied in STEP 4 of this cycle. Park counts corrected +1 for both ideas before the current-cycle park increment was applied.

**Process improvement:** When writing the ideas_register.md in future cycles, explicitly verify that STEP 5 parked ideas (not just promoted ideas) have their park counts incremented. The STEP 5 park write is a distinct register update from the STEP 4 promoted-idea write.

## Process Notes

- IW-20260508-01 generated correctly via STEP -1.6 auto-trigger (17 open ideas < 20 threshold)
- All 22 eligible agents submitted (Facilitator charter-excluded as expected)
- Meta-review conducted — clean outcome, no prompt patches
- 4 Challenger Type A counter-arguments productively challenged and resolved by PO
