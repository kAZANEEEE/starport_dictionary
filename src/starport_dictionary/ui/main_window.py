r"""主窗口：单窗口三屏 + 快捷键 + 后端调用。

这一层是**唯一**同时认识 UI 和 backend 的地方——页面只发信号，后端只被这里调用。
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QLabel, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from starport_dictionary.api.backend import SearchBackend
from starport_dictionary.ui.store import FeedbackRecord, FeedbackStore, RecentStore
from starport_dictionary.ui.theme import APP_NAME, APP_VERSION, StarfieldBackground, icon_path
from starport_dictionary.ui.transitions import ScreenTransitions
from starport_dictionary.ui.views import DetailView, HomeView, ResultsView

PAGE_HOME, PAGE_RESULTS, PAGE_DETAIL = 0, 1, 2


class MainWindow(QMainWindow):
    def __init__(self, backend: SearchBackend, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.backend = backend
        self.feedback = FeedbackStore()
        self.recent = RecentStore()
        self._last_query = ""

        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        icon = icon_path()
        if icon.is_file():
            self.setWindowIcon(QIcon(str(icon)))
        self.resize(1080, 760)
        self.setMinimumSize(880, 620)

        # 背景层（星点）+ 前景容器
        self._bg = StarfieldBackground(self)
        central = QWidget(self)
        central.setObjectName("Root")

        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget(central)
        self.home = HomeView(self.stack)
        self.results = ResultsView(self.stack)
        self.detail = DetailView(self.stack)
        self.stack.addWidget(self.home)
        self.stack.addWidget(self.results)
        self.stack.addWidget(self.detail)

        # 内容左右留白（搜索框在中间才像"中心"）
        holder = QWidget(central)
        hl = QVBoxLayout(holder)
        hl.setContentsMargins(56, 28, 56, 28)
        hl.addWidget(self.stack)
        outer.addWidget(holder)
        self.setCentralWidget(central)

        # 状态栏
        self.status = QLabel("", self)
        self.status.setObjectName("Status")
        self.statusBar().addPermanentWidget(self.status)
        self.statusBar().setStyleSheet("QStatusBar{background:#0b1020;color:#6f78a0;}")

        # 接线
        self.home.submitted.connect(self.do_search)
        self.results.back_requested.connect(self.go_home)
        self.results.search_again.connect(self.do_search)
        self.results.entry_chosen.connect(self.open_entry)
        self.results.feedback_given.connect(self.on_feedback)
        self.detail.back_requested.connect(self.go_results)
        self.detail.entry_chosen.connect(self.open_entry)

        # 快捷键
        QShortcut(QKeySequence("Ctrl+K"), self, self.focus_search)
        QShortcut(QKeySequence("Escape"), self, self.on_escape)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)

        self.transitions = ScreenTransitions(self.stack)

        self.home.set_recent(self.recent.load())
        self._update_status()
        self.home.focus_input()

    # ---------- 布局事件：背景铺满 ----------
    def resizeEvent(self, event) -> None:  # noqa: N802
        self._bg.setGeometry(self.rect())
        super().resizeEvent(event)

    # ---------- 状态栏 ----------
    def _update_status(self) -> None:
        try:
            stats = self.backend.stats()
            self.status.setText(
                f"知识库 {stats.entry_count} 条 · {stats.module_count} 个模块 · "
                f"反馈 {self.feedback.count()} 条 · {APP_NAME} {APP_VERSION}"
            )
        except Exception:
            self.status.setText(f"{APP_NAME} {APP_VERSION}")

    # ---------- 导航 ----------
    def focus_search(self) -> None:
        if self.stack.currentIndex() == PAGE_HOME:
            self.home.focus_input()
        else:
            self.results.input.setFocus()
            self.results.input.selectAll()

    def go_home(self) -> None:
        self.transitions.goto(PAGE_HOME, forward=False)
        self.transitions = ScreenTransitions(self.stack)

        self.home.set_recent(self.recent.load())
        self.home.focus_input()

    def go_results(self) -> None:
        self.transitions.goto(PAGE_RESULTS, forward=False)

    def on_escape(self) -> None:
        idx = self.stack.currentIndex()
        if idx == PAGE_DETAIL:
            self.go_results()
        elif idx == PAGE_RESULTS:
            self.go_home()

    # ---------- 业务 ----------
    def do_search(self, query: str) -> None:
        q = (query or "").strip()
        if not q:
            return
        self._last_query = q
        resp = self.backend.search(q, limit=8)
        self.results.show_response(resp)
        self.transitions.goto(PAGE_RESULTS, forward=True)
        self.recent.add(q)
        self._update_status()

    def open_entry(self, entry_id: str) -> None:
        entry = self.backend.get_entry(entry_id)
        if entry is None:
            self.status.setText(f"条目 {entry_id} 未找到")
            return
        self.detail.show_entry(entry)
        self.transitions.goto(PAGE_DETAIL, forward=True)

    def on_feedback(self, verdict: str) -> None:
        resp = getattr(self.results, "_response", None)
        if resp is None or not resp.has_results:
            return
        best = resp.best
        record = FeedbackRecord(
            query=self._last_query,
            verdict=verdict,
            best_entry_id=best.entry_id,
            best_title=best.title,
            candidates=[h.entry_id for h in resp.hits],
            backend=resp.backend,
            app_version=APP_VERSION,
        )
        ok = self.feedback.add(record)
        self.status.setText("已记录反馈，谢谢" if ok else "反馈写入失败（不影响使用）")
        self._update_status()
