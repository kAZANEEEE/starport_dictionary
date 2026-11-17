+++
id = "py.fs.check_extension"
title = "判断文件后缀"
language = "python"
category_id = "programming.filesystem"
status = "tested"
aliases = ["判断文件扩展名", "检查是不是py文件", "怎么判断文件类型", "获取文件后缀名"]
tags = ["python", "pathlib", "file", "suffix", "extension"]
scenario = "只想处理某一种格式的文件时，比如遍历时只挑 .py，或者判断用户上传的是不是 .jpg"
tested_versions = ["3.10", "3.11", "3.12", "3.13", "3.14"]
related_ids = ["py.fs.get_suffixes", "py.fs.traverse_directory"]
sources = ["Python 官方文档 pathlib.Path.suffix", "Python 官方文档 PurePath.name"]
+++

## 代码

```python
from pathlib import Path

file_path = Path("example.PY")

if file_path.suffix.lower() == ".py":
    print("这是一个 Python 文件")
else:
    print("不是 Python 文件")
```

## 功能描述

取出文件名的最后一个后缀，统一转成小写再比较，判断它是不是 `.py` 文件。

## 逐句解释

- `from pathlib import Path`：从标准库导入 `Path`，后面所有路径操作都走它，不用拼字符串。
- `Path("example.PY")`：把字符串变成路径对象。这一步不检查文件是否存在，纯粹是解析字符串。
- `.suffix`：取路径最后一个后缀，返回值带点号，比如 `".PY"`。没有后缀时返回空字符串。
- `.lower()`：把 `".PY"` 转成 `".py"`。Windows 上文件名大小写不敏感，不转的话 `.PY` 会被误判成「不是 Python 文件」。
- `== ".py"`：直接比较字符串。

## 原理解释

`suffix` 的做法是：拿到路径最后一段（`name`），从**最后一个点**往后切。

所以：

| 路径 | `.suffix` |
|---|---|
| `a/b.py` | `.py` |
| `a/archive.tar.gz` | `.gz` |
| `a/Makefile` | `""` |
| `a/.bashrc` | `""` |

`.bashrc` 那种以点开头的文件会被当成「没有后缀」，因为 `pathlib` 认为开头那个点是隐藏文件的标记，不是后缀分隔符。

## 注意事项

- **只取最后一个后缀**，`archive.tar.gz` 得到的是 `.gz`。要全部后缀用 `.suffixes`。
- **后缀不代表真实类型**。把 `a.txt` 改名成 `a.jpg`，`suffix` 照样返回 `.jpg`。真想判断格式得读文件头（`imghdr` 已废弃，可用 `python-magic` 或自己读前几个字节）。
- **大小写看需求**。要区分 `.PY` 和 `.py` 就别调 `.lower()`。
- **别用 `os.path.splitext` 混着写**，两种写法混在一个项目里容易出意外，统一用 `pathlib`。
- 路径对象没有后缀时 `.suffix` 是空字符串，`if file_path.suffix == ".py"` 不会抛异常，但也要留意 `""` 这种边界。
