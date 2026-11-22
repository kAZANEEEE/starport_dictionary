---
id: py.os.temp_file
title: 创建临时文件
description: 程序中间产物放临时目录，用完自动或不自动删
language: python
category_id: programming.filesystem
module: tempfile
origin: stdlib
import: "import tempfile"
qualname: "tempfile.NamedTemporaryFile / mkstemp"
signature: 'tempfile.NamedTemporaryFile(delete=True, suffix=".txt")'
args:
  - name: "delete"
    required: false
    default: "True"
    accepts: "True = 离开 with 块自动删；False = 保留文件（需要路径给别人用时）"
    nesting: "一般直接写 True/False"
  - name: "suffix"
    required: false
    default: '""'
    accepts: "后缀，如 \".txt\"、\".json\""
    nesting: "一般直接写字面量"
returns: "文件对象：.name 是临时路径；with 块结束时按 delete 决定删不删"
object:
  id: file.path
  name: 文件路径
  aliases: [临时文件, 临时目录, 中间文件, 缓存文件, temp]
action:
  id: create.new
  name: 创建
  aliases: [创建, 生成, 新建, 开临时文件, tempfile]
targets: []
utterances:
  direct:
    - 创建临时文件
    - 用临时文件存中间结果
    - 临时目录怎么写
  questions:
    - 怎么创建临时文件
    - 临时文件会自动删除吗
    - 怎么拿到临时文件的路径
  colloquial:
    - 中间结果放哪儿比较合适
    - 想生成个临时文件给别人程序读
  technical:
    - tempfile
    - NamedTemporaryFile
    - TemporaryDirectory
    - 自动删除
  short_queries:
    - 临时文件
    - tempfile
    - 临时目录
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "NamedTemporaryFile 各版本一致；Windows 上文件被打开时不能再次打开同一路径"
sources:
  - Python 官方文档 tempfile
---

# 创建临时文件

## 功能描述

输入后缀等参数，输出一个文件对象；默认在离开 `with` 块时**自动删除**。

## 推荐代码

```python
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write("中间结果")
    f.flush()
    print("路径:", f.name)
    print(Path(f.name).read_text(encoding="utf-8"))

Path(f.name).unlink()      # delete=False 就要自己删

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "a.txt"
    p.write_text("x", encoding="utf-8")
    print("临时目录里有:", [x.name for x in Path(d).iterdir()])
```

## 语句解释

### NamedTemporaryFile(delete=...)

生成一个名字唯一的临时文件。`delete=True` 时出块自动删。

### 为什么常写 delete=False

因为 **Windows 上文件打开期间别人打不开**，你要用路径再读一次就得关掉，关掉就被删了，所以先设 False 手动删。

### TemporaryDirectory()

生成一个临时目录，出块时整个删掉，适合放一堆中间文件。

## 原理解释

**一句话：** 它在系统的临时目录里造一个不重名的文件，名字由系统保证唯一。

**执行逻辑：**

1. 找系统临时目录（Linux 是 /tmp，Windows 是用户 Temp）
2. 生成一个带随机后缀的名字
3. 创建这个文件
4. 交给你的代码使用
5. 关闭时按 `delete` 决定删除

**机器层（可跳过）：** 就是普通文件，只是放在系统会定期清理的目录里。

**边界（从逻辑推出来）：**

- 第 2 步保证唯一，所以多进程同时跑不会撞名
- 第 5 步前文件一直被占用，所以 Windows 上不能"打开着再按路径读"
- 它**不保证**程序崩溃后一定被删（`delete=False` 时更是明确不删）
- 临时目录可能被系统清理，别把它当长期存储

## 注意事项

- Windows 上 `delete=False` 更常见（否则路径没法再用）。
- 手动删记得 `unlink()`，别留垃圾。
- 临时文件不能当持久存储，重启或清理就没了。
- 敏感数据用完立刻删，别留在 temp 里。

## 使用场景

- 处理大文件时的中间产物。
- 把内存数据写成临时文件给外部程序读。
- 测试里造一次性文件。
