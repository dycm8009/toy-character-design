# Market Readiness Scorecard

这是 `toy-character-design` 的内部审美与商品就绪自检表。

**不是行业标准，也不是销量预测模型。** 它的作用是让 Agent 在“图很好看”之外，检查角色是否真的具有身份、系列能力和商品表达空间。

默认 9 维，每项 0–5 分，总分 45。

内部启发式通过线：

> **总分 ≥ 36/45，且任一维度不得低于 3。**

低于阈值时不要只修最终渲染，应回到对应设计层。

---

## 1. Recognition / 识别度

### 5 分

- 黑色剪影仍可识别主要身份
- 缩略图仍保留明显 token
- 不依赖服装和场景

### 3 分

- 正面大图能认出
- 去掉颜色或服装后辨识度明显下降

### 0–2 分

- 主要依赖发型、服装、道具
- 与大量同类角色无法区分

**失败回退：Visual DNA**

---

## 2. Personality & Emotion / 人格与情绪

### 5 分

- 一句话能说清角色长期情绪价值
- 存在自然的人格张力
- 外形与人格互相解释

### 3 分

- 有性格词，但视觉上体现较弱

### 0–2 分

- 只有“可爱、活泼、温柔、酷”等通用标签

**失败回退：IP Core**

---

## 3. Form & Face Originality / 形体与五官原创性

### 5 分

- 比例、质量分布和 face grammar 形成独立系统
- 不像通用动画脸
- 没有明显拼接成熟 IP 的独占特征组合

### 3 分

- 有一个新鲜点，但整体仍较常规

### 0–2 分

- 大头圆脸大眼模板
- 或明显接近单一热门角色

**失败回退：Aesthetic Route / Visual DNA**

---

## 4. Color & Material / 配色与材质

### 5 分

- 颜色强化结构
- 材质有明确视觉/触觉/叙事任务
- 软硬、透明、光泽等关系有设计理由

### 3 分

- 配色协调，但材质主要还是渲染表现

### 0–2 分

- 靠渐变、珠光、高饱和或“高级 3D”掩盖弱造型

**失败回退：Material Map / Palette**

---

## 5. Series Grammar / 系列语法

### 5 分

- 能用一句 transformation rule 解释全系列
- 各款差异明显但仍属于同一 IP
- 隐藏款是结构/材质/机制升级

### 3 分

- 主题统一，但主要仍靠换装和配色

### 0–2 分

- 多款像不同 IP
- 或所有款几乎一样

**失败回退：Series Transformation Rule**

---

## 6. Narrative Necessity / 叙事必要性

### 5 分

- 每款都有存在理由
- pose / prop / expression 都来自 narrative beat
- 不需要长篇故事也能理解状态

### 3 分

- 有主题名字，但部分款式仍像凑数

### 0–2 分

- 款式名只是“红色款、冬日款、魔法款”等装饰标签

**失败回退：Variant Card**

---

## 7. Play / Usage Potential / 可玩与使用潜力

### 5 分

- 至少存在一个自然的展示、触摸、挂戴、拆换、造型或互动价值
- 互动与角色机制一致

### 3 分

- 主要是静态摆件，但陈列价值清晰

### 0–2 分

- 角色结构与商品形态不匹配
- 加入互动只是为了追趋势

**失败回退：Product Form / Interaction Mode**

---

## 8. Product Plausibility / 商品实现合理性

### 5 分

- 材质边界、重心、分件逻辑、挂点等有基本考虑
- 未知工厂参数明确标 TBD
- 概念复杂度与目标产品形态基本匹配

### 3 分

- 概念合理，但生产信息尚未补齐

### 0–2 分

- 依赖无法解释的悬空、超薄结构、碎小透明件等效果
- 把 AI 渲染能力误当成量产能力

**失败回退：Product / Production Optional**

---

## 9. Shareability & Reference Distance / 传播与参考距离

### 5 分

- Hero shot 有清楚第一眼钩子
- 角色有可截图、可展示、可挂戴或可互动的传播点
- 与成熟 IP 保持明显距离

### 3 分

- 视觉完整，但第一眼记忆点一般

### 0–2 分

- “像某某角色”成为主要评价
- 或只有精致，没有可复述特征

**失败回退：Visual DNA / Product Hook**

---

# 强制快测

评分前必须执行以下测试。

## A. Silhouette Test

把角色转为纯黑。

**Pass：**至少两个身份结构仍成立。

**Fail：**服装、颜色或五官消失后变成普通人形/普通小动物。

---

## B. Thumbnail Test

缩小到约 80–120 px。

**Pass：**仍能看到至少一个强身份信号。

**Fail：**必须放大才能通过睫毛、花纹、配件辨认。

---

## C. Outfit Removal Test

概念上去掉：

- 服装
- 手持道具
- 场景
- 临时发饰

**Pass：**基础角色仍然成立。

**Fail：**变成无特征人体/动物模板。

---

## D. Grayscale Test

转灰度检查大形和层级。

**Pass：**主要结构仍清楚。

**Fail：**角色完全靠色彩差异分层。

---

## E. Reference Distance Test

检查是否同时命中同一成熟 IP 的多个高权重识别特征。

高风险组合包括：

- 近似头部外轮廓 + 近似嘴/牙系统
- 近似耳/角 + 近似眼距/五官布局
- 近似头身比例 + 近似材质边界 + 近似标志物

**Pass：**仅共享抽象设计原则，具体形态独立。

**Fail：**用户第一反应只能用某个商业 IP 名称描述它。

只换色不算解决。

---

## F. Route Diversity Test（阶段 1 使用）

如果一次探索 4 条路线：

- 至少 3 类 silhouette
- 至少 3 类 body mass
- 至少 3 类 face grammar
- 至少 2 种 material strategy
- 不允许 4 条都以 cute 为最高人格轴

失败则重新发散，不进入角色锁定。

---

# REPORT 建议格式

```markdown
## Aesthetic & Market Readiness

| Dimension | Score | Evidence | Action |
|---|---:|---|---|
| Recognition | 4/5 | ... | ... |
| Personality & Emotion | 4/5 | ... | ... |
| Form & Face Originality | 3/5 | ... | ... |
| Color & Material | 4/5 | ... | ... |
| Series Grammar | 5/5 | ... | ... |
| Narrative Necessity | 4/5 | ... | ... |
| Play / Usage | 3/5 | ... | ... |
| Product Plausibility | 4/5 | ... | ... |
| Shareability & Distance | 4/5 | ... | ... |

Total: 35/45 — FAIL
Return to: Visual DNA + Product Form
```

不要为了过线虚增分数；分数的价值在于指出下一步应该回到哪一层。