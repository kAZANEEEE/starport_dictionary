---
id: py.sqlite.connect
title: 连接 SQLite 数据库
description: 打开一个数据库文件，拿到连接和游标
language: python
category_id: programming.database
module: sqlite3

object:
  id: sql.connection
  name: 数据库连接
  aliases: [数据库连接, 连接, 数据库, sqlite, conn]

action:
  id: create.new
  name: 创建
  aliases: [连接, 打开, 创建连接, 建立, connect]

targets: []

utterances:
  direct:
    - 连接 SQLite 数据库
    - 打开数据库文件
    - 创建数据库连接
  questions:
    - 怎么用 Python 连接 sqlite
    - 如何打开一个 db 文件
    - 数据库文件不存在会怎样
  colloquial:
    - 想存点数据，用个本地库
    - 那个 .db 文件怎么连
  technical:
    - sqlite3.connect
    - cursor
    - sqlite3 connection
  short_queries:
    - sqlite
    - 连接数据库
    - db

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: sqlite3 是标准库；3.12 起默认 autocommit 行为可通过属性显式控制
sources:
  - Python 官方文档 sqlite3.connect
---

# 连接 SQLite 数据库

## 功能描述

输入数据库文件路径，输出连接对象；文件不存在会**自动创建**，不是报错。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect("demo.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS t (id INTEGER PRIMARY KEY, name TEXT)")
con.commit()

print(con.isolation_level)
con.close()
```

## 语句解释

### sqlite3.connect(path)

打开或新建数据库文件。`":memory:"` 表示纯内存库，程序退出就没了，适合测试。

### con.cursor()

游标用来执行 SQL、取结果。一个连接可以有多个游标。

### con.commit()

提交事务。**不 commit，改动别人（和别的连接）看不到**，关连接时可能丢失。

## 原理解释

**一句话：** 打开（或新建）一个数据库文件，拿到一张「操作凭证」。

**执行逻辑：**

1. 按路径找这个文件
2. 找到 → 打开；**没找到 → 直接建一个空的**
3. 建立连接对象（后续所有 SQL 都通过它）
4. `.cursor()` 从连接里开一个游标，真正执行 SQL 的是游标
5. 用完 `close()` 关掉

**机器层（可跳过）：** SQLite 没有服务进程，连接就是打开了那个文件并加锁。

**边界（从逻辑推出来）：**

- 第 2 步「没找到就新建」，所以**路径写错不会报错**，你只会得到一个空库
- 写操作要 `commit()` 才落盘，因为默认在事务里
- 多个连接同时写会抢锁，报 `database is locked`
- `":memory:"` 不落地到文件，程序退出就没了，适合测试
## 注意事项

- 文件不存在会自动创建，所以路径写错也不会报错，只会得到一个空库——**这是最坑的一点**。
- 一定要 `commit()`，否则数据等于没写。
- 用完要 `close()`，或 `with contextlib.closing(con)`。
- 多线程共享连接要小心，默认线程不安全；每线程一个连接最稳。
- 路径用绝对路径或确认工作目录，避免建到意料之外的地方。

## 使用场景

- 本地存配置、日志、抓取结果。
- 小工具的数据存储（不需要装数据库服务）。
- 测试时用 `:memory:` 快速建库。
