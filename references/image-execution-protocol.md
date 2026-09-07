# 生图执行协议 v1.0

适用范围：路线图、角色定型/多视角、群像、单人图、衍生场景、修复及验证图。
这是执行契约，不是给图像模型阅读的长 Prompt。主控按阶段编译最小任务包。

## 1. 角色职责与真实隔离

| 角色 | 可读内容 | 不可做的事 |
|---|---|---|
| Orchestrator / 主控 | 用户历史、已批准设计、运行账本、全部产物 | 伪造生成/评审凭据、自动修改已批准 DNA |
| Visual Executor / 生图 | 本次要求、本路线/款式、必要参考图、最新一条纠正 | 继承主会话、读取其他路线或全部失败历史 |
| Visual Reviewer / 独立评审 | 实际输出、批准参考、验收条件 | 读取生成者自评后代替看图、把未知记通过 |
| Batch Reviewer / 批次评审 | 四路真实图、用户边界、高权重差异维度 | 根据路线文案推断图片已经不同 |

每次生成和每次评审均新建隔离执行上下文。它们可以用相同模型，但不可共享会话历史。
引用同一张批准基准不是上下文污染；污染指无关探索/失败讨论和其他候选造成的非授权影响。
局部修复允许携带问题图，必须同时携带正确基准、需要修的偏差和保留项。
整体漂移重生不传失败图作为身份模板。

宿主必须真实记录 `id`、`runtime_receipt`、`isolated: true`、`inherits_parent_conversation: false` 和实际图片绑定顺序。
这些字段来自调度/附件执行记录，不得由模型凭空填写。脚本只能检验字段契约，不能独立证明宿主说的隔离真实存在。
不支持隔离、视觉查看或真实参考传入时停止，标 `blocked_capability`，不退化为主会话假隔离。
用户另行允许的非隔离探索必须独立标为未验证，不经本协议发布为合格基准。

## 2. 最小任务包和参考资产

生成任务包仅含：当前短提示、不可违反的逐条要求、必要图像、映射等必要支持文件，以及最新一条明确修正。
不要输入 18 类样式库、研究报告、其他路线、完整评审史或整份 design-spec。
来源角色/品牌名不作为原创生成的风格捷径；不把参考距离检查变成仿制组件组合。

每项参考记录 `id / role / path / sha256`；内部上游还记录 `source_task / source_revision`。
身份基准另有 `approved: true / approval_ref`；用户原始参考与已批准身份基准不是同一种角色。
`role` 为 identity、group、position_map、user_reference 或 validation。
图像参考顺序必须与真正传入工具的附件顺序一致。具体参数名以当前宿主工具契约为准，不臆造引用 ID。

| 阶段 | 必要输入 | 排除输入 |
|---|---|---|
| route | 用户要求、本路线短方向；需要时用户原始图 | 其他候选、其他路线 Prompt 和自评 |
| anchor | 选中图/批准基准、DNA、视角要求 | 已淘汰方案 |
| group | 批准身份图、系列/各款/材质要求 | 未批准修图、全部探索对话 |
| individual | 批准身份图、有效群像、真实映射、该款要求 | 上一款生成记录、旧群像映射 |
| validation | 本项验证必需的固定条件和实际参考 | 生成者解释与期望答案 |

输出必须导出真实文件再记录哈希，禁止使用占位图或仅有文件名的“结果”。
运行脚本检查文件范围、存在性、哈希和 PNG/JPEG/WebP 文件头；这不等于完成图像解码、审美判断或视觉真实性鉴定。
宿主评审仍需实际查看图像。其他格式先由宿主转换为支持格式并保存转换来源，不伪造哈希。

## 3. 阶段门槛与评审证据

每次生图后先单图 QC，再允许接入后续依赖。所有必检项要有 `pass / fail / unknown` 和可定位的 observation。
检查范围按任务编译，至少覆盖用户硬要求、身份/比例/五官、必要款式、肢体、材质、遮挡和所需文字。
人物无手/五官等情况按已批准设计调整适用检查，不能把合理抽象当畸形；也不能用抽象掩盖意外变形。
修复必须复核整组必检项。unknown 不通过，评分不能抵消硬要求失败。

路线探索单图通过后，批次评审读取全部真实候选，记录每对差异所在维度及图上观察。
四条路线有六组两两比较。默认每对至少三个高权重差异；颜色、衣服和动作不是独立高权重维度。
差异不足时指明需要重做的未批准路线，覆盖每个失败配对；仅重做这些路线，其余结果保留。
重做沿用原 task ID/subject 和预算。批次结果绑定图片哈希及输出版本，任何候选改图后必须重新比较。
用户的可爱、大头、对称五官等限制不可被多样性要求覆盖。目标不可达时交用户处理，不降低用户边界后假报通过。

`approve` 只记录实际用户选择，不能通过批准事件绕过 QC 失败。路线选择还要求当前版本的批次评审通过。
阶段 1 未通过时不自动开始定型、多视角或系列资产生成。

## 4. 有限自动纠错

```text
能力/参考/依赖检查 → 原任务账本预留尝试 → 新上下文生图
→ 导出真实结果 → 新上下文逐条评审
→ 通过：约定人工门槛 / 发布
→ 失败：分类 → 最小纠正 / 回批准基准重生 / 未锁定路线重做
→ 新上下文重新生成并完整复查 → 通过或达到上限停止
```

默认每个逻辑图片最多三次调用：initial 1 + correction 2。四条路线最多十二次，不另开不计数的“发散轮”。
工具错误、明确无输出和安全拦截也记录已发起尝试；安全拦截立即停止，不绕过。
缺能力、缺文件等调用前检查失败不扣生图次数。拒绝增加上下文或伪造结果来凑满流程。
评审格式或工具错误不能触发新的图像调用；修正评审执行，或报告待评审状态。

| issue / error | next action | 授权边界 |
|---|---|---|
| execution | patch | 保留正确区域，输入基准+失败图 |
| identity_drift | rerender | 回批准基准，排除错误图身份影响 |
| design，身份未锁定 | redesign | 同路线内自动重做，不改用户边界 |
| design，身份已锁定 | awaiting_design_approval | 等用户批准改动，不重定义 DNA 迁就结果 |
| spec_conflict | blocked_spec | 先解释冲突 |
| tool_error / interrupted | rerender 或 exhausted | 先核实调用状态；已预留次数不退还 |
| safety | blocked_safety | 立即停止 |

只附最新的具体偏差，不堆“更独特、更高级”等空泛否定词。
局部修复、重生、回退、改文件名、改执行器和刷新参考共同使用同一预算。
预算耗尽后留下真实结果和差异报告；新的超预算请求必须由用户批准新范围并链接原失败记录。

## 5. 版本依赖与失效传播

引用链为：批准身份基准 → 群像 → 实际位置映射/单人图 → 后续素材/报告。
每张图片使用不可覆盖的文件路径。参考哈希改变时不自动接受新内容。
批准结果的新版本发布或旧版本被撤回后，主控立即发 `invalidate`，递归把全部依赖标为 stale。
群像位置映射同时通过 `group_sha256` 绑定实际群像；旧映射不可用于新图。
失效不是删除：旧图、旧评审、旧引用和全部次数保留。
重新批准的参考通过 `refresh` 绑定；必须同一 task ID/subject，次数不清零。
影响范围不明确时阻断全部依赖；不要推断未检查的旧图仍然有效。

## 6. 可运行守卫和宿主边界

`execution_guard.py` 仅用 Python 3.10+ 标准库；状态/契约检查、最小任务包、依赖阻断、计数、批次门槛和重试决策是实际代码。
`run_task(state, task_id, root, host, persist)` 自动循环生成→评审→纠正，直到通过、人工门槛、能力失败或三次上限。
`Host` 是宿主实现的接口，仓库不包含某个商业生图服务或子 Agent 系统的已接通适配器。
测试中的 FakeHost 只测试状态，不代表已经执行真实生图、隔离盲审或质量验证。

宿主接口：

```python
fresh_context(role, image_hashes) -> receipt
# role: generate 或 review。为真正的隔离执行/附件绑定建立记录。
generate(packet, receipt) -> {"output": {"path": "...", "sha256": "..."}}
# 无结果时返回 {"error": "tool_error"} 或 {"error": "safety"}。
review(packet, receipt) -> {"checks": {"requirement_id": {"status": "pass", "observation": "..."}},
                            "issue": "execution", "repair_note": "..."}
# 全项通过时 issue / repair_note 可省略；失败时必须分类和指出修正。
```

上下文建立阶段只绑定附件、创建执行容器，不提前调用图像生成。`reserve` 持久化成功后才调用 generate。
宿主必须保证每次 generate 只触发一次真实生图，关闭隐藏的多图/自动重试；返回多张不能算成一次“图片尝试”。
本版 run_task 顺序执行一个任务；四路各自隔离，可由具备可靠共享账本锁的宿主并行。
默认按序运行也能保持隔离。没有正确的并发持久化时不要同时写同一账本。
`persist` 必须在成功返回前完成可靠写入，并确保整个 run_task 调用互斥；不能使用测试中的空 callback 当生产实现。

CLI 供能运行 Python 的 Agent 每步记录，不能替代真实工具调用：

```sh
python scripts/execution_guard.py init execution-ledger.json execution-plan.json
python scripts/execution_guard.py event execution-ledger.json reserve-event.json --root ./run
# 实际生图工具在 reserve 成功之后调用；导出图片再提交 output-event。
python scripts/execution_guard.py event execution-ledger.json output-event.json --root ./run
python scripts/execution_guard.py event execution-ledger.json review-event.json --root ./run
python scripts/execution_guard.py next execution-ledger.json route:R1
python -m unittest discover -s tests -v
```

计划结构见 `schemas/image-execution-plan.schema.json`；四路脚手架见 `schemas/example-execution-plan.json`。
事件类型：reserve、output、review、error、approve、invalidate、refresh、route_batch_review、extend_plan。
`extend_plan` 在新阶段获授权后追加新逻辑任务，不覆盖原状态；禁止为已有 stage/subject 换名重新计数。
四路批次事件提交 `context`（按 task ID 排序绑定候选图）、`pairs`（a/b/different_dimensions/observation）；失败另含 rework_ids、repair_note。
`refresh` 提交完整新 task 和 user_approval_ref；依赖图不改变，只更新版本/参考及获授权的要求。

CLI 使用相邻 `.lock` 目录阻止并发写，原子替换账本。若进程崩溃留锁，先确认原进程已退出并核对已预留调用，才可人工移除遗留锁。
处于 running 的任务不能自动再次调图；找回原结果后记录 output，或确认失败后记录 error/interrupted。
创建新 ledger 文件不具有“清空预算”的授权；同项目运行由主控维护唯一账本及来源链。

## 7. 验证与报告

交付分别列：协议/脚本变更、状态测试、实际宿主隔离证据、真实图片检查、用户确认。
本仓库的单元测试验证契约和执行边界，不评价美感、不证明子 Agent 真实隔离、不预测市场表现。
真实验收至少覆盖：四路差异化、左右眼/身份要求、群像漏款纠正、单图身份漂移纠正、三次仍失败停止、上游换版阻断下游。
没有实际执行的项目保留 pending/未验证，不能用模拟图、测试桩、文件头检查或自评分冒充。
