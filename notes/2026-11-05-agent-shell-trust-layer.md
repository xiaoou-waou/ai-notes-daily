# 2026-11-05｜Agent 的战场挪到了外壳与信任层

> 模型能力趋同后，这一天的新闻全指向同一件事：谁把"能干活的 Agent"装进你的电脑，谁就赢下一步。

**标签**：`#Agent` `#开源` `#大模型`
**生成时间**：2026-11-05 12:05（北京时间）

---

## 一、今日观察

把 11 月 4 日–5 日的几条大新闻并排放，会发现一条清晰的转移曲线：**模型公司不再只比"谁的模型更聪明"，开始军备竞赛"谁的外壳更好用、谁更可信"**。

| 事件 | 主语 | 抢的位置 |
|---|---|---|
| 混元 Hy4 正式版发布，首提视觉理解 + Computer Use，即将开源权重 | 腾讯 | "能看屏幕、能操作电脑"的通用 Agent 底座 |
| DeepSeek 开源 dsh-superagent-prototype：常驻仓库、自己接需求提 PR 的主动型编程智能体 | DeepSeek | 从"被动问答"到"主动干活"的 Agent 形态 |
| DeepSeek Harness 生态爆发：dsh-desktop 等"插件现做现装"衍生项目刷屏 GitHub | DeepSeek 社区 | Agent 的插件生态与工作流分发权 |
| Anthropic 开源 FlashProve：用零知识证明验证"这个回答确实出自指定模型" | Anthropic | API 服务的**信任层**——防暗中换模型 |
| Plato / Fragment / Serval 三笔 Agent 基础设施融资（1600 万 / 5600 万 / 1.5 亿美元） | 资本市场 | Agent 的测试、异常处置与运行治理 |

Hy4 把 Computer Use 塞进开源旗舰、FlashProve 解决"模型身份不可验证"、Harness 生态证明社区愿意为"外壳"贡献 17K+ star——三件事分别对应外壳的**能力面、信任面、生态面**。这是比单看任何一个 benchmark 更值得记的结构性信号。

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

1. **腾讯混元 Hy4 正式版发布：770B 参数，首次引入视觉理解与 Computer Use，即将开源权重** ——官方称首次跻身最强开源模型之列，同时承认与顶尖闭源模型仍有差距；已在腾讯云、元宝、ima 等产品上线。（🟢 南方+/科创板日报、新华网乌镇峰会报道均见 [南方+](https://www.nfnews.com/content/732GjXbP6W.html)、[央视网/新华网](https://news.cctv.cn/2026/11/05/ARTIzqLL7QFgTWSMEeYpIeCf261105.shtml)；权重尚未放出，开源时间以官方仓库为准）
2. **DeepSeek 开源 dsh-superagent-prototype（10 月 31 日，MIT 协议）**：常驻单个 GitHub 仓库的"主动型"编程智能体，听 Issue/飞书动静自己开工单、写代码、提 PR；官方明确标注为研究原型、非正式产品。（🟢 官方 GitHub 组织 deepseek-ai 发布，第三方报道见 [科技区角](https://www.x-techcon.com/article/205457.html)，仓库地址 github.com/deepseek-ai/dsh-superagent-prototype）
3. **DeepSeek Harness 插件生态爆发**：聚合数据显示 dsh-desktop（打包本地 Harness 运行时的桌面应用）约 17.2K star，DS-Bot、dsh-purge 等衍生项目快速上榜；此前 Harness 发布当天在 Hacker News 拿下约 352 分。（🟡 第三方聚合站 [GitHub.Locker](https://github.locker/topics/dsh-desktop) 与 [agentgid](https://agentgid.com/compare/deepseek-harness-vs-qwenpaw) 数据，star 数请以 GitHub 实时页面为准）
4. **Anthropic 开源 FlashProve**：基于零知识证明，让模型服务商在不公开权重的前提下证明"回答确实由指定模型生成"，针对 API 中模型被暗中替换问题；中文转述称检测速度提升数千倍、最快 17 秒。（🟡 多个中文聚合源转述，如 [今日 AI 要闻](http://mp.weixin.qq.com/s?__biz=MzkyOTE4NTI5Ng==&mid=2247484407&idx=1&sn=e4d781744d3545edbcefcab607b38fa0&chksm=c374af0be48157eb1c42207c1e1fd7a5bee455a46e812006f42a9141074242fefb45a07a0849#rd)，具体倍数与速度数据待 Anthropic 官方博客核实）
5. **Anthropic 更新 S-1 招股书：Q3 营收 169.6 亿美元（环比 +47%），披露约 8954 亿美元算力相关支出承诺**，同时营业亏损 5.67 亿美元，增速较 Q2 的 144% 放缓。（🟡 多家媒体援引 SEC 文件转述，如 [CSDN 鲲鹏昇腾社区转载](https://hwcomputing.csdn.net/6aea726940858c2d881853e6.html)，精确数字请以 SEC EDGAR 原始文件为准）
6. **Agent 基础设施融资潮**：Plato（模拟办公环境测试 Agent，Computer Work Val v1.0 基准）宣布 1600 万美元 A 轮；Fragment（采购/付款异常处置）披露总融资 5600 万美元；Serval（企业工作流自动化）1.5 亿美元 C 轮、估值 30 亿美元。（🟢 [The Agent Report 汇总](https://the-agent-report.com/2026/11/agent-proof-plato-fragment-serval)，各数字均为公司自报口径）

## 三、为什么值得记

- **"外壳"是模型趋同后的第一战场，且已被社区验证。** Harness 生态的爆发说明：模型能力接近时，开发者真正愿意投入的是插件、运行时和桌面形态。选型时应把"扩展生态健康度"当作和 benchmark 分数同级的指标。
- **信任层是被忽视的空白，FlashProve 方向比产品本身重要。** API 服务里"模型被暗中替换"长期只能靠信任承诺，零知识证明第一次给了可验证的出路——这对做采购、做合规的团队是实打实的风险控制抓手。
- **"主动型 Agent"从论文走进原型。** dsh-superagent 的核心原则是"尽量少占用人的注意力"，但它同时坦承是研究原型、代码多由 Agent 自己写。判断一个 Agent 产品成熟度，先看它敢不敢把自己的代码交给 Agent 维护。
- **评测侧也在跟着变。** Plato 的基准不看"回答得流不流利"，而检查 Agent 在模拟工具里留下的**最终状态**（如报表数字是否真算对）——评估 Agent 该从"看输出"转向"验状态"，这个方法论任何团队都能直接复用。

## 四、可行动

- [ ] clone `deepseek-ai/dsh-superagent-prototype`（MIT），跑通一个最小任务，重点读它的"主动触发规则"如何防止 Agent 乱开工单。
- [ ] 给自己常用的 Agent 工具做一次"外壳审计"：插件能否自定义？权限边界在哪？能否本地部署/审计？
- [ ] 把团队现有 Agent 评测从"看回答"改成"验终态"：挑 3 个真实业务任务，定义可程序化检查的完成状态。
- [ ] 若在采购模型 API，把"模型身份可验证"写进供应商评估项，关注 FlashProve 类方案的落地。
- [ ] 等混元 Hy4 权重放出后，关注其系统卡片里对 Computer Use 安全边界的描述，再决定是否在办公自动化场景试点。

## 五、术语卡

| 术语 | 解释 |
|---|---|
| Computer Use | 让模型看懂屏幕截图并直接操控键鼠/界面（含 Blender、CAD 等专业软件）完成计算机任务的能力，Agent 从"出主意"到"动手做"的关键一步 |
| Agent Harness | 包裹模型的"外壳"运行时：把文件读写、命令执行、插件管理等能力标准化为 Agent 可调用的接口，模型公司借此争夺工作流入口 |
| 零知识证明（ZKP） | 密码学技术：证明者能让验证者确信某个命题为真，却不泄露命题本身的具体内容。FlashProve 用它在不公开模型权重的情况下证明"回答出自该模型" |
| 状态校验型评测 | 不检查 Agent 的文字回答，而是程序化检查它在工具/系统里留下的最终状态（如订单是否真的创建、数字是否算对），是评估 Agent 可靠性的更严标准 |
| 主动型 Agent（Super-agent） | 不等指令、监听事件（Issue、群消息、异常监控）自行判断是否开工的智能体形态，工程难点在于触发边界与注意力成本控制 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
