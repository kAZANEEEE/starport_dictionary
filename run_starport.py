# -*- coding: utf-8 -*-
"""PyInstaller 打包入口（不是给人手动跑的）。

PyInstaller 需要一个真实脚本文件当入口，所以这里只做一件事：调 main()。
"""

import sys
from pathlib import Path

# 开发期直接从源码跑；打包后 PyInstaller 已经把 starport_dictionary 收进去了
if not getattr(sys, "frozen", False):
    sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from starport_dictionary.ui.app import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
