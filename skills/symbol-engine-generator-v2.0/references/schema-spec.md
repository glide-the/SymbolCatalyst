# JSON Schema Specification

## Table of Contents

1. [Root Schema](#root-schema)
2. [Engine Input](#engine-input)
3. [Symbol](#symbol)
4. [FantasyKnot](#fantasyknot)
5. [IndexicalOperation](#indexicaloperation)
6. [Proposition](#proposition)
7. [PowerChain](#powerchain)
8. [Output Blocks O1-O5](#output-blocks)
9. [Validation Rules](#validation-rules)

---

## Root Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SymbolEngineOutput",
  "type": "object",
  "required": ["engine_input", "symbol_graph", "rule_deck"],
  "properties": {
    "engine_input": { "$ref": "#/definitions/EngineInput" },
    "symbol_graph": { "$ref": "#/definitions/SymbolGraph" },
    "rule_deck": { "$ref": "#/definitions/RuleDeck" },
    "rewrite_log": { "$ref": "#/definitions/RewriteLog" },
    "silence_report": { "$ref": "#/definitions/SilenceReport" },
    "interrogation_seeds": {
      "type": "array",
      "items": { "type": "string" },
      "description": "可检验问题列表，禁止引导式废话"
    }
  }
}
```

---

## Engine Input

```json
{
  "EngineInput": {
    "type": "object",
    "description": "引擎输入，至少提供 I1-I4 中的一项",
    "properties": {
      "discourse_flow": {
        "type": "string",
        "description": "I1: 话语流——自然语言段落，包含情绪/判断/因果/定义/命题"
      },
      "tool_description": {
        "type": "object",
        "description": "I2: 工具/载体描述",
        "properties": {
          "carrier_type": {
            "type": "string",
            "enum": ["text", "voice", "image", "interactive_interface", "process", "institution"],
            "description": "载体类型"
          },
          "constraints": {
            "type": "array",
            "items": { "type": "string" },
            "description": "工具约束条件"
          },
          "bandwidth": {
            "type": "string",
            "enum": ["narrow", "medium", "wide"],
            "description": "信息通道带宽"
          }
        },
        "required": ["carrier_type"]
      },
      "observer_stance": {
        "type": "object",
        "description": "I3: 观察者立场/主体性描述",
        "properties": {
          "interrogation_intensity": {
            "type": "number",
            "minimum": 0,
            "maximum": 10,
            "description": "追问强度：0=不追问，10=最大追问"
          },
          "silence_threshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "沉默阈值：巫术风险超过此值即进入沉默策略"
          },
          "error_tolerance": {
            "type": "string",
            "enum": ["strict", "loose"],
            "description": "容错偏好"
          }
        },
        "required": ["interrogation_intensity", "silence_threshold"]
      },
      "reality_mapping_vars": {
        "type": "object",
        "description": "I4: 现实映射变量（仅抽象名，禁止具体机构名）",
        "properties": {
          "credibility": { "type": "number", "minimum": 0, "maximum": 1 },
          "commitment_cost": { "type": "number", "minimum": 0 },
          "information_asymmetry": { "type": "number", "minimum": 0, "maximum": 1 },
          "compliance_pressure": { "type": "number", "minimum": 0, "maximum": 1 },
          "time_debt": { "type": "number", "minimum": 0 },
          "power_distance": { "type": "number", "minimum": 0, "maximum": 10 }
        },
        "additionalProperties": {
          "type": "number",
          "description": "可扩展抽象变量"
        }
      }
    },
    "anyOf": [
      { "required": ["discourse_flow"] },
      { "required": ["tool_description"] },
      { "required": ["observer_stance"] },
      { "required": ["reality_mapping_vars"] }
    ]
  }
}
```

---

## Symbol

```json
{
  "Symbol": {
    "type": "object",
    "required": ["id", "label", "valence", "carrier", "origin", "time_form"],
    "properties": {
      "id": {
        "type": "string",
        "pattern": "^sym_[a-z0-9_]+$",
        "description": "唯一标识符"
      },
      "label": {
        "type": "string",
        "description": "抽象命名，禁止出现文化符号"
      },
      "valence": {
        "type": "object",
        "description": "情绪色彩向量，维度为抽象感受",
        "properties": {
          "tension": { "type": "number", "minimum": -1, "maximum": 1, "description": "张力" },
          "oppression": { "type": "number", "minimum": -1, "maximum": 1, "description": "压迫" },
          "seduction": { "type": "number", "minimum": -1, "maximum": 1, "description": "诱惑" },
          "hesitation": { "type": "number", "minimum": -1, "maximum": 1, "description": "迟疑" },
          "clarity": { "type": "number", "minimum": -1, "maximum": 1, "description": "清明" }
        },
        "additionalProperties": {
          "type": "number",
          "minimum": -1,
          "maximum": 1,
          "description": "可扩展情绪维度"
        }
      },
      "carrier": {
        "type": "string",
        "description": "所属工具/载体类型"
      },
      "origin": {
        "type": "object",
        "description": "来源片段引用",
        "properties": {
          "text_index": { "type": "integer", "description": "话语流中的字符位置" },
          "hash": { "type": "string", "description": "来源片段哈希" },
          "excerpt": { "type": "string", "description": "原文摘录" }
        }
      },
      "time_form": {
        "type": "object",
        "description": "时间化标记——感性空间分配，非物理时间",
        "properties": {
          "past": { "type": "number", "minimum": 0, "maximum": 1, "description": "过去的感性权重" },
          "present": { "type": "number", "minimum": 0, "maximum": 1, "description": "现在的感性权重" },
          "future": { "type": "number", "minimum": 0, "maximum": 1, "description": "未来的感性权重（对过去的对象化活动，先验想象力对感受时间的规划）" }
        },
        "required": ["past", "present", "future"]
      }
    }
  }
}
```

---

## FantasyKnot

```json
{
  "FantasyKnot": {
    "type": "object",
    "required": ["id", "repetition_pattern", "force_index", "exclusivity_filters"],
    "properties": {
      "id": {
        "type": "string",
        "pattern": "^fk_[a-z0-9_]+$"
      },
      "repetition_pattern": {
        "type": "object",
        "description": "重复信息模式",
        "properties": {
          "type": {
            "type": "string",
            "enum": ["n_gram", "thematic_loop", "narrative_recoil"],
            "description": "n-gram重复 / 主题回环 / 叙事回卷"
          },
          "pattern_signature": {
            "type": "string",
            "description": "模式签名（可为正则或主题描述）"
          },
          "frequency": {
            "type": "integer",
            "minimum": 1,
            "description": "在话语流中出现次数"
          },
          "linked_symbols": {
            "type": "array",
            "items": { "type": "string" },
            "description": "关联符号 id 列表"
          }
        },
        "required": ["type", "frequency"]
      },
      "force_index": {
        "type": "number",
        "minimum": 0,
        "description": "力量指数 = repetition_freq × exclusivity_strength × power_chain_trigger"
      },
      "exclusivity_filters": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "filter_type": {
              "type": "string",
              "enum": ["binary_opposition", "categorical_exclusion", "boundary_enforcement", "silence_induction"],
              "description": "筛选机制类型"
            },
            "condition": {
              "type": "string",
              "description": "筛选条件（抽象表达）"
            },
            "excluded_set": {
              "type": "array",
              "items": { "type": "string" },
              "description": "被排除的符号/模式 id"
            }
          },
          "required": ["filter_type", "condition"]
        }
      }
    }
  }
}
```

---

## IndexicalOperation

```json
{
  "IndexicalOperation": {
    "type": "object",
    "required": ["slice", "freeze", "stitch"],
    "properties": {
      "slice": {
        "type": "object",
        "description": "切片规则：如何从话语流中切出符号单位",
        "properties": {
          "method": {
            "type": "string",
            "enum": ["repetition_boundary", "negation_point", "causal_joint", "boundary_word", "emotional_shift"],
            "description": "切片方法"
          },
          "parameters": {
            "type": "object",
            "properties": {
              "min_repeat_count": { "type": "integer", "default": 2 },
              "context_window": { "type": "integer", "default": 50, "description": "上下文窗口（字符数）" }
            }
          }
        },
        "required": ["method"]
      },
      "freeze": {
        "type": "object",
        "description": "凝固规则：何时把流动变为定义/命题",
        "properties": {
          "trigger": {
            "type": "string",
            "enum": ["self_reference_count", "cross_reference_count", "explanatory_usage", "definition_pattern"],
            "description": "凝固触发条件"
          },
          "threshold": {
            "type": "integer",
            "minimum": 1,
            "description": "触发阈值"
          }
        },
        "required": ["trigger", "threshold"]
      },
      "stitch": {
        "type": "object",
        "description": "缝合规则：何时把多符号缝成模式/结构",
        "properties": {
          "min_symbols": {
            "type": "integer",
            "minimum": 2,
            "description": "最少要缝合的符号数"
          },
          "co_occurrence_threshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "共现率阈值"
          },
          "structural_form": {
            "type": "string",
            "enum": ["chain", "cluster", "hierarchy", "loop"],
            "description": "缝合后的结构形式"
          }
        },
        "required": ["min_symbols", "structural_form"]
      }
    }
  }
}
```

---

## Proposition

```json
{
  "Proposition": {
    "type": "object",
    "required": ["id", "statement", "causal_form", "boundary", "failure_conditions", "witchcraft_risk"],
    "properties": {
      "id": {
        "type": "string",
        "pattern": "^prop_[a-z0-9_]+$"
      },
      "statement": {
        "type": "string",
        "description": "规则文本（抽象表达）"
      },
      "causal_form": {
        "type": "object",
        "description": "因果表达结构（可重写）",
        "properties": {
          "antecedent": { "type": "string", "description": "前件" },
          "consequent": { "type": "string", "description": "后件" },
          "direction": {
            "type": "string",
            "enum": ["forward", "backward", "bidirectional"],
            "description": "因果方向：forward=前件→后件, backward=后件→前件, bidirectional=互构"
          }
        },
        "required": ["antecedent", "consequent", "direction"]
      },
      "boundary": {
        "type": "object",
        "description": "适用边界",
        "properties": {
          "applicable_carriers": {
            "type": "array",
            "items": { "type": "string" },
            "description": "适用的工具/载体类型"
          },
          "applicable_conditions": {
            "type": "string",
            "description": "适用条件描述"
          },
          "excluded_domains": {
            "type": "array",
            "items": { "type": "string" },
            "description": "排除的适用域"
          }
        }
      },
      "failure_conditions": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "condition": { "type": "string" },
            "degradation": {
              "type": "string",
              "enum": ["silence", "hypothesis", "rewrite", "discard"],
              "description": "降级方式"
            }
          },
          "required": ["condition", "degradation"]
        }
      },
      "rewrite_hooks": {
        "type": "object",
        "description": "可改写字段与触发器",
        "properties": {
          "rewritable_fields": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": ["statement", "causal_form", "boundary", "filters"]
            }
          },
          "triggers": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "event": { "type": "string", "description": "触发事件" },
                "target_field": { "type": "string" },
                "rewrite_direction": {
                  "type": "string",
                  "enum": ["strengthen", "exclude", "expand", "contract", "obscure"]
                }
              }
            }
          }
        }
      },
      "witchcraft_risk": {
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "description": "巫术风险分：定义反向制造原因的倾向"
      }
    }
  }
}
```

---

## PowerChain

```json
{
  "PowerChain": {
    "type": "object",
    "required": ["id", "motion_links", "active_carriers", "effect_on_rules"],
    "properties": {
      "id": {
        "type": "string",
        "pattern": "^pc_[a-z0-9_]+$"
      },
      "motion_links": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "position": { "type": "integer", "description": "链条位置序号" },
            "label": {
              "type": "string",
              "description": "抽象链节标签（意识形态/权力聚合/原则化/意志集中/集体认同/主权表达）"
            },
            "intensity": { "type": "number", "minimum": 0, "maximum": 1 }
          },
          "required": ["position", "label", "intensity"]
        },
        "description": "权力运动的抽象链条，从意识形态到主权表达"
      },
      "active_carriers": {
        "type": "array",
        "items": { "type": "string" },
        "description": "当前临时载体列表"
      },
      "effect_on_rules": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "target_proposition_id": { "type": "string" },
            "effect_type": {
              "type": "string",
              "enum": ["strengthen", "exclude", "expand", "contract", "obscure"],
              "description": "强化/排他/扩张/收缩/遮蔽"
            },
            "magnitude": { "type": "number", "minimum": 0, "maximum": 1 }
          },
          "required": ["target_proposition_id", "effect_type", "magnitude"]
        }
      }
    }
  }
}
```

---

## Output Blocks

### O1: Symbol Graph Snapshot

```json
{
  "SymbolGraphSnapshot": {
    "type": "object",
    "required": ["symbols", "fantasy_knots", "power_chains"],
    "properties": {
      "symbols": {
        "type": "array",
        "items": { "$ref": "#/definitions/Symbol" }
      },
      "fantasy_knots": {
        "type": "array",
        "items": { "$ref": "#/definitions/FantasyKnot" }
      },
      "power_chains": {
        "type": "array",
        "items": { "$ref": "#/definitions/PowerChain" }
      },
      "indexical_operations": {
        "type": "array",
        "items": { "$ref": "#/definitions/IndexicalOperation" }
      },
      "graph_metadata": {
        "type": "object",
        "properties": {
          "total_symbols": { "type": "integer" },
          "total_knots": { "type": "integer" },
          "total_chains": { "type": "integer" },
          "timestamp": { "type": "string", "format": "date-time" },
          "iteration": { "type": "integer" }
        }
      }
    }
  }
}
```

### O2: Rule Deck

```json
{
  "RuleDeck": {
    "type": "object",
    "required": ["propositions"],
    "properties": {
      "propositions": {
        "type": "array",
        "items": { "$ref": "#/definitions/Proposition" }
      },
      "deck_metadata": {
        "type": "object",
        "properties": {
          "total_rules": { "type": "integer" },
          "avg_witchcraft_risk": { "type": "number" },
          "silenced_count": { "type": "integer" },
          "rewritten_count": { "type": "integer" }
        }
      }
    }
  }
}
```

### O3: Rewrite Log

```json
{
  "RewriteLog": {
    "type": "object",
    "properties": {
      "entries": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["proposition_id", "timestamp", "trigger_source", "field_changed", "old_value", "new_value"],
          "properties": {
            "proposition_id": { "type": "string" },
            "timestamp": { "type": "string", "format": "date-time" },
            "trigger_source": {
              "type": "string",
              "enum": ["tool_difference", "exclusivity_filter", "power_chain", "interrogation", "witchcraft_remediation"],
              "description": "改写触发源"
            },
            "field_changed": {
              "type": "string",
              "enum": ["statement", "causal_form", "boundary", "filters", "failure_conditions"]
            },
            "old_value": { "description": "改写前的值" },
            "new_value": { "description": "改写后的值" },
            "reason": { "type": "string" }
          }
        }
      }
    }
  }
}
```

### O4: Silence Report

```json
{
  "SilenceReport": {
    "type": "object",
    "properties": {
      "entries": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["location", "silence_type", "reason"],
          "properties": {
            "location": {
              "type": "string",
              "description": "沉默发生的位置（stage + proposition_id）"
            },
            "silence_type": {
              "type": "string",
              "enum": ["boundary_exceeded", "failure_triggered", "witchcraft_high", "information_insufficient"],
              "description": "沉默类型：边界外/失败条件触发/巫术风险过高/信息不足"
            },
            "reason": {
              "type": "string",
              "description": "沉默原因"
            },
            "testable_question": {
              "type": "string",
              "description": "替代输出：一个可检验的追问"
            }
          }
        }
      }
    }
  }
}
```

### O5: Interrogation Seeds

```json
{
  "InterrogationSeeds": {
    "type": "object",
    "properties": {
      "seeds": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["question", "target", "testability"],
          "properties": {
            "question": {
              "type": "string",
              "description": "可检验问题（禁止引导式废话）"
            },
            "target": {
              "type": "string",
              "description": "追问目标（proposition_id 或 symbol_id）"
            },
            "testability": {
              "type": "string",
              "description": "如何检验此问题（需给出观察方法）"
            },
            "negation_source": {
              "type": "string",
              "description": "产生此追问的否定操作来源"
            }
          }
        }
      }
    }
  }
}
```

---

## Validation Rules

### 符号验证

- `id` 全局唯一
- `label` 禁止包含具体文化符号关键词
- `valence` 各维度 ∈ [-1, 1]
- `time_form` 三值之和应 ≈ 1.0（容差 ±0.1）

### 幻想结验证

- `force_index` 必须 > 0（否则不构成幻想结）
- `exclusivity_filters` 至少包含 1 个筛选器
- `linked_symbols` 引用的符号 id 必须存在于 `symbol_graph.symbols`

### 命题验证

- 必须同时具备 `boundary` 和 `failure_conditions`，否则触发巫术检测
- `witchcraft_risk` 超过 `observer_stance.silence_threshold` → 进入沉默策略
- `causal_form.direction` 为 `backward` 时自动 `risk += 0.2`

### 权力链验证

- `motion_links` 至少包含 2 个链节
- `effect_on_rules` 引用的 `target_proposition_id` 必须存在
- `active_carriers` 不得为空（权力必须有临时载体）
