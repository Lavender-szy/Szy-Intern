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

## 匿名函数与filter

```python
result = list(filter(lambda x: 条件, 可迭代对象))
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
`math.ceil`
### 向下取整
`math.floor()`
==**“向上”、“向下”是指数值大小，不是去掉小数部分**==
	eg:`math.ceil(-3.2)=-3`
## 阶乘
`math.factorial()`
	==只能接受非负数==
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
`random.radiant(a,b)`==闭区间==
## 随机选择==列表==里的一个元素
`random.choice([a,b,c])`
或先将列表保存到变量X中再进行随机
`random.choice(X)`
- **结果是字符串**
## 在列表中随机选择多个且不重复
`random.sample(列表名,抽取数量)`
- **结果是列表**
==三个重点==
1. 随机的结果一定是列表，**即使只有一个元素**
2. 不会重复
3. 抽取数量不能多于总人数
## 固定随机结果
