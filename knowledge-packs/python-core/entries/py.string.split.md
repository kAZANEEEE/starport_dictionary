---
id: py.string.split
title: 分割字符串
description: 按分隔符把一行字切成若干段
language: python
category_id: programming.basics

object:
  id: string.text
  name: 字符串
  aliases: [文本, 字串, 一行字, 内容, string, text]

action:
  id: convert.transform
  name: 转换
  aliases: [分割, 切开, 拆开, 变成列表, 转成, split]

targets: []

utterances:
  direct:
    - 分割字符串
    - 把字符串按逗号切开
    - 把一行拆成多段
    - 字符串转列表
  questions:
    - 怎么按分隔符拆分字符串
    - 如何把逗号分隔的内容变成列表
    - Python 怎么按空格切分
    - 怎么去掉多余的空格再切
  colloquial:
    - 这行字我想按逗号拆一下
    - 一整串东西怎么拆成一个个
    - 读进来的那行怎么分成几块
  goal_based:
    - 解析 csv 的一行
    - 把日志行拆成字段
  technical:
    - str.split
    - split()
    - split(" ")
    - python string to list
  short_queries:
    - 分割
    - 拆分
    - split
    - 切分

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: str.split 的参数和行为各版本一致
sources:
  - Python 官方文档 str.split
---

# 分割字符串

## 功能描述

按分隔符把字符串切成列表。不传参数时按任意空白切，并自动忽略连续空格。

## 推荐代码

```python
line = "  张三,28, 北京  "

print(line.split(","))        # ['  张三', '28', ' 北京  ']
print(line.split())           # ['张三,28,', '北京']
print(line.strip().split(","))# ['张三', '28', ' 北京']
print([x.strip() for x in line.split(",")])  # ['张三', '28', '北京']
```

## 语句解释

### .split(",")

按逗号切。**不会自动去掉两边的空格**，切出来的元素可能带空白。

### .split()

不带参数：按任意长度的空白切，并且丢弃开头结尾的空格，也不会产生空字符串。
这是“处理人随手敲的文本”时最好用的形式。

### .strip()

去掉首尾空白。切之前 strip 一次，或者切之后对每个元素 strip。

### 列表推导式

`[x.strip() for x in ...]` 是“切完逐个清理”的标准写法。

## 原理解释

`split` 从左往右扫描，遇到分隔符就切一刀。分隔符本身**不会出现在结果里**。
不传分隔符时，Python 用“任意连续空白”当一个分隔符，并且忽略结尾的空白——
所以 `"a  b".split()` 得到 `["a", "b"]` 而不是 `["a", "", "b"]`；
而 `"a  b".split(" ")` 会得到 `["a", "", "b"]`，中间那个空串是真实存在的。

## 注意事项

- `split()` 和 `split(" ")` 行为不同，前者会合并连续空白，后者不会。
- 用 `split(",")` 处理 CSV 只适合最简情况，字段里含逗号或引号必须用 `csv` 模块。
- 切完想取固定几段，用 `a, b, c = line.split(",")`，但段数不匹配会抛 `ValueError`。
- 只想切有限次：`line.split(",", 1)` 只切第一刀，后面整体保留。

## 使用场景

- 解析逗号/制表符分隔的一行数据。
- 从命令行参数或配置里拆出多个值。
- 把一段文字按句子、按词粗切（正式分词要用 jieba）。
