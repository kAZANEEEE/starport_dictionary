---
id: py.argparse.parse
title: 解析命令行参数
description: 拿到用户启动程序时敲的那些参数
language: python
category_id: programming.basics
module: argparse
origin: stdlib
import: "import argparse"
qualname: "argparse.ArgumentParser"

object:
  id: cli.args
  name: 命令行参数
  aliases: [命令行参数, 启动参数, 参数, argv, 命令行]

action:
  id: get.obtain
  name: 获取
  aliases: [解析, 读取, 拿到, 取值, parse, parse_args]

targets: []

utterances:
  direct:
    - 解析命令行参数
    - 读取启动参数
    - 处理命令行输入
  questions:
    - 怎么解析命令行参数
    - 如何让脚本接受参数
    - 怎么加 --help 说明
  colloquial:
    - 想让脚本跑的时候带个文件名
    - 别让人改代码，用参数传
  technical:
    - argparse
    - add_argument
    - parse_args
    - 位置参数与可选参数
  short_queries:
    - 命令行
    - argparse
    - 参数

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.2"
version_note: argparse 从 3.2 起在标准库；用法稳定
sources:
  - Python 官方文档 argparse
---

# 解析命令行参数

## 功能描述

输入「参数定义」+ 实际的命令行字符串，输出一个带属性的对象（如 `args.name`）；格式不对会自动报错并打印帮助。

## 推荐代码

```python
import argparse

parser = argparse.ArgumentParser(description="演示脚本")
parser.add_argument("path", help="要处理的文件路径")
parser.add_argument("--count", type=int, default=1, help="处理次数")

# 正常用法是从 sys.argv 取；这里显式给一份方便演示
args = parser.parse_args(["data.txt", "--count", "3"])
print(args.path, args.count, args.count + 1)
```

## 语句解释

### add_argument("path")

不带横线 = **位置参数**，必须给，按顺序对应。

### add_argument("--count", type=int, default=1)

带横线 = **可选参数**，可以不给（用 default）；`type=int` 会自动转成数字。

### parse_args(...)

真正去解析；不给参数就读 `sys.argv`（程序名之后的部分）。

## 原理解释

**一句话：** 它照着「参数清单」把命令行那串词逐个对上号，对不上就报错退出。

**执行逻辑：**

1. 先读命令行（`sys.argv[1:]`）
2. 拿第 1 个位置参数的定义去吃掉一个词，转成声明的类型
3. 遇到 `--count 3` 这种，识别成可选参数并吃掉后面的值
4. 遇到 `-h/--help` 就直接打印帮助并退出
5. 全部处理完：返回一个对象，属性名就是参数名；有多余/缺失的词就报错

**机器层（可跳过）：** 纯字符串解析，不启动任何外部程序。

**边界（从逻辑推出来）：**

- 第 2 步按顺序吃，所以位置参数的**顺序不能乱**
- 第 3 步的 `type=int` 失败时会由 argparse 直接报错退出——不是你代码里的异常
- 第 5 步「多余就报错」意味着定义和输入必须严格对应
- 因为 `-h` 是内置的（第 4 步），所以白送一个帮助页面，只要写了 `help=`

## 注意事项

- `type=int` 只做转换，范围校验要自己加（或用 `choices=`）。
- 布尔开关用 `action="store_true"`，别写 `--flag True`。
- 调试时给 `parse_args([...])` 传一份假参数，不要改 `sys.argv`。
- 位置参数多了会让用法难记，超过两个就该改成 `--option`。

## 使用场景

- 脚本接受输入文件/输出目录。
- 批量任务控制并发数、是否覆盖。
- 给工具加自动 `--help`。
