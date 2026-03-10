---
name: game-engine-generator
description: Generate desire-driven game narrative engine system prompts supporting research, narrative design, decision systems, data processing, and code generation. Use when the user needs to (1) create game narrative engines based on mimetic desire theory, (2) generate dynamic rule systems driven by desire triangles (Subject/Model/Object/Scapegoat), (3) build three-phase narrative loops (convergence → homogenization → scapegoat), (4) produce structured system prompts for game design or interactive fiction, or (5) transform philosophical/theoretical texts into executable game engine specifications.
---

# Game Engine Generator

Generate system prompts for desire-driven game narrative engines that cover five domains: research, narrative, decision-making, data processing, and code generation.

## Workflow

1. **Collect inputs**: Read user-provided world fragments, character descriptions, or theoretical texts from workspace
2. **Merge with prompt template**: Replace `[INSERT YOUR REQUIREMENT HERE]` in `assets/prompt-template.md` with the user's source material
3. **Execute the merged prompt**: Act as Expert Prompt Architect — transform the input into a structured engine specification
4. **Save output**: Write the generated system prompt to workspace as `game-engine-generator-prompt.md`
5. **Package**: Create a zip of all related resources for distribution

## Core Concepts

The engine is built on the **Mimetic Desire Triangle**:

- **Subject** → Player/desire carrier
- **Model/Mediator** → Rules/world-order/symbolic anchor
- **Object** → Scarce resource/victory condition
- **Scapegoat** → Sacrifice target for order restoration

Rule generation formula: `Rule(t) = f(Σ Desire_i(t) · Model_i)`

Three-phase narrative loop:
1. **Convergent** (`desire_saturation < 0.4`): competitive zero-sum
2. **Saturated** (`0.4 ≤ desire_saturation < 0.8`): identity politics, object loses weight
3. **Dissolution** (`desire_saturation ≥ 0.8`): scapegoat pressure rises, desire split or chaos

## Output Structure

Each engine run produces 5 blocks (JSON + readable text):
- **O1**: World & Desire Snapshot
- **O2**: Rule Deck (propositions with boundaries and failure conditions)
- **O3**: Narrative Script (character stories + branching conditions)
- **O4**: Chaos Report (failed rules, restart conditions)
- **O5**: Iteration Seeds (verifiable questions for next round)

## Resources

- **references/engine-theory.md**: Source theoretical text — desire triangle model, three-phase narrative logic, character evaluation system
- **assets/prompt-template.md**: Expert Prompt Architect template — replace `[INSERT YOUR REQUIREMENT HERE]` with user input
