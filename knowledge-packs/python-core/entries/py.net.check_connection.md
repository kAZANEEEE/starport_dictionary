---
id: py.net.check_connection
title: 检查网络能不能连上
description: 试着连一个地址端口，判断通不通
language: python
category_id: programming.filesystem

object:
  id: net.connection
  name: 网络连接
  aliases: [连接, 网络, 端口, 连通性, socket, connection]

action:
  id: inspect.check
  name: 判断
  aliases: [检查, 检测, 测试, 判断是否, 验证, check]

targets: []

utterances:
  direct:
    - 检查网络连接
    - 判断端口通不通
    - 测试能不能连上服务器
  questions:
    - 怎么检查网络是否可达
    - 如何判断某个端口有没有开
    - Python 怎么测试连接
  colloquial:
    - 想看看这个地址连不连得上
    - 服务是不是挂了，怎么探一下
  short_queries:
    - 连接
    - 端口
    - ping
    - socket

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: socket.create_connection 从 3.2 起支持 timeout 参数
sources:
  - Python 官方文档 socket.create_connection
---

# 检查网络能不能连上

## 功能描述

尝试和某个地址的某个端口建立 TCP 连接，用“成不成功”判断可达性。

## 推荐代码

```python
import socket

def is_reachable(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

print(is_reachable("127.0.0.1", 9, timeout=1))   # 大概率 False
print(is_reachable("127.0.0.1", 0, timeout=1))   # False
```

## 语句解释

### socket.create_connection((host, port), timeout)

尝试建 TCP 连接。成功返回一个已连接的 socket 对象，失败抛 `OSError`（含超时、拒绝、DNS 解析失败等）。

### with 语句

`with` 会在退出时自动关闭连接，不写的话每次都漏一个 socket。

### except OSError

把所有网络层错误统一当成“不通”。想区分“超时”和“拒绝”，分别捕获 `socket.timeout` 和 `ConnectionRefusedError`。

## 原理解释

TCP 连接成功的前提是对端端口在监听，所以“能连上”约等于“这个服务活着”，
但它**不检查应用层是否正常**——端口开了但接口返回 500，这里依然判定为通。

## 注意事项

- 这只是 TCP 层探测，不代表 HTTP 接口可用；要验接口得发真实请求。
- 探测公网地址时超时不要设太短，否则会把慢当成不通。
- 有些服务器会限速或封禁高频探测，别在循环里密集调用。
- 判断“本机端口有没有被占用”应该监听/查连接表，不是连它。

## 使用场景

- 程序启动前先确认依赖的服务（数据库、接口）在不在。
- 定时任务里做健康检查。
- 排错时快速区分“网络问题”还是“代码问题”。
