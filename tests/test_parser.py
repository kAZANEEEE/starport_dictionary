r"""解析器 + 加载器的测试（第二版：YAML 头、受控词表、严格字段）。"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from starport_dictionary.knowledge.loader import load_pack
from starport_dictionary.knowledge.parser import EntryFormatError, parse_entry_file

ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "knowledge-packs" / "python-core"
ENTRY = PACK_DIR / "entries" / "py.fs.check_extension.md"


def write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "e.md"
    p.write_text(textwrap.dedent(body), encoding="utf-8")
    return p


GOOD_HEAD = """\
---
id: py.x.demo
title: 演示条目
language: python
category_id: programming.basics
object:
  id: file.extension
  name: 文件后缀
  aliases: [后缀]
action:
  id: inspect.check
  name: 判断
  aliases: [检查]
utterances:
  direct: [判断后缀, 检查后缀]
  questions: [怎么判断后缀, 如何检查后缀]
  colloquial: [看看是什么后缀, 这个文件是什么格式]
  short_queries: [后缀, 扩展名, suffix]
status: draft
---

## 功能描述
有
## 推荐代码
```python
pass
```
## 语句解释
### pass
什么都不做。
## 原理解释
有
## 注意事项
有
## 使用场景
有
"""


def test_解析真实条目_字段对齐():
    e = parse_entry_file(ENTRY)
    assert e.id == "py.fs.check_extension"
    assert e.obj.id == "file.extension"
    assert e.action.id == "inspect.check"
    assert "后缀" in e.obj.aliases
    assert e.min_version == "3.10"
    assert ".py" in e.targets
    assert e.ambiguity and e.ambiguity[0].candidate_ids == ("py.fs.real_type",)
    assert ".py" in e.code


def test_索引词不含utterance():
    """这条是整个设计的命门：原话不能进索引，否则测试恒真。

    注意不能拿 title 去断言——title 本身就是一句 direct 说法，
    真正要拦的是那些「只会这么说」的口语。
    """
    e = parse_entry_file(ENTRY)
    terms = " ".join(e.index_terms())
    assert "我想知道文件名最后面是什么" not in terms
    assert "这个文件是什么格式" not in terms
    assert "后缀" in terms                      # object 别名可以进
    assert "file.extension" in e.tags_text()    # id 也在


def test_未知顶层字段要报错(tmp_path):
    p = write(tmp_path, GOOD_HEAD.replace("status: draft", "status: draft\nwhatever: 1"))
    with pytest.raises(EntryFormatError) as exc:
        parse_entry_file(p)
    assert "未定义字段" in str(exc.value)


def test_对象id不在词表要报错(tmp_path):
    p = write(tmp_path, GOOD_HEAD.replace("id: file.extension", "id: file.ext"))
    with pytest.raises(EntryFormatError) as exc:
        parse_entry_file(p)
    assert "不在受控词表" in str(exc.value)


def test_写了tested就必须有min_version(tmp_path):
    p = write(tmp_path, GOOD_HEAD.replace("status: draft", 'status: tested\ntested_versions: ["3.12"]'))
    with pytest.raises(EntryFormatError) as exc:
        parse_entry_file(p)
    assert "min_version" in str(exc.value)


def test_缺必需utterance类别要报错(tmp_path):
    p = write(
        tmp_path,
        GOOD_HEAD.replace("  short_queries: [后缀, 扩展名, suffix]\n", ""),
    )
    with pytest.raises(EntryFormatError) as exc:
        parse_entry_file(p)
    assert "缺类别" in str(exc.value)


def test_缺正文小节要报错(tmp_path):
    broken = GOOD_HEAD.split("## 注意事项")[0]
    p = write(tmp_path, broken)
    with pytest.raises(EntryFormatError) as exc:
        parse_entry_file(p)
    assert "缺小节" in str(exc.value)


def test_整个知识包能读出来():
    pack = load_pack(PACK_DIR)
    assert pack.id == "lang.python.core"
    assert len(pack.entries) >= 2
    assert pack.errors == ()
    ids = {e.id for e in pack.entries}
    assert "py.fs.check_extension" in ids
    assert "py.list.dedupe" in ids
