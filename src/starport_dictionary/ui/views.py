r"""三个页面：首页 / 结果 / 详情。

约定：页面**只发信号、不直接调后端**；后端调用统一由 MainWindow 做。

2026-11-22 交互修订：
- 首页加「条目 ID 怎么读」示例卡（用户要求：py.aaa.bbb.ccc() 到底指什么）
- 结果页：整卡可点、候选带一句话效果与层级徽章、不显示分数、支持 ↑↓ + Enter
- 详情页：import 语句可一键复制
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
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
from PySide6.QtCore import QTimer

from starport_dictionary.api.dto import EntryDTO, SearchResponse
from starport_dictionary.ui.widgets import (
    Badge,
    CandidateRow,
    ClickableFrame,
    CodeBlock,
    Section,
    first_sentence,
    md_to_html,
)

EXAMPLES = [
    "判断一个文件的后缀名",
    "把文件内容读取成字符串",
    "删除列表中的重复元素",
    "获取字典中某个键对应的值",
]

# 条目 ID 读法示例：三种层级各一个
ID_LEGEND = [
    ("py.dict.get", "内置类型", "dict 的 get 用法（不用 import）"),
    ("py.os.getcwd", "标准库", "os 模块里的 getcwd（import os）"),
    ("py.json.loads", "标准库", "json 模块里的 loads（import json）"),
]


# ================= 首页 =================
class IdLegend(QFrame):
    """讲清条目 ID 的读法——用户第一次看 py.dict.get 是会懵的。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(18, 14, 18, 14)
        lay.setSpacing(8)

        head = QHBoxLayout()
        t = QLabel("条目 ID 怎么读", self)
        t.setObjectName("SectionTitle")
        head.addWidget(t)
        head.addStretch(1)
        lay.addLayout(head)

        formula = QLabel(
            "py . <b>库/板块</b> . <b>具体用法</b>　→　意思是「Python 里这个库中的这个用法」",
            self,
        )
        formula.setObjectName("Body")
        formula.setTextFormat(Qt.RichText)
        formula.setWordWrap(True)
        lay.addWidget(formula)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)
        for r, (ident, level, meaning) in enumerate(ID_LEGEND):
            idl = QLabel(ident, self)
            idl.setObjectName("Mono")
            grid.addWidget(idl, r, 0)

            bad = Badge(level, "stdlib" if "标准库" in level else "builtin", self)
            grid.addWidget(bad, r, 1)

            ml = QLabel(meaning, self)
            ml.setObjectName("Muted")
            grid.addWidget(ml, r, 2)
        grid.setColumnStretch(2, 1)
        lay.addLayout(grid)

        note = QLabel(
            "注意：第三段是「用法名」，不一定等于模块名。准确的全名看详情页顶部那个等宽徽章"
            "（例如 pathlib.Path.suffix）。",
            self,
        )
        note.setObjectName("Hint")
        note.setWordWrap(True)
        lay.addWidget(note)


class HomeView(QWidget):
    """搜索框是这一屏的视觉中心，其余元素都往它收。"""

    submitted = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Home")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addStretch(1)

        center = QVBoxLayout()
        center.setSpacing(14)
        center.setAlignment(Qt.AlignHCenter)

        from starport_dictionary.ui.theme import icon_path

        logo_file = icon_path()
        if logo_file.is_file():
            logo = QLabel(self)
            pix = QPixmap(str(logo_file))
            logo.setPixmap(pix.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo.setAlignment(Qt.AlignCenter)
            center.addWidget(logo)

        mark = QLabel("STARPORT DICTIONARY", self)
        mark.setObjectName("BrandMark")
        mark.setAlignment(Qt.AlignCenter)
        center.addWidget(mark)

        sub = QLabel("描述你想实现什么，而不是搜索你不知道名字的 API", self)
        sub.setObjectName("Hint")
        sub.setAlignment(Qt.AlignCenter)
        center.addWidget(sub)

        center.addSpacing(14)

        self.input = QLineEdit(self)
        self.input.setObjectName("SearchInput")
        self.input.setPlaceholderText("你想实现什么？")
        self.input.setMinimumWidth(640)
        self.input.setClearButtonEnabled(True)
        self.input.returnPressed.connect(self._emit)
        center.addWidget(self.input, alignment=Qt.AlignHCenter)

        hint = QLabel("Enter 搜索　·　Ctrl+K 回到搜索框　·　Esc 返回　·　↑↓ 选候选", self)
        hint.setObjectName("Hint")
        hint.setAlignment(Qt.AlignCenter)
        center.addWidget(hint)

        center.addSpacing(18)

        # 示例芯片
        chips = QWidget(self)
        chip_lay = QHBoxLayout(chips)
        chip_lay.setContentsMargins(0, 0, 0, 0)
        chip_lay.setSpacing(10)
        chip_lay.addStretch(1)
        for text in EXAMPLES:
            b = QPushButton(text, chips)
            b.setObjectName("Chip")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, t=text: self._submit(t))
            chip_lay.addWidget(b)
        chip_lay.addStretch(1)
        center.addWidget(chips)

        # 最近搜索
        self.recent_box = QWidget(self)
        self.recent_lay = QHBoxLayout(self.recent_box)
        self.recent_lay.setContentsMargins(0, 6, 0, 0)
        self.recent_lay.setSpacing(8)
        self.recent_lay.addStretch(1)
        self.recent_box.setVisible(False)
        center.addWidget(self.recent_box)

        # ID 读法：紧跟在示例下面，一起构成中间那一栏
        legend_row = QHBoxLayout()
        legend_row.addStretch(1)
        self.legend = IdLegend(self)
        self.legend.setFixedWidth(720)
        legend_row.addWidget(self.legend)
        legend_row.addStretch(1)
        center.addSpacing(6)
        center.addLayout(legend_row)

        root.addLayout(center)
        root.addStretch(1)

        self.status = QLabel("", self)
        self.status.setObjectName("Status")
        self.status.setAlignment(Qt.AlignCenter)
        root.addWidget(self.status)

    def _emit(self) -> None:
        self._submit(self.input.text())

    def _submit(self, text: str) -> None:
        q = (text or "").strip()
        if q:
            self.submitted.emit(q)

    def focus_input(self) -> None:
        self.input.setFocus()
        self.input.selectAll()

    def set_recent(self, items: list[str]) -> None:
        while self.recent_lay.count() > 2:
            item = self.recent_lay.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        if not items:
            self.recent_box.setVisible(False)
            return
        label = QLabel("最近：", self.recent_box)
        label.setObjectName("Muted")
        self.recent_lay.insertWidget(1, label)
        for i, q in enumerate(items):
            b = QPushButton(q, self.recent_box)
            b.setObjectName("Ghost")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, t=q: self._submit(t))
            self.recent_lay.insertWidget(2 + i, b)
        self.recent_box.setVisible(True)


# ================= 最佳匹配卡 =================
class BestCard(ClickableFrame):
    """整张卡都能点，不再是"只有按钮能点"。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("BestCard")


# ================= 结果页 =================
class ResultsView(QWidget):
    """最佳匹配 + 其他候选 + 反馈 + 键盘导航。"""

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

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(10)
        back = QPushButton("← 返回", self)
        back.setObjectName("Ghost")
        back.setCursor(Qt.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)

        self.input = QLineEdit(self)
        self.input.setObjectName("SearchSmall")
        self.input.setPlaceholderText("换个说法试试（Enter 重新搜索）")
        self.input.returnPressed.connect(lambda: self.search_again.emit(self.input.text().strip()))
        self.input.installEventFilter(self)
        top.addWidget(self.input, 1)
        root.addLayout(top)

        self.meta = QLabel("", self)
        self.meta.setObjectName("Muted")
        root.addWidget(self.meta)

        self.best_card = BestCard(self)
        self.best_card.clicked.connect(lambda: self.entry_chosen.emit(self._shown_entry_id))
        self.best_lay = QVBoxLayout(self.best_card)
        self.best_lay.setContentsMargins(22, 18, 22, 16)
        self.best_lay.setSpacing(10)
        root.addWidget(self.best_card)

        self.others_title = QLabel("其他相关", self)
        self.others_title.setObjectName("SectionTitle")
        root.addWidget(self.others_title)

        self.others_box = QVBoxLayout()
        self.others_box.setSpacing(8)
        root.addLayout(self.others_box)

        self.setFocusPolicy(Qt.StrongFocus)

        self.kbd_hint = QLabel("↑↓ 选择候选　Enter 打开　Esc 返回", self)
        self.kbd_hint.setObjectName("Hint")
        root.addWidget(self.kbd_hint)
        root.addStretch(1)

    # ---- 渲染 ----
    def show_response(self, resp: SearchResponse) -> None:
        self._response = resp
        self.input.setText(resp.query)
        self._rows = []
        self._selected = -1
        self._clear(self.best_lay)
        self._clear(self.others_box)

        if not resp.has_results:
            self.meta.setText(f"没有找到与「{resp.query}」相关的能力")
            empty = QLabel(
                "试试换个说法：描述「想做什么」，而不是「叫什么」。\n"
                "例如：把文件读成字符串、去掉列表里重复的、发一个网络请求、判断文件后缀",
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
        self.meta.setText(f"「{resp.query}」找到 {len(resp.hits)} 条")

        # 标题 + 徽章
        head = QHBoxLayout()
        head.setSpacing(10)
        title = QLabel(best.title, self.best_card)
        title.setObjectName("CardTitle")
        head.addWidget(title)
        head.addWidget(Badge(
            {"builtin": "内置能力", "stdlib": "标准库", "thirdparty": "第三方"}.get(best.origin, "未标注"),
            best.origin or "unknown",
            self.best_card,
        ))
        head.addStretch(1)
        ident = QLabel(best.entry_id, self.best_card)
        ident.setObjectName("Mono")
        head.addWidget(ident)
        self.best_lay.addLayout(head)

        desc = first_sentence(best.description, 110)
        if desc:
            d = QLabel(desc, self.best_card)
            d.setObjectName("Body")
            d.setWordWrap(True)
            self.best_lay.addWidget(d)

        # 操作行
        actions = QHBoxLayout()
        actions.setSpacing(8)
        open_btn = QPushButton("查看完整内容  →", self.best_card)
        open_btn.setObjectName("Primary")
        open_btn.setCursor(Qt.PointingHandCursor)
        open_btn.clicked.connect(lambda: self.entry_chosen.emit(self._shown_entry_id))
        actions.addWidget(open_btn)
        actions.addStretch(1)

        ok = QPushButton("正确", self.best_card)
        ok.setObjectName("FeedbackBtn")
        ok.setProperty("verdict", "ok")
        ok.setCursor(Qt.PointingHandCursor)
        ok.clicked.connect(lambda: self._feedback("ok"))
        actions.addWidget(ok)

        bad = QPushButton("不正确", self.best_card)
        bad.setObjectName("FeedbackBtn")
        bad.setProperty("verdict", "bad")
        bad.setCursor(Qt.PointingHandCursor)
        bad.clicked.connect(lambda: self._feedback("bad"))
        actions.addWidget(bad)
        self.best_lay.addLayout(actions)

        # 其他候选
        others = resp.others
        self.others_title.setVisible(bool(others))
        for hit in others:
            row = CandidateRow(hit.entry_id, hit.title, hit.description, hit.origin,
                               hit.matched_terms, self)
            row.chosen.connect(self.entry_chosen.emit)
            self.others_box.addWidget(row)
            self._rows.append(row)
        # 不默认选中第一行：选中态留给用户按 ↑↓ 时才出现

    # ---- 键盘 ----
    def eventFilter(self, obj, event):  # noqa: N802
        """搜索框里按 ↓ 就往候选列表走，其余按键（左右、回车、输入）保持原生行为。"""
        from PySide6.QtCore import QEvent

        if obj is self.input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Down and self._rows:
                self.move_selection(1)
                self.setFocus(Qt.OtherFocusReason)   # 往下走就进列表
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

    # ---- 键盘导航 ----
    def _select(self, index: int, move_focus: bool = False) -> None:
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
        """Enter：选中候选就打开它；没选中就打开最佳匹配。"""
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


# ================= 详情页 =================
class ImportPanel(QFrame):
    """「要不要 import」这块——详情页最重要的信息。"""

    def __init__(self, entry: EntryDTO, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("ImportPanel")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(6)

        head = QHBoxLayout()
        t = QLabel("使用前需要 import 吗？", self)
        t.setObjectName("SectionTitle")
        head.addWidget(t)
        head.addStretch(1)
        lay.addLayout(head)

        hint = entry.import_hint
        if hint.kind == "builtin":
            ok = QLabel("✓ 无需导入 — 这是 Python 内置能力，直接写就行", self)
            ok.setObjectName("ImportBadgeOk")
            lay.addWidget(ok)
            return

        if hint.kind == "thirdparty" and hint.install:
            lay.addWidget(self._copy_row(hint.install, "安装命令", self))

        if hint.statement:
            lay.addWidget(self._copy_row(hint.statement, "import 语句", self))
        else:
            missing = QLabel("（条目未标注 import 语句）", self)
            missing.setObjectName("Muted")
            lay.addWidget(missing)

        note_text = {
            "stdlib": "标准库自带，只要写上面这行 import",
            "thirdparty": "第三方库：先装再用",
            "unknown": "该条目未标注所属层级，暂无法判断是否需要导入",
        }.get(hint.kind, "")
        if note_text:
            note = QLabel(note_text, self)
            note.setObjectName("Muted")
            lay.addWidget(note)

    def _copy_row(self, text: str, label: str, parent: QWidget) -> QWidget:
        row = QWidget(parent)
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)
        code = QLabel(text, row)
        code.setObjectName("ImportCode")
        code.setTextInteractionFlags(Qt.TextSelectableByMouse)
        code.setWordWrap(True)
        h.addWidget(code, 1)

        btn = QPushButton("复制", row)
        btn.setObjectName("CopyBtn")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setToolTip(f"复制{label}")

        def do_copy() -> None:
            from PySide6.QtWidgets import QApplication

            QApplication.clipboard().setText(text)
            btn.setText("已复制 ✓")
            QTimer.singleShot(1200, lambda: btn.setText("复制"))

        btn.clicked.connect(do_copy)
        h.addWidget(btn, 0, Qt.AlignTop)
        return row


class DetailView(QWidget):
    """完整知识内容。突出「要不要 import」和四段式原理。"""

    back_requested = Signal()
    entry_chosen = Signal(str)      # 点「相关知识」跳转

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        top = QHBoxLayout()
        back = QPushButton("← 返回结果（Esc）", self)
        back.setObjectName("Ghost")
        back.setCursor(Qt.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)
        top.addStretch(1)
        root.addLayout(top)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content = QWidget(self.scroll)
        self.lay = QVBoxLayout(self.content)
        self.lay.setContentsMargins(4, 4, 14, 24)
        self.lay.setSpacing(16)
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
        title.setObjectName("CardTitle")
        title.setWordWrap(True)
        self.lay.addWidget(title)

        badges = QHBoxLayout()
        badges.setSpacing(8)
        badges.addWidget(Badge(entry.origin_label, entry.origin or "unknown", self.content))
        badges.addWidget(Badge(entry.module_label, "unknown", self.content))
        qn = QLabel(entry.qualname or entry.id, self.content)
        qn.setObjectName("Mono")
        qn.setTextInteractionFlags(Qt.TextSelectableByMouse)
        badges.addWidget(qn)
        badges.addStretch(1)
        self.lay.addLayout(badges)

        desc = QLabel(md_to_html(entry.description), self.content)
        desc.setObjectName("Body")
        desc.setWordWrap(True)
        desc.setTextFormat(Qt.RichText)
        self.lay.addWidget(desc)

        self.lay.addWidget(ImportPanel(entry, self.content))

        if entry.signature:
            box = QFrame(self.content)
            box.setObjectName("Card")
            bl = QVBoxLayout(box)
            bl.setContentsMargins(16, 12, 16, 12)
            t = QLabel("调用形状", box)
            t.setObjectName("SectionTitle")
            bl.addWidget(t)
            s = QLabel(entry.signature, box)
            s.setObjectName("Mono")
            s.setWordWrap(True)
            bl.addWidget(s)
            self.lay.addWidget(box)

        if entry.principle:
            self.lay.addWidget(Section("原理解释", entry.principle, self.content))

        if entry.code:
            code_title = QLabel("使用示例", self.content)
            code_title.setObjectName("SectionTitle")
            self.lay.addWidget(code_title)
            self.lay.addWidget(CodeBlock(entry.code, entry.language or "python", self.content))

        if entry.args:
            self.lay.addWidget(self._args_table(entry))

        if entry.returns:
            self.lay.addWidget(Section("返回值", entry.returns, self.content))

        if entry.caveats:
            self.lay.addWidget(Section("注意事项", entry.caveats, self.content))

        if entry.scenario:
            self.lay.addWidget(Section("使用场景", entry.scenario, self.content))

        if entry.related:
            self.lay.addWidget(self._related(entry))

        self.lay.addStretch(1)
        self.scroll.verticalScrollBar().setValue(0)

    def _args_table(self, entry: EntryDTO) -> QWidget:
        box = QFrame(self.content)
        box.setObjectName("Card")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(10)

        t = QLabel("参数", box)
        t.setObjectName("SectionTitle")
        lay.addWidget(t)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(8)
        headers = ["参数名", "必填", "默认值", "能填什么", "能不能嵌套"]
        for c, h in enumerate(headers):
            lab = QLabel(h, box)
            lab.setObjectName("Muted")
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
        lay.setSpacing(8)
        t = QLabel("相关知识", box)
        t.setObjectName("SectionTitle")
        lay.addWidget(t)
        for rel in entry.related:
            if rel.exists:
                b = QPushButton("· " + rel.title + "  →", box)
                b.setObjectName("Ghost")
                b.setCursor(Qt.PointingHandCursor)
                b.setToolTip(rel.entry_id)
                b.clicked.connect(lambda _=False, eid=rel.entry_id: self.entry_chosen.emit(eid))
                lay.addWidget(b, alignment=Qt.AlignLeft)
            else:
                lab = QLabel(f"· {rel.entry_id}（未收录）", box)
                lab.setObjectName("Muted")
                lay.addWidget(lab)
        return box
