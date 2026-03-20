# Minecraft Document MCP

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.1-green.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个基于 FastMCP 框架的 Minecraft 文档 MCP 服务器，为 AI 助手提供中文 Minecraft Wiki 文档查询功能。

## 功能特性

- **Wiki 在线查询** - 从中文 Minecraft Wiki 获取词条内容
- **分类浏览** - 获取 Wiki 首页主要分类列表
- **简介/完整内容** - 支持获取词条简介或完整内容
- **Markdown 输出** - 所有查询结果以 Markdown 格式返回
- **MCP 协议支持** - 兼容 Model Context Protocol，可集成到 Claude Desktop 等客户端

## MCP 工具

| 工具名称                  | 功能描述             |
|-----------------------|------------------|
| `search_wiki_intro`   | 从 Wiki 搜索词条简介    |
| `search_wiki_full`    | 从 Wiki 搜索词条完整内容  |
| `get_wiki_categories` | 获取 Wiki 首页主要分类列表 |

## 安装

### 环境要求

- Python 3.12+
- uv 包管理器（推荐）

### 使用 uv 安装

```bash
uv add minecraft-document-mcp
```

### 使用 pip 安装

```bash
pip install minecraft-document-mcp
```

## 使用方法

### 启动服务器

##### 使用 fastmcp 运行
```bash
fastmcp run server.py
# 开发模式（支持热重载）
fastmcp dev server.py
```

#### 使用安装后的命令行工具

```bash
# uvx 拉取
uvx minecraft-document-mcp
# minedoc 命令
uvx minecraft-document-mcp minedoc

# 配置 Claude Code
claude mcp add --transport stdio --scope user minedoc "uvx --from minecraft-document-mcp minedoc" 
```

## 项目结构

```
minecraft-document-mcp/
├── pyproject.toml               # 项目配置
└── minecraft_document_mcp/      # 主包
    ├── __init__.py
    ├── cli.py                   # MCP 服务器入口
    └── src/
        └── api/
            ├── __init__.py
            ├── WikiApi.py       # Wiki API 请求工具
            └── WikiItems.py     # 数据项定义
```

## 依赖

- [fastmcp](https://github.com/jlowin/fastmcp) - MCP 框架
- [requests](https://docs.python-requests.org/) - HTTP 请求库
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析
- [markdownify](https://github.com/matthewwithanm/python-markdownify) - HTML 转 Markdown
- [lxml](https://lxml.de/) - XML/HTML 解析后端
- [dataclasses-json](https://github.com/lidatong/dataclasses-json) - 数据类序列化

## 许可证

[MIT License](LICENSE)

## 相关链接

- [Minecraft Wiki](https://zh.minecraft.wiki/) - 中文 Minecraft Wiki
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 协议文档
- [FastMCP](https://github.com/jlowin/fastmcp) - FastMCP 框架