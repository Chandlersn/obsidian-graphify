#!/bin/bash
# Graphify 快捷入口脚本
# 提供统一的命令入口，方便执行各种操作

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_PATH="${VAULT_PATH:-/mnt/d/obsidian-notes}"
GRAPHIFY_DIR="$VAULT_PATH/.graphify"

# 显示帮助
show_help() {
    echo "Graphify Knowledge Graph System - 快捷入口"
    echo ""
    echo "使用方法: graphify.sh <命令>"
    echo ""
    echo "命令:"
    echo "  update    - 更新图谱数据"
    echo "  auto      - 启动自动更新守护进程"
    echo "  open      - 打开图谱页面"
    echo "  collect   - 收录文章（需提供参数）"
    echo "  link      - 建立Wiki链接（需提供笔记路径）"
    echo "  status    - 查看当前状态"
    echo "  help      - 显示帮助信息"
    echo ""
    echo "示例:"
    echo "  ./graphify.sh update"
    echo "  ./graphify.sh auto"
    echo "  ./graphify.sh open"
    echo "  ./graphify.sh collect --title '标题' --content '内容' --source 'wechat'"
    echo "  ./graphify.sh link '/mnt/d/obsidian-notes/02-Knowledge/Wisdom/笔记.md'"
}

# 更新图谱
do_update() {
    echo "更新图谱数据..."
    python3 "$GRAPHIFY_DIR/github-repo/src/update_graph_html.py" "$VAULT_PATH"
    echo "✅ 图谱已更新"
}

# 启动守护进程
do_auto() {
    echo "启动自动更新守护进程..."
    echo "按 Ctrl+C 停止"
    python3 "$GRAPHIFY_DIR/github-repo/src/auto_update.py" "$VAULT_PATH"
}

# 打开图谱页面
do_open() {
    echo "打开图谱页面..."
    if command -v cmd.exe &> /dev/null; then
        # WSL 环境
        cmd.exe /c start "" "D:\\obsidian-notes\\.graphify\\graph.html"
    elif command -v open &> /dev/null; then
        # macOS
        open "$GRAPHIFY_DIR/graph.html"
    else
        # Linux
        xdg-open "$GRAPHIFY_DIR/graph.html"
    fi
    echo "✅ 图谱页面已打开"
}

# 收录文章
do_collect() {
    if [ $# -lt 2 ]; then
        echo "⚠️ 请提供收录参数"
        echo "示例: ./graphify.sh collect --title '标题' --content '内容' --source 'wechat'"
        exit 1
    fi
    echo "收录文章..."
    python3 "$GRAPHIFY_DIR/github-repo/skills/scripts/note_collector.py" "$@"
}

# 建立Wiki链接
do_link() {
    if [ $# -lt 1 ]; then
        echo "⚠️ 请提供笔记路径"
        echo "示例: ./graphify.sh link '/mnt/d/obsidian-notes/02-Knowledge/Wisdom/笔记.md'"
        exit 1
    fi
    echo "建立Wiki链接..."
    python3 "$GRAPHIFY_DIR/github-repo/skills/scripts/wiki_link_builder.py" "$1"
}

# 查看状态
do_status() {
    echo "Graphify 状态"
    echo "================"
    echo "Vault 路径: $VAULT_PATH"
    echo "Graphify 目录: $GRAPHIFY_DIR"
    echo ""
    
    # 检查守护进程
    if pgrep -f "auto_update.py" > /dev/null; then
        echo "守护进程: ✅ 运行中"
    else
        echo "守护进程: ⏹ 未运行"
    fi
    echo ""
    
    # 统计笔记数量
    NOTE_COUNT=$(find "$VAULT_PATH" -name "*.md" -not -path "*/.graphify/*" | wc -l)
    echo "笔记数量: $NOTE_COUNT"
    
    # 统计Wiki链接
    if [ -f "$GRAPHIFY_DIR/graph.html" ]; then
        echo "图谱文件: ✅ 存在"
        echo "打开命令: ./graphify.sh open"
    else
        echo "图谱文件: ❌ 不存在，请先执行 ./graphify.sh update"
    fi
}

# 主逻辑
case "${1:-help}" in
    update)
        do_update
        ;;
    auto)
        do_auto
        ;;
    open)
        do_open
        ;;
    collect)
        do_collect "${@:2}"
        ;;
    link)
        do_link "$2"
        ;;
    status)
        do_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "⚠️ 未知命令: $1"
        show_help
        exit 1
        ;;
esac