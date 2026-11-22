---
id: py.string.zfill
title: 数字补零对齐
description: 把 7 变成 007，编号、日期、文件名常用
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.zfill()"

object:
  id: string.text
  name: 字符串
  aliases: [文本, 数字, 编号, 补零, string]

action:
  id: convert.transform
  name: 转换
  aliases: [补零, 对齐, 格式化, 变成定长, zfill, rjust]

targets: []

utterances:
  direct:
    - 数字补零
    - 把 7 变成 007
    - 字符串按长度补零
  questions:
    - 怎么给数字补前导零
    - 如何生成 001 002 这种编号
    - zfill 和 rjust 有什么区别
  colloquial:
    - 文件名想按顺序排，得补零
    - 排序乱了，因为 10 排在 2 前面
  technical:
    - str.zfill
    - str.rjust
    - "f-string :03d"
    - 排序补零
  short_queries:
    - 补零
    - zfill
    - 对齐

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "str.zfill 各版本一致；f-string 的 :03d 需要 3.6+"
sources:
  - Python 官方文档 str.zfill
---

# 数字补零对齐

## 功能描述

输入字符串 + 目标长度，输出左边补 0 到该长度的新字符串；已够长就原样返回。

## 推荐代码

```python
for i in range(1, 4):
    print(str(i).zfill(3))     # 001 002 003

print("7".rjust(3, "0"))       # 007，和 zfill 等价
print(f"{7:03d}")              # 007，数字直接格式化更好

print("-5".zfill(3))           # -05  ← 负号会被特殊处理
print("abc".zfill(5))          # 00abc
```

## 语句解释

### .zfill(宽度)

左边补 `0` 到指定宽度。它只接受一个参数（宽度），补的字符固定是 0。

### .rjust(宽度, 填充符)

左边补任意字符，和 `zfill` 类似的用途，但能换填充符。

### f"{7:03d}"

数字的格式化写法：`03` 表示总宽度 3、不足补 0。**处理数字优先用这个**，不用先转字符串。

## 原理解释

**一句话：** 它数一下现在多长，不够就在左边垫 0，垫到你要的宽度为止。

**执行逻辑：**

1. 量一下当前字符串长度
2. 长度 ≥ 目标 → 原样返回（不截断）
3. 长度不够 → 算出差多少
4. 在左边补上这么多个 `0`
5. 返回新字符串

**机器层（可跳过）：** 造一个新字符串，长度等于目标宽度。

**边界（从逻辑推出来）：**

- 第 2 步不截断，所以 `"12345".zfill(3)` 还是 `"12345"`
- 第 4 步补的是字符 0，所以对已有前导负号的情况它会把 0 插在负号**后面**（`-5` → `-05`），这和其他语言的补零行为不同
- 因为它按**字符**算宽度，中文等多字节字符算 1 位
- 数字用 `:03d` 更直接：省掉转字符串，且宽度语义更明确

## 注意事项

- 补零是为了**字符串排序**好看，不是数值需要。
- 负数会变成 `-05`，如果你要 `005` 得自己处理符号。
- 数字优先 `f"{n:03d}"`，字符串才用 `zfill`。
- 只补左边，右边对齐用 `ljust`。

## 使用场景

- 生成 `img_001.jpg` 这种有序文件名。
- 日期/时间拼接（`2026-01-05`）。
- 固定宽度的编号输出。
