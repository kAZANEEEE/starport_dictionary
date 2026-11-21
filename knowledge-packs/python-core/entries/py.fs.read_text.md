---
id: py.fs.read_text
title: 读取文本文件
description: 把一个文本文件的内容读成字符串
language: python
category_id: programming.filesystem
module: pathlib

object:
  id: file.content
  name: 文件内容
  aliases: [内容, 文件数据, 文本内容, 读文件, file content]

action:
  id: get.obtain
  name: 获取
  aliases: [读取, 取, 拿到, 读出, read, get]

targets: []

utterances:
  direct:
    - 读取文本文件
    - 读文件内容
    - 把文件读成字符串
  questions:
    - 怎么读取一个文本文件
    - 如何读文件内容到变量里
    - Python 怎么打开文件读内容
  colloquial:
    - 想把 txt 里的字读出来
    - 文件里的内容怎么弄到程序里
  short_queries:
    - 读文件
    - 读取
    - read_text

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.5"
version_note: read_text 从 3.5 起有；encoding 参数后来才强调，3.10 起文档都建议显式写
sources:
  - Python 官方文档 pathlib.Path.read_text
---

# 读取文本文件

## 功能描述

把整个文本文件一次读成字符串。

## 推荐代码

```python
from pathlib import Path

# 演示用：先造一个文件，实际使用时这两行删掉
Path("sample.txt").write_text("你好，文件\n第二行\n", encoding="utf-8")

text = Path("sample.txt").read_text(encoding="utf-8")
print(text)
print("行数:", len(text.splitlines()))
```

## 语句解释

### Path(...).write_text(...)

演示造文件用的。第一行只是为了让这段代码自己就能跑，实际项目里删掉。

### .read_text(encoding="utf-8")

一次读完整个文件并解码成字符串。**encoding 一定要写**，不写就用系统默认编码，Windows 上常是 GBK，中文会乱码或报错。

### .splitlines()

按行切开，返回列表。比 `text.split("\n")` 稳，因为能处理 `\r\n`。

## 原理解释

**一句话：** 打开文件、一次性把里面所有字读出来、再关上，交给你一个字符串。

**执行逻辑：**

1. 按给定路径打开文件，拿到一个「文件句柄」（相当于系统给你的取件凭证）
2. 从凭证里把**全部字节**读出来（一次读完，不分块）
3. 按 `encoding` 指定的规则把字节翻译成文字
4. 自动关闭句柄（`with` 帮你做这一步）
5. 返回这一整段文字

**机器层（可跳过）：** 底层是 open → read 两三次系统调用，数据从磁盘进内存。

**边界（从逻辑推出来）：**

- 第 2 步是「一次读完」，所以**文件多大就占多大内存**——几百 MB 的日志不能这么读
- 第 3 步靠 `encoding` 翻译，规则不对就会乱码或直接抛 `UnicodeDecodeError`（Windows 默认是 GBK，中文最容易在这里坏）
- 第 1 步找不到文件直接抛 `FileNotFoundError`，所以「读之前先判断存在」是为了给更友好的提示，不是为了它
- 返回的是字符串，二进制文件（图片、exe）不能用它读
## 注意事项

- **文件很大时不要用 `read_text`**，会整个读进内存；逐行处理请用 `open()` 加 `for line in f`。
- 不写 `encoding` 是新手最常见的乱码原因。
- 文件不存在直接抛 `FileNotFoundError`，先判断用 `Path(p).exists()`。
- 读到的是字符串，要处理二进制（图片、exe）请用 `read_bytes()`。

## 使用场景

- 读配置、读 Markdown、读日志。
- 小文件的批量文本处理。
- 需要整段正则匹配时，一次读进来更方便。
