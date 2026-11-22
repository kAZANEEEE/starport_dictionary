---
id: py.hash.digest
title: 计算文件哈希
description: 算文件的 MD5/SHA256，用来校验是否被改过
language: python
category_id: programming.filesystem
module: hashlib
origin: stdlib
import: "import hashlib"
qualname: "hashlib.sha256()"

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

**一句话：** 把文件内容当成一大串数字，用固定公式搅拌出一个短指纹。

**执行逻辑：**

1. 建一个哈希计算器（先选算法，如 sha256）
2. 读一块字节喂进去，内部把它搅拌进当前状态
3. 继续喂下一块，直到文件读完
4. 结束，得到固定长度的结果，再转成十六进制文本
5. 两份内容只要有一个字节不同，第 4 步的结果就几乎必然不同

**机器层（可跳过）：** 分块喂入是为了不把整个文件读进内存，与一次读完结果相同。

**边界（从逻辑推出来）：**

- 第 2 步喂的是**字节**，所以必须二进制读；按文本读会做编码转换，指纹就不是原始内容的了
- 第 3 步可以分块，所以大文件也能算，代价只是多几次读盘
- 第 5 步的「几乎必然不同」是概率保证，理论上存在碰撞；MD5/SHA1 已经被有意构造出碰撞
- 指纹只能证明「内容变了没变」，不能证明「内容是谁给的」——那是签名的事
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
