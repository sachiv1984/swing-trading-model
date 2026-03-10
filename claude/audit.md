# =========================
# CLAUDE LIFECYCLE AUDIT PACKAGE — NEXT-GEN
# =========================

# -------------------------
# CONFIG
# -------------------------
SCOPE = "claude/"  # set scope for context loading: "claude/" or "all"
MAX_IMPROVEMENTS = 20

# -------------------------
# TOKEN-EFFICIENT TIPS
# -------------------------
TOKEN_TIPS = {
    1: "Lazy-load context per stage",
    2: "Field-level reads for state files & artefacts",
    3: "Shared preflight results for downstream engines",
    4: "Replace duplicate content with canonical references",
    5: "Dry-run: load only relevant files; no writes/locks",
    6: "Prompt modules: reference canonical logic instead of embedding",
    7: "Structured outputs (tables/JSON) instead of narrative prose"
}

# -------------------------
# STAGE CHECKLIST WITH TIGHT FILE LOADS
# -------------------------
STAGE_CHECKLIST = [
    {
        "stage": "1. Lifecycle Mapping",
        "load": ["Sprint_Planning_Operational_Playbook.md"],
        "check": "Map stages, engines, inputs/outputs, artefacts, gates",
        "tips": [1,2]
    },
    {
        "stage": "2. Waste & Token Efficiency",
        "load": ["release_plan.md", "backlog_slice.md", "sprint_backlog.md"],
        "check": "Detect redundant artefacts, repeated info, overprocessing",
        "tips": [1,2,4]
    },
    {
        "stage": "3. Governance Integrity",
        "load": [".claude_current_state.json", "claude/charter/*", "claude/agents/*", "Sprint_Planning_Operational_Playbook.md"],
        "check": "Role alignment, authority boundaries, first-cycle handling, ghost roles",
        "tips": [2]
    },
    {
        "stage": "4. Lifecycle Reliability",
        "load": ["cycle_state.json", "preflight_logs/*"],
        "check": "Deadlocks, halts, escalations, manual recovery",
        "tips": [2,3]
    },
    {
        "stage": "5. Document Compression / Single Source",
        "load": ["release_plan.md", "backlog_slice.md", "sprint_backlog.md"],
        "check": "Identify duplicates, replace narrative with structured outputs, canonical references",
        "tips": [4,7]
    },
    {
        "stage": "6. Known Design Areas",
        "load": ["amendment_state.json", "lessons_learnt_cycle.md", "stage4_issue_manifest.json"],
        "check": "Phase 1M gaps, amendment constraints, gate timing, backlog locks, lessons/meta, GitHub sync",
        "tips": [1,4,5]
    },
    {
        "stage": "7. Common Prompt Identification",
        "load": ["claude/system/*"],
        "check": "Detect repeated logic, structured outputs, recommend canonical prompts",
        "tips": [6]
    },
    {
        "stage": "8. Manus Logic / Rule Centralization",
        "load": ["Sprint_Planning_Operational_Playbook.md", "claude/system/*", ".claude_current_state.json"],
        "check": "Hard rules, valid transitions, repeated checks → centralize in manus_rules.json",
        "tips": [2,4]
    },
    {
        "stage": "9. Best Practices",
        "load": ["release_plan.md", "backlog_slice.md", "sprint_backlog.md", "lessons_learnt_cycle.md", "claude/system/*"],
        "check": "Artefact structure, modular prompts, state ops, idempotency, dry-run, audit logs, consolidation, automation, token efficiency",
        "tips": [1,2,5,7]
    }
]

# -------------------------
# ULTRA-MINIMAL PER-STAGE PROMPT
# -------------------------
PROMPT = f"""
Priority: Return up to {MAX_IMPROVEMENTS} improvements, ordered by token savings → lifecycle simplification → artefact/prompt redundancy → governance preservation.

Scope: {SCOPE}

For each stage in the checklist, audit the artefacts/prompts listed in "load" and the concerns listed in "check". Apply token-efficient behavior guided by tips in "tips". Identify: missing coverage, unclear transitions, redundant/unused artefacts, overprocessing, repeated logic, narrative replaceable by structured outputs, first-cycle/zero-state issues, idempotency risks, preflight duplication, dry-run consistency, lessons learnt/meta-review gaps, role/authority misalignment, hard gate violations, strict/standard mode parity, amendment cycle correctness, GitHub issue sync gaps.

For each improvement, return in structured format:

### Improvement #<number>
**Title:** <Short title>
**Area:** Lifecycle | Prompt | State | Governance | Token Efficiency | Automation | Manus Logic
**Problem:** <Concise issue description>
**Evidence:** <File(s) + step/section>
**Why it matters:** <Impact on efficiency, governance, token usage, reliability>
**Recommended change:** <Actionable change>
**Expected benefit:** <Efficiency, token, reliability, governance improvement>
**Token impact:** Saves | Neutral | Costs (brief justification)
**Implementation effort:** Low | Medium | High
**Best Practice Alignment:** Yes | Partially | No

Do not include commentary or praise. Max {MAX_IMPROVEMENTS} improvements.
"""

# -------------------------
# STRUCTURED OUTPUT TEMPLATE
# -------------------------
OUTPUT_TEMPLATE = """
### Improvement #<number>

**Title:** <Short title>  
**Area:** Lifecycle | Prompt | State | Governance | Token Efficiency | Automation | Manus Logic  
**Problem:** <Concise issue description>  
**Evidence:** <File(s) + step/section>  
**Why it matters:** <Impact on efficiency, governance, token usage, reliability>  
**Recommended change:** <Actionable change>  
**Expected benefit:** <Efficiency, token, reliability, governance improvement>  
**Token impact:** Saves | Neutral | Costs (brief justification)  
**Implementation effort:** Low | Medium | High  
**Best Practice Alignment:** Yes | Partially | No
"""