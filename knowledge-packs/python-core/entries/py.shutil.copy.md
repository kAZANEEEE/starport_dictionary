---
id: py.shutil.copy
title: 复制文件或目录
description: 连同元数据一起复制，跨盘也能用
language: python
category_id: programming.filesystem
module: shutil
origin: stdlib
import: "import shutil"
qualname: "shutil.copy() / shutil.copytree()"
signature: "shutil.copy(src, dst) / shutil.copytree(src, dst)"
args:
  - name: "src"
    required: true
    accepts: "要复制的文件（或目录，用 copytree）"
    nesting: "可以"
  - name: "dst"
    required: true
    accepts: "目标路径：给目录就复制进去，给文件名就改名；目录已存在会报错（copytree）"
    nesting: "可以，常配合 Path 拼接"
returns: "目标路径字符串（copy）/ 目标目录路径（copytree）；重名时 copytree 会抛 FileExistsError"
object:
  id: file.path
  name: 文件路径
  aliases: [文件, 复制, 备份, 拷贝, file]
action:
  id: create.new
  name: 创建
  aliases: [复制, 拷贝, 备份, 克隆, copy]
targets: []
utterances:
  direct:
    - 复制文件
    - 备份一个文件
    - 复制整个目录
  questions:
    - 怎么复制文件
    - copy 和 copy2 有什么区别
    - 复制目录到已存在的目录会怎样
  colloquial:
    - 想给文件留个备份
    - 把一个文件夹整体拷到别处
  technical:
    - shutil.copy
    - shutil.copy2
    - shutil.copytree
    - 保留修改时间
  short_queries:
    - 复制文件
    - copy
    - 备份
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "shutil 各函数稳定；copytree 的 dirs_exist_ok 是 3.8 起"
sources:
  - Python 官方文档 shutil.copy
  - Python 官方文档 shutil.copytree
---

# 复制文件或目录

## 功能描述

输入源路径和目标路径，复制出副本；`copy2` 会连修改时间一起保留，`copytree` 复制整个目录。

## 推荐代码

```python
import shutil
from pathlib import Path

Path("a.txt").write_text("内容", encoding="utf-8")

shutil.copy("a.txt", "b.txt")           # 复制成新文件
shutil.copy2("a.txt", "c.txt")          # 连修改时间一起复制
print(Path("b.txt").read_text(encoding="utf-8"))

Path("srcdir/inner").mkdir(parents=True, exist_ok=True)
Path("srcdir/inner/x.txt").write_text("x", encoding="utf-8")
shutil.copytree("srcdir", "dstdir", dirs_exist_ok=True)   # 整个目录
print(sorted(p.name for p in Path("dstdir").rglob("*")))
```

## 语句解释

### shutil.copy(src, dst)

复制内容 + 权限。`dst` 是目录时，会用原文件名复制进去。

### shutil.copy2(src, dst)

比 `copy` 多保留「修改时间」——备份时通常用这个。

### shutil.copytree(src, dst)

复制整个目录树。目标存在默认报错，`dirs_exist_ok=True` 可以合并进去。

## 原理解释

**一句话：** 它打开源文件读出字节，再写进目标文件——是真的复制了一份数据。

**执行逻辑：**

1. 打开源文件
2. 创建目标文件
3. 一块一块把字节读出来、写进去
4. 把源文件的权限（`copy2` 还有时间）复制到目标
5. 关闭两个文件

**机器层（可跳过）：** 因为要真的读写数据，所以复制大文件慢；同盘 `rename` 才是瞬间的。

**边界（从逻辑推出来）：**

- 第 3 步是真拷贝，所以复制 1GB 文件就要读 1GB、写 1GB
- 第 4 步说明 `copy` 不保留时间，备份想保持时间排序就得用 `copy2`
- 目标已存在时**文件会被覆盖**（copy），而 `copytree` 默认拒绝覆盖整个目录
- 中途出错会留下半个目标文件，脚本应自己清理

## 注意事项

- 备份用 `copy2`，否则修改时间会变成「现在」。
- 大文件复制要显示进度，别让人以为卡死。
- `copytree` 目标已存在会抛错，需要 `dirs_exist_ok=True`。
- 只想改名或同盘移动，用 `Path.rename`，别复制。

## 使用场景

- 备份重要文件（带时间戳的副本）。
- 打包前把资源拷到临时目录。
- 复制模板目录生成新项目。
