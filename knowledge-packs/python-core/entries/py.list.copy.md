---
id: py.list.copy
title: 复制列表（浅拷贝的坑）
description: 复制一份，但里面的可变元素还是共享的
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "list.copy() / copy.deepcopy()"
signature: "items.copy() / copy.deepcopy(items)"
args:
  - name: "items"
    required: true
    accepts: "要复制的列表（或嵌套结构）"
    nesting: "可以"
returns: "新列表：copy 是浅拷贝（内层共享）；deepcopy 层层独立"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 复制, 副本, 拷贝, copy]

action:
  id: create.new
  name: 创建
  aliases: [复制, 拷贝, 生成副本, 克隆, copy]

targets: []

utterances:
  direct:
    - 复制列表
    - 生成列表副本
    - 深拷贝列表
  questions:
    - 怎么复制一个列表
    - 为什么改了副本原列表也变了
    - 浅拷贝和深拷贝的区别
  colloquial:
    - 想改动又不影响原来的
    - 复制一份结果里面也一起改了
  technical:
    - list.copy
    - 切片复制
    - copy.deepcopy
    - 浅拷贝陷阱
  short_queries:
    - 复制
    - 拷贝
    - 深拷贝

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.3"
version_note: "list.copy 从 3.3 起；切片写法更老；copy.deepcopy 在 copy 模块"
sources:
  - Python 官方文档 list.copy
  - Python 官方文档 copy.deepcopy
---

# 复制列表（浅拷贝的坑）

## 功能描述

输入列表，输出一个新列表；**只复制最外层**，里面的可变元素仍和原列表共享。

## 推荐代码

```python
import copy

a = [1, 2, [3, 4]]

b = a.copy()          # 浅拷贝：外层新、内层共享
b[0] = 99
print(a[0])           # 1 ← 不受影响
b[2].append(5)
print(a[2])           # [3, 4, 5] ← 内层被改了！

c = copy.deepcopy(a)  # 深拷贝：层层都复制
c[2].append(6)
print(a[2])           # [3, 4, 5] ← 不受影响
```

## 语句解释

### a.copy() / a[:] / list(a)

三种浅拷贝写法，效果一样：新建一个列表，里面装的是**同样的元素引用**。

### b[0] = 99 为什么不影响 a

因为赋值是「改的是 b 的槽位」，把它换成另一个对象，a 那个槽位没动。

### b[2].append(5) 为什么影响 a

因为 `b[2]` 和 `a[2]` 指向**同一个内层列表**，改它当然是改同一个东西。

## 原理解释

**一句话：** 浅拷贝只把「目录」抄一份，里面的东西还是原来那些；深拷贝连里面的东西一起复制。

**执行逻辑：**

1. 建一个同样长度的新列表
2. 逐个把原列表元素**的引用**放进去（不复制元素本身）
3. 返回新列表——外层独立、内层共享
4. 深拷贝则在第 2 步递归：遇到容器就再复制一层，直到全是不可变对象

**机器层（可跳过）：** 浅拷贝只分配外层数组；深拷贝要遍历整棵结构。

**边界（从逻辑推出来）：**

- 第 2 步放的是引用，所以「改元素指向」（`b[0]=x`）互不影响，但「改元素内容」（`b[2].append`）会互相影响
- 元素是不可变的（数字、字符串、元组）时，浅拷贝就等于完全独立，不会有坑
- 深拷贝遇到自引用结构也能处理，但会保留共享关系（同一对象只复制一份）
- 深拷贝慢且占内存，只有确实要独立时才用

## 注意事项

- 嵌套列表/字典要独立，必须 `copy.deepcopy`。
- 元素都是不可变对象时，浅拷贝够了。
- `b = a` 不是复制，是起别名——改 b 就是改 a。
- 深拷贝对超大结构会明显变慢，先想清楚是否真的需要。

## 使用场景

- 保留原始数据做对比（需要深拷贝）。
- 生成一份可修改的模板（一维列表浅拷贝就够）。
- 递归/回溯算法里保存中间状态。
