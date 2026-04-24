#!/usr/bin/env python3
"""
笔记质量检查器
检查笔记格式是否符合规范

使用方法:
    python3 quality_checker.py /path/to/obsidian-notes
    python3 quality_checker.py /path/to/obsidian-notes --fix
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# 默认 vault 路径
DEFAULT_VAULT = "/mnt/d/obsidian-notes"


def extract_frontmatter(content):
    """提取 YAML frontmatter"""
    if not content.startswith('---'):
        return None, content
    
    end = content.find('---', 3)
    if end == -1:
        return None, content
    
    frontmatter_text = content[3:end].strip()
    body = content[end + 3:].strip()
    
    # 解析 YAML
    result = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip().strip('"\'')
    
    return result, body


def check_frontmatter(frontmatter):
    """检查 frontmatter 是否完整"""
    issues = []
    
    # 必需字段
    required = ['type', 'created', 'tags']
    for field in required:
        if field not in frontmatter:
            issues.append(f"缺少必需字段: {field}")
    
    # type 字段检查
    if 'type' in frontmatter:
        valid_types = [
            'original', 'material', 'project', 'system',
            'philosophy-index', 'philosophy-card', 'philosophy-guide', 'philosophy-explanation',
            'Material'  # 兼容旧格式
        ]
        if frontmatter['type'] not in valid_types:
            issues.append(f"type 值无效: {frontmatter['type']} (应为: original, material, project, system, philosophy-*)")
    
    # created 字段检查
    if 'created' in frontmatter:
        try:
            datetime.strptime(frontmatter['created'], '%Y-%m-%d')
        except ValueError:
            issues.append(f"created 格式无效: {frontmatter['created']} (应为: YYYY-MM-DD)")
    
    return issues


def check_body(body, title):
    """检查正文格式"""
    issues = []
    
    # 检查是否有核心观点（> 开头的引用块）
    if not re.search(r'^>\s*.+', body, re.MULTILINE):
        issues.append("缺少核心观点（> 一句话概括）")
    
    # 检查是否有关键概念区块
    if '## 关键概念' not in body:
        issues.append("缺少 ## 关键概念 区块")
    
    # 检查是否有相关笔记区块
    if '## 相关笔记' not in body:
        issues.append("缺少 ## 相关笔记 区块（建议添加 Wiki 链接）")
    
    # 检查标题是否重复
    if f"# {title}" in body:
        pass  # 正确
    else:
        # 检查是否有任意一级标题
        if not re.search(r'^#\s+.+', body, re.MULTILINE):
            issues.append("缺少一级标题")
    
    return issues


def check_wiki_links(body):
    """检查 Wiki 链接格式"""
    issues = []
    
    # 检查是否有空的 Wiki 链接 [[]]
    if re.search(r'\[\[\s*\]\]', body):
        issues.append("存在空的 Wiki 链接 [[]]")
    
    # 检查是否有格式错误的链接（缺少 ]）
    broken = re.findall(r'\[\[[^\]]+$', body, re.MULTILINE)
    if broken:
        issues.append(f"存在格式错误的 Wiki 链接: {broken[:2]}")
    
    return issues


def check_note(file_path):
    """检查单个笔记"""
    note_name = os.path.basename(file_path).replace('.md', '')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    frontmatter, body = extract_frontmatter(content)
    
    all_issues = []
    
    # 检查 frontmatter
    if frontmatter is None:
        all_issues.append("缺少 YAML frontmatter")
    else:
        all_issues.extend(check_frontmatter(frontmatter))
    
    # 检查正文
    all_issues.extend(check_body(body, note_name))
    
    # 检查 Wiki 链接
    all_issues.extend(check_wiki_links(body))
    
    return {
        'name': note_name,
        'path': file_path,
        'issues': all_issues,
        'quality': 'good' if len(all_issues) == 0 else 'needs_fix' if len(all_issues) <= 3 else 'poor'
    }


def scan_notes(vault_path):
    """扫描所有笔记"""
    results = []
    
    for root, dirs, files in os.walk(vault_path):
        # 跳过 .graphify 目录
        if '.graphify' in root:
            continue
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                result = check_note(file_path)
                results.append(result)
    
    return results


def print_report(results):
    """打印质量报告"""
    total = len(results)
    good = sum(1 for r in results if r['quality'] == 'good')
    needs_fix = sum(1 for r in results if r['quality'] == 'needs_fix')
    poor = sum(1 for r in results if r['quality'] == 'poor')
    
    print("=" * 60)
    print("📋 笔记质量检查报告")
    print("=" * 60)
    print(f"\n总笔记数: {total}")
    print(f"✅ 优质笔记: {good} ({good/total*100:.1f}%)")
    print(f"⚠️  需修复: {needs_fix} ({needs_fix/total*100:.1f}%)")
    print(f"❌ 质量差: {poor} ({poor/total*100:.1f}%)")
    
    # 显示需修复的笔记
    needs_fix_notes = [r for r in results if r['quality'] != 'good']
    if needs_fix_notes:
        print("\n" + "=" * 60)
        print("需要改进的笔记")
        print("=" * 60)
        
        for i, note in enumerate(needs_fix_notes, 1):
            status = "⚠️" if note['quality'] == 'needs_fix' else "❌"
            print(f"\n{status} {i}. {note['name']}")
            for issue in note['issues']:
                print(f"     - {issue}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='笔记质量检查器')
    parser.add_argument('vault_path', nargs='?', default=DEFAULT_VAULT, help='Obsidian vault 路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    print(f"扫描 vault: {args.vault_path}")
    
    results = scan_notes(args.vault_path)
    
    if args.json:
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_report(results)
    
    # 返回码：有问题返回 1，没问题返回 0
    has_issues = any(r['quality'] != 'good' for r in results)
    return 1 if has_issues else 0


if __name__ == '__main__':
    sys.exit(main())
