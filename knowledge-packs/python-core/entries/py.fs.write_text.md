---
id: py.fs.write_text
title: 写入文本文件
description: 把一段字符串写进文件，覆盖或追加
language: python
category_id: programming.filesystem
module: pathlib

object:
  id: file.content
  name: 文件内容
  aliases: [内容, 文件数据, 文本文件, 写文件, file content]

action:
  id: create.new
  name: 创建
  aliases: [写, 写入, 保存, 生成, 输出, write, save, create]

targets: []

utterances:
  direct:
    - 写入文本文件
    - 把字符串写到文件里
    - 保存文本到文件
    - 生成一个文本文件
  questions:
    - 怎么把内容写进文件
    - 如何用 Python 写文件
    - 怎么往文件里追加内容
    - Python 怎么写文件不会覆盖
  colloquial:
    - 想把结果存成一个 txt
    - 这个字符串得写出去，怎么办
    - 跑完的结果我想留到文件里
  goal_based:
    - 记录日志到文件
    - 把处理结果导出成文本
  technical:
    - pathlib write_text
    - open mode w
    - open mode a
    - python write file utf-8
  short_queries:
    - 写文件
    - 保存
    - write_text
    - 追加

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.5"
version_note: write_text 从 3.5 起有；3.10 起文档强调显式写 encoding
sources:
  - Python 官方文档 pathlib.Path.write_text
  - Python 官方文档 open 的模式参数
---

# 写入文本文件

## 功能描述

把字符串写进文件。默认**整体覆盖**，想追加要用 `open(..., "a")`。

## 推荐代码

```python
from pathlib import Path

# 覆盖写：文件不存在会新建，存在就把内容清空重写
Path("out.txt").write_text("第一行\n第二行\n", encoding="utf-8")

# 追加写：老内容保留，新内容加在末尾
with open("out.txt", "a", encoding="utf-8") as f:
    f.write("第三行\n")

print(Path("out.txt").read_text(encoding="utf-8"))
```

## 语句解释

### write_text(text, encoding)

一次写完，自动打开、写、关闭。**默认是覆盖**，不是追加——这是新手最容易误判的一点。

### open(path, "a", encoding)

`"a"` 是 append：
- `"w"` 覆盖，文件不存在就新建
- `"a"` 追加，文件不存在也新建
- `"x"` 只在文件不存在时创建，已存在直接报错

### with 语句

`with` 保证退出时关闭文件。不写 `with` 就得手动 `f.close()`，中间一旦抛异常，文件句柄会漏。

## 原理解释

**一句话：** 把一段文字写进文件，默认是「先清空、再写入」。

**执行逻辑：**

1. 打开文件；**如果文件已存在，先把长度截成 0**（这一步就是「覆盖」的真相）
2. 把字符串按 `encoding` 翻成字节
3. 把字节写进文件
4. 关闭文件（关闭时才真正落盘）
5. 返回写入的字符数（一般不用管）

**机器层（可跳过）：** open(截断) → write → close，close 触发缓冲区刷盘。

**边界（从逻辑推出来）：**

- 因为第 1 步先截断，**旧内容在你写第一个字节之前就已经没了**——写到一半出错，文件就是半截
- 想保留原内容必须用 `open(..., "a")`（追加），它不是「覆盖」的开关，而是另一条路径
- 编码不写就用系统默认，中文在 Windows 上会乱码
- 父目录不存在会在第 1 步就失败（`FileNotFoundError`），所以写之前要先 `mkdir`
## 注意事项

- **`"w"` 会清空原文件**。要保留原内容必须用 `"a"`。
- 一定要写 `encoding="utf-8"`，否则中文在 Windows 上可能乱码或直接报 `UnicodeEncodeError`。
- 目录不存在会抛 `FileNotFoundError`，要先 `Path(dir).mkdir(parents=True, exist_ok=True)`。
- 大量小段内容不要反复 `write_text` 覆盖，改成一次 `"a"` 追加或先拼好再写。
- 写完立刻读同一文件时，`with` 块要结束（关闭）之后再去读，别在块里读。

## 使用场景

- 把程序结果导出成 txt、csv、md。
- 记录运行日志（追加模式）。
- 生成配置文件、报告、脚本。
