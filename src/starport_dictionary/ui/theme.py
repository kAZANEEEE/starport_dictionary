r"""主题：颜色常量 + QSS 载入 + 一个极淡的星空背景。

打包成 exe 后 QSS 在 sys._MEIPASS 里，所以路径统一走 paths。
"""

from __future__ import annotations

import random
from pathlib import Path

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

# 深空色板（QSS 里用的是同一套值，改这里要同步改 dark.qss）
BG = "#0b1020"
SURFACE = "#121a33"
SURFACE_2 = "#131c38"
BORDER = "#1f2a4a"
ACCENT = "#7c6cff"
ACCENT_2 = "#4cc9f0"
TEXT = "#e6e9f5"
TEXT_MUTED = "#8b93b0"
OK = "#56d99a"
BAD = "#f07a7a"

APP_NAME = "Starport Dictionary"
APP_VERSION = "0.1.0"


def qss_path() -> Path:
    return Path(__file__).resolve().parent / "resources" / "dark.qss"


def load_stylesheet() -> str:
    p = qss_path()
    if not p.is_file():
        return ""
    return p.read_text(encoding="utf-8")


class StarfieldBackground(QWidget):
    """极淡的星点背景：一次性生成固定随机点，随窗口缩放重算比例位置。

    克制原则：不做闪烁动画，只提供一层质感，不抢搜索框的视觉重量。
    """

    def __init__(self, parent: QWidget | None = None, count: int = 90) -> None:
        super().__init__(parent)
        rnd = random.Random(20261122)  # 固定种子 → 每次启动星图一致
        self._stars = [(rnd.random(), rnd.random(), rnd.random() * 1.2 + 0.4, rnd.random()) for _ in range(count)]
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt 命名)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()
        for rx, ry, r, bright in self._stars:
            alpha = int(28 + bright * 70)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(180, 200, 255, alpha))
            painter.drawEllipse(QPointF(rx * w, ry * h), r, r)
        # 顶部一条极淡的紫色光带，作为"星港"的天际线
        painter.setPen(QPen(QColor(124, 108, 255, 26), 1))
        painter.drawLine(0, 2, w, 2)
        painter.end()
