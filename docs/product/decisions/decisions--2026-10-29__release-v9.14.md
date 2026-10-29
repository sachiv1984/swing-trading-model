Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.14
Cycle: 2026-10-29__release-v9.14
Last Updated: 2026-10-29

## Planning Decisions — v9.14

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Use full capacity: fill to 28.00 of the 28.00-day ceiling of the confirmed ~24–28 day band | Explicit user instruction: "plan release v9.14. Use full capacity". | Product Owner (direct user instruction) | 2026-10-29 |
| Plan v9.14 without a scheduled rebalance | DL-087 named v9.14 and allowed skipping the even-count cadence advisory; the user invoked `plan release v9.14` directly. The last diagnostics (DL-086) are 2 releases old. | Product Owner (user invocation) | 2026-10-29 |
| Seat `BLG-OPS-193` (P1) as ST-01 | The only ready P1. Production GitHub Pages deploys have failed on every `main` push since 2026-10-15. | Release Planning Engine (Product Owner role) | 2026-10-29 |
| Seat `BLG-QA-238`, `BLG-GOV-397`, `BLG-GOV-398` ahead of the round-robin (§1.4c override) | v9.13 closure §6 row 6: v9.13's deferred lessons-learnt patches, targeted at the "v9.14 sprint". If v9.14 shipped without them, `roadmap_prompt.md` STEP -1.5 would classify them OVERDUE and halt the next rebalance. The override displaced `BLG-QA-220`, `BLG-OPS-190`, `BLG-SPEC-195` (0.80d). | Product Owner (user decision in session) | 2026-10-29 |
| Treat `BLG-OPS-85`, `BLG-OPS-21`, `BLG-FEAT-99` as ungated | §1.3a gating-item-shipped check, whole condition met: `BLG-OPS-74` (v6.8); PT-04 (v6.1) plus `BLG-OPS-18` (v9.13); `BLG-SPEC-186` (v9.13). No gate text edited (`BLG-GOV-398`, seated, adds the write-back path). | Release Planning Engine (Head of Specs Team role) | 2026-10-29 |
| Re-gate `BLG-FEAT-58` and `BLG-BE-43` on the same condition (§1.3a option (b)) | False-positive date lapse: ~2026-10-20 projected PO-02's own data precondition, not these gates' clearance. PO-02 has not entered sprint planning. Bounded edit under `ESC-CLOSE-20261007-01`. | Release Planning Engine (Head of Specs Team role) | 2026-10-29 |
| Count the 17 explicitly-ungated items (`Gate criteria: None`) in the ready pool | `BLG-GOV-390` (v9.13 ST-35) fixed the scan, so v9.13's comparability exclusion is retired. 18.50d enters the pool. | Release Planning Engine (Head of Specs Team role) | 2026-10-29 |
| Defer `BLG-TECH-21` (P2) despite P2-first ordering | Dedicated-release constraint in its own scope; `Provisional-Target: v10.0`. §1.4c override, as at v9.10–v9.13. | Release Planning Engine (Product Owner role) | 2026-10-29 |
| Exclude `BLG-GOV-142`, `BLG-GOV-360`, `BLG-SPEC-199`, `BLG-OPS-196`, `BLG-GOV-361`, `BLG-GOV-374` as done or resolved | Resolution banners, a ✅ COMPLETE banner, a met scope, or delivered (2026-10-16). Left for `groom backlog`. | Release Planning Engine (Head of Specs Team role) | 2026-10-29 |
| Raise 8 effort estimates under the STEP 4 calibration check, before selection | Production deploy and Render dashboard (`BLG-OPS-193`), an `ensure_*` sweep (`BLG-BE-166`), and 6 unselected items with live steps. The raises did not change the pick. | Release Planning Engine (Head of Specs Team role) | 2026-10-29 |
| Route `strategy_rules.md` edits through the standing case (c) rule | ST-03 (§4.2.1/§8.2, conditional on the ruling), ST-09 (§4.1.5 Known Deviations entry, §4.1.3 if ambiguous), ST-22 (§13.5 roster row). `ESC-CLOSE-20261029-02` replaced per-cycle rulings. ST-52 uses a companion document instead. | Release Planning Engine (Head of Specs Team role) | 2026-10-29 |
| Restate missing, stale or out-of-release-dependent ACs | No AC: `BLG-QA-93`, `BLG-OPS-105`, `BLG-SPEC-77`, `BLG-GOV-191`. Live sample now possible (`BLG-GOV-178`). Concrete report (`BLG-OPS-85`). Arc 1 baseline unconfirmed (`BLG-OPS-21`). Aligned with ST-04 (`BLG-BE-169`). §13 citations (`BLG-AI-20`, `BLG-AI-22`, `BLG-BE-163`, `BLG-GOV-186`). Each is marked *(restated)* in the slice. | Release Planning Engine (Head of Specs Team role) | 2026-10-29 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-01 first in the sprint | P1. Every frontend staging and production check needs a working build. | Head of Specs Team | 2026-10-29 |
| ST-02 → ST-03 → ST-06; ST-04 → ST-05 → ST-06; ST-07 → ST-08 | Shared regime and FX functions; ST-05 reuses ST-04's stored rate instead of adding a second mechanism; one stale-marker pattern. | Head of Specs Team | 2026-10-29 |
| ST-10 (EPIC-02) before ST-29 (EPIC-05) | ST-29's error-path scenario asserts ST-10's status codes. | Head of Specs Team | 2026-10-29 |
| ST-22 and ST-28 coordinate on `SystemStatus.js` and `system-status.spec.js` | Both edit them in different EPICs; the second to merge rebases. | Head of Specs Team | 2026-10-29 |
| ST-44 → ST-45; ST-51 → ST-48 | Both governance stories bump `OPERATIONAL_GUIDE.md` (CLAUDE.md §8 step 2a); ST-48 writes to the changelog section ST-51 adds. | Head of Specs Team | 2026-10-29 |
| RISK-02 case (c) confirmations recorded at the sprint planning seal | Three stories in three EPICs name `strategy_rules.md` sections; bumps are taken in merge order. | Head of Specs Team | 2026-10-29 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
