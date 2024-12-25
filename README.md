# 短链接生成器

一个基于 GitHub Pages 的简单高效的短链接生成和重定向服务。

## 功能特点

- 🚀 纯静态实现，基于 GitHub Pages 托管
- 🔒 使用 SHA256 + Base64 生成安全可靠的短链接
- 📝 自动维护长短链接映射关系
- 🔍 支持批量生成和更新
- 🎯 简洁的短链接格式，无需后缀
- ⚡ 快速的重定向响应

## 工作原理

1. **短链接生成**：
   - 使用 SHA256 对长 URL 进行哈希
   - Base64 编码并提取字母数字字符
   - 生成12位的唯一短码

2. **重定向机制**：
   - 访问短链接时触发 404 页面
   - 通过 JavaScript 获取短码
   - 查找对应的 JSON 文件获取目标 URL
   - 实现自动重定向

## 使用方法

### 1. 安装依赖

```bash
pip install pandas
```

### 2. 生成短链接

```bash
# 添加单个URL
python .github/scripts/process_urls.py "https://example.com"

# 添加多个URL
python .github/scripts/process_urls.py "https://example1.com" "https://example2.com"

# 重新生成所有短链接
python .github/scripts/process_urls.py --all
```

### 3. 访问短链接

```
https://你的域名/短码
```

例如：`https://你的域名/MP4HC2TlFlL9`

## 项目结构

```
.
├── s/                  # 存储短链接JSON文件
│   └── *.json         # 短链接配置文件
├── _o.tsv             # 长短链接映射关系
├── 404.html           # 处理重定向的页面
├── index.html         # 项目主页
└── .github/scripts/   # 脚本目录
    └── process_urls.py # 短链接生成脚本
```

## 文件说明

1. **JSON 文件** (`s/*.json`)
   ```json
   {
     "l": "https://example.com"  // 目标长链接
   }
   ```

2. **映射文件** (`_o.tsv`)
   ```
   长URL    短码
   https://example.com    MP4HC2TlFlL9
   ```

## 部署说明

1. Fork 本项目到你的 GitHub 账号
2. 启用 GitHub Pages（设置为从主分支构建）
3. 克隆到本地后即可使用脚本生成短链接
4. 提交更改到 GitHub 后即可使用

## 注意事项

- 短链接一旦生成就不要修改，以保持链接的稳定性
- 定期备份 `_o.tsv` 和 `s/` 目录
- 不要删除或修改 `404.html`，它是重定向功能的核心

## 技术栈

- Python 3.x
- GitHub Pages
- JavaScript
- Pandas

## License

MIT License