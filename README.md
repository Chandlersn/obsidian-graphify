<div align="right">

**[English](README_EN.md)** | 中文

</div>

# obsidian-graphify

**将你的 Obsidian 笔记变成一张可视化的知识图谱，让知识真正「连起来」。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Obsidian](https://img.shields.io/badge/Obsidian-Compatible-purple.svg)](https://obsidian.md/)
[![vis-network](https://img.shields.io/badge/vis--network-v9.1.9-green.svg)](https://github.com/visjs/vis-network)

***

## 核心理念

```
笔记 → 解析链接 → 构建图谱 → 可视化 → 发现脉络 → 建立新链接 → 笔记
```

一个正向循环。写得越多，图谱越密；图谱越密，发现越多。

***

## 为什么做这个

传统笔记软件只解决「存储」问题：文件夹、标签、搜索。但没有解决「连接」问题。

当你有 10 条笔记时，可以靠记忆知道它们的关系。
当你有 50 条笔记时，就会开始遗忘。
当你有 100+ 条笔记时，它们自然就成了孤岛。

而Graphify ，就是把单个的笔记，变成一了张知识网络：

- **可视化** — 一张图看清所有知识
- **路径追踪** — BFS 最短路径，发现知识脉络
- **孤岛检测** — 高亮无连接节点，知道哪里需要补链接
- **热度统计** — 点击记录，显示你最关注的领域
- **影响力分析** — 通过计算你的点击数，进行PageRank 式排名，知道哪个知识点是你的核心，

***

## 从存储到连接

| 传统笔记软件  | Graphify | 为什么这样设计              |
| :------ | :------- | :------------------- |
| 文件夹树状结构 | 网状图谱     | 知识本来就是网状的            |
| 搜索关键词   | 点击节点直达   | 搜索需要知道关键词，图谱可以发现不知道的 |
| 标签分类    | 动态分类筛选   | 分类是静态的，图谱是动态生长的      |
| 笔记是孤岛   | 笔记是节点    | 孤岛之间没有路，节点之间有路径      |
| 靠记忆找关联  | 路径追踪算法   | 记忆会遗忘，算法不会           |

***

## 12 个核心功能

| #  | 功能          | 说明                          |
| :- | :---------- | :-------------------------- |
| 01 | **3级文件夹结构** | 原创/收藏分离，结构化管理笔记             |
| 02 | **可视化图谱**   | vis-network 渲染，一张图看清所有知识网络  |
| 03 | **快速搜索**    | Ctrl+K 秒级定位任意节点             |
| 04 | **分类筛选**    | 动态渲染按钮，自动同步笔记分类             |
| 05 | **路径追踪**    | BFS 最短路径，发现知识脉络             |
| 06 | **热度统计**    | localStorage 点击记录，显示你最关注的领域 |
| 07 | **孤岛检测**    | 高亮无连接节点，发现需要建立链接的内容         |
| 08 | **影响力分析**   | PageRank 式排名，知道哪个知识点最核心     |
| 09 | **主题切换**    | 深色/浅色模式，Linear 设计风格         |
| 10 | **飞书导入**    | 自动保存有价值消息到笔记库               |
| 11 | **PNG 导出**  | 保存图谱图片，分享知识结构               |
| 12 | **自动更新**    | watchdog 监控，实时同步图谱          |

***

## 技术栈

| 组件   | 技术                  | 为什么选它         |
| :--- | :------------------ | :------------ |
| 可视化  | vis-network v9.1.9  | 轻量、高性能、支持物理模拟 |
| 设计风格 | Linear.app          | 深色/浅色主题，干净现代  |
| 后端   | Python 3.x          | 简单、跨平台、易扩展    |
| 自动更新 | watchdog            | 文件监控，实时响应     |
| 集成   | Obsidian URI scheme | 点击节点直接打开笔记    |
| 存储   | localStorage        | 无需数据库，纯本地     |

***

## 安装前提

| 前置条件         | 版本要求 | 检查方式                | 说明   |
| :----------- | :--- | :------------------ | :--- |
| **Obsidian** | 任意版本 | 已安装并有一个 vault       | 笔记软件 |
| **Python**   | 3.6+ | `python3 --version` | 运行脚本 |
| **pip**      | 任意   | `pip3 --version`    | 安装依赖 |
| **Git**      | 任意   | `git --version`     | 克隆仓库 |

> 💡 **仓库地址**: `https://github.com/Chandlersn/obsidian-graphify`
>
> 克隆后无需额外安装 Graphify，所有核心代码都在仓库 `src/` 目录中。

***

## 快速开始

### 一键安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/Chandlersn/obsidian-graphify.git
cd obsidian-graphify

# 运行安装脚本（自动安装依赖 + 配置路径 + 生成图谱）
chmod +x scripts/install.sh
./scripts/install.sh
```

安装过程中会提示你输入 Obsidian vault 路径，例如：

- macOS: `/Users/yourname/Documents/obsidian-notes`
- Windows: `D:/Documents/obsidian-notes`
- Linux: `/home/yourname/obsidian-notes`

安装完成后：

```bash
# 打开图谱页面（显示你的笔记网络）
open /path/to/your/vault/.graphify/graph_fixed_beautiful.html

# 启动自动更新守护进程（可选，实时同步）
python3 /path/to/your/vault/.graphify/auto_update.py /path/to/your/vault &
```

### 手动安装

详见 [快速开始指南](docs/getting-started.md)。

***

## 文件结构

```
obsidian-graphify/
├── README.md              # 本文件
├── LICENSE                # MIT License
├── CHANGELOG.md           # 版本历史
├── assets/
│   └── screenshots/       # 截图演示
├── config/
│   └── config.yaml        # 配置文件
├── demo_notes/            # 示例笔记（演示 3 级结构）
│   ├── 01-System/
│   ├── 02-Knowledge/
│   ├── 03-Projects/
│   └── 04-Materials/
├── docs/                  # 详细文档
│   ├── getting-started.md
│   ├── folder-structure.md
│   ├── features.md
│   ├── customization.md
│   └── troubleshooting.md
├── scripts/
│   └── install.sh         # 安装脚本
├── skills/
│   └── SKILL.md           # Agent Skill 定义
└── src/                   # 核心代码
    ├── graph_fixed_beautiful.html  # 图谱页面
    ├── update_graph_html.py        # 图谱生成脚本
    ├── auto_update.py              # 自动更新守护进程
    ├── feishu_importer.py          # 飞书导入
    └ templates/                   # 笔记模板
```

***

## 推荐的 Vault 结构

```
obsidian-notes/
├── 01-System/          # 系统核心
├── 02-Knowledge/       # 知识领域
├── 03-Projects/        # 项目文档
├── 04-Materials/       # 收藏素材
├── 04-Templates/       # 笔记模板
└── .graphify/          # 图谱系统
```

详见 [文件夹结构设计理念](docs/folder-structure.md)。

***

## 截图

|                    深色主题                   |                     浅色主题                    |
| :---------------------------------------: | :-----------------------------------------: |
| ![Dark](assets/screenshots/dark-mode.png) | ![Light](assets/screenshots/light-mode.png) |

|                     路径追踪                     |                   热度统计                   |
| :------------------------------------------: | :--------------------------------------: |
| ![Path](assets/screenshots/path-tracing.png) | ![Heat](assets/screenshots/heat-map.png) |

***

## 文档

- [快速开始](docs/getting-started.md) — 详细安装指南
- [文件夹结构](docs/folder-structure.md) — 3 级结构设计理念
- [功能详解](docs/features.md) — 12 个功能完整说明
- [自定义配置](docs/customization.md) — 修改颜色、字体、分类
- [常见问题](docs/troubleshooting.md) — FAQ

***

## 设计灵感

> "Knowledge is a network, not a hierarchy."
> — Ted Nelson, Hypertext Pioneer

Graphify 把 Ted Nelson 的超文本理念落地到 Obsidian：

- **双向链接** — `[[笔记名]]` 创建节点和边
- **可视化** — 把隐藏的网络变成可见的图谱
- **发现** — 路径追踪、孤岛检测、影响力分析

***

## 贡献指南

欢迎贡献！

```bash
# 1. Fork 并克隆
git clone https://github.com/Chandlersn/obsidian-graphify.git

# 2. 创建分支
git checkout -b feature/your-feature

# 3. 提交更改
git commit -m "Add: your feature"

# 4. 推送并创建 PR
git push origin feature/your-feature
```

***

## 许可证

MIT License — 自由使用、修改、分发。

***

<div align="center">

**让知识从孤岛变成网络。**

*写得越多，图谱越密；图谱越密，发现越多。*

</div>
