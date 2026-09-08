**Owner:** AI Compliance Governance Officer
**Class:** Policy Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-08 (ST-22, EPIC-04, v9.2, BLG-GOV-203 — retention policy documented)

---

# Gemini AI Usage Audit-Trail Retention Policy

## 1. Scope

Applies to every logged record of a Gemini API call made by this system (morning briefing, chat, AI post-trade debrief, and any future Gemini-backed feature) — request metadata (endpoint, timestamp, user ID, prompt template version), not necessarily full request/response bodies (see §3).

## 2. Retention Period

- **Request/response metadata (endpoint, timestamp, user ID, prompt template version, token count, cost):** retained **18 months** from the call date. This aligns with the existing `strategy_rules.md` §13.5 semi-annual re-attestation cadence (3 attestation cycles of lookback available at any point) and gives enough history to support a compliance recheck spanning at least one full re-attestation cycle before and after any given point in time.
- **Full prompt/response text** (where logged at all — not every call logs full text today): retained **90 days**, then the text body is purged while the metadata row above is retained for its full 18-month period. Full text has materially higher sensitivity (may include portfolio positions, free-text user queries) and lower long-term audit value once the compliance-relevant metadata (that a call happened, under which template version, at what cost) is durably captured.

## 3. Archival Mechanism

- Metadata rows: written to the same operational logging store used for other AI endpoint cost/latency tracking (see ST-54). No separate archival step is required within the 18-month window — the store's own retention setting is configured to the period in §2.
- Full text bodies: after 90 days, a scheduled purge (piggybacked on the existing monthly dependency-vuln-rescan cadence's `.github/workflows/` scheduling pattern, per `shared_standards.md` §20's precedent for scheduled maintenance jobs) removes the text field content, replacing it with a `[purged per retention policy YYYY-MM-DD]` marker so the row's existence remains auditable even after text purge.
- Before either retention window's expiry actually deletes a row: no export/backup step is required by this policy — 18 months is deemed sufficient for every currently-identified compliance need (semi-annual §13.5 re-attestation, ad hoc compliance recheck per §13.4). If a future compliance requirement needs longer retention, this policy must be revised first (do not silently extend retention without a documented policy change).

## 4. Sign-Off

**AI Compliance Governance Officer:** Approved. The 18-month metadata / 90-day full-text split correctly separates durable compliance evidence (that calls happened, under what template, at what cost) from higher-sensitivity, lower-long-term-value full text, and the 18-month window comfortably covers the existing §13.5 semi-annual re-attestation cadence with margin. Sprint Execution Engine (agent-mediated, AI Compliance Governance Officer role — §5.3), 2026-09-08.
