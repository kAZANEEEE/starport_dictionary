r"""切屏过渡动画。

2026-11-22 立：反馈太少不行——按 Esc 瞬间跳回去，人会觉得"点了没反应"。
做法是**抓一张旧屏的快照压在顶层，然后让这张快照滑走/淡出**，露出下面的新屏。
好处：不去动 QStackedWidget 的布局（动布局必被布局管理器打回去），
也不会因为动画而让控件重建、滚动位置丢。

克制参数：170ms，OutCubic，位移只有屏宽的 12%——够感觉到"移动"，不拖沓。
"""

from __future__ import annotations

from PySide6.QtCore import (
    QAbstractAnimation,
    QEasingCurve,
    QPropertyAnimation,
    Qt,
)
from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel, QStackedWidget

DURATION_MS = 170
SHIFT_RATIO = 0.12


class ScreenTransitions:
    """给一个 QStackedWidget 装上「滑动 + 淡出」的切屏效果。"""

    def __init__(self, stack: QStackedWidget) -> None:
        self._stack = stack
        self._anims: list[QAbstractAnimation] = []

    def goto(self, index: int, *, forward: bool = True) -> None:
        """切到第 index 屏。forward=True 表示"往里走"，False 表示"往回退"。

        往回退时旧屏往右滑走（像退出一个页面），往里走时旧屏往左滑走。
        """
        if index == self._stack.currentIndex():
            return

        old = self._stack.grab()                 # 先把旧屏抓成位图
        self._stack.setCurrentIndex(index)       # 立刻切（下面被快照盖住，看不出来）

        overlay = QLabel(self._stack)
        overlay.setPixmap(old)
        overlay.setGeometry(self._stack.rect())
        overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        overlay.show()
        overlay.raise_()

        effect = QGraphicsOpacityEffect(overlay)
        overlay.setGraphicsEffect(effect)

        start = overlay.geometry()
        shift = int(start.width() * SHIFT_RATIO) * (-1 if forward else 1)
        end = start.translated(shift, 0)

        move = QPropertyAnimation(overlay, b"geometry", overlay)
        move.setDuration(DURATION_MS)
        move.setStartValue(start)
        move.setEndValue(end)
        move.setEasingCurve(QEasingCurve.OutCubic)

        fade = QPropertyAnimation(effect, b"opacity", overlay)
        fade.setDuration(DURATION_MS)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(QEasingCurve.OutCubic)

        def cleanup() -> None:
            overlay.deleteLater()

        for anim in (move, fade):
            anim.finished.connect(cleanup if anim is fade else lambda: None)
            anim.start(QAbstractAnimation.DeleteWhenStopped)
            self._anims.append(anim)

    def cancel_all(self) -> None:
        """窗口关闭/重切时停掉未完成的动画，避免野指针。"""
        for anim in self._anims:
            try:
                anim.stop()
            except RuntimeError:
                pass
        self._anims.clear()
