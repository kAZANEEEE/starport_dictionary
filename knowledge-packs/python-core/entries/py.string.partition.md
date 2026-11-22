---
id: py.string.partition
title: 按分隔符切成三段
description: 只要前后两半和中间那个分隔符，不用猜切了几段
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.partition()"
signature: "s.partition(分隔符) / s.rpartition(分隔符)"
args:
  - name: "分隔符"
    required: true
    accepts: "一个字符串；只切第一刀（rpartition 切最后一刀）"
    nesting: "可以，可以是变量"
returns: "三元组 (前, 分隔符, 后)；找不到分隔符时返回 (原文, \"\", \"\")"
object:
  id: string.text
  name: 字符串
  aliases: [文本, 分割, 切三段, 分隔符, string]
action:
  id: convert.transform
  name: 转换
  aliases: [切三段, 分割, 拆开, partition]
targets: []
utterances:
  direct:
    - 按分隔符切成三段
    - partition 怎么用
    - 字符串切成前后两半
  questions:
    - 怎么只按第一个分隔符切
    - partition 和 split 有什么区别
    - 取 = 前后两边的值怎么写
  colloquial:
    - 想拿等号前面的名字和后面的值
    - 只切一刀就够了，不用切成数组
  technical:
    - str.partition
    - rpartition
    - 三元组解包
  short_queries:
    - 切三段
    - partition
    - 分割
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "partition / rpartition 各版本一致"
sources:
  - Python 官方文档 str.partition
---

# 按分隔符切成三段

## 功能描述

输入分隔符，输出**固定三个**元素：分隔符左边、分隔符本身、分隔符右边。

## 推荐代码

```python
line = "name = starport"

print(line.partition("="))      # ('name ', ' = ', ' starport')
print(line.partition("=")[0])   # 'name '
print(line.partition("=")[2])   # ' starport'

key, sep, value = line.partition("=")
print(key.strip(), "→", value.strip())

print("没有等号".partition("="))   # ('没有等号', '', '')
```

## 语句解释

### partition(分隔符)

**只切第一个**分隔符，返回固定 3 个元素的元组。

### `key, sep, value = ...` 解包

固定三元素，所以永远能三个变量接住——**不用判断切出来几段**。

### 找不到分隔符

返回 `(整串, "", "")`，`sep` 是空字符串，可以据此判断「有没有切到」。

## 原理解释

**一句话：** 它找到第一个分隔符，把左右两边和分隔符本身一起交给你。

**执行逻辑：**

1. 从字符串开头找分隔符
2. 找到 → 把前面的部分、分隔符、后面的部分装成三元组返回
3. 找不到 → 整串当前段，后两段是空字符串
4. 后面的内容里即使还有分隔符，也不再处理

**机器层（可跳过）：** 一次查找 + 三次切片，不创建中间列表。

**边界（从逻辑推出来）：**

- 第 1 步只找第一个，所以 `a=b=c` 会得到 `("a", "=", "b=c")`——剩下的不切
- 第 3 步用空字符串表示「没找到」，所以结果永远是 3 个元素，解包不会失败
- 因为固定三段，它比 `split` 更适合「key=value」这种一定有一刀的场景
- 分隔符本身也返回，所以你能看出到底切到了没有

## 注意事项

- 想要全切用 `split`；只要一刀用 `partition`。
- 找不到时 `sep == ""`，可以用它判断。
- 前后两段通常还带空格，记得 `strip()`。
- 想从右边切（取扩展名、路径最后一段）用 `rpartition`。

## 使用场景

- 解析 `key=value` 形式的配置行。
- 拆 URL 的协议部分（`"http://x".partition("://")`）。
- 取文件名和扩展名（`"a.b.py".rpartition(".")`）。
