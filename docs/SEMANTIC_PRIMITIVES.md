# 语义基元词表（自动生成，别手改）

> 由 `tools/gen_primitives_doc.py` 从 `src/starport_dictionary/knowledge/primitives.py` 生成。
> 要改就改那个 .py 文件，然后重跑脚本。手改这份会在下次生成时被覆盖。

## Object（40 个）

| ID | 标准名称 | 别名 | 说明 |
|---|---|---|---|
| `file.extension` | 文件后缀 | 后缀、扩展名、文件扩展名、文件名后缀、suffix、extension | 文件名最后一个点之后的部分，如 .py |
| `file.name` | 文件名 | 名字、文件名称、filename、basename | 不含目录部分的文件名 |
| `file.path` | 文件路径 | 路径、绝对路径、相对路径、path、directory path | 文件或目录在文件系统中的位置 |
| `file.content` | 文件内容 | 内容、文件数据、读文件、文本文件、read_text、write_text、file content | 文件里存的字节/文本，和后缀无关 |
| `file.size` | 文件大小 | 大小、体积、多少字节、file size | 文件占用的字节数 |
| `file.mtime` | 文件修改时间 | 修改时间、最后修改、mtime、updated time | 文件内容最后一次被改动的时间 |
| `file.exists` | 文件是否存在 | 在不在、有没有这个文件、exist、exists、isfile、isdir、is_file、is_dir | 路径指向的东西是否存在 |
| `file.real_type` | 文件真实类型 | 真实格式、MIME、文件签名、magic number | 根据文件头判断的类型，和后缀不是一回事 |
| `dir.list` | 目录内容 | 目录列表、文件夹里有什么、listdir、rglob、glob、遍历目录、makedirs、mkdir、scandir | 某个目录下有哪些文件和子目录 |
| `list.element` | 列表元素 | 元素、某项、列表、值、item、list item | 列表中的一项 |
| `list.duplicate` | 列表重复元素 | 重复项、重复值、重复元素、重复、去重、duplicate | 列表里出现多次的值 |
| `dict.value` | 字典值 | 键值、字典里的值、items、keys、values、dict value、key value | 字典中某个键对应的值 |
| `string.text` | 字符串 | 文本、字串、字符串、string、text、文字 | 一段字符序列 |
| `json.object` | JSON 数据 | json、json 对象、json 文件 | JSON 格式的结构化数据 |
| `net.connection` | 网络连接 | 连接、网络、端口、socket、connect、ping、连通 | 到某个地址端口的连接状态 |
| `process.info` | 进程信息 | 进程、pid、process | 正在运行的程序实例 |
| `datetime.time` | 时间 | 时间戳、当前时间、datetime、timestamp | 某个时间点或时间间隔 |
| `env.variable` | 环境变量 | 环境、env、环境配置 | 进程可见的键值配置 |
| `db.record` | 数据库记录 | 记录、行、row、record | 数据库表里的一行 |
| `http.response` | HTTP 响应 | 响应、接口返回、请求结果、接口数据、response、接口 | 一次 HTTP 请求拿回来的状态码、头和正文 |
| `sql.connection` | 数据库连接 | 连接数据库、数据库连接、conn、cursor、connection | 程序和数据库之间的一条会话 |
| `csv.table` | 表格数据 | 表格、csv、数据表、行列数据、table | 按行列组织的数据，来自 CSV 或 DataFrame |
| `excel.sheet` | Excel 工作表 | excel、xlsx、工作表、电子表格、sheet | Excel 里的一个工作表 |
| `word.document` | Word 文档 | word、docx、文档、报告文件、document | Word 格式的文档 |
| `image.pixel` | 图片 | 图片、图像、照片、image、picture、截图 | 位图图像及其像素尺寸、格式 |
| `config.file` | 配置文件 | 配置、配置文件、yaml、toml、config | 存放程序设置的文本文件 |
| `gui.window` | 窗口 | 窗口、界面、窗体、window、窗体界面 | 桌面程序的主窗口或对话框 |
| `gui.button` | 按钮 | 按钮、点击、按键、button、click | 界面里可以点的一个控件 |
| `gui.table` | 界面表格 | 表格控件、列表控件、tableview、grid | 界面里展示多行数据的控件 |
| `gui.widget` | 界面控件 | 控件、输入框、标签、下拉框、widget | 界面里的基础元素 |
| `thread.task` | 后台任务 | 线程、后台任务、异步、不卡界面、thread、task | 与界面并行跑的一段工作 |
| `web.route` | 路由 | 路由、接口地址、url 路径、route、endpoint | Web 服务里一个 URL 对应的处理逻辑 |
| `web.request` | 请求参数 | 请求参数、表单、query、参数、request | 客户端发来的参数、表单和文件 |
| `web.response` | 响应内容 | 返回内容、响应、回给前端、response | Web 服务返回给客户端的内容 |
| `llm.prompt` | 提示词 | 提示词、prompt、问题、指令 | 发给大模型的那段输入 |
| `llm.response` | 模型回答 | 模型输出、回答、completion、llm response | 大模型返回的文本 |
| `audio.speech` | 语音 | 语音、声音、录音、音频、speech、audio | 音频数据，或识别/合成出来的语音 |
| `hash.digest` | 哈希值 | 哈希、摘要、校验值、md5、sha256、hash | 对内容算出的定长摘要，用来校验完整性 |
| `random.number` | 随机数 | 随机、随机数、抽样、random | 按某种分布取出的随机值 |
| `program.external` | 外部程序 | 子进程、命令行、subprocess、外部命令 | 由当前程序启动的另一个程序 |

## Action（12 个）

| ID | 标准名称 | 别名 | 说明 |
|---|---|---|---|
| `inspect.check` | 判断 | 检查、验证、确认、判断是否、看看是不是、检测、校验、改过、check、verify、通不通、可达 | 回答一个是非问题，返回值多为布尔 |
| `get.obtain` | 获取 | 取、取值、拿、拿到、读取、读出、读成、读进来、得到、get、read、fetch | 从某个对象上取出信息，不改变它 |
| `create.new` | 创建 | 新建、生成、写、写入、保存、追加、输出、build、create、new | 产生一个此前不存在的东西 |
| `modify.change` | 修改 | 改、更新、设置、set、update、modify | 改变已有对象的内容或状态 |
| `delete.remove` | 删除 | 移除、去掉、砍掉、remove、delete | 把某个东西从集合里或磁盘上拿掉 |
| `search.find` | 查找 | 搜索、找、定位、在不在、有没有、search、find、lookup、index、in | 在一堆东西里定位目标，不修改它们 |
| `filter.select` | 筛选 | 过滤、挑出、select、filter | 按条件从集合里留下子集 |
| `traverse.walk` | 遍历 | 循环、递归、逐个处理、列出、列出来、扫一遍、walk、iterate | 按顺序访问集合里的每一个元素 |
| `convert.transform` | 转换 | 转成、格式化、解析、拆分、切分、切开、拆开、分割、convert、parse、format | 把一种表示变成另一种表示 |
| `compare.diff` | 比较 | 对比、比较、差异、相同、一样、是否相同、diff、compare | 找出两个东西的相同与不同 |
| `sort.order` | 排序 | 排、顺序、升序、降序、从小到大、从大到小、sort、order | 按某个规则重新排列集合 |
| `run.execute` | 执行 | 运行、调用、run、execute、invoke | 让某个东西真正开始干活 |

## 加新词的规矩

1. 先查有没有语义相同的 ID，有就复用。
2. 不因为中文叫法不同就新建（后缀 / 扩展名 → 都是 `file.extension`）。
3. 真的新对象或新动作才加，并写清含义和适用范围。
