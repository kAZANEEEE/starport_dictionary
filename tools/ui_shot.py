# -*- coding: utf-8 -*-
"""渲染三屏截图（等动画结束再抓，否则会抓到过渡中的叠影）。

    set PYTHONPATH=src
    set QT_QPA_PLATFORM=offscreen
    set QT_QPA_FONTDIR=C:\Windows\Fonts
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

from PySide6.QtTest import QTest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from starport_dictionary.api.factory import get_backend  # noqa: E402
from starport_dictionary.ui.main_window import PAGE_DETAIL, PAGE_HOME, PAGE_RESULTS, MainWindow  # noqa: E402
from starport_dictionary.ui.theme import load_stylesheet  # noqa: E402

OUT = ROOT / "build" / "ui"
QUERY = "判断一个文件的后缀名"
SETTLE_MS = 320           # 等过渡动画（170ms）+ 清理完成


def settle(app: QApplication, ms: int = SETTLE_MS) -> None:
    """真的等事件循环跑完，别用 processEvents 敷衍（deleteLater 不会执行）。"""
    app.processEvents()
    QTest.qWait(ms)
    app.processEvents()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    app = QApplication([])
    app.setStyleSheet(load_stylesheet())

    win = MainWindow(get_backend())
    win.resize(1120, 780)
    win.show()
    settle(app, 200)

    # 首页
    win.home.input.setText(QUERY)
    settle(app, 120)
    win.grab().save(str(OUT / "01-home.png"))
    print("已渲染:", OUT / "01-home.png")

    # 结果页
    win.do_search(QUERY)
    settle(app)
    win.grab().save(str(OUT / "02-results.png"))
    print("已渲染:", OUT / "02-results.png")

    # 详情页
    win.open_entry(win.results._shown_entry_id)
    settle(app)
    win.grab().save(str(OUT / "03-detail.png"))
    print("已渲染:", OUT / "03-detail.png")

    # 回到结果页再回首页（顺便验证返回过渡不留残影）
    win.go_results()
    settle(app)
    win.grab().save(str(OUT / "04-back-results.png"))
    print("已渲染:", OUT / "04-back-results.png")

    win.go_home()
    settle(app)
    win.grab().save(str(OUT / "05-back-home.png"))
    print("已渲染:", OUT / "05-back-home.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
