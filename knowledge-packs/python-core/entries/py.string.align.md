---
id: py.string.align
title: 字符串对齐（补空格）
description: 让输出排成整齐的列
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.ljust() / str.rjust() / str.center()"
signature: 's.ljust(宽度, 填充=" ")  s.rjust(...)  s.center(...)'
args:
  - name: "宽度"
    required: true
    accepts: "目标总宽度（字符数）；已经够长就原样返回"
    nesting: "一般直接写数字"
  - name: "填充"
    required: false
    default: '" "（空格）'
    accepts: "用来补齐的字符，通常是空格或 -"
    nesting: "一般直接写字面量"
returns: "字符串：补齐后的新字符串；原字符串不变"
object:
  id: string.text
  name: 字符串
  aliases: [文本, 对齐, 空格, 列宽, string]
action:
  id: create.new
  name: 创建
  aliases: [对齐, 补空格, 补齐, 格式化, ljust]
targets: []
utterances:
  direct:
    - 字符串对齐
    - 补空格对齐
    - 让输出排整齐
  questions:
    - 怎么让输出的列对齐
    - ljust 和 rjust 怎么用
    - 数字右对齐怎么写
  colloquial:
    - 打印出来参差不齐，想对齐
    - 表格里的名字想左对齐、数字右对齐
  technical:
    - str.ljust
    - str.rjust
    - str.center
    - 对齐填充
  short_queries:
    - 对齐
    - ljust
    - 补空格
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "ljust / rjust / center 各版本一致"
sources:
  - Python 官方文档 str.ljust
---

# 字符串对齐（补空格）

## 功能描述

输入字符串 + 目标宽度，输出补齐到该宽度的新字符串；够长就原样返回，不截断。

## 推荐代码

```python
rows = [("张三", 90), ("李四四", 8), ("王五", 100)]

for name, score in rows:
    print(name.ljust(8) + str(score).rjust(5))

print("居中".center(12, "-"))   # -----居中-----
```

## 语句解释

### ljust(宽度)

左对齐：文字在左，右边补空格。

### rjust(宽度)

右对齐：数字常用，能对齐个位/十位/百位。

### center(宽度, 字符)

居中，两侧补指定字符。

## 原理解释

**一句话：** 它先量当前长度，不够就在指定那一侧补字符，补到目标宽度。

**执行逻辑：**

1. 量一下现在的字符数
2. 够长 → 原样返回
3. 不够 → 算出差多少
4. 按方向补到左边 / 右边 / 两边
5. 返回新字符串

**机器层（可跳过）：** 造一个新字符串，长度 = 目标宽度。

**边界（从逻辑推出来）：**

- 第 2 步不截断，所以超宽的内容会把整列撑开
- 第 1 步量的是**字符数**，中文算 1 个字符但显示占 2 个格子——**终端里还是对不齐**
- 因为返回新字符串，原字符串不变
- 数字要先 `str()` 才能对齐，或者直接用 f-string 的格式说明

## 注意事项

- 中文/emoji 会让「字符数对齐」在终端里看起来仍不齐，需要按显示宽度算（第三方 `wcwidth`）。
- 数字对齐更好用的写法：`f"{score:>5}"`。
- 超宽不截断，注意列宽要留够。
- 表格输出建议直接用 `\t` 或专门的库，别手工对齐。

## 使用场景

- 命令行打印对表格。
- 生成固定宽度的文本报告。
- 日志里对齐字段。
