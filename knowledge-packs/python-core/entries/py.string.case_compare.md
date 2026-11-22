---
id: py.string.case_compare
title: 忽略大小写比较
description: 用户输入 PyThOn 和 python 应该算一样
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.casefold() 后比较"
signature: "a.casefold() == b.casefold()"
args:
  - name: "a, b"
    required: true
    accepts: "两个字符串；比较前都先转成统一形式"
    nesting: "可以，可以是用户输入"
returns: "True/False：忽略大小写后是否相等；casefold 比 lower 更彻底（德语 ß 也能对上 ss）"
object:
  id: string.text
  name: 字符串
  aliases: [文本, 比较, 大小写, 用户输入, string]
action:
  id: compare.diff
  name: 比较
  aliases: [比较, 判断相等, 对比, 是否相同, compare]
targets: []
utterances:
  direct:
    - 忽略大小写比较字符串
    - 不区分大小写判断相等
    - 用户输入大小写不一样也算相同
  questions:
    - 怎么忽略大小写比较两个字符串
    - lower 和 casefold 有什么区别
    - 用户名比较要不要管大小写
  colloquial:
    - 用户输入 PyThOn，想当成 python
    - 校验验证码时不想管大小写
  technical:
    - casefold
    - lower 比较
    - 不区分大小写
    - 用户名规范化
  short_queries:
    - 忽略大小写
    - casefold
    - 不区分大小写
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.3"
version_note: "casefold 从 3.3 起；lower 更老但不够彻底"
sources:
  - Python 官方文档 str.casefold
---

# 忽略大小写比较

## 功能描述

输入两个字符串，先把它们都转成「统一的小写形式」，再比是否相等；`casefold()` 比 `lower()` 更彻底。

## 推荐代码

```python
a = "PyThOn"
b = "python"

print(a == b)                     # False
print(a.lower() == b.lower())     # True
print(a.casefold() == b.casefold())   # True

# 德语 ß：lower 处理不彻底，casefold 能对上 "ss"
print("STRASSE".casefold() == "straße".casefold())   # True
```

## 语句解释

### .lower()

转小写。大多数场景够用。

### .casefold()

更彻底的大小写折叠，能处理 ß、İ 这类特殊字符。**做「不区分大小写比较」应该用它**。

### 两边都要转

只转一边没意义——`a.lower() == b` 还是会失败。

## 原理解释

**一句话：** 它把两边都折成「同一套标准写法」，然后普通比较字符串。

**执行逻辑：**

1. 对第一个字符串逐个字符做大小写折叠
2. 对第二个字符串同样处理
3. 用 `==` 比较这两条折叠后的结果
4. 完全一致就 True，否则 False

**机器层（可跳过）：** 两次字符串转换 + 一次比较，O(n)。

**边界（从逻辑推出来）：**

- 第 1、2 步都要做，只折一边等于没折
- 折叠可能**改变长度**（ß → ss），所以折叠后的长度不一定等于原长
- 它只解决「比较」，不解决「存储」——要保原样就别覆盖原变量
- 中文没有大小写，折叠后原样不变

## 注意事项

- 两边都要转，别只转一边。
- 存储用户名这类场景，建议**入库时就统一存小写**，查的时候也用小写。
- 只是显示用的文本不要折叠，会改掉用户原本的大小写。
- 想做「模糊相等」还要 `strip()` 去空白。

## 使用场景

- 校验验证码、命令、邮箱。
- 用户名/标签去重（大小写不同算同一个）。
- 做「是否相同」的断言时统一大小写。
