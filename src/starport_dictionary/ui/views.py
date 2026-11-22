r"""三个页面（冷纸工程手册版）。

2026-11-22 重做：
- 首页不再居中 Hero + 彩色胶囊：改成左对齐编辑式排版，左"试这些"、右"ID 读法"
- 结果页：最佳匹配是一条带黄铜左线的区块，其余是细线分隔的行
- 详情页：区块之间用线和小标签分隔，不套圆角盒子
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from starport_dictionary.api.dto import EntryDTO, SearchResponse
from starport_dictionary.ui.theme import FS_HERO, icon_path
from starport_dictionary.ui.widgets import (
    Badge,
    Wordmark,
    CandidateRow,
    ClickableFrame,
    CodeBlock,
    Rule,
    Section,
    first_sentence,
    md_to_html,
    mono_label,
)

EXAMPLES = [
    "判断一个文件的后缀名",
    "把文件内容读取成字符串",
    "删除列表中的重复元素",
    "获取字典中某个键对应的值",
]

ID_LEGEND = [
    ("py.dict.get", "BUILTIN", "dict 的 get 用法，不用 import"),
    ("py.os.getcwd", "STDLIB", "os 模块里的 getcwd，import os"),
    ("py.json.loads", "STDLIB", "json 模块里的 loads，import json"),
]


# ================= 首页 =================
class IdLegend(QWidget):
    """ID 读法：一张表，不是一张卡片。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        head = QHBoxLayout()
        head.addWidget(mono_label("ENTRY ID / 条目 ID 怎么读", self))
        head.addStretch(1)
        lay.addLayout(head)

        formula = QLabel("py . 库/板块 . 具体用法", self)
        formula.setObjectName("Mono")
        lay.addWidget(formula)

        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(7)
        for r, (ident, level, meaning) in enumerate(ID_LEGEND):
            idl = QLabel(ident, self)
            idl.setObjectName("Mono")
            grid.addWidget(idl, r, 0)
            grid.addWidget(Badge(level, "builtin" if level == "BUILTIN" else "stdlib", self), r, 1)
            ml = QLabel(meaning, self)
            ml.setObjectName("Muted")
            ml.setWordWrap(True)
            grid.addWidget(ml, r, 2)
        grid.setColumnStretch(2, 1)
        lay.addLayout(grid)

        note = QLabel(
            "第三段是「用法名」，不一定等于模块名；准确全名看详情页顶部的等宽徽章。",
            self,
        )
        note.setObjectName("Hint")
        note.setWordWrap(True)
        lay.addWidget(note)


class HomeView(QWidget):
    submitted = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Home")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 18, 0, 8)
        root.setSpacing(0)

        # —— 顶行：图标 + 品牌 + 右侧统计 ——
        top = QHBoxLayout()
        top.setSpacing(10)
        top.addWidget(Wordmark(14, self))
        top.addSpacing(4)
        brand = QLabel("STARPORT DICTIONARY", self)
        brand.setObjectName("Brand")
        top.addWidget(brand)
        top.addStretch(1)
        self.stats = QLabel("", self)
        self.stats.setObjectName("Mono")
        top.addWidget(self.stats)
        root.addLayout(top)
        root.addSpacing(46)

        # —— 主张（左对齐，不是居中 Hero）——
        hero = QLabel("描述你想实现什么", self)
        hero.setObjectName("Hero")
        root.addWidget(hero)

        tagline = QLabel("不用先知道函数名。用你自己的话说，它给你能直接用的写法。", self)
        tagline.setObjectName("Tagline")
        tagline.setContentsMargins(0, 6, 0, 0)
        root.addWidget(tagline)
        root.addSpacing(22)

        # —— 搜索框（全宽）——
        self.input = QLineEdit(self)
        self.input.setObjectName("SearchInput")
        self.input.setPlaceholderText("例如：删除列表里重复的")
        self.input.setClearButtonEnabled(True)
        self.input.returnPressed.connect(self._emit)
        root.addWidget(self.input)

        # —— 刻度线 + 键位提示 ——
        root.addSpacing(8)
        self.ruler = Rule(self)
        root.addWidget(self.ruler)
        hint = QLabel("ENTER 搜索     CTRL+K 回搜索框     ESC 返回     ↑↓ 选候选", self)
        hint.setObjectName("Hint")
        root.addWidget(hint)
        root.addSpacing(30)

        # —— 两栏：左"试这些" / 右"ID 读法" ——
        cols = QHBoxLayout()
        cols.setSpacing(56)

        left = QVBoxLayout()
        left.setSpacing(2)
        left.addWidget(mono_label("TRY / 试这些", self))
        left.addSpacing(6)
        self.example_box = QVBoxLayout()
        self.example_box.setSpacing(0)
        for i, text in enumerate(EXAMPLES, start=1):
            b = QPushButton(f"{i:02d}   {text}", self)
            b.setObjectName("ExampleRow")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, t=text: self._submit(t))
            self.example_box.addWidget(b)
        left.addLayout(self.example_box)

        # 最近搜索
        self.recent_box = QWidget(self)
        self.recent_lay = QVBoxLayout(self.recent_box)
        self.recent_lay.setContentsMargins(0, 12, 0, 0)
        self.recent_lay.setSpacing(2)
        self.recent_box.setVisible(False)
        left.addWidget(self.recent_box)
        left.addStretch(1)

        right = QVBoxLayout()
        right.setSpacing(0)
        self.legend = IdLegend(self)
        right.addWidget(self.legend)
        right.addStretch(1)

        cols.addLayout(left, 5)
        cols.addLayout(right, 6)
        root.addLayout(cols)
        root.addStretch(1)

        root.addWidget(Rule(self))
        steps = QLabel("问一句  →  看候选  →  读原理  →  抄代码", self)
        steps.setObjectName("Steps")
        steps.setContentsMargins(0, 8, 0, 6)
        root.addWidget(steps)

        self.status = QLabel("", self)
        self.status.setObjectName("Status")
        root.addWidget(self.status)

    # ---- 行为 ----
    def _emit(self) -> None:
        self._submit(self.input.text())

    def _submit(self, text: str) -> None:
        q = (text or "").strip()
        if q:
            self.submitted.emit(q)

    def focus_input(self) -> None:
        self.input.setFocus()
        self.input.selectAll()

    def set_stats(self, text: str) -> None:
        self.stats.setText(text)

    def set_recent(self, items: list[str]) -> None:
        while self.recent_lay.count():
            item = self.recent_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        if not items:
            self.recent_box.setVisible(False)
            return
        self.recent_lay.addWidget(mono_label("RECENT / 最近", self.recent_box))
        for q in items:
            b = QPushButton(q, self.recent_box)
            b.setObjectName("Chip")
            b.setCursor(Qt.PointingHandCursor)
            b.setContentsMargins(30, 0, 0, 0)      # 和 01/02 的编号列对齐
            b.clicked.connect(lambda _=False, t=q: self._submit(t))
            self.recent_lay.addWidget(b)
        self.recent_box.setVisible(True)


# ================= 最佳匹配 =================
class BestCard(ClickableFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("BestCard")


# ================= 结果页 =================
class ResultsView(QWidget):
    entry_chosen = Signal(str)
    feedback_given = Signal(str)
    back_requested = Signal()
    search_again = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._response: SearchResponse | None = None
        self._shown_entry_id = ""
        self._rows: list[CandidateRow] = []
        self._selected = -1
        self.setFocusPolicy(Qt.StrongFocus)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 10, 0, 6)
        root.setSpacing(0)

        top = QHBoxLayout()
        top.setSpacing(12)
        back = QPushButton("← 返回", self)
        back.setObjectName("Ghost")
        back.setCursor(Qt.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)

        self.input = QLineEdit(self)
        self.input.setObjectName("SearchSmall")
        self.input.setPlaceholderText("换个说法，ENTER 重新搜索")
        self.input.returnPressed.connect(lambda: self.search_again.emit(self.input.text().strip()))
        self.input.installEventFilter(self)
        top.addWidget(self.input, 1)
        root.addLayout(top)
        root.addSpacing(12)

        self.meta = QLabel("", self)
        self.meta.setObjectName("Label")
        root.addWidget(self.meta)
        root.addSpacing(10)

        self.best_card = BestCard(self)
        self.best_card.clicked.connect(lambda: self.entry_chosen.emit(self._shown_entry_id))
        self.best_lay = QVBoxLayout(self.best_card)
        self.best_lay.setContentsMargins(16, 14, 16, 14)
        self.best_lay.setSpacing(9)
        root.addWidget(self.best_card)
        root.addSpacing(18)

        self.list_scroll = QScrollArea(self)
        self.list_scroll.setWidgetResizable(True)
        self.list_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_scroll.setFrameShape(QFrame.NoFrame)
        list_host = QWidget(self.list_scroll)
        host_lay = QVBoxLayout(list_host)
        host_lay.setContentsMargins(0, 0, 8, 0)
        host_lay.setSpacing(0)

        self.others_title = mono_label("OTHERS / 其他相关", list_host)
        host_lay.addWidget(self.others_title)
        host_lay.addSpacing(2)

        self.others_box = QVBoxLayout()
        self.others_box.setSpacing(0)
        host_lay.addLayout(self.others_box)
        host_lay.addStretch(1)

        self.list_scroll.setWidget(list_host)
        root.addWidget(self.list_scroll, 1)
        root.addSpacing(10)

        self.kbd_hint = QLabel("↑↓ 选候选      ENTER 打开      ESC 返回", self)
        self.kbd_hint.setObjectName("Hint")
        root.addWidget(self.kbd_hint)

    # ---- 渲染 ----
    def show_response(self, resp: SearchResponse) -> None:
        self._response = resp
        self.input.setText(resp.query)
        self._rows = []
        self._selected = -1
        self._clear(self.best_lay)
        self._clear(self.others_box)

        if not resp.has_results:
            self.meta.setText(f"0 RESULTS / 没有找到「{resp.query}」")
            empty = QLabel(
                "换个说法：描述「想做什么」，而不是「叫什么」。\n"
                "例如：把文件读成字符串 · 去掉列表里重复的 · 发一个网络请求 · 判断文件后缀",
                self.best_card,
            )
            empty.setObjectName("Muted")
            empty.setWordWrap(True)
            self.best_lay.addWidget(empty)
            self.others_title.setVisible(False)
            self.kbd_hint.setVisible(False)
            return

        self.kbd_hint.setVisible(True)
        best = resp.best
        self._shown_entry_id = best.entry_id
        self.meta.setText(f"{len(resp.hits):02d} RESULTS / 「{resp.query}」")

        head = QHBoxLayout()
        head.setSpacing(12)
        title = QLabel(best.title, self.best_card)
        title.setObjectName("CardTitle")
        head.addWidget(title)
        head.addStretch(1)
        head.addWidget(Badge(
            Badge.LEVELS.get(best.origin, "UNSET"), best.origin or "unknown", self.best_card,
        ))
        ident = QLabel(best.entry_id, self.best_card)
        ident.setObjectName("MonoId")
        head.addWidget(ident)
        self.best_lay.addLayout(head)

        desc = first_sentence(best.description, 120)
        if desc:
            d = QLabel(desc, self.best_card)
            d.setObjectName("Body")
            d.setWordWrap(True)
            self.best_lay.addWidget(d)

        actions = QHBoxLayout()
        actions.setSpacing(16)
        open_btn = QPushButton("查看完整内容  →", self.best_card)
        open_btn.setObjectName("Primary")
        open_btn.setCursor(Qt.PointingHandCursor)
        open_btn.clicked.connect(lambda: self.entry_chosen.emit(self._shown_entry_id))
        actions.addWidget(open_btn)
        actions.addSpacing(18)

        ok = QPushButton("这条对", self.best_card)
        ok.setObjectName("FeedbackBtn")
        ok.setProperty("verdict", "ok")
        ok.setCursor(Qt.PointingHandCursor)
        ok.setToolTip("这条正是我要的")
        ok.clicked.connect(lambda: self._feedback("ok"))
        actions.addWidget(ok)

        actions.addSpacing(10)
        bad = QPushButton("不是这条", self.best_card)
        bad.setObjectName("FeedbackBtn")
        bad.setProperty("verdict", "bad")
        bad.setCursor(Qt.PointingHandCursor)
        bad.setToolTip("不是这条 / 根本不是我要的")
        bad.clicked.connect(lambda: self._feedback("bad"))
        actions.addWidget(bad)
        actions.addStretch(1)
        self.best_lay.addLayout(actions)

        others = resp.others
        self.others_title.setVisible(bool(others))
        for i, hit in enumerate(others, start=2):
            row = CandidateRow(hit.entry_id, hit.title, hit.description, hit.origin, i, self)
            row.chosen.connect(self.entry_chosen.emit)
            self.others_box.addWidget(row)
            self._rows.append(row)

    # ---- 键盘 ----
    def eventFilter(self, obj, event):  # noqa: N802
        from PySide6.QtCore import QEvent

        if obj is self.input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Down and self._rows:
                self.move_selection(1)
                self.setFocus(Qt.OtherFocusReason)
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        key = event.key()
        if key in (Qt.Key_Down, Qt.Key_Tab):
            self.move_selection(1)
            event.accept()
            return
        if key in (Qt.Key_Up, Qt.Key_Backtab):
            self.move_selection(-1)
            event.accept()
            return
        if key in (Qt.Key_Return, Qt.Key_Enter):
            self.activate_selection()
            event.accept()
            return
        if key == Qt.Key_Escape:
            self.back_requested.emit()
            event.accept()
            return
        super().keyPressEvent(event)

    def _select(self, index: int) -> None:
        if not self._rows:
            return
        index = max(0, min(index, len(self._rows) - 1))
        for i, row in enumerate(self._rows):
            row.set_selected(i == index)
        self._selected = index

    def move_selection(self, delta: int) -> None:
        if not self._rows:
            return
        self._select(self._selected + delta if self._selected >= 0 else 0)

    def activate_selection(self) -> None:
        if 0 <= self._selected < len(self._rows):
            self.entry_chosen.emit(self._rows[self._selected].entry_id)
        elif self._shown_entry_id:
            self.entry_chosen.emit(self._shown_entry_id)

    def _feedback(self, verdict: str) -> None:
        self.feedback_given.emit(verdict)

    def _clear(self, layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear(item.layout())


# ================= import 面板 =================
class ImportPanel(QFrame):
    def __init__(self, entry: EntryDTO, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("ImportPanel")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 11, 14, 11)
        lay.setSpacing(7)

        lay.addWidget(mono_label("IMPORT / 用之前要 import 吗", self))

        hint = entry.import_hint
        if hint.kind == "builtin":
            ok = QLabel("无需导入 —— Python 内置，直接写", self)
            ok.setObjectName("ImportOk")
            lay.addWidget(ok)
            return

        if hint.kind == "thirdparty" and hint.install:
            lay.addWidget(self._copy_row(hint.install, "安装", self))

        if hint.statement:
            lay.addWidget(self._copy_row(hint.statement, "import", self))
        else:
            miss = QLabel("（条目未标注 import 语句）", self)
            miss.setObjectName("Muted")
            lay.addWidget(miss)

        note_text = {
            "stdlib": "标准库自带，写上面这行就行",
            "thirdparty": "第三方库：先装再用",
            "unknown": "该条目未标注层级，无法判断是否需要导入",
        }.get(hint.kind, "")
        if note_text:
            note = QLabel(note_text, self)
            note.setObjectName("Muted")
            lay.addWidget(note)

    def _copy_row(self, text: str, label: str, parent: QWidget) -> QWidget:
        row = QWidget(parent)
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        code = QLabel(text, row)
        code.setObjectName("ImportCode")
        code.setTextInteractionFlags(Qt.TextSelectableByMouse)
        code.setWordWrap(True)
        h.addWidget(code, 1)

        btn = QPushButton("COPY", row)
        btn.setObjectName("CopyBtn")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setToolTip(f"复制{label}")

        def do_copy() -> None:
            from PySide6.QtWidgets import QApplication

            QApplication.clipboard().setText(text)
            btn.setText("COPIED")
            QTimer.singleShot(1200, lambda: btn.setText("COPY"))

        btn.clicked.connect(do_copy)
        h.addWidget(btn, 0, Qt.AlignTop)
        return row


# ================= 详情页 =================
class DetailView(QWidget):
    back_requested = Signal()
    entry_chosen = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 10, 0, 6)
        root.setSpacing(0)

        top = QHBoxLayout()
        back = QPushButton("← 返回结果    ESC", self)
        back.setObjectName("Ghost")
        back.setCursor(Qt.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)
        top.addStretch(1)
        root.addLayout(top)
        root.addSpacing(10)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content = QWidget(self.scroll)
        self.lay = QVBoxLayout(self.content)
        self.lay.setContentsMargins(2, 2, 16, 28)
        self.lay.setSpacing(18)
        self.scroll.setWidget(self.content)
        root.addWidget(self.scroll, 1)

    def _clear(self) -> None:
        while self.lay.count():
            item = self.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

    def show_entry(self, entry: EntryDTO) -> None:
        self._clear()

        title = QLabel(entry.title, self.content)
        title.setObjectName("DetailTitle")
        title.setWordWrap(True)
        self.lay.addWidget(title)

        # 等宽元信息行：ID · 层级 · 模块 · 准确全名
        meta = QHBoxLayout()
        meta.setSpacing(10)
        ident = QLabel(entry.id, self.content)
        ident.setObjectName("MonoId")
        meta.addWidget(ident)
        meta.addWidget(Badge(entry.origin_label, entry.origin or "unknown", self.content))
        mod = QLabel(entry.module_label, self.content)
        mod.setObjectName("Mono")
        meta.addWidget(mod)
        if entry.qualname:
            qn = QLabel(entry.qualname, self.content)
            qn.setObjectName("Mono")
            qn.setTextInteractionFlags(Qt.TextSelectableByMouse)
            meta.addWidget(qn)
        meta.addStretch(1)
        self.lay.addLayout(meta)

        desc = QLabel(md_to_html(entry.description), self.content)
        desc.setObjectName("Body")
        desc.setWordWrap(True)
        desc.setTextFormat(Qt.RichText)
        self.lay.addWidget(desc)

        self.lay.addWidget(ImportPanel(entry, self.content))

        if entry.signature:
            box = QWidget(self.content)
            bl = QVBoxLayout(box)
            bl.setContentsMargins(0, 0, 0, 0)
            bl.setSpacing(7)
            bl.addWidget(mono_label("SIGNATURE / 调用形状", box))
            s = QLabel(entry.signature, box)
            s.setObjectName("Mono")
            s.setWordWrap(True)
            s.setTextInteractionFlags(Qt.TextSelectableByMouse)
            bl.addWidget(s)
            self.lay.addWidget(box)

        if entry.principle:
            self.lay.addWidget(Rule(self.content))
            self.lay.addWidget(Section("PRINCIPLE / 原理解释", entry.principle, self.content))

        if entry.code:
            self.lay.addWidget(Rule(self.content))
            self.lay.addWidget(mono_label("EXAMPLE / 使用示例", self.content))
            self.lay.addWidget(CodeBlock(entry.code, entry.language or "python", self.content))

        if entry.args:
            self.lay.addWidget(Rule(self.content))
            self.lay.addWidget(self._args_table(entry))

        if entry.returns:
            self.lay.addWidget(Rule(self.content))
            self.lay.addWidget(Section("RETURNS / 返回值", entry.returns, self.content))

        if entry.caveats:
            self.lay.addWidget(Rule(self.content))
            self.lay.addWidget(Section("CAVEATS / 注意事项", entry.caveats, self.content))

        if entry.scenario:
            self.lay.addWidget(Rule(self.content))
            self.lay.addWidget(Section("WHEN / 使用场景", entry.scenario, self.content))

        if entry.related:
            self.lay.addWidget(Rule(self.content))
            self.lay.addWidget(self._related(entry))

        self.lay.addStretch(1)
        self.scroll.verticalScrollBar().setValue(0)

    def _args_table(self, entry: EntryDTO) -> QWidget:
        box = QWidget(self.content)
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        lay.addWidget(mono_label("ARGS / 参数", box))

        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(9)
        headers = ["参数名", "必填", "默认值", "能填什么", "能不能嵌套"]
        for c, h in enumerate(headers):
            lab = QLabel(h, box)
            lab.setObjectName("SectionTitle")
            grid.addWidget(lab, 0, c)

        for r, a in enumerate(entry.args, start=1):
            name = QLabel(a.name, box)
            name.setObjectName("Mono")
            grid.addWidget(name, r, 0)

            req = QLabel("必填" if a.required else "可省", box)
            req.setObjectName("Body" if a.required else "Muted")
            grid.addWidget(req, r, 1)

            dft = QLabel(a.default or "—", box)
            dft.setObjectName("Mono")
            grid.addWidget(dft, r, 2)

            acc = QLabel(a.accepts or "—", box)
            acc.setObjectName("Body")
            acc.setWordWrap(True)
            acc.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            grid.addWidget(acc, r, 3)

            nest = QLabel(a.nesting or "—", box)
            nest.setObjectName("Muted")
            nest.setWordWrap(True)
            nest.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            grid.addWidget(nest, r, 4)

        grid.setColumnStretch(3, 3)
        grid.setColumnStretch(4, 3)
        lay.addLayout(grid)
        return box

    def _related(self, entry: EntryDTO) -> QWidget:
        box = QWidget(self.content)
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        lay.addWidget(mono_label("RELATED / 相关知识", box))
        for rel in entry.related:
            if rel.exists:
                b = QPushButton(f"{rel.entry_id}    {rel.title}  →", box)
                b.setObjectName("Ghost")
                b.setCursor(Qt.PointingHandCursor)
                b.clicked.connect(lambda _=False, eid=rel.entry_id: self.entry_chosen.emit(eid))
                lay.addWidget(b, alignment=Qt.AlignLeft)
            else:
                lab = QLabel(f"{rel.entry_id}（未收录）", box)
                lab.setObjectName("Muted")
                lay.addWidget(lab)
        return box
