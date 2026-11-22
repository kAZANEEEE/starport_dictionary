r"""切屏过渡（2026-11-22 重写）。

老大的话：**一切动画本质都是曲线，不能让曲线太平滑。**
旧版用 OutCubic——开头猛、结尾无痛地滑进终点，正是"AI 感"的来源之一：
什么都是匀速减速，什么都很顺。

新版用两条手写贝塞尔，各自有"脾气"：
  进入（前进）：(0.16, 0.84, 0.24, 1.00) 150ms —— 快速启动，末段收得很干脆。
  返回（后退）：(0.52, 0.00, 0.94, 0.30) 140ms —— 先压住不动，最后"啪"地抽走。
                （旧内容拖走了，新内容立刻在位，读起来像"关掉一页"而不是"溶化"）

同时：位移只有 10%，淡出比位移结束得早（0.85 倍时长），
所以肉眼看到的是"抽走"，不是"缓慢透明"。
"""

from __future__ import annotations

from PySide6.QtCore import QAbstractAnimation, QEasingCurve, QPointF, QPropertyAnimation, Qt
from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel, QStackedWidget

ENTER_MS = 150
BACK_MS = 140
SHIFT_RATIO = 0.10
FADE_RATIO = 0.85          # 淡出比位移先结束，避免"慢慢化掉"

# 手写曲线：(x1, y1, x2, y2)
CURVE_ENTER = (0.16, 0.84, 0.24, 1.00)
CURVE_BACK = (0.52, 0.00, 0.94, 0.30)


def make_curve(points: tuple[float, float, float, float]) -> QEasingCurve:
    """把 CSS 那种 cubic-bezier 变成 Qt 曲线。"""
    x1, y1, x2, y2 = points
    try:
        curve = QEasingCurve(QEasingCurve.Type.BezierSpline)
        curve.addCubicBezierSegment(QPointF(x1, y1), QPointF(x2, y2), QPointF(1.0, 1.0))
        return curve
    except Exception:                      # 老版本 Qt 兜底
        return QEasingCurve(QEasingCurve.Type.OutQuart)


class ScreenTransitions:
    """给 QStackedWidget 装"抽走旧屏"的过渡。

    做法：抓旧屏快照压顶层 → 立刻切页 → 快照滑走并淡出。
    不动布局、不重建控件、滚动位置不丢。
    """

    def __init__(self, stack: QStackedWidget) -> None:
        self._stack = stack
        self._anims: list[QAbstractAnimation] = []

    def goto(self, index: int, *, forward: bool = True) -> None:
        if index == self._stack.currentIndex():
            return

        old = self._stack.grab()
        self._stack.setCurrentIndex(index)

        overlay = QLabel(self._stack)
        overlay.setPixmap(old)
        overlay.setGeometry(self._stack.rect())
        overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        overlay.show()
        overlay.raise_()

        effect = QGraphicsOpacityEffect(overlay)
        overlay.setGraphicsEffect(effect)

        duration = ENTER_MS if forward else BACK_MS
        start = overlay.geometry()
        direction = -1 if forward else 1
        end = start.translated(int(start.width() * SHIFT_RATIO) * direction, 0)

        move = QPropertyAnimation(overlay, b"geometry", overlay)
        move.setDuration(duration)
        move.setStartValue(start)
        move.setEndValue(end)
        move.setEasingCurve(make_curve(CURVE_ENTER if forward else CURVE_BACK))

        fade = QPropertyAnimation(effect, b"opacity", overlay)
        fade.setDuration(int(duration * FADE_RATIO))
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(make_curve(CURVE_BACK if forward else CURVE_ENTER))

        fade.finished.connect(overlay.deleteLater)
        for anim in (move, fade):
            anim.start(QAbstractAnimation.DeleteWhenStopped)
            self._anims.append(anim)

    def cancel_all(self) -> None:
        for anim in self._anims:
            try:
                anim.stop()
            except RuntimeError:
                pass
        self._anims.clear()
