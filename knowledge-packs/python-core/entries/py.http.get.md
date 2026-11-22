---
id: py.http.get
title: 发 GET 请求
description: 从接口拿数据，最常用的网络操作
language: python
category_id: programming.filesystem
module: requests
origin: thirdparty
import: "import requests"
qualname: "requests.get()"
signature: "requests.get(url, params=None, timeout=None, headers=None)"
args:
  - name: "url"
    required: true
    accepts: "完整地址，如 https://api.x.com/v1/list"
    nesting: "可以，常配合 f-string 拼路径（注意别把用户输入直接拼进去）"
  - name: "params"
    required: false
    default: "None"
    accepts: "查询参数字典，会自动拼成 ?a=1&b=2"
    nesting: "可以，值可以是变量"
  - name: "timeout"
    required: false
    default: "不限（**强烈建议设**）"
    accepts: "秒数；不设可能永远卡住"
    nesting: "一般直接写数字"
returns: "Response 对象：.status_code 状态码、.text 文本、.json() 解析成字典、.headers 响应头"
object:
  id: http.response
  name: HTTP 响应
  aliases: [接口, 响应, 请求, 返回数据, response]
action:
  id: get.obtain
  name: 获取
  aliases: [请求, 获取, 拉取, 调用接口, get]
targets: []
utterances:
  direct:
    - 发 GET 请求
    - 调用接口拿数据
    - 请求一个网址
  questions:
    - 怎么用 requests 发 get 请求
    - 请求返回的是什么对象
    - 怎么判断请求成功没
  colloquial:
    - 想从接口拿点数据回来
    - 网页内容怎么抓下来
  technical:
    - requests.get
    - response.status_code
    - response.json
    - 超时
  short_queries:
    - 请求
    - get
    - 接口
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.8"
version_note: "requests 是第三方库，需 pip install requests；本机已装 2.32"
sources:
  - requests 官方文档 快速上手
---

# 发 GET 请求

## 功能描述

输入地址（+ 可选参数、超时），输出响应对象；**必须检查状态码**，因为 4xx/5xx 不会抛异常。

## 推荐代码

```python
import json
import threading
import http.server
import socketserver
import requests

# 演示用：起一个本地接口，实际使用时删掉这一段，换成真实 url
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true, "name": "starport"}')
    def log_message(self, *a): pass

srv = socketserver.TCPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/"

r = requests.get(url, timeout=3)
print(r.status_code)        # 200
print(r.json())             # {'ok': True, 'name': 'starport'}
srv.shutdown()
```

## 语句解释

### requests.get(url, timeout=3)

发 GET。**`timeout` 一定要写**，否则对方不响应时程序会一直等。

### r.status_code

HTTP 状态码：200 成功、404 没有、500 服务端出错。

### r.json()

把响应体按 JSON 解析成字典。内容不是 JSON 会抛 `ValueError`。

## 原理解释

**一句话：** 它拼出一个 HTTP 请求发过去，把服务器回的整包内容装进一个 Response 对象给你。

**执行逻辑：**

1. 解析 URL，拼出请求行和头
2. 建立 TCP 连接（可能是 https，需要 TLS 握手）
3. 发请求，等服务端回响应
4. 把状态码、响应头、响应体读进来
5. 关闭连接（或放回连接池）

**机器层（可跳过）：** 一次真实网络往返，耗时取决于网络，不在你代码的控制范围内。

**边界（从逻辑推出来）：**

- 第 3 步要等，所以不设 `timeout` 就可能卡很久——这是脚本"假死"的头号原因
- 第 4 步把响应体**整个读进内存**，下载大文件别用 `get`，用 `stream=True`
- 它**不把 4xx/5xx 当异常**，所以必须自己判断 `status_code`
- 因为第 5 步会关连接，取完 `.text` 后再用 `r.raw` 就没数据了

## 注意事项

- **一定写 `timeout`**。
- 检查 `r.status_code == 200` 或用 `r.raise_for_status()`。
- 大文件用 `stream=True` 分块读，别一次进内存。
- URL 里的查询参数用 `params=` 传，别自己拼（会自动转义）。

## 使用场景

- 调第三方接口拿数据。
- 抓取网页内容（再配合解析库）。
- 做健康检查、拉取配置。
