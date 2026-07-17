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
num[a:b]
```

切片：从列表中摘取片段，左闭右开

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
## 标准正态分布随机数组
`np.random.randn(a,b)`
生成一个a行b列的随机数组，其中数字来自标准正态分布
## 改变数组形状
`a.reshape(a,b)`把数组改成a行b列的
==改变形状前后，元素总数必须相同==
**可使用-1自动计算行数或列数**
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
