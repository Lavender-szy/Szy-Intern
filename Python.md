---
tags:
  - "#代码"
  - "#python"
date: 2026-07-10T14:20:00
---

# 基本数据类型
- 整数 int
- 浮点数 float
- 字符串 str
- 布尔型 bool

# 条件判断
if/elif/else条件判断

```python
if 条件1:
    命令1
elif 条件2:
    命令2
else:
    命令3
```

# 循环
## while循环

```python
while 条件:
    命令
    i += 1
```

## for循环

```python
for i in range():
    命令
```

==for循环不需要手动写 i += 1==

## break语句和continue语句
break：跳出循环体

continue：跳出==本次==循环，直接进行下一次循环

# 列表
## 创建列表

```python
num = [a, b, c, ...]
```

## 索引

```python
num[x]
```

x=0,1,2,……

## 修改

```python
num[x] = n
```

x=0,1,2,……

## 添加与删除
append()

```python
num.append(A)
```

remove()

```python
num.remove(A)
```

==pop()==

```python
num.pop()
```

删除最后一位

```python
num.pop(X)
```

删除第X+1位的元素

## ==切片与浅复制==

```python
num[起始索引:终点索引:步长]
num[::-1] #将结果的排列顺序反转
```

切片：从列表中摘取片段，左闭右开
- 起始索引如果是负的则说明：从**倒数**x位开始取切片到最后一位

```python
num1 = num[:]
```

浅复制：副本

# 元组
## 创建元组

```python
元组 = (a, b, c, ...)
```

元组创建后==不可修改==

元组的查找和列表一样

```python
元组[X]
```

# 字符串
**字符串常用操作**

==字符串.操作==

大小写

```python
字符串.upper()
字符串.lower()
```

去除字符串首尾的空白字符（空格、换行、制表符等）

```python
字符串.strip()
```

替换文本

```python
字符串.replace(旧, 新)
```

按分隔符拆分列表

```python
字符串.split("分隔符")
```

长度

```python
len(字符串)
```

# 函数
## 定义与调用

```python
def 函数名(参数1, 参数2=默认值):
    命令

函数名(实参1)
函数名(实参1, 参数2=实参2)
```

## 收集位置参数 `*args`

```python
def 函数名(*参数集合):
    for 参数 in 参数集合:
        命令
```

## 收集关键字参数 `**kwargs`

```python
def 函数名(**参数字典):
    for key, value in 参数字典.items():
        命令
```

## return返回值

```python
def 函数名(a, b):
    return 结果

result = 函数名(实参1, 实参2)
```

## 返回多个值

函数可以使用一个 `return` 返回多个结果，多个结果会自动组成元组；也可以使用相同数量的变量进行拆包。

```python
def 函数名(参数):
    return 结果1, 结果2, ...

结果元组 = 函数名(实参)
结果1, 结果2, ... = 函数名(实参)
```

## 变量作用域与global关键字

```python
变量 = 初始值

def 函数名():
    global 变量
    变量 = 新值
```

## 嵌套函数与闭包

```python
def 外层函数(外层参数):
    def 内层函数(内层参数):
        return 使用外层参数和内层参数的结果
    return 内层函数

函数变量 = 外层函数(实参)
结果 = 函数变量(实参)
```

函数可以赋值给变量，函数调用形式 `函数()` 不能出现在等号左边。

## 递归函数

```python
def 函数名(n):
    if 终止条件:
        return 基础结果
    return 函数名(规模更小的参数)
```

## 匿名函数、`map()`与`filter()`

匿名函数模板：

```python
lambda 参数: 返回结果
```

`map()`：将函数依次应用到可迭代对象的每个元素。

```python
结果迭代器 = map(函数, 可迭代对象)
结果列表 = list(结果迭代器)
```

`filter()`：保留使判断函数返回 `True` 的元素。

```python
结果迭代器 = filter(判断函数, 可迭代对象)
结果列表 = list(结果迭代器)
```

- `map()` 返回 `map` 迭代器，`filter()` 返回 `filter` 迭代器，它们都不是列表。
- 只需要遍历时可以直接放进 `for` 循环；需要查看全部结果、使用索引或反复使用时，可用 `list()` 转换。
- 迭代器按需产生结果，通常只能完整消耗一次。
- `map()` 是通用的逐个调用函数；NumPy 批量运算主要面向数值数组，由底层优化代码执行，适合大量数值计算。

```python
结果列表 = list(map(lambda x: 转换表达式, 可迭代对象))
筛选列表 = list(filter(lambda x: 判断条件, 可迭代对象))
```

## 质数判断

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

# 字典
## get()

```python
字典.get(键)
字典.get(键, 默认值)
```

get()方法用于获取字典中指定键的值，如果键不存在，则返回默认值（如果提供了第二个参数），否则返回None。

## update()

```python
字典.update({
    键1: 值1,
    键2: 值2,
})
```
==字典中相邻键值对之间必须加逗号==
## pop()

```python
removed = 字典.pop(键)
```

## items()

```python
for key, value in 字典.items():
	命令
```

items()大部分情况用于for循环，也可直接赋值给变量，返回一种特殊对象，类型为==dict_items==；遍历得到的每个元素是由key和value组成的元组，需要列表时使用`list(字典.items())`。

```python
items_view = 字典.items()
items_list = list(字典.items())
```
**字典元素赋值**
```python
字典[键] = 值
```
**组合嵌套字典**：
```python
外层字典[外层键] = {
    "字段1": 数据1,
    "字段2": 数据2
}
```
# 集合
==集合中的元素不重复；空集合可以创建==

## 创建空集合

```python
empty_set = set()
```

## 添加元素

```python
集合.add(元素)
```

## 删除元素

```python
集合.remove(元素)
```

==不存在会报错==

```python
集合.discard(元素)
```

==不存在也不会报错==

## 判断元素是否存在

```python
print(元素 in 集合)
```

结果：True/False

## 集合运算
### 并集

```python
A | B
```

### 交集

```python
A & B
```

### 差集

```python
A - B
```

```python
group_a = {"Alice", "Bob", "Cindy", "David"}
group_b = {"Bob", "David", "Emma"}
group_a.add("Frank")
group_a.discard("Grace")
all_people = group_a | group_b
both_groups = group_a & group_b
only_a = group_a - group_b
emma_in_a = "Emma" in group_a
print("所有人：", all_people)
print("两个组都有：", both_groups)
print("只在A组：", only_a)
print("Emma是否在A组：", emma_in_a)
```

# 文件的基本写入与读取
## 用open打开文件

```python
with open("文件名", "模式", encoding="utf-8") as file:
    命令
```

模式的类型

- "r"：读取文件
- "w"：覆盖写入
- "a"：不覆盖追加

## 写入内容

```python
with open("message.txt", "w", encoding="utf-8") as file:
    file.write("你好，Python！")
```

==文件内要换行的话要在字符串内加入换行符；多个字符串拼接需要用+，不能用逗号。==

```python
tasks = ["学习字典", "练习集合", "学习文件操作"]
with open("tasks.txt", "w", encoding="utf-8") as file:
    for i in tasks:
        file.write(i + "\n")
```

## 读取内容
### 读取全部内容

```python
content = file.read()
```

### 逐行读取文件
==文件对象本身可以直接放进for循环==

- 直接用print可能出现空行，因为文件中的每行自带换行符，print()也会换行。
- 使用line.strip()去掉行尾换行符。

```python
with open("tasks.txt", "r", encoding="utf-8") as file:
    for i in file:
        print("任务：" + i.strip())
```

## `readline()`、`readlines()`与`writelines()`

`readline()` 每次读取一行，文件读取位置会继续向后移动。

```python
with open("文件名", "r", encoding="utf-8") as file:
    一行内容 = file.readline()
```

`readlines()` 一次读取所有行并返回列表，每个元素通常保留行尾换行符。

```python
with open("文件名", "r", encoding="utf-8") as file:
    行列表 = file.readlines()
```

`writelines()` 一次写入多个字符串，但不会自动添加换行符。

```python
with open("文件名", "w", encoding="utf-8") as file:
    file.writelines(字符串列表)
```

# try/except异常处理

```python
try:
    可能出错的代码
except ValueError:
    出错后执行的代码
```

```python
try:
    price = float(input("请输入商品价格："))
    price_accounted = price * 0.9
    print(f"折后价格：{price_accounted}")
except ValueError:
    print("价格必须是数字")
```
==f-string格式：`f"文字{变量}"`，不能写成`f{"文字"}`==

## 完整异常处理结构

```python
try:
    可能出错的代码
except 异常类型1 as 异常变量:
    处理异常1
except 异常类型2:
    处理异常2
else:
    没有发生异常时执行
finally:
    无论是否发生异常都执行
```

执行顺序：

- 没有异常：`try → else → finally`
- 出现并捕获异常：`try → except → finally`

多个异常也可以合并捕获：

```python
try:
    可能出错的代码
except (异常类型1, 异常类型2) as 异常变量:
    处理代码
```

尽量写明异常类型，不建议只写空的 `except:`，否则容易隐藏真正的程序错误。

## 主动抛出异常 `raise`

当输入或数据不符合程序规则时，可以主动抛出异常，立即中断当前正常流程。

```python
if 不符合要求的条件:
    raise 异常类型("错误说明")
```

常见异常类型：

- `ValueError`：数值内容或转换内容不合法
- `TypeError`：对象类型使用不正确
- `ZeroDivisionError`：除数为零
- `FileNotFoundError`：文件不存在
- `KeyError`：字典中不存在指定键
- `IndexError`：索引超出范围

# Math模块
导入math模块
```python
import math
```
导入后
```python
math.工具名称
```
工具包括：圆周率、平方根、幂、向上、向下取整、阶乘、角度转换等
## 圆周率
`math.pi`
==是一个数值，不是函数，不能写math.pi()==
## 平方根
`math.sqrt()` 
## 幂运算
`math.pow(x,r)`
==类似于**，但是math.pow通常返回浮点数==
## 取整
### 向上取整
`math.ceil()`
### 向下取整
`math.floor()`
==**“向上”、“向下”是指数值大小，不是去掉小数部分**==
	eg:`math.ceil(-3.2)=-3`
## 阶乘
`math.factorial()`
	==只能接受非负整数==
## 角度弧度互转
### 角度转弧度
`math.radians()`
### 弧度转角度
`math.degrees()`
## 三角函数
`math.sin()`
`math.cos()`
`math.tan()`

```python
import math
student = 37
up = 6
car = math.ceil(student/up)
distance = math.sqrt(math.pow(4.2,2)+math.pow(5.6,2))
Choices = math.factorial(7)//math.factorial(4) #用//整除
print(f"至少需要的车辆数：{car}\n直线距离：{distance}\n职位安排数量：{Choices}")
```

# Random模块
生成随机结果
`import random`
调用方式：`random.函数名()`
## 随机整数
`random.randint(a,b)`==闭区间==
## 随机选择==列表==里的一个元素
`random.choice([a,b,c])`
或先将列表保存到变量X中再进行随机
`random.choice(X)`
- **结果类型与被选中的列表元素类型相同；列表元素是字符串时，结果才是字符串**
## 在列表中随机选择多个且不重复
`random.sample(列表名,抽取数量)`
- **结果是列表**
==三个重点==
1. 随机的结果一定是列表，**即使只有一个元素**
2. 不会重复
3. 抽取数量不能多于总人数
## 固定随机结果
`random.seed()`  每次得到相同的一组随机结果
## 打乱原列表
`random.shuffle(列表名)`
==**会直接修改原列表**==
不能用其赋值
❌`result = random.shuffle(numbers)`
## 随机小数
`random.uniform(a,b)`
`round(random.uniform(a,b), c)`保留c位小数

```python
import random
participants = [
    "Alice", "Bob", "Cindy", "David",
    "Emma", "Frank", "Grace", "Henry"
]

gifts = ["键盘", "鼠标", "耳机"]
random.seed(2026)
selected = random.sample(participants,3)
results = {}
for i in selected:
	money = random.randint(50,100)
	gift = random.choice(gifts)
	results[i] = {
		"money":money,
		"gift":gift
	}
for key,value in results.items():
	print(f"{key}获得{value['money']}元和{value['gift']}")
```

# datetime
`from datetime import datetime,date,timedelta`
## datetime获取当前日期和时间
```python
from datetime import datetime
now = datetime.now()
print(now)
```
## date获取今天的日期
```python
from datetime import date
today = date.today()
print(today)
```
## 使用 `strftime()` 格式化时间
先通过datetime获取当前日期和时间
接着对时间进行格式化：
```python
now = datetime.now()  
text = now.strftime("%Y年%m月%d日 %H:%M:%S")
```
常见格式符：
```python
%Y：四位年份
%m：月份
%d：日期
%H：24小时制小时
%M：分钟
%S：秒
```
## 使用 `strptime()` 解析字符串
	把字符串形式的时间输入转换为日期时间对象
`exam_date = datetime.strptime(text, "%Y-%m-%d")`
“%Y-%m-%d”格式必须与输入的一致
可以将用strptime()获得的时间相减，获得timedelta对象，用`.days`取得
## 使用`timedelta`做日期加减
```python
today = datetime.now()  
three_days_later = today + timedelta(days=3)
```
```python
timedelta(days=7)
timedelta(hours=2)
timedelta(minutes=30)
```

```python
from datetime import datetime, timedelta
start_text = "2026-07-16"
study_days = 5
start_date = datetime.strptime(start_text,"%Y-%m-%d")
end_date = start_date + timedelta(days=study_days)
exam_text = "2026-07-25"
exam_date = datetime.strptime(exam_text, "%Y-%m-%d")
remaining_days = exam_date - end_date
print(f"学习开始日期：{start_date.strftime('%Y年%m月%d日')}\n学习结束日期：{end_date.strftime('%Y年%m月%d日')}\n距离考试还有：{remaining_days.days}天")
```

# `SymPy`符号计算
```python
import sympy as sp
x = sp.symbols("x")
```
## 展开与因式分解
展开`expand()`：
```python
expression = (x + 2) ** 2
expanded = sp.expand(expression)
```
因式分解`factor`：
```python
expression = x ** 2 - 9
factored = sp.factor(expression)
```
## 化简`simplify()`
```python
expression = (x ** 2 - 1) / (x - 1)
result = sp.simplify(expression)
```
## 解方程`solve()`
使用`Eq()`表达等式：
`sp.Eq(等式左边,等式右边)`
```python
equation = sp.Eq(x ** 2 - 5 * x + 6, 0)
solutions = sp.solve(equation, x)

print(solutions)
```
==当只传一个表达式时，SymPy 默认解表达式=0==
## 求导`diff()`
`sp.diff(表达式, 对哪个变量求导, 求导次数)`
## 积分`integrate()`
不定积分：
`result = sp.integrate(expression, x)`
定积分：
`result = sp.integrate(expression, (未知数, 下界, 上界))`
无穷大：`sp.oo`
## 代入数值`subs()`
`result = expression.subs(未知数,数值)`
## 输出LaTeX格式
`latex_text = sp.latex(expression)`

```python
import sympy as sp
x = sp.symbols("x")
expression = (x - 2)*(x + 4)
expanded = sp.expand(expression)
derivation = sp.diff(expression,x)
solution = sp.solve(expression,x)
integral = sp.integrate(expression,(x,0,3))
latex_text = sp.latex(expanded)
print(f"展开结果；{expanded}\n导数：{derivation}\n方程的解：{solution}\n定积分：{integral}\nLatex：{latex_text}")
```

# Numpy
	高效处理大量数字和多维数组
`import numpy as np`
`a.ndim`：数组a的维度
`a.shape`：每个维度分别有多长，eg：二维数组输出结果为(行数,列数)
`a.size`：整个数组一共有多少元素
`a.dtype`：元素的数据类型
`a.astype(np.数据类型)`:转换数据类型
`a.itemsize`：每个元素占用的字节数
`a.nbytes`：整个数组占用的总字节数，通常等于 `a.size * a.itemsize`

## 固定随机结果

```python
np.random.seed(种子值)
```

使用相同种子并保持相同的随机调用顺序，可以重复得到相同的随机结果。
## 创建数组
```python
a = np.array([1, 2, 3, 4])#创建一维数组
b = np.array([
    [1, 2, 3],
    [4, 5, 6]
])#创建二维数组
```
### 常用数组创建方法
`np.arrange()`：按照固定步长生成创建
	`np.arrange(起点,终点,步长)`：左闭右开
	==适合知道步长的情况下自动创建数组==
`np.linspace()`：平均切成指定数量
	`np.linspace(起点,终点,数量)`：闭区间
	==适合知道数组元素数量的情况下==
`np.zeros()`：创建全是0的数组
	`np.zero(形状)`
`np.ones()`：创建全是1的数组
`np.full()`：使用指定数字填满
	`np.full(形状，填充值)`

## 二维数组索引
`b[行索引, 列索引]`
## 二维数组切片
```python
b[0, :] #取第一行
b[:, 1] #取第二列
```
## 数字批量运算
```python
a = np.array([1, 2, 3])
print(a + 10)
print(a * 2)
print(a ** 2)
```
两个形状相同的数组可以逐元素运算，直接a+b
矩阵乘法：`a@b`
## 通用函数`ufunc`
	一批可以一次处理整个数组的函数
```python
np.abs(a) #批量绝对值
np.sqrt(a) #批量平方根
np.exp(a) #指数函数
np.log(a) #自然对数
np.round(a,x) #四舍五入，x表示保留的小数位数，只是改变精度，不是把数组变成字符串
np.maximum(a,b) #a,b是两个形状相同的数组，或是可以进行广播的数组，每个元素对应比大小后返回一个新的数组
np.minimum(a,b)
```
## 数组形状操作
### `reshape()函数`
`a.reshape(a,b)`把数组改成a行b列的
==改变形状前后，元素总数必须相同==
**可使用-1自动计算行数或列数**
### 转置`.T`
`a.T`或`np.transspose(a)`
一维数组转置后没有变化
### 把多维数组展开成一维
`a.ravel()`：给原数组换一个观察方式，没有真正复制全部数据，修改会导致原数组改变
`a.flatten()`：创建独立副本，通常更安全，但会额外占用内存
`a.reshape(-1)`也可以展开
### 数组的副本`copy()`
==数组之间互相赋值并不能产生新的副本，而是同一个数组的不同名字==
	一般可变对象的赋值都不会自动复制，只是别名
```python
b = a
#两个名字指向同一个文件

b = a.copy()
#把文件复印一份，双方互不影响
```
==切片也可能与原数组共享数据，修改切片会改变原数组==
	python列表切片：通常产生新列表；
	而NumPy的普通切片**通常产生视图**。因为数组可能非常大，为了节省时间和内存
`copy()`可能是浅复制，如多维列表只能复制最外层，小列表依然共享，需要`deepcopy()`深复制

## 常用统计函数
```python
np.sum(a)    # 总和
np.mean(a)   # 平均值
np.max(a)    # 最大值
np.min(a)    # 最小值
```
axis：沿哪个方向计算
`axis=0`：按列计算
`axis=1`：按行计算
`np.mean(a, axis=1)`
```python
import numpy as np
np.random.seed(20181108)
num = np.random.randn(4,3)
data = num.astype(np.float32)
print(data)
print(data.ndim,data.shape,data.size,data.dtype,data.itemsize,data.nbytes)
row_two=data[1,:]
column_three=data[:,2]
reshaped_data=data.reshape(3,4)
row_means=np.mean(data,axis=1)
column_means=np.mean(data,axis=0)
print(row_two,column_three,reshaped_data,row_means,column_means)
```

## 数组的拼接与拆分
### `np.concatenate()`通用拼接
```python
np.concatenate((数组1, 数组2), axis=方向)
```
axis = 0：按行方向拼接（列数不动，增加行）
axis = 1：按列方向拼接（行数不动，增加列）
### `np.vstack()`上下堆叠
```python
result = np.vstack((a, b))
```
对一维数组使用则会将其变成二维数组
在二维数组里相当于`np.concatenate((a, b), axis=0)`
### `np.hstack()`左右堆叠
```python
result = np.hstack((a, b))
```
对一维数组使用则会将它们首尾相接
在二维数组里相当于`np.concatenate((a, b), axis=1)`
### `np.split()`一维数组的平均拆分/按照位置拆分
**平均拆分：**
```python
parts = np.split(a, 3)
```
==必须能够平均分，不然会报错==
**按照位置拆分：**
```python
parts = np.split(a, [x, y,...])
```
x、y，……是拆分位置，相当于拆分成`[;x]、[x,y]、...`（左闭右开）
### 二维数组的拆分
`np.vsplit()`：上下切
```python
parts = np.vsplit(matrix, 2)
```
`np.hsplit()`：左右切
```python
parts = np.hsplit(matrix, 2)
```
拆分之后输出一个列表，里面有三个数组
拆分后的赋值（一维二维均适用）：
**方法一**(适用于不知道分出几段)
```python
parts = np.split(array, [3, 7])
parts[0] = array[:3]
parts[1] = array[3:7]
parts[2] = array[7:]
```
**方法二**（适用于已经明确知道拆分数量）
```python
part1, part2, part3 = np.split(a, 3)
```

## 广播机制`Broadcasting`
==NumPy尝试让较小的数组适应较大的数组，然后进行逐元素运算==
	但并不是真的在内存里复制
如 批量处理数组元素
### 将标量广播到数组
标量：单个数字，标量可以广播到数组中的每个位置
### 将一维数组广播到二维数组
1. 从右侧对齐形状
```python
a = np.array([
    [10, 20, 30],
    [40, 50, 60]
])                      # shape: (2, 3)

b = np.array([1, 2, 3]) # shape: (3,)
```
将b的形状对齐a的右侧，即把b的形状视为(1,3)
2. 虚拟扩展
把`[1,2,3]`扩展成(2,3)的数组
3. 原数组并没有改变
### 广播的基本规则
**从右往左**比较，每一维满足：
	两个数字相同
	其中一个数字是1
	较小的数组缺少这一维，就理解这一维是1
其中的任意一项即可广播
==**即每个维度要么相同，要么可以从1扩展成这个维度**==
不然即使用reshape()改变形状使其符合
可以用行数组和列数组广播成一个表格

## 布尔数组与条件筛选
### 布尔掩码
比较运算会产生**布尔掩码**（一个由True和False构成的数组），可使用布尔掩码筛选数据
即**布尔索引**
```python
mask = scores >= 60
passed_scores = scores[mask]
```
或者
```python
passed_scores = scores[scores >= 60]
```
可以用布尔索引筛选二维数组，但获得的是**一维数组**，不保留原先的表格结构
### 筛选多条件
#### 并且 &
```python
mask = (scores >= 60) & (scores < 90)
```
- ==**不能写`and`，因为`and`只能用来判断单个真假值，但布尔掩码是TF数组**==
- **==用括号避免运算优先级问题==**
#### 或者 |
```python
mask = (scores < 60) | (scores >= 90)
```
### 条件取反 ~
```python
mask = scores >= 60
~mask
```
```python
scores[~(scores >= 60)]
```
### 批量修改数据
#### 使用布尔掩码
```python
scores[scores > 100] = 100
```
#### 使用`np.where()`
	可以同时修改满足&不满足条件的值
```python
scores = np.array([65, 45, 82, 58])
result = np.where(scores >= 60, "及格", "不及格")
```
`result=np.where(data < 0, 0, data)`的作用和`data[data<0]=0`达到的效果一致
**区别**：使用**布尔掩码**批量修改数据会直接修改原数组；而使用**where**会生成新数组
### 统计满足条件的数据数量
布尔掩码里True看作1，False看作0
用`np.sum()`统计满足条件的数据数量
### 检查是否至少有一个/全部满足条件
`np.any()`：检查是否至少有一个满足条件
`np.all()`：检查是否全部满足条件
### 二维数组按行或按列判断
```python
np.all(scores >= 60, axis=1) #按行判断
np.any(scores >= 90, axis=0) #按列判断
```

## 花式索引
	索引不连续的位置
### 一维数组的花式索引
可以直接使用索引列表
```python
selected = a[[0, 3, 4]] #外层括号表示从数组里取数据，内层括号是索引列表
print(selected)
```
或者将索引列表保存为NumPy数组
```python
indices = np.array([0, 3, 4])
result = a[indices]
```
### 二维数组的花式索引
`matrix[行，列]`
- 一次选择多行
```python
selected_rows = matrix[[3, 1]]
```
- 一次选择多列
```python
selected_columns = matrix[:, [2, 0]]
```
- 同时选择行和列
	- 不是取第0、2行和第1、2列组成一个大区域，而是成对索引
```python
matrix[[0, 2], [1, 2]]
```
- 行列组合索引(获取行列交叉位置)
```python
selected = matrix[[0, 2]][:, [1, 2]] #先选出行，再在选完的行内选列
```
**`modified_products[[1,3]][:,[1]]`这种表述会在第一步产生临时副本，不可以放在等号的左边，这种形式只能被查询不能被修改**
==花式索引通常返回副本（新数组），但当直接在左边使用索引时，可以修改原数组==
```python
a = np.array([10, 20, 30, 40])

b = a[[1, 3]]
b[0] = 999 #返回副本
a[[1, 3]] = 0 #修改原数组
```

## 排序
==NumPy默认升序==
**排序后可以生成副本（新数组），也可以修改原数组**
	`np.sort()`生成新数组
	`a.sort()`在原数组上修改
### `np.sort()`排序后返回排序完的数组
==axis=1== 默认按行内部元素排序：`modified_products[[1,3]][:,[1]]`
	也可以写`np.sort(matrix, axis=1)`
==axis=0== 按列排序（每一列内部排序）：`np.sort(matrix, axis=0)`
==axis=None== 所有元素放平后排序：`np.sort(matrix, axis=None)`
### `np.argsort()`排序后返回数组元素原索引
可以再使用排序完的索引得到对应元素
```python
prices = np.array([120, 90, 150, 110])

order = np.argsort(prices)
prices[order]
```
**可以用同一份顺序同步排列其他数组，避免元素对应错位**
### 降序排列
	先升序排列，再用`[::-1]`反转成降序
```python
np.sort()[::-1] #返回降序之后的数组
```
```python
descending_order = np.argsort(prices)[::-1] #返回降序之后的元素原索引
```
```python
np.sort(matrix, axis=1)[:, ::-1] #二维数组按行降序
```
### `np.partition()`部分排序后的数组
	部分排序，但还是完整的数组，取出部分数组要用切片
```python
np.partition(a, n) #把完整排序后应该位于索引n的位置，放到索引n
```
可以用`partition()`找最小的n个数：`np.partition(a, n-1)[:n-1]`
可以用`partition()`找最大的n个数：`np.partition(a,len(a)-n)[:n-1]`
### `np.argpartition()`部分排序之后的数组原索引
找最小的k个数：`indices = np.argpartition(a, k-1)[:k-1]`
找最大的k个数：`indices = np.argpartition(a, len(a) - k)[-k:]`
用花式索引`a[indices]`取数值
**但部分排序内部不保证顺序**，若不关心数值原索引，需要从大到小排序：
```python
values = np.sort(a[indices])[::-1]
```

## NumPy随机数
先用NumPy创建一个“随机数生成器”`rng`：
```python
import numpy as np
rng = np.random.default_rng(42)
```
42是随机种子seed，类比Random库的seed，用来生成同一组随机数
### 均匀分布随机数
#### `rng.random()` 0~1均匀分布随机小数
`rng.random(形状) `
eg.
```python
rng.random((2, 3))
```
#### `rng.uniform()`自选范围均匀分布随机数
```python
rng.uniform(low, high, size)
```
size=形状，可以加标量，也可以加数组（左闭右开）
**`random()`是`uniform()`在`[0,1)`范围下的特殊情况**
#### `rng.integers()`随机整数
```python
rng.integers(low,high,size)
```
### 正态分布随机数`normal()`
```python
rng.normal(size)
```
指定均值与标准差：
```python
rng.normal(loc,scale,size) #loc：均值；scale：标准差
```
### 随机抽样`choice()`
```python
rng.choice(names, size=3)
```
size：抽几个元素，可重复（即默认有放回抽样）
有放回抽样：`replace = True`
无放回抽样：`replace = False`（此时抽取个数不能超过元素个数）
```python
rng.choice(names, size=3, replace=True)
```
按概率抽样：`p=[a,b,c,d,e...]`
```python
rng.choice(
    names,
    size=10,
    p=[0.1, 0.2, 0.3, 0.4]
)
```
### 打乱数组：`shuffle()` 与 `permutation()`
`shuffle()`打乱并直接修改原数组
- 一维数组：
```python
a = np.array([1, 2, 3, 4, 5])

rng.shuffle(a)
```
- 二维数组：默认打乱整行

`permutation()` 返回新数组
```python
new_matrix = rng.permutation(matrix)
```


# OS模块

`os` 模块主要用于管理路径、文件夹以及文件本身；文件内部内容仍主要使用 `open()` 读取或写入。

```python
import os
```

## 路径与当前工作目录

- 路径：文件或文件夹在计算机中的位置。
- 绝对路径：从磁盘或系统根目录开始的完整位置。
- 相对路径：以当前工作目录为起点的位置。
- 当前工作目录不是 Python 界面的某一块，而是程序运行时默认用作相对路径起点的真实文件夹。
- 当前工作目录不一定等于当前 `.py` 文件所在目录。

### 获取当前工作目录

`getcwd()` 返回当前工作目录的**绝对路径**。

```python
当前工作目录 = os.getcwd()
```

当工作目录是 `某个目录` 时：

```python
open("文件名")
```

会以该工作目录为起点查找或创建文件。Python 会自动解析相对路径，不必先手动转换成绝对路径。

### 改变当前工作目录

```python
os.chdir("目标文件夹路径")
```

改变后，后续所有相对路径都会以新的工作目录为起点，因此不建议无必要地频繁修改。

## 拼接与处理路径

### 拼接路径 `join()`

`join()` 只生成路径字符串，不会创建文件或文件夹。

```python
路径 = os.path.join("文件夹", "子文件夹", "文件名")
```

### 转换为绝对路径 `abspath()`

```python
绝对路径 = os.path.abspath(相对路径或路径字符串)
```

即使目标不存在，`abspath()` 也可以根据当前工作目录生成绝对路径字符串。

### 获取路径各部分

```python
最后一部分 = os.path.basename(路径)
所在目录 = os.path.dirname(路径)
文件名主体, 扩展名 = os.path.splitext(文件名或路径)
```

## 判断路径

```python
是否存在 = os.path.exists(路径)
是否为文件 = os.path.isfile(路径)
是否为文件夹 = os.path.isdir(路径)
```

这些函数只返回 `True` 或 `False`，不会自动打印；需要查看时要保存或 `print()`。

## 查看文件夹内容

```python
名称列表 = os.listdir()
名称列表 = os.listdir(文件夹路径)
```

`listdir()` 返回的通常只是文件名和子文件夹名。需要进一步操作时，应使用 `os.path.join()` 与原文件夹路径拼接。

## 创建文件夹

创建一层文件夹：

```python
os.mkdir(文件夹路径)
```

创建多层文件夹：

```python
os.makedirs(多层文件夹路径, exist_ok=True)
```

`exist_ok=True` 表示目标文件夹已经存在时不报错。

## 重命名与移动

```python
os.rename(原路径, 新路径)
```

原路径与新路径位于不同文件夹时，也可以用于移动文件或文件夹，但目标父文件夹必须已经存在。

## 删除

删除文件：

```python
os.remove(文件路径)
```

删除空文件夹：

```python
os.rmdir(文件夹路径)
```

删除前通常先用 `isfile()`、`isdir()` 或 `exists()` 判断；`rmdir()` 不能删除非空文件夹。

## 获取文件大小

```python
文件大小 = os.path.getsize(文件路径)
```

返回单位是字节。

## 与 `open()` 的区别

- `os.path.join()`、`abspath()`：只生成或处理路径字符串。
- `exists()`、`isfile()`、`isdir()`：只检查路径。
- `mkdir()`、`makedirs()`：创建文件夹。
- `rename()`、`remove()`、`rmdir()`：修改或删除文件系统中的项目。
- `open()`：读取、创建或写入文件内容。


```python
import os

if not os.path.exists("study_data"):
    os.makedirs("study_data")

file_path = os.path.join("study_data", "python.txt")

with open(file_path, "w", encoding="utf-8") as file:
    file.write("Python\nNumPy\nSciPy")

is_file = os.path.isfile(file_path)
absolute_path = os.path.abspath(file_path)
file_size = os.path.getsize(file_path)

print("是否为文件：", is_file)
print("文件路径：", absolute_path)
print("文件大小：", file_size, "字节")
print("study_data中的内容：", os.listdir("study_data"))
```

# pickle模块

`pickle` 用于将列表、字典等 Python 对象保存为二进制文件，并在以后恢复为原来的对象类型。不要加载来源不明的 pickle 文件。

```python
import pickle
```

## 保存对象

```python
with open("文件名.pkl", "wb") as file:
    pickle.dump(Python对象, file)
```

## 读取对象

```python
with open("文件名.pkl", "rb") as file:
    Python对象 = pickle.load(file)
```

- `wb`：以二进制方式写入。
- `rb`：以二进制方式读取。
- `dump()`：保存对象。
- `load()`：恢复对象。

# 类和对象
- **类——把同一种事物的数据和相关操作组织在一起**
**创建类**：
```python
class 类名:
	类中的内容
```
==类可以像函数一样接受外部输入==
- **对象——根据类创建出来的具体事物**
**创建对象**：
```python
alice = Student()
bob = Student()
```
- **属性——对象自身保存的数据**
```python
alice.name
alice.score
```
## `_init()_`函数

利用`_init()`函数创建类：
```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score
```
创建对象：
```python
alice = Student("Alice", 90)
bob = Student("Bob", 80)
```
**self**：当前正在创建或操作的这个对象
- **方法——写在类里面，用来操作对象的函数**
```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def introduce(self):
        return f"我是{self.name}，成绩是{self.score}"
```
调用方法：
`alice.introduce()`
括号里不写东西
点号前面的内容自动交给self
==定义方法时必须写 self，调用方法时不用传 self==
## 继承
让特殊的类直接获得普通类已有的对象，只补充自己额外的类
### 父类和子类
```python
class 子类(父类):
    子类新增内容
```
### 子类继承父类内容需要super()
```python
class GraduateStudent(Student):
    def __init__(self, name, score, topic):
        super().__init__(name, score)
        self.topic = topic
```
即借助父类执行：
```python
self.name = name
self.score = score
```
super相当于直接调用父类的程序
## 封装
### 共有属性
`return(f"{basic_info}，利率：{self.interest_rate * 100}%")`
**任何人都可以操作修改**：`对象.balance`
### 单下划线属性
`self._balance`
**表示是内部使用的数据，但仍可以被修改**：`对象._balance`
### 双下划线属性
`self.__balance`
**类外不能直接使用原名称访问，`对象.__balance`会报错**
