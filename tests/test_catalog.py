r"""目录一致性测试：CATALOG.md 必须和实际条目对得上。

判据：跑一遍 gen_catalog 的逻辑，如果结果和仓库里的文件不同 → 说明有人改了条目忘了重生成。
这条测试就是「自动维护」的保险丝。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "knowledge-packs" / "python-core" / "CATALOG.md"


def test_目录文件存在():
    assert CATALOG.is_file(), "CATALOG.md 不存在，先跑 tools/gen_catalog.py"


def test_目录内容不是过期的():
    """重新生成一次，比对内容；不一致说明目录过期了。"""
    before = CATALOG.read_text(encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "gen_catalog.py")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0, f"生成器跑失败：{result.stderr}"
    after = CATALOG.read_text(encoding="utf-8")
    assert before == after, "CATALOG.md 已过期：改了条目但没重跑 tools/gen_catalog.py"


def test_每条条目都出现在目录里():
    text = CATALOG.read_text(encoding="utf-8")
    for md in (ROOT / "knowledge-packs" / "python-core" / "entries").glob("*.md"):
        assert md.stem in text, f"{md.stem} 没出现在 CATALOG.md 里"
