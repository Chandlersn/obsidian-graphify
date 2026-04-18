#!/usr/bin/env python3
"""
Graphify 自动更新守护进程
使用 watchdog 监控 Obsidian vault 变化，自动更新图谱

使用方法:
    python auto_update.py /path/to/your/obsidian-notes

依赖:
    pip install watchdog
"""

import os
import sys
import time
import subprocess
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("⚠️ 请先安装 watchdog:")
    print("   pip install watchdog")
    sys.exit(1)


class GraphifyHandler(FileSystemEventHandler):
    """文件变化处理器"""
    
    def __init__(self, vault_path, update_script):
        self.vault_path = vault_path
        self.update_script = update_script
        self.last_update = 0
        self.update_interval = 3  # 最小更新间隔（秒）
    
    def on_modified(self, event):
        """文件修改时触发"""
        if event.src_path.endswith('.md'):
            self._trigger_update()
    
    def on_created(self, event):
        """文件创建时触发"""
        if event.src_path.endswith('.md'):
            self._trigger_update()
    
    def on_deleted(self, event):
        """文件删除时触发"""
        if event.src_path.endswith('.md'):
            self._trigger_update()
    
    def _trigger_update(self):
        """触发更新（带防抖）"""
        current_time = time.time()
        
        if current_time - self.last_update < self.update_interval:
            return  # 防抖：短时间内只更新一次
        
        self.last_update = current_time
        
        print(f"\n[{time.strftime('%H:%M:%S')}] 检测到笔记变化，更新图谱...")
        
        # 执行更新脚本
        try:
            result = subprocess.run(
                ['python3', self.update_script, self.vault_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"更新失败: {result.stderr}")
        except Exception as e:
            print(f"执行错误: {e}")


def main():
    # 支持命令行参数
    vault_path = sys.argv[1] if len(sys.argv) > 1 else "/path/to/your/obsidian-notes"
    
    if vault_path == "/path/to/your/obsidian-notes":
        print("⚠️ 请先指定你的 Obsidian vault 路径！")
        print("   使用方法: python auto_update.py /path/to/your/obsidian-notes")
        sys.exit(1)
    
    # 更新脚本路径
    graphify_dir = os.path.join(vault_path, ".graphify")
    update_script = os.path.join(graphify_dir, "update_graph_html.py")
    
    if not os.path.exists(update_script):
        print(f"⚠️ 更新脚本不存在: {update_script}")
        print("   请确保 update_graph_html.py 在 .graphify 目录下")
        sys.exit(1)
    
    print("=" * 50)
    print("Graphify 自动更新守护进程")
    print("=" * 50)
    print(f"监控路径: {vault_path}")
    print(f"更新脚本: {update_script}")
    print(f"更新间隔: 3 秒（防抖）")
    print("-" * 50)
    print("按 Ctrl+C 停止监控")
    print("=" * 50)
    
    # 初始化观察者
    event_handler = GraphifyHandler(vault_path, update_script)
    observer = Observer()
    observer.schedule(event_handler, vault_path, recursive=True)
    observer.start()
    
    # 首次更新
    print("\n执行首次更新...")
    subprocess.run(['python3', update_script, vault_path])
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n停止监控...")
        observer.stop()
    
    observer.join()
    print("守护进程已停止")


if __name__ == '__main__':
    main()