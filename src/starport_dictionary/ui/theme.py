r"""主题 token。

2026-11-22 重做（朋友说"一股 AI 味"，量化后确认）：
旧版 53 个颜色、7 档圆角、12 个圆角盒子、紫色霓虹强调 → 标准 AI slop 指纹。
新版方向：**冷纸工程手册**。
  - 近黑底 + 暖白字（不是冷白，眼睛不刺）
  - 唯一强调色是**黄铜**（一条细线、一个标签），不再用紫色发光
  - 圆角只有 1 档 2px；不用阴影、不用渐变、不用发光
  - 层级靠字号/字重/间距/细线，不靠更多的框和颜色
  - 拉丁标签与编号一律等宽大写 + 字距，中文正文用系统黑体

改这里要同步改 resources/dark.qss（QSS 不支持变量，所以两份并行维护）。
"""

from __future__ import annotations

import random
from pathlib import Path

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

# ---------------- 颜色（12 个，旧版 53 个） ----------------
BG = "#0B0B0C"          # 页面底
SURFACE = "#111113"     # 比底色亮一档，用来做"当前行"
SURFACE_2 = "#151517"   # 再亮一档（hover）
LINE = "#26262A"        # 细线
LINE_STRONG = "#3C3C42" # 需要分开时的一条更明显的线
TEXT = "#E9E7E2"        # 正文（暖白）
TEXT_2 = "#A6A29A"      # 次要
TEXT_3 = "#8B857C"      # 标签、提示（对比度 ≥4.5:1，11px 也能读）
TEXT_4 = "#6E6A64"      # 只用于极弱的装饰性文字
ACCENT = "#C8A464"      # 黄铜——全站唯一的彩色
ACCENT_DIM = "#7E6A45"  # 黄铜的暗版，用于极小的标记
OK = "#8FAE63"          # 对（橄榄绿，不是霓虹薄荷）
BAD = "#B8634F"         # 不对（铁锈红）
CODE_BG = "#0E0E10"

# ---------------- 字号（7 档） ----------------
FS_MICRO = 11    # 等宽大写标签
FS_SMALL = 12    # 辅助说明
FS_BODY = 13     # 正文
FS_LEAD = 15     # 引导段
FS_TITLE = 19    # 条目标题
FS_H2 = 24       # 详情页标题
FS_HERO = 32     # 首页主张

RADIUS = 2       # 唯一一档圆角

APP_NAME = "Starport Dictionary"
APP_VERSION = "0.1.1"


def assets_dir() -> Path:
    import sys

    if getattr(sys, "frozen", False):
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        bundled = base / "assets"
        if bundled.is_dir():
            return bundled
        return Path(sys.executable).parent / "assets"
    return Path(__file__).resolve().parents[3] / "assets"


def icon_path() -> Path:
    return assets_dir() / "icon.png"


def qss_path() -> Path:
    return Path(__file__).resolve().parent / "resources" / "dark.qss"


def load_stylesheet() -> str:
    p = qss_path()
    if not p.is_file():
        return ""
    return p.read_text(encoding="utf-8")


class StarfieldBackground(QWidget):
    """背景：不再画"星空"，只画一层极稀疏的刻度点 + 一条黄铜顶线。

    旧版是满屏星点 + 紫色光带（典型深空模板）。新版把它压成"纸的纹理"：
    左上角一列淡淡的刻度，暗示仪表盘，而不是装饰。
    """

    def __init__(self, parent: QWidget | None = None, count: int = 46) -> None:
        super().__init__(parent)
        rnd = random.Random(20261122)
        self._dots = [(rnd.random(), rnd.random(), rnd.random()) for _ in range(count)]
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        w, h = self.width(), self.height()

        # 极淡的点阵（alpha 很低，只为让纯色底不显得像色块）
        painter.setPen(Qt.NoPen)
        for rx, ry, a in self._dots:
            painter.setBrush(QColor(233, 231, 226, int(8 + a * 10)))
            painter.drawRect(int(rx * w), int(ry * h), 1, 1)

        # 顶部一条黄铜细线——这是全站唯一的"品牌色出现"
        painter.setPen(QPen(QColor(200, 164, 100, 70), 1))
        painter.drawLine(0, 0, w, 0)
        painter.end()
