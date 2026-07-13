Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-13

# QA Evidence — EPIC-01 (Positions Grid View Parity)

**Cycle:** 2026-07-12__release-v7.0
**Sprint goal:** Close the Grid View/Table View position-risk badge and trailing-stop parity gap, resolve the v6.9-carried spec-reconciliation and data-correctness debt, and ship three new reporting and position-review features.

---

## ST-01 — positions.md Grid View badge placement subsection (BLG-SPEC-80)

**Spec reference:** `docs/specs/frontend/pages/positions.md#Alerts Column`
**Commit:** f5c0962c
**What was built:** Added an explicit "Grid View badge placement" paragraph to §Alerts Column documenting the dedicated alert row (below header, above stat tiles) where RISK OFF/GAP RISK badges render in Grid View. Version bumped 2.2→2.3.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| `positions.md` updated with an explicit Grid View badge-placement subsection | Pass |
| `BLG-FE-102` implementation can cite the spec directly | Pass — ST-02 implementation matches the subsection exactly |

**Deviations:** None

---

## ST-02 — Positions Grid View missing RISK OFF badge (BLG-FE-102)

**Spec reference:** `docs/specs/frontend/pages/positions.md#Alerts Column`
**Commit:** 2d4eaa57
**What was built:** Added `RiskOffCardBadge` to `PositionCard.js`, rendered in a new dedicated alert row (`PositionCardAlertsRow`) when `position.risk_off_exit === true`. Deep blue `#1E40AF` background, "RISK OFF" label, `data-testid="risk-off-badge"`.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| Grid View position cards show a RISK OFF badge when `risk_off_exit = true`, matching Table View's condition logic | Pass — same `position.risk_off_exit === true` condition as Table View's `AlertsCell` |
| Visual treatment matches spec (deep blue `#1E40AF`, "RISK OFF" label) | Pass |
| Badge coexists cleanly with the GAP RISK badge when both apply | Pass — both render in `PositionCardAlertsRow`, stacked |
| No change to Table View behaviour | Pass — `Positions.js` untouched by this story |

**Test scenarios:** `tests/e2e/epic01-v70-grid-badge-parity.spec.js` SC-GVP-01, SC-GVP-02, SC-GVP-03 (all passing, verified locally)

**Deviations:** None for this story. (See ST-05 for a related pre-existing Table View deviation discovered during this work — not introduced by ST-02.)

---

## ST-03 — Positions Grid View missing trailing-stop value and breach indicator (BLG-FE-97)

**Spec reference:** `docs/specs/frontend/pages/positions.md#Trailing Stop Column`
**Commit:** 2d4eaa57
**What was built:** Restructured the card's third stat tile to show "Init: {currency}{initial_stop}" subtext plus the trailing stop value, with an `AlertTriangle` icon (orange `#EA580C`) shown inline when breached — using the same breach condition as Table View (`current_price <= current_trailing_stop`, guarded by `trailStop > 0`).

**Acceptance criteria:**
| AC | Result |
|----|--------|
| Grid View position cards show both Initial Stop and current trailing stop values | Pass |
| Breach state shown via icon only (not a full badge/pill), matching Table View's breach condition logic | Pass — `AlertTriangle` icon only, same condition as `Positions.js` |
| No change to Table View behaviour | Pass — verified via SC-GVP-09 regression check |

**Test scenarios:** `tests/e2e/epic01-v70-grid-badge-parity.spec.js` SC-GVP-06, SC-GVP-07, SC-GVP-08, SC-GVP-09 (all passing, verified locally)

**Deviations:** None

---

## ST-04 — Positions Grid View badge parity Playwright coverage (BLG-QA-95)

**Spec reference:** N/A (test-authoring — the test file itself is the deliverable, Case C per execution_prompt.md STEP 3.1.A)
**Commit:** 19d2d5ba
**What was built:** `tests/e2e/epic01-v70-grid-badge-parity.spec.js` — 9 scenarios (SC-GVP-01 through SC-GVP-09) covering RISK OFF badge, GAP RISK badge, combined stacking, trailing-stop value, and breach icon in Grid View, plus a Table View regression check. Full parity with existing Table View `SC-RO-*`/`SC-TS-*`/`SC-GR-*` coverage.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| Grid View badge scenarios pass in CI for both RISK OFF and GAP RISK badge types | Pass — verified locally, 9/9 passing |
| Parity with existing `SC-RO-*` Table View coverage confirmed | Pass — same conditions, same fixtures pattern, Table View regression re-run (24/24 existing tests still passing) |

**Deviations:** None

---

## ST-05 — GAP RISK / RISK OFF combined-badge visual differentiation review (BLG-FE-104)

**Spec reference:** `docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md`, `docs/specs/frontend/pages/positions.md#Alerts Column`
**Commit:** (documentation only — no code change required for the stacking rule itself, already correctly implemented by ST-02/ST-03; see finding below)
**What was built:** Reviewed the combined/stacked badge state per the design decision record. Confirmed:
- Grid View (`PositionCardAlertsRow`, built in ST-02): RISK OFF renders above GAP RISK, `gap-1` (4px) vertical spacing, no truncation — matches decision record exactly.
- Table View (`AlertsCell`, pre-existing): already stacks RISK OFF above GAP RISK in a `flex-col gap-1` container — already compliant with the stacking/order rule, no change needed.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| Combined-badge state reviewed and confirmed distinguishable, or a fix is specified and implemented | Pass with notes — stacking/order/spacing confirmed distinguishable in both views (Grid View newly built to match, Table View already compliant). One related finding below required a deviation record rather than an in-scope fix. |

**Finding (DEV-EPIC01-ST05-01):** While verifying Table View's stacking compliance, discovered the Table View RISK OFF badge's own colour/label does not match the canonical spec independent of the stacking review — see deviation below. This does not invalidate the *stacking* confirmation (order and spacing are correct in both views), but it does mean the combined-badge decision record's stated "hue separation" rationale (blue-800 vs amber-600) does not hold for Table View as shipped (both badges are amber there). Grid View is unaffected — it was built fresh this sprint using the correct spec colour.

### DEV-EPIC01-ST05-01
**Priority:** P2
**Story:** ST-05
**AC:** positions.md §Alerts Column — Risk-Off Badge: Label "RISK OFF", Background `#1E40AF` (blue-800)
**Expected:** Table View's RISK OFF badge renders with label "RISK OFF" and background `#1E40AF` (blue-800), per canonical spec.
**Actual:** `src/pages/Positions.js` `AlertsCell` component renders the badge with `bg-amber-900/60 text-amber-300` (amber, not blue), label text "Risk-Off" (not "RISK OFF"), plus a `ShieldAlert` icon not mentioned in spec. Confirmed pre-existing since v6.2 — the existing passing test `SC-RO-02` (`tests/e2e/epic01-v62-stops-alerts.spec.js`) explicitly asserts this amber styling as expected/correct.
**Impact:** Undermines the combined-badge decision record's stated hue-separation rationale for Table View specifically (both RISK OFF and GAP RISK render in the amber family there — `bg-amber-900` vs `#D97706` — rather than the intended blue-vs-amber separation). Badges remain distinguishable today via icon presence, label text, and shade difference, so this is not a blocking safety gap, but it is a genuine, longstanding spec/implementation divergence that should be resolved deliberately (either bring Table View into spec compliance, or update the canonical spec to document amber as the accepted Table View treatment) rather than left silently inconsistent with the newly-built, spec-compliant Grid View badge.
**Backlog action:** BLG-FE-107 filed (see below) — out of scope to fix within EPIC-01/ST-05: `Positions.js` is owned by EPIC-02 in this cycle's Merge Order plan, and any colour fix must also update `SC-RO-02`'s current amber assertion plus receive its own design-gate-scoped UX decision (standardize to spec-blue vs. update the spec to accept amber).

**Deviations filed:** DEV-EPIC01-ST05-01 (P2, backlog item BLG-FE-107 filed for follow-up)

---
