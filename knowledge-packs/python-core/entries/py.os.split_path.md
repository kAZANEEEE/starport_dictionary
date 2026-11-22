---
id: py.os.split_path
title: 拆开路径
description: 从一条路径里分出目录和文件名，或取扩展名
language: python
category_id: programming.filesystem
module: os
origin: stdlib
import: "import os"
qualname: "os.path.split() / os.path.splitext()"
signature: "os.path.split(path) / os.path.splitext(path)"
args:
  - name: "path"
    required: true
    accepts: "一条路径字符串"
    nesting: "可以，常配合变量"
returns: "split 给 (目录, 文件名)；splitext 给 (去掉最后一个后缀的部分, 后缀)。都只看字符串，不查磁盘"
object:
  id: file.path
  name: 文件路径
  aliases: [路径, 目录, 文件名, 扩展名, path]
action:
  id: convert.transform
  name: 转换
  aliases: [拆开, 分割, 取文件名, 取目录, split]
targets: []
utterances:
  direct:
    - 拆开文件路径
    - 从路径里取文件名
    - 分离目录和文件名
  questions:
    - 怎么把路径拆成目录和文件名
    - 怎么只取扩展名不带点
    - split 和 splitext 有什么区别
  colloquial:
    - 给了个完整路径，想要文件名那一截
    - 想拿到不带后缀的文件名
  technical:
    - os.path.split
    - os.path.splitext
    - Path.stem
    - 路径拆分
  short_queries:
    - 拆路径
    - split
    - 取文件名
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "os.path.split / splitext 各版本一致"
sources:
  - Python 官方文档 os.path.split
  - Python 官方文档 os.path.splitext
---

# 拆开路径

## 功能描述

输入一条路径字符串，输出它的组成部分；**只做字符串切分，不检查文件是否存在**。

## 推荐代码

```python
import os
from pathlib import Path

p = "/home/xqs/data/report.tar.gz"

print(os.path.split(p))        # ('/home/xqs/data', 'report.tar.gz')
print(os.path.splitext(p))     # ('/home/xqs/data/report.tar', '.gz')

path = Path(p)
print(path.name)               # report.tar.gz
print(path.stem)               # report.tar   ← 去掉最后一个后缀
print(path.parent)             # /home/xqs/data
```

## 语句解释

### os.path.split(p)

在**最后一个分隔符**处切开，给 (目录, 文件名)。

### os.path.splitext(p)

在**最后一个点**处切开，给 (前面部分, 后缀)。

### Path 的属性写法

`.name` 文件名、`.stem` 去后缀的名字、`.parent` 目录——比字符串切分更清楚。

## 原理解释

**一句话：** 它们都是找「最后一个分隔符」或「最后一个点」，从那儿把字符串一分为二。

**执行逻辑（split）：**

1. 从右往左找最后一个路径分隔符
2. 找到 → 切两段返回（分隔符本身归到目录那侧）
3. 找不到 → 返回 `("", 整条路径)`

**执行逻辑（splitext）：**

1. 只看文件名部分，从右往左找最后一个点
2. 找到 → 点前面一段、点和后面一段
3. 找不到 → 返回 `(整条, "")`

**机器层（可跳过）：** 纯字符串操作，不碰磁盘。

**边界（从逻辑推出来）：**

- 第 1 步只找最后一个，所以 `a.tar.gz` 只用 splitext 得到 `.gz`
- 因为不查磁盘，所以路径不存在也能拆，结果照样「看起来对」
- 点开头的隐藏文件（`.env`）用 splitext 会得到 `('.env', '')`，因为那个点被当作前缀
- Windows 上两种分隔符都能认（`/` 和 `\`）

## 注意事项

- 这些函数只拆字符串，不验证路径合法性。
- 想拿「不带点的后缀」要自己 `splitext(p)[1].lstrip(".")`。
- 多后缀（`tar.gz`）只切最后一个，要全拆得自己循环。
- 新代码优先用 `Path` 的属性，可读性更好。

## 使用场景

- 从用户给的路径里取文件名做显示。
- 生成同名不同后缀的输出文件。
- 按目录分组文件。
