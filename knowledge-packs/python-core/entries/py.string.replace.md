---
id: py.string.replace
title: 字符串替换
description: 把字符串里的一段换成另一段
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.replace()"
signature: "s.replace(old, new, count=-1)"
args:
  - name: "old"
    required: true
    accepts: "要被换掉的那段文字"
    nesting: "可以，可以是变量"
  - name: "new"
    required: true
    accepts: "换成什么"
    nesting: "可以"
  - name: "count"
    required: false
    default: "-1"
    accepts: "最多换几次；不传就是全换"
    nesting: "一般直接写数字"
returns: "字符串：换好的**新**字符串；原字符串不变，所以要重新赋值"

object:
  id: string.text
  name: 字符串
  aliases: [文本, 字串, 文字, 内容, string, text]

action:
  id: modify.change
  name: 修改
  aliases: [替换, 改成, 换成, 修改, 更新, replace]

targets: []

utterances:
  direct:
    - 字符串替换
    - 把文本里的某个词换掉
    - 替换字符串中的子串
  questions:
    - 怎么替换字符串里的内容
    - 如何把一段文字换成别的
    - Python 怎么批量替换文本
  colloquial:
    - 想把里面的“A”全换成“B”
    - 这段文字里有个词要改掉
  short_queries:
    - 替换
    - replace
    - str

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: str.replace 参数一直是 (old, new, count)，行为没变
sources:
  - Python 官方文档 str.replace
---

# 字符串替换

## 功能描述

把字符串里的某段文字换成另一段，可以限制替换几次。

## 推荐代码

```python
text = "小猫爱吃小鱼，小猫很可爱"

print(text.replace("小猫", "小狗"))          # 全换
print(text.replace("小猫", "小狗", 1))       # 只换第一个
print(text)                                  # 原字符串没变
```

## 语句解释

### .replace(old, new)

返回**新字符串**，原字符串不可变，所以不会改到原来的变量。

### 第三个参数（count）

最多替换几次。不传就是全换，传 0 就等于没换。

### print 里直接调用

`replace` 有返回值，不赋值也能用，但记得原变量没被改。

## 原理解释

**一句话：** 从左往右找，找到就换掉，最后给你一条**新的**字符串（原来那条不变）。

**执行逻辑：**

1. 从字符串开头开始扫
2. 找到第一个与 `old` 完全一致的位置
3. 把这一段换成 `new`，接着从替换后的位置继续往后扫
4. 重复 2–3，直到扫完（或者替换次数到 `count` 上限）
5. 把拼好的新字符串返回

**机器层（可跳过）：** 字符串不可变，所以每轮都在造新串，最后拼成一个。

**边界（从逻辑推出来）：**

- 因为返回新串、不改原串，**不重新赋值就等于没改**：必须 `s = s.replace(...)`
- 第 2 步要求完全一致，所以区分大小写：`"Py"` 换不掉 `"py"`
- 替换进去的内容**不会再被同一轮匹配**，所以不会无限循环
- 要一次换多个词，链式调用会重复扫描；词多时用 `re.sub` 一把替换更省
## 注意事项

- 想改到原变量必须重新赋值：`text = text.replace(...)`。
- 替换是**区分大小写**的，`"Py"` 换不掉 `"py"`。
- 多个不同词一起换，链式调用或 `str.translate` / 正则 `re.sub` 更合适。
- 大量替换用 `re.sub` 带正则更快也更灵活，但普通字面替换 `replace` 就够。

## 使用场景

- 清理文本里的乱码标记、占位符。
- 生成文件名时把不安全字符换掉。
- 模板字符串的简单填充（复杂模板用 `str.format` 或 f-string）。
