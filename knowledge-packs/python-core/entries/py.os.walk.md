---
id: py.os.walk
title: 递归遍历目录树（os.walk）
description: 一层层往下走，同时拿到当前目录、子目录名和文件名
language: python
category_id: programming.filesystem
module: os
origin: stdlib
import: "import os"
qualname: "os.walk()"
signature: "os.walk(根目录, topdown=True)"
args:
  - name: "根目录"
    required: true
    accepts: "从哪个目录开始往下走"
    nesting: "可以"
  - name: "topdown"
    required: false
    default: "True"
    accepts: "True = 先父后子（可改 dirs 剪枝）；False = 反过来"
    nesting: "一般直接写 True"
returns: "生成器：每层给 (当前目录, 子目录名列表, 文件名列表)；只有名字没有路径"

object:
  id: dir.list
  name: 目录内容
  aliases: [目录, 目录树, 子目录, 文件夹, walk]

action:
  id: traverse.walk
  name: 遍历
  aliases: [遍历, 递归遍历, 走一遍, 深层遍历, walk]

targets: []

utterances:
  direct:
    - 递归遍历目录
    - 用 os.walk 遍历文件夹
    - 一层层往下遍历
  questions:
    - os.walk 怎么用
    - 如何同时拿到子目录和文件名
    - 怎么控制不进入某个子目录
  colloquial:
    - 想连子目录一起扫
    - 遍历的时候想跳过 .git 这种目录
  technical:
    - os.walk
    - topdown 参数
    - 修改 dirnames 跳过目录
  short_queries:
    - walk
    - 递归遍历
    - 目录树

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "os.walk 各版本一致；3.5 起支持 scandir 后端，3.12 起可用 Path.walk"
sources:
  - Python 官方文档 os.walk
---

# 递归遍历目录树（os.walk）

## 功能描述

输入根目录，逐个产出 `(当前目录路径, 子目录名列表, 文件名列表)` 三元组；默认自顶向下。

## 推荐代码

```python
import os
from pathlib import Path

Path("demo/sub").mkdir(parents=True, exist_ok=True)
Path("demo/a.txt").write_text("x", encoding="utf-8")
Path("demo/sub/b.txt").write_text("y", encoding="utf-8")

for root, dirs, files in os.walk("demo"):
    print(root, dirs, files)

# 想跳过某些目录：就地改 dirs（自顶向下时才有效）
for root, dirs, files in os.walk("demo"):
    dirs[:] = [d for d in dirs if d != "skip_me"]
    print("扫:", root, files)
```

## 语句解释

### for root, dirs, files in os.walk(根)

每进一层目录产出一次三元组：当前路径、这一层的子目录名、这一层的文件名。

### root / dirs / files 都是「当前这一层」

`dirs` 和 `files` 只有名字，没有路径；要完整路径得 `os.path.join(root, name)`。

### dirs[:] = [...] 就地修改

自顶向下时，**改 `dirs` 就能阻止它进入某些子目录**——这是剪枝的标准做法。

## 原理解释

**一句话：** 它从根目录开始，读一层、把子目录排进待办，再一个一个处理待办里的目录。

**执行逻辑：**

1. 把根目录放进待处理队列
2. 取出一个目录，读它的内容，分成「子目录」和「文件」
3. 产出 `(这个目录, 子目录列表, 文件列表)`
4. 把子目录追加进待处理队列（自顶向下：先产出当前层，再往下走）
5. 队列空了才结束

**机器层（可跳过）：** 每层一次目录读取；总开销与「目录数 + 文件数」成正比。

**边界（从逻辑推出来）：**

- 第 4 步决定顺序：默认先产出父目录再产出子目录（`topdown=True`）
- 因为第 3 步产出的是「当前层」，所以想只要文件、不要子目录，就得自己拼路径
- 第 4 步在读 `dirs` 之前/之后取决于方向，所以「改 `dirs` 剪枝」只在自顶向下时有效
- 遍历过程中删除/新建目录，可能影响后面看到的层（它边读边产，不是快照）

## 注意事项

- `files` 只有文件名，别直接当路径用。
- 想跳过 `.git`、`node_modules`，用 `dirs[:] = [...]` 剪枝，别在循环里 `continue`。
- 权限不足的目录会抛 `PermissionError`，需要包 try 才能继续扫。
- 3.12+ 也可以用 `Path(root).walk()`，写法更现代。

## 使用场景

- 统计项目里各类文件数量。
- 批量处理多级目录下的所有文件。
- 做文件索引、清理空目录。
