# Symbol Engine Generator - 快速索引

## 🎯 我想要...

### ...快速了解技能
→ 阅读 **[SKILL_SUMMARY.md](SKILL_SUMMARY.md)** (5分钟)

### ...立即开始使用
→ 阅读 **[QUICKSTART.md](QUICKSTART.md)** (基于你的现有文件)

### ...使用提示词模板
→ 查看 **[PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md)** (4个预设场景)

### ...理解提示词系统
→ 阅读 **[PROMPT_INTEGRATION_GUIDE.md](PROMPT_INTEGRATION_GUIDE.md)** (三层架构)

### ...集成我的研究笔记
→ 查看 **[integration_guide.md](integration_guide.md)** (文件映射)

### ...深入学习技能
→ 阅读 **[README.md](README.md)** (完整文档)

---

## 📁 文件导航

### 核心文件
- **SKILL.md** - 技能定义（含标准提示词前缀）
- **SKILL_SUMMARY.md** - 完整技能总结
- **QUICKSTART.md** - 快速开始指南
- **PROMPT_TEMPLATE.md** - 提示词模板库

### 集成指南
- **PROMPT_INTEGRATION_GUIDE.md** - 提示词集成指南
- **integration_guide.md** - 与研究笔记集成

### 参考文档
- **references/patterns.md** - 5种领域模式
- **references/schema-spec.md** - 完整JSON Schema
- **references/examples.md** - 8个使用示例

### 工具脚本
- **scripts/generate_charts.py** - 图表生成
- **scripts/download_assets.py** - 资源下载

### 素材资源
- **assets/card-backgrounds/** - 卡片背景（塔罗牌风格）
- **assets/character-illustrations/** - 人物插图
- **assets/world-materials/** - 世界观素材

---

## 🚀 三步快速开始

### 1️⃣ 选择提示词模板

```bash
# 查看模板
cat skills/symbol-engine-generator/PROMPT_TEMPLATE.md
```

### 2️⃣ 准备输入文件

```bash
# 复制研究笔记
mkdir -p files/research_notes
cp files/0*.md files/research_notes/
```

### 3️⃣ 调用技能

```
使用 symbol-engine-generator 技能：
- Domain: narrative
- Input: files/research_notes/
- Strict mode: true
```

---

## 📊 快速参考

### 支持的领域

| 领域 | 用途 | 模板 |
|------|------|------|
| **narrative** | 叙事游戏、交互小说 | 预设场景1 |
| **decision** | 决策系统、工作流 | 预设场景2 |
| **data** | 数据管道、ETL | 预设场景3 |
| **research** | 研究框架、学术笔记 | 预设场景4 |
| **code** | 代码生成、脚手架 | 自定义 |

### 模式开关

| 模式 | 值 | 效果 |
|------|-----|------|
| **fast_mode** | true | 跳过图表，仅JSON+MD |
| **fast_mode** | false | 生成完整图表 |
| **strict_mode** | true | 强制Schema校验 |
| **strict_mode** | false | 宽松模式 |

### 输出文件

```
files/data/
├── [domain]_[timestamp]_v[version].json  # 引擎配置
└── data_summary.md                       # 可读文档

files/charts/
├── state_flow.png                        # 状态流转图
└── task_dag.png                          # 任务DAG

files/logs/
└── execution_[timestamp].log             # 执行日志
```

---

## 🎨 提示词三层架构

```
L1: 技能元数据 (SKILL.md frontmatter)
  ↓ 触发技能
L2: 标准提示词前缀 (SKILL.md body)
  ↓ 统一质量标准
L3: 用户自定义参数 (你的输入)
  ↓ 特定领域定制
```

**参考**: [PROMPT_INTEGRATION_GUIDE.md](PROMPT_INTEGRATION_GUIDE.md)

---

## 💡 常见任务

### 任务1: 生成叙事引擎

```
使用 PROMPT_TEMPLATE.md 中的"场景1: 叙事游戏引擎"
替换 [INPUT SOURCE] 为你的文件路径
```

### 任务2: 快速原型开发

```
设置 fast_mode: true
跳过图表生成，仅输出核心配置
```

### 任务3: 生产部署验证

```
设置 strict_mode: true
强制完整Schema校验，报告所有问题
```

### 任务4: 集成现有笔记

```
参考 integration_guide.md
映射你的研究文件到符号系统组件
```

---

## 🆘 故障排查

| 问题 | 解决方案 |
|------|---------|
| 图表未生成 | 检查 fast_mode=false, 安装 matplotlib+mmdc |
| 符号提取不完整 | 使用明确标题（## 符号表） |
| JSON校验失败 | 设置 strict_mode=false 查看详细错误 |
| 技能未触发 | 更新 SKILL.md description |

---

## 📚 学习路径

```
初学者 (1-2小时)
  ├─ QUICKSTART.md
  ├─ 生成第一个模板
  └─ 查看输出文件

进阶用户 (1-2天)
  ├─ PROMPT_INTEGRATION_GUIDE.md
  ├─ references/patterns.md
  └─ 尝试不同领域

高级用户 (1-2周)
  ├─ 修改提示词模板
  ├─ 添加新的领域模式
  └─ 优化脚本工具
```

---

## 🎯 核心价值

✅ **自动化** - 从笔记到引擎模板，全自动流程
✅ **结构化** - JSON Schema + Markdown + 图表
✅ **可复用** - 模板化设计，支持多领域
✅ **可视化** - 状态流转图、任务DAG
✅ **容错性** - 智能降级，错误恢复

---

## 🔗 相关技能

- `superpowers:brainstorming` - 设计符号系统前的头脑风暴
- `superpowers:writing-plans` - 编写详细的实施计划
- `skill-creator` - 创建新的定制技能

---

**开始使用**: 从 [QUICKSTART.md](QUICKSTART.md) 或 [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md) 开始！

**深入理解**: 阅读 [SKILL_SUMMARY.md](SKILL_SUMMARY.md) 和 [PROMPT_INTEGRATION_GUIDE.md](PROMPT_INTEGRATION_GUIDE.md)

**完整文档**: 参考 [README.md](README.md)
