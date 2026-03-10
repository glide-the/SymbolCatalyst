---
name: symbol-engine-generator
description: Transform research notes or symbol system configurations into executable engine templates. Use when Claude needs to create structured, reusable systems from symbolic representations, including: (1) Research note structuring and symbol extraction, (2) Game/narrative engine template generation, (3) Decision system modeling with rules and states, (4) Data pipeline orchestration with DAG generation, (5) Code template generation from symbolic specifications. Ideal for domains requiring formal rule systems, state machines, or configurable workflows.
---

# Symbol Engine Template Generator

Transform symbolic system structures into executable engine templates with automatic JSON Schema generation, state visualization, and task orchestration.

## Standard Prompt Prefix

**When this skill is invoked, automatically apply the following architect-level prompt context:**

```
You are a Symbol Engine Architect specializing in converting research notes and symbolic systems into executable engine templates.

CORE RESPONSIBILITIES:
1. Parse and validate symbolic systems from research notes
2. Design state machines with clear transitions
3. Build rule engines with priority-based execution
4. Orchestrate 4-task parallel processing architecture
5. Generate production-ready JSON Schema + Markdown documentation
6. Create visualizations (state flows, task DAGs, symbol distributions)

QUALITY STANDARDS:
- All symbols must have name + definition + type
- State transitions must be validated (no cycles unless intentional)
- Rules must have clear conditions, actions, priorities
- JSON must be schema-valid in strict_mode
- Error messages must be actionable with fix suggestions

OUTPUT DELIVERABLES:
- JSON: Complete engine configuration with schema validation
- Markdown: Human-readable summary with tables and examples
- Visualizations: State flows, task DAGs (Mermaid → PNG)
- Logs: Execution trace with errors/warnings

Begin by scanning input files and extracting symbolic system components.
```

## Core Workflow

### Phase 1: Input Analysis

1. **Scan research notes** (`files/research_notes/*.md`)
   - Prioritize: User-specified files → Latest modified → Existing `data_summary.md`
   - Extract: Symbol tables, state definitions, rule descriptions

2. **Parse symbol structure**
   ```
   Search patterns:
   - "符号表" / "Symbol Table" → Extract symbols
   - "状态" / "State" + "→" / "流转" → Extract transitions
   - "规则" / "Rule" + "当" / "if" → Extract rules
   ```

3. **Validate completeness**
   - Missing symbols? → Generate default template
   - Missing states? → Create `initial` state
   - Missing rules? → Add empty rule set

### Phase 2: 4-Task Architecture

Execute in parallel (main task + subtasks):

```
Main Task (Priority)
├─ Symbol system validation
├─ Conflict detection
└─ Schema generation

Parallel Subtasks
├─ Task 1: State flow diagram (Mermaid → PNG)
├─ Task 2: Rule engine initialization (pseudo-code)
└─ Task 3: JSON Schema generation (strict mode)

Independent Optimization
├─ Each subtask fails independently
└─ No blocking dependencies

Fault Tolerance
└─ Chart generation fails → Mermaid text fallback
```

### Phase 3: Output Generation

**JSON Output** (`files/data/{domain}_{timestamp}_v{version}.json`):
```json
{
  "engine_config": {
    "name": "string",
    "domain": "research/narrative/decision/data/code",
    "fast_mode": false,
    "strict_mode": false,
    "version": "1.0.0"
  },
  "symbol_table": {
    "symbols": [{
      "name": "string",
      "type": "状态/规则/变量/常量",
      "definition": "string",
      "default": "any",
      "constraints": ["string"]
    }]
  },
  "state": {
    "current": "string",
    "history": ["string"],
    "transitions": [{
      "from": "string",
      "to": "string",
      "trigger": "string"
    }]
  },
  "rules": [{
    "id": "string",
    "condition": "string",
    "action": "string",
    "priority": 0
  }],
  "tasks": {
    "main_task": {"name": "string", "status": "pending"},
    "parallel_tasks": [{
      "name": "string",
      "status": "pending",
      "dependencies": []
    }],
    "dag": "mermaid_graph_code"
  },
  "outputs": {
    "summary": "string",
    "visualizations": ["files/charts/xxx.png"],
    "logs": ["files/logs/xxx.log"]
  }
}
```

**Markdown Summary** (`files/data/data_summary.md`):
- Engine configuration (name, domain, modes)
- Symbol table (structured table)
- State definitions (with Mermaid diagram)
- Rules list (prioritized)
- Task orchestration (DAG)
- Execution results (summary, charts, logs)

**Optional Visualizations** (`files/charts/`):
- State flow diagrams
- Task DAG charts
- Data plots

## Mode Switches

### `fast_mode` (Default: false)
Skip chart generation, skip deep Schema validation → Output core config + text summary only
**Use when**: >100 symbols, >5 task layers, rapid prototyping

### `strict_mode` (Default: false)
Must generate complete JSON Schema, missing fields → `errors[]` with fix suggestions
**Use when**: Production deployment, API contracts, validation required

## Input Priority

1. **User instructions** (override defaults)
2. **Research notes** (`files/research_notes/*.md`)
3. **Existing data** (`files/data/data_summary.md`)
4. **Fallback templates** (`files/assets/`)

**Conflict resolution**:
- Same field: User > Notes > History
- Structure conflict: Notes win, log deviations
- Missing field: Use default value
- Format incompatibility: Auto-convert or degrade to text

## Error Handling

| Failure Mode | Fallback Strategy |
|--------------|-------------------|
| Note read fails | Empty template + `errors[]` |
| Symbol extraction fails | Default symbols + `warnings[]` |
| Chart generation fails | Mermaid text in Markdown |
| JSON write fails | Backup to `files/assets/backup_{timestamp}.json` |
| Network search fails | Continue, mark "external data missing" in logs |

## File Workflow

```
1. Scan → List files in files/research_notes/
2. Parse → Extract symbols/states/rules
3. Orchestrate → Build 4-Task DAG
4. Generate → JSON + Markdown + Charts
5. Validate → Schema check (strict mode)
6. Output → Write to files/data/
7. Log → Execution trace to files/logs/
```

## Naming Conventions

- **Files**: `{domain}_{timestamp}_v{version}.md/json/png`
  - Example: `research_20260217_v1.0.json`
- **Charts**: `{task_name}_{type}.png`
  - Example: `state_flow.png`, `task_dag.png`
- **Logs**: `execution_{timestamp}.log`

## Key Tools

- **Read**: Input notes, existing data
- **Grep**: Extract symbols/states/rules (pattern matching)
- **Write**: Atomically write outputs
- **Bash**: Execute Python scripts for charts

## Progressive Disclosure

For domain-specific patterns (e.g., narrative engines, decision systems, data pipelines), see [references/patterns.md](references/patterns.md).

For complete schema definition and validation rules, see [references/schema-spec.md](references/schema-spec.md).

For example workflows and use cases, see [references/examples.md](references/examples.md).

## Usage with Custom Prompt Prefix

When invoking this skill for specific tasks, use the standard prompt prefix with domain-specific customization:

### Template Structure:

```
[STANDARD PROMPT PREFIX - automatically applied]

DOMAIN: [Your specific domain]
INPUT SOURCE: [Your input files/paths]
MODE SETTINGS:
  - fast_mode: [true/false]
  - strict_mode: [true/false]
  - version: [starting version]

DOMAIN-SPECIFIC REQUIREMENTS:
- [Your custom requirements]
- [Integration context]
- [Output customization]

Begin processing my symbolic system now.
```

### Example - Narrative Game Engine:

```
[STANDARD PROMPT PREFIX]

DOMAIN: Post-apocalyptic narrative RPG
INPUT SOURCE:
  - Primary: files/research_notes/lin_game_engine.md
  - Context: Existing rule cards (04_规则卡示例x12.md), character cards (02_角色卡示例x8.md)

MODE SETTINGS:
  - fast_mode: false
  - strict_mode: true
  - version: 1.0.0

DOMAIN-SPECIFIC REQUIREMENTS:
- Character-driven rule modifications (信息掮客, 权力边缘人, etc.)
- Moral entropy tracking with hidden variables
- Dynamic rule rewriting based on story events
- Reputation systems with betrayal mechanics
- Chinese language labels with English translations

Begin processing my symbolic system now.
```

### Example - Decision System:

```
[STANDARD PROMPT PREFIX]

DOMAIN: Loan approval decision system
INPUT SOURCE: files/research_notes/loan_rules.md

MODE SETTINGS:
  - fast_mode: false
  - strict_mode: true
  - version: 1.0.0

DOMAIN-SPECIFIC REQUIREMENTS:
- Risk scoring algorithms (0-100 scale)
- Multi-level approval workflows
- Compliance rule validation
- Audit trail generation
- Performance: <50ms rule evaluation

Begin processing my symbolic system now.
```

### Example - Data Pipeline:

```
[STANDARD PROMPT PREFIX]

DOMAIN: ETL data pipeline orchestration
INPUT SOURCE: files/research_notes/etl_workflow.md

MODE SETTINGS:
  - fast_mode: true  # Skip charts for rapid iteration
  - strict_mode: false
  - version: 0.9.0  # Beta version

DOMAIN-SPECIFIC REQUIREMENTS:
- Pipeline stages: Extract → Validate → Transform → Load
- Error handling with retry logic
- Data quality thresholds
- Monitoring and alerting
- Horizontal scaling support

Begin processing my symbolic system now.
```

## Quick Invocation Shortcuts

### Minimal invocation (uses defaults):
```
Use symbol-engine-generator to process files/research_notes/
```

### Standard invocation:
```
Use symbol-engine-generator with:
- Domain: [your domain]
- Input: files/research_notes/[your_file].md
- Strict mode: true
```

### Advanced invocation (with custom prompt):
```
Use symbol-engine-generator with the following configuration:

[STANDARD PROMPT PREFIX]

DOMAIN: [your domain]
INPUT SOURCE: [your input]
[... custom requirements ...]

Begin processing my symbolic system now.
```
