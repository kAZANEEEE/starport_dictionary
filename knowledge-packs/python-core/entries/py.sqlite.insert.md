---
id: py.sqlite.insert
title: 往表里插入数据
description: 安全地写入一行记录，避免 SQL 注入
language: python
category_id: programming.database
module: sqlite3

object:
  id: db.record
  name: 数据库记录
  aliases: [记录, 一行数据, 表记录, 数据行, record]

action:
  id: create.new
  name: 创建
  aliases: [插入, 添加, 写入, 新增, insert]

targets: []

utterances:
  direct:
    - 插入数据
    - 往表里写一行
    - 新增记录
  questions:
    - 怎么往 sqlite 表里插入数据
    - 如何防止 SQL 注入
    - 一次插入多条怎么写
  colloquial:
    - 存一条记录进库
    - 有变量要拼到 SQL 里怎么拼
  technical:
    - sqlite3 execute
    - executemany
    - 参数化查询 ?
  short_queries:
    - 插入
    - insert
    - 参数化

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: 参数化写法（? 占位符）各版本一致，且是唯一推荐写法
sources:
  - Python 官方文档 sqlite3 参数化查询
---

# 往表里插入数据

## 功能描述

输入表名 + 一行值，写入一条记录；用 `?` 占位符传参，**不要自己拼字符串**。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")

cur.execute("INSERT INTO t (name) VALUES (?)", ("张三",))
cur.executemany("INSERT INTO t (name) VALUES (?)", [("李四",), ("王五",)])
con.commit()

print(cur.execute("SELECT * FROM t").fetchall())
con.close()
```

## 语句解释

### INSERT ... VALUES (?)

`?` 是占位符，真正的值作为第二个参数传进去。**这一步就是防注入的关键**。

### 单个值要写成元组

`("张三",)` 后面那个逗号不能少，否则变成字符串而不是元组。

### executemany(...)

一次插多行，比循环 `execute` 快很多（少了解析 SQL 的次数）。

## 原理解释

**一句话：** 造一行新数据，按列的顺序把值填进去，然后追加到表末尾。

**执行逻辑：**

1. 解析 SQL 结构（`INSERT INTO 表 (列...) VALUES (?, ?)`），先把结构编译好
2. 把参数里的值按顺序**填进占位符**
3. 逐列检查约束（非空、类型、主键唯一）
4. 通过 → 新行追加进去；不通过 → 抛错，什么都不写
5. `commit()` 之后别人才看得到

**机器层（可跳过）：** 参数化 = SQL 结构与值分开传输，值永远不会被当成语法。

**边界（从逻辑推出来）：**

- 第 2 步「值只当值」是防注入的全部原理：`' OR 1=1 --` 只是一个字符串
- 用 f-string 拼 SQL 就等于跳过第 1 步、把值混进语法里，注入就成立了
- 第 3 步主键重复会抛 `IntegrityError`，批量插入要处理
- 单值要写成 `(v,)`，少了逗号就变成字符串，第 2 步会拆成多个字符
## 注意事项

- **永远用 `?` 占位符**，不要 f-string 拼值（拼表名/列名另说，那种要白名单校验）。
- 单值元组别忘逗号：`(v,)`。
- 需要拿自增 id 用 `cur.lastrowid`。
- 批量插入用 `executemany`，并放在同一个事务里 `commit`。

## 使用场景

- 保存抓取结果、日志、用户输入。
- 导入 CSV 数据到表里。
- 测试里建内存库造数据。
