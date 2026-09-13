# 2026-09-13｜中间层：一边被穿透，一边被重建

> AI 的信用不全在模型里，而在它穿过的那些中间层——这周它们被穿透，也在被重建。

**标签**：`#蒸馏` `#AI治理` `#垂直化` `#开源` `#工程实践`
**生成时间**：2026-09-13 12:00（北京时间）

---

## 一、今日观察

**主线：这周最值得记的不是任何一次模型发布，而是「中间层」同时发生的两件相反的事。**

过去两年我们习惯把 AI 的竞争力理解为模型本身的能力。但 9 月 8 日到 9 月 12 日这五天里，真正被争夺的是**模型之外的那些层**：API 访问与账号体系、学术规范、数据源授权、推理过程的可观测性。

一边是穿透：**Anthropic 说有人用 1.51 亿次对话把 Claude 的推理链抽走**；**25 位菲尔兹奖得主说 AI 公司把"解题"从"理解"里剥离出来单独变现**。两条攻击路径结构一样——绕过流程，直接取走最有价值的那层。

另一边是重建：**OpenAI 的金融版 ChatGPT 卖的不是模型，是 citation、数据授权和企业模板**；Anthropic 把"反蒸馏"写进了模型架构（强制先总结推理、preserved thinking）。

| 中间层 | 本周发生了什么 | 关键证据 |
| :-- | :-- | :-- |
| API 访问 / 账号体系 | **被穿透** | 阿里相关行动 5–7 月 **1.51 亿次**交互、峰值近 **300 万次/天**、来自 **3,500+** 个欺诈账号 |
| 学术规范（论文 / 同行评议 / 引用） | **被穿透** | 25 位菲尔兹奖得主联署：解题只是"概念理解"的**代理指标**，匆忙发布正在摧毁传承链 |
| 数据源授权与引用 | **被重建** | 金融版 ChatGPT 把每个数字**溯源到源表**，并做 entitlement 集成 |
| 模型推理过程 | **被加固** | Anthropic 让 Claude 先总结推理再回答，Fable 5.1 引入 preserved thinking |
| 用户会话路由 | 被暴露为**新风险面** | 用户以为在问 Kimi，请求却被中继给 Claude，附带的还有企业数据、凭据 |

一句话：**AI 竞争正在从"能不能做到"转向"凭什么算你的、能不能证明、能不能拿出去用"。** 前两篇笔记讲的是验证（9-05）和审计（9-12），今天这一层再往上一步——**归属与授权**。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Anthropic 9 月威胁情报报告：点名 7 家中国实验室的"工业级蒸馏"

Anthropic 于 **9 月 10 日**发布《Detecting and Countering Misuse of AI: September 2026》，覆盖 2025 年 12 月至 2026 年 8 月处置的七类滥用。蒸馏章节点名 **7 家中国实验室**：阿里巴巴、Moonshot AI、DeepSeek、智谱（Z.ai）、小米、商汤、MiniMax。

其中被 Anthropic 称为"**我们测量过的最大规模蒸馏攻击**"指向阿里：**5–7 月期间超过 1.51 亿次交互**，峰值近 **300 万次/天**，来自 **3,500+ 个欺诈账号**；手法是在每个请求注入固定提示，迫使 Claude 把思维链写在行内标签里，再转成 SFT 数据用于训练 Qwen 3.5 / 3.6 / 3.7。

更值得工程侧注意的是**中继（relay）问题**：Moonshot 在 10 天内把约 **30 万条真实客户请求**转给 Claude（用户以为在用 Kimi），DeepSeek 在 7 月 14 天内产生 **1,210 万次**交互；被中继的内容里据称包含俄罗斯政府数据库凭据、成都数百路摄像头监控数据等。

- 🟡 **归因部分待核实**：这是 Anthropic 单方面调查结论，**未披露归因的技术依据**，报道时阿里亦未公开回应。数字是 Anthropic 的观测值，不等于独立验证。
- 🟡 **口径冲突**：智谱的规模，两家媒体给出 **77 万次/10 天**（most.tw）与 **340 万次/17 天**（DataQuest）两个不同数字，官方报告口径待核，此处不做定论。
- 来源：[CNBC TV18](https://www.cnbctv18.com/technology/chinas-alibaba-ran-the-largest-ai-brain-theft-operation-ever-recorded-anthropic-report-19989124.htm) ｜ [DataQuest（含分实验室数据图）](https://www.dqindia.com/cybersecurity/ai-shifts-from-assistant-to-orchestrator-in-anthropic-report-12520326) ｜ [InsiderFinance](https://www.insiderfinance.io/news/anthropic-claude-misuse-tied-to-russia-and-china) ｜ [most.tw（中文整理）](https://most.tw/posts/ainews/anthropic-distillation-report-2026)

### 2. 🟢 美三机构联合公告 AA26-251A + 中方官方回应（9-08 / 9-09）

美东时间 **9 月 8 日**，NSA、CISA、FBI 联合发布编号 **AA26-251A** 的网络安全公告，点名 DeepSeek、月之暗面、阿里巴巴、MiniMax、阶跃星辰、智谱 6 家中国 AI 企业，指控其"工业规模蒸馏"美国前沿模型，并向美企提出三项防御建议：异常检测、对疑似恶意蒸馏请求"悄悄改变响应"、建立跨组织情报共享。

**9 月 9 日**，中国商务部新闻发言人答记者问，原文措辞为美方指控"**于事无凭，于法无据**"，认为蒸馏是"业内正常的技术和商业问题"，被政治化、工具化；外交部发言人毛宁同日作出回应。

- 这条的价值不在站队，而在**定性迁移**：复旦大学中国研究院刘典指出，美方此举把蒸馏从"企业间知识产权与服务条款争议"提升到了**国家安全与地缘科技竞争**层面。
- 来源：[中华人民共和国商务部官网（原文）](https://www.mofcom.gov.cn/syxwfb/art/2026/art_1d982b77535347f1bdebc1e5f59a9b4e.html) ｜ [环球时报 / 腾讯新闻](https://news.qq.com/rain/a/20260910A02PWG00) ｜ [俄罗斯卫星通讯社](https://sputniknews.cn/20260911/1073201244.html)

### 3. 🟢 25 位菲尔兹奖得主联署：《A Severe Misalignment of AI in Mathematics》（9-11）

**9 月 11 日**，陶哲轩在其博客发布联合声明，25 位在世菲尔兹奖得主署名，横跨 **1978 年（Pierre Deligne）到 2026 年（邓煜）**近半个世纪，并上线独立站点 [mathandai.org](https://mathandai.org/) 继续开放联署。署名者包括 Bhargava、Scholze、Viazovska、Kontsevich、Villani、Maynard、Hairer、Figalli 等。

声明最锋利的一句（官网原文）：

> "Solving problems is only a tool and proxy for achieving the primary goal of **conceptual understanding and insight**."

它**不反对** AI 做数学——明确承认 LLM 数学能力"近几个月大幅提升"。它反对的是发布方式：成果被匆忙公布，来不及写成论文、来不及提炼新方法、来不及厘清是否借鉴他人未发表工作，从而引发**署名与抄袭争议**；而没有愿意接手的数学家把这些想法"养大"，AI 产出的想法永远不会真正进入数学正典。

- 导火索是 **9 月 8 日 OpenAI 宣称约 1 万个并发 Agent、运行约 88 小时**（其间交换 270 万条消息、约 1,300 亿输出 token）给出纳维-斯托克斯方程存在性与光滑性的解答，随后 NYU 数学家 Tristan Buckmaster 提出优先权质疑。**克雷数学研究所目前仍将该问题列为"未解决"**。
- 🟡 Buckmaster 转述的"你为什么要毁掉自己的职业生涯"等细节出自其单方陈述，OpenAI 已否认，此处不作定论。
- 来源：[mathandai.org 声明全文（官方）](https://mathandai.org/) ｜ [陶哲轩博客](https://terrytao.wordpress.com/2026/09/11/a-severe-misalignment-of-ai-in-mathematics/) ｜ [Economic Times](https://m.economictimes.com/news/new-updates/mathematicians-vs-ai-war-erupts-why-top-maths-medal-winners-are-angry-with-openai-and-other-ai-companies/articleshow/134114469.cms) ｜ [腾讯新闻](https://news.qq.com/rain/a/20260912A07C7A00)

### 4. 🟢 OpenAI 上线 ChatGPT for Financial Services：卖的是 citation，不是模型（9-10）

**9 月 10 日** OpenAI 推出面向金融服务业的 ChatGPT Work 版本，由 **Morgan Stanley 与 Evercore 担任设计伙伴**，底层为 GPT-6 Astra。内置数据方包括 **Daloopa、PitchBook、LSEG News、Crunchbase、Quartr** 等，覆盖财报电话会逐字稿、财务报表、公司基本面与私募市场信息；数据在 OpenAI 自有基础设施上建索引以提升检索与引用能力。

真正值得抄的三处设计（均见官方页）：

- **可溯源**：用户可把数字与结论**追溯到底层源表的具体表格与段落**；
- **entitlement 集成**：与 S&P Capital IQ、LSEG、MSCI、Dow Jones Factiva、Moody's 做共享登录与授权打通，用户凭 ChatGPT 登录即可访问**其机构已订阅**的数据；
- **企业模板下发**：管理员可发布 Excel / Word / PowerPoint 模板，让输出直接落在公司自己的格式与风格里。

合规侧：SAML SSO、SCIM、RBAC、加密、可配置留存期，合规团队可导出 workspace 日志进入审计流程。另有 **50+ 个 MCP connector**（Datasite、Box、Preqin、FactSet、Intapp 等）。

- 来源：[Introducing ChatGPT for Financial Services（OpenAI 官方）](https://openai.com/index/introducing-chatgpt-financial-services/) ｜ [Reuters / The Star](https://www.thestar.com.my/tech/tech-news/2026/09/11/openai-launches-chatgpt-for-financial-services-industry)

### 5. 🟢 小米开源 Xiaomi-CocktailASR-1：把"鸡尾酒会难题"做到可用（9-11）

**9 月 11 日**，小米开源工业级目标说话人语音识别模型 **Xiaomi-CocktailASR-1**（Apache 2.0）。思路不是传统的盲源分离+降噪，而是**先给一段参考音频做声纹提示，只转录目标说话人**——把混合音频任务改写成目标说话人识别。

架构为端到端 LLM：**D2V2 音频编码器 + Adapter + LLM 解码器**，全部权重合并在单个 checkpoint；输入是"参考音频 + 1 秒静音 + 目标音频"拼接。

官方仓库给出的自评 WER（↓ 越低越好）：

| 测试集 | CocktailASR-1 | Qwen3-ASR | Gemini | StepAudio |
| :-- | :-- | :-- | :-- | :-- |
| LibriMix 2mix | **4.11** | 68.75 | 48.41 | 71.23 |
| LibriMix 3mix | **12.29** | 106.04 | 76.10 | 121.08 |
| AMI SDM（真实会议） | **21.81** | 38.18 | 52.95 | 110.50 |
| AliMeeting Far（真实会议） | **20.63** | 39.64 | 56.75 | 76.82 |

另两个工程特性很实用：**负样本拒识**（目标不在场时输出空文本，LibriSpeech neg 拒识率 **79.59%**），可显著降低智能音箱/车机的误触发；**CoT 模式**（`<think>`/`<answer>` 标签输出推理过程），WER 仅微降 0.24，主要为可解释性与调试服务。技术报告见 [arXiv:2609.11274](https://arxiv.org/abs/2609.11274)。

- 注：以上为作者自评数据，未见第三方复现。
- 来源：[GitHub 仓库（含完整评测表）](https://github.com/xiaomi-research/xiaomi-cocktailasr-1) ｜ [HF 权重 Ease3/Xiaomi-CocktailASR-1](https://huggingface.co/Ease3/Xiaomi-CocktailASR-1) ｜ [AIBase 中文报道](https://news.aibase.com/zh/news/31001)

### 6. 🟢 火山引擎 OpenViking：把 Agent 的 Memory / RAG / Skills 收敛成一个上下文数据库

火山引擎（volcengine）开源的 **OpenViking** 定位为 "Self-evolving Context Database for AI Agents"，把目前分散实现的三层收敛到一个底座：**Agent Memory（跨会话记忆）、Knowledge RAG（知识检索）、Skills（可调用技能）**。许可证为 **AGPL-3.0**（由 Apache-2.0 变更而来）。

几个可直接借鉴的设计：

- **Peer 命名空间**：记忆写入的隔离单元，默认由 git 派生（`{git_remote}` / `{git_root}` 模板），也支持 `cwd` 或 `OPENVIKING_PEER_ID`；无仓库目录回退到用户级空间；
- **viking:// URI**：资源与记忆用统一 URI 标识；
- **find / search / recall 三档检索接口**，`recall` 支持类型配额与 `max_chars` 预算控制；
- **MCP 侧把约束写进 schema**：`max_tokens` 64–32000、`dedup_turns` 0–100、`exclude_uris` 最长 200（超限静默截断会导致排除失效——这是个很实在的坑）；
- Harness 已支持 Claude Code、Codex、Cursor、TRAE、opencode 等。

对做长周期、跨天任务型 Agent 的团队，这是"记忆/知识独立成基础设施层"这条路线目前最完整的一个开源样本。

- 来源：[GitHub: volcengine/OpenViking](https://github.com/volcengine/OpenViking) ｜ [AI 技术日报 2026-09-12](https://www.cnblogs.com/itech/p/22944375)

---

## 三、为什么值得记

1. **"蒸馏"这个中性词，在 72 小时内被三套话术重新命名。** 美方安全机构叫它国家安全威胁，Anthropic 叫它 illicit distillation，中方叫它正常技术被政治化。技术没变，**变的是它被放进哪个制度框架里定价**。做技术选型时，"我用某家 API 产出的数据训练了自己的小模型"这句话的合规性，已经不再由服务条款单独决定。

2. **菲尔兹奖得主们其实在说一件所有知识工作者都该听的事：当产出可以被批量制造，"过程"才是稀缺品。** 声明里那句"解题只是工具与代理指标"可以直接平移到写代码、写研报、写方案——如果 Agent 能直接吐出结果，而没人再走一遍理解、简化、讲给别人的过程，那组织里真正流失的不是效率，是**传承链**。这也正好解释了为什么 OpenAI 金融版要把 citation 做成卖点：企业买的不是答案，是"能拿去给合规看"的那条链。

3. **中继（relay）是被低估的风险面，而且它不挑站队。** Anthropic 报告里最该让普通开发者警觉的不是 1.51 亿次交互，而是"**用户以为在问 A 模型，请求被转给了 B 模型**"——附带的还有企业数据、实时凭据、监控视频流。任何经过第三方路由/聚合层的调用，都新增了一个数据出境问题。这一条对国内用聚合 API 的团队同样成立，与你信不信 Anthropic 的归因无关。

4. **垂直化产品的护城河正在从"模型能力"移到"授权与溯源"。** 金融版 ChatGPT 真正难抄的不是 GPT-6 Astra，而是 LSEG / PitchBook / S&P 的 entitlement 集成和企业模板下发。反过来看国内机会：**谁手上有别人拿不到、又能被机器索引和引用的结构化数据，谁才有资格做垂类 Agent。** 光有模型没有数据源，最后只能做壳。

5. **一个容易被忽略的信号：可解释性正在从"加分项"变成"接口"。** CocktailASR-1 特意做了 CoT 模式（WER 几乎不涨），OpenViking 把检索预算和排除列表写进 MCP schema。这不是炫技，是**让人类/上层系统能插手中间步骤**——和上面"中间层"的主线是同一件事。

---

## 四、可行动

- [ ] **跑一遍 CocktailASR-1**：`pip install torch torchaudio transformers soundfile`，然后 `AutoModel.from_pretrained("Ease3/Xiaomi-CocktailASR-1", trust_remote_code=True, torch_dtype="bfloat16")`；拿自己一段多人会议录音（16k 单声道）测真实 WER，重点验证**负样本拒识**在你的场景里够不够（官方 LibriSpeech neg 是 79.59%，真实会议场景大概率更低）。
- [ ] **给自己的 Agent/RAG 输出加一层 citation**：参考金融版 ChatGPT 的做法——每个数字/结论必须能回溯到具体源文件的具体段落。先在你正在做的 RAG 链路里加一个"引用缺失就拒答"的开关，看命中率掉多少。
- [ ] **审计一次调用链路的路由层**：列出你所有经过第三方聚合/中转 API 的调用，确认请求体会不会被转发到你不知道的模型；企业数据、token、凭据是否在 payload 里。这项 30 分钟能做完，风险收益比最高。
- [ ] **评估 OpenViking 是否适合你的知识库**：重点看 `viking://` URI + Peer 命名空间能不能替代你现在的"向量库 + 手写记忆脚本"组合；注意 AGPL-3.0 对商业闭源集成的约束。如果只是个人知识库，先看 `find` / `recall` 的 budget 控制够不够用。
- [ ] **检查 Claude API 集成是否受新规影响**：Anthropic 已对可疑/特定地区账号启用强制身份验证，Fable 5.1 的 preserved thinking 会阻止新 API 账号改写推理前的上下文。如果你的应用依赖"改写 system prompt 或历史消息"这类技巧，需要重测。
- [ ] **读一遍 mathandai.org 的声明全文**：700 词左右，把它当成"当 AI 能直接产出结果时，组织如何保留理解链"的思考模板，套到你自己的团队流程上。

---

## 五、术语卡

| 术语 | 解释 |
| :-- | :-- |
| **知识蒸馏（Distillation）** | 用大模型（教师）的输出去训练小模型（学生）的技术。本身中性且合法，广泛用于压缩与加速。争议点在于：是否**违反服务条款**、是否通过**欺诈账号**绕过地域限制、是否抽取的是受保护的思维链而非普通输出。 |
| **思维链（Chain-of-Thought, CoT）** | 模型在给出最终答案前先输出中间推理步骤。它既是能力来源，也是**最值钱的训练数据**——这也是 Anthropic 报告里抽取目标的重点。反过来，CocktailASR-1 的 CoT 模式用于**可解释性**。 |
| **中继（Relay）** | 用户向 A 服务发请求，A 悄悄把请求转给 B 模型、再把 B 的回答当作自己的返回。本报告中最值得警惕的模式：用户的企业数据、凭据会随请求一起出境，而用户完全不知情。 |
| **WER（Word Error Rate）** | 字错率，语音识别的核心指标，越低越好。可超过 100%（插入/删除过多时）。对比 CocktailASR-1 的 4.11 与 Qwen3-ASR 的 68.75 时需注意：**这是混合音频场景**，不是普通单人识别。 |
| **Entitlement（数据授权）** | 用户/机构已订阅某数据服务的访问权。金融版 ChatGPT 的做法是与 S&P、LSEG 等做共享登录，让用户凭 ChatGPT 身份直接访问**机构已付费**的数据，避免重复采购与合规风险。 |
| **Preserved Thinking** | Anthropic 在 Fable 5.1 引入的机制：阻止新的 API 账号改写位于 Claude 推理之前的对话上下文——这是抽取思维链的常用手法。属于"把防御写进模型接口"而非仅靠封号。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
