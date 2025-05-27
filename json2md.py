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
def safe_filename(title, idx=None):
    name = re.sub(r'[\\/:*?"<>|]', '_', title)
    name = name.replace(' ', '_')
    if idx is not None:
        return f'{name}_{idx}.md'
    return name + '.md'

# 读取已存在的消息ID（支持分卷）
def get_existing_ids(md_filename):
    ids = set()
    if not os.path.exists(md_filename):
        return ids
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
    # 支持命令行参数传入json路径和可选分卷参数
    split = False
    json_path = 'result.json'
    for arg in sys.argv[1:]:
        if arg == '--split':
            split = True
        else:
            json_path = arg
    data = load_json(json_path)
    messages = data.get('messages', [])
    if not messages:
        print('没有消息可处理')
        return
    title = messages[0].get('title', 'result')
    out_dir = os.path.dirname(json_path)
    if split:
        max_per_file = 4000
        # 先统计所有分卷文件名
        split_files = {}
        for msg in messages:
            msg_id = msg.get('id')
            idx = msg_id // max_per_file + 1
            md_file = os.path.join(out_dir, safe_filename(title, idx))
            if md_file not in split_files:
                split_files[md_file] = set()
        # 读取每个分卷已存在的ID
        for md_file in split_files:
            split_files[md_file] = get_existing_ids(md_file)
        # 按ID分布写入对应分卷
        file_handles = {}
        try:
            for msg in messages:
                msg_id = msg.get('id')
                idx = msg_id // max_per_file + 1
                md_file = os.path.join(out_dir, safe_filename(title, idx))
                if msg_id in split_files[md_file]:
                    continue
                if md_file not in file_handles:
                    file_handles[md_file] = open(md_file, 'a', encoding='utf-8')
                file_handles[md_file].write(message_to_md(msg))
                split_files[md_file].add(msg_id)
        finally:
            for f in file_handles.values():
                f.close()
    else:
        md_filename = safe_filename(title)
        out_path = os.path.join(out_dir, md_filename)
        existing_ids = get_existing_ids(out_path)
        with open(out_path, 'a', encoding='utf-8') as f:
            for msg in messages:
                msg_id = msg.get('id')
                if msg_id not in existing_ids:
                    f.write(message_to_md(msg))

if __name__ == '__main__':
    main() 