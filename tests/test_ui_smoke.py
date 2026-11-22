r"""UI 冒烟测试：不显示窗口（offscreen），只验证构造、切屏、搜索、反馈。

用 FakeBackend 注入，验证「界面不依赖真实检索实现」——这本身就是解耦的证据。
"""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QApplication

from starport_dictionary.api.dto import (
    ArgDTO,
    EntryDTO,
    HitDTO,
    ImportHint,
    LibraryStats,
    RelatedDTO,
    SearchResponse,
)
from starport_dictionary.ui.main_window import PAGE_DETAIL, PAGE_HOME, PAGE_RESULTS, MainWindow
from starport_dictionary.ui.store import FeedbackRecord, FeedbackStore, RecentStore


class FakeBackend:
    """最小实现：证明 UI 只认协议，不认真实检索。"""

    name = "fake"

    def __init__(self) -> None:
        self.entry = EntryDTO(
            id="py.fs.check_extension",
            title="判断文件后缀",
            description="看文件名最后一段是不是某后缀",
            language="python",
            category_id="programming.filesystem",
            status="tested",
            origin="stdlib",
            import_stmt="from pathlib import Path",
            module="pathlib",
            qualname="pathlib.Path.suffix",
            signature="Path(path).suffix.lower() == 目标后缀",
            returns="True/False",
            principle="一句话：切出最后一段后缀再比较。",
            code="from pathlib import Path\nprint(Path('a.py').suffix)",
            caveats="只比字符串。",
            scenario="批量筛文件。",
            args=(ArgDTO(name="path", required=True, accepts="文件路径"),),
            related=(RelatedDTO("py.fs.get_extension", "获取文件后缀"),
                     RelatedDTO("py.not.exist")),
        )

    def search(self, query: str, limit: int = 8) -> SearchResponse:
        if not (query or "").strip():
            return SearchResponse(query=query or "", backend=self.name)
        return SearchResponse(
            query=query,
            hits=(
                HitDTO("py.fs.check_extension", "判断文件后缀", 105, ("后缀",),
                       description="取最后一段后缀再比较", origin="stdlib"),
                HitDTO("py.fs.get_extension", "获取文件后缀", 38, ("后缀",),
                       description="返回带点的后缀字符串", origin="stdlib"),
                HitDTO("py.os.remove", "删除文件", 20, ("文件",),
                       description="把文件从磁盘移除", origin="stdlib"),
            ),
            backend=self.name,
        )

    def get_entry(self, entry_id: str):
        if entry_id == self.entry.id:
            return self.entry
        for hit in self.search("x", limit=8).hits:
            if hit.entry_id == entry_id:
                return EntryDTO(id=hit.entry_id, title=hit.title, description=hit.description,
                                language="python", category_id="c", status="tested",
                                origin=hit.origin, import_stmt="import os")
        return None

    def stats(self) -> LibraryStats:
        return LibraryStats(entry_count=137, module_count=26, pack_count=1)


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def win(app, tmp_path, monkeypatch):
    # 反馈/最近搜索写到临时目录，别污染真实数据
    monkeypatch.setattr("starport_dictionary.ui.main_window.FeedbackStore",
                        lambda: FeedbackStore(tmp_path / "fb.jsonl"))
    monkeypatch.setattr("starport_dictionary.ui.main_window.RecentStore",
                        lambda: RecentStore(tmp_path / "recent.json"))
    w = MainWindow(FakeBackend())
    yield w
    w.close()


def test_启动在首页(win):
    assert win.stack.currentIndex() == PAGE_HOME
    assert win.home.input.placeholderText() == "你想实现什么？"


def test_搜索后到结果页(win):
    win.do_search("判断文件后缀")
    assert win.stack.currentIndex() == PAGE_RESULTS
    assert win.results._shown_entry_id == "py.fs.check_extension"


def test_空搜索不动(win):
    win.do_search("   ")
    assert win.stack.currentIndex() == PAGE_HOME


def test_点条目进详情(win):
    win.do_search("判断文件后缀")
    win.open_entry("py.fs.check_extension")
    assert win.stack.currentIndex() == PAGE_DETAIL
    assert win.detail.content.layout().count() > 4


def test_Esc_逐级返回(win):
    win.do_search("判断文件后缀")
    win.open_entry("py.fs.check_extension")
    win.on_escape()
    assert win.stack.currentIndex() == PAGE_RESULTS
    win.on_escape()
    assert win.stack.currentIndex() == PAGE_HOME


def test_反馈写进文件(win):
    win.do_search("判断文件后缀")
    win.on_feedback("ok")
    data = win.feedback.load_all()
    assert len(data) == 1
    rec = data[0]
    assert rec["query"] == "判断文件后缀"
    assert rec["verdict"] == "ok"
    assert rec["best_entry_id"] == "py.fs.check_extension"
    assert rec["candidates"]      # 候选也记下来了


def test_最近搜索会记(win):
    win.do_search("判断文件后缀")
    assert win.recent.load()[0] == "判断文件后缀"


def test_没有结果也不崩(win):
    win.backend = FakeBackend()
    win.results.show_response(SearchResponse(query="不存在的东西", backend="fake"))
    assert win.stack.currentIndex() == PAGE_HOME     # 只是渲染，不切屏


def test_详情页渲染缺字段条目(app):
    """origin 缺失、args 为空、related 缺失都该能显示。"""
    from starport_dictionary.ui.views import DetailView

    d = DetailView()
    d.show_entry(
        EntryDTO(id="py.x", title="空条目", description="什么都没有", language="python",
                 category_id="c", status="draft")
    )
    assert d.content.layout().count() > 0
    hint = EntryDTO(id="x", title="t", description="d", language="python",
                    category_id="c", status="draft").import_hint
    assert isinstance(hint, ImportHint)
    d.deleteLater()


# ---------- 存储层 ----------
def test_反馈存储追加与坏行容错(tmp_path):
    store = FeedbackStore(tmp_path / "fb.jsonl")
    store.add(FeedbackRecord(query="a", verdict="ok"))
    store.add(FeedbackRecord(query="b", verdict="bad"))
    (tmp_path / "fb.jsonl").open("a", encoding="utf-8").write("这不是 json\n")
    assert store.count() == 3
    assert len(store.load_all()) == 2       # 坏行被跳过


def test_最近搜索去重且限长(tmp_path):
    store = RecentStore(tmp_path / "r.json", limit=3)
    for q in ["a", "b", "c", "d"]:
        store.add(q)
    assert store.load() == ["d", "c", "b"]
    store.add("b")
    assert store.load() == ["b", "d", "c"]
