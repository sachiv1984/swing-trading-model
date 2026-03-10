# =========================
# CLAUDE LIFECYCLE AUDIT PACKAGE
# =========================

# 1. ULTRA-MINIMAL AUDIT PROMPT
PROMPT = """
Audit the Sprint Planning Operational Playbook and all referenced prompts, charters, strategies, agent definitions, and shared standards for lifecycle completeness, token efficiency, document compression, single source of truth, reusable prompts, and enforceable Manus logic. Cover all stages: Idea → Roadmap → Release Planning → Backlog Slice → Sprint Planning → Execution → Verification → Closure → Next Cycle. Identify: missing coverage, unclear transitions, redundant/unused artefacts, overprocessing, repeated logic, narrative replaceable by structured outputs, first-cycle/zero-state issues, idempotency risks, preflight duplication, dry-run consistency, lessons learnt/meta-review gaps, role/authority misalignment, hard gate violations, strict/standard mode parity, amendment cycle correctness, GitHub issue sync gaps. For each improvement, return: Title, Area (Lifecycle | Prompt | State | Governance | Token Efficiency | Automation | Manus Logic), Problem, Evidence (file + step/section), Why it matters, Recommended change, Expected benefit, Token impact (Saves | Neutral | Costs), Implementation effort (Low | Medium | High), Best Practice Alignment (Yes | Partially | No). Prioritize by token savings, lifecycle simplification, artefact/prompt redundancy, governance preservation. Max 20 improvements. No commentary or praise.
"""

# 2. TOKEN-EFFICIENT STAGE CHECKLIST
STAGE_CHECKLIST = [
    {
        "stage": "1. Lifecycle Mapping",
        "load": ["Playbook"],
        "check": "Map stages, engines, inputs/outputs, artefacts, gates",
        "note": "Summary only"
    },
    {
        "stage": "2. Waste & Token",
        "load": ["Phase artefacts"],
        "check": "Redundant artefacts, full-doc reads, repeated info",
        "note": "Load full artefacts only if verifying duplicates"
    },
    {
        "stage": "3. Governance",
        "load": [".claude_current_state.json", "charters", "agent definitions", "playbook"],
        "check": "Role alignment, authority boundaries, first-cycle handling, ghost roles",
        "note": "Field-level reads"
    },
    {
        "stage": "4. Lifecycle Reliability",
        "load": ["State files", "preflight logs"],
        "check": "Deadlocks, halts, escalations, manual recovery",
        "note": "Field-level reads"
    },
    {
        "stage": "5. Document Compression / Single Source",
        "load": ["All artefacts"],
        "check": "Duplicates, narrative→structured, canonical references",
        "note": "Load metadata/sections only"
    },
    {
        "stage": "6. Known Design Areas",
        "load": ["Playbook sections", "amendment artefacts", "lessons learnt", "stage4_issue_manifest.json"],
        "check": "Phase 1M gaps, amendment constraints, gate timing, backlog locks, lessons/meta, GitHub sync",
        "note": "Only referenced files"
    },
    {
        "stage": "7. Common Prompts",
        "load": ["Engine prompts"],
        "check": "Repeated logic/structured outputs, recommend canonical prompts",
        "note": "Load once per engine"
    },
    {
        "stage": "8. Manus Logic",
        "load": ["Playbook", "prompts", "state files"],
        "check": "Hard rules, valid transitions, repeated checks → centralize in manus_rules.json",
        "note": "Load rule-relevant sections only"
    },
    {
        "stage": "9. Best Practices",
        "load": ["Artefacts", "prompts", "state files", "lessons/meta"],
        "check": "Artefact structure, modular prompts, state ops, idempotency, dry-run, audit logs, consolidation, automation, token efficiency",
        "note": "Minimal field-level content"
    }
]

# 3. STRUCTURED OUTPUT TEMPLATE
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

# =========================
# TOKEN-SAVING TIPS (Optional Reference)
# =========================
TOKEN_TIPS = [
    "Lazy-load context per stage",
    "Field-level reads for state files & artefacts",
    "Shared preflight results for downstream engines",
    "Replace duplicate content with canonical references",
    "Dry-run: load only relevant files; no writes/locks",
    "Prompt modules: reference canonical logic instead of embedding",
    "Structured outputs (tables/JSON) instead of narrative prose"
]