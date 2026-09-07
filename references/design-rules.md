# Design Rules — 组合、反套路与系列化规则

本文件用于回答：**怎样把多个设计维度组合成一个成熟角色，而不是把模板字段逐项填满。**

---

## 1. 高权重与低权重维度

### 高权重：决定角色是谁

- silhouette_signature
- proportion_archetype
- body_mass_profile
- face_grammar
- recognition_tokens
- identity_material_cues

### 中权重：决定这个系列是什么

- emotion_core
- series_transformation_rule
- material_map
- palette_roles
- recurring_motifs

### 低权重：决定这一款此刻长什么样

- outfit
- hairstyle variant
- prop
- pose
- scene
- lighting

**规则：**候选之间只改低权重维度，不算真正的设计分叉。

---

## 2. 3+1 识别结构

一个新角色建议至少建立：

- 1 个强 silhouette signal
- 1 个比例 / 质量分布 signal
- 1 个 face / local token
- 1 个可选材质或表面 signal

不要求四项都夸张，但至少三项能稳定复述。

如果角色只能靠“发型 + 衣服 + 道具”识别，Visual DNA 不合格。

---

## 3. 大形先于小细节

设计顺序：

> 黑色大形 → 质量分布 → 头部外轮廓 → 五官语法 → 材质边界 → 色彩 → 小配件

禁止反过来从睫毛、纽扣、花纹、首饰开始堆细节。

### 快速删减法

当角色显得“很精致但很普通”时：

1. 去掉 70% 小装饰
2. 转成纯黑剪影
3. 找出最大 3 个形
4. 重新设计它们的比例关系
5. 再恢复必要细节

---

## 4. 比例不是头身比一个数字

至少同时考虑：

- head_height / total_height
- shoulder width / hip width
- torso length / leg length
- limb thickness
- center of mass
- horizontal vs vertical extension

### 常见母体

| 母体 | 特征 | 风险 |
|---|---|---|
| bean | 一体软圆体块 | 容易普通萌化 |
| pear | 下重上轻 | 容易亲和但缺攻击性 |
| top-heavy | 头肩上部重 | 易形成怪趣/力量感 |
| wedge | 楔形体块 | 适合雕塑感但可能僵硬 |
| column | 竖直拉长 | 适合冷感/时装感 |
| long-leg | 腿部主导 | 容易动画少女化 |
| irregular | 刻意失衡 | 需要明确设计理由 |

**规则：**如果采用常见母体，必须再用 silhouette 或 face grammar 增加第二识别层。

---

## 5. Face Grammar 规则

### 5.1 五官数量越多，不代表角色越完整

AI 角色常见失败：大眼 + 高光 + 睫毛 + 小鼻 + 樱桃嘴 + 腮红 + 精细眉毛全部存在，最后变成通用动画脸。

可优先删掉一部分信息，让脸形成明确语法。

### 5.2 只允许 1 个主视觉重心

一张脸优先选择：

- eyes-led
- mouth-led
- brow-led
- mask-led
- negative-space-led

其余器官降低存在感。

### 5.3 表情与身份分开

`face_grammar` 是身份；`expression` 是当前状态。

表情变化再大，也不应该改变：

- 基础眼距
- 五官主次关系
- 面部留白结构
- recognition token

---

## 6. 人格张力规则

角色不必复杂世界观，但最好存在一条张力：

> 看起来 X，但其实 Y。

可用的张力来源：

- 外表强硬 / 内心照顾别人
- 看似迟钝 / 对微小变化异常敏锐
- 总在哭 / 反而比别人更敢面对情绪
- 看似冷淡 / 对收藏的小东西非常执着
- 身体很巨大 / 行动极其谨慎
- 外形很柔软 / 性格非常固执

**禁止**把“反差”机械等同于“凶但善良”。

---

## 7. 颜色规则

颜色的任务是强化结构，不是补救弱设计。

### 推荐角色分工

- base：承担最大面积
- secondary：解释结构层级
- accent：引导视线
- neutral：控制呼吸空间

### 经验规则

- 强强调色一般不需要超过 1–2 个
- 隐藏款优先做结构 / 材质升级，再考虑换色
- 如果转灰度后角色完全失去层级，说明过度依赖颜色
- identity color 与 series color 要区分：前者长期保留，后者可按系列变化

---

## 8. 材质组合规则

### 8.1 每种材质必须有任务

材质至少承担一种：

- visual：视觉层级
- tactile：触感
- structural：结构功能
- interactive：互动功能
- narrative：叙事含义

没有任务的材质不要加。

### 8.2 软硬混合不是自动高级

当使用硬质脸 + 毛绒身体时，必须回答：

- 为什么脸需要硬？
- 为什么身体需要软？
- 硬软边界在哪里？
- 边界是否增强轮廓？
- 从侧面看是否仍然成立？

如果只是把普通 PVC 角色换成毛绒身，属于材质换皮。

### 8.3 透明件必须承载第二信息层

透明仅为了“好看”时价值有限。

优先让透明结构展示：

- 内部世界
- 状态变化
- 光线变化
- 可收集的内核
- 隐藏信息

---

## 9. 系列 Transformation Rule

### 9.1 一句话测试

必须能写成：

> “每一款都把 ______ 通过 ______ 变成不同状态，但始终保留 ______。”

例如：

> 每一款都把“今天没说出口的话”变成不同形态的邮包，但始终保留角色歪斜的邮差帽和软塌星形身体。

### 9.2 变体差异预算

默认启发式：

- 70% identity
- 20% theme
- 10% surprise

如果所有款几乎一样，提高 theme / surprise。

如果像不同 IP，降低 theme / surprise，恢复 identity。

### 9.3 系列内至少存在三种变化层级

一个 6–12 款系列不要只变化一个字段。可混合：

- structure
- expression
- material
- color
- prop
- pose
- surface
- interaction

但每款仍需受同一 transformation rule 控制。

---

## 10. Hidden / Secret 规则

隐藏款不应只是“普通款 + 金色”。

建议优先升级顺序：

1. silhouette / structure
2. material boundary
3. optical effect
4. interaction
5. removable part
6. special prop
7. palette

隐藏款仍必须保留 IDENTITY_LOCKED。

---

## 11. 配件规则

任何配件必须至少通过一项：

- Identity：永久身份物
- Narrative：解释当前剧情
- Interaction：用户能操作

如果只是填空，删掉。

### 配件数量克制

当角色已有强轮廓和强材质时，配件应减少。

当角色本体极简时，可让一个配件成为第二视觉层，但不能让配件替代角色身份。

---

## 12. 候选路线反同质化

一次输出 4 条路线时：

### 必须满足

- 至少 3 种 silhouette 家族
- 至少 3 种 body mass
- 至少 3 种 face grammar
- 至少 2 种 material strategy
- cute 不得在四条路线中全部为最高轴

### 不算差异

- 长发 vs 短发
- 红衣 vs 蓝衣
- 坐姿 vs 站姿
- 开心 vs 生气
- 冬装 vs 夏装

除非这些变化真正改变角色的高权重设计机制。

---

## 13. 防热门 IP 模仿规则

### 13.1 不建立品牌名 preset

禁止：

- `labubu-style`
- `skullpanda-style`
- `crybaby-style`
- `molly-style`
- 任何其他具体商业角色名作为生成模板

### 13.2 抽象设计机制

可以记录：

- “低五官信息 + 强轮廓”
- “情绪作为系列本体”
- “硬脸 + 柔软身体”
- “透明外壳揭示第二信息层”
- “极端表情成为系列函数”

### 13.3 Reference Distance Gate

如果一个新设计同时出现以下 2–3 项并明显指向同一个成熟 IP，回炉：

- 特殊耳/角轮廓高度相似
- 嘴/牙组合高度相似
- 眼距与五官布局高度相似
- 同位置固定标志高度相似
- 相同头身 + 相同材质边界 + 相同轮廓

**只换颜色不能解决相似问题。**

---

## 14. AI 脸排查

出现以下组合越多，风险越高：

- 对称椭圆脸
- 两只大高光眼
- 精细睫毛
- 小尖鼻
- 小微笑嘴
- 标准腮红
- 完整动画式头发层次
- “漂亮”但没有结构异常

修复优先级：

1. 重做 face grammar
2. 改变 head silhouette
3. 改 body mass
4. 减少五官信息
5. 增加有叙事依据的轻度非对称
6. 最后才改发型或服装

---

## 15. 缩略图与剪影规则

### Silhouette Test

纯黑后仍应看出至少两个身份结构。

### Thumbnail Test

约 80–120 px 时至少保留一个强识别信号。

### Grayscale Test

转灰度后主要层级仍成立。

### Outfit Removal Test

移除服装、场景、手持物后仍像同一个角色。

以上测试失败时，优先修高权重 DNA，不靠增加细节补救。

---

## 16. 什么时候应该停止加规则

当以下四件事已经成立时，不要继续模板化：

1. 剪影有身份
2. 五官有语法
3. 角色有一句人格张力
4. 系列有一句 transformation rule

之后应通过图像样本和人工审美判断继续迭代，而不是再增加十几个字段。