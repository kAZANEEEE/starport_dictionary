---
id: py.string.find
title: 查找子串位置
description: 某个词在第几个字符出现，找不到返回 -1
language: python
category_id: programming.basics
module: str

object:
  id: string.text
  name: 字符串
  aliases: [文本, 子串, 关键词, 位置, string]

action:
  id: search.find
  name: 查找
  aliases: [查找位置, 找下标, 定位, 在哪里, find, index]

targets: []

utterances:
  direct:
    - 查找子串位置
    - 某个词在第几位
    - 找子串的下标
  questions:
    - 怎么找一个子串在字符串里的位置
    - 找不到的时候会怎样
    - find 和 index 有什么区别
  colloquial:
    - 想知道这个词从第几个字开始
    - 找不到别报错，给个 -1 就行
  technical:
    - str.find
    - str.index
    - str.rfind
  short_queries:
    - 位置
    - find
    - index

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: find / rfind / index 各版本一致
sources:
  - Python 官方文档 str.find
  - Python 官方文档 str.index
---

# 查找子串位置

## 功能描述

输入字符串 + 子串，输出首次出现的下标；`find` 找不到返回 **-1**，`index` 找不到**抛异常**。

## 推荐代码

```python
s = "hello world"

print(s.find("world"))     # 6
print(s.find("xyz"))       # -1（不报错）
print(s.find("o"))         # 4（第一次出现）
print(s.rfind("o"))        # 7（最后一次）

try:
    s.index("xyz")
except ValueError as exc:
    print("index 会抛异常:", exc)
```

## 语句解释

### find(子串)

首次出现的下标，找不到返回 -1。

### rfind(子串)

最后一次出现的下标，找不到同样是 -1。

### index(子串)

和 `find` 一样找位置，但**找不到抛 `ValueError`**。

## 原理解释

**一句话：** 从左边开始一个位置一个位置地试，试到能对上就返回那个位置，试完都不行就说不存在。

**执行逻辑：**

1. 把指针放在位置 0
2. 从指针处开始，拿子串去比对
3. 对上 → 返回当前指针位置
4. 对不上 → 指针右移一位，回到第 2 步
5. 指针走到「长度 - 子串长度」还不行 → `find` 返回 -1，`index` 抛 `ValueError`

**机器层（可跳过）：** 朴素匹配最坏 O(n×m)，实际实现会用更快的子串搜索算法。

**边界（从逻辑推出来）：**

- 第 3 步返回的是**第一次**匹配的位置，后面的不管；要最后一次用 `rfind`
- 第 5 步两种方法行为相反：`find` 给 -1（可以当假值判断），`index` 抛错（必须包 try）
- 返回的是**字符下标**，中文也是一个字符算一位（不是字节）
- 找空字符串（`s.find("")`）返回 0，因为空串在任何位置都能匹配

## 注意事项

- `if s.find(x):` 是错的写法——位置 0 会被当成假；用 `if s.find(x) != -1` 或 `x in s`。
- 需要「找不到就报错」用 `index`，需要「找不到就继续」用 `find`。
- 找位置记得是**字符**下标，切片时直接用正好。
- 多模式、要分组时用 `re.search`。

## 使用场景

- 从文本里定位关键字段的起始位置。
- 检查某段是否存在（`!= -1` 或 `in`）。
- 取某个标记之前的子串（配合切片）。
