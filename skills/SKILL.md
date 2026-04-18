***

name: graphify-knowledge-graph-ui
description: "Create interactive knowledge graph visualizations with Graphify. 将 Obsidian 笔记变成可视化知识图谱，支持节点点击、路径追踪、热度统计、孤岛检测、主题切换。Use when user mentions "知识图谱", "graphify", "可视化笔记", "笔记图谱", "Obsidian图谱", "知识网络", "graph setup", "更新图谱", "同步笔记"."
tags: \[note-taking, obsidian, visualization, knowledge-graph, graphify]
version: 1.0.0
category: creative
source: <https://github.com/Chandlersn/obsidian-graphify>
linked\_files:
scripts/update\_graph\_html.py: 图谱数据生成脚本
scripts/auto\_update.py: 自动更新守护进程
templates/knowledge-graph-ui.html: 图谱可视化模板
------------------------------------------

# Graphify Knowledge Graph UI

> 将 Obsidian 笔记变成一张可视化的知识图谱，让知识真正「连起来」。
> 核心理念：**笔记 → 解析链接 → 构建图谱 → 可视化 → 发现脉络 → 建立新链接**
> GitHub: <https://github.com/Chandlersn/obsidian-graphify>

***

## 设计哲学

Graphify 的核心循环：

```
笔记 → 解析链接 → 构建图谱 → 可视化 → 发现脉络 → 建立新链接 → 笔记
```

一个正向循环。写得越多，图谱越密；图谱越密，发现越多。

与传统笔记软件的区别：

- **存储 vs 连接** — 传统软件只解决存储，Graphify 解决连接
- **搜索 vs 发现** — 搜索需要知道关键词，图谱可以发现不知道的
- **孤岛 vs 网络** — 孤岛之间没有路，节点之间有路径

***

## 前置条件

| 条件           | 检查方式                       |
| ------------ | -------------------------- |
| Obsidian 已安装 | 打开 Obsidian，确认 vault 存在    |
| Python 3.x   | `python --version` 应返回 3.x |
| pip 可用       | `pip --version`            |
| vault 路径可访问  | `ls /path/to/vault`        |

***

## 工作流程

### Phase 0: 环境准备

```
Step 0.1: 确认 vault 路径
  - 询问用户 vault 位置
  - WSL 环境：通常在 /mnt/d/obsidian-notes 或类似路径

Step 0.2: 检查现有 .graphify 目录
  - 如果存在 → 确认是否更新
  - 如果不存在 → 创建新目录
```

### Phase 1: 安装依赖

```
Step 1.1: 安装 Python 包
  pip install watchdog

Step 1.2: 验证安装
  python -c "import watchdog; print('OK')"
```

### Phase 2: 配置系统

```
Step 2.1: 创建 .graphify 目录
  mkdir -p {vault_path}/.graphify

Step 2.2: 复制核心文件
  - graph_fixed_beautiful.html → 主界面
  - update_graph_html.py → 数据生成
  - auto_update.py → 自动更新
  - vis-network.min.js → 可视化库

Step 2.3: 配置 vault 路径
  编辑 update_graph_html.py:
    OBSIDIAN_VAULT = "{vault_path}"
```

### Phase 3: 生成图谱

```
Step 3.1: 执行首次更新
  python {vault_path}/.graphify/update_graph_html.py {vault_path}

Step 3.2: 打开图谱页面
  browser: file://{vault_path}/.graphify/graph_fixed_beautiful.html

Step 3.3: 验证节点数量
  - 检查图谱是否显示笔记节点
  - 检查 Wiki 链接是否显示连线
```

### Phase 4: 启动自动更新（可选）

```
Step 4.1: 启动守护进程
  python {vault_path}/.graphify/auto_update.py {vault_path} &

Step 4.2: 测试实时更新
  - 创建新笔记，添加 Wiki 链接
  - 观察图谱是否自动更新
```

***

## 检查点设计

| 检查点        | 用户确认内容        |
| ---------- | ------------- |
| Phase 0 结束 | vault 路径是否正确？ |
| Phase 2 结束 | 是否继续生成图谱？     |
| Phase 3 结束 | 图谱显示是否正常？     |
| Phase 4 开始 | 是否启动自动更新？     |

**重要决策必须用户确认后再继续。**

***

## 输入/输出规格

### 输入

| 参数            | 类型   | 说明                | 示例                      |
| ------------- | ---- | ----------------- | ----------------------- |
| `vault_path`  | str  | Obsidian vault 路径 | `/mnt/d/obsidian-notes` |
| `auto_update` | bool | 是否启动自动更新          | `true` / `false`        |

### 输出

| 文件                                     | 说明       |
| -------------------------------------- | -------- |
| `.graphify/graph_fixed_beautiful.html` | 图谱可视化页面  |
| `.graphify/graph_data.json`            | 内嵌图谱数据   |
| `.graphify/update_graph_html.py`       | 数据生成脚本   |
| `.graphify/auto_update.py`             | 自动更新守护进程 |

***

## 核心功能

| #  | 功能     | 实现方式                                     |
| -- | ------ | ---------------------------------------- |
| 01 | 节点点击   | vis-network `click` event + Obsidian URI |
| 02 | 路径追踪   | BFS 最短路径算法                               |
| 03 | 热度统计   | localStorage 点击计数                        |
| 04 | 孤岛检测   | degree === 0 节点高亮                        |
| 05 | 影响力分析  | PageRank 简化版                             |
| 06 | 分类筛选   | 动态渲染分类按钮                                 |
| 07 | 快速搜索   | Ctrl+K 输入框                               |
| 08 | 主题切换   | CSS 变量 + localStorage                    |
| 09 | PNG 导出 | canvas.toDataURL()                       |
| 10 | 飞书导入   | feishu\_importer.py                      |

***

## 错误处理

| 错误          | 原因               | 解决方案                   |
| ----------- | ---------------- | ---------------------- |
| Python 脚本报错 | 缺少 watchdog      | `pip install watchdog` |
| 图谱无节点       | vault\_path 错误   | 检查路径配置                 |
| Wiki 链接不显示  | 链接笔记不存在          | 创建目标笔记                 |
| 自动更新不工作     | 路径参数错误           | 检查启动参数                 |
| 页面空白        | vis-network 加载失败 | 检查 CDN/本地文件            |
| 跨域错误        | file:// 协议限制     | 使用本地 vis-network 文件    |

***

## 自定义配置

### 修改主题颜色

编辑 `graph_fixed_beautiful.html`:

```css
/* 深色主题 */
--bg-color: #0f0f10;
--node-color: #e8590c;
--edge-color: rgba(255,255,255,0.15);

/* 浅色主题 */
--bg-color: #fafaf5;
--node-color: #e8590c;
--edge-color: rgba(0,0,0,0.1);
```

### 添加分类

编辑 `update_graph_html.py`:

```python
CATEGORY_COLORS = {
    "AI-ML": "#10b981",
    "Tools": "#3b82f6",
    "Projects": "#f59e0b",
    "Materials": "#8b5cf6",
}
```

***

## 使用示例

### 用户：帮我搭建知识图谱系统

```
→ Phase 0-4 完整流程
→ 确认 vault 路径后执行安装
→ 完成后打开图谱页面展示
```

### 用户：更新图谱

```
→ 执行 update_graph_html.py
→ 刷新图谱页面
→ 报告新增节点和链接数量
```

### 用户：启动自动更新

```
→ 启动 auto_update.py 守护进程
→ 监控 vault 变化
→ 实时更新图谱
```

***

## 注意事项

1. **路径一致性** — Windows/WSL 路径转换：`D:\path` → `/mnt/d/path`
2. **文件编码** — 笔记必须 UTF-8 编码
3. **链接格式** — 只识别 `[[笔记名]]` 格式
4. **性能限制** — 500+ 节点建议关闭物理模拟
5. **本地存储** — 热度数据保存在 localStorage，清除浏览器数据会丢失

***

## 设计灵感

> 知识的本质是网络，而非层级。

（Ted Nelson: "Everything is deeply intertwingled."）

本 skill 的对应关系：

- **存储** → Obsidian vault
- **连接** → Wiki 链接 `[[笔记名]]`
- **可视化** → vis-network 图谱
- **发现** → 路径追踪、孤岛检测、影响力分析

***

## 参考文档

- [快速开始](../docs/getting-started.md)
- [文件夹结构](../docs/folder-structure.md)
- [功能详解](../docs/features.md)
- [自定义配置](../docs/customization.md)
- [常见问题](../docs/troubleshooting.md)

***

## 相关 Skills

- `obsidian` — Obsidian vault 基础操作
- `wechat-article-scraper` — 微信文章收录到笔记库
- `feishu` — 飞书消息导入（可选）

