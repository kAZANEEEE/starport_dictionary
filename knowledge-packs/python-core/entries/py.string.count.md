---
id: py.string.count
title: 统计子串出现几次
description: 一段文字里某个词出现了多少回
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.count()"

object:
  id: string.text
  name: 字符串
  aliases: [文本, 子串, 关键词, 一段文字, string]

action:
  id: get.obtain
  name: 获取
  aliases: [统计, 计数, 数出现次数, 算, count]

targets: []

utterances:
  direct:
    - 统计子串出现次数
    - 某个词出现了几次
    - 字符串计数
  questions:
    - 怎么统计一个词在文本里出现几次
    - 如何数某个字符出现多少回
    - count 会重叠计数吗
  colloquial:
    - 想数一数这段文字里这个词出现几次
    - 日志里这个错误出现了多少条
  technical:
    - str.count
    - 不重叠计数
    - 统计关键词
  short_queries:
    - 计数
    - 次数
    - count

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: str.count 的 (sub, start, end) 参数各版本一致
sources:
  - Python 官方文档 str.count
---

# 统计子串出现几次

## 功能描述

输入字符串 + 子串，输出出现次数（整数）；**不重叠计数**，找不到返回 0 而不是报错。

## 推荐代码

```python
text = "错误 错误 还是错误"

print(text.count("错误"))      # 3
print(text.count("不存在"))    # 0

print("aaaa".count("aa"))      # 2 —— 不重叠，不是 3

print(text.count("错误", 0, 5))  # 只在前 5 个字符里数
```

## 语句解释

### .count(子串)

从左到右扫，每找到一个就把位置跳过该子串长度继续找。

### 找不到返回 0

不抛异常，所以「一次都没有」和「规则写错」在返回值上看起来一样。

### count(子, 起, 止)

只在指定区间里数，区间规则和切片一致（含头不含尾）。

## 原理解释

**一句话：** 它从头往后找，每找到一个就把指针挪到这个词的**末尾**，再继续找——所以互相重叠的不会重复计。

**执行逻辑：**

1. 指针放到起点
2. 从指针位置开始找子串
3. 找到 → 计数加 1，指针挪到这次匹配的**末尾**
4. 找不到 → 结束，返回计数

**机器层（可跳过）：** 内部用高效的子串搜索，最坏 O(n×m)，实际远快于此。

**边界（从逻辑推出来）：**

- 第 3 步「挪到末尾」导致不重叠：`"aaaa".count("aa")` 得 2，不是 3
- 第 4 步找不到就返回，所以结果是 0——**不是错误**，判断「是不是真的有」不能只看 count
- 因为不做任何编码/大小写处理，所以 `"Py".count("py")` 是 0
- 想数「不区分大小写的出现次数」要先统一 `.lower()`，但那会改变长度（极少数语言），统计位置时要注意

## 注意事项

- 不重叠计数，`"aaa".count("aa")` 是 1。
- 区分大小写，需要忽略就先 `lower()`。
- 统计单词出现次数建议先按空白切分成词，否则 `cat` 会把 `concatenate` 也算上。
- 统计多种模式、需要位置时用 `re.finditer`。

## 使用场景

- 日志里某个错误码出现多少次。
- 简单关键词热度统计。
- 检查文本里是否包含多个标记（`count` 大于 0）。
