# Beamer .tex 编写指南

本指南帮助 Claude 将用户提供的内容转化为高质量的 Beamer .tex 源码。

## 内容转换流程

1. **提取结构**: 从用户材料中提取标题、章节、关键论点
2. **构建 claim spine**: 每页幻灯片一个核心论点
3. **选择 frame 类型**: 根据内容选择最合适的 frame 布局
4. **生成 .tex**: 基于模板填充内容

## Frame 类型速查

### 文本列表帧
```latex
\begin{frame}{标题}
  \begin{itemize}
    \item 第一点
    \item 第二点
  \end{itemize}
\end{frame}
```

### 双栏帧
```latex
\begin{frame}{标题}
  \begin{columns}[T]
    \begin{column}{0.48\textwidth}
      左栏内容
    \end{column}
    \begin{column}{0.48\textwidth}
      右栏内容
    \end{column}
  \end{columns}
\end{frame}
```

### 表格帧
```latex
\begin{frame}{表格标题}
  \begin{table}
    \centering
    \begin{tabular}{lcc}
      \toprule
      \textbf{方法} & \textbf{A} & \textbf{B} \\
      \midrule
      方法1 & 85.2 & 72.1 \\
      方法2 & 87.6 & 74.3 \\
      \bottomrule
    \end{tabular}
  \end{table}
\end{frame}
```

### 图片帧
```latex
\begin{frame}{图片标题}
  \begin{center}
    \includegraphics[width=0.8\textwidth]{image.png}
  \end{center}
\end{frame}
```

### 强调帧（block/alertblock/exampleblock）
```latex
\begin{frame}{标题}
  \begin{block}{普通强调}
    普通内容
  \end{block}
  \begin{alertblock}{警告}
    需要注意的内容
  \end{alertblock}
\end{frame}
```

## 常用 LaTeX 元素

### 数学
```latex
行内公式: $E = mc^2$
编号公式: \begin{equation} ... \end{equation}
对齐公式: \begin{align*} ... \end{align*}
```

### 高亮
```latex
\alert{红色强调文字}
\textbf{粗体}
```

## SJTUBeamer 定制配置

### 隐藏导航栏超链接（仅保留页码）

SJTUBeamer 右下角默认显示导航超链接图标（前后页箭头等）和页码。去掉图标只保留页码：

```latex
\setbeamertemplate{navigation symbols}{\insertframenumber/\inserttotalframenumber}
```

**注意**：不要用 `{}` 清空，否则页码也会丢失（SJTUBeamer 的页码在 navigation symbols 区域内）。

### 移除封面机构名（解决标题溢出）

`\institute{...}` 会占用标题页空间，常导致标题文字被压缩或溢出。建议直接删除 `\institute` 行。

```latex
% 删除这行：
% \institute[SJTU]{上海交通大学}
```

### 移除自动结束页

SJTUBeamer 的 `\makebottom` 命令会生成一张中文"谢谢"结束页。英文 PPT 必须删除此命令。

如需尾页重复封面：
```latex
% 删掉 \makebottom，改用：
\maketitle
\end{document}
```

### 中英文版本同步

如果需要中英文两个版本，共用同一份图片资源：
```latex
\graphicspath{{images/}{figures/}}
```

**关键**：更新图片后，必须检查 `\graphicspath` 中所有目录下的同名文件，覆盖旧版缓存。LaTeX 按 `\graphicspath` 顺序搜索，第一个匹配到的文件被使用。

## 常见陷阱

1. **中文编码**: 使用 `ctexbeamer` 文档类，不要用 `beamer`
2. **图片路径**: 使用 `\graphicspath` 统一设置搜索路径，注意缓存覆盖
3. **标题**: 使用结论式标题（"方法 A 提升了 15% 精度"），而非话题式标题（"实验结果"）
4. **特殊字符**: LaTeX 中 `%` `#` `&` `_` `{` `}` 需要转义

## 内容精简原则

Beamer 不是 Word。每页幻灯片应该：
- 只传达 **一个核心信息**
- 文字尽量简短（每个要点 ≤2 行）
- 能用图表说明的不用纯文字
- 能用关键词的不用完整句子
- 详细内容放在备注或附录
