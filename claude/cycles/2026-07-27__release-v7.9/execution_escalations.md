Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

## ESC-EXEC-20260727-01

- **Raised at:** 2026-07-27T21:30:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-07-27__release-v7.9
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-08 / EPIC-08 — Provision a staging credential so SI-02 live gate re-checks don't depend on ad hoc session environment
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-08's premise (a governed-routine credential needs to be provisioned) is only half accurate. Investigation this session found `docs/security/api_key_security_register.md` entry #6 (Application X-API-Key, `RENDER_API_KEY` / `~/.api_keys`) already documents a working, provisioned credential for exactly this purpose — confirmed working 2026-07-09 (`BLG-OPS-99`, v6.8). The actual gap is that `~/.api_keys` does not persist into the container/session each governed routine runs in: confirmed absent in this session (`test -f ~/.api_keys` → not found), consistent with every recent scheduled roadmap rebalance's "credentials absent" finding. This is not a "credential was never created" problem — it is a "the already-provisioned credential's local copy isn't available in this environment" problem. Resolving it requires a human to either (a) supply the actual secret value into this/future session environments (e.g. via a `!`-prefixed shell command writing `~/.api_keys`, or configuring it as a persistent environment variable/secret at the Claude Code environment level), or (b) confirm a different, more durable storage mechanism. The engine cannot obtain or persist the real secret value itself — no account/console access, and committing it to the repo would itself be a security incident per the register's own warning.
- **Owning authority:** Infrastructure & Operations Owner
- **Unblock criteria:** A human confirms the `RENDER_API_KEY` value is available in the environment governed-routine sessions run in (however it is chosen to persist), and the next scheduled roadmap rebalance is able to perform a genuine live SI-02 re-check without a "credentials absent" finding.
- **SLA due-by:** Next scheduled roadmap rebalance (Workforce/Capacity-class SLA — Accepted Risk eligible, Product Owner only)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** Resolved 2026-07-28 — human supplied the `RENDER_API_KEY` value into this session's `~/.api_keys`. First attempt was Render's platform/management API key (`rnd_...` prefix, valid against `api.render.com` but returned 401 against the trading-assistant application itself) — same category of confusion as the historical `ESC-EXEC-20260703-01` precedent. Corrected to the actual application `API_KEY` value (from the production service's own Environment tab, not a personal Render account key), confirmed via `GET /trades` → 200. Live SI-02 re-check performed directly against production: `GET /trades` → `total_trades: 20`; `GET /trade-plans` → 11 plans, 0 with `position_id` set. No "credentials absent" finding — the unblock criteria's second clause is satisfied. Whether the SI-02 gate itself is MET/NOT MET given these figures is a `current_roadmap.md` determination left to the next `run roadmap` invocation (out of Sprint Execution's write scope) — this escalation closes on the credential/verification problem only, not on re-adjudicating the gate. Note: this fix is confirmed for *this* session only; whether `~/.api_keys` persists into future sessions is still unconfirmed — if a future governed-routine session reports "credentials absent" again, the persistence question (not the credential's validity) is the open item.

**Carried forward from `EPIC-08`'s branch** (unmerged — EPIC-08 has no PR of its own, blocked pending human credential action) via the `EPIC-12` branch's cross-EPIC merge, so this record isn't lost once `EPIC-12` lands on main.

---

## ESC-EXEC-20260727-02

**Raised by:** QA & Testing Owner (agent-mediated review of PR #1101, EPIC-14)
**Blocks execution:** No
**Blocks merge:** No — this is a tracked follow-up, not a defect in what's shipped in PR #1101.

**Finding:** ST-14's deliverable (`claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md`, § "Displacement Debt Register — Design") is a complete design, handed off for physical placement — per the write-scope hard gate (`execution_prompt.md` §7), this routine cannot create files under `claude/roadmap/` or edit `claude/system/roadmap_prompt.md`. Two separate actions are required to make the register real and self-sustaining:

1. Create `claude/roadmap/displacement_debt_register.md` using the format and seed content in `qa_evidence_EPIC-14.md`.
2. Edit `roadmap_prompt.md` STEP 8's "Displacement candidate flag" instruction so future cycles actually update this register (not just `initiative_register.md`).

Both actions are needed together — if only (1) lands, the register goes stale immediately after creation with no forcing function to keep it current; if only (2) lands, the instruction points at a file that doesn't exist. Recording this as a tracked escalation (rather than only a prose note inside `qa_evidence_EPIC-14.md`) so the dependency between the two isn't lost once this PR merges and this cycle's artefacts stop being actively read.

**Unblock criteria:** Roadmap Rebalance Engine or Head of Specs Team, at the next `run roadmap` or `manage roadmap` invocation, performs both (1) and (2) together and closes this escalation.

**Status:** Open — non-blocking, tracked for next roadmap-engine touch.
