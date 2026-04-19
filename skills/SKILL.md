---
name: graphify-knowledge-graph-ui
description: "将 Obsidian 笔记变成可视化知识图谱。支持笔记自动化收录、Wiki链接建立、图谱可视化更新。Use when user mentions \"知识图谱\", \"graphify\", \"可视化笔记\", \"笔记图谱\", \"收录文章\", \"笔记收录\", \"更新图谱\", \"同步笔记\", \"wiki链接\"."
tags: [note-taking, obsidian, visualization, knowledge-graph, graphify]
version: 2.2.0
category: creative
source: https://github.com/Chandlersn/obsidian-graphify
linked_files:
  scripts/note_collector.py: 核心收录脚本
  scripts/wiki_link_builder.py: Wiki链接建立脚本
  scripts/update_graph_html.py: 图谱数据生成脚本
  scripts/graphify.sh: 快捷入口脚本
---

# Graphify Knowledge Graph UI v2.2

> 将 Obsidian 笔记变成一张可视化的知识图谱，让知识真正「连起来」。
> 核心理念：**笔记 → 解析链接 → 构建图谱 → 可视化 → 发现脉络 → 建立新链接**

---

## 工具索引

所有脚本位于 `/mnt/d/obsidian-notes/.graphify/github-repo/skills/scripts/`：

| 工具 | 功能 |
|------|------|
| `note_collector.py` | 收录流程核心：分析→分类→格式化→链接→更新→展示 |
| `wiki_link_builder.py` | Wiki链接建立：匹配关键词相关笔记 |
| `update_graph_html.py` | 图谱数据生成：扫描vault生成graph.html |
| `graphify.sh` | 快捷入口：统一命令入口 |

模板位于 `/mnt/d/obsidian-notes/.graphify/github-repo/src/templates/`：

| 模板 | 用途 |
|------|------|
| `笔记模板.md` | 简化模板（YAML 4行 + 正文 + 关键概念 + 相关笔记） |

---

## 简化模板格式

```markdown
---
type: original
created: YYYY-MM-DD
tags: ["标签1", "标签2"]
---

# 笔记标题

> 一句话核心观点。

正文段落...

---

正文段落（段落间用 --- 分隔）...

（正文最后一句不加粗）

## 关键概念

- **概念名** → 简要解释
- **概念名** → 简要解释

---

## 相关笔记

- [[笔记名]] (关联理由)

---
```

**格式要点**：
- YAML 仅 4 行
- 正文直接呈现，无包裹区块
- 段落间用 `---` 分隔
- 正文最后一句不加粗
- 关键概念区块匹配 `## 关键概念`
- 相关笔记统一位置

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
python3 note_collector.py \
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

---

### Step 1.3: 应用简化模板并保存

**执行命令**：

```bash
# 原文收藏
python3 note_collector.py \
  --title "标题" \
  --content "内容" \
  --source "wechat" \
  --author "作者名" \
  --type collected \
  --save

# 提取要点
python3 note_collector.py \
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

---

### Step 1.4: 建立 Wiki 链接

**输入**：新保存的笔记文件路径

**执行命令**：

```bash
python3 wiki_link_builder.py "/mnt/d/obsidian-notes/02-Knowledge/Wisdom/标题.md"
```

**处理逻辑**：
1. 从 `tags` 字段和 `## 关键概念` 区块提取关键词
2. 搜索 vault 中匹配关键词的其他笔记
3. 在 `## 相关笔记` 区块添加 Wiki 链接

---

### Step 1.5: 更新图谱

**执行命令**：

```bash
python3 update_graph_html.py "/mnt/d/obsidian-notes"
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
cmd.exe /c start "" "D:\\obsidian-notes\\.graphify\\graph.html"
```

---

## Phase 2: 单独更新图谱

**执行命令**：

```bash
python3 update_graph_html.py "/mnt/d/obsidian-notes"
```

---

## Phase 3: 单独建立 Wiki 链接

**执行命令**：

```bash
python3 wiki_link_builder.py "/mnt/d/obsidian-notes/02-Knowledge/Wisdom/某篇文章.md"
```

---

## Phase 4: 启动自动更新守护进程

**执行命令**：

```bash
./graphify.sh auto
```

---

## 分类规则

| 一级分类 | 二级分类 | 关键词 |
|----------|----------|--------|
| Knowledge | Wisdom | 智慧、认知、哲学、思考、道理、顿悟 |
| Knowledge | AI-ML | AI、机器学习、LLM、模型、Agent |
| Knowledge | Architecture | 架构、系统设计、分布式 |
| Knowledge | Tools | 工具、技巧、Obsidian、Git |
| Projects | Graphify | Graphify、图谱、知识图谱 |
| Projects | Hermes-Agent | Hermes、Agent、飞书 |
| Materials | Articles | 外来文章默认位置 |

---

## 检查点

| 检查点 | 触发条件 | 用户操作 |
|--------|----------|----------|
| Step 1.2 | `need_ask=true` | 选择处理方式 |
| Step 1.3 | 分类不确定 | 手动指定分类 |
| Step 1.4 | Wiki链接未建立 | 检查关键词 |

---

## 边界条件

### Wiki 链接未建立

**原因**：
- `## 关键概念` 区块为空
- vault 中没有相关主题笔记

**处理**：手动补充关键词后重新执行

### 浏览器未打开

**替代命令**：

```bash
explorer.exe "D:\\obsidian-notes\\.graphify\\graph.html"
```

---

## 错误代码

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `E001` | vault路径不存在 | 检查 `/mnt/d/obsidian-notes` 是否挂载 |
| `E002` | 模板文件缺失 | 检查 `src/templates/笔记模板.md` |
| `E003` | 分类匹配失败 | 使用 `--category` 手动指定 |
| `E004` | 浏览器调用失败 | 使用 `explorer.exe` 替代 |

---

## 输出验证标准

| Phase | 成功标准 |
|-------|----------|
| Phase 1 | 文件生成 + YAML完整 + Wiki链接 + 图谱更新 + 浏览器打开 |
| Phase 2 | 图谱更新 + 节点数/边数正确 |
| Phase 3 | Wiki链接数量 > 0 |