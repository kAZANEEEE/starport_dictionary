r"""解析器的测试。

判据只有一条：拿真实的那条知识条目跑一遍，字段能对上。
故意不 mock 文件——这个解析器就是要吃真文件的，mock 起来反而测不到格式。
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from starport_dictionary.knowledge.parser import EntryFormatError, parse_entry_file

ROOT = Path(__file__).resolve().parents[1]
REAL_ENTRY = ROOT / "knowledge-packs" / "python-core" / "entries" / "py.fs.check_extension.md"


def write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "entry.md"
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


def test_解析真实条目(tmp_path):
    entry = parse_entry_file(REAL_ENTRY)

    assert entry.id == "py.fs.check_extension"
    assert entry.title == "判断文件后缀"
    assert entry.language == "python"
    assert entry.category_id == "programming.filesystem"
    assert entry.status == "tested"
    assert "pathlib" in entry.tags
    assert ".py" in entry.code
    assert "pathlib" in entry.code
    assert entry.principle  # 原理解释不能是空的
    assert entry.caveats


def test_可检索文本不包含代码(tmp_path):
    entry = parse_entry_file(REAL_ENTRY)
    text = entry.searchable_text()
    assert "判断文件后缀" in text
    assert "pathlib" in text          # tags 里的词在
    assert "import" not in text       # 代码不进来


def test_缺字段要报错(tmp_path):
    p = write(
        tmp_path,
        """\
        +++
        id = "py.x.demo"
        title = "缺一堆字段"
        +++

        ## 代码
        ```python
        pass
        ```
        ## 功能描述
        有
        ## 逐句解释
        有
        ## 原理解释
        有
        ## 注意事项
        有
        """,
    )
    with pytest.raises(EntryFormatError) as exc:
        parse_entry_file(p)
    assert "缺字段" in str(exc.value)


def test_缺小节要报错(tmp_path):
    p = write(
        tmp_path,
        """\
        +++
        id = "py.x.demo"
        title = "缺一节"
        language = "python"
        category_id = "programming.basics"
        status = "draft"
        scenario = "演示"
        aliases = ["测试"]
        tags = ["t"]
        tested_versions = ["3.12"]
        +++

        ## 代码
        ```python
        pass
        ```
        ## 功能描述
        有
        """,
    )
    with pytest.raises(EntryFormatError) as exc:
        parse_entry_file(p)
    assert "缺小节" in str(exc.value)


def test_id格式不对要报错(tmp_path):
    p = write(
        tmp_path,
        """\
        +++
        id = "BadID"
        title = "id 不合法"
        language = "python"
        category_id = "programming.basics"
        status = "draft"
        scenario = "演示"
        aliases = ["测试"]
        tags = ["t"]
        tested_versions = ["3.12"]
        +++

        ## 代码
        ```python
        pass
        ```
        ## 功能描述
        有
        ## 逐句解释
        有
        ## 原理解释
        有
        ## 注意事项
        有
        """,
    )
    with pytest.raises(EntryFormatError) as exc:
        parse_entry_file(p)
    assert "不符合格式" in str(exc.value)
