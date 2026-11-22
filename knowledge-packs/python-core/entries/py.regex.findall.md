---
id: py.regex.findall
title: 提取所有匹配内容
description: 用正则从一段文本里把符合条件的片段全部揪出来
language: python
category_id: programming.basics
module: re
origin: stdlib
import: "import re"
qualname: "regex.findall"
signature: "re.findall(规则, 文本)"
args:
  - name: "规则"
    required: true
    accepts: "正则字符串（r\"...\"）"
    nesting: "可以"
  - name: "文本"
    required: true
    accepts: "要在里面找的文本"
    nesting: "可以"
returns: "列表：所有匹配到的内容；规则里有分组时返回的是分组内容"

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

**一句话：** 从头扫到尾，每次匹配成功就记一笔，然后把所有记录交给你。

**执行逻辑：**

1. 从第 0 个位置尝试匹配
2. 成功 → 把这一段记下来，从**这一段的末尾**继续找
3. 失败 → 往后挪一个字符再试
4. 重复 1–3 直到走到字符串末尾
5. 把记下来的东西组成列表返回（没匹配到就是空列表）

**机器层（可跳过）：** 一趟扫描 + 每次匹配一次回溯尝试。

**边界（从逻辑推出来）：**

- 第 2 步从「末尾」继续，所以**不会重叠匹配**：`"aaa"` 用 `"aa"` 只能抓到 1 个
- 规则里有分组时，返回的会是分组内容而不是整段——`(A)(123)` 会得到元组列表
- 因为第 5 步一次性组成列表，文本很大时内存会涨，改用 `finditer`
- 匹配失败不报错，只给空列表，所以「什么都没抓到」和「规则写错」看起来一样
## 注意事项

- 加了分组会让返回结构变化，不需要分组就别加括号（或用 `(?:...)`）。
- 不支持重叠匹配。
- `findall` 一次性把结果全建出来，文本很大时用 `finditer` 省内存。
- 抓 HTML/JSON 别用正则，结构嵌套正则扛不住。

## 使用场景

- 从日志里批量抓错误码、IP、时间。
- 从一段文字里提取所有链接或邮箱。
- 解析命名规范固定的编号。
