#!/usr/bin/env python3
"""
飞书消息导入脚本
将飞书有价值消息保存到笔记库

使用方法:
    python feishu_importer.py --token YOUR_TOKEN

配置:
    或设置环境变量 FEISHU_TOKEN

依赖:
    pip install requests
"""

import os
import sys
import json
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("⚠️ 请先安装 requests:")
    print("   pip install requests")
    sys.exit(1)


# ==================== 用户配置 ====================
FEISHU_API_TOKEN = os.environ.get('FEISHU_TOKEN', '')
SAVE_DIR = "/mnt/d/obsidian-notes/04-Materials/Feishu"
# ================================================


class FeishuImporter:
    """飞书消息导入器"""
    
    def __init__(self, token=None, save_dir=None):
        self.token = token or FEISHU_API_TOKEN
        self.save_dir = save_dir or SAVE_DIR
        self.api_base = "https://open.feishu.cn/open-api"
        
        if not self.token:
            print("⚠️ 请设置飞书 API Token!")
            print("   方法1: 设置环境变量 FEISHU_TOKEN")
            print("   方法2: 命令行传入 --token YOUR_TOKEN")
            sys.exit(1)
        
        # 确保保存目录存在
        os.makedirs(self.save_dir, exist_ok=True)
    
    def _request(self, endpoint, method='GET', data=None):
        """发送 API 请求"""
        url = f"{self.api_base}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method == 'GET':
                resp = requests.get(url, headers=headers)
            else:
                resp = requests.post(url, headers=headers, json=data)
            
            return resp.json()
        except Exception as e:
            print(f"请求错误: {e}")
            return None
    
    def get_messages(self, chat_id, limit=50):
        """获取聊天消息"""
        endpoint = f"im/v1/chats/{chat_id}/messages"
        params = {'page_size': limit}
        
        result = self._request(endpoint)
        
        if result and result.get('code') == 0:
            return result.get('data', {}).get('items', [])
        
        return []
    
    def save_message(self, message, filename=None):
        """保存消息为笔记"""
        content = message.get('content', '')
        msg_type = message.get('msg_type', 'text')
        create_time = message.get('create_time', 0)
        
        # 解析内容
        if msg_type == 'text':
            try:
                content_obj = json.loads(content)
                text = content_obj.get('text', '')
            except:
                text = content
        else:
            text = f"[{msg_type}] {content}"
        
        # 生成文件名
        if not filename:
            timestamp = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d_%H%M')
            filename = f"飞书消息_{timestamp}.md"
        
        # 生成笔记内容
        note_content = f"""---
type: collected
source: feishu
created: {datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M')}
---

# 飞书消息

{text}

---
*导入时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        
        # 保存文件
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(note_content)
        
        print(f"✅ 保存消息: {filepath}")
        return filepath
    
    def import_recent_messages(self, chat_id, limit=10):
        """导入最近的聊天消息"""
        messages = self.get_messages(chat_id, limit)
        
        if not messages:
            print("未获取到消息")
            return
        
        print(f"获取到 {len(messages)} 条消息")
        
        for msg in messages:
            # 只保存文本消息
            if msg.get('msg_type') == 'text':
                self.save_message(msg)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='飞书消息导入')
    parser.add_argument('--token', help='飞书 API Token')
    parser.add_argument('--chat', help='聊天 ID')
    parser.add_argument('--limit', type=int, default=10, help='导入消息数量')
    parser.add_argument('--save-dir', help='保存目录')
    
    args = parser.parse_args()
    
    importer = FeishuImporter(
        token=args.token,
        save_dir=args.save_dir
    )
    
    if args.chat:
        importer.import_recent_messages(args.chat, args.limit)
    else:
        print("⚠️ 请指定聊天 ID (--chat)")
        print("   使用方法: python feishu_importer.py --chat YOUR_CHAT_ID")


if __name__ == '__main__':
    main()