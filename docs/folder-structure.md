# 3级文件夹结构设计

## 设计理念

知识不是孤岛，而是网络。文件夹结构的目标是：
- **结构化存储**：原创/收藏分离
- **易于维护**：分类清晰，自动检测
- **图谱友好**：路径即分类，自动映射

---

## 标准结构

```
obsidian-notes/                 (0级：根目录)
│
├── 01-System/                  (1级：系统核心)
│   ├── Core/                   (2级：核心概念)
│   │   └── SOUL.md            (3级：文档)
│   │   └── 设计理念.md
│   │
│   └── Config/                 (2级：配置文档)
│       └── config.yaml
│       └── 技能清单.md
│
├── 02-Knowledge/              (1级：知识领域)
│   ├── AI-ML/                 (2级：AI/Machine Learning)
│   │   ├── LLM基础.md
│   │   └── Agent架构.md
│   │
│   ├── Architecture/          (2级：架构设计）
│   │   ├── 系统设计.md
│   │   └── 分布式架构.md
│   │
│   └── Tools/                 (2级：工具使用）
│   │   ├── Obsidian技巧.md
│   │   └── Git最佳实践.md
│   │
│   └── Research/              (2级：研究笔记）
│       └── 论文阅读.md
│
├── 03-Projects/               (1级：项目文档）
│   ├── Graphify/              (2级：Graphify项目）
│   │   ├── 开发日志.md
│   │   ├── 功能清单.md
│   │
│   ├── Hermes-Agent/          (2级：Agent项目）
│   │   ├── 设计文档.md
│   │   ├── 集成方案.md
│   │
│   └── Integration/           (2级：集成项目）
│       └── 飞书对接.md
│
├── 04-Materials/              (1级：收藏素材）
│   ├── Articles/              (2级：文章收藏）
│   │   ├── 知识管理方法.md
│   │   └── 技术趋势分析.md
│   │
│   ├── Feishu/                (2级：飞书导入）
│   │   ├── 飞书消息_2026-04-16.md
│   │
│   └── References/            (2级：参考资料）
│       └── API文档收藏.md
│
├── 04-Templates/              (1级：笔记模板）
│   ├── General_Template.md    (通用模板）
│   ├── Project_Template.md    (项目模板）
│   └── Meeting_Template.md    (会议模板）
│
└── .graphify/                 (图谱系统）
    ├── graph_fixed_beautiful.html
    ├── update_graph_html.py
    ├── auto_update.py
    └── config.yaml
```

---

## 分类映射

文件夹路径 → 图谱节点分类：

| 文件夹 | 图谱分类 | 颜色 |
|--------|----------|------|
| `01-System/` | System | 白色 `#f7f8f8` |
| `02-Knowledge/AI-ML/` | AI-ML | 蓝色 `#5e6ad2` |
| `02-Knowledge/Architecture/` | Architecture | 浅蓝 `#409EFF` |
| `02-Knowledge/Tools/` | Tools | 绿色 `#67C23A` |
| `03-Projects/` | Projects | 绿色 `#4DAF73` |
| `04-Materials/` | Materials | 橙色 `#E6A23C` |

---

## YAML Frontmatter

每篇笔记开头添加：

```markdown
---
type: original      # 或 collected
created: 2026-04-16
tags: [知识图谱, Obsidian]
---

# 笔记标题

内容...
```

**type 字段说明**：
- `original`：原创内容（01-System, 02-Knowledge, 03-Projects）
- `collected`：收藏素材（04-Materials）

---

## 自动检测规则

Graphify 会根据路径自动判断：

```python
def get_note_category(file_path):
    rel_path = os.path.relpath(file_path, vault_path)
    
    if '01-System' in rel_path:
        return 'System'
    elif '02-Knowledge/AI-ML' in rel_path:
        return 'AI-ML'
    elif '02-Knowledge/Architecture' in rel_path:
        return 'Architecture'
    # ...
```

---

## 最佳实践

### 1. 新笔记放哪里？

| 内容类型 | 放置位置 |
|----------|----------|
| 自己写的思考/总结 | `02-Knowledge/` 对应子目录 |
| 项目开发文档 | `03-Projects/项目名/` |
| 别人的文章收藏 | `04-Materials/Articles/` |
| 飞书有价值消息 | `04-Materials/Feishu/` |

### 2. 子目录如何命名？

- 使用英文或拼音（便于文件系统）
- 语义清晰（`AI-ML` 而不是 `AI`）
- 避免过深嵌套（最多 2 级子目录）

### 3. 文件命名规范

```markdown
# 推荐
知识图谱系统.md
LLM基础概念.md
Agent架构设计.md

# 不推荐
2026-04-16-随便写的.md  # 前缀无意义
未命名.md               # 没有标题
draft.md                # 临时文件
```

---

## 扩展分类

如果你想添加新分类，修改 `config.yaml`：

```yaml
graph:
  colors:
    # 添加新分类
    Research: "#9B59B6"      # 紫色
    DevOps: "#E74C3C"        # 红色
    MLOps: "#3498DB"         # 深蓝
```

然后创建对应文件夹：

```bash
mkdir -p obsidian-notes/02-Knowledge/Research
mkdir -p obsidian-notes/02-Knowledge/DevOps
```