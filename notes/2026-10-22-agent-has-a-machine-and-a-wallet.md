# 2026-10-22｜agent 拿到了机器和钱包，唯独没人给它签字

> Claude Duet 把「替你动手」要的四样东西一次配齐，剩下那一样今天被 LiteLLM 后门当众拆穿。

**标签**：`#Agent` `#供应链安全` `#ClaudeDuet` `#开源生态`
**生成时间**：2026-10-22 12:11（北京时间）

---

## 一、今日观察

今天最值得记的不是哪个模型又涨了几分，而是 **agent 的"执行条件"第一次被一件产品一次性配齐**——而在配齐的同一天，这套条件里唯一没人负责的那一环，被当众打穿。

一个 agent 要真的替你干活，需要五样东西。前三样是能力，第四样是约束，第五样是信任：

| agent 需要什么 | 今天谁给了 | 给到什么程度 | 你现在能做什么 |
| :--- | :--- | :--- | :--- |
| **一台自己的机器** | Claude Duet | 独立虚拟机 + 自带浏览器，**你的笔记本/手机关机也照跑** | US 区 Pro/Max 加入 waitlist |
| 　（另一种形态） | Recursive Flint | 反向解法：不进云，塞进你自己的笔记本——40B MoE / 2.5B 激活，M4 Pro 上 **131 tok/s**，Apache 2.0 | Hugging Face 直接下载 |
| **属于你的记忆与身份** | Claude Duet | 继承你 Claude 账户已有的记忆、技能、已连接应用，官方称设置"几乎不用做" | 先清一遍你现有的连接器 |
| **一个钱包** | Claude Duet | Stripe **Link** 数字钱包 + **虚拟卡**（真实卡号不出让）+ Shopify Shop Pay | 付款前会先向你确认 |
| **一道防线** | Claude Duet | 新分类器 + 安全系统提示词；**信用卡号与政府身份证号一律拒绝**；发消息/付款/签约/删除均需你批准；**证券交易与账户间转账即使你批准也不做** | 在公开漏洞赏金范围内 |
| **一整条没被换过的依赖链** | **没人给** | **今天被打穿：LiteLLM 1.107.0 带凭据窃取器 + 后门** | `pip show litellm`；锁 `1.106.2`；查 `cook.pth` |

前五行的热闹，和最后一行的事故，是同一件事的两面：**能力这一侧今天全被补齐了，信任这一侧今天是被证明不存在。** 而这次攻击用的是 `.pth` 机制——Python 解释器一启动就执行，**跟你有没有 `import litellm` 无关**；删掉 litellm 目录也不清不掉。你给 agent 那台"独立虚拟机"再干净，只要它和你的 CI 共用一套 Python 环境，前面四道门就都白配。

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Anthropic 发布 Claude Duet：第一款把"机器 + 记忆 + 钱包"配齐的主动式 agent

美国时间 **10-21** 开放研究预览，基于 **Claude Opus 5.5**，独立 App 登陆 iOS / Android / claude.ai，先向 **US 区 Pro 与 Max 订阅用户**开放候补名单，预览期与其余 Claude 功能共用套餐额度。核心机制：

- **独立虚拟机 + 自带浏览器**：任务在后台跑，不要求你的设备开机；完成后或需要你复核时推送通知。
- **主动而非应答**：每天早上发一份简报，白天**每隔几小时**检查一次已连接账户（官方明说不停检查会太快耗光额度）；可语音或文字在一个持续线程里交互。
- **6,000+ 连接器**：Gmail / Slack / QuickBooks / Stripe / Gusto / Docusign / HubSpot / Canva / Shopify 等；即将支持用 1Password 里保存的登录态登录网站。
- **支付**：通过 Stripe 的 **Link** 数字钱包，确认商品后由 Link 请你批准，再用**虚拟卡**付款，真实卡号不共享；也可用 Shopify 的 Shop Pay 结账。
- **凭据处理**：沿用 Claude Managed Agents 的设计，**不直接看到你的密码或登录 token**；动作由 auto mode classifier 审批，提示词注入防护来自其 browser-use 研究；**红队 + 一家外部公司做了渗透测试，并纳入公开漏洞赏金**。
- **官方自曝短板**：可能误读会话或**误判紧急程度**；核心功能围绕工作构建，**订票这类个人事务"没那么强"**；暂时**还不能把浏览器画面展示给你看**。

来源：[Introducing Claude Duet（Anthropic 官方，经 Releasebot 全文转载）](https://releasebot.io/updates/anthropic)｜[Reuters / CNA](https://www.channelnewsasia.com/business/anthropic-unveils-claude-duet-ai-agent-app-6480311)｜[界面新闻](https://www.163.com/dy/article/L9R3I5OD0534A4SC.html)

### 2. 🟢 LiteLLM 1.107.0 被植入凭据窃取器与后门，PyPI 已隔离

**10-21** 当天，周下载量约 **2,300 万**的 LLM 代理库 LiteLLM 的 **1.107.0** 版本在 PyPI 与官方 Docker 镜像中被植入恶意代码，暴露约 **2 小时**。

- **投递路径**：攻击者用**三名工程师被盗的 GitHub CLI OAuth token**，一个账号触发 release workflow、另一个审批，针对一个**只差一个连字符的仿冒 fork（`Berri-AI/litellm` vs 正版 `BerriAI/litellm`）** 构建，构建来源被如实记录，因此"看起来是合法来源"。LiteLLM 称**尚未查明 token 最初是怎么丢的**。
- **时间线（UTC）**：11:39 发布到 PyPI → 13:20 PyPI 隔离 → 13:53 Docker 镜像移除。
- **载荷**：`cook.pth` + `cook.py` + `sitecustomize.py` 落在 `site-packages`。`.pth` 和 `sitecustomize.py` 在 **Python 解释器启动时自动执行，即使从不 import litellm**。`cook.py` 收集云凭据、SSH/GPG 私钥、Chromium/Firefox 浏览器数据、AI 编码工具配置与 LiteLLM proxy 凭据，用 **AES-256 + RSA-4096** 加密 POST 到仿冒域名 `www.litellm[.]dev/healthcheck`；`sitecustomize.py` 每小时查一次 GitHub 上的 `domain.txt` 拿域名，再从 `http://{domain}/codepy` 拉代码执行。
- **删不干净**：删除 litellm 包目录**不会**移除这三个文件，运行环境里自己的 `python` 或 `pip` 会再次触发。
- **处置**：按 StepSecurity 建议，任何跑过该版本的主机按**完全失陷**处理；版本固定在 `1.106.2`（**建议按 digest 锁**）；轮换该主机能触达的一切凭据——云密钥与实例角色、SSH/GPG、浏览器密码、AI 工具 token、CI 与 Vault 密钥、LiteLLM proxy 数据库里的各家 API key。
- 这是 LiteLLM **2026 年第二次**被投毒（上一次是 1.82.7 / 1.82.8，被关联到 TeamPCP）；两次之间尚未证实有联系。

来源：[Datadog Security Labs](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-docker/)｜[Upwind（首个发现者，GitHub issue #47826）](https://www.upwind.io/feed/litellm-1-107-0-supply-chain-attack-malicious-code-found-in-pypi-package)｜[Protect Computer（含 StepSecurity / SafeDep / Socket 交叉印证）](https://protect.computer/news/2026-10-21-litellm-1-107-0-pypi-docker-compromise)

### 3. 🟢 Anthropic 发布 API 版本 2026-10-21：SDK/CLI 许可从 MIT 换成 Apache 2.0，且带破坏性变更

同一天（10-21）开发者平台发布新 API 版本 `2026-10-21`，并配套默认发送该版本的 SDK/CLI：**Python 2.0.0、TypeScript 1.0.0、C# 13.0.0、Go 2.0.0、Java 3.0.0、PHP 1.0.0、Ruby 2.0.0、`ant` CLI 2.0.0**。官方明确两点：

- 新 SDK/CLI **有不依赖 API 版本的破坏性变更**；
- **许可从 MIT 改为 Apache 2.0**（这是合规口径会变的一条，不是版本号小事）。

同时 user profiles 新增 **`enforcement_status` 与 `enforcement_actions`** 字段，可查看 Anthropic 是否限制了你的某个终端客户，并用 `enforcement_status[]` 过滤器筛出处于限制/封禁状态的档案。

来源：[Anthropic Release Notes（Releasebot 转载，原始源 docs.claude.com）](https://releasebot.io/updates/anthropic)

### 4. 🟢 Google 联合 Meta 的 PyTorch 团队开源 TorchTPU；🟡 DeepSeek 开源推理引擎 DeepInfer

**去 CUDA 化的两端，同一周落地。**

- **TorchTPU（10-20，PyTorch Conference 2026）**：Google 与 Meta PyTorch 团队共同开发，**Apache 2.0**，目前 `torch_tpu 0.2.0` 在 PyPI（Python 3.11+）。它作为**原生 PyTorch 后端**接入 PrivateUse1 接口，把 TPU 变成与 GPU/CPU 并列的设备：`.to("cuda")` → `.to("tpu")`，分布式后端 `nccl` → `tpu_dist`。官方博客给出的口径：**约 450 个 ATen 算子**（含主流架构所需全部 Core ATen 的前反向）、已在 **HF 下载量最高的 5,000 个模型**上验证开箱执行、最高扩展到 **8,192 颗 Ironwood（TPU v7x）**；**52% MFU 训练 Qwen3 8B（TorchTitan + Ironwood，Google 自测）**。四个仓库一起开源：TorchTPU 本体 + 与 Inferact（vLLM）和 RadixArk（SGLang）合作的推理后端 + TorchTitan。**PyTorch/XLA 已废弃，仓库将于 11-15 归档**。
- 🟡 **DeepInfer（DeepSeek）**：据多家转述，DeepSeek 把支撑 V4.1 Flash 线上推理的引擎以 **Apache 2.0** 开源，支持 **NVIDIA SM100（Blackwell）与华为昇腾 950** 双平台，含分布式推理、推测解码、SWA Bounded Replay、结构化输出，并同步开源 token 编解码组件 `deepseek-recipe`。**但转述同时指出它明确缺失 KV cache 体系、prefill/decode 分离、多副本负载均衡**——即不是 hyperscaler 的现成替代品，而是针对单一模型族调优的生产引擎。另有"单集群日处理 155 万亿 Token"的说法。⚠️ 以上均为二手转述，**未在其 GitHub 仓库 README 中逐条核实，暂不作为既定事实**。

来源：[Introducing TorchTPU（PyTorch 官方博客）](https://pytorch.org/blog/introducing-torchtpu/)｜[Google Cloud 公告转述](https://gptonline.ai/google-open-sources-torchtpu-pytorch-tpus)｜[BYOBot 日报（DeepInfer 部分）](https://byobot.ai/ai-news/ai-daily-newsstand-october-21-2026)｜[腾讯研究院 AI 速递 20261021](https://www.sohu.com/a/1090360348_455313)

### 5. 🟡 Recursive 发布 Flint：一个"主要由 AI 自己造出来"的笔记本编程模型

由前 Salesforce 首席科学家 **Richard Socher** 创立的 Recursive（今年 5 月出隐身，**融资 6.5 亿美元、估值 46.5 亿美元**，投资方含 GV、NVIDIA、AMD Ventures）发布 **Flint**，Apache 2.0，可在 Hugging Face 免费下载。据多家转述（原始出处为 TechCrunch）：**40B 参数 MoE、单任务仅激活 2.5B**；在 **M4 Pro 的 MacBook Pro 上约 131 tok/s**（对比同机的 Gemma 4、Nemotron 3.5 Lightning 的 58–69 tok/s），RTX Spark 上超 150 tok/s；公司的自动化研究系统 **Eureka Machine** 参与了从预训练到后训练、推理的几乎每一步，其中**低比特训练把模型缩小 71% 而几乎没有质量损失**；**小团队在不到四个月内从零构建**。官方承认 Flint 需要比大型付费编程助手更多的引导，建议把大任务拆小。

⚠️ 上述参数、速度与融资数字**均来自媒体转述，未在官方模型卡或公司公告页逐条核实，标 🟡**。这条真正的价值不在分数，而在"**模型开发本身也开始被 agent 化**"这个信号。

来源：[AI News Feed（转述 TechCrunch）](https://ainewsfeed.tech/articles/recursive-releases-flint-a-laptop-coding-model-largely-built-by-ai-34452-en-us-v1)｜[Business Faces](https://businessfaces.net/article/274647)

### 6. 🟢 讯飞 1024 开发者节（今日开幕）：星火 X2.6 + Spark-Audio，走"全国产 + 云端协同"

**10-22**（今日）2026 科大讯飞全球 1024 开发者节在北京国家会议中心二期举行主论坛，合肥设分会场。官方会前预告口径：

- **讯飞星火 X2.6** 正式发布，**基于全国产算力**，强化编程与智能体能力，展示超长上下文与长程任务处理；
- 同步发布全国产**"云+端"协同方案**——让端侧与云端按**任务需求和数据边界**分工（敏感资料不上云、高频任务不下云）；
- 发布全国产语音基座大模型 **Spark-Audio**，覆盖语音识别、同声传译、实时语音交互与复杂音频理解；
- 首次发布**星帆 WinWork 数字员工平台**，尝试让 AI 在权限与规则边界内"进入岗位与流程"。

⚠️ 具体能力数值待会后官方材料公布，此处仅为议程/预告口径。同日国产侧还有：🟡 阿里 Qwen-Audio-3.1 语音全家桶（ASR/TTS/全双工 Realtime 共 5 款，**音频服务价格最高下调 95%**）、🟡 腾讯混元 Hy Image 3.5 preview（10-21，2K 分辨率，腾讯云 API 2K 图 0.15 元）——**价格与规格均来自日报转述，未核到官方定价页**。

🏦 🟡 **融资面**：据彭博社报道（经国内媒体转述），**DeepSeek 完成约 1,000 亿元人民币（约 150 亿美元）新一轮融资，投前估值仍约 5,000 亿元**；目标从 500 亿两次上调至约 1,000 亿，**不到半个月翻倍**，新老股东各约占一半；宁德时代拟增资约 100 亿元（首轮约 50 亿），腾讯、IDG 资本、砺思资本、拾象科技继续参与，新进石溪资本、中芯聚源、CPE 源峰、君联资本、吉利等**产业资本**；同时推进科创板 IPO。**均为"据报道"口径，交易未获官方确认，标 🟡**。

来源：[中国经济网](https://www.ce.cn/cysc/tech/gd2012/202610/t20261021_3267084.shtml)｜[中国经济新闻网](https://www.cet.com.cn/itpd/hlw/10625283.shtml)｜[合肥高新区（官方）](https://gxq.hefei.gov.cn/xwdt/yqyw/18982139.html)｜[CNMO（转述彭博社）](https://news.qq.com/rain/a/20261022A05T9B00)

## 三、为什么值得记

1. **"agent 能不能替你动手"的瓶颈，今天从模型能力正式搬到了执行条件。** Duet 给的东西里，最有分量的不是 Opus 5.5，而是**那台带浏览器的虚拟机**——它让 agent 第一次不依赖你的设备在线。同时它又立刻把这个能力钉死在边界里：发消息、付款、签约、删除全部要你批准，**证券交易和账户间转账"即使你批准也不做"**。这份"不做清单"比"能做清单"更值得抄进你自己的 agent 设计里。
2. **LiteLLM 事件真正的教训不是"有个包被投毒"，而是攻击面选在了你不会审的那一层。** 三个文件都落在 `site-packages`，靠 `.pth` 和 `sitecustomize.py` 在解释器启动时生效——这意味着"代码走查 + 依赖树扫描"这类常规动作**天然看不见它**，而 CI 里跑一次 `python` 就中招。对一个把各家 API key 集中存放的代理层来说，这是最坏的位置。
3. **构建来源（provenance）这次没能救场，因为它是"如实记录"的。** 攻击者针对只差一个连字符的 fork 构建，构建记录忠实写明了来源——所以"有 provenance"不等于"来源可信"。真正起作用的是**有人真的去读了产物**（Upwind 发现并开 issue）。这条比任何 SLSA 等级讨论都更可执行。
4. **硬件可移植性正在从"重写工程"变成"配置开关"，但代价是房东换人了。** TorchTPU 与 DeepInfer 同一周落地，方向一致：让你的代码不再预设 CUDA。可 TPU 只能从一家租、Trainium 只能从另一家租——**你拿到的是一扇更好开的门，门后还是同一个房东**。真正该做的是把"模型供应商"从架构决策降级为可替换选项，而不是以为自己解脱了。
5. **国产侧的路线已经写得很直白：算力全国产 + 任务按数据边界在云和端之间分流。** 讯飞把"云+端协同"和"全国产算力"绑在一起讲，等于承认**不是所有数据都能上云、也不是所有任务都该走云**——这跟 Recursive Flint 把模型塞进笔记本是同一个判断的两种落地。

## 四、可行动

- [ ] **立刻查你的环境有没有踩 LiteLLM**：`pip show litellm` 看版本；检查 lockfile 与容器镜像 digest；在 `site-packages` 里搜 `cook.pth` / `cook.py` / `sitecustomize.py`；查 `/tmp/remote_code_loader.lock`；看网络日志有没有到 `litellm.dev` 或 `raw.githubusercontent.com/letters9813/...` 的出站。命中就按完全失陷处理并轮换凭据。
- [ ] **把"按 digest 锁依赖"写进 CI 规则**，而不只是锁版本号。这次事件里版本号 1.107.0 是可被替换的，digest 才是你审过的那份。至少对代理层/网关类依赖（LiteLLM、各类 SDK、MCP server）强制。
- [ ] **检查你是否在用新版 Anthropic SDK**，并做两件事：读一遍 `2026-10-21` 的破坏性变更清单；把 **MIT → Apache 2.0** 的许可变化同步给法务/合规（Apache 2.0 多了明确的专利授权与声明要求，分发侧条款不一样）。
- [ ] **给你的 agent 抄一份"不做清单"**：参照 Duet 的口径——发消息、付款、签约、删除前必须人工确认；证券交易、账户间转账即使被批准也拒绝；信用卡号与政府身份证号一律不转发。把它写成系统提示词里的一段硬约束，而不是策略文档里的一句话。
- [ ] **如果你有 PyTorch 训练栈，花一小时试 TorchTPU 的迁移成本**：`pip install torch_tpu==0.2.0 --extra-index-url https://download.pytorch.org/whl/cpu`（注意默认安装会拉 CUDA 版），把 `.to("cuda")` 换成 `.to("tpu")`、分布式后端换 `tpu_dist` 跑一个最小模型。同时把 **11-15 PyTorch/XLA 归档**记进排期——还在 `torch_xla` 上的项目不到四周就要转只读。
- [ ] **给"我到底授权了哪些连接器"做一次盘点**。Duet 继承你 Claude 账户已有的记忆与已连接应用，这意味着**你现在没清理的授权，会在 agent 上线那天被自动继承**。

## 五、术语卡

| 术语 | 解释 |
| :--- | :--- |
| **`.pth` 文件** | Python 的 site-packages 机制：目录下任何 `.pth` 文件会在**解释器启动时**被读取，其中 `import xxx` 形式的行会被执行。攻击者用它做到"装了就中招、不 import 也中招"，且删掉原包不会移除它。 |
| **`sitecustomize.py`** | Python 启动时若能在路径中找到就**自动导入**的模块，本意是站点级定制，因此常被用作持久化落点。本次事件中它承担第二阶段的远程代码拉取（每小时一次）。 |
| **Provenance（构建来源）** | 记录一个软件包"由哪个仓库、哪次构建、哪条流水线产出"的元数据。本次事件中 provenance **如实记录了仿冒 fork**，说明它能回答"从哪来"，但回答不了"该不该信"。 |
| **MFU（Model FLOPS Utilization）** | 模型浮点运算利用率，衡量训练时硬件算力被真正用于有效计算的比例。Google 自报在 Ironwood 上用 TorchTitan 训练 Qwen3 8B 达 **52%**——是自测数字，跨硬件不可直接横向比。 |
| **MoE（Mixture of Experts）** | 混合专家架构：总参数量大（Flint 40B），但每个 token 只激活其中一小部分（2.5B）。这正是"能在笔记本上跑"的原因——**显存与算力按激活参数算，不按总参数算**。 |
| **虚拟卡（Virtual Card）** | 由发卡/钱包方为单笔或受限场景生成的一次性或受限卡号。Duet 通过 Stripe Link 用它付款，使**真实卡号不暴露给商户也不暴露给 agent**。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
