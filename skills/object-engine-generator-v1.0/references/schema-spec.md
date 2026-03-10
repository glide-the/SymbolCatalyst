# Complete JSON Schema Specification

## Root Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Symbol Engine Template",
  "type": "object",
  "required": ["engine_config", "symbol_table", "state", "rules", "tasks"],
  "properties": {
    "engine_config": {
      "$ref": "#/definitions/engine_config"
    },
    "symbol_table": {
      "$ref": "#/definitions/symbol_table"
    },
    "state": {
      "$ref": "#/definitions/state"
    },
    "rules": {
      "$ref": "#/definitions/rules"
    },
    "tasks": {
      "$ref": "#/definitions/tasks"
    },
    "outputs": {
      "$ref": "#/definitions/outputs"
    },
    "errors": {
      "type": "array",
      "items": {"type": "string"}
    },
    "warnings": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

## Definitions

### engine_config

```json
{
  "type": "object",
  "required": ["name", "domain", "version"],
  "properties": {
    "name": {
      "type": "string",
      "description": "Engine name (snake_case or camelCase)",
      "pattern": "^[a-zA-Z][a-zA-Z0-9_]*$",
      "examples": ["climate_model", "narrative_engine_v1", "decision_system"]
    },
    "domain": {
      "type": "string",
      "enum": ["research", "narrative", "decision", "data", "code"],
      "description": "Domain category"
    },
    "fast_mode": {
      "type": "boolean",
      "default": false,
      "description": "Skip chart generation and deep validation"
    },
    "strict_mode": {
      "type": "boolean",
      "default": false,
      "description": "Enforce complete JSON Schema, generate errors for missing fields"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version"
    }
  }
}
```

### symbol_table

```json
{
  "type": "object",
  "required": ["symbols"],
  "properties": {
    "symbols": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "type", "definition"],
        "properties": {
          "name": {
            "type": "string",
            "description": "Symbol identifier (unique within table)"
          },
          "type": {
            "type": "string",
            "enum": ["状态", "规则", "变量", "常量", "state", "rule", "variable", "constant"]
          },
          "definition": {
            "type": "string",
            "description": "Human-readable definition"
          },
          "default": {
            "description": "Default value (any JSON type)"
          },
          "constraints": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Validation constraints"
          }
        }
      }
    }
  }
}
```

### state

```json
{
  "type": "object",
  "required": ["current", "transitions"],
  "properties": {
    "current": {
      "type": "string",
      "description": "Current state identifier"
    },
    "history": {
      "type": "array",
      "items": {"type": "string"},
      "description": "State history (oldest first)"
    },
    "transitions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["from", "to", "trigger"],
        "properties": {
          "from": {"type": "string"},
          "to": {"type": "string"},
          "trigger": {"type": "string"},
          "condition": {
            "type": "string",
            "description": "Optional guard condition"
          }
        }
      }
    }
  }
}
```

### rules

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "condition", "action"],
    "properties": {
      "id": {
        "type": "string",
        "description": "Unique rule identifier"
      },
      "condition": {
        "type": "string",
        "description": "Trigger condition (natural language or pseudo-code)"
      },
      "action": {
        "type": "string",
        "description": "Action to execute when condition is met"
      },
      "priority": {
        "type": "number",
        "default": 0,
        "description": "Higher priority rules execute first"
      },
      "enabled": {
        "type": "boolean",
        "default": true
      }
    }
  }
}
```

### tasks

```json
{
  "type": "object",
  "required": ["main_task", "parallel_tasks"],
  "properties": {
    "main_task": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "status": {
          "type": "string",
          "enum": ["pending", "running", "completed", "failed"]
        }
      }
    },
    "parallel_tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "status": {
            "type": "string",
            "enum": ["pending", "running", "completed", "failed"]
          },
          "dependencies": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    },
    "dag": {
      "type": "string",
      "description": "Mermaid graph code representing task dependencies",
      "examples": [
        "graph TD\n  A[Main Task] --> B[Task 1]\n  A --> C[Task 2]\n  B --> D[Task 3]"
      ]
    }
  }
}
```

### outputs

```json
{
  "type": "object",
  "properties": {
    "summary": {
      "type": "string",
      "description": "Human-readable execution summary"
    },
    "visualizations": {
      "type": "array",
      "items": {
        "type": "string",
        "format": "uri"
      },
      "description": "Paths to generated charts (PNG/SVG)"
    },
    "logs": {
      "type": "array",
      "items": {
        "type": "string",
        "format": "uri"
      },
      "description": "Paths to execution log files"
    }
  }
}
```

## Validation Rules

### Strict Mode Constraints

When `strict_mode: true`:

1. **All required fields must be present**
   - Missing fields → Generate error: `"Field 'X' is required but missing"`

2. **Symbol table validation**
   - Duplicate symbol names → Error: `"Duplicate symbol: 'X'"`
   - Missing `definition` → Error: `"Symbol 'X' lacks definition"`

3. **State transition validation**
   - Circular dependencies (no path to terminal state) → Warning: `"State cycle detected: X → Y → X"`
   - Orphan states (unreachable) → Warning: `"Unreachable state: 'X'"`

4. **Rule validation**
   - Duplicate rule IDs → Error: `"Duplicate rule ID: 'X'"`
   - Malformed conditions → Error: `"Rule 'X' condition cannot be parsed"`

5. **Task DAG validation**
   - Cycles in dependencies → Error: `"Circular dependency in tasks: X → Y → X"`
   - Unresolvable dependencies → Error: `"Task 'X' depends on non-existent task 'Y'"`

### Fast Mode Constraints

When `fast_mode: true`:

- Skip chart generation (no visualizations array)
- Skip deep schema validation (only check required fields)
- Output only core config + text summary
- No Mermaid diagrams in output

## Error Format

```json
{
  "errors": [
    "Field 'symbol_table.symbols[0].definition' is required but missing",
    "Duplicate symbol ID: 'player_health'",
    "Circular dependency detected: state_a → state_b → state_a"
  ],
  "warnings": [
    "Using default symbol 'default_symbol' (no symbols provided)",
    "Unreachable state: 'terminal_state'",
    "Chart generation failed, using Mermaid text fallback"
  ]
}
```

## Example Valid Output

```json
{
  "engine_config": {
    "name": "narrative_engine_v1",
    "domain": "narrative",
    "fast_mode": false,
    "strict_mode": true,
    "version": "1.0.0"
  },
  "symbol_table": {
    "symbols": [
      {
        "name": "player_health",
        "type": "变量",
        "definition": "玩家当前生命值",
        "default": 100,
        "constraints": ["min: 0", "max: 100"]
      }
    ]
  },
  "state": {
    "current": "active",
    "history": ["initialized"],
    "transitions": [
      {
        "from": "initialized",
        "to": "active",
        "trigger": "game_start"
      }
    ]
  },
  "rules": [
    {
      "id": "combat_rule_001",
      "condition": "player_health < 30",
      "action": "trigger_critical_state()",
      "priority": 10
    }
  ],
  "tasks": {
    "main_task": {
      "name": "validate_symbols",
      "status": "completed"
    },
    "parallel_tasks": [
      {
        "name": "generate_state_flow",
        "status": "completed",
        "dependencies": []
      }
    ],
    "dag": "graph TD\n  A[validate_symbols] --> B[generate_state_flow]"
  },
  "outputs": {
    "summary": "Engine generated successfully with 1 symbol, 1 rule, and 2 states.",
    "visualizations": ["files/charts/state_flow.png"],
    "logs": ["files/logs/execution_20260217.log"]
  },
  "errors": [],
  "warnings": []
}
```
