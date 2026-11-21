---
id: py.os.getenv
title: 读取环境变量
description: 从系统环境里取一个配置值，取不到就用默认值
language: python
category_id: programming.basics
module: os

object:
  id: env.variable
  name: 环境变量
  aliases: [环境变量, 环境配置, 系统变量, env, 配置项]

action:
  id: get.obtain
  name: 获取
  aliases: [读取, 取值, 拿到, 查, getenv, environ]

targets: []

utterances:
  direct:
    - 读取环境变量
    - 获取环境变量的值
    - 从环境里取配置
  questions:
    - 怎么读环境变量
    - 环境变量不存在怎么给默认值
    - 如何把密钥放在环境变量里
  colloquial:
    - 想从系统里读个配置
    - 密钥不想写死在代码里
  technical:
    - os.environ
    - os.getenv
    - dotenv
    - 密钥不要硬编码
  short_queries:
    - 环境变量
    - getenv
    - env

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: os.getenv / os.environ 接口稳定
sources:
  - Python 官方文档 os.getenv
---

# 读取环境变量

## 功能描述

输入变量名，输出它的值（字符串）；不存在时返回 `None` 或你给的默认值。

## 推荐代码

```python
import os

print(os.getenv("STARPORT_DEMO", "没设置"))   # 没设置就给默认值
os.environ["STARPORT_DEMO"] = "hello"
print(os.getenv("STARPORT_DEMO"))            # hello

# 必填项：没设置就直接报错退出
api_key = os.environ["SOME_REQUIRED_KEY"] if "SOME_REQUIRED_KEY" in os.environ else None
print(api_key)
```

## 语句解释

### os.getenv(名字, 默认值)

不存在返回默认值（不传默认值就是 `None`），**不报错**。

### os.environ[名字]

不存在直接抛 `KeyError`，适合「必须有」的配置。

### 赋值 os.environ[...] = ...

只影响当前进程和它启动的子进程，不影响系统全局。

## 原理解释

**一句话：** 它去查当前进程自带的一张「字符串键值表」，有就给你，没有就给默认值。

**执行逻辑：**

1. 拿变量名去进程的环境表里找
2. 找到 → 把值（一定是字符串）返回
3. 没找到 → `getenv` 返回默认值；`environ[...]` 抛 `KeyError`
4. 你给它赋值时，只是改这张表里的一项

**机器层（可跳过）：** 环境表在进程启动时从父进程复制过来，之后互不影响。

**边界（从逻辑推出来）：**

- 第 2 步值**永远是字符串**，读数字/布尔要自己 `int()` / `== "1"`
- 第 3 步两种写法差别就在「没有时怎么办」，必填用 `environ[]`，可选用 `getenv`
- 第 4 步只改当前进程，所以程序里改的值影响不到别的程序
- 从 IDE 启动和从命令行启动，拿到的环境可能不同——这解释了「同样的代码在我这儿能跑」

## 注意事项

- 值都是字符串，数字要转换，布尔建议用 `"1"/"true"` 约定。
- 密钥放环境变量仍可能被子进程继承，注意别把环境整包传给不信任的程序。
- 打包成 exe 后环境可能不同，要有默认值兜底。
- 改 `os.environ` 不影响系统，重启程序就没了。

## 使用场景

- 读 API Key（不写进代码库）。
- 区分开发/生产环境（`ENV=dev`）。
- 让同一份程序在不同机器上跑不同配置。
