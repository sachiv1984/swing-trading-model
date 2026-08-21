# =========================
# CLAUDE LIFECYCLE AUDIT PACKAGE — v6
# =========================
# Continuous improvement instrument for the claude/ governance system.
# Produces: Resolved → Scorecard → Gap Register → Stage Findings → Improvements → Patch Manifest
#
# v6 changes vs v5:
#   - Scorecard formulas require CONFIRMED counts; estimated inputs flagged ~ with confidence tag
#   - B4 (hard gate compliance) returns "INSUFFICIENT HISTORY" not N/A when <3 cycles available
#   - Token budget methodology footnote: in-run context not captured; execution engine understated
#   - §14 self-version check (AUD-018 class) is CONDITIONAL on divergence, not persistent advisory
#   - Gap Register estimated inputs promoted to visible ESTIMATED flags in token budget table
#   - Tier placement rule: BR≥4 + Medium effort + no deps = Tier 2, not Tier 3
#   - Output format: tables and bullets only; scorecard arithmetic in appendix
#   - Patch manifest: every improvement has a machine-actionable PATCH block for Claude Code
#   - Config block auto-update: audit produces copy-paste config lines for next run
# =========================

# -------------------------
# CONFIG
# -------------------------
SCOPE = "claude/"
MAX_IMPROVEMENTS = 20
AUDIT_VERSION = "6"

# Prior audit tracking — the audit itself produces updated values at end (see §9 CONFIG UPDATE)
PRIOR_AUDIT_ID = "AUD-2026-08-21"
PRIOR_AUDIT_OPEN_ITEMS = [
    "AUD-2026-08-21-004", "AUD-2026-08-21-010", "AUD-2026-08-21-011",
    "AUD-2026-08-21-002", "AUD-2026-08-21-005", "AUD-2026-08-21-006",
    "AUD-2026-08-21-007", "AUD-2026-08-21-008", "AUD-2026-08-21-009",
    "AUD-2026-08-21-001", "AUD-2026-08-21-003",
]
  # All 11 improvements filed at AUD-2026-08-21 remain open at session end — this was a report-only
  # run (no "action all audit points" direction given). Highest-weight items: AUD-2026-08-21-004
  # (Sprint Close item-count reconciliation, weight 9) and AUD-2026-08-21-010 (merge_gate mid-session
  # re-sync, weight 9). AUD-2026-08-21-011 (pre-seal stale-feature scoping check) is D1-tracked STALE
  # (2 cycles carried, first flagged v8.7 Phase 3) — priority candidate for the next audit's B7/D1 check.

# Health Scorecard baseline — updated by audit output each run for trend tracking
PRIOR_SCORES = {
    "token_efficiency":      84,
    "governance_integrity":  74,
    "execution_reliability": 53,
    "friction_load":         44,
    "document_hygiene":      100,
}

# Completed cycle count — increment after each post-ship closure
# Used to determine B4 history sufficiency (need ≥3 cycles for hard gate compliance)
COMPLETED_CYCLES = 76  # current completed_cycle_count at AUD-2026-08-21

# -------------------------
# MISSING FILE RULE
# -------------------------
# If a file in a stage's "load" list cannot be retrieved:
#   - Record in Gap Register: path / status / impact / promote-to-improvement
#   - Do NOT invent content. Continue stage on available files.
#   - Stage with zero loadable files → NOT CHECKABLE.

# -------------------------
# TOKEN LOADING RULES
# -------------------------
TOKEN_TIPS = {
    1: "Lazy-load per stage — only files in that stage's load list",
    2: "Field-level reads — headers/version/status only unless full content needed",
    3: "Reuse reads — do not reload a file already loaded in a prior stage this session",
    4: "Canonical references — identify duplicates by path pointer, not by copying content",
    5: "Dry-run awareness — note write risks without executing",
    6: "Structured outputs — tables/JSON not prose",
    7: "Directory manifest first — list directory before loading individual files",
    8: "Skip cleanly — NOT CHECKABLE if no files loadable; move on",
}

# -------------------------
# EVIDENCE CLASSIFICATION
# -------------------------
# OBSERVED   — confirmed by execution evidence in a cycle record
# LATENT     — structurally present risk, not yet triggered
# THEORETICAL — possible but no evidence in any cycle record
#
# Priority weight = blast_radius × evidence_weight
# Weights: OBSERVED=3  LATENT=2  THEORETICAL=1

# -------------------------
# BLAST RADIUS
# -------------------------
# 1 — 1 file or engine
# 2 — 2-3 files or engines
# 3 — full phase (2-4 engines)
# 4 — multiple phases or all cycles
# 5 — every engine invocation / every cycle

# -------------------------
# TIER PLACEMENT RULES (v6 correction)
# -------------------------
# Tier 1: Low effort + no dependencies (any blast radius)
# Tier 2: Medium effort + no dependencies OR Tier 1 deps met
#         ALSO: Blast Radius ≥ 4 + Medium effort + no deps → Tier 2 (not Tier 3)
# Tier 3: High effort OR complex dependency chain OR requires new files + multi-engine coordination

# =========================
# STAGE CHECKLIST
# =========================

STAGE_CHECKLIST = [

    # -------------------------------------------------
    # PHASE 0: RESOLVED SINCE LAST AUDIT
    # -------------------------------------------------
    {
        "stage": "Phase 0 — Resolved Since Last Audit",
        "load": [
            "claude/system/prompt_change_log.md",  # entries since PRIOR_AUDIT_ID date only
            "claude/cycles/",                       # most recent lessons_learnt — outstanding actions table only
        ],
        "check": (
            "If PRIOR_AUDIT_OPEN_ITEMS is empty: output single line 'First audit run — no prior items.'\n"
            "Otherwise for each AUD-ID in PRIOR_AUDIT_OPEN_ITEMS:\n"
            "  Search prompt_change_log.md for matching filename + version entry.\n"
            "  Classify: RESOLVED (cite evidence ref) | PARTIAL (describe gap) | OPEN (no evidence).\n"
            "\n"
            "OUTPUT — one table only:\n"
            "| AUD-ID | Title (3 words) | Status | Evidence ref |\n"
            "No prose. OPEN items carry forward automatically — do not re-generate them as new findings."
        ),
        "tips": [2, 3]
    },

    # -------------------------------------------------
    # PHASE 1: HEALTH SCORECARD
    # -------------------------------------------------
    {
        "stage": "Phase 1 — Health Scorecard",
        "load": [
            "claude/system/shared_standards.md",       # §13 dry-run table — field-level
            "claude/system/OPERATIONAL_GUIDE.md",      # §14 governance table — field-level
            "claude/system/prompt_change_log.md",      # last 10 entries only
            "claude/cycles/",                          # ALL cycles: lessons_learnt files — friction count + type only
            "claude/agents/",                          # file count only
        ],
        "check": (
            "CONFIRMED COUNTS RULE: Every deduction must cite the specific file + field that produced the count.\n"
            "If a count cannot be confirmed from loaded content: mark it as ~N (estimated) and tag [ESTIMATED].\n"
            "A dimension with 2+ [ESTIMATED] inputs is tagged [LOW CONFIDENCE] and cannot be used for trend comparison.\n"
            "\n"
            "DIMENSION FORMULAS (start each at 100, subtract, floor at 0):\n"
            "\n"
            "TOKEN_EFFICIENCY:\n"
            "  -5 per confirmed inline schema block (cite file + step)\n"
            "  -5 per confirmed inline invariant block (cite file + section)\n"
            "  -3 per confirmed inline halt format block (cite file + step)\n"
            "  -4 per engine not using field-level preflight read (cite engine)\n"
            "  -8 per engine absent from shared_standards §13 dry-run table (cite engine name)\n"
            "\n"
            "GOVERNANCE_INTEGRITY:\n"
            "  -8 per advisory-only guard that should be a structural hard gate (cite file + rule)\n"
            "  -5 per authority role with no confirmed charter file (cite role name)\n"
            "  -6 per artefact absent from OPERATIONAL_GUIDE §13 register (cite artefact)\n"
            "  -4 per §14 version entry diverging from actual prompt file version (cite file)\n"
            "\n"
            "EXECUTION_RELIABILITY:\n"
            "  -7 per halt path with no defined recovery instruction (cite file + step)\n"
            "  -6 per write operation with ASSERTION-only idempotency (cite file + operation)\n"
            "  -5 per deferred patch carried 2+ cycles unresolved (cite patch)\n"
            "  -5 per engine missing zero-state bootstrap path (cite engine)\n"
            "\n"
            "FRICTION_LOAD:\n"
            "  (Window: cycles since PRIOR_AUDIT_ID only — not all-time cumulative. Confirmed at\n"
            "  AUD-2026-07-01: literal 'all cycles' wording is ambiguous and was resolved as\n"
            "  'since last audit' to match PRIOR_SCORES baseline methodology.)\n"
            "  -4 per confirmed Type A friction item since PRIOR_AUDIT_ID (cite cycle)\n"
            "  -3 per confirmed Type C friction item since PRIOR_AUDIT_ID (cite cycle)\n"
            "  -6 per friction item confirmed recurring across 2+ cycles (cite cycles)\n"
            "  -5 per deferred patch confirmed unresolved since PRIOR_AUDIT_ID (cite patch)\n"
            "  NORMALISED RATE NOTE (added AUD-2026-08-12-002): the raw score above is a window-scoped\n"
            "  total, not per-cycle-normalised — a window spanning fewer cycles can score higher even\n"
            "  when the underlying per-cycle friction rate is worsening. Alongside the raw score, always\n"
            "  report items-per-cycle-record = (total friction items this window) / (cycle-records this\n"
            "  window) and compare it to the prior audit's own reported rate, so a rising per-cycle rate\n"
            "  is never masked by a raw score that happens to improve because this window had fewer\n"
            "  cycles than the last one. (First observed AUD-2026-08-12: raw score rose 25→37 while the\n"
            "  rate rose 4.75→7.5 items/cycle-record — the two signals genuinely disagreed.)\n"
            "\n"
            "DOCUMENT_HYGIENE:\n"
            "  -4 per confirmed non-compliant header (cite file)\n"
            "  -5 per wrong document class declaration (cite file)\n"
            "  -4 per confirmed broken path reference (cite file + section)\n"
            "  -3 per agent file with non-standard role header format (cite file)\n"
            "\n"
            "OUTPUT FORMAT (tables only — arithmetic in SCORECARD APPENDIX at end of audit):\n"
            "\n"
            "SYSTEM HEALTH — [date]  |  Prior: [date or 'none']\n"
            "| Dimension | Score | Bar (▓=10pts) | Trend | Confidence |\n"
            "| Token Efficiency | XX | ▓▓▓▓▓░░░░░ | ▲/▼/─/NEW | HIGH/LOW |\n"
            "| Governance Integrity | XX | ... | ... | ... |\n"
            "| Execution Reliability | XX | ... | ... | ... |\n"
            "| Friction Load | XX | ... | ... | ... |\n"
            "| Document Hygiene | XX | ... | ... | ... |\n"
            "| **Overall** | **XX** | ... | ... | ... |\n"
            "\n"
            "If overall < 65: add row: | ⚠ GOVERNANCE HOLD RECOMMENDED | resolve P0 items before next cycle |\n"
            "\n"
            "SCORECARD APPENDIX (at end of document — not inline):\n"
            "Show full deduction workings per dimension. Label each count as CONFIRMED or ESTIMATED."
        ),
        "tips": [2, 6, 7]
    },

    # -------------------------------------------------
    # PHASE 2: GAP REGISTER
    # -------------------------------------------------
    {
        "stage": "Phase 2 — Gap Register",
        "load": [],  # populated from all stage load attempts
        "check": (
            "Consolidate all files that could not be loaded during any stage.\n"
            "Attempt explicit load of these high-value files if not already loaded:\n"
            "  claude/agents/ — directory listing\n"
            "  claude/system/lifecycle_schema.json — header only\n"
            "  claude/ideas/rejected_but_strong.md — header only\n"
            "  claude/scoring/ — directory listing\n"
            "  claude/system/OPERATIONAL_GUIDE.md §13 — table rows only\n"
            "  CLAUDE.md — header + command table only\n"
            "  .claude_current_state.json — status field only\n"
            "\n"
            "OUTPUT — one table only:\n"
            "| Stage | File | Status | Impact (5 words) | → Improvement? |\n"
            "No prose. Status options: NOT FOUND | PARTIAL | ESTIMATED (loaded but count unverified)"
        ),
        "tips": [2, 8]
    },

    # -------------------------------------------------
    # STAGE 1: LIFECYCLE MAPPING
    # -------------------------------------------------
    {
        "stage": "Stage 1 — Lifecycle Mapping",
        "load": [
            "CLAUDE.md",                             # command table + last-updated field
            "claude/README.md",                      # §4 engine list, file paths
            "claude/system/OPERATIONAL_GUIDE.md",    # §4 phase table, §14 version table — field-level
        ],
        "check": (
            "OUTPUT — tables only:\n"
            "\n"
            "TABLE 1 — Command path check:\n"
            "| Command | Prompt path in CLAUDE.md | File confirmed? | Invocation syntax match? |\n"
            "\n"
            "TABLE 2 — Engine documentation coverage:\n"
            "| Engine | In OPERATIONAL_GUIDE §4? | In README §4? | Gap |\n"
            "\n"
            "TABLE 3 — §14 version spot check (sample 3 engines from §14 vs prompt_change_log):\n"
            "| Engine | §14 version | Last log entry version | Match? |\n"
            "\n"
            "FINDINGS (bullet list only — no prose paragraphs):\n"
            "- Any broken path in CLAUDE.md command table\n"
            "- Any engine in OPERATIONAL_GUIDE §4 missing from README\n"
            "- CLAUDE.md Last Updated vs most recent engine version date — flag if >14 days stale\n"
            "- Any governed routine absent from CLAUDE.md command table (e.g. run audit)"
        ),
        "tips": [1, 2, 3]
    },

    # -------------------------------------------------
    # STAGE 2: BEHAVIOURAL AUDIT
    # -------------------------------------------------
    {
        "stage": "Stage 2 — Behavioural Audit",
        "load": [
            "claude/cycles/",  # ALL folders — per cycle load:
                               #   run_manifest.md (preflight table only)
                               #   lessons_learnt*.md (friction table + outstanding actions only)
        ],
        "check": (
            "COMPLIANCE TABLE:\n"
            "| Cycle | B1 Auth | B2 LL filed | B3 Prior patches | B4 Hard gate | B5 Action-now | B6 Log grew | B7 No 2nd carry |\n"
            "| compliance % | ... | ... | ... | ... | ... | ... | ... |\n"
            "\n"
            "B4 SPECIAL RULE (v6):\n"
            "  If COMPLETED_CYCLES < 3: mark B4 column as 'INSUFFICIENT HISTORY (need ≥3 cycles)'\n"
            "  Do NOT return N/A. Explain the history requirement explicitly.\n"
            "  If COMPLETED_CYCLES ≥ 3 AND no hard gates fired: mark as 'NO GATES FIRED — compliant'\n"
            "  If hard gates fired: check prior_status was set before halt AND block resolved within cycle.\n"
            "\n"
            "PATTERN TABLE:\n"
            "| Friction Type | Count (all cycles) | Top source file | Recurring? |\n"
            "| Type A | N | file.md | Yes/No |\n"
            "| Type B | ... | ... | ... |\n"
            "| Type C | ... | ... | ... |\n"
            "| Type D | ... | ... | ... |\n"
            "| Type E | ... | ... | ... |\n"
            "\n"
            "TREND LINE: Total friction items per cycle — list as [cycle_id: N, cycle_id: N, ...]\n"
            "State trend as: INCREASING / DECREASING / FLAT / INSUFFICIENT DATA\n"
            "\n"
            "Any B-check with compliance < 75% auto-generates an OBSERVED improvement.\n"
            "No prose narrative. Tables and bullet findings only."
        ),
        "tips": [2, 6, 7]
    },

    # -------------------------------------------------
    # STAGE 3: GOVERNANCE INTEGRITY
    # -------------------------------------------------
    {
        "stage": "Stage 3 — Governance Integrity",
        "load": [
            "claude/charter/team_charter.md",              # §3 role list, §6 invariants — field-level
            "claude/charter/document_lifecycle_guide.md",  # §3 document classes — field-level
            "claude/agents/",                              # ALL files — Role, Status, Version fields only
            "claude/system/OPERATIONAL_GUIDE.md",          # §13 register, §14 table — field-level
            "claude/cycles/",                              # most recent run_manifest.md preflight table only
        ],
        "check": (
            "TABLE 1 — Agent roster (mandatory before any findings):\n"
            "| Agent file | Role | Format | Version | Activated by | Status |\n"
            "Format: COMPLIANT (**Role:** format) | NON-COMPLIANT (## Role: or other)\n"
            "Status: CONFIRMED | NOT CONFIRMED | PATH-STALE\n"
            "\n"
            "TABLE 2 — Governance checks:\n"
            "| Check | Result | Evidence (file + section) |\n"
            "| G1 — All charter roles have agent file | PASS/FAIL | ... |\n"
            "| G2 — Agent lifecycle refs point to canonical path | PASS/FAIL | ... |\n"
            "| G3 — Artefact class declarations match lifecycle guide §3 | PASS/FAIL | ... |\n"
            "| G4 — §13 register covers scoring + ideas + lessons artefacts | PASS/FAIL | ... |\n"
            "| G5 — Design gate bypass authority in charter (not prose-only) | PASS/FAIL | ... |\n"
            "\n"
            "No prose. All findings as table rows."
        ),
        "tips": [2, 3, 7]
    },

    # -------------------------------------------------
    # STAGE 4: LIFECYCLE RELIABILITY
    # -------------------------------------------------
    {
        "stage": "Stage 4 — Lifecycle Reliability",
        "load": [
            "claude/system/lifecycle_schema.json",       # full
            "claude/system/shared_standards.md",         # §10 guard algorithm — section-level
            "claude/system/roadmap_prompt.md",           # STEP -1, STEP 0, STEP 8.5, STEP 9.0
            ".claude_current_state.json",                # status, prior_status fields only
        ],
        "check": (
            "TABLE — Reliability checks:\n"
            "| Check | Result | Evidence |\n"
            "| R1 — All lifecycle states have valid entry AND exit transitions | PASS/FAIL | ... |\n"
            "| R2 — All hard gate halt paths have defined recovery instruction | PASS/FAIL | list uncovered |\n"
            "| R3 — Idempotency: classify each write op STRUCTURAL/ASSERTION/ABSENT | see sub-table |\n"
            "| R4 — Re-evaluate max age rule exists in STEP -1.5 | PASS/FAIL | ... |\n"
            "| R5 — All engines have zero-state bootstrap path | PASS/FAIL | list missing |\n"
            "| R6 — Concurrent write prevention referenced at state-write step | PASS/FAIL | list missing |\n"
            "\n"
            "R3 SUB-TABLE:\n"
            "| Write operation | File | Guard type | Engine |\n"
            "| decision_log.md append | ... | ASSERTION/STRUCTURAL/ABSENT | ... |\n"
            "\n"
            "No prose. Flag any ASSERTION or ABSENT write as requiring improvement."
        ),
        "tips": [2, 3, 6]
    },

    # -------------------------------------------------
    # STAGE 5: TOKEN BUDGET ANALYSIS
    # -------------------------------------------------
    {
        "stage": "Stage 5 — Token Budget Analysis",
        "load": [
            "claude/system/roadmap_prompt.md",               # full — count lines
            "claude/system/release_planning_prompt.md",      # full — count lines
            "claude/system/sprint_planning_prompt.md",       # full — count lines
            "claude/system/execution_prompt.md",             # full — count lines
            "claude/system/delivery_verification_prompt.md", # full — count lines
            "claude/system/post_ship_closure.md",            # full — count lines
            "claude/system/shared_standards.md",             # §13 dry-run table
            "claude/system/lessons_learnt_prompt.md",        # full — count lines
        ],
        "check": (
            "TOKEN BUDGET TABLE:\n"
            "Count exact line numbers for each engine prompt. Mark any count you cannot confirm as ~N [ESTIMATED].\n"
            "\n"
            "| Engine | Lines | ~Tokens | Preflight files (N) | ~Preflight tokens | Inline blocks (N) | ~Block tokens | Total/invoke | Invoke/cycle | Cycle cost | Confidence |\n"
            "\n"
            "Formula: tokens = lines × 8 | preflight = Σ(file_lines × 8) | total = prompt + preflight + blocks\n"
            "\n"
            "METHODOLOGY FOOTNOTE (mandatory — print this exactly):\n"
            "⚠ This table does not capture in-run context accumulation. For execution_prompt.md,\n"
            "  actual per-invocation cost grows with sprint size (loaded EPIC items add to context).\n"
            "  Reported cost may understate actual by 30–50% on large sprints. Use as lower bound.\n"
            "\n"
            "CONFIDENCE column: HIGH if line count confirmed | LOW if estimated\n"
            "Any LOW CONFIDENCE row: add note 'load and count file to confirm'\n"
            "\n"
            "RANKED SAVINGS TABLE:\n"
            "| Rank | Opportunity | Current tokens/cycle | Post-fix tokens/cycle | Saving |\n"
            "| 1 | ... | ... | ... | ... |\n"
            "\n"
            "DEAD LOAD CHECK:\n"
            "| Engine | File loaded at preflight | Used beyond preflight check? | Dead? |\n"
            "\n"
            "DRY-RUN GAP:\n"
            "| Engine | In §13 dry-run table? | If not: token risk per failed run |\n"
            "\n"
            "CYCLE TOTAL: sum all Cycle cost column entries. State as: ~N tokens/typical cycle.\n"
            "\n"
            "No prose. All output as tables."
        ),
        "tips": [1, 2, 6]
    },

    # -------------------------------------------------
    # STAGE 6: ENGINE HANDOFF INTEGRITY
    # -------------------------------------------------
    {
        "stage": "Stage 6 — Engine Handoff Integrity",
        "load": [
            "claude/system/release_planning_prompt.md",      # §5 write scope, STEP output templates
            "claude/system/sprint_planning_prompt.md",       # STEP 0 load list, STEP -1.1 input fields
            "claude/system/execution_prompt.md",             # STEP -1 load list
            "claude/system/delivery_verification_prompt.md", # STEP 0 load list
            "claude/system/post_ship_closure.md",            # §4 inputs
            "claude/system/shared_standards.md",             # §14 preflight field scope
        ],
        "check": (
            "HANDOFF TABLE (one row per field per pair):\n"
            "| Pair | Field/Section | Producer writes? | Consumer reads? | Match? |\n"
            "\n"
            "Pairs to check:\n"
            "  Release Planning → Sprint Planning\n"
            "  Sprint Planning → Sprint Execution\n"
            "  Sprint Execution → Delivery Verification\n"
            "  Delivery Verification → Post-Ship Closure\n"
            "  Roadmap Rebalance → Release Planning\n"
            "  Amendment Cycle → Sprint Planning\n"
            "\n"
            "Flag each mismatch as:\n"
            "  CONSUMER READS UNGUARANTEED FIELD — producer may not write it\n"
            "  DEAD OUTPUT — producer writes field no consumer reads\n"
            "  SCHEMA VERSION MISMATCH — consumer assumes version producer does not declare\n"
            "\n"
            "No prose."
        ),
        "tips": [2, 3, 6]
    },

    # -------------------------------------------------
    # STAGE 7: PROMPT ARCHITECTURE & COMPRESSION
    # -------------------------------------------------
    {
        "stage": "Stage 7 — Prompt Architecture & Compression",
        "load": [
            "claude/system/roadmap_prompt.md",           # full — structure analysis
            "claude/system/shared_standards.md",         # §10 halt format, §13, §14, §15
            "claude/system/lessons_learnt_prompt.md",    # §1 invocation rule
        ],
        "check": (
            "COMPLEXITY TABLE:\n"
            "| Engine | STEPs | Hard gates | Branches | Inline blocks | Lines | Flagged? |\n"
            "Flag if: STEPs > 15 OR lines > 500 OR inline blocks > 5\n"
            "\n"
            "EXTRACTION TABLE:\n"
            "| Category | Confirmed instances (cite file+step) | Canonical home | Saving if extracted |\n"
            "| Halt format blocks | N (CONFIRMED/ESTIMATED) | shared_standards §10 | ~lines×8×N |\n"
            "| Invariant lists | N (CONFIRMED/ESTIMATED) | system/invariants.md | ~lines×8×N |\n"
            "| JSON schemas | N (CONFIRMED/ESTIMATED) | shared_standards §16 | ~lines×8×N |\n"
            "| Role verify blocks | N (CONFIRMED/ESTIMATED) | shared module | ~lines×8×N |\n"
            "\n"
            "Mark any count that cannot be confirmed from loaded content as ~N [ESTIMATED].\n"
            "\n"
            "INVOCATION GUARD TABLE:\n"
            "| lessons_learnt_prompt.md §1 guard type | STRUCTURAL / ADVISORY |\n"
            "| invocation_context parameter required? | YES / NO |\n"
            "| Calling engines that pass structured context | list or NONE |\n"
            "\n"
            "§14 VERSION DRIFT CHECK (v6 — conditional only):\n"
            "Load OPERATIONAL_GUIDE §14 version table. Load header of each engine prompt.\n"
            "If ALL versions match: output '§14 ALIGNED — no drift detected. Conditional check passes.'\n"
            "If ANY version mismatches: list mismatches and generate improvement.\n"
            "Do NOT recommend adding a persistent advisory check to every engine invocation.\n"
            "The standing rule in OPERATIONAL_GUIDE §14 v3.6 already governs this — reinforce only if drift found.\n"
            "\n"
            "No prose paragraphs."
        ),
        "tips": [1, 4, 6, 7]
    },

    # -------------------------------------------------
    # STAGE 8: AMENDMENT CYCLE COMPLETENESS
    # -------------------------------------------------
    {
        "stage": "Stage 8 — Amendment Cycle Completeness",
        "load": [
            "claude/system/amendment_cycle_prompt.md",   # full
            "claude/system/shared_standards.md",         # §10 guard algorithm
            "claude/system/lifecycle_schema.json",        # Amendment_In_Progress state
        ],
        "check": (
            "TABLE — Amendment checks:\n"
            "| Check | Result | Evidence |\n"
            "| A1 — Amendment_In_Progress has complete mini state machine | PASS/FAIL | ... |\n"
            "| A2 — First-amendment zero-state handled (no prior-amendment assumptions) | PASS/FAIL | ... |\n"
            "| A3 — Withdrawal path defined: state transition + state.json + backlog rollback | PASS/FAIL | ... |\n"
            "| A4 — Two-authority ratification is mode-independent (not bypassable) | PASS/FAIL | ... |\n"
            "| A5 — One-active-amendment rule is a hard gate (not self-enforced) | PASS/FAIL | ... |\n"
            "| A6 — Sprint Planning guards Amendment_In_Progress state explicitly | PASS/FAIL | ... |\n"
            "| A7 — amendment_lessons.md has defined sunset or optional status | PASS/FAIL | ... |\n"
            "\n"
            "No prose."
        ),
        "tips": [2, 3]
    },

    # -------------------------------------------------
    # STAGE 9: SINGLE SOURCE OF TRUTH
    # -------------------------------------------------
    {
        "stage": "Stage 9 — Single Source of Truth",
        "load": [
            "claude/README.md",                    # §3 invariants
            "claude/system/roadmap_prompt.md",     # §9 invariants
            "claude/charter/team_charter.md",      # §6 invariants
            "claude/system/shared_standards.md",   # §10-§16 section headers only
        ],
        "check": (
            "TABLE — SST checks:\n"
            "| Check | Result | Duplicate count | Token cost of duplicates | Evidence |\n"
            "| SST1 — Invariant lists: unique canonical source? | PASS/FAIL | N copies | ~tokens | files |\n"
            "| SST2 — Halt format: all engines reference §10 only? | PASS/FAIL | N inline | ~tokens | files |\n"
            "| SST3 — JSON schemas in shared_standards §16? | PASS/FAIL | N inline | ~tokens | files |\n"
            "| SST4 — workforce_capacity.md has single declared write owner | PASS/FAIL | — | — | file+section |\n"
            "| SST5 — scored_initiatives uses cycle-scoped naming | PASS/FAIL | — | — | file |\n"
            "\n"
            "(Note for future audit runs: as of AUD-2026-07-27, `scored_initiatives.md` is a deliberate\n"
            "single rolling file, not cycle-scoped-named — but `roadmap_prompt.md` STEP 6 v8.6 enforces\n"
            "read-before-write + re-read-after-write overwrite verification as a compensating control.\n"
            "Report FAIL on the literal naming check but do not treat as a fresh finding unless the\n"
            "compensating control itself is found broken.)\n"
            "\n"
            "No prose."
        ),
        "tips": [3, 4, 6]
    },

    # -------------------------------------------------
    # STAGE 10: KNOWN DESIGN GAPS & DEFERRED PATCHES
    # -------------------------------------------------
    {
        "stage": "Stage 10 — Known Design Gaps & Deferred Patches",
        "load": [
            "claude/cycles/",                          # ALL lessons_learnt — outstanding patches tables only
            "claude/system/prompt_change_log.md",      # all entries — cross-check resolution
            "claude/ideas/ideas_window.json",           # schema fields — field-level
            "claude/ideas/rejected_but_strong.md",      # header only
        ],
        "check": (
            "D1 — PATCH AGE TABLE:\n"
            "| File | Section | Change | Owner | Target | First recorded | Cycles carried | Status |\n"
            "Status: RESOLVED | ACTIVE (1 cycle) | STALE (2 cycles) | OVERDUE (3+ cycles)\n"
            "Any STALE or OVERDUE → auto-generates OBSERVED improvement.\n"
            "\n"
            "D2-D5 — DESIGN GAP TABLE:\n"
            "| Check | Result | Evidence |\n"
            "| D2 — ideas_window.json has per_agent_submission_count field | PASS/FAIL | ... |\n"
            "| D3 — rejected_but_strong.md exists with compliant header | PASS/FAIL | ... |\n"
            "| D4 — Challenger failure has halt/park instruction for Score-4 and Score-5 | PASS/FAIL | ... |\n"
            "| D5 — Re-evaluate max age enforced structurally in STEP -1.5 | PASS/FAIL | ... |\n"
            "\n"
            "No prose."
        ),
        "tips": [2, 7]
    },

    # -------------------------------------------------
    # STAGE 11: BEST PRACTICES COMPLIANCE
    # -------------------------------------------------
    {
        "stage": "Stage 11 — Best Practices Compliance",
        "load": [
            "claude/system/roadmap_prompt.md",           # STEP -1.3, STEP 9 write plan
            "claude/system/shared_standards.md",         # §13, §14, §15
            "claude/charter/document_lifecycle_guide.md", # Class 6 requirements
        ],
        "check": (
            "TABLE — BP checks (feed results back to Health Scorecard dimensions):\n"
            "| Check | Result | Evidence | Dimension |\n"
            "| BP-01 All engine prompts: Class 6 compliant headers | PASS/FAIL/PARTIAL | ... | Governance |\n"
            "| BP-02 Agent roster uses field-level reads | PASS/FAIL | ... | Token |\n"
            "| BP-03 sprint_backlog_index.json schema in §16 | PASS/FAIL | ... | Token |\n"
            "| BP-04 stage4_issue_manifest.json schema in §16 | PASS/FAIL | ... | Token |\n"
            "| BP-05 Decision log append-only: STRUCTURAL guard | PASS/FAIL | ... | Reliability |\n"
            "| BP-06 run roadmap supports --dry-run | PASS/FAIL | ... | Token+Reliability |\n"
            "| BP-07 run roadmap in §13 dry-run table | PASS/FAIL | ... | Governance |\n"
            "| BP-08 All engines have zero-state bootstrap | PASS/FAIL/PARTIAL | ... | Reliability |\n"
            "| BP-09 Displacement rule mode-independent | PASS/FAIL | ... | Governance |\n"
            "| BP-10 GitHub sync idempotency active | PASS/FAIL | ... | Reliability |\n"
            "| BP-11 scored_initiatives class = Class 4 | PASS/FAIL | ... | Governance |\n"
            "| BP-12 §13 register covers all known artefacts | PASS/FAIL | ... | Governance |\n"
            "| BP-13 prompt_change_log has entry for every engine version | PASS/FAIL | ... | Governance |\n"
            "| BP-14 lifecycle_schema.json loaded for transitions | PASS/FAIL/PARTIAL | ... | Reliability |\n"
            "| BP-15 All prior action-now patches applied | PASS/FAIL | ... | Reliability |\n"
        ),
        "tips": [2, 3, 6]
    },
    # -------------------------------------------------
    # STAGE 12: ROUTINE CONSOLIDATION ANALYSIS
    # -------------------------------------------------
    {
        "stage": "Stage 12 — Routine Consolidation Analysis",
        "load": [
            "claude/system/OPERATIONAL_GUIDE.md",          # §4 phase table, §6M known gaps, §12 trigger table
            "claude/system/shared_standards.md",           # §13 dry-run table
            "claude/system/roadmap_prompt.md",             # STEP 4 idea intake sub-steps — field-level
            "claude/system/post_ship_closure.md",          # §4 inputs, STEP list — field-level
            "claude/system/execution_prompt.md",           # STEP list line count — field-level
        ],
        "check": (
            "PURPOSE: Identify governed routines that could be collapsed into a calling engine as a\n"
            "mandatory step sequence, reducing lifecycle friction and closing known skippable gaps.\n"
            "This is NOT a token efficiency check — it is a lifecycle architecture check.\n"
            "\n"
            "CONSOLIDATION CRITERIA (score each engine against all 5):\n"
            "C1 — SINGLE TRIGGER: engine only ever runs at one fixed lifecycle point\n"
            "C2 — NO AUTHORITY SEPARATION: invoking role identical to the calling phase role\n"
            "C3 — SINGLE DOWNSTREAM CONSUMER: output consumed only by the immediately following engine\n"
            "C4 — NO INDEPENDENT GATE NEED: failure can be advisory/inline halt; no own state entry needed\n"
            "C5 — OPTIONAL OR SKIPPABLE: documented optional/recommended — skipping creates a known gap\n"
            "\n"
            "VERDICT RULES:\n"
            "  CONSOLIDATE — C1+C2+C3+C4 all met. C5 (skippable with known gap) auto-elevates\n"
            "                to CONSOLIDATE even if only 3 of C1-C4 met.\n"
            "  REVIEW      — meets C1+C2 but fails C3 or C4; warrants discussion\n"
            "  BOUNDARY    — fails C1 or C2; must remain a separate governed routine\n"
            "\n"
            "KEEP-SEPARATE OVERRIDES (any one forces BOUNDARY regardless of criteria):\n"
            "  - Engine has its own --dry-run support\n"
            "  - Engine has its own lifecycle_schema.json state entry other engines check\n"
            "  - Engine is invoked by more than one calling engine\n"
            "  - Collapsing it would push the receiving engine above 500 lines or 15 STEPs\n"
            "\n"
            "ENGINES TO EVALUATE:\n"
            "  manage roadmap (Phase 1M), groom backlog (Phase 1M), run ideas (Phase 0),\n"
            "  run design-gate (Phase 1.5), run delivery verification (Phase 4)\n"
            "  Note: roadmap rebalance, release planning, sprint planning, sprint execution,\n"
            "  post-ship closure, amendment cycle are NOT candidates — mandatory phase engines\n"
            "  with independent authority or multi-consumer outputs.\n"
            "\n"
            "TABLE 1 — Consolidation scoring:\n"
            "| Engine | C1 | C2 | C3 | C4 | C5 | dry-run? | own state? | multi-caller? | recv overload? | VERDICT |\n"
            "Mark each: checkmark (supports) | x (blocks) | ~ (partial)\n"
            "\n"
            "TABLE 2 — CONSOLIDATE/REVIEW verdicts only:\n"
            "| Engine | Verdict | Absorbing engine | As which STEP | Known gap closed |"
            " Token saving (prompt lines x 8) | Receiving engine line delta | Net |\n"
            "\n"
            "TABLE 3 — Known gaps closed by consolidation:\n"
            "| Known gap (cite OPERATIONAL_GUIDE section) | Currently caused by |"
            " Closed if consolidated into | Residual risk |\n"
            "\n"
            "COST/BENEFIT RULE:\n"
            "If consolidation saves S tokens/cycle but adds L lines to receiving engine:\n"
            "  Receiving engine would exceed 500 lines post-consolidation: verdict -> REVIEW,\n"
            "  note line budget constraint. Otherwise: net saving = S - (L x 8 x invocations/cycle).\n"
            "  Report net saving in TABLE 2.\n"
            "\n"
            "End with one bullet list: recommended consolidation actions in priority order.\n"
            "No prose paragraphs."
        ),
        "tips": [1, 2, 6]
    },

]

# =========================
# IMPROVEMENT FORMAT
# =========================

AUDIT_INDEX_FORMAT = """
At the TOP of section 5 (Improvements List), before any individual improvement,
output a single JSON block with this exact structure and comment marker:

```json
// AUDIT_INDEX
[
  {
    "id": "AUD-YYYY-MM-DD-NNN",
    "title": "<max 8 words>",
    "weight": <int>,
    "tier": <1|2|3>,
    "effort": "Low|Medium|High",
    "patches": <int — number of PATCH blocks in this improvement>,
    "files": ["<exact path>", ...],
    "depends_on": ["AUD-...", ...] or []
  },
  ...
]
```

Rules:
- One entry per improvement, sorted by weight descending (same order as improvements list).
- `patches` = exact count of PATCH blocks in that improvement (0 if improvement only adds to audit.py config).
- `files` = every file that any PATCH block in this improvement touches.
- `depends_on` = AUD-IDs that must be applied before this one (empty array if none).
- This block must be valid JSON. No trailing commas. No comments inside the array.
- The `// AUDIT_INDEX` comment is the anchor Claude Code uses to locate this block.
- Do not repeat this block anywhere else in the document.
"""

IMPROVEMENT_FORMAT = """
### AUD-[DATE]-[NNN]
**Title:** <max 12 words>
**Area:** Lifecycle | Prompt | State | Governance | Token Efficiency | Automation | Handoff
**Evidence Classification:** OBSERVED | LATENT | THEORETICAL
**Blast Radius:** 1–5
**Priority Weight:** <blast × evidence_weight>
**Problem:** <2 sentences max — what, where>
**Evidence:** <file path + section/step — exact>
**Recommended change:** <file path + section + operation (INSERT/REPLACE/APPEND) + text block>
**Expected benefit:** <quantified: tokens/cycle, compliance %, or governance outcome>
**Token impact:** Saves/Neutral/Costs — <lines × 8 × loads/cycle = N tokens/cycle>
**Implementation effort:** Low | Medium | High
**Dependencies:** <AUD-IDs or None>

PATCH:
  operation: INSERT_AFTER | REPLACE | APPEND | CREATE_FILE
  file: <exact path>
  anchor: "<exact string to locate insertion/replacement point in file>"
  content: |
    <exact text to insert or replace with>
"""

# =========================
# OUTPUT FORMAT RULES
# =========================

OUTPUT_FORMAT_RULES = """
MANDATORY OUTPUT FORMAT RULES (v6):

1. TABLES AND BULLETS ONLY for stage findings. No prose paragraphs in stage sections.
2. SCORECARD: show the score table inline; move all arithmetic to SCORECARD APPENDIX at end.
3. IMPROVEMENTS: use the exact format above. Problem field: 2 sentences max.
4. PATCH BLOCKS: every improvement must include a PATCH block with operation, file, anchor, content.
   - anchor must be an exact string that appears once in the target file (for str_replace)
   - If the change requires creating a new file: operation = CREATE_FILE, anchor = N/A
   - If the change requires multiple edits: produce multiple numbered PATCH blocks (PATCH 1, PATCH 2)
4b. AUDIT_INDEX JSON BLOCK: output at the TOP of section 5 (Improvements List), before any improvement.
   - Anchor comment on first line: // AUDIT_INDEX
   - One entry per improvement, sorted weight descending (same order as list)
   - Fields: id, title (≤8 words), weight, tier, effort, patches (count of PATCH blocks), files (all
     files any PATCH touches), depends_on (AUD-IDs that must precede; [] if none)
   - Must be valid JSON — no trailing commas, no comments inside the array
   - Claude Code uses the // AUDIT_INDEX anchor to locate and parse this block
5. No "Why it matters" field — absorbed into Problem (2 sentences = what + why).
6. AUDIT SUMMARY: 3 sentences only. Then SLA block. Then CONFIG UPDATE block.
7. CONFIG UPDATE BLOCK (mandatory — produce at end of every audit):
   Copy-paste ready Python to update audit.py config for next run:

   # === PASTE INTO audit.py CONFIG AFTER THIS RUN ===
   PRIOR_AUDIT_ID = "AUD-YYYY-MM-DD"
   PRIOR_AUDIT_OPEN_ITEMS = ["AUD-...-001", "AUD-...-002", ...]  # all OPEN items
   PRIOR_SCORES = {
       "token_efficiency":      XX,
       "governance_integrity":  XX,
       "execution_reliability": XX,
       "friction_load":         XX,
       "document_hygiene":      XX,
   }
   COMPLETED_CYCLES = N  # increment by completed cycles since last audit
   # === END PASTE ===
"""

# =========================
# FULL AUDIT PROMPT
# =========================

_STAGE_CHECKLIST_TEXT = "\n".join(
    "=" * 50 + "\n"
    f"STAGE: {s['stage']}\n"
    f"LOAD: {s['load']}\n"
    f"TIPS: {s.get('tips', [])}\n"
    f"CHECK:\n{s['check']}\n"
    for s in STAGE_CHECKLIST
)

PROMPT = f"""
You are running the Claude Lifecycle Audit v{AUDIT_VERSION} against: {SCOPE}

Goals: Effective · Efficient · Low Friction · Token-Friendly · Machine-Actionable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT EXECUTION RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Tables and bullets only in stage findings. No prose paragraphs.
2. Scorecard arithmetic → SCORECARD APPENDIX at end (not inline).
3. Confirmed counts only. Unknown counts → ~N [ESTIMATED]. 2+ estimated inputs → [LOW CONFIDENCE].
4. Every improvement must have a PATCH block with: operation, file, anchor (exact string), content.
4b. AUDIT_INDEX: output the JSON index block at the very top of section 5, before any improvement.
    Anchor line: // AUDIT_INDEX  Fields: id, title, weight, tier, effort, patches, files, depends_on.
    Must be valid JSON. Claude Code parses this to build its execution plan without reading full doc.
5. B4 compliance: if COMPLETED_CYCLES < 3 → "INSUFFICIENT HISTORY (need ≥3 cycles)" not N/A.
6. §14 drift check: CONDITIONAL — report only if drift detected. Do not recommend persistent advisories.
7. Tier placement: Blast Radius ≥ 4 + Medium effort + no deps → Tier 2 (not Tier 3).
8. Token budget: print methodology footnote about in-run context accumulation on execution engine.
9. Gap Register estimated inputs: mark LOW CONFIDENCE in token budget table, not just Gap Register.
10. End with CONFIG UPDATE block — copy-paste Python to update audit.py for next run.
11. No commentary. No praise. Evidence must trace to file + section.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTION ORDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. RESOLVED SINCE LAST AUDIT
2. HEALTH SCORECARD  (table only; arithmetic → appendix)
3. GAP REGISTER
4. STAGE FINDINGS  (Stages 1–12; tables/bullets only)
5. IMPROVEMENTS LIST
   5a. AUDIT_INDEX JSON block  ← Claude Code parses this first
   5b. Individual improvements (sorted weight desc; each with PATCH block)
6. CROSS-IMPROVEMENT MAP  (dependencies + conflicts)
7. IMPLEMENTATION TIERS  (Tier 1/2/3 per tier placement rules)
8. AUDIT SUMMARY  (3 sentences)
9. SLA BLOCK
10. SCORECARD APPENDIX  (full arithmetic)
11. CONFIG UPDATE BLOCK  (copy-paste Python)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{_STAGE_CHECKLIST_TEXT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPROVEMENT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{IMPROVEMENT_FORMAT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUDIT_INDEX FORMAT (top of section 5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{AUDIT_INDEX_FORMAT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{OUTPUT_FORMAT_RULES}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLA BLOCK FORMAT (print verbatim at §9)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SLA
- Cadence: every 3 cycles
- OBSERVED + Blast Radius ≥ 3, open after 2 audit cycles → P0 escalation to Head of Specs Team
- Overall score < 65 → GOVERNANCE HOLD: no new cycles until resolved
- Output filed as: claude/cycles/<cycle_id>/audit_report_AUD-<date>.md  (Class 3)
- The audit report must be committed in the same session it is produced — do not defer the commit to a later session (BLG-GOV-169). An audit report that exists only as an uncommitted working-tree file is not filed.
- The §11 CONFIG UPDATE block this run produces must be applied to `claude/audit.py`'s own CONFIG constants (`PRIOR_AUDIT_ID`, `PRIOR_AUDIT_OPEN_ITEMS`, `PRIOR_SCORES`, `COMPLETED_CYCLES`) in the same commit as the filed report — not deferred to a future session. This closes the recurring pattern first flagged at AUD-2026-07-20-006 and confirmed recurring a 3rd time at AUD-2026-08-08 (config still showed AUD-2026-07-27 when the true last audit was AUD-2026-08-03).
- In the same commit, also write `.claude_current_state.json.last_audit_id`, `last_audit_utc`, `last_audit_overall_score`, `last_audit_open_items` (count), and `last_audit_cycle_count` to this run's own values. These fields exist in the state schema and are surfaced at every session start, but no prior version of this file ever instructed writing them — confirmed stale at `AUD-2026-07-20` values (3 audits behind) at the start of the AUD-2026-08-08 run. Added AUD-2026-08-08-004.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRIOR AUDIT STATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STALENESS CHECK (mandatory, added AUD-2026-07-20-006 — 2 consecutive audits found this config block un-pasted):
Before trusting the constants below, locate the most recent filed report at
claude/cycles/<id>/audit_report_AUD-<date>.md and read its own §11 Config Update block.
If PRIOR_AUDIT_ID above does not match that report's own AUD-ID, the config was not pasted in
after that run — note the staleness explicitly in this run's own report preamble (as AUD-2026-07-20
did) and use the values from that report's §11 block as the actual baseline, not the stale constants
below.

Prior Audit ID:        {PRIOR_AUDIT_ID or "None — first run"}
Open items:            {PRIOR_AUDIT_OPEN_ITEMS or "None"}
Prior scores:          {PRIOR_SCORES}
Completed cycles:      {COMPLETED_CYCLES}
"""

# =========================
# OUTPUT SECTIONS (reference)
# =========================

OUTPUT_SECTIONS = [
    "## 1. Resolved Since Last Audit",
    "## 2. Health Scorecard",
    "## 3. Gap Register",
    "## 4. Stage Findings",
    "###  Stage 1 — Lifecycle Mapping",
    "###  Stage 2 — Behavioural Audit",
    "###  Stage 3 — Governance Integrity",
    "###  Stage 4 — Lifecycle Reliability",
    "###  Stage 5 — Token Budget Analysis",
    "###  Stage 6 — Engine Handoff Integrity",
    "###  Stage 7 — Prompt Architecture & Compression",
    "###  Stage 8 — Amendment Cycle Completeness",
    "###  Stage 9 — Single Source of Truth",
    "###  Stage 10 — Known Design Gaps & Deferred Patches",
    "###  Stage 11 — Best Practices Compliance",
    "###  Stage 12 — Routine Consolidation Analysis",
    "## 5. Improvements List",
    "###  5a. AUDIT_INDEX (JSON — Claude Code entry point)",
    "###  5b. Individual improvements (AUD-ID order, weight desc)",
    "## 6. Cross-Improvement Map",
    "## 7. Implementation Tiers",
    "## 8. Audit Summary",
    "## 9. SLA",
    "## 10. Scorecard Appendix",
    "## 11. Config Update",
]