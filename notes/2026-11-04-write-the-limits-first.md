# 2026-11-04｜写清边界的今天就能跑，写含糊的到期还是空仓库

> 四份可下载的文件都写明自己做不到什么；一句 "by Nov 4" 的承诺，到期日仍是空仓库。

**标签**：`#工程选型` `#开放权重` `#RAG` `#Agent治理` `#国产算力`
**生成时间**：2026-11-04 12:07（北京时间）

---

## 一、今日观察

今天把材料按「**有没有把限制写进产物**」重排一遍，会出现一条比按公司、按领域分组都整齐的分界线。

美团承认国产加速卡单卡显存不足 80GB，于是把并行度绑死在超节点上；RAGFlow 承认检索准确率已经饱和，于是放弃优化 retriever，转去做「供给什么上下文」；Anthropic 承认权重不能公开、也承认这个项目不会被维护，于是把适用范围写成 README 里的四条硬件路线；CrowdStrike 承认 agent 拿着合法凭证也会做没人授权的事，于是交付的不是「更安全」的承诺，而是一个能按下去了的开关。这四份东西今天都能下载、能跑、能核数字。

唯一没写清边界的是今天最响的那条：Kimi K3.1 Pro 官方博客只写了一句 **"Full model weights will be released by Nov 4, 2026."**，没写时区、平台、许可证。到了 11 月 4 日早晨的第三方实地核查，HF / GitHub / ModelScope 三处都还没有 K3.1 Pro 仓库；而多家聚合稿已经把它写成「今天正式开源全部权重」。

| 先承认的限制 | 谁把它写进产物 | 因此放弃了什么 | 今天能核到的东西 |
| :--- | :--- | :--- | :--- |
| 国产卡单卡显存 **不足 80GB** | 美团 LongCat-2.5（11-2 技术博客） | 通用的跨节点并行 | FSDP 单卡吞吐较 DDP **+86%**；W4A4 相对 W8A8 prefill/decode 吞吐 **+43.3% / +42.77%** |
| 检索已经够准（BM25+grep **91%**） | RAGFlow 知识编译论文（arXiv 2610.41172） | 不再追准确率 | 结构化工件**无可检测准确率增益**；claim-evidence 树平均省 **38%** query token；决策门 **140s→30s** |
| 权重必须保密、项目不维护 | Anthropic FlashProve 0.16.0 | 公开权重、长期支持 | 单张 H100 / 1024 token / 24 批 **~110 tok/s**；`cp_verify` CPU 秒级；可靠性在 **Lean 4** 里证明 |
| agent 拿合法凭证也会越权 | CrowdStrike（11-3 官方公告） | 「agent 不会失控」这种承诺 | **AI Kill Switch 今日可用**：终止进程、禁止重启、切断企业网、全程审计 |
| **没写清**：时区 / 平台 / 许可证 | Kimi K3.1 Pro "by Nov 4" | — | 官方原句一句；🟡 到期日早晨三平台仍无仓库 |

CrowdStrike 在同一批新闻稿的小字里写了一句几乎可以直接抄进选型规范的话：**"Customers should make their purchase decisions based upon features that are currently available."** 它把 Kill Switch 标成 "available today"，把 Falcon Observe 的 GA 排到 Q4 FY27，把 endpoint 侧终止写成 "soon"——三个时态写在同一天的稿子里。**把已交付和未交付分开写，本身就是一种工程能力。**

## 二、事实清单
> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

**1. Kimi K3.1 Pro 权重：承诺到期，三平台仍无仓库**　🟢 官方原句 / 🟡 平台状态
官方博客 Availability 段逐字写着 **"Full model weights will be released by Nov 4, 2026."**，全文**未写时区、发布平台、开源许可证**。两份独立核查（北京时间 **11-3 09:25** 与 **11-4 06:44**）分别查了 HF `moonshotai`、GitHub `MoonshotAI`、ModelScope，均**未见 K3.1 Pro 仓库**，最新开源模型仍是 9 月 2 日更新的 `Kimi-K3`；许可证未公布。⚠️ 官方未写时区，若按美西时间，交付可能落在北京时间 11-5；上述为核查时点状态，之后如已上线以官方仓库为准。另有聚合稿直接写成「今天正式开源全部权重」，与可核状态不符，本条不采信。
来源：[Kimi 官方博客](https://www.kimi.ai/blog/kimi-k3-1-pro) · [核查一（11-4 06:44）](http://mp.weixin.qq.com/s?__biz=Mzg2NzU4MDgzMA==&mid=2247567672&idx=1&sn=2089fd351740b1224a8bd1ba3bce0a0e) · [核查二（11-3 09:25）](http://mp.weixin.qq.com/s?__biz=MzY5MDQ5NDQ3OA==&mid=2247483734&idx=1&sn=66aebe0f4ce7e7dfa58f655a4dd15b53) · [HF 官方主页](https://huggingface.co/moonshotai) · [腾讯新闻本周看点（11-2 预告口径）](https://news.qq.com/rain/a/20261102A0C2E300) · [误写为「已开源」的聚合稿](https://post.m.smzdm.com/p/awwde3w2)

**2. 美团 LongCat-2.5：把 80GB 显存上限写进并行策略**　🟢
官方技术博客：**总参数 1.6 万亿 / 每 token 激活约 480 亿**，中训练与 SFT 采用最长 **1M token** 序列，累计训练量数万亿 token；针对国产卡单卡显存**不足 80GB**，FSDP 与 EP 并行度均与单超节点卡数一致，让通信留在超节点高速互联域内，长序列 SFT 单卡吞吐较 DDP 基线 **+86%**。W4A4 推理相对 W8A8 INT8 基线：prefill / decode 吞吐 **+43.3% / +42.77%**，TTFT / TPOT 降低 **15.91% / 19.72%**，GMM 算子平均 **1.73×**。模型已在 longcat.ai 与 API 上线；官方新闻页称多项主流基准成绩介于 Claude-Opus-4.8 与 Claude-Opus-5 之间（厂商自测，未引具体分值）。
来源：[美团技术博客](https://tech.meituan.com/2026/11/02/Meituan-LongCat-2.5.html) · [美团官方新闻](https://www.meituan.com/news/NN261102280001343) · [新华网 11-3](https://www.news.cn/tech/20261103/41b545db19f348038365821485069a8b/c.html) · [科技日报 11-3](https://www.stdaily.com/web/gdxw/2026-11/03/content_607278.html)

**3. RAGFlow「知识编译」：明确承认编译不是更好的检索器**　🟢
arXiv **2610.41172**（10-30 提交，13 页）摘要：仅用 BM25/grep + MiniMax M3 的 harness，在 BrowseComp-Plus 答对 **85%**、multi-hop FRAMES **91%**，没有编译索引也没有向量索引；结构化工件（导航树、实体图、时间线、wiki 等）在 FRAMES 上**没有可检测的准确率增益**，PageIndex 式大纲在规模上反而退化。真正被测的机制是「叶节点为断言-证据对」的导航树：证据够用时 query token **−91%**、不够时 **+1.9%**，平均 **−38%**；**2%** 为盈亏平衡充分率，实测接近 **43%**。决策门把延迟从 **140s 降到 30s**——省 token 是用检索轮数换的。⚠️ 该文为 10-30 预印本、本周转热，不是今日发布。
来源：[arXiv 摘要](https://arxiv.org/abs/2610.41172) · [RAGFlow GitHub](https://github.com/infiniflow/ragflow) · [InfoQ 解读（11-4）](https://xie.infoq.cn/article/9892eab0eeac4f19f61c2fe77)

**4. Anthropic FlashProve 0.16.0：连「不维护」都写在版本号旁边**　🟢
GitHub README 首行：**Version 0.16.0 · A research artifact: not maintained, not accepting contributions · Apache 2.0**。做法分三步：provider 发布 commitment ID 绑定一组权重（权重保密）、GPU 为每次回复生成证明、任何人用 `cp_verify` 在普通 CPU 上**秒级**验证。跑通满尺寸 **Llama 4 Maverick / 1024 token / 单张 H100**，24 请求批下 prefill **约 110 tok/s**；协议可靠性在 **Lean 4** 中形式化证明，作弊未被抓到的概率约 **q/2¹²⁴ + 2⁻¹⁰¹**。README 还写清了四条硬件路线（CPU 验证需 <2GB RAM、构建 1–2 分钟、校验 <2s；真实 Maverick 路线需 **330GB RAM / 245GB 磁盘 / 数小时**），并明确 **commitment ID 必须从可信方取得，不能来自被检查的服务器**。
来源：[GitHub README](https://github.com/anthropics/FlashProve) · [AI 技术日报 11-4](https://www.cnblogs.com/itech/p/23543093)

**5. CrowdStrike：把「agent 会越权」写成今天可按下的开关**　🟢（金额 🟡）
11-3 Fal.Con Europe 官方稿：**AI Kill Switch 今日可用**，管理员可在 agent 运行处终止进程、禁止其在目标主机重启、切断企业网络访问，操作全程进审计链。官方直陈 agent 拥有系统级权限，"**can take actions no one authorized, even when no adversary is involved**"。同日宣布已签署收购 Fiddler AI 的最终协议，Fiddler 将以 **Falcon Observe** 出售、**Q4 FY27** 才 GA；该稿 Transaction Details **只写「以现金为主 + 部分附归属条件股票」，未披露金额**。媒体口径的 **4.95 亿美元（Fiddler 约 4 亿 + Dreadnode 约 9500 万）** 未见官方数字，标 🟡。新闻稿小字另注明未发布功能 "still in development and subject to change"，并建议客户**按当前可用功能做采购决定**。
来源：[Kill Switch 官方稿](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-introduces-ai-kill-switch-for-ai-safety/) · [Fiddler 收购官方稿](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-to-acquire-fiddler-to-deliver-agent-observability/) · [官方 pressroom](https://www.crowdstrike.com/en-us/press-releases/) · [金额转述 🟡](https://k.sina.com.cn/article_5952915705_162d248f906703sdqg.html)

**6. 其余预告态与资本侧动向**　🟡（待官方源核实，不作既定事实）
- 腾讯混元 **Hy4 预览版**：Arena.ai 榜 **1.45 万次**真实智能体会话中开放模型第 2 / 综合第 10，净改善率 **5.4%**（Kimi K3 Max 为 6.6%），单任务中位成本 **$0.26 vs $0.80**（低约 **68%**）；正式版发布时间、参数与完整技术细节**均未公布**。来源：[凤凰网科技转述](https://app.myzaker.com/news/article.php?pk=6aea98abb15ec0371a69038f)
- 苹果智能接入千问：**11-4 起** iOS 开发者 Beta 测试，**12 月**随 iOS 27.3 正式推送，**不含下一代 Siri**。来源：[腾讯新闻本周看点](https://news.qq.com/rain/a/20261102A0C2E300)
- 资本侧：零一万物获杭州市 / 临平区两级国资**数亿元**投资、总部落地杭州临平（[中国经济新闻网 11-3](https://www.cet.com.cn/wzsy/cyzx/10644868.shtml)）；墨芯人工智能完成**近 10 亿元 C+ 轮**（[投资界转述 11-3](https://www.163.com/dy/article/LAQ3N0HE05198R3E.html)）。均为企业口径或媒体转述，未读公告原文。

## 三、为什么值得记

1. **「能不能下载」和「有没有写清边界」是同一件事的两面。** 今天四份可核查材料，全都把适用范围、硬件下限或自己不做的东西放在最显眼的位置；唯一被写成事实却没交付的那条，恰好连时区、平台、许可证三项都没定义。边界不是免责声明，是交付的一部分。
2. **RAGFlow 那句「编译不是更好的检索器」值得抄进任何 RAG 复盘。** 当 harness 已把 recall 做到 91%，继续调 chunk_size、换 embedding、上 GraphRAG 就都不再是决定性变量。它甚至诚实报告了代价：省 38% token 是靠多跑检索轮数换来的，延迟得额外加决策门才拉得回来。**只报收益不报代价的优化，大概率没做消融。**
3. **CrowdStrike 官方自己给出了选型纪律**：按已交付的功能做采购决定，不按 roadmap。Kill Switch 标 "available today"，Falcon Observe 排到 Q4 FY27，endpoint 侧终止写 "soon"——三个时态写在同一天的稿子里。反观今天不少聚合稿，把「by Nov 4」「即将发布」「开发者 Beta」直接写成了完成时。
4. **国产算力这条线的价值不在「也能训万亿模型」，在它把硬件限制翻译成了架构。** 单卡显存不足 80GB → 并行度对齐超节点 → W4A4 全链路 INT4。这些是可迁移的工程模式，而「跑分介于哪两个闭源模型之间」不是。

## 四、可行动

- [ ] **今天就去核一次权重状态**：打开 `huggingface.co/moonshotai`，只认 `moonshotai/` 前缀的仓库，下载前先读 LICENSE 与模型卡；名字里带 `unrestricted` 的第三方仓库不要碰。
- [ ] **给自己的技术选型表加一列「状态」**：只填 `available today` / `preview` / `beta` / `announced` 四种值，禁止把 `announced` 当成可部署依赖；引用分数时同时记录 benchmark 版本与 harness。
- [ ] **RAG 流水线先跑一次极简对照**：BM25+grep 的 baseline 打一遍 golden set，再决定要不要上向量库 / GraphRAG；若采用「断言-证据对」，务必同时量 token 与端到端延迟，并加一个「证据是否够」的决策门。
- [ ] **按 CrowdStrike 那三步自查 agent 运行时**：能否在它运行的地方终止进程、能否阻止重启、能否单独断网；三个动作是否都留审计记录。缺任一项就别放它拿生产凭证。
- [ ] **想验「API 背后是哪个模型」可先跑 FlashProve 的 CPU 路线**：`verifier/build.sh` 后用 `bin/cp_verify` 校验仓库里的示例证明（<2GB RAM、校验 <2s），确认末行 `YES` 与退出码 0；注意 README 明说示例只证明验证器能跑，不证明任何线上服务。

## 五、术语卡

| 术语 | 解释 |
| :--- | :--- |
| **W4A4** | 权重（Weight）与激活（Activation）同时量化到 4 bit 的推理方案；相对 W8A8 省带宽与显存，但需硬件有原生 INT4 矩阵乘单元，并靠等价变换（如 FlatQuant）补回精度。 |
| **知识编译（Knowledge Compilation）** | RAGFlow 论文提出的概念：在摄入期用 LLM 为文档补上 chunk 本身没有的上下文（导航树、实体图、时间线、断言-证据对等）。它是「上下文供给层」，不是更好的检索器。 |
| **Harness** | 包住模型的执行框架：自己写查询、读结果、改写、决定何时收工。ReAct / DeepResearch 类系统里，检索不再是一次 query→相似度调用。 |
| **AI Kill Switch** | 由管理员触发、可在 agent 运行处终止其进程并切断企业网络访问的控制开关；CrowdStrike 将其放进 Falcon Guardian，并强调全程写入审计链。 |
| **Commitment ID** | 零知识推理证明里 provider 先发布的标识，把服务绑定到某一组权重而不公开权重本身；验证方必须从可信第三方取得，不能从被检查的服务端拿。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
