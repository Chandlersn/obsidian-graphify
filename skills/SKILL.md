---
name: graphify-knowledge-graph-ui
description: "将 Obsidian 笔记变成可视化知识图谱。支持笔记自动化收录、Wiki链接建立、图谱可视化更新。Use when user mentions \"知识图谱\", \"graphify\", \"可视化笔记\", \"笔记图谱\", \"收录文章\", \"笔记收录\", \"更新图谱\", \"同步笔记\", \"wiki链接\"."
tags: [note-taking, obsidian, visualization, knowledge-graph, graphify]
version: 2.1.0
category: creative
source: https://github.com/Chandlersn/obsidian-graphify
linked_files:
  scripts/note_collector.py: 核心收录脚本
  scripts/wiki_link_builder.py: Wiki链接建立脚本
  scripts/update_graph_html.py: 图谱数据生成脚本
  scripts/graphify.sh: 快捷入口脚本
  templates/通用文章模板.md: 元数据模板
---

# Graphify Knowledge Graph UI

> 将 Obsidian 笔记变成一张可视化的知识图谱，让知识真正「连起来」。
> 核心理念：**笔记 → 解析链接 → 构建图谱 → 可视化 → 发现脉络 → 建立新链接**

---

## 工具索引

所有脚本位于 `/mnt/d/obsidian-notes/.graphify/github-repo/skills/scripts/`：

| 工具 | Wiki链接 | 功能 |
|------|----------|------|
| [[note_collector.py]] | 收录流程核心 | 分析→分类→格式化→链接→更新→展示 |
| [[wiki_link_builder.py]] | Wiki链接建立 | 根据关键词匹配相关笔记 |
| [[update_graph_html.py]] | 图谱数据生成 | 扫描vault生成graph.html |
| [[graphify.sh]] | 快捷入口 | 统一命令入口 |

模板位于 `/mnt/d/obsidian-notes/.graphify/github-repo/src/templates/`：

| 模板 | Wiki链接 | 用途 |
|------|----------|------|
| [[通用文章模板.md]] | 元数据模板 | 所有收录文章的标准格式 |

---

## Phase 1: 笔记自动化收录

### 适用场景

用户发送文章内容，需要收录到笔记库并自动分类、建立链接、更新图谱。

### Step 1.1: 接收内容并判断来源

**输入**：`title`（标题）、`content`（内容）、`source`（来源）、`author`（作者，可选）

**判断规则**：

| source | 类型判断 | 后续处理 |
|--------|----------|----------|
| `user` | 原创 | 直接收录，不询问 |
| `wechat` | 外来 | 询问处理方式 |
| `web` | 外来 | 询问处理方式 |
| `feishu` | 外来 | 直接提取要点 |
| `book` | 外来 | 提取要点 |

**执行命令**：

```bash
python3 [[note_collector.py]] \
  --title "标题" \
  --content "内容" \
  --source "wechat" \
  --author "作者名"
```

**输出**：返回分析结果 JSON

```json
{
  "keywords": ["认知", "智慧", "顿悟"],
  "category": "Knowledge",
  "subcategory": "Wisdom",
  "quality": "medium",
  "need_ask": true,
  "question": "这是一篇来自 wechat 的文章，请选择处理方式",
  "options": ["原文收藏", "提取要点", "跳过"]
}
```

---

### Step 1.2: 外来素材处理（需用户确认）

**检查点**：如果 `need_ask=true`，使用 `clarify()` 询问用户。

**询问模板**：

```
这是一篇来自 {source} 的文章，作者: {author}。
关键词: {keywords}
建议分类: {category}/{subcategory}

请选择处理方式：
  1. 原文收藏 - 一字不差保存到 Materials/Articles
  2. 提取要点 - 精炼核心内容到 Knowledge/{subcategory}
  3. 跳过 - 不收录此文章
```

**用户选择后的处理**：

| 选择 | type值 | 存放位置 |
|------|--------|----------|
| 原文收藏 | `collected` | `04-Materials/Articles/` |
| 提取要点 | `extracted` | `02-Knowledge/{subcategory}/` |

---

### Step 1.3: 应用模板并保存

**执行命令**：

```bash
# 原文收藏
python3 [[note_collector.py]] \
  --title "标题" \
  --content "内容" \
  --source "wechat" \
  --author "作者名" \
  --type collected \
  --save

# 提取要点
python3 [[note_collector.py]] \
  --title "标题" \
  --content "内容" \
  --source "wechat" \
  --author "作者名" \
  --type extracted \
  --save
```

**输出**：生成文件路径

```
✅ 已保存: /mnt/d/obsidian-notes/02-Knowledge/Wisdom/标题.md
```

**生成的文件格式**：

```yaml
---
type: collected        # collected | extracted | original
source: wechat
author: "作者名"
created: 2026-04-19
updated: 2026-04-19
category: Knowledge
subcategory: Wisdom
tags: [认知, 智慧, 顿悟]
keywords: [认知, 智慧, 顿悟]
quality: medium
importance: 3
readiness: complete
related_notes: []
references: []
aliases: []
---

# 标题

> 一句话概括核心观点

## 核心主题
本文讨论 **Knowledge/Wisdom** 相关内容。

## 关键概念索引
- **认知** → 简要解释
- **智慧** → 简要解释
- **顿悟** → 简要解释

## 正文内容
{原文内容}

---

## 相关笔记
<!-- 自动填充 -->

## 参考资料
- 原文链接（如有）
```

---

### Step 1.4: 建立 Wiki 链接

**输入**：新保存的笔记文件路径

**执行命令**：

```bash
python3 [[wiki_link_builder.py]] "/mnt/d/obsidian-notes/02-Knowledge/Wisdom/标题.md"
```

**处理逻辑**：

1. 从 `keywords` 字段提取关键词
2. 搜索 vault 中匹配关键词的其他笔记
3. 在 `## 相关笔记` 区块添加 Wiki 链接

**输出**：

```
✅ 建立 3 个 Wiki 链接:
  - [[认知转变]] (智慧)
  - [[真正的智慧从何而来]] (智慧)
  - [[道理与智慧]] (智慧)
```

---

### Step 1.5: 更新图谱

**执行命令**：

```bash
python3 [[update_graph_html.py]] "/mnt/d/obsidian-notes"
```

**输出**：

```
扫描 vault: /mnt/d/obsidian-notes
✅ 更新完成: /mnt/d/obsidian-notes/.graphify/graph.html
   节点数: 35
   边数: 30
```

---

### Step 1.6: 打开浏览器展示

**执行命令**：

```bash
powershell.exe -Command "Start-Process '浏览器路径' -ArgumentList 'file:///D:/obsidian-notes/.graphify/graph.html'"
```

**或使用快捷脚本**：

```bash
./[[graphify.sh]] open
```

---

## Phase 2: 单独更新图谱

### 适用场景

用户已有笔记，只需更新图谱可视化。

### Step 2.1: 执行更新

**执行命令**：

```bash
python3 [[update_graph_html.py]] "/mnt/d/obsidian-notes"
```

**输出**：节点数、边数、图谱路径

---

### Step 2.2: 打开浏览器

**执行命令**：

```bash
./[[graphify.sh]] open
```

---

## Phase 3: 单独建立 Wiki 链接

### 适用场景

用户有新笔记，需要与现有笔记建立关联。

### Step 3.1: 执行链接建立

**输入**：笔记文件路径

**执行命令**：

```bash
python3 [[wiki_link_builder.py]] "/mnt/d/obsidian-notes/02-Knowledge/Wisdom/某篇文章.md"
```

**输出**：建立的链接列表

---

## Phase 4: 启动自动更新守护进程

### 适用场景

用户需要实时监控 vault 变化并自动更新图谱。

### Step 4.1: 启动守护进程

**执行命令**：

```bash
./[[graphify.sh]] auto
# 或
python3 /mnt/d/obsidian-notes/.graphify/github-repo/src/auto_update.py "/mnt/d/obsidian-notes" &
```

**输出**：

```
启动自动更新守护进程...
监控路径: /mnt/d/obsidian-notes
```

---

## 快捷命令汇总

所有命令通过 `graphify.sh` 入口：

| 命令 | 功能 | 示例 |
|------|------|------|
| `collect` | 收录文章 | `./graphify.sh collect "标题" "内容" "wechat" "作者"` |
| `link` | 建立链接 | `./graphify.sh link "/path/to/note.md"` |
| `update` | 更新图谱 | `./graphify.sh update` |
| `open` | 打开浏览器 | `./graphify.sh open` |
| `auto` | 启动守护进程 | `./graphify.sh auto` |

---

## 分类规则参考

Agent 根据内容关键词自动判断分类：

| 一级分类 | 二级分类 | 关键词 |
|----------|----------|--------|
| Knowledge | Wisdom | 智慧、认知、哲学、思考、道理、顿悟、人生 |
| Knowledge | AI-ML | AI、机器学习、LLM、模型、Agent、神经网络 |
| Knowledge | Architecture | 架构、系统设计、分布式、微服务 |
| Knowledge | Tools | 工具、技巧、Obsidian、Git、Python |
| Knowledge | Research | 研究、论文、实验、方法论 |
| Projects | Graphify | Graphify、图谱、知识图谱 |
| Projects | Hermes-Agent | Hermes、Agent、飞书 |
| Materials | Articles | 外来文章默认位置 |

---

## 边界条件处理

### 分类不确定

**问题**：内容关键词无法匹配任何分类

**处理**：
1. 默认放入 `04-Materials/Articles/`
2. 提示用户手动指定分类

```bash
python3 [[note_collector.py]] ... --category_override "Knowledge/Wisdom"
```

---

### Wiki 链接未建立

**问题**：`wiki_link_builder.py` 未找到匹配笔记

**原因**：
1. `keywords` 字段为空
2. vault 中没有相关主题笔记

**处理**：
1. 检查生成文件的 keywords 字段
2. 手动补充关键词后重新执行

---

### 浏览器未打开

**问题**：WSL 环境下 `powershell.exe` 调用失败

**处理**：
1. 检查浏览器路径是否正确
2. 使用替代命令：

```bash
# 直接用 Windows 路径打开
explorer.exe "D:\\obsidian-notes\\.graphify\\graph.html"
```

---

### 文件名冲突

**问题**：同标题文件已存在

**处理**：
1. 自动添加时间戳后缀：`标题_20260419.md`
2. 提示用户确认

---

## 检查点设计

| 检查点位置 | 触发条件 | 用户操作 |
|------------|----------|----------|
| Step 1.2 | `need_ask=true` | 选择处理方式（原文/提取/跳过） |
| Step 1.3 | 分类不确定 | 手动指定分类 |
| Step 1.4 | 文件名冲突 | 确认覆盖或重命名 |

---

## 输出验证标准

| Phase | 成功标准 |
|-------|----------|
| Phase 1 | 文件生成 + 元数据完整 + Wiki链接建立 + 图谱更新 + 浏览器打开 |
| Phase 2 | 图谱更新 + 节点数/边数正确 |
| Phase 3 | Wiki链接数量 > 0 |
| Phase 4 | 守护进程启动 + 监控日志正常 |

---

## 错误代码对照

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `E001` | vault路径不存在 | 检查 `/mnt/d/obsidian-notes` 是否挂载 |
| `E002` | 模板文件缺失 | 检查 `src/templates/通用文章模板.md` |
| `E003` | 分类匹配失败 | 使用 `--category_override` 手动指定 |
| `E004` | powershell调用失败 | 使用 `explorer.exe` 替代 |
| `E005` | 文件写入失败 | 检查目录权限 |

---

## 相关文档

- [[folder-structure]] - 文件夹结构规范
- [[metadata-spec]] - 元数据字段详解
- [[features]] - 图谱功能说明