---
id: py.http.headers
title: 自定义请求头
description: 带 Token、改 UA、声明要什么格式
language: python
category_id: programming.filesystem
module: requests
origin: thirdparty
import: "import requests"
qualname: "requests.get(headers=...)"
signature: "requests.get(url, headers={...})"
args:
  - name: "headers"
    required: false
    default: "None"
    accepts: "字典：键是头名、值是字符串；常见 Authorization、User-Agent、Accept"
    nesting: "可以，值可以用 f-string 拼（注意别把密钥写进日志）"
returns: "Response 对象：和普通请求一样；服务端靠这些头决定怎么回你"
object:
  id: http.response
  name: HTTP 响应
  aliases: [接口, 请求头, Token, 认证, response]
action:
  id: modify.change
  name: 修改
  aliases: [加请求头, 带 Token, 改 UA, 认证, headers]
targets: []
utterances:
  direct:
    - 自定义请求头
    - 请求带上 Token
    - 修改 User-Agent
  questions:
    - 怎么给请求加 header
    - 怎么带 Authorization
    - 为什么接口返回 403
  colloquial:
    - 接口要 token，怎么传进去
    - 网站不让我访问，说要改 UA
  technical:
    - requests headers
    - Authorization Bearer
    - User-Agent
    - "403"
  short_queries:
    - 请求头
    - header
    - token
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.8"
version_note: "requests 各版本一致；头名大小写不敏感"
sources:
  - requests 官方文档 自定义请求头
---

# 自定义请求头

## 功能描述

输入地址 + 头字典，把额外的头一起发出去；鉴权、指定格式、伪装 UA 都靠它。

## 推荐代码

```python
import threading
import http.server
import socketserver
import requests

# 演示用：本地接口把收到的 Authorization 头回声出来
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get("Authorization", "（没带）")
        body = f'{{"auth": "{auth}"}}'.encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

srv = socketserver.TCPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/"

r = requests.get(url, headers={"Authorization": "Bearer abc123"}, timeout=3)
print(r.json())     # {'auth': 'Bearer abc123'}
srv.shutdown()
```

## 语句解释

### headers={"Authorization": "Bearer abc123"}

最常见的鉴权写法：`Bearer` 后面跟 token。

### {"Accept": "application/json"}

声明「我要 JSON」，有些接口靠这个决定返回格式。

### {"User-Agent": "..."}

默认 UA 是 `python-requests/x.x`，有些网站会直接拒它。

## 原理解释

**一句话：** 头就是随请求一起发过去的一串「键: 值」，服务端拿它判断你是谁、要什么。

**执行逻辑：**

1. 取默认头（含 `User-Agent: python-requests/...`）
2. 把你传的 `headers` 合并进去（同名覆盖）
3. 补上 `Content-Length` 等必要头
4. 发出去
5. 服务端按这些头决定鉴权、返回格式、是否限流

**机器层（可跳过）：** 头就是请求报文开头的几行文本，不额外耗时。

**边界（从逻辑推出来）：**

- 第 2 步是「覆盖」，所以传 `User-Agent` 能盖掉默认值
- 因为服务端靠头鉴权，所以 token 泄露 = 别人能冒充你，**别把 token 打进日志**
- 头名大小写不敏感，但值区分大小写
- 用 `json=` 时不需要手写 `Content-Type`，会自动加；手写反而可能冲突

## 注意事项

- token 从环境变量读，别硬编码进代码。
- 打印响应时别把头（含 token）一起打出来。
- 403/401 通常是头不对或 token 过期，先查这两个。
- 有些接口要求 `Content-Type: application/json`，用 `json=` 会自动带。

## 使用场景

- 调需要 token 的接口（GitHub、大模型、自家后端）。
- 抓有 UA 校验的页面。
- 指定返回格式（JSON/XML）。
