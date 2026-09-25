# 2026-09-25｜今天最贵的失败，全都不报错

> 物理世界是唯一骗不了的裁判，但它要价最高；工具、环境、配置三层的失败全都静悄悄。

**标签**：`#评测` `#Agent` `#静默失败` `#工程陷阱`
**生成时间**：2026-09-25 12:11（北京时间）

---

## 一、今日观察

把今天这几件事按「失败会不会报错」排开，形状立刻出来了：

| 层 | 事件 | 失败会报错吗 | 谁来判分 | 关键数字 |
| :--- | :--- | :--- | :--- | :--- |
| **物理层** | DrivingBench 让 4 个前沿模型开真车 | **会**——撞了、没到终点，榜上一目了然 | 世界 | 只有 **1/4** 跑完；成功那次 **246.6M tokens / $7.74** |
| **环境层** | CAVEAT 利益错位市场 | 不会 | 环境的利益 | 最优购买率 **78.6% → 17.3%** |
| **工具层** | ToolUniverse 静默失败审计 | 不会 | 没人判 | **91** 例，API 层占 **51** |
| **配置层** | Claude Code 2.1.282 | 不会（刚被堵上） | 被改的人 | 克隆一个仓库就能开你的遥测 |
| **评分层** | MentalHealthBench | 会报错，但**阅卷人是出题方自己** | GPT-5.6 Sol | **80+** 专家、**5,262** 条标准 |

主线是：**失败的可见性和严重性成反比。**

越是需要被信任的环节，越是没有报错机制的环节。工具返回 `success` 却掉了字段，环境给你全对的信息却把排序换了，仓库配置悄悄把遥测打开——这三件事都不会抛异常，所以你的监控栈根本看不到。而唯一会大声报错的裁判（真实世界的车）入场券最贵：**$7.74 跑 134.7 米**，折合约 **$92/英里**，是同距离油钱的约 **500 倍** 🟡。

第二层观察：**判据的可协商程度，决定了这条评测值多少钱。** MentalHealthBench 是今天最精致的评测——80 多位持证临床专家、三审制、每条标准带 -10~+10 的临床权重；DrivingBench 是最粗糙的——一条中心线、4 米容差、到没到终点。但前者的阅卷人是 OpenAI 自己的 GPT-5.6 Sol，后者是物理世界。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. DrivingBench：唯一跑完全程的模型，花了别的模型 41 倍的钱 🟢

三位研究者（Aditya Ramabadran、Simon Mahns、Tobias Gessler）给 4 个前沿模型一辆 2022 款丰田 Corolla 的方向盘、油门和刹车，在停车场里跑 134.7 米锥桶赛道。车辆装 comma.ai 的 comma four 跑 openpilot，经 OBD-C 接 CAN 总线；模型只通过三个 MCP 工具操作：`observe()` / `set_motion()` / `stop_now()`。同一段连续对话内最多 3 次尝试，全部 medium 推理强度。

官方榜单（drivingbench.com）逐次数据：

| 模型（harness） | #1 | #2 | #3 | 最好成绩 |
| :--- | :--- | :--- | :--- | :--- |
| **GPT-6 Astra**（Codex·medium） | 49% · 67.3m · 81.2M/$2.01 | **100% · 134.7m · 5:22 · 246.6M/$7.74** | — | **100%** |
| Claude Fable 5.1（Claude Code·medium） | 9% · 17.5m · 3.58M/$0.96 | 10% · 27.3m · 4.87M/$1.35 | 45% · 73.7m · 82.1M/$1.64 | 45% |
| Grok 4.6（Cursor·medium） | 8% · 14.4m · 2.22M/$0.18 | 11% · 22.6m · 3.29M/$0.19 | 10% · 22.2m · 3.52M/$0.29 | 11% |
| GPT-5.6 Sol（Codex·medium） | 6% · 15.0m · 3.36M/$0.35 | 6% · 15.6m · 4.73M/$0.43 | 6% · 17.1m · 2.52M/$0.27 | 6% |

*（progress 定义：沿赛道中心线、保持在 4 米内的推进比例；碰撞只保留撞之前的进度。上表 token/成本为官方榜单原值。）*

按官方榜单自行计算：**Astra 成功那次 $7.74，是 Grok 4.6 最好那次 $0.19 的约 41 倍**；Grok 三次尝试合计只花 $0.66，总共走了不到 23 米。失败很便宜，成功很贵。

其余细节（🟡，来自媒体转述，官方站未逐条展示）：每轮推理 5–13 秒，车只能以约 0.94 mph 挪动；速度上限 0.5–3.5 m/s，超 6 m/s 直接解除控制；人类操作员始终坐驾驶位脚踩刹车。最值得记的一条：**模型（尤其 Astra）一度以安全为由拒绝开真车，研究者把 MCP server 改名为 "DrivingBench Sandbox" 就通过了**——安全边界被一个名字击穿。

来源：[drivingbench.com 官方榜单](https://drivingbench.com) · [officechai](https://officechai.com/ai/driving-bench-gpt-6-astra-becomes-first-model-to-drive-a-real-car-through-a-course) · [Web Pulse（含完整榜单表）](https://wpnews.pro/news/gpt-6-astra-has-gained-the-ability-to-drive-a-car) · [AI and Tech News（成本与安全拒答）](https://www.aiandtech.news/article/openai-model-drives-toyota-corolla-around-parking-lot-test-course)

### 2. MentalHealthBench：专家出题，出题方阅卷 🟢（分数为 🟡）

OpenAI 发布开放心理健康基准（官方页标注 2026-09-23），与 **80 多名**持证心理学家/精神科医生共同构建，覆盖 **22 国、19 种语言、近 20 个亚专业**。三档严重程度：Non-acute / High-acuity / Emergencies；四类用户：成人、13–17 岁青少年、照护者、临床医生。

机制上它做得很扎实（🟢 官方页原文）：每条标准权重 **-10 到 +10**，权重绝对值代表临床重要性；每条对话至少 **3 位**专家审阅，**至少 2 人同意且第 3 人不反对**才保留；总分可分解到 **10 个**专家定义的行为维度（官方举例：safety、seeking context、preserving user agency、providing actionable guidance）。

关键结构：**自动评分器是 GPT-5.6 Sol**——标准由外部专家写，判定由 OpenAI 自己的模型做。

另一项并行研究很值得抄：OpenAI 找了 **44 位**用过 AI 做情绪支持的成年人（16 国、14 语言）独立评分并自己写标准。结论是**用户更看重 practical next steps and tone，专家更看重 gathering relevant context 与解读模糊情境**——而官方明确写了：*The benchmark's final scoring criteria are based on expert consensus; this separate analysis did not change them.*

官方自陈局限原话：*"No benchmark captures everything that matters in a personal conversation."*

🟡 需注意两处：一是**官方页正文没有给出任何模型分数**（分数只在图表里），流传的 Astra 57.3% / Sol 53.9% / Opus 5.5 52.4% / Luna 50.2% / GPT-4o(2025-03) 32.1% / Gemini 2.5 Pro 29.5%，以及 1,215 条对话、5,262 条标准、non-acute 53.5% / high-acuity 18.2% / emergency 28.3% 等数字，均来自 Unite.AI 对论文与图表的转述，**未在官方页正文核实**；二是至少一家媒体（AI Insiders）直接点破"self-graded exam"的结构问题。

来源：[OpenAI 官方页](https://openai.com/index/introducing-mentalhealthbench/) · [Unite.AI（分数与构成占比）](https://www.unite.ai/openai-debuts-mentalhealthbench-for-ai-mental-health-conversations/) · [Pivot News](https://pivotnews.ai/healthcare/openai-releases-open-mental-health-benchmark-built-with-80) · [AI Insiders（阅卷人结构批评）](https://aiinsiders.net/article/openai-built-a-mental-health-benchmark-then-graded-it-with)

### 3. ToolUniverse 审计：91 个静默失败，76 个发生在 agent 拿到结果之前 🟢

arXiv 2609.26836（2026-09-21 提交）审计了 ToolUniverse 里的 **15 个**科学工具（104 个 wrapper、198 个测试用例），人工验证出 **91 例静默失败**——调用报成功，但返回的字段/数据不完整，且**没有任何通知给 agent 或用户**。

按 7 个 failure locus 分层：**API 层 51 例、wrapper 层 25 例**，另有 3 例无法确定位置；Agent Usability Gap（L6）为 **0 例**。

> 换算一下：**76/91 的失败发生在 agent 拿到结果之前。** agent 侧再好的错误处理也接不到。

**7/15 的工具在超过半数测试用例中失败**：ExpressionAtlas 75%、BV-BRC 67%、AMPSphere 67%、CTIS 53%、ChIP-Atlas 53%、KEGG 53%、Reactome 53%。

三个具体案例（原文级细节，二手报道全都没有）：
- **BiGG Models**：模型 `iRC1080` 的 `organism` 字段在 API 的模型详情接口返回 **null**，而同一个字段在网页搜索结果里是有的。
- **CryoET Data Portal**：GraphQL API 支持返回 child datasets，但 wrapper 的返回 schema **完全省略了这个字段**，agent 因此永远发现不了项目下的层级关系。
- **ChIP-Atlas**：MACS2 分数按文档是 **-10log10(Q-value)** 变换，agent 当成原始置信度读，从同一份数据得出了**相反**的结论。

作者提出 **contextual reliability** 作为替代品：*"the extent to which an Agent–Tool interaction preserves and communicates the information, qualifiers, provenance, scope, and meaning required to support the intended scientific conclusion, across the interaction chain."*

局限原话：*"Establishing that a failure is silent is inherently harder than detecting an explicit error."* 并明确说比例不代表 agent-tool 交互中的典型分布。

来源：[arXiv:2609.26836](https://arxiv.org/abs/2609.26836) · [全文 HTML](https://arxiv.org/html/2609.26836v1)

### 4. CAVEAT：信息一个字都没错，决策还是崩了 61 个百分点 🟢

arXiv 2609.27273（2026-09-23 提交）测的是"当环境自己有利益时，Agent 还守不守用户目标"。CAVEAT 建了 **9 个**浏览器市场环境、**52 个** Standard 任务，把现实市场的引导手段归成 **8 类**：Sponsored placement、Preferential ranking、Drip pricing、Promotional framing、Defaults & bundling、Scarcity & social proof、Trust signals、Friction & obstruction。

**关键设计：所有机制呈现的都是准确信息。** 两版市场里用户请求、商品、属性、价格、可用性和"用户最优选项"完全相同，唯一变量是呈现方式。结果：

- 匹配对照 **78.6%** → 激励错位 **17.3%**，降 **61.3 个百分点**；五个模型家族降幅 **37.2–78.9 个百分点**
- 最强配置（GPT-5.6-Sol，low reasoning）：**91.0% → 53.8%**
- CAVEAT-Hard（2,112 个商品、88 页结果）：GPT-5.6-Sol high reasoning **90.0% → 0.0%**

三个失效入口的消融数据（本文最值钱的部分）：
1. **Objective Drift**：构造 25 对"两个同等优先级、只颠倒陈述顺序"的请求，商品与最优解都不变 → **25 对全部改选**，系统性偏向先被提到的那个偏好。
2. **Premature Search Closure**：把某个次优商品从原位挪到靠近顶部的 sponsored 位 → 访问率 **45/60 → 60/60**，购买率 **0/60 → 48/60**。Hard 上 50 次失败**全部停在第 1 页**（共 88 页）。
3. **Premature Commitment with Unresolved Evidence**：找到过最优商品却排除掉的 **23 例**中，最常见是混淆 list price 与 payable price；13 例在正确处理的重复中成功。

**CAVEAT-Harness 的消融是最反直觉的一条**：完整 harness 把 Shop 上的最优购买率从 11.7% 提到 66.7%（摘要里的 +55.0 个百分点），但拆开看——**只加"结构化任务说明"只有 6.7%，只加"下单前验证工具"就有 66.7%**。光靠 prompt 描述同样原则只有 30.0%。Hard 上 0.0% → 80.0%。代价是 **2.6× runtime、2.3× steps、2.3× tool calls**。

来源：[arXiv:2609.27273](https://arxiv.org/abs/2609.27273) · [全文 HTML](https://arxiv.org/html/2609.27273v1)

### 5. Claude Code 2.1.282：仓库不能再替你打开遥测 🟡

Claude Code 2.1.282 的核心改动是：项目级/本地 settings 里的遥测变量（如 `CLAUDE_CODE_ENABLE_TELEMETRY`、`OTEL_LOG_*`）**被忽略**，只有 user 或 managed settings 生效；并在启动时、`/status`、`claude doctor` 里列出被忽略的遥测变量。这堵上的是一个供应链式配置攻击：**克隆一个仓库就能悄悄打开你的遥测导出**。同批还修了 Bash 权限规则里 mid-pattern `:*` 被跳过、resume 会话丢失 extended thinking、managed settings 里一个嵌套值无效导致整块被忽略等问题。

🟡 说明：以上来自 changelog 转载站（updatify / AI-TLDR / ai.jp.net）三方交叉，**未直连 Anthropic 官方 release notes 核实**。

来源：[updatify 转载的 2.1.282 changelog](https://updatify.io/releases/claude-code/40ee944d-e511-49af-b0b4-d6a509705213) · [AI/TLDR](https://ai-tldr.dev/releases/anthropic-claude-code-2-1-282) · [ai.jp.net 分析](https://www.ai.jp.net/article/claude-code-v2-1-282-blocks-repository-level-telemetry-tampering-with-major-secu-0d86b1)

### 6. 国产开源侧：一个把"阅卷人"也开源了，一个把参数压掉 60 倍 🟡

- **HuatuoGPT-3（FreedomIntelligence）**：提出 **OnePO**——跳过领域 SFT，用单阶段 RL 直接做医学适配，配"teacher retirement"（模型追上教师奖励后自动撤掉教师引导）。**HealthBench 上仅用 2 万训练样本拿到 67.2**，比 SFT+RL 高 2.7 分、比纯 RL 高 7.4 分；32B 变体 70.3。开源训练代码、OnePO-Medical-20K 数据集，以及一个 **8B 的 rubric grader**（HuatuoGPT-3-Grader-8B）。27B 版基于 Qwen3.8-27B。
- **AntSpeaker/MECT（蚂蚁集团开源）**：把 MoE 式专家分工引入全监督声纹训练，**9.57M 参数在 VoxCeleb1 上追平（均值略超）587M 参数的预训练模型**，参数相差约 60 倍；通过因果重训练做到 **100ms 流式延迟 + 近离线精度**。

🟡 说明：两条均为聚合站/自媒体转述（AGI Hunt、thenextgentechinsider、网易号、微博），**GitHub 仓库与 HF 页面未逐一核实**。

来源：[AGI Hunt 日报](https://agihunt.info/en/daily/2026-09-25) · [The Next Gen Tech Insider（HuatuoGPT-3）](https://thenextgentechinsider.com/pulse/freedomintelligence-unveils-huatuogpt-3-series-with-one-stage-policy-optimization) · [网易号（AntSpeaker/MECT）](https://www.163.com/dy/article/L7KAF1IP05561FZF.html)

---

## 三、为什么值得记

1. **`pass/fail` 是工具接口设计里最贵的一个布尔值。** 91 例静默失败里 76 例在 API 层/wrapper 层就已经发生——agent 收到的是"成功 + 部分数据"，它没有任何信号可以判断自己拿到的是不是全部。这意味着**错误处理的完备程度对你没有帮助**，因为根本没有错误。真正要改的是返回值契约：completeness、provenance、qualifier 必须跟着 data 一起走。

2. **"信息全对"也能把决策带偏 61 个百分点——这推翻了"检索准就安全"的假设。** CAVEAT 的 8 种机制没有一种是假信息，性能退化全部来自顺序、显著性、时机。只要你的 Agent 会在网页/列表/搜索结果里挑东西，排序权就在别人手里，而这是一个独立于 prompt 注入的攻击面。

3. **"先想清楚要什么"远不如"下单前再查一遍"管用。** CAVEAT-Harness 的消融很刺眼：结构化任务说明单独只贡献 6.7 个百分点，验证工具单独贡献 66.7。这和 9-24 记的"瓶颈下沉到运行时层"是同一件事的两面——能力在规划阶段已经够了，缺口发生在**提交之前的最后一步**。

4. **看 benchmark 先问一句：判分这件事能不能被被测方影响？** DrivingBench 的判据不可协商（车到没到终点），所以它 4 个模型只跑完 1 个，我们信；MentalHealthBench 的判据高度可协商（阅卷人是出题方自己的模型），所以它精致到 5,262 条标准，我们仍要打折扣。注意 OpenAI 至少做对了一件事：它**公开了"用户和专家评分不一致"这项研究，并明确说没有据此改评分**——这个披露比分数本身更能说明判据的选择是一种权力。

5. **便宜的评测不是在省钱，是在省掉信号。** Astra 成功那次 $7.74，Grok 最好那次 $0.19，相差约 41 倍；而 Grok 走不到 23 米。**失败便宜，成功贵**——任何"跑得很省的评测"都值得怀疑它到底测到了什么。

---

## 四、可行动

- [ ] **给自建 MCP 工具的返回值加三个字段**：`completeness`（是全量还是截断/子集）、`provenance`（来源、版本、时间戳）、`qualifier`（数值的单位与变换，例如 ChIP-Atlas 那个 `-10log10(Q)`）。先给你最常用的 3 个工具加，别一次铺开。
- [ ] **做一个"静默失败探针"**：对关键工具调用，主动构造已知答案的查询（已知存在的记录 ID、已知非空的字段），每天跑一次比对返回条数与字段完整度。ToolUniverse 那 7/15 工具 >50% 失败率就是靠"人工审计 + 已知答案"抓出来的，不是靠监控。
- [ ] **在下单/提交/发送类动作前加一步证据校验**：抄 CAVEAT-Harness 的 verification tool——要求 Agent 在提交前证明"搜索已足够完整、缺失或冲突的事实是否仍可能改变结论"。这是 +55 个百分点里贡献最大的一块（单独 +66.7pp）。
- [ ] **结构化目标说明要写，但别指望它单独生效**（消融只有 6.7pp）：把用户请求先固化成 hard requirements / comparative requirements / **仅用户明确陈述的优先级**，并在整个回合里锁死。它防的是 Objective Drift（25 对请求全部改选那个）。
- [ ] **清一遍 Claude Code 的仓库级配置**：跑 `claude doctor` 看哪些遥测变量被忽略；把 `CLAUDE_CODE_ENABLE_TELEMETRY` 之类从项目 settings 迁到 user settings；检查 `.claude/settings.json` 是否会进版本库。
- [ ] **给自己团队的评测立一条规矩**：凡是 LLM-as-judge，必须在结果旁写明 grader 模型名与版本；凡是用它评自家模型的地方，标红。能换成可外部复现的判据（执行结果、单元测试、真实终点）就换。

---

## 五、术语卡

| 术语 | 解释 |
| :--- | :--- |
| **静默失败（silent failure）** | 工具调用返回成功状态，但数据不完整/字段缺失/语义被改，且没有向 agent 或用户发出任何通知。与抛异常相反，它不产生可观测信号，因此监控栈完全看不到。 |
| **contextual reliability（上下文可靠性）** | ToolUniverse 论文提出的替代指标：agent–tool 交互在整条链路上是否**保留并传达**了支撑科学结论所需的信息、限定词、来源、范围与含义。比"调用是否成功"多问一层"这个数还带着它的意思吗"。 |
| **激励错位环境（incentive-misaligned environment）** | CAVEAT 的定义：环境（如电商平台）自身对结果有利害关系，会通过排序、赞助、延迟披露费用等方式引导 agent 偏离用户目标。关键点是**信息可以完全准确**，退化只来自呈现方式。 |
| **过早搜索终止（Premature Search Closure）** | Agent 只比较了少量可见选项就停止搜索并下单。CAVEAT 消融：把次优品挪到顶部赞助位，访问率 45/60→60/60，购买率 0/60→48/60；Hard 上 50 次失败全部停在第 1 页（共 88 页）。 |
| **OnePO（One-stage Policy Optimization）** | 单阶段策略优化：跳过领域 SFT，直接用 RL 把基座模型适配到垂直领域，避免被模仿分布锁死；配 "teacher retirement"，模型追上教师奖励后自动撤掉教师引导。 |
| **MoE（Mixture of Experts，混合专家）** | 用一组"专家"子网络 + 路由按需激活，推理时只算部分参数。蚂蚁 AntSpeaker/MECT 把它搬到声纹验证这种全监督小任务上，9.57M 参数追平 587M 预训练模型。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
