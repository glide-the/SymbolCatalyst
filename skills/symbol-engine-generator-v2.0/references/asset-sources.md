# 素材资源获取指南（Asset Sourcing Guide）

当引擎输出需要可视化呈现时，以下资源可用于获取素材。

> **约束**：使用素材时，仅作为视觉载体（Tool/Carrier）。禁止将具体文化符号直接编码进引擎的符号系统。素材服务于对象化过程中的视觉呈现，不影响公理组与命题逻辑。

---

## 1. 规则卡视觉背景

规则卡（Proposition Card）输出时可能需要视觉背景图作为载体。

| 来源 | URL | 搜索关键词 | 说明 |
|------|-----|-----------|------|
| Pinterest | https://www.pinterest.com | `abstract art card background` / `minimalist texture` / `gradient card design` | 适合规则卡背景；使用抽象纹理/渐变，避免具象图腾 |
| Unsplash | https://unsplash.com | `abstract texture` / `gradient` / `minimal pattern` | 免费高质量图片，CC0 协议 |
| Pexels | https://www.pexels.com | `abstract background` / `dark texture` | 免费素材，商用友好 |
| Freepik | https://www.freepik.com | `abstract card template` / `minimalist card` | 部分免费，需署名；Premium 无需署名 |

**使用要点**：
- 选择抽象/几何/渐变风格，避免包含具体文化意象
- 推荐尺寸：750×1050px（标准卡片比例）
- 存放路径：`assets/card-backgrounds/`

---

## 2. 符号图谱节点图标

符号（Symbol）在可视化符号图谱时可使用图标增强可读性。

| 来源 | URL | 搜索关键词 | 说明 |
|------|-----|-----------|------|
| The Noun Project | https://thenounproject.com | `abstract symbol` / `node` / `force` / `tension` | 矢量图标库，按概念搜索 |
| Lucide Icons | https://lucide.dev | `circle` / `diamond` / `triangle` / `hexagon` | 开源 SVG 图标集，几何形状适合符号节点 |
| Heroicons | https://heroicons.com | `eye` / `lock` / `lightning-bolt` / `exclamation` | 抽象功能性图标 |
| Phosphor Icons | https://phosphoricons.com | `graph` / `node` / `flow` / `warning` | MIT 协议，风格一致 |

**使用要点**：
- 以几何抽象图形表示符号类型（圆=流动态，菱形=凝固态，六边形=幻想结）
- 颜色映射 valence 向量（如 tension → 红系，clarity → 蓝绿系）
- 存放路径：`assets/symbol-icons/`

---

## 3. 权力链与运转流程图示

权力链（PowerChain）和 10 阶段运转循环的可视化。

| 来源 | URL | 说明 |
|------|-----|------|
| Mermaid Live Editor | https://mermaid.live | 在线编辑 Mermaid 图表并导出 PNG/SVG；引擎内置 `scripts/generate_charts.py` 可直接生成 |
| draw.io / diagrams.net | https://app.diagrams.net | 免费流程图工具，适合复杂权力链可视化 |
| Excalidraw | https://excalidraw.com | 手绘风格图表，适合非正式展示 |
| Figma | https://figma.com | 专业设计工具，适合高保真输出 |

**使用要点**：
- 优先使用 `scripts/generate_charts.py` 自动生成 Mermaid 图（`--type power_chain` / `--type runtime_loop`）
- 手动美化时使用上述工具导入 .mmd 文件
- 存放路径：`assets/diagrams/`

---

## 4. 情绪色彩/Valence 调色板

valence 向量可视化时的色彩参考。

| 维度 | 推荐色相 | Hex 示例 |
|------|----------|----------|
| tension（张力） | 暖红/橙 | `#E63946` / `#F4845F` |
| oppression（压迫） | 深紫/暗灰 | `#4A0E4E` / `#3D3D3D` |
| seduction（诱惑） | 洋红/粉 | `#E91E90` / `#FF69B4` |
| hesitation（迟疑） | 淡蓝/雾灰 | `#A8DADC` / `#B0B0B0` |
| clarity（清明） | 青/绿 | `#06D6A0` / `#1D8A6E` |

来源参考:
- Coolors: https://coolors.co — 调色板生成器
- Adobe Color: https://color.adobe.com — 色彩理论工具

---

## 5. 字体资源

规则卡文本渲染时的字体选择。

| 字体 | 来源 | 用途 | 协议 |
|------|------|------|------|
| Noto Sans SC | https://fonts.google.com/noto/specimen/Noto+Sans+SC | 中文正文 | OFL |
| Inter | https://fonts.google.com/specimen/Inter | 英文界面/标签 | OFL |
| JetBrains Mono | https://www.jetbrains.com/lp/mono/ | 代码/JSON 展示 | OFL |
| LXGW WenKai | https://github.com/lxgw/LxgwWenKai | 中文标题/规则卡名称 | OFL |

---

## 6. 资源目录结构（推荐）

当需要使用视觉素材时，建议按以下结构组织：

```
assets/
├── card-backgrounds/     # 规则卡背景图（抽象/渐变/纹理）
├── symbol-icons/         # 符号节点图标（SVG/PNG）
├── diagrams/             # 权力链/运转流程图（Mermaid 导出）
├── palettes/             # 调色板配置文件
└── fonts/                # 字体文件
```

每个目录下建议放置 `index.json` 记录素材元数据：

```json
{
  "assets": [
    {
      "filename": "abstract_gradient_01.png",
      "source": "unsplash",
      "source_url": "https://unsplash.com/photos/xxx",
      "license": "CC0",
      "usage": "card-background",
      "notes": "抽象渐变，无具体文化意象"
    }
  ]
}
```

---

## 自动下载脚本

项目自带 `scripts/download_assets.py`，可自动下载或生成占位素材：

```bash
# 生成全部占位素材（无需 API key）
python scripts/download_assets.py --all --limit 5

# 从 Unsplash 下载抽象背景（需 API key）
python scripts/download_assets.py --type card-backgrounds --limit 5 --api-key YOUR_KEY

# 从 Lucide CDN 下载几何图标
python scripts/download_assets.py --type symbol-icons --source lucide --limit 8

# 生成色域配置 + 字体清单
python scripts/download_assets.py --type palettes
python scripts/download_assets.py --type fonts
```

支持的 `--type`：

| 类型 | 说明 |
|---|---|
| `card-backgrounds` | 抽象渐变/几何背景（Unsplash API 或 SVG 占位图） |
| `symbol-icons` | 几何图标（Lucide CDN 或 SVG 占位图） |
| `palettes` | 情绪色彩向量配色文件（JSON + CSS） |
| `fonts` | 字体清单 + bash 下载脚本 |

所有下载的素材会自动写入 `assets/` 目录，并生成 `index.json` 元数据。

---

## 边界声明

- 本指南仅提供素材获取方向，不替代对素材版权的独立核实
- 使用任何素材前，需确认其许可协议与使用场景匹配
- 当素材包含可识别的文化符号时，仅用于视觉载体层，不编码进 Symbol/Proposition 数据结构
