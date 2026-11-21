---
id: py.regex.match
title: 判断字符串是否匹配正则
description: 用规则检查一段文本的形状对不对
language: python
category_id: programming.basics
module: re

object:
  id: regex.pattern
  name: 正则表达式
  aliases: [正则, 规则, 模式, 匹配规则, regex, pattern]

action:
  id: inspect.check
  name: 判断
  aliases: [匹配, 检查, 判断是否, 校验, match, fullmatch]

targets: []

utterances:
  direct:
    - 判断字符串是否匹配正则
    - 用正则校验格式
    - 检查是否符合规则
  questions:
    - 怎么判断字符串符合某个格式
    - 如何用正则校验手机号
    - Python 正则怎么判断匹配
  colloquial:
    - 想检查这串是不是邮箱格式
    - 这个输入合法吗，用规则卡一下
  technical:
    - re.match
    - re.fullmatch
    - re.search
    - re.compile
  short_queries:
    - 正则
    - match
    - 匹配

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: re 模块接口稳定；3.11 起 re 的解析错误信息更清楚
sources:
  - Python 官方文档 re.match
  - Python 官方文档 re.fullmatch
---

# 判断字符串是否匹配正则

## 功能描述

输入规则 + 字符串，输出匹配结果（`Match` 对象或 `None`）；用 `fullmatch` 才是“整串都符合”。

## 推荐代码

```python
import re

# match：只要求从开头匹配
print(bool(re.match(r"\d+", "123abc")))      # True
print(bool(re.match(r"\d+", "abc123")))      # False（不是从开头）

# fullmatch：整串都必须符合
print(bool(re.fullmatch(r"\d+", "123")))     # True
print(bool(re.fullmatch(r"\d+", "123abc")))  # False

# 实用写法：先编译，再复用
phone = re.compile(r"1[3-9]\d{9}")
print(bool(phone.fullmatch("13800001111")))  # True
```

## 语句解释

### re.match(规则, 字符串)

从**开头**匹配，但**不要求匹配到结尾**——所以 `\d+` 能匹配 `"123abc"`。

### re.fullmatch(...)

整串都必须符合。**校验格式（手机号、身份证）应该用这个**，不是 `match`。

### re.compile(规则)

预编译，规则复用时更快，也避免每次重写格式串。

## 原理解释

`match` 和 `fullmatch` 都是“成功返回 `Match`，失败返回 `None`”，**失败不抛异常**。
`Match` 里还能取分组：`m.group(1)`。

`r"..."` 是原始字符串，正则里反斜杠不会被 Python 先解释一遍——**写正则一律用 `r""`**。

## 注意事项

- 校验格式用 `fullmatch`；`match` 会放过后面多余的内容。
- 用 `r""` 原始字符串，否则 `\d` 可能被当成转义。
- 别在循环里反复 `re.compile`，提到循环外。
- 正则不是万能的：嵌套结构（HTML、JSON）用正则解析必出错，用专门解析器。

## 使用场景

- 校验用户输入（手机号、邮箱、编号）。
- 从日志行里判断有没有关键字。
- 过滤文件名是否符合命名规范。
