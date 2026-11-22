---
id: py.string.isdigit
title: 判断字符串是不是数字
description: 用户输入能不能直接转成整数
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.isdigit() / str.isnumeric() / str.isdecimal()"
signature: "s.isdigit()  s.isdecimal()  s.isnumeric()"
args:
  - name: "s"
    required: true
    accepts: "要检查的字符串（不能是数字类型）"
    nesting: "可以，常配合 s.strip() 先去空白"
returns: "True/False：全是数字字符才为真；空字符串、带负号、带小数点都是 False"
object:
  id: string.text
  name: 字符串
  aliases: [文本, 用户输入, 数字判断, 是不是数字, string]
action:
  id: inspect.check
  name: 判断
  aliases: [判断, 检查, 验证, 是不是, isdigit]
targets: []
utterances:
  direct:
    - 判断字符串是不是数字
    - 检查输入是不是整数
    - 验证是不是纯数字
  questions:
    - 怎么判断用户输入的是不是数字
    - isdigit 和 isnumeric 有什么区别
    - 负数和 3.14 为什么判断失败
  colloquial:
    - 用户输入的数字能不能直接 int()
    - 想拦住「abc」这种输入
  technical:
    - str.isdigit
    - str.isnumeric
    - 负数小数
    - 转换异常
  short_queries:
    - 是不是数字
    - isdigit
    - 纯数字
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "isdigit / isnumeric / isdecimal 各版本一致；三者对特殊数字字符判断不同"
sources:
  - Python 官方文档 str.isdigit
---

# 判断字符串是不是数字

## 功能描述

输入字符串，输出它是否**全部由数字字符组成**；负号、小数点、空格都会让它判为 False。

## 推荐代码

```python
print("123".isdigit())      # True
print("12.5".isdigit())     # False ← 有小数点
print("-1".isdigit())       # False ← 有负号
print("".isdigit())         # False ← 空字符串
print(" 12".strip().isdigit())  # True ← 先去空白

# 真正想「能不能转成数字」用 try 更稳
def to_number(s: str):
    try:
        return int(s)
    except ValueError:
        return None

print(to_number("-1"), to_number("3.5"))
```

## 语句解释

### isdigit()

所有字符都是数字才 True。它判断的是**字符类别**，不是数值合法性。

### isnumeric() / isdecimal()

比 isdigit 更宽/更窄：`isnumeric` 认得罗马数字、汉字数字这类；`isdecimal` 只认十进制数字。

### 为什么不直接用 isdigit 校验输入

因为 `-1`、`3.5`、`1_000`（下划线）都是合法数字但 `isdigit()` 判 False。

## 原理解释

**一句话：** 它逐个字符看「这个字符属不属于数字类别」，全属于才回答 True。

**执行逻辑：**

1. 从第一个字符开始
2. 检查它在 Unicode 里是不是被归为数字
3. 不是 → 立刻返回 False
4. 是 → 看下一个
5. 全部看完都合格 → True（**空字符串除外，直接 False**）

**机器层（可跳过）：** 一趟线性扫描，看的是 Unicode 类别表。

**边界（从逻辑推出来）：**

- 第 2 步看的是「字符类别」，所以负号 `-`、小数点 `.` 不是数字字符，直接 False
- 第 5 步空字符串返回 False（因为没有字符能通过检查），这点常被忽略
- 因为第 3 步立刻返回，所以 `"12a"` 在第二个字符就失败
- 它**不检查数值范围**，`"999999999999999999999"` 是 True，但转 int 没问题、转 int8 就越界

## 注意事项

- 负号、小数点、空格都会判 False，别拿它校验真实数字输入。
- 校验「能不能转成数字」用 `try: int(s) / float(s)` 更可靠。
- 空字符串是 False，判空前先 `strip()`。
- 中文数字（"一二三"）用 `isnumeric()` 可能为 True，但 `int()` 转不了。

## 使用场景

- 快速排除明显不是数字的输入（先粗筛）。
- 校验「纯数字编号」、「手机号」这类只含数字的字段。
- 数据清洗前做一次粗判断。
