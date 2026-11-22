---
id: py.regex.match
title: 判断字符串是否匹配正则
description: 用规则检查一段文本的形状对不对
language: python
category_id: programming.basics
module: re
origin: stdlib
import: "import re"
qualname: "re.fullmatch() / re.match()"
signature: "re.fullmatch(规则, 文本) / re.match(规则, 文本)"
args:
  - name: "规则"
    required: true
    accepts: "正则字符串，必须用 r\"...\" 原始字符串"
    nesting: "可以，可以是 re.compile 过的对象"
  - name: "文本"
    required: true
    accepts: "要检查的字符串"
    nesting: "可以"
returns: "Match 对象或 None；校验格式用 fullmatch（match 只要求从开头匹配）"

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

**一句话：** 拿一条规则去卡字符串开头，卡得上就返回匹配结果，卡不上就返回 None。

**执行逻辑：**

1. 把规则编译成内部对象（`compile` 过就复用）
2. 从字符串**第 0 个字符**开始尝试匹配
3. 规则里的 `\d+` 这类片段尽可能多吃字符
4. 整条规则走通 → 返回 `Match`；中途失败 → 从头换种吃法再试（回溯）
5. 从开头就卡不上 → 返回 None（**不抛异常**）

**机器层（可跳过）：** 回溯型匹配，最坏情况会指数级变慢（嵌套量词时）。

**边界（从逻辑推出来）：**

- 第 2 步只从开头试，所以 `"abc123"` 用 `\d+` 匹配失败——它不扫描中间
- 第 3 步「尽可能多吃」，但**不要求吃到结尾**，所以 `"123abc"` 能匹配成功
- 要「整串都必须符合」得用 `fullmatch`，格式校验都该用它
- 第 4 步的回溯在极端规则下会很慢，写正则要避免嵌套量词
## 注意事项

- 校验格式用 `fullmatch`；`match` 会放过后面多余的内容。
- 用 `r""` 原始字符串，否则 `\d` 可能被当成转义。
- 别在循环里反复 `re.compile`，提到循环外。
- 正则不是万能的：嵌套结构（HTML、JSON）用正则解析必出错，用专门解析器。

## 使用场景

- 校验用户输入（手机号、邮箱、编号）。
- 从日志行里判断有没有关键字。
- 过滤文件名是否符合命名规范。
