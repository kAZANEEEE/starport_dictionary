---
id: py.fs.traverse_directory
title: 遍历文件夹里所有文件
description: 递归找出一个目录下的全部文件
language: python
category_id: programming.filesystem
module: pathlib
origin: stdlib
import: "from pathlib import Path"
qualname: "pathlib.Path.rglob"
signature: "Path(root).rglob(\"*\")"
args:
  - name: "root"
    required: true
    accepts: "要开始遍历的目录路径"
    nesting: "可以，常见是 Path.cwd() 或用户输入的目录"
  - name: "pattern"
    required: false
    default: "\"*\""
    accepts: "匹配模式，如 \"*\"、\"*.py\"、\"**/*.txt\""
    nesting: "一般直接写字面量"
returns: "生成器：一个个吐出 Path 对象（含目录）；要列表得 list(...)"

object:
  id: dir.list
  name: 目录内容
  aliases: [目录, 文件夹, 文件夹里有什么, 目录列表, listdir, directory]

action:
  id: traverse.walk
  name: 遍历
  aliases: [循环, 递归, 逐个处理, 走一遍, walk, iterate]

targets: []

utterances:
  direct:
    - 遍历文件夹
    - 递归遍历目录
    - 把目录下所有文件列出来
  questions:
    - 怎么遍历文件夹里所有文件
    - 如何递归列出目录下所有文件
    - Python 怎么走一遍整个目录
  colloquial:
    - 我想把一个文件夹里的东西全找出来
    - 文件夹里面还有文件夹，怎么全扫一遍
  goal_based:
    - 统计某个目录下有多少个文件
  short_queries:
    - 遍历
    - 目录
    - rglob

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.5"
version_note: rglob 从 3.5 起就有；3.12 加入了 walk()，但这里用的写法兼容更广
sources:
  - Python 官方文档 pathlib.Path.rglob
---

# 遍历文件夹里所有文件

## 功能描述

递归列出目录下的所有文件，包括子目录里的。

## 推荐代码

```python
from pathlib import Path

root = Path(".")
files = [p for p in root.rglob("*") if p.is_file()]

print(len(files))
for p in files[:5]:
    print(p)
```

## 语句解释

### Path(".")

当前目录。换成任意目录路径都行。

### .rglob("*")

递归匹配所有条目，把子目录里的也带出来。只想看一层用 `.glob("*")`。

### if p.is_file()

`rglob` 连目录也会一起返回，这个判断只留下文件。

### 列表推导式

把结果一次性收集成列表。文件特别多时改成生成器（去掉方括号），省内存。

## 原理解释

**一句话：** 像翻抽屉——先看这一层有什么，遇到子目录就钻进去继续看。

**执行逻辑：**

1. 列出当前目录下的所有条目
2. 逐个检查：是文件就交给筛选条件判断；是目录就**回到第 1 步**从它里面开始
3. 子目录看完了，退回来继续处理当前目录剩下的条目
4. 全部走完，把符合条件的收集成列表

**机器层（可跳过）：** 每进一层目录就多一次目录读取调用，开销与「目录数 + 文件数」成正比。

**边界（从逻辑推出来）：**

- 第 2 步会钻进子目录，所以结果**包含任意深度的文件**；只要一层就用 `glob("*")`
- 第 1 步会连目录一起返回，所以要 `if p.is_file()` 过滤，否则目录也会被当成结果
- 遇到没权限的子目录，第 1 步直接抛异常，整个遍历中断——需要不想被打断就得在那一步包 `try`
- 数据太多时列表会很大，改成生成器（去掉方括号）就能边遍历边处理
## 注意事项

- 目录里如果有几万文件，先 `len()` 再遍历，避免一次占满内存。
- 会跟随符号链接，可能绕成环；要排除可以用 `Path.walk()`（3.12+）或自己判断。
- 权限不足的子目录会直接抛 `PermissionError`，需要 `try/except` 跳过。
- 想按后缀筛，配合 `p.suffix == ".py"`，别用字符串 `endswith` 拼路径。

## 使用场景

- 批量处理某个项目里的所有源码。
- 统计目录规模和文件类型分布。
- 做索引、备份、搜索前的文件收集。
