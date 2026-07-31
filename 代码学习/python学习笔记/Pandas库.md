

> 目标：用 Pandas 完成量化数据的读取、检查、筛选、清洗、计算、分组、合并和时间序列处理。  
> 记号：以下示例通常使用 `df` 表示 `DataFrame`，使用 `s` 表示 `Series`。

---

# 0. Pandas、NumPy 与数据库的分工

## 定义

- **Pandas**：处理带行列标签的表格型数据。
- **NumPy**：处理纯数值数组、矩阵和密集数值计算。
- **MySQL**：存储、查询和预先筛选大量数据。

## 常见量化流程

```text
数据库读取需要的数据
→ Pandas 清洗、整理、分组、合并和构造特征
→ 转成 NumPy 数组进行密集计算
→ 将结果放回 Pandas 表格
```

## Tips

- 行情原始表通常适合 Pandas。
- 收益率矩阵、协方差矩阵、情景模拟矩阵通常适合 NumPy。
- Pandas 和 NumPy 可以互相转换，不是二选一。

---

# 1. `Series` 和 `DataFrame`

## 1.1 `Series`

### 定义

`Series` 是一维、带索引标签的数据。

一条 `Series` 主要包含：

- `values`：数据；
- `index`：标签；
- `name`：名称；
- `dtype`：数据类型。

### 模板

```python
import pandas as pd

s = pd.Series(
    data,
    index=index_labels,
    name="名称"
)
```

### 例子

```python
scores = pd.Series(
    [85, 92, 78],
    index=["小明", "小红", "小刚"],
    name="考试成绩"
)

scores.values
scores.index
scores.name
scores.dtype
scores.shape
scores.size
```

按标签访问：

```python
scores["小红"]
```

### 用字典创建

```python
prices = pd.Series({
    "苹果": 8.5,
    "香蕉": 4.2,
    "橙子": 6.8
})
```

转换关系：

```text
字典的键 → Series.index
字典的值 → Series.values
```

### Tips

- `Series` 可以理解为“带标签、可向量化计算的一维数组”。
- 它看起来像字典，但计算时会按标签自动对齐。
- 字典的键不能重复，`Series` 的索引可以重复。

---

## 1.2 `DataFrame`

### 定义

`DataFrame` 是二维、带行索引和列名的表格。

特点：

- 有行索引 `index`；
- 有列名 `columns`；
- 每列可以有不同的数据类型；
- 每一列本质上是一个 `Series`。

### 模板：字典中放列表

```python
df = pd.DataFrame({
    "列1": [值1, 值2, 值3],
    "列2": [值1, 值2, 值3]
})
```

### 例子

```python
students = pd.DataFrame({
    "姓名": ["小明", "小红", "小刚"],
    "年龄": [20, 19, 21],
    "成绩": [85.5, 92.0, 78.5],
    "是否及格": [True, True, True]
})
```

转换关系：

```text
外层字典的键     → 列名
键对应的列表     → 一整列
列表中相同位置   → 同一行
```

### 模板：自定义索引

```python
df = pd.DataFrame(
    {
        "列1": [...],
        "列2": [...]
    },
    index=["标签1", "标签2", "标签3"]
)
```

### 例子

```python
students = pd.DataFrame(
    {
        "姓名": ["小明", "小红", "小刚"],
        "成绩": [85, 92, 78]
    },
    index=["S001", "S002", "S003"]
)
```

### 用多个 `Series` 创建

```python
name_series = pd.Series(
    ["小明", "小红"],
    index=["S01", "S02"]
)

score_series = pd.Series(
    [85, 92],
    index=["S01", "S02"]
)

df = pd.DataFrame({
    "姓名": name_series,
    "成绩": score_series
})
```

### 用嵌套字典创建

```python
df = pd.DataFrame({
    "姓名": {
        "S01": "小明",
        "S02": "小红"
    },
    "成绩": {
        "S01": 85,
        "S02": 92
    }
})
```

转换关系：

```text
外层键 → 列名
内层键 → 行索引
内层值 → 单元格数据
```

### Tips

- 字典本身不会自动变成 `DataFrame`，必须调用 `pd.DataFrame(...)`。
- 字典中各列表长度通常必须相同。
- 可以粗略理解为：`DataFrame ≈ 列名 → Series`。

---

## 1.3 查看表格结构

### 模板

```python
print(df)        # 实际数据
df.shape         # (行数, 列数)
df.columns       # 列名
df.index         # 行索引
df.dtypes        # 各列数据类型
df.head()        # 前 5 行
df.tail()        # 后 5 行
df.info()        # 结构、非缺失数量、类型、内存
df.describe()    # 数值列统计摘要
```

### 指定行数

```python
df.head(3)
df.tail(2)
```

### `info()` 与 `describe()`

```python
df.info()
```

`info()` 直接打印结构，返回值是 `None`。

```python
summary = df.describe()
```

`describe()` 返回新的 `DataFrame`，可以保存。

### Tips

- 列名属性是 `columns`，不是 `column`。
- 不要写 `print(df.info())`，否则会额外打印 `None`。
- `df.describe()` 默认主要统计数值列。
- 新拿到数据时先运行：`head()`、`shape`、`columns`、`dtypes`、`info()`。

---

## 1.4 仅选择列，不筛选行

### 模板

```python
df["列名"]          # 返回 Series
df[["列名"]]        # 返回 DataFrame
df[["列1", "列2"]]  # 返回 DataFrame
```

### 例子

```python
price_series = products["单价"]
price_table = products[["单价"]]
basic_info = products[["商品名", "单价"]]
```

### Tips

```text
单中括号 + 单列名 → Series
双中括号 + 列名列表 → DataFrame
```

---

# 2. 数据读取与保存

## 2.1 读取 CSV

### 定义

`pd.read_csv()` 将 CSV 文件读取为 `DataFrame`。

### 模板

```python
df = pd.read_csv("文件路径.csv")
```

### 常用参数

```python
df = pd.read_csv(
    "prices.csv",
    usecols=["date", "symbol", "close", "volume"],
    dtype={"symbol": "string"},
    na_values=["", "NA", "null"]
)
```

### 直接解析日期

```python
df = pd.read_csv(
    "prices.csv",
    parse_dates=["date"]
)
```

### Tips

- Windows 路径可使用原始字符串：

```python
df = pd.read_csv(r"C:\data\prices.csv")
```

- 读取后先检查列名、类型、缺失值和行数。
- 股票代码不要轻易读成整数，否则前导零可能丢失。
- 日期有时会被读成字符串，后面可用 `pd.to_datetime()` 转换。

---

## 2.2 保存 CSV

### 模板

```python
df.to_csv(
    "output.csv",
    index=False,
    encoding="utf-8-sig"
)
```

### Tips

- `index=False`：不把行索引额外写入文件。
- 中文 Excel 打开乱码时可尝试 `encoding="utf-8-sig"`。
- 若行索引本身有业务意义，例如日期，可考虑保留索引。

---

## 2.3 Pandas 与 NumPy 转换

### DataFrame / Series 转 NumPy

```python
arr = df.to_numpy()
arr = df["return"].to_numpy()
```

### NumPy 转 DataFrame

```python
df = pd.DataFrame(
    arr,
    index=row_labels,
    columns=column_labels
)
```

### Tips

- 转成 NumPy 后会失去行列标签。
- DataFrame 各列类型不同，转成 NumPy 时可能统一为较宽泛的类型。
- 需要密集矩阵运算时再转换，不要过早丢失标签。

---

# 3. 索引、筛选与赋值

## 3.1 `loc`：按标签选择

### 定义

`loc` 按行标签和列标签选择。

### 模板

```python
df.loc[行标签, 列标签]
```

### 例子

```python
df.loc["P102"]                    # 一行
df.loc["P102", "单价"]            # 单元格
df.loc[["P101", "P103"]]          # 多行
df.loc[:, ["商品名", "单价"]]      # 所有行、指定列
df.loc[["P101", "P103"], ["商品名", "单价"]]
```

### 标签切片

```python
df.loc["P101":"P103"]
```

### Tips

- `loc` 标签切片通常包含右端点。
- 行标签和列标签之间用逗号分隔。
- 多行、多列列表会形成完整交叉区域。

---

## 3.2 `iloc`：按整数位置选择

### 定义

`iloc` 按从 0 开始的位置选择。

### 模板

```python
df.iloc[行位置, 列位置]
```

### 例子

```python
df.iloc[0]          # 第一行
df.iloc[1, 2]       # 第二行、第三列
df.iloc[:3, :2]     # 前三行、前两列
df.iloc[[0, 2], [1, 3]]
```

### Tips

- `iloc` 切片不包含右端点，与 NumPy 相同。
- `loc` 看标签，`iloc` 看位置。
- 行索引即使恰好是整数，也不要混淆标签和位置。

---

## 3.3 布尔筛选

### 模板

```python
mask = df["列名"] > 某值
result = df.loc[mask]
```

### 多条件

```python
mask = (
    (df["条件列1"] > 某值)
    & (df["条件列2"] == 某类别)
)

result = df.loc[mask]
```

### 同时选择列

```python
result = df.loc[
    mask,
    ["列1", "列2"]
]
```
==行条件，列选择==

### 运算符

```text
&  并且
|  或者
~  取反
```

### Tips

- 每个条件必须单独加括号。
- 不能使用 Python 的 `and`、`or` 连接 `Series` 条件。
- 推荐统一写成 `df.loc[行条件, 列选择]`。

---

## 3.4 `isin()`

### 定义

判断值是否属于给定集合。

### 模板

```python
df["列"].isin([值1, 值2])
```

### 例子

```python
df.loc[
    df["industry"].isin(["银行", "证券"])
]
```

### SQL 对应

```sql
WHERE industry IN ('银行', '证券')
```

---

## 3.5 `between()`

### 定义

判断数值是否位于指定区间。

### 模板

```python
df["列"].between(下限, 上限)
```

### 例子

```python
df.loc[
    df["price"].between(10, 50)
]
```

### Tips

默认包含上下限。

---

## 3.6 安全赋值

### 模板

```python
df.loc[行条件, "目标列"] = 新值
```

### 例子

```python
df.loc[
    df["库存"] == 0,
    "是否上架"
] = False
```

同时修改多列：

```python
df.loc[
    df["库存"] == 0,
    ["是否上架", "单价"]
] = [False, 0]
```

### 先复制再修改

```python
modified = df.copy()

modified.loc[
    modified["return"] > 0.1,
    "return"
] = 0.1
```

### Tips：避免链式赋值

不推荐：

```python
df[df["库存"] == 0]["是否上架"] = False
```

推荐：

```python
df.loc[df["库存"] == 0, "是否上架"] = False
```

记忆：

```text
原表.loc[目标行, 目标列] = 新值
```

---

## 3.7 设置和恢复索引

### 普通列变成索引

```python
df = df.set_index("date")
```

### 索引恢复为普通列

```python
df = df.reset_index()
```

### 不保留原索引

```python
df = df.reset_index(drop=True)
```

### Tips

- 日期常被设置成索引，方便时间切片和重采样。
- `set_index()` 默认返回新表；可重新赋值。
- 重置索引后，旧索引默认会变成普通列。

---

# 4. 数据清洗

## 4.1 检查缺失值

### 模板

```python
df.isna()
df.notna()
df.isna().sum()
```

### 每行缺失数量

```python
df.isna().sum(axis=1)
```

### Tips

- `isna()` 和 `isnull()` 基本等价。
- `df.isna().sum()` 常用于快速查看每列缺失数量。

---

## 4.2 删除缺失值

### 删除任何包含缺失值的行

```python
cleaned = df.dropna()
```

### 只检查指定列

```python
cleaned = df.dropna(
    subset=["date", "symbol", "close"]
)
```

### 至少保留一定数量的非缺失值

```python
cleaned = df.dropna(thresh=3)
```

### Tips

- 不要看到缺失值就直接全部删除。
- 关键标识字段缺失通常更适合删除。
- 价格缺失、成交量缺失等需要结合业务判断。

---

## 4.3 填充缺失值

### 固定值填充

```python
df["volume"] = df["volume"].fillna(0)
```

### 多列使用不同值

```python
df = df.fillna({
    "volume": 0,
    "industry": "UNKNOWN"
})
```

### 前向填充

```python
df["close"] = df["close"].ffill()
```

### 后向填充

```python
df["close"] = df["close"].bfill()
```

### 分组内填充

```python
df["close"] = (
    df.groupby("symbol")["close"]
      .ffill()
)
```

### Tips

- 多股票数据不能直接全表前向填充，否则可能把一只股票的值填到另一只股票。
- 使用填充前必须先按股票和日期排序。
- 收益率缺失通常不应随意填成 0，需判断含义。

---

## 4.4 重复值

### 检查整行重复

```python
df.duplicated()
df.duplicated().sum()
```

### 按关键字段检查

```python
df.duplicated(
    subset=["date", "symbol"]
)
```

### 删除重复

```python
df = df.drop_duplicates(
    subset=["date", "symbol"],
    keep="last"
)
```

### Tips

- 行情数据常用 `date + symbol` 作为联合唯一键。
- `keep="first"` 保留第一条，`keep="last"` 保留最后一条。
- 删除前先查清重复数据产生原因。

---

## 4.5 数据类型转换

### 普通类型转换

```python
df["volume"] = df["volume"].astype("int64")
df["symbol"] = df["symbol"].astype("string")
```

### 安全转换数值

```python
df["volume"] = pd.to_numeric(
    df["volume"],
    errors="coerce"
)
```

### 转换日期

```python
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)
```

### Tips

- `errors="coerce"` 会把无法转换的值变成缺失值。
- 转换后再次检查 `isna().sum()`。
- 带缺失值的整数列可考虑 Pandas 可空整数类型：

```python
df["volume"] = df["volume"].astype("Int64")
```

---

## 4.6 重命名列

### 模板

```python
df = df.rename(columns={
    "旧列名": "新列名"
})
```
==rename()默认返回一个新的dataframe，不修改原来的df==

### 统一列名格式

```python
df.columns = (
    df.columns
      .str.strip() #删除列名前后的空格
      .str.lower() #全部转成小写
      .str.replace(" ", "_") #把空格替换成下划线
)
```

### Tips

- 真实数据中列名可能有空格、大小写不统一。
- 重命名后检查关键列是否存在。

---

## 4.7 异常值处理

### 截断上下限

```python
df["return"] = df["return"].clip(
    lower=-0.1,
    upper=0.1
)
#把return限制在-0.1~0.1之间，超出边界的数按照边界赋值
```

### 条件替换：`where()`

保留满足条件的值，不满足的改成指定值：

```python
df["return"] = df["return"].where(
    df["return"] >= -0.1,
    -0.1
)
```

### 条件替换：`mask()`

满足条件的值改成指定值：

```python
df["return"] = df["return"].mask(
    df["return"] > 0.1,
    0.1
)
#和where()逻辑相反，类似条件成立就替换，不成立则保留
```

### Tips

```text
where：条件为 True 时保留
mask：条件为 True 时替换
clip：直接限制上下界
```

---

# 5. 向量化计算、排序与标签对齐

## 5.1 创建新列

### 模板

```python
df["新列"] = 表达式
```

### 例子

```python
df["amount"] = df["close"] * df["volume"]
df["excess_return"] = df["return"] - df["benchmark_return"]
```

### 使用 `assign()`

```python
new_df = df.assign(
    amount=df["close"] * df["volume"]
)
```

### Tips

- Pandas 列运算通常不需要循环。
- 列名应表达业务含义。
- `assign()` 返回新表，便于链式操作。

---

## 5.2 常用聚合

### 模板

```python
s.sum()
s.mean()
s.std()
s.var()
s.min()
s.max()
s.median()
s.quantile(0.25)
s.count()
s.nunique()
```

### DataFrame 按列统计

```python
df[["return", "volume"]].mean()
```

### Tips

- Pandas 聚合通常默认跳过缺失值。
- `count()` 统计非缺失值数量。
- `size` 更偏向统计总行数，包含缺失值。

---

## 5.3 排序

### 按值排序

```python
df.sort_values(
    by="return",
    ascending=False
)
```

### 多列排序

```python
df.sort_values(
    by=["date", "symbol"],
    ascending=[True, True]
)
```

### 按索引排序

```python
df.sort_index()
```

### 原地排序

```python
df.sort_values(
    "return",
    inplace=True
)
```

### Tips

- 多股票时间序列计算前通常先按 `symbol + date` 排序。
- 默认返回新表，除非使用 `inplace=True`。
- 排序后索引不会自动重排，可使用：

```python
df = df.sort_values("return").reset_index(drop=True)
```

---

## 5.4 排名与选前若干项

### 排名

```python
df["rank"] = df["factor"].rank(
    ascending=False,
    method="first"
)
```

### 最大若干项

```python
top = df.nlargest(5, "factor")
```

### 最小若干项

```python
bottom = df.nsmallest(5, "volatility")
```

### Tips

- `rank()` 返回排名值，不会直接筛选行。
- `ascending=False` 表示数值越大排名越靠前。
- `method` 控制并列值如何处理。

---

## 5.5 标签自动对齐

### 定义

Pandas 运算时会按照索引标签匹配，而不是只看位置。

### 例子

```python
a = pd.Series(
    [10, 20],
    index=["A", "B"]
)

b = pd.Series(
    [1, 2],
    index=["B", "A"]
)

a + b
```

结果：

```text
A → 10 + 2
B → 20 + 1
```

### 标签缺失

```python
a = pd.Series([10, 20], index=["A", "B"])
b = pd.Series([1, 2], index=["B", "C"])

a + b
```

缺少对应标签的位置会得到 `NaN`。

### 指定缺失填充值

```python
a.add(b, fill_value=0)
```

### Tips

- 自动对齐是 Pandas 的核心特点，也是常见错误来源。
- 运算前检查索引是否一致：

```python
a.index.equals(b.index)
```

- 不需要标签对齐、只想按位置计算时可先转 NumPy，但要明确知道自己在做什么。

---

## 5.6 累计计算

```python
s.cumsum()
s.cumprod()
s.cummax()
s.cummin()
```

### 量化例子：累计净值

```python
df["nav"] = (1 + df["return"]).cumprod()
```

### Tips

- 累计收益不是简单的收益率累加。
- 多股票数据必须分组后分别累计：

```python
df["nav"] = (
    1 + df["return"]
).groupby(df["symbol"]).cumprod()
```

---

# 6. `groupby` 分组计算

## 6.1 核心逻辑

### 定义

`groupby` 的逻辑是：

```text
拆分 split
→ 每组计算 apply
→ 合并 combine
```


---

## 6.2 基础分组聚合

### 模板

```python
df.groupby("分组列")["数值列"].mean()
```

### 例子

```python
mean_returns = (
    df.groupby("symbol")["return"]
      .mean()
)
```

### 多列分组

```python
result = (
    df.groupby(["date", "industry"])["return"]
      .mean()
)
```

### Tips

- 默认情况下，分组键可能进入结果索引。
- 想让分组键保持普通列，可使用：

```python
df.groupby("symbol", as_index=False)["return"].mean()
```

---

## 6.3 `agg()`：每组压缩成统计结果

### 定义

`agg()` 对每组做一个或多个统计，结果行数通常减少。

### 命名聚合模板

```python
result = (
    df.groupby("symbol")
      .agg(
          新列名1=("原列名", "统计函数"),
          新列名2=("原列名", "统计函数")
      )
)
```

### 量化例子

```python
summary = (
    df.groupby("symbol")
      .agg(
          mean_return=("return", "mean"),
          volatility=("return", "std"),
          trading_days=("return", "count"),
          total_volume=("volume", "sum")
      )
      .reset_index()
)
```

### Tips

- `agg()` 类似 SQL 的 `GROUP BY`。
- `count` 只统计非缺失值。
- 统计总行数可使用 `size`：

```python
df.groupby("symbol").size()
```

---

## 6.4 `transform()`：计算后保持原行数

### 定义

`transform()` 在每组内部计算，然后把结果返回到该组每一行。

### 模板

```python
df["新列"] = (
    df.groupby("分组列")["数值列"]
      .transform("统计函数")
)
```

### 例子

```python
df["symbol_mean_return"] = (
    df.groupby("symbol")["return"]
      .transform("mean")
)
```

### 分组标准化

```python
group_mean = (
    df.groupby("industry")["factor"]
      .transform("mean")
)

group_std = (
    df.groupby("industry")["factor"]
      .transform("std")
)

df["factor_zscore"] = (
    df["factor"] - group_mean
) / group_std
```

### Tips

```text
agg       → 每组缩成少数行
transform → 保持与原表相同行数
```

量化中行业中性化、分组排名、分组填充常用 `transform()`。

---

## 6.5 分组排名

### 模板

```python
df["group_rank"] = (
    df.groupby("date")["factor"]
      .rank(
          ascending=False,
          method="first"
      )
)
```

### 量化含义

在每个交易日内部，对所有股票的因子值分别排名。

### Tips

- 横截面选股通常是“按日期分组后排名”。
- 行业中性排名通常是“按日期和行业分组后排名”。

---

## 6.6 分组时间序列计算

### 上一期值

```python
df["previous_close"] = (
    df.groupby("symbol")["close"]
      .shift(1)
)
```

### 收益率

```python
df["return"] = (
    df.groupby("symbol")["close"]
      .pct_change()
)
```

### 差分

```python
df["price_change"] = (
    df.groupby("symbol")["close"]
      .diff()
)
```

### Tips

- 分组时间计算前必须先排序：

```python
df = df.sort_values(["symbol", "date"])
```

- 不分组直接 `pct_change()`，可能把一只股票的最后一行和下一只股票的第一行连接计算。

---

# 7. 数据合并与变形

## 7.1 `concat()`：沿某个方向拼接

### 纵向追加行

```python
combined = pd.concat(
    [df1, df2],
    axis=0,
    ignore_index=True
)
```

### 横向追加列

```python
combined = pd.concat(
    [df1, df2],
    axis=1
)
```

### Tips

```text
axis=0 → 上下拼接，增加行
axis=1 → 左右拼接，增加列
```

- 纵向拼接时列名会按标签对齐。
- `ignore_index=True` 会重新生成连续索引。
- 横向拼接时行索引会自动对齐。

---

## 7.2 `merge()`：按键连接表格

### 定义

`merge()` 类似 SQL 的 `JOIN`。

### 模板

```python
result = pd.merge(
    left_df,
    right_df,
    on="连接键",
    how="left"
)
```

### 多个连接键

```python
result = pd.merge(
    prices,
    factors,
    on=["date", "symbol"],
    how="left"
)
```

### 不同列名连接

```python
result = pd.merge(
    left_df,
    right_df,
    left_on="stock_code",
    right_on="symbol",
    how="left"
)
```

### `how`

```text
inner → 只保留两边都匹配的键
left  → 保留左表全部行
right → 保留右表全部行
outer → 保留两边全部键
```

### 检查连接关系

```python
result = pd.merge(
    left_df,
    right_df,
    on=["date", "symbol"],
    how="left",
    validate="one_to_one"
)
```

常见值：

```text
one_to_one
one_to_many
many_to_one
many_to_many
```

### 显示匹配来源

```python
result = pd.merge(
    left_df,
    right_df,
    on="symbol",
    how="outer",
    indicator=True
)
```

### Tips

- 合并前检查连接键是否唯一。
- 多对多连接可能导致行数爆炸。
- 合并前后比较行数：

```python
len(left_df)
len(result)
```

- 量化数据常用 `date + symbol` 作为联合连接键。

---

## 7.3 `pivot()`：长表转宽表

### 定义

把某列的不同取值展开成多列。

### 模板

```python
wide = df.pivot(
    index="行索引列",
    columns="展开列",
    values="数值列"
)
```

### 量化例子

```python
return_matrix = df.pivot(
    index="date",
    columns="symbol",
    values="return"
)
```

结果：

```text
行 → 日期
列 → 股票代码
值 → 收益率
```

### Tips

- `pivot()` 要求同一 `index + columns` 组合只能有一个值。
- 存在重复组合时会报错，应先处理重复或使用 `pivot_table()`。

---

## 7.4 `pivot_table()`：允许聚合的透视表

### 模板

```python
table = df.pivot_table(
    index="date",
    columns="symbol",
    values="return",
    aggfunc="mean"
)
```

### Tips

- `pivot_table()` 可以处理重复键，通过 `aggfunc` 聚合。
- 默认聚合函数通常是均值，最好明确写出。

---

## 7.5 `melt()`：宽表转长表

### 模板

```python
long_df = wide_df.melt(
    id_vars=["date"],
    var_name="symbol",
    value_name="return"
)
```

### 例子

原宽表：

```text
date | AAA | BBB
```

转换成长表：

```text
date | symbol | return
```

### Tips

- 长表更适合筛选、分组、合并。
- 宽表更适合矩阵计算和横截面对比。

---

# 8. 日期与金融时间序列

## 8.1 转换日期

### 模板

```python
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)
```

### 指定格式

```python
df["date"] = pd.to_datetime(
    df["date"],
    format="%Y-%m-%d",
    errors="coerce"
)
```

### Tips

- 转换失败的日期在 `errors="coerce"` 下会变成 `NaT`。
- 转换后检查：

```python
df["date"].isna().sum()
```

---

## 8.2 日期属性 `.dt`

日期列为 datetime 类型后：

```python
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["weekday"] = df["date"].dt.dayofweek
df["quarter"] = df["date"].dt.quarter
```

### Tips

- `.dt` 用于普通日期列。
- 日期已经放入索引后，可使用 `df.index.year` 等属性。
- `dayofweek` 通常为周一 0 到周日 6。

---

## 8.3 日期索引与日期切片

### 设置日期索引

```python
df = (
    df.set_index("date")
      .sort_index()
)
```

### 日期切片

```python
df.loc["2026-01-01":"2026-01-31"]
```

### 指定某月

```python
df.loc["2026-01"]
```

### Tips

- 日期索引必须先转换成 datetime。
- 时间序列操作前先排序。
- 多股票长表一般不会只把日期设为唯一索引，因为同一天有多只股票；可保留日期列或使用多重索引，但当前学习以普通列分组为主。

---

## 8.4 `shift()`：移动数据

### 定义

将数据按行移动，用于取得上一期或下一期值。

### 模板

```python
s.shift(1)     # 向下移动 1 行，取得上一期
s.shift(-1)    # 向上移动 1 行，取得下一期
```

### 量化例子

```python
df["previous_close"] = (
    df.groupby("symbol")["close"]
      .shift(1)
)
```

### 构建信号并避免未来数据

```python
df["signal"] = (
    df["factor"] > 0
).astype(int)

df["position"] = (
    df.groupby("symbol")["signal"]
      .shift(1)
)
```

### Tips

- `shift(1)` 常用于避免使用当天尚未可知的信息。
- 使用未来数据会造成前视偏差。
- 多股票数据通常必须先分组。

---

## 8.5 `pct_change()`：变化率

### 定义

计算当前值相对上一期的比例变化。

### 模板

```python
s.pct_change()
```

### 量化例子

```python
df["return"] = (
    df.groupby("symbol")["close"]
      .pct_change()
)
```

计算逻辑：

```text
当前价格 / 上一期价格 - 1
```

### Tips

- 第一条记录通常没有上一期，因此结果是缺失值。
- 计算前先按股票和日期排序。
- 不同频率、复权方式会影响收益率含义。

---

## 8.6 `diff()`：差值

### 模板

```python
s.diff()
```

### 例子

```python
df["price_change"] = (
    df.groupby("symbol")["close"]
      .diff()
)
```

计算逻辑：

```text
当前值 - 上一期值
```

### Tips

```text
diff()       → 绝对变化
pct_change() → 相对变化率
```

---

## 8.7 `rolling()`：滚动窗口

### 定义

使用当前行及之前若干行形成窗口，逐行计算。

### 模板

```python
s.rolling(窗口长度).统计函数()
```

### 移动平均

```python
df["ma_20"] = (
    df.groupby("symbol")["close"]
      .transform(
          lambda s: s.rolling(20).mean()
      )
)
```

### 滚动波动率

```python
df["vol_20"] = (
    df.groupby("symbol")["return"]
      .transform(
          lambda s: s.rolling(20).std()
      )
)
```

### 控制最少数据量

```python
s.rolling(
    window=20,
    min_periods=5
).mean()
```

### Tips

- 默认窗口数据不足时结果为缺失值。
- `min_periods` 决定至少需要多少个有效观测。
- 滚动计算前必须正确排序。
- 量化中要确认窗口是否包含当前期，以及结果何时可用于交易。

---

## 8.8 `expanding()`：扩展窗口

### 定义

窗口从序列开头不断扩大到当前行。

### 模板

```python
s.expanding().mean()
```

### 量化例子

```python
df["expanding_mean"] = (
    df.groupby("symbol")["return"]
      .transform(
          lambda s: s.expanding().mean()
      )
)
```

### Tips

```text
rolling   → 固定长度窗口
expanding → 从起点累计扩展
```

---

## 8.9 `ewm()`：指数加权窗口

### 模板

```python
s.ewm(
    span=20,
    adjust=False
).mean()
```

### 量化例子

```python
df["ema_20"] = (
    df.groupby("symbol")["close"]
      .transform(
          lambda s: s.ewm(
              span=20,
              adjust=False
          ).mean()
      )
)
```

### Tips

- 越新的数据通常权重越高。
- `span` 越小，指标对近期变化越敏感。
- EMA 常用于趋势指标。

---

## 8.10 `resample()`：时间重采样

### 定义

按新的时间频率分组聚合。

### 前提

时间列通常需要成为 `DatetimeIndex`。

```python
daily = (
    df.set_index("date")
      .sort_index()
)
```

### 日线转月度统计

```python
monthly = daily.resample("ME").agg({
    "close": "last",
    "volume": "sum",
    "return": "mean"
})
```

### OHLC 重采样

```python
weekly = daily.resample("W").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
})
```

### 多股票重采样

```python
weekly = (
    df.set_index("date")
      .groupby("symbol")
      .resample("W")
      .agg({
          "open": "first",
          "high": "max",
          "low": "min",
          "close": "last",
          "volume": "sum"
      })
      .reset_index()
)
```

### Tips

- OHLC 不同列的聚合规则不同。
- `volume` 通常求和，`close` 通常取最后值。
- 周/月频率边界需要结合业务定义检查。
- 重采样前确认日期索引和排序正确。

---

# 9. 量化常用完整处理模板

## 9.1 读取和初检

```python
import pandas as pd
import numpy as np

df = pd.read_csv(
    "prices.csv",
    parse_dates=["date"],
    dtype={"symbol": "string"}
)

df.head()
df.shape
df.columns
df.dtypes
df.info()
```

---

## 9.2 清洗

```python
df = (
    df.drop_duplicates(
        subset=["date", "symbol"],
        keep="last"
    )
    .dropna(
        subset=["date", "symbol", "close"]
    )
)

df["volume"] = pd.to_numeric(
    df["volume"],
    errors="coerce"
)

df["volume"] = df["volume"].fillna(0)

df = df.sort_values(
    ["symbol", "date"]
).reset_index(drop=True)
```

---

## 9.3 计算收益和指标

```python
df["return"] = (
    df.groupby("symbol")["close"]
      .pct_change()
)

df["ma_20"] = (
    df.groupby("symbol")["close"]
      .transform(
          lambda s: s.rolling(
              20,
              min_periods=20
          ).mean()
      )
)

df["vol_20"] = (
    df.groupby("symbol")["return"]
      .transform(
          lambda s: s.rolling(
              20,
              min_periods=20
          ).std()
      )
)
```

---

## 9.4 构建简单因子与信号

```python
df["momentum"] = (
    df.groupby("symbol")["close"]
      .pct_change(20)
)

df["factor_rank"] = (
    df.groupby("date")["momentum"]
      .rank(
          ascending=False,
          method="first"
      )
)

df["signal"] = (
    df["factor_rank"] <= 5
).astype(int)
```

---

## 9.5 避免前视偏差

```python
df["position"] = (
    df.groupby("symbol")["signal"]
      .shift(1)
)
```

### 策略收益

```python
df["strategy_return"] = (
    df["position"] * df["return"]
)
```

---

## 9.6 按日期得到组合收益

```python
daily_strategy = (
    df.groupby("date", as_index=False)
      .agg(
          portfolio_return=(
              "strategy_return",
              "mean"
          ),
          holdings=("position", "sum")
      )
)
```

### 累计净值

```python
daily_strategy["nav"] = (
    1 + daily_strategy["portfolio_return"]
).cumprod()
```

### Tips

- 这里只是等权示例，实际工作需要考虑权重、手续费、停牌、涨跌停和成交约束。
- 信号通常要 `shift(1)` 后才用于收益计算。
- 聚合组合收益前要确认缺失值和持仓数量。

---

# 10. 常见错误与检查清单

## 10.1 `Series` 与 `DataFrame` 混淆

```python
df["close"]       # Series
df[["close"]]     # DataFrame
```

---

## 10.2 `loc` 与 `iloc` 混淆

```text
loc  → 标签
iloc → 位置
```

---

## 10.3 布尔条件忘记括号

错误：

```python
df["a"] > 0 & df["b"] < 1
```

正确：

```python
(df["a"] > 0) & (df["b"] < 1)
```

---

## 10.4 使用 `and` / `or`

错误：

```python
(df["a"] > 0) and (df["b"] < 1)
```

正确：

```python
(df["a"] > 0) & (df["b"] < 1)
```

---

## 10.5 链式赋值

不推荐：

```python
df[df["return"] > 0.1]["return"] = 0.1
```

推荐：

```python
df.loc[
    df["return"] > 0.1,
    "return"
] = 0.1
```

---

## 10.6 时间序列未排序

在 `shift()`、`pct_change()`、`rolling()` 前：

```python
df = df.sort_values(["symbol", "date"])
```

---

## 10.7 多股票计算时忘记分组

错误风险：

```python
df["return"] = df["close"].pct_change()
```

推荐：

```python
df["return"] = (
    df.groupby("symbol")["close"]
      .pct_change()
)
```

---

## 10.8 `agg()` 与 `transform()` 混淆

```text
agg       → 减少行数，生成分组摘要
transform → 保持原行数，结果回填到每一行
```

---

## 10.9 合并后行数异常

检查：

```python
df[["date", "symbol"]].duplicated().sum()
len(left_df)
len(result)
```

必要时使用：

```python
validate="one_to_one"
```

---

## 10.10 标签对齐造成 `NaN`

检查：

```python
left.index.equals(right.index)
```

需要按位置计算时，明确转换：

```python
left.to_numpy() + right.to_numpy()
```

---

## 10.11 `info()` 的返回值

```python
df.info()
```

直接打印结构，返回 `None`。

---

## 10.12 量化中的前视偏差

错误思路：

```text
使用当天收盘后才能知道的信号
去计算同一天已经发生的收益
```

常见处理：

```python
df["position"] = (
    df.groupby("symbol")["signal"]
      .shift(1)
)
```

---

# 11. 高频函数速查

## 创建与读取

```python
pd.Series()
pd.DataFrame()
pd.read_csv()
df.to_csv()
```

## 查看

```python
df.head()
df.tail()
df.shape
df.columns
df.index
df.dtypes
df.info()
df.describe()
```

## 选择与赋值

```python
df["col"]
df[["col1", "col2"]]
df.loc[rows, cols]
df.iloc[rows, cols]
df.copy()
```

## 筛选

```python
isin()
between()
isna()
notna()
```

## 清洗

```python
dropna()
fillna()
ffill()
bfill()
duplicated()
drop_duplicates()
astype()
pd.to_numeric()
pd.to_datetime()
rename()
clip()
where()
mask()
```

## 排序与统计

```python
sort_values()
sort_index()
rank()
nlargest()
nsmallest()
sum()
mean()
std()
median()
quantile()
count()
nunique()
cumsum()
cumprod()
```

## 分组

```python
groupby()
agg()
transform()
size()
```

## 合并与变形

```python
pd.concat()
pd.merge()
pivot()
pivot_table()
melt()
```

## 时间序列

```python
shift()
pct_change()
diff()
rolling()
expanding()
ewm()
resample()
```

## NumPy 转换

```python
df.to_numpy()
pd.DataFrame(array)
```

---

# 12. 当前 10 小时学习范围

本次重点掌握：

```text
1. Series / DataFrame
2. 数据读取与结构检查
3. loc / iloc / 布尔筛选 / 安全赋值
4. 缺失值、重复值和类型转换
5. 向量化计算、排序、排名和标签对齐
6. groupby / agg / transform
7. concat / merge / pivot / melt
8. 日期、shift、pct_change、rolling、resample
9. 量化数据综合处理
```

暂不深入：

```text
高级 MultiIndex
复杂字符串正则
Categorical 内部机制
Styler 表格美化
query / eval 优化
大型数据库性能优化
复杂自定义 apply
```
