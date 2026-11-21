---
id: py.hash.digest
title: 计算文件哈希
description: 算文件的 MD5/SHA256，用来校验是否被改过
language: python
category_id: programming.filesystem

object:
  id: hash.digest
  name: 哈希值
  aliases: [哈希, 摘要, 校验值, 指纹, md5, sha256, hash]

action:
  id: get.obtain
  name: 获取
  aliases: [计算, 算出, 取值, 生成, 算, compute]

targets: []

utterances:
  direct:
    - 计算文件哈希
    - 算文件的 md5
    - 获取文件的 sha256
    - 校验文件有没有被改过
  questions:
    - 怎么算一个文件的哈希值
    - 如何比较两个文件是否相同
    - Python 怎么用 sha256 校验文件
    - 大文件怎么算哈希不爆内存
  colloquial:
    - 想确认下载的文件没坏
    - 这个文件是不是被改过，怎么验证
    - 两个文件看着一样，其实一样吗
  goal_based:
    - 下载后校验完整性
    - 给文件生成指纹做去重
  technical:
    - hashlib md5
    - hashlib sha256
    - hexdigest
    - file checksum python
  short_queries:
    - 哈希
    - md5
    - sha256
    - 校验

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: hashlib 各算法接口稳定；md5/sha1 在某些 FIPS 环境下可能被禁用
sources:
  - Python 官方文档 hashlib
---

# 计算文件哈希

## 功能描述

算文件的指纹（MD5 或 SHA256），用来判断内容是否一致、有没有被改动。

## 推荐代码

```python
import hashlib
from pathlib import Path

# 演示用：先造一个文件，实际使用时删掉这一行
Path("data.bin").write_bytes(b"hello starport")

def file_hash(path, algo="sha256") -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

print(file_hash("data.bin"))
print(file_hash("data.bin", "md5"))
```

## 语句解释

### hashlib.new(algo)

按名字创建哈希对象，`sha256` / `md5` / `sha1` 都行。比 `hashlib.sha256()` 灵活，因为算法名可以是变量。

### open(path, "rb")

**必须二进制读**。按文本读会做编码转换，算出来的哈希和真实内容不一致。

### iter(lambda: f.read(1MB), b"")

每次读 1 MB，读到空字节就停。这样大文件也不会一次吃满内存。

### .hexdigest()

返回十六进制字符串，方便打印和比较。

## 原理解释

哈希把任意长度的内容压成固定长度的指纹：内容变一个字节，指纹就完全不同。
所以“算两份内容的哈希、比字符串是否相等”就等于“比内容是否相同”，
但只需要传 64 个字符，比逐字节比较省事（尤其跨网络比较时）。

哈希是单向的：从指纹反推不出原文。**但它不能防伪造**——能被用来校验“是否被改动”，
不能用来证明“来源可信”（那需要签名）。

## 注意事项

- 文件读取必须 `"rb"`，文本模式会改写字节。
- 大文件要分块读，别 `f.read()` 一把梭。
- MD5/SHA1 已不抗碰撞，只用于“校验传输完整性”够用，别用于密码存储。
- 用哈希判断文件是否相同时，先比大小更省时间：大小不同直接不同。
- 文件夹没有哈希，要自己把子文件哈希拼起来再算一次。

## 使用场景

- 下载完校验文件完整性（对比发布方给的哈希）。
- 去重：内容相同但文件名不同的文件。
- 构建缓存：内容没变就跳过重复处理。
