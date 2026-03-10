# 规则卡示例 ×8 + 输出样例 O1-O5

## Table of Contents

1. [规则卡示例](#规则卡示例)
2. [输出样例 O1: Symbol Graph Snapshot](#o1-symbol-graph-snapshot)
3. [输出样例 O2: Rule Deck](#o2-rule-deck)
4. [输出样例 O3: Rewrite Log](#o3-rewrite-log)
5. [输出样例 O4: Silence Report](#o4-silence-report)
6. [输出样例 O5: Interrogation Seeds](#o5-interrogation-seeds)

---

## 规则卡示例

### 卡 1：重复凝固

```
名称：重复凝固
触发：当某片段在话语流中重复出现 ≥3 次且被用于自我解释
效果：符号图 [新增凝固符号] + force_index [+0.2/次重复]
代价：信息损失——流动态的可能性被压缩为单一定义
边界：适用于话语流长度 > 200字符的输入；短文本中重复可能仅为修辞
失败条件：当重复片段跨越 >3 种不同工具且结构完全一致 → 降级为假设（可能是引用而非幻想）
可改写字段：statement / boundary
巫术风险：0.1 — 纯统计触发，定义造因倾向低
追问提示：该重复片段在不同载体上的结构是否存在差异？
```

### 卡 2：排他筛选激活

```
名称：排他筛选激活
触发：当符号图中出现二元对立结构且一方被系统性排除
效果：符号图 [标记被排除符号为"筛选外"] + exclusivity_filters [+1个筛选器]
代价：边界收缩——系统的可容纳解释数减少
边界：适用于符号图中存在 ≥2 个对立符号的场景
失败条件：当排他机制排除了 >80% 的已有符号 → 降级为沉默（系统过度封闭）
可改写字段：filters / boundary
巫术风险：0.3 — 排他筛选可能遮蔽替代解释，存在中度定义造因倾向
追问提示：被排除的符号是否在其他工具载体上呈现不同结构？
```

### 卡 3：权力链传导

```
名称：权力链传导
触发：当权力链中相邻链节的 intensity 差值 > 0.4
效果：符号图 [激活传导路径上的所有载体] + 目标命题的 causal_form [direction 可能翻转]
代价：沉默概率上升——权力传导过程中信息可能被遮蔽
边界：适用于权力链包含 ≥3 个活跃链节的场景
失败条件：当所有 active_carriers 同时失责（载体列表为空） → 降级为沉默
可改写字段：causal_form / statement / boundary
巫术风险：0.2 — 权力链本身不造因，但其改写效果可能掩盖原因缺失
追问提示：权力运动经过哪些载体时产生了结构性变化？
```

### 卡 4：因果倒置标记

```
名称：因果倒置标记
触发：当命题的 causal_form.direction 为 backward 且无外部验证锚点
效果：符号图 [目标命题标记巫术警告] + witchcraft_risk [+0.3]
代价：信息损失——该命题的可用性降级，可能进入沉默
边界：适用于所有包含因果声称的命题
失败条件：当该命题是唯一解释路径且无替代命题 → 降级为假设而非直接丢弃
可改写字段：causal_form / statement
巫术风险：0.5 — 因果倒置是巫术的核心信号
追问提示：能否找到独立于该定义的原因来验证后件？
```

### 卡 5：追问否定展开

```
名称：追问否定展开
触发：当对命题的子词执行否定操作后产生 ≥2 个替代命题
效果：符号图 [新增替代命题节点] + 原命题的 rewrite_hooks [标记已被追问]
代价：边界收缩——原命题的确定性降低
边界：适用于 interrogation_intensity ≥ 5 的观察者立场
失败条件：当否定后所有替代命题的 witchcraft_risk 均 > 0.6 → 降级为沉默
可改写字段：statement / causal_form / boundary / filters
巫术风险：0.05 — 追问本身不造因，是系统的自检机制
追问提示：否定后的替代命题中，哪些可通过观察被验证或否证？
```

### 卡 6：工具载体切换

```
名称：工具载体切换
触发：当工具描述 I2 中的 carrier_type 发生变更
效果：符号图 [所有符号的 carrier 字段更新] + 幻想结的 force_index [可能重算]
代价：信息损失——在新载体上，原有排他筛选可能失效
边界：适用于系统内存在 ≥1 个已凝固符号的场景
失败条件：当新载体无法承载任何已有符号 → 降级为沉默（工具不兼容）
可改写字段：statement / filters
巫术风险：0.15 — 载体切换本身不造因，但切换中信息重构可能引入偏差
追问提示：同一幻想结在新旧载体上的重复模式是否结构相同？
```

### 卡 7：边界收缩

```
名称：边界收缩
触发：当命题经历 ≥2 次 failure_conditions 触发但未被丢弃
效果：符号图 [命题的 boundary.applicable_conditions 缩小] + 沉默概率 [+0.1/次触发]
代价：信息损失——命题的适用范围缩小，可能变得无用
边界：适用于已经过至少一轮追问驱动的命题
失败条件：当 boundary 缩小为空集 → 降级为丢弃
可改写字段：boundary / failure_conditions
巫术风险：0.1 — 边界收缩是防御机制，非造因行为
追问提示：收缩后的边界是否仍然覆盖了最初想要解释的现象？
```

### 卡 8：沉默策略触发

```
名称：沉默策略触发
触发：当 witchcraft_risk ≥ silence_threshold 或所有 failure_conditions 同时触发
效果：符号图 [命题标记为"沉默态"] + 输出 [该位置仅输出可检验问题]
代价：沉默概率上升至 1.0——该位置放弃确定性结论
边界：适用于 witchcraft_risk ≥ observer_stance.silence_threshold
失败条件：当系统内 >50% 的命题进入沉默 → 标记"系统性沉默"，建议重新输入
可改写字段：statement（重写为问题形式）
巫术风险：0.0 — 沉默本身是对巫术的防御，非造因
追问提示：沉默的位置是否指向了精神世界中尚未被对象化的区域？
```

---

## O1: Symbol Graph Snapshot

```json
{
  "symbols": [
    {
      "id": "sym_repetitive_force",
      "label": "重复性力量",
      "valence": {
        "tension": 0.7,
        "oppression": 0.3,
        "seduction": 0.1,
        "hesitation": -0.2,
        "clarity": -0.4
      },
      "carrier": "text",
      "origin": {
        "text_index": 42,
        "hash": "a3f7c2",
        "excerpt": "一种不断重复的信息，它表现出力量"
      },
      "time_form": {
        "past": 0.3,
        "present": 0.5,
        "future": 0.2
      }
    },
    {
      "id": "sym_boundary_absence",
      "label": "边界缺失",
      "valence": {
        "tension": 0.5,
        "oppression": 0.6,
        "seduction": 0.4,
        "hesitation": 0.3,
        "clarity": -0.7
      },
      "carrier": "text",
      "origin": {
        "text_index": 380,
        "hash": "d9e1b4",
        "excerpt": "不能说明自己的适用边界和失败条件"
      },
      "time_form": {
        "past": 0.1,
        "present": 0.7,
        "future": 0.2
      }
    }
  ],
  "fantasy_knots": [
    {
      "id": "fk_causal_loop",
      "repetition_pattern": {
        "type": "thematic_loop",
        "pattern_signature": "定义→因果→定义",
        "frequency": 4,
        "linked_symbols": ["sym_repetitive_force", "sym_boundary_absence"]
      },
      "force_index": 3.6,
      "exclusivity_filters": [
        {
          "filter_type": "binary_opposition",
          "condition": "有定义 vs 无原因",
          "excluded_set": ["sym_external_cause"]
        }
      ]
    }
  ],
  "power_chains": [
    {
      "id": "pc_ideology_to_sovereignty",
      "motion_links": [
        { "position": 0, "label": "意识形态", "intensity": 0.9 },
        { "position": 1, "label": "权力聚合", "intensity": 0.7 },
        { "position": 2, "label": "原则化", "intensity": 0.5 },
        { "position": 3, "label": "意志集中", "intensity": 0.3 },
        { "position": 4, "label": "集体认同", "intensity": 0.2 },
        { "position": 5, "label": "主权表达", "intensity": 0.1 }
      ],
      "active_carriers": ["text", "process"],
      "effect_on_rules": [
        {
          "target_proposition_id": "prop_silence_as_truth",
          "effect_type": "strengthen",
          "magnitude": 0.4
        }
      ]
    }
  ],
  "graph_metadata": {
    "total_symbols": 2,
    "total_knots": 1,
    "total_chains": 1,
    "timestamp": "2026-02-18T00:00:00Z",
    "iteration": 1
  }
}
```

---

## O2: Rule Deck

```json
{
  "propositions": [
    {
      "id": "prop_silence_as_truth",
      "statement": "在无法确定原因之前，沉默是唯一不制造意识形态的响应",
      "causal_form": {
        "antecedent": "原因不可确定",
        "consequent": "响应为沉默",
        "direction": "forward"
      },
      "boundary": {
        "applicable_carriers": ["text", "voice", "interactive_interface"],
        "applicable_conditions": "当巫术风险 ≥ 0.6 或失败条件全部触发",
        "excluded_domains": []
      },
      "failure_conditions": [
        {
          "condition": "沉默本身被用作权力工具（选择性沉默以遮蔽信息）",
          "degradation": "rewrite"
        }
      ],
      "rewrite_hooks": {
        "rewritable_fields": ["statement", "boundary"],
        "triggers": [
          {
            "event": "power_chain_shift",
            "target_field": "statement",
            "rewrite_direction": "contract"
          }
        ]
      },
      "witchcraft_risk": 0.15
    },
    {
      "id": "prop_interrogation_as_form",
      "statement": "追问是唯一的真理形式结构——每个子词可否定，每条因果可重写",
      "causal_form": {
        "antecedent": "存在命题",
        "consequent": "必须可被追问",
        "direction": "forward"
      },
      "boundary": {
        "applicable_carriers": ["text", "voice", "interactive_interface", "process"],
        "applicable_conditions": "适用于所有命题，无例外",
        "excluded_domains": []
      },
      "failure_conditions": [
        {
          "condition": "追问本身变为不可追问的教条",
          "degradation": "hypothesis"
        }
      ],
      "rewrite_hooks": {
        "rewritable_fields": ["causal_form"],
        "triggers": []
      },
      "witchcraft_risk": 0.1
    }
  ],
  "deck_metadata": {
    "total_rules": 2,
    "avg_witchcraft_risk": 0.125,
    "silenced_count": 0,
    "rewritten_count": 0
  }
}
```

---

## O3: Rewrite Log

```json
{
  "entries": [
    {
      "proposition_id": "prop_silence_as_truth",
      "timestamp": "2026-02-18T00:05:00Z",
      "trigger_source": "interrogation",
      "field_changed": "boundary",
      "old_value": {
        "applicable_conditions": "当巫术风险 ≥ 0.5"
      },
      "new_value": {
        "applicable_conditions": "当巫术风险 ≥ 0.6 或失败条件全部触发"
      },
      "reason": "追问驱动发现：阈值 0.5 导致过多命题进入沉默，边界需放宽至 0.6"
    },
    {
      "proposition_id": "prop_interrogation_as_form",
      "timestamp": "2026-02-18T00:07:00Z",
      "trigger_source": "power_chain",
      "field_changed": "statement",
      "old_value": "追问是真理的唯一形式",
      "new_value": "追问是唯一的真理形式结构——每个子词可否定，每条因果可重写",
      "reason": "权力链传导使原表述过于绝对，补充结构性限定以降低巫术风险"
    }
  ]
}
```

---

## O4: Silence Report

```json
{
  "entries": [
    {
      "location": "Stage 8 / fk_causal_loop → prop_candidate_003",
      "silence_type": "witchcraft_high",
      "reason": "候选命题 prop_candidate_003 (\"定义即原因\") 的因果结构为 backward 方向且无外部验证锚点，witchcraft_risk = 0.7，超过 silence_threshold = 0.6",
      "testable_question": "是否存在独立于该定义的可观察证据，可以验证其声称的因果关系？"
    },
    {
      "location": "Stage 6 / sym_boundary_absence → prop_candidate_007",
      "silence_type": "boundary_exceeded",
      "reason": "候选命题试图解释所有工具载体上的现象但仅基于单一载体(text)的观察，超出其 boundary",
      "testable_question": "在非文本载体（voice/image）上，同一重复模式是否产生相同的凝固结构？"
    }
  ]
}
```

---

## O5: Interrogation Seeds

```json
{
  "seeds": [
    {
      "question": "sym_repetitive_force 的重复模式在语音载体上是否仍呈现相同的力量指数？",
      "target": "sym_repetitive_force",
      "testability": "在语音载体上重新运行 Stage 1-2，比较 force_index 差异",
      "negation_source": "对 carrier='text' 执行否定：若 carrier≠text，结构是否改变？"
    },
    {
      "question": "prop_silence_as_truth 的沉默策略是否会被权力链用作遮蔽工具？",
      "target": "prop_silence_as_truth",
      "testability": "在 power_chain 中增加一个以沉默为 active_carrier 的链节，观察 effect_on_rules 变化",
      "negation_source": "否定 '沉默不制造意识形态' → 沉默在何种条件下制造意识形态？"
    },
    {
      "question": "fk_causal_loop 的排他筛选是否遮蔽了 '外部原因' 之外的其他解释路径？",
      "target": "fk_causal_loop",
      "testability": "移除 binary_opposition 筛选器，重新运行 Stage 4-5，观察被排除符号的回归",
      "negation_source": "否定 exclusivity_filter 的 excluded_set → 被排除的符号是否携带有效信息？"
    },
    {
      "question": "time_form 中 future 权重为 0.2 的符号，其先验想象力是否足以驱动下一轮命题生成？",
      "target": "sym_repetitive_force",
      "testability": "将 future 权重调至 0.5，观察 Stage 6 生成的命题集合差异",
      "negation_source": "否定 future=0.2 → 若未来感性空间更大，命题方向如何变化？"
    }
  ]
}
```
