# -*- coding: utf-8 -*-
"""拿一批真实问题去搜，看看 130 条到底能答上多少。"""
import sys
from pathlib import Path

ROOT = Path(r"D:\some_project\Starport-Dictionary")
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starport_dictionary.knowledge.loader import load_all_packs
from starport_dictionary.search.baseline import search

entries = [e for p in load_all_packs(ROOT / "knowledge-packs") for e in p.entries]
by_id = {e.id: e for e in entries}

# 真实会问的问题：左边是问题，右边是「我认为该命中的条目」（None = 库里就没有）
CASES = [
    ("怎么读一个 csv 文件", None),
    ("发一个 http 请求拿 json", None),
    ("用 tkinter 弹个窗口", None),
    ("读 excel 表格", None),
    ("多线程下载会不会卡住界面", None),
    ("把两个字典合并", "py.dict.merge"),
    ("列表里重复的怎么去掉", "py.list.dedupe"),
    ("读文件里的每一行", "py.fs.open_with"),
    ("判断文件后缀", "py.fs.check_extension"),
    ("json 字符串转字典", "py.json.loads"),
    ("按分数给学生排序", "py.list.sort"),
    ("数据库里插一条记录", "py.sqlite.insert"),
    ("怎么让程序等两秒", "py.time.sleep"),
    ("统计每个词出现几次", "py.collections.counter"),
    ("手机号格式校验", "py.regex.match"),
    ("生成一个随机数", "py.random.randint"),
]

print(f"库里有 {len(entries)} 条\n")
covered = missing = 0
for q, want in CASES:
    hits = search(q, entries, limit=5)
    top = by_id.get(hits[0].entry_id).title if hits else "（没找到）"
    if want is None:
        missing += 1
        print(f"[库里没有] {q:26} → 搜到: {top}")
    else:
        ok = "✅" if hits and hits[0].entry_id == want else "⚠️"
        if hits and hits[0].entry_id == want:
            covered += 1
        print(f"[{ok} 有] {q:26} → {top}")

print()
print(f"库里已覆盖且搜得到：{covered} / {covered + missing} 个测试问题")
print(f"库里根本没有的：{missing} 个")
