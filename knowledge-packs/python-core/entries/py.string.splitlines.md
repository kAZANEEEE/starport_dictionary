---
id: py.string.splitlines
title: 按行切分文本
description: 把多行文本变成行的列表，自动处理各种换行
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.splitlines()"
signature: "s.splitlines(keepends=False)"
args:
  - name: "keepends"
    required: false
    default: "False"
    accepts: "True = 每行保留行尾换行符；False = 去掉"
    nesting: "一般直接写 True/False"
returns: "列表：每一行一个字符串；空行会保留，末尾没有多余空元素"
object:
  id: string.text
  name: 字符串
  aliases: [文本, 多行文本, 每一行, 行列表, string]
action:
  id: convert.transform
  name: 转换
  aliases: [按行切分, 拆成行, 分行, splitlines]
targets: []
utterances:
  direct:
    - 按行切分文本
    - 把多行文本变成列表
    - 文本分行
  questions:
    - 怎么把多行字符串拆成行的列表
    - splitlines 和 split("\n") 有什么区别
    - 怎么处理 \r\n 换行
  colloquial:
    - 读进来一大段文字，想按行处理
    - Windows 的换行和 Linux 不一样，怎么统一
  technical:
    - str.splitlines
    - 换行符
    - keepends
  short_queries:
    - 分行
    - splitlines
    - 按行
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "splitlines 各版本一致；它认得 \\n、\\r\\n、\\r 等多种换行"
sources:
  - Python 官方文档 str.splitlines
---

# 按行切分文本

## 功能描述

输入一段多行文本，输出每行一个元素的列表；自动识别 `\n`、`\r\n`、`\r` 等换行，并且**不会留下末尾空元素**。

## 推荐代码

```python
text = "第一行\n第二行\n\n第四行"

print(text.splitlines())          # ['第一行', '第二行', '', '第四行']
print("a\r\nb".splitlines())      # ['a', 'b']  ← 自动处理 \r\n
print("a\r\nb".split("\n"))       # ['a\r', 'b']  ← 会留个 \r

print(text.splitlines(keepends=True))   # 保留换行符
```

## 语句解释

### splitlines()

按换行切，**换行符本身不会出现在结果里**。

### 和 split("\n") 的区别

`split("\n")` 只认 `\n`，`\r\n` 会留下尾部的 `\r`；`splitlines()` 认得多种换行。

### keepends=True

保留行尾换行符，需要「原样拼回去」时用。

## 原理解释

**一句话：** 它一路扫过去，遇到任何一种换行标记就切一刀，切完不把换行符放进结果。

**执行逻辑：**

1. 从开头扫，记住这一行从哪开始
2. 遇到 `\n`、`\r`、`\r\n` 等换行标记
3. 把「开始位置到换行前」那一段放进列表
4. 跳过换行标记，重置开始位置
5. 走到结尾：**如果还剩内容才收尾**，所以末尾的换行不会产生空元素

**机器层（可跳过）：** 一次线性扫描。

**边界（从逻辑推出来）：**

- 第 2 步认得多种标记，所以跨平台读文件时比 `split("\n")` 稳
- 第 5 步决定 `"a\n"` 得到 `['a']` 而不是 `['a', '']`；但**中间**的空行会保留成空字符串
- 因为第 3 步切掉了换行符，拼回去要用 `"\n".join(lines)`
- 它只处理文本，二进制数据要先解码

## 注意事项

- 处理文件内容优先用它，不要 `split("\n")`（会留下 `\r`）。
- 中间空行会保留，判空时注意 `if line.strip()`。
- 要保留原换行用 `keepends=True`。
- 逐行处理大文件还是用 `for line in f`，别先读成一个大字符串。

## 使用场景

- 解析多行文本（配置、日志片段）。
- 把从网页/剪贴板拿到的一大段文字按行处理的。
- 统计行数（`len(text.splitlines())`）。
