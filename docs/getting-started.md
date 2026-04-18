# 快速开始指南

## 安装步骤

### 方法 1: 一键安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/Chandlersn/obsidian-graphify.git
cd obsidian-graphify

# 2. 运行安装脚本
chmod +x scripts/install.sh
./scripts/install.sh

# 3. 输入你的 Obsidian vault 路径
# 示例: /Users/yourname/Documents/obsidian-notes
```

### 方法 2: 手动安装

```bash
# 1. 安装 Python 依赖
pip install watchdog

# 2. 复制文件到你的 vault
mkdir -p /path/to/your/obsidian-notes/.graphify
cp src/*.py /path/to/your/obsidian-notes/.graphify/
cp src/*.html /path/to/your/obsidian-notes/.graphify/
```

***

## 使用方法

### 1. 打开图谱页面

```bash
# macOS
open /path/to/your/obsidian-notes/.graphify/graph_fixed_beautiful.html

# Windows
start /path/to/your/obsidian-notes/.graphify/graph_fixed_beautiful.html

# Linux
xdg-open /path/to/your/obsidian-notes/.graphify/graph_fixed_beautiful.html
```

### 2. 启动自动更新（可选）

```bash
python /path/to/your/obsidian-notes/.graphify/auto_update.py /path/to/your/obsidian-notes
```

### 3. 写第一条 Wiki 链接

在 Obsidian 中创建两篇笔记：

**笔记 A (知识图谱.md)**:

```markdown
[[Wiki链接]] 是 Obsidian 的核心特性
```

**笔记 B (Wiki链接.md)**:

```markdown
[[知识图谱]] 使用 Wiki链接建立连接
```

刷新图谱页面，看到两个节点连在一起！

***

## 配置

编辑 `config.yaml`：

```yaml
obsidian:
  vault_path: "/your/actual/path"  # ← 改成你的路径

graph:
  theme: "dark"  # 或 "light"
  primary_color: "#5e6ad2"  # 自定义主色
```

***

## 常见问题

### Q: 图谱没有显示节点？

**原因**: 路径配置错误或没有笔记

**解决**:

1. 检查 `config.yaml` 中的 `vault_path`
2. 确保 vault 中有 `.md` 文件
3. 运行 `python update_graph_html.py /your/path` 手动更新

### Q: Wiki 链接不显示连接？

**原因**: 链接的笔记不存在

**解决**: 确保 `[[笔记名]]` 对应的笔记文件存在

### Q: 自动更新不工作？

**原因**: watchdog 未安装或路径错误

**解决**:

```bash
pip install watchdog
python auto_update.py /correct/path
```

***

<br />

