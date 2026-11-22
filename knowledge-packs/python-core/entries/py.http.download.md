---
id: py.http.download
title: 下载文件到本地
description: 大文件别一次读进内存，边收边写
language: python
category_id: programming.filesystem
module: requests
origin: thirdparty
import: "import requests"
qualname: "requests.get(stream=True) + 分块写"
signature: "requests.get(url, stream=True) → iter_content(块大小)"
args:
  - name: "url"
    required: true
    accepts: "文件地址"
    nesting: "可以"
  - name: "stream"
    required: false
    default: "False"
    accepts: "True = 不一次读完，改成边下边给（大文件必须开）"
    nesting: "一般直接写 True"
  - name: "块大小"
    required: false
    default: "8192 字节"
    accepts: "iter_content(chunk_size=...) 每次读多少字节"
    nesting: "一般直接写数字"
returns: "无（写到文件里）；用 r.iter_content 分块读，配合 with open('wb') 写盘"
object:
  id: file.content
  name: 文件内容
  aliases: [文件, 下载, 保存文件, 大文件, download]
action:
  id: create.new
  name: 创建
  aliases: [下载, 保存到本地, 写文件, 拉取, download]
targets: []
utterances:
  direct:
    - 下载文件到本地
    - 把网页文件保存下来
    - 下载大文件
  questions:
    - 怎么用 requests 下载文件
    - 大文件怎么下载不爆内存
    - 下载进度怎么显示
  colloquial:
    - 想把这个链接的文件存下来
    - 一下载就卡死，内存爆了
  technical:
    - requests stream
    - iter_content
    - 分块下载
    - 二进制写
  short_queries:
    - 下载
    - stream
    - 保存文件
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.8"
version_note: "stream + iter_content 在 requests 各版本一致"
sources:
  - requests 官方文档 原始响应内容
---

# 下载文件到本地

## 功能描述

输入文件地址，输出磁盘上的文件；**必须用 `stream=True` + 分块写**，否则大文件会占满内存。

## 推荐代码

```python
import threading
import http.server
import socketserver
from pathlib import Path
import requests

# 演示用：本地服务返回一段二进制
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"x" * 20000
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

srv = socketserver.TCPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/"

r = requests.get(url, stream=True, timeout=5)
r.raise_for_status()
total = 0
with open("downloaded.bin", "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)
        total += len(chunk)
print("下了", total, "字节，磁盘上", Path("downloaded.bin").stat().st_size)
srv.shutdown()
```

## 语句解释

### stream=True

告诉 requests「先别把内容全读进内存」，等你要时才读。

### r.iter_content(8192)

每次给你 8192 字节，边收边写。

### open(..., "wb")

二进制写，别用 `"w"`（文本模式会破坏字节）。

## 原理解释

**一句话：** 它一个包一个包地收，你收到一块就写一块，内存里只有当前这一块。

**执行逻辑：**

1. 建立连接，先不读响应体
2. 反复从连接里读 `chunk_size` 字节
3. 每块立刻写进文件、然后丢掉
4. 读到结束
5. 关闭连接和文件

**机器层（可跳过）：** 内存峰值 ≈ 块大小（几 KB），与文件大小无关。

**边界（从逻辑推出来）：**

- 第 2 步「反复读」是省内存的关键；不加 `stream` 就是第 1 步一次性读完整包进内存
- 第 3 步立刻写盘，所以中途断网会留下**不完整的文件**
- 因为先建连接再传数据，所以下载前可以用 `r.headers` 拿文件大小做进度
- 重定向会被自动跟随，最终地址看 `r.url`

## 注意事项

- 大文件必须 `stream=True`，否则内存爆。
- 用 `"wb"` 写，且写完检查大小是否等于 `Content-Length`。
- 断点续传可以用 `Range` 头 + 追加模式。
- 别把下载内容当 `r.text` 用，二进制会乱码。

## 使用场景

- 下载模型文件、安装包、图片。
- 批量爬取资源到本地。
- 给下载进度条提供数据（边收边更新）。
