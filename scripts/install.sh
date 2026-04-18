#!/bin/bash
# Graphify 一键安装脚本

set -e

echo "=================================================="
echo "  Graphify Knowledge Graph System - 安装脚本"
echo "=================================================="

# 检查 Python
echo ""
echo "检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    echo "   请先安装 Python3: https://www.python.org/"
    exit 1
fi
echo "✅ Python3 已安装: $(python3 --version)"

# 检查 pip
echo ""
echo "检查 pip..."
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip 未安装"
    exit 1
fi
echo "✅ pip 已安装"

# 安装依赖
echo ""
echo "安装依赖..."
pip3 install watchdog -q
echo "✅ watchdog 已安装"

# 获取用户输入
echo ""
echo "=================================================="
echo "  配置 Obsidian Vault 路径"
echo "=================================================="
echo ""
echo "请输入你的 Obsidian vault 路径:"
echo "示例: /Users/yourname/Documents/obsidian-notes"
echo "      D:/Documents/obsidian-notes"
echo ""
read -p "> " VAULT_PATH

# 验证路径
if [ -z "$VAULT_PATH" ]; then
    echo "❌ 路径不能为空"
    exit 1
fi

if [ ! -d "$VAULT_PATH" ]; then
    echo ""
    echo "⚠️  路径不存在: $VAULT_PATH"
    echo "   是否创建此目录?"
    read -p "> [y/N] " CREATE_DIR
    if [ "$CREATE_DIR" = "y" ] || [ "$CREATE_DIR" = "Y" ]; then
        mkdir -p "$VAULT_PATH"
        echo "✅ 目录已创建"
    else
        echo "❌ 请提供有效的 vault 路径"
        exit 1
    fi
fi

# 创建 .graphify 目录
GRAPHIFY_DIR="$VAULT_PATH/.graphify"
mkdir -p "$GRAPHIFY_DIR"

echo ""
echo "复制 Graphify 文件..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 复制核心文件
if [ -d "$SCRIPT_DIR/src" ]; then
    cp "$SCRIPT_DIR/src/*.py" "$GRAPHIFY_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/*.html" "$GRAPHIFY_DIR/" 2>/dev/null || true
    echo "✅ 核心文件已复制"
else
    # 从当前目录复制
    cp "$(dirname "$SCRIPT_DIR")/src/*.py" "$GRAPHIFY_DIR/" 2>/dev/null || true
    cp "$(dirname "$SCRIPT_DIR")/src/*.html" "$GRAPHIFY_DIR/" 2>/dev/null || true
    echo "✅ 核心文件已复制"
fi

# 复制模板（可选）
TEMPLATE_SRC="$SCRIPT_DIR/../demo_notes/04-Templates"
TEMPLATE_DST="$VAULT_PATH/04-Templates"
if [ -d "$TEMPLATE_SRC" ]; then
    mkdir -p "$TEMPLATE_DST"
    cp "$TEMPLATE_SRC/*.md" "$TEMPLATE_DST/" 2>/dev/null || true
    echo "✅ 笔记模板已复制"
fi

# 创建配置文件
CONFIG_FILE="$GRAPHIFY_DIR/config.yaml"
cat > "$CONFIG_FILE" << EOF
# Graphify 配置文件

obsidian:
  vault_path: "$VAULT_PATH"

graph:
  theme: "dark"
  primary_color: "#5e6ad2"
  max_label_length: 12

update:
  auto: true
  interval: 3
EOF
echo "✅ 配置文件已创建: $CONFIG_FILE"

# 完成
echo ""
echo "=================================================="
echo "  ✅ 安装完成！"
echo "=================================================="
echo ""

# 修改脚本中的 vault 配置
echo "配置 vault 路径..."
sed -i "s|OBSIDIAN_VAULT = \"/path/to/your/obsidian-notes\"|OBSIDIAN_VAULT = \"$VAULT_PATH\"|g" "$GRAPHIFY_DIR/update_graph_html.py"
sed -i "s|OBSIDIAN_VAULT = \"/path/to/your/obsidian-notes\"|OBSIDIAN_VAULT = \"$VAULT_PATH\"|g" "$GRAPHIFY_DIR/auto_update.py"
echo "✅ 路径配置已更新"

# 首次生成图谱数据
echo ""
echo "生成图谱数据..."
python3 "$GRAPHIFY_DIR/update_graph_html.py" "$VAULT_PATH"
echo "✅ 图谱数据已生成"

echo ""
echo "下一步:"
echo "  1. 打开图谱页面:"
echo "     open $GRAPHIFY_DIR/graph_fixed_beautiful.html"
echo ""
echo "  2. 启动自动更新守护进程:"
echo "     python3 $GRAPHIFY_DIR/auto_update.py $VAULT_PATH"
echo ""
echo "  3. 在 Obsidian 中写一条 Wiki 链接:"
echo "     [[另一个笔记名]] 是这篇笔记的相关内容"
echo ""
echo "  4. 刷新图谱页面，看到连接出现！"
echo ""
echo "=================================================="