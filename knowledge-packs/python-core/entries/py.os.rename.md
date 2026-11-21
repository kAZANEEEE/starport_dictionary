---
id: py.os.rename
title: 重命名或移动文件
description: 改文件名，或者挪到别的目录
language: python
category_id: programming.filesystem
module: os

object:
  id: file.path
  name: 文件路径
  aliases: [文件, 文件名, 路径, 源文件, file path]

action:
  id: modify.change
  name: 修改
  aliases: [重命名, 改名, 移动, 挪, rename, move]

targets: []

utterances:
  direct:
    - 重命名文件
    - 移动文件到别的目录
    - 改文件名
  questions:
    - 怎么给文件改名
    - 如何把文件移到另一个文件夹
    - 目标文件已存在会怎样
  colloquial:
    - 这批文件想统一改名
    - 把处理的文件挪到 done 目录
  technical:
    - os.rename
    - shutil.move
    - Path.rename
    - 覆盖风险
  short_queries:
    - 重命名
    - rename
    - 移动

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.4"
version_note: Path.rename 从 3.4 起；shutil.move 支持跨盘
sources:
  - Python 官方文档 os.rename
  - Python 官方文档 shutil.move
---

# 重命名或移动文件

## 功能描述

输入源路径 + 目标路径，改名字或挪位置；同盘可直接 `rename`，跨盘要用 `shutil.move`。

## 推荐代码

```python
import os
import shutil
from pathlib import Path

# 演示用：先造一个文件
Path("old.txt").write_text("x", encoding="utf-8")

Path("old.txt").rename("new.txt")            # 同目录改名
os.rename("new.txt", "renamed.txt")          # 等价写法

Path("renamed.txt").replace("final.txt")     # 目标存在时直接覆盖

print(sorted(p.name for p in Path(".").glob("*.txt")))
```

## 语句解释

### Path.rename(目标)

改名或移动。**目标已存在时在 Windows 上会报错**（不像 POSIX 会静默覆盖）。

### Path.replace(目标)

目标存在时强制覆盖，这是“确保覆盖”的正确写法。

### shutil.move(源, 目标)

跨盘移动用它——`rename` 只改目录项，跨盘会抛 `OSError`。

## 原理解释

**一句话：** 改个名字（或换个所在目录），文件本身一个字节都不动。

**执行逻辑：**

1. 在源目录里找到那个名字对应的条目
2. 检查目标路径的上级目录存在吗、目标名字被占用吗
3. 把目录表里这个条目改指到新的名字/位置
4. 文件内容原地不动，只是登记信息改了

**机器层（可跳过）：** 同盘时只改目录项，属于「改登记」，所以瞬间完成。

**边界（从逻辑推出来）：**

- 第 3 步只在**同一个磁盘分区**内成立；跨盘时那个登记无处可改，抛错——要跨盘必须真的复制一遍（`shutil.move`）
- 第 2 步发现目标名已被占用时，Windows 上会直接报错而不是覆盖；要覆盖得用 `replace`
- 因为不改内容，所以大文件重命名也是瞬间的
- 文件正被别的程序打开时，第 3 步在 Windows 会失败
## 注意事项

- 目标已存在时 `rename` 在 Windows 会抛 `FileExistsError`，要覆盖用 `replace`。
- 跨盘移动用 `shutil.move`，别用 `rename`。
- 目标目录必须存在，不存在的父目录不会自动建。
- 批量改名时先算好映射再执行，避免中途撞名。
- 移动正在被别的程序打开的文件，Windows 会失败。

## 使用场景

- 批量给文件加时间前缀。
- 处理完的文件挪到 `done/` 目录。
- 把上传的临时文件改名成正式文件。
