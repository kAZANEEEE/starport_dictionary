# 语义基元词表（自动生成，别手改）

> 由 `tools/gen_primitives_doc.py` 从 `src/starport_dictionary/knowledge/primitives.py` 生成。
> 要改就改那个 .py 文件，然后重跑脚本。手改这份会在下次生成时被覆盖。

## Object（20 个）

| ID | 标准名称 | 别名 | 说明 |
|---|---|---|---|
| `file.extension` | 文件后缀 | 后缀、扩展名、文件扩展名、文件名后缀、suffix、extension | 文件名最后一个点之后的部分，如 .py |
| `file.name` | 文件名 | 名字、文件名称、filename、basename | 不含目录部分的文件名 |
| `file.path` | 文件路径 | 路径、绝对路径、相对路径、path、directory path | 文件或目录在文件系统中的位置 |
| `file.content` | 文件内容 | 内容、文件数据、读文件、文本文件、file content | 文件里存的字节/文本，和后缀无关 |
| `file.size` | 文件大小 | 大小、体积、多少字节、file size | 文件占用的字节数 |
| `file.mtime` | 文件修改时间 | 修改时间、最后修改、mtime、updated time | 文件内容最后一次被改动的时间 |
| `file.exists` | 文件是否存在 | 在不在、有没有这个文件、exist | 路径指向的东西是否存在 |
| `file.real_type` | 文件真实类型 | 真实格式、MIME、文件签名、magic number | 根据文件头判断的类型，和后缀不是一回事 |
| `dir.list` | 目录内容 | 目录列表、文件夹里有什么、listdir、rglob、glob、遍历目录 | 某个目录下有哪些文件和子目录 |
| `list.element` | 列表元素 | 元素、某项、列表、值、item、list item | 列表中的一项 |
| `list.duplicate` | 列表重复元素 | 重复项、重复值、重复元素、重复、去重、duplicate | 列表里出现多次的值 |
| `dict.value` | 字典值 | 键值、字典里的值、dict value、key value | 字典中某个键对应的值 |
| `string.text` | 字符串 | 文本、字串、字符串、string、text、文字 | 一段字符序列 |
| `json.object` | JSON 数据 | json、json 对象、json 文件 | JSON 格式的结构化数据 |
| `net.connection` | 网络连接 | 连接、网络、端口、socket、connect、ping、连通 | 到某个地址端口的连接状态 |
| `process.info` | 进程信息 | 进程、pid、process | 正在运行的程序实例 |
| `datetime.time` | 时间 | 时间戳、当前时间、datetime、timestamp | 某个时间点或时间间隔 |
| `env.variable` | 环境变量 | 环境、env、环境配置 | 进程可见的键值配置 |
| `db.record` | 数据库记录 | 记录、行、row、record | 数据库表里的一行 |
| `program.external` | 外部程序 | 子进程、命令行、subprocess、外部命令 | 由当前程序启动的另一个程序 |

## Action（12 个）

| ID | 标准名称 | 别名 | 说明 |
|---|---|---|---|
| `inspect.check` | 判断 | 检查、验证、确认、判断是否、看看是不是、检测、check、verify、通不通、可达 | 回答一个是非问题，返回值多为布尔 |
| `get.obtain` | 获取 | 取、拿、拿到、读取、读出、读成、读进来、得到、get、read、fetch | 从某个对象上取出信息，不改变它 |
| `create.new` | 创建 | 新建、生成、build、create、new | 产生一个此前不存在的东西 |
| `modify.change` | 修改 | 改、更新、设置、set、update、modify | 改变已有对象的内容或状态 |
| `delete.remove` | 删除 | 移除、去掉、砍掉、remove、delete | 把某个东西从集合里或磁盘上拿掉 |
| `search.find` | 查找 | 搜索、找、定位、在不在、有没有、search、find、lookup、index、in | 在一堆东西里定位目标，不修改它们 |
| `filter.select` | 筛选 | 过滤、挑出、select、filter | 按条件从集合里留下子集 |
| `traverse.walk` | 遍历 | 循环、递归、逐个处理、列出、列出来、扫一遍、walk、iterate | 按顺序访问集合里的每一个元素 |
| `convert.transform` | 转换 | 转成、格式化、解析、convert、parse、format | 把一种表示变成另一种表示 |
| `compare.diff` | 比较 | 对比、差异、diff、compare | 找出两个东西的相同与不同 |
| `sort.order` | 排序 | 排、顺序、升序、降序、从小到大、从大到小、sort、order | 按某个规则重新排列集合 |
| `run.execute` | 执行 | 运行、调用、run、execute、invoke | 让某个东西真正开始干活 |

## 加新词的规矩

1. 先查有没有语义相同的 ID，有就复用。
2. 不因为中文叫法不同就新建（后缀 / 扩展名 → 都是 `file.extension`）。
3. 真的新对象或新动作才加，并写清含义和适用范围。
