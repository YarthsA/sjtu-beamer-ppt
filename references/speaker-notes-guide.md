# 讲稿备注生成指南

PPTX 转换完成后，用 python-pptx 为每页幻灯片添加演讲备注，方便汇报时参考。

## 时间分配原则

按演讲总时长分配各页讲稿比例：

| 页类型 | 建议时长 | 15分钟示例 |
|--------|----------|-----------|
| 封面 | 15-25s | 20s |
| 目录 | 10-15s | 10s |
| Section divider | 5-10s | 5s |
| 普通内容页 | 30-60s | 40s |
| 总结页 | 30-45s | 35s |
| 结尾致谢 | 10-15s | 10s |

**公式**：总页数 N，可用时间 T 秒 → 普通页 = (T - 封面目录结尾开销) / (N - 过渡页数)

## 讲稿撰写原则

- 每页 **2-4 句**，不要念 PPT 原文
- 过渡页（Section divider）一句话带过
- 图表页：先解释坐标轴，再指关键趋势，最后总结结论
- 首尾页用口语化开场白/结束语

## 实现方式

直接用 python-pptx 的 `slide.notes_slide` API：

```python
from pptx import Presentation

NOTES_CN = {
    1: "各位老师好，...",
    2: "报告分为...",
    # ...
}

prs = Presentation("slides.pptx")
for i, slide in enumerate(prs.slides):
    page = i + 1
    note_text = NOTES_CN.get(page, "")
    if note_text:
        ns = slide.notes_slide
        ns.notes_text_frame.clear()
        ns.notes_text_frame.text = note_text
prs.save("slides.pptx")
```

## 中英文讲稿

如果需要中英文两个版本，通常的做法是：
1. 分别编译中文和英文 PDF
2. 分别转换为 PPTX
3. 分别添加对应的中/英文备注

不要试图在一个 PPTX 里混合中英文备注。

## 注意事项

- 备注脚本用完后删除，不要留在工作目录
- 先转换 PPTX 再加备注 —— 顺序不能反（转换会覆盖 PPTX）
- 讲稿文本中的 `"` 和 `\` 等字符需要转义或用三引号包裹
