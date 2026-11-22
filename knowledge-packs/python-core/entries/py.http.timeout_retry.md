---
id: py.http.timeout_retry
title: 超时与重试
description: 网络请求不能裸奔，超时和重试都要写
language: python
category_id: programming.filesystem
module: requests
origin: thirdparty
install: "pip install requests"
import: "import requests"
qualname: "requests.exceptions / 重试循环"
signature: "try: requests.get(url, timeout=5) except requests.RequestException"
args:
  - name: "timeout"
    required: true
    accepts: "连不上和读不到的时间上限（秒）；可传元组 (连接超时, 读取超时)"
    nesting: "一般直接写数字"
  - name: "重试次数"
    required: false
    default: "2~3 次"
    accepts: "失败后重试几次；建议配合递增等待"
    nesting: "一般直接写数字"
returns: "成功返回 Response；失败抛 requests.RequestException 的子类（Timeout / ConnectionError / HTTPError）"
object:
  id: http.response
  name: HTTP 响应
  aliases: [接口, 请求, 超时, 重试, response]
action:
  id: inspect.check
  name: 判断
  aliases: [处理超时, 判断失败, 重试, 容错, retry]
targets: []
utterances:
  direct:
    - 请求超时怎么处理
    - 网络请求重试
    - 接口不稳定怎么容错
  questions:
    - requests 超时报什么异常
    - 怎么自动重试几次
    - 怎么区分超时和连接失败
  colloquial:
    - 网络不稳，请求老失败
    - 想让脚本失败了自己再试两次
  technical:
    - requests.exceptions
    - Timeout
    - ConnectionError
    - 指数退避
  short_queries:
    - 超时
    - 重试
    - 异常
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.8"
version_note: "requests 2.x 的异常层次稳定：RequestException 是总根"
sources:
  - requests 官方文档 异常
---

# 超时与重试

## 功能描述

输入地址 + 超时秒数，输出响应；失败时按异常类型分流，并可以重试有限次数。

## 推荐代码

```python
import time
import requests

def fetch(url: str, retries: int = 3):
    for i in range(retries):
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()      # 4xx/5xx 变异常
            return r.json()
        except requests.Timeout:
            print(f"第 {i+1} 次超时")
        except requests.ConnectionError:
            print(f"第 {i+1} 次连不上")
        except requests.HTTPError as exc:
            print("服务端返回错误:", exc)
            break                     # 4xx/5xx 重试没意义
        time.sleep(1 + i)             # 递增等待，别死磕
    return None

print(fetch("http://127.0.0.1:9/", retries=1))   # 演示：必然连不上，只试一次
```

## 语句解释

### requests.Timeout

超时（连接或读取超时）。**可以重试**。

### requests.ConnectionError

连不上（DNS 失败、被拒、网络断）。可以重试，但要递增等待。

### r.raise_for_status()

把 4xx/5xx 变成 `HTTPError`。**这是让状态码也走异常路径的关键一行**。

## 原理解释

**一句话：** 请求失败会抛不同类型的异常，你按类型决定「重试」还是「放弃」。

**执行逻辑：**

1. 发请求，等最多 `timeout` 秒
2. 连不上 → 抛 `ConnectionError`
3. 连上但超时没读完 → 抛 `Timeout`
4. 拿到了但状态码是 4xx/5xx → `raise_for_status()` 抛 `HTTPError`
5. 用 `except` 分流：网络问题重试，业务错误直接放弃

**机器层（可跳过）：** 重试不改变单次请求的耗时，只是把「可能失败」变成「多试几次」。

**边界（从逻辑推出来）：**

- 第 2、3 步属于「网络层临时故障」，重试有意义
- 第 4 步属于「服务端明确拒绝」，重试通常没用，反而加重对方负担
- 因为第 1 步有上限，所以重试必须自己写循环——`requests` 不自动重试
- 重试次数 × 超时时间 = 最坏等待时长，别设成 10 次 × 30 秒

## 注意事项

- 永远写 `timeout`，并**区分连接超时与读取超时**（可传元组）。
- 4xx/5xx 不要盲重试。
- 重试之间要有等待（1s、2s、4s 递增），别瞬间轰炸。
- 幂等的 GET 可以重试；POST 要小心重复提交。

## 使用场景

- 抓数据时应对偶发网络抖动。
- 调第三方接口做容错。
- 定时任务里避免一次失败就中断。
