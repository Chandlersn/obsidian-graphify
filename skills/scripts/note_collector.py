#!/usr/bin/env python3
"""
笔记自动化收录脚本 v2.2
简化模板格式：YAML 4行 + 正文 + 关键概念 + 相关笔记

使用方法:
    python note_collector.py --content "文章内容" --title "标题" --source "wechat"
    python note_collector.py --file "/path/to/article.md" --source "web"
"""

import os
import re
import sys
import json
import argparse
import yaml
from datetime import datetime
from pathlib import Path

# ==================== 配置 ====================
# 支持环境变量配置，默认值用于向后兼容
VAULT_PATH = os.environ.get("OBSIDIAN_VAULT_PATH", "/mnt/d/obsidian-notes")
GRAPHIFY_DIR = os.path.join(VAULT_PATH, ".graphify")
CONFIG_PATH = os.environ.get(
    "GRAPHIFY_CONFIG_PATH",
    os.path.join(GRAPHIFY_DIR, "github-repo", "config", "config.yaml")
)

# 默认分类规则（向后兼容）
DEFAULT_CATEGORY_RULES = {
    "Knowledge": {
        "keywords": ["知识", "概念", "原理", "方法", "技巧", "理论", "AI", "LLM", "架构", "设计"],
        "subcategories": {
            "Wisdom": ["智慧", "认知", "哲学", "思考", "道理", "人生", "顿悟"],
            "AI-ML": ["AI", "机器学习", "LLM", "模型", "Agent", "神经网络"],
            "Architecture": ["架构", "系统设计", "分布式", "微服务"],
            "Tools": ["工具", "技巧", "Obsidian", "Git", "Python"],
            "Research": ["研究", "论文", "实验", "方法论"]
        }
    },
    "Projects": {
        "keywords": ["项目", "开发", "实现", "集成", "部署", "Graphify", "Hermes"],
        "subcategories": {
            "Graphify": ["Graphify", "图谱", "知识图谱"],
            "Hermes-Agent": ["Hermes", "Agent", "飞书"],
            "Integration": ["集成", "对接", "API"]
        }
    },
    "Materials": {
        "keywords": [],
        "subcategories": {
            "Articles": ["文章", "收藏"],
            "Feishu": ["飞书"],
            "References": ["参考", "API文档"]
        }
    },
    "System": {
        "keywords": ["系统", "配置", "核心", "设计理念", "SOUL"],
        "subcategories": {
            "Core": ["核心", "SOUL", "设计理念"],
            "Config": ["配置", "技能"]
        }
    }
}

def load_category_rules():
    """从 config.yaml 加载分类规则，失败则返回默认规则"""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if config and 'categories' in config:
                    # 转换 config.yaml 格式为内部格式
                    rules = {}
                    for cat, cat_config in config['categories'].items():
                        rules[cat] = {
                            'keywords': cat_config.get('keywords', []),
                            'subcategories': {}
                        }
                        for subcat, subcat_config in cat_config.get('subcategories', {}).items():
                            rules[cat]['subcategories'][subcat] = subcat_config.get('keywords', [])
                    return rules
    except Exception as e:
        print(f"[Warning] Failed to load config.yaml: {e}, using default rules")
    
    return DEFAULT_CATEGORY_RULES
# ==============================================

class NoteCollector:
    def __init__(self, vault_path=VAULT_PATH):
        self.vault_path = vault_path
        self.category_rules = load_category_rules()
        
    def analyze_content(self, content, title):
        """分析内容，提取关键信息"""
        keywords = self._extract_keywords(content, title)
        category, subcategory = self._classify(title, content, keywords)
        key_concepts = self._extract_key_concepts(content, keywords)
        summary = self._generate_summary(content, title)
        
        return {
            "keywords": keywords,
            "category": category,
            "subcategory": subcategory,
            "key_concepts": key_concepts,
            "summary": summary,
            "tags": keywords[:5]
        }
    
    def _extract_keywords(self, content, title=""):
        """提取关键词"""
        domain_keywords = [
            "认知", "智慧", "哲学", "思考", "道理", "人生", "顿悟", "开窍",
            "AI", "机器学习", "LLM", "模型", "Agent", "神经网络",
            "架构", "系统设计", "分布式", "微服务",
            "工具", "技巧", "Obsidian", "Git", "Python",
            "研究", "论文", "实验", "方法论",
            "项目", "开发", "实现", "集成", "部署",
            "时间", "意识", "精神", "创造力", "沟通", "悲剧", "苦难"
        ]
        
        text = title + " " + content
        matched = [kw for kw in domain_keywords if kw in text]
        
        title_short = re.findall(r'[\u4e00-\u9fa5]{2,4}', title)
        title_kw = [w for w in title_short if w not in ["如何", "什么", "为什么", "怎么"]]
        
        keywords = list(set(matched + title_kw))
        return keywords[:12]
    
    def _classify(self, title, content, keywords):
        """自动分类"""
        text = title + " " + content[:500]
        
        best_category = "Materials"
        best_subcategory = "Articles"
        best_score = 0
        
        for cat, rules in self.category_rules.items():
            cat_score = sum(1 for kw in rules["keywords"] if kw in text)
            
            for subcat, sub_kw in rules["subcategories"].items():
                sub_score = sum(1 for kw in sub_kw if kw in text)
                total_score = cat_score + sub_score
                
                if total_score > best_score:
                    best_score = total_score
                    best_category = cat
                    best_subcategory = subcat
        
        return best_category, best_subcategory
    
    def _extract_key_concepts(self, content, keywords):
        """提取核心概念"""
        concepts = []
        for kw in keywords[:8]:
            sentences = re.findall(r'[^。]*' + kw + r'[^。]*。', content)
            if sentences:
                explanation = sentences[0][:50] + "..." if len(sentences[0]) > 50 else sentences[0]
                concepts.append({"name": kw, "desc": explanation})
        
        if not concepts:
            concepts = [{"name": "概念1", "desc": "待提炼"}, {"name": "概念2", "desc": "待提炼"}]
        
        return concepts
    
    def _generate_summary(self, content, title):
        """生成摘要"""
        first_para = content.split('\n\n')[0] if '\n\n' in content else content[:100]
        clean = re.sub(r'[#\*\>\-\n]', ' ', first_para)
        return clean[:80] + "..." if len(clean) > 80 else clean
    
    def format_note(self, title, content, source, author="", 
                    type_override=None, category_override=None, subcategory_override=None):
        """格式化笔记（简化模板）"""
        analysis = self.analyze_content(content, title)
        
        note_type = type_override or ("original" if source == "user" else "collected")
        category = category_override or analysis["category"]
        subcategory = subcategory_override or analysis["subcategory"]
        
        # 简化 YAML（4行）
        yaml_lines = [
            "---",
            f"type: {note_type}",
            f"created: {datetime.now().strftime('%Y-%m-%d')}",
            f'tags: {json.dumps(analysis["tags"], ensure_ascii=False)}',
            "---"
        ]
        
        # 标题和摘要
        header = [
            f"# {title}",
            "",
            f"> {analysis['summary']}",
            ""
        ]
        
        # 正文（原样保留）
        body_lines = content.split('\n')
        
        # 关键概念
        concepts_lines = [
            "---",
            "",
            "## 关键概念",
            ""
        ]
        for concept in analysis["key_concepts"]:
            concepts_lines.append(f"- **{concept['name']}** → {concept['desc']}")
        
        # 相关笔记（预留）
        related_lines = [
            "",
            "---",
            "",
            "## 相关笔记",
            "",
            "- [[]]",
            "---"
        ]
        
        # 组合
        note = '\n'.join(yaml_lines + header + body_lines + concepts_lines + related_lines)
        
        return note, category, subcategory
    
    def get_save_path(self, title, category, subcategory):
        """获取保存路径"""
        if category == "Knowledge":
            base = os.path.join(self.vault_path, "02-Knowledge", subcategory)
        elif category == "Projects":
            base = os.path.join(self.vault_path, "03-Projects", subcategory)
        elif category == "Materials":
            base = os.path.join(self.vault_path, "04-Materials", subcategory)
        elif category == "System":
            base = os.path.join(self.vault_path, "01-System", subcategory)
        else:
            base = os.path.join(self.vault_path, "02-Knowledge")
        
        os.makedirs(base, exist_ok=True)
        
        filename = title + ".md"
        filepath = os.path.join(base, filename)
        
        # 文件名冲突处理
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime("%Y%m%d")
            filepath = os.path.join(base, f"{title}_{timestamp}.md")
        
        return filepath
    
    def save_note(self, title, content, source, author="", 
                  type_override=None, category_override=None, subcategory_override=None):
        """保存笔记"""
        note, category, subcategory = self.format_note(
            title, content, source, author, type_override, category_override, subcategory_override
        )
        
        filepath = self.get_save_path(title, category, subcategory)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(note)
            print(f"✅ 笔记已保存: {filepath}")
        except IOError as e:
            print(f"❌ 保存笔记失败: {filepath}")
            print(f"   错误: {e}")
            raise
        
        return filepath, category, subcategory
    
    def update_graph(self):
        """更新知识图谱"""
        update_script = os.path.join(GRAPHIFY_DIR, "github-repo/src/update_graph_html.py")
        
        if os.path.exists(update_script):
            import subprocess
            result = subprocess.run(
                ['python3', update_script, self.vault_path],
                capture_output=True, text=True
            )
            print(result.stdout)
            return result.returncode == 0
        return False
    
    def build_wiki_links(self, filepath):
        """建立 Wiki 链接"""
        link_script = os.path.join(GRAPHIFY_DIR, "github-repo/skills/scripts/wiki_link_builder.py")
        
        if os.path.exists(link_script):
            import subprocess
            result = subprocess.run(
                ['python3', link_script, filepath],
                capture_output=True, text=True
            )
            print(result.stdout)
            return result.returncode == 0
        return False
    
    def open_browser(self):
        """打开浏览器展示图谱"""
        import subprocess
        subprocess.run([
            'cmd.exe', '/c', 'start', '""',
            'D:\\obsidian-notes\\.graphify\\graph.html'
        ])
        print("🌐 浏览器已打开")
    
    def collect(self, title, content, source="user", author="", 
                ask_for_type=True, auto_open=True):
        """完整收录流程"""
        print(f"\n{'='*50}")
        print(f"笔记收录: {title}")
        print(f"{'='*50}")
        
        # Step 1: 分析内容
        print("\n[1] 分析内容...")
        analysis = self.analyze_content(content, title)
        print(f"   分类: {analysis['category']}/{analysis['subcategory']}")
        print(f"   关键词: {', '.join(analysis['keywords'][:5])}")
        
        # Step 2: 询问处理方式（外来文章）
        if source != "user" and ask_for_type:
            return {
                "need_ask": True,
                "question": f"这是一篇来自 {source} 的文章，作者: {author}。\n请选择处理方式:",
                "options": [
                    "原文收藏 - 一字不差保存到 Materials",
                    "提取要点 - 精炼核心内容到 Knowledge",
                    "跳过 - 不收录此文章"
                ],
                "analysis": analysis,
                "content": content,
                "title": title,
                "source": source,
                "author": author
            }
        
        # Step 3: 保存笔记
        print("\n[2] 格式化并保存...")
        filepath, category, subcategory = self.save_note(
            title, content, source, author
        )
        
        # Step 4: 建立 Wiki 链接
        print("\n[3] 建立 Wiki 链接...")
        self.build_wiki_links(filepath)
        
        # Step 5: 更新图谱
        print("\n[4] 更新知识图谱...")
        self.update_graph()
        
        # Step 6: 打开浏览器
        if auto_open:
            print("\n[5] 打开浏览器...")
            self.open_browser()
        
        print(f"\n{'='*50}")
        print("✅ 收录完成!")
        print(f"   文件: {filepath}")
        print(f"   分类: {category}/{subcategory}")
        print(f"{'='*50}\n")
        
        return {
            "need_ask": False,
            "filepath": filepath,
            "category": category,
            "subcategory": subcategory
        }


def main():
    parser = argparse.ArgumentParser(description='笔记自动化收录 v2.2')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--content', help='文章内容')
    parser.add_argument('--file', help='从文件读取内容')
    parser.add_argument('--source', default='user', help='来源: user/wechat/feishu/web/book')
    parser.add_argument('--author', default='', help='作者')
    parser.add_argument('--type', choices=['original', 'collected', 'extracted'], help='覆盖类型')
    parser.add_argument('--category', help='覆盖分类')
    parser.add_argument('--subcategory', help='覆盖子分类')
    parser.add_argument('--no-ask', action='store_true', help='不询问处理方式')
    parser.add_argument('--no-open', action='store_true', help='不自动打开浏览器')
    parser.add_argument('--save', action='store_true', help='直接保存')
    
    args = parser.parse_args()
    
    # 获取内容
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        print("请提供 --content 或 --file")
        sys.exit(1)
    
    # 收录
    collector = NoteCollector()
    
    if args.save:
        # 直接保存模式
        filepath, cat, subcat = collector.save_note(
            args.title, content, args.source, args.author,
            args.type, args.category, args.subcategory
        )
        collector.build_wiki_links(filepath)
        collector.update_graph()
        if not args.no_open:
            collector.open_browser()
    else:
        # 标准流程
        result = collector.collect(
            title=args.title,
            content=content,
            source=args.source,
            author=args.author,
            ask_for_type=not args.no_ask and args.source != 'user',
            auto_open=not args.no_open
        )
        
        if result.get("need_ask"):
            print("\n" + result["question"])
            for i, opt in enumerate(result["options"], 1):
                print(f"  {i}. {opt}")


if __name__ == '__main__':
    main()