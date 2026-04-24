#!/usr/bin/env python3
"""
知识图谱分析器
分析笔记网络的中心性、桥梁节点、子网络

使用方法:
    python3 graph_analyzer.py /path/to/obsidian-notes
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# 默认 vault 路径
DEFAULT_VAULT = "/mnt/d/obsidian-notes"


def extract_wiki_links(content):
    """提取笔记中的 Wiki 链接"""
    pattern = r'\[\[([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    return [m.strip().split('|')[0].strip() for m in matches]


def build_graph(vault_path):
    """构建知识图谱"""
    nodes = {}
    edges = []
    
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
                
                nodes[note_name] = {
                    'path': file_path,
                    'out_links': wiki_links,
                    'in_links': []
                }
                
                for link in wiki_links:
                    edges.append((note_name, link))
    
    # 计算入链
    for source, target in edges:
        if target in nodes:
            nodes[target]['in_links'].append(source)
    
    return nodes, edges


def calculate_degree_centrality(nodes):
    """计算度中心性（连接数）"""
    centrality = {}
    for name, info in nodes.items():
        # 总连接数 = 出链 + 入链
        out_degree = len(info['out_links'])
        in_degree = len(info['in_links'])
        centrality[name] = {
            'total': out_degree + in_degree,
            'out': out_degree,
            'in': in_degree
        }
    return centrality


def find_bridges(nodes, edges):
    """识别桥梁节点（连接不同子网络的节点）"""
    # 使用简单的启发式：连接了多个不同分类的笔记
    bridges = []
    
    for name, info in nodes.items():
        if len(info['in_links']) >= 2:
            # 检查入链来源的多样性
            sources = set(info['in_links'])
            if len(sources) >= 2:
                bridges.append({
                    'name': name,
                    'connections': len(info['in_links']),
                    'sources': list(sources)[:5]
                })
    
    return sorted(bridges, key=lambda x: x['connections'], reverse=True)


def find_clusters(nodes):
    """识别知识簇（紧密连接的笔记群）"""
    # 简单实现：找出相互连接的笔记组
    visited = set()
    clusters = []
    
    def dfs(node, cluster):
        if node in visited or node not in nodes:
            return
        visited.add(node)
        cluster.append(node)
        
        for link in nodes[node]['out_links']:
            if link in nodes and link not in visited:
                dfs(link, cluster)
        
        for source in nodes[node]['in_links']:
            if source not in visited:
                dfs(source, cluster)
    
    for name in nodes:
        if name not in visited:
            cluster = []
            dfs(name, cluster)
            if len(cluster) >= 2:
                clusters.append(cluster)
    
    return sorted(clusters, key=len, reverse=True)


def analyze(nodes, edges):
    """执行完整分析"""
    centrality = calculate_degree_centrality(nodes)
    bridges = find_bridges(nodes, edges)
    clusters = find_clusters(nodes)
    
    return {
        'centrality': centrality,
        'bridges': bridges,
        'clusters': clusters
    }


def print_report(nodes, edges, analysis):
    """打印分析报告"""
    total = len(nodes)
    centrality = analysis['centrality']
    bridges = analysis['bridges']
    clusters = analysis['clusters']
    
    print("=" * 60)
    print("🕸️ 知识图谱分析报告")
    print("=" * 60)
    print(f"\n总节点数: {total}")
    print(f"总边数: {len(edges)}")
    print(f"平均连接数: {len(edges)*2/total:.1f}")
    
    # 核心节点（连接数最多）
    print("\n" + "=" * 60)
    print("⭐ 核心节点（连接数 TOP 10）")
    print("=" * 60)
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1]['total'], reverse=True)[:10]
    for i, (name, stats) in enumerate(sorted_nodes, 1):
        print(f"{i}. {name}")
        print(f"   总连接: {stats['total']} (出: {stats['out']}, 入: {stats['in']})")
    
    # 桥梁节点
    if bridges:
        print("\n" + "=" * 60)
        print("🌉 桥梁节点（连接多个笔记）")
        print("=" * 60)
        for i, bridge in enumerate(bridges[:10], 1):
            print(f"{i}. {bridge['name']} ({bridge['connections']} 个连接)")
    
    # 知识簇
    if clusters:
        print("\n" + "=" * 60)
        print("🔗 知识簇（紧密连接的笔记群）")
        print("=" * 60)
        for i, cluster in enumerate(clusters[:5], 1):
            print(f"\n簇 {i} ({len(cluster)} 个笔记):")
            print(f"   {', '.join(cluster[:8])}")
            if len(cluster) > 8:
                print(f"   ... 等 {len(cluster)} 个")
    
    # 边缘笔记（只有 1 个连接）
    print("\n" + "=" * 60)
    print("🍃 边缘笔记（连接数 <= 1）")
    print("=" * 60)
    low_connect = [(name, stats) for name, stats in centrality.items() if stats['total'] <= 1]
    if low_connect:
        print(f"共 {len(low_connect)} 篇")
        for name, stats in low_connect[:10]:
            print(f"   - {name} (连接数: {stats['total']})")
    else:
        print("无边缘笔记")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='知识图谱分析器')
    parser.add_argument('vault_path', nargs='?', default=DEFAULT_VAULT, help='Obsidian vault 路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    print(f"扫描 vault: {args.vault_path}")
    
    nodes, edges = build_graph(args.vault_path)
    analysis = analyze(nodes, edges)
    
    if args.json:
        import json
        print(json.dumps({
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'top_nodes': sorted(analysis['centrality'].items(), key=lambda x: x[1]['total'], reverse=True)[:10],
            'bridges': analysis['bridges'][:10],
            'clusters': analysis['clusters'][:5]
        }, ensure_ascii=False, indent=2))
    else:
        print_report(nodes, edges, analysis)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
