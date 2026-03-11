# =========================
# CLAUDE LIFECYCLE AUDIT PACKAGE — v3
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
# - Skip that file and record it as a gap in the findings.
# - Do not invent content. Do not skip the stage entirely.
# - Flag the missing file as a potential Improvement in its own right
#   (Area: Lifecycle, Token Efficiency, or Automation as appropriate).

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
            "claude/system/roadmap_prompt.md"
        ],
        "check": (
            "Map all stages, engines, inputs/outputs, artefacts, and gates. "
            "Verify the README correctly describes the execution model and "
            "references the correct prompt file. Identify any lifecycle stages "
            "that are described but have no governing routine."
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
            "that should be extracted, and narrative prose replaceable by "
            "structured outputs."
        ),
        "tips": [1, 2, 4, 7]
    },
    {
        "stage": "3. Governance Integrity",
        "load": [
            "claude/charter/team_charter.md",
            "claude/charter/document_lifecycle_guide.md",
            "claude/agents/",         # all agent files — field-level read: Role, Status, Version headers only
            "claude/system/roadmap_prompt.md"  # Sections 1–4 and STEP -1.3 only
        ],
        "check": (
            "Verify role alignment and authority boundaries against the charter. "
            "Check for ghost roles (agent files not activated by any routine). "
            "Verify agent lifecycle compliance references point to "
            "claude/charter/document_lifecycle_guide.md, not an external path. "
            "Check first-cycle/zero-state handling."
        ),
        "tips": [2, 3]
    },
    {
        "stage": "4. Lifecycle Reliability",
        "load": [
            "claude/system/roadmap_prompt.md",  # STEP -1, STEP 0, STEP 8.5, STEP 12
            "claude/cycles/",                   # most recent cycle folder: run_manifest.md, lessons_learnt.md (field-level)
            "claude/roadmap/decision_log.md"    # header and entry count only
        ],
        "check": (
            "Check for deadlock conditions, halt paths without defined recovery, "
            "idempotency risks in the decision log and write plan, "
            "preflight marker file accumulation, and missing completion conditions. "
            "Verify the append-only invariant has structural enforcement, not just instruction."
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
            "Identify content duplicated across files. "
            "Find inline rule/schema blocks in prompts that should be extracted to "
            "canonical reference files. "
            "Check for single-source-of-truth violations (e.g. workforce capacity "
            "dual write targets, invariants defined in multiple places). "
            "Identify narrative replaceable by structured outputs or canonical references."
        ),
        "tips": [4, 6, 7]
    },
    {
        "stage": "6. Known Design Gaps",
        "load": [
            "claude/system/roadmap_prompt.md",         # STEP 4, STEP 5.1, STEP 11
            "claude/system/lessons_learnt_prompt.md",  # Section 1 Invocation Rule, Section 3
            "claude/cycles/",                          # most recent lessons_learnt.md — outstanding actions only
            "claude/ideas/",                           # submissions/ manifest if present; rejected_but_strong.md header
            "claude/scoring/scored_initiatives.md"     # header only — may not exist
        ],
        "check": (
            "Check: lessons learnt invocation guard is structural (not advisory). "
            "Check: idea submission quota has a tracking mechanism. "
            "Check: scoring schema exists and defines a fixed scale. "
            "Check: Challenger failure has a defined recovery path. "
            "Check: amendment cycle has a governing template. "
            "Check: Re-evaluate state has a maximum age / cross-run enforcement. "
            "Note any outstanding actions from prior cycles not yet actioned."
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
            "Identify logic blocks repeated across both prompt files "
            "(e.g. invariant lists, lifecycle compliance checks, role verification). "
            "Recommend extraction to canonical shared modules. "
            "Check whether both prompts carry a version field and change log."
        ),
        "tips": [6]
    },
    {
        "stage": "8. Manus Logic / Rule Centralisation",
        "load": [
            "claude/system/roadmap_prompt.md",              # Section 9 Invariants; Decision Log Invariant; STEP 8.5
            "claude/charter/document_lifecycle_guide.md",   # Section 9 Known Deviation Standard
            "claude/README.md"                              # Section 3 Core Invariants
        ],
        "check": (
            "Identify hard rules and valid state transitions that are "
            "embedded inline across multiple documents. "
            "Recommend centralisation into a shared invariants/rules file "
            "(e.g. claude/system/invariants.md or manus_rules.json). "
            "Check that halt conditions have defined recovery procedures. "
            "Check that write safety gate (STEP 8.5) failure has a defined output format."
        ),
        "tips": [2, 4]
    },
    {
        "stage": "9. Best Practices",
        "load": [
            "claude/system/roadmap_prompt.md",         # STEP -1.3, STEP -1.4, STEP 9 write plan
            "claude/system/lessons_learnt_prompt.md",  # Section 6 Action Rules
            "claude/cycles/",                          # most recent cycle — lessons_learnt.md summary only
            "claude/charter/document_lifecycle_guide.md"  # Class 6 requirements
        ],
        "check": (
            "Artefact structure compliance (Class 6 headers, version, change log). "
            "Agent manifest vs full-file reads in preflight. "
            "Cycle artefact schemas defined inline vs extractable. "
            "Idempotency: decision log structural enforcement. "
            "Dry-run mode availability. "
            "Strict/standard mode parity. "
            "Bootstrap / zero-state path for first run. "
            "GitHub issue sync rule (if any external tracking is referenced)."
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

Missing file rule: if a file in a stage's "load" list does not exist, skip it, flag it as a gap finding, and continue the stage on available files. Do not invent content.

For each stage in STAGE_CHECKLIST:
1. Load only the files listed in "load" (apply tips from "tips" to minimise token cost).
2. Audit the concerns listed in "check".
3. Identify improvements in any of these categories:
   missing coverage | unclear transitions | redundant/unused artefacts | overprocessing |
   repeated logic | narrative replaceable by structured outputs | first-cycle/zero-state issues |
   idempotency risks | preflight duplication | dry-run consistency | lessons learnt/meta-review gaps |
   role/authority misalignment | hard gate violations | strict/standard mode parity |
   amendment cycle correctness | GitHub issue sync gaps.

Return up to {MAX_IMPROVEMENTS} improvements, ordered by priority. Use this format exactly:

### Improvement #<n>
**Title:** <Short title>
**Area:** Lifecycle | Prompt | State | Governance | Token Efficiency | Automation | Manus Logic
**Problem:** <Concise issue description>
**Evidence:** <Exact file path(s) + section/step>
**Why it matters:** <Impact on efficiency, governance, token usage, or reliability>
**Recommended change:** <Actionable change with target file path>
**Expected benefit:** <Efficiency, token, reliability, or governance improvement>
**Token impact:** Saves | Neutral | Costs — <one-line justification>
**Implementation effort:** Low | Medium | High
**Best Practice Alignment:** Yes | Partially | No

No commentary. No praise. Max {MAX_IMPROVEMENTS} improvements.
"""

# -------------------------
# OUTPUT TEMPLATE (reference)
# -------------------------
OUTPUT_TEMPLATE = """
### Improvement #<n>
**Title:** <Short title>
**Area:** Lifecycle | Prompt | State | Governance | Token Efficiency | Automation | Manus Logic
**Problem:** <Concise issue description>
**Evidence:** <Exact file path(s) + section/step>
**Why it matters:** <Impact on efficiency, governance, token usage, or reliability>
**Recommended change:** <Actionable change with target file path>
**Expected benefit:** <Efficiency, token, reliability, or governance improvement>
**Token impact:** Saves | Neutral | Costs — <one-line justification>
**Implementation effort:** Low | Medium | High
**Best Practice Alignment:** Yes | Partially | No
"""
