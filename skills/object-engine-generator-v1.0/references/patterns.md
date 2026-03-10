# Domain-Specific Patterns

## Narrative Engine Pattern

**Use for**: Story-driven games, interactive fiction, role-playing systems

### Symbol Structure
```markdown
## Symbol Table
- 角色: 状态变量，包含姓名/性格/动机/禁忌
- 信誉度: 连续变量，范围 [0, 100]
- 道德熵: 隐藏变量，阈值 50 触发崩溃

## State Flow
初始 → 遭遇抉择 → 执行选择 → 后果结算 → 下一个场景
    ↓                         ↓
  触发规则               状态更新

## Rules
1. 当 "信誉度 < 30" → 触发 "社会性死亡"
2. 当 "做出承诺" → 激活 "承诺悖论规则"
```

### Output Characteristics
- **State visualization**: Character arc flow diagrams
- **Rules**: Priority-based narrative branching
- **Tasks**: Chapter/scene generation pipeline
- **Charts**: Character relationship graphs, choice consequence trees

---

## Decision System Pattern

**Use for**: Business logic, workflow automation, expert systems

### Symbol Structure
```markdown
## Symbol Table
- 决策变量: 离散变量，枚举值 {批准/拒绝/转交}
- 风险评分: 连续变量，0-100
- 合规状态: 布尔值

## State Flow
待处理 → 风险评估 → 合规检查 → 决策 → 执行
              ↓           ↓
           高风险      不合规
              ↓           ↓
           人工审查     拒绝/补充材料

## Rules
1. 当 "风险评分 > 80" → 转人工审查
2. 当 "合规状态 == false" → 自动拒绝
3. 当 "决策变量 == 转交" → 分配到下一级审批人
```

### Output Characteristics
- **State visualization**: Decision tree diagrams
- **Rules**: Conditional logic with priorities
- **Tasks**: Parallel evaluation pipelines (risk + compliance)
- **Charts**: Decision flowcharts, approval DAGs

---

## Data Pipeline Pattern

**Use for**: ETL workflows, data processing, analytics

### Symbol Structure
```markdown
## Symbol Table
- 数据源: 常量，{API/数据库/文件}
- 数据质量: 状态变量，{clean/dirty/transforming}
- 吞吐量: 连续变量，records/sec

## State Flow
抽取 → 验证 → 转换 → 加载 → 监控
  ↓      ↓      ↓      ↓      ↓
失败  脏数据  错误  失败  告警

## Rules
1. 当 "数据质量 == dirty" → 触发清洗流程
2. 当 "吞吐量 < 阈值" → 横向扩展
3. 当 "验证失败率 > 5%" → 发送告警
```

### Output Characteristics
- **State visualization**: Pipeline DAG with data flow
- **Rules**: Alerting thresholds, auto-scaling triggers
- **Tasks**: Parallel ETL stages (extract → validate → transform → load)
- **Charts**: Pipeline architecture diagrams, monitoring dashboards

---

## Code Template Generator Pattern

**Use for**: Boilerplate generation, scaffolding, project initialization

### Symbol Structure
```markdown
## Symbol Table
- 框架: 常量，{React/Vue/Angular}
- 语言: 常量，{TypeScript/JavaScript}
- 状态管理: 常量，{Redux/Zustand/Context}

## State Flow
配置选择 → 模板生成 → 文件写入 → 依赖安装 → 完成

## Rules
1. 当 "框架 == React" && "状态管理 == Redux" → 生成 Redux store 结构
2. 当 "语言 == TypeScript" → 添加类型定义文件
```

### Output Characteristics
- **State visualization**: Project architecture diagrams
- **Rules**: Conditional file generation based on config
- **Tasks**: File generation sequence (package.json → src/ → tests/)
- **Charts**: Project structure trees, dependency graphs

---

## Research Note Structuring Pattern

**Use for**: Academic research, knowledge management, literature synthesis

### Symbol Structure
```markdown
## Symbol Table
- 假设: 状态变量，待验证命题
- 证据: 变量集合，引用文献
- 结论: 状态变量，验证结果

## State Flow
文献收集 → 假设生成 → 实验设计 → 数据收集 → 分析 → 结论
            ↓                           ↓
         需验证                      修正假设

## Rules
1. 当 "证据强度 > 阈值" → 假设升级为理论
2. 当 "出现反例" → 降级或废弃假设
3. 当 "样本量 < 30" → 标记"需要更多数据"
```

### Output Characteristics
- **State visualization**: Research methodology flowcharts
- **Rules**: Evidence evaluation criteria
- **Tasks**: Literature review pipeline (search → extract → synthesize)
- **Charts**: Concept maps, evidence networks
