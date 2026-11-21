---
id: py.list.remove
title: 按值删除列表元素
description: 知道值不知道下标，怎么把它从列表里拿掉
language: python
category_id: programming.basics
module: list

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 某个值, 元素值, items]

action:
  id: delete.remove
  name: 删除
  aliases: [删除, 去掉, 移除, 拿掉, remove, pop]

targets: []

utterances:
  direct:
    - 按值删除列表元素
    - 删掉列表里的某个值
    - 从列表移除元素
  questions:
    - 怎么删除列表里指定的值
    - remove 和 pop 有什么区别
    - 值不存在会报错吗
  colloquial:
    - 知道内容不知道是第几个，怎么删
    - 想把所有相同的都删掉
  technical:
    - list.remove
    - list.pop
    - del 语句
    - 遍历时删除
  short_queries:
    - 删除元素
    - remove
    - pop

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: list.remove / pop / del 各版本一致
sources:
  - Python 官方文档 list.remove
  - Python 官方文档 list.pop
---

# 按值删除列表元素

## 功能描述

输入一个值，`remove` 删掉**第一个相等**的元素（原地改，返回 None）；`pop` 按**下标**删并返回被删的元素。

## 推荐代码

```python
nums = [1, 2, 3, 2]

nums.remove(2)          # 只删第一个 2
print(nums)             # [1, 3, 2]

last = nums.pop()       # 删最后一个并返回
print(last, nums)       # 2 [1, 3]

del nums[0]             # 按下标删，无返回值
print(nums)             # [3]

# 想删掉所有等于 2 的：重建列表，别边遍历边删
print([x for x in [1, 2, 2, 3] if x != 2])
```

## 语句解释

### remove(值)

从左往右找第一个相等的元素并删除。**值不存在抛 `ValueError`**。

### pop(下标)

默认删最后一个。返回被删的元素。**下标越界抛 `IndexError`**。

### del 列表[下标]

按下标删，不返回值，可以切片批量删。

### 推导式重建

要删「所有匹配」时最安全：不在原列表上动刀。

## 原理解释

**一句话：** 列表是一排紧挨着的格子，删掉一个，后面的所有元素都要往前挪一格。

**执行逻辑（`remove`）：**

1. 从第 0 个格子开始，拿值跟目标比
2. 相等 → 从这个位置开始，把后面每个元素往前挪一格
3. 列表长度减 1
4. 直接返回，**后面的相同值不再处理**

**机器层（可跳过）：** 挪动是内存拷贝，所以删列表靠前的位置更慢，O(n)。

**边界（从逻辑推出来）：**

- 第 4 步「只处理第一个」是 `remove` 的定义，要全删必须自己重建列表
- 第 2 步要挪动，所以「遍历列表的同时删除」会让下标错位，漏掉元素——正确做法是重建或倒序遍历
- 因为要挪动，删除代价与「被删位置之后的元素个数」成正比
- `pop()` 删末尾最便宜（不用挪），删开头最贵

## 注意事项

- `remove` 值是「相等」判断，`1` 和 `True` 会被认为相等。
- 值不存在抛 `ValueError`，不确定就先 `if x in lst`。
- **别在 for 循环里删同一个列表**，会跳过元素；改用推导式或倒序。
- `remove` 原地改并返回 None。

## 使用场景

- 从待办列表里移除完成的一项。
- 用户取消某个选项。
- 清理无效数据（配合筛选重建）。
