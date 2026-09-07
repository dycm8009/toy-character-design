# toy-character-design

一个用于原创潮玩角色与系列设计的 Skill。

它保留原有“群像 → 单人图 → 一致性检查”的稳定生成流程，但把设计起点前移到 **审美路线探索、IP Core、Visual DNA、系列变形语法与材质策略**，避免把潮玩设计简化成固定 chibi 模板、换装和姿势变化。

## 核心变化

### 1. 从“填模板”改为“先发散路线”

角色未定型时，默认先提出 4 条明显不同的审美路线。不同路线至少要在轮廓、比例、五官语法、材质、情绪姿态或系列机制中的 3 个高权重维度上产生差异。

只换颜色、服装、发型和动作，不算不同路线。

### 2. 不再默认 Chibi

`chibi`、大眼、圆脸、可爱微笑、vinyl figure 都只是可选表达，不再写进基础模板。

角色改由以下核心维度定义：

- `silhouette_signature`
- `recognition_tokens`
- `proportion_archetype`
- `body_mass_profile`
- `face_grammar`
- `personality_axes`
- `character_paradox`

### 3. 先定义系列语法，再设计具体款式

每个系列先写一句 `series_transformation_rule`，明确为什么这些款属于同一系列。

如果去掉服装和配色后无法解释系列关系，说明设计仍然只是“换装合集”。

### 4. 材质成为设计语言

使用 `material_map` 描述：

> 部件 → 材料 → 颜色 → 表面 → 透明度 → 触感

而不是只在 Prompt 里写 `matte vinyl`、`glossy` 等渲染词。

### 5. 双重质量检查

最终同时进行：

- 视觉一致性 QC
- 审美 / 市场就绪 QC

并加入剪影、缩略图、去服装、参考距离等测试。

## 工作流

```text
需求
  ↓
审美路线探索
  ↓
IP Core + Visual DNA
  ↓
系列变形语法
  ↓
材质 / 商品形态 / 互动
  ↓
群像
  ↓
实际位置映射
  ↓
单人图
  ↓
视觉一致性 QC
  ↓
审美与市场就绪 QC
```

## 目录

```text
toy-character-design/
├── SKILL.md
├── README.md
├── schemas/
│   └── design-spec.yaml
├── references/
│   ├── style-presets.md
│   ├── design-rules.md
│   └── market-readiness-scorecard.md
├── agents/
│   └── openai.yaml
└── assets/
```

## 参考文件如何使用

`SKILL.md` 只保留流程、硬规则和关键模板，避免提示词不断膨胀。

`references/style-presets.md` 是按“设计机制”组织的样式库，不按热门品牌或具体 IP 命名。

`references/design-rules.md` 记录组合、反套路、系列化、材质和参考距离规则。

`references/market-readiness-scorecard.md` 提供 9 维自检表与强制快测。

`schemas/design-spec.yaml` 是完整结构化字段，可由 Agent 自动推导；不是要求用户逐项填写的表单。

## 原则

- 学习热门潮玩的设计方法，不复制具体 IP 的独占识别组合。
- 一致性锁定的是身份 DNA，不是所有细节。
- 姿势和服装是表现层，不应承担角色主要辨识度。
- 概念阶段不知道真实工厂限制时标记为 TBD，不虚构精确生产参数。
- 内部评分阈值属于 Skill 的启发式自检，不是行业标准。