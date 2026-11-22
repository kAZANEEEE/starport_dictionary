# -*- coding: utf-8 -*-
"""加 install 字段（模型 + 解析器）。第三方条目显示安装命令用。"""
from pathlib import Path

p = Path(r"D:\some_project\Starport-Dictionary\src\starport_dictionary\models\entry.py")
s = p.read_text(encoding="utf-8")
anchor = '    returns: str = ""      # 返回什么：类型 + 一句话说明'
if "install: str" not in s and anchor in s:
    s = s.replace(anchor, anchor + '\n    install: str = ""      # 第三方库的安装命令，如 pip install requests', 1)
    p.write_text(s, encoding="utf-8")
print("模型 install:", "install: str" in s)

q = Path(r"D:\some_project\Starport-Dictionary\src\starport_dictionary\knowledge\parser.py")
t = q.read_text(encoding="utf-8")
if '"install"' not in t:
    t = t.replace('    "returns",\n', '    "returns",\n    "install",\n', 1)
    t = t.replace(
        '        returns=str(meta.get("returns") or "").strip(),',
        '        returns=str(meta.get("returns") or "").strip(),\n'
        '        install=str(meta.get("install") or "").strip(),',
        1,
    )
    q.write_text(t, encoding="utf-8")
print("解析器 install:", '"install"' in t)
