# =========================
# CLAUDE LIFECYCLE AUDIT PACKAGE — v4
# =========================

# -------------------------
# CONFIG
# -------------------------
SCOPE = "claude/"
MAX_IMPROVEMENTS = 20

# -------------------------
# MISSING FILE HANDLING RULE
# -------------------------
# If a file listed in a stage's "load" does not exist:
# - Record it immediately as a GAP FINDING using the format below.
# - Do not invent content. Do not skip the stage entirely.
# - Flag the missing file as a potential Improvement in its own right
#   (Area: Lifecycle, Token Efficiency, or Automation as appropriate).
# - Continue the stage on all available files.
#
# GAP FINDING FORMAT (emit before any Improvement for this stage):
#
#   ⚠ GAP — Stage <n>
#   File: <exact path>
#   Status: Not found | Partially loaded | Header only
#   Impact: <one sentence — what audit check is blind without this file>
#   Flag as Improvement: Yes | No
#
# All gap findings must appear in the output under a "## Gap Register" section
# that precedes the numbered improvements list.

# -------------------------
# TOKEN-EFFICIENT TIPS
# -------------------------
TOKEN_TIPS = {
    1: "Lazy-load context per stage — load only files listed in 'load'",
    2: "Field-level reads for state files & artefacts — do not load full file if only headers needed",
    3: "Shared preflight results — reuse governance file reads across stages",
    4: "Replace duplicate content with canonical references",
    5: "Dry-run awareness — note write-path risks without executing writes",
    6: "Prompt modules — reference canonical logic by path instead of embedding inline",
    7: "Structured outputs (tables/JSON) instead of narrative prose"
}

# -------------------------
# STAGE CHECKLIST — REAL claude/ FILE PATHS
# -------------------------
STAGE_CHECKLIST = [
    {
        "stage": "1. Lifecycle Mapping",
        "load": [
            "claude/README.md",
            "claude/system/roadmap_prompt.md",
            "claude/system/OPERATIONAL_GUIDE.md"   # §4 phase table — header scan only
        ],
        "check": (
            "Map all stages, engines, inputs/outputs, artefacts, and gates. "
            "Verify the README correctly describes the execution model, references the correct "
            "prompt file paths (not stale names), and lists all governed routines — not just "
            "Roadmap Rebalance. Identify any lifecycle stages that are described in the "
            "OPERATIONAL_GUIDE but have no governing routine, or are governed but absent "
            "from the README. Flag any broken file path references in the README. "
            "Check that the README lifecycle guide filename matches the actual file on disk."
        ),
        "tips": [1, 2]
    },
    {
        "stage": "2. Waste & Token Efficiency",
        "load": [
            "claude/roadmap/current_roadmap.md",
            "claude/backlog/backlog.md",
            "claude/roadmap/decision_log.md",
            "claude/system/roadmap_prompt.md"
        ],
        "check": (
            "Detect redundant artefacts, repeated information across files, "
            "overprocessing in step definitions, inline schema/rule blocks "
            "that should be extracted, and narrative prose replaceable by structured outputs. "
            "For each inline block identified (invariants, halt formats, schema definitions), "
            "estimate the token cost: count approximate lines in the block × average tokens "
            "per line (assume 8 tokens/line), then multiply by the number of engine loads "
            "per cycle that embed the block. Report as: "
            "'~<N> lines × 8 tokens × <M> loads/cycle = ~<total> tokens/cycle saved if extracted.' "
            "Identify all files where the same content appears more than once."
        ),
        "tips": [1, 2, 4, 7]
    },
    {
        "stage": "3. Governance Integrity",
        "load": [
            "claude/charter/team_charter.md",
            "claude/charter/document_lifecycle_guide.md",
            "claude/agents/",         # ENUMERATE ALL agent files — field-level read per file:
                                      # extract Role, Status, Version header fields only.
                                      # Build a complete list: [filename → role name → status].
                                      # Do not skip any file. Record any file that cannot be
                                      # read as a Gap Finding for this stage.
            "claude/system/roadmap_prompt.md",      # Sections 1–4 and STEP -1.3 only
            "claude/system/OPERATIONAL_GUIDE.md"    # §7 Governing Routines list only
        ],
        "check": (
            "Step 1 — Build the agent roster: list every agent file found in claude/agents/ "
            "with its declared role name and status. Record any agent file missing a "
            "Role or Status header as a compliance gap. "
            "Step 2 — Ghost role check: for each agent role, confirm it is activated by "
            "at least one governed routine in OPERATIONAL_GUIDE §7 or roadmap_prompt STEP -1.3. "
            "Any role with a charter file but no governing routine activation is a ghost role. "
            "Step 3 — Authority boundary check: verify that every decision-authority role "
            "named in engine prompts (STEP -1.3 required roles list) has a corresponding "
            "agent charter file. Flag any role named in prompts but absent from claude/agents/. "
            "Step 4 — Lifecycle compliance references: verify agent files reference "
            "claude/charter/document_lifecycle_guide.md (not any external path or stale filename). "
            "Step 5 — First-cycle / zero-state handling: confirm a bootstrap path exists "
            "for cycles where no prior cycle folder is present."
        ),
        "tips": [2, 3]
    },
    {
        "stage": "4. Lifecycle Reliability",
        "load": [
            "claude/system/roadmap_prompt.md",      # STEP -1, STEP 0, STEP 8.5, STEP 12
            "claude/system/OPERATIONAL_GUIDE.md",   # §4.1 state machine table
            "claude/system/lifecycle_schema.json",  # full — if absent, record as Gap Finding
            "claude/cycles/",                       # most recent cycle folder:
                                                    #   run_manifest.md (preflight status table only)
                                                    #   lessons_learnt.md or lessons_learnt_cycle.md
                                                    #   (outstanding actions section only)
                                                    # If folder or files absent: record as Gap Finding
            "claude/roadmap/decision_log.md"        # header and entry count only
        ],
        "check": (
            "Check for deadlock conditions: any state from which no forward transition exists "
            "and no recovery path is defined. "
            "Check halt paths: every hard gate halt must have a defined output format and a "
            "resume instruction. Verify against shared_standards.md §10 halt format. "
            "Check idempotency risks: for every write operation in the roadmap engine "
            "(decision log append, backlog commit, state file update), confirm a guard exists "
            "that prevents duplicate output on re-invocation. "
            "Check preflight marker file accumulation: verify marker files created at STEP -1 "
            "are cleaned up on success and on halt. "
            "Check the append-only invariant on decision_log.md: is enforcement structural "
            "(e.g. append-only flag, write plan gate) or advisory (text instruction only)? "
            "Check outstanding actions from the most recent lessons_learnt file: list any "
            "actions that have no recorded resolution and no carry-forward entry. These are "
            "active governance debts and must each appear as an evidence item in a finding."
        ),
        "tips": [2, 3, 5]
    },
    {
        "stage": "5. Document Compression / Single Source of Truth",
        "load": [
            "claude/system/roadmap_prompt.md",          # Sections 9, 10; STEP 6, STEP 7, STEP 11 inline schemas
            "claude/system/lessons_learnt_prompt.md",   # full
            "claude/README.md",
            "claude/charter/document_lifecycle_guide.md" # invariant definitions only
        ],
        "check": (
            "Identify content duplicated across files. For each duplicate identified, record: "
            "(a) the content description, (b) all file paths where it appears, "
            "(c) token cost estimate using the formula: lines × 8 tokens × engine loads/cycle. "
            "Find inline rule/schema blocks in prompts that should be extracted to canonical "
            "reference files — apply the same token cost formula. "
            "Check for single-source-of-truth violations: workforce_capacity dual write targets, "
            "invariants defined in multiple places, halt formats defined per-engine rather than "
            "once in shared_standards.md. "
            "Check sprint_backlog_index.json schema: is it defined inline in sprint_planning_prompt "
            "and again in execution_prompt, or is there a single canonical definition? "
            "Identify narrative replaceable by structured outputs or canonical references."
        ),
        "tips": [4, 6, 7]
    },
    {
        "stage": "6. Known Design Gaps",
        "load": [
            "claude/system/roadmap_prompt.md",         # STEP 4, STEP 5.1, STEP 11
            "claude/system/lessons_learnt_prompt.md",  # Section 1 Invocation Rule, Section 3
            "claude/cycles/",                          # most recent lessons_learnt.md or
                                                       # lessons_learnt_cycle.md —
                                                       # outstanding actions section only.
                                                       # If file absent: record as Gap Finding.
            "claude/ideas/",                           # submissions/ manifest if present;
                                                       # rejected_but_strong.md header only.
                                                       # If absent: record as Gap Finding.
            "claude/scoring/scored_initiatives.md"     # header only — if absent: Gap Finding
        ],
        "check": (
            "Check 1 — Lessons learnt invocation guard: is the guard in lessons_learnt_prompt.md §1 "
            "structural (machine-enforceable via token/parameter) or advisory (text instruction only)? "
            "Advisory = gap finding. "
            "Check 2 — Idea submission quota tracking: does ideas_window.json carry a "
            "per-agent submission count field? If not, the quota rule has no enforcement mechanism. "
            "Check 3 — Scoring schema fixed scale: does scored_initiatives.md carry a "
            "declared scoring scale definition, or is it implied by column headers only? "
            "Check 4 — Challenger failure recovery: does roadmap_prompt STEP 5.1 define a "
            "recovery path when the Challenger produces no §13-referenced counter-argument "
            "for a Score-4 or Score-5 item? If not, this is an uncovered failure mode. "
            "Check 5 — Amendment cycle template: does a governing template exist for the "
            "amendment record format, or is format implied by prose instructions only? "
            "Check 6 — Re-evaluate state maximum age: does STEP -1.5 or any preflight "
            "enforce a cross-run maximum age for initiatives in Re-evaluate state? "
            "Check 7 — amendment_lessons.md status: is this artefact still listed in §13 "
            "Artefact Register? Does it have a producing step, schema, and lessons loop connection? "
            "If it is a retained-for-compat ghost artefact, flag for retirement or formalisation. "
            "Note any outstanding actions from prior cycle lessons_learnt not yet actioned."
        ),
        "tips": [1, 4, 5]
    },
    {
        "stage": "7. Common Prompt Identification",
        "load": [
            "claude/system/roadmap_prompt.md",        # full — identify repeated logic blocks
            "claude/system/lessons_learnt_prompt.md"  # full
        ],
        "check": (
            "Identify logic blocks repeated across both prompt files. For each repeated block: "
            "(a) describe the content, (b) list file paths and sections, "
            "(c) estimate token cost: lines × 8 tokens × loads/cycle for each copy. "
            "Recommend extraction to canonical shared modules with reference-by-path. "
            "Check whether both prompts carry a version field, Last Updated field, and change log. "
            "Check whether the prompt change log (claude/system/prompt_change_log.md) records "
            "every version bump visible in both prompts' change logs — flag any version bump "
            "in a prompt changelog that has no corresponding entry in prompt_change_log.md."
        ),
        "tips": [6]
    },
    {
        "stage": "8. Manus Logic / Rule Centralisation",
        "load": [
            "claude/system/roadmap_prompt.md",              # Section 9 Invariants; Decision Log Invariant; STEP 8.5
            "claude/charter/document_lifecycle_guide.md",   # Section 9 Known Deviation Standard
            "claude/README.md",                             # Section 3 Core Invariants
            "claude/system/shared_standards.md",            # §10 halt format; §13 dry-run standard
            "claude/system/lifecycle_schema.json"           # if absent: Gap Finding — state machine has no machine-readable authority
        ],
        "check": (
            "Identify hard rules and valid state transitions embedded inline across multiple documents. "
            "For each rule appearing in more than one document: record all locations, classify as "
            "drift risk, and recommend centralisation target file. "
            "Recommend centralisation into a shared invariants/rules file "
            "(claude/system/invariants.md) if it does not already exist. "
            "Check halt format: is the halt report format defined once in shared_standards.md §10 "
            "and referenced by path from all engines, or is it re-specified inline per engine? "
            "If inline: estimate total duplicated tokens (count halt format block lines × 8 × number "
            "of engines that embed it). "
            "Check that every halt condition has a defined resume instruction. "
            "Check that the write safety gate (STEP 8.5) failure has a defined output format "
            "that matches the shared_standards.md §10 halt format schema. "
            "Check lifecycle_schema.json: does it exist and encode all transitions from "
            "OPERATIONAL_GUIDE §4.1? If absent, the state machine is prose-only — flag as "
            "a reliability and interpretability gap."
        ),
        "tips": [2, 4]
    },
    {
        "stage": "9. Best Practices",
        "load": [
            "claude/system/roadmap_prompt.md",          # STEP -1.3, STEP -1.4, STEP 9 write plan
            "claude/system/shared_standards.md",        # §9 header quick-ref; §10 halt; §13 dry-run; §14 preflight fields; §15 spec debt
            "claude/system/lessons_learnt_prompt.md",   # Section 6 Action Rules (if present)
            "claude/cycles/",                           # most recent cycle — lessons_learnt summary only
            "claude/charter/document_lifecycle_guide.md" # Class 6 requirements
        ],
        "check": (
            "Run each check below as a named sub-check. Record PASS, FAIL, or NOT CHECKABLE "
            "(if a required file was a Gap Finding). "
            "\n"
            "BP-01 Class 6 headers: do all files in claude/system/ carry Owner, Status: Active, "
            "Version, and Last Updated fields? "
            "\n"
            "BP-02 Agent manifest vs full-file reads: does roadmap_prompt STEP -1.3 use field-level "
            "reads (Role, Status, Version only) for agent files, or does it load full agent files? "
            "\n"
            "BP-03 Cycle artefact schemas: are sprint_backlog_index.json schema and "
            "stage4_issue_manifest.json schema defined in shared_standards.md, or inline in engine prompts? "
            "\n"
            "BP-04 Idempotency — decision log: does the decision log have a structural append-only "
            "guard (write plan gate, pre-commit check), or is append-only enforced by instruction only? "
            "\n"
            "BP-05 Dry-run mode: does the Roadmap Rebalance engine (roadmap_prompt.md) support "
            "a --dry-run flag? If absent, flag as missing — this is the highest-impact engine "
            "and the only one without dry-run support. "
            "\n"
            "BP-06 Strict/standard mode parity: for every rule declared mode-independent "
            "(e.g. net-zero displacement, lessons learnt invocation), verify the prompt text "
            "explicitly states 'mode-independent' or 'applies in both strict and standard mode.' "
            "\n"
            "BP-07 Bootstrap / zero-state path: does each engine define behaviour when no prior "
            "cycle folder exists? Record which engines have an explicit zero-state path and which do not. "
            "\n"
            "BP-08 GitHub issue sync: does stage4_issue_manifest.json have a declared schema "
            "in shared_standards.md? Does the sync gh command have an idempotency guard (IMP-35 gap 4)? "
            "Does governance_sync.yml close issues by numeric ID (not string ST-id)? "
            "Flag any known defects from execution_escalations.md that have not been resolved. "
            "\n"
            "BP-09 Scored initiatives class: are scored_initiatives_<cycle_id>.md files "
            "declared as Class 3 (Operational Record) or Class 4 (Planning Document)? "
            "Class 4 is non-compliant for immutable cycle records. "
            "\n"
            "BP-10 Artefact register completeness: does OPERATIONAL_GUIDE §13 list every "
            "artefact directory and file type produced by all engines, including claude/scoring/, "
            "claude/ideas/rejected_but_strong.md, and lifecycle_schema.json?"
        ),
        "tips": [1, 2, 5, 7]
    }
]

# -------------------------
# PROMPT
# -------------------------
PROMPT = f"""
Priority order for improvements: token savings → lifecycle simplification → artefact/prompt redundancy → governance preservation.

Scope: {SCOPE}

---

## EXECUTION INSTRUCTIONS

### Phase 0 — Gap Register (MANDATORY FIRST OUTPUT)

Before producing any improvements, produce a "## Gap Register" section.

For every file listed in any stage's "load" that cannot be found or read:
- Record it with this format:

  ⚠ GAP — Stage <n>
  File: <exact path>
  Status: Not found | Partially loaded | Header only
  Impact: <one sentence — what audit check is blind without this file>
  Promote to Improvement: Yes | No

If a file is partially loaded (field-level only), record it as "Partial — field-level" with the fields successfully read.

If no gaps are found, write: "No gaps detected — all stage load files successfully read."

The Gap Register is non-optional. An audit without a Gap Register is incomplete.

---

### Phase 1 — Stage Audits

For each stage in STAGE_CHECKLIST:
1. Load only the files listed in "load" (apply tips from "tips" to minimise token cost).
2. For Stage 3: enumerate ALL agent files found in claude/agents/ — list each filename and its extracted Role and Status header values in a table before proceeding to the checks. Do not skip any file. Files that cannot be read are Gap Findings.
3. For Stage 9: run each named sub-check (BP-01 through BP-10) and record PASS, FAIL, or NOT CHECKABLE as a structured table before deriving improvements.
4. Audit the concerns listed in "check".
5. Identify improvements using the categories below.

---

### Phase 2 — Improvements List

Return up to {MAX_IMPROVEMENTS} improvements, ordered by priority. Use this format exactly:

### Improvement #<n>
**Title:** <Short title>
**Area:** Lifecycle | Prompt | State | Governance | Token Efficiency | Automation | Manus Logic
**Problem:** <Concise issue description>
**Evidence:** <Exact file path(s) + section/step>
**Why it matters:** <Impact on efficiency, governance, token usage, or reliability>
**Recommended change:** <Actionable change with target file path>
**Expected benefit:** <Efficiency, token, reliability, or governance improvement>
**Token impact:** Saves | Neutral | Costs — <quantified: ~N lines × 8 tokens × M loads/cycle = ~X tokens/cycle>
**Implementation effort:** Low | Medium | High
**Best Practice Alignment:** Yes | Partially | No

Improvement categories:
   missing coverage | unclear transitions | redundant/unused artefacts | overprocessing |
   repeated logic | narrative replaceable by structured outputs | first-cycle/zero-state issues |
   idempotency risks | preflight duplication | dry-run consistency | lessons learnt/meta-review gaps |
   role/authority misalignment | hard gate violations | strict/standard mode parity |
   amendment cycle correctness | GitHub issue sync gaps | artefact class misclassification |
   missing machine-readable schema | disconnected artefact | advisory-only guard.

---

### Phase 3 — Cross-Improvement Conflict & Dependency Map

After the improvements list, produce a "## Implementation Map" section with two sub-sections:

#### Dependencies (implement A before B)
List any improvement pairs where one must be completed before the other is coherent.
Format: Improvement #X must precede Improvement #Y — <one sentence reason>.

#### Conflicts (implementing A may affect B)
List any improvement pairs that touch the same file or concept and may create inconsistency if applied independently.
Format: Improvement #X and Improvement #Y both affect <file/concept> — coordinate to avoid re-work.

If no dependencies or conflicts exist, write "None identified."

---

### Phase 4 — Implementation Tiers

After the Implementation Map, produce a "## Implementation Tiers" section:

**Tier 1 — Do first (prerequisite fixes, broken references, low effort):**
List improvement numbers with one-line rationale.

**Tier 2 — Do second (structural improvements, medium effort, no Tier 1 dependencies):**
List improvement numbers with one-line rationale.

**Tier 3 — Do last (schema extractions, new files, high effort or Tier 1/2 dependencies):**
List improvement numbers with one-line rationale.

---

No commentary outside the defined sections. No praise. Max {MAX_IMPROVEMENTS} improvements.
"""

# -------------------------
# OUTPUT TEMPLATE (reference)
# -------------------------
OUTPUT_TEMPLATE = """
## Gap Register

⚠ GAP — Stage <n>
File: <exact path>
Status: Not found | Partially loaded | Header only
Impact: <one sentence>
Promote to Improvement: Yes | No

---

### Improvement #<n>
**Title:** <Short title>
**Area:** Lifecycle | Prompt | State | Governance | Token Efficiency | Automation | Manus Logic
**Problem:** <Concise issue description>
**Evidence:** <Exact file path(s) + section/step>
**Why it matters:** <Impact on efficiency, governance, token usage, or reliability>
**Recommended change:** <Actionable change with target file path>
**Expected benefit:** <Efficiency, token, reliability, or governance improvement>
**Token impact:** Saves | Neutral | Costs — <~N lines × 8 tokens × M loads/cycle = ~X tokens/cycle>
**Implementation effort:** Low | Medium | High
**Best Practice Alignment:** Yes | Partially | No

---

## Implementation Map

#### Dependencies (implement A before B)
Improvement #X must precede Improvement #Y — <reason>.

#### Conflicts (implementing A may affect B)
Improvement #X and Improvement #Y both affect <file/concept> — coordinate to avoid re-work.

---

## Implementation Tiers

**Tier 1 — Do first:**
- #X — <one-line rationale>

**Tier 2 — Do second:**
- #X — <one-line rationale>

**Tier 3 — Do last:**
- #X — <one-line rationale>
"""