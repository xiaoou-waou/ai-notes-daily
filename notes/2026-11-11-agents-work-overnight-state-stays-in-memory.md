# 2026-11-11｜Agent 开始跨夜工作，状态还留在内存里

> 任务时长按天算了，可断点、幂等、版本迁移这三笔账，没人替你记。

**标签**：`#Agent` `#长任务` `#工程实践` `#模型发布`
**生成时间**：2026-11-11 12:20（北京时间）

---

## 一、今日观察

11 月 9 日到 11 日这三天，几家实验室发布的东西，卖点第一次不是"更聪明"，而是**"能跑更久"**。官方措辞几乎可以互换：Google 说 "long-horizon"、"built for sustained agentic workflows"；Anthropic 拿"连续 8 天"当封面案例；Meta 直接把产品定位写成 "the work agents repeat all day"。

把这几天的动作按"时间尺度被改到了哪一层"排开，问题就露出来了：

| 层 | 今天谁动了 | 时间尺度被改成了什么 | 还卡在哪个默认值 |
|---|---|---|---|
| **任务侧** | Gemini 4 Carbon（11-10 GA）、Claude Fable 5.2（11-09） | 8 天 / 1000+ 子智能体 / 10 个跨夜循环 | 单次上下文 1M token，再长也要重开一轮 |
| **执行环境** | Antigravity Remote Agents（2.29） | 合上笔记本仍在跑，手机上批权限 | 云沙盒 TTL 默认 7 天 |
| **框架** | 微软 Durable Task 扩展 GA（11-09） | 会话 ID 活过进程，重放不重调模型 | 序列化 ≠ 持久化，得自己存 |
| **训练** | 美团 LongCat-2.5（11-10 开源） | 未跑完的 rollout 存着接着跑 | 这套只在训练侧成立 |
| **计价** | Meta Muse Ember（11-09） | 约 $0.14 / 任务，"全天重复的活" | 仍按 token 计，不按"跑成功一次"计 |

**最值得记的是第四行和第三行其实是同一件事的两端。** 训练侧早就把"跑不完就存下来接着跑"做成了标准件——LongCat 的 partial rollout，本意就是让没跑完的长任务先存着，等下一轮接着跑；而推理侧直到 11 月 9 日，微软还在为一件事单独发一篇 GA 公告：把会话状态搬出 worker 进程。

顺便把两个数字摊开看：Anthropic 的 8 天，是模型跑完一个 OS 原型的时间；Google Cloud 给 agent 沙盒的默认 TTL 是 7 天。**这不是同一个系统的两个参数，也不构成任何因果**——我只是拿它们当一把尺子，量的是"任务能有多长"和"租给你多久"之间的默认值差距。这个差距真实的含义是：**今天你想跑一个长任务，第一件要设计的不是 prompt，是"它活过租期之后住哪"。**

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. Gemini 4 Carbon 向所有付费开发者开放，官方定位就是"长周期" 🟢

Google 11-10 正式开放 Carbon，官方原话是 "frontier performance in cybersecurity and **long-horizon agentic workflows**"，并明确它"通过消耗比 Argon 更多的 token 来做深度探索、缜密推理并运行**扩展验证循环**"。三项独立基准（CursorBench 4.0、Perplexity 的 WANDR、Zapier 的 AutomationBench）第一，官方称**单任务成本比次优外部模型低 2 倍以上**。

价格：首发 **$2 输入 / $10 输出**（每百万 token），**12 月 1 日起调至 $4 / $20**。

最能说明时间尺度的一个细节：Antigravity 的 `/swarm` 预览里，一队 agent 用 206 张工程图纸，**跑了 10 个跨夜循环（overnight loops）**，拼出一个 906K 三角面的 Three.js 重建。"跨夜"成了计量单位。

来源：[blog.google — Gemini 4 Carbon is now available](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available)

### 2. Fable 5.2 的 8 天，和一句最诚实的客户评语 🟢

Anthropic 11-09 的公告里，官方实验是：一名工程师让 Fable 5.2 设计一个操作系统原型，模型从空文件夹起步，协调**超过 1000 个子智能体**，**连续八天**编写、测试、审查代码，产出能在笔记本上启动的系统（内核、磁盘/键盘/网络驱动、持久化存储、窗口、登录界面、安装器）。

比这个数字更有价值的是公告里 Uber 工程师的评语：

> "It works until the job is actually complete instead of **stopping at a plausible checkpoint**."

他让模型跑了一次 10–12 小时的安全审计，派出约 170 个 reviewer agent。这句话精确命名了长任务的失败模式：**不是跑崩，是停在一个看起来合理的检查点上，然后宣布完成。**

来源：[anthropic.com — Claude Fable 5.2 and Mythos 5.2](https://www.anthropic.com/claude-fable-and-mythos-5-2)

### 3. Muse Ember：把"全天重复的活"单独定了一次价 🟢

Meta 11-09 发布，官方称其为"最小、最省"的模型，用途写得很直白：tool calls、coding subtasks、routing、extraction、long document parsing——"**the work agents repeat all day**"。

规格：**$0.10 输入 / $0.50 输出**每百万 token，缓存读 **$0.004**，1M 上下文，最高 512K 输出；官方口径约 **$0.14 / 每个 Artificial Analysis 任务**。AA 智能指数 36，与 Claude Haiku 5.5 同分，但 Meta 称单任务成本约为其三分之一。产品线拆成三档：Wonder 管最难的问题，Spark 管编码与 agent 工作流，Ember 管"可规模化重复"。

来源：[research.meta.ai — Introducing Our Smallest, Most Efficient Model: Muse Ember](https://research.meta.ai/blog/muse-ember)

### 4. 美团 LongCat-2.5 以 MIT 开源，训练侧先解决了"跑不完" 🟢

11-10 官方开源（11-02 发布），MIT 协议，可商用推理部署与二次训练，无需额外授权。总参数 **1.6 万亿**，每 token 激活约 **480 亿**，**100 万上下文**，W4A4 量化推理。

技术博客里最该记的不是参数量，是训练机制：采用 **partial rollout 异步训练**，让"未跑完的长任务保存后续跑"；过采样率按通过率动态调整，过滤全对/全错的样本组；对跨 checkpoint 的旧轨迹做梯度校正。同时**把真实 Agent 的失败轨迹转化成可复现、可验证的训练任务**。

工程约束也写得具体：国产卡**单卡显存不足 80GB**，FSDP 双重分片 + 拓扑感知并行后，长序列 SFT 单卡吞吐较 DDP 基线 **+86%**。

来源：[tech.meituan.com — 美团 LongCat-2.5 正式开源：从看见，到抵达](https://tech.meituan.com/2026/11/10/Meituan-LongCat-2.5-Open-Source.html)

### 5. 微软 Durable Task 扩展 GA：把会话状态搬出 worker 进程 🟢

11-09 GA（注意：GA 的是**扩展**，不是 Agent Framework 本身——后者 1.0 早在今年 4 月 GA，媒体标题容易混）。核心能力三条：

- 每个对话有稳定的 **durable session ID**，会话状态保存在 worker 进程之外，重启或换 worker 后可接上同一对话；
- 编排重放时**复用已记录的结果，不再次调用模型**——这是直接省钱的那一条；
- 人工审批用 `WaitForExternalEvent` 等待（示例超时设为 24 小时），**不需要 worker 常驻**。

官方还专门写了一句容易被忽略的：序列化会话引用**不等于**保存，应用必须自己持久化这个引用。

来源：[Microsoft Community Hub — Durable Task extension for Microsoft Agent Framework is now GA](https://techcommunity.microsoft.com/blog/AppsonAzureBlog/durable-task-extension-for-microsoft-agent-framework-is-now-generally-available/4571100)

### 6. Antigravity 把 agent 搬进云 VM；沙盒默认租 7 天 🟢 / 🟡

2.29 版本（changelog 11-03，9to5Google 11-06 报道）引入 Remote Agents：任务跑在隔离的 Google 云虚拟机里，关掉浏览器、合上笔记本继续跑，权限可以从手机批。CLI 需 1.4.12+。

限制要写清：仅 AI Pro / Ultra **个人账号**，Workspace 与 Cloud 商业账号暂无；**Voice Mode 目前只支持本地会话，云端会话用不了**（🟡 这一条来自对官方文档的转述，未见原始页面逐字核对）。

另一头，Google Cloud 的 Managed Agents 沙盒文档写明 TTL 为 **7 天**，每次交互自动重置——这解释了"为什么续跑不能只靠会话还活着"。

来源：[9to5Google — Antigravity Remote Agents](https://9to5google.com/2026/11/06/google-antigravity-remote-agents-voice-mode/) ／ [Google Cloud 文档 — Managed Agents sandbox environment](https://clouddocs-dot-devsite-v2-prod.appspot.com/gemini-enterprise-agent-platform/build/managed-agents/sandbox-environment)

## 三、为什么值得记

**1. 长任务的失败模式第一次被一句话命名了。** "Stopping at a plausible checkpoint" 和 9-25 那类静默失败不是一回事：静默失败是**该响的没响**，这个是**响得不对**——它报了完成，只是完成的是它自己挑的一个子目标。对长任务来说，这意味着"做完了"这个判断不能交给模型，验证点必须由外部写死。这也是为什么 Carbon 和 Fable 5.2 的官方描述里都在强调"扩展验证循环"和"对抗性验证器"，而不是单纯强调分数。

**2. 续跑是四件正交的事，不是"加个 checkpoint"。** 大部分团队做了第一件就以为覆盖了全部：

- **状态存在进程外**——微软已经点明"序列化 ≠ 持久化"；
- **副作用去重**——重放会重放工具调用，一封邮件不能发两次；
- **代码版本迁移**——恢复一个 run 的代码，几乎不可能是暂停它的那份代码（发布正是它被中断的原因）。如果新版本改了 state 结构，checkpoint 就是一段你的代码读不懂的 payload，而且失败得很安静：字段缺失被默认为 `false`，agent 把已经批准的步骤重做一遍；
- **谁来唤醒**——暂停的 run 不会自己重启，得有队列重投或者一个扫表进程。

**3. 训练侧比推理侧早半步解决了同一件事。** partial rollout 本质就是训练时的 checkpoint + 续跑；LongCat 那篇还更进一步，把失败轨迹转成可复现的训练任务——**失败被记成了资产**。部署侧目前没有对应物：一个跑了 6 小时的任务失败，大多数人拿到的只有一条日志，不是一条可以重放的用例。

**4. 时间尺度错配，先咬到的是钱，不是能力。** "8 天""10 个跨夜循环""10–12 小时审计"——这些任务的失败成本是几十到几百倍的 token 重放。而多数框架的重放在恢复时会重新调用模型；微软把"重放不重调模型"单独拎出来讲，恰恰说明这不是默认行为。**长任务的经济性，一大半不在单价，在重放次数。**

## 四、可行动

- [ ] **加一条"重启演练"**：让 agent 跑到第 3 步时 `kill -9`，再拉起。检查两件事：(a) 是否从断点续而不是从头来；(b) 是否重发了副作用。这是唯一能证明"续跑真的成立"的测试，比读文档可靠。
- [ ] **给 checkpoint 的 payload 加版本号，读不懂就拒绝恢复**（fail closed）。宁可让 run 挂掉报 `NewerCheckpoint`，也别让缺失字段默默默认成 `false`，导致已批准的步骤被重做。
- [ ] **所有有外部副作用的工具加幂等键**，键用 `run_id + step` 确定性生成。这样重放无论从哪一步接上，都不会发第二封邮件。
- [ ] **核对编排器的 termination grace period**：Kubernetes 默认 30 秒。如果你的优雅退出流程要给 agent 90 秒收尾，这个值不改，退出处理等于没写——超时后直接 SIGKILL，状态照样烂在半路。
- [ ] **跨夜任务先量租期**：确认沙盒/会话的 TTL，把 checkpoint 落到租期之外的对象存储上。别指望"会话还活着"能兜底——Google 那边给的是 7 天。

## 五、术语卡

| 术语 | 解释 |
|---|---|
| **Partial rollout** | 强化学习采样时，没跑完的长轨迹先保存，等下一轮资源或时机接着跑。LongCat-2.5 用它做异步训练，避免单个长任务拖住整个 batch |
| **Durable session / 持久会话** | 会话状态存放在 worker 进程之外，用一个稳定 ID 引用；进程重启或换机器后仍能接上同一个对话 |
| **幂等键（idempotency key）** | 由 `run_id + step` 确定性生成的键。工具执行前先查"这个键做过没有"，保证重放不重复产生副作用 |
| **重放（replay）** | 编排器恢复时按历史事件重新推进流程，已记录的结果直接复用。设计得当时不会二次调用模型，也就不重复付费 |
| **Sandbox TTL** | 云沙盒的存活时长，到期回收。Google Managed Agents 的默认值是 7 天，每次交互重置计时 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
