# 短链接服务

一个简单高效的短链接服务平台，专注于链接简化和快速重定向。

## 功能特点

- **即时响应**: 毫秒级重定向，无等待时间
- **安全可靠**: 内置隐私保护，不记录访问信息
- **简单高效**: 直接访问短码即可跳转
- **兼容性强**: 支持各种客户端访问（浏览器、curl等）
- **响应式设计**: 完美适配移动端和桌面端

## 技术实现

- 纯静态实现，基于 GitHub Pages 托管
- 使用 JSON 文件存储链接映射
- 支持 HTML5 和 JavaScript 重定向
- 针对性能优化，文件体积极小
- 完善的错误处理和容错机制

## 目录结构

```
.
├── index.html          # 首页
├── 404.html           # 404页面（处理重定向）
├── s/                 # 短链接JSON文件目录
│   └── *.json        # 短链接配置文件
└── .github/          # GitHub相关配置
    └── scripts/      # 自动化脚本
```

## 使用方法

1. **访问短链接**:
   - 格式：`https://你的域名/:shortcode`
   - 示例：`https://你的域名/C8myuP83hXZO`

2. **JSON文件格式**:
   ```json
   {
       "l": "https://目标网址"
   }
   ```

3. **自动化部署**:
   - 将JSON文件放入 `s` 目录
   - 自动生成对应的重定向页面

## 配置说明

支持通过 `config.json` 或命令行参数进行配置：

```json
{
    "json_dir": "s",           // JSON文件目录
    "log_level": "INFO",       // 日志级别
    "verify_urls": true,       // 是否验证URL
    "require_https": true,     // 是否要求HTTPS
    "show_progress": true      // 是否显示进度
}
```

命令行参数：
```bash
python generate_redirects.py [选项]

选项：
  --config FILE      配置文件路径
  --json-dir DIR     JSON文件目录
  --log-level LEVEL  日志级别 (DEBUG/INFO/WARNING/ERROR)
  --no-verify       禁用URL验证
  --no-progress     禁用进度显示
```

## 性能优化

- 使用压缩的HTML和JavaScript代码
- 实现双重重定向机制（meta refresh + JavaScript）
- 采用异步加载和错误处理
- 优化的文件结构和缓存策略

## 注意事项

1. 建议使用HTTPS链接以确保安全
2. 短码长度固定为12位字符
3. 支持同时使用多种重定向方式
4. 自动处理URL编码和解码
5. 内置防循环重定向保护

## 开发说明

1. **本地测试**:
   ```bash
   python -m http.server 8000
   ```

2. **生成重定向页面**:
   ```bash
   python .github/scripts/generate_redirects.py
   ```

3. **备份和恢复**:
   - 重要文件已包含 .bak 备份
   - 定期同步到远程仓库

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目。在提交代码前，请确保：

1. 代码风格符合规范
2. 添加了必要的注释
3. 更新了相关文档
4. 测试了所有功能

## 许可证

MIT License