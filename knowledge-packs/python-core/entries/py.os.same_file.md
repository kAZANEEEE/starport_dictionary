---
id: py.os.same_file
title: 判断两个路径是不是同一个文件
description: 硬链接、软链接、相对路径写法不同，其实指向同一个文件
language: python
category_id: programming.filesystem
module: os
origin: stdlib
import: "import os"
qualname: "os.path.samefile()"
signature: "os.path.samefile(path1, path2)"
args:
  - name: "path1, path2"
    required: true
    accepts: "两个路径；**都必须存在**，否则抛 FileNotFoundError"
    nesting: "可以"
returns: "True/False：底层是不是同一个文件（比较的是文件标识，不是路径字符串）"
object:
  id: file.path
  name: 文件路径
  aliases: [路径, 同一个文件, 硬链接, 软链接, path]
action:
  id: compare.diff
  name: 比较
  aliases: [比较, 判断相同, 是否同一个, 对比, samefile]
targets: []
utterances:
  direct:
    - 判断两个路径是不是同一个文件
    - 比较两个路径是否相同
    - 软链接指向的是不是同一个
  questions:
    - 怎么判断两个路径指向同一个文件
    - 路径字符串比较为什么不够
    - samefile 和 == 有什么区别
  colloquial:
    - 这两个路径看着不一样，是不是同一个文件
    - 软链接和原来的文件算同一个吗
  technical:
    - os.path.samefile
    - inode
    - 硬链接
    - 路径规范化
  short_queries:
    - 同一文件
    - samefile
    - 路径比较
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "os.path.samefile 是 3.2 起跨平台可用；3.4 起 samefile 支持 Path"
sources:
  - Python 官方文档 os.path.samefile
---

# 判断两个路径是不是同一个文件

## 功能描述

输入两个路径，输出它们是否指向**磁盘上同一个文件**；比较的是文件身份，不是路径文字。

## 推荐代码

```python
import os
from pathlib import Path

Path("data").mkdir(exist_ok=True)
Path("data/a.txt").write_text("x", encoding="utf-8")

print("data/a.txt" == "./data/a.txt")                  # False 纯字符串比较
print(os.path.samefile("data/a.txt", "./data/a.txt"))  # True 同一个文件
print(Path("data/a.txt").samefile("./data/a.txt"))     # True 也能这么写
```

## 语句解释

### os.path.samefile(a, b)

看底层文件标识是否相同。能识别 `./`、`..`、软链接、硬链接。

### 和字符串 == 的区别

字符串比较只看文字；路径写法不同就算不相等。

### 两个路径都必须存在

不存在会抛 `FileNotFoundError`，用之前先判断存在。

## 原理解释

**一句话：** 它去问文件系统「这两个路径记录的是不是同一份数据」，而不是比字符串。

**执行逻辑：**

1. 对第一个路径取文件标识（设备号 + inode 号，相当于文件的身份证）
2. 对第二个路径做同样的事
3. 比较两个标识是否相同
4. 相同 → True；不同 → False

**机器层（可跳过）：** 两次 `stat` 查询，不读文件内容，很快。

**边界（从逻辑推出来）：**

- 第 1、2 步要能取到标识，所以**路径必须存在**
- 因为它比的是「身份证」而不是路径，所以软链接、硬链接、`../` 写法都能正确识别
- 反过来：字符串 `==` 只看写法，`"a.txt"` 和 `"./a.txt"` 会被判为不同
- 跨磁盘的两个文件设备号不同，永远 False

## 注意事项

- 路径不存在会抛异常，先 `exists()` 或包 try。
- 判断「路径写法是否等价」用 `Path(...).resolve()` 比较；判断「是不是同一份数据」用 `samefile`。
- 只比文件名不比路径的写法是错的，容易误判同名文件。
- Windows 上不区分大小写，`A.txt` 和 `a.txt` 会判为同一个。

## 使用场景

- 上传文件去重（是不是已经存过同一个文件）。
- 判断软链接指向的是不是已经在处理的文件。
- 校验备份是否真的复制到了同一个源。
