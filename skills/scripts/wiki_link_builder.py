#!/usr/bin/env python3
"""
Wiki 链接自动建立脚本 v2.2
适配简化模板：匹配 "## 关键概念" 区块

使用方法:
  python wiki_link_builder.py <new_note_path> [--vault <vault_path>]

示例:
  python wiki_link_builder.py "/mnt/d/obsidian-notes/02-Knowledge/Wisdom/真正的智慧从何而来.md"
"""

import os
import re
import sys
from collections import Counter

# ==================== 配置 ====================
DEFAULT_VAULT = "/mnt/d/obsidian-notes"
MIN_MATCH_COUNT = 2
MAX_LINKS = 8

# 语义匹配规则
SEMANTIC_GROUPS = {
    '智慧': ['智慧', '道理', '开窍', '顿悟'],
    '认知': ['认知', '体系', '转变', '开窍'],
    '创造力': ['创造力', '创造'],
    '时间': ['时间', '意识', '精神'],
    '沟通': ['沟通', '道理', '包装'],
    '悲剧': ['悲剧', '苦难', '表达'],
    '生命': ['生命', '活着', '死亡'],
    '哲学': ['哲学', '思考', '反思'],
}
# ==============================================

def extract_keywords(content):
    """从文档内容提取关键词（适配简化模板）"""
    # 新格式：## 关键概念
    concept_pattern = r'## 关键概念\n([\s\S]*?)(?:\n---|\n## |$)'
    concept_match = re.search(concept_pattern, content)
    
    keywords = []
    if concept_match:
        # 匹配 "- **概念名** → 解释"
        bullet_pattern = r'- \*\*([^*]+)\*\* →'
        keywords = re.findall(bullet_pattern, concept_match.group(1))
        keywords = [k.strip() for k in keywords]
    
    # 补充：从 tags 字段提取
    tags_pattern = r'tags: \[([^\]]+)\]'
    tags_match = re.search(tags_pattern, content)
    if tags_match:
        tags_str = tags_match.group(1)
        tags = re.findall(r'"([^"]+)"', tags_str)
        keywords.extend(tags)
    
    # 补充：高频词
    words = re.findall(r'[\u4e00-\u9fa5]{2,8}', content)
    word_freq = Counter(words)
    high_freq = [w for w, c in word_freq.most_common(20) 
                 if c >= MIN_MATCH_COUNT and len(w) >= 3]
    keywords.extend(high_freq[:5])
    
    return list(set(keywords))[:15]

def get_semantic_tags(text):
    """从文本提取语义标签"""
    tags = []
    for group, keywords in SEMANTIC_GROUPS.items():
        if any(kw in text for kw in keywords):
            tags.append(group)
    return tags

def get_category(file_path, vault_path):
    rel_path = os.path.relpath(file_path, vault_path)
    parts = rel_path.split(os.sep)
    return parts[0] if len(parts) > 1 else "Root"

def scan_vault_for_keywords(vault_path, exclude_note=None):
    """扫描 vault，建立关键词→笔记映射"""
    keyword_to_notes = {}
    
    for root, dirs, files in os.walk(vault_path):
        if '.graphify' in root:
            continue
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if exclude_note and file_path == exclude_note:
                    continue
                
                note_name = file[:-3]
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    continue
                
                keywords = extract_keywords(content)
                for kw in keywords:
                    if kw not in keyword_to_notes:
                        keyword_to_notes[kw] = []
                    keyword_to_notes[kw].append({
                        'name': note_name,
                        'path': file_path,
                        'category': get_category(file_path, vault_path)
                    })
    
    return keyword_to_notes

def find_related_notes(new_note_path, vault_path):
    """找出与新笔记相关的现有笔记"""
    with open(new_note_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    note_name = os.path.basename(new_note_path)[:-3]
    
    # 关键词匹配
    new_keywords = extract_keywords(content)
    keyword_to_notes = scan_vault_for_keywords(vault_path, exclude_note=new_note_path)
    
    note_scores = {}
    for kw in new_keywords:
        if kw in keyword_to_notes:
            for note_info in keyword_to_notes[kw]:
                name = note_info['name']
                if name not in note_scores:
                    note_scores[name] = {'score': 0, 'matched_keywords': [], 'info': note_info}
                note_scores[name]['score'] += 1
                note_scores[name]['matched_keywords'].append(kw)
    
    # 语义匹配
    my_tags = get_semantic_tags(note_name)
    
    for root, dirs, files in os.walk(vault_path):
        if '.graphify' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                other_name = file[:-3]
                other_path = os.path.join(root, file)
                if other_path == new_note_path:
                    continue
                
                other_tags = get_semantic_tags(other_name)
                common_tags = set(my_tags) & set(other_tags)
                
                if common_tags:
                    if other_name not in note_scores:
                        note_scores[other_name] = {
                            'score': len(common_tags),
                            'matched_keywords': list(common_tags),
                            'info': {'name': other_name, 'path': other_path, 
                                     'category': get_category(other_path, vault_path)}
                        }
                    else:
                        note_scores[other_name]['score'] += len(common_tags)
                        note_scores[other_name]['matched_keywords'].extend(common_tags)
    
    # 按得分排序
    sorted_notes = sorted(note_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    
    return sorted_notes[:MAX_LINKS]

def add_wiki_links(note_path, related_notes):
    """在笔记中添加 wiki 链接（适配简化模板）"""
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 构建链接列表
    link_lines = []
    for note_name, data in related_notes:
        keywords = data['matched_keywords'][:3]
        link_lines.append(f"- [[{note_name}]] ({'、'.join(keywords)})")
    
    # 检查是否已有相关笔记区块
    if '## 相关笔记' in content:
        # 替换现有区块中的占位符
        placeholder_pattern = r'(## 相关笔记\n)([\s\S]*?)(\n---)'
        placeholder_match = re.search(placeholder_pattern, content)
        
        if placeholder_match:
            # 检查是否只有占位符
            existing = placeholder_match.group(2).strip()
            if existing == "- [[]]" or existing == "":
                # 替换占位符
                new_block = placeholder_match.group(1) + "\n" + "\n".join(link_lines) + "\n" + placeholder_match.group(3)
                content = content[:placeholder_match.start()] + new_block + content[placeholder_match.end():]
                
                with open(note_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return len(related_notes)
            else:
                # 已有实际链接，跳过
                print(f"  ⏭ 已存在相关笔记链接，跳过")
                return 0
    
    # 在关键概念后添加相关笔记区块
    concept_pattern = r'## 关键概念\n([\s\S]*?)(\n---)'
    concept_match = re.search(concept_pattern, content)
    
    if concept_match:
        # 在关键概念后的 --- 后添加
        insert_pos = concept_match.end()
        link_block = "\n\n## 相关笔记\n\n" + "\n".join(link_lines) + "\n\n---"
        content = content[:insert_pos] + link_block + content[insert_pos:]
    else:
        # 末尾添加
        content += "\n\n---\n\n## 相关笔记\n\n" + "\n".join(link_lines) + "\n\n---"
    
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return len(related_notes)

def main():
    if len(sys.argv) < 2:
        print("使用方法: python wiki_link_builder.py <note_path> [--vault <vault_path>]")
        print("示例: python wiki_link_builder.py '/mnt/d/obsidian-notes/02-Knowledge/Wisdom/真正的智慧从何而来.md'")
        return
    
    note_path = sys.argv[1]
    vault_path = sys.argv[3] if len(sys.argv) >= 4 and sys.argv[2] == '--vault' else DEFAULT_VAULT
    
    if not os.path.exists(note_path):
        print(f"❌ 笔记不存在: {note_path}")
        return
    
    print(f"分析笔记: {os.path.basename(note_path)}")
    
    related_notes = find_related_notes(note_path, vault_path)
    
    if not related_notes:
        print("⚠️ 未找到相关笔记")
        return
    
    print(f"发现 {len(related_notes)} 个相关笔记:")
    for note_name, data in related_notes:
        keywords = data['matched_keywords'][:3]
        print(f"  - {note_name} (匹配: {'、'.join(keywords)})")
    
    link_count = add_wiki_links(note_path, related_notes)
    if link_count > 0:
        print(f"✅ 已添加 {link_count} 个 wiki 链接")

if __name__ == '__main__':
    main()