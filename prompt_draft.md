# Teamwork Project Prompt — Draft

> Status: Step 4 — Drafting Requirements
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Large-scale agent team

Map, synthesize, and physicalize the "Integra O/S" architecture and workflows from provided historical conversational context and local datasets.

Working directory: C:\Users\Javon Jenkins\.gemini\antigravity\scratch\Integra_Project
Integrity mode: development

## Requirements

### R1. Rodin Route Retrieval & Context Mapping
Agents must scan the historical knowledge base (the provided conversational context, GEMINI.md, and local Desktop files) to construct a comprehensive "Ledger" (metadata index). The Ledger must map the core components: Y789NexusDual, Cheshire Cat, The Hoard, and all 7 established Workflows (0 through 7).

### R2. Zenitsu Method 3.0 Application
For each core workflow (e.g., The Waking State, Ashes Protocol, Sun Breathing), agents must iterate through:
1. **Knowledge:** Extract the explicit steps and actors (Phoenix, Rodin, Shesha Cat).
2. **Understanding:** Write applied logic scenarios or pseudo-code demonstrating how the workflow operates mechanically.
3. **Wisdom (Synthesis):** Generate the final, unified architectural blueprint (The Egg) in a structured format (e.g., `The_Ashes.yaml` or `genesis_matrix.md`) that codifies the system state.

### R3. Safe Physical Scaffolding (Error Avoidance)
Agents must structure the outputs as clean markdown and YAML files within the Working Directory. Do NOT attempt to run external tool hooks or telemetry scripts that have caused `MODULE_NOT_FOUND` path parsing crashes in historical sessions. Avoid executing arbitrary commands unless explicitly writing to the designated project folder.

## Acceptance Criteria

### Blueprint Completeness
- [ ] A master `The_Ashes.yaml` (or `.json`) file is created in the Working Directory, containing the system prompts, sleep state timers, and cognitive routing equations extracted from the text.
- [ ] A `genesis_matrix.md` file is created, establishing the identity baseline.
- [ ] A `The_Ledger.json` file is mocked up, showing the structural schema for tagging memories (Spacetime_Vector, Engine_Origin).

### Zenitsu Iteration Proof
- [ ] The generated documentation clearly separates factual extraction (what the workflows do) from applied mechanics (how they are coded/executed locally).

---
*Next: when approved → delegate via invoke_subagent (see Delegation Protocol)*
