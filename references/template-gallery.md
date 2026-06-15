# 预设主题组合

根据使用场景选择合适的预设。将预设的主题选项填入 `\usetheme[...]{sjtubeamer}` 即可。

## 预设列表

### academic-formal — 正式学术报告
```latex
\usetheme[maxplus,red,dark,miniframes]{sjtubeamer}
```
- **场景**: 学术会议报告、成果汇报、基金申请汇报
- **特点**: 现代全幅封面，红色主调，深色背景显庄重，顶部圆点导航清晰

### academic-clean — 清爽学术风格
```latex
\usetheme[min,blue,light,smoothbars]{sjtubeamer}
```
- **场景**: 课程展示、读书报告、文献调研汇报
- **特点**: 极简封面，蓝色清新，浅色背景适合长时间阅读

### defense — 毕业答辩
```latex
\usetheme[max,red,dark,infolines]{sjtubeamer}
```
- **场景**: 本科/硕士/博士毕业答辩
- **特点**: 经典渐变封面，红色主调庄重大方，底部信息栏显示进度

### group-meeting — 组会进度汇报
```latex
\usetheme[min,blue,light,default]{sjtubeamer}
```
- **场景**: 课题组周会、双周会
- **特点**: 极简高效，快速制作，重点突出

### seminar — 现代研讨会
```latex
\usetheme[maxplus,blue,dark,miniframes]{sjtubeamer}
```
- **场景**: 学术沙龙、技术分享、跨组交流
- **特点**: 蓝色科技感，深色背景现代感强

### bilingual — 中英双语
```latex
\usetheme[maxplus,red,light,miniframes]{sjtubeamer}
```
- **场景**: 国际学术交流、中英双语报告
- **特点**: 浅色背景对双语排版友好，红色标识校徽辨识度高

## 快速选择指南

| 你的场景 | 推荐预设 |
|----------|----------|
| 我要做毕业答辩 | `defense` |
| 课题组组会汇报 | `group-meeting` |
| 学术会议做报告 | `academic-formal` |
| 课程作业展示 | `academic-clean` |
| 和其他组交流 | `seminar` |
| 面向国际听众 | `bilingual` |
| 不确定 | `academic-formal`（最通用） |
