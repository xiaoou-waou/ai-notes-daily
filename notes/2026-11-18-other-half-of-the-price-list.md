# 2026-11-18｜价格表的另一半，写在你的前缀里

> 三家把缓存价压到输入价的 4–5%，但吃不吃得到这个价，取决于你的请求前缀有多干净。

**标签**：`#成本结构` `#prompt缓存` `#上下文工程` `#Agent工程` `#开源工具`
**生成时间**：2026-11-18 12:10（北京时间）

---

## 一、今日观察

今天最容易被记住的数字是"降了 20%"。但把三家的价目表并排放，会发现降得最狠的不是标准价，是缓存价：

| 模型 | 输入价（每百万 token） | 缓存命中价 | 缓存价 / 输入价 |
| :--- | :--- | :--- | :--- |
| GPT-6.2 Astra | $8.00（较上代 −20%） | $0.40（−60%） | **5%** |
| Qwen4-Max | $1.50 | $0.075 | **5%** |
| Hy4 flash | ¥0.50 | ¥0.02 | **4%** |

三家不同公司、不同架构、不同币种，把同一个比值定在了 4–5%。这意味着价格表事实上已经分成两档，两档之间差 **20 倍**——而决定你在哪一档的，不是采购量，是你的**请求前缀稳不稳定**。

"缓存"今天同时在三个地方被定价，而且三层互相咬合：

| 层 | 今天谁在动这条线 | 发生了什么 | 代价记在谁头上 |
| :--- | :--- | :--- | :--- |
| **显存里的 KV 缓存** | vLLM 0.34.0 | 默认块大小 16→64，按预热后实际空闲显存扩容；MiniMax-M3 在 H200 上从 43.3 万 token 拓到 67.2 万 | 并发 128 时每 token 解码延迟 **+6–18%** |
| **价目表上的缓存价** | OpenAI / 阿里 / 腾讯 | 缓存价压到输入价的 4–5% | 厂商让掉的，是它本来就要省的算力 |
| **请求里的前缀** | Duco / TokenEconomizer | 工具描述从约 20 万 token 降到约 2 万；23 个工具描述里只有 7 个被真正调用 | 使用方自己 |

三层里只有第三层是今天就能动的。而两篇工程材料恰好说明它们不是三件事：Duco 把工具描述从静态前缀里挪出去之后，AWS 官方博文的原话是——"静态前缀（系统提示加三个 meta-tool）保持又小又稳，skill 加载进对话而不是工具列表，所以加载 skill 不会让缓存失效"。**省 token 和吃到缓存价，是同一个动作的两面。**

反面证据来自同一天的另一份财报：英伟达 2027 财年 Q3 营收 1158 亿美元、同比翻倍，数据中心 1076 亿；CFO 在电话会上说 Hopper 续约价最高到原价两倍、B300 发布以来涨超 60%。模型层在打折，算力层在涨价，中间那段差价，只能从"少发点没用的 token"里抠。

需要交代撞题：09-17《同一张价目表，四倍账单》的结论是"单价这条路走到头，战场搬到路由、形态、供给"；本轮不是同一个论点——本轮说的是**同一张价目表自己分叉成两档**，而分叉依据（前缀稳不稳）是一个不动模型、不动供应商就能改的工程变量。11-17 写过 Qwen4-Max 把 cost per task 当发布会头牌，这里只用它的单价做横比。11-12 提过"共享输入只计一次"，那是计费口径；这里是缓存命中率的架构问题。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 GPT-6.2 Astra / Sol：标准价降两成，缓存价降六成
11 月 17 日，OpenAI 发布 GPT-6.2 Astra 与 GPT-6.2 Sol，即日进入 ChatGPT Work、Codex 与 API。Astra 定价 **输入 $8 / 缓存输入 $0.40 / 输出 $40**（每百万 token，输入输出较 GPT-6 Astra **降 20%**，缓存 **降 60%**）；Sol 沿用 GPT-6.1 Sol 的 **$2 / $0.1 / $10** 不变。官方称 Astra 在多步专业任务评测（Agents' Last Exam）上较上代 **提升 5.2 分、执行成本不到上代三分之一**；Sol 在 Cognition 的 FrontierCode 2.0 上仅落后 Astra **0.5 分以内、成本约其五分之一**，在 LifeVal 日常任务上超过 GPT-6 Astra、成本约其七分之一。安全侧：两款模型均达到其准备框架的网络安全"**关键（Critical）**"与生物化学"**高（High）**"级别，Astra 另达"自我改进 High"；OpenAI 同步收紧高风险网络安全协助的默认限制。
来源：[界面新闻](https://www.163.com/dy/article/LC0ION540534A4SC.html)｜[凤凰网科技](https://tech.ifeng.com/c/8y90EqdveQg)｜[The Daily AI Briefing](https://www.aiimpacthub.com/ai-news/2026-11-18)
🟡 英国 AISI 称两个预发布版本出现"明显的鲁棒性回退"、OpenAI 随后调整了拒答边界——此说见于聚合日报转述，未见 AISI 原文，仅记为待核实。

### 2. 🟢 微软一次发七款自研模型：用"够用"定价，把边界写进脚注
Ignite 2026（11 月 17 日），微软发布七款 MAI 模型。核心是 **MAI Code 2**：在 DeepSWE 1.1、Terminal Bench 2.1、SWE-Atlas、FrontierCode v1.1 四个基准上，达到 **GPT-6.1 Sol 98% 的编码质量、约 40% 的价格**；对 Claude Opus 5.5 是 **96% 性能、5% 的价格**；258 人盲测前端任务中 **64%** 的情况下被优先选择。但官方原文明确写了边界：**"它们尚未为更难的问题调优，比如基础科学研究，以及超长程的 agentic 工作。"** 决策模型 **Decision 1.1** 比 GPT-Sol 6.1 **快 50 倍、便宜 79 倍**（4,000 家客户在用，在 AA Decision Index 上领先 Jev、Google 与 OpenAI）。同日宣布 **MAI Licensed Weights**：客户可用自有数据定制权重，并跑在自己的 Azure 环境里，经 Frontier Company 交付。配套 Maia 200 已投产，每瓦 token 数提升 1.7 倍。
来源：[Microsoft AI 官方](https://microsoft.ai/news/microsoft-ignite-2026)｜[微软官方博客（Ignite 主题演讲）](https://blogs.microsoft.com/blog/2026/11/17/ignite-2026-building-the-frontier-ecosystem)

### 3. 🟢 TokenEconomizer：不改模型、不改 agent，编码 agent 成本降 18.4–30.9%
11 月 16 日，UC Berkeley、微软研究院与微软安全团队开源 **TokenEconomizer**。它读取同一仓库已完成会话的日志，用"微技能（micro-skill）+ 工具裁剪 + 卡死干预"三种手段减少后续会话的浪费，不改 agent、不改底层模型。评测：**277 个 SWE-Bench 任务、6 个仓库、5 种 agent 与模型组合，平均单任务成本降 18.4–30.9%，30 个"仓库 × 组合"全部省钱，Pass@1 在 5 组中有 4 组上升**；起始时无任何历史，累计成本在第 6 个任务起低于基线。前置剖面（Claude Code × 60 个任务）给出三个浪费源：同仓库有 5 个以上完成任务后，**30% 的工具调用在重复此前动作**（跨仓库只有 **7%**）；**每轮收到 23 个工具描述，16 个从未被调用**；**17% 的失败任务吃掉了 32% 的花费**。作为对照，直接调低 reasoning effort 省得一样多甚至更多，但性能明显下降。Web-Bench 顺序开发降 16.0–21.2%，安全审计（每个任务都是新仓库）降 6.4–19.6%。
来源：[Microsoft Research 官方博客](https://www.microsoft.com/en-us/research/blog/tokeneconomizer-learning-from-experience-to-make-ai-coding-agents-more-efficient/)｜[论文页](https://www.microsoft.com/en-us/research/publication/tokeneconomizer-experience-driven-black-box-cost-control-for-coding-agents/)

### 4. 🟢 Duco：300–400 个工具的描述占掉 20 万 token，改成按需加载后降到 2 万
AWS 11 月 16 日发布客户案例：金融服务运营平台 Duco（月处理 200 亿笔交易、200+ 客户、含全球前 20 大银行中的 7 家）把 agent 栈重建在 Bedrock AgentCore 上。每个租户通过 Gateway 暴露 **300–400 个工具**，**约 20 万 token 的工具描述在工作开始前就被塞进上下文**，导致对话越长质量越差。改法是 MCP 的 `skill://`、`system://`、`ui://` 资源类型加三个 meta-tool——`load_skill`、`find_tool`、`invoke_tool`，把描述移出静态上下文、按需拉取：**主上下文从约 20 万降到约 2 万 token（−90%）**，并且**保住了 prompt caching**。官方称不需要改基础设施，同一批模型、同一批工具、同一批任务，响应质量经评测框架验证有提升。业务侧：对账部署快 10 倍，一家全球银行 onboarding 成本降 70%、直通处理率提升 20% 以上。
来源：[AWS Machine Learning Blog（官方）](https://aws.amazon.com/blogs/machine-learning/how-duco-transforms-financial-data-automation-with-amazon-bedrock-agentcore/)

### 5. 🟢 vLLM 0.34.0：默认值改了，容量涨一半，解码慢一点
11 月 16 日发布的 vLLM 0.34.0（1,061 个提交、412 位贡献者）把 Extensible KV cache 设为默认，`gpu_memory_utilization` 默认 1.0，按预热与 CUDA graph 捕获后**实际空闲的显存**来定缓存大小；默认 block size 从 **16 改为 64**。官方举例：MiniMax-M3 在 H200 上缓存从 **43.3 万 token 拓到 67.2 万**。代价写在同一条 release note 里：部分 H200 模型在**并发 128 时每 token 解码延迟上升 6–18%**。同时 Model Runner V1 被移除，设 `VLLM_USE_V2_MODEL_RUNNER=0` 会直接启动失败。
来源：[vLLM 0.34.0 release notes（社区汇总）](https://wittywires.com/forums/topic/vllm-0-34-0-adds-10-models-and-makes-its-new-kv-cache-sizing-the-default)｜[升级要点整理](https://onlinelearningportal.website/vllm-0-34-upgrade-guide)

### 6. 🟢 英伟达 Q3：模型层在打折，算力层在涨价
截至 10 月 25 日的 2027 财年 Q3：营收 **1158 亿美元（同比 +103%、环比 +20%）**，数据中心 **1076 亿（+110%）**，GAAP 毛利率 74.8%；Q4 指引 **1300 亿美元 ±3%**，毛利率指引 71–72%。CFO 兼临时 CEO 克雷斯在电话会上称，按多年期协议 Hopper 的续约价最高达原价两倍，**B300 自推出以来价格上涨超过 60%**；云业务积压订单达 2.5 万亿美元。
来源：[NVIDIA 官方新闻稿](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-third-quarter-fiscal-2027)｜[证券时报](https://www.stcn.com/article/detail/4341237.html)

---

## 三、为什么值得记

1. **折扣是乘数，浪费是加数。** 20% 的折扣乘在一个 20 万 token 的脏前缀上，绝对值仍然是脏的。价目表上的百分比，救不了请求结构上的浪费——这是今天两份工程材料最硬的共同结论。

2. **缓存价差 20 倍，意味着 prompt 架构已经是一个财务决策。** 没人愿意为"每次请求重发一遍工具说明书"付 20 倍的钱，但绝大多数团队从没测过自己请求里的 cached token 占比。这个数字今天在 OpenAI 和 Anthropic 的响应体里都直接返回，取一次就能知道。

3. **"经验不跨仓库"（同仓库 30% 重复、跨仓库只有 7%）直接否掉了"装个插件就降本"的期待。** 三个主打固定策略的开源插件都只在部分仓库有效，这解释得通：省钱策略必须按仓库、按业务自适应，没有通用解。

4. **便宜的模型把边界写在脚注里。** 40% 的价格买 98% 的质量，前提是你在做"日常企业编码"；微软自己写明"尚未为更难的问题调优，比如基础科学研究和超长程 agentic 工作"——而那恰好是最贵、最需要模型的那类任务。省下的钱，会以返工的形式还回去。

---

## 四、可行动

- [ ] **先算一次真实单价。** 从 API 响应里取 `usage.prompt_tokens_details.cached_tokens`（OpenAI）或 `cache_read_input_tokens`（Anthropic），除以总输入 token 得到命中率。低于 50% 说明前缀设计有问题，降价对你几乎无感。
- [ ] **数一遍"每轮固定发送的工具描述条数"与"实际被调用条数"。** TokenEconomizer 的基线是 23 发 7 用；比值比这更差时，先做工具裁剪，收益大于换模型。
- [ ] **把工具 schema 移出系统提示。** 静态前缀里只留 2–3 个 meta-tool（`find_tool` / `load_skill` / `invoke_tool`），其余按需拉取。关键是保持静态前缀"小而稳"——否则一加载就破缓存，白忙。
- [ ] **在同一个仓库连跑 10 个以上任务再评估 TokenEconomizer。** 开源、不需要自带 API key、学到的内容只留在本地；它的收益从第 6 个任务才开始转正，单个任务上看不出效果。
- [ ] **升 vLLM 0.34 前先做对照。** 同一负载下 `--block-size 16` 与默认 64 各跑一轮，量 TPOT 与最大并发。这次的默认值是拿延迟换容量，不是纯赚。

---

## 五、术语卡

| 术语 | 解释 |
| :--- | :--- |
| **prompt caching（前缀缓存）** | 服务端把请求开头那段完全相同的 token 的计算结果存下来复用。命中部分按缓存价计费，通常只有输入价的 4–5%，但要求前缀逐字节一致才命中。 |
| **前缀稳定性** | 请求开头（系统提示 + 工具定义）在各次调用之间保持不变的程度。任何一处改动都会让它之后的缓存全部失效——所以"往系统提示里加一句"是有价格的。 |
| **KV cache** | 推理时把每层注意力的 key/value 缓存下来避免重算；vLLM 的 block size 就是这块显存的分页粒度，块越大越省管理开销，但更容易产生内部碎片。 |
| **micro-skill** | TokenEconomizer 的做法：把"这个仓库的测试是这么跑的"这类一句话知识，在多次会话确认后写入启动上下文，被后续证据推翻就撤回。 |
| **TPOT** | Time Per Output Token，每个输出 token 的解码耗时。区别于 TTFT（首 token 延迟）：TPOT 决定长输出的体感速度，也正是扩大 KV 缓存时要付出的代价。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
