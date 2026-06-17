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

## 防溢出规范 (Overflow Prevention)

**这是生成 .tex 时必须遵守的硬性规则。** Beamer 幻灯片空间有限（16:9 约 13.3"×7.5"），违反以下限制大概率导致内容溢出。

### 硬性内容量限制

| 内容类型 | 单页上限 | 超标处理 |
|----------|----------|----------|
| itemize/enumerate 条目 | ≤5 条（每条 ≤2 行） | 拆分到多页，或用 `\pause` 分步显示 |
| 纯文本段落 | ≤8 行（含空行） | 缩写句子，删冗余词 |
| block/alertblock | ≤3 个 | 多余的移到下一页 |
| 表格列数 | ≤4 列 | 用 `\footnotesize` 缩小，或拆成两个表格 |
| 表格行数 | ≤8 行 | 用 `\footnotesize` 缩小，或拆到多页 |
| 图片 | `width≤0.85\textwidth`, `height≤0.75\textheight` | 减小 width 参数 |
| 代码行 | ≤15 行，每行 ≤80 字符 | 用 `\tiny` 缩小，或 `allowframebreaks` 分页 |
| 双栏每栏条目 | ≤4 条（每栏） | 拆为两页分别展示 |

### 内容过多时的自动处理策略

**按优先级依次尝试，直到内容能在 1 页放下：**

1. **删冗余** — 去掉"的"/"了"/"是"等虚词，精简单词
2. **缩字号** — 在 frame 环境内临时缩小：
   ```latex
   \begin{frame}{标题}
     \small          % 或 \footnotesize
     ...内容...
   \end{frame}
   ```
3. **缩行距** — 列表太挤时用 `topsep=0pt, itemsep=2pt`：
   ```latex
   \begin{itemize}
     \setlength{\itemsep}{2pt}
     \setlength{\topsep}{0pt}
     \item ...
   \end{itemize}
   ```
4. **拆分多页** — 添加分页标题：
   ```latex
   \begin{frame}{方法概述 (1/2)}
     ...
   \end{frame}
   \begin{frame}{方法概述 (2/2)}
     ...
   \end{frame}
   ```
5. **长内容自动分页** — 仅限参考文献/附录，正文谨慎使用：
   ```latex
   \begin{frame}[allowframebreaks]{参考文献}
   ```

### 常见溢出场景与预设方案

| 场景 | 症状 | 预设方案 |
|------|------|----------|
| 6 个要点 + 1 个公式 | 底部公式被截 | `\footnotesize` + `itemsep=0pt`，公式用行内 `$...$` |
| 5 列宽表 | 右边超出边框 | `\footnotesize` + 缩小列间距 `\tabcolsep=3pt` |
| 三栏布局 | 内容重叠 | 调为 `0.32\textwidth` × 3，间距 `0.02\textwidth` |
| 代码 >15 行 | 底部行不可见 | `\tiny` + `numbers=none`，或 `allowframebreaks` |
| 图片 + 解释文字 | 文字被挤出 | 图片 `height=0.55\textheight`，文字单独放另一页 |
| 双 block + 大表格 | 表格太挤 | 删掉一个 block，或表格用 `\scriptsize` |

### 生成 .tex 时的自检清单

每页 frame 写完，逐一确认：
- [ ] itemize ≤5 条？
- [ ] block ≤3 个？
- [ ] 表格 ≤4 列、≤8 行？
- [ ] 图片 `width ≤0.85\textwidth` 或 `height ≤0.75\textheight`？
- [ ] 无"6 个小 block 叠罗汉"的 layout？

**如果任一检查不通过 → 先尝试缩小/精简，仍不行 → 拆分多页。**

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
