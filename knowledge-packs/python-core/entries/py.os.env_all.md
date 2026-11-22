---
id: py.os.env_all
title: 列出所有环境变量
description: 看看这台机器上有哪些配置项
language: python
category_id: programming.basics
module: os
origin: stdlib
import: "import os"
qualname: "os.environ"
signature: "os.environ / dict(os.environ)"
args:
  - name: "无参数"
    required: false
    default: "—"
    accepts: "os.environ 本身就是个映射对象，不用传参"
    nesting: "可以 dict(os.environ) 转成普通字典再处理"
returns: "映射对象：键是变量名、值是字符串；可以遍历、取长度、转字典"
object:
  id: env.variable
  name: 环境变量
  aliases: [环境变量, 系统配置, 环境, env, 变量表]
action:
  id: get.obtain
  name: 获取
  aliases: [列出, 遍历, 全部取出, 查看全部, environ]
targets: []
utterances:
  direct:
    - 列出所有环境变量
    - 遍历环境变量
    - 查看系统配置项
  questions:
    - 怎么打印所有环境变量
    - os.environ 怎么遍历
    - 环境变量有多少个
  colloquial:
    - 想看看机器上有哪些环境变量
    - 排查配置问题时想把环境全打出来
  technical:
    - os.environ
    - 环境变量遍历
    - dict(os.environ)
  short_queries:
    - 环境变量列表
    - environ
    - 全部变量
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "os.environ 各版本一致；3.5+ 在 Windows 上大小写不敏感"
sources:
  - Python 官方文档 os.environ
---

# 列出所有环境变量

## 功能描述

输入无（`os.environ` 本身就是映射对象），输出「变量名 → 字符串值」的完整列表。

## 推荐代码

```python
import os

count = len(os.environ)
print("环境变量个数:", count)

for key in sorted(os.environ)[:5]:
    print(key, "=", os.environ[key][:40])

# 排序后转成普通字典
env = dict(os.environ)
print("PATH 在里面吗:", "PATH" in env)
```

## 语句解释

### os.environ

不是函数，是一个**映射对象**，像字典一样用。

### len(os.environ)

环境变量个数。

### dict(os.environ)

转成普通字典，方便排序、复制、`json.dumps`。

## 原理解释

**一句话：** 它把当前进程自带的那张「名字 → 值」表暴露出来，你能遍历、能改。

**执行逻辑：**

1. 读取进程的环境表（启动时从父进程复制来的）
2. 遍历时逐个给出「变量名」
3. 用变量名去取，就得到字符串值
4. 给它赋值时，只改当前进程这张表

**机器层（可跳过）：** 环境表在进程内存里，读它不涉及磁盘或系统调用。

**边界（从逻辑推出来）：**

- 第 1 步是**复制**来的，所以别的进程后来改了你也看不到
- 第 3 步值永远是字符串，数字要自己转换
- 改 `os.environ` 只影响当前进程和它启动的子进程
- 打印全部变量时注意：里面可能有令牌、路径这类敏感信息，别贴到公开地方

## 注意事项

- 别把整个环境变量打印到日志或聊天里，可能泄露令牌。
- 想要某个值用 `os.getenv("名字", 默认)`，不要遍历。
- Windows 上环境变量名大小写不敏感。
- 遍历时别改（增删），会抛 RuntimeError。

## 使用场景

- 排查「为什么读不到配置」时把环境打出来。
- 启动子进程前筛出需要传递的变量。
- 统计/审计运行时环境（注意脱敏）。
