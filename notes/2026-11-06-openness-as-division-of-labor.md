# 2026-11-06｜同一天三种"开放"，画的都是分工线

> 百度交出预训练起点，Kimi 接管运行时，OpenAI 发放准入资格——"开放"正在变成厂商与用户之间的一场分工谈判。

**标签**：`#开源` `#Agent` `#模型开放`
**生成时间**：2026-11-06 12:03（北京时间）

---

## 一、今日观察

过去 48 小时，"开放"这个词出现了三次，但三家公司交出来的东西完全不在同一层。把它们按**「厂商把哪段工作交给你、把哪段接过去自己做」**重新排一遍，会发现这不是三种慷慨程度，而是三种分工方案：

| 谁 | 交给你的 | 自己接管的 | 你省下的 | 你新增的负担 |
|---|---|---|---|---|
| **百度 ERNIE 5.5 Flash Base** | 预训练终点 checkpoint（未经中训练与后训练） | 33.5T tokens 的预训练 | 从零训练的天文成本 | 中训练、后训练、Agent 行为塑造全流程自己跑 |
| **Kimi Hosted Agents** | 业务定义与工具接入 | Harness 运行时（官方称自建需数月） | 数月基础设施搭建与持续运维 | 运行时绑定单一平台 |
| **OpenAI GPT-6 Cyber** | 一纸使用资格（Daybreak Red 审核） | 安全边界、蜜罐与审计 | 自建攻防能力评估 | SSO、MFA、API IP 白名单、被持续审计 |
| **OpenRUA uni-robot-agent** | 可复现 harness 与模块化消融接口 | 环境—模型交互的标准化 | 具身环境适配工程 | 可信评测没人替你做（官方自己列了榜单三大注水漏洞） |

这张表的分界线不在"开放多少"，而在**分工线画在哪一层**。百度把线画在预训练终点之后——官方博客原话是"开放预训练终点权重，让开发者能够在已有的通用能力之上，自行选择模型下一阶段的训练方向"，即把"训练成什么"这个分歧最大的决策交还给你。Kimi 把线画在 Harness 这一层，把 Agent 投产前最贵的那段工程（上下文管理、工具调用、权限控制、中断恢复）整个收走做成订阅。OpenAI 把线画在门口：模型能力定级 Critical，但访问对象收窄到通过 Daybreak Red 身份与组织安全审核的客户。

值得警惕的是表格外面的那句话：**分工线怎么画，厂商是单方面决定的**。百度判断你缺的是训练起点，Kimi 判断你缺的是运维时间，OpenAI 判断你缺的是资质——三家都没问过你，但每一家都重新定义了"开放"该长什么样。选型的第一步不是比较参数，是先想清楚自己缺的是哪一段。

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. OpenAI 发布 GPT-6 Cyber：能力定级 Critical，访问走审核制 🟢

北京时间 11 月 6 日，OpenAI 推出安全专精模型 GPT-6 Cyber。官方 System Card：在 Preparedness Framework 下定级 **Cybersecurity Critical**（前代 GPT-5.6 Cyber 为 High）；ExploitGym **48.5%**（前代 32.1%，相对提升 51%）；无源码 Web 漏洞发现率 **40.3%**（未做安全专项训练的 GPT-6 Astra 为 32.0%）；无任何安全指令时 **99.93%** 测试不越出授权范围（前代 94.49%），启用安全指令后 100%。实战成果（Reuters 转述官方数据）：Firefox 发现 **81 个**此前未知高危漏洞（Mozilla 已开始修复）；为 **948 个** Linux 内核漏洞写出可用 exploit，其中 **588 个**此前未知。访问仅向 Daybreak Red 审核客户开放（身份核验、SSO、MFA、API IP 白名单），后续数周扩大到全部获批客户。

- 官方 System Card：https://deploymentsafety.openai.com/gpt-6-cyber
- Reuters（经 CNA 转述）：https://channelnewsasia.com/business/openai-launches-gpt-6-cyber-critical-cybersecurity-rating-6528536

### 2. 百度开源文心 5.5 Flash Base：交出的是"预训练终点"，不是成品 🟢

11 月 5 日发布并开放权重：稀疏 MoE，总参数 **280B**、每 token 激活 **14B**，**33.5T tokens** 从零预训练，训练上下文 128K、微调与推理支持 1M。官方博客明确：本次权重是**预训练终点的 checkpoint，未经中训练与后训练**，"可作为领域适配、指令微调和强化学习研究的共同起点"；提供 FP8 与 BF16 两种权重，联合 vLLM、SGLang 提供生态支持。注意官方评测口径：对比对象全部是其他家的开源 Base 模型（鞭牛士指出多为上一代），"同尺寸 SOTA"应在这一前提下理解。

- 官方技术博客：https://ernie.baidu.com/zh/release/ernie-5-5-flash-base/
- Hugging Face（FP8）：https://huggingface.co/baidu/ERNIE-5.5-Flash-Base
- 鞭牛士（评测口径提醒）：https://www.bianews.com/news/details?id=248649

### 3. Kimi Hosted Agents：官方原话就是"Harness as a Service" 🟢

11 月 5 日，月之暗面发布托管智能体服务，官方新闻页标题即"Harness as a Service"：企业无需自建运行框架即可获得 **7×24 托管环境**，支持长程任务与多智能体协作；提供独立沙箱、网络访问权限控制、随时中止会话、执行留痕与审计导出；内置 **140+ Skills 与 30+ 插件**；官方称企业自建一套可靠 Harness 需投入数月并持续维护。入口 platform.kimi.com。首批 8 个金融 Agent 模板（投研建模、IPO 跟踪、持仓监控等）来自北京商报报道，标 🟡。

- 官方新闻页：https://www.kimi.com/news/kimi-hosted-agents
- 北京商报（模板数，🟡）：https://www.bbtnews.com.cn/2026/1105/610467.shtml

### 4. 清华×伯克利 OpenRUA 开源 uni-robot-agent：同一模型，harness 决定从 0 到 31.39 🟢

11 月 3 日，OpenRUA 项目（清华大学与 UC Berkeley 团队，28 位作者，含 Pieter Abbeel、刘知远等）发布统一具身智能体框架 uni-robot-agent（arXiv 2611.01560，GitHub Open-RUA/uni-robot-agent）。官方页核心数据：RoboDojo 基准上 **Qwen3.5 至 3.7 Flash 全部 0.00 分，Qwen3.8 Flash 达 31.39 分**——不改权重，能力随 harness 与模型代际涌现。⚠️ 媒体标题"零样本 Qwen 跑赢 GPT-6 Astra（28.97）"需谨慎：AI 邮报指出这是**跨框架的旧基线对比，同一框架下 GPT-6 Astra 分数仍更高**，不能读成全面超越。

- 官方项目页：https://openrua.ai/uni-robot-agent
- 论文：https://arxiv.org/abs/2611.01560
- 修正性分析（🟡）：https://www.aiposthub.com/openrua-uni-robot-agent-unified-harness-open-models

### 5. OpenRUA 同期发文：机器人 Agent 榜单有三大注水漏洞 🟢

11 月 2 日，OpenRUA 发布《Revisiting RUA》，指出具身智能体榜单分数虚高的三个来源：**不公平的执行预算**、**执行中向 Agent 泄漏特权任务进度**、**评测前把测试任务的解法内建进 Agent**，并提出封堵协议。这套审计问题不限于机器人领域。

- 官方页：https://openrua.ai/revisiting-rua

### 6. 一批 Agent/基础设施融资落地 🟡

Fal（AI 推理云）11-3 融 **13 亿美元**、估值 160 亿（Bessemer 领投、Nvidia 参投，据报年化收入 8 亿美元）；Applied Compute 11-2 融 **3.5 亿美元**、估值 32.5 亿（自报年化收入 1 亿）；Traversal（AI SRE，查故障根因的 Agent）11-3 融 **1.2 亿美元**、估值 10 亿，自报单季 **15 万次**故障调查；Sand AI（视频生成）11-5 宣成 **2 亿美元** A+，年内第三轮、10 个月累计 3 亿美元，跻身独角兽。均为公司自报口径经媒体转述。

- 汇总源：https://infotechlead.com/tech/vc-funding-deals-fal-applied-compute-traversal-powerup-money-99424
- Sand AI（科创板日报经网易转述）：https://www.163.com/dy/article/LB0R2KJG0550B1DU.html

## 三、为什么值得记

1. **Base 权重正在成为新的开源姿势，而且这个选择是被成本结构逼出来的。** 33.5T tokens 的预训练没人重复得起，但 Agent 时代每家要的后训练方向（代码、客服、投研）差异太大——厂商干脆把"训练成什么"整个交出去，只保留预训练这一段。开放的粒度不再由慷慨程度决定，由后训练的不可复用性决定。
2. **Harness as a Service 意味着竞争从模型 API 下沉到了运行时。** 继 11-05 观察到"Agent 战场挪到外壳与信任层"之后，Kimi 把这句话产品化了：外壳开始单独收门票。代价是绑定方式变了——以前锁定你的是模型质量，以后锁定你的是环境与 Skills 生态。迁移成本要按"换运行时"来估，不是按"换模型"。
3. **GPT-6 Cyber 展示了一条反向曲线：能力越强的开放，开放面越窄。** Critical 定级 + 审核制访问 + 组织安全要求，本质是用"准入"替代"阉割"——不削弱模型，只筛人。可以预期这套模式（能力全量、访问收窄）会被更多高能力模型复制，"能不能用到"会越来越像"有没有资质"的问题。
4. **Revisiting RUA 的三个漏洞是通用审计清单。** 任何 Agent 榜单都值得问三句：执行预算公平吗？执行中有没有向 Agent 泄漏特权信息？测试任务的解法是不是提前内建了？这三问在代码 Agent、Web Agent 榜单上同样适用——尤其是媒体转述"开源小模型跑赢闭源旗舰"时，先检查是不是跨框架对比。

## 四、可行动

- [ ] 下载 ERNIE-5.5-Flash-Base（HF 有 FP8/BF16），按 vLLM/SGLang cookbook 起一次推理；再用自己领域的一小批数据做一次小规模 SFT，实测"起点 + 自己后训练"与直接调 API 的差距，再决定要不要走自训路线。
- [ ] 把一条现有自建 Agent 工作流迁到 Kimi Hosted Agents 试用环境跑通，记录两边投入：自建 Harness 的维护工时 vs 平台订阅费 + 绑定风险，得出真实的 TCO 对比。
- [ ] 安全团队把"Daybreak Red 资质"写进供应商评估清单；暂无资质的团队先用已全量开放的 GPT-5.6 Cyber，不要等 Critical 级模型放开通。
- [ ] 用 Revisiting RUA 的三问（预算/泄漏/内建）审计你最近引用过的任何一个 Agent benchmark 论文或榜单，至少标注一次"执行预算是否对齐"。
- [ ] 下次看到"开源模型跑赢闭源旗舰"类标题，先确认分数是否出自同一 harness、同一评测协议——跨框架旧基线不构成对比。

## 五、术语卡

| 术语 | 解释 |
|---|---|
| **Base 模型 / 后训练** | 只做完预训练的语言模型，会续写但不会对话与遵循指令。中训练（继续预训练）与后训练（SFT/RLHF 等）把 Base 变成可用产品；本次百度开放的就是这道工序之前的 checkpoint |
| **Harness** | 模型之外的整套运行框架：上下文与会话管理、工具调用、权限控制、任务中断恢复等。同一模型换 harness，实测表现可以差出一个数量级（见 uni-robot-agent 的 0.00 → 31.39） |
| **Daybreak Red** | OpenAI 面向高级授权安全工作（渗透测试、漏洞利用开发等）的访问层级，需身份核验与组织安全要求（SSO/MFA/IP 白名单），GPT-6 Cyber 首发仅向其获批客户开放 |
| **MoE（混合专家）** | 稀疏激活架构：总参数很大，但每个 token 只激活其中一小部分（如 280B 总参 / 14B 激活），在容量与单 token 计算成本之间取平衡 |
| **RUA（Robot-Use Agent）** | 操作真实或仿真机器人的具身智能体；其榜单评测存在执行预算不公、特权进度泄漏、解法内建三类已知的注水漏洞 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
