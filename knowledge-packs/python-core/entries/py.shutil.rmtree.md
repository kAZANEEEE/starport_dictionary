---
id: py.shutil.rmtree
title: 删除整个目录
description: 连子目录带文件一起删，非常危险
language: python
category_id: programming.filesystem
module: shutil
origin: stdlib
import: "import shutil"
qualname: "shutil.rmtree()"
signature: "shutil.rmtree(path, ignore_errors=False)"
args:
  - name: "path"
    required: true
    accepts: "要删的目录路径（不能是文件）"
    nesting: "可以，但**务必先打印绝对路径确认**"
  - name: "ignore_errors"
    required: false
    default: "False"
    accepts: "True = 删不掉的跳过不报错（慎用，会掩盖问题）"
    nesting: "一般直接写 True/False"
returns: "None：没有返回值；副作用是整个目录树被删除，不进回收站"
object:
  id: dir.list
  name: 目录内容
  aliases: [目录, 文件夹, 目录树, 子目录, directory]
action:
  id: delete.remove
  name: 删除
  aliases: [删除, 清空, 移除, 递归删除, rmtree]
targets: []
utterances:
  direct:
    - 删除整个目录
    - 递归删除文件夹
    - 清空目录
  questions:
    - 怎么删除整个文件夹
    - rmtree 会删掉里面所有东西吗
    - 删除目录有回收站吗
  colloquial:
    - 想把临时目录整个删掉
    - 目录里还有子目录，怎么一次删完
  technical:
    - shutil.rmtree
    - os.rmdir
    - ignore_errors
    - 危险操作
  short_queries:
    - 删目录
    - rmtree
    - 清空目录
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "shutil.rmtree 各版本一致；失败时可能留下半个目录树"
sources:
  - Python 官方文档 shutil.rmtree
---

# 删除整个目录

## 功能描述

输入一个目录路径，把里面**所有文件和子目录**递归删掉；不进回收站，删了就没了。

## 推荐代码

```python
import shutil
from pathlib import Path

target = Path("tmpdir").resolve()
Path("tmpdir/sub").mkdir(parents=True, exist_ok=True)
Path("tmpdir/sub/a.txt").write_text("x", encoding="utf-8")

print("要删的是:", target)      # 先打印确认，这一步不能省
shutil.rmtree(target)
print("还在吗:", target.exists())   # False
```

## 语句解释

### shutil.rmtree(路径)

递归删除。它只认**目录**，传文件会抛 `NotADirectoryError`。

### 先 resolve() 再打印

`resolve()` 把相对路径变成绝对路径，你能肉眼确认到底删哪个。

### 和 os.rmdir 的区别

`rmdir` 只能删**空目录**；`rmtree` 连里面的东西一起删。

## 原理解释

**一句话：** 它先钻进目录把里面的东西一层层删光，最后删掉这个目录本身。

**执行逻辑：**

1. 列出目录里的所有条目
2. 是文件 → 直接删
3. 是子目录 → 回到第 1 步，先钻进去删
4. 子目录都空了 → 删掉这个子目录
5. 最后删掉根本身

**机器层（可跳过）：** 深度优先的递归删除；每次删除都是一次系统调用。

**边界（从逻辑推出来）：**

- 第 3 步是递归，所以**路径写错一个字符，可能删掉完全不相干的目录**
- 第 2 步删除不可撤销，标准库没有回收站，只有第三方 `send2trash` 能做到
- 中途因为权限失败会停下，留下**半个目录树**（这也是 `ignore_errors` 存在的理由）
- 正在被打开的文件在 Windows 上删不掉，会抛 `PermissionError`

## 注意事项

- **执行前必须打印 `Path(p).resolve()`**，肉眼确认再删。
- 不要拼后缀字符串，用 `Path` 操作。
- 删不掉的用 `ignore_errors=True` 会静默跳过，排查问题时反而更难。
- 想进回收站得用 `send2trash`（第三方）。

## 使用场景

- 清理构建产物、临时目录。
- 测试前后重置产物目录。
- 卸载式清理（慎用，做成需二次确认）。
