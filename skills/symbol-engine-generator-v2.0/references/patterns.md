# 运转模式详解 + 伪代码 + 巫术检测算法 + 可选增强

## Table of Contents

1. [10阶段运转模式详解](#10阶段运转模式详解)
2. [巫术检测算法](#巫术检测算法)
3. [最小伪代码](#最小伪代码)
4. [可选增强](#可选增强)

---

## 10阶段运转模式详解

### Stage 1: 感受场进入（Field Ingestion）

**输入**：`discourse_flow: string`（话语流 I1）

**处理**：
1. 对话语流进行 n-gram 分析（n=2,3,4），提取重复频次 ≥ 2 的片段
2. 标记"未出现在任何已知定义中"的重复片段为幻想候选
3. 计算每个候选的初始 force_index = frequency × length_weight
4. 按 force_index 降序排列

**输出**：`fantasy_candidates[{fragment, frequency, force_index, position}]`

**失败策略**：
- 话语流为空 → 返回空列表 + SilenceReport entry: `{type: "information_insufficient", reason: "无话语流输入"}`
- 话语流过短（< 50字符） → 降低 n-gram 范围至 n=2，标记 `low_confidence`

---

### Stage 2: 切片化（Slicing）

**输入**：`fantasy_candidates[]`

**处理**：
1. 对每个候选执行范指切片：
   - **重复点**：标记片段在话语流中的所有出现位置
   - **否定可插入点**：识别片段中可被否定的子词（名词/动词/形容词/副词），标记为 negation_slots
   - **因果连接点**：检测"因为/所以/导致/使得/触发"等因果连接词的位置
   - **边界词**：检测"但是/然而/除非/只有/仅当"等边界标记词
2. 生成 raw_symbol 结构：`{fragment, positions[], negation_slots[], causal_joints[], boundary_words[]}`

**输出**：`raw_symbols[]`

**失败策略**：
- 无可切片内容 → 生成最小符号集：`[{label: "未分化场", carrier: input_carrier, valence: {tension: 0}}]`
- 切片结果 > 100 → 按 force_index 截取 top 50，标记 `truncated`

---

### Stage 3: 凝固（Freezing）

**输入**：`raw_symbols[]`

**处理**：
1. 对每个 raw_symbol 统计其"解释性使用"次数：
   - 自我解释：片段被用于定义自身（A is A 结构） → self_ref_count
   - 世界解释：片段被用于定义其他对象 → cross_ref_count
2. 凝固判定：`self_ref_count + cross_ref_count ≥ freeze_threshold`（默认 threshold = 3）
3. 达到阈值的片段凝固为正式 Symbol + Definition
4. 未达阈值的保持"流动态"标记

**输出**：`frozen_symbols[]` + `frozen_definitions[]` + `fluid_symbols[]`

**失败策略**：
- 无片段达到阈值 → 降低 threshold 至 2 并重试一次
- 降低后仍无 → 保持全部为流动态，标记 `no_freezing_occurred`

---

### Stage 4: 结构筛选（Exclusivity Filtering）

**输入**：`frozen_symbols[]`

**处理**：
1. 扫描符号间的对立关系（valence 向量余弦相似度 < -0.5 的符号对）
2. 检测系统性排他：某符号的出现是否总伴随另一符号的缺失
3. 提取排他机制类型：
   - `binary_opposition`：二元对立
   - `categorical_exclusion`：类别排除（某类符号被系统性忽略）
   - `boundary_enforcement`：边界强制（某些符号不允许跨越特定边界）
   - `silence_induction`：沉默诱导（某些符号的出现导致讨论终止）
4. 生成筛选器列表

**输出**：`exclusivity_filters[]`

**失败策略**：
- 无排他信号 → 生成默认开放筛选器：`{filter_type: "none", condition: "all symbols accepted"}`
- 检测到全排他（排除 >80% 符号） → 标记 `over_filtering_warning`

---

### Stage 5: 符号化与秩序化（Symbolization & Ordering）

**输入**：`frozen_symbols[]` + `exclusivity_filters[]`

**处理**：
1. 为每个凝固符号生成完整 Symbol 结构（id/label/valence/carrier/origin/time_form）
2. 情绪色彩向量化：
   - 从上下文窗口提取情绪词 → 映射到 valence 维度
   - 向量归一化到 [-1, 1]
3. 时间化标记：
   - 分析符号的时态倾向（过去/现在/未来语境）
   - 分配 time_form 权重（三值之和 ≈ 1.0）
4. 构建幻想结：
   - 将重复模式 + 排他筛选 + 权力链触发度 组合为 FantasyKnot
   - 计算 force_index = frequency × exclusivity_strength × power_trigger
5. 生成符号图谱（节点=符号，边=共现/因果/排他关系）

**输出**：`symbol_graph{symbols[], edges[]}` + `fantasy_knots[]`

**失败策略**：
- 向量化失败（无情绪词匹配） → 保留文本标签，标记 `unquantified`
- time_form 无法分配 → 默认 `{past: 0.33, present: 0.34, future: 0.33}`

---

### Stage 6: 命题生成（Proposition Generation）

**输入**：`symbol_graph` + `fantasy_knots[]`

**处理**：
1. 从符号图谱的边（因果关系/共现关系）生成候选命题
2. 每条命题必须构造：
   - `statement`：抽象规则文本
   - `causal_form`：明确 antecedent/consequent/direction
   - `boundary`：适用载体 + 条件 + 排除域
   - `failure_conditions`：至少 1 条（触发时降级为 silence/hypothesis/rewrite/discard）
3. 计算初始 witchcraft_risk（基于 Stage 8 信号的预扫描）
4. 附加 rewrite_hooks（标记可改写字段）

**输出**：`propositions[]`

**失败策略**：
- 无法生成边界 → 标记 `ideology_risk`，命题降级为假设
- 无法生成失败条件 → witchcraft_risk += 0.4，强制标记

---

### Stage 7: 追问驱动（Interrogation Driver）

**输入**：`propositions[]` + observer_stance.interrogation_intensity

**处理**：
1. 对每条命题的 statement 进行子词分解
2. 对每个子词执行否定操作：
   - 名词否定："X" → "非X" / "X的缺失"
   - 动词否定："做" → "不做" / "反向做"
   - 量词否定："所有" → "部分" / "无"
3. 从否定结果重构替代命题
4. 评估因果反馈：原命题的 causal_form 如何塑造了其 statement 的表达方式
5. 标记"结构封闭"警告：若否定后命题仍完全自洽
6. 根据 interrogation_intensity 决定展开深度（0=跳过，10=全部子词）

**输出**：`alternative_propositions[]` + `causal_feedback_analysis`

**失败策略**：
- 否定后全部自洽 → 标记 `structurally_closed`，witchcraft_risk += 0.2
- 替代命题爆炸（> 50条） → 按 relevance 截取 top 20

---

### Stage 8: 巫术检测（Witchcraft Detector）

**输入**：`propositions[]` + `alternative_propositions[]`

**处理**：详见下方 [巫术检测算法](#巫术检测算法)

**输出**：`witchcraft_scores[]` + 处置决策列表

**失败策略**：
- 检测器无法判定 → 保守处理，全部标记 `risk = 0.5`
- 检测器自身进入递归（检测规则引用自身） → 中止，输出 `detector_recursion` 警告

---

### Stage 9: 权力链改写（Power Rewrite）

**输入**：`propositions[]` + `reality_mapping_vars (I4)` + `power_chains[]`

**处理**：
1. 将 I4 变量映射到权力链的 motion_links intensity：
   - `credibility` → 影响"意识形态"链节
   - `power_distance` → 影响"权力聚合"和"意志集中"链节
   - `commitment_cost` → 影响"原则化"链节
   - `compliance_pressure` → 影响"集体认同"链节
   - `information_asymmetry` → 影响所有链节的 `obscure` 倾向
2. 计算权力链对每条命题的 effect_on_rules
3. 执行改写：
   - `strengthen`：收紧命题的 causal_form
   - `exclude`：缩小 boundary，增加 excluded_domains
   - `expand`：放宽 boundary
   - `contract`：缩小 statement 的适用范围
   - `obscure`：增加 witchcraft_risk，可能触发沉默
4. 记录所有改写到 RewriteLog

**输出**：`rewritten_propositions[]` + `rewrite_log_entries[]`

**失败策略**：
- 无 I4 输入 → 跳过本阶段，保持原命题
- 权力链为空 → 跳过本阶段

---

### Stage 10: 输出封装（Packaging）

**输入**：所有阶段产出

**处理**：
1. 组装 O1: SymbolGraphSnapshot（symbols + fantasy_knots + power_chains + metadata）
2. 组装 O2: RuleDeck（propositions + deck_metadata）
3. 组装 O3: RewriteLog（收集所有改写记录）
4. 组装 O4: SilenceReport（收集所有沉默决策）
5. 组装 O5: InterrogationSeeds（从 alternative_propositions 中提取可检验问题）
6. 生成 JSON 版本 + 可读文本版本

**输出**：`{O1, O2, O3, O4, O5}` × 2（JSON + Markdown）

**失败策略**：
- 部分数据缺失 → 输出已有数据 + 缺失字段报告
- JSON 序列化失败 → 降级为纯文本输出

---

## 巫术检测算法

### 信号定义

```
SIGNAL_1: 定义自指环 (Self-Referential Loop)
  检测: 在定义图中寻找长度 ≤ 3 的环
    def_graph = build_graph(definitions, references)
    cycles = find_cycles(def_graph, max_length=3)
    FOR each cycle:
      IF cycle 不包含任何外部验证锚点（非自生成的观察/测量）:
        risk += 0.3

SIGNAL_2: 因果倒置 (Causal Inversion)
  检测: 在话语流中，consequent 出现的位置 < antecedent 出现的位置
    FOR each proposition:
      consequent_pos = first_occurrence(prop.causal_form.consequent, discourse_flow)
      antecedent_pos = first_occurrence(prop.causal_form.antecedent, discourse_flow)
      IF consequent_pos < antecedent_pos AND prop.causal_form.direction == "forward":
        risk += 0.2

SIGNAL_3: 边界缺失 (Boundary Absence)
  检测: 命题缺少 boundary 或 failure_conditions
    FOR each proposition:
      IF prop.boundary is NULL or EMPTY:
        risk += 0.2
      IF prop.failure_conditions is NULL or EMPTY:
        risk += 0.2

SIGNAL_4: 排他性封闭 (Exclusivity Closure)
  检测: 筛选器排除了所有替代解释
    FOR each proposition:
      alternatives = get_alternative_propositions(prop)
      filtered = apply_filters(alternatives, prop.exclusivity_filters)
      IF len(filtered) == 0 AND len(alternatives) > 0:
        risk += 0.3

SIGNAL_5: 否定不可插入 (Negation Immunity)
  检测: 子词否定后命题仍完全自洽
    FOR each proposition:
      negations = generate_negations(prop.statement)
      contradictions = [n for n in negations if contradicts(n, prop)]
      IF len(contradictions) == 0:
        risk += 0.2

SIGNAL_6: 载体单一声称 (Single-Carrier Claim)
  检测: 声称仅在一种工具上有效但使用了跨工具词汇
    FOR each proposition:
      IF len(prop.boundary.applicable_carriers) == 1:
        cross_carrier_terms = detect_cross_carrier_vocabulary(prop.statement)
        IF len(cross_carrier_terms) > 0:
          risk += 0.1
```

### 处置决策矩阵

```
total_risk = sum(signal_risks)

IF total_risk < 0.3:
  → PASS: 记录风险分，命题正常输出
  → 标记: witchcraft_risk = total_risk

ELIF 0.3 <= total_risk < 0.6:
  → REMEDIATE: 强制补充边界与失败条件
  → 动作:
    1. 若 boundary 缺失 → 生成最小 boundary (仅适用于当前 carrier)
    2. 若 failure_conditions 缺失 → 生成默认条件: "当出现反例时降级为假设"
    3. 标记: witchcraft_risk = total_risk, remediated = true
  → 重新评估: 补充后重跑 SIGNAL_3，risk 可能降低

ELIF total_risk >= 0.6:
  → SILENCE: 不输出确定性结论
  → 动作:
    1. 命题标记为 silenced
    2. 替换 statement 为可检验问题
    3. 写入 SilenceReport
    4. 生成 InterrogationSeed
  → 标记: witchcraft_risk = total_risk, silenced = true
```

### 反巫术审计日志

每次巫术检测必须输出审计记录：

```json
{
  "proposition_id": "prop_xxx",
  "signals_triggered": ["SIGNAL_1", "SIGNAL_3"],
  "signal_details": {
    "SIGNAL_1": { "cycle": ["def_a", "def_b", "def_a"], "external_anchors": 0 },
    "SIGNAL_3": { "missing": ["failure_conditions"] }
  },
  "total_risk": 0.5,
  "disposition": "remediate",
  "remediation_actions": ["added default failure_condition"],
  "post_remediation_risk": 0.3
}
```

---

## 最小伪代码

### `ingest_field(discourse_flow) → fantasy_candidates[]`

```
FUNCTION ingest_field(discourse_flow):
  INPUT: discourse_flow: string
  OUTPUT: fantasy_candidates[]

  IF discourse_flow is EMPTY:
    RETURN [], SilenceEntry("information_insufficient")

  ngrams = extract_ngrams(discourse_flow, n=[2,3,4])
  repeated = filter(ngrams, frequency >= 2)
  known_defs = get_existing_definitions()
  candidates = [r for r in repeated if r.fragment NOT IN known_defs]

  FOR each candidate:
    candidate.force_index = candidate.frequency * length_weight(candidate.fragment)

  SORT candidates BY force_index DESC
  RETURN candidates

  FAILURE: discourse_flow < 50 chars → reduce n to [2], mark low_confidence
```

### `extract_repetition(candidates) → repetition_patterns[]`

```
FUNCTION extract_repetition(candidates):
  INPUT: fantasy_candidates[]
  OUTPUT: repetition_patterns[]

  patterns = []
  FOR each candidate:
    IF candidate appears as thematic_loop (same theme, different words):
      patterns.append({type: "thematic_loop", ...})
    ELIF candidate is exact n-gram repeat:
      patterns.append({type: "n_gram", ...})
    ELIF candidate shows narrative_recoil (story returns to same point):
      patterns.append({type: "narrative_recoil", ...})

  RETURN patterns

  FAILURE: no patterns → RETURN [{type: "n_gram", frequency: 1, pattern: "undifferentiated"}]
```

### `slice_symbols(candidates) → raw_symbols[]`

```
FUNCTION slice_symbols(candidates):
  INPUT: fantasy_candidates[]
  OUTPUT: raw_symbols[]

  symbols = []
  FOR each candidate:
    positions = find_all_positions(candidate.fragment, discourse_flow)
    negation_slots = find_negatable_subwords(candidate.fragment)
    causal_joints = find_causal_connectors(candidate.fragment)
    boundary_words = find_boundary_markers(candidate.fragment)

    symbols.append({
      fragment: candidate.fragment,
      positions: positions,
      negation_slots: negation_slots,
      causal_joints: causal_joints,
      boundary_words: boundary_words
    })

  IF len(symbols) > 100:
    symbols = symbols[:50]  // truncate, mark truncated

  RETURN symbols

  FAILURE: no sliceable content → RETURN minimal symbol set
```

### `freeze_definitions(raw_symbols) → frozen[], fluid[]`

```
FUNCTION freeze_definitions(raw_symbols, threshold=3):
  INPUT: raw_symbols[]
  OUTPUT: frozen_symbols[], frozen_definitions[], fluid_symbols[]

  frozen = []
  fluid = []

  FOR each symbol in raw_symbols:
    self_ref = count_self_references(symbol, discourse_flow)
    cross_ref = count_cross_references(symbol, discourse_flow)

    IF self_ref + cross_ref >= threshold:
      frozen.append(formalize_symbol(symbol))
    ELSE:
      fluid.append(symbol)

  IF len(frozen) == 0 AND threshold > 2:
    RETURN freeze_definitions(raw_symbols, threshold=2)  // retry with lower threshold

  RETURN frozen, extract_definitions(frozen), fluid

  FAILURE: still no freezing → mark no_freezing_occurred, return all as fluid
```

### `build_fantasy_knots(frozen_symbols, filters, power_chains) → knots[]`

```
FUNCTION build_fantasy_knots(frozen_symbols, exclusivity_filters, power_chains):
  INPUT: frozen_symbols[], exclusivity_filters[], power_chains[]
  OUTPUT: fantasy_knots[]

  knots = []
  repetition_groups = group_by_repetition_pattern(frozen_symbols)

  FOR each group in repetition_groups:
    exclusivity_strength = compute_exclusivity(group, exclusivity_filters)
    power_trigger = compute_power_trigger(group, power_chains)
    force_index = group.frequency * exclusivity_strength * power_trigger

    knots.append(FantasyKnot(
      repetition_pattern=group.pattern,
      force_index=force_index,
      exclusivity_filters=relevant_filters(group, exclusivity_filters)
    ))

  SORT knots BY force_index DESC
  RETURN knots

  FAILURE: no groups → RETURN empty list, mark no_fantasy_knots
```

### `generate_propositions_with_boundaries(symbol_graph, knots) → propositions[]`

```
FUNCTION generate_propositions_with_boundaries(symbol_graph, fantasy_knots):
  INPUT: symbol_graph, fantasy_knots[]
  OUTPUT: propositions[]

  propositions = []
  FOR each edge in symbol_graph.edges:
    prop = Proposition(
      statement = verbalize_edge(edge),
      causal_form = extract_causal_form(edge),
      boundary = infer_boundary(edge, symbol_graph),
      failure_conditions = generate_failure_conditions(edge),
      rewrite_hooks = identify_rewritable_fields(edge),
      witchcraft_risk = 0  // to be computed in Stage 8
    )

    IF prop.boundary is EMPTY:
      prop.witchcraft_risk += 0.4
      prop.metadata.ideology_risk = true

    IF prop.failure_conditions is EMPTY:
      prop.witchcraft_risk += 0.4
      prop.failure_conditions = [default_failure_condition()]

    propositions.append(prop)

  RETURN propositions

  FAILURE: no edges → generate propositions from isolated symbols as hypotheses
```

### `apply_negation_transform(propositions, intensity) → alternatives[]`

```
FUNCTION apply_negation_transform(propositions, interrogation_intensity):
  INPUT: propositions[], interrogation_intensity: int (0-10)
  OUTPUT: alternative_propositions[], causal_feedback_analysis

  IF interrogation_intensity == 0:
    RETURN [], null

  alternatives = []
  causal_feedback = []

  FOR each prop in propositions:
    subwords = tokenize(prop.statement)
    depth = ceil(len(subwords) * interrogation_intensity / 10)
    target_subwords = subwords[:depth]

    FOR each subword in target_subwords:
      negated = negate(subword)
      alt_statement = replace(prop.statement, subword, negated)
      alt_prop = reconstruct_proposition(alt_statement, prop)
      alternatives.append(alt_prop)

    // 因果反馈分析
    causal_feedback.append({
      proposition_id: prop.id,
      causal_shapes_expression: analyze_causal_feedback(prop.causal_form, prop.statement),
      expression_shapes_causal: analyze_expression_feedback(prop.statement, prop.causal_form)
    })

  IF all alternatives are self-consistent with original:
    MARK "structurally_closed" warning

  RETURN alternatives, causal_feedback

  FAILURE: alternatives > 50 → truncate to top 20 by relevance
```

### `detect_witchcraft(propositions, alternatives) → scores[], dispositions[]`

```
FUNCTION detect_witchcraft(propositions, alternative_propositions):
  INPUT: propositions[], alternative_propositions[]
  OUTPUT: witchcraft_scores[], dispositions[]

  scores = []
  dispositions = []

  FOR each prop in propositions:
    risk = 0.0
    signals = []

    // SIGNAL 1: Self-referential loop
    cycles = find_definition_cycles(prop, max_length=3)
    FOR each cycle:
      IF no_external_anchor(cycle):
        risk += 0.3
        signals.append("SIGNAL_1")

    // SIGNAL 2: Causal inversion
    IF causal_inverted(prop, discourse_flow):
      risk += 0.2
      signals.append("SIGNAL_2")

    // SIGNAL 3: Boundary absence
    IF prop.boundary is EMPTY: risk += 0.2
    IF prop.failure_conditions is EMPTY: risk += 0.2
    IF risk increased: signals.append("SIGNAL_3")

    // SIGNAL 4: Exclusivity closure
    alts = get_alternatives_for(prop.id, alternative_propositions)
    IF len(alts) > 0 AND all_filtered_out(alts, prop.filters):
      risk += 0.3
      signals.append("SIGNAL_4")

    // SIGNAL 5: Negation immunity
    IF no_contradictions(prop, alternative_propositions):
      risk += 0.2
      signals.append("SIGNAL_5")

    // SIGNAL 6: Single-carrier claim
    IF single_carrier_with_cross_vocab(prop):
      risk += 0.1
      signals.append("SIGNAL_6")

    prop.witchcraft_risk = min(risk, 1.0)
    scores.append({proposition_id: prop.id, risk: risk, signals: signals})

    // Disposition
    IF risk < 0.3:
      dispositions.append({id: prop.id, action: "pass"})
    ELIF risk < 0.6:
      remediate(prop)
      dispositions.append({id: prop.id, action: "remediate"})
    ELSE:
      silence(prop)
      dispositions.append({id: prop.id, action: "silence"})

  RETURN scores, dispositions

  FAILURE: detector recursion → abort, mark all as risk=0.5
```

### `rewrite_by_power_chain(propositions, reality_vars, chains) → rewritten[]`

```
FUNCTION rewrite_by_power_chain(propositions, reality_mapping_vars, power_chains):
  INPUT: propositions[], reality_mapping_vars (I4), power_chains[]
  OUTPUT: rewritten_propositions[], rewrite_log_entries[]

  IF reality_mapping_vars is NULL:
    RETURN propositions, []  // skip

  log = []

  // Map I4 to chain intensities
  FOR each chain in power_chains:
    update_intensity(chain, "意识形态", reality_mapping_vars.credibility)
    update_intensity(chain, "权力聚合", reality_mapping_vars.power_distance)
    update_intensity(chain, "原则化", reality_mapping_vars.commitment_cost)
    update_intensity(chain, "集体认同", reality_mapping_vars.compliance_pressure)

    IF reality_mapping_vars.information_asymmetry > 0.5:
      boost_obscure_tendency(chain)

  // Apply effects
  FOR each chain in power_chains:
    FOR each effect in chain.effect_on_rules:
      prop = find_proposition(effect.target_proposition_id, propositions)

      SWITCH effect.effect_type:
        "strengthen" → tighten(prop.causal_form)
        "exclude" → shrink(prop.boundary)
        "expand" → widen(prop.boundary)
        "contract" → narrow(prop.statement)
        "obscure" → prop.witchcraft_risk += effect.magnitude * 0.5

      log.append(RewriteLogEntry(
        proposition_id=prop.id,
        trigger_source="power_chain",
        field_changed=affected_field,
        old_value=old,
        new_value=new,
        reason=describe_chain_effect(chain, effect)
      ))

  RETURN propositions, log

  FAILURE: chain or vars malformed → skip, log warning
```

### `emit_outputs(all_stage_data) → {O1, O2, O3, O4, O5}`

```
FUNCTION emit_outputs(stage_data):
  INPUT: all accumulated stage data
  OUTPUT: {O1, O2, O3, O4, O5} in JSON + Markdown

  O1 = SymbolGraphSnapshot(
    symbols=stage_data.frozen_symbols,
    fantasy_knots=stage_data.fantasy_knots,
    power_chains=stage_data.power_chains,
    indexical_operations=stage_data.indexical_ops,
    graph_metadata=compute_metadata(stage_data)
  )

  O2 = RuleDeck(
    propositions=stage_data.rewritten_propositions,
    deck_metadata=compute_deck_stats(stage_data)
  )

  O3 = RewriteLog(entries=stage_data.all_rewrite_entries)

  O4 = SilenceReport(entries=stage_data.all_silence_entries)

  O5 = InterrogationSeeds(
    seeds=generate_seeds(
      stage_data.alternative_propositions,
      stage_data.silenced_propositions,
      stage_data.causal_feedback
    )
  )

  json_output = serialize_json({O1, O2, O3, O4, O5})
  markdown_output = render_markdown({O1, O2, O3, O4, O5})

  RETURN json_output, markdown_output

  FAILURE: partial data → output available blocks, add missing_fields report
```

---

## 可选增强

### 增强 1：时间化符号空间建模

将 time_form（过去/现在/未来）建模为三维感性空间坐标。

**坐标定义**：
- `past` 轴：对象化活动的沉淀，已凝固的符号权重
- `present` 轴：当前话语流中的活跃度权重
- `future` 轴：先验想象力对感受时间的规划权重

**迁移规则**：
```
迁移条件:
  past → present: 当已凝固符号被重新引入话语流
  present → future: 当符号被用于规划/预测语境
  future → past: 当先验想象力的规划被对象化为定义
  any → silence: 当 time_form 三值均 < 0.1（符号时间性消解）

迁移公式:
  new_weight[axis] = old_weight[axis] + delta * migration_rate
  normalize(new_weight) such that sum ≈ 1.0
```

### 增强 2：沉默策略分层

三种沉默类型，分别输出不同的可检验追问：

| 沉默类型 | 触发条件 | 追问形式 |
|----------|----------|----------|
| 边界外沉默 | 命题超出 boundary | "该命题在 [排除域] 中是否有独立验证？" |
| 巫术沉默 | witchcraft_risk ≥ threshold | "是否存在不依赖该定义的因果路径？" |
| 信息不足沉默 | 输入数据不足以判定 | "需要补充哪些载体上的观察数据？" |

### 增强 3：工具差异模拟器

同一话语流在不同工具上重跑引擎，比较结构差异：

```
FUNCTION simulate_tool_differences(discourse_flow, carrier_types[]):
  results = {}
  FOR each carrier in carrier_types:
    input = EngineInput(discourse_flow=discourse_flow, tool_description={carrier_type: carrier})
    results[carrier] = run_engine(input)

  bias_table = []
  FOR each pair (c1, c2) in combinations(carrier_types, 2):
    diff = compare_symbol_graphs(results[c1].O1, results[c2].O1)
    bias_table.append({
      carrier_pair: [c1, c2],
      symbol_diff_count: diff.added + diff.removed,
      proposition_diff_count: compare_rules(results[c1].O2, results[c2].O2),
      force_index_variance: variance([r.O1.fantasy_knots.force_index for r in results.values()])
    })

  OUTPUT: tool_structure_bias_table
```

### 增强 4：权力链扰动实验

对现实映射变量施加扰动（±10%/±30%），观察规则改写轨迹：

```
FUNCTION perturb_power_chain(propositions, reality_vars, perturbation_levels=[0.1, 0.3]):
  stability_report = []

  FOR each var_name in reality_vars:
    FOR each delta in perturbation_levels:
      perturbed_vars_up = copy(reality_vars); perturbed_vars_up[var_name] *= (1 + delta)
      perturbed_vars_down = copy(reality_vars); perturbed_vars_down[var_name] *= (1 - delta)

      result_up = rewrite_by_power_chain(propositions, perturbed_vars_up, power_chains)
      result_down = rewrite_by_power_chain(propositions, perturbed_vars_down, power_chains)

      stability_report.append({
        variable: var_name,
        perturbation: delta,
        props_changed_up: count_changes(propositions, result_up),
        props_changed_down: count_changes(propositions, result_down),
        most_sensitive_prop: find_most_changed(propositions, result_up, result_down)
      })

  OUTPUT: stability_report (哪些变量对哪些命题最敏感)
```

### 增强 5：反向因果审计

审计"因果形式如何推动表达"，输出依赖图：

```
FUNCTION audit_reverse_causality(propositions):
  dependency_graph = {}

  FOR each prop in propositions:
    // 分析：prop.causal_form 如何影响了 prop.statement 的词汇选择
    causal_to_expression = analyze_vocabulary_influence(
      prop.causal_form,
      prop.statement
    )

    // 分析：prop.statement 的表达方式如何反向塑造了 prop.causal_form
    expression_to_causal = analyze_structural_influence(
      prop.statement,
      prop.causal_form
    )

    dependency_graph[prop.id] = {
      causal_drives_expression: causal_to_expression,  // 哪些因果词决定了表达
      expression_drives_causal: expression_to_causal,  // 哪些表达词反向塑造因果
      bidirectional_strength: compute_bidirectional_score(causal_to_expression, expression_to_causal),
      risk_note: "双向强度 > 0.7 时，因果与表达可能互构——接近巫术结构"
    }

  OUTPUT: dependency_graph (可视化为有向图，节点=命题，边=因果-表达依赖)
```
