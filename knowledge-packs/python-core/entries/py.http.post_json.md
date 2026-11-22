---
id: py.http.post_json
title: 发 POST 并传 JSON
description: 往接口提交数据，最常用的是 json=
language: python
category_id: programming.filesystem
module: requests
origin: thirdparty
install: "pip install requests"
import: "import requests"
qualname: "requests.post(json=...)"
signature: "requests.post(url, json=数据, timeout=5)"
args:
  - name: "url"
    required: true
    accepts: "接口地址"
    nesting: "可以"
  - name: "json"
    required: false
    default: "None"
    accepts: "会被自动转成 JSON 文本，并设好 Content-Type"
    nesting: "可以，嵌套字典也行"
  - name: "data"
    required: false
    default: "None"
    accepts: "表单提交用；和 json 二选一，别同时传"
    nesting: "可以"
returns: "Response 对象：.status_code 判断成败、.json() 取回包"
object:
  id: http.response
  name: HTTP 响应
  aliases: [接口, 提交数据, 响应, 返回数据, response]
action:
  id: create.new
  name: 创建
  aliases: [提交, 发送, 上传数据, 调用, post]
targets: []
utterances:
  direct:
    - 发 POST 请求
    - 提交 JSON 数据给接口
    - 往接口写入数据
  questions:
    - 怎么用 requests 发 post
    - json 和 data 参数有什么区别
    - 提交表单怎么写
  colloquial:
    - 想往服务器存一条数据
    - 接口要 POST，怎么带参数
  technical:
    - requests.post
    - json 参数
    - Content-Type
    - 表单提交
  short_queries:
    - post
    - 提交
    - 接口写入
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.8"
version_note: "requests 是第三方库；已装 2.32"
sources:
  - requests 官方文档 快速上手
---

# 发 POST 并传 JSON

## 功能描述

输入地址 + 数据，发 POST 请求；`json=` 自动转 JSON 并设好头，`data=` 是表单提交。

## 推荐代码

```python
import threading
import http.server
import socketserver
import requests

# 演示用：起一个本地接口，实际使用删掉这段换成真实 url
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"received": true}')
        print("服务端收到:", body.decode())
    def log_message(self, *a): pass

srv = socketserver.TCPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/"

r = requests.post(url, json={"name": "张三", "age": 20}, timeout=3)
print(r.status_code)     # 201
print(r.json())          # {'received': True}
srv.shutdown()
```

## 语句解释

### json=数据

自动做两件事：把字典转成 JSON 文本 + 把 `Content-Type` 设成 `application/json`。

### data=数据

表单提交（`application/x-www-form-urlencoded`）。**和 `json` 二选一**。

### status_code 201

创建成功通常返回 201，不是 200；所以判断要写 `r.ok` 或 `< 400`。

## 原理解释

**一句话：** 它把数据编码成请求体，带上方法和头，发出去，再把回包装进 Response。

**执行逻辑：**

1. 把 `json=` 的数据转成 JSON 文本
2. 设置 `Content-Type: application/json` 和 `Content-Length`
3. 建立连接，发送 POST 请求 + 请求体
4. 读回状态码、头、响应体
5. 关闭连接

**机器层（可跳过）：** 一次网络往返；请求体大时会分块传。

**边界（从逻辑推出来）：**

- 第 1 步是自动转换，所以传 `datetime` 会失败（它不认），要先转成字符串
- 第 2 步自动设头，所以**不要再用 `headers` 手动写 `Content-Type`**，容易冲突
- 第 4 步不检查状态码，所以 4xx 也不会抛异常
- 一个请求只能带一种体：`json=` 和 `data=` 同时传，只有 `data` 生效

## 注意事项

- `json=` 和 `data=` 二选一。
- 中文会自动转义成 `\uXXXX`，多数服务端都能正确解析，不用特殊处理。
- 传文件要用 `files=`。
- 仍然要写 `timeout`。

## 使用场景

- 提交表单/评论/订单。
- 调用需要写数据的接口。
- 上报日志、埋点。
