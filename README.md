# toy-character-design

原创潮玩角色与系列设计 Skill。保留“审美路线 → IP Core / Visual DNA → 系列语法 → 材质 → 群像 → 实际位置映射 → 单人图 → 双重 QC”的设计主线。

## v2.1：生图执行层

不同路线、每款图片和每次修复使用独立上下文；评审与生成也隔离。
干净上下文排除无关历史，但保留当前要求和真实批准参考。
四路必须生成真实候选，逐图检查后再比较六组两两差异；不能把四张路线卡当作四种视觉答案。

每个逻辑图片最多 **首次 1 次 + 纠正 2 次，共 3 次生图调用**。
局部修复、整体重生、重新发散、工具失败共用次数；不通过的结果不能作为下游参考。
每次修复后重查全部要求。身份已批准后，需要改 DNA 的问题交用户决定。
上游改图会递归失效下游，并使旧群像位置映射失效；版本更新不清空预算。
用户的可爱、对称五官或比例偏好优先于样式库启发式，不为反套路而违反要求。

## 内容与职责

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 当前入口、设计步骤、确认节点、执行硬边界 |
| `references/design-workflow-v2.md` | 完整保留升级前 v2 的设计说明与模板；执行规则以当前入口/协议为准 |
| `references/image-execution-protocol.md` | 隔离、真实参考、逐图/批次评审、自动纠错及宿主接口 |
| `references/style-presets.md` | 18 类设计机制，不按商业 IP 命名 |
| `references/design-rules.md` | 组合、反套路、系列化与参考距离建议；服从用户边界 |
| `references/market-readiness-scorecard.md` | 审美自检与快测，不代表市场成功 |
| `schemas/design-spec.yaml` | 内部设计状态，不是用户填表 |
| `schemas/image-execution-plan.schema.json` | 可校验的执行任务计划结构 |
| `schemas/example-execution-plan.json` | 四路任务脚手架，不是实测图片或批准结果 |
| `scripts/execution_guard.py` | 实际状态守卫、最小任务包、有限重试循环和 CLI |
| `tests/test_execution_guard.py` | 不联网、不生图的合成状态测试 |
| `reports/execution-protocol-verification.md` | 本次实施验证范围和未验证项目 |

## 开始使用

先加载 `SKILL.md`，每个生图阶段读取执行协议；仅按需读取设计知识，不把全库送入生图任务。
设计已获批准时直接进入对应阶段，不重问已经回答的问题。

执行层使用 Python 3.10+ 标准库：

```sh
python -m unittest discover -s tests -v
python scripts/execution_guard.py init execution-ledger.json schemas/example-execution-plan.json
python scripts/execution_guard.py next execution-ledger.json route:R1
```

示例计划可初始化和检查，**这些命令不会生成图片**。
真实运行由宿主提供 `Host.fresh_context / generate / review`，并可靠持久化同一账本。
`run_task` 会自动执行有限的生成—评审—纠正循环；CLI 可供主控逐步记录真实调用。
新阶段通过获授权的 `extend_plan` 添加，不能覆盖已有任务来刷新预算。

## 能力边界

仓库已提供协议、状态管理和可测试的自动纠错控制逻辑，不包含已接通某个平台的生图/子 Agent 适配器。
宿主不支持真实隔离或图片传入时停止，不把“忽略上下文”的文本当作隔离。
上下文凭据由宿主执行记录提供；脚本不能独立鉴别宿主是否诚实。
自动状态测试不代表已经生成高质量角色，也不代表通过真实隔离视觉验证。

设计来源沿用原仓库的改编基础 `zsyggg/designer-toy-skill`；继续保留群像到单人图的核心思想，并扩展原创设计和执行保障。
