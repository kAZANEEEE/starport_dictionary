# -*- coding: utf-8 -*-
"""粗糙版验证器：把每条知识条目里的「推荐代码」真跑一遍，只回答一件事——挂没挂。

刻意不做的事（等条目过百再说）：
- 不区分「代码写错了」还是「环境缺文件」
- 不扫描危险调用
- 不改条目的 status，只出报告

做的三道保险：
1. 在临时目录里跑，cwd 是临时的，跑完就删
2. 用 sys.executable -I 起子进程（隔离模式：不吃 PYTHONPATH、不吃用户 site-packages）
3. 5 秒超时，卡死就杀掉

用法：
    set PYTHONPATH=src
    py -3 tools/verify_entries.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starport_dictionary.knowledge.loader import load_all_packs  # noqa: E402

TIMEOUT = 5


def run_code(code: str) -> tuple[str, str]:
    """返回 (结论, 详情)。结论只有 pass / fail / timeout 三种。"""
    with tempfile.TemporaryDirectory(prefix="sd_verify_") as tmp:
        script = Path(tmp) / "entry.py"
        script.write_text(code, encoding="utf-8")

        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env.pop("PYTHONPATH", None)  # 别让本项目的包混进条目代码的运行环境

        try:
            proc = subprocess.run(
                [sys.executable, "-I", str(script)],
                cwd=tmp,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return "timeout", f"超过 {TIMEOUT} 秒还没结束"

        if proc.returncode == 0:
            return "pass", (proc.stdout or "").strip().splitlines()[-1] if proc.stdout.strip() else ""
        # 失败时取 stderr 最后一行——通常就是异常类型那句
        err = (proc.stderr or "").strip().splitlines()
        return "fail", err[-1] if err else f"退出码 {proc.returncode}"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    packs = load_all_packs(ROOT / "knowledge-packs")
    entries = [e for p in packs for e in p.entries]
    if not entries:
        print("没读到任何条目")
        return 1

    results = []
    for entry in entries:
        verdict, detail = run_code(entry.code)
        results.append(
            {
                "id": entry.id,
                "title": entry.title,
                "declared_status": entry.status,
                "verdict": verdict,
                "detail": detail,
            }
        )

    # —— 打印表 ——
    print(f"{'条目':32} {'声明状态':10} {'实跑结果':9} 详情")
    print("-" * 96)
    for r in results:
        print(f"{r['id']:32} {r['declared_status']:10} {r['verdict']:9} {r['detail'][:44]}")

    passed = sum(1 for r in results if r["verdict"] == "pass")
    print()
    print(f"共 {len(results)} 条：通过 {passed}，挂 {len(results) - passed}")

    # 声明是 tested 但实跑挂了 —— 这才是要立刻处理的不一致
    liars = [r for r in results if r["declared_status"] == "tested" and r["verdict"] != "pass"]
    if liars:
        print()
        print("⚠️ 声明 tested 但实跑没通过：")
        for r in liars:
            print(f"   {r['id']}: {r['detail']}")

    out = ROOT / "build" / "verify-report.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print()
    print(f"报告已写：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
