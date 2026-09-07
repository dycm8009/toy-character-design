# Style Presets — 设计机制库

本文件不是“热门 IP 风格库”。所有 preset 都按**可复用设计机制**组织，禁止写成“像某某角色”。

使用规则：

- 一条审美路线默认选 **1 个 Primary preset**。
- 最多叠加 **1 个 Secondary preset**。
- 不要把 4–5 个 preset 同时堆进 Prompt。
- preset 只规定设计倾向，不规定具体器官、服装和标志物。
- 同一轮路线探索应优先选择机制差异较大的 preset。

---

## 1. soft-round-minimal

**核心**：柔和大体块 + 极低五官信息量。

- Silhouette：连续圆弧、少折点、肢体短但不必大头
- Body mass：bean / pear / compact
- Face：点状或窄小五官，大面积留白
- Palette：低到中饱和，大色块
- Material：哑光软胶、短绒、磨砂质感
- Strength：亲和、图标化、缩略图稳定
- Risk：非常容易滑向“普通可爱吉祥物”
- Counter-rule：必须加入一个非常具体的轮廓 signature 或人格反差

---

## 2. cute-edge

**核心**：柔软主体里加入少量尖锐、危险或倔强信号。

- Silhouette：圆体块中插入 1–2 个尖角/折线
- Face：可爱但不必微笑，可由嘴/牙/眉形成张力
- Personality：cute 高，weird / rebellious 至少一项中高
- Material：软硬对比适配度高
- Strength：第一眼亲近，第二眼出现反差
- Risk：直接借用成熟怪兽 IP 的耳、牙、角组合
- Counter-rule：所有尖锐器官必须重新发明形态、数量和位置关系

---

## 3. emotion-first

**核心**：角色不是“有一种表情”，而是“由某种情绪机制构成”。

- IP Core：emotion_core 权重最高
- Face：允许眼泪、眼睑、嘴角、脸部留白成为系统
- Series：每款是一种情绪原因、阶段或应对动作
- Material：透明件、液体感、柔软件适合把情绪可视化
- Strength：系列故事天然成立
- Risk：角色设计退化成“不同哭脸/笑脸”
- Counter-rule：情绪必须同时影响结构、姿态或材质，而不只改表情

---

## 4. lanky-fashion

**核心**：修长比例、姿态和服饰轮廓共同形成冷感或时装感。

- Silhouette：长腿、长臂、窄躯干、延伸型头发/帽体
- Head ratio：不追求超大头
- Face：可低信息量、冷眼睑、弱表情
- Pose：站姿也可以成立，但需要结构化重心
- Material：硬质搪胶、织物、金属小件可混合
- Strength：明显区别于大头萌系
- Risk：滑向普通动画少女/时装插画
- Counter-rule：必须有非写实 body mass 或强识别头部结构

---

## 5. sculptural-geometry

**核心**：角色像一件小型雕塑，几何关系优先于“人体正确”。

- Silhouette：球、楔、柱、扇、块体组合
- Body mass：wedge / column / top-heavy / irregular
- Face：可以嵌入表面而非独立五官
- Material：单色哑光、石感、金属感、半透明块体
- Strength：强轮廓、强设计师玩具感
- Risk：过于抽象导致没有角色性
- Counter-rule：保留一个稳定人格信号或行为特征

---

## 6. creature-organic

**核心**：先设计“生物结构”，再判断它像不像人。

- Silhouette：耳/鳍/叶/尾/角/壳与身体共同构成外轮廓
- Proportion：creature / irregular
- Face：不需要符合人类五官位置
- Series：可以围绕生长、蜕变、季节、栖息环境变化
- Material：毛、半透明、软胶、颗粒表面适配度高
- Strength：最容易摆脱 AI 人脸
- Risk：变成通用宠物小怪兽
- Counter-rule：至少一个器官必须与角色世界规则直接相关

---

## 7. mascot-symbolic

**核心**：让角色像一个可以被快速画出来的符号系统。

- Silhouette：2–3 个极简大形
- Face：图形化，减少高光、睫毛、写实结构
- Palette：1 主色 + 1 辅色 + 少量强调
- Series：通过符号变化而不是复杂服装变化
- Strength：品牌化、图标化、跨媒介稳定
- Risk：过度简化而没有收藏价值
- Counter-rule：需要一个有雕塑价值的体积关系或材质反差

---

## 8. absurd-expression

**核心**：极端表情本身就是系列语法。

- Face：嘴、眉、眼距、脸部挤压可产生大幅变化
- Expression intensity：3–5
- Body：相对稳定，让脸成为主舞台
- Series：每款一个极端反应或失控瞬间
- Strength：传播、表情包、短视频截帧能力强
- Risk：只剩搞怪，没有角色身份
- Counter-rule：不管表情多极端，silhouette 和 recognition token 不变

---

## 9. quiet-melancholy

**核心**：弱动作、弱表情、强情绪留白。

- Silhouette：收拢、低重心、包裹感
- Face：小幅眼睑、嘴角变化，大面积安静留白
- Pose：蜷缩、低头、靠坐、抱膝、停顿
- Palette：低饱和、灰阶邻近色、单一强调色
- Strength：成熟、安静、情绪投射空间大
- Risk：整体太弱，缩略图失去识别度
- Counter-rule：用轮廓或材质提供强信号，不靠高饱和色救场

---

## 10. retro-nostalgia

**核心**：从旧时代物件、印刷、玩具结构和色彩记忆中抽象规则。

- Silhouette：可借鉴旧玩具的机械感、圆角塑料感、布偶比例
- Face：印刷式、贴花式、旧动画式简化，但不复制具体角色
- Palette：褪色红、奶油、旧蓝绿、烟灰等
- Finish：做旧、磨砂、旧塑料、旧织物
- Strength：情绪记忆与收藏感
- Risk：堆“复古元素”变成主题装饰
- Counter-rule：只选一个年代机制，并让它进入身体结构

---

## 11. vinyl-plush-hybrid

**核心**：硬质视觉识别 + 柔软触感身体。

- Structure：硬脸/头部 + 毛绒身体，或反向组合
- Silhouette：连接处必须成为设计的一部分
- Face：硬质部分负责清晰身份 token
- Body：毛长、毛向、软塌程度参与轮廓
- Strength：可展示、可触摸、可挂包
- Risk：只把既有 PVC 角色“套一层毛”
- Counter-rule：重新设计硬/软边界，不允许只是材质替换

---

## 12. transparent-inner-scene

**核心**：透明外层不是装饰，而是揭示第二层信息。

- Structure：外壳 + 内部独立信息层
- Inner scene：星核、天气、房间、植物、记忆物等原创机制
- Face：尽量避免透明结构干扰身份识别
- Series：每款改变内部世界，外部 DNA 保持
- Strength：开箱 reveal 和隐藏款潜力强
- Risk：直接滑向成熟艺术家的“解剖/半剖”签名语言
- Counter-rule：禁止默认骨骼/器官解剖；内部信息必须来自本 IP 世界规则

---

## 13. crystal-optical

**核心**：光学效果本身构成系列统一语法。

- Material：透明、半透明、磨砂透明、珠光、折射、渐变
- Silhouette：外轮廓保持简洁，避免透明件过碎
- Palette：控制色数，强调光学层次而非彩虹堆砌
- Series：每款改变“光如何穿过角色”
- Strength：收藏陈列和隐藏款升级明显
- Risk：变成普通透明换色
- Counter-rule：至少一个结构层级随光学规则变化

---

## 14. tactile-craft

**核心**：缝线、编织、刺绣、手作不完美成为角色语言。

- Silhouette：软塌、偏斜、非绝对对称
- Face：刺绣、布贴、压纹、针脚均可成为五官语法
- Texture：毛圈、针织、短绒、粗布、手作缝线
- Personality：适合温暖、怪趣、民艺感
- Strength：明显区别于光滑 AI 3D 手办
- Risk：变成普通布偶
- Counter-rule：加入一个不可替代的结构或异常比例

---

## 15. interactive-hair-fashion

**核心**：头发/毛发既是轮廓，也是用户可以参与改变的区域。

- Silhouette：静态时有清晰基准发型
- Interaction：梳理、扎、夹、变换局部造型
- Series：颜色、长度、纹理、发饰可成为系列变量
- Strength：UGC 和穿搭能力强
- Risk：角色身份完全依赖发型
- Counter-rule：脸与身体至少保留两个独立 identity token

---

## 16. mini-diorama

**核心**：角色和一个小型环境结构不可分割。

- Silhouette：角色 + 环境形成整体外轮廓
- Scene：不是背景，而是实体的一部分
- Series：每款是同一世界规则下的一个小地点/事件
- Strength：故事密度高、陈列性强
- Risk：场景太复杂，角色本身无辨识度
- Counter-rule：拿掉场景后角色仍需通过至少一个 identity token 被识别

---

## 17. soft-squishy

**核心**：挤压、回弹、软体变形参与造型。

- Silhouette：鼓包、软塌、挤压痕迹可设计化
- Face：允许随着变形产生幽默变化
- Material：PU foam、soft elastomer 等概念方向；生产参数需供应商确认
- Strength：触觉、解压、互动
- Risk：变成普通食物拟物软捏
- Counter-rule：角色 DNA 不能只靠“像某种食物”

---

## 18. asymmetry-character

**核心**：轻度不对称本身形成“活过的痕迹”。

- Silhouette：一侧耳/发/肩/肢体存在稳定差异
- Face：单侧斑点、眉形、伤痕、腮红、眼睑等
- Personality：倔强、顽皮、手作、生命感
- Strength：快速摆脱模板化标准脸
- Risk：为了怪而随机加缺陷
- Counter-rule：不对称必须能用一句角色故事解释

---

# Face Grammar 快速库

这些不是固定脸型，只是用于发散路线：

| 机制 | 说明 |
|---|---|
| dot-eye | 极小眼，依靠留白和轮廓表达 |
| lid-heavy | 眼睑主导，眼球信息弱 |
| slit-eye | 细窄眼，适合冷感/倔强 |
| no-pupil | 取消瞳孔，强调异质感 |
| mouth-led | 嘴或牙是脸部主信号 |
| brow-led | 眉形承担主要人格信息 |
| mask-face | 面部像一整块面罩/面片 |
| negative-space | 五官极少，以面部留白形成气质 |
| off-center | 局部轻微偏位形成手作/怪趣感 |
| no-mouth | 无嘴，情绪通过眼睑、姿态和轮廓传达 |

组合时不要机械地“每项选一个”。真正需要锁定的是一条可复述的 `face_grammar`。

# 路线探索推荐分组

为了避免 4 条候选仍然相似，可优先从不同组各取一个：

- **符号型**：soft-round-minimal / mascot-symbolic
- **冲突型**：cute-edge / absurd-expression / asymmetry-character
- **情绪型**：emotion-first / quiet-melancholy
- **形体型**：lanky-fashion / sculptural-geometry / creature-organic
- **材质型**：vinyl-plush-hybrid / transparent-inner-scene / crystal-optical / tactile-craft / soft-squishy
- **体验型**：interactive-hair-fashion / mini-diorama

默认不从同一组连续抽 4 条路线。