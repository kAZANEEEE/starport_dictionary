---
id: py.string.format
title: 格式化字符串
description: 把变量嵌进文本里（f-string / format / %）
language: python
category_id: programming.basics
module: str

object:
  id: string.text
  name: 字符串
  aliases: [文本, 模板, 字符串, 一句话, string]

action:
  id: create.new
  name: 创建
  aliases: [格式化, 拼接变量, 生成文本, 填充, format]

targets: []

utterances:
  direct:
    - 格式化字符串
    - 把变量放进字符串里
    - 字符串模板填充
  questions:
    - 怎么把变量拼进字符串
    - f-string 怎么用
    - 如何控制小数位数
  colloquial:
    - 想拼一句带变量的话
    - 数字只想要两位小数怎么弄
  technical:
    - f-string
    - str.format
    - 百分号占位
    - 格式化小数
  short_queries:
    - 格式化
    - f-string
    - 占位

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.6"
version_note: f-string 从 3.6 起；3.12 起支持嵌套引号与更复杂表达式
sources:
  - Python 官方文档 格式化字符串字面量
---

# 格式化字符串

## 功能描述

输入模板 + 变量，输出拼好的字符串。三种写法里 **f-string 优先**。

## 推荐代码

```python
name = "星港"
score = 91.567

print(f"{name} 的分数是 {score:.2f}")     # 星港 的分数是 91.57
print(f"{name} 长 {len(name)} 个字")

print("{} 的分数是 {:.2f}".format(name, score))
print("%s 的分数是 %.2f" % (name, score))   # 老写法，知道就行
```

## 语句解释

### f"{变量}"

f-string：字符串前加 `f`，大括号里放表达式，会直接求值。

### {score:.2f}

格式说明：`.2f` = 保留两位小数的浮点。`:.0%` 是百分比，`,` 是千分位。

### .format(...) / % 写法

老代码里还有，读得懂即可；新代码统一用 f-string。

## 原理解释

**一句话：** 先写一条带空位的句子，再把变量的值填进空位。

**执行逻辑：**

1. 扫描模板，找到第一个 `{}` 或 `{名字}`
2. 取出对应的值
3. 按冒号后面的格式规则把它变成文本（比如保留两位小数）
4. 用这段文本替换空位
5. 重复 1–4 直到没有空位
6. 返回拼好的字符串

**机器层（可跳过）：** f-string 在编译期就把「文字」和「表达式」拆开，运行时只做拼接。

**边界（从逻辑推出来）：**

- 第 3 步的格式规则决定小数位、千分位、百分比；不写就按默认字符串形式输出
- 因为空位是按顺序或按名字填的，`.format` 位置传错不会报错，只会填错——f-string 没这个问题
- 想输出真正的花括号要写两层 `{{}}`，否则会被当空位
- 拼 SQL 时值仍然要走参数化，格式化只解决「怎么拼成文本」，不解决安全
## 注意事项

- 大括号要转义：想输出字面量 `{}` 时写 `{{}}`。
- 引号别和外层冲突，3.12 起才允许嵌套同种引号；老版本用不同引号。
- 别用 `%` 拼 SQL（注入风险），也别用字符串拼 JSON。
- 需要千分位 `f"{n:,}"`，百分比 `f"{r:.1%}"`，这些比手写计算清楚。

## 使用场景

- 日志、提示信息。
- 报表输出对齐。
- 生成文件名、SQL 片段（值仍要用参数化）。
