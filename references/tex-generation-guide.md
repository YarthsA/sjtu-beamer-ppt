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

### 公式帧
```latex
\begin{frame}{公式标题}
  \begin{equation}
    E = mc^2
  \end{equation}
\end{frame}
```

### 代码帧（必须加 `[fragile]`）
```latex
\begin{frame}[fragile]{代码标题}
  \begin{codeblock}[language=Python]{Python}
import numpy as np
  \end{codeblock}
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
  \begin{figure}
    \centering
    \includegraphics[width=0.8\textwidth]{image.png}
    \caption{图片说明}
  \end{figure}
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
  \begin{exampleblock}{示例}
    示例内容
  \end{exampleblock}
\end{frame}
```

### 长内容帧（自动分页）
```latex
\begin{frame}[allowframebreaks]{参考文献}
  \printbibliography[heading=none]
\end{frame}
```

## 覆盖与动画

### 逐步显示（pause）
```latex
\begin{frame}{逐步显示}
  第一步内容 \pause
  第二步内容 \pause
  第三步内容
\end{frame}
```

### 条件显示
```latex
\begin{frame}{条件显示}
  \only<1>{仅第 1 页显示}
  \only<2>{仅第 2 页显示}
  \uncover<1-2>{第 1-2 页显示}
  \visible<3>{从第 3 页开始可见}
\end{frame}
```

## 常用 LaTeX 元素

### 数学
```latex
行内公式: $E = mc^2$
编号公式: \begin{equation} ... \end{equation}
对齐公式: \begin{align*} ... \end{align*}
```

### 列表
```latex
\begin{itemize}       % 无序列表
\begin{enumerate}     % 有序列表
\begin{description}   % 定义列表
```

### 高亮
```latex
\alert{红色强调文字}
\textbf{粗体}
\textit{斜体}
\highlight{主题色高亮}  % SJTUBeamer 特有
```

## 常见陷阱

1. **代码帧必须加 `[fragile]`**: 含有 `verbatim`、`lstlisting`、`codeblock` 的 frame 必须加 `[fragile]` 选项
2. **中文编码**: 使用 `ctexbeamer` 文档类，不要用 `beamer`
3. **图片路径**: 使用 `\graphicspath{{figures/}}` 统一设置图片搜索路径
4. **特殊字符**: LaTeX 中 `%` `#` `&` `_` `{` `}` 需要转义
5. **行距**: Beamer 内容空间有限，避免一个 frame 塞太多内容（建议 ≤5 个要点）
6. **标题**: 建议使用结论式标题（"方法 A 提升了 15% 精度"），而非话题式标题（"实验结果"）

## 内容精简原则

Beamer 不是 Word。每页幻灯片应该：
- 只传达 **一个核心信息**
- 文字尽量简短（每个要点 ≤2 行）
- 能用图表说明的不用纯文字
- 能用关键词的不用完整句子
- 详细内容放在备注或附录
