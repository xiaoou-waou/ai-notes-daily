# 2026-10-29｜今天没有新模型上桌，四把"验收尺子"先量出了自己的问题

> 今天的主角不是模型，是"判断这活干完了没有"的那把尺子——它今天被证明比被量的活更不可靠。

**标签**：`#评测` `#Agent工程` `#交付` `#可信度`
**生成时间**：2026-10-29 12:20（北京时间）

---

## 一、今日观察

今天没有一个重量级模型发布。但四份互不相干的官方文件——Cognition 的基准、Artificial Analysis 的复跑、Ai2 的论文、Anthropic 一位招聘经理的个人博客——在 48 小时内指向同一层：**验收**。

更值钱的是它们之间的分工：前两份回答"模型到底错在哪"，后两份回答"谁有资格判定它做完了"。

先看干活那侧。Cognition 在 FrontierCode 2.0 里做了一件少见的诚实事：**主动把"越界/做多了"（scope）的评判标准放宽**，再来看失败分布。放宽之后，唯一大幅上升的失败原因是"没做完、没顾到"（thoroughness）：

| 阻断项类别 | FrontierCode 1.1 失败率 | FrontierCode 2.0 失败率 | 备注 |
|---|---|---|---|
| **Thoroughness**（该补的没补、该顾到的没顾到） | **11.7%** | **19.2%** | 阻断项总数 168 → **501**（3 倍） |
| Core behavior（核心行为就不对） | 9.5% | 14.9% | |
| Avoiding regressions | 1.3% | 3.3% | |
| **Scope**（做了不该做的、越界） | **9.0%** | **3.8%** | 2.0 **主动放宽**了 scope 标准后才测出来的 |

（失败率＝该类别中未通过的阻断检查占比，为 Opus 5.5 / Fable 5.1 / GPT-6.1 Sol / GPT-6 Astra 高推理档的均值，来源见下。）

结论值得抄：**今天最强的 coding 模型，主要失败模式不是"做多了"，是"漏了"**——而且这个结论是先把"做多了"这条罪名减刑之后才成立的。

再看验收那侧。四把尺子今天各自被戳了一次：

| 这把尺子 | 谁在什么时候证明它不稳 | 你手上能替换它的东西 |
|---|---|---|
| 代码基准的**版本号** | FrontierCode 1.1 → 2.0，**所有模型分数集体下滑**：Opus 5.5 54.6%→45.5%、GPT-6 Astra 53.3%→42.8%、Grok 4.7 47.6%→28.6%、Gemini 4 Argon 47.5%→26.3%、Cognition 自家 SWE-2 **50.0%→23.9%**、Kimi K3 44.2%→17.7% | 分数必须连着"基准版本 + 跑分方"一起引用 |
| **跑分方 / harness** | Artificial Analysis 独立复跑同一套 132 任务：Opus 5.5 **46.4%**，而 Cognition 官方报 **45.5%** | 差异可归因：Stirrup harness、每任务跑 **3 次**、**500 turn** 上限、**GPT-6 Luna (medium)** 当 rubric 判官 |
| **LLM 当判官** | Ai2《Old Ideas, Novel Problems》：把提示词里"评审认为其中一个想法更新颖"那句话删掉，同一批配对里 **≥52.6%（实测 55.8%）判定翻转**，成对准确率摆动 **超过 50 点**，偶尔跌破随机线 | 加给定答案的对照组、固定至少两种措辞再比 |
| **人类面试** | Anthropic 工程经理 Felix Rieseberg 本月**取消**了团队的编程题面试，并承认："我还没找到更好的办法" | 暂时改成看作品集里的小原型（taste / empathy / principled thinking） |
| （对照）把验收**前移**做成产品的 | Replit：PR 到达评审者之前，agent 已在隔离沙箱里把应用打开、按客户的方式点一遍，附上**截图和视频** | 评审动作从"读 diff"变成"看证据" |

一句话：**能力在往前跑，验收在被往前推，而夹在中间的"完工判定"今天被证明是整条链上最脆的一环。**

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Cognition 发布 FrontierCode 2.0：先给"做多了"减刑，再测出"漏了"才是主犯

**2026-10-27** 官方博客。20 多位顶尖开源开发者、**每任务投入 40 小时以上**，从自己维护的仓库出题，量的是"这份改动 maintainer 会不会真的合并"。

关键数据：

- **20+ 位 maintainer、每任务 >40 小时**；阻断项比 1.0 多 **43%**；题目覆盖仓库数多 **55%**；参考解平均修改文件数 **+67%**、代码行数 **+89%**、代码库规模 **+25%**。
- **80% 的任务里，官方参考解与上游真实 PR 不一致**（1.0 为 60%）——基准本身在给上游仓库挑错。
- 审计流水线上，**一个 agent 在某个上游项目里发现了真实安全漏洞**，人工复核后已报告给该仓库维护者。
- 八个模型的 1.1 → 2.0 对照见上文表格；官方自评："基准远未饱和，最好的模型也只有 **45%**"。
- 最锋利的一条：Cognition 明写"**写更多正确的代码不一定涨分**"，并把"推理档位越高分数反而越低"当作 benchmark 的特性而非 bug。

来源：[Cognition 官方博客 · FrontierCode 2.0](https://cognition.ai/blog/frontier-code-2.0)

### 2. 🟢 Artificial Analysis 独立复跑同一套题：榜首模型跑出两个不同的数

同一模型、同一 132 道题，**Cognition 官方 45.5% vs Artificial Analysis 46.4%**。差别全部来自可列举的执行配置：

- harness 是自家的 **Stirrup**（开源，`github.com/ArtificialAnalysis/Stirrup`），**每任务跑 3 次**取均值、**500 turn 上限**、后台命令可持续运行、任务等权平均；
- rubric 判官用 **GPT-6 Luna (medium)**；
- 触发零分的两种情形：**任一阻断检查失败**，或 **trajectory scanner 判定它在偷看答案**。

来源：[Artificial Analysis · FrontierCode 2.0](https://artificialanalysis.ai/evaluations/frontiercode-2-0)

### 3. 🟢 Ai2：让 LLM 判定"这个想法新不新"，改一句提示词就翻车

论文《Old Ideas, Novel Problems: The Instability of LLM-Based Novelty Evaluation》，arXiv:2610.02022，**v1 于 2026-10-01 提交、v3 于 2026-10-26 修订**（本周转热）。作者 Noy Sternlicht、Simra Shahid、Peter Jansen、Daniel S. Weld、Pao Siangliulue、Tom Hope。

摘要与正文原文可核的结论：

- 六位判官（GPT-5.1 / 5.2 / 5.4、Claude Sonnet 4.5 / Opus 4.5 / Opus 4.6）上，只告诉判官一句"评审认为 A 更新颖、B 不新颖"，就能让它对**超过一半的相同配对改变裁决**，成对准确率摆动**超过 50 个点**，**偶尔低于随机**。
- 对 GPT-5.4 而言，P3（带提示）→P4（删掉那句话）造成 **52.6 点**落差，两者在 **至少 52.6%、实际 55.8%** 的配对上给出不同裁决，P4 下准确率**跌破 50%**。
- **同一个改动，帮了这一个判官、害了另一个**——不存在"更安全的通用措辞"。
- **加文献检索、加推理预算基本没用**：带检索的 agentic 判官 **0.78 macro-F1、成本 10×**；两个为该任务专门打造的评测系统，都被论文自己的**最廉价 prompt baseline** 击败，且后者**最多便宜 32 倍**。
- 全部实验的 API 花费约 **$15,000**（2026 年公开价，含预研与废弃实验）。

⚠️ 部分中文/英文自媒体转述中的具体绝对值（如"GPT-5.4 从 93.5% 掉到 40.9%"、"0.854 vs 0.772 macro-F1"、"$2.59 vs $82.05"、样本池 154/145）我未能在 arXiv 正文与摘要中直接核到，**本条目不予引用**，只用上面这些有原文背书的数字。

来源：[arXiv:2610.02022 abs](https://arxiv.org/abs/2610.02022) ｜ [Ai2 官方博客（未能直连，转述版见 HF 博客页）](https://huggingface.co/blog/allenai/novelty-bench)

### 4. 🟢 Anthropic 一位工程经理取消编程题面试，并明说"还没找到替代品"

Felix Rieseberg（Claude.ai / Cowork / Claude Code Desktop 前工程负责人，Electron 联合维护者）**2026-10-27** 个人博客：

- 原句："**This month, I laid the traditional coding interview to rest.** As a hiring manager at Anthropic, I stopped asking candidates to do them."
- 理由："给你出一道 React 小题，已经跟考你手写汇编差不多没意义了——**Claude 现在这两样都比人强**。"并称"团队里最有产出的那批人，与这类考试的成绩无关"。
- 替代方案**没想好**："I haven't quite gotten there yet — but I'm scanning resumes and portfolios for **little prototypes that exhibit taste, empathy, and principled thinking**."
- 同一篇里给出一个可直接抄的样本：Anthropic 内部大家把 Claude Code 当 CLI 用成习惯了，最后是**两位入职不久的工程师 Anthony Morris 和 Alice Zhao 用一个周末做出可运行原型，约 8 天后首个公开版本上线**——Claude Code 的图形界面。

来源：[Felix Rieseberg 个人博客（一手）](https://felixrieseberg.com/hunger-beats-tenure-advice-for-junior-engineers/) ｜ [The Register 报道](https://www.theregister.com/ai-and-ml/2026/10/28/anthropic-engineer-declares-the-coding-interview-dead/5306115)

### 5. 🟢 Replit 把"验收"前移：非工程师也能提一个已经被测过的 PR

**2026-10-27** 官方博客《Anyone can now bring their ideas into the company codebase》，Cloud Agents 对现有仓库开放给全部 Pro & Enterprise 客户。

- 非工程角色（设计、客服、PM）用**自然语言**描述改动 → agent 找代码、在实时预览旁改 → 在隔离云沙箱里**打开应用、像真实客户一样点一遍**，失败就自己改了再测 → 最终 **PR/MR 上附带截图和运行视频**。
- **工程师保留控制权**：文档写明"开 PR 不等于合并或部署"；每条审阅意见可以被沉淀成团队给 agent 的书面指令（**skills**），但**每条更新都要工程师批准才生效**（该能力处早期访问阶段）。
- 厂商自报的内部数：workspace memory 让 **token 用量下降 51%**，一个常见数据任务从 **16 分钟降到 1 分钟**（Replit 自测，未见第三方核实）。

来源：[Replit 官方博客](https://replit.com/blog/anyone-can-bring-ideas-to-company-codebase)

### 6. 🟡 DeepSeek-V5 标识符出现在官方 harness 仓库（待官方源核实）

多家日报转述：10-27 晚有开发者在 DeepSeek 的 `deepseek-harness` 的 `provider.spec.ts` 中发现 `deepseek-v5`、`deepseek-v5-open`、`deepseek-v5-next` 三个标识符，与已有的 `deepseek-v4-pro` 并列，被视为新一代模型的发布前准备。

我未能直接打开该仓库文件核实，**此条仅作线索记录，不作为发布事实**。来源：[IT之家转述，2026-10-28](https://view.inews.qq.com/a/20261028A0A69M00)

---

## 三、为什么值得记

**1. "换了一版基准就暴跌"这类结论，要先问它改了哪些评分口径。**
Cognition 这次的说服力恰恰来自它**先动了自己的尺子**：明确把 scope 标准放松（失败率 9.0%→3.8%，相当于给"友好的越界"平反），thoroughness 才以 19.2% 站上第一。任何"新一代基准让模型集体掉分"的报道，第一件事是找出它松了哪一条、紧了哪一条——否则你看到的只是标准的位移，不是能力的位移。

**2. LLM-as-judge 已经铺到评测链的每个角落，而它是今天被证明最脆的一环。**
AA 用 GPT-6 Luna 打 rubric 分、ideation 系统用 LLM 判新颖性、无数团队用 LLM 给 harness 输出打分。Ai2 的数据说明这条替人之路的容错率比想象低得多：同一配对 **55.8% 翻转**、**偶尔低于随机**、**加检索加大推理预算都不救**、**专用评测系统打不过最简单的 prompt baseline 还贵 32 倍**。结论不是"别用 LLM 裁判"，而是**它必须被当成流水线里最不可信的组件来监控，而且要有对照组**。

**3. "多给推理预算"不是默认提分项。**
Cognition 把非单调性当作 benchmark 的特性来宣传，并给出实例：PostHog Android SDK 那道题，GPT-6 Astra 低推理档 **5/5 通过**、高推理档只有 **1/5**——因为它在高档位下删掉了一个属于 `posthog.api` 公开面的类。另一个方向上，thoroughness 的失败率随档位从 26.0% 降到 15.3%，仍是所有类别里最高的。**默认值应该逐档实测，而不是默认拉满。**

**4. 今天唯一动手改工程流程的，是 Replit，而不是任何一家做模型的。**
它卖的不是更强的代码生成，而是**把证据做进 PR**：先自测、再录像、最后交给人签字。当"写代码"的边际成本继续下降，稀缺的那一环就是"谁、凭什么、在什么证据上判定这活能合"。这个缺口今天被四份文件指出来了，但目前只有一家在做产品。

---

## 四、可行动

- [ ] **固定你的评测口径**：把自己的 agent 评测脚本里的 harness 名、每任务重跑次数、turn 上限、judge 模型写进 `eval_config.yaml` 并进 git；换任何一项就新开结果文件，绝不覆写旧数。（AA 与 Cognition 的 0.9 分之差，就是这四个变量的差。）
- [ ] **给 LLM-as-judge 加稳定栅**：同一批评分至少跑两种 prompt 措辞（关键变量是"是否透露标准答案倾向"这类元信息），混入 20–30 组已知答案的对照 pair；**翻转率超过 20% 就暂停用它做自动筛选**。（Ai2 实测对照条件下翻转 55.8%。）
- [ ] **在给 agent 的任务描述里显式写"穷尽"要求**：同类输入类型要一并支持、兄弟代码路径里同样的 bug 要一起修——thoroughness 是 FrontierCode 2.0 里唯一失败率上升且阻断项数量三倍增长的类别，而它恰恰是可以靠提示词补的。
- [ ] **别把 reasoning effort 当默认旋钮**：在自己最看重的一批任务上跑 low / medium / max 三档，看分数是否非单调；同时记 token 成本，做三档 × 分数 × 成本的对照表。
- [ ] **复刻"PR 之前先自证"**：在 CI 里加一步，让 agent 在提交前跑通关键路径并录制截图/视频，把链接写进 PR 描述，评审者不开分支也能验收；把所有重复出现的审阅意见沉淀成仓库里的 agent 指令文件，并由人批准后才生效。
- [ ] （团队）**如果还在用编程题面试，加一道"AI 写得很自信但有错"的代码仓挑错环节**——这是原博评论区里最高频的替代方案；注意这是社区建议，不是 Anthropic 官方口径，Rieseberg 本人明确说替代方案尚未成型。

---

## 五、术语卡

| 术语 | 一句话解释 | 为什么今天重要 |
|---|---|---|
| **Thoroughness 阻断项** | 评测里"没有被明确写出、但从业者理应想到"的完成度要求（如同类输入是否都支持、兄弟路径的同一个 bug 是否一起修） | FrontierCode 2.0 中数量 **168→501**、失败率 **11.7%→19.2%**，是唯一双升的主要类别 |
| **Blocking criteria（阻断式评分）** | 一票否决型检查：任一不过，整题直接记 0 分；通过者在 rubric 上按权重加权算分 | 决定了分数不等于"通过率"：同一个模型同一套题，用两种口径会读出两个不同的数 |
| **Eval harness（评测脚手架）** | 包裹模型之外的整套执行壳：工具、文件读写、turn 上限、重跑次数、后处理 | Cognition 官方 45.5% 与 AA 46.4% 的差额，全部来自 harness 差异（Stirrup / 3 次 / 500 turn / Luna judge） |
| **Novelty judge（新颖性判官）** | 用一个 LLM 判断另一个 LLM 提出的科研想法是否真的新颖，常见于自动化科研流水线 | Ai2 证明它对提示词措辞极度敏感：>50% 配对翻转、>50 点摆动，偶发低于随机 |
| **Skills（团队给 agent 的书面指令）** | 仓库里描述"本团队怎么写代码"的机器可读约定，agent 提交 PR 时须遵守 | Replit 让审阅意见自动沉淀成 skills，但每条更新需工程师批准后才生效——把"人的判断"固化成可版本化的资产 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
