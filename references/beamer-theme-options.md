# SJTUBeamer 主题选项参考

## 语法

```latex
\usetheme[选项1,选项2,...]{sjtubeamer}
```

选项通过逗号分隔传入。不指定的选项使用默认值。

## 选项分类

### 封面样式 (Cover Style)

| 选项 | 效果 | 适用场景 |
|------|------|----------|
| `maxplus` | 现代全幅封面，支持头图背景 | 正式学术报告、研讨会、公开演讲 |
| `max` | 经典渐变封面，带背景图案 | 学术报告、课程展示 |
| `min` | 极简封面，无背景图 | 简洁风格、组会汇报 |

### 主色调 (Color Scheme)

| 选项 | 效果 |
|------|------|
| `red` | 交大红为主色调，红色标题栏和强调色 |
| `blue` | 交大蓝为主色调，蓝色标题栏和强调色 |

### 亮度模式 (Brightness)

| 选项 | 效果 |
|------|------|
| `light` | 浅色背景，适合日常投影 |
| `dark` | 深色背景，适合正式场合或大屏幕 |

### 导航栏样式 (Navigation Bar)

| 选项 | 效果描述 |
|------|----------|
| `miniframes` | 顶部小圆点导航，每个 section 一组点 |
| `infolines` | 底部信息栏，显示节/小节/页码 |
| `sidebar` | 左侧边栏导航 |
| `default` | Beamer 默认导航栏 |
| `smoothbars` | 平滑过渡的顶部导航条 |
| `split` | 分割式导航 |
| `shadow` | 带阴影的导航 |
| `tree` | 树形导航结构 |
| `smoothtree` | 平滑树形导航 |

### 校徽位置 (Logo Position)

| 选项 | 效果 |
|------|------|
| `topright` | 校徽在右上角 |
| `bottomright` | 校徽在右下角 |

## 推荐组合

### 正式学术报告
```latex
\usetheme[maxplus,red,dark,miniframes]{sjtubeamer}
```

### 清爽日常风格
```latex
\usetheme[min,blue,light,smoothbars]{sjtubeamer}
```

### 答辩
```latex
\usetheme[max,red,dark,infolines]{sjtubeamer}
```

### 研讨会
```latex
\usetheme[maxplus,blue,dark,miniframes]{sjtubeamer}
```

### 组会汇报
```latex
\usetheme[min,blue,light,default]{sjtubeamer}
```

### 双语展示
```latex
\usetheme[maxplus,red,light,miniframes]{sjtubeamer}
```

## 注意事项

1. `max` 主题默认带正文背景图，如需关闭：`\setbeamertemplate{background}{}`
2. 首次编译某些组合时，MiKTeX 可能需要下载额外的颜色/字体包
3. `dark` 模式下代码块和公式的对比度已优化，无需额外设置
