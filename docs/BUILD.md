# 打包成 Windows EXE

> 2026-11-22 · 本项目实测通过的打包流程（不是通用教程）

## 产物

```
dist/StarportDictionary.exe     约 37.6 MB，单文件，双击即用
```

知识库（137 条 Markdown）**打包进 exe**，用户不需要安装 Python，也不需要把 Markdown 文件放在旁边。

## 打包命令

```powershell
cd D:\some_project\Starport-Dictionary

py -3 -m PyInstaller --noconfirm --clean --windowed --onefile `
  --name StarportDictionary `
  --paths src `
  --add-data "knowledge-packs;knowledge-packs" `
  --add-data "src/starport_dictionary/ui/resources;starport_dictionary/ui/resources" `
  --hidden-import PySide6.QtCore --hidden-import PySide6.QtGui --hidden-import PySide6.QtWidgets `
  --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.Qt3DCore `
  --exclude-module PySide6.QtMultimedia --exclude-module PySide6.QtQuick `
  --exclude-module tkinter --exclude-module pytest `
  run_starport.py
```

### 每个参数为什么这么写

| 参数 | 原因 |
|---|---|
| `--windowed` | 双击时不弹黑框控制台 |
| `--onefile` | 交付物是一个文件，不用给用户一个文件夹 |
| `--add-data "knowledge-packs;knowledge-packs"` | 知识库必须打进去；运行时由 `paths.packs_root()` 从 `sys._MEIPASS` 找 |
| `--add-data .../ui/resources;...` | QSS 也是资源，漏了就变成无样式白窗口 |
| `--exclude-module PySide6.QtWebEngineCore` 等 | 这几块各有几十 MB，用不到，排除后体积从 ~120MB 降到 37.6MB |
| `--exclude-module pytest` | 别把测试框架打进去 |

## 自检（必做）

exe 是窗口程序，没有控制台，所以自检结论**落盘**：

```powershell
.\dist\StarportDictionary.exe --smoke
# 退出码 0 = 通过；结论在：
#   %LOCALAPPDATA%\StarportDictionary\smoke\smoke.json
#   %LOCALAPPDATA%\StarportDictionary\smoke\detail.png
```

`smoke.json` 会记录：载入条目数、查询、最佳命中、候选数、详情是否渲染、截图路径。

**实测结果（2026-11-22）：**

```json
{"ok": true, "entry_count": 137, "module_count": 26, "errors": [],
 "query": "判断一个文件的后缀名", "best_entry_id": "py.fs.check_extension",
 "hit_count": 8, "detail_rendered": true}
```

## 验证「双击能开」的正确方法

`--onefile` 会**启动两个进程**（引导器 + 真正的应用），窗口属于**子进程**：

```powershell
$p = Start-Process .\dist\StarportDictionary.exe -PassThru
Start-Sleep 12
Get-Process -Name StarportDictionary | Select-Object Id,MainWindowTitle
# 应该看到 MainWindowTitle = Starport Dictionary 0.1.0
```

只看 `$p.MainWindowTitle` 会得到空字符串——那是引导器进程，**不是窗口没开**。

## 坑

| 现象 | 原因 | 处理 |
|---|---|---|
| 窗口一片白 | QSS 没打包进去 | `--add-data` 补 resources |
| 启动报「知识库加载失败」 | knowledge-packs 没打包 | 检查 `--add-data` 与 `paths.packs_root()` |
| 中文变方块 | 缺字体（离屏渲染时常见） | exe 用系统字体正常；离屏截图设 `QT_QPA_FONTDIR=C:\Windows\Fonts` |
| 启动慢 3–5 秒 | onefile 每次都要解压到临时目录 | 可接受；要更快改 `--onedir` |
| 用户数据找不到 | 打包后写到 `%LOCALAPPDATA%\StarportDictionary` | 开发期写仓库内 `data/`，见 `paths.py` |

## 用户数据位置

| 内容 | 路径 |
|---|---|
| 反馈 | `%LOCALAPPDATA%\StarportDictionary\feedback.jsonl` |
| 最近搜索 | `%LOCALAPPDATA%\StarportDictionary\recent.json` |
| 自检产物 | `%LOCALAPPDATA%\StarportDictionary\smoke\` |
