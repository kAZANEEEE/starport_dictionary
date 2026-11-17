# -*- coding: utf-8 -*-
"""手动跑一遍：把一条知识条目读成对象，看看字段对不对。"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from starport_dictionary.knowledge.parser import parse_entry_file

path = Path("knowledge-packs/python-core/entries/py.fs.check_extension.md")
e = parse_entry_file(path)

print("id       :", e.id)
print("title    :", e.title)
print("分类      :", e.category_id)
print("状态      :", e.status)
print("实测版本  :", ", ".join(e.tested_versions))
print("别名      :", "、".join(e.aliases))
print("标签      :", ", ".join(e.tags))
print("代码行数  :", len(e.code.splitlines()))
print()
print("可检索文本（给搜索引擎的那份，代码不在里面）:")
print(e.searchable_text())
