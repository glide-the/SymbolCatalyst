# 角色设定评价系统接入 — 执行 Issue 清单

> 基于 `doc/角色设定评价系统设计师与引擎规范分析.md` 修订后的结论：skill 本身就是转换模块系统，`game-engine-package` 可直接导入角色设定评价系统。

---

## Issue 1: 创建 Agent 配置，集成三个 skill 的流水线

**优先级**: P0
**标签**: `agent-config`, `pipeline`

**描述**:
将 `symbol-engine-generator-v2.0`、`object-engine-generator-v1.0`、`game-engine-generator-v1.0` 三个 skill 注册到 agent 配置中，定义按阶段顺序执行的流水线。

**验收条件**:
- [ ] agent 配置文件（`.agent.md` 或同类格式）已创建，包含三个 skill 的注册声明
- [ ] 流水线阶段顺序明确：skill 1 → skill 2 → skill 3
- [ ] 每个阶段的输入/输出数据传递协议已定义
- [ ] agent 可被正常加载，skill 可被正常调用

**关联文件**:
- `skills/symbol-engine-generator-v2.0/SKILL.md`
- `skills/object-engine-generator-v1.0/SKILL.md`
- `skills/game-engine-generator-v1.0/SKILL.md`

---

## Issue 2: 统一 `symbol_engine*.json` 中的路径为相对路径

**优先级**: P0
**标签**: `path-normalization`, `data`

**描述**:
审查 `files/data/symbol_engine_20260218_v2.0.json` 中的 `outputs.visualizations`、`outputs.logs`、`outputs.data_files` 等字段，将所有绝对路径或不规范路径转换为相对于包根目录的路径。

**验收条件**:
- [ ] `symbol_engine*.json` 中所有 `path` / `file` / `source` 类字段使用相对路径
- [ ] 路径格式统一为 POSIX 风格（`/` 分隔符），无 `/Users/...` 前缀
- [ ] 路径引用的文件在包目录结构中实际存在
- [ ] 编写路径校验脚本，可自动检测绝对路径残留

**关联文件**:
- `files/data/symbol_engine_20260218_v2.0.json`

---

## Issue 3: 统一素材索引 `index.json` 中的路径为相对路径

**优先级**: P0
**标签**: `path-normalization`, `assets`

**描述**:
审查 `skills/*/assets/*/index.json` 中的资源引用路径，确保全部使用相对路径。

**验收条件**:
- [ ] `card-backgrounds/index.json`、`character-illustrations/index.json`、`world-materials/index.json` 等所有索引文件中的路径为相对路径
- [ ] `symbol-icons/index.json`、`palettes/index.json`、`fonts/index.json` 同样处理
- [ ] 路径可在压缩包解压后正确解析

**关联文件**:
- `skills/symbol-engine-generator-v2.0/assets/*/index.json`
- `skills/object-engine-generator-v1.0/assets/*/index.json`

---

## Issue 4: 完善 Skill 3 打包逻辑，输出 `game-engine-package.zip`

**优先级**: P1
**标签**: `packaging`, `skill-3`

**描述**:
完善 `game-engine-generator-v1.0` 的打包流程，确保最终输出一个结构合规的 `game-engine-package.zip`，可直接被角色设定评价系统导入。

**验收条件**:
- [ ] Skill 3 工作流明确定义 zip 打包步骤
- [ ] 压缩包目录结构规范化：
  ```
  game-engine-package/
  ├── data/
  │   ├── symbol_engine_*.json        # 主规则数据
  │   ├── data_summary.md             # 引擎摘要
  │   └── research_notes/             # 语义补层
  ├── charts/
  │   └── state_flow.mmd              # 状态流图
  ├── logs/
  │   └── rule_engine_pseudo.txt      # 执行伪代码
  ├── assets/                         # 素材资源
  │   ├── card-backgrounds/
  │   ├── character-illustrations/
  │   └── world-materials/
  └── game-engine-generator-prompt.md # 系统提示词
  ```
- [ ] 所有包内路径为相对路径
- [ ] 包可被正常解压并保持目录结构完整

**关联文件**:
- `skills/game-engine-generator-v1.0/SKILL.md`
- `skills/game-engine-generator-v1.0/assets/prompt-template.md`

---

## Issue 5: 定义 `game-engine-package` 导入协议规范

**优先级**: P1
**标签**: `protocol`, `documentation`

**描述**:
编写压缩包的导入协议文档，明确角色设定评价系统导入 `game-engine-package` 时的文件要求、必填字段、可选字段、版本兼容策略。

**验收条件**:
- [ ] 协议文档创建，包含以下内容：
  - 必须包含的文件列表与命名约定
  - `symbol_engine*.json` 的最小必填字段集（`engine_config`、`symbol_table`、`rules`、`state`）
  - 可选字段列表与默认行为
  - 版本号格式与兼容性规则
  - 素材资源引用的路径规范（相对路径要求）
- [ ] 提供一份 JSON Schema 用于校验包内 `symbol_engine*.json` 的结构合规性

---

## Issue 6: 端到端验证 — 用现有样本走完 skill 流水线

**优先级**: P1
**标签**: `validation`, `e2e`

**描述**:
使用现有 `files/` 下的样本数据，执行完整的 skill 1 → skill 2 → skill 3 流水线，验证生成的 `game-engine-package.zip` 是否结构合规。

**验收条件**:
- [ ] 以 `files/data/symbol_engine_20260218_v2.0.json` 作为 skill 2 产出样本输入 skill 3
- [ ] skill 3 成功生成 `game-engine-generator-prompt.md`
- [ ] skill 3 成功输出 `game-engine-package.zip`
- [ ] 解压后的包结构符合 Issue 4 定义的目录规范
- [ ] 包内所有路径为相对路径（可通过 Issue 2 的校验脚本检测）
- [ ] `symbol_engine*.json` 通过 JSON Schema 校验（Issue 5 的 Schema）

---

## Issue 7: 补充 Skill 间数据传递的中间格式说明

**优先级**: P2
**标签**: `documentation`, `pipeline`

**描述**:
当前三个 skill 的 SKILL.md 各自定义了输入输出，但缺少 skill 间数据交接的显式格式说明。需要补充文档明确：
- Skill 1 → Skill 2 传递的数据格式（O1-O5 的具体 JSON 结构约束）
- Skill 2 → Skill 3 传递的数据格式（`symbol_engine*.json` + 补充文件列表）

**验收条件**:
- [ ] 在 `doc/` 或对应 skill 的 `references/` 下新增数据传递格式说明
- [ ] 格式说明包含字段列表、类型约束、必填/可选标记
- [ ] Skill 2 的 `schema-spec.md` 与 Skill 1 的输出格式一致或有显式转换说明

**关联文件**:
- `skills/symbol-engine-generator-v2.0/references/schema-spec.md`
- `skills/object-engine-generator-v1.0/references/schema-spec.md`

---

## Issue 8: 同步更新 `08_角色设定评价系统接入说明.md`

**优先级**: P2
**标签**: `documentation`, `sync`

**描述**:
`08_角色设定评价系统接入说明.md` 仍基于旧的理解（SymbolCatalyst 只是资产归档仓，需要外部转换模块），需要同步更新以反映"skill 即转换模块"的正确定位。

**验收条件**:
- [ ] 移除"需要在运行时工程中实现独立转换模块"的描述
- [ ] 更新项目定位为"承载 skill 流水线的 agent 工作空间"
- [ ] 更新"下一步最小落地动作"为 agent 配置 + 打包 + 端到端验证
- [ ] 与 `doc/角色设定评价系统设计师与引擎规范分析.md` 的结论保持一致

**关联文件**:
- `08_角色设定评价系统接入说明.md`
- `doc/角色设定评价系统设计师与引擎规范分析.md`

---

## Issue 9: 编写路径校验脚本

**优先级**: P2
**标签**: `tooling`, `validation`

**描述**:
编写一个校验脚本，可自动扫描 `game-engine-package` 目录或 zip 中的所有 JSON 文件，检测是否存在绝对路径引用。

**验收条件**:
- [ ] 脚本支持扫描目录或 zip 文件
- [ ] 检测所有 JSON 文件中的 `path`、`file`、`source`、`url` 等字段
- [ ] 对包含绝对路径的字段输出警告信息（文件名 + 字段路径 + 当前值）
- [ ] 返回失败退出码（如有绝对路径）或成功退出码（全部合规）

---

## Issue 10: 审查 `resourceManifest` 配置块的完整性

**优先级**: P2
**标签**: `data-quality`, `validation`

**描述**:
对照分析文档 3.5 节中定义的目标配置块列表，审查当前 `symbol_engine_20260218_v2.0.json` 中已覆盖哪些块、缺失哪些块，并标记需要 skill 流水线补全的内容。

**验收条件**:
- [ ] 产出一份覆盖率报告：`meta` / `symbolDictionary` / `variableModel` / `ruleCatalog` / `runtimeRuleCards` / `stateModel` / `promptAssets` / `resourceManifest` / `trace` / `reviewQueue` 各块的完成度
- [ ] 对缺失的块标注"应由哪个 skill 阶段补全"
- [ ] 如有块需要手动补充，列出具体字段和建议值

**关联文件**:
- `files/data/symbol_engine_20260218_v2.0.json`
- `doc/角色设定评价系统设计师与引擎规范分析.md` 第 3.5 节

---

## 执行优先级总览

| 优先级 | Issue | 核心工作 |
| --- | --- | --- |
| **P0** | #1 | Agent 配置与 skill 流水线集成 |
| **P0** | #2 | symbol_engine JSON 路径标准化 |
| **P0** | #3 | 素材索引路径标准化 |
| **P1** | #4 | Skill 3 打包逻辑完善 |
| **P1** | #5 | 导入协议规范文档 |
| **P1** | #6 | 端到端验证 |
| **P2** | #7 | Skill 间数据传递格式说明 |
| **P2** | #8 | 顶层接入文档同步更新 |
| **P2** | #9 | 路径校验脚本 |
| **P2** | #10 | 配置块覆盖率审查 |

建议执行顺序：先完成 P0（#1→#2→#3），再推进 P1（#4→#5→#6），最后补齐 P2。
