r"""程序入口。

    py -3 -m starport_dictionary.ui.app              # 开发期
    py -3 -m starport_dictionary.ui.app --smoke       # 打包后自检（不开窗口，产出截图+json）
    StarportDictionary.exe                            # 打包后正常使用

启动顺序刻意简单：QApplication → 载入样式 → 建后端 → 开窗口。
后端加载失败也让窗口起来（显示错误），而不是一闪就退。
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from starport_dictionary.api.factory import get_backend
from starport_dictionary.paths import data_root
from starport_dictionary.ui.main_window import PAGE_HOME, MainWindow
from starport_dictionary.ui.theme import APP_NAME, APP_VERSION, icon_path, load_stylesheet

SMOKE_QUERY = "判断一个文件的后缀名"


def _run_smoke(app: QApplication) -> int:
    """打包自检：不开真窗口，走一遍「搜索 → 详情 → 渲染」，把结果写成文件。

    为什么不在窗口模式下用 stdout：exe 是 windowed，没有控制台，结论只能落盘。
    """
    out_dir = data_root() / "smoke"
    out_dir.mkdir(parents=True, exist_ok=True)
    result: dict = {"ok": False, "app_version": APP_VERSION}

    try:
        backend = get_backend()
        stats = backend.stats()
        result["entry_count"] = stats.entry_count
        result["module_count"] = stats.module_count
        result["errors"] = list(stats.errors)

        win = MainWindow(backend)
        win.resize(1120, 780)
        win.show()
        app.processEvents()

        win.do_search(SMOKE_QUERY)
        app.processEvents()
        best = win.results._shown_entry_id
        result["query"] = SMOKE_QUERY
        result["best_entry_id"] = best
        result["hit_count"] = len(win.results._response.hits) if win.results._response else 0

        win.open_entry(best)
        app.processEvents()
        result["detail_rendered"] = win.detail.content.layout().count() > 3

        win.stack.setCurrentIndex(2)
        app.processEvents()
        shot = out_dir / "detail.png"
        win.grab().save(str(shot))
        result["screenshot"] = str(shot)

        result["ok"] = bool(result.get("hit_count")) and result.get("detail_rendered", False)
    except Exception as exc:  # 打包问题必须留下证据
        logging.exception("smoke 失败")
        result["error"] = f"{type(exc).__name__}: {exc}"

    (out_dir / "smoke.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0 if result["ok"] else 2


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv)
    smoke = "--smoke" in args

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if smoke:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        # 离屏渲染需要一个字体目录，否则中文会变方块
        if sys.platform == "win32" and "QT_QPA_FONTDIR" not in os.environ:
            os.environ["QT_QPA_FONTDIR"] = str(Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts")

    app = QApplication(args)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(load_stylesheet())
    icon = icon_path()
    if icon.is_file():
        app.setWindowIcon(QIcon(str(icon)))

    if smoke:
        return _run_smoke(app)

    try:
        backend = get_backend()
    except Exception as exc:  # 知识库坏了也要让人看见原因
        logging.exception("初始化后端失败")
        QMessageBox.critical(None, APP_NAME, f"知识库加载失败：\n{exc}")
        return 1

    win = MainWindow(backend)
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
