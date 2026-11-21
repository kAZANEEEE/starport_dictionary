---
id: py.regex.findall
title: 提取所有匹配内容
description: 用正则从一段文本里把符合条件的片段全部揪出来
language: python
category_id: programming.basics
module: re

object:
  id: regex.pattern
  name: 正则表达式
  aliases: [正则, 规则, 模式, 匹配, regex, pattern]

action:
  id: get.obtain
  name: 获取
  aliases: [提取, 找出, 拿到全部, 抓取, findall, 抽取]

targets: []

utterances:
  direct:
    - 提取所有匹配的内容
    - 用正则找出全部
    - 把文本里的链接都抓出来
  questions:
    - 怎么用正则提取所有匹配项
    - 如何从文本里抓出所有数字
    - Python 正则怎么拿到全部结果
  colloquial:
    - 这段文字里所有邮箱都找出来
    - 想一次抓全，不要只抓第一个
  technical:
    - re.findall
    - re.finditer
    - group
  short_queries:
    - 提取
    - findall

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: re.findall / finditer 接口稳定
sources:
  - Python 官方文档 re.findall
---

# 提取所有匹配内容

## 功能描述

输入规则 + 文本，输出**所有匹配结果的列表**（没有匹配就是空列表）；要位置和分组用 `finditer`。

## 推荐代码

```python
import re

text = "订单号 A123，另一个 B456，还有 C789"
print(re.findall(r"[A-Z]\d{3}", text))   # ['A123', 'B456', 'C789']

# 带分组时，返回的是分组内容
print(re.findall(r"([A-Z])(\d{3})", text))   # [('A','123'), ('B','456'), ('C','789')]

for m in re.finditer(r"[A-Z]\d{3}", text):
    print(m.group(), m.start())
```

## 语句解释

### findall(规则, 文本)

返回列表。**有一条分组就只返回分组内容，多条分组返回元组**——这个行为最容易踩。

### finditer(...)

返回 `Match` 对象的迭代器，能拿到 `.start()`、`.groups()`，适合还要位置信息的场景。

### [A-Z]\d{3}

`[A-Z]` 一个大写字母，`\d{3}` 三个数字。

## 原理解释

`findall` 是“从头扫到尾，每次匹配完从结束位置继续”，所以不会重复匹配同一段。
它**不做重叠匹配**：`"aaa"` 用 `"aa"` 只能抓到 1 个。

不需要分组时别加括号，否则返回值形状会变——这是“明明匹配到了却拿不到完整串”的常见原因。

## 注意事项

- 加了分组会让返回结构变化，不需要分组就别加括号（或用 `(?:...)`）。
- 不支持重叠匹配。
- `findall` 一次性把结果全建出来，文本很大时用 `finditer` 省内存。
- 抓 HTML/JSON 别用正则，结构嵌套正则扛不住。

## 使用场景

- 从日志里批量抓错误码、IP、时间。
- 从一段文字里提取所有链接或邮箱。
- 解析命名规范固定的编号。
