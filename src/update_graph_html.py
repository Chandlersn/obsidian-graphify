#!/usr/bin/env python3
"""
Graphify 数据生成脚本
从 Obsidian vault 提取笔记并生成图谱数据

使用方法:
    python update_graph_html.py /path/to/your/obsidian-notes

配置:
    修改下方 OBSIDIAN_VAULT 为你的 vault 路径
"""

import os
import re
import json
from pathlib import Path

# ==================== 用户配置 ====================
# 修改这里为你的 Obsidian vault 路径
OBSIDIAN_VAULT = "/mnt/d/obsidian-notes"
GRAPHIFY_DIR = os.path.join(OBSIDIAN_VAULT, ".graphify")
HTML_TEMPLATE = os.path.join(GRAPHIFY_DIR, "graph_fixed_beautiful.html")
OUTPUT_HTML = os.path.join(GRAPHIFY_DIR, "graph.html")
# ================================================


def extract_wiki_links(content):
    """提取笔记中的 Wiki 链接 [[笔记名]]"""
    pattern = r'\[\[([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    return [m.strip() for m in matches]


def extract_frontmatter(content):
    """提取 YAML frontmatter"""
    if not content.startswith('---'):
        return {}
    
    end = content.find('---', 3)
    if end == -1:
        return {}
    
    frontmatter_text = content[3:end].strip()
    result = {}
    
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip().strip('"\'')
    
    return result


def get_note_category(file_path, vault_path):
    """根据文件路径确定分类"""
    rel_path = os.path.relpath(file_path, vault_path)
    parts = rel_path.split(os.sep)
    
    if len(parts) >= 2:
        category = parts[0]
        # 映射分类名
        category_map = {
            '01-System': 'System',
            '02-Knowledge': 'Knowledge',
            '03-Projects': 'Projects',
            '04-Materials': 'Materials',
            '04-Templates': 'Templates'
        }
        return category_map.get(category, category)
    
    return 'General'


def scan_notes(vault_path):
    """扫描 vault 中的所有笔记"""
    notes = []
    
    for root, dirs, files in os.walk(vault_path):
        # 跳过 .graphify 目录
        if '.graphify' in root:
            continue
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取信息
                frontmatter = extract_frontmatter(content)
                wiki_links = extract_wiki_links(content)
                
                # 笔记名（去除 .md 后缀）
                note_name = file.replace('.md', '')
                
                # 分类
                category = get_note_category(file_path, vault_path)
                
                # 预览内容（去除 frontmatter 后的前 100 字）
                preview_start = content.find('---', 3) + 3 if content.startswith('---') else 0
                preview = content[preview_start:preview_start + 100].strip()
                
                notes.append({
                    'id': len(notes) + 1,
                    'label': note_name,
                    'group': category,
                    'tooltip': preview,
                    'file_path': os.path.relpath(file_path, vault_path),
                    'type': frontmatter.get('type', 'original'),
                    'wiki_links': wiki_links,
                    'connections': len(wiki_links)
                })
    
    return notes


def build_edges(notes):
    """构建边（Wiki 链接连接）"""
    edges = []
    note_names = {n['label']: n['id'] for n in notes}
    
    for note in notes:
        for link in note['wiki_links']:
            if link in note_names:
                edges.append({
                    'from': note['id'],
                    'to': note_names[link],
                    'type': 'wiki-link'
                })
    
    return edges


def generate_graph_data(vault_path):
    """生成图谱数据"""
    notes = scan_notes(vault_path)
    edges = build_edges(notes)
    
    return {
        'nodes': notes,
        'edges': edges
    }


def update_html(graph_data, template_path, output_path, vault_name=None):
    """更新 HTML 文件中的数据"""
    # 如果模板不存在，使用内置模板
    if not os.path.exists(template_path):
        print(f"模板文件不存在: {template_path}")
        print("请确保 graph_fixed_beautiful.html 存在于 .graphify 目录")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 替换数据块（使用更精确的正则）
    data_json = json.dumps(graph_data, ensure_ascii=False, indent=4)
    
    # 查找并替换整个 graphData 定义块（包含 nodes 和 edges）
    # 匹配从 const graphData = { 到 }; 为止
    pattern = r'const graphData = \{\s*"nodes":\s*\[[^\]]*\],\s*"edges":\s*\[[^\]]*\]\s*\};'
    
    # 构建新的 graphData（确保格式正确）
    new_graph_data = f'const graphData = {data_json};'
    
    new_html = re.sub(pattern, new_graph_data, html_content, count=1)
    
    # 如果正则匹配失败，尝试更宽松的匹配
    if new_html == html_content:
        # 使用标记区域替换
        start_marker = '// ========== Dynamic data area - modify directly here =========='
        end_marker = '// ======================================================'
        
        start_idx = html_content.find(start_marker)
        end_idx = html_content.find(end_marker, start_idx)
        
        if start_idx != -1 and end_idx != -1:
            # 构建新的数据块
            new_block = f'''{start_marker}
        // 自动生成 - 请勿手动修改
        const graphData = {data_json};
        {end_marker}'''
            
            new_html = html_content[:start_idx] + new_block + html_content[end_idx + len(end_marker):]
            print("   使用标记区域替换")
        else:
            print("⚠️ 未找到数据区域标记")
            return False
    
    # 更新 vault 名称（如果提供）
    if vault_name:
        vault_pattern = r'const OBSIDIAN_VAULT_NAME = "[^"]*";'
        vault_replacement = f'const OBSIDIAN_VAULT_NAME = "{vault_name}";'
        new_html = re.sub(vault_pattern, vault_replacement, new_html, count=1)
        print(f"   Vault 名称: {vault_name}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✅ 更新完成: {output_path}")
    print(f"   节点数: {len(graph_data['nodes'])}")
    print(f"   边数: {len(graph_data['edges'])}")
    
    return True


def main():
    # 支持命令行参数
    import sys
    
    vault_path = sys.argv[1] if len(sys.argv) > 1 else OBSIDIAN_VAULT
    
    if vault_path == "/path/to/your/obsidian-notes":
        print("⚠️ 请先配置你的 Obsidian vault 路径！")
        print("   方法1: 修改脚本中的 OBSIDIAN_VAULT")
        print("   方法2: 命令行传入路径 python update_graph_html.py /your/path")
        return
    
    print(f"扫描 vault: {vault_path}")
    
    # 从路径提取 vault 名称
    vault_name = os.path.basename(vault_path.rstrip('/'))
    
    graph_data = generate_graph_data(vault_path)
    
    # 模板使用 graph_fixed_beautiful.html，输出到 graph.html
    template_path = HTML_TEMPLATE
    
    # 如果输出文件不存在，先复制模板
    if not os.path.exists(OUTPUT_HTML):
        import shutil
        shutil.copy(HTML_TEMPLATE, OUTPUT_HTML)
        print(f"   初始化: 从模板创建 {OUTPUT_HTML}")
    
    update_html(graph_data, template_path, OUTPUT_HTML, vault_name)


if __name__ == '__main__':
    main()