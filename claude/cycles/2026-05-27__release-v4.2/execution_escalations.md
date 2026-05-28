Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-28

---

# Execution Escalations — 2026-05-27__release-v4.2

---

## ESC-EXEC-20260528-01

- **Raised at:** 2026-05-28T00:00:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-27__release-v4.2
- **Step:** STEP 3 — Execution Loop, EPIC-01
- **ST/EPIC item:** ST-01 — Anthropic API Accountability & Key Security
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-01 requires Director of HR and AI Compliance Officer to: (a) review the AI Compliance Officer charter for explicit Anthropic API coverage and update if a gap exists (BLG-GOV-66), and (b) confirm the ANTHROPIC_API_KEY security posture (minimum permissions, env var only, no log exposure) and document the confirmation (BLG-GOV-65). These are human sign-off items that cannot be completed by the execution engine.
- **Owning authority:** Director of HR; AI Compliance & Governance Officer
- **Unblock criteria:** Director of HR confirms charter coverage; AI Compliance Officer confirms key security posture; documentation committed to `exec/2026-05-27__release-v4.2/EPIC-01`; AC-01 through AC-04 met.
- **SLA due-by:** 2026-05-31T00:00:00Z (72-hour default)
- **Blocks execution:** No (EPIC-01 can complete ST-02; escalation tracks outstanding human items)
- **Disposition:** Open
- **Resolution summary:** —

---

## ESC-EXEC-20260528-02

- **Raised at:** 2026-05-28T00:00:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-27__release-v4.2
- **Step:** STEP 3 — Execution Loop, EPIC-01
- **ST/EPIC item:** ST-03 — Claude API Log Hygiene Policy
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-03 AC-02 requires Infrastructure & Operations Owner to inspect Render production logs (both staging and production environments) to confirm that `ANTHROPIC_API_KEY` and full prompt text are NOT captured. The engine cannot independently access Render log data. The engine can produce the policy framework document but cannot independently verify production log hygiene.
- **Owning authority:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
- **Unblock criteria:** Infrastructure & Operations Owner inspects Render production logs and confirms (or remediates) non-exposure of API key and full prompt text; log hygiene policy document produced with all four ACs met; committed to `exec/2026-05-27__release-v4.2/EPIC-01`.
- **SLA due-by:** 2026-05-31T00:00:00Z (72-hour default)
- **Blocks execution:** No (EPIC-01 can complete with ST-02 only; ST-01 and ST-03 are parallel delegated items)
- **Disposition:** Open
- **Resolution summary:** —

---

## ESC-EXEC-20260528-03

- **Raised at:** 2026-05-28T00:00:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-27__release-v4.2
- **Step:** STEP 3 — Execution Loop, EPIC-02
- **ST/EPIC item:** ST-04 — API Performance Baseline Update (OA-3)
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-04 requires a live environment timing run for `POST /ai/check-daily-cost` to obtain p50 latency data. The Infrastructure & Operations Owner must execute the timing run in staging or production, then record the result in `docs/ops/api_performance_baseline.md`. The engine cannot independently run live API timing calls.
- **Owning authority:** Infrastructure & Operations Owner
- **Unblock criteria:** Live (or estimated) timing run completed for `POST /ai/check-daily-cost`; result added to `docs/ops/api_performance_baseline.md`; reviewed by Infrastructure & Operations Owner; committed to `exec/2026-05-27__release-v4.2/EPIC-02`.
- **SLA due-by:** 2026-05-31T00:00:00Z (72-hour default)
- **Blocks execution:** No (EPIC-02 can operate independently)
- **Disposition:** Open
- **Resolution summary:** —

---

## ESC-EXEC-20260528-04

- **Raised at:** 2026-05-28T00:00:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-27__release-v4.2
- **Step:** STEP 3 — Execution Loop, EPIC-02
- **ST/EPIC item:** ST-05 — Claude API First Monthly Cost Review
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-05 AC-01 requires actual Claude API call volume and cost data from live logging (gemini_audit_log table or equivalent). The FinOps & Resource Architect must query production data and produce the first monthly review report. The engine cannot access production database or Render logs independently.
- **Owning authority:** FinOps & Resource Architect; Infrastructure & Operations Owner
- **Unblock criteria:** First monthly review report produced with actual API call volume and cost data; monthly monitoring cadence defined; cost alert threshold defined; BLG-OPS-30 scope reference updated to Claude API; committed to `exec/2026-05-27__release-v4.2/EPIC-02`.
- **SLA due-by:** 2026-05-31T00:00:00Z (72-hour default)
- **Blocks execution:** No (EPIC-02 can operate independently)
- **Disposition:** Open
- **Resolution summary:** —

---

## ESC-EXEC-20260528-05

- **Raised at:** 2026-05-28T00:00:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-27__release-v4.2
- **Step:** STEP 3 — Execution Loop, EPIC-02
- **ST/EPIC item:** ST-06 — Claude API Thesis Generation Latency Baseline
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-06 AC-01 requires minimum 10 sample calls from a live environment for p50/p95 measurement of `POST /trade-plans/{plan_id}/generate-thesis`. The Head of Engineering or Infrastructure & Operations Owner must run these calls in staging or production and record the timing results.
- **Owning authority:** Head of Engineering; Infrastructure & Operations Owner
- **Unblock criteria:** p50/p95 latency baseline from ≥10 live sample calls recorded in `docs/ops/api_performance_baseline.md`; regression threshold defined; committed to `exec/2026-05-27__release-v4.2/EPIC-02`.
- **SLA due-by:** 2026-05-31T00:00:00Z (72-hour default)
- **Blocks execution:** No (EPIC-02 can operate independently)
- **Disposition:** Open
- **Resolution summary:** —

---

## ESC-EXEC-20260528-06

- **Raised at:** 2026-05-28T00:00:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-27__release-v4.2
- **Step:** STEP 3 — Execution Loop, EPIC-04
- **ST/EPIC item:** ST-12 — SI-04 Strategy Version Comparison Pre-Planning
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-12 requires Product Owner to define: which strategy versions to include in the SI-04 comparison view, the performance comparison methodology (deterministic), and a UI view concept. These are product definition decisions that require PO authority. The engine can produce the scope definition document once these inputs are provided.
- **Owning authority:** Product Owner
- **Unblock criteria:** Product Owner provides: (1) list of strategy versions to compare, (2) performance comparison methodology definition, (3) UI view concept description; Head of Specs Team sign-off obtained; engine produces and commits SI-04 scope definition document to `exec/2026-05-27__release-v4.2/EPIC-04`.
- **SLA due-by:** 2026-05-31T00:00:00Z (72-hour default)
- **Blocks execution:** No (EPIC-04 can complete ST-11 and ST-13 independently)
- **Disposition:** Open
- **Resolution summary:** —
