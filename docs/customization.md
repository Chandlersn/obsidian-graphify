# 自定义配置

## 修改颜色

编辑 `config.yaml`：

```yaml
graph:
  primary_color: "#5e6ad2"  # 主色调
  
  colors:
    System: "#f7f8f8"       # 白色
    Knowledge: "#5e6ad2"    # 蓝色
    Projects: "#4DAF73"     # 绿色
    Materials: "#E6A23C"    # 橙色
    AI-ML: "#5e6ad2"        # 蓝色
    Architecture: "#409EFF" # 浅蓝
    Tools: "#67C23A"        # 绿色
```

---

## 修改主题

```yaml
graph:
  theme: "dark"  # 或 "light"
```

或直接在界面点击 Sidebar 的"主题"按钮切换。

---

## 修改节点标签长度

```yaml
graph:
  max_label_length: 12  # 最多 12 个字符
```

超过限制会截断显示 `...`

---

## 添加新分类

1. 在 `config.yaml` 添加颜色：

```yaml
graph:
  colors:
    Research: "#9B59B6"   # 新分类：紫色
```

2. 创建对应文件夹：

```bash
mkdir -p obsidian-notes/02-Knowledge/Research
```

3. 在文件夹中创建笔记，自动归类

---

## 修改更新间隔

```yaml
update:
  interval: 3  # 秒，防抖间隔
```

值越小更新越快，但可能频繁触发

---

## 禁用功能

```yaml
features:
  path_tracing: false    # 关闭路径追踪
  heat_map: false        # 关闭热度统计
  influence: false       # 关闭影响力分析
```

---

## 修改字体

在 `graph_fixed_beautiful.html` 中修改 CSS：

```css
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    /* 或换成其他字体 */
    font-family: 'Source Sans Pro', sans-serif;
}
```

---

## 修改布局

### Sidebar 宽度

```css
.sidebar {
    width: 64px;  /* 默认 64px */
    /* 改成更宽 */
    width: 80px;
}
```

### 节点大小

在 vis-network 配置中：

```javascript
nodes: {
    size: 25,  /* 默认 25 */
    /* 改成更大 */
    size: 35,
}
```

---

## 自定义 CSS 样式

创建 `custom.css`：

```css
/* 自定义节点样式 */
.vis-network .node {
    border-radius: 12px;
}

/* 自定义弹窗样式 */
.modal-overlay {
    background: rgba(0, 0, 0, 0.8);
}

/* 自定义筛选按钮 */
.filter-btn {
    border-radius: 8px;
}
```

然后在 HTML 中引入：

```html
<link rel="stylesheet" href="custom.css">
```

---

## 翻译界面语言

在 `graph_fixed_beautiful.html` 中修改文本：

```javascript
// 分类翻译
function translateCategory(cat) {
    const map = {
        'System': '系统',       // 中文
        'Knowledge': '知识',
        // 或改成其他语言
        'System': 'System',     // 英文
        'Knowledge': 'Knowledge',
    };
    return map[cat] || cat;
}
```

---

## 高级自定义

### 添加新功能按钮

在 Sidebar HTML 中添加：

```html
<button class="sidebar-btn" onclick="yourFunction()">
    <svg>...</svg>
    <span>新功能</span>
</button>
```

### 自定义算法

修改路径追踪算法（DFS vs BFS）：

```javascript
// 当前：BFS（广度优先）
function findShortestPath(start, end) {
    // BFS 实现...
}

// 改成 DFS（深度优先）
function findPathDFS(start, end) {
    // DFS 实现...
}
```

---

## 配置文件完整示例

```yaml
# 完整配置示例

obsidian:
  vault_path: "/Users/yourname/Documents/obsidian-notes"
  auto_update: true

graph:
  theme: "dark"
  primary_color: "#5e6ad2"
  max_label_length: 12
  
  colors:
    System: "#f7f8f8"
    Knowledge: "#5e6ad2"
    Projects: "#4DAF73"
    Materials: "#E6A23C"
    General: "#909399"
    AI-ML: "#5e6ad2"
    Architecture: "#409EFF"
    Tools: "#67C23A"
    Research: "#9B59B6"
    DevOps: "#E74C3C"

update:
  enabled: true
  interval: 3
  file_types:
    - ".md"

feishu:
  enabled: false
  save_dir: "04-Materials/Feishu"

features:
  filter: true
  path_tracing: true
  heat_map: true
  influence: true
  island_detection: true
  export_png: true
```