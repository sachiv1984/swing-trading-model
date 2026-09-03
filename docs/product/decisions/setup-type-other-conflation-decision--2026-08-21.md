**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-21
**BLG-ID:** BLG-FEAT-93
**Story:** ST-07
**Cycle:** 2026-08-21__release-v9.0

---

# `trade_plans.setup_type = "Other"` Conflation — Accept-As-Is Decision

**Decision date:** 2026-08-21
**Resolves:** `ESC-EXEC-20260821-02`

---

## Background

`ST-13` (`BLG-QA-150`, EPIC-04, v8.9) fixed `trade_plans.setup_type` having no server-side default by normalizing null/absent/empty to `"Other"` on `POST /trade-plans`. This closed the immediate data-quality gap (every stored row now has a groupable, non-null value) but means a plan where the user explicitly selected "Other" from the dropdown is now indistinguishable, in the stored data, from one that was never actively classified at all.

## Decision

**Accept the conflation. No new distinguishing field, enum value, or schema change.**

`setup_type = "Other"` continues to mean "either the user explicitly chose Other, or nothing was classified" — a single bucket covering both cases. `PUT /trade-plans/{id}` is **not** extended with the same null→"Other" normalization ST-13 applied to `POST` — see §"PUT left unchanged" below for why.

## Rationale

1. **The feature this protects doesn't exist yet.** `win_rate_by_setup_type` is a *future* SI-02 predesign query (`docs/specs/si02/si02_query_predesign.md` §"pre-design queries") — not a shipped, live, or even scheduled feature. Nothing observable is degraded today by this conflation; there is no current consumer whose output is wrong.
2. **SI-02 itself is far from its own trigger gate.** Per repeated live re-checks this cycle and prior cycles (`docs/product/decisions/si02-reentry-trigger-criteria.md`, `docs/ops/render_starter_tier_headroom_reassessment_2026-08-13.md` §4, and this cycle's own ST-25/ST-26), the ≥20-linked-closed-trades gate remains far from met (single digits as of the most recent confirmed reading). The analytics precision this conflation would affect is not close to being load-bearing.
3. **A distinguishing mechanism is real, avoidable complexity added ahead of need.** Every candidate fix — a new `setup_type_source` column, a distinct `"Unclassified"` enum value (considered and named in `arc6_prerequisite_field_population_audit_2026-08-16.md` §4.2, which deferred the same question to this decision), or a null-preserving default reversed out of ST-13 — touches schema, the frontend `SETUP_TYPE_OPTIONS` enumeration, and/or the eventual `win_rate_by_setup_type` query logic itself. Building that now, speculatively, ahead of the feature and the trade volume that would actually use it, is premature.
4. **The right time to decide the mechanism is when SI-02's analytics work is actually scheduled**, informed by the real trade volume and precision needs at that time — not guessed now against a query that doesn't exist. This decision does not close that door; it defers it to the story that actually builds `win_rate_by_setup_type`, which should re-open this question with real data in hand.
5. **This is the exact off-ramp the story's own scope offers.** `BLG-FEAT-93`'s scope explicitly names "make an explicit, documented decision to accept the conflation with rationale" as a valid resolution, matching the option ST-13's own original AC offered — this is not a shortcut around the story, it is one of its two designed outcomes.

## PUT left unchanged (no default extension)

The story's scope also asked: "if a fix is chosen, also decide whether to extend the default to `PUT`." Since no fix (no distinguishing mechanism) is chosen, the question becomes narrower: should `PUT /trade-plans/{id}` mirror `POST`'s null→`"Other"` normalization for consistency, independent of the distinguishing-mechanism question?

**Decision: no.** `update_plan()`'s existing semantics — `None` in the request body means "don't touch this field," uniformly across every field, not just `setup_type` — is a general PUT contract, not a `setup_type`-specific gap. Special-casing `setup_type` to treat `null` as "reset to Other" while every other field treats `null` as "leave unchanged" would be a surprising, undocumented exception to that contract for API consumers. A client that wants to explicitly reset a plan's `setup_type` to the canonical default can already do so by sending `setup_type: "Other"` directly — the same value `POST`'s default resolves to — which is a discoverable, explicit action rather than an implicit side effect of sending `null`.

**Consequence (accepted, not a new gap):** a `trade_plans` row created before ST-13 shipped, with `setup_type` still `null`, and never explicitly re-classified by the user, remains `null` indefinitely. This is a small, bounded, backward-looking dataset (pre-v8.9 plans only) — a one-off backfill (`UPDATE trade_plans SET setup_type = 'Other' WHERE setup_type IS NULL`) would close it directly, but requires live production database access this session does not have. Noted here as a disclosed, low-priority follow-up rather than silently left unaddressed — a future session with production DB access may run it if warranted, but it is not itself blocking this decision or any current feature.

## Spec updated

`docs/specs/api_contracts/trade_plan_endpoints.md`'s `PUT /trade-plans/{id}` section (`"Same fields as POST (all optional for PUT)"`) now cross-references this decision, clarifying that the `POST`-only null→`"Other"` normalization does not apply on update.

## Sign-off

**Product Owner:** Approved — 2026-08-21. Accept-as-is is the correct call while `win_rate_by_setup_type` remains an unbuilt, far-gated future feature; re-open this decision when that feature is actually scheduled.
