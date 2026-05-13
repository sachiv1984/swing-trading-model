# STEP 9 Write Plan — <cycle_id>

Context refresh completed: Yes (STEP 8.5.A)

For each file record: action (create | modify | append-only), reason, and the STEP 8 decision or lifecycle requirement that requires it.

---

### 1) `claude/roadmap/current_roadmap.md`
Action: modify
Traceability: STEP 8 decision(s) — `<list>`
Delta:
- Add: `<items | none>`
- Replace: `<items | none>`
- Defer: `<items + conditions | none>`
- Kill: `<items | none>`
- Hard gate status changes: `<gate → new status + evidence artefact reference | none>`

---

### 2) `claude/roadmap/decision_log.md`
Action: append-only
Traceability: STEP 8 decision(s) — `<list>`
Append entries for: `<Add | Replace | Defer | Kill | No-change>`

Pre-write entry count: N = `<n>`
Post-write must equal: N + `<entries added this run>`

---

### 3) `claude/backlog/backlog.md`
Action: modify (reconciliation only)
Traceability: STEP 8 decision(s) — `<list>`
- Promoted to Roadmap: `<count + list>`
- Deferred/Parked: `<count + list>`
- Killed/Closed: `<count + list>`
- Duplicates removed: `<count>`
- Stale ideas closed: `<count>`
- Provisional-Target fields added: `<list | none>`

---

### 4) `claude/roadmap/workforce_capacity.md`
Action: create | modify | none
Traceability: STEP 7 economics + STEP 8 decisions — `<summary>`
- Capacity freed: `<FTE + skills | none>`
- Allocation changes: `<initiative → FTE/skills | none>`

---

### 5) `claude/roadmap/initiative_register.md`
Action: create | modify | none
Traceability: STEP 8 decision(s) — `<list>`
- Status updates: `<initiative → status>`
- Displacement candidate flags: `<initiative → flag + rationale + date | none>`
- Effort bands added/updated: `<initiative → S/M/L | none>`

---

### 6) `claude/cycles/<cycle_id>/cycle_record.md`
Action: create | modify
Sections present: STEP 2 · STEP 3 · STEP 4 · STEP 5 · STEP 8

---

### Additional files (if applicable)

| File path | Action | Reason | Traceability |
|-----------|--------|--------|--------------|
| `<path>` | create / modify / append | `<reason>` | `<STEP 8 decision or lifecycle requirement>` |

---

## Integrity Checks (all must pass before STEP 9 proceeds)

- [ ] All files within Section 4 write scope
- [ ] Every write traceable to STEP 8 decision or lifecycle compliance only — no formatting-only edits
- [ ] Decision log append-only and duplicate-checked
- [ ] Backlog edits reconciliation-only (no grooming, no new items unless required by a STEP 8 Add)
- [ ] PoG documents Class 8 compliant and written only for items with recorded hard gates
- [ ] Hard gate "complete" markings in `current_roadmap.md` reference evidence artefacts
- [ ] Displacement candidate flags written to `initiative_register.md` only
- [ ] Effort bands recorded for all new/updated roadmap/backlog items in `scored_initiatives.md`
- [ ] All action-now prompt patches confirmed, version-incremented, recorded in `prompt_change_log.md`
- [ ] All deferred patches have named owner, target date, specific file, specific section (or are escalations)
- [ ] Meta-review conducted if due and recorded in `meta_review.md`
- [ ] All `Advancing` register rows updated to terminal status (`Promoted-Added` or `Promoted-Rejected`)

Any check fails → discard plan; halt per STEP 8.5.E.
