r"""可复用控件：徽章、代码块（含 Python 高亮）、区块、候选行。

刻意做得"薄"：控件只负责显示，不碰后端、不存状态。
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

from starport_dictionary.ui.theme import ACCENT, ACCENT_2, OK, TEXT, TEXT_MUTED


# ---------------- 徽章 ----------------
class Badge(QLabel):
    """小徽章。level 决定配色（builtin/stdlib/thirdparty/unknown）。"""

    def __init__(self, text: str, level: str = "unknown", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("Badge")
        self.setProperty("level", level)
        self.setAlignment(Qt.AlignCenter)


# ---------------- Markdown → 富文本 ----------------
_CODE_RE = re.compile(r"`([^`]+)`")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")


def first_sentence(text: str, limit: int = 70) -> str:
    """描述取第一句并截断——候选行只需要「这条大概是干嘛的」。"""
    t = (text or "").strip().replace("\n", " ")
    t = t.replace("**", "").replace("`", "")
    if not t:
        return ""
    cut = t.split("。")[0]
    return cut if len(cut) <= limit else cut[: limit - 1] + "…"


def md_to_html(text: str) -> str:
    """把知识条目里的轻量 markdown 转成富文本（只支持 **粗体** 和 `代码`）。"""
    if not text:
        return ""
    out = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = _BOLD_RE.sub(r"<b>\1</b>", out)
    out = _CODE_RE.sub(
        r'<span style="font-family:Consolas,monospace;color:%s;background:#0a0f1e;">\1</span>'
        % ACCENT_2,
        out,
    )
    lines = []
    for raw in out.split("\n"):
        line = raw.rstrip()
        if line.startswith("- "):
            lines.append(
                '<div style="margin-left:6px;">&nbsp;·&nbsp;' + line[2:] + "</div>"
            )
        elif line:
            lines.append(line + "<br/>")
        else:
            lines.append("")
    return "".join(lines)


# ---------------- Python 高亮 ----------------
class PythonHighlighter(QSyntaxHighlighter):
    """极简 Python 高亮：关键字、字符串、注释、数字、内置函数。"""

    def __init__(self, document) -> None:
        super().__init__(document)
        kw = QTextCharFormat()
        kw.setForeground(QColor(ACCENT))
        kw.setFontWeight(QFont.DemiBold)
        self._rules: list[tuple[re.Pattern, QTextCharFormat]] = [
            (
                re.compile(
                    r"\b(def|class|return|if|elif|else|for|while|try|except|finally|with|as|"
                    r"import|from|in|not|and|or|is|None|True|False|lambda|yield|pass|break|"
                    r"continue|raise|global|assert|del|await|async)\b"
                ),
                kw,
            )
        ]
        string_fmt = QTextCharFormat()
        string_fmt.setForeground(QColor(OK))
        self._rules.append((re.compile(r'"[^"\n]*"|\'[^\'\n]*\''), string_fmt))

        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor(TEXT_MUTED))
        self._rules.append((re.compile(r"#[^\n]*"), comment_fmt))

        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("#f0c674"))
        self._rules.append((re.compile(r"\b\d+(\.\d+)?\b"), num_fmt))

        builtin_fmt = QTextCharFormat()
        builtin_fmt.setForeground(QColor(ACCENT_2))
        self._rules.append(
            (
                re.compile(
                    r"\b(print|len|str|int|float|list|dict|set|tuple|open|range|enumerate|"
                    r"zip|sorted|sum|min|max|any|all|isinstance|type|super)\b"
                ),
                builtin_fmt,
            )
        )

    def highlightBlock(self, text: str) -> None:  # noqa: N802
        for pattern, fmt in self._rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


# ---------------- 代码块 ----------------
class CodeBlock(QFrame):
    """只读代码块 + 复制按钮 + 语言标签。"""

    def __init__(self, code: str, language: str = "python", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("CodeFrame")
        self._code = code.rstrip("\n")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QWidget(self)
        hb = QHBoxLayout(header)
        hb.setContentsMargins(12, 8, 10, 4)
        lang = QLabel(language.upper(), header)
        lang.setObjectName("Mono")
        hb.addWidget(lang)
        hb.addStretch(1)
        self.copy_btn = QPushButton("复制代码", header)
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
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        lines = max(1, self._code.count("\n") + 1)
        line_h = self.editor.fontMetrics().lineSpacing()
        self.editor.setFixedHeight(min(lines + 1, 22) * line_h + 16)
        root.addWidget(self.editor)

        self._highlighter = PythonHighlighter(self.editor.document())

    def _copy(self) -> None:
        QApplication.clipboard().setText(self._code)
        self.copy_btn.setText("已复制 ✓")
        from PySide6.QtCore import QTimer

        QTimer.singleShot(1200, lambda: self.copy_btn.setText("复制代码"))


# ---------------- 区块 ----------------
class Section(QWidget):
    """一个带标题的正文区块。"""

    def __init__(self, title: str, body: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        t = QLabel(title, self)
        t.setObjectName("SectionTitle")
        lay.addWidget(t)

        b = QLabel(md_to_html(body), self)
        b.setObjectName("Body")
        b.setWordWrap(True)
        b.setTextFormat(Qt.RichText)
        b.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lay.addWidget(b)


# ---------------- 可点的卡片基类 ----------------
class ClickableFrame(QFrame):
    """整块可点。父类只管发出 clicked，视觉高亮靠 QSS 的 [selected] 属性。"""

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
    """结果页的一条候选：标题 + 层级徽章 + ID + 一句话效果。

    分数不再显示——它对用户没意义；换成「这条是干嘛的」。
    """

    chosen = Signal(str)

    def __init__(self, entry_id: str, title: str, description: str, origin: str,
                 terms: tuple[str, ...] = (), parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Candidate")
        self.setFocusPolicy(Qt.NoFocus)   # 焦点留在结果页，方向键才连续
        self.entry_id = entry_id

        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(4)

        top = QHBoxLayout()
        top.setSpacing(8)
        name = QLabel(title, self)
        name.setObjectName("RowTitle")
        top.addWidget(name)
        top.addWidget(Badge(
            {"builtin": "内置", "stdlib": "标准库", "thirdparty": "第三方"}.get(origin, "未标注"),
            origin or "unknown",
            self,
        ))
        top.addStretch(1)
        ident = QLabel(entry_id, self)
        ident.setObjectName("Mono")
        top.addWidget(ident)
        lay.addLayout(top)

        desc = first_sentence(description)
        if desc:
            d = QLabel(desc, self)
            d.setObjectName("Muted")
            d.setWordWrap(True)
            lay.addWidget(d)
        else:
            uniq = list(dict.fromkeys(terms))
            if uniq:
                d = QLabel("命中：" + "、".join(uniq[:4]), self)
                d.setObjectName("Muted")
                lay.addWidget(d)

        self.clicked.connect(lambda: self.chosen.emit(self.entry_id))
