# 2026-11-16｜进门看门牌，付钱用令牌

> 美国时间 11-13 一天之内，agent 商业化最后一段路被拆成两半各自交付：Poppy v1.0 发门牌，ChatGPT Wallet 发令牌。

**标签**：`#Agent` `#AgenticCommerce` `#支付` `#DeepSeek` `#AnthropicIPO`
**生成时间**：2026-11-16 09:44（北京时间）

---

## 一、今日观察

过去两个月这条笔记线写过两次"最后一公里"：**10-19** 写的是网站成片对 agent 关门——"能替你做事"是一张一张白名单谈出来的；**10-22** 写的是 Duet 配齐了机器、记忆和钱包，但那是**一家产品的单点方案**（Stripe Link 虚拟卡 + Shop Pay）。

美国时间 11-13 这一天，两半路同时从"单点方案"变成了"制度接口"：Sierra 和 Meta 发 **Poppy v1.0**（进门），OpenAI 发 **ChatGPT Wallet**（付钱）。同一天，DeepSeek 把"开放"从权重推进到整套产品能力，Anthropic 敲定 IPO 区间。按"最后一公里拆成几段"重新排，比按公司排清晰得多：

| 拆出的环节 | 今天谁交付 | 一个月前的状态 | 留下来的制度接口 |
| :--- | :--- | :--- | :--- |
| **进门：身份与权限** | Sierra + Meta，Poppy **v1.0** | 网站成片关门，逐家谈白名单 | `/.well-known/poppy` 发现文件 + OAuth 双向授权；Shopify 全量自动发布 |
| **付钱：资金流** | OpenAI，**ChatGPT Wallet** | Duet 的 Stripe Link 虚拟卡（单点） | 三大卡组织共建 + 每笔生物识别 + 一次性支付令牌 |
| **复用：能力分发** | DeepSeek，**全家桶 API** | 开放权重，工具链自己搭 | 参数化工具调用 + 独立计费的 Search / Fetch / OCR / ASR / TTS |
| **买单：资本市场** | Anthropic **IPO 定价区间** | 私募市场定价（最后一轮约 $58.90/股，🟡 经媒体转引） | $70–78/股、代码 ANT、11-19 纳斯达克挂牌 |

关键变化不是哪个功能更强，而是**"谈"变成了"装"**：Poppy 给每家公司一条自助开门路径（实现包 + 校验器 + 分阶段接入），不需要再等哪家 agent 厂商上门谈判；Wallet 把"替人付钱"钉进卡组织的标准流程，而不是某家产品的临场发挥。而 OpenAI 自己承认的那句"部分网站可能误拦 Wallet 付款、风控可能把合法 agent 订单标为欺诈"，提醒我们：**接口上线是一天的事，两端风控对齐是几个月的事。**

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Sierra + Meta 发布 Personal Agent Protocol（Poppy）v1.0

**11-13**（Sierra 官方博客）。核心机制：接入企业在标准路径 `/.well-known/poppy` 放发现文件，agent 到站先读门牌再动手；鉴权走 **OAuth**，客户可随时管理授权范围；协议大量复用现有标准（**MCP、OpenAPI、UCP**），不另造轮子。当日要点：

- **Shopify 为平台上所有商户自动发布 Poppy 文件**，覆盖 **175+ 国家**，商户零配置；
- 设计伙伴新增 60 家、**总数超 100 家**（Delta、Hyatt、Wayfair、Intuit、Salesforce、Turkish Airlines、Checkout.com、Global Payments 等）；初始伙伴为 Meta、Genesys、Instinct、NiCE、Rocket、Shopify、Stripe、Walmart（**10-06** 首次公布）；
- **已上线跑通**：Mercury（查余额、交易分类、发起支付/转账——走账户自身审批流）、Turkish Airlines（查票价、按预订号调行程，升级商务舱需客户批准后付款）、Synchrony；
- Shopify 共同撰写 **commerce extension** 连接 UCP：agent 可游客或登录身份购物，**某些动作前必须先问客户**；Meta 的 Muse 在每个站点默认优先查找 Poppy；
- v1.0 规格与实现包（含校验器）已公开。

来源：[Releasing Personal Agent Protocol 1.0（Sierra 官方博客）](https://sierra.ai/blog/releasing-poppy)｜[v1.0 规格原文](https://personalagentprotocol.org/docs/1.0/spec)｜[10-06 首次公告](https://sierra.ai/blog/introducing-personal-agent-protocol)

### 2. 🟢 OpenAI 推出 ChatGPT Wallet：dot 付钱全程不见真实卡号

**11-13**（美国时间周五）官宣。首批面向**美国年满 18 岁的 Pro 订阅用户**，与 **American Express、Mastercard、Visa** 三大卡组织共同开发：

- 流程：dot 比价、加购物车、备好结账页 → **停下交还人类** → 用户核对商品、总额与所用卡 → **Face ID / 指纹逐笔批准** → 卡组织网络下发**一次性支付令牌**（临时卡号 + 独立安全码与有效期）→ 商家用令牌收款；**agent 与商户全程接触不到真实卡号**；
- 卡的积分与争议保护保留；OpenAI 称**初期不抽取交易佣金**；
- **官方自认两个坑**：部分网站可能无意拦截 Wallet 付款；商户风控可能把合法 agent 订单当欺诈。配套发布了商家 playbook，防欺诈与支付合作方含 Stripe、Adyen、Checkout.com；
- 未来方向：在用户预设的**限额 / 品类 / 时间窗**内预授权。

来源：[CNBC（经美国中文电视转述）](https://weibo.com/1885985453/RriZA37wI)｜[Precise Impact 11-14 简报（引 CNBC）](https://www.preciseimpact.ai/briefing/ai-news-digest-2026-11-14)｜[Bots n' Beans（含 OpenAI 官方口径转引）](https://botsnbeans.com/news/chatgpt-wallet-dots-pay-muse-poppy-checkout)

### 3. 🟢 DeepSeek 开放"全家桶应用 API"：从开放权重走向服务化

**11-13**（北京时间晚间）公告。V4.1-Flash 在 **Messages / Responses / Chat Completions** 三类接口下支持：联网搜索（思考模式下可在多步推理中自主搜索并读链接）、文件输入（PDF / Office / 图片）、链接阅读、安全校验参数；同时把 **Search、Fetch、OCR、ASR、TTS** 开放为独立接口，可单独或组合调用。计费（token 费之外另收）：

- **文字/图片搜索与网页抓取各 5 元/千次、OCR 1.5 元/千页、语音识别 0.39 元/小时、语音合成 1.5 元/万字符**（ASR/TTS 限时 5 折）；
- 基于新版 API 开源了轻量前端 Demo（`github.com/deepseek-ai/chat-demo`），可导入 App 历史对话，官方称开发者可"**1:1 复刻完整的 DeepSeek App**"；
- 对外提供服务需开启安全校验参数，并自行承担内容审核、大模型登记、AI 标识等义务。

来源：[澎湃新闻](https://m.thepaper.cn/newsDetail_forward_34470944)｜[北京商报](https://www.bbtnews.com.cn/2026/1114/611243.shtml)｜[智东西（含官方价目表）](https://news.qq.com/rain/a/20261115A0C1KM00)

### 4. 🟢 Gemini 4 Hydrogen 发布：专管"快速执行"的速度档，🟡 跑分待核官方原文

**11-13/14** 多源报道。基于 Carbon 改编，定位**高速 agentic 执行**（写代码、跑测试、日常任务），深度长推理仍留给 Carbon / Argon：

- **1M token 上下文，全窗口统一价 $1.50 / $7.50 每百万输入/输出**；四档思考层级 low / medium / high / **xhigh（新增超高档）**，默认 high；
- 官方口径：相比 Gemini 3.8 Flash，high 档**任务完成快 2.5 倍**；即日全量上线并**集成进 Google 搜索**，另覆盖 Gemini 应用、AI Studio、API 与 Antigravity；
- Antigravity 上线 **Orchestrator**：同一会话可在 Carbon、Hydrogen 间动态切换，任务成功率接近 Carbon、速度快 19%、少耗 24% 配额；
- 🟡 聚合日报给出的跑分（Artificial Analysis 智能指数 high 档 51 分、超 Argon 的 50；xhigh 达 54；Terminal-Bench 4.1 从 18.2% → 57%）**未核到官方博客原文，暂不作为既定事实**。

来源：[网易/ZAKER（转 Google 官方口径）](https://www.163.com/dy/article/LBMLHLLV0550A7YJ.html)｜[聚合日报 lininn（跑分出处，🟡）](https://lininn.cn/page/ai-daily-2026-11-14-morning)｜[CSDN 每日简报（引 VentureBeat）](https://blog.csdn.net/debug_fan/article/details/170816344)

### 5. 🟢 Anthropic IPO 敲定：$70–78/股，11-19 挂牌，估值最高约 $1.4 万亿

**11-18 定价、11-19 纳斯达克挂牌**，代码 **ANT**。发行 **8.25 亿股**，区间 **$70–78**；完全稀释估值最高约 **1.4 万亿美元**（不计选择权与限制型股票约 1 万亿），明显低于此前市场一度预期的约 2 万亿；另有约 **260 亿美元**私募。招股文件两个值得记住的口径：

- **前九个月营收 332 亿美元，同比 +1206%**；已签约的算力及基础设施支出承诺总额高达约 **8,954 亿美元**；
- 前九个月收入中有 **5%–7% 来自此后会被认定为不合规的客户群体**——上市披露要求下被重点管控的风险敞口。

来源：[重庆日报（引市场资讯）](https://www.cqrb.cn/caijingzonghe/2026-11-13/2820557_pc.html)｜[富联网](https://moneylink.com.tw/RealtimeNews/NewsContent.aspx?SN=2445156002)｜[腾讯新闻（引《财富》）](https://news.qq.com/rain/a/20261115A0CALV00)

## 三、为什么值得记

1. **制度化的门槛跨越，比能力提升更值得记。** 10-19 的结论是"'能不能动'一张一张白名单谈出来的"；Poppy 的意义在于把"谈"变成了"装"——任何公司今天都可以自己放一个发现文件、跑一遍官方校验器，不需要等哪家 agent 厂商上门。覆盖面从"名单上那几家"变成"所有愿意放文件的人"，这才是协议与集成的区别。
2. **付钱这一半的设计哲学可以直接抄。** 逐笔批准起步（而不是先做预授权）、一次性令牌替代真实卡号、agent 与商户**双重不可见**、每次审批留痕。这与 10-22 从 Duet 抄的"不做清单"是同一思路，但这次是卡组织级的标准动作，不是某家产品的临场发挥——标准动作的好处是**争议责任的分配已经有成熟先例**（chargeback）。
3. **最诚实的细节是 OpenAI 承认风控错位。** 路修通了，但商户风控会把合法 agent 订单当欺诈、部分网站会误拦——**"功能发布"不等于"落地完成"**。做 agent 集成的人应该把这条写进预期管理：协议可用之后，真正的工期花在对齐两端的 fraud 规则上。
4. **三种"开放"在同一天给出了三种账单。** Poppy 收的是信任（OAuth 授权粒度），Wallet 收的是通道（暂时免佣，方向是生态位），DeepSeek 收的是工具调用次数（搜索/抓取 5 元/千次）——**开放从来不是免费，只是换了计费单位**。选型时该问的不是"谁更开放"，而是"它的开放按什么单位向我收钱"。

## 四、可行动

- [ ] **读一遍 Poppy v1.0 规格**（personalagentprotocol.org/docs/1.0/spec），并用官方 implementation kit 里的 validator 给自己的站点/API 起草一份 `/.well-known/poppy` 文件——体验"被 agent 找到"到底需要声明哪些端点与权限边界。
- [ ] **如果你有 Shopify 店铺，先审计再集成**：店铺已自动发布 Poppy 文件，先检查它对外暴露了哪些端点、哪些动作要求先问客户，再决定要不要接 agent 流量。
- [ ] **用 DeepSeek 开源 chat-demo 搭一套自己的对话应用**，实测并记录**工具调用费与 token 费的占比**——搜索与抓取都是 5 元/千次，搜索型应用的账单结构会因这次开放而改变，值得先算一笔。
- [ ] **把三条支付设计抄进你的 agent**：逐笔人工批准、一次性令牌、agent 全程不见真实卡号。商家侧则反过来：检查风控规则会不会把 Wallet 订单误判为欺诈（OpenAI 自己承认这是现状）。
- [ ] **11-18/11-19 盯 Anthropic 定价与首日表现**，把它当 AI 板块的信心指标；顺带记住招股书里"5%–7% 收入来自此后会被认定为不合规客户"这个口径——做合规预算时用得上。

## 五、术语卡

| 术语 | 解释 |
| :--- | :--- |
| **`/.well-known` 发现文件** | IETF 约定的标准路径前缀，网站把机器可读的元信息放在这个固定位置供自动发现（如 `/.well-known/acme-challenge`）。Poppy 把"本店允许 agent 做什么"的清单放在 `/.well-known/poppy`，agent 到站先读门牌再动手。 |
| **一次性支付令牌（payment token）** | 卡组织网络为单笔交易发行的替代凭据（临时卡号 + 独立安全码与有效期）。商户用它收款，**拿不到真实卡号**；agent 侧同样不可见。ChatGPT Wallet 的安全设计核心。 |
| **UCP（Universal Commerce Protocol）** | 管购物动作本身的协议（找商品、加购物车、结账）。Poppy 只管"进门"之前的事——自报身份、获知权限；两者由 Shopify 共同撰写的 commerce extension 连接，分工明确不重叠。 |
| **双向授权** | Poppy 的权限模型：用户侧决定给 agent 只读还是可交易，企业侧决定外部 agent 在自家系统里最多能走多远——**两边都点头，一次交互才成立**。与 OAuth 的委托授权机制兼容。 |
| **服务化开放** | 与"开放权重"相对：不改一版模型，而是把产品背后的整套能力（搜索、抓取、OCR、语音）做成带计费的 API。DeepSeek 这次的关键点——权重照样开源，但**复用产品形态要按调用次数付费**。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
