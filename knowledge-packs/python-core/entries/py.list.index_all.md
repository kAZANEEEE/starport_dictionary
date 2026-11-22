---
id: py.list.index_all
title: 找出所有匹配的位置
description: index 只给第一个，想全找出来得换写法
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "[i for i, x in enumerate(items) if 条件]"
signature: "[i for i, x in enumerate(items) if x == 目标]"
args:
  - name: "items"
    required: true
    accepts: "要搜索的列表"
    nesting: "可以"
  - name: "条件"
    required: true
    accepts: "判断每个元素是否符合的表达，如 x == 3"
    nesting: "可以，可以是复合条件"
returns: "列表：所有匹配元素的下标（按出现顺序）；没有匹配返回空列表"
object:
  id: list.element
  name: 列表元素
  aliases: [列表, 位置, 下标, 所有匹配, items]
action:
  id: search.find
  name: 查找
  aliases: [找全部, 找所有位置, 定位, 搜索, find]
targets: []
utterances:
  direct:
    - 找出所有匹配的位置
    - 找所有下标
    - 列出等于某值的所有位置
  questions:
    - 怎么找到所有出现的下标
    - index 只能给第一个，怎么全拿
    - 怎么找出所有符合条件的元素位置
  colloquial:
    - 这个值出现了好几处，都想找出来
    - 想知道所有「错误」出现在第几行
  technical:
    - enumerate 推导式
    - list.index
    - 所有匹配下标
  short_queries:
    - 所有位置
    - 全部下标
    - 查找全部
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "enumerate + 推导式各版本一致"
sources:
  - Python 官方文档 enumerate
  - Python 官方文档 list.index
---

# 找出所有匹配的位置

## 功能描述

输入列表 + 条件，输出**所有**满足条件的下标；`list.index()` 只给第一个，所以要自己遍历。

## 推荐代码

```python
items = ["错误", "正常", "错误", "警告", "错误"]

print(items.index("错误"))                                  # 0 只给第一个
print([i for i, x in enumerate(items) if x == "错误"])      # [0, 2, 4]

# 条件可以是任意表达式
nums = [3, 8, 12, 5]
print([i for i, n in enumerate(nums) if n > 5])             # [1, 2]
```

## 语句解释

### enumerate(items)

产出 `(下标, 元素)`。

### 推导式里只要下标

`[i for i, x in ...]` 只把下标收进结果，元素用 `x` 参与判断。

### 和 index 的区别

`index` 一找到就停；推导式会走完整列表。

## 原理解释

**一句话：** 它从头到尾走一遍，每遇到一个符合条件的就把它的位置记下来。

**执行逻辑：**

1. 下标从 0 开始
2. 取一个元素，判断条件
3. 成立 → 记下当前下标
4. 不成立 → 跳过
5. 走完返回记下的下标列表

**机器层（可跳过）：** 一趟遍历，O(n)，不会提前停止。

**边界（从逻辑推出来）：**

- 第 3 步「记下所有」是它和 `index` 的区别：`index` 在第一个命中就返回
- 没有匹配时返回空列表（不是 -1、也不报错）
- 因为走完整列表，元素多时比 `index` 慢——但只要第一个就用 `index`
- 条件里能写任意表达式，所以「找所有大于 5 的位置」也一个写法

## 注意事项

- 要是只要第一个，用 `index` 更快。
- 拿到的下标可以直接去切片或改元素。
- 别在遍历的同时删元素，会让后面的下标偏移。
- 需要「元素 + 下标」都要，把 `x` 也收进结果：`[(i, x) for ...]`。

## 使用场景

- 找出所有出错行的行号。
- 批量替换前先定位所有目标。
- 统计某值分布在哪些位置。
