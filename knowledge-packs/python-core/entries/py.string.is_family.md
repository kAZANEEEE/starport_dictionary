---
id: py.string.is_family
title: 字符类型判断族
description: isalpha / isspace / isalnum 各管什么
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.isalpha() / isspace() / isalnum() / isupper()"
signature: "s.isalpha()  s.isdigit()  s.isalnum()  s.isspace()  s.isupper()  s.islower()"
args:
  - name: "s"
    required: true
    accepts: "要检查的字符串（不能是数字类型）"
    nesting: "可以，常配合 strip() 先去空白"
returns: "True/False：**全部字符**都符合该类别才为真；空字符串一律 False"
object:
  id: string.text
  name: 字符串
  aliases: [文本, 字符类型, 判断, 是不是字母, string]
action:
  id: inspect.check
  name: 判断
  aliases: [判断, 检查, 验证, 是不是, isalpha]
targets: []
utterances:
  direct:
    - 判断是不是字母
    - 判断是不是空白
    - 字符类型判断
  questions:
    - isalpha 和 isalnum 有什么区别
    - 怎么判断全是空格
    - 为什么空字符串返回 False
  colloquial:
    - 想检查输入里有没有非法字符
    - 这串是不是纯字母
  technical:
    - isalpha
    - isalnum
    - isspace
    - isupper
  short_queries:
    - 字符判断
    - isalpha
    - 判断类型
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "这些判断方法各版本一致；对中文 isalpha 也算 True"
sources:
  - Python 官方文档 str.isalpha
---

# 字符类型判断族

## 功能描述

输入字符串，输出它是否**全部由某类字符组成**；有一个不合格就 False，空字符串也 False。

## 推荐代码

```python
print("abc".isalpha())      # True
print("abc1".isalpha())     # False（有数字）
print("abc1".isalnum())     # True（字母或数字都行）
print("   ".isspace())      # True
print("ABC".isupper())      # True
print("".isalpha())         # False ← 空字符串没有字符，不算
print("中文".isalpha())     # True ← 中文也算字母类
```

## 语句解释

### isalpha()

全是字母（含中文）。有数字、空格、标点就 False。

### isalnum()

全是字母或数字。常用来校验「用户名只允许字母数字」。

### isspace()

全是空白字符（空格、`\t`、`\n`）。

### isupper() / islower()

全是大写 / 全是小写。混着就 False。

## 原理解释

**一句话：** 它逐个字符查「属于这个类别吗」，有一个不属于立刻返回 False。

**执行逻辑：**

1. 从第一个字符开始
2. 检查它属不属于目标类别
3. 不属于 → 立刻 False
4. 属于 → 看下一个
5. 全部通过 → True；**一个字符都没有 → False**

**机器层（可跳过）：** 一趟扫描，查 Unicode 类别表。

**边界（从逻辑推出来）：**

- 第 3 步立刻返回，所以只要有一个非法字符就 False
- 第 5 步空字符串返回 False（"全部字符都合格"在没有字符时视为不成立）
- 它判断的是**字符类别**不是语义，所以 `"中文".isalpha()` 是 True
- `isalnum()` 不管顺序，只要求每个字符都是字母或数字

## 注意事项

- 空字符串一律 False，判空前先 `strip()`。
- 中文会被 `isalpha()` 判为 True，做英文校验要额外限制 ASCII。
- 这些是「全字符」判断，不是「包含」判断；要判断包含用正则。
- 别靠它们校验数字格式（负号、小数点都不算）。

## 使用场景

- 校验用户名（只允许字母数字）。
- 清洗数据前粗筛。
- 判断一行是不是空行（`line.isspace()`）。
