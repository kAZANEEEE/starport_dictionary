# -*- coding: utf-8 -*-
"""抓过渡动画的几帧，证明它真的在动（而不是瞬间切换）。

跑法：
    set PYTHONPATH=src & set QT_QPA_PLATFORM=offscreen & set QT_QPA_FONTDIR=C:\Windows\Fonts
    py -3 tools/ui_transition_shot.py

产物：build/ui/frame-back-*.png
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from PySide6.QtTest import QTest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from starport_dictionary.api.factory import get_backend  # noqa: E402
from starport_dictionary.ui.main_window import MainWindow  # noqa: E402
from starport_dictionary.ui.theme import load_stylesheet  # noqa: E402
from starport_dictionary.ui.transitions import DURATION_MS  # noqa: E402

OUT = ROOT / "build" / "ui"
QUERY = "判断一个文件的后缀名"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    app = QApplication([])
    app.setStyleSheet(load_stylesheet())

    win = MainWindow(get_backend())
    win.resize(1120, 780)
    win.show()
    app.processEvents()
    QTest.qWait(200)

    # 先进详情页（两跳都让动画跑完）
    win.do_search(QUERY)
    QTest.qWait(300)
    win.open_entry(win.results._shown_entry_id)
    QTest.qWait(300)

    # 触发「返回结果」的过渡，沿时间轴抓帧
    offsets = [0, DURATION_MS // 3, (DURATION_MS * 2) // 3, DURATION_MS]
    win.go_results()
    elapsed = 0
    for i, at in enumerate(offsets):
        QTest.qWait(max(0, at - elapsed))
        elapsed = at
        path = OUT / f"frame-back-{i}.png"
        win.grab().save(str(path))
        print(f"第 {i} 帧（约 {at}ms）:", path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
