# Telegram JSON2MD 📨📦

[![GitHub stars](https://img.shields.io/github/stars/Liu8Can/telegram-json2md?style=flat-square)](https://github.com/Liu8Can/telegram-json2md/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Liu8Can/telegram-json2md?style=flat-square)](https://github.com/Liu8Can/telegram-json2md/network)
[![GitHub issues](https://img.shields.io/github/issues/Liu8Can/telegram-json2md?style=flat-square)](https://github.com/Liu8Can/telegram-json2md/issues)
[![MIT License](https://img.shields.io/github/license/Liu8Can/telegram-json2md?style=flat-square)](LICENSE)

---

## 📝 项目简介

本工具可将 Telegram 频道导出的 `result.json` 聊天记录批量转换为美观的 Markdown 文件，便于归档、阅读和后续处理。

✨ **主要特性**
- 自动以频道标题命名 Markdown 文件（如 `gogo科技_资源收藏（重生）.md`）
- 支持增量追加：只会追加新消息，避免重复
- 自动处理图片、贴纸（静态/动态贴纸会有提示）
- 输出文件与 `result.json` 保持在同一目录
- 纯 Python 实现，零依赖，跨平台

---

## 🚀 快速开始

1. **克隆仓库**

```bash
git clone https://github.com/Liu8Can/telegram-json2md.git
cd telegram-json2md
```

2. **将 `json2md.py` 脚本放在任意你喜欢的位置**

3. **用命令行进入你要处理的频道导出文件夹（即 `result.json` 所在目录）**

4. **执行如下命令**

```bash
python "D:\Download\Telegram Desktop\ChatExport_2025-05-26 (5)\json2md.py" result.json
```

- 你也可以在任意目录下指定 `result.json` 的完整路径：

```bash
python 路径/json2md.py 路径/某频道/result.json
```

5. **脚本会自动在 `result.json` 同目录下生成以频道标题命名的 Markdown 文件**

---

## 🛠️ 本地常用命令

- 克隆仓库：
  ```bash
  git clone https://github.com/Liu8Can/telegram-json2md.git
  ```
- 进入目录：
  ```bash
  cd telegram-json2md
  ```
- 运行脚本（示例）：
  ```bash
  python 路径/json2md.py 路径/某频道/result.json
  ```
- 查看/编辑生成的 Markdown 文件：
  ```bash
  code 路径/某频道/频道名.md  # VSCode
  notepad 路径/某频道/频道名.md  # 记事本
  ```

---

## ⚠️ 注意事项

- 只支持 Telegram 官方导出的 JSON 格式。
- 如果 `result.json` 更新，脚本会自动增量追加新消息。
- 若有广告或无用内容，建议后期用文本编辑器批量删除。
- 文件名会自动去除特殊字符，空格会变为下划线。
- 静态贴纸、图片会自动插入，动态贴纸（.tgs）会有文本提示。

---

## 💡 批量处理建议

如需批量处理多个频道，可结合批处理脚本或 Python 脚本遍历所有子文件夹，自动调用本工具。

---

## 📬 联系与反馈

如有更多需求或问题，欢迎在 [Issues](https://github.com/Liu8Can/telegram-json2md/issues) 区留言！

---

> Made with ❤️ by [Liu8Can](https://github.com/Liu8Can) 