**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-14
**Approved by:** Product Owner — 2026-07-14
**Story:** ST-03 — Table View RISK OFF badge colour/label spec compliance (BLG-FE-107)
**Cycle:** 2026-07-14__release-v7.1

---

# UX Decision Record — Table View RISK OFF Badge Spec Compliance

## 1. Question

`positions.md` §Alerts Column specifies the RISK OFF badge as Label "RISK OFF", Background `#1E40AF` (blue-800). The shipped Table View (`AlertsCell`) instead renders amber (`bg-amber-900/60 text-amber-300`), label "Risk-Off", plus an unspecified `ShieldAlert` icon — pre-existing since v6.2, encoded as expected by `SC-RO-02`. The v7.0 Grid View RISK OFF badge (ST-02) correctly ships the spec's blue. ST-03 (`DEV-EPIC01-ST05-01`) asks the design gate to resolve which side is canonical: (a) fix Table View to match spec, or (b) accept amber as canonical and update the spec plus the combined-badge decision record.

## 2. Review Findings

- The blue-vs-amber hue separation is not cosmetic — it is the safety rationale documented in `docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md` (2026-07-12) for letting a user tell RISK OFF (regime-level exit signal) apart from GAP RISK (earnings/weekend-hold flag) at a glance when the two badges stack in the same cell. That review explicitly relied on RISK OFF being blue-800 and GAP RISK being amber-600 as two non-adjacent hue families.
- Accepting amber as canonical for Table View (option b) would put both RISK OFF and GAP RISK in the same amber family in Table View specifically, directly invalidating the hue-separation finding that review already signed off on — while Grid View would remain blue/amber, producing a second, new inconsistency between views instead of resolving the existing one.
- Table View and Grid View share the same data source (`risk_off_exit`) and, per §Alerts Column's Grid View badge-placement note (v7.0 — ST-01), are already specified to use "same visual treatment (colour, label, pill shape) as Table View — no Grid-View-specific styling variant." Grid View already complies. Making Table View match Grid View is the smaller, lower-risk change, and requires no spec rewrite — `positions.md` §Alerts Column's Risk-Off Badge table has been correct since v6.2; only the Table View implementation drifted from it.
- The extra `ShieldAlert` icon in the shipped Table View has no spec basis in either the Risk-Off Badge or Gap Risk Badge tables (both specify text-label pills, no icon) and is dropped along with the colour/label fix, bringing Table View to full parity with the specified/Grid-View pattern.

## 3. Decision

**Option (a): bring Table View into spec compliance.** `positions.md` §Alerts Column is confirmed correct and unchanged — no spec edit required. Table View's `AlertsCell` must be changed to match: Background `#1E40AF` (blue-800), label "RISK OFF" (not "Risk-Off"), no icon. `SC-RO-02` (`tests/e2e/epic01-v62-stops-alerts.spec.js`) must be updated in the same commit to assert the spec-correct blue/label instead of the amber values it currently encodes as expected. `DEV-EPIC01-ST05-01` closes on merge — resolution: spec was correct, implementation is being corrected to match.

This also restores the precondition the combined-badge differentiation review already relied on: after this fix, `SC-GVP-02` (Grid View parity) and `SC-RO-02` (Table View) assert the same blue-800 RISK OFF value, and the v7.0 hue-separation finding holds for both views as originally reviewed.

## 4. §13 Compliance

Display-only colour/label correction to an existing alert badge. No new automation, no new data source. Not in scope for §13 review.

## 5. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-14
- **Product Owner:** Approved — 2026-07-14
