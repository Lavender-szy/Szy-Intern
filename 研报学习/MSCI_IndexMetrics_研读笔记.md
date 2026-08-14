	——用一套统一“体检表”回答：一个指数到底**赚了什么、暴露了什么、承担了什么风险、能不能真的投**
# 1.核心术语
1. **IndexMetrics**：MSCI 用于统一评价指数的分析框架，把指数从**绩效、暴露、风险、可投资性**等角度拆开检查
2. **主动收益 Active Return**：指数收益 - 基准收益
3. **主动暴露 Active Exposure**：指数相对于母指数/基准多暴露或少暴露了什么
4. **FaCS 因子暴露**：用标准差表示组合相对基准的因子倾斜强度
5. **Active Share**：指数持仓权重相对基准到底改了多少
6. **有效成分股数量 Effective Number of Constituents**：不是“有多少股票”，而是考虑权重后，组合相当于多少只股票等权持有
7. **Weight Multiplier**：某股票在策略指数里的权重÷它在基准里的权重
8. **ATVR**：年化成交金额比率，用于衡量流动性
9. **Days to Trade**：在资金规模和每日成交限制下，需要几天才能完成建仓/调仓
10. **Performance Drag**：由指数换手和假设交易成本估算的收益拖累
11. **Sortino Ratio**：类似夏普，但只惩罚下行波动
12. **VaR / CVaR**：一个看“坏到什么门槛”，一个看“突破门槛后平均还能坏到哪里”

# 2.这篇研报在解决什么问题
前面两篇：
- [[研报——因子投资的基础]]：**因子是什么**
- [[机构投资组合中的多因子指数配置]]：**多个因子怎样组合、怎样落地**

这一篇继续往后一步：

==已经有很多因子指数、ESG指数、主题指数了，怎么判断一只指数到底好不好？==

不能只比：
- 谁历史收益最高；
- 谁回测曲线最好看。

还要同时回答：
1. **收益怎么样？**
2. **为什么会有这些收益？**
3. **实际暴露的是不是我想要的东西？**
4. **承担了什么绝对风险、相对风险、尾部风险？**
5. **大资金能不能真的复制？成本多高？**

所以 MSCI 做了一个统一的“指数体检框架”——**IndexMetrics**。

# 3.IndexMetrics的整体框架
[此处插入研报原图：Exhibit 1「MSCI IndexMetrics框架的指标分组」]

可以把 IndexMetrics 理解成四张体检单：

## 3.1 Key Metrics：先看全貌
回答：
- 赚了多少；
- 波动多大；
- 相对基准多赚多少；
- 为了多赚这些，偏离基准有多大；
- 换手大不大；
- 估值大概什么水平。

主要指标：
- Total Return
- Total Risk
- Return/Risk
- Sharpe Ratio
- Active Return
- Tracking Error
- Information Ratio
- Historical Beta
- Number of Constituents
- Turnover
- P/B、P/E、Dividend Yield

## 3.2 Exposure：到底买到了什么
看：
- 因子暴露；
- 行业暴露；
- 国家/地区暴露；
- 大中小盘暴露；
- 基本面；
- ESG；
- 气候变化。

## 3.3 Performance：收益从哪里来
不是只看：
**最终赚了3%超额收益**

而是继续拆：
- 因子贡献多少；
- 行业贡献多少；
- 国家贡献多少；
- 个股选择贡献多少；
- 哪些具体股票贡献最大。

## 3.4 Investability：理论上好，现实里能不能买
看：
- 集中度；
- 容量；
- 流动性；
- 换手；
- 复制成本；
- 大资金完成交易需要多少天。

==IndexMetrics = 收益结果 + 收益来源 + 风险路径 + 真实实施难度==

# 4.Key Metrics怎么读
## 4.1 Total Return vs Active Return
### Total Return
不管基准，指数自己赚多少。

### Active Return
$$
\text{主动收益}=\text{指数收益}-\text{基准收益}
$$

eg.
- 指数年化8%
- 基准年化5%

主动收益=3%

**主动收益回答的是：这套规则相对“直接买市场”到底多赚了多少。**

## 4.2 Total Risk vs Tracking Error
### Total Risk
指数自己的波动。

### Tracking Error
$$
TE=\text{主动收益序列的年化标准差}
$$

看的是：
**指数相对基准的领先/落后有多不稳定。**

- 总风险：我自己的净值抖不抖
- 跟踪误差：我相对基准抖不抖

## 4.3 Return/Risk
$$
\text{Return/Risk}=\frac{\text{年化总收益}}{\text{年化总风险}}
$$

缺点：
- 没扣无风险收益

所以更标准的是夏普比率。

## 4.4 Sharpe Ratio
$$
\text{Sharpe}=\frac{\text{指数收益}-\text{无风险收益}}{\text{总风险}}
$$

问题：
**承担全部组合风险后，超过无风险资产的收益值不值？**

## 4.5 Information Ratio
$$
IR=\frac{\text{主动收益}}{\text{跟踪误差}}
$$

问题：
**为了偏离基准，我每承担1单位主动风险，换来了多少超额收益？**

- Sharpe：站在“持有这个组合本身”的角度
- IR：站在“相对基准做主动偏离”的角度

## 4.6 Historical Beta
$$
\beta=\rho_{P,B}\times\frac{\sigma_P}{\sigma_B}
$$

Beta：
- 1：和基准敏感度差不多
- >1：市场涨跌时反应更大
- <1：对市场波动更钝

# 5.研报里的七个因子指数结果
[此处插入研报原图：Exhibit 3「MSCI ACWI Factor Indexes — Key Metrics」]

[此处插入研报原图：Exhibit 4「Relative Performance」]

样本：
1998.12.31—2020.3.31

研报比较：
- Enhanced Value
- Equal Weighted
- Momentum
- Quality
- High Dividend Yield
- Minimum Volatility
- Diversified Multi-Factor（DMF）
vs MSCI ACWI

值得记的不是“谁第一”，而是：

### 1.样本期内七个策略都跑赢了市场
同时：
- Sharpe普遍高于基准
- IR为正

==仅代表这一历史样本，不代表未来。==

### 2.动量很贵
Momentum：
- 主动收益：3.3%
- 跟踪误差：8.0%
- IR：0.42
- ==年化单边换手率：92.8%==

原因：
动量信号衰减很快，要不断更新持仓。

### 3.DMF的重点是“效率”
DMF：
- 主动收益：3.4%
- 跟踪误差：3.9%
- ==IR：0.87，全表最高==
- 换手率：40.1%

说明：
它不是单纯追求某一个最强因子，而是通过分散多个因子，让主动收益相对更稳定。

和上一篇对应：
==多因子的价值经常体现在“更稳定地获得超额收益”，而不是把收益最高的因子全部叠加。==

# 6.Exposure：不能相信指数名字，要验货
## 6.1 因子暴露怎么看
MSCI FaCS把主动因子暴露表示成：
**相对母指数偏离多少个标准差**

经验阈值：
- > +0.2：显著正暴露
- < -0.2：显著负暴露

[此处插入研报原图：Exhibit 5「Factor Box」]

eg.
- Enhanced Value：Value暴露最高
- High Dividend Yield：Yield暴露最高

这一步是在确认：
**“叫价值指数的，真的更价值吗？”**

## 6.2 多因子指数到底暴露了什么
[此处插入研报原图：Exhibit 6「DMF Active Factor Group Exposures」]

DMF主要目标：
- **低规模 Low Size**
- **动量 Momentum**
- **质量 Quality**
- **价值 Value**

历史上这四个也是平均暴露最明显的因子组。

其他因子会被约束：
- 半年指数审议时，非目标因子暴露通常控制在约0.25以内

==构建多因子指数，不只是把四个因子“加起来”，还要控制不想要的第五、第六种暴露。==

## 6.3 为什么还要看行业暴露
[此处插入研报原图：Exhibit 7「DMF vs Momentum主动行业权重」]

对比：
### DMF
- 优化构建
- 明确限制行业偏离
- 历史行业主动权重更稳定

### Momentum
- 规则更直接
- 没有同等强度的行业约束
- 行业主动权重波动明显更大

所以：
**同样是获得因子收益，一个策略可能顺便赌了行业，另一个没有。**

==目标因子暴露 ≠ 全部风险来源==

# 7.基本面指标：给因子标签做第二次验货
IndexMetrics还看：
- P/B
- Price/Cash Earnings
- P/E
- Dividend Yield
- 长期EPS增长
- Sustainable Growth
- ROE
- Debt/Equity

[此处插入研报原图：Exhibit 9「Financial Ratios」]

### Value
Enhanced Value平均P/B：
- 1.0

ACWI：
- 2.2

说明确实更便宜。

### Quality
Debt/Equity：
- Quality：约0.5
- DMF：约0.7
- 市场：约1.9

说明质量/多因子组合历史上杠杆更低。

### High Dividend
股息率：
- High Dividend：4.0%
- ACWI：2.3%

==风险模型告诉我“因子暴露”，财务比率告诉我“这些暴露在真实公司特征里长什么样”。==

# 8.ESG部分怎么理解
这篇研报已经不只评价因子指数，也把同一框架扩展到了ESG和气候指数。

## 8.1 ESG Score
0—10：
- 10最好
- 0最差

看的是：
公司相对同行，管理**财务上重要的ESG风险与机会**的能力。

公司最终映射为：
AAA → AA → A → BBB → BB → B → CCC

## 8.2 ESG Leaders / Laggards
### ESG Leaders
指数中AAA/AA公司的权重

### ESG Laggards
指数中B/CCC公司的权重

## 8.3 ESG Trend
- Positive：过去一年评级升级公司权重
- Negative：过去一年评级降级公司权重

## 8.4 Values & Norms
还会看：
- 烟草
- 民用枪械
- 争议性武器
- 联合国全球契约违规
- Red Flag
- Orange Flag

[此处插入研报原图：Exhibit 11「ACWI ESG Leaders vs ACWI」]

截至2020.3：
- ESG Score：7.1 vs 6.0
- ESG Leaders权重：46.6% vs 27.4%
- ESG Laggards：0% vs 7.7%
- 指数评级：AA vs A

说明：
**不能只看指数名字里有没有“ESG”，要量化它到底改善了多少。**

# 9.气候变化指标
气候部分可以分成四类：

## 9.1 Carbon Footprint：现在排多少
- Carbon Emissions
- Carbon Intensity
- Weighted Average Carbon Intensity

### Carbon Emissions
每投入100万美元对应多少吨CO2e

### Carbon Intensity
每100万美元销售额对应多少吨CO2e

一个偏：
**投资组合碳足迹**

一个偏：
**公司经营活动的碳效率**

## 9.2 Transition Risk：以后转型难不难
- Low Carbon Transition Score
- Solutions
- Product & Operational Transition
- Asset Stranding

### Asset Stranding
未来政策/技术/需求变化后，一些高碳资产可能失去经济价值。

eg.
煤矿、油气储备原来是资产，
低碳转型后可能无法按原计划变现。

## 9.3 Clean Technology：有没有转型机会
五类：
- 替代能源
- 能源效率
- 绿色建筑
- 污染防治
- 可持续水资源

### Green/Brown Net Revenue Exposure
$$
\text{绿/棕收入比}
=
\frac{\text{清洁技术收入}}
{\text{化石能源相关收入}}
$$

越高：
组合收入来源相对更“绿”。

## 9.4 两种低碳指数不是一回事
[此处插入研报原图：Exhibit 13「Low Carbon Target & Climate Change」]

### Low Carbon Target
重点：
**直接压低碳足迹和化石燃料储备暴露，同时控制跟踪误差**

2020.3：
- Carbon Emissions：32 vs ACWI 166
- Potential Carbon Emissions：16 vs 3763

### Climate Change Index
重点：
不只是“少买高碳公司”，还根据低碳转型：
- 加码可能受益的公司
- 减少转型风险高的公司

==Low Carbon更像“减碳”，Climate Change更像“围绕转型重新定价”。==

# 10.Performance Attribution：超额收益到底从哪来
[此处插入研报原图：Exhibit 14「DMF Performance Attribution Tree」]

DMF样本：
1998.12—2020.3

- 总收益：8.11%
- 基准：4.73%
- 主动收益：3.37%

继续拆主动收益：
- Currency
- Common Factors
- Asset Selection

其中最大来源：
**Common Factors**

继续拆：
- 国家
- 行业
- Risk Indices / Style Factors

风格因子贡献：
==约3.12%==

进一步发现：
主要来自方法论明确想要的：
- Value
- Low Size
- Momentum
- Quality

这一步很重要：

**好的结果 ≠ 好的方法**

还要问：
> 我赚的钱，真的是我原本想承担的因子风险赚的吗？

如果一个“质量指数”最后主要靠：
- 超配科技；
- 赌某个国家；
- 少数几只股票；

那即使收益很好，也不一定说明质量因子本身有效。

# 11.个股贡献
[此处插入研报原图：Exhibit 16「Top and Bottom Contributions」]

近似：
$$
\text{个股主动贡献}
\approx
\text{主动权重}\times\text{个股主动收益}
$$

作用：
- 谁把最近3个月的超额收益推上去了？
- 谁拖了后腿？
- 是广泛因子效果，还是少数股票偶然贡献？

==绩效归因就是把“结果”一层层倒回去找原因。==

# 12.风险不能只看波动率
## 12.1 Downside Deviation
只看负收益的波动。

Sharpe的问题：
- 上涨很多也会提高波动率

Sortino只问：
**坏波动有多大。**

## 12.2 Sortino Ratio
IndexMetrics设最低可接受收益=0：

$$
\text{Sortino}
=
\frac{\text{年化收益}}
{\text{下行波动}}
$$

- Sharpe：所有波动都惩罚
- Sortino：只惩罚下跌方向

## 12.3 VaR
95% VaR=-8%

含义：
历史上大约5%的月份，亏损超过8%。

注意：
**VaR只告诉你门槛，不告诉你门槛之外有多惨。**

## 12.4 CVaR / Expected Shortfall
如果：
- VaR95%=-8%
- CVaR95%=-12%

意思：
落入最差5%的月份后，平均亏约12%。

==VaR：坏事从哪里开始  
CVaR：坏事发生以后平均有多坏==

## 12.5 Maximum Drawdown
最大峰值→谷底跌幅。

## 12.6 Drawdown Period
跌下去多久才走出这一段回撤。

这个对机构非常重要：
- 亏20%但3个月恢复
- vs
- 相对基准每年差一点但连续10年

心理和治理压力完全不同。

# 13.长期赢，也可能连续十年跑输
[此处插入研报原图：Exhibit 18「Key Risk Metrics」]

Minimum Volatility：
- 总风险：10.4%
- ACWI：15.5%
- 下行波动、VaR、CVaR也更低

符合它的设计目标。

但最值得记的是Enhanced Value：

虽然长期样本最终表现很好，
==最大主动回撤持续期达到125个月==

超过10年。

High Dividend：
- 最大主动回撤持续期只有10个月

这和上一篇的“职业风险”完全对应：

**长期因子溢价存在**
≠
**投资委员会有能力等到它兑现**

# 14.可投资性：因子不是越纯越好
这一点和上一篇直接衔接：

[[机构投资组合中的多因子指数配置#4.3.1 因子暴露 vs 可投资性]]

基本关系：

因子暴露↑  
→ 偏离市值加权↑  
→ 集中度可能↑  
→ 容量↓  
→ 流动性压力↑  
→ 交易成本↑

==研究里的最佳因子组合，不一定是现实资金里的最佳指数。==

# 15.集中度不能只数股票数量
## 15.1 Average Number of Constituents
有多少只股票。

但问题：
100只股票中：
- 第一只占80%
- 另外99只一共20%

你不能说它“很分散”。

所以要看：

## 15.2 Effective Number of Constituents
$$
N_{\text{eff}}
=
\frac{1}{\sum_i w_i^2}
$$

直觉：
**把现在这套不等权组合，换算成“相当于多少只股票等权”。**

- 越高：越分散
- 越低：越集中

eg.
两只股票：
- 50% / 50%

$$
N_{\text{eff}}=\frac{1}{0.5^2+0.5^2}=2
$$

如果：
- 90% / 10%

$$
N_{\text{eff}}
=\frac{1}{0.9^2+0.1^2}
\approx1.22
$$

虽然名义上2只股票，
实际上接近“1只多一点”。

# 16.Parent Index Coverage
衡量：
**我的因子指数选出来的股票，在母指数里原本覆盖了多少权重。**

覆盖率高：
- 和母指数重合多

覆盖率低：
- 只选了母指数里较小的一部分
- 主动倾斜通常更强

DMF平均覆盖率：
==11.9%==

说明：
虽然有约689只成分股，但它实际上聚焦在母指数中较小的一部分权重。

# 17.Active Share
$$
AS
=
\frac12\sum_i|w_i^{指数}-w_i^{基准}|
$$

直觉：
**如果我从基准变成这只指数，到底需要重新挪动多少权重。**

- 0%：完全一样
- 越接近100%：差异越大

DMF：
==Active Share约88.8%==

说明相对ACWI倾斜非常明显。

注意：
Active Share高 ≠ 一定更好  
只是说明：
**更不像基准**

# 18.Weight Multiplier
$$
WM_i=\frac{w_i^{指数}}{w_i^{基准}}
$$

eg.
某股票：
- 基准权重0.2%
- 因子指数权重1%

Weight Multiplier=5

说明：
这只股票被放大到基准的5倍。

用途：
- 找出极端超配
- 判断容量
- 判断集中度
- 看策略有没有因为因子打分把某些小权重股票放太大

# 19.Capacity：资金规模上去之后还能不能做
Stock Ownership：

$$
\text{持有比例}
=
\frac{\text{指数权重}\times\text{基金规模}}
{\text{股票市值}}
$$

可以用：
- Full Market Cap
- Free Float Market Cap

eg.
基金100亿美元，
某股票指数权重2%：

要买2亿美元。

如果这只股票自由流通市值只有20亿美元：
基金就要持有它自由流通盘的10%。

资金继续放大：
- 冲击成本↑
- 建仓难度↑
- 指数容量下降

==容量不是指数的固定属性，它和“你有多少钱”直接相关。==

# 20.Days to Trade：可投资性里非常实用的指标
IndexMetrics默认：
- Fund Size：100亿美元
- 每只股票每天最多交易其日流动性的20%

然后问：
**需要多少天把组合调整完成？**

三种情形：

## 20.1 Relative to Benchmark
从基准组合→因子指数

用于：
机构原来持有ACWI，
现在准备切换成因子策略。

## 20.2 Periodic Index Review
再平衡前→再平衡后

用于：
每次指数调仓时真实要交易多少。

## 20.3 Relative to Cash
现金→指数

用于：
全新建仓。

每一种都看：
- 平均
- 95分位
- 最大值
- 完成95%交易量需要多久

==平均交易0.5天，不代表组合0.5天就全部搞定。尾部几只难交易股票可能拖很久。==

# 21.ATVR
ATVR：
Annualized Traded Value Ratio

衡量证券年化成交活跃程度。

IndexMetrics看：
**成分股ATVR的加权平均**

一般：
ATVR越高
→ 流动性越好

但不能只看ATVR，
还要结合：
- 你的资金规模
- 指数权重
- 换手
- 尾部Days to Trade

# 22.Turnover和复制成本
## 22.1 单边换手
$$
\text{Turnover}
=
\frac12
\sum_i|w_{i,\text{after}}-w_{i,\text{before}}|
$$

### 为什么有1/2
因为：
总权重增加=总权重减少

如果直接把买卖绝对变化都加起来，
同一笔资产迁移会被算两遍。

所以乘1/2得到单边换手。

## 22.2 Performance Drag
附录给出的估算：

$$
\text{Performance Drag}
=
2\times
\text{单边换手率}
\times
\text{单边交易成本}
$$

eg.
Momentum：
- 换手92.8%
- 假设单边交易成本50bp

$$
2\times92.8\%\times0.50\%
=0.928\%
$$

即约：
==92.8bp年化拖累==

DMF：
- 换手40.1%

同样假设下：
≈40.1bp

母指数ACWI：
- 换手3.1%
- 拖累约3.1bp

==毛收益很高但换手极高的策略，净收益可能被实施成本吃掉一大块。==

# 23.为什么真实交易成本不能只靠这个公式
研报明确提醒：

Performance Drag只是：
**固定成本×换手的线性近似**

真实市场冲击通常：
- 资金越大，冲击不一定线性增长
- 小盘股更敏感
- 集中交易日更敏感
- 市场波动时成本也会变化

所以IndexMetrics的这个指标更适合：
**横向比较指数的实施压力**

不是：
精确预测你真实会付多少交易成本。

# 24.为什么要看Top Holdings和Active Weights
[此处插入研报原图：Exhibit 25「Top Constituents and Top/Bottom Active Positions」]

### Top Holdings
看：
指数绝对持仓最大是谁。

### Top Active Weights
看：
相对基准最超配谁。

### Bottom Active Weights
看：
相对基准最少配谁。

eg.
一只股票指数权重=0，
但基准权重=2%

主动权重：
-2%

说明：
这个指数虽然没有“做空”，
但相对基准是明显低配。

截至2020.3，DMF对：
- Microsoft
- Apple
- Amazon
等大权重基准股票有明显负主动权重。

这说明：
**因子指数的主动收益不只来自“买什么”，也来自“相对基准少买什么”。**

# 25.把IndexMetrics变成自己的指数选择流程
这是我读完以后最值得留下的实操框架：

## Step 1：先问目标
我为什么需要这只指数？
- Value？
- Quality？
- Multi-Factor？
- ESG？
- Low Carbon？
- 降风险？
- 提高收益率？

## Step 2：看Exposure
==它真的给了我要的暴露吗？==
- 目标因子够不够强？
- 有没有行业/国家/规模意外押注？
- 财务比率是否支持指数标签？

## Step 3：看Performance Attribution
==过去的超额收益是不是来自我本来就想要的暴露？==
- 因子贡献？
- 行业贡献？
- 国家贡献？
- 个股选择？

如果收益主要来自意外押注：
历史好看也要小心。

## Step 4：看Risk Profile
不能只看波动率：
- Total Risk
- Tracking Error
- Downside Deviation
- VaR
- CVaR
- Maximum Drawdown
- Active Drawdown Period

尤其问：
**如果它连续5—10年跑输基准，我还能不能坚持？**

## Step 5：看Investability
- Active Share
- Effective Number
- Coverage
- Stock Ownership
- Days to Trade
- Turnover
- Performance Drag

问：
**这套策略在我的资金规模下还能不能复制？**

## Step 6：实施以后继续监控
IndexMetrics不仅用于选指数，
也用于实施后检查：
- 因子暴露有没有漂移
- 行业偏离有没有变大
- 风险有没有改变
- 换手/容量有没有恶化
- ESG/气候指标有没有偏离目标

==选指数不是一次性决策，而是持续验证“实际结果有没有仍然符合最初目标”。==

# 26.这篇和上一篇真正串起来的地方
上一篇的核心：
**机构目标与约束 → 选因子 → 选实施方式**

这一篇把“实施方式怎么评价”具体量化：

### 上一篇说：
因子暴露 vs 可投资性有权衡

### 这一篇给指标：
因子暴露：
- FaCS Exposure
- Active Share

可投资性：
- Effective Number
- Coverage
- Stock Ownership
- ATVR
- Days to Trade
- Turnover
- Performance Drag

### 上一篇说：
多因子可以降低相对风险

### 这一篇给指标：
- Active Return
- Tracking Error
- IR
- Active Drawdown
- Attribution

所以可以理解成：

==上一篇给“投资决策框架”，这一篇给“量化检查表”。==

# 27.我认为最重要的几个结论
1. **指数名字不重要，真实暴露重要**
	- “Value”“Quality”“ESG”都必须用数据验货

2. **历史超额收益必须做归因**
	- 要确认钱是不是从目标因子赚来的

3. **总风险和相对风险是两个维度**
	- 总风险低，不等于相对基准稳定
	- 相对基准稳定，也不等于绝对下跌少

4. **长期有效不等于投资者能坚持**
	- Enhanced Value历史上可以连续125个月相对跑输

5. **成分股数量≠真正分散**
	- 要看Effective Number

6. **因子暴露越强，通常越要付出实施代价**
	- 容量、流动性、换手、成本都可能恶化

7. **平均流动性不够**
	- 要看95分位和最大Days to Trade

8. **毛收益≠投资者最后拿到的收益**
	- 高频换手会产生Performance Drag

9. **多因子的价值不只是提高收益**
	- 更重要的是提高主动收益的稳定性和IR

10. ==评价指数应该同时看：Performance + Exposure + Risk + Investability==

# 28.几个公式放在一起
## 主动收益
$$
R_A=R_P-R_B
$$

## Tracking Error
$$
TE=\sqrt{12}\times\sigma(R_{A,\text{monthly}})
$$

## Information Ratio
$$
IR=\frac{R_A}{TE}
$$

## Sharpe
$$
Sharpe=\frac{R_P-R_f}{\sigma_P}
$$

## Effective Number
$$
N_{\text{eff}}=\frac{1}{\sum_iw_i^2}
$$

## Active Share
$$
AS=\frac12\sum_i|w_i^P-w_i^B|
$$

## Weight Multiplier
$$
WM_i=\frac{w_i^P}{w_i^B}
$$

## Stock Ownership
$$
SO_i=\frac{w_i\times FundSize}{MarketCap_i}
$$

## 单边换手
$$
Turnover=\frac12\sum_i|w_{i,after}-w_{i,before}|
$$

## Performance Drag
$$
Performance\ Drag
=
2\times Turnover\times Trading\ Cost
$$

# 29.全篇一句话
==不要问“哪只指数历史收益最高”，而要问：它为什么赚钱、承担了什么风险、真实暴露是什么，以及在我的资金规模下能不能低成本地把这套暴露买下来并长期坚持。==
