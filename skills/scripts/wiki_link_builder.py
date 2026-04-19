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
    """从文档内容提取关键词（适配多种模板格式）"""
    keywords = []
    
    # 1. 从标题提取（H1）
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        title_keywords = re.findall(r'[知识|图谱|系统|Agent|技能|笔记|认知|智慧|时间|沟通|创造|哲学][图谱|系统|技能|笔记|脉络|链接|统计|分析]*', title)
        keywords.extend([k for k in title_keywords if len(k) >= 2])
    
    # 2. 从 tags 字段提取（支持两种格式）
    tags_pattern1 = r'tags:\s*\[([^\]]+)\]'
    tags_match1 = re.search(tags_pattern1, content)
    if tags_match1:
        tags_str = tags_match1.group(1)
        tags = re.findall(r'"([^"]+)"', tags_str)
        keywords.extend(tags)
    
    tags_pattern2 = r'tags:\s*\n((?:\s*- .+\n)+)'
    tags_match2 = re.search(tags_pattern2, content)
    if tags_match2:
        tags = re.findall(r'- (.+)', tags_match2.group(1))
        keywords.extend([t.strip() for t in tags])
    
    # 3. 从 ## 关键概念 区块提取
    concept_pattern = r'## 关键概念\n([\s\S]*?)(?:\n---|\n## |$)'
    concept_match = re.search(concept_pattern, content)
    if concept_match:
        bullet_pattern = r'- \*\*([^*]+)\*\* →'
        concept_keywords = re.findall(bullet_pattern, concept_match.group(1))
        keywords.extend([k.strip() for k in concept_keywords])
    
    # 4. 从 ## 核心主题 提取（旧格式）
    core_pattern = r'## 核心主题\n([\s\S]*?)(?:\n## |$)'
    core_match = re.search(core_pattern, content)
    if core_match:
        core_keywords = re.findall(r'- (.+)', core_match.group(1))
        keywords.extend([k.strip() for k in core_keywords])
    
    # 5. 高频词补充
    words = re.findall(r'[\u4e00-\u9fa5]{2,8}', content)
    word_freq = Counter(words)
    stopwords = {'的', '是', '在', '有', '和', '与', '或', '等', '这', '那', '一个', '什么', '怎么', '如何', '可以', '能够', '已经', '还是', '但是', '因为', '所以', '如果', '那么', '只是', '就是', '不是', '没有', '现在', '之前', '之后', '下面', '上面', '里面', '外面', '一起', '你的', '我的', '他的', '这个', '那个', '这些', '那些', '让你的'}
    high_freq = [w for w, c in word_freq.most_common(30) 
                 if c >= MIN_MATCH_COUNT and len(w) >= 3 and w not in stopwords]
    keywords.extend(high_freq[:8])
    
    unique_keywords = list(set(keywords))
    unique_keywords = [k for k in unique_keywords if len(k) >= 2 and k not in stopwords]
    
    return unique_keywords[:20]

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

def scan_vault_for_keywords(vault_path, exclude_note=None, exclude_dirs=None):
    """扫描 vault，建立关键词→笔记映射
    
    Args:
        vault_path: vault 根目录
        exclude_note: 要排除的笔记路径（通常是当前笔记）
        exclude_dirs: 要排除的目录列表，默认 ['.graphify']
                       设置为 [] 则不排除任何目录
    """
    if exclude_dirs is None:
        exclude_dirs = ['.graphify']  # 默认排除
    
    keyword_to_notes = {}
    
    for root, dirs, files in os.walk(vault_path):
        # 检查是否要排除此目录
        skip = False
        for exclude_dir in exclude_dirs:
            if exclude_dir in root:
                skip = True
                break
        if skip:
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

def find_related_notes(new_note_path, vault_path, exclude_dirs=None):
    """找出与新笔记相关的现有笔记
    
    Args:
        exclude_dirs: 要排除的目录列表，默认 ['.graphify']
                     设置为 [] 则包含所有目录（用于链接 .graphify 内容）
    """
    if exclude_dirs is None:
        exclude_dirs = ['.graphify']
    
    with open(new_note_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    note_name = os.path.basename(new_note_path)[:-3]
    
    # 关键词匹配
    new_keywords = extract_keywords(content)
    keyword_to_notes = scan_vault_for_keywords(vault_path, exclude_note=new_note_path, exclude_dirs=exclude_dirs)
    
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
        # 检查是否要排除此目录
        skip = False
        for exclude_dir in exclude_dirs:
            if exclude_dir in root:
                skip = True
                break
        if skip:
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
        print("使用方法: python wiki_link_builder.py <note_path> [--vault <vault_path>] [--include-graphify]")
        print("示例: python wiki_link_builder.py '/mnt/d/obsidian-notes/02-Knowledge/Wisdom/真正的智慧从何而来.md'")
        print("      python wiki_link_builder.py '/mnt/d/obsidian-notes/03-Material/文章.md' --include-graphify")
        print("\n选项:")
        print("  --include-graphify  包含 .graphify 目录中的笔记（用于链接项目文档）")
        return
    
    note_path = sys.argv[1]
    vault_path = DEFAULT_VAULT
    exclude_dirs = ['.graphify']  # 默认排除
    
    # 解析参数
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == '--vault' and i + 1 < len(args):
            vault_path = args[i + 1]
        elif arg == '--include-graphify':
            exclude_dirs = []  # 不排除任何目录
    
    if not os.path.exists(note_path):
        print(f"❌ 笔记不存在: {note_path}")
        return
    
    print(f"分析笔记: {os.path.basename(note_path)}")
    if exclude_dirs:
        print(f"排除目录: {exclude_dirs}")
    else:
        print("包含所有目录（含 .graphify）")
    
    related_notes = find_related_notes(note_path, vault_path, exclude_dirs)
    
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