# Python 知识目录（自动生成，别手改）

> 由 `tools/gen_catalog.py` 从条目头生成。改条目内容或加条目后重跑脚本。
> 手改这份会在下次生成时被覆盖。

**共 130 条**

| 层 | 条数 |
|---|---|
| 内置能力（不用 import） | 56 |
| 标准库（要 import） | 74 |

## 内置能力（不用 import） — 56 条

_Python 自带，直接写就行_

### builtins — 8 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `builtins.open()` | 逐行读取大文件 | 输入文件路径，逐行产出内容（含行尾换行符），内存占用与文件大小无关 | — | `py.fs.open_with` |
| `enumerate` | 遍历时带上下标 | 输入可迭代对象，输出「(序号, 元素)」对；序号默认从 0 开始，可用 `start=` 改 | — | `py.list.enumerate` |
| `raise` | 主动抛出异常 | 输入一个异常对象，输出「立刻中断当前函数」；调用方要么接住，要么继续往上抛 | — | `py.exceptions.raise` |
| `sum() / max() / min()` | 求和 / 最大 / 最小 | 输入一组数，输出总和 / 最大值 / 最小值；**空序列求 sum 得 0，求 max/min 抛 `ValueError`** | — | `py.list.sum_max` |
| `try / except` | 捕获异常 | 输入一段可能出错的代码 + 一个异常类型，出错时接住并执行处理分支；类型不匹配就照常抛出 | — | `py.exceptions.try` |
| `try / finally` | 无论如何都要执行的清理 | 输入一段代码 + 一段收尾代码，输出「收尾代码一定会跑」；即使中间 `return`、抛异常也都跑 | — | `py.exceptions.finally` |
| `with ... as（上下文管理器）` | 用 with 自动收尾 | 输入一个「上下文管理器」，输出它的资源对象，并在离开代码块时**自动执行收尾**（即使抛异常） | — | `py.exceptions.with` |
| `zip` | 同时遍历两个列表 | 输入两个（或多个）可迭代对象，输出「(第一个的第 i 个, 第二个的第 i 个)」这样的元组；**长度不同时按最短的截断** | — | `py.list.zip` |

### dict — 9 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `dict 推导式 {k: v for ...}` | 用推导式生成字典 | 输入「键表达式 + 值表达式 + 来源」，输出一个新字典；可加条件筛掉不要的项 | — | `py.dict.comprehension` |
| `dict.fromkeys()` | 批量造一个字典 | 输入一批键 + 一个初值，输出字典：每个键都对应**同一个**初值对象；不传初值则都是 `None` | — | `py.dict.fromkeys` |
| `dict.get` | 取字典里的值 | 按键取值 | — | `py.dict.get` |
| `dict.items()` | 遍历字典 | 输入字典，逐个访问它的键、值或键值对；顺序等于插入顺序（3.7+） | — | `py.dict.iterate` |
| `dict.keys() / dict.values() / dict.items()` | 拿字典的键或值列表 | 输入字典，输出键视图 / 值视图 / 键值对视图；**要真列表得 `list(...)` 套一层** | — | `py.dict.keys_values` |
| `dict.pop` | 取出并删除字典里的项 | 输入键（+ 可选默认值），输出它的值并从字典移除；键不存在时：给了默认值就返回默认值，没给就抛 `KeyError` | — | `py.dict.pop` |
| `dict.setdefault` | 缺键时给个默认值 | 输入键 + 默认值，输出这个键的值：键存在原样返回，不存在就**写入默认值再返回** | — | `py.dict.setdefault` |
| `dict.update() / dict ｜ dict` | 合并两个字典 | 输入两个字典，输出合并后的字典；**重复键以右边为准** | — | `py.dict.merge` |
| `sorted(d.items(), key=lambda kv: kv[1])` | 按值排序字典 | 输入字典，输出按值排好的**列表**（`(键, 值)` 对）；字典本身不会被排序 | — | `py.dict.sort_by_value` |

### list — 19 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `[i for i, x in enumerate(items) if 条件]` | 找出所有匹配的位置 | 输入列表 + 条件，输出**所有**满足条件的下标；`list.index()` 只给第一个，所以要自己遍历 | — | `py.list.index_all` |
| `any() / all()` | 判断有没有 / 是不是全都满足 | 输入一批真假值，输出一个布尔：`any` = 至少一个真，`all` = 全为真 | — | `py.list.any_all` |
| `dict.fromkeys()` | 列表去重 | 把列表里重复的值去掉，只留第一次出现的位置，顺序不变 | — | `py.list.dedupe` |
| `filter() / 列表推导式` | 按条件筛选列表 | 输入列表 + 一个判断条件，输出**只包含通过条件的元素的新列表**，原列表不变 | — | `py.list.filter` |
| `items.index(max(items))` | 找最大值在第几个 | 输入一个列表，输出最大值的下标；Python **没有内置的 argmax**，所以要用 `index(max(...))` 组合 | — | `py.list.max_index` |
| `list.copy() / copy.deepcopy()` | 复制列表（浅拷贝的坑） | 输入列表，输出一个新列表；**只复制最外层**，里面的可变元素仍和原列表共享 | — | `py.list.copy` |
| `list.count()` | 数某个值出现几次 | 输入一个值，输出它在列表里出现了几次；找不到返回 0，不报错 | — | `py.list.count` |
| `list.extend()` | 往列表里追加多个元素 | 输入可迭代对象，把它里面的元素**逐个**接到列表末尾；原地修改，返回 None | — | `py.list.extend` |
| `list.index() / in` | 查找列表里的元素 | 判断某个值在不在列表里（`in`），或者取它第一次出现的下标（`index`） | — | `py.list.find` |
| `list.insert()` | 在指定位置插入元素 | 输入下标 + 元素，把元素插到该下标**之前**（原元素和后面全部后移）；原地修改，返回 None | — | `py.list.insert` |
| `list.remove` | 按值删除列表元素 | 输入一个值，`remove` 删掉**第一个相等**的元素（原地改，返回 None）；`pop` 按**下标**删并返回被删的元素 | — | `py.list.remove` |
| `list.reverse() / reversed()` | 反转列表 | 把元素顺序颠倒 | — | `py.list.reverse` |
| `map() / 列表推导式` | 批量转换列表元素 | 输入列表 + 一个转换操作，输出**每个元素都被转换过的新列表**，元素个数不变 | — | `py.list.map` |
| `sorted() / list.sort()` | 给列表排序 | 把列表排成升序或降序，也能按自定义规则（比如字典的某个键）排 | — | `py.list.sort` |
| `sorted(key=lambda x: (字段1, 字段2))` | 按多个字段排序 | 输入列表 + 一个返回元组的 key 函数，输出按「元组里靠前字段优先」排好的新列表 | — | `py.list.sort_multi` |
| `分批切片 items[i:i+n]` | 把列表分批 | 输入列表 + 每批大小，输出一个「列表的列表」；最后一组不足时就是短的 | — | `py.list.chunk` |
| `切片 list[a:b]` | 取列表的一段 | 输入列表 + 起止下标（可带步长），输出**新列表**；起始含、结束不含，越界自动截断不报错 | — | `py.list.slice` |
| `列表推导式` | 用推导式生成列表 | 输入“表达式 + 遍历 + 可选条件”，输出一个新列表，等价于 `for` 循环 + `append` | — | `py.list.comprehension` |
| `列表推导式 [x for row in m for x in row]` | 展平嵌套列表 | 输入「列表的列表」，输出把它们接起来的一维列表；**只压一层** | — | `py.list.flatten` |

### set — 2 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `set 运算 & ｜ -` | 集合运算（交并差） | 输入两个集合（或能变成集合的序列），输出交、并、差的结果；**结果无序** | — | `py.set.ops` |
| `set()` | 用集合去重 | 输入可迭代对象，输出一个**元素唯一**的集合；顺序不保证 | — | `py.set.dedupe` |

### str — 18 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `f-string / str.format()` | 格式化字符串 | 输入模板 + 变量，输出拼好的字符串 | — | `py.string.format` |
| `split() + len()` | 统计有多少个词 | 英文：`len(text.split())` 就是词数 | — | `py.string.count_words` |
| `str.casefold() 后比较` | 忽略大小写比较 | 输入两个字符串，先把它们都转成「统一的小写形式」，再比是否相等；`casefold()` 比 `lower()` 更彻底 | — | `py.string.case_compare` |
| `str.count()` | 统计子串出现几次 | 输入字符串 + 子串，输出出现次数（整数）；**不重叠计数**，找不到返回 0 而不是报错 | — | `py.string.count` |
| `str.encode() / bytes.decode()` | 字符串与字节互转 | 输入字符串 + 编码名，输出 `bytes`；反过来 `bytes.decode(编码)` 得到字符串 | — | `py.string.encode` |
| `str.find() / str.index()` | 查找子串位置 | 输入字符串 + 子串，输出首次出现的下标；`find` 找不到返回 **-1**，`index` 找不到**抛异常** | — | `py.string.find` |
| `str.isalpha() / isspace() / isalnum() / isupper()` | 字符类型判断族 | 输入字符串，输出它是否**全部由某类字符组成**；有一个不合格就 False，空字符串也 False | — | `py.string.is_family` |
| `str.isdigit() / str.isnumeric() / str.isdecimal()` | 判断字符串是不是数字 | 输入字符串，输出它是否**全部由数字字符组成**；负号、小数点、空格都会让它判为 False | — | `py.string.isdigit` |
| `str.join()` | 把列表拼成字符串 | 输入一个字符串列表 + 一个分隔符，输出把它们连起来的一个字符串（分隔符插在中间，不在末尾） | — | `py.string.join` |
| `str.ljust() / str.rjust() / str.center()` | 字符串对齐（补空格） | 输入字符串 + 目标宽度，输出补齐到该宽度的新字符串；够长就原样返回，不截断 | — | `py.string.align` |
| `str.partition()` | 按分隔符切成三段 | 输入分隔符，输出**固定三个**元素：分隔符左边、分隔符本身、分隔符右边 | — | `py.string.partition` |
| `str.replace()` | 字符串替换 | 把字符串里的某段文字换成另一段，可以限制替换几次 | — | `py.string.replace` |
| `str.split()` | 分割字符串 | 按分隔符把字符串切成列表 | — | `py.string.split` |
| `str.splitlines()` | 按行切分文本 | 输入一段多行文本，输出每行一个元素的列表；自动识别 `\n`、`\r\n`、`\r` 等换行，并且**不会留下末尾空元素** | — | `py.string.splitlines` |
| `str.startswith() / str.endswith()` | 判断开头或结尾 | 输入字符串 + 一个或多个候选，输出 `True/False`：是不是以它们开头（或结尾） | — | `py.string.startswith` |
| `str.strip()` | 去掉首尾空白 | 输入一个字符串，输出**首尾**空白被删掉的版本（中间的空格保留），返回新字符串 | — | `py.string.strip` |
| `str.upper() / str.lower()` | 转换大小写 | 输入字符串，输出大小写变换后的**新字符串**；原字符串不变 | — | `py.string.upper_lower` |
| `str.zfill()` | 数字补零对齐 | 输入字符串 + 目标长度，输出左边补 0 到该长度的新字符串；已够长就原样返回 | — | `py.string.zfill` |


## 标准库（要 import） — 74 条

_标准库里现成的，import 之后可用_

### argparse — 1 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `argparse.ArgumentParser` | 解析命令行参数 | 输入「参数定义」+ 实际的命令行字符串，输出一个带属性的对象（如 `args.name`）；格式不对会自动报错并打印帮助 | `import argparse` | `py.argparse.parse` |

### collections — 3 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `collections.counter` | 统计每个元素出现几次 | 输入可迭代对象，输出一个“元素 → 次数”的字典，还带取 Top N 的方法 | `from collections import Counter, defaultdict` | `py.collections.counter` |
| `collections.defaultdict` | 带默认值的字典 | 输入「默认值工厂」，输出一个字典：读不存在的键时**自动建一个默认值并写回字典**，所以能直接 `d[k].append(x)` | `from collections import Counter, defaultdict` | `py.collections.defaultdict` |
| `collections.namedtuple` | 具名元组 | 输入「类型名 + 字段名列表」，输出一个类：实例既能按下标取，也能按字段名取；**不可变** | `from collections import namedtuple` | `py.collections.namedtuple` |

### dataclasses — 1 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `dataclasses.dataclass` | 用 dataclass 定义数据结构 | 输入「字段名 + 类型（+ 默认值）」，输出一个类：自动生成 `__init__`、`__repr__`、`__eq__` | `from dataclasses import dataclass, field` | `py.dataclass.define` |

### datetime — 7 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `datetime + timedelta` | 日期加减几天 | 输入一个时间 + 一个间隔，输出新的时间；原对象不变，返回的是新对象 | `from datetime import datetime, timedelta` | `py.datetime.add_days` |
| `datetime.diff` | 算两个时间差多少 | 输入两个时间对象，输出一个 `timedelta`（天数 + 秒数）；用 `.days` / `.total_seconds()` 取具体数值 | `from datetime import datetime` | `py.datetime.diff` |
| `datetime.format` | 把时间格式化成字符串 | 输入一个时间对象 + 格式串，输出字符串；反过来解析用 `strptime` | `from datetime import datetime` | `py.datetime.format` |
| `datetime.fromtimestamp()` | 时间戳转成可读时间 | 输入秒数（浮点），输出本地的 `datetime` 对象；要字符串还得再 `.strftime()` | `from datetime import datetime` | `py.datetime.ts_to_str` |
| `datetime.now` | 获取当前时间 | 拿到当前时间，并能格式化成字符串、算出两段代码之间的耗时 | `from datetime import datetime` | `py.datetime.now` |
| `datetime.parse` | 把字符串解析成时间 | 输入日期时间字符串 + 格式串，输出 `datetime` 对象；格式对不上就抛 `ValueError` | `from datetime import datetime` | `py.datetime.parse` |
| `datetime.weekday() / isoweekday()` | 判断星期几 | 输入一个日期，输出它是周几的数字；中文名字要自己映射（标准库不内置中文星期） | `from datetime import datetime` | `py.datetime.weekday` |

### functools — 1 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `functools.lru_cache` | 缓存函数结果 | 输入一个函数，输出「带记忆的同款函数」：参数相同就直接返回上次结果，不重新执行；`cache_info()` 能看到命中情况 | `from functools import lru_cache` | `py.functools.lru_cache` |

### hashlib — 1 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `hashlib.sha256()` | 计算文件哈希 | 算文件的指纹（MD5 或 SHA256），用来判断内容是否一致、有没有被改动 | `import hashlib` | `py.hash.digest` |

### itertools — 2 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `itertools.chain` | 串联多个列表一起处理 | 输入若干个可迭代对象，输出一条「依次取完所有元素」的流水线；**不复制数据** | `from itertools import chain` | `py.itertools.chain` |
| `itertools.product` | 生成所有组合（笛卡尔积） | 输入两个（或多个）可迭代对象，输出「每种搭配都出现一次」的元组序列；总数 = 各列表长度的乘积 | `from itertools import product` | `py.itertools.product` |

### json — 5 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `json.dump()` | 把数据写成 JSON 文件 | 输入 Python 对象 + 文件对象，把 JSON 文本写进文件；**`ensure_ascii=False` 才能保住中文** | `import json` | `py.json.write` |
| `json.dumps` | 转成 JSON 字符串 | 输入字典/列表，输出 JSON 文本；要写文件用 `json.dump`（不带 s） | `import json` | `py.json.dumps` |
| `json.load()` | 读取 JSON 文件 | 把 JSON 文件解析成 Python 的字典或列表 | `import json` | `py.json.read` |
| `json.loads` | 从字符串解析 JSON | 输入一段 JSON 文本，输出对应的 Python 对象（dict / list）；格式不合法抛 `JSONDecodeError` | `import json` | `py.json.loads` |
| `链式 .get() 取嵌套字段` | 安全地取嵌套字段 | 输入一串字段名，逐层往下取；**中间缺任何一层就返回兜底值，而不是抛异常** | `import json` | `py.json.get_nested` |

### logging — 3 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `logging.basicConfig()` | 输出日志（比 print 规范） | 输入一条消息 + 级别，输出到控制台（或文件）；低于设定级别的消息**直接丢弃不处理** | `import logging` | `py.logging.basic` |
| `logging.exception()` | 记录异常堆栈到日志 | 输入一条说明，输出日志行 + **完整异常堆栈**；必须在 `except` 块里调用才有效 | `import logging` | `py.logging.exception` |
| `logging.handlers.RotatingFileHandler` | 把日志写进文件 | 输入日志消息，输出到文件（可同时输出到控制台）；文件超过大小会自动切分 | `import logging` | `py.logging.file` |

### os — 13 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `os.chdir()` | 切换工作目录 | 输入一个目录路径，把它设成当前工作目录；之后的相对路径都以它为基准 | `import os` | `py.os.chdir` |
| `os.environ` | 列出所有环境变量 | 输入无（`os.environ` 本身就是映射对象），输出「变量名 → 字符串值」的完整列表 | `import os` | `py.os.env_all` |
| `os.getcwd` | 获取当前工作目录 | 问程序“我现在站在哪个目录” | `import os` | `py.os.getcwd` |
| `os.getenv` | 读取环境变量 | 输入变量名，输出它的值（字符串）；不存在时返回 `None` 或你给的默认值 | `import os` | `py.os.getenv` |
| `os.listdir` | 列出目录里的东西 | 拿到一个目录下的所有条目名（文件和子目录混在一起，**不含子目录里的内容**） | `import os` | `py.os.listdir` |
| `os.makedirs` | 创建目录（含上级） | 建目录 | `import os` | `py.os.makedirs` |
| `os.path.getmtime()` | 取文件修改时间 | 输入文件路径，输出时间戳（浮点秒数）；配合 `datetime.fromtimestamp` 变成人能看的时间 | `import os` | `py.os.get_mtime` |
| `os.path.samefile()` | 判断两个路径是不是同一个文件 | 输入两个路径，输出它们是否指向**磁盘上同一个文件**；比较的是文件身份，不是路径文字 | `import os` | `py.os.same_file` |
| `os.path.split() / os.path.splitext()` | 拆开路径 | 输入一条路径字符串，输出它的组成部分；**只做字符串切分，不检查文件是否存在** | `import os` | `py.os.split_path` |
| `os.path_join` | 拼接路径 | 输入若干路径片段，输出用**当前系统分隔符**接好的路径；用 `Path` 的重载 `/` 也行，还可读性更好 | `import os` | `py.os.path_join` |
| `os.remove() / os.unlink()` | 删除文件 | 输入文件路径，把它从磁盘上移除；文件不存在抛 `FileNotFoundError`，路径是目录则抛 `IsADirectoryError` | `import os` | `py.os.remove` |
| `os.rename` | 重命名或移动文件 | 输入源路径 + 目标路径，改名字或挪位置；同盘可直接 `rename`，跨盘要用 `shutil.move` | `import os` | `py.os.rename` |
| `os.walk()` | 递归遍历目录树（os.walk） | 输入根目录，逐个产出 `(当前目录路径, 子目录名列表, 文件名列表)` 三元组；默认自顶向下 | `import os` | `py.os.walk` |

### pathlib — 8 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `pathlib.Path.exists` | 判断文件或目录是否存在 | 问一个路径到底有没有东西，以及它是文件还是目录 | `from pathlib import Path` | `py.fs.exists` |
| `pathlib.Path.read_text` | 读取文本文件 | 把整个文本文件一次读成字符串 | `from pathlib import Path` | `py.fs.read_text` |
| `pathlib.Path.resolve()` | 转成绝对路径并规范化 | 输入任意路径，输出「相对当前工作目录算好、`.` 和 `..` 都消掉」的绝对路径 | `from pathlib import Path` | `py.os.path_resolve` |
| `pathlib.Path.rglob` | 遍历文件夹里所有文件 | 递归列出目录下的所有文件，包括子目录里的 | `from pathlib import Path` | `py.fs.traverse_directory` |
| `pathlib.Path.stat().st_size` | 获取文件大小 | 输入文件路径，输出它占的**字节数**（整数）；路径不存在抛 `FileNotFoundError` | `from pathlib import Path` | `py.fs.get_size` |
| `pathlib.Path.suffix` | 判断文件后缀 | 取出文件名的最后一个后缀，统一转成小写再比较，判断它是不是 `.py` 文件 | `from pathlib import Path` | `py.fs.check_extension` |
| `pathlib.Path.suffix` | 获取文件后缀 | 从路径里取出最后一个后缀，返回带点号的字符串，比如 `".py"` | `from pathlib import Path` | `py.fs.get_extension` |
| `pathlib.Path.write_text` | 写入文本文件 | 把字符串写进文件 | `from pathlib import Path` | `py.fs.write_text` |

### random — 3 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `random.choice` | 随机选一个 | 从序列里随机挑一个元素，或者生成一个随机整数 | `import random` | `py.random.choice` |
| `random.randint()` | 生成随机整数 | 输入下界、上界，输出它们之间（**含两端**）的一个随机整数；要「不含右端」用 `randrange` | `import random` | `py.random.randint` |
| `random.shuffle` | 打乱列表顺序 | 把列表里元素的顺序随机重排 | `import random` | `py.random.shuffle` |

### re — 3 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `re.fullmatch() / re.match()` | 判断字符串是否匹配正则 | 输入规则 + 字符串，输出匹配结果（`Match` 对象或 `None`）；用 `fullmatch` 才是“整串都符合” | `import re` | `py.regex.match` |
| `regex.findall` | 提取所有匹配内容 | 输入规则 + 文本，输出**所有匹配结果的列表**（没有匹配就是空列表）；要位置和分组用 `finditer` | `import re` | `py.regex.findall` |
| `regex.sub` | 正则替换 | 输入规则 + 替换内容 + 文本，输出替换后的新字符串；`count` 限制最多替换几次 | `import re` | `py.regex.sub` |

### shutil — 2 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `shutil.copy() / shutil.copytree()` | 复制文件或目录 | 输入源路径和目标路径，复制出副本；`copy2` 会连修改时间一起保留，`copytree` 复制整个目录 | `import shutil` | `py.shutil.copy` |
| `shutil.rmtree()` | 删除整个目录 | 输入一个目录路径，把里面**所有文件和子目录**递归删掉；不进回收站，删了就没了 | `import shutil` | `py.shutil.rmtree` |

### socket — 1 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `socket.create_connection()` | 检查网络能不能连上 | 尝试和某个地址的某个端口建立 TCP 连接，用“成不成功”判断可达性 | `import socket` | `py.net.check_connection` |

### sqlite3 — 15 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `CREATE INDEX` | 给字段建索引 | 输入表名 + 列名，建立一个「值的排好序的对照表」，之后按这列查询不用扫全表 | `import sqlite3` | `py.sqlite.create_index` |
| `DROP TABLE` | 删除表 | 输入表名，把整张表（结构 + 所有数据）从数据库删掉；只想清数据不删表用 `DELETE FROM 表` | `import sqlite3` | `py.sqlite.drop_table` |
| `SELECT ... LIMIT ? OFFSET ?` | 分页查询 | 输入「每页几条 + 跳过几条」，输出这一页的数据；**必须配 `ORDER BY`**，否则每次翻页顺序都可能变 | `import sqlite3` | `py.sqlite.pagination` |
| `SELECT COUNT(*)` | 统计表里有多少行 | 输入表名（可带条件），输出行数；只返回一个数字，不把数据取出来 | `import sqlite3` | `py.sqlite.count_rows` |
| `UPDATE ... SET a=?, b=?` | 一次更新多列 | 输入「列 = ?」的多组赋值 + 条件，一条 SQL 改多个字段；**没写的列保持原值** | `import sqlite3` | `py.sqlite.update_multi` |
| `sqlite.connect` | 连接 SQLite 数据库 | 输入数据库文件路径，输出连接对象；文件不存在会**自动创建**，不是报错 | `import sqlite3` | `py.sqlite.connect` |
| `sqlite.create_table` | 建表 | 输入表名 + 字段定义，创建一张表；用 `IF NOT EXISTS` 可重复执行不报错 | `import sqlite3` | `py.sqlite.create_table` |
| `sqlite.delete` | 删除数据库记录 | 输入表名 + 条件，删除匹配的行；删空整表用 `DELETE FROM t`（不加 WHERE） | `import sqlite3` | `py.sqlite.delete` |
| `sqlite.insert` | 往表里插入数据 | 输入表名 + 一行值，写入一条记录；用 `?` 占位符传参，**不要自己拼字符串** | `import sqlite3` | `py.sqlite.insert` |
| `sqlite.select` | 查询数据库记录 | 输入 SQL + 参数，输出结果集；`fetchall` 全取、`fetchone` 取一条、`fetchmany(n)` 取 n 条 | `import sqlite3` | `py.sqlite.select` |
| `sqlite.transaction` | 事务处理 | 把多条写操作打包：全部成功才 `commit()`，中途出错就 `rollback()`，数据库回到操作前 | `import sqlite3` | `py.sqlite.transaction` |
| `sqlite.update` | 更新数据库记录 | 输入表名、要改的字段、条件，更新匹配的行；返回没值，但 `cur.rowcount` 告诉你改了几行 | `import sqlite3` | `py.sqlite.update` |
| `sqlite3.Cursor.executemany()` | 批量插入数据 | 输入一条带占位符的 SQL + 一批参数，把每项参数各执行一次；**一次调用完成全部插入** | `import sqlite3` | `py.sqlite.executemany` |
| `sqlite3.Cursor.executescript()` | 一次执行多条 SQL | 输入一段含多条语句的 SQL 文本，逐条执行；**语句之间用分号分隔** | `import sqlite3` | `py.sqlite.executescript` |
| `sqlite3.Row` | 查询结果按列名取值 | 输入连接（设置 `row_factory`），输出「既能下标、又能按列名取」的行对象；`dict(row)` 可转普通字典 | `import sqlite3` | `py.sqlite.row_factory` |

### tempfile — 1 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `tempfile.NamedTemporaryFile / mkstemp` | 创建临时文件 | 输入后缀等参数，输出一个文件对象；默认在离开 `with` 块时**自动删除** | `import tempfile` | `py.os.temp_file` |

### time — 2 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `time.sleep` | 让程序等一会儿 | 输入秒数（可以是小数），让当前线程暂停那么久，没有返回值 | `import time` | `py.time.sleep` |
| `time.timestamp` | 获取时间戳 | 拿到“从 1970-01-01 UTC 到现在过了多少秒”的浮点数，常用来做文件名或算耗时 | `import time` | `py.time.timestamp` |

### typing — 2 条

| 全名 | 中文名 | 一句话效果 | 要写的 import | id |
|---|---|---|---|---|
| `X ｜ None / typing.Optional` | 参数默认写 None 的套路 | 输入「参数名 + 类型 + 默认 None」，输出一个可选参数；函数体里再用 `if x is None` 换成真正的默认值 | `from typing import Optional` | `py.typing.default_none` |
| `typing 类型标注` | 类型标注 | 输入函数/变量的声明，输出带类型说明的代码；**运行时不做检查**，只是给人和工具看的说明 | `from typing import Optional` | `py.typing.annotate` |
