# 2026-11-24｜判断被拆出来了，独立性没跟上

> 今天的四个发布都把"判断"从"生成"里拆成了独立一步，但拆给谁，独立性差了三档。

**标签**：`#Agent工程` `#审批自动化` `#决策模型` `#语义治理` `#架构模式`
**生成时间**：2026-11-24 12:00（北京时间）

---

## 一、今日观察

今天最响的模型新闻是智谱 GLM-5.4：官方博客写明把 GLM-5 基座的 **28 层循环跑两遍**、权重共享，宣称达到 2T–3T 参数级水平；代价是官方自己承认的——模型容易陷进"马拉松式思考"的长循环。这是架构新闻，值得看，但不是今天最该抄进生产系统的东西。

同一批发布里，另外四件事做的是同一个动作：**把"判断"从"生成"里剥离出来，单独交给一个东西去做。** 剥离之后的问题立刻变成了：判断者是谁、它和被抓判断的东西隔了几层。

按独立性从低到高，今天恰好凑齐了四档：

**第一档，同一个主体。** Anthropic 的 Claude Ship（beta）把 PR 之后的四步——审、改、批——都交给了 Claude。官方文档写得很清楚：Code Review 已 GA；PR Steward 处理失败的 CI、冲突和评审意见，**设计上不负责批准或合并**；Claude Approvals 按仓库里的 `.claude/approvals.yml` 判断谁还差几票，可以发"批准式 review"。也就是说，写代码的是它，找问题的也是它，点头的还是它——只是这三次点头之间的策略由人写在一个 YAML 里。Claude Code 团队自报的数字是：6 月到 9 月合并 PR 数翻倍，回滚率反降 40%。

**第二档，独立的小模型。** AWS 的 Strands Decider v2 是一个"只打分、不写字"的模型族：给它一个场景和一组既定选项，它直接给每个选项输出概率，不做文本生成。基于 Gemma 4，五档规模到 31B，Apache 2.0，权重已上 Hugging Face。它的意义不是分数，是形态——**agent 循环里大量动作本来就是"从固定选项里选一个"**（走哪个工具、路由到哪个队列、这条工单归哪类），这类动作不需要造句。v1 在亚马逊内部工单分类上换掉 Claude Sonnet 4.6 后，单次调用从 **4,215 ms 降到 897 ms**，按列表价折算每百万张工单从约 **2.22 万美元降到 500 美元**。

**第三档，独立的进程。** Google 的语义治理策略（Preview，11 月 20 日）把裁判放在 Agent Gateway 上、agent 自己的代码之外：模型提议一个工具调用，先送去策略引擎，由一个 LLM 裁判回答两个问题——符不符合你写的明文政策，以及是不是用户真的要它做的。两问都过才放行；不过就整条调用换成拒绝消息，判断和理由写进 Cloud Logging。这一步的价值在于**它管的不是"你能做什么"，而是"这一次做的算不算数"**——权限列表挡不住间接提示注入，因为被注入的那个调用，本身就在权限之内。

**第四档，根本不看内容。** Google 同期把 Envoy 往 agent 流量上推：解析请求体、在 OpenAI/Anthropic/Gemini 三种格式间转换、按 **token/分钟与 token/天** 给租户或模型限额，推理前就返回 429；还能按 MCP 的 JSON-RPC 方法路由、把 system prompt 相同的请求送到已缓存 KV 的 GPU 上。

四档摆在一起，取舍很清楚：**越独立的东西越看不见内容，越懂内容的东西越难独立。** Envoy 不会误判，因为它根本不判断语义；Claude Approvals 最懂代码，但它和被审的代码出自同一个模型家族。

而且今天最值得抄的一条设计，藏在细节里：Anthropic 把"谁能改审批规则"留在了人手里——据 TechCrunch 转述，修改审批策略文件本身的 PR 始终需要两个人批准；在组织设置里开关这组 agent，需要 Owner 角色。**能自动批代码的 agent 已经出现了，但"批'什么可以被自动批'"这一步没有交出去。** 这是整套设计里唯一一处递归被主动切断的地方。

Google 那边也有一个必须写在验收清单上的洞：**流式响应不参与语义评估**。官方要求被治理的模型调用走支持的非流式路径；只带文本的回复也不评估，因为它不触发动作。这意味着如果你们的 agent 链路默认开 stream，那道语义闸门从旁边就走了过去。

撞题要交代：11-03 写的是"闸门之间的缝隙有多长"（时间维度），本轮问的是**判断者与被判断者隔了几层**（结构维度）；10-27 写的是三份官方文件自认边界没挡住，本轮不问挡没挡住，问的是**挡住它的那个东西是谁**；09-22 写默认值归谁，本轮只把"默认状态"当作一档独立性的外在表现，不展开。GLM-5.4 的循环架构 11-20、11-22 已从"斜率"和"容量"两个角度写过，此处只作开场，不重复。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Claude Ship：写代码的那个模型，开始给自己的 PR 点批准

11 月 24 日发布（beta），面向 Team / Enterprise。三个组件：**Code Review**（已 GA，行内评论按严重程度排序）、**PR Steward**（处理失败检查、合并冲突、人和机器人的评审意见并推修复提交，**不批准也不合并**）、**Claude Approvals**（按策略判断谁还差几票，可发批准式 review）。

官方文档里几条容易被漏掉的机制：策略文件是仓库根下的 **`.claude/approvals.yml`**，可以规定某路径的改动需要几人批准、Claude 能在哪些地方批准；**只有在 GitHub 里把它设成 required check，才会真正阻塞合并**；文档明确警告，若同时用 auto-merge 或 merge queue 且策略不要求人工批准，变更可能"在无人审查的情况下合并"。建议先以 **observe 模式**跑（只报告"会怎么判"，不阻塞，且照常计费）。计费按各 agent 的 token 走 usage credits，与套餐内用量分开，PR Steward 默认没有自己的支出上限。不适用于启用 Zero Data Retention、HIPAA 或客户自管密钥的组织。

🟡 效果数据为 Anthropic 自报（TechCrunch 转述）：Claude Code 团队 **90% 以上**代码由 Claude 写；6–9 月合并 PR 数**翻倍**、回滚比例**下降 40%**。这两组数字不能证明"AI 审得好"，只能说明流程变快、返工没变多。
来源：[Claude Code 官方文档：Claude Ship](https://code.claude.com/docs/en/claude-ship)｜[IT之家（TechCrunch 转述，三组件与策略文件）](https://www.ithome.com/1/031/257.htm)｜[凤凰网科技（审批权限受团队策略限制）](https://tech.ifeng.com/c/8yJ2TwIuMw7)

### 2. 🟢 AWS Strands Decider v2：只给选项打分，不生成文字

11 月 23 日发布，五个开源决策模型，基于 **Gemma 4**，从边缘版到 **31B**，**Apache 2.0**，权重在 Hugging Face 与 AWS 的 Decider 仓库。定位是"系统一"：一次前向就给完所有候选的概率，不做文本生成。v2 的训练集含 **1,748 万**条决策样本；读出层直接给选项 token 打分（v1 用的是 pointer head）；改用前缀双向注意力，共享状态只编码一次。

🟢 精度与校准（AWS 自测，未见第三方复现）：六项文本基准均分从 v1 26B-A4B 的 **70.0** 升到 v2 31B 的 **82.1**，小尺寸 E4B 从 62.7 升到 **74.4**；期望校准误差从 **0.062** 降到 **0.027**（越低越敢拿它的概率当阈值用）；图像任务 **90.1**、视频 **70.2**。路由实验里，在 Claude Haiku 5.5 与 Sonnet 5.5 之间分流，保留了 Sonnet **94%** 的任务完成度，只花 **44%** 的钱。

⚠️ **成本数字的来源要说准**：**98% 成本下降、78% 响应提速来自 v1**，场景是亚马逊内部一张大型工单系统的 20 类分类，单次调用 4,215 ms → 897 ms、每百万张约 $22,200 → $500。AWS 自己在 11 月 9 日的说明里把结论限定在"高频、答案集固定"的任务上；需要写解释、标签体系常改、或超出上下文的任务仍要 LLM。多条转述把这条记在了 v2 头上，属于口径滑移。
来源：[Unite.AI（规格、基准、v1 成本证据与限制条款）](https://www.unite.ai/aws-releases-strands-decider-v2-and-sandboxes-more-coding-agents)｜[SiliconANGLE 转述（发布范围与许可）](https://tpsreport.news/news/aws-strands-decider-v2-open-weight-decision-models)｜[Daily Artifact（与 Gemini Decision 1 的对比）](https://dailyartifact.ai/story/aws-launches-5-new-open-decision-models-for-ai-agents-1oisd)

### 3. 🟢 同一批还发了 Box CLI：凭据不进沙箱

AWS 同时给 Strands Box（去年 10 月开源的 OS 级沙箱）加了 Box CLI，支持把 **Claude Code、Codex、Kiro CLI** 装进去跑。针对的是"YOLO 模式"——关掉所有权限提示让 agent 自由执行终端命令、改文件、调外部工具。做法是策略管沙箱：限制可访问的文件、命令、网络主机；**API key 与 AWS token 存在沙箱之外，只有策略批准的请求出沙箱时才注入**，agent 全程不持有凭据；还能按任务切 profile（编码 agent 给仓库权限，排障 agent 只给只读诊断）。AWS 自己总结的原则是：**隔离必须独立于被隔离的模型而运作**。
来源：[Unite.AI（Box CLI 与凭据外置）](https://www.unite.ai/aws-releases-strands-decider-v2-and-sandboxes-more-coding-agents)｜[AI Agent News（策略与 profile 切换）](https://aiagentnews.io/stories/aws-releases-strands-decider-v2-models-and-box-cli-for-agent-sandboxing)

### 4. 🟢 Google 语义治理：把"权限"升级成"意图"，但流式不评估

11 月 20 日发布，Preview。检查点放在 **Agent Gateway**、agent 代码之外。模型提议工具调用 → 网关送策略引擎 → LLM 裁判对照"对话上下文 + 系统指令 + 工具描述 + 你写的明文政策"作判断。两问都过才放行；不过则**整条调用**（含同一响应里的其他 tool call）替换成可自定义的拒绝消息，判断与理由进 Cloud Logging。用户意图检查**默认开启**，不需要额外写政策，针对的正是间接提示注入。政策由法务/合规用自然语言写，无需改代码或重新部署；可管全部工具或单个工具的具名参数。支持 Gemini、Anthropic Messages、平台托管 Claude 以及 OpenAI 兼容接口（含自托管 vLLM）。官方明确说裁判是概率模型、**结论可能波动**，建议先 dry run 再转执行。

**限制里有两条硬边界**：只带文本的回复不评估（不触发动作）；**流式响应不评估**，被治理的调用必须走受支持的非流式路径。
来源：[DailyByte（两问机制、示例、流式限制）](https://dailybyte.pk/blog/google-semantic-governance-policies-block-ai-agent-calls-23-november-2026)｜[AI Magazine Canada（政策写法与追责边界）](https://aimagazine.ca/ai-policy-in-canada/google-semantic-governance-policies-agent-rules)｜[SecurTek（同一批还发了跨云 Agent 异常检测）](https://securteksecurity.com/news/google-semantic-governance-agent-anomaly-detection-cross-cloud)

### 5. 🟢 Envoy 长出"按 token 计价"的控制面

11 月 23–24 日公布，四块能力：**请求体解析与格式互转**（在 OpenAI / Anthropic / Gemini 之间翻译，也能实时解析 SSE 流统计 token 用量）；**token 配额**（按 token/分钟、token/天 对租户、项目或模型限额，推理前估算并直接返 429，同时统计累计 token 与消息数，用于压制失控的递归 agent 循环）；**路由**（把 system prompt 相同的请求送到已缓存 KV 的 GPU；主模型失败或 429 时切备用池；MCP 流量按 JSON-RPC 2.0 体与 `Mcp-Method` / `Mcp-Name` 头路由，后端校验不匹配就拒）；**安全检查**（经外部处理接口接 Model Armour、ShieldGemma 或本地分类器，查提示注入与敏感数据外泄）。

Google 给的理由很直接：传统七层代理不适配 agent，因为关键策略信息在请求体里而不在 URL 或 header 里；agent 的消耗也不该按请求数计，该按 token 计。公告未给性能数字与第三方验证。
来源：[SecurityBrief（四块能力与设计理由）](https://securitybrief.com.au/story/google-cloud-extends-envoy-for-autonomous-ai-agents)｜[AI in Context（429 前置与 MCP 头）](https://aiincontext.com/articles/envoy-adds-token-quotas-and-model-routing-for-autonomous-ai-agents)

### 6. 🟢 两个"发布但不交付"的对照：GLM-5.4 与星辰 4.1

**GLM-5.4**（11 月 23 日，官方博客）：把 GLM-5 基座的 **28 层循环两遍**，权重共享；30B 同构消融显示，参数不变、训练算力只多约 **10%**，循环版在数学、科学推理、长上下文上收益最大，且**平均输出长度下降 10–14%**——部分推理从显式 token 挪进了隐式深度。工程上三个改动值得记：门控渐进更新（第一遍小步写、第二遍全量写，避免激活爆炸）、混合 KV cache（**多跑一遍只多一个滑动窗口的 KV**，而非整份上下文）、稀疏注意力索引复用（第二遍零额外索引开销）。吞吐：**非高峰 200 tok/s，高峰 70–80 tok/s**。API 标注 "Coming Soon"，权重计划在"完成必要安全加固后"开源。

**星辰 Xing4.1-Preview**（11 月 22–23 日放权重）：**285B 总参 / 约 17B 激活**，45 层，256 路由专家激活 8 个加 1 个共享，MLA + DeepSeek 稀疏注意力，原生 **100 万**上下文，**Apache 2.0**。技术报告（arXiv:2611.22115，11 月 17 日提交）称在 **8,192 张昇腾 910C** 上、用 MindSpore 完成预训练，报告里的数字是系统效率（prefill 4.68×、解码 2.67–3.77×），**不是能力跑分**；模型卡未给对标闭源旗舰的成绩。BF16 权重约 **521 GiB / 261 个分片**，按模型卡需约 8 张 80GB 卡（TP=8）；NVFP4 版本约 190GB。
来源：[Z.ai 官方博客：GLM-5.4](https://z.ai/blog/glm-5.4)｜[The Hype（Xing4.1 规格与 DeepSeek 谱系）](https://thehype.news/china-telecom-xing4-1-preview)｜[Baillie（分片数、模型卡未给跑分）](https://baillie.ai/news/2026-11-23/china-telecom-posts-open-weights-for-xing4-1-preview-a-285b-model-it-says-was)

---

## 三、为什么值得记

1. **"自审自批"的真实风险不是审错，是信号退化。** 同一个模型家族写、审、批，它在审的其实是自己上一次的输出分布。合并数翻倍、回滚率降 40% 是好数字，但它度量的是"流程没变慢"，不是"审出来的问题变多了"。要判断这套东西有没有用，得看一个它自己产不出的指标：**被人驳回的 AI 批准有多少**。这个数只有你部署了 observe 模式才拿得到。

2. **Decider 的真正价值是把"判断"变成一个可校准的概率，而不是省钱。** 98% 那个数字来自单点部署的 v1，推广价值有限；但 ECE 从 0.062 压到 0.027 是可迁移的——只有当模型说"我有 0.8 的把握"时真有八成对，你才敢拿这个阈值去决定"要不要升级到大模型"。**校准是路由的前提，不是路由的副产品。** 这也解释了为什么 94% / 44% 这笔交换敢做：省的不是模型，是"在不该花的地方不花"。

3. **独立性和理解力是反比，选档位就是选你愿意接受哪种失败。** Envoy 那种只看 token 的限额几乎不会出错，代价是它完全不知道自己在放行什么；语义裁判看得懂内容，代价是结论会波动、流式还看不见；Claude Approvals 最懂代码，代价是它和被审对象同源。没有一档是全能的，只有"你的失败模式是哪一种"。

4. **唯一不该外包的判断，是"谁有权改规则"。** Anthropic 把审批策略写进仓库（可 review、可追溯、可 CODEOWNERS），又把改策略本身的 PR 钉成两人批准、把开关锁在 Owner 角色后面。这两道锁都不聪明，但它们不可递归绕过——**一套自动化系统的可信度，最终取决于它给自己留了几道不能自动通过的门。**

---

## 四、可行动

- [ ] **如果试 Claude Ship，先跑 observe 两周再开执行。** 把"它想批的"与"人实际批的"做差集，重点看假阳性（它批了但人不该批）。注意 observe 模式照常计费，先设 PR Steward 的月度上限。
- [ ] **确认 `.claude/approvals.yml` 被设成 GitHub required check。** 不设就只是评论，不阻塞合并；若同时开 auto-merge 或 merge queue 且策略不要求人工批准，官方文档写明会出现"无人审查即合并"。
- [ ] **把 approvals.yml 本身纳入 CODEOWNERS 双人审批，并检查谁有 Owner 权限。** 规则文件的修改权，等于整套审批系统的根权限。
- [ ] **给 agent 循环做一次"打分 vs 生成"拆分。** 把过去一周的调用按"从固定选项里选"和"需要写解释"分类；前者占比高，就值得引入一个 decider 类小模型，并先用 ECE 而不是准确率来验收。
- [ ] **如果你的链路默认开 stream，别把语义治理当成已覆盖。** 官方明确流式响应不评估；要么把受治理的调用改成非流式，要么把检查点前移到工具侧（MCP 网关 / 出口代理）——那里看到的是调用本身，不是流。
- [ ] **抄 Box CLI 的凭据模型：key 不进沙箱，出网时按策略注入。** 这条不依赖模型不犯错，是整套隔离里最抗腐化的一层。
- [ ] **GLM-5.4 现在只有 Z.ai Chat 与 Coding Plan，API 标 "Coming Soon"，权重待安全加固。** 别写进依赖清单，等 API 与权重都有日期再评估。

---

## 五、术语卡

| 术语 | 解释 |
| :--- | :--- |
| **决策模型（decider）** | 不做文本生成、只给一组既定选项打分的模型：一次前向输出各选项的概率。适合 agent 循环里的路由、分类、工具选择等高频小判断。 |
| **期望校准误差（ECE）** | 模型自称的置信度与实际正确率的平均偏差。ECE = 0.027 意味着它说"八成把握"时，长期看真有约八成对。阈值型路由必须先看这个数，而不是只看准确率。 |
| **策略即代码（policy as code）** | 把审批/访问规则写成仓库里的文件（如 `.claude/approvals.yml`），随代码一起 review、版本化和追溯，而不是配在某个后台页面里。好处是可审计，风险是它变成了新的根权限。 |
| **语义治理 vs 权限控制** | 权限控制回答"这个 agent 能不能删文件"；语义治理回答"这一次删文件，是不是用户要它做的"。后者用来挡间接提示注入——被注入的调用往往完全在权限之内。 |
| **凭据外置（credential injection at egress）** | 沙箱内不存放任何密钥；只有当一条请求通过策略检查、准备离开沙箱时，才由外层注入凭据。这样即使 agent 被提示注入控制，也拿不到可复用的密钥。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
