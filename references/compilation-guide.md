# 编译指南

## 环境要求

| 组件 | 用途 | 安装方式 |
|------|------|----------|
| MiKTeX | LaTeX 发行版 | `winget install MiKTeX.MiKTeX` |
| XeLaTeX | 编译器（支持中文） | MiKTeX 自带 |

## MiKTeX 配置

```powershell
initexmf --set-config-value=[MPM]AutoInstall=1
```

确保首次编译时缺失包自动下载，避免交互式弹窗（Claude Code 中无法交互）。

## 编译命令

### 推荐方式（避免 PDF 被锁定）

Windows PDF 阅读器会锁定正在查看的 PDF，导致 xelatex 无法写入。用 `-jobname` 编译到临时名再覆盖：

```bash
xelatex -interaction=nonstopmode -jobname=tmp main.tex
mv -f tmp.pdf main.pdf
```

### 清理编译产物

```bash
latexmk -C  # 清理所有生成文件
```

## 中文字体

模板使用 `fontset=windows`，映射关系：

| ctex 名称 | Windows 字体 |
|-----------|-------------|
| 宋体 | SimSun |
| 黑体 | SimHei |
| 楷体 | KaiTi |

## 故障排查

### PDF 被锁定 (Permission denied)

**现象**：编译报错 `Permission denied: 'slides.pdf'`，或 pdf_to_pptx 无法读取。

**原因**：Windows PDF 阅读器（Edge/Adobe Reader）正在预览该文件。

**方案 A**（推荐）：用 `-jobname` 编译到临时名：
```bash
xelatex -interaction=nonstopmode -jobname=tmp slides.tex
mv -f tmp.pdf slides.pdf
```

**方案 B**：关闭 PDF 阅读器后重试。

### 图片缓存未更新

**现象**：重新生成了图片，但编译后的 PDF 里仍然是旧图。

**原因**：`\graphicspath` 按顺序搜索多个目录，在非预期目录中找到了同名旧文件。

**解决**：
1. 用 `find . -name "目标图片名"` 找到所有副本
2. 把新图覆盖到所有位置，或删除旧缓存
3. 重新编译

### 缺失包

```
! LaTeX Error: File `xxx.sty' not found.
```

**解决**：AutoInstall 已启用时会自动下载。否则手动：
```powershell
mpm --install <package-name>
```

### 字体未找到

```
! fontspec error: font not found
```

**解决**：确认系统安装了 SimSun/SimHei，使用 `fontset=windows`。

### 编码错误

```
! Package inputenc Error: Unicode character
```

**解决**：使用 XeLaTeX（不是 pdfLaTeX），文件编码为 UTF-8。

## 日志分析

编译失败时，查看 `.log` 文件最后 50 行，关注以 `!` 开头的错误行：

```bash
grep "^!" main.log | tail -10
```

常见错误级别：
- `!` = 致命错误，编译停止
- `Warning` = 警告，通常不影响输出
- `Overfull \hbox` = 内容溢出，检查该页内容是否过多
