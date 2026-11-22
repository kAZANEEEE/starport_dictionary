r"""可复用控件（冷纸工程手册版）。

2026-11-22 重做要点：
- 徽章不再是彩色圆角块，改成等宽小字（层级用颜色，不用形状）
- 候选行不是卡片，是"一行字 + 一条细线"
- 代码块去掉圆角与外框，只留上下两条线
"""

from __future__ import annotations

import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from starport_dictionary.ui.theme import (
    ACCENT,
    ACCENT_DIM,
    CODE_BG,
    FS_MICRO,
    OK,
    TEXT,
    TEXT_2,
    TEXT_3,
)


def mono_label(text: str, parent: QWidget | None = None) -> QLabel:
    """等宽大写小标签——全站"工程感"的主要来源。"""
    lab = QLabel(text, parent)
    lab.setObjectName("Label")
    return lab


class Badge(QLabel):
    """层级标记：等宽小字，颜色区分，不加底色/圆角。"""

    LEVELS = {
        "builtin": "BUILTIN",
        "stdlib": "STDLIB",
        "thirdparty": "3RD-PARTY",
        "unknown": "UNSET",
    }

    def __init__(self, text: str, level: str = "unknown", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("Badge")
        self.setProperty("level", level)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


# ---------------- Markdown → 富文本 ----------------
_CODE_RE = re.compile(r"`([^`]+)`")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")


def first_sentence(text: str, limit: int = 70) -> str:
    t = (text or "").strip().replace("\n", " ")
    t = t.replace("**", "").replace("`", "")
    if not t:
        return ""
    cut = t.split("。")[0]
    return cut if len(cut) <= limit else cut[: limit - 1] + "…"


def md_to_html(text: str) -> str:
    if not text:
        return ""
    out = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = _BOLD_RE.sub(r"<b>\1</b>", out)
    out = _CODE_RE.sub(
        '<span style="font-family:Consolas,monospace;color:%s;">\\1</span>' % ACCENT,
        out,
    )
    lines = []
    for raw in out.split("\n"):
        line = raw.rstrip()
        if line.startswith("- "):
            lines.append('<div style="margin-left:8px;color:%s;">·&nbsp;' % TEXT_2 + line[2:] + "</div>")
        elif re.match(r"^\d+\.", line):
            lines.append('<div style="margin-left:2px;">' + line + "</div>")
        elif line:
            lines.append('<div style="margin:0 0 6px 0;">' + line + "</div>")
        else:
            lines.append("")
    return "".join(lines)


# ---------------- Python 高亮 ----------------
class PythonHighlighter(QSyntaxHighlighter):
    """低饱和高亮：关键字黄铜、字符串橄榄、注释灰、数字暖黄。"""

    def __init__(self, document) -> None:
        super().__init__(document)
        rules: list[tuple[re.Pattern, QTextCharFormat]] = []

        kw = QTextCharFormat()
        kw.setForeground(QColor(ACCENT))
        kw.setFontWeight(QFont.DemiBold)
        rules.append((
            re.compile(
                r"\b(def|class|return|if|elif|else|for|while|try|except|finally|with|as|"
                r"import|from|in|not|and|or|is|None|True|False|lambda|yield|pass|break|"
                r"continue|raise|global|assert|del|await|async)\b"
            ),
            kw,
        ))

        string_fmt = QTextCharFormat()
        string_fmt.setForeground(QColor(OK))
        rules.append((re.compile(r'"[^"\n]*"|\'[^\'\n]*\''), string_fmt))

        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor(TEXT_3))
        comment_fmt.setFontItalic(True)
        rules.append((re.compile(r"#[^\n]*"), comment_fmt))

        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("#D2B27A"))
        rules.append((re.compile(r"\b\d+(\.\d+)?\b"), num_fmt))

        fn_fmt = QTextCharFormat()
        fn_fmt.setForeground(QColor(TEXT))
        rules.append((re.compile(r"\b(print|len|str|int|float|list|dict|set|tuple|open|"
                                 r"range|enumerate|zip|sorted|sum|min|max|any|all)\b"), fn_fmt))
        self._rules = rules

    def highlightBlock(self, text: str) -> None:  # noqa: N802
        for pattern, fmt in self._rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


# ---------------- 代码块 ----------------
class CodeBlock(QFrame):
    def __init__(self, code: str, language: str = "python", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("CodeFrame")
        self._code = code.rstrip("\n")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QWidget(self)
        hb = QHBoxLayout(header)
        hb.setContentsMargins(12, 8, 6, 6)
        hb.setSpacing(8)
        hb.addWidget(mono_label(language.upper(), header))
        hb.addStretch(1)
        self.copy_btn = QPushButton("COPY", header)
        self.copy_btn.setObjectName("CopyBtn")
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.clicked.connect(self._copy)
        hb.addWidget(self.copy_btn)
        root.addWidget(header)

        self.editor = QPlainTextEdit(self)
        self.editor.setObjectName("CodeEdit")
        self.editor.setPlainText(self._code)
        self.editor.setReadOnly(True)
        self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)
        lines = max(1, self._code.count("\n") + 1)
        line_h = self.editor.fontMetrics().lineSpacing()
        self.editor.setFixedHeight(min(lines + 1, 24) * line_h + 14)
        root.addWidget(self.editor)

        self._highlighter = PythonHighlighter(self.editor.document())

    def _copy(self) -> None:
        QApplication.clipboard().setText(self._code)
        self.copy_btn.setText("COPIED")
        from PySide6.QtCore import QTimer

        QTimer.singleShot(1200, lambda: self.copy_btn.setText("COPY"))


# ---------------- 区块 ----------------
class Section(QWidget):
    """标题（等宽小字）+ 正文。区块之间靠间距和一条线分开，不套盒子。"""

    def __init__(self, title: str, body: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        lay.addWidget(mono_label(title, self))

        b = QLabel(md_to_html(body), self)
        b.setObjectName("Body")
        b.setWordWrap(True)
        b.setTextFormat(Qt.RichText)
        b.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lay.addWidget(b)


class Rule(QFrame):
    """一条 1px 横线，用来分组。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(1)
        self.setStyleSheet("background-color:#26262A;")


# ---------------- 可点区块 ----------------
class ClickableFrame(QFrame):
    clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)

    def set_selected(self, on: bool) -> None:
        if self.property("selected") != on:
            self.setProperty("selected", on)
            self.style().unpolish(self)
            self.style().polish(self)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


# ---------------- 候选行 ----------------
class CandidateRow(ClickableFrame):
    """一行：序号（等宽）+ 标题 + 层级 + ID + 一句话效果。"""

    chosen = Signal(str)

    def __init__(self, entry_id: str, title: str, description: str, origin: str,
                 index: int = 0, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Candidate")
        self.setFocusPolicy(Qt.NoFocus)
        self.entry_id = entry_id

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 9, 12, 9)
        lay.setSpacing(3)

        top = QHBoxLayout()
        top.setSpacing(10)
        idx = QLabel(f"{index:02d}", self)
        idx.setObjectName("MonoId")
        idx.setFixedWidth(20)
        top.addWidget(idx)

        name = QLabel(title, self)
        name.setObjectName("RowTitle")
        top.addWidget(name)

        top.addWidget(Badge(
            Badge.LEVELS.get(origin, "UNSET"), origin or "unknown", self,
        ))
        top.addStretch(1)

        ident = QLabel(entry_id, self)
        ident.setObjectName("MonoId")
        top.addWidget(ident)
        lay.addLayout(top)

        desc = first_sentence(description, 80)
        if desc:
            d = QLabel(desc, self)
            d.setObjectName("Muted")
            d.setWordWrap(True)
            d.setContentsMargins(30, 0, 0, 0)
            lay.addWidget(d)

        self.clicked.connect(lambda: self.chosen.emit(self.entry_id))
