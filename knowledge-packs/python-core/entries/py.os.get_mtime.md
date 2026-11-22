---
id: py.os.get_mtime
title: 取文件修改时间
description: 这个文件最后一次改动是什么时候
language: python
category_id: programming.filesystem
module: os
origin: stdlib
import: "import os"
qualname: "os.path.getmtime()"
signature: "os.path.getmtime(path) / Path(path).stat().st_mtime"
args:
  - name: "path"
    required: true
    accepts: "文件（或目录）路径；不存在会抛异常"
    nesting: "可以"
returns: "浮点数：从 1970 年起的秒数（时间戳）；要给人看再用 datetime.fromtimestamp 转换"
object:
  id: file.mtime
  name: 文件修改时间
  aliases: [修改时间, 最后修改, 更新时间, mtime, 时间戳]
action:
  id: get.obtain
  name: 获取
  aliases: [取, 获取, 查看, 读, getmtime]
targets: []
utterances:
  direct:
    - 获取文件修改时间
    - 查看文件最后修改时间
    - 文件是什么时候改的
  questions:
    - 怎么取文件的修改时间
    - 怎么按修改时间排序文件
    - getmtime 返回的是什么
  colloquial:
    - 想找出今天改过的文件
    - 按时间顺序列出文件
  technical:
    - os.path.getmtime
    - st_mtime
    - fromtimestamp
    - 按时间排序
  short_queries:
    - 修改时间
    - mtime
    - 时间戳
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.4"
version_note: "os.path.getmtime 更老；Path.stat 从 3.4 起"
sources:
  - Python 官方文档 os.path.getmtime
---

# 取文件修改时间

## 功能描述

输入文件路径，输出时间戳（浮点秒数）；配合 `datetime.fromtimestamp` 变成人能看的时间。

## 推荐代码

```python
import os
from datetime import datetime
from pathlib import Path

Path("demo.txt").write_text("x", encoding="utf-8")

ts = os.path.getmtime("demo.txt")
print(ts)                                    # 1795xxxxxx.123
print(datetime.fromtimestamp(ts))            # 2026-11-22 13:05:01

# 按修改时间排序文件
files = sorted(Path(".").glob("*.txt"), key=lambda p: p.stat().st_mtime)
print([p.name for p in files])
```

## 语句解释

### os.path.getmtime(path)

返回浮点秒数。要「多久之前改的」就再减一下当前时间。

### datetime.fromtimestamp(ts)

转成本地时间对象。**不转的话就只是个数字**。

### key=lambda p: p.stat().st_mtime

按修改时间排序的标准写法：每个文件取一次时间当排序依据。

## 原理解释

**一句话：** 它只是问文件系统「这个文件上次被写是什么时候」，不读文件内容。

**执行逻辑：**

1. 按路径找到目录项
2. 读出元数据里的「修改时间」字段（一个时间戳）
3. 返回这个数字

**机器层（可跳过）：** 一次 `stat` 查询，再大的文件也瞬间返回。

**边界（从逻辑推出来）：**

- 第 2 步返回的是**时间戳**，不是年月日，所以必须转换才能读
- `stat` 的时间有「访问时间(atime)、修改时间(mtime)、状态变更(ctime)」三种，日常说「最后改的」用 mtime
- 因为只查元数据，所以拿一批文件的 mtime 很快
- 复制文件时如果不用 `copy2`，mtime 会变成「现在」——这是备份脚本常踩的坑

## 注意事项

- 返回的是秒数，转人读时间用 `datetime.fromtimestamp`。
- 想「多久没改了」用 `time.time() - ts`。
- 排序用 `st_mtime`，不要用 `st_ctime`（那是元数据变更时间，不是内容修改）。
- 跨时区显示要注意，`fromtimestamp` 用的是本地时区。

## 使用场景

- 找最近改过的文件（增量处理）。
- 按时间给文件排序、生成归档。
- 判断缓存是否过期。
