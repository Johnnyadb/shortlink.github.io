# shortlink.github.io
一个简单高效的短链接生成器

## 项目简介
这个项目可以将长URL转换为短链接，便于分享和使用。它使用SHA256和Base64编码来生成唯一的短链接，并提供Web界面进行访问。

## 功能特点
- 将长URL转换为最多12字符的短链接
- 支持批量处理URL
- 保持短链接的唯一性和稳定性
- 提供Web重定向服务

## 安装说明
1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/shortlink.github.io.git
cd shortlink.github.io
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 添加新的链接
```bash
python .github/scripts/process_urls.py "你的长链接URL"
```

### 2. 批量添加多个链接
```bash
python .github/scripts/process_urls.py "链接1" "链接2" "链接3"
```

### 3. 重新生成所有短链接
清空s文件夹，并按照 _o.tsv 文件中的长链接列表重新生成所有短链接：
```bash
python .github/scripts/process_urls.py --all
```

## 文件结构
- `_o.tsv`: 存储长链接和短链接的对应关系
- `s/`: 存储所有短链接的JSON文件
- `.github/scripts/process_urls.py`: 核心处理脚本
- `index.html`, `index.redirect.html`: Web访问和重定向页面

## 注意事项
- 生成的短链接是唯一且稳定的
- 重新生成所有短链接会清空s文件夹
- 确保Python环境已正确配置

## License
MIT License