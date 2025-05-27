import json
import os
import re
import sys

# 读取JSON文件
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# 递归处理消息内容为Markdown
def parse_text(text):
    if isinstance(text, str):
        return text
    result = ''
    for item in text:
        if isinstance(item, str):
            result += item
        elif isinstance(item, dict):
            t = item.get('text', '')
            if item.get('type') == 'text_link':
                # 链接内可能还需要加粗等
                result += f'[{t}]({item.get("href", "#")})'
            elif item.get('type') == 'bold':
                result += f'**{t}**'
            elif item.get('type') == 'italic':
                result += f'*{t}*'
            else:
                result += t
    return result

def message_to_md(msg):
    md = f'#### 消息ID: {msg.get("id", "")} | {msg.get("date", "")}\n\n'
    if msg.get('from'):
        md += f'**来自**: {msg.get("from", "")}  \n'
    if msg.get('title'):
        md += f'**标题**: {msg.get("title", "")}  \n'
    if msg.get('action'):
        md += f'**动作**: {msg.get("action", "")}  \n'
    # 处理图片
    photo = msg.get('photo')
    if photo and photo != '(File not included. Change data exporting settings to download.)':
        md += f'![图片]({photo})\n\n'
    if msg.get('text'):
        content = parse_text(msg["text"])
        # 按段落分行
        for line in content.split('\n'):
            if line.strip():
                md += f'> {line.strip()}\n'
        md += '\n'
    md += '\n---\n\n'
    return md

# 生成安全的文件名
def safe_filename(title):
    # 替换非法字符为下划线
    name = re.sub(r'[\\/:*?"<>|]', '_', title)
    name = name.replace(' ', '_')
    return name + '.md'

# 读取已存在的消息ID
def get_existing_ids(md_filename):
    if not os.path.exists(md_filename):
        return set()
    ids = set()
    with open(md_filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#### 消息ID:'):
                parts = line.split()
                if len(parts) > 2:
                    try:
                        ids.add(int(parts[2]))
                    except Exception:
                        pass
    return ids

def main():
    # 支持命令行参数传入json路径
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        json_path = 'result.json'
    data = load_json(json_path)
    messages = data.get('messages', [])
    if not messages:
        print('没有消息可处理')
        return
    # 获取文件名
    title = messages[0].get('title', 'result')
    md_filename = safe_filename(title)
    # 输出到json所在目录
    out_path = os.path.join(os.path.dirname(json_path), md_filename)
    # 获取已存在的消息ID
    existing_ids = get_existing_ids(out_path)
    # 追加写入新消息
    with open(out_path, 'a', encoding='utf-8') as f:
        for msg in messages:
            msg_id = msg.get('id')
            if msg_id not in existing_ids:
                f.write(message_to_md(msg))

if __name__ == '__main__':
    main() 