# 编译指南

## 环境要求

| 组件 | 用途 | 安装方式 |
|------|------|----------|
| MiKTeX | LaTeX 发行版 | `winget install MiKTeX.MiKTeX` |
| XeLaTeX | 编译器（支持中文） | MiKTeX 自带 |
| latexmk | 自动化编译工具 | `mpm --install latexmk` |

## MiKTeX 关键配置

### 启用自动安装缺失包

```powershell
initexmf --set-config-value=[MPM]AutoInstall=1
```

这确保编译时遇到缺失的包会自动下载，而不是弹出交互式对话框（在 Claude Code 中无法交互）。

### 手动安装常用包

```powershell
mpm --install ctex
mpm --install beamer
mpm --install cjk
mpm --install latexmk
initexmf --update-config
```

## 编译命令

### 推荐方式（通过 skill 脚本）

```powershell
pwsh -File scripts/compile_tex.ps1 -TexFile main.tex -WorkDir /path/to/project
```

### 手动编译

```bash
# 方式一：使用 latexmk（推荐，自动处理多次编译）
latexmk -xelatex -interaction=nonstopmode main.tex

# 方式二：手动 XeLaTeX
xelatex main.tex
xelatex main.tex  # 运行两次以解析交叉引用
```

### 清理编译产物

```bash
latexmk -C  # 清理所有生成文件
```

## 中文字体

模板默认使用 `fontset=windows`，映射关系：

| ctex 名称 | Windows 字体 |
|-----------|-------------|
| 宋体 | SimSun |
| 黑体 | SimHei |
| 楷体 | KaiTi |
| 仿宋 | FangSong |

如果需要其他字体选项：
- `fontset=fandol`: 使用 Fandol 开源字体（TeX 自带）
- `fontset=ubuntu`: 用于在线平台（如 TeXPage）

## 常见编译错误

### 1. Missing package

```
! LaTeX Error: File `xxx.sty' not found.
```

**解决**: MiKTeX 会自动下载（如果 AutoInstall 已启用）。否则手动安装：
```powershell
mpm --install <package-name>
```

### 2. 字体未找到

```
! fontspec error: font not found
```

**解决**: 确认使用 `fontset=windows`，且系统安装了 SimSun/SimHei。

### 3. 编码错误

```
! Package inputenc Error: Unicode character
```

**解决**: 确保使用 XeLaTeX（不是 pdfLaTeX），文件编码为 UTF-8。

### 4. fragile frame 缺少

```
! Missing \endcsname inserted
```

**解决**: 包含代码块的 frame 需要加 `[fragile]` 选项：
```latex
\begin{frame}[fragile]{标题}
```

### 5. 路径含空格

latexmk 可能在含空格的路径下出错。解决：将项目放在无空格路径下，或使用短路径名。

## 首次编译注意

首次编译新项目时，MiKTeX 需要下载多个依赖包（ctex、cjk、beamer 等），可能需要 **5-15 分钟**。后续编译会很快。

如果编译卡住，检查是否弹出了 MiKTeX Package Manager 的交互式对话框——AutoInstall 应该能避免这种情况。

## 日志分析

编译失败时，查看 `.log` 文件最后 50 行，关注以 `!` 开头的错误行：

```bash
grep "^!" main.log | tail -10
```

常见错误级别：
- `!` = 致命错误，编译停止
- `Warning` = 警告，通常不影响输出
- `Overfull \hbox` = 内容溢出，检查该页内容是否过多
