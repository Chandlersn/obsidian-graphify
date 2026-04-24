#!/usr/bin/env python3
"""
知识孤岛检测器
扫描所有笔记，检测无 Wiki 链接的笔记，并基于关键词建议可能的连接

使用方法:
    python3 island_detector.py /path/to/obsidian-notes
    python3 island_detector.py /path/to/obsidian-notes --suggest
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# 默认 vault 路径
DEFAULT_VAULT = "/mnt/d/obsidian-notes"


def extract_wiki_links(content):
    """提取笔记中的 Wiki 链接 [[笔记名]]"""
    pattern = r'\[\[([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    return [m.strip().split('|')[0].strip() for m in matches]  # 处理 [[笔记|别名]] 格式


def extract_keywords(content, title):
    """从笔记内容提取关键词"""
    keywords = set()
    
    # 从标题提取
    title_words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', title)
    keywords.update([w for w in title_words if len(w) >= 2])
    
    # 从 ## 关键概念 区块提取
    concept_pattern = r'## 关键概念\n([\s\S]*?)(?:\n---|\n## |$)'
    concept_match = re.search(concept_pattern, content)
    if concept_match:
        concept_section = concept_match.group(1)
        # 提取 **概念名** 格式
        concepts = re.findall(r'\*\*([^*]+)\*\*', concept_section)
        keywords.update(concepts)
    
    # 从 tags 提取
    tags_pattern = r'tags:\s*\[(.*?)\]'
    tags_match = re.search(tags_pattern, content)
    if tags_match:
        tags = tags_match.group(1)
        tag_list = re.findall(r'"([^"]+)"', tags)
        keywords.update(tag_list)
    
    # 过滤无意义词
    stop_words = {'的', '是', '在', '和', '与', '或', '等', '了', '对', '为', '这', '那', '如何', '什么', '为什么', '怎么'}
    keywords = keywords - stop_words
    
    return keywords


def scan_notes(vault_path):
    """扫描所有笔记，返回笔记信息字典"""
    notes = {}
    
    for root, dirs, files in os.walk(vault_path):
        # 跳过 .graphify 目录
        if '.graphify' in root:
            continue
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                note_name = file.replace('.md', '')
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                wiki_links = extract_wiki_links(content)
                keywords = extract_keywords(content, note_name)
                
                notes[note_name] = {
                    'path': file_path,
                    'wiki_links': wiki_links,
                    'keywords': keywords,
                    'has_outgoing': len(wiki_links) > 0,
                    'incoming_count': 0  # 后续计算
                }
    
    return notes


def calculate_incoming_links(notes):
    """计算每个笔记的入链数"""
    for note_name, note_info in notes.items():
        for link in note_info['wiki_links']:
            if link in notes:
                notes[link]['incoming_count'] += 1


def find_islands(notes):
    """找出孤岛笔记（无出链也无入链）"""
    islands = []
    
    for note_name, note_info in notes.items():
        if not note_info['has_outgoing'] and note_info['incoming_count'] == 0:
            islands.append({
                'name': note_name,
                'keywords': note_info['keywords'],
                'path': note_info['path']
            })
    
    return islands


def find_semi_islands(notes):
    """找出半孤岛笔记（有出链但无入链，或反之）"""
    semi_islands = []
    
    for note_name, note_info in notes.items():
        has_outgoing = note_info['has_outgoing']
        has_incoming = note_info['incoming_count'] > 0
        
        if (has_outgoing and not has_incoming) or (not has_outgoing and has_incoming):
            semi_islands.append({
                'name': note_name,
                'keywords': note_info['keywords'],
                'path': note_info['path'],
                'type': '只有出链' if has_outgoing else '只有入链'
            })
    
    return semi_islands


def suggest_connections(island, all_notes, top_n=5):
    """为孤岛笔记建议可能的连接"""
    suggestions = []
    island_keywords = island['keywords']
    
    for note_name, note_info in all_notes.items():
        if note_name == island['name']:
            continue
        
        # 计算关键词重叠
        overlap = island_keywords & note_info['keywords']
        if overlap:
            score = len(overlap)
            suggestions.append({
                'name': note_name,
                'score': score,
                'common_keywords': list(overlap)[:5]
            })
    
    # 按分数排序，返回 top N
    suggestions.sort(key=lambda x: x['score'], reverse=True)
    return suggestions[:top_n]


def print_report(islands, semi_islands, notes, suggest=False):
    """打印检测报告"""
    total = len(notes)
    island_count = len(islands)
    semi_count = len(semi_islands)
    
    print("=" * 60)
    print("📊 知识孤岛检测报告")
    print("=" * 60)
    print(f"\n总笔记数: {total}")
    print(f"孤岛笔记: {island_count} ({island_count/total*100:.1f}%)")
    print(f"半孤岛笔记: {semi_count} ({semi_count/total*100:.1f}%)")
    print(f"健康笔记: {total - island_count - semi_count} ({(total-island_count-semi_count)/total*100:.1f}%)")
    
    if islands:
        print("\n" + "=" * 60)
        print("🏝️ 孤岛笔记（无连接）")
        print("=" * 60)
        for i, island in enumerate(islands, 1):
            print(f"\n{i}. {island['name']}")
            print(f"   关键词: {', '.join(list(island['keywords'])[:5])}")
            
            if suggest:
                suggestions = suggest_connections(island, notes)
                if suggestions:
                    print(f"   建议连接:")
                    for s in suggestions[:3]:
                        print(f"     → [[{s['name']}]] (共同关键词: {', '.join(s['common_keywords'])})")
    
    if semi_islands:
        print("\n" + "=" * 60)
        print("🔗 半孤岛笔记（单向连接）")
        print("=" * 60)
        for i, semi in enumerate(semi_islands, 1):
            print(f"\n{i}. {semi['name']} ({semi['type']})")
            print(f"   关键词: {', '.join(list(semi['keywords'])[:5])}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='知识孤岛检测器')
    parser.add_argument('vault_path', nargs='?', default=DEFAULT_VAULT, help='Obsidian vault 路径')
    parser.add_argument('--suggest', action='store_true', help='显示连接建议')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    print(f"扫描 vault: {args.vault_path}")
    
    # 扫描笔记
    notes = scan_notes(args.vault_path)
    
    # 计算入链
    calculate_incoming_links(notes)
    
    # 找出孤岛
    islands = find_islands(notes)
    semi_islands = find_semi_islands(notes)
    
    # 输出报告
    if args.json:
        import json
        result = {
            'total': len(notes),
            'islands': islands,
            'semi_islands': semi_islands
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(islands, semi_islands, notes, suggest=args.suggest)
    
    return 0 if len(islands) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
