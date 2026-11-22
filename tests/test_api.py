r"""api 层的测试：DTO 契约、后端适配、缺失数据容错。

这些测试**不碰 UI**，跑得很快；P1 之后 UI 测试另开文件。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from starport_dictionary.api.dto import EntryDTO, ImportHint, RelatedDTO
from starport_dictionary.api.local_backend import LocalKnowledgeBackend
from starport_dictionary.paths import packs_root

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def backend() -> LocalKnowledgeBackend:
    return LocalKnowledgeBackend(packs_root())


# ---------- 后端契约 ----------
def test_能加载全部条目(backend):
    stats = backend.stats()
    assert stats.entry_count >= 130
    assert stats.module_count >= 20
    assert stats.errors == ()


def test_搜索返回_dto(backend):
    resp = backend.search("判断文件后缀", limit=5)
    assert resp.query == "判断文件后缀"
    assert resp.backend == "local"
    assert 0 < len(resp.hits) <= 5
    best = resp.best
    assert best is not None
    assert best.entry_id.startswith("py.")
    assert best.title            # 标题要带出来，不能只有 id
    assert best.matched_terms    # 「凭什么命中」要有东西


def test_空查询返回空结果(backend):
    resp = backend.search("   ")
    assert resp.hits == ()
    assert resp.has_results is False


def test_limit_生效(backend):
    assert len(backend.search("文件", limit=3).hits) <= 3


def test_取条目并转成_dto(backend):
    entry = backend.get_entry("py.dict.get")
    assert entry is not None
    assert entry.title == "取字典里的值"
    assert entry.signature.startswith("d.get")
    assert entry.args and entry.args[0].name == "key"
    assert entry.returns


def test_取不存在的条目返回_none(backend):
    assert backend.get_entry("py.不存在.条目") is None


def test_检索不会抛异常(backend):
    """任何怪查询都不该让界面崩。"""
    for q in ["", "   ", "!!!", "a" * 500, "🙂", "文件后缀\x00"]:
        resp = backend.search(q)
        assert resp is not None


# ---------- DTO 展示逻辑 ----------
def test_内置能力不需要_import():
    dto = EntryDTO(id="x", title="t", description="d", language="python",
                   category_id="c", status="tested", origin="builtin")
    assert dto.import_hint.kind == "builtin"
    assert dto.import_hint.needs_import is False
    assert dto.origin_label == "内置能力"


def test_标准库要显示_import():
    dto = EntryDTO(id="x", title="t", description="d", language="python",
                   category_id="c", status="tested", origin="stdlib",
                   import_stmt="import os")
    assert dto.import_hint.needs_import is True
    assert dto.import_hint.statement == "import os"


def test_第三方要显示安装命令():
    dto = EntryDTO(id="x", title="t", description="d", language="python",
                   category_id="c", status="tested", origin="thirdparty",
                   import_stmt="import requests", install="pip install requests")
    hint = dto.import_hint
    assert hint.kind == "thirdparty"
    assert hint.install == "pip install requests"


def test_未标注层时如实说未知():
    dto = EntryDTO(id="x", title="t", description="d", language="python",
                   category_id="c", status="tested")
    assert dto.import_hint.kind == "unknown"
    assert dto.origin_label == "未标注"


def test_相关条目缺失时标记为不存在():
    assert RelatedDTO("py.x").exists is False
    assert RelatedDTO("py.x", "标题").exists is True


def test_真实条目的相关条目能带上标题(backend):
    entry = backend.get_entry("py.fs.check_extension")
    assert entry is not None
    assert entry.related
    # 至少有一个能解析出标题（其余的允许缺失）
    assert any(r.title for r in entry.related)


# ---------- ImportHint 直接构造 ----------
def test_import_hint_needs_import():
    assert ImportHint(kind="stdlib").needs_import is True
    assert ImportHint(kind="builtin").needs_import is False
