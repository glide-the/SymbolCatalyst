# Symbol Engine Generator - 完整技能总结

## 🎯 技能概述

**名称**: `symbol-engine-generator`

**核心功能**: 将研究笔记或符号系统配置转换为可执行引擎模板

**支持领域**: 叙事游戏 / 决策系统 / 数据管道 / 研究框架 / 代码生成

**独特价值**: 自动提取符号系统 → 生成 JSON Schema → 可视化状态流转 → 编排任务执行

---

## 📁 完整文件结构

```
symbol-engine-generator/
├── SKILL.md                            # ✅ 核心技能定义（含标准提示词前缀）
│
├── 文档层 (Documentation)
│   ├── README.md                       # 技能使用指南
│   ├── QUICKSTART.md                   # 快速开始（基于你的现有文件）
│   ├── PROMPT_TEMPLATE.md              # 🆕 标准提示词模板库
│   ├── PROMPT_INTEGRATION_GUIDE.md     # 🆕 提示词集成指南
│   └── integration_guide.md            # 与现有研究笔记的集成
│
├── 参考层 (References)
│   ├── patterns.md                     # 领域模式（叙事/决策/数据/代码/研究）
│   ├── schema-spec.md                  # 完整 JSON Schema 定义
│   └── examples.md                     # 8个使用示例
│
├── 脚本层 (Scripts)
│   ├── generate_charts.py              # 图表生成（Mermaid → PNG）
│   └── download_assets.py              # 资源下载（Pinterest 素材）
│
└── 资产层 (Assets)
    ├── card-backgrounds/               # 卡片背景（5个占位符 + README）
    ├── character-illustrations/        # 人物插图（5个占位符 + README）
    └── world-materials/                # 世界素材（5个占位符 + README）
```

---

## 🔄 提示词三层架构

### 第 1 层：技能元数据 (SKILL.md frontmatter)

```yaml
name: symbol-engine-generator
description: Transform research notes into executable engine templates...
```

**作用**: 技能发现与触发

### 第 2 层：标准提示词前缀 (SKILL.md body)

```markdown
You are a Symbol Engine Architect specializing in...

CORE RESPONSIBILITIES:
1. Parse and validate symbolic systems
2. Design state machines
3. Build rule engines
4. Orchestrate 4-task architecture
5. Generate JSON Schema + documentation
6. Create visualizations

QUALITY STANDARDS:
- All symbols: name + definition + type
- State transitions: validated
- Rules: clear conditions, actions, priorities
- JSON: schema-valid
- Errors: actionable

OUTPUT DELIVERABLES:
- JSON: Engine configuration
- Markdown: Human-readable docs
- Visualizations: State flows, DAGs
- Logs: Execution trace
```

**作用**: 统一质量标准与架构定义

### 第 3 层：用户自定义 (PROMPT_TEMPLATE.md)

```
DOMAIN: [narrative/decision/data/research/code]
INPUT SOURCE: [你的输入文件]
MODE SETTINGS:
  - fast_mode: [true/false]
  - strict_mode: [true/false]
  - version: [1.0.0]
DOMAIN-SPECIFIC REQUIREMENTS:
  - [你的自定义要求]
```

**作用**: 特定领域与任务定制

---

## 🎨 四种使用模式

### 模式 1: 快速原型（Fast Mode）

```bash
# 最简调用
Use symbol-engine-generator to process files/research_notes/

# 实际执行的提示词
[L1: 技能元数据]
[L2: 标准提示词前缀]
[L3: 默认配置 - fast_mode=false, strict_mode=false]
```

**输出**: JSON + Markdown（无图表）

### 模式 2: 标准生成（Standard Mode）

```bash
# 标准调用
Use symbol-engine-generator with:
- Domain: narrative
- Input: files/research_notes/lin_game_engine.md
- Strict mode: true

# 实际执行的提示词
[L1: 技能元数据]
[L2: 标准提示词前缀]
[L3: 用户指定参数]
```

**输出**: JSON + Markdown + 图表 + 日志

### 模式 3: 完整自定义（Full Customization）

```bash
# 使用 PROMPT_TEMPLATE.md
[复制完整模板，填写所有占位符]

# 实际执行的提示词
[L1: 技能元数据]
[L2: 标准提示词前缀]
[L3: 完整自定义配置]
```

**输出**: 完全定制化的引擎模板

### 模式 4: 预设场景（Preset Scenarios）

```bash
# 选择预设场景（叙事/决策/数据/研究）
[复制对应场景模板]

# 实际执行的提示词
[L1: 技能元数据]
[L2: 标准提示词前缀]
[L3: 预设场景配置]
```

**输出**: 针对特定领域优化的模板

---

## 📊 输入输出映射

### 输入：你的研究笔记

```
files/
├── 02_角色卡示例x8.md              → 符号表（角色类型）
├── 04_规则卡示例x12.md             → 规则库（12条规则）
├── 03_世界观骨架模板.md            → 状态定义
└── 05_叙事章节Demo.md              → 状态流转
```

### 输出：引擎模板

```
files/data/
├── lin_narrative_engine_v1.0.json  # JSON Schema
└── data_summary.md                 # 可读文档

files/charts/
├── state_flow.png                  # 状态流转图
├── task_dag.png                    # 任务 DAG
└── symbol_distribution.png         # 符号分布图

files/logs/
└── execution_20260217.log          # 执行日志
```

---

## 🛠️ 核心工作流程

### Phase 1: 输入分析

```
1. Scan research notes
   ↓
2. Parse symbol structure
   - "符号表" → Extract symbols
   - "状态" + "→" → Extract transitions
   - "规则" + "当/if" → Extract rules
   ↓
3. Validate completeness
   - Missing symbols → Generate defaults
   - Missing states → Create initial
   - Missing rules → Add empty set
```

### Phase 2: 4-Task 并行执行

```
Main Task (Priority)
├─ Symbol system validation
├─ Conflict detection
└─ Schema generation

Parallel Subtasks
├─ Task 1: State flow diagram (Mermaid → PNG)
├─ Task 2: Rule engine initialization
└─ Task 3: JSON Schema generation

Fault Tolerance
└─ Chart generation fails → Mermaid text fallback
```

### Phase 3: 输出生成

```
1. JSON Output
   - engine_config: name, domain, modes
   - symbol_table: symbols with types
   - state: current, history, transitions
   - rules: conditions, actions, priorities
   - tasks: orchestration DAG
   - outputs: summary, visualizations, logs

2. Markdown Summary
   - Engine configuration
   - Symbol table (table format)
   - State definitions (Mermaid diagram)
   - Rules list (prioritized)
   - Task orchestration (DAG)
   - Execution results

3. Visualizations
   - State flow diagrams
   - Task DAG charts
   - Data plots

4. Logs
   - Execution trace
   - Errors and warnings
```

---

## 🎯 关键特性

### 1. 自动符号提取

**支持的格式**:
```markdown
## 符号表
- 变量名: 类型，描述

## Symbol Table
| name | type | definition |
```

**输出**:
```json
{
  "symbols": [{
    "name": "变量名",
    "type": "类型",
    "definition": "描述",
    "default": null,
    "constraints": []
  }]
}
```

### 2. 状态机验证

**支持的格式**:
```markdown
状态A → 状态B: 触发条件
State A → State B [trigger]
```

**验证项**:
- ✓ 循环依赖检测
- ✓ 不可达状态警告
- ✓ 初始/终止状态识别

**输出**: Mermaid 图表

### 3. 规则引擎构建

**支持的格式**:
```markdown
1. 当 [条件] → [动作]
   - 优先级: [数字]
   - 代价: [描述]
```

**提取**:
- condition (条件)
- action (动作)
- priority (优先级)
- cost (代价)
- counter_rule (反制规则)

### 4. 错误恢复

| 失败场景 | 降级策略 |
|---------|---------|
| 笔记读取失败 | 空模板 + errors[] |
| 符号提取失败 | 默认符号 + warnings[] |
| 图表生成失败 | Mermaid 文本 |
| JSON 写入失败 | 备份文件 |

---

## 📚 文档导航

### 新用户入门

1. **README.md** - 了解技能功能
2. **QUICKSTART.md** - 基于你的现有文件快速开始
3. **PROMPT_TEMPLATE.md** - 选择适合的提示词模板

### 深入学习

4. **PROMPT_INTEGRATION_GUIDE.md** - 理解提示词三层架构
5. **integration_guide.md** - 集成你的研究笔记
6. **references/patterns.md** - 学习领域模式

### 参考资料查询

7. **references/schema-spec.md** - 查阅完整 Schema
8. **references/examples.md** - 查看 8 个示例
9. **assets/*/README.md** - 了解资源使用

---

## 🚀 快速开始

### Step 1: 准备输入

```bash
# 复制你的研究笔记到标准位置
mkdir -p files/research_notes
cp files/02_角色卡示例x8.md files/research_notes/
cp files/04_规则卡示例x12.md files/research_notes/
```

### Step 2: 选择提示词模板

```bash
# 查看可用模板
cat skills/symbol-engine-generator/PROMPT_TEMPLATE.md

# 选择"场景 1: 叙事游戏引擎（临游戏）"
```

### Step 3: 调用技能

```
使用 symbol-engine-generator 技能：
- Domain: narrative
- Input: files/research_notes/
- Strict mode: true
- Character-driven rule modifications
- Moral entropy tracking
- Dynamic rule rewriting
```

### Step 4: 查看输出

```bash
# 生成的文件
ls files/data/
lin_narrative_engine_v1.0.json
data_summary.md

ls files/charts/
state_flow.png
task_dag.png
```

---

## 💡 最佳实践

### ✅ 推荐做法

1. **明确的领域指定**
   ```
   Domain: narrative ✅
   Domain: [missing] ❌
   ```

2. **首次使用严格模式**
   ```
   strict_mode: true  # 发现所有问题
   fast_mode: false   # 生成完整图表
   ```

3. **版本迭代**
   ```
   v1.0 → v1.1 → v2.0
   每次改进都升级版本号
   ```

4. **查看错误信息**
   ```
   errors[]: 修复必须项
   warnings[]: 优化建议项
   ```

### ❌ 避免做法

1. **跳过符号表定义**
2. **使用不一致的命名**
3. **忽略生成的警告**
4. **在生产环境使用 fast_mode**
5. **忘记备份研究笔记**

---

## 🎓 学习路径

### 初级（1-2 小时）

- [ ] 阅读 README.md
- [ ] 运行 QUICKSTART.md 中的示例
- [ ] 生成第一个引擎模板

### 中级（1-2 天）

- [ ] 理解 PROMPT_INTEGRATION_GUIDE.md
- [ ] 尝试不同领域模式（references/patterns.md）
- [ ] 自定义提示词模板

### 高级（1-2 周）

- [ ] 添加新的领域模式
- [ ] 贡献预设场景模板
- [ ] 优化脚本和工具

---

## 🆘 获取帮助

### 常见问题

**Q: 图表未生成？**
A: 检查 fast_mode 是否为 false，确保安装了 matplotlib 和 mmdc

**Q: 符号提取不完整？**
A: 使用明确的标题（## 符号表, ## 规则, ## 状态）

**Q: JSON 校验失败？**
A: 设置 strict_mode: false 查看详细错误，然后修复笔记

**Q: 如何集成现有文件？**
A: 参考 integration_guide.md

### 社区资源

- **技能目录**: `skills/symbol-engine-generator/`
- **示例文件**: `files/` (你的研究笔记)
- **参考文档**: `references/`

---

## 🎉 总结

**Symbol Engine Generator** 技能通过三层提示词架构（元数据 + 标准前缀 + 用户自定义），确保每次符号对象化活动都能获得：

✅ **高质量输出** - 统一的质量标准
✅ **结构化结果** - JSON + Markdown + 图表
✅ **可追溯性** - 完整的执行日志
✅ **可定制性** - 灵活的领域适配
✅ **容错能力** - 智能降级策略

**立即开始**: 选择一个提示词模板，体验符号系统对象化的强大能力！

---

**生成时间**: 2026-02-17
**技能版本**: 1.0.0
**文档版本**: Final
