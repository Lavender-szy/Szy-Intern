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

# 固定随机结果

```python
np.random.seed(种子值)
```

使用相同种子并保持相同的随机调用顺序，可以重复得到相同的随机结果。
# 创建数组
```python
a = np.array([1, 2, 3, 4])#创建一维数组
b = np.array([
    [1, 2, 3],
    [4, 5, 6]
])#创建二维数组
```
## 常用数组创建方法
`np.arange()`：按照固定步长生成创建
	`np.arange(起点,终点,步长)`：左闭右开
	==适合知道步长的情况下自动创建数组==
`np.linspace()`：平均切成指定数量
	`np.linspace(起点,终点,数量)`：闭区间
	==适合知道数组元素数量的情况下==
`np.zeros()`：创建全是0的数组
	`np.zeros(形状)`
`np.ones()`：创建全是1的数组
`np.full()`：使用指定数字填满
	`np.full(形状，填充值)`

# 二维数组索引
`b[行索引, 列索引]`
# 二维数组切片
```python
b[0, :] #取第一行
b[:, 1] #取第二列
```
# 数字批量运算
```python
a = np.array([1, 2, 3])
print(a + 10)
print(a * 2)
print(a ** 2)
```
两个形状相同的数组可以逐元素运算，直接a+b
矩阵乘法：`a@b`
# 通用函数`ufunc`
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
# 数组形状操作
## `reshape()函数`
`a.reshape(a,b)`把数组改成a行b列的
==改变形状前后，元素总数必须相同==
**可使用-1自动计算行数或列数**
## 转置`.T`
`a.T`或`np.transpose(a)`
一维数组转置后没有变化
## 把多维数组展开成一维
`a.ravel()`：给原数组换一个观察方式，没有真正复制全部数据，修改会导致原数组改变
`a.flatten()`：创建独立副本，通常更安全，但会额外占用内存
`a.reshape(-1)`也可以展开
## 数组的副本`copy()`
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

# 常用统计函数
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

# 数组的拼接与拆分
## `np.concatenate()`通用拼接
```python
np.concatenate((数组1, 数组2), axis=方向)
```
axis = 0：按行方向拼接（列数不动，增加行）
axis = 1：按列方向拼接（行数不动，增加列）
## `np.vstack()`上下堆叠
```python
result = np.vstack((a, b))
```
对一维数组使用则会将其变成二维数组
在二维数组里相当于`np.concatenate((a, b), axis=0)`
## `np.hstack()`左右堆叠
```python
result = np.hstack((a, b))
```
对一维数组使用则会将它们首尾相接
在二维数组里相当于`np.concatenate((a, b), axis=1)`
## `np.split()`一维数组的平均拆分/按照位置拆分
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
## 二维数组的拆分
`np.vsplit()`：上下切
```python
parts = np.vsplit(matrix, 2)
```
`np.hsplit()`：左右切
```python
parts = np.hsplit(matrix, 2)
```
以上示例拆分之后输出一个列表，里面有两个数组
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

# 广播机制`Broadcasting`
==NumPy尝试让较小的数组适应较大的数组，然后进行逐元素运算==
	但并不是真的在内存里复制
如 批量处理数组元素
## 将标量广播到数组
标量：单个数字，标量可以广播到数组中的每个位置
## 将一维数组广播到二维数组
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
## 广播的基本规则
**从右往左**比较，每一维满足：
	两个数字相同
	其中一个数字是1
	较小的数组缺少这一维，就理解这一维是1
其中的任意一项即可广播
==**即每个维度要么相同，要么可以从1扩展成这个维度**==
不然即使用reshape()改变形状使其符合
可以用行数组和列数组广播成一个表格

# 布尔数组与条件筛选
## 布尔掩码
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
## 筛选多条件
### 并且 &
```python
mask = (scores >= 60) & (scores < 90)
```
- ==**不能写`and`，因为`and`只能用来判断单个真假值，但布尔掩码是TF数组**==
- **==用括号避免运算优先级问题==**
### 或者 |
```python
mask = (scores < 60) | (scores >= 90)
```
## 条件取反 ~
```python
mask = scores >= 60
~mask
```
```python
scores[~(scores >= 60)]
```
## 批量修改数据
### 使用布尔掩码
```python
scores[scores > 100] = 100
```
### 使用`np.where()`
	可以同时修改满足&不满足条件的值
```python
scores = np.array([65, 45, 82, 58])
result = np.where(scores >= 60, "及格", "不及格")
```
`result=np.where(data < 0, 0, data)`的作用和`data[data<0]=0`达到的效果一致
**区别**：使用**布尔掩码**批量修改数据会直接修改原数组；而使用**where**会生成新数组
## 统计满足条件的数据数量
布尔掩码里True看作1，False看作0
用`np.sum()`统计满足条件的数据数量
## 检查是否至少有一个/全部满足条件
`np.any()`：检查是否至少有一个满足条件
`np.all()`：检查是否全部满足条件
## 二维数组按行或按列判断
```python
np.all(scores >= 60, axis=1) #按行判断
np.any(scores >= 90, axis=0) #按列判断
```

# 花式索引
	索引不连续的位置
## 一维数组的花式索引
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
## 二维数组的花式索引
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
- 行列组合索引(获取行列交叉位置)——**链式花式索引**
```python
selected = matrix[[0, 2]][:, [1, 2]] #先选出行，再在选完的行内选列
```
**`modified_products[[1,3]][:,[1]]`这种表述会在第一步产生临时副本，不可以放在等号的左边，这种形式只能被查询不能被修改，若想要被修改，则使用`np.ix_()`**
- 行列组合索引——**`np.ix_()`**
```python
result = a[np.ix_([0, 2], [1, 3])]
```
`np.ix_()`接收两个一维索引序列，不需要嵌套
==花式索引通常返回副本（新数组），但当直接在左边使用索引时，可以修改原数组==
```python
a = np.array([10, 20, 30, 40])

b = a[[1, 3]]
b[0] = 999 #返回副本
a[[1, 3]] = 0 #修改原数组
```

# 排序
==NumPy默认升序==
**排序后可以生成副本（新数组），也可以修改原数组**
	`np.sort()`生成新数组
	`a.sort()`在原数组上修改
## `np.sort()`排序后返回排序完的数组
==axis=1== 默认按行内部元素排序：`modified_products[[1,3]][:,[1]]`
	也可以写`np.sort(matrix, axis=1)`
==axis=0== 按列排序（每一列内部排序）：`np.sort(matrix, axis=0)`
==axis=None== 所有元素放平后排序：`np.sort(matrix, axis=None)`
## `np.argsort()`排序后返回数组元素原索引
可以再使用排序完的索引得到对应元素
```python
prices = np.array([120, 90, 150, 110])

order = np.argsort(prices)
prices[order]
```
**可以用同一份顺序同步排列其他数组，避免元素对应错位**
## 降序排列
	先升序排列，再用`[::-1]`反转成降序
```python
np.sort(a)[::-1] #返回降序之后的数组
```
```python
descending_order = np.argsort(prices)[::-1] #返回降序之后的元素原索引
```
```python
np.sort(matrix, axis=1)[:, ::-1] #二维数组按行降序
```
## `np.partition()`部分排序后的数组
	部分排序，但还是完整的数组，取出部分数组要用切片
```python
np.partition(a, n) #把完整排序后应该位于索引n的位置，放到索引n
```
可以用`partition()`找最小的n个数：`np.partition(a, n-1)[:n]`
可以用`partition()`找最大的n个数：`np.partition(a,len(a)-n)[-n:]`
## `np.argpartition()`部分排序之后的数组原索引
找最小的k个数：`indices = np.argpartition(a, k-1)[:k]`
找最大的k个数：`indices = np.argpartition(a, len(a) - k)[-k:]`
用花式索引`a[indices]`取数值
**但部分排序内部不保证顺序**，若不关心数值原索引，需要从大到小排序：
```python
values = np.sort(a[indices])[::-1]
```

# NumPy随机数
先用NumPy创建一个“随机数生成器”`rng`：
```python
import numpy as np
rng = np.random.default_rng(42)
```
42是随机种子seed，类比Random库的seed，用来生成同一组随机数
## 均匀分布随机数
### `rng.random()` 0~1均匀分布随机小数
`rng.random(形状) `
eg.
```python
rng.random((2, 3))
```
### `rng.uniform()`自选范围均匀分布随机数
```python
rng.uniform(low, high, size)
```
size=形状，可以加标量，也可以加数组（左闭右开）
**`random()`是`uniform()`在`[0,1)`范围下的特殊情况**
### `rng.integers()`随机整数
```python
rng.integers(low,high,size)
```
## 正态分布随机数`normal()`
```python
rng.normal(size=size)
```
指定均值与标准差：
```python
rng.normal(loc,scale,size) #loc：均值；scale：标准差
```
## 随机抽样`choice()`
```python
rng.choice(names, size=3)
```
size：抽几个元素，可重复（即默认有放回抽样）
有放回抽样：`replace = True`
无放回抽样：`replace = False`（此时抽取个数不能超过元素个数）
```python
rng.choice(names, size=3, replace=False)
```
按概率抽样：`p=[a,b,c,d,e...]`
```python
rng.choice(
    names,
    size=10,
    p=[0.1, 0.2, 0.3, 0.4]
)
```
## 打乱数组：`shuffle()` 与 `permutation()`
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
