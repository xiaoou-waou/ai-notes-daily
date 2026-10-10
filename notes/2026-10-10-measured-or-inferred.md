# 2026-10-10｜「这是测的还是算的」，今天第一次被写进产物里

> 紫外线全天图逐像素标出「测得/预测」，报表数字可下钻到 SQL——模型补的那部分，今天开始被显式标注。

**标签**：`#出处标注` `#决策模型` `#Agent训练` `#推理引擎` `#国产Token经济`
**生成时间**：2026-10-10 12:32（北京时间）

---

## 一、今日观察

今天六件事指向同一个动作：**把"这部分是观测到的、那部分是模型补的"写进产物本身**。

不是发论文讲方法，是直接在交付物里加一个字段。Anthropic 的紫外线全天图给每个像素标 `measured` / `predicted` 并附不确定度；Claude Dashboards 让每个数字可点开看它背后的 query、每个图表标最后刷新时间；vLLM v0.31.0 把前缀缓存的 extra key 按来源打 tag，让 LoRA 名和 `cache_salt` 不再撞车；Anthropic OSS Scanner 与 Hugging Face Carbon-A 反过来标——明说"输出 100% 由模型生成，无人复核"、"5.66 亿是候选位点，不是确认基因"。

| 产物 | 标的是什么 | 关键数字 | 信源 |
| :--- | :--- | :--- | :--- |
| 紫外线全天图 | 每个像素：测得 / 预测 + 不确定度 | 约 **1/3** 天区是推算；遮住已观测区再补，**差异约 10%** | 🟢 |
| Claude Dashboards | 每个数字背后的 query + 最后刷新时间 | — | 🟢 |
| vLLM v0.31.0 | prefix cache extra key 按来源打 tag | LoRA 名与 `cache_salt` 不再碰撞 | 🟢 |
| Microsoft-Decision-1 | 「这个概率在什么扰动下不变」 | 8 种扰动下结论翻转 **1.3%**，选项改写/逆序/打乱 **0 次** | 🟢（厂商自测） |
| Anthropic OSS Scanner | 「这份报告没有人核过」 | 97 条高危中 **85 条（88%）** 达标，真误报 **1 条** | 🟢 |
| HF Carbon-A | 「这些是候选，不是确认基因」 | 42 个基准基因组 macro-F1 **0.944** | 🟡 |

但今天真正值得记的是**反面那半句**。紫外线图做完后，Ménard 在最暗的天区里用肉眼看到一个个淡淡的圆——那是 GALEX 单次观测的足迹，由地球大气残余辉光造成。Claude 在项目一开始就把它列进了问题清单，**但地图仍然通过了两轮由其他 agent 执行的审查，没人发现**。

也就是说：**能给"推算"打标签的系统，自己识别不出"喂进来的观测本身就是坏的"。** 标注出处防的是混淆，防不住上游污染。多一轮 AI 审查也不等于多一层保障——审查者和被审查者共享同一套盲区。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. Microsoft-Decision-1：主打指标不是准确率，是「换个说法结论还一样」

🟢 微软官方博客（10-09，作者 Achint Srivastava，Office of the CTO）：给定固定选项集，单次前向返回每个选项的**校准概率**；题型支持 yes/no、多选、打分，以及按 rubric 给 AI 回答与 agent 动作评分。基于 **Qwen3.5-9B** 后训练，后续将 rebase 到 MAI 与 OpenAI 模型。已在 Microsoft Foundry 上线，OpenRouter 已开通。

- 鲁棒性（官方列为四大挑战之一）：对同一请求做 **8 种扰动**（改写、换选项描述、选项重排、改 key、无害格式噪声等），**平均 1.3%** 的决策发生翻转；**选项描述改写、选项逆序或打乱时 0 次翻转**
- 准确率：官方称 **36 项基准、近 15 万道题**（训练时 blind）中排名第一
- 安全：**11 项基准、5,250 条请求**（有害内容、越狱、prompt injection）
- 定价：**$0.042 / 百万输入 token，输出免费**
- 内部实测：Xbox Research 用其分类 **10,000+** 条玩家反馈，质量对标 GPT-6 Sol，**快 14 倍以上、成本约 1/200**；Copilot 团队用于回答质量评分，对标 GPT-5.6 Luna，**快 100 倍**；Microsoft Discovery 的自适应重规划中，打分一致性是 LLM 打分的 **46 倍**、速度快 3 倍，端到端重规划快近 4 倍
- 微软自己写的动机：一次决策加 100ms，20 步串行流程就是 **2 秒纯等待**

🟡 **一处必须点出的口径冲突**：官方博客原文写的是"**2.5 times quicker than H2O-Lightning-4B v1.1, the runner-up**，以及 35 倍于 GPT-6 Sol"；而多家二手转述（dev.to 日报、腾讯新闻、BigGo）写的是"**比次快的 Quyet-1.0-Large 快 4.5 倍**，35 倍于 GPT-6 Sol"。官方帖带有编者注"本帖已更新，补充了 Jev 的准确率与校准基准"。**连"次快是谁、快几倍"都对不上，说明这个品类的速度基准还没有共同口径**——引用时以官方博客为准，且只能当作厂商自测。

来源：[Microsoft Command Line - Introducing Microsoft-Decision-1](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/)

### 2. 紫外线全天图：约三分之一天区是模型补的，且逐像素标了出来

🟢 Anthropic 研究页（10-08）：约翰霍普金斯大学天体物理学家、Anthropic 研究员 **Brice Ménard** 用 Claude Science 调度多个 agent，下载并交叉校准 GALEX（约 **38,000** 次观测、覆盖约 **2/3** 天空）、Swift、FIMS/SPEAR 等公开巡天数据，再用 inpainting 补齐从未被紫外观测的约 **1/3** 天区（含大部分银盘），并从 Gaia 估算 **1 亿+** 颗恒星的紫外贡献。

- 官方原文要点：**"Additional layers of the map label each pixel as 'measured' or 'predicted' and provide uncertainty estimates."**（附图层逐像素标注测得/预测，并给出不确定度）
- 验证方式：遮住已有观测的区域再让模型补，预测与实测**相差约 10%**
- 翻车处：Ménard 肉眼发现 GALEX 圆形观测足迹的残痕；Claude 在项目初期已列出该问题，**但地图仍通过了两轮由其他 agent 执行的审查而未被发现**；他指出后，Claude 追溯并修正了全部 38,000 条观测
- 迭代：终版历经**十多版**

> 注：官方研究页本次直连抓取未成功，上述数字与引语来自官方页检索片段，并与 The Decoder、CellCog 两家的独立转述逐项一致。

来源：[Anthropic - The missing map of the sky](https://www.anthropic.com/research/the-missing-map-of-the-sky) · [The Decoder](https://the-decoder.com/anthropics-claude-science-creates-the-first-complete-ultraviolet-map-of-the-sky/)

### 3. Agent Lightning v1.0：训练用的就是部署的那一份 harness

🟢 微软亚洲研究院官方博客（10-07）+ 仓库核实：**约 3,500 行**、**MIT** 许可、**18,630★**。核心是正式定义的 **Harnessed Agentic RL**——在 agent 与模型之间放一个 OpenAI 兼容的 LLM 代理，**现有 harness 代码一行不改**，只需把原本指向模型 API 的 endpoint 指到该代理，训练框架即可记录 prompt、response 与 logprob。

- 效果（官方）：SWE-smith + mini-SWE-agent + **Qwen3.5-9B**，SWE-bench Verified Pass@1 **41.8% → 56.4%（+14.6 个百分点）**，训练集约 **6,000** 条样本，无需大规模算力
- **Collocated Async RL**：rollout 与模型更新共用同一批 GPU，端到端约为同步 RL 的 **2 倍**，且比常规异步 RL 用更少的卡
- Agent 以**标准 Kubernetes Job** 运行，不依赖 Modal Sandbox / E2B 等付费沙箱
- 官方列出的四个坑：**retokenization 与样本合并**（文本过 tokenizer 后 token 边界漂移，相邻调用无法合并）、**advantage 计算**（子 agent 与上下文摘要会把一次 rollout 切成多份，样本级计算会重复计数）、**loss 归一化**（按样本数平均会让"切得多"的 rollout 权重虚高）、**后端调度**（样本数与长度要等 harness 跑完才知道，却要映射到固定的 GPU 与并行配置）

来源：[Microsoft Research - Agent Lightning v1.0](https://www.microsoft.com/en-us/research/blog/agent-lightning-v1-0-a-3500-line-lightweight-agentic-rl-framework-for-training-agents-with-real-harnesses/) · [github.com/microsoft/agent-lightning](https://github.com/microsoft/agent-lightning)

### 4. 反向标注：两家把「这不是人核过的」直接写进了产品说明

🟢 **Anthropic OSS Scanner**（10-08）：面向开源项目的**免费、opt-in** 漏洞扫描，由最强模型（含 Claude Mythos）执行，**输出完全由模型生成、无人复核与分诊**。官方披露：6 个月内识别 **29,000+** 候选漏洞，**人工只复核了约 6,000 条**，已共享近 5,000 条未验证报告给主动索取报告的维护者；验证环节请渗透测试员复核 **48 个项目、97 条 critical/high**，其中 **85 条（88%）** 达到协调披露标准，剩余 12 条中 11 条是重复、**仅 1 条是真误报**。不设 90 天披露期（因为可能有误报）。维护者需提交 PR 加 `project.yaml`（仓库地址 + 联系邮箱 + Dockerfile，审计须能离线完成）。
官方自陈瓶颈原话："**We remain bottlenecked on our human capacity to validate these findings.**"

🟡 **Hugging Face Carbon-A**（10-08）：1.2B 参数，从 DNA 直接预测蛋白编码区，上下文 **98,304** bp；扫过 GenBank 公开组装建成 Carbon Annotation Database：**48,167** 个组装、**22,617** 个类群、**5.66 亿**个预测位点；42 个基准基因组 macro 平均核苷酸 F1 **0.944**。HF 明确两点：这些是 **"gene candidates"** 而非确认基因；与 ActiveSite / UCSD 的实验"**do not yet establish that those RNAs are translated into proteins**"。（二级转述 HF 官方博客，未直连核实。）

来源：[The Hacker News - Anthropic Launches Free AI Vulnerability Scanner](https://thehackernews.com/2026/10/anthropic-launches-free-ai.html) · [Security Affairs](https://securityaffairs.com/200685/ai/claude-helps-secure-open-source-as-anthropic-offers-free-vulnerability-scanning.html) · [TSNMedia - Two Open Models From 8 October](https://tsnmedia.org/open-models-jetbrains-mellum2-1-hugging-face-carbon-a)

### 5. vLLM v0.31.0：连缓存键都要标出处

🟢 GitHub release（10-05，**717 commits / 307 contributors**）。与今天主线直接相关的两处：

- **缓存键按来源打 tag**（#51899）：prefix cache 的 extra keys 现在按来源标记，**LoRA 名与 `cache_salt` 不再碰撞**；#59335 把 LoRA 路径纳入 block hash。**以前两个不同来源的缓存可能命中同一个块——这是"出处"问题最工程化的一例。**
- **Fast Restart**（#56680）：新增 `vllm preload` CLI 启动权重缓存守护进程，让**量化后的权重跨引擎重启常驻 GPU 显存**，并已支持数据并行、MTP draft 模型、`/health` 端点与就绪等待；另有基于 CRIU 的初始化引擎快照（实验性）
- 破坏性变更（升级前必读）：per-request `mm_processor_kwargs` / `media_io_kwargs` 需 `--trust-request-mm-kwargs` 才生效；**`tokenizer_mode="slow"` 已移除**；`--enable-mamba-fine-grained-prefix-cache` 更名；`quantization="fp8"` 改为 `fp8_per_tensor` 简写；AllSpark INT8 W8A16 后端移除

来源：[github.com/vllm-project/vllm/releases/tag/v0.31.0](https://github.com/vllm-project/vllm/releases/tag/v0.31.0)

### 6. 国产侧：Token 成了计量单位，也成了抵押物

🟡 **中国信通院《面向词元（Token）服务的智算基础设施发展研究报告（2026年）》**（10-09 发布，第十六届智慧城市与智能经济博览会）：推理算力**首次超越训练算力**成为需求主体；引 TrendForce 数据称 2026 年北美五大云厂商 AI 训练算力年增 **56%+**、推理算力年增约 **122%**；提出"**Token 工厂**"——核心效益指标从总算力、上架率转向**每瓦 Token 产出、单位 Token 成本、服务 SLA**；商业模式从"卖硬件→卖服务→卖价值"三级跃迁（TaaS / AaaS / RaaS）。地方配套：北京经开区"词元十条"按算力租赁费 **30%** 补贴、最高 **2,000 万元**。（转述官方报告，未直连信通院原文。）

🟢 **广东汕头全国首个"词元出海贷"**（中国金融新闻网 10-09）：人民银行汕头市分行联合汕头市财政局、华侨试验区推动中行汕头分行落地，**首笔 100 万元**专项授信。风控从"看资产"转为"看词元"——把营业收入、词元采购量、算力服务合约价值、海外订单流水、跨境应收账款纳入授信评估；设"词元供给贷/应用贷/服务贷/个人贷"四个子方案。

🟡 **openJiuwen 发布并开源企业级 AgentOS**（10-08/09，华为 2012 实验室 + 华为云等联合）：GitHub 与 AtomGit 同步，**Apache-2.0**；四个组件（分布式 agent runtime、jiuwenswarm 工作与编码 agent、Conch 沙箱、agent 接入网关）；蜂群协同 + 执行轨迹自演进 + 多租户隔离 + 故障恢复；插件化，技能/连接器/插件/专家/专家团五类资产经 Agentic Hub 分发；支持 openEuler / Ubuntu；HC2026 上一体机方案称可**小时级**完成端到端私有化部署。（Pandaily + 量子位转述，仓库直连未成功。）

来源：[C114 - 中国信通院 Token 工厂报告](https://m.c114.com.cn/w16-1318875.html) · [中国金融新闻网 - 词元出海贷](https://www.financialnews.com.cn/2026-10/09/content_458394.html) · [Pandaily - openJiuwen AgentOS](https://pandaily.com/openjiuwen-open-source-enterprise-agentos-swarm-sandbox-multi-tenant-appliance)

---

## 三、为什么值得记

1. **「可下钻」正在从加分项变成及格线。** 天图标到像素、Dashboard 标到 query、Google Cloud 给 Gemini agent 的审计轨迹**归因给 agent 而不是人**（官方原话：identity "is stamped into the logs that capture its work"）。三家做的都是同一件事：让下游有能力追问"这个数从哪来"。推论很硬——**以后凡是 AI 产出的数字，不能下钻到来源的那个就是次品**，不管它看起来多漂亮。

2. **贴标签防的是混淆，防不住污染。** 今天最该记住的一条是负面证据：GALEX 的圆形残痕是**仪器伪影，不是模型错误**；它在项目初期就被列入问题清单，仍然通过了**两轮**由其他 agent 执行的审查。这说明两件事：一，数据质量问题的最终检验目前还得靠人的肉眼；二，**"再加一轮 AI 审查"基本不增加保障**——审查者和生产者共享同一套表示与盲区。想真正加一层，得换模态（人看）、换数据源（独立观测），不是换一个 agent。

3. **「这个数在什么条件下还成立」第一次被写成了产品规格。** 10-09 那篇问的是"同一个判断会得到几个数字"，今天微软把答案做成了卖点：8 种扰动、1.3% 翻转、选项顺序 0 翻转。这是品类成熟的好信号。**但要同时看到坏信号**：官方博客与多家二手转述连"次快是谁、快几倍"都对不上（H2O-Lightning-4B v1.1 @2.5× vs Quyet-1.0-Large @4.5×），说明这张榜还没有共同口径。**先自己跑一遍扰动回归，再看厂商数字。**

4. **训练与部署共用一份代码，是「可追溯」缺的最后一块。** 此前你能追溯数据出处、能追溯查询出处，但追溯不了"这个策略到底是在哪个 agent 上训出来的"——因为训练框架里的那份 agent 是重写的。Agent Lightning 把代理插在中间，让 **+14.6 分这个提升量落在你真正会部署的那个 agent 身上**。代价是四个明确的工程坑，且微软把它们逐条写出来了——**愿意写清楚坑的开源项目，通常比只给一个分数的可信。**

---

## 四、可行动

- [ ] **给所有 AI 产出的字段加 `source` 枚举：`retrieved` / `generated` / `inferred`，不确定度单独存一列。** 参照天图的做法——它标的是**每个像素**而不是整张图。粗到"整份报告标一次"等于没标。
- [ ] **用 Agent Lightning v1.0 把现有 agent 接进 RL，只改 endpoint 不写代码。** 把 harness 的模型地址指向它的 OpenAI 兼容代理即可；先用 SWE-smith + mini-SWE-agent + Qwen3.5-9B 复现 41.8% → 56.4%。四个坑里最先咬人的通常是 **retokenization**（harness 存的是文本，重过 tokenizer 后边界漂移，相邻调用合并失败），接之前先确认你的 harness 是否暴露 logprob。
- [ ] **给决策类调用加"扰动回归"：打乱选项顺序、改写 prompt、加无害格式噪声，测结论翻转率。** 微软自测基线是 1.3%（选项改写/逆序/打乱 0 次）。**注意别拿厂商数字直接比**——官方与二手的速度对比对象都不一致。
- [ ] **升 vLLM v0.31.0 前先过一遍 breaking changes**：`tokenizer_mode="slow"` 已移除；`quantization="fp8"` 改 `fp8_per_tensor`；per-request 多模态 kwargs 现在要 `--trust-request-mm-kwargs`。**如果你之前靠 `cache_salt` 做多租户隔离，升级后行为会变**（extra key 现在按来源打 tag，LoRA 名不再与之碰撞）。顺手测一下 `vllm preload`，它能把百 GB 权重的冷启动从"每次都拉"变成常驻显存。
- [ ] **给"AI 生成但无人复核"的输入建 triage 流程，而不是拒收。** OSS Scanner 的 88% 达标率意味着**每 100 条高危报告里有约 12 条需要你判断**（11 条重复、1 条误报）。成本不在"收到"，在"判断"。维护开源项目的话可以现在申请加入（PR 加 `project.yaml` + 能离线构建的 Dockerfile）。
- [ ] **对高风险产物保留一次人工目视检查，别用"多跑一轮 agent 审查"替代。** 天图的教训足够具体：两轮都没抓到的，是人在屏幕上看到的。

---

## 五、术语卡

| 术语 | 解释 | 今天为什么重要 |
| :--- | :--- | :--- |
| **Inpainting（图像/数据补全）** | 用已观测部分学到的统计关系，去推算从未观测区域的值。天图里学的是"紫外亮度 ↔ 可见光/红外/射电亮度"的关系，再补到没被紫外观测过的天区。 | 约 1/3 天区是这样来的。它本身不是问题，**不标出来才是**。 |
| **测得 / 预测 标注（measured vs predicted）** | 在产物里为每个最小单元标注它是直接观测得到的，还是模型推算出来的，并附不确定度。与"置信度"的区别：置信度说"我对这个值多确信"，出处标注说"这个值是不是测出来的"。 | Anthropic 把它做成了天图的附加图层；Claude Dashboards 用"可点开看 query + 最后刷新时间"实现了同一件事的商业版。 |
| **扰动翻转率（perturbation flip rate）** | 对同一请求施加等价改写（换措辞、改选项描述、重排选项、改 key、加无害格式噪声）后，模型给出不同结论的比例。 | Microsoft-Decision-1 首次把它当主打指标：8 种扰动下 1.3%，选项改写/逆序/打乱 0 次。**这是"同一个判断会得到几个数字"的可交付版本。** |
| **Harnessed Agentic RL / Agent Harness** | Harness 是模型之外的那层软件，负责工具、上下文、执行与控制流。传统 agentic RL 要在训练框架里把 agent 重写一遍，训出来的和部署的不是同一个。Harnessed Agentic RL 让**部署用的那份 harness 直接参与训练**。 | Agent Lightning v1.0 正式定义并开源（MIT，约 3,500 行）。+14.6 分的可信度来自"训的就是部署的那个"。 |
| **Token 工厂 / 每瓦 Token 产出** | 信通院报告里的新形态定义：以 Token 为统一计量单元，把电力与算力转化为标准化 Token 输出并按量计费。效益指标从"有多少卡"换成"每瓦产多少 Token"。 | 国产侧把 Token 从技术指标变成了**计量单位、计费单位，乃至授信依据**（汕头词元出海贷把词元采购量写进风控模型）。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
