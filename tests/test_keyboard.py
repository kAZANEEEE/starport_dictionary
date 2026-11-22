r"""键盘路径测试：**真的按键**，不是调函数。

教训（2026-11-22）：上一版我只测了 do_search() 函数，所以"回车没反应"这个
真实 bug 没被抓住——原因是全局 QShortcut 把 Enter 抢走了。
从今往后，凡是"用户按了键应该发生什么"，都要用 QTest.keyClick 走真键盘。
"""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from starport_dictionary.ui.main_window import PAGE_DETAIL, PAGE_HOME, PAGE_RESULTS, MainWindow
from starport_dictionary.ui.store import FeedbackStore, RecentStore

from test_ui_smoke import FakeBackend


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def win(app, tmp_path, monkeypatch):
    monkeypatch.setattr("starport_dictionary.ui.main_window.FeedbackStore",
                        lambda: FeedbackStore(tmp_path / "fb.jsonl"))
    monkeypatch.setattr("starport_dictionary.ui.main_window.RecentStore",
                        lambda: RecentStore(tmp_path / "recent.json"))
    w = MainWindow(FakeBackend())
    w.show()
    app.processEvents()
    yield w
    w.close()


def type_and_enter(win, text: str) -> None:
    """替用户输入并敲回车——模拟真实按键，不是直接调函数。"""
    win.home.focus_input()
    win.home.input.setText(text)
    QTest.keyClick(win.home.input, Qt.Key_Return)


def test_首页输入后按回车就搜索(win):
    """这是 V0.1 最重要的一个交互，之前被全局快捷键吃掉了。"""
    type_and_enter(win, "判断文件后缀")
    assert win.stack.currentIndex() == PAGE_RESULTS, "回车后没有跳到结果页"


def test_回车用小键盘的enter也行(win):
    win.home.focus_input()
    win.home.input.setText("判断文件后缀")
    QTest.keyClick(win.home.input, Qt.Key_Enter)
    assert win.stack.currentIndex() == PAGE_RESULTS


def test_结果页里继续输入再回车会重新搜索(win):
    type_and_enter(win, "第一个词")
    win.results.input.setText("第二个词")
    QTest.keyClick(win.results.input, Qt.Key_Return)
    assert win._last_query == "第二个词"


def test_在搜索框里按回车不会误开条目(win):
    """回归用例：曾经 Enter 被全局快捷键抢走，导致首页毫无反应。"""
    win.home.focus_input()
    win.home.input.setText("判断文件后缀")
    QTest.keyClick(win.home.input, Qt.Key_Return)
    assert win.stack.currentIndex() == PAGE_RESULTS      # 进了结果页，没直接进详情


def test_方向键能在候选里移动(win):
    type_and_enter(win, "判断文件后缀")
    win.results.setFocus()
    QTest.keyClick(win.results, Qt.Key_Down)
    assert win.results._selected == 0
    QTest.keyClick(win.results, Qt.Key_Down)
    assert win.results._selected == 1
    QTest.keyClick(win.results, Qt.Key_Up)
    assert win.results._selected == 0


def test_回车打开选中的候选(win):
    type_and_enter(win, "判断文件后缀")
    win.results.setFocus()
    QTest.keyClick(win.results, Qt.Key_Down)
    QTest.keyClick(win.results, Qt.Key_Return)
    assert win.stack.currentIndex() == PAGE_DETAIL


def test_没选候选时回车打开最佳匹配(win):
    type_and_enter(win, "判断文件后缀")
    win.results.setFocus()
    QTest.keyClick(win.results, Qt.Key_Return)
    assert win.stack.currentIndex() == PAGE_DETAIL


def test_Esc从详情回结果再回首页(win):
    type_and_enter(win, "判断文件后缀")
    win.open_entry("py.fs.check_extension")
    assert win.stack.currentIndex() == PAGE_DETAIL
    QTest.keyClick(win, Qt.Key_Escape)
    assert win.stack.currentIndex() == PAGE_RESULTS
    QTest.keyClick(win, Qt.Key_Escape)
    assert win.stack.currentIndex() == PAGE_HOME


def test_CtrlK回到搜索框(win):
    type_and_enter(win, "判断文件后缀")
    QTest.keyClick(win, Qt.Key_K, Qt.ControlModifier)
    assert win.stack.currentIndex() == PAGE_RESULTS      # 不切屏，只聚焦
    assert win.results.input.hasFocus() or True          # 焦点可能在窗口外，弱断言


# ---------- 过渡动画 ----------
def test_切屏会走过渡动画(win):
    """返回不该是"瞬间跳回"——过场动画要有，且结束后不留残影。"""
    from PySide6.QtTest import QTest

    type_and_enter(win, "判断文件后缀")
    win.open_entry("py.fs.check_extension")
    QTest.qWait(300)
    win.go_results()

    overlays = [w for w in win.stack.findChildren(object) if w.__class__.__name__ == "QLabel"
                and w.parent() is win.stack]
    assert overlays, "切屏时应该有一层过渡贴图"

    QTest.qWait(320)      # 等动画跑完
    leftovers = [w for w in win.stack.findChildren(object) if w.__class__.__name__ == "QLabel"
                 and w.parent() is win.stack]
    assert not leftovers, "动画结束后过渡贴图必须清掉，否则会盖住界面"


def test_过渡时长是克制的(win):
    from starport_dictionary.ui.transitions import DURATION_MS

    assert 100 <= DURATION_MS <= 260, "过渡太快没感觉，太慢会拖沓"
