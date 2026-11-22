# -*- coding: utf-8 -*-
"""把三屏渲染成 PNG（离屏），用来肉眼验收视觉，不需要人工点。

    set PYTHONPATH=src
    set QT_QPA_PLATFORM=offscreen
    py -3 tools/ui_shot.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from PySide6.QtWidgets import QApplication  # noqa: E402

from starport_dictionary.api.factory import get_backend  # noqa: E402
from starport_dictionary.ui.main_window import PAGE_DETAIL, PAGE_HOME, PAGE_RESULTS, MainWindow  # noqa: E402
from starport_dictionary.ui.theme import load_stylesheet  # noqa: E402

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

    shots = []
    # 首页
    win.stack.setCurrentIndex(PAGE_HOME)
    win.home.input.setText(QUERY)
    app.processEvents()
    shots.append(("01-home.png", PAGE_HOME))

    # 结果页
    win.do_search(QUERY)
    app.processEvents()
    shots.append(("02-results.png", PAGE_RESULTS))

    # 详情页
    best = win.results._shown_entry_id
    win.open_entry(best)
    app.processEvents()
    shots.append(("03-detail.png", PAGE_DETAIL))

    for name, idx in shots:
        win.stack.setCurrentIndex(idx)
        app.processEvents()
        path = OUT / name
        win.grab().save(str(path))
        print("已渲染:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
