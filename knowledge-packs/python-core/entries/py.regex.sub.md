---
id: py.regex.sub
title: 正则替换
description: 按规则把匹配到的部分换掉
language: python
category_id: programming.basics
module: re

object:
  id: regex.pattern
  name: 正则表达式
  aliases: [正则, 规则, 模式, 匹配规则, regex, pattern]

action:
  id: modify.change
  name: 修改
  aliases: [替换, 换成, 改写, 清洗, sub, replace]

targets: []

utterances:
  direct:
    - 正则替换
    - 按规则替换文本
    - 用正则批量替换
  questions:
    - 怎么用正则替换内容
    - 如何把多余空格都换成单个
    - Python 正则怎么替换分组内容
  colloquial:
    - 把文本里所有数字都抹掉
    - 想按模式批量改文字
  technical:
    - re.sub
    - 反向引用 \1
    - sub count 参数
  short_queries:
    - 正则替换
    - sub

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: re.sub 的 (pattern, repl, string, count) 参数稳定
sources:
  - Python 官方文档 re.sub
---

# 正则替换

## 功能描述

输入规则 + 替换内容 + 文本，输出替换后的新字符串；`count` 限制最多替换几次。

## 推荐代码

```python
import re

text = "价格：100 元，折扣后 80 元"
print(re.sub(r"\d+", "N", text))            # 价格：N 元，折扣后 N 元
print(re.sub(r"\d+", "N", text, count=1))   # 只换第一个

# 用分组重新排列
print(re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", "2026-11-22"))  # 22/11/2026

# 压缩多余空白
print(re.sub(r"\s+", " ", "a   b    c"))    # a b c
```

## 语句解释

### re.sub(规则, 替换, 文本)

替换全部匹配。替换内容里的 `\1` `\2` 引用分组——**要用原始字符串 `r"\1"`**。

### count=1

最多替换 1 次。不传就是全换。

### \s+

一个或多个空白字符，用来压缩多余空格。

## 原理解释

`sub` 也是一次从左到右扫描，每次匹配成功后把匹配段替换成新内容，然后从替换后的位置继续。
所以它**不会无限循环**：替换进去的内容不会被同一轮再匹配一次。

替换内容可以是函数：`re.sub(pat, lambda m: m.group().upper(), s)`，能按匹配内容动态决定。

## 注意事项

- 替换串里的反斜杠要写 `r"\1"`，普通字符串 `"\1"` 会变成控制字符。
- 要替换的内容含 `$`、`\` 时注意转义（`re.escape`）。
- 只替换部分时用 `count`，不要自己先切字符串。
- 替换 HTML/JSON 里的内容，先解析再改，别直接 `sub`。

## 使用场景

- 清洗文本（去多余空白、去特殊符号）。
- 批量改格式（日期顺序、电话号码加分隔）。
- 做脱敏（把身份证号、手机号替换成掩码）。
