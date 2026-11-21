---
id: py.string.upper_lower
title: 转换大小写
description: 全部变大写、变小写，或者首字母大写
language: python
category_id: programming.basics
module: str

object:
  id: string.text
  name: 字符串
  aliases: [文本, 字串, 大小写, 字母, string]

action:
  id: convert.transform
  name: 转换
  aliases: [转换, 变大写, 变小写, 首字母大写, upper, lower]

targets: []

utterances:
  direct:
    - 字符串转大写
    - 全部变小写
    - 首字母大写
  questions:
    - 怎么把字符串变成大写
    - 如何忽略大小写比较
    - Python 怎么把首字母大写
  colloquial:
    - 用户输入大小写乱七八糟，想统一
    - 比较的时候不想管大小写
  technical:
    - str.upper
    - str.lower
    - casefold
    - title
  short_queries:
    - 大写
    - 小写
    - upper
    - lower

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: casefold 从 3.3 起，用于更彻底的不区分大小写比较
sources:
  - Python 官方文档 str.upper
  - Python 官方文档 str.casefold
---

# 转换大小写

## 功能描述

输入字符串，输出大小写变换后的**新字符串**；原字符串不变。

## 推荐代码

```python
s = "Hello World"

print(s.upper())        # HELLO WORLD
print(s.lower())        # hello world
print(s.title())        # Hello World
print(s.capitalize())   # Hello world（只有第一个字母大写）

# 不区分大小写地比较
print("PyThOn".lower() == "python")   # True
```

## 语句解释

### .upper() / .lower()

全大写 / 全小写。返回新串。

### .title()

每个单词首字母大写（按空格切分判断）。

### .capitalize()

整个字符串首字母大写，其余全部小写——和 `title()` 不一样。

### .casefold()

比 `lower()` 更彻底，德语 ß 这类字符也能正确比较。要做「不区分大小写比较」用它。

## 原理解释

**一句话：** 它按字符逐个查表，把每个字母换成对应的大写或小写形态。

**执行逻辑：**

1. 从第一个字符开始
2. 查这个字符有没有大小写对应形态：有就换成目标形态，没有就原样保留
3. 把结果写进新字符串
4. 走到结尾，返回新串

**机器层（可跳过）：** 按 Unicode 表逐字符映射，一次线性遍历。

**边界（从逻辑推出来）：**

- 第 2 步「没有对应形态就原样」，所以数字、标点、中文都不受影响
- 因为返回新串，原变量不变：必须 `s = s.upper()`
- 大小写映射不是一一对应（某些语言一个字符能变成两个），所以 `len()` 可能变长
- `title()` 是按「单词边界」判断的，`"don't".title()` 会得到 `"Don'T"`——这就是它不常用在标题外的原因

## 注意事项

- 转换返回新串，别指望原地改。
- 比较时统一 `lower()`/`casefold()`，但**存库前想清楚**要不要保留原样。
- `title()` 对带撇号的词会出错，标题场景宁可自己按空格切。
- 中文没有大小写，这几个方法对中文是原样返回。

## 使用场景

- 统一用户输入（邮箱、命令）。
- 不区分大小写的搜索和比较。
- 生成标题、规范化的文件名。
