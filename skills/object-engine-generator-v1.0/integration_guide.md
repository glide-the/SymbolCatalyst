# Integration Guide: Connecting Your Research Notes to Symbol Engine Generator

## 概述

本指南说明如何将你现有的 **"临游戏叙事引擎"** 研究文件与新的 **symbol-engine-generator** 技能连接，实现自动化引擎模板生成。

## 📋 你的研究文件映射

### 文件 → 符号系统组件

| 研究文件 | 提取内容 | 符号系统组件 |
|---------|---------|-------------|
| `02_角色卡示例x8.md` | 8个角色定义 | **符号表** - 角色类型、性格、动机 |
| `04_规则卡示例x12.md` | 12条游戏规则 | **规则库** - 条件、动作、优先级 |
| `03_世界观骨架模板.md` | 世界观状态 | **状态定义** - 初始状态、转换触发器 |
| `05_叙事章节Demo.md` | 剧情流程 | **状态流转** - 章节之间的转换 |
| `06_商业模式x3.md` | 运营模式 | **任务编排** - 并行任务 DAG |

### 自动提取规则

技能会自动识别以下模式：

```markdown
## 符号表 / Symbol Table
- 变量名: 类型，描述

## 规则 / Rules
1. 当 [条件] → [动作]

## 状态 / States
状态A → 状态B: 触发条件
```

## 🔧 快速集成

### 方法 1: 创建主入口文件

创建一个整合文件引用所有研究笔记：

```bash
# 创建 research_notes 目录
mkdir -p files/research_notes

# 创建主入口文件
cat > files/research_notes/lin_engine_master.md << 'EOF'
# 临游戏叙事引擎 - 主配置文件

## 引擎信息
- 名称: lin_narrative_engine
- 领域: narrative
- 版本: 1.0.0
- 模式: strict_mode: true

## 符号表引用
@import: ../02_角色卡示例x8.md
  提取: 所有角色定义作为符号

## 规则库引用
@import: ../04_规则卡示例x12.md
  提取: 所有规则卡转换为规则格式

## 状态定义
@import: ../03_世界观骨架模板与示例.md
  提取: 世界观状态作为初始状态

## 状态流转
@import: ../05_叙事章节Demo与动态改写算法.md
  提取: 章节转换作为状态转换

## 任务编排
@import: ../06_商业模式x3与内容生成模板.md
  提取: 运营流程作为任务 DAG
EOF
```

### 方法 2: 直接使用现有文件

技能支持直接处理多个文件：

```bash
# 符号引擎会自动扫描目录
files/research_notes/
├── 02_角色卡示例x8.md
├── 04_规则卡示例x12.md
├── 03_世界观骨架模板.md
├── 05_叙事章节Demo.md
└── 06_商业模式x3.md
```

直接复制文件到 research_notes 目录：

```bash
cp files/02_角色卡示例x8.md files/research_notes/
cp files/04_规则卡示例x12.md files/research_notes/
cp files/03_世界观骨架模板与示例.md files/research_notes/
cp files/05_叙事章节Demo与动态改写算法.md files/research_notes/
```

## 🎯 完整工作流

### Step 1: 准备输入

```bash
# 复制研究笔记
mkdir -p files/research_notes
cp files/0*.md files/research_notes/

# 可选：创建主配置
cat > files/research_notes/engine_config.yaml << 'EOF
engine:
  name: lin_narrative_engine
  domain: narrative
  fast_mode: false
  strict_mode: true

input_files:
  - 02_角色卡示例x8.md
  - 04_规则卡示例x12.md
  - 05_叙事章节Demo与动态改写算法.md

output:
  format: [json, markdown]
  include_charts: true
EOF
```

### Step 2: 调用技能

在对话中：

```
请使用 symbol-engine-generator 技能
处理 files/research_notes/ 下的所有笔记
```

### Step 3: 查看输出

```bash
# 生成的文件
tree files/data files/charts

files/data/
├── lin_narrative_engine_20260217_v1.0.json
└── data_summary.md

files/charts/
├── state_flow.png
├── task_dag.png
└── symbol_distribution.png
```

## 📊 数据流图

```
研究笔记 (Markdown)
    ↓
[符号提取器]
    ↓
符号表 + 状态 + 规则
    ↓
[4-Task 编排器]
    ↓
JSON Schema + Markdown + 图表
    ↓
可执行引擎模板
```

## 🔍 提取示例

### 从角色卡提取符号

**输入** (`02_角色卡示例x8.md`):
```markdown
## 信息掮客
- 性格: 机会主义、不可知论者
- 动机: 建立独立信息网络
- 禁忌: 不能承诺绝对忠诚
```

**输出** (符号表):
```json
{
  "name": "信息掮客",
  "type": "角色类型",
  "definition": "以信息交易为生的中立角色",
  "default": {
    "性格": ["机会主义", "不可知论者"],
    "动机": "建立独立信息网络",
    "禁忌": "不能承诺绝对忠诚"
  }
}
```

### 从规则卡提取规则

**输入** (`04_规则卡示例x12.md`):
```markdown
## 规则卡 01：信誉契约
- 触发: 当你向NPC做出「正式承诺」时
- 效果: 立即获得资源 ×2
- 代价: 承诺期间「信誉度」锁定，若违约则扣除信誉 ×3
```

**输出** (规则):
```json
{
  "id": "rule_credit_contract",
  "condition": "player_makes_promise_to_npc() == true",
  "action": "multiply_resource(2) AND lock_reputation()",
  "priority": 10,
  "cost": {
    "type": "conditional",
    "value": "reputation * 3",
    "trigger": "promise_broken"
  }
}
```

### 从叙事Demo提取状态流转

**输入** (`05_叙事章节Demo.md`):
```markdown
### 【开场序列】→【剧情推进 1：集市偶遇】→【抉择点 1】→【抉择后分支】
```

**输出** (状态转换):
```json
{
  "from": "开场序列",
  "to": "剧情推进_1",
  "trigger": "player_presses_space",
  "condition": null
}
```

## 🛠️ 自定义提取规则

如果自动提取不理想，可以添加提示：

```markdown
<!-- @symbol-extract-priority: high -->
## 关键符号
- 信誉度: 核心状态变量
- 道德熵: 隐藏变量，玩家不可见

<!-- @rule-format: structured -->
## 规则定义
使用格式: 当 [条件] → [效果] | 代价: [代价]

<!-- @state-flow: explicit -->
## 状态流转
使用格式: 状态A → 状态B [触发条件]
```

## 📈 迭代优化

### 第1次运行

```bash
# 初次生成
Input: 原始研究笔记
Output: v1.0 引擎模板

# 查看生成的 JSON
cat files/data/lin_narrative_engine_v1.0.json
```

### 第2次优化

```bash
# 根据输出调整笔记
# 添加缺失的符号定义
# 修正规则条件

# 重新生成
Input: 优化后的笔记
Output: v1.1 引擎模板
```

### 第3次完善

```bash
# 添加可视化资源
# 下载 Pinterest 素材

# 最终生成
Input: 完整笔记 + 资源
Output: v2.0 生产就绪引擎
```

## 🎨 资源集成

### 使用提供的占位符

技能已生成占位符素材：

```bash
# 卡片背景
ls skills/symbol-engine-generator/assets/card-backgrounds/
placeholder_001.svg  # 可替换为塔罗牌风格背景

# 人物插图
ls skills/symbol-engine-generator/assets/character-illustrations/
placeholder_001.svg  # 可替换为角色插画

# 世界素材
ls skills/symbol-engine-generator/assets/world-materials/
placeholder_001.svg  # 可替换为废土风格素材
```

### 从 Pinterest 下载真实素材

```bash
# 查看下载说明
cat skills/symbol-engine-generator/assets/card-backgrounds/README.md

# 手动下载后替换
mv ~/Downloads/tarot_bg_01.png \
   skills/symbol-engine-generator/assets/card-backgrounds/placeholder_001.svg
```

## 🔗 与其他系统集成

### 导出到游戏引擎

```bash
# 生成 Unity C# 类
python skills/symbol-engine-generator/scripts/export_unity.py \
  --input files/data/lin_narrative_engine_v1.0.json \
  --output unity_scripts/

# 生成 Unreal Blueprints
python skills/symbol-engine-generator/scripts/export_unreal.py \
  --input files/data/lin_narrative_engine_v1.0.json \
  --output blueprints/
```

### 集成到内容工具链

```bash
# 导出为 Markdown 格式（便于内容编辑）
python skills/symbol-engine-generator/scripts/export_markdown.py \
  --input files/data/lin_narrative_engine_v1.0.json \
  --output content_tools/
```

## 📝 最佳实践

### 1. 保持笔记结构化

```markdown
## 符号表
使用列表格式，每个符号一行

## 规则
使用编号列表，包含条件、动作、优先级

## 状态
使用箭头表示转换：A → B: trigger
```

### 2. 使用一致的命名

```markdown
# 好的命名
信誉度 (reputation)
道德熵 (moral_entropy)

# 避免使用
信誉 / Reputation / rep (不统一)
```

### 3. 添加元数据

```markdown
## 元数据
- 作者: 你的名字
- 版本: 1.0
- 最后更新: 2026-02-17
- 状态: 草稿/测试/生产
```

### 4. 版本控制

```bash
# 使用 Git 跟踪变更
git add files/research_notes/
git commit -m "Update rules: add moral_entropy mechanics"

# 生成新版本时自动升级版本号
v1.0 → v1.1 → v2.0
```

## 🚀 下一步

1. **运行首次生成** - 使用现有笔记生成 v1.0 模板
2. **审查输出** - 检查 JSON Schema 和 Markdown 文档
3. **调整笔记** - 根据提取结果优化笔记格式
4. **添加资源** - 下载 Pinterest 素材替换占位符
5. **迭代完善** - 重复以上步骤直到满意

## 🆘 故障排查

### 问题：符号提取不完整

**解决**：在笔记中添加明确的标记
```markdown
<!-- @symbol: 信誉度 -->
- 类型: 状态变量
- 范围: 0-100
```

### 问题：规则条件无法解析

**解决**：使用结构化格式
```markdown
## 规则: 信誉契约
- 条件: player_makes_promise()
- 效果: resource *= 2
- 代价: reputation *= 3 (if promise_broken)
```

### 问题：状态流转缺失

**解决**：显式声明转换
```markdown
## 状态流转
初始 → 角色_选择: player_clicks_start
角色_选择 → 世界_生成: player_confirms_character
```

---

**开始使用：**

```
请使用 symbol-engine-generator 技能处理 files/research_notes/ 下的所有文件
```
