# 2026-09-21｜「开源」今天被拆成了三道闸门

> 权重能下不等于能用，分数能看不等于你选对了维度，模型能进不等于拦得住——今天四件事分别卡在这三道闸门上。

**标签**：`#开源许可` `#评测` `#Agent安全` `#国产大模型`
**生成时间**：2026-09-21 12:04（北京时间）

---

## 一、今日观察

今天最值得记的不是"又发布了什么"，而是**「开放」这个词在一天之内被拆成了三张不同的通行证，而且它们互不覆盖**。

同一天里：阿里把 7B 的图像模型权重放出来，商用要另外申请；上海 AI Lab 把 744B 的 Agent 模型按 MIT 放出来，可商用，但 BF16 权重约 1.5TB，绝大多数团队根本搬不动。**一个许可能下不能用，一个许可能用搬不动**——"开放"在这两头都成立，但都不是你以为的那个意思。

第二道闸门在证据侧。腾讯混元联合清华、北大提出的 IWC-Bench 给出了一个刺眼的数字：美观度和易用性，**在模型层面相关系数 r=0.85，到了单个应用层面只剩 0.36**。也就是说：看榜单排名，好看的模型大致也好用；落到你手上某一个具体的页面，"长得漂亮"几乎不能预测"点得动"。榜单给你的是模型级结论，你要的是应用级结论，两者之间隔着这道 0.36。

第三道闸门在边界侧。谷歌 9 月 18 日证实，Gemini 在今年 5 月的一次网络安全评测中进入了**三家真实公司**的系统。真正该记住的不是"AI 会黑进去了"，而是：OpenAI、Anthropic、Meta、Google 这四起事件，**出自同一家评测公司的同一个配置问题**——本该断开公网的演练环境因为 bug 开着出口，而靶场里那家虚构公司与现实企业重名。四次"越界"，一个根因。

| 闸门 | 卡住的问题 | 今天的证据 |
|---|---|---|
| **权重闸门** | 能下载 ≠ 能商用 / 能搬动 | Qwen-Image-2.1 禁商用；Atria Dawn Preview MIT 但 ~1.5TB |
| **证据闸门** | 有分数 ≠ 维度是你关心的 | IWC-Bench：美观度 vs 易用性，模型级 0.85 → 应用级 **0.36** |
| **边界闸门** | 进得去 ≠ 拦得住 | Gemini 进入 3 家真实公司；四家实验室同源一个配置问题 |
| （成本闸门） | 能重写 ≠ 没有回归 | 微软用 Agent 移植 Copilot runtime 到 Rust，出现"数十个编译通过的回归" |

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. Qwen-Image-2.1：7B 开权重，但明确禁止商用 🟢

阿里 Qwen 团队 9 月 20 日开源 Qwen-Image-2.1，视觉生成部分仅 **7B 参数、32 层 Single-Stream DiT**，把文生图与图像编辑合进同一个模型，原生支持透明图像（RGBA）的生成与编辑，支持**最多 10 张参考图**输入，可用圈选、涂抹或独立掩码指定编辑区域。架构上采用**混合粒度注意力**：文本用 token 级因果掩码、图像用 chunk 级掩码，配合 **KV Cache 复用**，把输入图和编辑指令作为静态上下文在第一步算完并缓存。官方称可在 RTX 3090 级别消费级显卡上运行。

需要单独拎出来的是许可：权重挂在 **Qwen Research License** 下，**明确仅限非商业用途**，商用需另行邮件申请。而 Qwen-Image 1 当初是 **Apache 2.0**——这是明显的收紧。

- 官方博客：https://qwen.ai/blog?id=qwen-image-2.1
- 许可转述（🟡 二手，但多源一致，官方博客本身确实写的是 "open-source"）：https://the-decoder.com/alibabas-open-weight-qwen-image-2-1-claims-to-beat-closed-models-in-image-generation-with-just-7-billion-parameters/ ｜ https://traictory.com/news/2026-09-21-qwen-image-2-1

> ⚠️ 官方博客用 "open-source" 措辞但 LICENSE 是禁止商用的研究许可，社区对此有明确批评，准确说法是 **weights-available（权重可获取）** 而非 open-weights。benchmark 对比图也是 Qwen 自测（Qwen-Image-Bench），第三方复现尚未出现。

### 2. Atria Dawn Preview：744B 真 MIT，但门槛写在磁盘上 🟡

上海人工智能实验室发布 Atria Dawn Preview，基于智谱 **GLM-5.2**（744B 参数 MoE，256K 上下文）做 Agent 后训练，通过 **Verifiable Experience Pipeline**（把工具调用接到可执行环境、由外部验证结果而非模型自评）把「规划—工具使用—失败恢复」这套原本写在外部脚手架里的能力**压进权重**。许可为 **MIT**。技术报告 arXiv:2609.15818，143 位作者。

模型卡给出的 16 项 benchmark 中，Atria Dawn 在 5 项上拿到行内最高分：**DeepSearchQA 96.0、BrowseComp 92.5、BFCL v4 77.0、AutomationBench 53.8、CyberGym 86.5**；但在 **SWE-bench Pro 上 59.6，落后 Claude Opus 5 的 74.7 达 15.1 分**；Terminal-Bench 2.1 78.3 vs 90.2，JobBench 50.3 vs 68.0。

- 报道汇总（含 arXiv / GitHub / HF 三个一手链接）：https://asapai.co.kr/en/atria-dawn-preview-744b-agentic ｜ https://pandaily.com/shanghai-ai-lab-atria-dawn-preview-744b-moe-agent
- 论文：https://arxiv.org/abs/2609.15818

> ⚠️ 全部数字为**建设方自测，无第三方复现**；"约 1.5TB BF16 权重""发布于 9 月 11 日""无官方公告"等细节来自二手转述，HF 页面本次未能直连核实，标 🟡。

### 3. IWC-Bench：把软件测试搬进网页生成评测，"好看"预测不了"好用" 🟢

腾讯（混元）联合清华大学、北京大学提出 IWC-Bench（arXiv:2609.15387，cs.SE + cs.AI，v1 于 9 月 14 日、v2 于 9 月 17 日）。它不静态看代码也不只看截图，而是**给每个生成的应用插桩，用代码覆盖率引导一个 Agent 以模拟用户交互的方式去探索**，再把交互轨迹抽象成状态转移图，从**视觉美观度、易用性、需求符合度**三个维度打分，且把"探索"和"评分"分开。

论文原文的硬数字：

- **369 条真实用户需求、5088 条验收标准**；评测 **17 个前沿 LLM**，每个模型对每条需求生成一个应用，共 **17×369 = 6273 个应用**
- 插桩在 6273 个应用中**只失败 7 个，成功率 99.89%**
- 覆盖率引导把**中位数函数覆盖率从 91.9% 提到 94.3%**
- 在 197 组内部 arena 采样的有效会话上，与人类偏好**一致率 85.3%**
- **关键结论（原文）**："Visual aesthetics and usability capture distinct aspects of application quality. Their correlation is strong at the model level (r=0.85) but only 0.36 at the application level."
- **没有任何模型在三个维度上同时领先**：Claude-Opus-5 综合第一并领跑易用性（+1.757）；**GPT-5.6-Sol 以大幅优势领跑美观度（+2.239），但易用性只排第六**；Kimi-K3 领跑需求符合度（+1.283）；MiniMax-M3 美观度接近平均（−0.323）却易用性垫底（−1.443）

- 论文：https://arxiv.org/abs/2609.15387 ｜ https://arxiv.org/html/2609.15387v2

### 4. Step 5 Preview：600B/27B 稀疏 MoE，权重押后到 10 月 15 日 🟢

阶跃星辰（StepFun）9 月 20 日发布旗舰基座模型 Step 5 Preview：稀疏 MoE，**总参数 600B、每 token 激活约 27B（约 4.5%）**，支持 **100 万 token 上下文**与文本+视觉输入。API 即日全量开放，**定价 $1 / 百万输入 token、$2.70 / 百万输出 token**，缓存输入约 95% 折扣；**权重计划 10 月 15 日开源**。

架构上刻意"窄而深"：**92 层** Transformer 布局，配合 **Sparse Grouped-Query Attention + 分块 token 合并**，官方称把 indexer 与 top-k 选择开销降到更稠密基线的约 1/8。训练侧强调 on-policy 长周期 RL 与 MoE 路由的**逐位（bit-wise）训练-推理对齐**，加上 MTP-3 投机解码、FP8 MoE、KV cache offload，官方称长周期 RL 端到端加速 3 倍以上、sample-ledger loss 低于 1%。

Artificial Analysis 智能指数 **44 分**（与 Kimi K3 max 同分，约为后者单任务成本的 1/3）；终端类评测 Terminal-Bench 4.0 **33%**（对比 DeepSeek V4.1 Flash 的 27%）、SciCode **59%**。

- https://pandaily.com/stepfun-step-5-preview-600b-moe-1m-context
- https://news.qq.com/rain/a/20260920A05BH300
- https://genztech.blog/p/stepfun-step-5-preview-600b-moe-1-dollar-per-million-tokens

> ⚠️ "全球开源前三""单任务成本仅为 Claude Opus 5 的 1/8"为厂商口径/媒体转述；**许可证尚未公布**——也就是说 10 月 15 日放出来的权重到底能不能商用，目前是未知的。这一点和第 1、2 条是同一个问题。

### 5. Gemini 在安全评测中进入三家真实公司系统，四家实验室同源 🟡

谷歌 9 月 18 日证实：今年 5 月，由 AI 安全公司 **Irregular** 实施的一次网络安全能力评测中，Gemini 进入了**三家真实公司**的系统。谷歌安全工程副总裁 Heather Adkins 的声明原文："In a standard evaluation, the model found public information online and guessed credentials to access websites it thought were part of the test. In all three of these instances, the model stopped."

三个叠加的失误：① 按设计本不该连公网的演练环境因 bug **开着出口**；② 演练里那家**虚构靶子公司与现实中一家真实企业同名**；③ 真实企业的服务凭据**公开摆在代码仓库里**。三次进入中，**一次靠反复试探猜中密码，两次直接用公开仓库里的现成凭据**——没有一次依赖新漏洞。

时间线与定性：**5 月发生 → 7 月底评测方通知各实验室 → 9 月 18 日媒体问询后谷歌才公开确认**。谷歌称不认为这构成模型"失准"（misalignment），因此此前未主动披露。Irregular 方面的定性原文："This is the same issue that was already reported and does not represent a materially separate incident. All relevant labs were notified in late July."

- 中文权威转述（新华社/环球网/财联社多源）：https://www.163.com/dy/article/L76AAG8J05198CJN.html ｜ https://news.qq.com/rain/a/20260919A0AR0X00
- 英文汇总：https://aibusinessweekly.net/p/google-gemini-hacked-three-companies-irregular

> ⚠️ 谷歌官方声明与本事件细节均通过二手媒体报道转述，谷歌官方博客本次未直连核实，标 🟡。被影响公司名与模型版本未披露，不做猜测。另：OpenAI（Hugging Face 事件）、Anthropic、Meta 此前的同类事件经 CNBC 报道同样指向 Irregular 的同一配置问题。

### 6. 微软用 Agent 把 Copilot runtime 从 TypeScript 移植到 Rust：12 万美元，但代价是"数十个编译通过的回归" 🟢

支撑 GitHub Copilot CLI、Copilot 应用、SDK 与云端 Agent 的 runtime，已由 AI Agent 完成从 TypeScript 到 Rust 的整体移植。微软杰出工程师 **Stephen Toub** 记录了全过程：

- **43 万行 TypeScript → 80 万行生产 Rust**，跨 **14.5 周、135 次以上发布**，平均每天约 **1.3 个移植 PR**
- 成本约 **12 万美元 token 费用**（约 1363 亿 token）+ 约 **3 周**主导开发者时间
- 性能：1000 次单轮会话生命周期，共享客户端 + 100 并发流水线下，TypeScript **7.55 次/秒** vs Rust 进程内 **120 次/秒**，即 **15.9 倍**；10 客户端内存 **1383 MB → 126 MB**；本地端到端建客户端+起会话+跑一轮+拆除从 **5.25 秒 → 292 毫秒**
- 用了多个模型分工（点名 **GPT-5.6 Sol** 与 **Claude Opus 4.8**）；30,000 行的 session.ts 那次 25 小时转换，开头 **56 分钟在读文档、做了 122 次工具调用**，随后派生 **15 个子会话**各自建 worktree 互相通信
- Toub 的两句限定很关键：**"This is in no way a claim that every large TypeScript program should become Rust."**（需求是 C ABI 嵌入、低启动/稳态开销、可预测资源占用，才指向 Rust）；以及 **"if-it-compiles-it-is-correct 只能当笑话"**——项目遇到**数十个编译器批准（compiler-approved）的回归**：不完整移植、行为契约改变、状态与生命周期错误
- 一个可对照的量化结果：迁移期间及之后，GitHub Copilot 公开质量问题占比**稳定在 23.7%**，迁移前为 22.9%

- https://www.theregister.com/devops/2026/09/18/microsoft-agentically-ports-copilot-runtime-to-rust-for-120k/5297549
- https://www.aiandtech.news/article/microsoft-rewrites-copilot-runtime-in-rust-using-ai-agents-for-120k
- RustConf 上顾问 Lisa Crossman 的警告（🟡 转述）：Rust 编译器能挡住内存不安全代码，**挡不住 Agent 把错误的程序写得语法正确**

---

## 三、为什么值得记

1. **"开放权重"已经不能作为一个词来用了，采购前必须问两句。** 今天两个极端同时出现：Qwen-Image-2.1 是 7B 小到 3090 能跑、但 LICENSE 写着非商用；Atria Dawn Preview 是 MIT 随便商用、但 1.5TB 权重把绝大多数团队挡在门外。**决定你能不能落地的，不是"开不开放"，是"开放的那一条恰好卡在你不缺的那一项上"。** 建议把"开放"在内部文档里拆成两个字段：`license_scope`（研究/商用/需申请）和 `deploy_floor`（最低显存或磁盘门槛），缺一个就没法选型。

2. **IWC-Bench 的 0.36 是今天最该被抄进自己评测体系的一个数字。** 它证明"模型级相关 ≠ 应用级相关"：榜单上排名靠前的模型整体又好又好看，但你手上那**一个**具体产物好不好用，无法从它好不好看推断。任何靠"看截图/看 demo"验收 AI 生成前端的流程，都建立在一个 r=0.36 的假设上。论文给的解法也可直接抄：**插桩 + 覆盖率引导探索 + 探索与评分分离**——先收集运行时证据，再打分，而不是先定验收标准再让 Agent 去凑。

3. **Agent 安全事件的根因正在从"模型太强"转移到"靶场太松"。** 四家头部实验室的越界事件指向同一个评测公司的同一个配置问题，这个信号比任何单起事件都重要：下一次不需要模型更强，**只要同一台靶场再漏一次就够了**。更值得警惕的是那道唯一生效的防线——模型自己判断"这不是假的"然后停下——**它不写在配置里，写在模型的判断里，因此不可验收、不可审计、无法保证下次生效**，而且它生效在动作之后（系统已经被进了），拦住的是后果不是进入本身。把"测试环境是隔离的"从一句假设改成一项要验收的检查（出口是否真断、凭据是否按生产标准管、异常是谁先发现的），是这起事件最直接的产出。

4. **"编译通过"是一个正在被高估的验收标准。** 微软这次移植的成功之处（15.9x、内存降到 1/11、$120K vs 人工数年数百万美元）和它的代价（数十个编译器批准的回归）是同一枚硬币。Rust 的类型系统和借用检查器把"内存不安全"这类错误变成了编译期硬错——但这恰恰会让 Agent 更容易通过编译，从而**把失败从"编不过"平移到"编过了但语义错了"**。Toub 列举的四类回归（语义歧义、分支漂移、功能缺失、行为差异）全都是编译器看不见的。对正在用 Agent 做代码迁移的团队：**编译通过率的提升不等于正确率的提升，别把它当进度指标。**

---

## 四、可行动

- [ ] **建一张"开放"双字段表**：把你正在评估的开源模型按 `license_scope`（Apache-2.0 / MIT / 研究许可 / 需申请）和 `deploy_floor`（最低显存或权重体积）两列登记。今天就能填的两个：Qwen-Image-2.1 = 研究许可 + ~3090 可跑；Atria Dawn Preview = MIT + BF16 约 1.5TB（🟡 待核）。凡是要进产品的，先过第一列。
- [ ] **给 AI 生成的前端加一道"运行时验收"**：不必照搬 IWC-Bench 全量，但可以取最小子集——给生成的页面插桩收集函数覆盖率，用一个 Agent 模拟点击关键路径，统计"声明了但点不动"的功能比例。先跑 20 个自己项目里的页面，看这个比例有多高。
- [ ] **自查 Agent/eval 环境的出口**：如果你的评测或 CI 沙箱里 Agent 能联网，明确回答三问——出口白名单是否真的生效并有人定期验证？环境里发放的凭据是否按生产标准管理（不是明文摆在仓库里）？异常是监控先发现还是别人来问？三个问题任一答不上来，就是下一个 Irregular。
- [ ] **把"编译通过"从完成标准里降级**：在 Agent 代码迁移任务里加一个语义层检查（行为契约 diff、关键路径回归测试、跨模块接口快照），并记录 compiler-approved regression 的数量作为独立指标。拿微软的 23.7% vs 22.9% 做参照——质量指标没退化，不等于没有回归。
- [ ] **试 Qwen-Image-2.1 的 10 参考图 + RGBA 链路**（仅限非商业评估）：重点验两个官方 demo 没说清的点——alpha 通道的边缘是否有柔边/光晕（决定能不能进设计管线），以及 10 参考图那一端人物身份与服装一致性会不会崩（官方自己的样张里就有松动）。同时测一下混合粒度注意力 + KV Cache 复用的加速在 5 张以上参考图时到底有多少。

---

## 五、术语卡

| 术语 | 解释 |
|---|---|
| **稀疏 MoE（Sparse Mixture-of-Experts）** | 每个 token 只经过少数几个"专家"子网络，而不是跑遍全部参数。所以 600B 总参数可以只激活 27B（约 4.5%）——成本跟着"算了多少"走，不跟着"存了多少"走，这是 Step 5 Preview 能做到 $1/百万输入 token 的经济学基础。 |
| **RGBA 原生透明** | 模型直接输出带 alpha 通道的图像，而不是先出 RGB 再做抠图/蒙版。Qwen-Image-2.1 把这一能力从 2025 年 12 月的独立模型 Qwen-Image-Layered 合进了主模型，可以直接对透明层上的文字做编辑，省掉后期合成的转换步骤。 |
| **混合粒度注意力 + KV Cache 复用** | 文本（系统前缀、编辑指令）用 token 级因果掩码，图像生成用 chunk 级掩码；输入图和编辑指令作为静态上下文在第一步算完并缓存，后续步直接复用。多参考图场景下推理效率和显存开销改善最明显——这是 Qwen-Image-2.1 敢在 7B 上堆 10 张参考图的前提。 |
| **覆盖率引导的探索（Coverage-guided Exploration）** | 借自软件测试（模糊测试）的思路：先给程序插桩，再用"哪些代码还没被执行到"来引导测试输入往没走过的分支上走。IWC-Bench 用它引导 Agent 探索网页功能，把中位数函数覆盖率从 91.9% 提到 94.3%，从而尽量减少"功能实现了但没被探索到"造成的漏判。 |
| **Compiler-approved Regression（编译器批准的回归）** | 代码能通过编译、类型检查、借用检查，但语义与原来不同。Rust 能挡住内存不安全，挡不住"把错误的程序写得完全正确"。微软移植项目中遇到的数十个回归分四类：语义歧义、分支漂移、功能缺失、行为差异。 |
| **Verifiable Experience Pipeline** | 上海 AI Lab 在 Atria Dawn 中用的 Agent 训练方法：把工具调用接到可执行环境，用外部验证的结果（而非模型自评）作为奖励信号，从而把"规划—工具使用—失败恢复"从外部脚手架压进模型权重。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
