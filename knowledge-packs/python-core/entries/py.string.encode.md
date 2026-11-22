---
id: py.string.encode
title: 字符串与字节互转
description: 编码成 bytes 或解码回字符串
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.encode() / bytes.decode()"
signature: "s.encode(encoding=\"utf-8\")；b.decode(encoding)"
args:
  - name: "encoding"
    required: false
    default: "\"utf-8\""
    accepts: "编码名，如 \"utf-8\"、\"gbk\"；解码时必须和编码时一致"
    nesting: "一般直接写字面量"
  - name: "errors"
    required: false
    default: "\"strict\""
    accepts: "\"strict\" 报错、\"replace\" 换成替代符、\"ignore\" 丢弃"
    nesting: "一般直接写字面量"
returns: "bytes（编码后）或 str（解码后）；编码不匹配会抛 UnicodeDecodeError"

object:
  id: string.text
  name: 字符串
  aliases: [文本, 字节, 编码, 二进制数据, string]

action:
  id: convert.transform
  name: 转换
  aliases: [编码, 解码, 转成字节, 变成文本, encode, decode]

targets: []

utterances:
  direct:
    - 字符串转字节
    - 字节转字符串
    - 编码解码
  questions:
    - 怎么把字符串变成 bytes
    - 如何把 bytes 解码成中文
    - encoding 写错会怎样
  colloquial:
    - 网络传回来的是一堆 b'...'，怎么变中文
    - 写文件要字节，字符串怎么转
  technical:
    - str.encode
    - bytes.decode
    - UnicodeDecodeError
    - utf-8 gbk
  short_queries:
    - 编码
    - 解码
    - bytes

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "encode/decode 各版本一致；错误处理参数 errors= 也通用"
sources:
  - Python 官方文档 str.encode
  - Python 官方文档 bytes.decode
---

# 字符串与字节互转

## 功能描述

输入字符串 + 编码名，输出 `bytes`；反过来 `bytes.decode(编码)` 得到字符串。编码不匹配会抛 `UnicodeDecodeError`。

## 推荐代码

```python
s = "中文"

b = s.encode("utf-8")
print(b)                 # b'\xe4\xb8\xad\xe6\x96\x87'
print(len(b))            # 6 —— 6 个字节
print(len(s))            # 2 —— 2 个字符

print(b.decode("utf-8")) # 中文

# 编码猜错会直接报错——这是最常见的乱码来源
try:
    b.decode("gbk")
except UnicodeDecodeError as exc:
    print("编码不对:", type(exc).__name__)
```

## 语句解释

### str.encode(编码)

把字符按编码规则变成字节序列。**默认是 utf-8**。

### bytes.decode(编码)

把字节按同样规则解释回字符。**必须用写的时候那个编码**。

### errors="replace" / "ignore"

容错参数：`replace` 把坏字节换成替代符，`ignore` 直接丢弃。

## 原理解释

**一句话：** 字符串是「字符编号」，字节是「存储/传输的原始数据」，编码就是两者之间的翻译规则。

**执行逻辑：**

1. 编码：从字符串里取一个字符，查它在指定编码里的编号
2. 把这个编号按规则写成 1~4 个字节，接到结果里
3. 所有字符处理完，得到 `bytes`
4. 解码：反过来——读字节，按规则还原编号，再查成字符
5. 遇到不符合规则的字节序列 → 抛 `UnicodeDecodeError`

**机器层（可跳过）：** 一个中文在 UTF-8 里占 3 字节，在 GBK 里占 2 字节——所以长度会变。

**边界（从逻辑推出来）：**

- 第 2 步说明编码不同、字节数不同：同一个中文 UTF-8 3 字节、GBK 2 字节
- 第 5 步是「解码必须有正确的编码」的原因：规则不对就还原不出字符
- 因为 `bytes` 不是字符串，`b"中文"` 直接写会报错，必须带编码
- `len()` 对 `str` 是字符数、对 `bytes` 是字节数，混着用会算错

## 注意事项

- 存/传之前统一用 UTF-8，别混 GBK。
- 解码失败通常是「编码写错」或「数据被截断」，别一上来就 `errors="ignore"`（会静默丢数据）。
- `b"..."` 里只能放 ASCII，中文要 `"中文".encode()`。
- 处理外部文件时，编码是文件属性之一，别假设。

## 使用场景

- 网络收发：socket 只认 bytes。
- 读写二进制文件、加密/哈希前的数据处理。
- 处理他人给的 GBK 老文件（先解码再编码成 UTF-8）。
