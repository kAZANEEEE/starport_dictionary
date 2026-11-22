r"""数据目录解析：开发期和打包后（exe）走不同位置。

2026-11-22 定：
- 知识库（knowledge-packs）是**只读资源**，开发时在仓库里，打包后随 exe 一起分发（sys._MEIPASS）。
- 用户数据（反馈、最近搜索）是**可写**的，一律放 %LOCALAPPDATA%\StarportDictionary。

为什么不把知识库也放 LOCALAPPDATA：用户不该手动改它；以后有知识包更新，随版本替换更省事。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

APP_DIR_NAME = "StarportDictionary"


def is_frozen() -> bool:
    """是不是 PyInstaller 打出来的 exe。"""
    return bool(getattr(sys, "frozen", False))


def _repo_root() -> Path:
    """开发期：从本文件往上找到仓库根（含 knowledge-packs 的那层）。"""
    return Path(__file__).resolve().parents[2]


def packs_root() -> Path:
    """知识库根目录（只读）。"""
    if is_frozen():
        # PyInstaller onefile 解到 _MEIPASS；onedir 时在 exe 同级
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        bundled = base / "knowledge-packs"
        if bundled.is_dir():
            return bundled
        return Path(sys.executable).parent / "knowledge-packs"
    return _repo_root() / "knowledge-packs"


def data_root() -> Path:
    """用户数据根目录（可写）。打包后用 LOCALAPPDATA，开发期用仓库内 data/。"""
    if is_frozen():
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
        root = base / APP_DIR_NAME
    else:
        root = _repo_root() / "data"
    root.mkdir(parents=True, exist_ok=True)
    return root


def feedback_file() -> Path:
    return data_root() / "feedback.jsonl"


def recent_file() -> Path:
    return data_root() / "recent.json"
